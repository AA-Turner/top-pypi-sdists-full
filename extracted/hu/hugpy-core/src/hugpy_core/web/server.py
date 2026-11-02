"""Installed Flask HTTP entry point.

The application and its routes are assembled by ``abstract_flask`` in
``web.app.build_app``. Telemetry collection has its own systemd unit.
"""
from __future__ import annotations

import argparse
import logging


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="hugpy-core serve")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7020)
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO)

    from hugpy_core import schema
    schema.ensure()
    from hugpy_core.models.identity import reconcile
    from hugpy_core.imports.functions import core_dsn
    import psycopg
    with psycopg.connect(core_dsn()) as conn:
        result = reconcile(conn)
    logging.getLogger(__name__).info("model identity reconciliation: %s", result)
    from hugpy_core.web.app import build_app
    from werkzeug.serving import run_simple
    run_simple(args.host, args.port, build_app(), threaded=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
