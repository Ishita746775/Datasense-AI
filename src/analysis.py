"""
Data Analysis & Health Profiling Module for Datasense AI.
Provides automated dataset statistics, column-level introspection, and data quality metrics.
"""

import pandas as pd
from typing import Dict, Any


def get_dataset_overview(df: pd.DataFrame) -> Dict[str, Any]:
    """Computes high-level overview metrics for a given DataFrame."""
    if df is None or df.empty:
        return {
            "rows": 0,
            "columns": 0,
            "missing_values": 0,
            "duplicates": 0,
        }

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
    }


def get_column_details(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a structured summary DataFrame of column names, data types,

    missing counts, and unique value counts.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    return pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values,
    })


def get_missing_values_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a filtered DataFrame listing columns with non-zero missing values."""
    if df is None or df.empty:
        return pd.DataFrame(columns=["Column", "Missing Values"])

    missing_df = df.isnull().sum().reset_index()
    missing_df.columns = ["Column", "Missing Values"]
    return missing_df[missing_df["Missing Values"] > 0]


def get_statistical_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a transposed pandas statistical describe table."""
    if df is None or df.empty:
        return pd.DataFrame()

    return df.describe(include="all").T
