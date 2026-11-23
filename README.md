# Datasense AI 📊

Datasense AI is an intelligent, interactive web application built with Streamlit and Python. It streamlines exploratory data analysis by offering instant statistical summaries, interactive Plotly visualizations, plain-English dataset querying, and downloadable summary reports in both text and PDF formats.

---

## ✨ Features

- **Multi-Format Ingestion**: Upload CSV or Excel spreadsheets (`.csv`, `.xlsx`, `.xls`), or explore the built-in sample sales dataset.
- **Automated Data Profiling**: Instantly view dataset shape, column data types, missing value counts, and duplicate record detection.
- **Interactive Visualizations**: Generate customizable Plotly charts including bar charts, line trends, scatter plots, pie distributions, and histograms.
- **Natural Language Dataset Q&A**: Ask questions in simple English (e.g., total sales, average metrics, highest performing items, missing rows) without writing SQL or Python.
- **Exportable Reports**: Generate and download comprehensive analysis reports in plain text (`.txt`) and formatted PDF (`.pdf`) format via ReportLab.

---

## 📁 Project Structure

```text
Datasense-AI/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI workflow (automated tests)
├── .streamlit/
│   └── config.toml            # Streamlit theme & server configuration
├── sample_datasets/
│   └── sales_data.csv         # Demo dataset for quick testing
├── src/
│   ├── __init__.py
│   ├── analysis.py            # Summary statistics and data health profiling
│   ├── visualizations.py      # Plotly interactive chart builders
│   ├── report_generator.py    # Plain text and PDF report export logic
│   └── qa_engine.py           # Natural language dataset query engine
├── tests/
│   ├── __init__.py
│   └── test_qa_engine.py      # Automated unit tests
├── uploads/
│   └── .gitkeep               # Preserves uploads directory in git
├── app.py                     # Main Streamlit dashboard application
├── qa_engine.py               # Compatibility wrapper
├── requirements.txt           # Project dependencies
└── .gitignore                 # Standard Python & Streamlit ignore file
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10, 3.11, or 3.12 installed on your machine.

### 2. Clone or Navigate to the Repository
```bash
git clone https://github.com/<your-username>/Datasense-AI.git
cd Datasense-AI
```

### 3. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Running Unit Tests

Run the test suite to verify core analysis and query engine functionality:
```bash
python -m unittest discover -s tests -v
```

---

## 🛠️ Built With

- [Streamlit](https://streamlit.io/) - Web application framework
- [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/) - Data manipulation and numerical operations
- [Plotly](https://plotly.com/python/) - Interactive charting
- [ReportLab](https://www.reportlab.com/) - PDF document generation
- [OpenPyXL](https://openpyxl.readthedocs.io/) - Excel file parsing
