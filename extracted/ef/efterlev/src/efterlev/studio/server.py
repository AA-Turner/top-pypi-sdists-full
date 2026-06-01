"""Localhost server for the browser Studio.

`efterlev studio` builds the workspace's render payload, injects it into the
bundled single-page app, serves it on 127.0.0.1, and opens the browser. The
scan/agents still run on your machine — this is local-first, no SaaS, no
phone-home. The page is self-contained (data injected inline), so it works
offline with no external requests.

`efterlev studio --live` adds a live mode: it spawns the real pipeline
(`report run`, scan + gap only) as a subprocess that records its typed event
stream to a temp JSONL file (see `efterlev.events.recorder`); this server
tails that file and streams the events to the browser over SSE (`/events`),
which animates the flow from the *real* run instead of a sample. Still
local-first — the subprocess and this server both run on your machine.
"""

from __future__ import annotations

import importlib.resources
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

_PLACEHOLDER = "/*STUDIO_DATA*/{}"


def _template() -> str:
    return (
        importlib.resources.files("efterlev.studio")
        .joinpath("web", "index.html")
        .read_text(encoding="utf-8")
    )


def build_served_html(
    root: Path | None = None, *, stream: bool = False, sample: bool = False
) -> str:
    """The full single-page app with this workspace's data injected inline.

    `stream=True` flags the page to drive its animation from live SSE events
    (`/events`). `sample=True` serves the precomputed govnotes sample posture
    (instant, keyless) instead of reading `root`.
    """
    from efterlev.studio.web_data import build_studio_data, load_sample_studio_data

    data = load_sample_studio_data() if sample else build_studio_data(root)
    data["stream"] = stream
    return _template().replace(_PLACEHOLDER, json.dumps(data))


def materialize_sample() -> Path:
    """Copy the bundled govnotes sample to a fresh temp workspace, initialized.

    Returns the temp root (infra/ + .github/workflows/ + an initialized
    `.efterlev/`) so `--live --sample` can run the real pipeline against it
    without touching the installed package or prompting the init wizard. The
    workspace is initialized with the best available backend so verdicts can
    actually stream: a local `claude` subscription (keyless) if present, else
    the Anthropic API if a key is set, else the default.
    """
    import os
    import shutil
    import tempfile

    from efterlev.config import LLMConfig
    from efterlev.llm.claude_code_client import claude_cli_available
    from efterlev.studio.web_data import sample_dir
    from efterlev.workspace import init_workspace

    if claude_cli_available():
        # claude_code agents pin Sonnet 4.6 (v0.1.175) — keyless + fast.
        llm_config: LLMConfig | None = LLMConfig(backend="claude_code", model="claude-sonnet-4-6")
    elif os.environ.get("ANTHROPIC_API_KEY"):
        llm_config = LLMConfig(backend="anthropic")
    else:
        llm_config = None  # default; gap can't classify without a backend, scan flow still streams

    src = sample_dir()
    dst = Path(tempfile.mkdtemp(prefix="efterlev-govnotes-"))
    shutil.copytree(src / "infra", dst / "infra")
    gw = src / "github_workflows"
    if gw.is_dir():
        shutil.copytree(gw, dst / ".github" / "workflows")
    init_workspace(dst, "fedramp-20x-moderate", llm_config=llm_config)
    return dst


def _write_page(handler: BaseHTTPRequestHandler, body: bytes) -> None:
    handler.send_response(200)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


_REPORT_SPECS = [
    ("Gap report", "reports/gap-*.html"),
    ("POA&M", "reports/poam/poam-*.md"),
    ("OSCAL POA&M", "reports/oscal/*poam*.json"),
    ("OSCAL Component Definition", "reports/oscal/*component*.json"),
    ("3PAO inspector", "reports/inspector*.html"),
    ("Resource inventory", "reports/inventory/inventory-*.html"),
    ("VDR", "reports/vdr/vdr-*.md"),
    ("Submission package", "submissions/submission-*.zip"),
    ("Scan (JSON)", "reports/scan-*.json"),
]
_CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".json": "application/json",
    ".md": "text/markdown; charset=utf-8",
    ".zip": "application/zip",
}


def _out_dir(root: Path | None) -> Path | None:
    if root is None:
        return None
    from efterlev.paths import reports_dir

    out = reports_dir(root).parent  # `<root>/efterlev-out/`
    return out if out.is_dir() else None


