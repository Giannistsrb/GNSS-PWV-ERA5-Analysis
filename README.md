# GNSS-PWV-ERA5 Analysis

A Python-based framework for retrieving Precipitable Water Vapour (PWV) from GNSS observations and evaluating ERA5 reanalysis products.

The project compares GNSS-derived PWV measurements against ERA5-derived PWV and applies statistical bias correction to improve agreement between the two datasets.

---

## Overview

Atmospheric water vapour is one of the most important variables in weather and climate studies. GNSS observations provide continuous measurements of atmospheric delay, which can be converted into PWV.

This project implements an end-to-end processing pipeline:

- GNSS observation processing
- ZTD to PWV conversion
- ERA5 atmospheric data processing
- GNSS–ERA5 comparison
- Statistical validation
- Bias correction

---

## Project Objective

The main objective of this project is to evaluate the capability of ERA5 reanalysis data to reproduce GNSS-derived PWV observations.

The analysis focuses on:

- Quantifying the agreement between GNSS and ERA5 PWV
- Identifying systematic biases in ERA5 estimates
- Applying bias correction techniques
- Evaluating the improvement after correction
- Developing and validating an independent CAPE calculation algorithm from ERA5 atmospheric profiles

## Data Sources

### 1. GNSS observations

GNSS measurements are used to derive Zenith Total Delay (ZTD), which is converted into PWV.

### 2 .ERA5 Reanalysis

ERA5 atmospheric reanalysis data from ECMWF are used to compute atmospheric parameters and estimate PWV for comparison.

---


## Experimental Configuration

The analysis was performed using the following configuration:

### Observation Period

- Year: 2025
- Month: December
- Measurement days:
  - 21 December 2025
  - 22 December 2025
  - 23 December 2025
  - 24 December 2025

### GNSS Station Information

- Latitude: 41.5858688° N
- Longitude: 12.6779392° E
- Sensor height above mean sea level: 58 m

### ERA5 Configuration

- ERA5 spatial resolution: 0.10° × 0.10°
- Dataset type: ERA5 hourly reanalysis

## Processing Workflow

```text
GNSS observations
        |
        v
Zenith Total Delay (ZTD)
        |
        +----------------+
        |                |
        v                v
    GNSS PWV        ZTD FFT analysis
        |
        |
        v
ERA5 atmospheric data
        |
        +----------------+
        |                |
        v                v
    ERA5 PWV          CAPE calculation
        |
        v
GNSS–ERA5 validation
        |
        v
Bias correction

```

## ERA5 Reanalysis

ERA5 reanalysis data from ECMWF are used to estimate atmospheric parameters and calculate PWV for comparison with GNSS observations.

## Methodology

The analysis consists of the following steps:

### 1. GNSS PWV Retrieval

GNSS Zenith Total Delay is separated into:

Zenith Hydrostatic Delay (ZHD)
Zenith Wet Delay (ZWD)

The Zenith Wet Delay is converted into PWV.

### 2. ZTD Frequency Analysis (Fourier Transform)

Fourier Transform (FFT) analysis was applied to GNSS-derived Zenith Total Delay (ZTD) observations in order to investigate the frequency characteristics of the atmospheric delay signal.

The ZTD time series was transformed from the time domain into the frequency domain to identify dominant spectral components and evaluate the variability of the atmospheric signal during the observation period.

Example FFT spectrum:

![FFT analysis of ZTD variations](outputs/plots/FFT/FFT_ZTD_m_1200-2200_21122025.pdf)

### 3. ERA5 PWV Estimation

ERA5 atmospheric variables are processed to obtain PWV values at the corresponding location and time.

### 4. Statistical Validation

The agreement between GNSS PWV and ERA5 PWV is evaluated using:

Bias
Mean Absolute Error (MAE)
Root Mean Square Error (RMSE)
Pearson correlation coefficient
Coefficient of determination (R²)

### 5. Atmospheric Instability Analysis (CAPE)

Convective Available Potential Energy (CAPE) was calculated from ERA5 atmospheric profiles using a custom implementation developed for this project.

The CAPE analysis consisted of three approaches:

```text
ERA5 atmospheric profiles (temperature, humidity, pressure)
                         |
                         v
              +----------------------+
              |                      |
              v                      v
     MetPy CAPE calculation   Custom CAPE algorithm
              |                      |
              |                      |
              +----------+-----------+
                         |
                         v
              Comparison and validation
                         |
                         v
             ERA5 native CAPE product
```

The implemented algorithm derives CAPE from ERA5 thermodynamic profiles and was evaluated against the native CAPE product provided by the ERA5 reanalysis dataset.

