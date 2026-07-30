"""
data_loading.py
===============

Functions for loading and preprocessing all project datasets.

Supported data sources
----------------------

• GNSS log files
• Weather sensor measurements
• ERA5 NetCDF datasets

The module also includes utilities for

    - extracting meteorological variables,
    - converting timestamps,
    - computing hourly averages,
    - Fourier analysis of GNSS observations.

Author
------
Ioannis Tsormpatzoglou
"""

__author__ = "Ioannis Tsormpatzoglou"
__version__ = "3.0"

import datetime
import re
from datetime import timedelta, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import netCDF4
import numpy as np
import pandas as pd
import xarray as xr
from scipy.fft import fft, fftfreq

from src.config import *
from src.physics import Relative_to_specific_humidity


def load_gnss_data(log_file, YEAR, MONTH, DAY):

    TIMESTAMPS_sec = []
    ZTD_SENSOR = []

    if not Path(log_file).exists():
        return pd.DataFrame({"ZTD_m": []}, index=pd.DatetimeIndex([], name="timestamp_utc"))

    pattern = re.compile(r"#TROPINFOA.*;SAASTAMOINEN,([\d.e+-]+)")
    gnzda_pattern = re.compile(r"\$GNZDA,(\d+\.\d+),(\d+),(\d+),(\d+)")

    base_time = None

    with open(log_file, "r") as f:
        for line in f:

            if "$GNZDA" in line:
                m = gnzda_pattern.search(line)
                if m and base_time is None:
                    hhmmss = m.group(1)
                    hours = int(hhmmss[0:2])
                    minutes = int(hhmmss[2:4])
                    seconds = int(hhmmss[4:6])

                    base_time = datetime.datetime(
                        int(m.group(4)), int(m.group(3)), int(m.group(2)),
                        hours, minutes, seconds,
                        tzinfo=timezone.utc
                    )

            if line.startswith("#TROPINFOA"):
                match = pattern.search(line)
                if match:
                    #if 2.360 <= float(match.group(1)) <= 2.420:
                        ZTD_SENSOR.append(float(match.group(1)))

                        time_field = int(line.split(",")[5])
                        TIMESTAMPS_sec.append(time_field)

    if base_time is None:
        base_time = datetime.datetime(YEAR, MONTH, DAY, tzinfo=timezone.utc)

    t0 = TIMESTAMPS_sec[0]
    TIMESTAMPS_UTC = [base_time + timedelta(milliseconds=(t - t0)) for t in TIMESTAMPS_sec]
    
    return pd.DataFrame({"ZTD_m": pd.Series(ZTD_SENSOR).rolling(3, center=True).median().values}, index=TIMESTAMPS_UTC)

def load_sensor_data(sensor_csv):

    cols = ["humidity_percent", "temperature_c", "pressure_hpa"]

    if not Path(sensor_csv).exists():
        df_sensor   = pd.DataFrame(columns=cols)
    else:
        df_sensor   = pd.read_csv(sensor_csv, parse_dates=["timestamp_utc"], on_bad_lines="skip")
        df_sensor   = df_sensor.set_index("timestamp_utc")

    return df_sensor

def extract_sensor_data(df):
    
    cols = ["p_sens_hpa",
            "temp_sens_C",
            "temp_sens_K",
            "hum_sens_kg/kg",
            "hum_sens_percent"]

    if df is None or df.empty:
        print("No sensor data -> running ERA5 only mode")
        df.index = pd.to_datetime(df.index, utc=True)
        return pd.DataFrame(columns=cols, index=pd.DatetimeIndex([], name="timestamp_utc"))
    
    df = df.copy()
    df.index = pd.to_datetime(df.index, utc=True)

    # Extract variables: 
    relative_humidity_sensor = df["humidity_percent"].rename("hum_sens_percent")
    temperature_sensor_C     = df["temperature_c"].rename("temp_sens_C")
    pressure_sensor_hPa      = df["pressure_hpa"].rename("p_sens_hpa")
    temperature_sensor_K     = (temperature_sensor_C + 273.15).rename("temp_sens_K")
    specific_humidity_sensor = Relative_to_specific_humidity(relative_humidity_sensor,
                                        temperature_sensor_C,
                                        pressure_sensor_hPa).rename("hum_sens_kg/kg")
    
    sensor_data = pd.concat([pressure_sensor_hPa, 
                             temperature_sensor_C, 
                             temperature_sensor_K, 
                             specific_humidity_sensor, 
                             relative_humidity_sensor], axis = 1)
    
    sensor_data = sensor_data.copy()
    sensor_data.index = pd.to_datetime(sensor_data.index, utc=True)

    return sensor_data


def extract_era5_data(pressure_file, single_file, format):
        
        if format == "xarray":
            # Open datasets with xarray:
            ds = xr.merge([xr.open_dataset(pressure_file), xr.open_dataset(single_file)])
            print(ds)
            return ds
            
        if format == "netcdf":

            # Open datasets in netCDF4 format:
            # Two different calls from ERA-5 to retrieve different meteorological parameters from API call:
            era5        = netCDF4.Dataset(pressure_file)
            era5_single = netCDF4.Dataset(single_file)
            return era5, era5_single

       
def FourierTransform(df, col, tinit, tfin, YEAR, MONTH, DAY):

    if df is None or df.empty:
        print("Empty GNSS data")
        return

    df = df.sort_index()
    df = df.between_time(tinit, tfin)

    X = df[col].dropna().values

    if len(X) < 10:
        print("Not enough data for FFT")
        return

    X = X - np.mean(X)

    fft_vals = fft(X)
    freq = fftfreq(n = len(X) , d = 300)

    power = np.abs(fft_vals) ** 2

    plt.figure(figsize=(10,5))
    plt.plot(freq, np.log(fft_vals))
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power")
    plt.title(f"RAW ZTD Power Spectrum for {DAY}-{MONTH}-{YEAR}")
    plt.grid()

    save_dir="FFT_plots"
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    filename = f"FFT_{col}_{tinit.replace(':','')}-{tfin.replace(':','')}-{DAY}_{MONTH}_{YEAR}.pdf"
    save_path = save_dir / filename

    plt.savefig(save_path, format="pdf", bbox_inches="tight")
    print(f"Saved FFT plot -> {save_path}")

    return freq, power

# If the sensor data is missing:
import numpy as np

class EmptySensor(dict):

    def __getitem__(self, key):
        return np.array([np.nan])


