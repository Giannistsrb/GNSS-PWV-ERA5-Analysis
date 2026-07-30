"""
analysis.py
===========

Analysis utilities used throughout the project.

This module contains routines for

    • statistical analysis,
    • comparison metrics,
    • validation,
    • derived atmospheric products.

Author
------
Ioannis Tsormpatzoglou
"""

__author__ = "Ioannis Tsormpatzoglou"
__version__ = "3.0"

import pandas as pd
from src.data_loading import extract_era5_data
from src.physics import *
from src.config import *

def compute_pwv_era5(ds):

    time = pd.to_datetime(ds["valid_time"].values, utc = True)

    pressure_levels = ds["pressure_level"].values.squeeze()

    p_surface = ds["sp"].values.squeeze()
    q         = ds["q"].values.squeeze()
    pwv_era5  = PWV_From_Integration(q, pressure_levels * 100)
    t2m       = ds["t2m"].values.squeeze()
    d2m       = ds["d2m"].values.squeeze()
    cape      = ds["cape"].values.squeeze()


    Tm  = ZhangModelWeightedAverageTemperature(t2m)
    WVF = WATER_VAPOR_FACTOR(Tm)

    zwd_era5 = pwv_era5 / WVF
    zhd_era5 = ZHD(p_surface / 100, LATITUDE, SENSOR_HEIGHT)
    ztd_era5 = zwd_era5 + zhd_era5
    df = pd.concat([pd.DataFrame(ztd_era5,  index = time, columns = ["ZTD_ERA5_m"]),
                    pd.DataFrame(zhd_era5,  index = time, columns = ["ZHD_ERA5_m"]),
                    pd.DataFrame(zwd_era5,  index = time, columns = ["ZWD_ERA5_m"]),
                    pd.DataFrame(pwv_era5,  index = time, columns = ["PWV_ERA5_mm"]),
                    pd.DataFrame(cape,      index = time, columns = ["CAPE_ERA5_J_kg"]), 
                    pd.DataFrame(p_surface, index = time, columns = ["P_surface_ERA5_Pa"]),
                    pd.DataFrame(d2m,       index = time, columns = ["Dewpoint 2m_ERA5_K"]),
                    pd.DataFrame(t2m,       index = time, columns = ["Temp_surface_ERA5_K"]), 
                    pd.DataFrame(Tm,        index = time, columns = ["Tm_ERA5_K"]), 
                    pd.DataFrame(WVF,       index = time, columns = ["WVF_ERA5"])], axis = 1)
                    

    return df

def compute_pwv_sensor(df_gnss, df_sensor):

    # ===== RAW GNSS:
    ztd_sens_raw = df_gnss.dropna()

    # ===== HOURLY:
    T_sens_h     = df_sensor["temp_sens_K"].resample("1h").mean()
    p_sens_hpa_h = df_sensor["p_sens_hpa"].resample("1h").mean()
    q_sens_h     = df_sensor["hum_sens_kg/kg"].resample("1h").mean()
    RH_sens      = df_sensor["hum_sens_percent"].resample("1h").mean()

    Tm  = ZhangModelWeightedAverageTemperature(T_sens_h)
    WVF = WATER_VAPOR_FACTOR(Tm)
    
    ztd_sens_h = ztd_sens_raw.resample("1h").mean().rolling(window=8, center=True, min_periods=1).mean()
    zhd_sens_h = ZHD(p_sens_hpa_h, LATITUDE, SENSOR_HEIGHT)
    zwd_sens_h = ztd_sens_h["ZTD_m"] - zhd_sens_h
    pwv_sens_h = zwd_sens_h * WVF

    df_sensor_h   = pd.concat([ztd_sens_h.rename(columns = {'ZTD_m': 'ZTD_sensor_m'}), 
                               zhd_sens_h.rename("ZHD_sensor_m"), 
                               zwd_sens_h.rename("ZWD_sensor_m"), 
                               pwv_sens_h.rename("PWV_sensor_mm"), 
                               T_sens_h.rename("Temp_sensor_K"),
                               p_sens_hpa_h.rename("P_sensor_hPa"),
                               q_sens_h.rename("q_sens_kg_kg"),
                               RH_sens.rename("RH_sensor_%"), 
                               Tm.rename("Tm_sensor_K"),
                               WVF.rename("WVF_sensor")], axis = 1)
    
    return ztd_sens_raw, df_sensor_h

def compute_cape(ds):

    time = pd.to_datetime(ds["valid_time"].values, utc = True)

    P_profile  = ds["pressure_level"].values.squeeze() * 100.0
    T_profile  = ds["t"].values.squeeze()
    Td_surface = ds["d2m"].values.squeeze()
    T_surface  = ds["t2m"].values.squeeze()
    P_surface  = ds["sp"].values.squeeze()
    q_profile  = ds["q"].values.squeeze()
    
    cape = np.zeros(len(time))

    for t in range(len(time)):

        P = P_profile[P_profile < P_surface[t]]
        P = np.insert(P, 0, P_surface[t])

        T = T_profile[t][P_profile < P_surface[t]]
        T = np.insert(T, 0, T_surface[t])

        q         = q_profile[t][P_profile < P_surface[t]]
        q_surface = humidity_from_dewpoint(Td_surface[t], P_surface[t])
        q         = np.insert(q, 0, q_surface)

        cape[t] = CAPE_calculation(T,
                                   Td_surface[t],
                                   T_surface[t],
                                   P,
                                   P_surface[t],
                                   q)
          
    cape = pd.DataFrame(cape, index = time, columns = ["CAPE_J_kg"])

    return cape

def compute_metpy_cape(ds):

    time = pd.to_datetime(ds["valid_time"].values, utc=True)

    P_levels   = ds["pressure_level"].values.squeeze() * 100  # hPa -> Pa

    T_profile  = ds["t"].values.squeeze()       # K
    q_profile  = ds["q"].values.squeeze()       # kg/kg

    P_surface  = ds["sp"].values.squeeze()      # Pa
    T_surface  = ds["t2m"].values.squeeze()     # K
    Td_surface = ds["d2m"].values.squeeze()     # K

    cape_values = []

    for i in range(len(time)):

        # Keep only pressure levels above the surface
        mask = P_levels < P_surface[i]

        P  = P_levels[mask]
        T  = T_profile[i][mask]
        q  = q_profile[i][mask]

        # Dewpoint profile from specific humidity
        Td = dewpoint_from_q(T, q, P)

        # Insert surface point
        P  = np.insert(P,   0, P_surface[i])
        T  = np.insert(T,   0, T_surface[i])
        Td = np.insert(Td, 0, Td_surface[i])

        # Sort pressure levels from high to low pressure
        idx = np.argsort(P)[::-1]

        P  = P[idx]
        T  = T[idx]
        Td = Td[idx]

        # CAPE calculation using MetPy
        cape = metpy_cape(P, T, Td)

        cape_values.append(cape)

    return pd.DataFrame(cape_values, index=time, columns=["CAPE_MetPy_J_kg"])

def save_statistics_csv(stats, filename):

    from src.paths import TABLES_DIR

    save_path = TABLES_DIR / filename

    stats.to_csv(save_path)

    print(f"Saved statistics -> {save_path}")

def bias_correction(df, reference_col, model_col):

    bias = (df[model_col] - df[reference_col]).mean()

    corrected = df[model_col] - bias

    df[f"{model_col}_corrected"] = corrected

    print("\nBias correction: ")
    print(f"Original bias: {bias:.3f} mm")

    return df










