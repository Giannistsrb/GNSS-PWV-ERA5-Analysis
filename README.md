# GNSS-PWV-ERA5 Analysis

## GNSS-based Precipitable Water Vapour Retrieval and Validation using ERA5 Reanalysis


## Overview

This project investigates atmospheric water vapour variability using GNSS meteorology techniques and ERA5 atmospheric reanalysis data.

The main objective is to retrieve **Precipitable Water Vapour (PWV)** from GNSS-derived **Zenith Total Delay (ZTD)** observations and compare the retrieved atmospheric parameters against ERA5 reanalysis products.

The analysis combines:

- GNSS atmospheric delay observations
- ERA5 pressure-level and single-level meteorological variables
- Surface meteorological observations
- Atmospheric thermodynamic calculations


The study focuses on GNSS observations collected during:

**21–24 December 2025**


The developed processing pipeline performs:

- GNSS ZTD quality control
- Zenith Hydrostatic Delay (ZHD) estimation
- Zenith Wet Delay (ZWD) retrieval
- PWV conversion
- ERA5 PWV calculation
- Atmospheric stability analysis using CAPE
- GNSS versus ERA5 comparison
- Automated scientific visualization



---

# Scientific Background


## GNSS Meteorology

GNSS signals travelling through the Earth's atmosphere experience a delay due to atmospheric refractivity.

The total atmospheric delay in the zenith direction is expressed as:


\[
ZTD = ZHD + ZWD
\]


where:

- **ZTD**: Zenith Total Delay
- **ZHD**: Zenith Hydrostatic Delay
- **ZWD**: Zenith Wet Delay


The hydrostatic component is mainly controlled by atmospheric pressure, while the wet component is associated with atmospheric water vapour.


---

## Precipitable Water Vapour (PWV)

The atmospheric water vapour content can be expressed as:

\[
PWV = \Pi \cdot ZWD
\]


where:

- PWV is the equivalent liquid water depth (mm)
- ZWD is the zenith wet delay
- Π is the water vapour conversion factor


The conversion factor depends on the weighted mean atmospheric temperature:

\[
\Pi =
\frac{10^6}
{\rho_w R_v (k_2' + k_3/T_m)}
\]


In this project, the weighted mean temperature is estimated using the Zhang empirical relationship:


\[
T_m = 0.72T_s + 70.2
\]


where:

- \(T_s\) is the surface temperature.



---

# Data Sources


## GNSS Observations

GNSS atmospheric observations were obtained from a receiver providing:

- Zenith Total Delay (ZTD)
- Timestamp information


The GNSS observations were processed to obtain hourly atmospheric parameters.


---

## ERA5 Reanalysis

ERA5 is the fifth generation atmospheric reanalysis dataset produced by the European Centre for Medium-Range Weather Forecasts (ECMWF).


ERA5 variables used in this project:


### Pressure levels

- Temperature
- Specific humidity


### Single levels

- Surface pressure
- 2 m temperature
- 2 m dew point temperature
- Convective Available Potential Energy (CAPE)



---

# Methodology


The complete processing workflow is:

GNSS Receiver
|
|
v
Zenith Total Delay (ZTD)
|
|
+----------------+
| |
v v
ZHD calculation ZWD retrieval
| |
| |
+----------------+
|
v
PWV estimation

ERA5 Atmospheric Profiles
|
|
v
Atmospheric PWV calculation

          |
          |
          v

GNSS vs ERA5 comparison



---

# Atmospheric Stability Analysis


Convective Available Potential Energy (CAPE) is calculated to investigate atmospheric instability.

CAPE represents the amount of buoyant energy available for an air parcel during vertical ascent.

The calculation uses:

- Temperature profiles
- Specific humidity profiles
- Surface temperature
- Surface dew point temperature
- Pressure profiles


Two approaches are implemented:

1. Custom thermodynamic CAPE calculation
2. MetPy surface-based CAPE calculation


The two approaches are compared against ERA5 CAPE values.



---

# Project Structure

GNSS-PWV-ERA5-Analysis/

│
├── main.py
├── requirements.txt
├── README.md
│
├── src/
│ ├── config.py
│ ├── constants.py
│ ├── paths.py
│ ├── physics.py
│ ├── data_loading.py
│ ├── era5_api.py
│ ├── pipeline.py
│ ├── plotting.py
│ └── analysis.py
│
├── data/
│ ├── sensor/
│ │ ├── csv_files/
│ │ └── log_files/
│ │
│ └── era5/
│
├── outputs/
│ ├── plots/
│ └── tables/
│
└── docs/

---

# Installation


Clone the repository:


```bash

git clone https://github.com/USERNAME/GNSS-PWV-ERA5-Analysis.git

Navigate into the project folder:

cd GNSS-PWV-ERA5-Analysis

Install dependencies:

pip install -r requirements.txt

Running the Pipeline

Execute:

python main.py

The pipeline will:

Load GNSS observations
Load ERA5 datasets
Calculate atmospheric parameters
Estimate PWV
Calculate CAPE
Produce comparison plots

Results are stored automatically in:

outputs/plots/

Generated Products

The pipeline produces:

Atmospheric Delay Products
ZTD
ZHD
ZWD
Water Vapour Products
GNSS-derived PWV
ERA5 PWV
Atmospheric Stability Products
ERA5 CAPE
Calculated CAPE
MetPy CAPE
Visualization

Example outputs:

└── plots/

    ERA5_VS_SENSOR_21122025.pdf

Software Requirements

Main Python libraries:

NumPy
Pandas
Xarray
NetCDF4
SciPy
Matplotlib
MetPy
CDS API

Future Improvements

Future developments include:

Machine learning based PWV forecasting
Short-term atmospheric prediction models
Integration with additional GNSS stations
Real-time GNSS meteorological monitoring
ERA5-Land comparison
Deep learning approaches for water vapour prediction

Author

Ioannis Tsormpatzoglou

GNSS Meteorology | Atmospheric Science | Machine Learning Applications


    










