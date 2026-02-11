# Ontario Rental Intelligence

Ontario Rental Intelligence is an end-to-end data pipeline that collects, stores, and transforms live Ontario rental housing listings. 

The project focuses on real-world data ingestion, pagination, rate-limited scraping, SQL-based data cleaning, and reproducible snapshot generation to produce an analysis-ready dataset for downstream exploration and visualization.

---

## Project Objectives

- Build a reliable pipeline for ingesting live rental listings
- Handle real-world challenges such as pagination and rate limiting
- Produce a clean, structured dataset suitable for analysis and visualization
- Emphasize reproducibility and maintainable code structure

---

## Data Source

Rental listings are collected from publicly available online classifieds.  
The pipeline is designed to adapt to changing listing volumes and page counts.

---

## Pipeline Overview

1. Generate page URLs programmatically  
2. Request pages using browser-like headers  
3. Apply rate limiting between page requests  
4. Parse listing cards from each page  
5. Store raw listings in DuckDB  
6. Create a cleaned analytics table using SQL transformations  
7. Export both raw and cleaned datasets to CSV  
8. Produce a reproducible point-in-time market snapshot

---

## Extracted Fields (Raw Table)

- Listing title  
- Price (raw text)  
- Location  
- Unit type (e.g. apartment, condo, house)  
- Square footage (when available)  
- Number of bedrooms  
- Listing URL  

---

## Cleaned Fields (Analytics Table)

- price_monthly (integer, NULL-safe)
- bedrooms (numeric)
- sqft (integer)
- location_clean (standardized text)
- market_area (Toronto, Peel, York, Durham, Halton, Other)
- is_duplicate (URL-based deduplication flag)
- is_low_price_flag (possible non-residential or marketing listing)
- listing_url

---

## Tech Stack

- Python (data ingestion)
- requests
- BeautifulSoup
- DuckDB (embedded analytical database)
- SQL (data cleaning and transformation layer)
- GitHub (version control)

---

## Design Decisions

- Data is captured as a **point-in-time snapshot** rather than appended across runs  
- Rate limiting is applied to avoid overwhelming the source site  
- Raw fields are preserved to support flexible downstream transformations  
- Pagination is handled explicitly to ensure predictable execution
- Cleaning logic is implemented in SQL to simulate production-style transformation workflows

---

## Future Work

- Add historical tracking across multiple snapshot runs
- Implement price-per-square-foot derived metrics
- Add anomaly detection for extreme listings
- Build exploratory analysis notebook (EDA)
- Develop Power BI dashboard for rental market insights

---

## Data Flow Architecture

Web Pages → Python Scraper → DuckDB (Raw Table) → SQL Transformations → Clean Table → CSV Export → Analysis / BI

