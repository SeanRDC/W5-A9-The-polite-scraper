import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

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