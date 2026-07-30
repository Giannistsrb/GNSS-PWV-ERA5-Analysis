"""
physics.py
==========

Physical and meteorological calculations for the
GNSS-PWV-ERA5 Analysis project.

This module contains the mathematical formulations required for:

    - GNSS atmospheric delay estimation
    - Zenith Hydrostatic Delay (ZHD)
    - Zenith Wet Delay (ZWD)
    - Precipitable Water Vapour (PWV)
    - Weighted Mean Atmospheric Temperature (Tm)
    - Water Vapour Factor (WVF)
    - Humidity transformations
    - Atmospheric stability calculations
    - Convective Available Potential Energy (CAPE)

The implemented methods combine GNSS meteorology theory with
ERA5 atmospheric reanalysis data.

Main physical applications:

    GNSS:
        ZTD -> ZHD + ZWD -> PWV

    Atmospheric thermodynamics:
        Temperature / humidity profiles -> CAPE


Author
------
Ioannis Tsormpatzoglou

Project
-------
GNSS-PWV-ERA5 Analysis

Version
-------
3.0
"""

__author__ = "Ioannis Tsormpatzoglou"
__version__ = "3.0"


# ==============================================================
# External Libraries
# ==============================================================

import math as m

import metpy.calc as mpcalc
import numpy as np

from metpy.units import units

# ==============================================================
# Project Constants
# ==============================================================

from src.constants import (
    GRAVITY,
    LIQUID_WATER_DENSITY,
    GAS_CONSTANT_OF_WATER_VAPOR,
    K3_CONSTANT,
    DRY_AIR_GAS_CONSTANT
)


                                # ============================================= #
                                # ================ PWV PHYSICS ================ #
                                # ============================================= #

def ZHD(p_surface_hPa, lat_phi, h_sens):
    zhd_m = 0.0022768 * p_surface_hPa / (
        1 - 0.00266 * np.cos(2 * m.pi * lat_phi / 180)
        - 0.00028 * h_sens)
    return zhd_m

# Convert temperature in z m above ground to ground temperature for small z:
def tzm_to_surface(tzm, z_km):
    DALR = 9.8 # C / km Dry adiabatic lapse rate
    return tzm + DALR * z_km
    
def ZhangModelWeightedAverageTemperature(T_ground_K):
    return 0.72 * T_ground_K + 70.20

def WATER_VAPOR_FACTOR(Tm):
    return LIQUID_WATER_DENSITY * GAS_CONSTANT_OF_WATER_VAPOR / (
        DRY_AIR_GAS_CONSTANT + K3_CONSTANT / Tm)

def PWV_From_Integration(q, p):
    # q: specific humidity in kg/kg
    # p: pressure levels in Pa
    q_mid = (q[:, :-1] + q[:, 1:]) / 2
    return 1 / GRAVITY * np.sum(q_mid * np.abs(np.diff(p)), axis=1) 

def ZWD_From_PWV_Retrieval(Π, PWV):
    return Π * PWV

# Get the relative humidity from dewpoint and temperature in a specific level:
def RelativeHumidityFromDewpoint(T_K, Tdp_K):
    Tc = T_K - 273.15
    Td = Tdp_K - 273.15
    return 1E+2 * np.exp(17.67 * Td / (Td + 243.5) - 17.67 * Tc / (Tc + 243.5))

#Relative humidity to specific humidity conversion:
def Relative_to_specific_humidity(RH, T_C, p):
    e_s = 6.112 * np.exp((17.67 * T_C) / (T_C + 243.5)) # Saturation vapor pressure (Magnus formula)
    e = RH * e_s # Actual Vapor Pressure 
    q = 0.622 * e / (p - 0.378 * e) # Specific Humidity (p: Pascal)
    return q 

                                # ============================================= #
                                # ============== CAPE PHYSICS ================= #
                                # ============================================= #

# Saturation specific humidity (Moist adiabatic region):
def saturation_specific_humidity(T, P):
    # Conversion from K to C:
    Tc = T - 273.15 
    # Saturation vapor pressure (Magnus) [hPa]
    es = 6.112 * np.exp(17.67 * Tc / (Tc + 243.5))
    # Conversion from hPa to Pa:
    es *= 100.0
    
    # Saturation specific humidity:
    qs = 0.622 * es / (P - 0.378 *  es)

    return qs

# Saturation mixing ratio:
def saturation_mixing_ratio(T,P):
    Tc = T - 273.15 
    es = 6.112 * np.exp(17.67 * Tc / (Tc + 243.5))
    es *= 100.0 # hPa->Pa
    r = 0.622 * es / (P - es)
    return r

# Actual humidity of air parcel/environment:
def humidity_from_dewpoint(Td, P):
    # Conversion from K to C:
    Tdc = Td - 273.15 
    # Saturation vapor pressure (Magnus) [hPa]
    es = 6.112 * np.exp(17.67 * Tdc / (Tdc + 243.5))
    # Conversion from hPa to Pa:
    es *= 100.0
    
    # Saturation specific humidity:
    q = 0.622 * es / (P - 0.378 *  es)

    return q

