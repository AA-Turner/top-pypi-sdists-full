from .imports import *
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("selenium").setLevel(logging.WARNING)

# ---- Chrome options (keep yours; add safe fallbacks) ----



def _resolve_chrome_binary():
    candidates = [
        get_env_value('CHROME_BINARY'),
        '/usr/bin/chromium-browser',  # 146
        '/usr/bin/google-chrome',
        shutil.which('chromium-browser'),
        shutil.which('google-chrome'),
    ]
    for path in candidates:
        if path and os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    return None
chrome_options = Options()
_bin = _resolve_chrome_binary()
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
