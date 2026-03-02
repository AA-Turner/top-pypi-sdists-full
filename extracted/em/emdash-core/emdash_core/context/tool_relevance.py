"""Tool relevance scores for context ranking.

This module defines how much relevance weight each tool type contributes
when an entity is discovered through that tool during exploration.

Scoring Philosophy:
- Highest: Actions that modify code (write_file, apply_diff) - these are
  what the agent is actively working on
- High: Deliberate investigation (expand_node, get_callers, read_file)
- Medium: Targeted search (semantic_search, text_search, grep)
- Low: Broad discovery (list_files, graph algorithms)
"""

# Tool-based relevance scores
# These scores become the base_score for ContextItems
TOOL_RELEVANCE = {
    # Highest relevance - active modifications (what we're working on NOW)
    "write_to_file": 1.0,
    "apply_diff": 1.0,
    "execute_command": 0.9,  # Often running tests/builds on specific files

    # High relevance - deliberate investigation
    "get_callers": 0.9,
    "get_callees": 0.9,
    "get_class_hierarchy": 0.85,
    "get_impact_analysis": 0.85,
    "read_file": 0.8,
    "get_neighbors": 0.8,

    # Medium-high relevance
    "expand_node": 0.6,

    # Medium relevance - targeted search
    "semantic_search": 0.7,
    "text_search": 0.65,
    "grep": 0.6,
    "get_file_dependencies": 0.6,
    "find_entity": 0.55,

    # Lower relevance - broad discovery
    "list_files": 0.3,
    "glob": 0.3,

    # Lowest relevance - graph algorithms (bulk results, less targeted)
    "get_top_pagerank": 0.2,
    "get_communities": 0.2,
    "get_central_nodes": 0.2,
}

# Default score for unknown tools
DEFAULT_TOOL_RELEVANCE = 0.3

# Tools where only top N results are considered highly relevant
SEARCH_TOOLS = {"semantic_search", "text_search", "grep", "find_entity"}

# How many top results from search tools get full relevance score
TOP_RESULTS_LIMIT = 3

# Score multiplier for non-top search results
NON_TOP_RESULT_MULTIPLIER = 0.5


def get_tool_relevance(tool_name: str) -> float:
    """Get the relevance score for a tool.

    Args:
        tool_name: Name of the tool

    Returns:
        Relevance score between 0.0 and 1.0
    """
    return TOOL_RELEVANCE.get(tool_name, DEFAULT_TOOL_RELEVANCE)


def is_search_tool(tool_name: str) -> bool:
    """Check if a tool is a search tool (where only top results are relevant).

    Args:
        tool_name: Name of the tool

    Returns:
        True if it's a search tool
    """
    return tool_name in SEARCH_TOOLS