# Updraft parcel temperature:
def parcel_temperature_profile(Td_surface, T_surface, P_profile, P_surface):

    Rd, Rv = 287, 461
    Cp = 1004
    Lv = 2.501e6

    # ==========================================================
    # Create dense pressure grid (1 hPa step)
    # ==========================================================
    P_dense = np.arange(P_surface, P_profile[-1] - 100, -100.0)
    T_dense = np.zeros_like(P_dense)
    q_dense = np.zeros_like(P_dense)

    # ==========================================================
    # Bolton LCL
    # ==========================================================
    T_LCL = (1 / (1 / (Td_surface - 56) + np.log(T_surface / Td_surface) / 800) + 56)
    P_LCL = P_surface * (T_LCL / T_surface) ** (Cp / Rd)

    # Surface humidity
    q_surface = humidity_from_dewpoint(Td_surface, P_surface)

    # ==========================================================
    # Parcel ascent
    # ==========================================================
    for i, P in enumerate(P_dense):

        if i == 0:

            T_dense[i] = T_surface
            q_dense[i] = q_surface

            continue

        T_prev = T_dense[i-1]

        # -----------------------------
        # Dry adiabatic
        # -----------------------------
        if P > P_LCL:

            T_dense[i] = (T_surface * (P / P_surface) ** (Rd / Cp))
            q_dense[i] = q_surface

        # -----------------------------
        # Moist adiabatic lapse rate:
        # -----------------------------
        else:

            r = saturation_mixing_ratio(T_prev, P)

            numerator = (1 + Lv * r / (Rd * T_prev))
            denominator = (1 + (Lv**2 * r) / (Cp * Rv * T_prev**2))

            dTdP = (Rd * T_prev /(Cp * P) * numerator / denominator)
            dP   = P - P_dense[i-1]

            T_dense[i] = (T_prev + dTdP * dP) 

            r_new = saturation_mixing_ratio(T_dense[i], P)

            q_dense[i] = r_new / (1+r_new) 

    # ==========================================================
    # Interpolate back to ERA5 pressure levels:
    # ==========================================================

    T_interp = np.interp(P_profile, P_dense[::-1], T_dense[::-1])
    q_interp = np.interp(P_profile, P_dense[::-1], q_dense[::-1])

    return T_interp, q_interp

# Virtual Temperature:
def virtual_temperature(T, q):
    Rd, Rv = 287, 461  # J/(kg * K)
    r = q / (1 - q)    # mixing ratio (mass of wet / mass of dry)
    epsilon = Rd / Rv  # ratio of gas constants (dry / wet)
    
    T_virtual = T * (1 + r / epsilon) / (1 + r)

    return T_virtual

# Buoyancy acceleration (B) of air parcel:
def Buoyancy(Tv_e, Tv_p):
    g = GRAVITY

    B = g * (Tv_p - Tv_e) / Tv_e

    return B

# Integrate Positives Buoyancies to find CAPE:
def CAPE(Buoyancy, P_profile, Tv_environment):

    Rd = 287
    g = GRAVITY

    B_positive = np.maximum(Buoyancy,0)

    dz_dp = - Rd * Tv_environment / (g * P_profile)

    cape = np.trapezoid(B_positive * dz_dp, P_profile)

    return cape

def CAPE_calculation(T_profile, Td_surface, T_surface, P_profile, P_surface, q_profile):

    # Virtual Temperature of the parcel:
    T_p, q_p  = parcel_temperature_profile(Td_surface, T_surface, P_profile, P_surface)
    Tv_p      = virtual_temperature(T_p, q_p)
    
    # Virtual Temperature of the environment:
    T_e  = T_profile
    Tv_e = virtual_temperature(T_e, q_profile)

    B = Buoyancy(Tv_e, Tv_p)
    
    cape = CAPE(B, P_profile, Tv_e)

    return cape

# Dewpoint temperature from specific humidity:
def dewpoint_from_q(T, q, P):

    e = 0.622
    w = q / (1 - q)
    e = (w * P) / (e + w)

    e_hPa = e / 100.0

    a = 17.625
    b = 243.04

    gamma = np.log(e_hPa / 6.1094)

    Td_C = b * gamma / (a - gamma)

    Td_K = Td_C + 273.15

    return Td_K

# Cape calculation:
def metpy_cape(P, T, Td):

    pressure    =  P * units.pascal 
    temperature =  T * units.kelvin
    dewpoint    = Td * units.kelvin 

    idx = np.argsort(pressure)[::-1]

    pressure    = pressure[idx]
    temperature = temperature[idx]
    dewpoint    = dewpoint[idx]

    cape, cin = mpcalc.surface_based_cape_cin(pressure, temperature, dewpoint)

    return cape.to("J/kg").magnitude