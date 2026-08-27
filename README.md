# Retail Sales & Inventory Performance Analysis

A retail analytics project analyzing sales, profitability, and inventory
health across 10 stores and 170 products, using **Python (Pandas)** for
data cleaning and **SQL** for aggregation and analysis.

## Project overview

The dataset simulates one year (2024) of retail transactions across 5
regions in New Zealand (Auckland, Wellington, Christchurch, Hamilton,
Dunedin), including deliberately realistic **data quality problems** —
duplicate transactions, missing prices, inconsistent date formats, and
sign-entry errors — which were identified and resolved as the first stage
of the analysis, exactly as would be required with real retail data.

## Data cleaning (Python / Pandas)

Starting from 6,090 raw transaction rows, the cleaning process:

| Issue | Rows affected | Fix applied |
|---|---|---|
| Duplicate transactions | 82 | Removed via `drop_duplicates()` on transaction-identifying columns |
| Missing `unit_price` | 122 | Filled by joining back to the product catalog price |
| Inconsistent date formats (`DD/MM/YYYY` mixed with `YYYY-MM-DD`) | ~180 | Standardized via multi-format date parsing |
| Negative `quantity_sold` (sign entry errors) | 61 | Corrected using absolute value |

**Result: 6,008 clean transactions** ready for analysis (from 6,090 raw rows).

See [`analysis.py`](analysis.py) for the full cleaning + analysis code, and
[`analysis_findings.txt`](analysis_findings.txt) for the raw output.

## Key findings

- **Total revenue: $4,053,637** across 6,008 transactions, **$1,698,725
  profit** (41.9% margin)
- **Apparel** was the top revenue category ($957,818 / 23.6%), narrowly
  ahead of Grocery ($875,925 / 21.6%)
- **Auckland** generated the most regional revenue ($1,620,175) — more than
  double the next closest region (Dunedin, $843,096)
- Discounted transactions actually had a **lower** average value ($640.95)
  than full-price ones ($719.96) — discounts didn't drive larger basket sizes
  in this dataset
- **December was the peak sales month** ($595,435), consistent with holiday
  shopping seasonality
- **9.6% of all store-product combinations** (140 of 1,455) were at or below
  their reorder point at the snapshot date — Grocery had the most items at
  stockout risk (34 combinations)

## SQL analysis

The same core questions were also answered directly in SQL against a
SQLite version of the cleaned data — see [`retail_analysis.sql`](retail_analysis.sql).
This covers revenue by category/region, discount impact, top profit-driving
products, monthly trend, and inventory stockout risk — all verified to
produce numbers matching the Python analysis exactly.

## Files

| File | Description |
|---|---|
| `generate_retail_data.py` | Generates the synthetic dataset (with intentional data quality issues) |
| `stores.csv`, `products.csv`, `inventory.csv`, `sales_raw.csv` | Raw source tables |
| `analysis.py` | Pandas cleaning pipeline + full analysis |
| `sales_clean.csv` | Cleaned transaction data (output of `analysis.py`) |
| `analysis_findings.txt` | Full text output of the cleaning log and analysis |
| `retail.db` | SQLite database built from the cleaned data |
| `retail_analysis.sql` | SQL queries answering the same business questions |

## About the data

This is **synthetic data**, generated with Python (`Faker` + `NumPy`)
specifically for this project, including intentionally injected data quality
issues to practice realistic cleaning workflows. No real store or
transaction data is included.