def discover_reports(root: Path | None) -> list[dict[str, str]]:
    """The latest of each generated artifact under `<root>/efterlev-out/`."""
    out = _out_dir(root)
    if out is None:
        return []
    items: list[dict[str, str]] = []
    for label, pat in _REPORT_SPECS:
        files = [p for p in out.glob(pat) if p.is_file()]
        if not files:
            continue
        f = max(files, key=lambda p: p.stat().st_mtime)
        items.append({"label": label, "rel": str(f.relative_to(out)), "name": f.name})
    return items


def _handle_reports(handler: BaseHTTPRequestHandler, root: Path | None, path: str) -> bool:
    """Serve /reports (JSON index) and /report?f=<rel> (a file). Returns handled."""
    from urllib.parse import parse_qs, urlparse

    if path.rstrip("/") == "/reports":
        body = json.dumps({"reports": discover_reports(root)}).encode("utf-8")
        handler.send_response(200)
        handler.send_header("Content-Type", "application/json")
        handler.send_header("Content-Length", str(len(body)))
        handler.end_headers()
        handler.wfile.write(body)
        return True
    if urlparse(path).path == "/report":
        rel = (parse_qs(urlparse(path).query).get("f") or [""])[0]
        out = _out_dir(root)
        # Allowlist, not path-sanitization: the requested `rel` is only used to
        # look up a path object that `discover_reports` already built from a
        # trusted glob under efterlev-out/. The user string never becomes a
        # path segment, so traversal (`../`, absolute paths) can't escape — it
        # simply won't match a key. (Also clears CodeQL py/path-injection.)
        allowed = {r["rel"]: (out / r["rel"]) for r in discover_reports(root)} if out else {}
        target = allowed.get(rel)
        if target is None or not target.is_file():
            handler.send_response(404)
            handler.end_headers()
            return True
        data = target.read_bytes()
        handler.send_response(200)
        handler.send_header("Content-Type", _CONTENT_TYPES.get(target.suffix.lower(), "text/plain"))
        handler.send_header("Content-Length", str(len(data)))
        handler.end_headers()
        handler.wfile.write(data)
        return True
    return False


def _handle_worklist(handler: BaseHTTPRequestHandler, root: Path | None, path: str) -> bool:
    """Serve /worklist (JSON of the next-step worklist for the workspace at `root`).

    Mirrors the reports endpoint: pure read of current state, no LLM/network/writes.
    With no workspace (sample mode), returns an empty `items` list so the page
    can hide the card cleanly.
    """
    if path.rstrip("/") != "/worklist":
        return False
    if root is None:
        body = json.dumps({"stage": None, "headline": None, "items": []}).encode("utf-8")
    else:
        from dataclasses import asdict

        from efterlev.worklist import build_worklist

        wl = build_worklist(root)
        body = json.dumps(
            {
                "stage": wl.stage,
                "headline": wl.headline,
                "overall_pct": wl.overall_pct,
                "items": [asdict(i) for i in wl.items],
            }
        ).encode("utf-8")
    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)
    return True


def _make_handler(html: str, root: Path | None = None) -> type[BaseHTTPRequestHandler]:
    body = html.encode("utf-8")

    class _Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path in ("/", "/index.html"):
                _write_page(self, body)
            elif _handle_reports(self, root, self.path) or _handle_worklist(self, root, self.path):
                pass
            else:
                self.send_response(204)
                self.end_headers()

        def log_message(self, *_args: object) -> None:  # silence access log
            pass

    return _Handler


