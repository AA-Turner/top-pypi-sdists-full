from .imports import *
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("selenium").setLevel(logging.WARNING)

# ---- Chrome options (keep yours; add safe fallbacks) ----
chrome_options = Options()
_bin = get_env_value('CHROME_BINARY')
if _bin:
    chrome_options.binary_location = _bin
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.experimental_options["prefs"] = chrome_prefs

MIN_HTML_BYTES = 2048  # tune: consider <2KB suspicious for real pages
