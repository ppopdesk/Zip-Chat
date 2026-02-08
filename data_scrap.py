import os, re, json, time, random
import requests
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
URLS_FILE = os.path.join(BASE_DIR, "article_urls.txt")
OUT_FILE  = os.path.join(BASE_DIR, "zipcar_articles.jsonl")

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
})

ARTICLE_ID_RE = re.compile(r"/articles/(\d+)", re.IGNORECASE)

def article_id_from_url(url: str) -> str:
    m = ARTICLE_ID_RE.search(url)
    if not m:
        raise ValueError(f"Could not extract article id from: {url}")
    return m.group(1)

def fetch_article_json(article_url: str, locale: str = "en-us"):
    aid = article_id_from_url(article_url)
    api_url = f"https://support.zipcar.com/api/v2/help_center/{locale}/articles/{aid}.json"
    r = session.get(api_url, timeout=30)
    r.raise_for_status()
    return r.json()["article"], api_url

def strip_html(html: str) -> str:
    # Zendesk 'body' often comes as HTML
    soup = BeautifulSoup(html or "", "html.parser")
    return soup.get_text(" ", strip=True)

def main():
    with open(URLS_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    ok = fail = 0
    with open(OUT_FILE, "w", encoding="utf-8") as out:
        for i, url in enumerate(urls, 1):
            try:
                article, api_url = fetch_article_json(url, locale="en-us")
                text = strip_html(article.get("body", ""))

                doc = {
                    "url": url,
                    "api_url": api_url,
                    "title": article.get("title", ""),
                    "last_updated": article.get("updated_at", ""),
                    "section_id": article.get("section_id"),
                    "body": text,
                    "source": "support.zipcar.com"
                }

                if not doc["body"]:
                    raise ValueError("Empty body from API")

                out.write(json.dumps(doc, ensure_ascii=False) + "\n")
                ok += 1
                if i % 25 == 0:
                    print(f"[{i}/{len(urls)}] ok={ok} fail={fail}")

                time.sleep(0.4 + random.random() * 0.5)

            except Exception as e:
                fail += 1
                print(f"[{i}/{len(urls)}] FAIL {url} :: {e}")
                time.sleep(1.0 + random.random() * 1.0)

    print(f"Done. ok={ok} fail={fail}. Output: {OUT_FILE}")

if __name__ == "__main__":
    main()
