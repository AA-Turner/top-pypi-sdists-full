import asyncio
from collections.abc import Iterable
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

import playwright.sync_api
from playwright.sync_api import Page

from .base import AgentTools


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
                'input',  // All input fields
                'textarea',  // Text areas
                'select',  // Dropdowns
                '[role="button"]',
                '[onclick]',
                '[tabindex]:not([tabindex="-1"])'
            ];

            const seen = new Set();

            // Helper to get associated label for an input
            function getLabel(el) {
                // Try aria-label first (often most descriptive for icons)
                const ariaLabel = el.getAttribute('aria-label');
                if (ariaLabel) return ariaLabel;

                // Try title (tooltip)
                const title = el.getAttribute('title');
                if (title) return title;

                // Try id-based label
                if (el.id) {
                    const label = document.querySelector(`label[for="${el.id}"]`);
                    if (label) return label.innerText.trim();
                }

                // Try parent label
                const parentLabel = el.closest('label');
                if (parentLabel) return parentLabel.innerText.trim();

                // Try placeholder
                const placeholder = el.getAttribute('placeholder');
                if (placeholder) return `[${placeholder}]`;

                return '';
            }

            // Helper to get semantic parent context
            function getParentContext(el) {
                const semanticParents = [
                    'form', 'nav', 'header', 'footer', 'main', 'aside', 'section', 'article', 'dialog',
                    '[role="dialog"]', '[role="navigation"]', '[role="form"]', '[role="banner"]', '[role="contentinfo"]'
                ];

                const parent = el.closest(semanticParents.join(','));
                if (!parent) return 'BODY';

                let context = parent.tagName.toLowerCase();

                // Enhance context with attributes
                if (parent.getAttribute('aria-label')) context += ` (${parent.getAttribute('aria-label')})`;
                else if (parent.id) context += ` (#${parent.id})`;
                else if (parent.getAttribute('role')) context += ` [role="${parent.getAttribute('role')}"]`;

                return context.toUpperCase();
            }

            selectors.forEach(selector => {
                document.querySelectorAll(selector).forEach((el, idx) => {
                    // Skip if already seen
                    if (seen.has(el)) return;
                    seen.add(el);

                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);

                    // Improved visibility check
                    const isVisible = rect.width > 0 &&
                                    rect.height > 0 &&
                                    style.visibility !== 'hidden' &&
                                    style.display !== 'none' &&
                                    style.opacity !== '0';

                    if (!isVisible) return;

                    // Check if element is at least partially within the viewport
                    const vw = window.innerWidth;
                    const vh = window.innerHeight;
                    const isOnScreen = rect.right > 0 &&
                                       rect.bottom > 0 &&
                                       rect.left < vw &&
                                       rect.top < vh;

                    // Generate TRULY unique selector using nth-child
                    let uniqueSelector = '';
                    if (el.id) {
                        uniqueSelector = `#${el.id}`;
                    } else {
                        // Build path from element to body with nth-child for uniqueness
                        let path = [];
                        let current = el;
                        while (current && current !== document.body) {
                            let selector = current.tagName.toLowerCase();

                            // Add classes if present (for readability)
                            // Note: SVG elements have className as SVGAnimatedString, not string
                            if (current.className && typeof current.className === 'string') {
                                const classes = current.className.split(' ')
                                    .filter(c => c && !c.startsWith('css-'))
                                    .slice(0, 2);
                                if (classes.length > 0) {
                                    selector += '.' + classes.join('.');
                                }
                            }

                            // **CRITICAL**: Add nth-child to ensure uniqueness
                            // Find position among siblings of same type
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

                    // Get label/context for form fields
                    const label = getLabel(el);
                    const parentContext = getParentContext(el);

                    // Build text representation
                    // Prioritize: innerText -> aria-label -> title -> value -> alt -> label
                    let text = el.innerText?.trim().substring(0, 100) ||
                               el.getAttribute('aria-label') ||
                               el.getAttribute('title') ||
                               el.value ||
                               el.alt ||
                               label ||
                               '';

                    // Convert viewport-relative coords to page-absolute
                    // (needed for full_page screenshot annotation alignment)
                    const pageX = rect.x + window.scrollX;
                    const pageY = rect.y + window.scrollY;

                    elements.push({
                        selector: uniqueSelector,
                        text: text,
                        tag: el.tagName.toLowerCase(),
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
                        // viewport-relative coords for click targeting
                        viewport_bbox: {
                            x: Math.round(rect.x),
                            y: Math.round(rect.y),
                            width: Math.round(rect.width),
                            height: Math.round(rect.height)
                        },
                        isVisible: rect.width > 0 && rect.height > 0,
                        isOnScreen: isOnScreen
                    });
                });
            });

            return elements.filter(e => e.isVisible);
        }
        """

        try:
            raw_elements = page.evaluate(js_code)

            for idx, elem in enumerate(raw_elements):
                elem["index"] = idx
                elements.append(elem)

        except Exception as e:
            print(f"⚠️  Error extracting elements: {e}")

        return elements

    def get_element_by_index(
        self, elements: List[Dict[str, Any]], index: int
    ) -> Optional[Dict[str, Any]]:
        for elem in elements:
            if elem["index"] == index:
                return elem
        return None


def to_urls(u: Optional[Union[str, Iterable[str]]] = None) -> Optional[Iterable[str]]:
    if u is None:
        return None
    if isinstance(u, str):
        return [u]
    return u


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
        self.pages = {}
        self.listen_network = listen_network
        self.listen_console = listen_console
        if listen_network:
            self._setup_network_listener()
        self.last_extracted_elements = None
        self.extractor = ElementExtractor()

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
                print("[DEBUG][BrowserTools.close] Closing browser")
            self.browser.close()
        except Exception as e:
            if self.debug_mode:
                print(f"[DEBUG][BrowserTools.close] Error closing browser: {e}")

        try:
            if self.debug_mode:
                print("[DEBUG][BrowserTools.close] Exiting playwright context")
            self._playwright_context.__exit__()
        except Exception as e:
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.close] Error exiting playwright context: {e}"
                )

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

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

    def _setup_network_listener(self):
        def on_request(request: playwright.sync_api.Request):
            page_id = self._get_page_id_by_request(request)
            if page_id:
                if not hasattr(self, "network_requests"):
                    self.network_requests = {}
                if page_id not in self.network_requests:
                    self.network_requests[page_id] = []
                self.network_requests[page_id].append(request)

        def on_console_message(msg: playwright.sync_api.ConsoleMessage):
            page_id = self._get_page_id_by_console_message(msg)
            if page_id:
                if not hasattr(self, "console_logs"):
                    self.console_logs = {}
                if page_id not in self.console_logs:
                    self.console_logs[page_id] = []
                self.console_logs[page_id].append(msg)

        for page in self.pages.values():
            if self.listen_network:
                page.on("request", on_request)
            if self.listen_console:
                page.on("console", on_console_message)

    def navigate_to_url(
        self, url: str, page_id: Optional[str] = None
    ) -> Dict[str, str]:
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
            page = self.browser.new_page()
            if page is None:
                raise RuntimeError("Failed to create a new browser page.")
            self.pages[page_id] = page
        else:
            page_id = page_id
            if page_id not in self.pages:
                raise ValueError(f"Page '{page_id}' does not exist.")
            page = self.pages[page_id]
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.navigate_to_url] Reusing existing page {page_id}"
                )

        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.navigate_to_url] Navigating to {url}")
        page.goto(url)
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.navigate_to_url] Navigation complete. page.url={page.url}, title={page.title()}"
            )
        return dict(page_id=page_id)

    def click(
        self,
        page_id: str,
        selector: Optional[str] = None,
        x: Optional[float] = None,
        y: Optional[float] = None,
    ):
        """Click an element by CSS selector, or click at a specific position using x,y coordinates (viewport-relative pixels). Provide either selector OR both x and y."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.click] page_id={page_id}, selector={selector}, x={x}, y={y}"
            )
        if page_id not in self.pages:
            raise ValueError(f"Page '{page_id}' does not exist.")
        page = self.pages[page_id]
        if selector is not None:
            page.click(selector)
        elif x is not None and y is not None:
            page.mouse.click(x, y)
        else:
            raise ValueError(
                "Provide either 'selector' OR both 'x' and 'y' coordinates."
            )
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.click] Click complete. Current url={page.url}")

    def fill(self, page_id: str, selector: str, value: str):
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.fill] page_id={page_id}, selector={selector}, value={value!r}"
            )
        if page_id not in self.pages:
            raise ValueError(f"Page '{page_id}' does not exist.")
        page = self.pages[page_id]
        page.fill(selector, value)
        if self.debug_mode:
            print("[DEBUG][BrowserTools.fill] Fill complete")

    def get_html(self, page_id: str) -> str:
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_html] page_id={page_id}")
        if page_id not in self.pages:
            raise ValueError(f"Page '{page_id}' does not exist.")
        page = self.pages[page_id]
        content = page.content()
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_html] Got HTML content, length={len(content)}"
            )
        return content

    def get_text(self, page_id: str, selector: str) -> str:
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_text] page_id={page_id}, selector={selector}"
            )
        if page_id not in self.pages:
            raise ValueError(f"Page '{page_id}' does not exist.")
        page = self.pages[page_id]
        text = page.inner_text(selector)
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_text] Got text, length={len(text)}, preview={text[:200]!r}"
            )
        return text

    def get_attribute(
        self, page_id: str, selector: str, attribute: str
    ) -> Optional[str]:
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_attribute] page_id={page_id}, selector={selector}, attribute={attribute}"
            )
        if page_id not in self.pages:
            raise ValueError(f"Page '{page_id}' does not exist.")
        page = self.pages[page_id]
        value = page.get_attribute(selector, attribute)
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_attribute] Result: {value!r}")
        return value

    def get_attributes(self, page_id: str, selector: str) -> Dict[str, Optional[str]]:
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_attributes] page_id={page_id}, selector={selector}"
            )
        if page_id not in self.pages:
            raise ValueError(f"Page '{page_id}' does not exist.")
        page = self.pages[page_id]
        element_handle = page.query_selector(selector)
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

    def get_all_links(self, page_id: str) -> Dict[str, str]:
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_all_links] page_id={page_id}")
        if page_id not in self.pages:
            raise ValueError(f"Page '{page_id}' does not exist.")
        page = self.pages[page_id]
        links = page.query_selector_all("a")
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_all_links] Found {len(links)} <a> elements"
            )
        result = {
            link.inner_text(): href
            for link in links
            if (href := link.get_attribute("href")) is not None
        }
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_all_links] Returning {len(result)} links with href"
            )
        return result

    def get_network_requests(self, page_id: str) -> Iterable[dict]:
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_network_requests] page_id={page_id}")
        if page_id not in self.pages:
            raise ValueError(f"Page '{page_id}' does not exist.")

        requests = self.network_requests.get(page_id, [])
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_network_requests] Found {len(requests)} requests for page {page_id}"
            )
            for r in requests:
                print(
                    f"[DEBUG][BrowserTools.get_network_requests]   {r.method} {r.url}"
                )

        return [
            {
                "request": {
                    "url": request.url,
                    "method": request.method,
                    "headers": dict(request.headers),
                    "post_data": request.post_data,
                },
                "response": {
                    "status": res.status if (res := request.response()) else None,
                    "headers": dict(res.headers)
                    if (res := request.response())
                    else None,
                    "body": res.text() if (res := request.response()) else None,
                },
            }
            for request in self.network_requests.get(page_id, [])
        ]

    def get_console_logs(self, page_id: str) -> Iterable[dict]:
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_console_logs] page_id={page_id}")
        if page_id not in self.pages:
            raise ValueError(f"Page '{page_id}' does not exist.")

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
            for msg in self.console_logs.get(page_id, [])
        ]

    def list_pages(self) -> Iterable[dict]:
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

    def close_page(self, page_id: str):
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.close_page] page_id={page_id}")
        if page_id in self.pages:
            page = self.pages[page_id]
            page.close()
            del self.pages[page_id]
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.close_page] Page closed. Remaining pages: {list(self.pages.keys())}"
                )
        else:
            raise ValueError(f"Page '{page_id}' does not exist.")

    def execute_javascript(self, page_id: str, script: str):
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.execute_javascript] page_id={page_id}, script={script[:200]!r}"
            )
        if page_id not in self.pages:
            raise ValueError(f"Page '{page_id}' does not exist.")
        page = self.pages[page_id]
        result = page.evaluate(script)
        if self.debug_mode:
            result_preview = repr(result)[:500] if result is not None else "None"
            print(f"[DEBUG][BrowserTools.execute_javascript] Result: {result_preview}")
        return result

    def get_page_summary(self, page_id: str):
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_page_summary] page_id={page_id}")
        if page_id not in self.pages:
            raise ValueError(f"Page '{page_id}' does not exist.")
        page = self.pages[page_id]
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_page_summary] Extracting elements from page url={page.url}"
            )
        self.last_extracted_elements = self.extractor.extract_elements(page)
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_page_summary] Extracted {len(self.last_extracted_elements)} elements"
            )
            for elem in self.last_extracted_elements:
                print(
                    f"[DEBUG][BrowserTools.get_page_summary]   [{elem['index']}] <{elem['tag']}> text={elem['text'][:50]!r} bbox={elem['viewport_bbox']} selector={elem['selector'][:80]}"
                )
        return self.last_extracted_elements

    def get_element_by_summary_index(self, page_id: str, index: int):
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_element_by_summary_index] page_id={page_id}, index={index}"
            )
        if page_id not in self.pages:
            raise ValueError(f"Page '{page_id}' does not exist.")
        page = self.pages[page_id]
        if self.last_extracted_elements is None:
            if self.debug_mode:
                print(
                    "[DEBUG][BrowserTools.get_element_by_summary_index] No cached elements, extracting now"
                )
            self.last_extracted_elements = self.extractor.extract_elements(page)
        element = self.extractor.get_element_by_index(
            self.last_extracted_elements, index
        )
        if self.debug_mode:
            if element:
                print(
                    f"[DEBUG][BrowserTools.get_element_by_summary_index] Found element: <{element['tag']}> text={element['text'][:50]!r}"
                )
            else:
                print(
                    f"[DEBUG][BrowserTools.get_element_by_summary_index] No element found at index {index}"
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
        if page_id not in self.pages:
            raise ValueError(f"Page '{page_id}' does not exist.")

        page = self.pages[page_id]

        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.screenshot] Taking screenshot of url={page.url}"
            )

        # Inject marker overlays for interactive elements
        if show_markers:
            self.last_extracted_elements = self.extractor.extract_elements(page)
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.screenshot] Injecting markers for {len(self.last_extracted_elements)} elements"
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
                    // Highlight border around the element
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

                    // Numbered label at top-left corner
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
            page.evaluate(marker_js, self.last_extracted_elements)

        # Build highlight CSS for a specific element
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

        image_data = page.screenshot(**screenshot_kwargs)
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.screenshot] Screenshot taken, size={len(image_data)} bytes"
            )

        # Remove injected marker overlays
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
            self.fill.__name__,
            self.get_html.__name__,
            self.get_text.__name__,
            self.get_page_summary.__name__,
            self.get_element_by_summary_index.__name__,
            self.get_attribute.__name__,
            self.get_attributes.__name__,
            self.get_all_links.__name__,
            self.execute_javascript.__name__,
            self.screenshot.__name__,
        ]

        if self.allow_close_page:
            tools.append(self.close_page.__name__)
        if self.listen_network:
            tools.append(self.get_network_requests.__name__)
        if self.listen_console:
            tools.append(self.get_console_logs.__name__)

        return tools
