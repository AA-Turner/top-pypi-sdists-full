"""Process entrypoint for one deployed persistent browser worker."""

from __future__ import annotations

import os
from pathlib import Path

from matrx_scraper.cloud_browser.streaming.supervisor import SelkiesSupervisor
from matrx_scraper.cloud_browser.worker.auth import Es256WorkerTokenVerifier
from matrx_scraper.cloud_browser.worker.cloud_computer_launch import CloudComputerLaunch
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
    # A lease nobody renews makes the worker ASK the server; only a definite
    # "this run has ended" stops it (lease_watchdog.py). A Cloud Computer (the
    # image sets BROWSER_WORKER_DESKTOP_SESSION) then stops only the browser run
    # and keeps the person's machine; a fleet worker ends its process.
    worker.enable_lease_watchdog(
        keep_process_on_ended_run=bool(os.environ.get("BROWSER_WORKER_DESKTOP_SESSION"))
    )
    # Read at the process boundary: the Cloud Computer image sets it to "1".
    clipboard = os.environ.get("BROWSER_WORKER_STREAM_CLIPBOARD", "0") == "1"
    # The Cloud Computer image turns this on: its stream runs from boot.
    keep_warm = os.environ.get("BROWSER_WORKER_STREAM_KEEP_WARM", "0") == "1"
    # The Cloud Computer image sets MATRX_CLOUD_COMPUTER=1; its launch carries the
    # machine files token + bridge URL. Read here, once, and passed down.
    cloud_computer = None
    if os.environ.get("MATRX_CLOUD_COMPUTER") == "1":
        cloud_computer = CloudComputerLaunch(
            files_token=os.environ.get("MATRX_CLOUD_FILES_TOKEN", ""),
            files_url=os.environ.get("MATRX_CLOUD_FILES_URL", ""),
            process_env=dict(os.environ),
        )
    return create_worker_app(
        worker,
        stream=SelkiesSupervisor(enable_clipboard=clipboard, keep_warm=keep_warm),
        cloud_computer=cloud_computer,
    )


app = build_app()
