# abstract_youtube/extract.py

import json
import re
from urllib.parse import urlparse, parse_qs

from abstract_webtools import requestManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
def make_driver():
    opts = Options()
    opts.binary_location = '/usr/bin/chromium-browser'
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-gpu')

    service = Service('/usr/local/bin/chromedriver')
    return webdriver.Chrome(service=service, options=opts)

def extract_googlevideo_urls_from_html(html: str) -> list[str]:
    """
    DEBUG / INSPECTION ONLY.
    Finds googlevideo URLs embedded in JS blobs.
    """
    urls = set()
    for m in re.findall(r'"(https://[^"]+googlevideo\.com[^"]+)"', html):
        try:
            urls.add(json.loads(f'"{m}"'))
        except Exception:
            continue
    return list(urls)


def extract_player_response(url: str) -> dict:

    driver = make_driver()
    driver.get(url)
    html = driver.page_source

    m = re.search(
        r"ytInitialPlayerResponse\s*=\s*(\{.+?\});",
        html,
        re.S,
    )
    if not m:
        raise RuntimeError("ytInitialPlayerResponse not found")

    return json.loads(m.group(1))


def iter_streaming_urls(player_response: dict):
    streaming = player_response.get("streamingData", {})
    formats = (
        streaming.get("formats", []) +
        streaming.get("adaptiveFormats", [])
    )

    for fmt in formats:
        if "url" in fmt:
            yield fmt["url"], fmt
        elif "signatureCipher" in fmt:
            yield fmt["signatureCipher"], fmt
