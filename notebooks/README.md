# Ethiopia Financial Inclusion Forecasting

## Project Overview
This repository tracks Ethiopia's financial inclusion trends and forecasts Access (Account Ownership) and Usage (Digital Payments) using a structured and enriched dataset. Task 1 focuses on **data exploration and enrichment**.

## Task 1 – Data Exploration & Enrichment
**Objective:** Load, explore, and enrich Ethiopia's financial inclusion dataset to prepare it for further analysis and forecasting.

**Steps Completed:**
1. Loaded starter dataset (`ethiopia_fi_unified_data.csv`) and reference codes.
2. Explored observations, events, impact links, and targets.
3. Identified gaps in indicators and temporal coverage.
4. Enriched dataset by adding:
   - Additional observations (e.g., infrastructure, mobile money, demographics)
   - Additional events (policies, product launches, partnerships)
   - Additional impact links (relationships between events and indicators)
5. Logged all additions in `data_enrichment_log.md`.
6. Saved enriched dataset to `data/processed/ethiopia_fi_enriched_data.csv`.

## Folder Structure
- `data/raw/` – Original datasets  
- `data/processed/` – Enriched dataset ready for analysis  
- `notebooks/` – Jupyter notebooks for exploration and enrichment  
- `dashboard/` – Streamlit dashboard (Task 5)  
- `models/` – Folder for trained models  
- `reports/figures/` – Plots and figures  
- `data_enrichment_log.md` – Log of all data additions and sources  
- `requirements.txt` – Python packages required  

## Installation
```bash
# Clone repository
git clone <repo_url>
cd ethiopia-fi-forecast

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install required packages
pip install -r requirements.txt
