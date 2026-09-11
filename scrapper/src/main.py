import os
import requests

cache_path = "cache/catalogue-page-1.html"

if os.path.exists(cache_path):
    with open(cache_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    print("CACHE HIT")
else:
    try:
        headers = {"User-Agent": "FlyRankInternship-A9/1.0 (https://github.com/SeanRDC/W5-A9-The-polite-scraper)"}
        response = requests.get("https://books.toscrape.com/catalogue/page-1.html", headers=headers, timeout=5)
        
        if response.status_code == 200:
            raw_text = response.text
            with open(cache_path, 'w', encoding='utf-8') as file:
                file.write(raw_text)
            print("FETCH")
            html_content = raw_text
    except Exception as e:
        print({"message": f"{str(e)}"})
print(len(html_content))