def _make_live_handler(
    html: str,
    buffer: list[str],
    cond: threading.Condition,
    done: threading.Event,
    root: Path | None = None,
) -> type[BaseHTTPRequestHandler]:
    """Handler that serves the page and streams `buffer` over SSE at /events.

    `buffer` is the growing list of JSON event lines; `cond` notifies when it
    grows or `done` is set. Each connection replays from the start (so a page
    reload re-runs the animation) then follows new events until `done`.
    """
    body = html.encode("utf-8")

    class _Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path in ("/", "/index.html"):
                _write_page(self, body)
            elif self.path.startswith("/events"):
                self._stream()
            elif _handle_reports(self, root, self.path) or _handle_worklist(self, root, self.path):
                pass
            else:
                self.send_response(204)
                self.end_headers()

        def _stream(self) -> None:
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            idx = 0
            try:
                while True:
                    with cond:
                        while idx >= len(buffer) and not done.is_set():
                            cond.wait(timeout=15)
                            if idx >= len(buffer) and not done.is_set():
                                # heartbeat — also surfaces a dropped client
                                self.wfile.write(b": ping\n\n")
                                self.wfile.flush()
                        chunk = buffer[idx:]
                        idx = len(buffer)
                        finished = done.is_set() and idx >= len(buffer)
                    for line in chunk:
                        self.wfile.write(b"data: " + line.encode("utf-8") + b"\n\n")
                        self.wfile.flush()
                    if finished:
                        self.wfile.write(b"event: done\ndata: {}\n\n")
                        self.wfile.flush()
                        return
            except (BrokenPipeError, ConnectionResetError, ValueError):
                return  # client went away

        def log_message(self, *_args: object) -> None:
            pass

    return _Handler


def _serve(
    server: ThreadingHTTPServer,
    url: str,
    *,
    open_browser: bool,
    serve: bool,
) -> tuple[str, ThreadingHTTPServer]:
    import webbrowser

    if not serve:
        threading.Thread(target=server.serve_forever, daemon=True).start()
        return url, server
    print(f"Efterlev Studio → {url}")
    print("  (local-first; press Ctrl-C to stop)")
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStudio stopped.")
    finally:
        server.shutdown()
    return url, server


def run_studio_web(
    root: Path | None = None,
    *,
    open_browser: bool = True,
    port: int = 0,
    serve: bool = True,
    sample: bool = False,
) -> tuple[str, ThreadingHTTPServer]:
    """Serve the Studio app on localhost. Returns (url, server).

    With `serve=True` (default) this blocks on the server until interrupted.
    `serve=False` starts the server in the background and returns immediately
    (used by tests). `port=0` picks a free port. `sample=True` serves the
    precomputed govnotes sample posture (instant, keyless).
    """
    html = build_served_html(root, sample=sample)
    server = ThreadingHTTPServer(("127.0.0.1", port), _make_handler(html, root))
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    return _serve(server, url, open_browser=open_browser, serve=serve)


def run_studio_live(
    root: Path,
    *,
    open_browser: bool = True,
    port: int = 0,
    serve: bool = True,
    _prefilled: list[str] | None = None,
) -> tuple[str, ThreadingHTTPServer]:
    """Serve the Studio app in live mode: stream a real scan+gap run.

    Spawns `report run` (scan + gap only) as a subprocess that records its
    event stream to a temp JSONL file; tails the file and streams the events
    to the browser over SSE. `_prefilled` is a test hook — when given, skips
    the subprocess and serves those event lines as an already-complete stream.
    """
    html = build_served_html(root, stream=True)
    buffer: list[str] = []
    cond = threading.Condition()
    done = threading.Event()

    if _prefilled is not None:
        buffer.extend(_prefilled)
        done.set()
    else:
        _start_live_pipeline(root, buffer, cond, done)

    server = ThreadingHTTPServer(
        ("127.0.0.1", port), _make_live_handler(html, buffer, cond, done, root)
    )
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    if serve:
        print("  running a real scan + gap classification — verdicts stream in as the agent works")
    return _serve(server, url, open_browser=open_browser, serve=serve)


def _tail_event_log(
    log: Path,
    buffer: list[str],
    cond: threading.Condition,
    done: threading.Event,
    proc_done: threading.Event,
) -> None:
    """Tail `log` and push each line into `buffer`; signal `done` when `proc_done`
    is set and the file is fully drained. Shared by --live (subprocess sets
    proc_done on exit) and --watch (a watcher thread sets proc_done on
    agent_finished). Standalone helper so both modes use exactly the same
    tail logic — no fork in the streaming semantics."""
    import time

    while not log.exists() and not proc_done.is_set():
        time.sleep(0.05)
    try:
        fh = log.open(encoding="utf-8")
    except OSError:
        with cond:
            done.set()
            cond.notify_all()
        return
    with fh:
        while True:
            line = fh.readline()
            if line:
                s = line.strip()
                if s:
                    with cond:
                        buffer.append(s)
                        cond.notify_all()
                continue
            if proc_done.is_set():
                trailing = fh.readline()
                if not trailing:
                    break
                s = trailing.strip()
                if s:
                    with cond:
                        buffer.append(s)
                        cond.notify_all()
                continue
            time.sleep(0.08)
    with cond:
        done.set()
        cond.notify_all()


