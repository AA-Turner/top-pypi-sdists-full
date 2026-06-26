from __future__ import annotations
from contextlib import contextmanager
# selenium lazy — see abstract_webtools/_lazy.py. Loads on first driver build.
from abstract_webtools._lazy import LazyModule as _LazyModule, LazyAttr as _LazyAttr
webdriver = _LazyModule("selenium.webdriver")
Service = _LazyAttr("selenium.webdriver.chrome.service", "Service")
Options = _LazyAttr("selenium.webdriver.chrome.options", "Options")

CHROMIUM_BIN = '/usr/bin/chromium-browser'
CHROMEDRIVER_BIN = '/usr/local/bin/chromedriver'

def _build_options() -> Options:
    opts = Options()
    opts.binary_location = CHROMIUM_BIN
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-gpu')
    return opts

@contextmanager
def chrome_driver():
    service = Service(CHROMEDRIVER_BIN)
    driver = webdriver.Chrome(service=service, options=_build_options())
    try:
        yield driver
    finally:
        driver.quit()  # sends /shutdown to chromedriver, then SIGTERM to chrome

def get_url_source(url: str) -> str:
    with chrome_driver() as driver:
        driver.get(url)
        return driver.page_source
