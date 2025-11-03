# scanner/crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def crawl(base_url, max_pages=20):
    """
    Crawl a target website and return a list of discovered internal links.
    - Follows only links that belong to the same domain.
    - Avoids duplicates and stops after max_pages to prevent infinite loops.
    """
    visited = set()
    to_visit = [base_url]
    found_links = []

    # Normalize base domain
    parsed_base = urlparse(base_url)
    base_domain = parsed_base.netloc

    while to_visit and len(visited) < max_pages:
        current = to_visit.pop(0)
        if current in visited:
            continue

        visited.add(current)

        try:
            response = requests.get(current, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            if "text/html" not in response.headers.get("Content-Type", ""):
                continue  # skip non-HTML pages

            soup = BeautifulSoup(response.text, "html.parser")

            for link_tag in soup.find_all("a", href=True):
                href = link_tag.get("href").strip()
                new_link = urljoin(current, href)
                parsed_new = urlparse(new_link)

                # Only follow same-domain links (avoid external sites)
                if parsed_new.netloc == base_domain and new_link not in visited:
                    found_links.append(new_link)
                    to_visit.append(new_link)

        except requests.exceptions.RequestException:
            continue  # skip broken URLs and timeouts

    return list(set(found_links))  # ensure uniqueness
