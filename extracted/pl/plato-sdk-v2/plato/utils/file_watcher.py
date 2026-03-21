"""Agent-side file watcher sidecar for checkpoint triggers.

Runs on the agent VM as a background process.  Polls workspace directories
for files matching configured glob patterns.  When a match is detected,
reads the current tool execution context for span information and pushes
a trigger event over a plain TCP socket to the world VM's
:class:`~plato.worlds.checkpoint.CheckpointTriggerServer`.

Usage (started automatically by :class:`~plato.agents.runner.AgentRunner`)::

    python3 -m plato.utils.file_watcher /tmp/plato-file-watcher-config.json

Config file format::

    {
        "server_url": "10.0.0.1:8765",
        "patterns": ["**/progress.json"],
        "watch_paths": ["/workspace/code"],
        "poll_interval_s": 2.0
    }
"""

from __future__ import annotations

import json
import logging
import os
import socket
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

logger = logging.getLogger(__name__)

TOOL_EXECUTION_CONTEXT_PATH = Path("/tmp/plato-tool-execution-context.json")
TOOL_START_SPOOL_PATH = Path("/tmp/plato-tool-starts.jsonl")


def _snapshot_mtimes(watch_paths: list[str], patterns: list[str]) -> dict[str, float]:
    """Return ``{absolute_path: mtime}`` for all files matching any pattern."""
    mtimes: dict[str, float] = {}
    for watch_path in watch_paths:
        root = Path(watch_path)
        if not root.exists():
            continue
        for pattern in patterns:
            for path in root.glob(pattern):
                if path.is_file():
                    try:
                        mtimes[str(path)] = os.stat(path).st_mtime
                    except OSError:
                        pass
    return mtimes


def _read_span_context() -> dict[str, str]:
    """Read current span/trace context from tool execution files."""
    result: dict[str, str] = {"span_id": "", "trace_id": "", "tool_name": ""}

    # Base context (agent-level span)
    if TOOL_EXECUTION_CONTEXT_PATH.exists():
        try:
            ctx = json.loads(TOOL_EXECUTION_CONTEXT_PATH.read_text())
            result["span_id"] = ctx.get("span_id", "")
            result["trace_id"] = ctx.get("trace_id", "")
        except Exception:
            pass

    # Try to find the most recent tool start for better span attribution
    if TOOL_START_SPOOL_PATH.exists():
        try:
            text = TOOL_START_SPOOL_PATH.read_text()
            lines = text.strip().splitlines()
            if lines:
                # Last line is most recent tool start
                last = json.loads(lines[-1])
                if last.get("span_id"):
                    result["span_id"] = last["span_id"]
                if last.get("trace_id"):
                    result["trace_id"] = last["trace_id"]
                if last.get("tool_name"):
                    result["tool_name"] = last["tool_name"]
        except Exception:
            pass

    return result


def _send_trigger(
    sock: socket.socket | None,
    server_url: str,
    path: str,
    pattern: str,
    span_ctx: dict[str, str],
) -> socket.socket | None:
    """Send a trigger event over TCP, reconnecting if needed."""
    event = json.dumps(
        {
            "path": path,
            "pattern": pattern,
            "span_id": span_ctx.get("span_id", ""),
            "trace_id": span_ctx.get("trace_id", ""),
            "tool_name": span_ctx.get("tool_name", ""),
            "timestamp": datetime.now(UTC).isoformat(),
        }
    )
    payload = (event + "\n").encode()

    for attempt in range(2):
        try:
            if sock is None:
                host, port_str = server_url.rsplit(":", 1)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5.0)
                sock.connect((host, int(port_str)))
                logger.info("Connected to trigger server at %s", server_url)
            sock.sendall(payload)
            return sock
        except Exception:
            logger.debug("Send failed (attempt %d), reconnecting", attempt + 1)
            if sock is not None:
                try:
                    sock.close()
                except Exception:
                    pass
                sock = None
    logger.warning("Failed to send trigger event to %s", server_url)
    return None


def run(config_path: str) -> None:
    """Main loop: poll for file changes and send trigger events."""
    config_file = Path(config_path)
    if not config_file.exists():
        logger.error("Config file not found: %s", config_path)
        return

    config = json.loads(config_file.read_text())
    server_url: str = config["server_url"]
    patterns: list[str] = config["patterns"]
    watch_paths: list[str] = config["watch_paths"]
    poll_interval: float = config.get("poll_interval_s", 2.0)

    logger.info(
        "File watcher starting: server=%s patterns=%s watch_paths=%s poll=%.1fs",
        server_url,
        patterns,
        watch_paths,
        poll_interval,
    )

    prev = _snapshot_mtimes(watch_paths, patterns)
    sock: socket.socket | None = None

    try:
        while True:
            time.sleep(poll_interval)

            # Exit if config file deleted (cleanup signal)
            if not config_file.exists():
                logger.info("Config file removed, exiting")
                break

            curr = _snapshot_mtimes(watch_paths, patterns)
            if curr == prev:
                continue

            # Find changed/new files
            changed_files: list[str] = []
            for fpath, mtime in curr.items():
                if fpath not in prev or prev[fpath] != mtime:
                    changed_files.append(fpath)

            if not changed_files:
                prev = curr
                continue

            span_ctx = _read_span_context()

            for fpath in changed_files:
                # Find which pattern matched this file
                matched_pattern = patterns[0]  # default
                for p in patterns:
                    for wp in watch_paths:
                        try:
                            rel = Path(fpath).relative_to(wp)
                            if rel.match(p):
                                matched_pattern = p
                                break
                        except ValueError:
                            pass

                logger.info("File trigger: %s (pattern=%s)", fpath, matched_pattern)
                sock = _send_trigger(sock, server_url, fpath, matched_pattern, span_ctx)

            prev = curr
    except KeyboardInterrupt:
        pass
    finally:
        if sock is not None:
            try:
                sock.close()
            except Exception:
                pass
        logger.info("File watcher exiting")


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    if len(sys.argv) < 2:
        print(f"Usage: python3 -m {__name__} <config-path>", file=sys.stderr)
        return 1
    run(sys.argv[1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
