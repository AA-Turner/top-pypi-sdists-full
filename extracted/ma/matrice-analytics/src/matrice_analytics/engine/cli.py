"""``matrice-analytics`` — the command an app author runs before publishing.

    matrice-analytics validate ./v1.4                 # is this app ready?
    matrice-analytics validate --all applications/    # are all of them?
    matrice-analytics describe ./v1.4                 # what would run, without running it
    matrice-analytics schema app.schema.json          # editor completion for app.yaml

``validate`` is the point of the whole package. It loads ``app.yaml``, reads the three files the
version uploads beside it, cross-checks them, and then **runs the engine** over synthetic frames to
prove the key strings the dashboard will send to ClickHouse come back with data in them. That last
step is the only verification a ``custom`` stage ever gets.

Exit codes: ``0`` ready, ``1`` a check failed, ``2`` the command line was wrong.

The subcommands are thin: each delegates to a library function that a host repo can call directly
(:func:`~matrice_analytics.engine.testing.validate_app`,
:func:`~matrice_analytics.engine.testing.validate_apps`), because automating "are all apps ready"
should not require shelling out.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

__all__ = ["build_parser", "main"]

_PROG = "matrice-analytics"

#: The engine's annotations are PEP 604 unions evaluated at runtime by Pydantic, so the package's
#: declared ``>=3.8`` floor does not apply to it. Saying so beats an import-time ``TypeError``
#: whose traceback points at a Pydantic internal.
_MIN_PYTHON = (3, 10)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=_PROG,
        description="Validate an analytics application against the engine that will run it.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    validate = subcommands.add_parser(
        "validate",
        help="run every generated check for one app, or for every app under a root",
        description=(
            "Loads app.yaml, reads metrics.json / widgets.json / post_processing_config.json, "
            "cross-checks them, and runs the engine to prove every declared key is really "
            "published. Exit 0 when ready."
        ),
    )
    validate.add_argument("app", nargs="+", help="an app folder, its app.yaml, or a bare app id")
    validate.add_argument(
        "--all",
        action="store_true",
        help="treat each argument as a root to search for app folders, not as one app",
    )
    validate.add_argument(
        "--summary",
        action="store_true",
        help="one line per app instead of the full per-check report",
    )

    describe = subcommands.add_parser(
        "describe",
        help="print what the generated suite would do, without running it",
    )
    describe.add_argument("app", nargs="+", help="an app folder, its app.yaml, or a bare app id")

    schema = subcommands.add_parser(
        "schema",
        help="write the app.yaml JSON Schema, for editor completion",
    )
    schema.add_argument("output", nargs="?", default="app.schema.json", help="'-' for stdout")
    schema.add_argument("--indent", type=int, default=2)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if sys.version_info < _MIN_PYTHON:  # pragma: no cover - depends on the interpreter
        needed = ".".join(str(part) for part in _MIN_PYTHON)
        running = ".".join(str(part) for part in sys.version_info[:3])
        print(
            f"{_PROG} needs Python {needed} or newer; this interpreter is {running}. The package "
            f"declares a lower floor for its legacy modules, but the analytics engine does not "
            f"import on it.",
            file=sys.stderr,
        )
        return 2

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        return _validate(args)
    if args.command == "describe":
        return _describe(args)
    return _schema(args)


def _validate(args: argparse.Namespace) -> int:
    from matrice_analytics.engine.testing import validate_app, validate_apps

    failed = False
    blocks: list[str] = []

    if args.all:
        for root in args.app:
            result = validate_apps(root)
            blocks.append(result.summary() if args.summary else result.report())
            if not result.ok:
                failed = True
    else:
        for app in args.app:
            result = validate_app(app)
            if args.summary:
                blocks.append(f"{'PASS' if result.passed else 'FAIL'}  {result.app_id}  ({result.source})")
            else:
                blocks.append(result.report())
            if not result.passed:
                failed = True

    print("\n\n".join(blocks))
    return 1 if failed else 0


def _describe(args: argparse.Namespace) -> int:
    from matrice_analytics.engine.testing import describe_suite

    print("\n\n".join(describe_suite(app) for app in args.app))
    return 0


def _schema(args: argparse.Namespace) -> int:
    from matrice_analytics.engine.manifest.jsonschema import main as schema_main

    return schema_main([args.output, "--indent", str(args.indent)])


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
