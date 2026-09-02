"""Graph builder utility for constructing LangGraph StateGraph instances."""

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from .nodes import (
    checklist_creation_node,
    commit_node,
    completion_node,
    implementation_node,
    implementation_review_node,
    initiate_node,
    planning_node,
    pull_request_node,
    retrieve_node,
    setup_node,
    verification_node,
)
from .pilot_workflow import (
    error_handler_node,
    route_after_checklist_creation,
    route_after_commit,
    route_after_implementation,
    route_after_implementation_review,
    route_after_initiate,
    route_after_plan,
    route_after_pull_request,
    route_after_retrieve,
    route_after_setup,
    route_after_verify,
)
from .state_schema import WorkOnIssueState


def build_work_on_issue_graph(checkpointer=None) -> CompiledStateGraph:
    """Construct and compile the work-on-jira-issue StateGraph.

    Args:
        checkpointer: Optional LangGraph checkpointer (e.g. ``SqliteSaver``)
            for durable state persistence.  Pass ``None`` for in-memory-only
            execution (useful for tests and diagram generation).

    Returns:
        A compiled ``CompiledStateGraph`` ready for invocation.
    """
    graph = StateGraph(WorkOnIssueState)

    # -- nodes ---------------------------------------------------------------
    # ADR: No implementation_gate node shall be added to this graph.
    # The work-on-issue workflow is fully autonomous; human gates were
    # removed per issue #1898. See specs/1898-remove-planning-gate-interrupt/spec.md
    # for rationale.
    graph.add_node("initiate", initiate_node)
    graph.add_node("setup", setup_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("planning", planning_node)
    graph.add_node("checklist_creation", checklist_creation_node)
    graph.add_node("implementation", implementation_node)
    graph.add_node("implementation_review", implementation_review_node)
    graph.add_node("verification", verification_node)
    graph.add_node("commit", commit_node)
    graph.add_node("pull_request", pull_request_node)
    graph.add_node("completion", completion_node)
    graph.add_node("error_handler", error_handler_node)

    # -- entry point ---------------------------------------------------------
    graph.set_entry_point("initiate")

    # -- edges ---------------------------------------------------------------
    graph.add_conditional_edges(
        "initiate",
        route_after_initiate,
        {"setup": "setup", "error_handler": "error_handler"},
    )
    graph.add_conditional_edges(
        "setup",
        route_after_setup,
        {"retrieve": "retrieve", "error_handler": "error_handler"},
    )
    graph.add_conditional_edges(
        "retrieve",
        route_after_retrieve,
        {"planning": "planning", "error_handler": "error_handler"},
    )
    graph.add_conditional_edges(
        "planning",
        route_after_plan,
        {"checklist_creation": "checklist_creation", "error_handler": "error_handler"},
    )
    graph.add_conditional_edges(
        "checklist_creation",
        route_after_checklist_creation,
        {"implementation": "implementation", "error_handler": "error_handler"},
    )
    graph.add_conditional_edges(
        "implementation",
        route_after_implementation,
        {"implementation_review": "implementation_review", "error_handler": "error_handler"},
    )
    graph.add_conditional_edges(
        "implementation_review",
        route_after_implementation_review,
        {"verification": "verification", "error_handler": "error_handler"},
    )
    graph.add_conditional_edges(
        "verification",
        route_after_verify,
        {"commit": "commit", "implementation": "implementation", "error_handler": "error_handler"},
    )
    graph.add_conditional_edges(
        "commit",
        route_after_commit,
        {"pull_request": "pull_request", "error_handler": "error_handler"},
    )
    graph.add_conditional_edges(
        "pull_request",
        route_after_pull_request,
        {"completion": "completion", "error_handler": "error_handler"},
    )
    graph.add_edge("completion", END)
    graph.add_edge("error_handler", END)

    return graph.compile(checkpointer=checkpointer)
