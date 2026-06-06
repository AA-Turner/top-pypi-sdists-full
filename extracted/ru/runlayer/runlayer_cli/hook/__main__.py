"""``python -m runlayer_cli.hook`` entrypoint (frozen binaries use argv[0] dispatch instead)."""

from __future__ import annotations

from runlayer_cli.truststore_init import inject as _inject_truststore

_inject_truststore()

# ruff: noqa: E402 - imports below intentionally come after _inject_truststore()
import sys

from runlayer_cli.hook import _transcript_stream_worker
from runlayer_cli.hook.dispatch import run_hook
from runlayer_cli.hook.relay import TRANSCRIPT_STREAM_WORKER_SENTINEL


def main() -> None:
    if len(sys.argv) >= 2 and sys.argv[1] == TRANSCRIPT_STREAM_WORKER_SENTINEL:
        sys.argv = [sys.argv[0], *sys.argv[2:]]
        _transcript_stream_worker.main()
        return
    run_hook()


if __name__ == "__main__":
    main()
