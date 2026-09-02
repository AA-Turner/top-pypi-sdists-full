from matrx_scraper.search import wrapped_brave_search

try:
    from matrx_connect import Emitter
except ImportError:
    from typing import Any

    Emitter = Any

LOCAL_DEBUG = False


async def search_web_mcp_quick(
    queries: list[str],
    freshness: str = None,
    count: int = 10,
    emitter: Emitter = None,
    call_id: str = None,
) -> dict:
    """
    MCP tool wrapper for web search that adds AI agent guidance.

    Uses the core wrapped_brave_search function for all search logic,
    then appends agent-specific instructions for next steps.
    """
    search_result = await wrapped_brave_search(
        queries=queries,
        freshness=freshness,
        count=count,
        extra_snippets=True,
        emitter=emitter,
        call_id=call_id,
    )

    formatted_results = search_result["unique_text_summary"]

    agent_guidance = """
---
Next steps:
Assess if this context answers the user's query. If gaps remain or deeper detail is needed, take action:
- Use `web_read` to get complete content from any of the URLs shown in the search results above
- Use `web_read` on any specific URLs the user mentioned that seem relevant
- Try `web_search` with different or more specific terms if these results miss the mark

If the context above sufficiently answers the query, respond directly to the user."""

    final_text_content = formatted_results + agent_guidance

    return {"status": "success", "result": final_text_content}
