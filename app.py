"""
Datasense AI - Main Application Entry Point
An interactive Streamlit platform for automated data analysis, visualization,
natural language querying, and reporting.
"""

import os
import sys
from pathlib import Path

# Ensure application root is in python path
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import streamlit as st
import pandas as pd
import numpy as np

from src.analysis import (
    get_dataset_overview,
    get_column_details,
    get_missing_values_summary,
    get_statistical_summary,
)
from src.visualizations import (
    plot_missing_values,
    plot_bar_chart,
    plot_line_chart,
    plot_scatter,
    plot_pie_chart,
    plot_histogram,
)
from src.qa_engine import answer_question
from src.report_generator import build_text_report, build_pdf_report

# -----------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------
st.set_page_config(
    page_title="Datasense AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# 2. CUSTOM DESIGN / STYLING
# -----------------------------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
.block-container {
    padding-top: 2rem;
}
[data-testid="stMetric"] {
    background-color: #1C2333;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #2D3748;
}
h1, h2, h3 {
    color: #60A5FA;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# 3. SESSION STATE INITIALIZATION
# -----------------------------------
if "df" not in st.session_state:
    st.session_state.df = None
if "dataset_name" not in st.session_state:
    st.session_state.dataset_name = None

# -----------------------------------
# 4. SIDEBAR & NAVIGATION
# -----------------------------------
st.sidebar.title("📊 Datasense AI")
st.sidebar.caption("Intelligent Data Analysis Platform")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Upload Dataset",
        "Data Analysis",
        "Visualizations",
        "Ask Datasense AI",
        "Dataset Report"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📁 Dataset Source")

# Sample dataset path
SAMPLE_DATASET_PATH = APP_DIR / "sample_datasets" / "sales_data.csv"

# Option to quickly load sample dataset
if SAMPLE_DATASET_PATH.exists():
    if st.sidebar.button("Load Sample Dataset (Sales Data)"):
        st.session_state.df = pd.read_csv(SAMPLE_DATASET_PATH)
        st.session_state.dataset_name = "sales_data.csv (Sample)"
        st.sidebar.success("Sample dataset loaded!")

# -----------------------------------
# 5. FILE UPLOADER
# -----------------------------------
st.title("📊 Datasense AI")
st.write(
    "Your AI-powered data analysis assistant. "
    "Understand, explore, and query your data effortlessly without complex code."
)

uploaded_file = st.file_uploader(
    "Upload your CSV or Excel dataset",
    type=["csv", "xlsx", "xls"],
    help="Supported file types: .csv, .xlsx, .xls"
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            st.session_state.df = pd.read_csv(uploaded_file)
        else:
            st.session_state.df = pd.read_excel(uploaded_file)

        st.session_state.dataset_name = uploaded_file.name
        st.sidebar.success(f"Loaded: {uploaded_file.name}")
    except Exception as e:
        st.error(f"Unable to read the uploaded file: {e}")

# Working DataFrame reference
df = st.session_state.df
dataset_name = st.session_state.dataset_name

if df is not None:
    st.sidebar.info(f"**Active Dataset:** {dataset_name}\n\n**Rows:** {df.shape[0]} | **Cols:** {df.shape[1]}")
    if st.sidebar.button("Clear Dataset"):
        st.session_state.df = None
        st.session_state.dataset_name = None
        st.rerun()

# -----------------------------------
# 6. DASHBOARD PAGE
# -----------------------------------
if page == "Dashboard":
    st.header("Dashboard Overview")

    if df is not None:
        metrics = get_dataset_overview(df)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Rows", f"{metrics['rows']:,}")
        col2.metric("Total Columns", f"{metrics['columns']:,}")
        col3.metric("Missing Values", f"{metrics['missing_values']:,}")
        col4.metric("Duplicate Rows", f"{metrics['duplicates']:,}")

        st.subheader("Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)

        st.subheader("Dataset Structure & Types")
        info_df = get_column_details(df)
        st.dataframe(info_df, use_container_width=True)

    else:
        st.info("👋 Welcome! Please upload a dataset or click **'Load Sample Dataset'** in the sidebar to get started.")

        st.markdown("""
        ### What you can do with Datasense AI:
        - 📂 **Multi-format Support:** Upload CSV or Excel spreadsheets effortlessly.
        - 🔍 **Automated Profiling:** Instantly detect data types, duplicates, and missing values.
        - 📈 **Interactive Visualizations:** Generate dynamic Plotly bar charts, trends, scatters, and histograms.
        - 🤖 **Natural Language Q&A:** Ask questions in plain English to uncover insights without coding.
        - 📄 **Exportable Reports:** Download comprehensive reports in TXT or PDF formats.
        """)

# -----------------------------------
# 7. UPLOAD DATASET PAGE
# -----------------------------------
elif page == "Upload Dataset":
    st.header("📁 Dataset Upload & Inspection")

    if df is not None:
        st.success(f"Active dataset: **{dataset_name}**")

        st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")

        st.subheader("Full Dataset View")
        st.dataframe(df, use_container_width=True)

        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Current Dataset as CSV",
            data=csv_data,
            file_name=f"datasense_export_{Path(dataset_name).stem}.csv",
            mime="text/csv"
        )
    else:
        st.warning("Please upload a CSV or Excel file, or load the sample dataset to inspect data.")

# -----------------------------------
# 8. DATA ANALYSIS PAGE
# -----------------------------------
elif page == "Data Analysis":
    st.header("🔍 Statistical Analysis & Quality Check")

    if df is not None:
        st.subheader("Statistical Summary")
        st.dataframe(get_statistical_summary(df), use_container_width=True)

        st.subheader("Column Level Deep Dive")
        for column in df.columns:
            with st.expander(f"📌 {column} ({df[column].dtype})"):
                st.write("**Total Values:**", len(df[column]))
                st.write("**Missing Values:**", int(df[column].isnull().sum()))
                st.write("**Unique Values:**", int(df[column].nunique()))

                if pd.api.types.is_numeric_dtype(df[column]):
                    col_mean = df[column].mean()
                    col_max = df[column].max()
                    col_min = df[column].min()
                    st.write(f"**Mean:** {col_mean:,.2f}" if pd.notnull(col_mean) else "**Mean:** N/A")
                    st.write(f"**Maximum:** {col_max:,.2f}" if pd.notnull(col_max) else "**Maximum:** N/A")
                    st.write(f"**Minimum:** {col_min:,.2f}" if pd.notnull(col_min) else "**Minimum:** N/A")

        st.subheader("Data Health & Integrity")
        missing_count = int(df.isnull().sum().sum())
        duplicate_count = int(df.duplicated().sum())

        col_m, col_d = st.columns(2)
        with col_m:
            if missing_count == 0:
                st.success("✅ No missing values detected!")
            else:
                st.warning(f"⚠️ Found {missing_count} missing value(s).")
        with col_d:
            if duplicate_count == 0:
                st.success("✅ No duplicate records detected!")
            else:
                st.warning(f"⚠️ Found {duplicate_count} duplicate row(s).")

        st.subheader("Missing Values Distribution")
        missing_df = get_missing_values_summary(df)

        if not missing_df.empty:
            fig = plot_missing_values(missing_df)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("All columns are 100% complete.")

    else:
        st.warning("Please upload a dataset first.")

# -----------------------------------
# 9. VISUALIZATION PAGE
# -----------------------------------
elif page == "Visualizations":
    st.header("📈 Interactive Visualizations")

    if df is not None:
        numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
        all_columns = df.columns.tolist()

        if len(all_columns) > 0:
            st.subheader("Create Custom Chart")

            chart_type = st.selectbox(
                "Choose Chart Type",
                ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram"]
            )

            x_column = st.selectbox("Select Dimension / Category (X-axis)", all_columns)

            if chart_type in ["Bar Chart", "Line Chart", "Scatter Plot"]:
                if numeric_columns:
                    y_column = st.selectbox("Select Metric (Y-axis)", numeric_columns)

                    if chart_type == "Bar Chart":
                        fig = plot_bar_chart(df, x_column, y_column)
                    elif chart_type == "Line Chart":
                        fig = plot_line_chart(df, x_column, y_column)
                    else:
                        fig = plot_scatter(df, x_column, y_column)

                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("This chart type requires at least one numeric column.")

            elif chart_type == "Pie Chart":
                fig = plot_pie_chart(df, x_column)
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Histogram":
                if pd.api.types.is_numeric_dtype(df[x_column]):
                    fig = plot_histogram(df, x_column)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Select a numerical column to generate a histogram.")
        else:
            st.warning("No columns found in this dataset.")
    else:
        st.warning("Please upload a dataset first.")

# -----------------------------------
# 10. ASK DATASENSE AI PAGE
# -----------------------------------
elif page == "Ask Datasense AI":
    st.header("🤖 Ask Datasense AI")
    st.write("Query your dataset using simple, conversational English.")

    if df is not None:
        question = st.text_input(
            "Enter your question:",
            placeholder="e.g. What is the total sales? or Which product has the highest sales?"
        )

        if st.button("Get Answer", type="primary"):
            if question.strip():
                with st.spinner("Analyzing dataset..."):
                    answer = answer_question(df, question)
                    st.markdown("### 💡 Answer")
                    st.info(answer)
            else:
                st.warning("Please enter a question first.")

        st.markdown("---")
        st.subheader("💡 Example Questions to Try:")
        st.markdown("""
        - *What is the total sales?*
        - *What is the average sales?*
        - *Which product has the highest sales?*
        - *How many rows are there?*
        - *How many missing values are there?*
        - *What are the column names?*
        """)
    else:
        st.warning("Please upload a dataset first.")

# -----------------------------------
# 11. DATASET REPORT GENERATOR
# -----------------------------------
elif page == "Dataset Report":
    st.header("📄 Automated Report Generator")
    st.write("Generate and download comprehensive summary reports for your dataset.")

    if df is not None:
        report_text = build_text_report(df)

        st.subheader("Report Preview")
        st.text_area("Analysis Summary", report_text, height=350)

        col_txt, col_pdf = st.columns(2)

        with col_txt:
            st.download_button(
                label="📥 Download Plain Text (.txt) Report",
                data=report_text,
                file_name=f"Datasense_Report_{Path(dataset_name).stem}.txt",
                mime="text/plain"
            )

        with col_pdf:
            try:
                pdf_bytes = build_pdf_report(report_text)
                st.download_button(
                    label="📄 Download Formatted PDF (.pdf) Report",
                    data=pdf_bytes,
                    file_name=f"Datasense_Report_{Path(dataset_name).stem}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error compiling PDF report: {e}")
    else:
        st.warning("Please upload a dataset first.")

# -----------------------------------
# 12. FOOTER
# -----------------------------------
st.markdown("---")
st.caption("Datasense AI • Intelligent Data Analysis Platform • Built with Streamlit, Pandas & Plotly")
