import os
import re
import requests
import tempfile
import time
import xml.etree.ElementTree as ET
from .base_tool import BaseTool
from .tool_registry import register_tool
from .http_utils import request_with_retry

try:
    from markitdown import MarkItDown

    MARKITDOWN_AVAILABLE = True
except ImportError:
    MARKITDOWN_AVAILABLE = False


@register_tool("ArXivTool")
class ArXivTool(BaseTool):
    """
    Search arXiv for papers by keyword using the public arXiv API.
    """

    def __init__(
        self,
        tool_config,
        base_url="http://export.arxiv.org/api/query",
    ):
        super().__init__(tool_config)
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "ToolUniverse/1.0 (arxiv client; contact: support@tooluniverse.ai)"
            }
        )
        self._last_request_time = 0.0

    def run(self, arguments):
        query = arguments.get("query")
        limit = int(arguments.get("limit", 10))
        # sort_by: relevance | lastUpdatedDate | submittedDate
        sort_by = arguments.get("sort_by", "relevance")
        # sort_order: ascending | descending
        sort_order = arguments.get("sort_order", "descending")

        if not query:
            return {"error": "`query` parameter is required."}

        return self._search(query, limit, sort_by, sort_order)

    def _search(self, query, limit, sort_by, sort_order):
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max(1, min(limit, 200)),
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }

        try:
            self._respect_rate_limit()
            response = request_with_retry(
                self.session,
                "GET",
                self.base_url,
                params=params,
                timeout=20,
                max_attempts=5,
                backoff_seconds=1.0,
            )
        except requests.RequestException as e:
            return {
                "error": "Network error calling arXiv API",
                "reason": str(e),
            }

        if response.status_code != 200:
            return {
                "error": f"arXiv API error {response.status_code}",
                "reason": response.reason,
            }

        # Parse Atom XML
        try:
            root = ET.fromstring(response.text)
        except ET.ParseError as e:
            return {
                "error": "Failed to parse arXiv response",
                "reason": str(e),
            }

        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = []
        for entry in root.findall("atom:entry", ns):
            title_text = entry.findtext(
                "atom:title",
                default="",
                namespaces=ns,
            )
            title = (title_text or "").strip()
            summary_text = entry.findtext(
                "atom:summary",
                default="",
                namespaces=ns,
            )
            summary = (summary_text or "").strip()
            link_el = entry.find("atom:link[@type='text/html']", ns)
            if link_el is not None:
                link = link_el.get("href")
            else:
                link = entry.findtext("atom:id", default="", namespaces=ns)
            published = entry.findtext("atom:published", default="", namespaces=ns)
            updated = entry.findtext("atom:updated", default="", namespaces=ns)
            authors = [
                a.findtext("atom:name", default="", namespaces=ns)
                for a in entry.findall("atom:author", ns)
            ]
            primary_category = ""
            cat_el = entry.find("{http://arxiv.org/schemas/atom}primary_category")
            if cat_el is not None:
                primary_category = cat_el.get("term", "")

            entries.append(
                {
                    "title": title,
                    "abstract": summary,
                    "authors": authors,
                    "published": published,
                    "updated": updated,
                    "category": primary_category,
                    "url": link,
                }
            )

        return entries

    def _respect_rate_limit(self):
        """arXiv asks clients to avoid rapid-fire requests; keep a 3s gap."""
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < 3.0:
            time.sleep(3.0 - elapsed)
        self._last_request_time = time.time()


