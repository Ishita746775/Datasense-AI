"""
Plotly Visualization Module for Datasense AI.
Provides modular chart generation helpers for interactive data exploration.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional


def plot_missing_values(missing_df: pd.DataFrame) -> Optional[go.Figure]:
    """Generates a bar chart showing missing values by column."""
    if missing_df is None or missing_df.empty:
        return None

    fig = px.bar(
        missing_df,
        x="Column",
        y="Missing Values",
        title="Missing Values Analysis",
        color="Missing Values",
        color_continuous_scale="Reds"
    )
    fig.update_layout(template="plotly_dark")
    return fig


def plot_bar_chart(df: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
    """Generates an interactive bar chart."""
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=f"{y_col} by {x_col}",
        color_discrete_sequence=["#60A5FA"]
    )
    fig.update_layout(template="plotly_dark")
    return fig


def plot_line_chart(df: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
    """Generates an interactive line chart."""
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        title=f"{y_col} Trend over {x_col}",
        markers=True,
        color_discrete_sequence=["#38BDF8"]
    )
    fig.update_layout(template="plotly_dark")
    return fig


def plot_scatter(df: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
    """Generates an interactive scatter plot."""
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        title=f"{x_col} vs {y_col}",
        color_discrete_sequence=["#818CF8"]
    )
    fig.update_layout(template="plotly_dark")
    return fig


def plot_pie_chart(df: pd.DataFrame, col: str, top_n: int = 15) -> go.Figure:
    """Generates an interactive pie chart for categorical distributions."""
    pie_data = (
        df[col]
        .dropna()
        .astype(str)
        .value_counts()
        .head(top_n)
        .reset_index()
    )
    pie_data.columns = ["Category", "Count"]

    fig = px.pie(
        pie_data,
        names="Category",
        values="Count",
        title=f"Distribution of {col} (Top {top_n})"
    )
    fig.update_layout(template="plotly_dark")
    return fig


def plot_histogram(df: pd.DataFrame, col: str) -> go.Figure:
    """Generates an interactive histogram for numerical distribution."""
    fig = px.histogram(
        df,
        x=col,
        title=f"Distribution of {col}",
        marginal="box",
        color_discrete_sequence=["#A78BFA"]
    )
    fig.update_layout(template="plotly_dark")
    return fig
