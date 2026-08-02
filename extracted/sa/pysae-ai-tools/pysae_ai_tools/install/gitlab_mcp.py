"""Install the GitLab MCP server (zereight/gitlab-mcp) in ~/.claude.json."""

import os
from typing import Any

from .common.base import EnvVar, McpTool


class GitlabMcpTool(McpTool):
    name = "gitlab-mcp"
    server_name = "gitlab"
    cli_help = "Install/configure the GitLab MCP server"

    @property
    def env_vars(self) -> list[EnvVar]:
        return [
            EnvVar(
                "GITLAB_PERSONAL_ACCESS_TOKEN",
                help=(
                    "glab config get token --host gitlab.com"
                    "  # or GitLab → Preferences → Access Tokens → New Token (api scope)"
                ),
            ),
        ]

    def build_config(self) -> dict[str, Any]:
        token = os.environ.get("GITLAB_PERSONAL_ACCESS_TOKEN", "").strip()
        if not token:
            raise ValueError("GITLAB_PERSONAL_ACCESS_TOKEN must be set")
        return {
            "command": "npx",
            "args": ["-y", "@zereight/mcp-gitlab"],
            "env": {
                "GITLAB_PERSONAL_ACCESS_TOKEN": token,
                "GITLAB_API_URL": os.environ.get("GITLAB_API_URL", "https://gitlab.com/api/v4"),
                "USE_PIPELINE": "true",
                "USE_MILESTONE": "true",
                "USE_GITLAB_WIKI": "false",
            },
        }


tool = GitlabMcpTool()
