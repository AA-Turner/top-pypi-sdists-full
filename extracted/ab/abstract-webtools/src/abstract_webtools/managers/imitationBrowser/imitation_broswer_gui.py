import sys
import logging
import time
import random
import json
import csv
import re
from typing import Optional, Dict, List, Any, Callable, Tuple
from dataclasses import dataclass
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlparse

# ---------- PyQt6 ----------
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTextEdit, QCheckBox, QComboBox, QLabel,
    QFileDialog, QSpinBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# ---------- Selenium (optional engine) ----------
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# ---------- Requests / parsing ----------
from bs4 import BeautifulSoup
import requests
from urllib.robotparser import RobotFileParser

# ---------- Playwright (optional engine) ----------
try:
    from playwright.sync_api import sync_playwright, Browser, Page
    PLAYWRIGHT_AVAILABLE = True
except Exception:
    PLAYWRIGHT_AVAILABLE = False

# ---------- Configure logging ----------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================================================
# Shared config + robots
# =========================================================

@dataclass
class EmulatorConfig:
    engine: str = "Playwright"  # "Playwright" or "Selenium"
    headless: bool = True
    proxy: Optional[str] = None
    proxy_pool: Optional[List[str]] = None
    stealth_mode: bool = True
    disable_images: bool = True
    user_agent: Optional[str] = None
    timeout: int = 10

class PoliteFetcher:
    def __init__(self, session: requests.Session, user_agent: str):
        self.session = session
        self.user_agent = user_agent
        self.parsers: Dict[str, RobotFileParser] = {}

    def allowed(self, url: str) -> bool:
        base = urlparse(url)._replace(path='', params='', query='', fragment='').geturl()
        if base not in self.parsers:
            rp = RobotFileParser()
            try:
                resp = self.session.get(urljoin(base, '/robots.txt'), timeout=6)
                rp.parse(resp.text.splitlines()) if resp.ok else rp.parse([])
            except Exception:
                rp.parse([])
            self.parsers[base] = rp
        return self.parsers[base].can_fetch(self.user_agent, url)

    @staticmethod
    def sleep(min_s=0.8, max_s=2.2):
        time.sleep(random.uniform(min_s, max_s))

# =========================================================
# Base engine interface
# =========================================================

