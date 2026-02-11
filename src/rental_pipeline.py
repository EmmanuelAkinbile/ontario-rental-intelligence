"""
Ontario Rental Intelligence – Data Ingestion Script

Scrapes Ontario rental listings using paginated, rate-limited requests.
Designed to produce a point-in-time snapshot of the rental market.
"""

# import all necessary libraries
import time
import csv
import requests 
import duckdb
from bs4 import BeautifulSoup 

con = duckdb.connect("ontario_rentals.duckdb")

con.execute("DROP TABLE IF EXISTS rentals_raw;")
con.execute("""
            CREATE TABLE IF NOT EXISTS rentals_raw(
            title TEXT,
            price_raw TEXT,
            location TEXT,
            unit_type TEXT, 
            sqft_raw TEXT,
            bedrooms_raw TEXT,
            url TEXT,
            scraped_at TIMESTAMP
            );
            """)
con.execute("DELETE FROM rentals_raw;")

# define url of webpage to scrape from
url = "https://www.kijiji.ca/b-apartments-condos/gta-greater-toronto-area/c37l1700272?msockid=0133c66d12326754043ed03d131d665b"

# use browser-like headers to reduce request blocking
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-CA,en;q=0.9",
    "Connection": "keep-alive",
}

base_url = "https://www.kijiji.ca/b-apartments-condos/gta-greater-toronto-area/c37l1700272?msockid=0133c66d12326754043ed03d131d665b"
max_pages = 100

all_rows = []

for page_num in range(1, max_pages + 1):

    if page_num == 1:
        url = base_url
    else:
        url = base_url.replace("/gta-greater-toronto-area/", f"/gta-greater-toronto-area/page-{page_num}/")

    response = requests.get(url, headers=headers, timeout=30)

    # use BeautifulSoup to parse the text from the response 
    parsed_response = BeautifulSoup(response.text, "html.parser") 

    cards = parsed_response.find_all("section", attrs= {"data-testid":"listing-card"})

    
    for card in cards:
        link_tag = card.find("a", attrs={"data-testid": "listing-link"})
        title = link_tag.get_text(strip=True)
        href = link_tag["href"]

        price_tag = card.find("p", attrs= {"data-testid": "listing-price"})
        price = price_tag.get_text(strip=True) if price_tag else None

        details_tag = card.find("div", attrs={"data-testid": "listing-details"})
        location_text = details_tag.get_text(strip=True) if details_tag else None

        unit_li = card.find("li", attrs= {"aria-label": "Unit type"})
        unit_type = unit_li.get_text(strip=True) if unit_li else None

        size = card.find("li", attrs= {"aria-label": "Size (sqft)"})
        sqft = size.get_text(strip=True) if size else None

        bed = card.find("li", attrs= {"aria-label": "Bedrooms"})
        beds = bed.get_text(strip=True) if bed else None

        row = {
            "title": title,
            "price_raw": price,
            "location": location_text,
            "unit_type": unit_type,
            "sqft_raw": sqft,
            "bedrooms_raw": beds,
            "url": href
            }
        all_rows.append(row)
        
    time.sleep(2)

con.executemany(
    """
    INSERT INTO rentals_raw
    (title, price_raw, location, unit_type, sqft_raw, bedrooms_raw, url, scraped_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP);
    """,
    [
        (
            row["title"],
            row["price_raw"],
            row["location"],
            row["unit_type"],
            row["sqft_raw"],
            row["bedrooms_raw"],
            row["url"],
        )
        for row in all_rows
    ],
)

output_file = "kijiji_rentals_raw.csv"

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames= all_rows[0].keys())
    writer.writeheader()
    writer.writerows(all_rows)

con.execute(r"""
CREATE OR REPLACE TABLE kijiji_rentals_clean AS
    SELECT
        title,
        price_monthly,
        bedrooms,
        sqft,
        unit_type_clean
        location_clean,
        market_area,
        CASE WHEN price_monthly IS NOT NULL AND price_monthly < 300 THEN 1 ELSE 0 END AS extreme_low_price_flag,
        url
    FROM (
        SELECT
            title,
            CASE
                WHEN price_raw IS NULL THEN NULL
                WHEN lower(trim(price_raw)) = 'please contact' THEN NULL
                ELSE CAST(
                regexp_replace(
                    regexp_replace(price_raw, '[$,]', '', 'g'),
                    '\.00$', ''
                ) AS INTEGER
                )
            END AS price_monthly,
            try_cast(nullif(trim(bedrooms_raw),'') AS DOUBLE) AS bedrooms,
            try_cast(regexp_replace(lower(trim(sqft_raw)), 'sqft', '') AS INTEGER) AS sqft,
                        
                -- Minimal cleanup: remove trailing dot, trim whitespace         
                TRIM(REGEXP_REPLACE(location, '\.•$', '')) AS location_clean,

                -- Standardized GTA bucket for analysis          
                CASE
                        
                -- Toronto (includes common Toronto sub-areas + “City of Toronto” wording)           
                WHEN LOWER(location) LIKE '%toronto%' 
                    OR LOWER(location) LIKE '%city of toronto%'
                    OR LOWER(location) LIKE '%north york%'
                    OR LOWER(location) LIKE '%scarborough%'
                    OR LOWER(location) LIKE '%etobicoke%'
                    OR LOWER(location) LIKE '%east york%'
                    OR LOWER(location) LIKE '%york%'
                    OR LOWER(location) LIKE '%downtown%'
                THEN 'Toronto'

                -- Peel Region
                WHEN LOWER(location) LIKE '%mississauga%'
                    OR LOWER(location) LIKE '%brampton%'
                    OR LOWER(location) LIKE '%caledon%'
                    OR LOWER(location) LIKE '%peel%'
                THEN 'Peel'

                -- York Region
                WHEN LOWER(location) LIKE '%markham%'
                    OR LOWER(location) LIKE '%vaughan%'
                    OR LOWER(location) LIKE '%richmond hill%'
                    OR LOWER(location) LIKE '%newmarket%'
                    OR LOWER(location) LIKE '%aurora%'
                    OR LOWER(location) LIKE '%whitchurch%'
                    OR LOWER(location) LIKE '%stouffville%'
                    OR LOWER(location) LIKE '%king%'
                    OR LOWER(location) LIKE '%schomberg%'
                    OR LOWER(location) LIKE '%york region%'
                THEN 'York'

                -- Durham Region
                WHEN LOWER(location) LIKE '%pickering%'
                    OR LOWER(location) LIKE '%ajax%'
                    OR LOWER(location) LIKE '%whitby%'
                    OR LOWER(location) LIKE '%oshawa%'
                    OR LOWER(location) LIKE '%clarington%'
                    OR LOWER(location) LIKE '%durham%'
                THEN 'Durham'

                -- Halton Region
                WHEN LOWER(location) LIKE '%oakville%'
                    OR LOWER(location) LIKE '%burlington%'
                    OR LOWER(location) LIKE '%milton%'
                    OR LOWER(location) LIKE '%halton%'
                THEN 'Halton'

                -- Anything else that slips through (still useful to keep)
                ELSE 'Other / Unknown'
                END AS market_area,
                NULLIF(TRIM(unit_type), '') AS unit_type_clean,
                url  
        FROM rentals_raw) t
    QUALIFY ROW_NUMBER() OVER (PARTITION BY url ORDER BY url) = 1;
""")

# export cleaned analyticcal table to CSV for downstream tools (Power BI)
con.execute(r"""
COPY kijiji_rentals_clean
TO 'kijiji_rentals_clean.csv'
WITH (HEADER, DELIMITER ',');
""")

con.close()