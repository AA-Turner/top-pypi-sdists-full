"""Process entrypoint for one deployed persistent browser worker."""

from __future__ import annotations

import os
from pathlib import Path

from matrx_scraper.cloud_browser.streaming.supervisor import SelkiesSupervisor
from matrx_scraper.cloud_browser.worker.auth import Es256WorkerTokenVerifier
from matrx_scraper.cloud_browser.worker.http_app import create_worker_app
from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker


def _required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


def build_app():
    worker_id = _required("BROWSER_WORKER_ID")
    public_key_pem = (
        os.environ.get("BROWSER_WORKER_PUBLIC_KEY_PEM", "").replace("\\n", "\n").strip()
    )
    if public_key_pem:
        public_key = public_key_pem
    else:
        public_key = Path(_required("BROWSER_WORKER_PUBLIC_KEY_FILE")).read_text()
    verifier = Es256WorkerTokenVerifier(
        issuer=_required("BROWSER_WORKER_TOKEN_ISSUER"),
        public_key_pem=public_key,
    )
    worker = BrowserWorker(
        worker_id=worker_id,
        token_verifier=verifier,
        xvfb_display=os.environ.get("DISPLAY", ":99"),
    )
    return create_worker_app(worker, stream=SelkiesSupervisor())


app = build_app()
