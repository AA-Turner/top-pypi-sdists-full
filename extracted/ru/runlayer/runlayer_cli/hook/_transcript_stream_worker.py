"""Detached transcript stream worker for Claude Code event hooks.

Spawned by relay.py as a fire-and-forget subprocess. Not intended for direct use.
"""

from __future__ import annotations

from runlayer_cli.truststore_init import inject as _inject_truststore

_inject_truststore()

# ruff: noqa: E402 - imports below intentionally come after _inject_truststore()
import argparse
import json
import sys
from typing import Any

from runlayer_cli.hook.transcript_stream import (
    clear_transcript_stream_active,
    run_transcript_stream,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    payload: dict[str, Any] = {}
    try:
        wrapper = json.loads(sys.stdin.read() or "{}")
        if not isinstance(wrapper, dict):
            return
        client_name = wrapper.get("client")
        raw_payload = wrapper.get("payload")
        if not isinstance(client_name, str) or not isinstance(raw_payload, dict):
            return
        payload = raw_payload
        start_offset = wrapper.get("start_offset", 0)
        if not isinstance(start_offset, int):
            start_offset = 0
        run_transcript_stream(
            client_name=client_name,
            payload=payload,
            start_offset=start_offset,
            debug=args.debug,
        )
    except Exception:
        clear_transcript_stream_active(payload)


if __name__ == "__main__":
    main()