@register_tool("ArXivPDFSnippetsTool")
class ArXivPDFSnippetsTool(BaseTool):
    """
    Fetch an arXiv paper's PDF and return bounded text snippets around user-provided terms.
    Uses markitdown to convert PDF to markdown text.
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "ToolUniverse/1.0 (arxiv pdf client; contact: support@tooluniverse.ai)"
            }
        )
        if MARKITDOWN_AVAILABLE:
            self.md_converter = MarkItDown()
        else:
            self.md_converter = None

    def run(self, arguments):
        arxiv_id = arguments.get("arxiv_id")
        pdf_url = arguments.get("pdf_url")
        terms = arguments.get("terms")

        # Validate terms
        if not isinstance(terms, list) or not [
            t for t in terms if isinstance(t, str) and t.strip()
        ]:
            return {
                "status": "error",
                "error": "`terms` must be a non-empty list of strings.",
                "retryable": False,
            }

        # Determine PDF URL
        if isinstance(pdf_url, str) and pdf_url.strip():
            final_pdf_url = pdf_url.strip()
        elif isinstance(arxiv_id, str) and arxiv_id.strip():
            # Build PDF URL from arXiv ID
            arxiv_id = arxiv_id.strip()
            # Remove any version suffix (e.g., v1, v2) and arXiv: prefix
            clean_id = arxiv_id.replace("arXiv:", "").split("v")[0]
            final_pdf_url = f"https://arxiv.org/pdf/{clean_id}.pdf"
        else:
            return {
                "status": "error",
                "error": "Provide either `arxiv_id` (e.g., '2301.12345') or `pdf_url`.",
                "retryable": False,
            }

        # Check if markitdown is available
        if not MARKITDOWN_AVAILABLE:
            return {
                "status": "error",
                "error": "markitdown library not available. Install with: pip install 'markitdown[all]'",
                "retryable": False,
            }

        # Parse optional parameters
        try:
            window_chars = int(arguments.get("window_chars", 220))
        except (TypeError, ValueError):
            window_chars = 220
        window_chars = max(20, min(window_chars, 2000))

        try:
            max_snippets_per_term = int(arguments.get("max_snippets_per_term", 3))
        except (TypeError, ValueError):
            max_snippets_per_term = 3
        max_snippets_per_term = max(1, min(max_snippets_per_term, 10))

        try:
            max_total_chars = int(arguments.get("max_total_chars", 8000))
        except (TypeError, ValueError):
            max_total_chars = 8000
        max_total_chars = max(1000, min(max_total_chars, 50000))

        # Download PDF to temp file
        try:
            resp = request_with_retry(
                self.session, "GET", final_pdf_url, timeout=60, max_attempts=3
            )
            if resp.status_code != 200:
                return {
                    "status": "error",
                    "error": f"PDF download failed (HTTP {resp.status_code})",
                    "url": final_pdf_url,
                    "status_code": resp.status_code,
                    "retryable": resp.status_code in (408, 429, 500, 502, 503, 504),
                }

            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(resp.content)
                tmp_path = tmp.name

            # Convert PDF to markdown using markitdown
            try:
                result = self.md_converter.convert(tmp_path)
                text = (
                    result.text_content
                    if hasattr(result, "text_content")
                    else str(result)
                )
            except Exception as e:
                # Clean up temp file
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
                return {
                    "status": "error",
                    "error": f"PDF to markdown conversion failed: {str(e)}",
                    "url": final_pdf_url,
                    "retryable": False,
                }

            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except Exception:
                pass

        except Exception as e:
            return {
                "status": "error",
                "error": f"PDF download/processing failed: {str(e)}",
                "url": final_pdf_url,
                "retryable": True,
            }

        # Extract snippets around terms
        snippets = []
        total_chars = 0
        low = text.lower()

        for raw_term in terms:
            if not isinstance(raw_term, str):
                continue
            term = raw_term.strip()
            if not term:
                continue

            needle = term.lower()
            found = 0
            for m in re.finditer(re.escape(needle), low):
                if found >= max_snippets_per_term:
                    break
                start = max(0, m.start() - window_chars)
                end = min(len(text), m.end() + window_chars)
                snippet = text[start:end].strip()
                # Bound total output size
                if total_chars + len(snippet) > max_total_chars:
                    break
                snippets.append({"term": term, "snippet": snippet})
                total_chars += len(snippet)
                found += 1

        return {
            "status": "success",
            "pdf_url": final_pdf_url,
            "snippets": snippets,
            "snippets_count": len(snippets),
            "truncated": total_chars >= max_total_chars,
        }
