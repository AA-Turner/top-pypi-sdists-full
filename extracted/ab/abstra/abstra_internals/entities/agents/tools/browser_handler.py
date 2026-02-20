import json
import os
import time
from typing import Any, Dict

from abstra_internals.constants import get_persistent_dir
from abstra_internals.entities.agents.tools.browser_session import BrowserSession
from abstra_internals.entities.agents.tools.click_strategy import ClickStrategyLearner

DOWNLOAD_KEYWORDS = [
    "download",
    "baixar",
    "exportar",
    "export",
    "excel",
    "xlsx",
    "csv",
    "pdf",
    "imprimir",
    "print",
    "gerar",
    "generate",
    "arquivo",
    "file",
    "report",
    "save",
    "salvar",
]


class NavigateHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "navigate"

    @property
    def description(self) -> str:
        return "Navigate the browser to a URL. Returns the page state with interactive elements."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to navigate to (must start with http:// or https://).",
                },
            },
            "required": ["url"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        url = action_input.get("url", "")
        if not url:
            return "Error: 'url' is required."
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        self._session.ensure_browser()
        page = self._session.page

        for wait_until in ["networkidle", "domcontentloaded", "load"]:
            try:
                page.goto(url, wait_until=wait_until, timeout=30000)
                break
            except Exception:
                if wait_until == "load":
                    return f"Error: Failed to navigate to {url}"
                continue

        self._session.wait_for_page_ready(timeout_ms=15000)
        self._session.inject_blob_interceptor()
        return self._session.get_page_summary()


class ClickHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session
        self._click_learner = ClickStrategyLearner()

    @property
    def name(self) -> str:
        return "click"

    @property
    def description(self) -> str:
        return "Click an interactive element by its index number from the page summary."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "index": {
                    "type": "integer",
                    "description": "The index of the element to click.",
                },
            },
            "required": ["index"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        index = action_input.get("index")
        if index is None:
            return "Error: 'index' is required."

        self._session.ensure_browser()
        elem = self._session.get_element_by_index(int(index))
        if elem is None:
            return f"Error: No element found with index {index}."

        selector = elem.get("selector", "")
        text = (elem.get("text", "") or "")[:50]
        element_type = elem.get("tag", "unknown")
        bbox = elem.get("bbox", {})
        viewport_bbox = elem.get("viewport_bbox", bbox)
        page = self._session.page

        click_success = False
        successful_strategy = None
        strategies = self._click_learner.get_ordered_strategies(element_type)

        for strategy in strategies:
            if click_success:
                break
            try:
                if strategy == "bbox":
                    vbbox = viewport_bbox
                    if not vbbox or vbbox.get("x") is None or vbbox.get("y") is None:
                        self._click_learner.record_result(element_type, strategy, False)
                        continue
                    click_x = vbbox["x"] + (vbbox.get("width", 0) / 2)
                    click_y = vbbox["y"] + (vbbox.get("height", 0) / 2)
                    viewport = page.viewport_size
                    if (
                        click_x < 0
                        or click_y < 0
                        or (
                            viewport
                            and (
                                click_x > viewport["width"]
                                or click_y > viewport["height"]
                            )
                        )
                    ):
                        self._click_learner.record_result(element_type, strategy, False)
                        continue
                    page.mouse.click(click_x, click_y)
                    click_success = True
                    successful_strategy = "bbox"
                elif strategy == "text":
                    if not text or len(text) <= 2:
                        self._click_learner.record_result(element_type, strategy, False)
                        continue
                    loc = page.get_by_text(text, exact=True)
                    if loc.count() == 1:
                        loc.click(timeout=5000)
                    else:
                        page.get_by_text(text, exact=False).first.click(timeout=5000)
                    click_success = True
                    successful_strategy = "text"
                elif strategy == "selector":
                    page.locator(selector).first.click(timeout=5000)
                    click_success = True
                    successful_strategy = "selector"
                elif strategy == "force":
                    page.locator(selector).first.click(force=True, timeout=5000)
                    click_success = True
                    successful_strategy = "force"
                elif strategy == "js":
                    page.locator(selector).first.evaluate("el => el.click()")
                    click_success = True
                    successful_strategy = "js"
            except Exception:
                self._click_learner.record_result(element_type, strategy, False)
                continue

        if click_success and successful_strategy:
            self._click_learner.record_result(element_type, successful_strategy, True)
        if not click_success:
            return f"Error: Failed to click element {index} ({text})."

        text_lower = (text or "").lower()
        is_potential_download = any(kw in text_lower for kw in DOWNLOAD_KEYWORDS)
        if is_potential_download:
            self._session.inject_blob_interceptor()
            if not self._session.wait_for_pending_downloads(timeout=3.0):
                page.wait_for_timeout(2000)

        self._session.wait_for_page_ready(timeout_ms=8000)
        return self._session.get_page_summary()


class TypeTextHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "type_text"

    @property
    def description(self) -> str:
        return "Type text into an input field by its index number."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "index": {
                    "type": "integer",
                    "description": "The index of the input element.",
                },
                "text": {"type": "string", "description": "The text to type."},
            },
            "required": ["index", "text"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        index = action_input.get("index")
        text = action_input.get("text", "")
        if index is None:
            return "Error: 'index' is required."

        self._session.ensure_browser()
        elem = self._session.get_element_by_index(int(index))
        if elem is None:
            return f"Error: No element found with index {index}."

        selector = elem.get("selector", "")
        page = self._session.page

        try:
            locator = page.locator(selector).first
            locator.click(timeout=5000)
            locator.fill("")
            locator.type(text, delay=50)
            self._session.wait_for_page_ready(timeout_ms=5000)
            return self._session.get_page_summary()
        except Exception as e:
            return f"Error typing into element {index}: {e}"


class PressKeyHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "press_key"

    @property
    def description(self) -> str:
        return "Press a keyboard key (e.g. 'Enter', 'Tab', 'Escape', 'ArrowDown')."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "The key to press."},
            },
            "required": ["key"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        key = action_input.get("key", "")
        if not key:
            return "Error: 'key' is required."

        self._session.ensure_browser()
        page = self._session.page

        try:
            page.keyboard.press(key)
            wait_ms = 8000 if key.lower() == "enter" else 3000
            self._session.wait_for_page_ready(timeout_ms=wait_ms)
            return self._session.get_page_summary()
        except Exception as e:
            return f"Error pressing key '{key}': {e}"


class SelectOptionHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "select_option"

    @property
    def description(self) -> str:
        return "Select an option from a dropdown/select element by its index number."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "index": {
                    "type": "integer",
                    "description": "The index of the select element.",
                },
                "option": {
                    "type": "string",
                    "description": "The value or visible text of the option.",
                },
            },
            "required": ["index", "option"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        index = action_input.get("index")
        option = action_input.get("option", "")
        if index is None:
            return "Error: 'index' is required."

        self._session.ensure_browser()
        elem = self._session.get_element_by_index(int(index))
        if elem is None:
            return f"Error: No element found with index {index}."

        selector = elem.get("selector", "")
        page = self._session.page

        try:
            page.locator(selector).first.select_option(option, timeout=5000)
            self._session.wait_for_page_ready(timeout_ms=3000)
            return self._session.get_page_summary()
        except Exception as e:
            return f"Error selecting option '{option}' on element {index}: {e}"


class HoverHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "hover"

    @property
    def description(self) -> str:
        return "Hover over an interactive element by its index number."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "index": {
                    "type": "integer",
                    "description": "The index of the element to hover over.",
                },
            },
            "required": ["index"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        index = action_input.get("index")
        if index is None:
            return "Error: 'index' is required."

        self._session.ensure_browser()
        elem = self._session.get_element_by_index(int(index))
        if elem is None:
            return f"Error: No element found with index {index}."

        selector = elem.get("selector", "")
        page = self._session.page

        try:
            page.locator(selector).first.hover(timeout=10000)
            self._session.wait_for_page_ready(timeout_ms=3000)
            return self._session.get_page_summary()
        except Exception as e:
            return f"Error hovering over element {index}: {e}"


class CheckCheckboxHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "check_checkbox"

    @property
    def description(self) -> str:
        return "Check or uncheck a checkbox by its index number."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "index": {
                    "type": "integer",
                    "description": "The index of the checkbox element.",
                },
                "checked": {
                    "type": "boolean",
                    "description": "True to check, False to uncheck.",
                },
            },
            "required": ["index"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        index = action_input.get("index")
        if index is None:
            return "Error: 'index' is required."
        should_check = action_input.get("checked", True)

        self._session.ensure_browser()
        elem = self._session.get_element_by_index(int(index))
        if elem is None:
            return f"Error: No element found with index {index}."

        selector = elem.get("selector", "")
        page = self._session.page

        try:
            page.locator(selector).first.set_checked(should_check)
            self._session.wait_for_page_ready(timeout_ms=3000)
            return self._session.get_page_summary()
        except Exception as e:
            return f"Error {'checking' if should_check else 'unchecking'} element {index}: {e}"


class ExtractTextHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "extract_text"

    @property
    def description(self) -> str:
        return "Extract text content from all elements matching a CSS selector."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "selector": {
                    "type": "string",
                    "description": "CSS selector to match elements.",
                },
            },
            "required": ["selector"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        selector = action_input.get("selector", "")
        if not selector:
            return "Error: 'selector' is required."

        self._session.ensure_browser()
        page = self._session.page

        try:
            texts = page.locator(selector).all_inner_texts()
            if not texts:
                return f"No elements found matching '{selector}'."
            result = []
            for i, text in enumerate(texts):
                text = text.strip()
                if text:
                    result.append(f"  {i}: {text}")
            if not result:
                return f"Elements found matching '{selector}' but they contain no text."
            return f"Extracted text from {len(result)} elements:\n" + "\n".join(result)
        except Exception as e:
            return f"Error extracting text with selector '{selector}': {e}"


class ScreenshotHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "screenshot"

    @property
    def description(self) -> str:
        return "Refresh the page state and return the current interactive elements."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {}}

    def execute(self, action_input: Dict[str, Any]) -> str:
        self._session.ensure_browser()
        return self._session.get_page_summary()


class WaitHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "wait"

    @property
    def description(self) -> str:
        return "Wait for a specified number of seconds before continuing."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "seconds": {
                    "type": "number",
                    "description": "Number of seconds to wait (max 30).",
                },
            },
            "required": ["seconds"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        seconds = min(float(action_input.get("seconds", 1)), 30)
        self._session.ensure_browser()
        self._session.page.wait_for_timeout(int(seconds * 1000))
        return f"Waited {seconds} seconds.\n" + self._session.get_page_summary()


class RunJavascriptHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "run_javascript"

    @property
    def description(self) -> str:
        return (
            "Execute JavaScript code on the current page and return the result. "
            "Use 'return' to get a value back (e.g. 'return document.title')."
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "script": {
                    "type": "string",
                    "description": "JavaScript code to execute. Use 'return' to get a value back.",
                },
            },
            "required": ["script"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        script = action_input.get("script", "")
        if not script:
            return "Error: 'script' is required."

        self._session.ensure_browser()
        page = self._session.page

        try:
            result = page.evaluate(f"() => {{ {script} }}")
            if result is None:
                return "JavaScript executed successfully (no return value)."
            return f"JavaScript result: {result}"
        except Exception as e:
            return f"Error executing JavaScript: {e}"


class ListDownloadsHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "list_downloads"

    @property
    def description(self) -> str:
        return (
            "List all browser downloads triggered during this session. "
            "Shows download index, filename, status, and path. "
            "Use 'move_download' to save a completed download."
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {}}

    def execute(self, action_input: Dict[str, Any]) -> str:
        downloads = self._session._downloads
        if not downloads:
            return (
                "No downloads yet. Downloads are triggered by clicking download links."
            )

        lines = [f"Downloads ({len(downloads)} total):"]
        for i, dl in enumerate(downloads):
            filename = "unknown"
            status = "pending"
            abs_path = ""
            try:
                filename = dl.suggested_filename or "unknown"
                failure = dl.failure()
                if failure:
                    status = f"failed ({failure})"
                else:
                    path = dl.path()
                    if path:
                        abs_path = os.path.abspath(path)
                        size = os.path.getsize(path)
                        status = f"completed ({size} bytes)"
            except Exception:
                pass
            line = f"  {i}: {filename} - {status}"
            if abs_path:
                line += f" - path: {abs_path}"
            lines.append(line)

        return "\n".join(lines)


class MoveDownloadHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "move_download"

    @property
    def description(self) -> str:
        persistent_dir = get_persistent_dir()
        return (
            f"Move a completed browser download to persistent storage ({persistent_dir}). "
            "Use 'list_downloads' first to see available downloads."
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "download_index": {
                    "type": "integer",
                    "description": "Index from list_downloads.",
                },
                "destination": {
                    "type": "string",
                    "description": "Destination path relative to persistent storage.",
                },
            },
            "required": ["download_index", "destination"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        dl_index = action_input.get("download_index")
        destination = action_input.get("destination", "")
        if dl_index is None:
            return "Error: 'download_index' is required."
        if not destination:
            return "Error: 'destination' is required."

        downloads = self._session._downloads
        if dl_index < 0 or dl_index >= len(downloads):
            return f"Error: Invalid download index {dl_index}. Use 'list_downloads' to see available downloads."

        dl = downloads[dl_index]
        try:
            failure = dl.failure()
            if failure:
                return f"Error: Download failed: {failure}"

            tmp_path = dl.path()
            if not tmp_path:
                return "Error: Download is still in progress. Wait and try again."

            dest_dir = get_persistent_dir()
            dest_path = (dest_dir / destination).resolve()
            if not str(dest_path).startswith(str(dest_dir.resolve())):
                return "Error: Path traversal not allowed."

            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dl.save_as(str(dest_path))
            size = dest_path.stat().st_size
            return f"Download moved to: {dest_path} ({size} bytes)"
        except Exception as e:
            return f"Error moving download: {e}"


class WaitForDownloadHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "wait_for_download"

    @property
    def description(self) -> str:
        return (
            "Wait for a file download to complete. "
            "Call this after clicking a download button."
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Expected filename (optional, for matching).",
                },
                "timeout": {
                    "type": "integer",
                    "description": "Max seconds to wait (default 60, max 120).",
                },
            },
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        filename = action_input.get("filename", "")
        wait_timeout = min(int(action_input.get("timeout", 60)), 120)
        self._session.ensure_browser()
        page = self._session.page
        if not page:
            return "Error: No browser session."

        dl_dir = self._session._download_dir
        if dl_dir and filename:
            target = os.path.join(dl_dir, filename)
            if os.path.exists(target):
                size = os.path.getsize(target)
                return f"File {filename} already downloaded ({size} bytes)."

        if dl_dir and os.path.exists(dl_dir) and os.listdir(dl_dir):
            now = time.time()
            for f in os.listdir(dl_dir):
                fp = os.path.join(dl_dir, f)
                if os.path.isfile(fp) and (now - os.path.getmtime(fp)) < 30:
                    if not filename:
                        size = os.path.getsize(fp)
                        return f"Found recently downloaded file: {f} ({size} bytes)"

        self._session.inject_blob_interceptor()

        check_interval = 2
        elapsed = 0

        while elapsed < wait_timeout:
            page.wait_for_timeout(check_interval * 1000)
            elapsed += check_interval

            blob_downloads = self._session.check_blob_downloads()
            if blob_downloads:
                d = blob_downloads[0]
                return f"File downloaded: {d.filename} ({d.size} bytes)"

            if dl_dir and os.path.exists(dl_dir):
                now = time.time()
                for f in os.listdir(dl_dir):
                    fp = os.path.join(dl_dir, f)
                    if (
                        os.path.isfile(fp)
                        and (now - os.path.getmtime(fp)) < elapsed + 5
                    ):
                        if not filename or filename.lower() in f.lower():
                            size = os.path.getsize(fp)
                            if size > 0:
                                return f"File downloaded: {f} ({size} bytes)"

        return f"No download detected within {wait_timeout} seconds. Try clicking the download button first."


class NewTabHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "new_tab"

    @property
    def description(self) -> str:
        return "Open a new browser tab, optionally navigating to a URL."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to open in the new tab (optional, opens blank if omitted).",
                },
            },
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        self._session.ensure_browser()
        new_page = self._session.create_tab()
        if not new_page:
            return "Error: Failed to create new tab."

        url = action_input.get("url", "")
        if url:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            try:
                new_page.goto(url, wait_until="domcontentloaded", timeout=30000)
                self._session.wait_for_page_ready(timeout_ms=10000)
            except Exception as e:
                return f"New tab opened but failed to navigate to {url}: {e}"

        tab_count = self._session.get_tab_count()
        if url:
            return self._session.get_page_summary()
        return f"New tab opened. Total tabs: {tab_count}, active: {self._session._active_tab_index}"


class SwitchTabHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "switch_tab"

    @property
    def description(self) -> str:
        return "Switch to a specific browser tab by index (0-based)."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "index": {"type": "integer", "description": "Tab index (0-based)."},
            },
            "required": ["index"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        index = action_input.get("index")
        if index is None:
            return "Error: 'index' is required."

        self._session.ensure_browser()
        if self._session.switch_tab(int(index)):
            return self._session.get_page_summary()
        tab_count = self._session.get_tab_count()
        return f"Error: Invalid tab index {index}. Available: 0-{tab_count - 1}"


class CloseTabHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "close_tab"

    @property
    def description(self) -> str:
        return "Close the currently active browser tab."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {}}

    def execute(self, action_input: Dict[str, Any]) -> str:
        self._session.ensure_browser()
        if self._session.close_tab():
            tab_count = self._session.get_tab_count()
            return f"Tab closed. Remaining: {tab_count}, active: {self._session._active_tab_index}"
        return "Error: Cannot close the last tab."


class MakeRequestHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "make_request"

    @property
    def description(self) -> str:
        return "Make an HTTP request (GET, POST, etc.). Useful for direct API calls."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to request."},
                "method": {
                    "type": "string",
                    "description": "HTTP method (GET, POST, PUT, DELETE).",
                },
                "headers": {
                    "type": "string",
                    "description": "JSON string of headers (optional).",
                },
                "body": {
                    "type": "string",
                    "description": "Request body for POST/PUT (optional).",
                },
            },
            "required": ["url"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        url = action_input.get("url", "")
        if not url:
            return "Error: 'url' is required."

        method = action_input.get("method", "GET").upper()
        headers_str = action_input.get("headers")
        body = action_input.get("body")

        headers = {}
        if headers_str:
            try:
                headers = json.loads(headers_str)
            except json.JSONDecodeError:
                return "Error: Invalid JSON in 'headers'."

        try:
            import requests as http_requests

            resp = http_requests.request(
                method=method,
                url=url,
                headers=headers,
                data=body,
                timeout=30,
            )
            content = resp.text
            if len(content) > 5000:
                content = (
                    content[:5000] + f"... (truncated, {len(resp.text)} chars total)"
                )
            return (
                f"HTTP {resp.status_code} {resp.reason}\n"
                f"Content-Type: {resp.headers.get('content-type', 'unknown')}\n\n"
                f"{content}"
            )
        except Exception as e:
            return f"Request failed: {e}"


class InspectNetworkLogsHandler:
    def __init__(self, session: BrowserSession) -> None:
        self._session = session

    @property
    def name(self) -> str:
        return "inspect_network_logs"

    @property
    def description(self) -> str:
        return "Filter and inspect recent network traffic from the browser."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "filter_text": {
                    "type": "string",
                    "description": "Filter by URL substring or method (e.g. 'api/v1', 'POST').",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max logs to return (default 10).",
                },
            },
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        filter_text = action_input.get("filter_text", "").lower()
        limit = action_input.get("limit", 10)

        logs = self._session.get_network_logs()
        if not logs:
            return "No network logs captured yet. Navigate to a page first."

        filtered = logs
        if filter_text:
            filtered = [
                log
                for log in logs
                if filter_text in log.get("url", "").lower()
                or filter_text in log.get("method", "").lower()
            ]

        recent = filtered[-limit:]
        if not recent:
            return f"No network logs matching '{filter_text}'."

        lines = [f"Network logs ({len(recent)} of {len(filtered)} matching):"]
        for log in recent:
            lines.append(
                f"  {log.get('method', '?')} {log.get('status', '?')} "
                f"{log.get('url', '?')[:100]} [{log.get('type', '?')}]"
            )
        return "\n".join(lines)


class SaveFactHandler:
    def __init__(self, memory_manager: Any) -> None:
        self._memory = memory_manager

    @property
    def name(self) -> str:
        return "save_fact"

    @property
    def description(self) -> str:
        return (
            "Save an important fact to long-term memory. "
            "Use for codes, URLs, credentials, or extracted data you'll need later."
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "fact": {"type": "string", "description": "The fact to remember."},
            },
            "required": ["fact"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        fact = action_input.get("fact", "")
        if not fact:
            return "Error: 'fact' is required."
        self._memory.add_fact(fact)
        return f"Fact saved: {fact}"
