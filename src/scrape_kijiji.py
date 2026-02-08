"""
Ontario Rental Intelligence – Data Ingestion Script

Scrapes Ontario rental listings using paginated, rate-limited requests.
Designed to produce a point-in-time snapshot of the rental market.
"""

# import all necessary libraries
import time
import csv
import requests 
from bs4 import BeautifulSoup 

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

output_file = "kijiji_rentals_gta_raw.csv"

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames= all_rows[0].keys())
    writer.writeheader()
    writer.writerows(all_rows)
