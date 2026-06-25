"""Back-compat shim. The generic LangChain usage extraction moved to
``aigie.tracing.lc_usage`` so it can be shared by both the LangGraph and
LangChain integrations without a langgraph→langchain import cycle.
"""

from __future__ import annotations

from aigie.tracing.lc_usage import (
    extract_langchain_usage,
    usage_payload,
)

__all__ = ["extract_langchain_usage", "usage_payload"]
