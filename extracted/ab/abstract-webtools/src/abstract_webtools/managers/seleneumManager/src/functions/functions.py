# --- NEW helpers: unique temp profile + free port + options builder ---
from ..imports import *
def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port

def _make_profile_dir(base="/var/tmp/selenium-profiles") -> str:
    os.makedirs(base, exist_ok=True)
    return tempfile.mkdtemp(prefix="cw-", dir=base)

def _make_chrome_options(binary_path: str | None = None,
                         user_data_dir: str | None = None) -> tuple[Options, str]:
    opts = Options()
    if binary_path:
        opts.binary_location = binary_path
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-software-rasterizer")
    opts.add_argument("--disable-extensions")

    prof = user_data_dir or _make_profile_dir()
    opts.add_argument(f"--user-data-dir={prof}")
    opts.add_argument(f"--remote-debugging-port={_free_port()}")

    prefs = {"profile.managed_default_content_settings.images": 2}
    opts.add_experimental_option("prefs", prefs)
    return opts, prof

def _looks_like_html(text_or_bytes: bytes | str) -> bool:
    if not text_or_bytes:
        return False
    s = text_or_bytes if isinstance(text_or_bytes, str) else text_or_bytes.decode("utf-8", "ignore")
    if len(s) < MIN_HTML_BYTES:
        return False
    lowered = s.lower()
    return ("<html" in lowered and "</html>" in lowered) or "<body" in lowered

def _requests_fallback(url: str, headers: dict | None = None, timeout: float = 15.0):
    """Plain requests fallback. Returns `requests.Response | None`."""
    try:
        sess = requests.Session()
        sess.headers.update(headers or {"User-Agent": "Mozilla/5.0"})
        # honor simple redirects and cert issues as needed
        resp = sess.get(url, timeout=timeout, allow_redirects=True, verify=False)
        return resp
    except Exception as e:
        logging.warning(f"requests fallback failed for {url}: {e}")
        return None

def _wait_until_ready(driver, timeout: float = 10.0):
    """Waits for DOM readiness and presence of <body>."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") in ("interactive", "complete")
        )
    except Exception:
        pass
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except Exception:
        pass
    # small settle delay for late JS injections
    time.sleep(0.3)

