"""Hidden hook relay command for use by runlayer-hook.sh and aiwatch-enforce."""

import json
import sys
import time
from pathlib import Path

import httpx
import typer

from runlayer_cli.api import API_KEY_HEADER_NAME, USER_AGENT
from runlayer_cli.config import load_config
from runlayer_cli.hook.transcript_stream import (
    clear_transcript_stream_active,
    run_transcript_stream,
)
from runlayer_cli.tls import http_client

app = typer.Typer(hidden=True)

_TARGETS: dict[str, tuple[str, int]] = {
    "enforce": ("/api/v1/hooks/cursor", 30),
    "event": ("/api/v1/hooks/events", 5),
    "tool-pre": ("/api/v1/hooks/tool/pre", 30),
    "tool-post": ("/api/v1/hooks/tool/post", 30),
}

_DEBUG_DIR = Path("/tmp")


def _write_debug(
    target: str, url: str, request_body: str, resp: httpx.Response | None
) -> None:
    """Write structural metadata only — never the bodies.

    Bodies can contain credentials piped via stdin, tool inputs with file
    paths / tokens, and policy verdicts that may quote scanned content. We'd
    rather lose body-level debuggability than persist anything sensitive to
    `/tmp` (world-readable on most setups). Size + status + URL is enough to
    confirm the relay reached the backend; reproduce payload-level issues by
    re-running the hook with a controlled stdin instead.
    """
    ts = int(time.time())
    data = {
        "timestamp": ts,
        "url": url,
        "request_body_size": len(request_body) if request_body else 0,
        "response_status": resp.status_code if resp else None,
        "response_body_size": len(resp.text) if resp else None,
    }
    path = _DEBUG_DIR / f"runlayer-relay-{target}-{ts}.json"
    path.write_text(json.dumps(data, indent=2))


@app.command()
def relay(
    target: str = typer.Argument(
        help="Relay target: 'enforce', 'event', 'tool-pre', or 'tool-post'"
    ),
    timeout: int | None = typer.Option(None, help="Override default timeout (seconds)"),
    debug: bool = typer.Option(False, "--debug", hidden=True),
) -> None:
    """Read JSON from stdin, resolve credentials, POST to the hooks endpoint."""
    if target == "stream-transcript":
        stream_transcript(debug=debug)
        return

    if target not in _TARGETS:
        typer.echo(
            "Unknown target: "
            f"{target}. Use 'enforce', 'event', 'tool-pre', or 'tool-post'.",
            err=True,
        )
        raise typer.Exit(1)
    endpoint, default_timeout = _TARGETS[target]
    effective_timeout = timeout if timeout is not None else default_timeout

    config = load_config()
    host = config.default_host
    if not host:
        raise typer.Exit(1)
    secret = config.get_secret_for_host(host)
    if not secret:
        raise typer.Exit(1)

    url = f"{host}{endpoint}"
    payload = sys.stdin.read()
    try:
        with http_client() as client:
            resp = client.post(
                url,
                content=payload,
                headers={
                    "Content-Type": "application/json",
                    API_KEY_HEADER_NAME: secret,
                    "User-Agent": USER_AGENT,
                },
                timeout=effective_timeout,
            )
        if debug:
            try:
                _write_debug(target, url, payload, resp)
            except Exception:
                pass
        sys.stdout.write(resp.text)
        raise typer.Exit(0 if resp.is_success else 2)
    except (httpx.HTTPError, OSError):
        if debug:
            try:
                _write_debug(target, url, payload, None)
            except Exception:
                pass
        raise typer.Exit(2)


def stream_transcript(
    debug: bool = False,
) -> None:
    """Read a transcript stream request from stdin and forward live events."""
    payload = {}
    try:
        wrapper = json.loads(sys.stdin.read() or "{}")
        if not isinstance(wrapper, dict):
            raise typer.Exit(0)
        client_name = wrapper.get("client")
        raw_payload = wrapper.get("payload")
        if not isinstance(client_name, str) or not isinstance(raw_payload, dict):
            raise typer.Exit(0)
        payload = raw_payload
        start_offset = wrapper.get("start_offset", 0)
        if not isinstance(start_offset, int):
            start_offset = 0
        run_transcript_stream(
            client_name=client_name,
            payload=payload,
            start_offset=start_offset,
            debug=debug,
        )
    except typer.Exit:
        raise
    except Exception:
        clear_transcript_stream_active(payload)
