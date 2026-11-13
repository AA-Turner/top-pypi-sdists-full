"""Process-isolated graph executor for the Go multi-process queue worker.

Entrypoint: ``python -m langgraph_api.executor``

Opens single-dispatch bidi streams to the Orchestrator service at
``LANGGRAPH_ORCHESTRATOR_ADDRESS``.

This module intentionally avoids importing the HTTP/SSE server stack.
"""
