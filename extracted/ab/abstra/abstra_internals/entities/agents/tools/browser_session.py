import base64
import os
import pathlib
import tempfile
import time
from collections import deque
from typing import Any, Deque, Dict, List, Optional, Set

from abstra_internals.entities.agents.tools.download_detector import (
    BLOB_DOWNLOAD_INTERCEPTOR_JS,
    DownloadDetector,
    DownloadInfo,
    DownloadStatus,
    extract_filename,
    is_download_response,
    is_likely_download_url,
)

EXTRACT_ELEMENTS_JS = """
() => {
    const elements = [];
    const selectors = [
        'a[href]', 'button', 'input', 'textarea', 'select',
        '[role="button"]', '[onclick]',
        '[tabindex]:not([tabindex="-1"])'
    ];
    const seen = new Set();

    function getLabel(el) {
        const ariaLabel = el.getAttribute('aria-label');
        if (ariaLabel) return ariaLabel;
        const title = el.getAttribute('title');
        if (title) return title;
        if (el.id) {
            const label = document.querySelector(`label[for="${el.id}"]`);
            if (label) return label.innerText.trim();
        }
        const parentLabel = el.closest('label');
        if (parentLabel) return parentLabel.innerText.trim();
        const placeholder = el.getAttribute('placeholder');
        if (placeholder) return placeholder;
        return '';
    }

    function getParentContext(el) {
        const semanticParents = [
            'form', 'nav', 'header', 'footer', 'main', 'aside',
            'section', 'article', 'dialog',
            '[role="dialog"]', '[role="navigation"]', '[role="form"]'
        ];
        const parent = el.closest(semanticParents.join(','));
        if (!parent) return 'BODY';
        let context = parent.tagName.toLowerCase();
        if (parent.id) context += ` (#${parent.id})`;
        else if (parent.getAttribute('aria-label')) context += ` (${parent.getAttribute('aria-label')})`;
        else if (parent.getAttribute('role')) context += ` [role="${parent.getAttribute('role')}"]`;
        return context.toUpperCase();
    }

    selectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            if (seen.has(el)) return;
            seen.add(el);

            const rect = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);
            const isVisible = rect.width > 0 && rect.height > 0 &&
                style.visibility !== 'hidden' &&
                style.display !== 'none' &&
                style.opacity !== '0';
            if (!isVisible) return;

            let uniqueSelector = '';
            if (el.id) {
                uniqueSelector = '#' + el.id;
            } else {
                let path = [];
                let current = el;
                while (current && current !== document.body) {
                    let sel = current.tagName.toLowerCase();
                    if (current.className && typeof current.className === 'string') {
                        const classes = current.className.split(' ')
                            .filter(c => c && !c.startsWith('css-'))
                            .slice(0, 2);
                        if (classes.length > 0) sel += '.' + classes.join('.');
                    }
                    if (current.parentElement) {
                        const siblings = Array.from(current.parentElement.children);
                        const sameTag = siblings.filter(s => s.tagName === current.tagName);
                        if (sameTag.length > 1) {
                            const idx = sameTag.indexOf(current) + 1;
                            sel += ':nth-of-type(' + idx + ')';
                        }
                    }
                    path.unshift(sel);
                    current = current.parentElement;
                }
                uniqueSelector = path.join(' > ');
            }

            let text = (el.innerText || '').trim().substring(0, 100) ||
                el.getAttribute('aria-label') ||
                el.getAttribute('title') ||
                el.value || el.alt ||
                getLabel(el) || '';

            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;

            elements.push({
                selector: uniqueSelector,
                text: text,
                tag: el.tagName.toLowerCase(),
                parent_context: getParentContext(el),
                attributes: {
                    href: el.href || '',
                    type: el.type || '',
                    placeholder: el.getAttribute('placeholder') || '',
                    name: el.name || '',
                    label: getLabel(el)
                },
                bbox: {
                    x: Math.round(rect.x + scrollLeft),
                    y: Math.round(rect.y + scrollTop),
                    width: Math.round(rect.width),
                    height: Math.round(rect.height)
                },
                viewport_bbox: {
                    x: Math.round(rect.x),
                    y: Math.round(rect.y),
                    width: Math.round(rect.width),
                    height: Math.round(rect.height)
                },
                isOnScreen: rect.bottom > 0 && rect.top < window.innerHeight &&
                    rect.right > 0 && rect.left < window.innerWidth
            });
        });
    });

    return elements;
}
"""

