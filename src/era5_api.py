"""
era5_api.py
===========

Download utilities for ERA5 reanalysis data.

This module communicates with the Copernicus Climate Data Store (CDS)
API and retrieves:

    • Pressure-level variables
    • Single-level variables

The downloaded NetCDF files are stored locally for later processing.

Author
------
Ioannis Tsormpatzoglou
"""

__author__ = "Ioannis Tsormpatzoglou"
__version__ = "3.0"

import cdsapi
from src.paths import *
from src.config import PRESSURE_LEVELS

def era5_api_call(DAY, YEAR, MONTH, HOURLY_TIME, AREA, CALLFORDATA):

    if not CALLFORDATA: 
        return None

    DATE_TAG = f"{DAY}{MONTH}{YEAR}" 

    era5_pressure_levels_file = ERA5_DIR / f"era5_pressure_levels_{DATE_TAG}.nc"
    era5_single_file          = ERA5_DIR / f"era5_single_{DATE_TAG}.nc"

    c = cdsapi.Client()

    c.retrieve(
        "reanalysis-era5-pressure-levels",
        {
             "product_type": "reanalysis",
             "variable": ["specific_humidity", 
                          "temperature"],
             "pressure_level": PRESSURE_LEVELS,
             "year": YEAR,
             "month": MONTH,
             "day": DAY,
             "time": HOURLY_TIME,
             "area": AREA,
             "format": "netcdf"
         },

         era5_pressure_levels_file
    )

    c.retrieve(
        "reanalysis-era5-single-levels",
        {
            "product_type": "reanalysis",
            "variable": ["surface_pressure", 
                         "2m_temperature", 
                         '2m_dewpoint_temperature', 
                         "convective_available_potential_energy",],
            "year": YEAR,
            "month": MONTH,
            "day": DAY,
            "time": HOURLY_TIME,
            "area": AREA,
            "format": "netcdf"
        },

        era5_single_file
    )
        
    return {"era5_pressure_levels_file": era5_pressure_levels_file,
            "era5_single_file": era5_single_file}