"""Generic kubectl command execution tool.

Allows running arbitrary kubectl commands server-side via tbot identity.
RBAC is enforced by the Teleport role assigned to the bot identity.
"""

from __future__ import annotations

import shlex

from cube_cloud.teleport.kubeconfig import run_kubectl
from cube_cloud.teleport.tbot_manager import tbot

BLOCKED_SUBCOMMANDS = {
    "delete", "drain", "cordon", "taint", "edit",
    "patch", "apply", "create", "replace",
}


async def kubectl_exec(command: str, cluster: str | None = None, profile: str = "admin") -> str:
    """Execute a kubectl command server-side.

    Args:
        command: The kubectl command (without the 'kubectl' prefix).
        cluster: Target Cube cluster name. Required.
        profile: User's Teleport role for kubeconfig scoping.

    Returns formatted output string.
    """
    if not tbot.is_ready:
        return "tbot credentials not ready. Server-side kubectl is not available yet."

    if not cluster:
        return "Error: cluster name is required. Use cube_list to see available clusters."

    args = shlex.split(command)
    if not args:
        return "Error: empty command"

    subcommand = args[0].lower()
    if subcommand in BLOCKED_SUBCOMMANDS:
        return (
            f"Error: '{subcommand}' is blocked for safety. "
            f"Blocked commands: {', '.join(sorted(BLOCKED_SUBCOMMANDS))}"
        )

    output, rc = await run_kubectl(args, cluster=cluster, profile=profile, timeout=120)

    if rc != 0:
        return f"kubectl {command} (cluster: {cluster})\n\nExit code: {rc}\n\n{output}"

    return f"kubectl {command} (cluster: {cluster})\n\n{output}"
