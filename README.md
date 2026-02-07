# Ontario Rental Intelligence

Ontario Rental Intelligence is an end-to-end data pipeline that collects and structures live Ontario rental housing listings. The project focuses on real-world data ingestion, pagination, rate-limited scraping, and clean schema design to produce a reproducible snapshot of the rental market for downstream analysis.

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
5. Extract structured fields from each listing  
6. Produce a point-in-time snapshot that replaces previous runs  

---

## Extracted Fields (v1)

- Listing title  
- Price (raw text)  
- Location  
- Unit type (e.g. apartment, condo, house)  
- Square footage (when available)  
- Number of bedrooms  
- Listing URL  

---

## Tech Stack

- Python  
- requests  
- BeautifulSoup  
- GitHub (version control)

---

## Design Decisions

- Data is captured as a **point-in-time snapshot** rather than appended across runs  
- Rate limiting is applied to avoid overwhelming the source site  
- Raw fields are preserved to support flexible downstream transformations  
- Pagination is handled explicitly to ensure predictable execution  

---

## Future Work

- Persist data to a database
- Add data cleaning and normalization steps
- Perform exploratory data analysis
- Build dashboards and visualizations
- Extend the pipeline to support historical tracking
