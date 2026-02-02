import requests
import re
from .base_tool import BaseTool
from html import unescape
from .tool_registry import register_tool
import io
import os
import sys
import subprocess
import pdfplumber
from playwright.sync_api import sync_playwright


@register_tool("URLHTMLTagTool")
class URLHTMLTagTool(BaseTool):
    """
    Fetches a webpage and extracts the content of a specified HTML tag.
    Expects: {"url": "https://..."}
    The tag to extract is specified in the tool's configuration.
    The tag to extract is specified in the tool's configuration.
    Optional: {"timeout": <seconds>} (default 20)
    Returns: {"content": "<extracted content>"} or {"error": "..."}
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.tag_to_fetch = tool_config["fields"].get("tag", "title")
        self.return_key = tool_config["fields"].get("return_key", "content")

    def run(self, arguments: dict):
        url = arguments.get("url")
        if not url:
            return {"error": "Parameter 'url' is required."}

        # Basic validation
        if not (url.startswith("http://") or url.startswith("https://")):
            return {"error": "URL must start with http:// or https://"}

        timeout = arguments.get("timeout", 20)
        try:
            resp = requests.get(url, timeout=timeout)
        except requests.Timeout:
            return {"error": "Request timed out."}
        except Exception as e:
            return {"error": f"Request failed: {e}"}

        if resp.status_code != 200:
            return {"error": f"HTTP {resp.status_code}", "detail": resp.text[:300]}

        ctype = resp.headers.get("Content-Type", "").lower()
        if "html" not in ctype:
            # Still attempt extraction if text-like
            if not ctype.startswith("text/"):
                return {"error": "Response is not HTML."}

        text = resp.text

        # Extract <tag>...</tag>
        m = re.search(
            rf"<{self.tag_to_fetch}>(.*?)</{self.tag_to_fetch}>",
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if not m:
            return {"error": f"No <{self.tag_to_fetch}> tag found."}

        raw_content = m.group(1).strip()
        # Collapse whitespace
        cleaned = re.sub(r"\s+", " ", raw_content)
        cleaned = unescape(cleaned)

        return {self.return_key: cleaned}


@register_tool("URLToPDFTextTool")
class URLToPDFTextTool(BaseTool):
    """
    Loads a webpage (with JavaScript), exports it as a PDF, and extracts text.
    Expects: {"url": "https://..."}
    Optional: {"timeout": <seconds>} (default 30)
    Returns: {"text": "<extracted text>"} or {"error": "..."}
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.return_key = tool_config["fields"].get("return_key", "text")

    def _ensure_playwright_browsers(
        self,
        browsers=("chromium",),
        with_deps: bool = False,
        timeout_seconds: int = 600,
    ):
        """
        Ensure Playwright browser binaries are installed.

        Returns
            None on success, or an error string on failure.
        """
        # Allow user to skip auto-install via env var
        if os.environ.get("PLAYWRIGHT_SKIP_BROWSER_INSTALL", "") in (
            "1",
            "true",
            "True",
        ):
            return "PLAYWRIGHT_SKIP_BROWSER_INSTALL is set; skipping browser install."

        # Detect if running inside an active asyncio event loop (Colab/Jupyter)
        try:
            import asyncio

            loop = asyncio.get_event_loop()
            running_async = loop.is_running()
        except Exception:
            running_async = False

        def try_launch_one_sync():
            try:
                from playwright.sync_api import sync_playwright

                with sync_playwright() as p:
                    b = getattr(p, browsers[0])
                    browser = b.launch(headless=True, timeout=10_000)
                    browser.close()
                return True, None
            except Exception as e:
                return False, str(e)

        async def try_launch_one_async():
            try:
                from playwright.async_api import async_playwright

                async with async_playwright() as p:
                    b = getattr(p, browsers[0])
                    browser = await b.launch(headless=True, timeout=10_000)
                    await browser.close()
                return True, None
            except Exception as e:
                return False, str(e)

        if running_async:
            # Use async Playwright API for browser launch check
            try:
                ok, msg = loop.run_until_complete(try_launch_one_async())
            except Exception as e:
                ok, msg = False, str(e)
        else:
            ok, msg = try_launch_one_sync()

        if ok:
            return None  # browsers are already installed

        # Attempt install using the same Python executable
        cmd = [sys.executable, "-m", "playwright", "install"] + list(browsers)
        if with_deps:
            cmd.append("--with-deps")

        try:
            subprocess.run(
                cmd, check=True, capture_output=True, text=True, timeout=timeout_seconds
            )
        except subprocess.CalledProcessError as e:
            stdout = e.stdout or ""
            stderr = e.stderr or ""
            return f"playwright install failed (exit {e.returncode}). stdout:\n{stdout}\nstderr:\n{stderr}"
        except Exception as e:
            return f"Failed to run playwright install: {e}"

        # Try launching again after install
        if running_async:
            try:
                ok2, msg2 = loop.run_until_complete(try_launch_one_async())
            except Exception as e:
                ok2, msg2 = False, str(e)
        else:
            ok2, msg2 = try_launch_one_sync()

        if ok2:
            return None
        return f"Browsers installed but launch still fails: {msg2}"

    def run(self, arguments: dict):
        url = arguments.get("url")
        if not url:
            return {"error": "Parameter 'url' is required."}
        if not (url.startswith("http://") or url.startswith("https://")):
            return {"error": "URL must start with http:// or https://"}

        timeout = arguments.get("timeout", 30)

        # First, check if the URL returns HTML or a downloadable file
        try:
            resp = requests.head(url, timeout=timeout, allow_redirects=True)
            content_type = resp.headers.get("Content-Type", "").lower()
            # If it's not HTML, handle it as a simple text download
            is_html = "text/html" in content_type or "application/xhtml" in content_type
            if not is_html:
                # Download the file directly and return its text content
                resp = requests.get(url, timeout=timeout, allow_redirects=True)
                if resp.status_code != 200:
                    return {"error": f"HTTP {resp.status_code}"}
                text = resp.text
                if not text.strip():
                    return {"error": "File appears to be empty or binary."}
                return {self.return_key: text.strip()}
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to check content type: {e}"}

        # Ensure browsers are installed (auto-install if needed)
        ensure_error = self._ensure_playwright_browsers(
            browsers=("chromium",), with_deps=False
        )
        if ensure_error is not None:
            return {"error": f"Playwright browser check/install failed: {ensure_error}"}

        # Detect if running inside an active asyncio event loop (Colab/Jupyter)
        try:
            import asyncio

            loop = asyncio.get_event_loop()
            running_async = loop.is_running()
        except Exception:
            running_async = False

        if running_async:
            # Use async Playwright API
            from playwright.async_api import async_playwright
            import nest_asyncio

            nest_asyncio.apply()

            async def async_pdf():
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    page = await browser.new_page()
                    await page.goto(
                        url, timeout=timeout * 1000, wait_until="networkidle"
                    )
                    pdf_bytes = await page.pdf(format="A4", print_background=True)
                    await browser.close()
                    return pdf_bytes

            try:
                pdf_bytes = loop.run_until_complete(async_pdf())
            except Exception as e:
                return {"error": f"Failed to render webpage to PDF (async): {e}"}
        else:
            # Use sync Playwright API
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    page.goto(url, timeout=timeout * 1000, wait_until="networkidle")
                    pdf_bytes = page.pdf(format="A4", print_background=True)
                    browser.close()
            except Exception as e:
                return {"error": f"Failed to render webpage to PDF (sync): {e}"}

        # Step 2: Extract text from PDF
        try:
            text = ""
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if not text.strip():
                return {"error": "No text could be extracted from rendered PDF."}
            return {self.return_key: text.strip()}
        except Exception as e:
            return {"error": f"Failed to extract text from PDF: {e}"}
