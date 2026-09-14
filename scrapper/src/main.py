import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from datetime import datetime, timezone
import json
from pydantic import BaseModel, ValidationError
from typing import Optional

class BookRecord(BaseModel):
    title: str
    price_text: str
    price_gbp: float
    description: Optional[str]
    availability_text: str
    rating_text: str
    product_url: str
    source_page: str
    fetched_at: str

def fetch_html(url, cache_path):
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        print("CACHE HIT")
        return html_content, False
    else:
        try:
            headers = {"User-Agent": "FlyRankInternship-A9/1.0 (https://github.com/SeanRDC/W5-A9-The-polite-scraper)"}
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                raw_text = response.text
                with open(cache_path, 'w', encoding='utf-8') as file:
                    file.write(raw_text)
                print("FETCH")
                html_content = raw_text
                return html_content, True
        except Exception as e:
            print({"message": f"{str(e)}"})
    
current_url = "https://books.toscrape.com/catalogue/page-1.html"
pages_visited = 0
discovered_urls = []

while pages_visited < 3 and current_url is not None:
    dynamic_cache_path = f"cache/catalogue-page-{pages_visited + 1}.html"
    
    html, was_live_requests = fetch_html(current_url, dynamic_cache_path)
    
    if was_live_requests:
        time.sleep(0.5)
        
    soup = BeautifulSoup(html, "html.parser")
    h3_element = soup.find_all("h3")
    for h3 in h3_element:
        a_element = h3.find("a")
        if a_element and a_element.has_attr('href'):
            href = a_element['href']
            discovered_urls.append(urljoin(current_url, href))
    
    li_element = soup.find("li", class_="next")
    
    if li_element:
        a_li_element = li_element.find("a")
        if a_li_element and a_li_element.has_attr('href'):
            href = a_li_element['href']
            current_url = urljoin(current_url, href)
    else:
        current_url = None
        
    pages_visited += 1
    
discovered = list(set(discovered_urls))
print(f"catalogue_pages = {pages_visited}, discovered = {len(discovered_urls)}, unique_urls = {len(discovered)}")

raw_records = []

for book, url in enumerate(discovered):
    dynamic_cache_path = f"cache/book-{book}.html"
    html, was_live_requests = fetch_html(url, dynamic_cache_path)
    
    if was_live_requests:
        time.sleep(0.5)
        
    soup = BeautifulSoup(html, "html.parser")
    
    product_area = soup.find("article", class_="product_page")
    title = product_area.find("h1").text
    price = product_area.find("p", class_="price_color").text
    availability = product_area.find("p", class_="instock availability").text.strip()

    p_element = product_area.find("p",class_="star-rating")
    rating = p_element['class'][1]

    id_attribute = product_area.find(id = "product_description")
    if id_attribute:
        description = id_attribute.find_next("p").text
    else:
        description = None
        
    source_page = "https://books.toscrape.com/catalogue/page-1.html"
    
    fetched_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    
    build_dict = {
    "title": title,
    "product_url": url,
    "price_text": price,
    "availability_text": availability,
    "rating_text": rating,
    "description": description,
    "source_page": source_page,
    "fetched_at": fetched_at
    }

    raw_records.append(build_dict)

print(json.dumps(raw_records[0], indent=2))
print(f"detail_pages = {len(raw_records)}")


for record in raw_records:
    price_val = record["price_text"]
    record["price_gbp"] = float(price_val.replace("£", "").replace("Â", ""))

valid_records = []
errors = []

for record in raw_records:
    try:
        clean_book = BookRecord(**record)
        clean_dict = clean_book.model_dump()
        valid_records.append(clean_dict)
    except ValidationError as e:
        errors.append({"original_data": record, "error_message": str(e)})
        
os.makedirs("output", exist_ok=True)

with open("output/books.json", "w", encoding="utf-8") as file:
    json.dump(valid_records, file, indent=4)

with open("output/errors.json", "w", encoding="utf-8") as file:
    json.dump(errors, file, indent=4)
    
print(f"valid_records = {len(valid_records)}")