class BaseEngine:
    DEFAULT_USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'
    ]

    def __init__(self, cfg: EmulatorConfig):
        self.cfg = cfg
        self.user_agent = cfg.user_agent or random.choice(self.DEFAULT_USER_AGENTS)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
        self.proxy_pool = cfg.proxy_pool or ([cfg.proxy] if cfg.proxy else [])
        if self.proxy_pool:
            picked = random.choice(self.proxy_pool)
            self.session.proxies = {'http': picked, 'https': picked}
        self.polite = PoliteFetcher(self.session, self.user_agent)

    # interface
    def scrape(self, url: str, wait_for: Optional[str], selectors: Dict[str, str]) -> Dict[str, Any]:
        raise NotImplementedError

    def crawl(self, start_url: str, selectors: Dict[str,str], next_selector: Optional[str], same_host_only: bool, max_pages: int, max_depth: int) -> Dict[str, Any]:
        seen, out, q = set(), [], deque([(start_url, 0)])
        base_host = urlparse(start_url).netloc
        # try sitemaps
        for u in self.discover_sitemap_urls(start_url):
            q.append((u, 0))

        while q and len(out) < max_pages:
            url, depth = q.popleft()
            if url in seen or depth > max_depth:
                continue
            seen.add(url)
            if not self.polite.allowed(url):
                out.append({'url': url, 'status': 'skipped_by_robots'})
                continue
            self.polite.sleep()

            res = self.scrape(url, wait_for=None, selectors=selectors)
            # carry minimal result to output; if selenium/playwright, we can attach 'html' too
            entry = {
                'url': url,
                'status': res.get('status'),
                'title': res.get('title'),
                'data': res.get('data'),
            }
            if 'html' in res:
                entry['html'] = res['html']
            out.append(entry)

            if res.get('status') in ('success','fallback_success'):
                soup: BeautifulSoup = res['soup']
                # pagination
                if next_selector:
                    nxt = soup.select_one(next_selector)
                    if nxt and nxt.get('href'):
                        q.append((urljoin(url, nxt['href']), depth+1))
                # same-host breadth
                for a in soup.select('a[href]'):
                    href = urljoin(url, a['href'])
                    if same_host_only and urlparse(href).netloc != base_host:
                        continue
                    if href.startswith(('mailto:', 'javascript:')):
                        continue
                    if href not in seen:
                        q.append((href, depth+1))

            # politeness between pages
            self.polite.sleep(0.5, 1.6)

        return {'status': 'ok', 'pages': out}

    def discover_sitemap_urls(self, root: str) -> List[str]:
        base = urlparse(root)._replace(path='', params='', query='', fragment='').geturl()
        urls = [urljoin(base, p) for p in ('/sitemap.xml', '/sitemap_index.xml')]
        out = []
        for u in urls:
            try:
                r = self.session.get(u, timeout=6)
                if r.ok and ('<urlset' in r.text or '<sitemapindex' in r.text):
                    soup = BeautifulSoup(r.text, 'xml')
                    for loc in soup.select('url > loc, sitemap > loc'):
                        out.append(loc.text.strip())
            except Exception:
                pass
        return out

    def quit(self):
        pass

    # helpers
    @staticmethod
    def _extract(soup: BeautifulSoup, selectors: Dict[str,str]) -> Dict[str, Any]:
        data = {}
        for key, selector in selectors.items():
            els = soup.select(selector)
            data[key] = [el.get_text(strip=True) for el in els] if els else None
        return data


# =========================================================
# Selenium engine (wraps your previous logic)
# =========================================================

class SeleniumEngine(BaseEngine):
    DEFAULT_WINDOW_SIZES = [
        (1920, 1080), (1366, 768), (1440, 900), (1536, 864), (1280, 720)
    ]

    def __init__(self, cfg: EmulatorConfig):
        super().__init__(cfg)
        self.driver = None
        self.wait: Optional[WebDriverWait] = None
        self._init_driver()

    def _pick_proxy(self) -> Optional[str]:
        return random.choice(self.proxy_pool) if self.proxy_pool else self.cfg.proxy

    def _init_driver(self):
        options = Options()
        if self.cfg.headless:
            options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument(f'--user-agent={self.user_agent}')
        width, height = random.choice(self.DEFAULT_WINDOW_SIZES)
        options.add_argument(f'--window-size={width},{height}')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        proxy = self._pick_proxy()
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        # CDP: block heavy resources
        try:
            self.driver.execute_cdp_cmd("Page.enable", {})
            self.driver.execute_cdp_cmd("Network.enable", {})
            if self.cfg.disable_images:
                self.driver.execute_cdp_cmd("Network.setBlockedURLs", {
                    "urls": ["*.png","*.jpg","*.jpeg","*.gif","*.webp","*.svg","*.woff","*.woff2","*.ttf","*.otf","*.avi","*.mp4","*.mp3","*.mov"]
                })
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": self.user_agent})
        except Exception:
            pass
        self.driver.implicitly_wait(5)
        self.wait = WebDriverWait(self.driver, self.cfg.timeout)

    def scrape(self, url: str, wait_for: Optional[str], selectors: Dict[str, str]) -> Dict[str, Any]:
        if not self.polite.allowed(url):
            return {'url': url, 'status': 'skipped_by_robots'}
        self.polite.sleep()
        try:
            self.driver.get(url)
            # wait for doc complete + brief idle
            self.driver.execute_script("""
                return new Promise(resolve=>{
                    const check=()=>{ if(document.readyState==='complete') resolve(); else setTimeout(check,100); };
                    check();
                });
            """)
            time.sleep(0.6)
            if wait_for:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, wait_for)))
            # tiny human-ish activity
            self.driver.execute_script("document.body.dispatchEvent(new Event('mousemove'));")
            time.sleep(0.2)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string.strip() if soup.title else None
            data = self._extract(soup, selectors) if selectors else {}
            return {'url': url, 'status': 'success', 'title': title, 'data': data, 'soup': soup, 'html': html, 'cookies': self.driver.get_cookies()}
        except Exception as e:
            logger.warning(f"[Selenium] Failed {url}: {e}")
            # fallback with requests
            try:
                r = self.session.get(url, timeout=self.cfg.timeout)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, 'html.parser')
                title = soup.title.string.strip() if soup.title else None
                data = self._extract(soup, selectors) if selectors else {}
                return {'url': url, 'status': 'fallback_success', 'title': title, 'data': data, 'soup': soup, 'cookies': r.cookies.get_dict()}
            except Exception as e2:
                return {'url': url, 'status': 'failed', 'error': str(e2)}

    def screenshot(self, url: str, out_path: str):
        try:
            self.driver.get(url)
            time.sleep(0.5)
            self.driver.save_screenshot(out_path)
        except Exception:
            pass

    def quit(self):
        try:
            if self.driver: self.driver.quit()
        except Exception:
            pass
        self.driver = None


