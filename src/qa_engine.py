"""
Natural Language Q&A Engine for Datasense AI.
Answers basic English questions about an uploaded dataset using Python and Pandas.
"""

import re
import pandas as pd
from typing import Optional, List


def _has_keyword(keywords: List[str], text: str) -> bool:
    """Checks if any keyword appears as a standalone word/phrase in text."""
    for kw in keywords:
        pattern = r'\b' + re.escape(kw) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def answer_question(df: pd.DataFrame, question: str) -> str:
    """Answers basic English questions about an uploaded dataset.

    Uses Python and Pandas without requiring an external AI API.
    """
    if df is None or df.empty:
        return "Please upload a dataset first."

    q = question.lower().strip()

    if not q:
        return "Please enter a question."

    # Identify numeric and categorical columns
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    categorical_columns = df.select_dtypes(
        include=["object", "category", "string"]
    ).columns.tolist()

    # Helper: find a column mentioned in the question
    def find_column(columns):
        for col in columns:
            name = str(col).lower().replace("_", " ")
            if re.search(r'\b' + re.escape(name) + r'\b', q) or name in q:
                return col
        return None

    # 1. Total number of rows
    if any(phrase in q for phrase in ["how many rows", "number of rows", "total records", "row count", "count rows"]):
        return f"Your dataset contains {len(df)} rows."

    # 2. Total number of columns
    if any(phrase in q for phrase in ["how many columns", "number of columns", "column count"]):
        return f"Your dataset contains {len(df.columns)} columns."

    # 3. Dataset column names
    if any(phrase in q for phrase in ["column names", "what columns", "list columns", "show columns"]):
        return "Your dataset columns are: " + ", ".join(map(str, df.columns))

    # 4. Missing values
    if _has_keyword(["missing", "null", "empty values", "nan"], q):
        missing = int(df.isnull().sum().sum())
        details = df.isnull().sum()
        result = f"Your dataset contains {missing} missing values.\n\n"
        for col, count in details.items():
            if count > 0:
                result += f"- {col}: {count} missing value(s)\n"
        if missing == 0:
            result += "There are no missing values."
        return result.strip()

    # 5. Duplicate records
    if _has_keyword(["duplicate", "duplicates"], q):
        duplicates = int(df.duplicated().sum())
        return f"Your dataset contains {duplicates} duplicate rows."

    # 6. Identify a numeric column
    metric = find_column(numeric_columns)

    # If no numeric column is explicitly mentioned, find a sensible default if asking for aggregations
    is_aggregation = _has_keyword(
        ["total", "sum", "overall", "average", "mean", "highest", "maximum", "largest", "most", "lowest", "minimum", "smallest", "least", "top", "best"],
        q
    )

    if metric is None and numeric_columns and is_aggregation:
        if "sales" in q:
            metric = next(
                (c for c in numeric_columns if "sales" in str(c).lower()),
                numeric_columns[0]
            )
        elif "quantity" in q:
            metric = next(
                (c for c in numeric_columns if "quantity" in str(c).lower()),
                numeric_columns[0]
            )
        else:
            metric = numeric_columns[0]

    # 7. Total / sum
    if _has_keyword(["total", "sum", "overall"], q):
        if metric:
            value = df[metric].sum()
            return f"Total {metric} = {value:,.2f}"
        return "No numeric column was found."

    # 8. Average
    if _has_keyword(["average", "mean"], q):
        if metric:
            value = df[metric].mean()
            return f"Average {metric} = {value:,.2f}"
        return "No numeric column was found."

    # 9. Maximum value
    if _has_keyword(["highest", "maximum", "largest", "most"], q) and not _has_keyword(["top", "best"], q):
        if metric and not df[metric].dropna().empty:
            value = df[metric].max()
            row = df.loc[df[metric].idxmax()]
            return (
                f"Highest {metric} = {value:,.2f}\n\n"
                f"Corresponding record:\n{row.to_string()}"
            )
        return "No numeric column or valid values found."

    # 10. Minimum value
    if _has_keyword(["lowest", "minimum", "smallest", "least"], q):
        if metric and not df[metric].dropna().empty:
            value = df[metric].min()
            row = df.loc[df[metric].idxmin()]
            return (
                f"Lowest {metric} = {value:,.2f}\n\n"
                f"Corresponding record:\n{row.to_string()}"
            )
        return "No numeric column or valid values found."

    # 11. Find top products, regions, or categories
    if _has_keyword(["top", "best"], q):
        group_column = find_column(categorical_columns)

        if group_column and metric:
            grouped = (
                df.groupby(group_column)[metric]
                .sum()
                .sort_values(ascending=False)
                .head(5)
            )

            return (
                f"Top 5 {group_column} by {metric}:\n\n"
                + grouped.to_string()
            )

    # 12. Count unique values in a column
    if _has_keyword(["unique", "different"], q):
        column = find_column(df.columns.tolist())

        if column:
            return (
                f"{column} has {df[column].nunique()} unique values."
            )

    # 13. General statistical summary
    if _has_keyword(["summary", "statistics", "describe"], q):
        return df.describe(include="all").to_string()

    # 14. Fallback for unsupported question
    return (
        "Sorry, I could not understand that question.\n\n"
        "Try asking:\n"
        "- What is the total sales?\n"
        "- What is the average sales?\n"
        "- Which product has the highest sales?\n"
        "- How many missing values are there?\n"
        "- How many rows are there?"
    )
