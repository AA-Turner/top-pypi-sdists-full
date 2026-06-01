"""Detached relay worker — receives JSON on stdin, POSTs to the hooks endpoint.

Spawned by relay.py as a fire-and-forget subprocess. Not intended for direct use.
"""

from __future__ import annotations

from runlayer_cli.truststore_init import inject as _inject_truststore

_inject_truststore()

# ruff: noqa: E402 - imports below intentionally come after _inject_truststore()
import argparse
import sys

from runlayer_cli.hook.relay import RelayError, _TARGETS, _load_credentials, _post


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", choices=list(_TARGETS))
    parser.add_argument("--timeout", type=int, default=None)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    endpoint, default_timeout = _TARGETS[args.target]
    effective_timeout = args.timeout if args.timeout is not None else default_timeout

    payload = sys.stdin.read()
    try:
        host, secret = _load_credentials()
        _post(
            host,
            secret,
            endpoint,
            payload,
            target=args.target,
            timeout=effective_timeout,
            debug=args.debug,
        )
    except (RelayError, Exception):
        pass


if __name__ == "__main__":
    main()
