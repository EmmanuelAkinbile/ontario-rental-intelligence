# Ontario Rental Intelligence

An end-to-end data pipeline that collects, cleans, and analyzes live Ontario rental listings to generate market-level housing insights.

---

## Business Objective

Build a reproducible rental market intelligence pipeline to:

- Standardize messy rental listing data
- Quantify price differences across regions and unit types
- Derive price-per-square-foot benchmarks
- Surface inventory mix and bedroom price premiums
- Produce an analysis-ready dataset for BI dashboards

---

## Key Insights Generated

Using SQL-based transformations and exploratory analysis:

- Toronto commands the highest median rent and price-per-square-foot
- Apartments dominate supply in Toronto (~45%), while basements lead in Peel and Durham
- Price-per-square-foot reveals density-driven premiums in core markets
- Rent increases non-linearly with bedroom count (clear bedroom premium curve)
- Inventory mix differs materially across regions, affecting pricing dynamics

---

## Tech Stack

- Python (data ingestion)
- requests + BeautifulSoup (scraping)
- DuckDB (analytical storage)
- SQL (data cleaning & transformation layer)
- Jupyter Notebook (EDA)
- GitHub (version control)

---

## Project Structure

/rental_pipeline.py → Data ingestion + storage

/rental_eda_queries.sql → Analytical SQL queries

/rental_eda.ipynb → Exploratory analysis + interpretation

/kijiji_rentals_clean.csv → Clean analytics-ready dataset (snapshot)

---

## Data Flow

Web Pages  
→ Python Scraper  
→ DuckDB (Raw Table)  
→ SQL Transformations  
→ Clean Table  
→ CSV Snapshot  
→ EDA / BI

---

## Design Decisions

- Snapshot-based architecture (point-in-time market view)
- SQL-driven transformation layer (production-style modeling)
- Explicit pagination and rate limiting
- URL-based deduplication
- Structured anomaly filtering (extreme price flag)

---

## Future Enhancements

- Historical tracking across multiple snapshots
- Automated anomaly detection
- Power BI dashboard
- Regional trend comparison over time
