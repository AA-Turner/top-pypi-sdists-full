"""Typed world→agent RPC layer.

Replaces SSH-based control between the world VM and its agent VMs with a
structured HTTP protocol (unary requests + long-poll waits). The shared contract lives here
(``plato.rpc.protocol``, ``plato.rpc.errors``, ``plato.rpc.models``); the
world-side client under ``plato.rpc.client``; the agent-side daemon under
``plato.agents.daemon``. SSH remains only as the bootstrap channel
(``plato.rpc.client.bootstrap``) and for the data plane (rsync, git objects).

Design doc: docs/agent-rpc-design.md.
"""

from plato.rpc.protocol import DEFAULT_PORT, PROTOCOL_VERSION

__all__ = ["DEFAULT_PORT", "PROTOCOL_VERSION"]
