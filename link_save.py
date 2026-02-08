import os
import re
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITEMAP_FILE = os.path.join(BASE_DIR, "sitemap.xml")
OUT_FILE = os.path.join(BASE_DIR, "article_urls.txt")

# Matches: https://support.zipcar.com/hc/en-us/articles/123456789-Whatever
ARTICLE_RE = re.compile(r"^https?://[^/]+/hc/[^/]+/articles/\d+")

NS = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

tree = ET.parse(SITEMAP_FILE)
root = tree.getroot()

article_urls = []
seen = set()

for url in root.findall("ns:url", NS):
    loc_el = url.find("ns:loc", NS)
    if loc_el is None or not loc_el.text:
        continue

    loc = loc_el.text.strip()

    if ARTICLE_RE.match(loc) and loc not in seen:
        seen.add(loc)
        article_urls.append(loc)

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(article_urls) + "\n")

print(f"Remember: ignoring categories/sections; keeping only articles.")
print(f"Saved {len(article_urls)} article URLs to: {OUT_FILE}")
print("First:", article_urls[0] if article_urls else "NONE")
print("Last :", article_urls[-1] if article_urls else "NONE")