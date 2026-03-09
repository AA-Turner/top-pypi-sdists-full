import asyncio
import threading
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
import unittest

import duckduckgo_mcp_server.server

from duckduckgo_mcp_server.server import (
    RateLimiter,
    DuckDuckGoSearcher,
    SearchResult,
    WebContentFetcher,
)


class DummyCtx:
    async def info(self, message):
        return None

    async def error(self, message):
        return None


class TestRateLimiter(unittest.TestCase):
    def test_acquire_removes_expired_entries(self):
        limiter = RateLimiter(requests_per_minute=1)
        limiter.requests.append(datetime.now() - timedelta(minutes=2))

        asyncio.run(limiter.acquire())

        self.assertEqual(len(limiter.requests), 1)
        self.assertLess((datetime.now() - limiter.requests[0]).total_seconds(), 1.0)


class TestDuckDuckGoSearcher(unittest.TestCase):
    def test_format_results_for_llm_populates_entries(self):
        searcher = DuckDuckGoSearcher()
        results = [
            SearchResult(
                title="First Result",
                link="https://example.com/first",
                snippet="Snippet one",
                position=1,
            ),
            SearchResult(
                title="Second Result",
                link="https://example.com/second",
                snippet="Snippet two",
                position=2,
            ),
        ]

        formatted = searcher.format_results_for_llm(results)
        print(formatted)

        self.assertIn("Found 2 search results", formatted)
        self.assertIn("1. First Result", formatted)
        self.assertIn("URL: https://example.com/first", formatted)

    def test_format_results_for_llm_handles_empty(self):
        searcher = DuckDuckGoSearcher()

        formatted = searcher.format_results_for_llm([])
        print(formatted)

        self.assertIn("No results were found", formatted)


class TestWebContentFetcher(unittest.TestCase):
    def test_fetch_and_parse_extracts_clean_text(self):
        html_content = """
        <html>
            <head>
                <title>Example</title>
                <script>console.log('ignored');</script>
                <style>body { background: #fff; }</style>
            </head>
            <body>
                <nav>Navigation</nav>
                <header>Header</header>
                <h1>Sample Heading</h1>
                <p>Some meaningful paragraph.</p>
                <footer>Footer</footer>
            </body>
        </html>
        """

        class SimpleHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(html_content.encode("utf-8"))

            def log_message(self, format, *args):
                return

        server = HTTPServer(("127.0.0.1", 0), SimpleHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            fetcher = WebContentFetcher()
            url = f"http://127.0.0.1:{server.server_address[1]}"
            text = asyncio.run(fetcher.fetch_and_parse(url, DummyCtx()))

            self.assertIn("Sample Heading", text)
            self.assertIn("Some meaningful paragraph.", text)
            self.assertNotIn("Navigation", text)
            self.assertNotIn("console.log", text)
        finally:
            server.shutdown()
            thread.join()

    def test_fetch_and_parse_pagination(self):
        html_content = "<html><body><p>" + "A" * 100 + "</p></body></html>"

        class SimpleHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(html_content.encode("utf-8"))

            def log_message(self, format, *args):
                return

        server = HTTPServer(("127.0.0.1", 0), SimpleHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            fetcher = WebContentFetcher()
            url = f"http://127.0.0.1:{server.server_address[1]}"

            # Fetch first 50 chars
            text = asyncio.run(fetcher.fetch_and_parse(url, DummyCtx(), start_index=0, max_length=50))
            self.assertIn("start_index=50 to see more", text)
            self.assertIn("of 100 total", text)

            # Fetch from offset 50
            text = asyncio.run(fetcher.fetch_and_parse(url, DummyCtx(), start_index=50, max_length=50))
            self.assertNotIn("to see more", text)
            self.assertIn("of 100 total", text)
        finally:
            server.shutdown()
            thread.join()
