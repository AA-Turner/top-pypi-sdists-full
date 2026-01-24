from ..imports import *
from .functions import *
from .functions import _free_port,_make_chrome_options,_looks_like_html,_requests_fallback,_wait_until_ready,_make_profile_dir
from .seleneumManager import *
# ---- Hardened page-source retrieval with fallback ----
def get_selenium_source(url, max_retries: int = 2, request_fallback: bool = True, timeout: float = 12.0):
    url_mgr = urlManager(url)
    if not url_mgr.url:
        return None
    url = str(url_mgr.url)

    manager = seleneumManager(url)
    key, driver = manager.get_driver(url)

    last_exc = None
    try:
        for attempt in range(1, max_retries + 1):
            try:
                driver.get(url)
                _wait_until_ready(driver, timeout=timeout)
                html = driver.page_source or ""
                if not _looks_like_html(html):
                    html = driver.execute_script(
                        "return document.documentElement ? document.documentElement.outerHTML : '';"
                    ) or html
                if _looks_like_html(html):
                    return html
                logging.warning(f"Selenium returned suspicious HTML (len={len(html)}) for {url} "
                                f"[attempt {attempt}/{max_retries}]")
            except Exception as e:
                last_exc = e
                logging.warning(f"Selenium attempt {attempt}/{max_retries} failed for {url}: {e}")
            time.sleep(0.5 * attempt)

        if request_fallback:
            resp = _requests_fallback(url, headers={"User-Agent": "Mozilla/5.0"})
            if resp is not None:
                ctype = (resp.headers.get("content-type") or "").lower()
                body = resp.text if hasattr(resp, "text") else (
                    resp.content.decode("utf-8", "ignore") if hasattr(resp, "content") else ""
                )
                if "application/json" in ctype:
                    try:
                        return json.dumps(resp.json())
                    except Exception:
                        return body
                return body if _looks_like_html(body) or body else None
    finally:
        # critical: release the user-data-dir to avoid “already in use”
        manager.close_driver(key)

    if last_exc:
        logging.error(f"Unable to retrieve page for {url}: {last_exc}")
    return None

def get_driver(self, url):
    # always new
    bin_path = get_env_value('CHROME_BINARY')
    opts, prof = _make_chrome_options(binary_path=bin_path, user_data_dir=None)
    driver = webdriver.Chrome(options=opts)
    # store so close_all() can clean up
    key = f"{url}#{time.time()}"
    self._sessions[key] = {"driver": driver, "profile": prof}
    return driver
