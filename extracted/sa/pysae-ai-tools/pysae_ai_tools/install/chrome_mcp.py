"""Install the Chrome DevTools MCP server in ~/.claude.json."""

from typing import Any

from ..config import DATA_DIR
from .common.base import McpTool

# Dedicated, persistent Chrome profile for Claude. Kept under the data dir
# (never the cache dir, which may be purged) so sign-ins survive across runs
# and Claude never touches the user's day-to-day Chrome profile.
CHROME_PROFILE_DIR = DATA_DIR / "chrome-profile"


class ChromeMcpTool(McpTool):
    name = "chrome-mcp"
    server_name = "chrome-devtools"
    cli_help = "Install/configure the Chrome DevTools MCP server"

    def build_config(self) -> dict[str, Any]:
        # Package name is ``chrome-devtools-mcp`` on npm — no @anthropic-ai
        # scope (the scoped name is reserved but unpublished, npm 404).
        #
        # The MCP launches its own Chrome on a dedicated ``--user-data-dir``
        # rather than attaching to a running instance: recent Chrome refuses
        # remote debugging on the default profile, so the launch-a-dedicated-
        # profile path is the only reliable one and it keeps auth persistent.
        args: list[str] = [
            "chrome-devtools-mcp@latest",
            "--user-data-dir",
            str(CHROME_PROFILE_DIR),
        ]
        return {"command": "npx", "args": args}

    def prepare(self) -> None:
        CHROME_PROFILE_DIR.mkdir(parents=True, exist_ok=True)


tool = ChromeMcpTool()
