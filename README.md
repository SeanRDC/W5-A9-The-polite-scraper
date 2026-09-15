# The Polite Scraper (FlyRank Internship W5-A9)

A fault-tolerant, polite web scraping pipeline built in Python. This ETL script downloads catalogue pages, extracts product data, normalizes raw text, enforces strict schema validation, and gracefully survives network failures.

**Author:** Sean Rhani Jarin Dela Cruz

# Target Classification

* **Target Site:** Books to Scrape (http://books.toscrape.com)
* **Purpose:** This site is a public practice sandbox built specifically for people to practice scraping.
* **Scope:** The first 3 catalogue pages only.
* **Data Collected:** Book details including titles, prices, availability, ratings, product URLs, and descriptions.
* **Robots.txt Result:** No robots file found.

*I will not reuse this code on another site without checking its rules and terms first.*

## Architecture & Limitations
This scraper uses `requests` and `BeautifulSoup4`. A headless browser (like Playwright or Selenium) was intentionally avoided because the required data is already fully present in the raw HTML payload sent by the server; simulating a browser would only add unnecessary computational cost and memory overhead.

**Limitation:** The scraper relies on static DOM selectors. If the website changes its HTML structure (e.g., altering the `product_page` class), the extraction logic will break and require maintenance.

## Politeness & Ethics Rules
I believe in respectful automation. This pipeline implements:
* **Identification:** Sends a custom `User-Agent` (`FlyRankInternship-A9/1.0`) with a link to this repository.
* **Rate Limiting:** Enforces a mandatory 0.5-second `time.sleep()` delay between all live requests.
* **Resource Protection:** Utilizes local filesystem caching (`cache/`) during development to prevent hammering the server with repeated requests.
* **Timeouts & Safety:** All live requests have a strict 5-second timeout and are wrapped in intelligent retry logic for 5xx server errors (ignoring 404s/403s).
* **Ethics:** Use official APIs when available, never bypass paywalls or authentication, and collect only the data strictly necessary for the task.

## Data Schema (Pydantic)
Every record is validated against this strict schema before serialization:
* `title`: str
* `price_text`: str
* `price_gbp`: float (normalized from string)
* `description`: Optional[str]
* `availability_text`: str
* `rating_text`: str
* `product_url`: str (canonical absolute URL)
* `source_page`: str
* `fetched_at`: str (ISO 8601 UTC timestamp)

## Setup & Execution

1. Clone the repository and navigate to the project folder.
    ```
   cd scrapper
2. Install the required dependencies:
    ```
   pip install requests beautifulsoup4 pydantic
3. Run the pipeline:
    ```
   python main.py
## Run Report Evidence
Below is the receipt of a successful execution demonstrating the fault-tolerant safety net (handling 1 intentionally broken URL):

```json
{
    "Duration": 1.84,
    "Pages fetched": 1,
    "Cache hits": 60,
    "Valid records": 60,
    "Invalid records": 0,
    "Failed pages": 1
}
```