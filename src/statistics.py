"""
statistics.py

Statistical validation methods
for GNSS-PWV-ERA5 comparison.

Author:
Ioannis Tsormpatzoglou
"""

import numpy as np
import pandas as pd

def bias(reference, model):
    return np.mean(model - reference)

def mae(reference, model):
    return np.mean(np.abs(model - reference))

def rmse(reference, model):
    return np.sqrt(np.mean((model - reference) ** 2))

def correlation(reference, model):
    return np.corrcoef(reference, model)[0, 1]

def r2(reference, model):

    ss_res = np.sum((reference - model) ** 2)
    ss_tot = np.sum((reference - np.mean(reference)) ** 2)

    return 1 - ss_res / ss_tot

def comparison_statistics(df, reference_column, model_column):

    reference = df[reference_column].dropna()

    model = df[model_column].loc[reference.index]

    results = { "Samples":
                len(reference),

                "Bias_mm":
                bias(reference, model),

                "MAE_mm":
                mae(reference, model),

                "RMSE_mm":
                rmse(reference, model),

                "Correlation":
                correlation(reference, model),

                "R2":
                r2(reference, model)

    }


    return pd.DataFrame(results, index=[model_column])