READINESS_INJECTOR_JS = """
() => {
    if (window.__pageReadinessInjected) return;
    window.__pageReadinessInjected = true;
    window.__lastDomMutation = Date.now();
    window.__domMutationCount = 0;

    const observer = new MutationObserver((mutations) => {
        window.__lastDomMutation = Date.now();
        window.__domMutationCount += mutations.length;
    });

    if (document.body) {
        observer.observe(document.body, {
            childList: true, subtree: true,
            attributes: true, characterData: true
        });
    } else {
        const docObserver = new MutationObserver(() => {
            if (document.body) {
                docObserver.disconnect();
                observer.observe(document.body, {
                    childList: true, subtree: true,
                    attributes: true, characterData: true
                });
            }
        });
        docObserver.observe(document.documentElement, { childList: true, subtree: true });
    }
}
"""

READINESS_CHECK_JS = """
() => {
    const now = Date.now();
    const observerPresent = !!window.__pageReadinessInjected;
    const timeSinceLastMutation = window.__lastDomMutation
        ? now - window.__lastDomMutation
        : (observerPresent ? 99999 : 0);

    const selectors = ['a[href]', 'button', 'input', 'select', 'textarea',
                       '[role="button"]', '[onclick]', '[tabindex]:not([tabindex="-1"])'];
    const seen = new Set();
    let visibleCount = 0;

    for (const sel of selectors) {
        for (const el of document.querySelectorAll(sel)) {
            if (seen.has(el)) continue;
            seen.add(el);
            const rect = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);
            if (rect.width > 0 && rect.height > 0 &&
                style.visibility !== 'hidden' &&
                style.display !== 'none' &&
                style.opacity !== '0') {
                visibleCount++;
                if (visibleCount >= 5) break;
            }
        }
        if (visibleCount >= 5) break;
    }

    const loadingSelectors = [
        '[class*="spinner"]', '[class*="loading"]', '[class*="skeleton"]',
        '[role="progressbar"]', '.loader'
    ];
    let isLoading = false;
    for (const sel of loadingSelectors) {
        try {
            const el = document.querySelector(sel);
            if (el && el.offsetParent !== null) { isLoading = true; break; }
        } catch(e) {}
    }

    const bodyText = (document.body?.innerText || '').trim();
    if (bodyText.length < 100) {
        if (/^(loading|please wait|carregando|aguarde|cargando)\\.{0,3}$/i.test(bodyText)) {
            isLoading = true;
        }
    }

    const hasMainContent = document.body
        && document.body.children.length > 0
        && bodyText.length > 50;

    return {
        readyState: document.readyState,
        timeSinceLastMutation: timeSinceLastMutation,
        mutationCount: window.__domMutationCount || 0,
        interactiveElementCount: visibleCount,
        hasMainContent: hasMainContent,
        isLoading: isLoading,
        bodyTextLength: bodyText.length
    };
}
"""


