"""Agent-side RPC daemon (``plato-agent-daemon``).

Serves the /v1 agent RPC API (see plato.rpc) over HTTP on the session mesh. Started by the world VM via one bootstrap SSH command; from then
on all world→agent control rides this daemon instead of SSH.
"""
