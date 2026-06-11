"""Transitional forwarder for the renamed package.

``linkedin-scraper-mcp`` was renamed to ``mcp-server-linkedin``. This package
depends on the new one and forwards the console entry point, so existing
``uvx linkedin-scraper-mcp`` configurations keep working while users migrate.
"""

import sys

_NOTICE = (
    "linkedin-scraper-mcp was renamed to mcp-server-linkedin. "
    "Update your config to: uvx mcp-server-linkedin@latest"
)


def main() -> None:
    print(_NOTICE, file=sys.stderr)
    from linkedin_mcp_server.cli_main import main as real_main

    real_main()
