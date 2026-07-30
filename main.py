"""
main.py
=======

Main entry point of the GNSS-PWV-ERA5 Analysis project.

This script orchestrates the complete processing workflow:

    1. Optionally downloads ERA5 reanalysis data from the Copernicus CDS API.
    2. Loads GNSS observations and weather sensor measurements.
    3. Computes atmospheric quantities from ERA5.
    4. Retrieves PWV from GNSS-derived Zenith Total Delay.
    5. Computes Convective Available Potential Energy (CAPE).
    6. Compares GNSS observations against ERA5.
    7. Produces figures and processed datasets.

The processing is performed independently for each measurement day.

Author
------
Ioannis Tsormpatzoglou

Project
-------
GNSS-PWV-ERA5 Analysis
"""

__author__ = "Ioannis Tsormpatzoglou"
__version__ = "3.0"

from src.config import CONFIG, SENSORDATAEXISTS, CALLFORDATA, HOURLY_TIME, AREA
from src.era5_api import era5_api_call
from src.pipeline import run
from src.plotting import *
from src.analysis import *
from src.data_loading import *

df_all_days = []

if __name__ == "__main__":
    
    for DAY in CONFIG["DAYS"]:

        era5_files = None 


        if CALLFORDATA:
            era5_files = era5_api_call(DAY,
                                       CONFIG["YEAR"],
                                       CONFIG["MONTH"],
                                       HOURLY_TIME,
                                       AREA,
                                       CALLFORDATA)
        
        print(f"\n================ RUNNING DAY: {DAY}-{CONFIG['MONTH']}-{CONFIG['YEAR']} ================\n")

        if SENSORDATAEXISTS:
            df_era5, df_sens_raw, df_sensor_h, df_era5_sensor = run(DAY, CONFIG, era5_files)
            df_all_days.append(df_era5_sensor)
        else:
            df_era5 = run(DAY, CONFIG, era5_files)

    df_all_days = pd.concat(df_all_days)
    plot_pwv_scatter_all_days(df_all_days, "PWV_sensor_mm", "PWV_ERA5_mm")




    

        

        


    
    

