"""Plain fetches impersonate the NEWEST Chrome the installed curl_cffi supports and let
the library build the wire headers (62-URL benchmark, 2026-10-16: 26 -> 31 of 62)."""

from __future__ import annotations

import asyncio
import re
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from fixture_origins import allow_fixture_origins
import pytest

from matrx_scraper import scraper
from matrx_scraper.parser import knobs
from matrx_scraper.scraper import RequestType, fetch

curl_requests = pytest.importorskip("curl_cffi.requests")


def _installed_chrome_majors() -> list[int]:
    return [
        int(m.group(1))
        for b in curl_requests.BrowserType
        if (m := re.match(r"^chrome(\d+)$", b.value))
    ]


def test_newest_target_is_detected_from_the_installed_library() -> None:
    assert scraper.newest_chrome_target() == f"chrome{max(_installed_chrome_majors())}"


def test_default_profile_uses_the_newest_target_not_a_pinned_one() -> None:
    profile = scraper.get_random_header_profile()
    assert profile["impersonate"] == scraper.newest_chrome_target()
    assert profile["library_headers"] is True
    assert profile["impersonate"] not in {"chrome131", "chrome120", "chrome110"} or (
        scraper.newest_chrome_target() == profile["impersonate"]
    )


def test_knob_override_wins_and_auto_means_detect() -> None:
    try:
        knobs.configure_parser_knobs(lambda key: "chrome124" if key == "impersonate_target" else None)
        assert scraper.impersonation_target() == "chrome124"
        assert scraper.get_random_header_profile()["impersonate"] == "chrome124"
        knobs.configure_parser_knobs(lambda key: "auto")
        assert scraper.impersonation_target() == scraper.newest_chrome_target()
    finally:
        knobs.configure_parser_knobs(None)


def test_library_profile_sends_only_caller_additions() -> None:
    profile = scraper.get_random_header_profile()
    headers = dict(profile["headers"], Referer="https://example.com/")
    assert scraper._curl_wire_headers(profile, headers, None) == {"Referer": "https://example.com/"}
    wire = scraper._curl_wire_headers(profile, headers, "Custom/1.0")
    assert wire["User-Agent"] == headers["User-Agent"] and "Sec-Ch-Ua" not in wire


def test_hand_written_profile_still_sends_everything() -> None:
    profile = scraper.HEADER_PROFILES[0]
    assert scraper._curl_wire_headers(profile, profile["headers"], None) is profile["headers"]


def test_wire_carries_the_newest_chrome_built_by_the_library(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, str] = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            captured.update({k.lower(): v for k, v in self.headers.items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body>ok</body></html>")

        def log_message(self, *args: object) -> None:
            return

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    allow_fixture_origins(monkeypatch, f"http://{host}:{port}")
    try:
        response = asyncio.run(
            fetch(f"http://{host}:{port}/", request_type=RequestType.NORMAL, use_curl_cffi=True)
        )
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    assert response.status_code == 200
    major = max(_installed_chrome_majors())
    assert f"Chrome/{major}" in captured["user-agent"]
    assert f'v="{major}"' in captured.get("sec-ch-ua", "")
