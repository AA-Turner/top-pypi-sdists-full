"""Process entrypoint for one deployed persistent browser worker."""

from __future__ import annotations

import os
from pathlib import Path

from matrx_scraper.cloud_browser.streaming.supervisor import SelkiesSupervisor
from matrx_scraper.cloud_browser.worker.auth import Es256WorkerTokenVerifier
from matrx_scraper.cloud_browser.worker.cloud_computer_launch import launch_from_environment
from matrx_scraper.cloud_browser.worker.http_app import create_worker_app
from matrx_scraper.cloud_browser.worker.machine_browsers import (
    DEFAULT_MAX_BROWSERS,
    MachineBrowsers,
)
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
    desktop = bool(os.environ.get("BROWSER_WORKER_DESKTOP_SESSION"))

    def new_worker() -> BrowserWorker:
        worker = BrowserWorker(
            worker_id=worker_id,
            token_verifier=verifier,
            xvfb_display=os.environ.get("DISPLAY", ":99"),
        )
        # A lease nobody renews makes the worker ASK the server; only a definite
        # "this run has ended" stops it (lease_watchdog.py). A Cloud Computer (the
        # image sets BROWSER_WORKER_DESKTOP_SESSION) then stops only the browser run
        # and keeps the person's machine; a fleet worker ends its process.
        worker.enable_lease_watchdog(keep_process_on_ended_run=desktop)
        return worker

    worker = new_worker()
    # WHAT THIS COPY IS, read once at the process boundary: the Cloud Computer image
    # sets MATRX_CLOUD_COMPUTER=1 (image identity, never a per-machine switch). Its
    # stream shares the clipboard and runs from boot; a fleet worker does neither.
    is_cloud_computer = os.environ.get("MATRX_CLOUD_COMPUTER") == "1"
    clipboard = is_cloud_computer
    keep_warm = is_cloud_computer
    # Its launch carries the machine files token + bridge URL. Read here, once, and passed down.
    cloud_computer = None
    # The token is taken once and kept only in this process's memory, which is then
    # closed to the agent's processes (same uid): cloud_computer_launch, review 3 D2.
    host = worker
    if is_cloud_computer:
        cloud_computer = launch_from_environment(os.environ)
        # A Cloud Computer runs several named browsers, one per run
        # (machine_browsers.py); a fleet worker keeps one run per process.
        host = MachineBrowsers(
            worker,
            factory=new_worker,
            max_browsers=DEFAULT_MAX_BROWSERS,
        )
    return create_worker_app(
        host,  # type: ignore[arg-type]
        stream=SelkiesSupervisor(enable_clipboard=clipboard, keep_warm=keep_warm),
        cloud_computer=cloud_computer,
    )


app = build_app()