The comparison was performed to assess the consistency of the independently calculated CAPE values with the ERA5 reference product.

The calculated CAPE values are stored as an additional atmospheric diagnostic parameter for further analysis.

Due to the limited number of available observation days, CAPE–PWV statistical relationships were not evaluated in this study.


## Bias Correction

The comparison showed a systematic bias between ERA5 and GNSS PWV.

ERA5 showed a systematic dry bias compared with GNSS-derived PWV observations.

A mean bias correction was applied:

PWV_corrected = PWV_ERA5 - Bias

After correction:

The mean bias was reduced close to zero.
RMSE improved.
The agreement between ERA5 and GNSS PWV increased.

## Results

The project produces:

## Summary Results

### 1. GNSS–ERA5 PWV Comparison
![PWV scatter comparison](outputs/plots/PWV_GNSS_vs_ERA5_scatter_all_data.pdf)

### 2. Time-Series Comparison
![PWV time series](outputs/plots/ERA5_VS_SENSOR_21122025.pdf)

### 3. ZTD Frequency Analysis
![FFT spectrum](outputs/plots/FFT/FFT_ZTD_m_1200-2200_21122025.pdf)

### 4. Validation Statistics
Generated outputs:

```text
outputs/

├── plots/
│   ├── ERA5 vs GNSS comparison plots
│   ├── PWV scatter plots
│   └── FFT analysis plots
│
└── tables/
    ├── statistics_raw_summary.csv
    └── statistics_summary_biased.csv
```
The performance of ERA5 PWV was evaluated against GNSS-derived PWV observations before and after applying bias correction.

### Before Bias Correction
```text
| Day | Samples | Bias (mm) | MAE (mm) | RMSE (mm) | Correlation | R² |
|---|---:|---:|---:|---:|---:|---:|
| 21-12-2025 | 13 | -6.625 | 6.625 | 6.643 | 0.640 | -116.504 |
| 22-12-2025 | 13 | -6.973 | 6.973 | 7.006 | 0.669 | -78.045 |
| 23-12-2025 | 6 | -8.226 | 8.226 | 8.243 | 0.780 | -103.538 |
| 24-12-2025 | 12 | -6.303 | 6.303 | 6.547 | 0.419 | -10.232 |
```
### After Bias Correction
```text
| Day | Samples | Bias (mm) | MAE (mm) | RMSE (mm) | Correlation | R² |
|---|---:|---:|---:|---:|---:|---:|
| 21-12-2025 | 13 | ~0.000 | 0.373 | 0.498 | 0.640 | 0.341 |
| 22-12-2025 | 13 | ~0.000 | 0.484 | 0.674 | 0.669 | 0.268 |
| 23-12-2025 | 6 | ~0.000 | 0.464 | 0.534 | 0.780 | 0.562 |
| 24-12-2025 | 12 | ~0.000 | 1.444 | 1.774 | 0.419 | 0.176 |
```
### Summary

Bias correction successfully removed the systematic offset between ERA5 and GNSS PWV.

The evaluated ERA5 PWV estimates showed a consistent dry bias of approximately 6–8 mm during the selected observation period.

## Project Structure

```text
GNSS-PWV-ERA5-Analysis/

├── main.py
│
├── src/
│   ├── analysis.py
│   ├── statistics.py
│   ├── plotting.py
│   ├── physics.py
│   └── pipeline.py
│
├── data/
│   └── sensor/
│
├── outputs/
│   ├── plots/
│   └── tables/
│
└── README.md
```



## Installation

- Clone the repository:
```text
git clone https://github.com/Giannistsrb/GNSS-PWV-ERA5-Analysis.git
```
- Install required packages:
```text
pip install -r requirements.txt
```

- ERA5 Data Access:

ERA5 data are retrieved from the Copernicus Climate Data Store (CDS) using the ECMWF API.

The required ERA5 variables are automatically downloaded and processed by the pipeline.

## Usage

Run the processing pipeline:
```text
python main.py
```

The pipeline will:

1. Load GNSS observations
2. Process ERA5 data
3. Retrieve PWV values
4. Compare GNSS and ERA5
5. Apply bias correction
6. Generate plots and statistics

## Future Improvements

Possible future extensions:

- Multi-year GNSS–ERA5 validation
- Machine learning based PWV correction
- Short-term PWV forecasting
- Integration with numerical weather prediction models
- Extreme weather event analysis
  
## Author
Ioannis Tsormpatzoglou
GNSS-PWV-ERA5 Analysis Project

## Main Libraries

The project uses:

- pandas and numpy for data processing
- xarray for ERA5 NetCDF handling
- matplotlib for visualization
- scipy for statistical analysis
- MetPy for atmospheric calculations



