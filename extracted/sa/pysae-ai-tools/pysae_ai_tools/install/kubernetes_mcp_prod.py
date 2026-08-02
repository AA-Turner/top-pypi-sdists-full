"""Install the Kubernetes prod MCP server (read-only) in ~/.claude.json."""

from typing import Any

from .common import kubeconfig
from .common.base import McpTool

CONTEXT = "pysae-prod"


class KubernetesMcpProdTool(McpTool):
    name = "kubernetes-mcp-prod"
    server_name = "kubernetes-prod"
    cli_help = "Install/configure the Kubernetes prod MCP server (read-only)"

    def build_config(self) -> dict[str, Any]:
        # Pinned to the ``pysae-prod`` cluster via a single-context KUBECONFIG
        # (the server ignores K8S_CONTEXT and follows the current-context).
        # ``ALLOW_ONLY_READONLY_TOOLS`` blocks every mutating tool — prod stays
        # inspect-only, mirroring the MongoDB prod MCP's ``--readOnly``.
        return {
            "command": "npx",
            "args": ["mcp-server-kubernetes@latest"],
            "env": {
                "KUBECONFIG": str(kubeconfig.dedicated_kubeconfig_path(CONTEXT)),
                "K8S_CONTEXT": CONTEXT,
                "ALLOW_ONLY_READONLY_TOOLS": "true",
            },
        }

    def prepare(self) -> None:
        kubeconfig.write_dedicated_kubeconfig(CONTEXT)


tool = KubernetesMcpProdTool()
