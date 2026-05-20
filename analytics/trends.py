import pandas as pd
import numpy as np
from typing import Dict, Any

def compute_trend(series: pd.Series) -> float:
    """Calculate the linear trend (slope) of a numeric pandas Series.
    Uses simple linear regression (np.polyfit) to compute the slope.
    Returns 0.0 if series is empty or constant.
    """
    if series.empty:
        return 0.0
    x = np.arange(len(series))
    y = series.values.astype(float)
    # If all y are equal, slope is zero
    if np.allclose(y, y[0]):
        return 0.0
    slope, _ = np.polyfit(x, y, 1)
    return float(slope)

def analyze_numeric_trends(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze numeric columns in a DataFrame and return statistics.
    For each numeric column, compute mean, min, max, and trend slope.
    Returns a dictionary keyed by column name.
    """
    results = {}
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        series = df[col].dropna()
        results[col] = {
            "mean": series.mean(),
            "min": series.min(),
            "max": series.max(),
            "trend": compute_trend(series),
        }
    return results
