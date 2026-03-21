import asyncio
import base64
from collections.abc import Iterable
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Dict, List, Optional, TypedDict, Union
from uuid import uuid4

import playwright.sync_api
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from .base import AgentTools


class ClientCertificate(TypedDict):
    origin: str
    pfx_base64: str
    passphrase: str


class ElementExtractor:
    def __init__(self):
        self.interactive_selectors = [
            "a[href]",
            "button",
            "input",
            "textarea",
            "select",
            "input[type='button']",
            "input[type='submit']",
            "[role='button']",
            "[onclick]",
            "[tabindex]:not([tabindex='-1'])",
        ]

    def extract_elements(self, page: Page) -> List[Dict[str, Any]]:
        elements = []

        js_code = """
        () => {
            const elements = [];
            const selectors = [
                'a[href]',
                'button',
                'input',
                'textarea',
                'select',
                '[role="button"]',
                '[onclick]',
                '[tabindex]:not([tabindex="-1"])'
            ];

            const seen = new Set();

            function getLabel(el) {
                const ariaLabel = el.getAttribute('aria-label');
                if (ariaLabel) return ariaLabel;

                const title = el.getAttribute('title');
                if (title) return title;

                if (el.id) {
                    const label = document.querySelector(`label[for="${CSS.escape(el.id)}"]`);
                    if (label) return label.innerText.trim();
                }

                const parentLabel = el.closest('label');
                if (parentLabel) return parentLabel.innerText.trim();

                const placeholder = el.getAttribute('placeholder');
                if (placeholder) return `[${placeholder}]`;

                return '';
            }

            function getParentContext(el) {
                const semanticParents = [
                    'form', 'nav', 'header', 'footer', 'main', 'aside', 'section', 'article', 'dialog',
                    '[role="dialog"]', '[role="navigation"]', '[role="form"]', '[role="banner"]', '[role="contentinfo"]'
                ];

                const parent = el.closest(semanticParents.join(','));
                if (!parent) return 'BODY';

                let context = parent.tagName.toLowerCase();

                if (parent.getAttribute('aria-label')) context += ` (${parent.getAttribute('aria-label')})`;
                else if (parent.id) context += ` (#${parent.id})`;
                else if (parent.getAttribute('role')) context += ` [role="${parent.getAttribute('role')}"]`;

                return context.toUpperCase();
            }

            selectors.forEach(selector => {
                document.querySelectorAll(selector).forEach((el, idx) => {
                    if (seen.has(el)) return;
                    seen.add(el);

                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);

                    const isVisible = rect.width > 0 &&
                                    rect.height > 0 &&
                                    style.visibility !== 'hidden' &&
                                    style.display !== 'none' &&
                                    style.opacity !== '0';

                    if (!isVisible) return;

                    const vw = window.innerWidth;
                    const vh = window.innerHeight;
                    const isOnScreen = rect.right > 0 &&
                                       rect.bottom > 0 &&
                                       rect.left < vw &&
                                       rect.top < vh;

                    // Check if element is actually the topmost at its center.
                    // Filters elements hidden behind sticky headers, overlays,
                    // or positioned at (0,0) behind page chrome.
                    let isTopmost = true;
                    if (isOnScreen) {
                        const cx = rect.left + rect.width / 2;
                        const cy = rect.top + rect.height / 2;
                        if (cx >= 0 && cy >= 0 && cx < vw && cy < vh) {
                            const topEl = document.elementFromPoint(cx, cy);
                            isTopmost = !topEl || topEl === el || el.contains(topEl);
                        }
                    }

                    let uniqueSelector = '';
                    if (el.id) {
                        uniqueSelector = `#${CSS.escape(el.id)}`;
                    } else {
                        let path = [];
                        let current = el;
                        while (current && current !== document.body) {
                            let selector = current.tagName.toLowerCase();

                            if (current.className && typeof current.className === 'string') {
                                const classes = current.className.split(' ')
                                    .filter(c => c && !c.startsWith('css-'))
                                    .slice(0, 2);
                                if (classes.length > 0) {
                                    selector += '.' + classes.join('.');
                                }
                            }

                            if (current.parentElement) {
                                const siblings = Array.from(current.parentElement.children);
                                const sameTagSiblings = siblings.filter(s => s.tagName === current.tagName);
                                if (sameTagSiblings.length > 1) {
                                    const index = sameTagSiblings.indexOf(current) + 1;
                                    selector += `:nth-of-type(${index})`;
                                }
                            }

                            path.unshift(selector);
                            current = current.parentElement;
                        }
                        uniqueSelector = path.join(' > ');
                    }

                    const label = getLabel(el);
                    const parentContext = getParentContext(el);

                    let text = el.innerText?.trim().substring(0, 100) ||
                               el.getAttribute('aria-label') ||
                               el.getAttribute('title') ||
                               el.value ||
                               el.alt ||
                               label ||
                               '';

                    const pageX = rect.x + window.scrollX;
                    const pageY = rect.y + window.scrollY;

                    let category;
                    const isInDropdown = el.closest('.dropdown-menu, [role="listbox"], [role="menu"]');
                    if (isInDropdown) {
                        category = 'dropdown-option';
                    } else if (el.tagName === 'BUTTON' || el.type === 'submit' || el.type === 'button' || el.getAttribute('role') === 'button') {
                        category = 'action-button';
                    } else if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT') {
                        category = 'form-input';
                    } else if (el.tagName === 'A' && el.href) {
                        category = 'navigation-link';
                    } else {
                        category = 'other';
                    }

                    elements.push({
                        selector: uniqueSelector,
                        text: text,
                        tag: el.tagName.toLowerCase(),
                        category: category,
                        parent_context: parentContext,
                        attributes: {
                            href: el.href || '',
                            onclick: el.onclick ? 'yes' : '',
                            role: el.getAttribute('role') || '',
                            type: el.type || '',
                            tabindex: el.tabIndex || 0,
                            placeholder: el.getAttribute('placeholder') || '',
                            name: el.name || '',
                            ariaLabel: el.getAttribute('aria-label') || '',
                            title: el.getAttribute('title') || '',
                            dataTestId: el.getAttribute('data-testid') || '',
                            label: label
                        },
                        bbox: {
                            x: Math.round(pageX),
                            y: Math.round(pageY),
                            width: Math.round(rect.width),
                            height: Math.round(rect.height)
                        },
                        viewport_bbox: {
                            x: Math.round(rect.x),
                            y: Math.round(rect.y),
                            width: Math.round(rect.width),
                            height: Math.round(rect.height)
                        },
                        isVisible: rect.width > 0 && rect.height > 0,
                        isOnScreen: isOnScreen,
                        isTopmost: isTopmost
                    });
                });
            });

            const visible = elements.filter(e => e.isVisible && e.isOnScreen && e.isTopmost);

            // Keep DOM order but move dropdown options to the end.
            // Dropdown items (e.g. 88 currency options) bury critical
            // elements like submit buttons when listed inline.
            const main = visible.filter(e => e.category !== 'dropdown-option');
            const dropdown = visible.filter(e => e.category === 'dropdown-option');
            return main.concat(dropdown);
        }
        """

        try:
            raw_elements = page.evaluate(js_code)

            for idx, elem in enumerate(raw_elements):
                elem["index"] = idx
                elements.append(elem)

        except Exception as e:
            print(f"[WARN][ElementExtractor] Error extracting elements: {e}")

        return elements

    def get_element_by_index(
        self, elements: List[Dict[str, Any]], index: int
    ) -> Optional[Dict[str, Any]]:
        for elem in elements:
            if elem["index"] == index:
                return elem
        return None


