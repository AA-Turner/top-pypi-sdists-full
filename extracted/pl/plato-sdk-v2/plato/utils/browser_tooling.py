"""Shell environment shared by browser pre-login and agent execution."""

AGENT_BROWSER_SOCKET_DIR_EXPORT = 'export AGENT_BROWSER_SOCKET_DIR="${AGENT_BROWSER_SOCKET_DIR:-$HOME/.agent-browser}"'
"""Use the same per-user daemon directory over SSH and RPC, independent of XDG.

A nonempty caller override wins; the default matches agent-browser's home
fallback. SSH's PAM session may set XDG_RUNTIME_DIR while an RPC job does not.
"""