class BrowserSession:
    MAX_NETWORK_LOGS = 500

    def __init__(self, download_dir: Optional[str] = None) -> None:
        self._playwright: Any = None
        self._browser: Any = None
        self._context: Any = None
        self._active_tab_index: int = 0
        self._elements: List[Dict[str, Any]] = []
        self._downloads: List[Any] = []
        self._download_dir = download_dir
        self._blob_interceptor_injected: Set[int] = set()
        self._download_detector: Optional[DownloadDetector] = None
        self._captured_network_logs: Deque[Dict[str, Any]] = deque(
            maxlen=self.MAX_NETWORK_LOGS
        )

    @property
    def is_started(self) -> bool:
        return self._context is not None and self.page is not None

    @property
    def page(self) -> Any:
        if self._context and self._context.pages:
            if self._active_tab_index >= len(self._context.pages):
                self._active_tab_index = len(self._context.pages) - 1
            return self._context.pages[self._active_tab_index]
        return None

    def ensure_browser(self) -> None:
        if self.page is not None:
            return

        from playwright.sync_api import sync_playwright

        self._playwright = sync_playwright().start()

        # When SELENIUM_REMOTE_URL is set (cloud), Playwright automatically
        # connects through Selenium Grid instead of launching a local browser.
        # See: https://playwright.dev/docs/selenium-grid
        self._browser = self._playwright.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--disable-default-apps",
                "--disable-sync",
                "--disable-translate",
                "--disable-features=TranslateUI,BlinkGenPropertyTrees",
                "--disable-ipc-flooding-protection",
            ],
        )

        context_kwargs: Dict[str, Any] = {
            "viewport": {"width": 1280, "height": 720},
            "accept_downloads": True,
            "user_agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            "locale": "en-US",
            "timezone_id": "America/Sao_Paulo",
            "extra_http_headers": {
                "Accept-Language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
                "Sec-CH-UA": '"Chromium";v="131", "Not_A Brand";v="24"',
                "Sec-CH-UA-Mobile": "?0",
                "Sec-CH-UA-Platform": '"Windows"',
            },
        }

        downloads_dir = ""
        if self._download_dir:
            pathlib.Path(self._download_dir).mkdir(parents=True, exist_ok=True)
            downloads_dir = self._download_dir

        cert_b64 = os.environ.get("ABSTRA_BROWSER_CERTIFICATE_BASE64", "")
        if cert_b64:
            passphrase = os.environ.get("ABSTRA_BROWSER_CERTIFICATE_PASSPHRASE", "")
            origin = os.environ.get("ABSTRA_BROWSER_CERTIFICATE_ORIGIN", "")
            pfx_bytes = base64.b64decode(cert_b64)
            self._cert_tmp = tempfile.NamedTemporaryFile(suffix=".pfx", delete=False)
            self._cert_tmp.write(pfx_bytes)
            self._cert_tmp.flush()
            context_kwargs["client_certificates"] = [
                {
                    "origin": origin,
                    "pfxPath": self._cert_tmp.name,
                    "passphrase": passphrase,
                }
            ]

        self._context = self._browser.new_context(**context_kwargs)

        if downloads_dir:
            self._download_detector = DownloadDetector(downloads_dir)
            self._setup_download_interception(downloads_dir)

        self._context.on("response", self._capture_network_log)

        self._context.new_page()
        self._active_tab_index = 0
        self.page.on("download", self._on_download)

    def _setup_download_interception(self, downloads_dir: str) -> None:
        saved_urls: Set[str] = set()

        def _save_body(body: bytes, filename: str, url: str) -> Optional[DownloadInfo]:
            filepath = os.path.join(downloads_dir, filename)
            if os.path.exists(filepath):
                name, ext = os.path.splitext(filename)
                filepath = os.path.join(
                    downloads_dir, f"{name}_{int(time.time())}{ext}"
                )
            with open(filepath, "wb") as f:
                f.write(body)
            size = len(body)
            info = DownloadInfo(
                filename=os.path.basename(filepath),
                path=filepath,
                size=size,
                timestamp=time.time(),
                status=DownloadStatus.COMPLETED,
                url=url,
            )
            if self._download_detector:
                self._download_detector.event_downloads.append(info)
            saved_urls.add(url)
            return info

        def _intercept_xhr(route: Any) -> None:
            request = route.request
            if request.resource_type not in ("xhr", "fetch", "document"):
                route.continue_()
                return
            if not is_likely_download_url(request.url):
                route.continue_()
                return
            try:
                response = route.fetch()
                headers = response.headers
                ct = headers.get("content-type", "")
                cd = headers.get("content-disposition", "")
                if is_download_response(ct, cd) and response.status == 200:
                    cl = int(headers.get("content-length", 0))
                    if cl <= 50 * 1024 * 1024:
                        filename = extract_filename(request.url, ct, cd)
                        body = response.body()
                        if body and len(body) > 0 and len(body) <= 50 * 1024 * 1024:
                            _save_body(body, filename, request.url)
                route.fulfill(response=response)
            except Exception:
                try:
                    route.continue_()
                except Exception:
                    pass

        self._context.route("**/*", _intercept_xhr)

        def _check_response(response: Any) -> None:
            try:
                if response.request.resource_type not in ("xhr", "fetch"):
                    return
                if response.url in saved_urls:
                    return
                headers = response.headers
                ct = headers.get("content-type", "")
                cd = headers.get("content-disposition", "")
                if not is_download_response(ct, cd) or response.status != 200:
                    return
                filename = extract_filename(response.url, ct, cd)
                body = response.body()
                if body and 0 < len(body) <= 50 * 1024 * 1024:
                    _save_body(body, filename, response.url)
            except Exception:
                pass

        self._context.on("response", _check_response)

    def _capture_network_log(self, response: Any) -> None:
        try:
            req = response.request
            self._captured_network_logs.append(
                {
                    "url": response.url,
                    "method": req.method,
                    "status": response.status,
                    "type": req.resource_type,
                }
            )
        except Exception:
            pass

    def _on_download(self, dl: Any) -> None:
        self._downloads.append(dl)
        if self._download_dir:
            filename = dl.suggested_filename or "download"
            filename = pathlib.Path(filename).name
            if not filename:
                filename = "download"
            base = pathlib.Path(self._download_dir)
            dest = base / filename
            if not str(dest.resolve()).startswith(str(base.resolve())):
                return
            counter = 1
            while dest.exists():
                stem = pathlib.Path(filename).stem
                suffix = pathlib.Path(filename).suffix
                dest = base / f"{stem}_{counter}{suffix}"
                counter += 1
            try:
                dl.save_as(str(dest))
                if self._download_detector:
                    self._download_detector.download_finished(
                        str(dest),
                        dest.stat().st_size if dest.exists() else 0,
                        dl.url,
                    )
            except Exception as e:
                print(f"[BROWSER] Error saving download to {dest}: {e}")

    # --- Multi-tab support ---

    def create_tab(self) -> Any:
        if self._context:
            new_page = self._context.new_page()
            self._active_tab_index = len(self._context.pages) - 1
            new_page.on("download", self._on_download)
            return new_page
        return None

    def switch_tab(self, index: int) -> bool:
        if not self._context:
            return False
        pages = self._context.pages
        if 0 <= index < len(pages):
            self._active_tab_index = index
            try:
                pages[index].bring_to_front()
            except Exception:
                pass
            return True
        return False

    def close_tab(self) -> bool:
        if not self._context or len(self._context.pages) <= 1:
            return False
        page = self.page
        if page:
            page_id = id(page)
            self._blob_interceptor_injected.discard(page_id)
            page.close()
            # Re-validate index against the (now shorter) pages list
            num_pages = len(self._context.pages)
            if self._active_tab_index >= num_pages:
                self._active_tab_index = max(0, num_pages - 1)
            return True
        return False

    def get_tab_count(self) -> int:
        if self._context:
            return len(self._context.pages)
        return 0

    def get_current_url(self) -> str:
        page = self.page
        if page:
            try:
                return page.url
            except Exception:
                pass
        return ""

    def get_element_text_by_index(self, index: int) -> str:
        for elem in self._elements:
            if elem.get("index") == index:
                return (elem.get("text", "") or "")[:100]
        return ""

    def get_element_count(self) -> int:
        return len(self._elements)

    # --- Download helpers ---

    def wait_for_pending_downloads(self, timeout: float = 3.0) -> bool:
        """Wait for any in-flight downloads to complete.

        Returns True if a download detector is available and was used,
        False if the caller should fall back to a fixed sleep.
        """
        if self._download_detector:
            self._download_detector.wait_for_pending_downloads(timeout=timeout)
            return True
        return False

    # --- Network logs ---

    def get_network_logs(self) -> List[Dict[str, Any]]:
        return list(self._captured_network_logs)

    # --- Blob downloads ---

    def inject_blob_interceptor(self) -> None:
        page = self.page
        if not page:
            return
        page_id = id(page)
        if page_id in self._blob_interceptor_injected:
            return
        try:
            page.evaluate(BLOB_DOWNLOAD_INTERCEPTOR_JS)
            self._blob_interceptor_injected.add(page_id)
        except Exception:
            pass

    def check_blob_downloads(self) -> List[DownloadInfo]:
        page = self.page
        if not page:
            return []
        try:
            blobs = page.evaluate("window.__interceptedBlobs || []")
            if not blobs:
                return []
            page.evaluate("window.__interceptedBlobs = []")
            downloads = []
            for blob in blobs:
                filename = blob.get("filename", f"download_{int(time.time())}")
                filename = os.path.basename(filename)
                data_b64 = blob.get("data", "")
                if not data_b64 or not self._download_dir:
                    continue
                filepath = os.path.join(self._download_dir, filename)
                if os.path.exists(filepath):
                    name, ext = os.path.splitext(filename)
                    filepath = os.path.join(
                        self._download_dir, f"{name}_{int(time.time())}{ext}"
                    )
                    filename = os.path.basename(filepath)
                try:
                    file_data = base64.b64decode(data_b64)
                    with open(filepath, "wb") as f:
                        f.write(file_data)
                    info = DownloadInfo(
                        filename=filename,
                        path=filepath,
                        size=len(file_data),
                        timestamp=time.time(),
                        status=DownloadStatus.COMPLETED,
                        url=blob.get("url"),
                    )
                    downloads.append(info)
                    if self._download_detector:
                        self._download_detector.event_downloads.append(info)
                except Exception:
                    pass
            return downloads
        except Exception:
            return []

    # --- Download detector delegates ---

    def snapshot_before_action(self) -> None:
        if self._download_detector:
            self._download_detector.snapshot_before_action()

    def detect_new_downloads(self, action: str = "") -> List[DownloadInfo]:
        if self._download_detector:
            return self._download_detector.detect_new_downloads(action)
        return []

    # --- Page readiness ---

    def wait_for_page_ready(
        self, timeout_ms: int = 15000, min_elements: int = 1
    ) -> bool:
        page = self.page
        if not page:
            return False

        deadline = time.time() + (timeout_ms / 1000)

        try:
            remaining = max(0, int((deadline - time.time()) * 1000))
            page.wait_for_load_state("networkidle", timeout=min(remaining, 5000))
        except Exception:
            pass

        if time.time() >= deadline:
            return False

        try:
            page.evaluate(READINESS_INJECTOR_JS)
        except Exception:
            pass

        poll_interval_ms = 300
        dom_settle_ms = 500
        relaxed_deadline = deadline - (timeout_ms / 1000) * 0.4

        while time.time() < deadline:
            try:
                page.evaluate(READINESS_INJECTOR_JS)
            except Exception:
                pass
            try:
                status = page.evaluate(READINESS_CHECK_JS)
            except Exception:
                page.wait_for_timeout(poll_interval_ms)
                continue

            dom_settled = status["timeSinceLastMutation"] >= dom_settle_ms
            has_elements = status["interactiveElementCount"] >= min_elements
            has_content = status["hasMainContent"]
            not_loading = not status["isLoading"]
            doc_ready = status["readyState"] in ("complete", "interactive")

            if (
                dom_settled
                and not_loading
                and doc_ready
                and (has_elements or has_content)
            ):
                return True

            if (
                time.time() >= relaxed_deadline
                and dom_settled
                and not_loading
                and doc_ready
            ):
                return True

            page.wait_for_timeout(poll_interval_ms)

        return False

    # --- Element extraction ---

    def extract_elements(self) -> List[Dict[str, Any]]:
        if self.page is None:
            return []
        for attempt in range(3):
            try:
                raw = self.page.evaluate(EXTRACT_ELEMENTS_JS)
                for idx, elem in enumerate(raw):
                    elem["index"] = idx
                self._elements = raw
                return self._elements
            except Exception:
                if attempt < 2:
                    self.page.wait_for_timeout(2000)
                self._elements = []
        return self._elements

    def get_element_by_index(self, index: int) -> Optional[Dict[str, Any]]:
        for elem in self._elements:
            if elem.get("index") == index:
                return elem
        return None

    def get_page_summary(self) -> str:
        if self.page is None:
            return "No browser page open."
        try:
            title = self.page.title()
            url = self.page.url
        except Exception:
            return "Failed to read page state."

        self.extract_elements()

        lines = [f'Page: "{title}" | URL: {url}']

        if not self._elements:
            lines.append("No interactive elements found.")
            return "\n".join(lines)

        lines.append(f"Interactive Elements ({len(self._elements)} total):")
        for elem in self._elements:
            tag = elem.get("tag", "?").upper()
            text = elem.get("text", "")
            attrs = elem.get("attributes", {})
            ctx = elem.get("parent_context", "")
            idx = elem.get("index", "?")

            parts = [f"  {idx}: [{tag}]"]
            if text:
                parts.append(f'"{text}"')
            attr_parts = []
            if attrs.get("type"):
                attr_parts.append(f"type={attrs['type']}")
            if attrs.get("placeholder"):
                attr_parts.append(f'placeholder="{attrs["placeholder"]}"')
            if attrs.get("href"):
                href = attrs["href"]
                if len(href) > 60:
                    href = href[:60] + "..."
                attr_parts.append(f"href={href}")
            if attrs.get("name"):
                attr_parts.append(f"name={attrs['name']}")
            if attr_parts:
                parts.append(", ".join(attr_parts))
            if ctx and ctx != "BODY":
                parts.append(f"({ctx})")
            lines.append(" ".join(parts))

        if self._downloads:
            pending = 0
            completed = 0
            for dl in self._downloads:
                try:
                    if dl.failure() or dl.path():
                        completed += 1
                    else:
                        pending += 1
                except Exception:
                    pending += 1
            dl_parts = []
            if completed:
                dl_parts.append(f"{completed} completed")
            if pending:
                dl_parts.append(f"{pending} pending")
            lines.append(
                f"Downloads: {', '.join(dl_parts)}. "
                "Use 'list_downloads' to see details, 'move_download' to save."
            )

        tab_count = self.get_tab_count()
        if tab_count > 1:
            lines.append(f"Tabs: {tab_count} open (active: {self._active_tab_index})")

        return "\n".join(lines)

    def take_screenshot(self, path: Optional[str] = None) -> Optional[str]:
        if self.page is None:
            return None
        if path is None:
            tmp = tempfile.NamedTemporaryFile(
                suffix=".jpg", delete=False, prefix="screenshot_"
            )
            path = tmp.name
            tmp.close()
        try:
            self.page.screenshot(path=path, type="jpeg", quality=50)
            return path
        except Exception:
            return None

    def close(self) -> None:
        try:
            if self._context:
                try:
                    self._context.unroute("**/*")
                except Exception:
                    pass
                self._context.close()
        except Exception:
            pass
        try:
            if self._browser:
                self._browser.close()
        except Exception:
            pass
        try:
            if self._playwright:
                self._playwright.stop()
        except Exception:
            pass
        try:
            tmp = getattr(self, "_cert_tmp", None)
            if tmp:
                os.unlink(tmp.name)
        except Exception:
            pass

        self._context = None
        self._browser = None
        self._playwright = None
        self._elements = []
        self._downloads = []
        self._blob_interceptor_injected.clear()
        self._captured_network_logs.clear()