# =========================================================
# Playwright engine
# =========================================================

class PlaywrightEngine(BaseEngine):
    def __init__(self, cfg: EmulatorConfig):
        super().__init__(cfg)
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError("Playwright is not installed. `pip install playwright` and `python -m playwright install chromium`.")
        self._pl = sync_playwright().start()
        self.browser: Optional[Browser] = None
        self.context = None
        self.page: Optional[Page] = None
        self._init_browser()

    @staticmethod
    def _parse_proxy(p: str) -> Dict[str, str]:
        # supports http://user:pass@host:port or http(s)://host:port
        u = urlparse(p)
        d = {"server": f"{u.scheme}://{u.hostname}:{u.port}"}
        if u.username or u.password:
            d["username"] = u.username or ""
            d["password"] = u.password or ""
        return d

    def _init_browser(self):
        launch_args = {
            "headless": self.cfg.headless,
            "args": [
                "--disable-dev-shm-usage",
                "--no-sandbox",
            ]
        }
        if self.proxy_pool:
            launch_args["proxy"] = self._parse_proxy(random.choice(self.proxy_pool))
        elif self.cfg.proxy:
            launch_args["proxy"] = self._parse_proxy(self.cfg.proxy)

        self.browser = self._pl.chromium.launch(**launch_args)
        ctx_args = {
            "user_agent": self.user_agent,
            "java_script_enabled": True,
            "viewport": {"width": 1280, "height": 800}
        }
        self.context = self.browser.new_context(**ctx_args)

        # Block heavy resources for speed
        if self.cfg.disable_images:
            def _route(route, request):
                if request.resource_type in ("image","font","media"):
                    return route.abort()
                return route.continue_()
            self.context.route("**/*", _route)

        self.page = self.context.new_page()

    def _goto(self, url: str, wait_for: Optional[str]):
        self.page.goto(url, wait_until="domcontentloaded", timeout=self.cfg.timeout * 1000)
        # brief network idle
        self.page.wait_for_timeout(600)
        if wait_for:
            self.page.wait_for_selector(wait_for, timeout=self.cfg.timeout * 1000)

    def scrape(self, url: str, wait_for: Optional[str], selectors: Dict[str, str]) -> Dict[str, Any]:
        if not self.polite.allowed(url):
            return {'url': url, 'status': 'skipped_by_robots'}
        self.polite.sleep()
        try:
            self._goto(url, wait_for)
            # light human-ish activity
            self.page.mouse.move(50, 50)
            self.page.wait_for_timeout(150)
            html = self.page.content()
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string.strip() if soup.title else None
            data = self._extract(soup, selectors) if selectors else {}
            cookies = {c['name']: c['value'] for c in self.context.cookies()}
            return {'url': url, 'status': 'success', 'title': title, 'data': data, 'soup': soup, 'html': html, 'cookies': cookies}
        except Exception as e:
            logger.warning(f"[Playwright] Failed {url}: {e}")
            # fallback with requests
            try:
                r = self.session.get(url, timeout=self.cfg.timeout)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, 'html.parser')
                title = soup.title.string.strip() if soup.title else None
                data = self._extract(soup, selectors) if selectors else {}
                return {'url': url, 'status': 'fallback_success', 'title': title, 'data': data, 'soup': soup, 'cookies': r.cookies.get_dict()}
            except Exception as e2:
                return {'url': url, 'status': 'failed', 'error': str(e2)}

    def screenshot(self, url: str, out_path: str):
        try:
            self._goto(url, wait_for=None)
            self.page.screenshot(path=out_path, full_page=True)
        except Exception:
            pass

    def quit(self):
        try:
            if self.context: self.context.close()
        except Exception:
            pass
        try:
            if self.browser: self.browser.close()
        except Exception:
            pass
        try:
            if self._pl: self._pl.stop()
        except Exception:
            pass
        self.browser = None
        self.page = None
        self.context = None


