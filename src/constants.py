"""
constants.py
============

Physical and meteorological constants used in the
GNSS-PWV-ERA5 Analysis project.

This module contains constants required for:

    - Atmospheric thermodynamics
    - Water vapour calculations
    - GNSS meteorology
    - CAPE calculations

Keeping all physical constants in a separate module improves
readability and avoids hard-coded values throughout the project.

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
# Fundamental Physical Constants
# ==============================================================

# Acceleration due to gravity
# Units: m s^-2
GRAVITY = 9.80665


# Density of liquid water
# Units: kg m^-3
LIQUID_WATER_DENSITY = 1E3


# Density of air
# Units: kg m^-3
AIR_DENSITY = 1.20



# ==============================================================
# Gas Constants
# ==============================================================

# Specific gas constant of water vapour
# Units: J kg^-1 K^-1
GAS_CONSTANT_OF_WATER_VAPOR = 461.51


# Dry air gas constant term used in refractivity equations
DRY_AIR_GAS_CONSTANT = 22.1



# ==============================================================
# GNSS Atmospheric Delay Constants
# ==============================================================

# Refractivity constant related to wet delay
# Used in water vapour factor calculation
K3_CONSTANT = 3.739E5



# ==============================================================
# Atmospheric Thermodynamics
# ==============================================================

# Dry adiabatic lapse rate
# Units: K m^-1
DRY_ADIABATIC_LAPSE_RATE = 6.5E-3