def _slim_element(element: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "index": element["index"],
        "selector": element["selector"],
        "text": element["text"],
        "tag": element["tag"],
        "category": element["category"],
        "parent_context": element["parent_context"],
        "type": element.get("attributes", {}).get("type", ""),
        "href": element.get("attributes", {}).get("href", ""),
    }


def to_urls(u: Optional[Union[str, Iterable[str]]] = None) -> Optional[Iterable[str]]:
    if u is None:
        return None
    if isinstance(u, str):
        return [u]
    return u


def _prepare_script(script: str) -> str:
    """Wrap bare `return` statements in an async IIFE for Playwright evaluate()."""
    if "return " in script and not script.strip().startswith("("):
        return f"(async () => {{ {script} }})()"
    return script


def _is_target_closed(e: Exception) -> bool:
    msg = str(e)
    return "Target" in msg and "closed" in msg


class BrowserTools(AgentTools):
    urls: Optional[Iterable[str]]
    browser: playwright.sync_api.Browser
    pages: Dict[str, playwright.sync_api.Page]
    listen_network: bool
    listen_console: bool
    network_requests: Dict[str, List[playwright.sync_api.Request]]
    console_logs: Dict[str, List[playwright.sync_api.ConsoleMessage]]
    debug_mode: bool
    allow_close_page: bool
    headless: bool

    def __init__(
        self,
        url: Optional[Union[str, Iterable[str]]] = None,
        listen_network: bool = False,
        listen_console: bool = False,
        debug_mode: bool = False,
        allow_close_page: bool = True,
        headless: bool = True,
        client_certificate: Optional[ClientCertificate] = None,
    ):
        self.urls = to_urls(url)
        self.debug_mode = debug_mode
        self.allow_close_page = allow_close_page
        self.headless = headless
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.__init__] url={url}, listen_network={listen_network}, listen_console={listen_console}, debug_mode={debug_mode}, allow_close_page={allow_close_page}"
            )
            print(f"[DEBUG][BrowserTools.__init__] resolved urls={self.urls}")
        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():
                if self.debug_mode:
                    print(
                        "[DEBUG][BrowserTools.__init__] Found running event loop, unsetting it"
                    )
                asyncio._set_running_loop(None)
        except RuntimeError:
            if self.debug_mode:
                print("[DEBUG][BrowserTools.__init__] No running event loop found")
        self._playwright_context = playwright.sync_api.sync_playwright()
        pw = self._playwright_context.start()
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.__init__] Playwright started, launching chromium (headless={self.headless})"
            )
        self.browser = pw.chromium.launch(headless=self.headless)
        if self.debug_mode:
            print("[DEBUG][BrowserTools.__init__] Browser launched successfully")
        self._browser_context = self._build_browser_context(client_certificate)
        self.pages = {}
        self.listen_network = listen_network
        self.listen_console = listen_console
        self.network_requests = {}
        self.console_logs = {}
        self._extracted_elements: Dict[str, List[Dict[str, Any]]] = {}
        self.extractor = ElementExtractor()

    def _build_browser_context(
        self, client_certificate: Optional[ClientCertificate]
    ) -> playwright.sync_api.BrowserContext:
        context_options: Dict[str, Any] = {}

        if client_certificate is not None:
            origin: str = client_certificate["origin"]
            pfx_base64: str = client_certificate["pfx_base64"]
            passphrase: str = client_certificate["passphrase"]

            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools._build_browser_context] Using client certificate for origin={origin}"
                )

            context_options["client_certificates"] = [
                {
                    "origin": origin,
                    "pfx": base64.b64decode(pfx_base64),
                    "passphrase": passphrase,
                }
            ]
            context_options["ignore_https_errors"] = True

        return self.browser.new_context(**context_options)

    def close(self):
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.close] Closing {len(self.pages)} pages")
        for page_id, page in list(self.pages.items()):
            try:
                if self.debug_mode:
                    print(f"[DEBUG][BrowserTools.close] Closing page {page_id}")
                page.close()
            except Exception as e:
                if self.debug_mode:
                    print(
                        f"[DEBUG][BrowserTools.close] Error closing page {page_id}: {e}"
                    )
        self.pages.clear()

        try:
            if self.debug_mode:
                print("[DEBUG][BrowserTools.close] Closing browser context")
            self._browser_context.close()
        except Exception as e:
            if self.debug_mode:
                print(f"[DEBUG][BrowserTools.close] Error closing browser context: {e}")

        try:
            if self.debug_mode:
                print("[DEBUG][BrowserTools.close] Closing browser")
            self.browser.close()
        except Exception as e:
            if self.debug_mode:
                print(f"[DEBUG][BrowserTools.close] Error closing browser: {e}")

        try:
            if self.debug_mode:
                print("[DEBUG][BrowserTools.close] Exiting playwright context")
            self._playwright_context.__exit__(None, None, None)
        except Exception as e:
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.close] Error exiting playwright context: {e}"
                )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def _get_page(self, page_id: str) -> Page:
        if page_id not in self.pages:
            raise ValueError(f"Page '{page_id}' does not exist.")
        return self.pages[page_id]

    def _handle_page_crash(self, page_id: str):
        self.pages.pop(page_id, None)
        self._extracted_elements.pop(page_id, None)
        raise RuntimeError(
            "Browser page has closed or crashed. "
            "Call navigate_to_url to start a new session."
        )

    def _get_page_id_by_request(
        self, request: playwright.sync_api.Request
    ) -> Optional[str]:
        for page_id, page in self.pages.items():
            if request.frame.page == page:
                return page_id
        return None

    def _get_page_id_by_console_message(
        self, msg: playwright.sync_api.ConsoleMessage
    ) -> Optional[str]:
        for page_id, page in self.pages.items():
            if msg.page == page:
                return page_id
        return None

    def _attach_listeners(self, page: playwright.sync_api.Page):
        if self.listen_network:

            def on_request(request: playwright.sync_api.Request):
                page_id = self._get_page_id_by_request(request)
                if page_id:
                    if page_id not in self.network_requests:
                        self.network_requests[page_id] = []
                    self.network_requests[page_id].append(request)

            page.on("request", on_request)

        if self.listen_console:

            def on_console_message(msg: playwright.sync_api.ConsoleMessage):
                page_id = self._get_page_id_by_console_message(msg)
                if page_id:
                    if page_id not in self.console_logs:
                        self.console_logs[page_id] = []
                    self.console_logs[page_id].append(msg)

            page.on("console", on_console_message)

    def navigate_to_url(
        self, url: str, page_id: Optional[str] = None
    ) -> Dict[str, str]:
        """Navigate to a URL. If page_id is provided, reuses that page; otherwise creates a new page. Returns page_id, final url, and title. After navigation, call get_page_summary to discover interactive elements on the new page."""
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.navigate_to_url] url={url}, page_id={page_id}")
        if self.urls is not None and url not in self.urls:
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.navigate_to_url] URL not allowed. allowed_urls={list(self.urls)}"
                )
            raise PermissionError(f"URL '{url}' is not allowed.")

        if page_id is None:
            page_id = str(uuid4())
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.navigate_to_url] Creating new page with id={page_id}"
                )
            try:
                page = self._browser_context.new_page()
            except Exception as e:
                if _is_target_closed(e):
                    raise RuntimeError(
                        "Browser has closed. Cannot create new pages. "
                        "The browser session may have expired."
                    )
                raise
            if page is None:
                raise RuntimeError("Failed to create a new browser page.")
            self.pages[page_id] = page
            self._attach_listeners(page)
        else:
            page = self._get_page(page_id)
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.navigate_to_url] Reusing existing page {page_id}"
                )

        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.navigate_to_url] Navigating to {url}")

        try:
            page.goto(url)
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise

        self._extracted_elements.pop(page_id, None)
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.navigate_to_url] Navigation complete. page.url={page.url}, title={page.title()}"
            )
        return dict(page_id=page_id, url=page.url, title=page.title())

    def click(
        self,
        page_id: str,
        selector: Optional[str] = None,
        x: Optional[float] = None,
        y: Optional[float] = None,
    ):
        """Click an element by CSS selector, or click at specific x,y coordinates. Provide either selector OR both x and y. IMPORTANT: Use selectors from get_page_summary or get_element_by_summary_index. Prefer click_element(page_id, index) to avoid selector errors."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.click] page_id={page_id}, selector={selector}, x={x}, y={y}"
            )
        page = self._get_page(page_id)

        try:
            if selector is not None:
                element = page.query_selector(selector)
                if element is None:
                    available = self._get_available_selectors_hint(page_id)
                    raise ValueError(
                        f"Selector '{selector}' not found on the page. "
                        f"Use click_element(page_id, index) with an index from get_page_summary instead. "
                        f"{available}"
                    )
                page.click(selector, timeout=5000)
            elif x is not None and y is not None:
                page.mouse.click(x, y)
            else:
                raise ValueError(
                    "Provide either 'selector' OR both 'x' and 'y' coordinates."
                )
        except ValueError:
            raise
        except PlaywrightTimeoutError:
            available = self._get_available_selectors_hint(page_id)
            raise ValueError(
                f"Element '{selector}' found but not clickable (timeout). "
                f"Use click_element(page_id, index) with an index from get_page_summary. "
                f"{available}"
            )
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise

        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.click] Click complete. Current url={page.url}")

    def click_element(self, page_id: str, index: int):
        """Click an interactive element by its index from the last get_page_summary. This is the preferred way to click — pass the index number directly instead of a CSS selector. Call get_page_summary first to see available elements and their indices."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.click_element] page_id={page_id}, index={index}"
            )
        element = self._resolve_element(page_id, index)
        self.click(page_id, selector=element["selector"])
        return element

    def _resolve_element(self, page_id: str, index: int) -> Dict[str, Any]:
        page = self._get_page(page_id)
        cached = self._extracted_elements.get(page_id)
        if cached is None:
            cached = self.extractor.extract_elements(page)
            self._extracted_elements[page_id] = cached

        element = self.extractor.get_element_by_index(cached, index)

        if element is not None:
            selector = element.get("selector", "")
            try:
                if selector and not page.query_selector(selector):
                    if self.debug_mode:
                        print(
                            f"[DEBUG][BrowserTools._resolve_element] Stale selector at index {index}, re-extracting"
                        )
                    cached = self.extractor.extract_elements(page)
                    self._extracted_elements[page_id] = cached
                    element = self.extractor.get_element_by_index(cached, index)
            except Exception as e:
                if _is_target_closed(e):
                    self._handle_page_crash(page_id)
                raise

        if element is None:
            count = len(cached)
            raise ValueError(
                f"No element at index {index}. "
                f"Page has {count} elements (indices 0-{count - 1}). "
                f"Call get_page_summary to see current elements."
            )
        return element

    def _get_available_selectors_hint(self, page_id: str) -> str:
        cached = self._extracted_elements.get(page_id)
        if cached is None:
            return ""
        selectors = [
            e["selector"]
            for e in cached
            if e.get("selector") and not e["selector"].startswith("form.")
        ]
        if not selectors:
            return ""
        preview = selectors[:10]
        hint = "Available selectors from last page summary: " + ", ".join(preview)
        if len(selectors) > 10:
            hint += f" ... and {len(selectors) - 10} more"
        return hint

    def fill(self, page_id: str, selector: str, value: str):
        """Fill a form field with a value using a CSS selector. IMPORTANT: Use selectors from get_page_summary or get_element_by_summary_index. Prefer fill_element(page_id, index, value) to avoid selector errors."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.fill] page_id={page_id}, selector={selector}, value={value!r}"
            )
        page = self._get_page(page_id)

        try:
            element = page.query_selector(selector)
            if element is None:
                available = self._get_available_selectors_hint(page_id)
                raise ValueError(
                    f"Selector '{selector}' not found on the page. "
                    f"Use fill_element(page_id, index, value) with an index from get_page_summary instead. "
                    f"{available}"
                )
            page.fill(selector, value, timeout=5000)
        except ValueError:
            raise
        except PlaywrightTimeoutError:
            available = self._get_available_selectors_hint(page_id)
            raise ValueError(
                f"Element '{selector}' found but not fillable (timeout). "
                f"Use fill_element(page_id, index, value) with an index from get_page_summary. "
                f"{available}"
            )
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise

        if self.debug_mode:
            print("[DEBUG][BrowserTools.fill] Fill complete")

    def fill_element(self, page_id: str, index: int, value: str):
        """Fill a form field by its index from the last get_page_summary. This is the preferred way to fill — pass the index number directly instead of a CSS selector. Call get_page_summary first to see available elements and their indices."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.fill_element] page_id={page_id}, index={index}, value={value!r}"
            )
        element = self._resolve_element(page_id, index)
        self.fill(page_id, selector=element["selector"], value=value)
        return element

    def get_html(self, page_id: str) -> str:
        """Get the full HTML content of the page. Prefer get_page_summary for identifying interactive elements — use this only when you need raw HTML inspection."""
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_html] page_id={page_id}")
        page = self._get_page(page_id)
        try:
            content = page.content()
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_html] Got HTML content, length={len(content)}"
            )
        return content

    def get_text(self, page_id: str, selector: str) -> str:
        """Get the inner text content of an element by CSS selector."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_text] page_id={page_id}, selector={selector}"
            )
        page = self._get_page(page_id)
        try:
            element = page.query_selector(selector)
            if element is None:
                raise ValueError(
                    f"Selector '{selector}' not found. "
                    f"Call get_page_summary to see current elements."
                )
            text = page.inner_text(selector)
        except ValueError:
            raise
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_text] Got text, length={len(text)}, preview={text[:200]!r}"
            )
        return text

    def get_attribute(
        self, page_id: str, selector: str, attribute: str
    ) -> Optional[str]:
        """Get a single HTML attribute value from an element by CSS selector."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_attribute] page_id={page_id}, selector={selector}, attribute={attribute}"
            )
        page = self._get_page(page_id)
        try:
            element = page.query_selector(selector)
            if element is None:
                raise ValueError(
                    f"Selector '{selector}' not found. "
                    f"Call get_page_summary to see current elements."
                )
            value = page.get_attribute(selector, attribute)
        except ValueError:
            raise
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_attribute] Result: {value!r}")
        return value

    def get_attributes(self, page_id: str, selector: str) -> Dict[str, Optional[str]]:
        """Get all HTML attributes of an element by CSS selector. Returns a dict of attribute name to value."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_attributes] page_id={page_id}, selector={selector}"
            )
        page = self._get_page(page_id)
        try:
            element_handle = page.query_selector(selector)
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise
        if element_handle is None:
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.get_attributes] No element found for selector={selector}"
                )
            raise ValueError(f"Selector '{selector}' did not match any elements.")
        attrs = element_handle.evaluate(
            "el => { const attrs = {}; for (let attr of el.attributes) { attrs[attr.name] = attr.value; } return attrs; }"
        )
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_attributes] Found {len(attrs)} attributes: {list(attrs.keys())}"
            )
        return attrs

    def get_all_links(self, page_id: str) -> List[Dict[str, str]]:
        """Get all links on the page as a list of {text, href} objects."""
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_all_links] page_id={page_id}")
        page = self._get_page(page_id)
        try:
            links = page.query_selector_all("a")
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_all_links] Found {len(links)} <a> elements"
            )
        result = []
        for link in links:
            href = link.get_attribute("href")
            if href is not None:
                result.append({"text": link.inner_text(), "href": href})
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_all_links] Returning {len(result)} links with href"
            )
        return result

    def get_network_requests(self, page_id: str) -> Iterable[dict]:
        """Get all captured network requests for a page. Requires listen_network=True on initialization."""
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_network_requests] page_id={page_id}")
        self._get_page(page_id)

        requests = self.network_requests.get(page_id, [])
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_network_requests] Found {len(requests)} requests for page {page_id}"
            )
            for r in requests:
                print(
                    f"[DEBUG][BrowserTools.get_network_requests]   {r.method} {r.url}"
                )

        result = []
        for request in requests:
            res = request.response()
            result.append(
                {
                    "request": {
                        "url": request.url,
                        "method": request.method,
                        "headers": dict(request.headers),
                        "post_data": request.post_data,
                    },
                    "response": {
                        "status": res.status if res else None,
                        "headers": dict(res.headers) if res else None,
                        "body": res.text() if res else None,
                    },
                }
            )
        return result

    def get_console_logs(self, page_id: str) -> Iterable[dict]:
        """Get all captured console log messages for a page. Requires listen_console=True on initialization."""
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_console_logs] page_id={page_id}")
        self._get_page(page_id)

        logs = self.console_logs.get(page_id, [])
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_console_logs] Found {len(logs)} console messages for page {page_id}"
            )

        return [
            {
                "type": msg.type,
                "text": msg.text,
                "location": {
                    "url": msg.location["url"],
                    "lineNumber": msg.location["lineNumber"],
                    "columnNumber": msg.location["columnNumber"],
                }
                if msg.location
                else None,
            }
            for msg in logs
        ]

    def list_pages(self) -> Iterable[dict]:
        """List all open browser pages with their page_id, URL, and title."""
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.list_pages] Total pages: {len(self.pages)}")
            for pid, p in self.pages.items():
                print(
                    f"[DEBUG][BrowserTools.list_pages]   page_id={pid}, url={p.url}, title={p.title()}"
                )
        return [
            {
                "page_id": page_id,
                "url": page.url,
                "title": page.title(),
            }
            for page_id, page in self.pages.items()
        ]

    def wait(self, page_id: str, milliseconds: int = 1000):
        """Wait for a specified number of milliseconds (default 1000). Use this instead of execute_javascript with setTimeout — it does NOT invalidate the element cache. Useful for waiting after clicks, form submissions, or page transitions before taking a screenshot or calling get_page_summary."""
        if milliseconds < 0 or milliseconds > 30000:
            raise ValueError("milliseconds must be between 0 and 30000.")
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.wait] page_id={page_id}, milliseconds={milliseconds}"
            )
        page = self._get_page(page_id)
        try:
            page.wait_for_timeout(milliseconds)
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise
        if self.debug_mode:
            print("[DEBUG][BrowserTools.wait] Wait complete")

    def close_page(self, page_id: str):
        """Close a browser page by its page_id."""
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.close_page] page_id={page_id}")
        if page_id in self.pages:
            page = self.pages[page_id]
            page.close()
            del self.pages[page_id]
            self._extracted_elements.pop(page_id, None)
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.close_page] Page closed. Remaining pages: {list(self.pages.keys())}"
                )
        else:
            raise ValueError(f"Page '{page_id}' does not exist.")

    def execute_javascript(self, page_id: str, script: str):
        """Execute JavaScript code on the page and return the result. WARNING: JavaScript execution may change the DOM. After calling this, the cached page summary is invalidated — call get_page_summary before using any selectors from a previous summary."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.execute_javascript] page_id={page_id}, script={script[:200]!r}"
            )
        page = self._get_page(page_id)
        script = _prepare_script(script)
        try:
            result = page.evaluate(script)
        except PlaywrightTimeoutError:
            raise ValueError(
                "JavaScript execution timed out. "
                "Simplify the script or check for infinite loops."
            )
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            error_str = str(e)
            if "SyntaxError" in error_str:
                raise ValueError(
                    f"JavaScript syntax error: {error_str}. "
                    f"Check for invalid syntax. Do not use bare 'return' statements."
                )
            raise
        self._extracted_elements.pop(page_id, None)
        if self.debug_mode:
            result_preview = repr(result)[:500] if result is not None else "None"
            print(f"[DEBUG][BrowserTools.execute_javascript] Result: {result_preview}")
        return result

    def get_page_summary(self, page_id: str, max_elements: int = 50):
        """Return a list of interactive elements visible on the page (up to max_elements, default 50). Each element has: index, selector, text, tag, category, parent_context, type, href. Use the index with click_element(page_id, index) or fill_element(page_id, index, value) to interact. Call this after ANY action that changes the DOM to get fresh data."""
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_page_summary] page_id={page_id}")
        page = self._get_page(page_id)
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_page_summary] Extracting elements from page url={page.url}"
            )
        try:
            full_elements = self.extractor.extract_elements(page)
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise
        self._extracted_elements[page_id] = full_elements
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_page_summary] Extracted {len(full_elements)} elements"
            )
            for elem in full_elements:
                print(
                    f"[DEBUG][BrowserTools.get_page_summary]   [{elem['index']}] <{elem['tag']}> text={elem['text'][:50]!r} bbox={elem['viewport_bbox']} selector={elem['selector'][:80]}"
                )
        slim = [_slim_element(e) for e in full_elements]
        total = len(slim)
        if total > max_elements:
            slim = slim[:max_elements]
            slim.append(
                {
                    "note": (
                        f"{total - max_elements} more elements not shown (total: {total}). "
                        f"click_element/fill_element still work with any index 0-{total - 1}. "
                        f"Call get_page_summary(page_id, max_elements={total}) to see all."
                    )
                }
            )
        return slim

    def get_element_by_summary_index(self, page_id: str, index: int):
        """Get detailed information about a specific element by its index from the last get_page_summary result. Returns the full element data including selector, text, tag, bbox, attributes. Use this when you need details beyond what get_page_summary shows (e.g., coordinates, attributes)."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_element_by_summary_index] page_id={page_id}, index={index}"
            )
        element = self._resolve_element(page_id, index)
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_element_by_summary_index] Found element: <{element['tag']}> text={element['text'][:50]!r}"
            )
        return element

    def screenshot(
        self,
        page_id: str,
        show_markers: bool = False,
        highlight_element: Optional[str] = None,
    ) -> Path:
        """Take a screenshot of the page for visual analysis. Use show_markers=True to overlay numbered labels on all interactive elements (buttons, links, inputs). Use highlight_element with a CSS selector to highlight a specific element with a red border."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.screenshot] page_id={page_id}, show_markers={show_markers}, highlight_element={highlight_element}"
            )
        page = self._get_page(page_id)

        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.screenshot] Taking screenshot of url={page.url}"
            )

        if show_markers:
            try:
                full_elements = self.extractor.extract_elements(page)
            except Exception as e:
                if _is_target_closed(e):
                    self._handle_page_crash(page_id)
                raise
            self._extracted_elements[page_id] = full_elements
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.screenshot] Injecting markers for {len(full_elements)} elements"
                )
            marker_js = """
            (elements) => {
                const container = document.createElement('div');
                container.id = '__abstra_markers__';
                container.style.pointerEvents = 'none';
                container.style.position = 'absolute';
                container.style.top = '0';
                container.style.left = '0';
                container.style.zIndex = '2147483647';
                document.body.appendChild(container);

                elements.forEach((elem) => {
                    const border = document.createElement('div');
                    border.style.position = 'absolute';
                    border.style.left = elem.bbox.x + 'px';
                    border.style.top = elem.bbox.y + 'px';
                    border.style.width = elem.bbox.width + 'px';
                    border.style.height = elem.bbox.height + 'px';
                    border.style.border = '2px solid rgba(255, 0, 0, 0.7)';
                    border.style.borderRadius = '2px';
                    border.style.pointerEvents = 'none';
                    container.appendChild(border);

                    const label = document.createElement('div');
                    label.textContent = elem.index;
                    label.style.position = 'absolute';
                    label.style.left = elem.bbox.x + 'px';
                    label.style.top = (elem.bbox.y - 24) + 'px';
                    label.style.background = 'rgba(255, 0, 0, 0.85)';
                    label.style.color = 'white';
                    label.style.fontSize = '16px';
                    label.style.fontWeight = 'bold';
                    label.style.fontFamily = 'monospace';
                    label.style.padding = '2px 6px';
                    label.style.borderRadius = '4px';
                    label.style.lineHeight = '20px';
                    label.style.pointerEvents = 'none';
                    label.style.whiteSpace = 'nowrap';
                    container.appendChild(label);
                });
            }
            """
            page.evaluate(marker_js, full_elements)

        highlight_css = None
        if highlight_element:
            safe_selector = highlight_element.replace("\\", "\\\\").replace('"', '\\"')
            highlight_css = f"{safe_selector} {{ outline: 3px solid red !important; box-shadow: 0 0 8px rgba(255,0,0,0.6) !important; }}"
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.screenshot] Highlight CSS for selector: {highlight_element}"
                )

        screenshot_kwargs: Dict[str, Any] = {"type": "jpeg", "full_page": show_markers}
        if highlight_css:
            screenshot_kwargs["style"] = highlight_css

        try:
            image_data = page.screenshot(**screenshot_kwargs)
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise

        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.screenshot] Screenshot taken, size={len(image_data)} bytes"
            )

        if show_markers:
            page.evaluate(
                "() => { const el = document.getElementById('__abstra_markers__'); if (el) el.remove(); }"
            )
            if self.debug_mode:
                print("[DEBUG][BrowserTools.screenshot] Marker overlays removed")

        with NamedTemporaryFile(delete=False, suffix=".jpg") as f:
            image_path = Path(f.name)
            if self.debug_mode:
                print(f"[DEBUG][BrowserTools.screenshot] Saving to {image_path}")
            image_path.write_bytes(image_data)

        return image_path

    def __tools__(self):
        tools = [
            self.navigate_to_url.__name__,
            self.list_pages.__name__,
            self.click.__name__,
            self.click_element.__name__,
            self.fill.__name__,
            self.fill_element.__name__,
            self.get_html.__name__,
            self.get_text.__name__,
            self.get_page_summary.__name__,
            self.get_element_by_summary_index.__name__,
            self.get_attribute.__name__,
            self.get_attributes.__name__,
            self.get_all_links.__name__,
            self.execute_javascript.__name__,
            self.wait.__name__,
            self.screenshot.__name__,
        ]

        if self.allow_close_page:
            tools.append(self.close_page.__name__)
        if self.listen_network:
            tools.append(self.get_network_requests.__name__)
        if self.listen_console:
            tools.append(self.get_console_logs.__name__)

        return tools
