"""Compatibility shim: blender-mcp is now mcp-for-blender."""

import sys

_NOTICE = """\
──────────────────────────────────────────────────────────────
  blender-mcp is now mcp-for-blender.

  This package is a compatibility wrapper. Everything still
  works and there is nothing you need to change today.

  When convenient, update your MCP client config to:
      uvx mcp-for-blender

  https://github.com/ahujasid/mcp-for-blender
──────────────────────────────────────────────────────────────
"""


def main():
    # stderr only — stdout is the JSON-RPC channel for this stdio server
    print(_NOTICE, file=sys.stderr, flush=True)
    from blender_mcp.server import main as _real_main
    return _real_main()
