"""
plotting.py
===========

Visualization utilities for the GNSS-PWV-ERA5 Analysis project.

Available plots include

     Time series
     ERA5 versus sensor comparisons
     GNSS observations
     PWV
     ZTD
     ZHD
     ZWD
     CAPE
     Fourier spectra

All figures are exported as publication-quality PDF files.

Author
------
Ioannis Tsormpatzoglou
"""

__author__ = "Ioannis Tsormpatzoglou"
__version__ = "3.0"

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from scipy.stats import linregress
import numpy as np

OUTPUT_DIR = Path("outputs")
PLOTS_DIR = OUTPUT_DIR / "plots"

PLOTS_DIR.mkdir(parents=True, exist_ok=True)

def plot_timeseries_from_dataframe(df, ylabel):

    plt.figure(figsize=(8, 6))

    plt.plot(df.index, df[ylabel])
  
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    plt.xlabel("Time (UTC)")
    plt.xticks(rotation=45)

    plt.ylabel(ylabel)

    date_str_title = df.index[0].strftime("%d-%m-%Y")
    date_str_file  = df.index[0].strftime("%d_%m_%Y")

    plt.title(f"{ylabel} - {date_str_title}")

    plt.grid(True)
    plt.tight_layout()

    # Safe folder/file name (replace characters not allowed in paths)
    safe_col = str(ylabel).replace("/", "_").replace("\\", "_")

    save_path = PLOTS_DIR / f"{safe_col}_{date_str_file}.pdf"

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()

def era5_sensor_comparison_subplots(df_gnss, df_era5, df_sensor_era5):

    date_str = df_sensor_era5.index[0].strftime("%d%m%Y")

    fig = plt.figure(figsize=(14, 10))

    gs = GridSpec(3, 2, figure=fig)

    ax1 = fig.add_subplot(gs[0, 0])
    ax6 = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[1, 1])
    ax4 = fig.add_subplot(gs[2, 0])
    ax5 = fig.add_subplot(gs[2, 1])

    ax1.plot(df_gnss.index, df_gnss["ZTD_m"], label="Sensor")
    ax1.set_title("GNSS Raw Signals from Sensor")
    ax1.set_ylabel("ZTD (m)")
    ax1.legend()

    ax6.plot(df_era5.index, df_era5["CAPE_ERA5_J_kg"], label="ERA5")
    ax6.plot(df_era5.index, df_era5["CAPE_J_kg"], label = "Calculated")
    ax6.plot(df_era5.index, df_era5["CAPE_MetPy_J_kg"], label = "Metpy")
    ax6.set_title("CAPE")
    ax6.set_ylabel("CAPE (J/kg)")
    ax6.legend()
    
    ax2.plot(df_sensor_era5.index, df_sensor_era5["ZTD_sensor_m"], label="Sensor")
    ax2.plot(df_sensor_era5.index, df_sensor_era5["ZTD_ERA5_m"],   label="ERA5")
    ax2.set_title("ZTD - ERA5 vs Sensor")
    ax2.set_ylabel("ZTD (m)")
    ax2.legend()

    ax3.plot(df_sensor_era5.index, df_sensor_era5["ZHD_sensor_m"], label="Sensor")
    ax3.plot(df_sensor_era5.index, df_sensor_era5["ZHD_ERA5_m"],   label="ERA5")
    ax3.set_title("ZHD - ERA5 vs Sensor")
    ax3.set_ylabel("ZHD (m)")
    ax3.legend()

    ax4.plot(df_sensor_era5.index, df_sensor_era5["ZWD_sensor_m"], label="Sensor")
    ax4.plot(df_sensor_era5.index, df_sensor_era5["ZWD_ERA5_m"],   label="ERA5")
    ax4.set_title("ZWD - ERA5 vs Sensor")
    ax4.set_ylabel("ZWD (m)")
    ax4.legend()

    ax5.plot(df_sensor_era5.index, df_sensor_era5["PWV_sensor_mm"],           label="Sensor")
    ax5.plot(df_sensor_era5.index, df_sensor_era5["PWV_ERA5_mm"],             label="ERA5")
    ax5.plot(df_sensor_era5.index, df_sensor_era5["PWV_ERA5_mm_corrected"],   label="ERA5-Bias correction", color = "black")
    ax5.set_title("PWV - ERA5 vs Sensor & Bias Correction")
    ax5.set_ylabel("PWV (m)")
    ax5.legend()
    

    for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        ax.grid(True)

    plt.tight_layout()


    # folder per variable
    save_path = PLOTS_DIR / f"ERA5_VS_SENSOR_{date_str}.pdf"

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()

def plot_pwv_scatter(df, reference_col, model_col):

    date_str = df.index[0].strftime("%d%m%Y")

    x = df[reference_col]
    y = df[model_col]

    # Linear Regression:
    slope, intercept, r_value, p_value, std_err = linregress(x, y)

    plt.figure(figsize = (7, 7))

    plt.scatter(x, y, label = "ERA5 vs GNSS")

    # Regression line: 
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = slope * x_line + intercept

    plt.plot(x_line, y_line, label = f"Linear fit: y={slope:.2f}x+{intercept:.2f}")
    plt.plot(x_line, x_line, linestyle = "--", label = "Perfect agreement (y=x)")

    plt.xlabel("GNSS PWV (mm)")
    plt.ylabel("ERA5 PWV (mm)")
    plt.legend()
    plt.grid(True)

    plt.title(f"GNSS PWV vs ERA5 PWV - {date_str}")

    save_path = PLOTS_DIR / f"PWV_GNSS_vs_ERA5_scatter_{date_str}.pdf"

    plt.savefig(save_path, dpi = 300, bbox_inches = "tight")

    plt.close()

    print(f"Saved scatter plot --> {save_path}")

def plot_pwv_scatter_all_days(df, reference_col, model_col):

    date_str = df.index[0].strftime("%d%m%Y")

    x = df[reference_col]
    y = df[model_col]

    # Linear Regression:
    slope, intercept, r_value, p_value, std_err = linregress(x, y)

    plt.figure(figsize = (7, 7))

    plt.scatter(x, y, label = "ERA5 PWV samples")

    # Regression line: 
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = slope * x_line + intercept

    plt.plot(x_line, y_line, label = f"Linear fit: y={slope:.2f}x+{intercept:.2f}")
    plt.plot(x_line, x_line, linestyle = "--", label = "Perfect agreement (y=x)")

    plt.xlabel("GNSS PWV (mm)")
    plt.ylabel("ERA5 PWV (mm)")
    plt.legend()
    plt.grid(True)

    plt.title(f"GNSS PWV vs ERA5 PWV - All Data")

    save_path = PLOTS_DIR / f"PWV_GNSS_vs_ERA5_scatter_all_data.pdf"

    plt.savefig(save_path, dpi = 300, bbox_inches = "tight")

    plt.close()

    print(f"Saved scatter plot --> {save_path}")


     

    

