"""
Unit tests for Datasense AI core modules:
- src.qa_engine
- src.analysis
- src.report_generator
"""

import sys
import unittest
from pathlib import Path
import pandas as pd

# Ensure repository root is on sys.path
REPO_DIR = Path(__file__).resolve().parent.parent
if str(REPO_DIR) not in sys.path:
    sys.path.insert(0, str(REPO_DIR))

from src.qa_engine import answer_question
from src.analysis import (
    get_dataset_overview,
    get_column_details,
    get_missing_values_summary,
    get_statistical_summary,
)
from src.report_generator import build_text_report, build_pdf_report


class TestQAEngine(unittest.TestCase):
    """Test suite for Natural Language Q&A Engine."""

    def setUp(self):
        # Sample test dataframe
        self.df = pd.DataFrame({
            "Order_ID": [1, 2, 3, 4],
            "Product": ["Laptop", "Mobile", "Tablet", "Monitor"],
            "Sales": [50000.0, 20000.0, 15000.0, 25000.0],
            "Quantity": [2, 1, 3, 2],
            "Region": ["North", "South", "East", "West"]
        })

    def test_empty_dataframe(self):
        result = answer_question(pd.DataFrame(), "how many rows")
        self.assertEqual(result, "Please upload a dataset first.")

    def test_none_dataframe(self):
        result = answer_question(None, "how many rows")
        self.assertEqual(result, "Please upload a dataset first.")

    def test_row_count(self):
        result = answer_question(self.df, "how many rows")
        self.assertIn("4 rows", result)

    def test_column_count(self):
        result = answer_question(self.df, "how many columns")
        self.assertIn("5 columns", result)

    def test_column_names(self):
        result = answer_question(self.df, "what are the column names")
        self.assertIn("Order_ID", result)
        self.assertIn("Product", result)

    def test_missing_values_none(self):
        result = answer_question(self.df, "are there any missing values")
        self.assertIn("no missing values", result.lower())

    def test_missing_values_present(self):
        df_with_nan = self.df.copy()
        df_with_nan.loc[0, "Sales"] = None
        result = answer_question(df_with_nan, "how many missing values")
        self.assertIn("1 missing value", result)

    def test_total_metric(self):
        result = answer_question(self.df, "what is the total sales")
        self.assertIn("110,000.00", result)

    def test_average_metric(self):
        result = answer_question(self.df, "what is the average sales")
        self.assertIn("27,500.00", result)

    def test_highest_metric(self):
        result = answer_question(self.df, "which has the highest sales")
        self.assertIn("50,000.00", result)
        self.assertIn("Laptop", result)

    def test_unsupported_question(self):
        result = answer_question(self.df, "what is the meaning of life")
        self.assertIn("Sorry, I could not understand", result)


class TestAnalysisModule(unittest.TestCase):
    """Test suite for Data Analysis & Profiling module."""

    def setUp(self):
        self.df = pd.DataFrame({
            "A": [1, 2, 2, None],
            "B": ["apple", "banana", "banana", "orange"]
        })

    def test_dataset_overview(self):
        overview = get_dataset_overview(self.df)
        self.assertEqual(overview["rows"], 4)
        self.assertEqual(overview["columns"], 2)
        self.assertEqual(overview["missing_values"], 1)
        self.assertEqual(overview["duplicates"], 1)

    def test_column_details(self):
        details = get_column_details(self.df)
        self.assertEqual(len(details), 2)
        self.assertIn("Column Name", details.columns)

    def test_missing_values_summary(self):
        missing = get_missing_values_summary(self.df)
        self.assertEqual(len(missing), 1)
        self.assertEqual(missing.iloc[0]["Column"], "A")
        self.assertEqual(missing.iloc[0]["Missing Values"], 1)


class TestReportGenerator(unittest.TestCase):
    """Test suite for Report Generation."""

    def setUp(self):
        self.df = pd.DataFrame({
            "Product": ["Widget A", "Widget B"],
            "Price": [10.5, 20.0]
        })

    def test_text_report(self):
        text = build_text_report(self.df)
        self.assertIn("DATASENSE AI - DATA ANALYSIS REPORT", text)
        self.assertIn("Total Rows:    2", text)

    def test_pdf_report(self):
        text = build_text_report(self.df)
        pdf_bytes = build_pdf_report(text)
        self.assertTrue(len(pdf_bytes) > 500)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))


if __name__ == "__main__":
    unittest.main()