def run_studio_watch(
    root: Path | None,
    event_log_path: Path,
    *,
    open_browser: bool = True,
    port: int = 0,
    serve: bool = True,
) -> tuple[str, ThreadingHTTPServer]:
    """Attach mode: serve the Studio page and stream events from an externally-
    driven `report run`. The driver (the AI install prompt, a CI job, a user) sets
    `EFTERLEV_STUDIO_EVENT_LOG=<event_log_path>` for its `report run`, then opens
    Studio in this mode — Studio renders progress without spawning a pipeline,
    so the driver stays in control of the run."""
    html = build_served_html(root, stream=True)
    buffer: list[str] = []
    cond = threading.Condition()
    done = threading.Event()
    _start_attach_tailer(event_log_path, buffer, cond, done)
    server = ThreadingHTTPServer(
        ("127.0.0.1", port), _make_live_handler(html, buffer, cond, done, root)
    )
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    if serve:
        print(f"  attached — tailing {event_log_path}; start `report run` to stream events")
    return _serve(server, url, open_browser=open_browser, serve=serve)


def _start_live_pipeline(
    root: Path,
    buffer: list[str],
    cond: threading.Condition,
    done: threading.Event,
) -> None:
    """Run `report run` (scan+gap) in a subprocess; tail its event log into `buffer`."""
    import subprocess
    import sys
    import tempfile

    log = Path(tempfile.mkdtemp(prefix="efterlev-studio-")) / "events.jsonl"
    proc_done = threading.Event()

    def worker() -> None:
        env = {**os.environ, "EFTERLEV_STUDIO_EVENT_LOG": str(log)}
        # Skip only the LLM Documentation Agent — keep the deterministic report
        # stages (POA&M, OSCAL, VDR, inventory, inspector) so the command
        # center's Reports panel has artifacts to link after the run.
        cmd = [
            sys.executable, "-m", "efterlev", "report", "run",
            "--target", str(root), "--skip-document",
        ]  # fmt: skip
        # Skip the interactive init wizard when the workspace is already set up
        # (always true for --live --sample; common for real repos) — otherwise
        # `report run` would block the live run on stdin prompts.
        if (root / ".efterlev").is_dir():
            cmd.append("--skip-init")
        try:
            # Fixed argv list (no shell=True); the only dynamic element is the
            # resolved --target path, passed as a single argv element — no shell
            # injection surface. Bare `# nosemgrep` per CLAUDE.md gotcha
            # (registry rule_ids don't match short-form annotations).
            subprocess.run(cmd, env=env, check=False)  # nosemgrep
        finally:
            proc_done.set()

    threading.Thread(target=worker, daemon=True).start()
    threading.Thread(
        target=lambda: _tail_event_log(log, buffer, cond, done, proc_done), daemon=True
    ).start()


def _start_attach_tailer(
    log: Path,
    buffer: list[str],
    cond: threading.Condition,
    done: threading.Event,
) -> None:
    """Attach mode — tail an event log written by an external `report run` (e.g.,
    the AI install prompt with EFTERLEV_STUDIO_EVENT_LOG set). Doesn't spawn a
    pipeline. Signals `done` when the stream emits `agent_finished` (the
    pipeline's main completion event), with a 2s flush grace so trailing events
    land before the page's done handler fires."""
    import json as _json
    import time

    log.parent.mkdir(parents=True, exist_ok=True)
    proc_done = threading.Event()

    def watcher() -> None:
        seen_finish_at: float | None = None
        while not proc_done.is_set():
            time.sleep(0.5)
            with cond:
                tail_lines = list(buffer[-50:])
            if seen_finish_at is None:
                for line in tail_lines:
                    try:
                        if _json.loads(line).get("kind") == "agent_finished":
                            seen_finish_at = time.time()
                            break
                    except Exception:
                        continue
            if seen_finish_at is not None and time.time() - seen_finish_at > 2.0:
                proc_done.set()
                return

    threading.Thread(target=watcher, daemon=True).start()
    threading.Thread(
        target=lambda: _tail_event_log(log, buffer, cond, done, proc_done), daemon=True
    ).start()
