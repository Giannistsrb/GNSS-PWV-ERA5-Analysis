"""
paths.py
========

Central path management for the GNSS-PWV-ERA5 Analysis project.

All input data and output directories are defined here.

Author
------
Ioannis Tsormpatzoglou
"""


from pathlib import Path


def sensor_exists(sensor_csv_path):
    return Path(sensor_csv_path).exists()



# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent



# =========================
# DATA DIRECTORIES
# =========================

DATA_DIR = BASE_DIR / "data"


# GNSS + weather sensor data
DATA_SENSOR_DIR = DATA_DIR / "sensor"

CSV_SENSOR_DIR = DATA_SENSOR_DIR / "csv_files"

LOG_SENSOR_DIR = DATA_SENSOR_DIR / "log_files"



# ERA5 datasets
ERA5_DIR = DATA_DIR / "era5"



# =========================
# OUTPUT DIRECTORIES
# =========================

OUTPUT_DIR = BASE_DIR / "outputs"

PLOTS_DIR = OUTPUT_DIR / "plots"

TABLES_DIR = OUTPUT_DIR / "tables"



# Create directories if missing

ERA5_DIR.mkdir(parents=True, exist_ok=True)

CSV_SENSOR_DIR.mkdir(parents=True, exist_ok=True)

LOG_SENSOR_DIR.mkdir(parents=True, exist_ok=True)

PLOTS_DIR.mkdir(parents=True, exist_ok=True)

TABLES_DIR.mkdir(parents=True, exist_ok=True)