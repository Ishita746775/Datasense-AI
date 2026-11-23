"""
Automated Report Generation Module for Datasense AI.
Supports plain text export and formatted PDF export using ReportLab.
"""

from io import BytesIO
from datetime import datetime
import pandas as pd

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


def build_text_report(df: pd.DataFrame) -> str:
    """Builds a formatted text analysis report from a dataset."""
    if df is None or df.empty:
        return "No dataset loaded."

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report_lines = [
        "DATASENSE AI - DATA ANALYSIS REPORT",
        "=" * 50,
        f"Generated On: {now}",
        "",
        "1. DATASET OVERVIEW",
        "-" * 50,
        f"Total Rows:    {df.shape[0]}",
        f"Total Columns: {df.shape[1]}",
        "",
        "2. COLUMN INFORMATION & DATA TYPES",
        "-" * 50,
        df.dtypes.to_string(),
        "",
        "3. STATISTICAL SUMMARY",
        "-" * 50,
        df.describe(include="all").to_string(),
        "",
        "4. DATA QUALITY & INTEGRITY",
        "-" * 50,
        f"Total Missing Values: {df.isnull().sum().sum()}",
        f"Duplicate Rows:       {df.duplicated().sum()}",
        "",
        "5. MISSING VALUES BY COLUMN",
        "-" * 50,
        df.isnull().sum().to_string(),
        "",
        "=" * 50,
        "Report generated automatically by Datasense AI",
    ]

    return "\n".join(report_lines)


def build_pdf_report(report_text: str, title: str = "Datasense AI - Dataset Analysis Report") -> bytes:
    """Generates a downloadable PDF document from the report text using ReportLab."""
    pdf_buffer = BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)

    styles = getSampleStyleSheet()
    elements = [
        Paragraph(title, styles["Title"]),
        Spacer(1, 15),
        Preformatted(report_text, styles["Code"])
    ]

    pdf.build(elements)
    return pdf_buffer.getvalue()
