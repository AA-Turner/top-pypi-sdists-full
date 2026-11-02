"""Run the CLI as ``python -m labqoat``."""

from __future__ import annotations

from labqoat.cli.cli_application import CliApplication

if __name__ == "__main__":
    code = CliApplication.main()
    if code:
        raise SystemExit(code)
