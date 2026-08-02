"""Install the Kubernetes dev MCP server (read/write) in ~/.claude.json."""

from typing import Any

from .common import kubeconfig
from .common.base import McpTool

CONTEXT = "pysae-dev"


class KubernetesMcpDevTool(McpTool):
    name = "kubernetes-mcp-dev"
    server_name = "kubernetes-dev"
    cli_help = "Install/configure the Kubernetes dev MCP server (read/write)"

    def build_config(self) -> dict[str, Any]:
        # npm package ``mcp-server-kubernetes``, pinned to the ``pysae-dev``
        # cluster via a single-context KUBECONFIG. K8S_CONTEXT is kept as a
        # belt-and-braces hint, but the server ignores it (4.0.4) and follows
        # the kubeconfig current-context — hence the dedicated file.
        return {
            "command": "npx",
            "args": ["mcp-server-kubernetes@latest"],
            "env": {
                "KUBECONFIG": str(kubeconfig.dedicated_kubeconfig_path(CONTEXT)),
                "K8S_CONTEXT": CONTEXT,
            },
        }

    def prepare(self) -> None:
        kubeconfig.write_dedicated_kubeconfig(CONTEXT)


tool = KubernetesMcpDevTool()
