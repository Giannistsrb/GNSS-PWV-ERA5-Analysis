"""
config.py
=========

Central configuration file for the GNSS-PWV-ERA5 Analysis project.

This module contains all user-defined parameters required for the
processing pipeline, including:

    - Measurement period
    - Station coordinates
    - Sensor height
    - ERA5 pressure levels
    - ERA5 spatial grid
    - User options for data availability and API retrieval

All project settings should be modified from this file.

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
# Project Configuration
# ==============================================================

CONFIG = {

    # Measurement period
    "YEAR": "2025",
    "MONTH": "12",

    # Measurement days
    "DAYS": [
        "21",
        "22",
        "23",
        "24"
    ],

    # GNSS station coordinates
    "LATITUDE": 41.5858688,
    "LONGITUDE": 12.6779392,

    # ERA5 spatial resolution request
    "GRID_STEP": 0.10,

    # GNSS antenna / sensor height above mean sea level (m)
    "SENSOR_HEIGHT": 58,

    # ERA5 pressure levels used for PWV integration
    "PRESSURE_LEVELS": [
        str(p)
        for p in range(1000, 500, -100)
    ]
}


# ==============================================================
# User Options
# ==============================================================

SENSORDATAEXISTS = (
    input(
        "DO YOU HAVE SENSOR DATA FOR THESE DAYS (Yes/No)? "
    )
    .strip()
    .lower()
    == "yes"
)


CALLFORDATA = (
    input(
        "DO YOU WANT TO CALL FOR API DATA FROM ERA5 (Yes/No)? "
    )
    .strip()
    .lower()
    == "yes"
)


# ==============================================================
# Derived Parameters
# ==============================================================

YEAR = CONFIG["YEAR"]
MONTH = CONFIG["MONTH"]
DAYS = CONFIG["DAYS"]

LATITUDE = CONFIG["LATITUDE"]
LONGITUDE = CONFIG["LONGITUDE"]

GRID_STEP = CONFIG["GRID_STEP"]

SENSOR_HEIGHT = CONFIG["SENSOR_HEIGHT"]

PRESSURE_LEVELS = CONFIG["PRESSURE_LEVELS"]


# ==============================================================
# ERA5 Request Parameters
# ==============================================================

HOURLY_TIME = [
    f"{hour:02d}:00"
    for hour in range(24)
]


# ERA5 bounding box:
#
# North
# West
# South
# East

NORTH = LATITUDE + GRID_STEP
WEST = LONGITUDE - GRID_STEP
SOUTH = LATITUDE - GRID_STEP
EAST = LONGITUDE + GRID_STEP


AREA = [
    NORTH,
    WEST,
    SOUTH,
    EAST
]


# ==============================================================
# Configuration Information
# ==============================================================

print("================ Coordinates =================")
print(f"Latitude : {LATITUDE}")
print(f"Longitude: {LONGITUDE}")
print(f"Height   : {SENSOR_HEIGHT} m")

print("\nERA5 Area:")
print("N:", NORTH)
print("W:", WEST)
print("S:", SOUTH)
print("E:", EAST)