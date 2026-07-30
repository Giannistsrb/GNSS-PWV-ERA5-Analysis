"""
pipeline.py
===========

Main processing pipeline for the GNSS-PWV-ERA5 Analysis project.

This module coordinates the complete workflow for a single
measurement day.

Workflow
--------
GNSS observations
        │
Weather sensor measurements
        │
ERA5 reanalysis
        │
        ▼
Atmospheric calculations
        │
        ▼
PWV retrieval
        │
        ▼
CAPE estimation
        │
        ▼
ERA5 vs Sensor comparison
        │
        ▼
Figures and processed datasets

Author
------
Ioannis Tsormpatzoglou
"""

__author__ = "Ioannis Tsormpatzoglou"
__version__ = "3.0"

from src.physics import *
from src.data_loading import *
from src.constants import *
from src.paths import *
from src.config import *
from src.analysis import *
from src.plotting import *

def run(DAY, config, era5_files):

    DATE_TAG = f"{DAY}{config['MONTH']}{config['YEAR']}"
    
    sensor_csv   = DATA_SENSOR_DIR / "csv_files" / f"{DATE_TAG}_data.csv"
    df_gnss_log  = DATA_SENSOR_DIR / "log_files" / f"{DATE_TAG}_gnss.log"

    df_gnss    = load_gnss_data(df_gnss_log, YEAR, MONTH, DAY)
    csv_sensor = load_sensor_data(sensor_csv)   
    df_sensor  = extract_sensor_data(csv_sensor)

    if era5_files is not None:
        era5_pressure_levels_file = era5_files["era5_pressure_levels_file"]
        era5_single_file = era5_files["era5_single_file"]
    
    else:
        era5_pressure_levels_file = ERA5_DIR / f"era5_pressure_levels_{DATE_TAG}.nc"
        era5_single_file = ERA5_DIR / f"era5_single_{DATE_TAG}.nc"
    
   
    ds_era5 = extract_era5_data(era5_pressure_levels_file, 
                                era5_single_file, "xarray")
        
    df_era5    = compute_pwv_era5(ds_era5)
    cape       = compute_cape(ds_era5)
    cape_metpy = compute_metpy_cape(ds_era5)
    df_era5 = df_era5.join(cape, how = 'inner')
    df_era5 = df_era5.join(cape_metpy, how = 'inner')
    print(df_era5)


    if SENSORDATAEXISTS: 
        df_sens_raw, df_sensor_h   = compute_pwv_sensor(df_gnss, df_sensor)
        df_era5_sensor             = df_era5.join(df_sensor_h, how = 'inner')
        FourierTransform(df_sens_raw, "ZTD_m", "12:00", "22:00", YEAR, MONTH, DAY)
        era5_sensor_comparison_subplots(df_sens_raw, df_era5, df_era5_sensor)
        return df_era5, df_sens_raw, df_sensor_h, df_era5_sensor
    
    return df_era5




