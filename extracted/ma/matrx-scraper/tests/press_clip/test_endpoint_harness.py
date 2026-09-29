"""Real scraper-owned press-clip endpoint proof, using only a local fixture server."""
from __future__ import annotations

import base64
import contextlib
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pymupdf
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from matrx_scraper.ai_browser import url_guard
from matrx_scraper.api.press_clip_router import router

FIXTURES = Path(__file__).with_name("fixtures")


@contextlib.contextmanager
def _fixture_server():
    handler = partial(SimpleHTTPRequestHandler, directory=str(FIXTURES))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/news_article.html"
    finally:
        server.shutdown()
        thread.join()


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_endpoint_runs_real_chromium_and_returns_printed_artifacts(monkeypatch: pytest.MonkeyPatch):
    """The fixed route emits a real PDF, preview and every PDF-page raster."""
    async def allow_fixture(url: str) -> str:
        return url
    monkeypatch.setattr(url_guard, "validate_public_http_url", allow_fixture)
    with _fixture_server() as url:
        response = _client().post(
            "/press-clips/render",
            json={"url": url, "client_name": "Birchwood Avenue Renovation"},
        )
    assert response.status_code == 200, response.text
    body = response.json()
    pdf = base64.b64decode(body["pdf_base64"])
    preview = base64.b64decode(body["preview_png_base64"])
    rasters = [base64.b64decode(item) for item in body["page_rasters_base64"]]
    assert pdf.startswith(b"%PDF-") and preview.startswith(b"\x89PNG")
    assert rasters and all(page.startswith(b"\x89PNG") for page in rasters)
    doc = pymupdf.open(stream=pdf, filetype="pdf")
    try:
        assert doc.page_count == len(rasters)
        printed_text = " ".join(" ".join(page.get_text().split()) for page in doc)
        assert "Birchwood Avenue Renovation completes its kitchen" in printed_text
    finally:
        doc.close()
    assert body["report"]["root_selector_used"] == "article#story.story"
    assert body["meta"]["headline"] == "Birchwood Avenue Renovation completes its kitchen"


def test_endpoint_rejects_non_public_target_before_browser(monkeypatch: pytest.MonkeyPatch):
    async def deny(_url: str) -> str:
        raise ValueError("private resolver detail must not escape")
    monkeypatch.setattr(url_guard, "validate_public_http_url", deny)
    response = _client().post("/press-clips/render", json={"url": "http://169.254.169.254/latest"})
    assert response.status_code == 422
    assert "publicly routable" in response.text
    assert "resolver detail" not in response.text
