"""Computer-use primitives shared between the computer-use agent and the SDK.

``base`` holds the pieces both computers need (ToolResult, the action
recorder mixin, bash-output capping, clip-op hooks). ``remote_computer``
holds :class:`RemoteDesktopComputer`, which proxies every action to a remote
ubuntu-vm desktop over HTTP — the only computer the SDK exposes. The local
Xvfb-backed ``DesktopComputer`` deliberately stays in the computer-use agent
package: MCP-exposed computer use always targets a remote desktop VM, never
the agent VM itself.
"""

from plato.computer_use.base import ToolResult
from plato.computer_use.remote_computer import RemoteDesktopComputer

__all__ = ["RemoteDesktopComputer", "ToolResult"]
