"""Dreadnode process entrypoint."""

from __future__ import annotations


def run(argv: list[str] | None = None) -> None:
    from dreadnode.app.cli import run as app_run

    app_run(argv)


if __name__ == "__main__":
    run()