# =========================================================
# QThreads using the engine abstraction
# =========================================================

class ScrapeWorker(QThread):
    result_signal = pyqtSignal(dict)
    log_signal = pyqtSignal(str)

    def __init__(self, cfg: EmulatorConfig, task: Dict):
        super().__init__()
        self.cfg = cfg
        self.task = task
        self._cancel = False

    def cancel(self): self._cancel = True

    def _make_engine(self) -> BaseEngine:
        if self.cfg.engine == "Playwright":
            return PlaywrightEngine(self.cfg)
        return SeleniumEngine(self.cfg)

    def run(self):
        engine: Optional[BaseEngine] = None
        try:
            if self._cancel: return
            engine = self._make_engine()
            if self._cancel: return
            res = engine.scrape(
                url=self.task['url'],
                wait_for=self.task.get('wait_for'),
                selectors=self.task.get('selectors', {})
            )
            self.result_signal.emit(res)
        except Exception as e:
            self.result_signal.emit({'url': self.task.get('url'), 'status': 'failed', 'error': f"[{type(e).__name__}] {str(e)}"})
        finally:
            self.log_signal.emit(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Scraping completed for {self.task.get('url')}")
            if engine: engine.quit()


class CrawlWorker(QThread):
    result_signal = pyqtSignal(dict)
    log_signal = pyqtSignal(str)

    def __init__(self, cfg: EmulatorConfig, task: Dict):
        super().__init__()
        self.cfg = cfg
        self.task = task
        self._cancel = False

    def cancel(self): self._cancel = True

    def _make_engine(self) -> BaseEngine:
        if self.cfg.engine == "Playwright":
            return PlaywrightEngine(self.cfg)
        return SeleniumEngine(self.cfg)

    def run(self):
        engine: Optional[BaseEngine] = None
        try:
            if self._cancel: return
            engine = self._make_engine()
            if self._cancel: return
            res = engine.crawl(
                start_url=self.task['url'],
                selectors=self.task.get('selectors', {}),
                next_selector=self.task.get('next_selector'),
                same_host_only=self.task.get('same_host_only', True),
                max_pages=self.task.get('max_pages', 50),
                max_depth=self.task.get('max_depth', 2)
            )
            self.result_signal.emit(res)
        except Exception as e:
            self.result_signal.emit({'url': self.task.get('url'), 'status': 'failed', 'error': f"[{type(e).__name__}] {str(e)}"})
        finally:
            self.log_signal.emit(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Crawling completed for {self.task.get('url')}")
            if engine: engine.quit()

# =========================================================
# PyQt6 GUI
# =========================================================

class ScraperGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robust Web Scraper (PyQt6: Playwright / Selenium)")
        self.setGeometry(100, 100, 1000, 760)
        self.profiles = {}
        self.last_result = None
        self.workers: List[QThread] = []
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Engine selector
        engine_row = QHBoxLayout()
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["Playwright", "Selenium"])
        engine_row.addWidget(QLabel("Engine:"))
        engine_row.addWidget(self.engine_combo)
        self.layout.addLayout(engine_row)

        # URL input
        self.url_label = QLabel("URL to Scrape:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        self.layout.addWidget(self.url_label)
        self.layout.addWidget(self.url_input)

        # Wait-for selector
        self.wait_for_label = QLabel("Wait for Selector (optional):")
        self.wait_for_input = QLineEdit()
        self.wait_for_input.setPlaceholderText(".content")
        self.layout.addWidget(self.wait_for_label)
        self.layout.addWidget(self.wait_for_input)

        # Crawl options
        crawl_row = QHBoxLayout()
        self.next_selector_input = QLineEdit()
        self.next_selector_input.setPlaceholderText(".next a")
        self.max_pages_input = QSpinBox(); self.max_pages_input.setRange(1, 5000); self.max_pages_input.setValue(50)
        self.max_depth_input = QSpinBox(); self.max_depth_input.setRange(1, 25); self.max_depth_input.setValue(2)
        self.same_host_check = QCheckBox("Same Host Only"); self.same_host_check.setChecked(True)
        crawl_row.addWidget(QLabel("Next Page Selector:")); crawl_row.addWidget(self.next_selector_input)
        crawl_row.addWidget(QLabel("Max Pages:")); crawl_row.addWidget(self.max_pages_input)
        crawl_row.addWidget(QLabel("Max Depth:")); crawl_row.addWidget(self.max_depth_input)
        crawl_row.addWidget(self.same_host_check)
        self.layout.addLayout(crawl_row)

        # Selectors JSON
        self.selectors_label = QLabel('Extract Selectors JSON (e.g. {"title": "h1", "body": ".article p"})')
        self.selectors_input = QTextEdit()
        self.layout.addWidget(self.selectors_label)
        self.layout.addWidget(self.selectors_input)

        # Profiles
        prof_row = QHBoxLayout()
        self.profile_combo = QComboBox(); self.profile_combo.addItems(["(none)"])
        self.profile_combo.currentTextChanged.connect(self.apply_profile)
        self.load_profiles_btn = QPushButton("Load Profiles")
        self.load_profiles_btn.clicked.connect(self.load_profiles)
        prof_row.addWidget(QLabel("Profile:"))
        prof_row.addWidget(self.profile_combo)
        prof_row.addWidget(self.load_profiles_btn)
        self.layout.addLayout(prof_row)

        # Options
        opts = QHBoxLayout()
        self.headless_check = QCheckBox("Headless"); self.headless_check.setChecked(True)
        self.stealth_check = QCheckBox("Stealth-ish"); self.stealth_check.setChecked(True)
        self.disable_images_check = QCheckBox("Block images/fonts/media"); self.disable_images_check.setChecked(True)
        opts.addWidget(self.headless_check); opts.addWidget(self.stealth_check); opts.addWidget(self.disable_images_check)
        self.layout.addLayout(opts)

        # Proxy
        px = QHBoxLayout()
        self.proxy_input = QLineEdit(); self.proxy_input.setPlaceholderText("Proxy URL or path to .txt list")
        self.load_proxy_btn = QPushButton("Load Proxy List")
        self.load_proxy_btn.clicked.connect(self.load_proxy_list)
        px.addWidget(QLabel("Proxy:")); px.addWidget(self.proxy_input); px.addWidget(self.load_proxy_btn)
        self.layout.addLayout(px)

        # Buttons
        btns = QHBoxLayout()
        self.scrape_button = QPushButton("Scrape"); self.scrape_button.clicked.connect(self.start_scrape)
        self.crawl_button = QPushButton("Crawl"); self.crawl_button.clicked.connect(self.start_crawl)
        self.cancel_button = QPushButton("Cancel"); self.cancel_button.clicked.connect(self.cancel_tasks)
        self.save_button = QPushButton("Save Results"); self.save_button.clicked.connect(self.save_results)
        btns.addWidget(self.scrape_button); btns.addWidget(self.crawl_button); btns.addWidget(self.cancel_button); btns.addWidget(self.save_button)
        self.layout.addLayout(btns)

        # Output
        self.output_label = QLabel("Output:")
        self.output_text = QTextEdit(); self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_label); self.layout.addWidget(self.output_text)

        # Logs
        self.log_label = QLabel("Logs:")
        self.log_text = QTextEdit(); self.log_text.setReadOnly(True)
        self.layout.addWidget(self.log_label); self.layout.addWidget(self.log_text)

    # ---------- profiles ----------
    def load_profiles(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Selector Profiles", "", "JSON (*.json)")
        if not path: return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.profiles = json.load(f)
            self.profile_combo.clear(); self.profile_combo.addItems(["(none)"] + list(self.profiles.keys()))
            self.log(f"Loaded profiles from {path}")
        except Exception as e:
            self.log(f"Error loading profiles: {e}")

    def apply_profile(self):
        name = self.profile_combo.currentText()
        if name != "(none)" and name in self.profiles:
            p = self.profiles[name]
            self.selectors_input.setPlainText(json.dumps(p.get('selectors', {}), indent=2))
            self.wait_for_input.setText(p.get('wait_for',''))
            self.next_selector_input.setText(p.get('next_selector',''))
            self.log(f"Applied profile: {name}")

    # ---------- proxies ----------
    def load_proxy_list(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Proxy List", "", "Text (*.txt);;All Files (*)")
        if not path: return
        try:
            with open(path,'r',encoding='utf-8') as f:
                lines = [ln.strip() for ln in f if ln.strip()]
            self.proxy_input.setText(path)
            self.log(f"Loaded {len(lines)} proxies")
        except Exception as e:
            self.log(f"Error loading proxy list: {e}")

    def get_proxy_pool(self) -> List[str]:
        p = self.proxy_input.text().strip()
        if not p: return []
        if p.endswith('.txt'):
            try:
                with open(p,'r',encoding='utf-8') as f:
                    return [ln.strip() for ln in f if ln.strip()]
            except Exception:
                return []
        return [p]

    # ---------- actions ----------
    def start_scrape(self):
        url = self.url_input.text().strip()
        if not url:
            self.log("Please enter a URL"); return
        try:
            selectors = json.loads(self.selectors_input.toPlainText().strip() or "{}")
        except json.JSONDecodeError:
            self.log("Invalid selectors JSON"); return
        cfg = EmulatorConfig(
            engine=self.engine_combo.currentText(),
            headless=self.headless_check.isChecked(),
            proxy_pool=self.get_proxy_pool(),
            stealth_mode=self.stealth_check.isChecked(),
            disable_images=self.disable_images_check.isChecked()
        )
        task = {'url': url, 'wait_for': self.wait_for_input.text().strip() or None, 'selectors': selectors}
        self.toggle_buttons(False)
        w = ScrapeWorker(cfg, task)
        w.result_signal.connect(self.display_results)
        w.log_signal.connect(self.log_text.append)
        w.finished.connect(lambda: self.toggle_buttons(True))
        self.workers.append(w); w.start()

    def start_crawl(self):
        url = self.url_input.text().strip()
        if not url:
            self.log("Please enter a URL"); return
        try:
            selectors = json.loads(self.selectors_input.toPlainText().strip() or "{}")
        except json.JSONDecodeError:
            self.log("Invalid selectors JSON"); return
        cfg = EmulatorConfig(
            engine=self.engine_combo.currentText(),
            headless=self.headless_check.isChecked(),
            proxy_pool=self.get_proxy_pool(),
            stealth_mode=self.stealth_check.isChecked(),
            disable_images=self.disable_images_check.isChecked()
        )
        task = {
            'url': url,
            'selectors': selectors,
            'next_selector': self.next_selector_input.text().strip() or None,
            'same_host_only': self.same_host_check.isChecked(),
            'max_pages': self.max_pages_input.value(),
            'max_depth': self.max_depth_input.value()
        }
        self.toggle_buttons(False)
        w = CrawlWorker(cfg, task)
        w.result_signal.connect(self.display_results)
        w.log_signal.connect(self.log_text.append)
        w.finished.connect(lambda: self.toggle_buttons(True))
        self.workers.append(w); w.start()

    def cancel_tasks(self):
        for w in self.workers:
            try: w.cancel()
            except Exception: pass
        self.workers.clear()
        self.toggle_buttons(True)
        self.log("All tasks cancelled")

    # ---------- results / export ----------
    def display_results(self, res: Dict[str, Any]):
        self.last_result = res
        if 'pages' in res:
            short = {'status': res.get('status'), 'pages': [
                {'url': p.get('url'), 'title': p.get('title'), 'status': p.get('status'), 'data': p.get('data')}
                for p in res.get('pages', [])
            ]}
            self.output_text.setPlainText(json.dumps(short, indent=2, ensure_ascii=False))
        else:
            short = {k: res.get(k) for k in ('url','title','status','data','cookies')}
            self.output_text.setPlainText(json.dumps(short, indent=2, ensure_ascii=False))

    def _slug(self, s: str) -> str:
        return re.sub(r'[^a-zA-Z0-9._-]+','_', s)[:120]

    def save_results(self):
        if not self.last_result:
            self.log("No results to save"); return
        out_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if not out_dir: return
        out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
        try:
            if 'pages' in self.last_result:
                pages = self.last_result['pages']
                # JSONL
                with open(out/'results.jsonl','w',encoding='utf-8') as f:
                    for p in pages: f.write(json.dumps(p, ensure_ascii=False) + '\n')
                # CSV
                keys = sorted({k for p in pages for k in ['url','title','status'] | set((p.get('data') or {}).keys())})
                with open(out/'results.csv','w',encoding='utf-8',newline='') as f:
                    w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
                    for p in pages:
                        row = {'url': p.get('url'), 'title': p.get('title'), 'status': p.get('status')}
                        for k,v in (p.get('data') or {}).items():
                            row[k] = '|'.join(v) if isinstance(v, list) else v
                        w.writerow(row)
                # HTML dumps present?
                for p in pages:
                    html = p.get('html')
                    if html:
                        fname = self._slug(urlparse(p['url']).path or 'index') + '.html'
                        (out/fname).write_text(html, encoding='utf-8')
                self.log(f"Saved crawl results to: {out_dir}")
            else:
                (out/'results.json').write_text(json.dumps(self.last_result, indent=2, ensure_ascii=False), encoding='utf-8')
                self.log(f"Saved results to: {out_dir}/results.json")
        except Exception as e:
            self.log(f"Error saving results: {e}")

    # ---------- util ----------
    def toggle_buttons(self, enabled: bool):
        self.scrape_button.setEnabled(enabled)
        self.crawl_button.setEnabled(enabled)

    def log(self, msg: str):
        self.log_text.append(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

    def closeEvent(self, event):
        self.cancel_tasks()
        event.accept()


# ---------- Optional Abstract integrations (kept, not removed) ----------
try:
    from abstract_webtools.managers.networkManager import NetworkManager
    from abstract_webtools.managers.videoDownloader import downloadvideo
    from abstract_webtools.managers.crawlManager import SitemapGenerator
    from abstract_webtools.managers.dynamicRateLimiter import DynamicRateLimiterManager
except ImportError:
    NetworkManager = None
    downloadvideo = None
    SitemapGenerator = None
    DynamicRateLimiterManager = None


# ---------- main ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScraperGUI()
    window.show()
    sys.exit(app.exec())
