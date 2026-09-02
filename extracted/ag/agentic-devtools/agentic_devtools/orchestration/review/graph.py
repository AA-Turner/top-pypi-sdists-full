"""Graph builder for the LangGraph PR review pipeline.

Constructs a ``CompiledStateGraph`` with the following node sequence::

    fetch_pr_details → source_context → scaffold_comments → review_files → summarize_and_decide → post_results

The ``source_context`` node is always traversed. When ``source_context_enabled``
is ``False`` in the graph state the node performs a fast pass-through, setting
``context_status="disabled"`` on each file entry without performing any I/O.

LangGraph imports are deferred until ``build_review_graph()`` so callers can
gracefully detect a missing optional dependency before graph construction.
"""

from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from langgraph.graph.state import CompiledStateGraph

from .state import ReviewGraphState

# ---------------------------------------------------------------------------
# Known optional top-level packages: ModuleNotFoundError is suppressed only
# when the missing module belongs to one of these packages. Errors for any
# other module (transitive dependency failures, packaging issues, etc.) are
# re-raised immediately so they surface as hard errors rather than silently
# degrading to stub nodes.
# ---------------------------------------------------------------------------
_OPTIONAL_TOP_LEVEL_DEPS = frozenset({"langgraph", "langchain", "langchain_core", "langchain_community"})

# ---------------------------------------------------------------------------
# Stub node implementations (replaced by real nodes once wired)
# ---------------------------------------------------------------------------


def _stub_fetch_pr_details(state: dict[str, Any]) -> dict[str, Any]:
    """Stub: fetch PR details from Azure DevOps."""
    return {}


def _stub_source_context(state: dict[str, Any]) -> dict[str, Any]:
    """Stub: retrieve source context for changed files."""
    return {}


def _stub_scaffold_comments(state: dict[str, Any]) -> dict[str, Any]:
    """Stub: scaffold review comment threads."""
    return {}


def _stub_review_files(state: dict[str, Any]) -> dict[str, Any]:
    """Stub: review changed files with LLM."""
    return {"file_results": []}


def _stub_summarize_and_decide(state: dict[str, Any]) -> dict[str, Any]:
    """Stub: aggregate findings and produce verdict."""
    return {}


def _stub_post_results(state: dict[str, Any]) -> dict[str, Any]:
    """Stub: post results back to Azure DevOps."""
    return {}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

# Node registry — maps node names to their implementations.
# Import real nodes when available; fall back to stubs otherwise.
_NODE_REGISTRY: dict[str, Any] = {
    "fetch_pr_details": _stub_fetch_pr_details,
    "source_context": _stub_source_context,
    "scaffold_comments": _stub_scaffold_comments,
    "review_files": _stub_review_files,
    "summarize_and_decide": _stub_summarize_and_decide,
    "post_results": _stub_post_results,
}


def _load_real_nodes() -> None:
    """Import real node implementations and update the registry.

    Only ``ModuleNotFoundError`` raised for a known optional top-level package
    (e.g. ``langgraph``, ``langchain``) is suppressed here.  Any
    ``ModuleNotFoundError`` for a different module name — which indicates a
    missing transitive dependency of an installed package — is re-raised
    immediately so that packaging / runtime failures surface as a hard error
    rather than a silent fall-back to stub nodes.  Other ``ImportError``
    subclasses (missing name inside a module, import-time code bugs, etc.) are
    always re-raised.
    """
    try:
        from .nodes.fetch_pr_details import fetch_pr_details_node

        _NODE_REGISTRY["fetch_pr_details"] = fetch_pr_details_node
    except ModuleNotFoundError as exc:
        if (exc.name or "").split(".")[0] not in _OPTIONAL_TOP_LEVEL_DEPS:
            raise

    try:
        from .nodes.source_context import source_context_node

        _NODE_REGISTRY["source_context"] = source_context_node
    except ModuleNotFoundError as exc:
        if (exc.name or "").split(".")[0] not in _OPTIONAL_TOP_LEVEL_DEPS:
            raise

    try:
        from .nodes.scaffold_comments import scaffold_comments_node

        _NODE_REGISTRY["scaffold_comments"] = scaffold_comments_node
    except ModuleNotFoundError as exc:
        if (exc.name or "").split(".")[0] not in _OPTIONAL_TOP_LEVEL_DEPS:
            raise

    try:
        from .nodes.review_files import review_files_node

        _NODE_REGISTRY["review_files"] = review_files_node
    except ModuleNotFoundError as exc:
        if (exc.name or "").split(".")[0] not in _OPTIONAL_TOP_LEVEL_DEPS:
            raise

    try:
        from .nodes.summarize_and_decide import summarize_and_decide_node

        _NODE_REGISTRY["summarize_and_decide"] = summarize_and_decide_node
    except ModuleNotFoundError as exc:
        if (exc.name or "").split(".")[0] not in _OPTIONAL_TOP_LEVEL_DEPS:
            raise

    try:
        from .nodes.post_results import post_results_node

        _NODE_REGISTRY["post_results"] = post_results_node
    except ModuleNotFoundError as exc:
        if (exc.name or "").split(".")[0] not in _OPTIONAL_TOP_LEVEL_DEPS:
            raise


def build_review_graph(checkpointer: Any = None, *, provider_factory: Any = None) -> CompiledStateGraph:
    """Construct and compile the PR review ``StateGraph``.

    Args:
        checkpointer: Optional LangGraph checkpointer for durable state
            persistence.  Pass ``None`` for in-memory execution.
        provider_factory: Optional pre-built provider factory.  When
            supplied it is bound to the ``review_files`` node via a closure
            so that provider instances — which may retain resolved API keys —
            are never placed inside :class:`ReviewGraphState` and therefore
            never captured by the checkpointer or returned in the final graph
            result.

    Returns:
        A compiled ``CompiledStateGraph`` ready for invocation.
    """
    from langgraph.graph import END, StateGraph

    _load_real_nodes()

    graph = StateGraph(ReviewGraphState)

    graph.add_node("fetch_pr_details", _NODE_REGISTRY["fetch_pr_details"])
    graph.add_node("source_context", _NODE_REGISTRY["source_context"])
    graph.add_node("scaffold_comments", _NODE_REGISTRY["scaffold_comments"])

    review_files_fn = _NODE_REGISTRY["review_files"]
    if provider_factory is not None:
        review_files_fn = functools.partial(review_files_fn, provider_factory=provider_factory)
    graph.add_node("review_files", review_files_fn)

    graph.add_node("summarize_and_decide", _NODE_REGISTRY["summarize_and_decide"])
    graph.add_node("post_results", _NODE_REGISTRY["post_results"])

    graph.set_entry_point("fetch_pr_details")

    graph.add_edge("fetch_pr_details", "source_context")
    graph.add_edge("source_context", "scaffold_comments")
    graph.add_edge("scaffold_comments", "review_files")
    graph.add_edge("review_files", "summarize_and_decide")
    graph.add_edge("summarize_and_decide", "post_results")
    graph.add_edge("post_results", END)

    return graph.compile(checkpointer=checkpointer)
