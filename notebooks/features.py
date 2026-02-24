"""Fourier seasonal features for temperature forecasting."""

import numpy as np
import pandas as pd

SEASONAL_PERIODS = {
    "year": 365.25,
    "month": 365.25 / 12,
    "bi_week": 14,
    "week": 7,
}


def fourier_features(index, ref_date, periods=SEASONAL_PERIODS):
    """Create sin/cos Fourier features for multi-scale seasonality.

    Parameters
    ----------
    index : DatetimeIndex
        Dates for which to compute features.
    ref_date : Timestamp
        Reference date for computing day offsets (typically df.index[0]).
    periods : dict
        Mapping of name -> period in days.
    """
    t = np.array([(d - ref_date).days for d in index])
    cols = {}
    for name, period in periods.items():
        cols[f"sin_{name}"] = np.sin(2 * np.pi * t / period)
        cols[f"cos_{name}"] = np.cos(2 * np.pi * t / period)
    return pd.DataFrame(cols, index=index)
