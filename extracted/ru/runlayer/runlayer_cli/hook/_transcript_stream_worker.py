"""Detached transcript stream worker for Claude Code event hooks.

Spawned by relay.py as a fire-and-forget subprocess. Not intended for direct use.
"""

from __future__ import annotations

from runlayer_cli.truststore_init import inject as _inject_truststore

_inject_truststore()

# ruff: noqa: E402 - imports below intentionally come after _inject_truststore()
import argparse
import contextlib
import json
import sys
import threading
from typing import Any

from runlayer_cli.hook.relay import (
    TRANSCRIPT_FLUSH_MAX_BYTES,
    flush_stale_transcript_sent_states,
    send_unsent_transcript,
)
from runlayer_cli.hook.transcript_stream import (
    _CLAIM_HEARTBEAT_SECONDS,
    _session_id,
    clear_transcript_stream_active,
    clear_transcript_stream_claim,
    heartbeat_transcript_stream_claim,
    resolve_transcript_path,
    run_transcript_stream,
)


def _flush_backlog(client_name: str, payload: dict[str, Any], *, debug: bool) -> None:
    """Deliver unsent ranges before tailing starts: the tailer reads only bytes
    appended after start_offset, so the sent-offset→EOF backlog must flush here
    or the tailer's offset persistence would mark that gap as delivered. Also
    sweeps stale sent-states of sessions that died without a Stop."""
    path = resolve_transcript_path(payload)
    if path is not None:
        with contextlib.suppress(Exception):
            send_unsent_transcript(
                client_name,
                "Stop",
                payload,
                path,
                max_bytes=TRANSCRIPT_FLUSH_MAX_BYTES,
                debug=debug,
            )
    with contextlib.suppress(Exception):
        flush_stale_transcript_sent_states(
            client_name,
            exclude_session_id=_session_id(payload),
            debug=debug,
        )


def _flush_backlog_with_claim_heartbeat(
    client_name: str,
    payload: dict[str, Any],
    *,
    claim_token: str | None,
    debug: bool,
) -> None:
    if claim_token is None:
        _flush_backlog(client_name, payload, debug=debug)
        return

    stopped = threading.Event()

    def heartbeat() -> None:
        while not stopped.is_set():
            with contextlib.suppress(Exception):
                heartbeat_transcript_stream_claim(payload, claim_token)
            if stopped.wait(_CLAIM_HEARTBEAT_SECONDS):
                break

    heartbeat_thread = threading.Thread(target=heartbeat, daemon=True)
    heartbeat_thread.start()
    try:
        _flush_backlog(client_name, payload, debug=debug)
    finally:
        stopped.set()
        heartbeat_thread.join(timeout=1.0)


def main() -> None:
    # Frozen aiwatch spawns the worker via the sentinel argv re-exec (routed
    # through aiwatch.py:main, which marks the runtime + is frozen-detected).
    # The unfrozen ``-m runlayer_cli.hook._transcript_stream_worker`` spawn is
    # the pip-installed ``runlayer`` package and must keep reading config.yaml,
    # so it does NOT mark the aiwatch runtime.
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    payload: dict[str, Any] = {}
    claim_token: str | None = None
    try:
        wrapper = json.loads(sys.stdin.read() or "{}")
        if not isinstance(wrapper, dict):
            return
        raw_claim_token = wrapper.get("claim_token")
        if isinstance(raw_claim_token, str) and raw_claim_token:
            claim_token = raw_claim_token
        client_name = wrapper.get("client")
        raw_payload = wrapper.get("payload")
        if isinstance(raw_payload, dict):
            payload = raw_payload
        if not isinstance(client_name, str) or not isinstance(raw_payload, dict):
            return
        start_offset = wrapper.get("start_offset", 0)
        if not isinstance(start_offset, int):
            start_offset = 0
        _flush_backlog_with_claim_heartbeat(
            client_name,
            payload,
            claim_token=claim_token,
            debug=args.debug,
        )
        run_transcript_stream(
            client_name=client_name,
            payload=payload,
            start_offset=start_offset,
            debug=args.debug,
            claim_token=claim_token,
        )
    except Exception:
        clear_transcript_stream_active(payload)
    finally:
        if claim_token is not None:
            clear_transcript_stream_claim(payload, claim_token)


if __name__ == "__main__":
    main()
