# pip install selenium webdriver-manager beautifulsoup4
import json, re, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def make_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1400,900")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/123.0.0.0 Safari/537.36")
    caps = {
        "goog:loggingPrefs": {"performance": "ALL"},
    }
    driver = webdriver.Chrome(ChromeDriverManager().install(),
                              options=chrome_options,
                              desired_capabilities=caps)
    return driver

def get_all_meta_selenium(url: str) -> dict:
    driver = make_driver()
    try:
        driver.get(url)
        time.sleep(2)  # let SSR/consent bits settle
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        out = {"title": soup.title.text.strip() if soup.title else None,
               "meta": [], "links": [], "json_ld": [], "citation": {}}

        for m in soup.find_all("meta"):
            entry = {k: m.get(k) for k in ("name","property","http-equiv","itemprop","charset","content")}
            entry = {k: v for k, v in entry.items() if v}
            if entry:
                out["meta"].append(entry)
                k = (entry.get("name") or entry.get("property") or "").lower()
                if k.startswith("citation_") and "content" in entry:
                    out["citation"].setdefault(k, []).append(entry["content"])

        for l in soup.find_all("link"):
            rel = l.get("rel")
            if isinstance(rel, list): rel = " ".join(rel)
            out["links"].append({
                "rel": rel, "href": l.get("href"),
                "type": l.get("type"), "title": l.get("title"), "hreflang": l.get("hreflang")
            })

        for s in soup.find_all("script", type=re.compile(r"application/ld\+json", re.I)):
            txt = s.get_text(strip=True)
            try: out["json_ld"].append(json.loads(txt))
            except Exception: out["json_ld"].append({"raw": txt})

        # Example: collect request headers via CDP logs (optional)
        logs = driver.get_log("performance")
        # parse logs if you want request/response headers

        return out
    finally:
        driver.quit()

