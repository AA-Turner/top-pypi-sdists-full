from __future__ import annotations
from abstract_utilities import get_home_dir
from .imports import *
import os,tempfile,shutil,requests
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Dict, Any
# selenium lazy — see abstract_webtools/_lazy.py. Loads on first chrome_driver() use.
from abstract_webtools._lazy import LazyModule as _LazyModule, LazyAttr as _LazyAttr
webdriver = _LazyModule("selenium.webdriver")
Service = _LazyAttr("selenium.webdriver.chrome.service", "Service")
Options = _LazyAttr("selenium.webdriver.chrome.options", "Options")
logger = get_logFile(__name__)
def make_writable_runtime_dir(base: str = None) -> Path:
    tmp_path = "tmp/selenium-runtime"
    base = base or os.path.join(get_home_dir(),tmp_path)
    path = Path(base)
    path.mkdir(parents=True, exist_ok=True)
    path.chmod(0o700)
    return path
@contextmanager
def chrome_driver(
    headless: bool = True,
    referer: str | None = None,
    user_agent: str | None = None,
    headers: Optional[dict[str, str]] = None,
):
    runtime_root = make_writable_runtime_dir()

    profile_dir = tempfile.mkdtemp(prefix="chrome-profile-", dir=str(runtime_root))
    cache_dir = tempfile.mkdtemp(prefix="chrome-cache-", dir=str(runtime_root))

    options = Options()

    if headless:
        options.add_argument("--headless=new")

    options.add_argument(f"--user-data-dir={profile_dir}")
    options.add_argument(f"--disk-cache-dir={cache_dir}")

    if user_agent:
        options.add_argument(f"--user-agent={user_agent}")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")

    driver = None

    try:
        driver = webdriver.Chrome(options=options)

        if headers:
            driver.execute_cdp_cmd("Network.enable", {})

            extra_headers = {
                key: value
                for key, value in headers.items()
                if key.lower()
                not in {"user-agent", "host", "connection", "content-length"}
            }

            if referer and "Referer" not in extra_headers:
                extra_headers["Referer"] = referer

            if extra_headers:
                driver.execute_cdp_cmd(
                    "Network.setExtraHTTPHeaders",
                    {"headers": extra_headers},
                )

        yield driver

    finally:
        if driver is not None:
            driver.quit()

        shutil.rmtree(profile_dir, ignore_errors=True)
        shutil.rmtree(cache_dir, ignore_errors=True)




def get_rendered_html(
    url: str,
    timeout: int = 30,
    referer: str | None = None,
    user_agent: str | None = None,
    headers: Optional[dict[str, str]] = None,
) -> str:
    with chrome_driver(
        headless=True,
        referer=referer,
        user_agent=user_agent,
        headers=headers,
    ) as driver:
        driver.set_page_load_timeout(timeout)
        driver.get(url)
        return driver.page_source
def get_requested_html(
    url: str,
    session: requests.Session | None = None,
    headers: Optional[dict[str, str]] = None,
    timeout: int = 30,
    referer: str | None = None,
    user_agent: str | None = None,
) -> str:
    owns_session = session is None
    session = session or requests.Session()

    request_headers = dict(headers or {})

    if user_agent and "User-Agent" not in request_headers:
        request_headers["User-Agent"] = user_agent

    if referer and "Referer" not in request_headers:
        request_headers["Referer"] = referer

    try:
        with session.get(
            url,
            headers=request_headers or None,
            timeout=timeout,
        ) as response:
            response.raise_for_status()
            return response.text

    finally:
        if owns_session:
            session.close()

def fetch_html(
    url: str,
    session: requests.Session | None = None,
    headers: Optional[dict[str, str]] = None,
    timeout: int = 30,
    referer: str | None = None,
    user_agent: str | None = None,
) -> str:
    try:
        return get_rendered_html(
            url=url,
            timeout=timeout,
            referer=referer,
            user_agent=user_agent,
            headers=headers,
        )

    except Exception as exc:
        print(f"Selenium failed for {url}, falling back to requests: {exc}")

        return get_requested_html(
            url=url,
            session=session,
            headers=headers,
            timeout=timeout,
            referer=referer,
            user_agent=user_agent,
        )
