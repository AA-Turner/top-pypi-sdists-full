"""Synthetic Tool wrapper for Slack — no local install.

The Slack integration in this repo is a set of subcommands
(``pysae-ai-tools slack …``) that hit the Slack Web API directly from
our scripts. There is no MCP server to install and no binary to put on
PATH. This module exists solely so that ``tools configure`` and
``tools status`` surface the SLACK_* env vars those subcommands need.

``get_state`` reports the tool as already installed
(``needs_install=False``) so the meta-installer short-circuits to
``up-to-date``; ``do_install`` is a no-op safety net invoked only if
state reporting fails.
"""

from .common.base import BaseTool, InstallReport, ToolState


class SlackTool(BaseTool):
    """Synthetic tool for the Slack subcommands — no binary, no MCP server."""

    # Vars consumed by `pysae-ai-tools slack …` (direct Slack API calls from our
    # scripts, not an MCP). The tool declares them so ``tools configure`` /
    # ``tools status`` surface them; the registry reads them from here.
    env_pre_configure = ("SLACK_BOT_TOKEN", "SLACK_USER_TOKEN", "SLACK_CLIENT_ID", "SLACK_CLIENT_SECRET")
    env_help = {
        "SLACK_BOT_TOKEN": "AWS Secrets Manager (ai-tools/slack slack-app-token) ou OAuth via `slack get-token`",
        "SLACK_USER_TOKEN": "OAuth user-flow via `slack get-token --user-only` (cache local)",
        "SLACK_CLIENT_ID": "AWS Secrets Manager (ai-tools/slack slack-client-id)",
        "SLACK_CLIENT_SECRET": "AWS Secrets Manager (ai-tools/slack slack-client-secret)",
    }

    @property
    def name(self) -> str:
        return "slack-env"

    def get_state(self) -> ToolState:
        return ToolState(
            needs_install=False,
            needs_update=False,
            extra={"managed_by": "pysae-ai-tools slack subcommands (no install)"},
        )

    def do_install(self) -> InstallReport:
        return InstallReport(
            action="noop",
            method="no install required",
            extra={"note": "Slack integration uses direct API calls from `pysae-ai-tools slack …`."},
        )


tool = SlackTool()
