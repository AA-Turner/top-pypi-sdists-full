"""Process-isolated graph runner for the Go multi-process queue worker.

Entrypoint: ``python -m langgraph_api.runner``

Speaks the Runner gRPC service (bidi Execute) over ``LANGGRAPH_RUNNER_BIND``
(``unix:///path`` locally, ``host:port`` for sandboxes). Liveness is
``grpc.health.v1.Health``.

This module intentionally avoids importing the HTTP/SSE server stack.
"""
