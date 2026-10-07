"""Mimic exactly what a model sees when a tool is called.

Usage:
    Update the test name at the bottom in `if __name__` and run this file.

Provides `run_tool()` which takes a tool name and args dict (exactly as a model
would produce them) and returns the exact dict the model receives back — the
output of `ToolResult.to_tool_result_content()`.

To add a new tool test, write a function that calls `run_tool()` with the
args the model would send.
"""

from __future__ import annotations

import asyncio
import json
import time
from typing import Any

import rich
from matrx_utils import cleanup_async_resources, clear_terminal, vcprint

from matrx_ai._ext import get_ext
from matrx_ai.config.usage_config import TokenUsage, _get_db_pricing_lookup
from matrx_ai.tools.models import ToolContext, ToolResult

create_test_execution_context = get_ext("create_test_execution_context")
create_test_tool_context = get_ext("create_test_tool_context")
initialize = get_ext("initialize")

initialize()
_ctx_token = create_test_execution_context(is_admin=False)


COST_COMPARISON_MODELS = [
    ("Small", "gemini-3-flash-preview", "google"),
    ("Medium", "gpt-5.2", "openai"),
    ("Large", "claude-opus-4", "anthropic"),
]

CHARS_PER_TOKEN = 4


def _estimate_cost_table(content: str) -> None:
    char_count = len(content)
    estimated_tokens = max(1, char_count // CHARS_PER_TOKEN)

    print()
    print("=" * 80)
    print("INPUT TOKEN COST ESTIMATE (tool result as input to next model turn)")
    print("=" * 80)
    print(f"  Content length:    {char_count:>10,} chars")
    print(f"  Estimated tokens:  {estimated_tokens:>10,} tokens  (~{CHARS_PER_TOKEN} chars/token)")
    print()
    print(f"  {'Model':<14} {'Tier':<8} {'$/M Input':>12} {'Est. Cost':>24}")
    print(f"  {'─' * 14} {'─' * 8} {'─' * 12} {'─' * 24}")

    _pricing_lookup = _get_db_pricing_lookup()
    for label, model_name, api in COST_COMPARISON_MODELS:
        pricing = _pricing_lookup.get(model_name)
        if not pricing:
            print(f"  {label:<14} {'—':<8} {'N/A':>12} {'N/A':>24}")
            continue

        usage = TokenUsage(
            input_tokens=estimated_tokens,
            output_tokens=0,
            cached_input_tokens=0,
            matrx_model_name=model_name,
            provider_model_name=model_name,
            api=api,
        )
        cost = usage.calculate_cost()
        tier = pricing.get_tier(estimated_tokens)
        price_per_m = tier.input_price if tier else 0

        cost_cents = cost * 100 if cost is not None else None
        cost_str = f"${cost:.6f} ({cost_cents:.2f}¢)" if cost is not None else "N/A"
        print(f"  {label:<14} {price_per_m:>7.2f} {'$/M':>5} {cost_str:>24}")

    print("=" * 80)


def _build_ctx(tool_name: str, stream: bool = True) -> ToolContext:
    return create_test_tool_context(tool_name)


def _get_tool_map() -> dict[str, Any]:
    from matrx_ai.tools.implementations import (
        code_execute_python,
        code_fetch_code,
        code_fetch_tree,
        # Code
        code_store_html,
        db_insert,
        # Database
        db_query,
        db_schema,
        db_update,
        fs_list,
        fs_mkdir,
        # Filesystem
        fs_read,
        fs_search,
        fs_write,
        # Interaction
        interaction_ask,
        # Math
        math_calculate,
        memory_forget,
        memory_recall,
        memory_search,
        # Memory
        memory_store,
        memory_update,
        # News
        news_get_headlines,
        # Research
        research_web,
        seo_check_meta_descriptions,
        seo_check_meta_tags_batch,
        # SEO
        seo_check_meta_titles,
        seo_get_keyword_data,
        # Shell
        shell_execute,
        shell_python,
        # Text
        text_analyze,
        text_regex_extract,
        travel_create_summary,
        travel_get_activities,
        travel_get_events,
        # Travel
        travel_get_location,
        travel_get_restaurants,
        travel_get_weather,
        web_read,
        # Web
        web_search,
    )

    from matrx_ai.tools.implementations.pick_list_tools import pick_list

    return {
        "math_calculate": math_calculate,
        "text_analyze": text_analyze,
        "text_regex_extract": text_regex_extract,
        "web_search": web_search,
        "web_read": web_read,
        "research_web": research_web,
        "db_query": db_query,
        "db_insert": db_insert,
        "db_update": db_update,
        "db_schema": db_schema,
        "memory_store": memory_store,
        "memory_recall": memory_recall,
        "memory_search": memory_search,
        "memory_update": memory_update,
        "memory_forget": memory_forget,
        "fs_read": fs_read,
        "fs_write": fs_write,
        "fs_list": fs_list,
        "fs_search": fs_search,
        "fs_mkdir": fs_mkdir,
        "shell_execute": shell_execute,
        "shell_python": shell_python,
        "pick_list": pick_list,
        "seo_check_meta_titles": seo_check_meta_titles,
        "seo_check_meta_descriptions": seo_check_meta_descriptions,
        "seo_check_meta_tags_batch": seo_check_meta_tags_batch,
        "seo_get_keyword_data": seo_get_keyword_data,
        "code_store_html": code_store_html,
        "code_fetch_code": code_fetch_code,
        "code_fetch_tree": code_fetch_tree,
        "code_execute_python": code_execute_python,
        "news_get_headlines": news_get_headlines,
        "interaction_ask": interaction_ask,
        "travel_get_location": travel_get_location,
        "travel_get_weather": travel_get_weather,
        "travel_get_restaurants": travel_get_restaurants,
        "travel_get_activities": travel_get_activities,
        "travel_get_events": travel_get_events,
        "travel_create_summary": travel_create_summary,
    }


_YELLOW = "\033[93m"
_CYAN = "\033[96m"
_RESET = "\033[0m"
_GREEN = "\033[92m"
_RED = "\033[91m"


def _yline(char: str = "═", width: int = 80) -> str:
    return f"{_YELLOW}{char * width}{_RESET}"


def _cline(char: str = "═", width: int = 80) -> str:
    return f"{_CYAN}{char * width}{_RESET}"


def _rline(char: str = "═", width: int = 80) -> str:
    return f"{_RED}{char * width}{_RESET}"


def _gline(char: str = "═", width: int = 80) -> str:
    return f"{_GREEN}{char * width}{_RESET}"


async def run_tool(
    tool_name: str,
    args: dict[str, Any],
    *,
    stream: bool = True,
    print_result: bool = True,
    use_db: bool | None = None,
) -> dict[str, Any]:
    """Execute a tool exactly as the executor would and return the model-facing result."""

    tool_map = _get_tool_map()
    func = tool_map.get(tool_name)
    if func is None:
        raise ValueError(
            f"Tool '{tool_name}' not in TOOL_MAP. Available: {sorted(tool_map.keys())}"
        )

    ctx = _build_ctx(tool_name, stream=stream)

    print()
    print(_yline("═"))
    print(f"{_YELLOW}  TOOL: {tool_name}")
    print(f"{_YELLOW}  ARGS (what the model sends):{_RESET}")
    vcprint(args, title="ARGS", color="yellow")
    print(_yline("═"))

    start = time.perf_counter()
    result: ToolResult = await func(args, ctx)
    elapsed = time.perf_counter() - start

    model_facing = result.to_tool_result_content()

    if print_result:
        print()
        print(_cline("─"))
        print(f"MODEL RECEIVES (to_tool_result_content):{_RESET}")
        print(_cline("─"))
        rich.print(model_facing)
        print()

        print(_cline("─", 80))
        print(f"CONTENT (the actual string the model reads):{_RESET}")
        print(_cline("─", 80))
        content = model_facing.get("content", "")
        if isinstance(content, str):
            try:
                parsed = json.loads(content)
                rich.print(parsed)
            except (json.JSONDecodeError, TypeError):
                print(content[:3000])
                if len(content) > 3000:
                    print(f"\n... [{len(content):,} chars total, truncated for display]")
        else:
            rich.print(content)

        print()
        print(_cline("─"))

        if result.success:
            vcprint(f"  SUCCESS: {result.success}", color="green")
        else:
            vcprint(f"  SUCCESS: {result.success}", color="red")

        is_error = model_facing.get("is_error", False)
        if is_error:
            vcprint(f"  IS_ERROR: {is_error}", color="red")
        else:
            vcprint(f"  IS_ERROR: {is_error}", color="green")
        print(f"  DURATION: {elapsed:.2f}s (result.duration_ms={result.duration_ms}ms)")
        if result.usage:
            print(f"  USAGE: {result.usage}")
        if result.child_usages:
            print(f"  CHILD USAGES: {result.child_usages}")
        print(_cline("═"))
        print()
        print()
        print()
        print()
        print()

        content_for_cost = model_facing.get("content", "")
        if isinstance(content_for_cost, str) and content_for_cost:
            _estimate_cost_table(content_for_cost)

        if result.success:
            print()
            print()
            print(_gline("═"))

            vcprint(f"  TOOL NAME: {tool_name}", color="green")
            vcprint(f"  SUCCESS: {result.success}", color="green")
            print(_gline("═"))
        else:
            print()
            print()
            print(_rline("═"))
            vcprint(f"  TOOL NAME: {tool_name}", color="red")
            vcprint(f"  SUCCESS: {result.success}", color="red")
            print(_rline("═"))

    return model_facing


# ============================================================================
# MATH
# ============================================================================


async def test_math_calculate():
    return await run_tool(
        "math_calculate",
        {
            "expression": "(12 * 8) + (45 / 3) - 7",
        },
    )


# ============================================================================
# TEXT
# ============================================================================


async def test_text_analyze():
    return await run_tool(
        "text_analyze",
        {
            "text": "The quick brown fox jumps over the lazy dog. This is a sample text for analysis. It contains multiple sentences and various words.",
            "analysis_type": "summary",
        },
    )


async def test_text_regex_extract():
    return await run_tool(
        "text_regex_extract",
        {
            "text": "Contact us at support@example.com or sales@company.org for more info.",
            "pattern": r"[\w.+-]+@[\w-]+\.[\w.-]+",
            "find_all": True,
        },
    )


# ============================================================================
# WEB
# ============================================================================


async def test_web_search():
    return await run_tool(
        "web_search",
        {
            "queries": ["Python 3.13 new features"],
            "max_results_per_query": 3,
        },
    )


async def test_web_read():
    return await run_tool(
        "web_read",
        {
            "urls": ["https://docs.python.org/3/whatsnew/3.13.html"],
            "max_content_length": 5000,
        },
    )


async def test_research_web():
    return await run_tool(
        "research_web",
        {
            "queries": ["latest AI developments 2026", "LLM benchmarks 2026"],
            "instructions": "Focus on practical breakthroughs that affect software developers. Include specific model names and capabilities.",
            "research_depth": "shallow",
        },
    )


# ============================================================================
# DATABASE
# ============================================================================


async def test_db_query():
    return await run_tool(
        "db_query",
        {
            "query": "SELECT id, name FROM tool.definition WHERE is_active = true LIMIT 5",
        },
    )


async def test_db_schema():
    return await run_tool(
        "db_schema",
        {
            "table": "tool.definition",
        },
    )


# ============================================================================
# MEMORY
# ============================================================================


async def test_memory_store():
    return await run_tool(
        "memory_store",
        {
            "key": "test_preference",
            "content": "User prefers dark mode and concise responses.",
            "memory_type": "long",
            "scope": "user",
            "importance": 0.7,
        },
    )


async def test_memory_recall():
    return await run_tool(
        "memory_recall",
        {
            "query": "user preferences",
            "scope": "user",
            "limit": 5,
        },
    )


async def test_memory_search():
    return await run_tool(
        "memory_search",
        {
            "query": "dark mode",
            "scope": "user",
            "limit": 5,
        },
    )


# ============================================================================
# FILESYSTEM
# ============================================================================


async def test_fs_write_then_read():
    await run_tool(
        "fs_write",
        {
            "path": "test_file.txt",
            "content": "Hello from fs_write test!\nLine 2.",
            "create_dirs": True,
        },
    )
    return await run_tool(
        "fs_read",
        {
            "path": "test_file.txt",
        },
    )


async def test_fs_list():
    return await run_tool(
        "fs_list",
        {
            "path": ".",
            "recursive": False,
        },
    )


async def test_fs_search():
    return await run_tool(
        "fs_search",
        {
            "pattern": "*.txt",
            "path": ".",
            "max_results": 20,
        },
    )


# ============================================================================
# SHELL
# ============================================================================


async def test_shell_execute():
    return await run_tool(
        "shell_execute",
        {
            "command": "echo 'Hello from shell test' && date",
            "timeout_seconds": 10,
        },
    )


async def test_shell_python():
    return await run_tool(
        "shell_python",
        {
            "code": "import sys; print(f'Python {sys.version}')\nprint(2 + 2)",
            "timeout_seconds": 10,
        },
    )


# ============================================================================
# USER LISTS
# ============================================================================


# ============================================================================
# PICK LISTS (one tool: pick_list, with actions)
# ============================================================================


async def test_pick_list_list():
    return await run_tool("pick_list", {"action": "list", "page": 1, "page_size": 10})


async def test_pick_list_get():
    lists = await run_tool("pick_list", {"action": "list", "page": 1, "page_size": 1}, print_result=False)
    out = getattr(lists, "output", None) or {}
    rows = out.get("lists") or out.get("items") or []
    if not rows:
        print("  [skip] No pick lists found — run test_pick_list_create first.")
        return lists
    return await run_tool("pick_list", {"action": "get", "pick_list_id": rows[0]["id"]})


async def test_pick_list_create():
    return await run_tool(
        "pick_list",
        {
            "action": "create",
            "pick_list_name": "Tech Stack Choices",
            "description": "Backend technology options",
            "items": [
                {"label": "FastAPI", "help_text": "Python async web framework", "group_name": "Python"},
                {"label": "Django", "help_text": "Full-featured Python framework", "group_name": "Python"},
                {"label": "Express", "help_text": "Node.js web framework", "group_name": "JavaScript"},
            ],
        },
    )


async def test_pick_list_update_item():
    return await run_tool(
        "pick_list",
        {
            "action": "update_item",
            "item_id": "00000000-0000-0000-0000-000000000000",
            "label": "Updated Label",
            "help_text": "Updated via test_pick_list_update_item",
        },
    )


async def test_pick_list_batch_update():
    return await run_tool(
        "pick_list",
        {
            "action": "batch_update",
            "pick_list_id": "00000000-0000-0000-0000-000000000000",
            "items": [
                {"id": "00000000-0000-0000-0000-000000000001", "label": "Item A Updated"},
                {"id": "00000000-0000-0000-0000-000000000002", "label": "Item B Updated"},
            ],
        },
    )


# ============================================================================
# SEO
# ============================================================================


async def test_seo_check_meta_titles():
    return await run_tool(
        "seo_check_meta_titles",
        {
            "titles": [
                # Good: within 15-60 chars, under 600px desktop / 500px mobile
                "Best Python Frameworks 2026 - Complete Guide",
                # Bad: too short (1 char) — should fail seo_length_ok and title_ok
                "A",
                # Bad: too short (8 chars) — below 15-char minimum
                "Short",
                # Bad: too long — exceeds 60 chars and pixel limits
                "This is an extremely long title that probably exceeds the recommended character limit for search engine optimization and will get truncated in search results pages",
                # Edge: exactly at 60 chars but all wide 'A' — passes char limit, fails pixel limits
                "A" * 60,
                # Edge: 61 chars — fails both char limit and pixel limits
                "A" * 61,
            ],
        },
    )


async def test_seo_check_meta_descriptions():
    return await run_tool(
        "seo_check_meta_descriptions",
        {
            "descriptions": [
                # Good: ~99 chars / ~608px — passes both desktop (920px) and mobile (680px) limits
                "Learn about the best Python frameworks in 2026. Compare FastAPI, Django, and Flask with benchmarks.",
                # Bad: too short (6 chars) — below 70-char minimum, should fail
                "Short.",
                # Bad: too long — exceeds 160 chars
                "This is an extremely long meta description that goes well beyond the recommended one hundred and sixty character limit for SEO optimization purposes and will likely be truncated by Google in search results.",
                # Edge: mobile truncation risk — under 160 chars but may exceed 680px mobile limit
                "Explore the top Python web frameworks in 2026 including FastAPI, Django, Flask, and Tornado with extensive benchmarks, real-world production comparisons, and migration guides.",
            ],
        },
    )


# ============================================================================
# CODE
# ============================================================================


async def test_code_store_html():
    return await run_tool(
        "code_store_html",
        {
            "html_input": "<html><body><h1>Test Page</h1><p>Hello world</p></body></html>",
        },
    )


async def test_code_fetch_code():
    return await run_tool(
        "code_fetch_code",
        {
            "project_root": "/home/arman/projects/aidream",
            "subdirectory": "ai/tool_system/implementations",
            "output_mode": "clean",
        },
    )


async def test_code_fetch_tree():
    return await run_tool(
        "code_fetch_tree",
        {
            "project_root": "/home/arman/projects/aidream",
            "subdirectory": "ai/tool_system",
            "show_all_directories": True,
        },
    )


# ============================================================================
# NEWS
# ============================================================================


async def test_news_get_headlines():
    return await run_tool(
        "news_get_headlines",
        {
            "country": "us",
            "category": "technology",
            "language": "en",
        },
    )


# ============================================================================
# USER TABLES (legacy)
# ============================================================================


# ============================================================================
# PERSONAL TABLES
# ============================================================================


# ============================================================================
# QUESTIONNAIRE
# ============================================================================


async def test_interaction_ask():
    return await run_tool(
        "interaction_ask",
        {
            "introduction": "Help me understand your project requirements:",
            "questions": [
                {
                    "id": "framework",
                    "prompt": "Which framework do you prefer?",
                    "component_type": "dropdown",
                    "options": ["FastAPI", "Django", "Flask", "Express"],
                },
                {
                    "id": "scale",
                    "prompt": "How important is performance?",
                    "component_type": "slider",
                },
            ],
        },
    )


# ============================================================================
# TRAVEL
# ============================================================================


async def test_travel_get_location():
    return await run_tool("travel_get_location", {})


async def test_travel_get_weather():
    return await run_tool(
        "travel_get_weather",
        {
            "city": "San Francisco",
        },
    )


async def test_travel_get_restaurants():
    return await run_tool(
        "travel_get_restaurants",
        {
            "city": "San Francisco",
        },
    )


async def test_travel_get_activities():
    return await run_tool(
        "travel_get_activities",
        {
            "city": "San Francisco",
            "weather": "sunny",
        },
    )


async def test_travel_get_events():
    return await run_tool(
        "travel_get_events",
        {
            "city": "San Francisco",
            "weather": "sunny",
        },
    )


async def test_travel_create_summary():
    return await run_tool(
        "travel_create_summary",
        {
            "location": "San Francisco",
            "weather_info": {"condition": "sunny", "temp": 68},
            "restaurants": [{"name": "House of Prime Rib", "cuisine": "American"}],
            "activities": [{"name": "Golden Gate Bridge Walk", "type": "outdoor"}],
            "events": [{"name": "Outside Lands", "type": "music festival"}],
        },
    )


# ============================================================================
# DATABASE (write operations)
# ============================================================================


async def test_db_insert():
    return await run_tool(
        "db_insert",
        {
            "table": "notes",
            "data": {
                "label": "Test note",
                "content": "This is a test insertion from mimic_model_tests.",
            },
        },
    )


async def test_db_update():
    return await run_tool(
        "db_update",
        {
            "table": "notes",
            "data": {"content": "Updated content from test_db_update."},
            "match": {"label": "Test note"},
        },
    )


# ============================================================================
# MEMORY (additional operations)
# ============================================================================


async def test_memory_update():
    return await run_tool(
        "memory_update",
        {
            "key": "test_preference",
            "content": "User now prefers light mode and detailed responses.",
            "scope": "user",
            "importance": 0.8,
        },
    )


async def test_memory_forget():
    return await run_tool(
        "memory_forget",
        {
            "key": "test_preference",
            "scope": "user",
        },
    )


# ============================================================================
# FILESYSTEM (additional operations)
# ============================================================================


async def test_fs_mkdir():
    return await run_tool(
        "fs_mkdir",
        {
            "path": "test_subdir/nested",
            "parents": True,
        },
    )
# ============================================================================
# SEO (additional operations)
# ============================================================================


async def test_seo_check_meta_tags_batch():
    return await run_tool(
        "seo_check_meta_tags_batch",
        {
            "meta_data": [
                {
                    # Good title and good description
                    "title": "Best Python Frameworks 2026 - Complete Developer Guide",
                    "description": "Explore the top Python web frameworks in 2026 including FastAPI, Django, and Flask with detailed benchmarks and real-world production comparisons.",
                },
                {
                    # Both too short — should surface issues on both
                    "title": "A",
                    "description": "Too short.",
                },
                {
                    # Title too long, description at the mobile truncation boundary
                    "title": "This Is An Extremely Long Meta Title That Definitely Exceeds Sixty Characters And Should Fail",
                    "description": "Explore the top Python web frameworks in 2026 including FastAPI, Django, Flask, and Tornado with extensive benchmarks, real-world production comparisons, and migration guides.",
                },
            ],
        },
    )


async def test_seo_get_keyword_data():
    return await run_tool(
        "seo_get_keyword_data",
        {
            "keywords": ["python fastapi", "web framework python"],
            "date_from": "2025-01-01",
            "date_to": "2025-12-31",
            "location_code": 2840,
            "language_code": "en",
            "sort_by": "search_volume",
        },
    )


# ============================================================================
# CODE
# ============================================================================


async def test_code_execute_python():
    return await run_tool(
        "code_execute_python",
        {
            "code_input": "import sys\nprint(f'Python {sys.version}')\nresult = sum(range(1, 101))\nprint(f'Sum 1-100 = {result}')",
            "timeout_seconds": 15,
        },
    )


async def test_code_execute_python_with_markers():
    return await run_tool(
        "code_execute_python",
        {
            "code_input": "```python\nimport math\nprint(f'Pi = {math.pi:.6f}')\nprint(f'sqrt(2) = {math.sqrt(2):.6f}')\n```",
            "timeout_seconds": 15,
        },
    )


# ============================================================================
# USER LISTS (additional operations)
# ============================================================================


# ============================================================================
# ALL AVAILABLE TESTS
# ============================================================================
#
#   Math:       test_math_calculate
#   Text:       test_text_analyze, test_text_regex_extract
#   Web:        test_web_search, test_web_read
#   Research:   test_research_web
#   Database:   test_db_query, test_db_insert, test_db_update, test_db_schema
#   Memory:     test_memory_store, test_memory_recall, test_memory_search,
#               test_memory_update, test_memory_forget
#   Filesystem: test_fs_write_then_read, test_fs_list, test_fs_search, test_fs_mkdir
#   Shell:      test_shell_execute, test_shell_python
#   Pick Lists: test_pick_list_list, test_pick_list_get, test_pick_list_create,
#               test_pick_list_update_item, test_pick_list_batch_update
#   SEO:        test_seo_check_meta_titles, test_seo_check_meta_descriptions,
#               test_seo_check_meta_tags_batch, test_seo_get_keyword_data
#   Code:       test_code_store_html, test_code_fetch_code, test_code_fetch_tree,
#               test_code_execute_python, test_code_execute_python_with_markers
#   News:       test_news_get_headlines
#   Interaction:test_interaction_ask
#   Travel:     test_travel_get_location, test_travel_get_weather,
#               test_travel_get_restaurants, test_travel_get_activities,
#               test_travel_get_events, test_travel_create_summary
#
# ============================================================================


ALL_TESTS: list[tuple[str, str, Any]] = [
    # (number_label, display_name, coroutine_function)
    ("1", "math_calculate             [Math]", test_math_calculate),
    ("2", "text_analyze               [Text]", test_text_analyze),
    ("3", "text_regex_extract         [Text]", test_text_regex_extract),
    ("4", "web_search                 [Web]", test_web_search),
    ("5", "web_read                   [Web]", test_web_read),
    ("6", "research_web               [Research]", test_research_web),
    ("7", "db_query                   [Database]", test_db_query),
    ("8", "db_insert                  [Database]", test_db_insert),
    ("9", "db_update                  [Database]", test_db_update),
    ("10", "db_schema                  [Database]", test_db_schema),
    ("11", "memory_store               [Memory]", test_memory_store),
    ("12", "memory_recall              [Memory]", test_memory_recall),
    ("13", "memory_search              [Memory]", test_memory_search),
    ("14", "memory_update              [Memory]", test_memory_update),
    ("15", "memory_forget              [Memory]", test_memory_forget),
    ("16", "fs_write_then_read         [Filesystem]", test_fs_write_then_read),
    ("17", "fs_list                    [Filesystem]", test_fs_list),
    ("18", "fs_search                  [Filesystem]", test_fs_search),
    ("19", "fs_mkdir                   [Filesystem]", test_fs_mkdir),
    ("20", "shell_execute              [Shell]", test_shell_execute),
    ("21", "shell_python               [Shell]", test_shell_python),
    # 22-26 were the legacy in-package browser_* tools — deleted; the
    # cloud_browser_* tools live in aidream/services/cloud_browser and are
    # covered by aidream/services/cloud_browser/tests.
    ("27", "pick_list list            [Pick Lists]", test_pick_list_list),
    ("27b", "pick_list get            [Pick Lists]", test_pick_list_get),
    ("27c", "pick_list create         [Pick Lists]", test_pick_list_create),
    ("27d", "pick_list update_item    [Pick Lists]", test_pick_list_update_item),
    ("27e", "pick_list batch_update   [Pick Lists]", test_pick_list_batch_update),
    ("33", "seo_check_meta_titles      [SEO]", test_seo_check_meta_titles),
    ("34", "seo_check_meta_descriptions[SEO]", test_seo_check_meta_descriptions),
    ("35", "seo_check_meta_tags_batch  [SEO]", test_seo_check_meta_tags_batch),
    ("36", "seo_get_keyword_data       [SEO]", test_seo_get_keyword_data),
    ("37", "code_store_html            [Code]", test_code_store_html),
    ("38", "code_fetch_code            [Code]", test_code_fetch_code),
    ("39", "code_fetch_tree            [Code]", test_code_fetch_tree),
    ("40", "code_execute_python        [Code]", test_code_execute_python),
    ("41", "code_execute_python_markers[Code]", test_code_execute_python_with_markers),
    ("42", "news_get_headlines         [News]", test_news_get_headlines),
    ("53", "interaction_ask            [Interaction]", test_interaction_ask),
    ("54", "travel_get_location        [Travel]", test_travel_get_location),
    ("55", "travel_get_weather         [Travel]", test_travel_get_weather),
    ("56", "travel_get_restaurants     [Travel]", test_travel_get_restaurants),
    ("57", "travel_get_activities      [Travel]", test_travel_get_activities),
    ("58", "travel_get_events          [Travel]", test_travel_get_events),
    ("59", "travel_create_summary      [Travel]", test_travel_create_summary),
]


async def _run_interactive() -> None:
    total = len(ALL_TESTS)

    clear_terminal()
    print("=" * 70)
    print(f"  TOOL TEST RUNNER  —  {total} tests available")
    print("=" * 70)
    print()
    for num, name, _ in ALL_TESTS:
        print(f"  {num:>3}.  {name}")
    print()

    while True:
        raw = input(f"Start at which number? [1–{total}]: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= total:
            start_idx = int(raw) - 1
            break
        print(f"  Please enter a number between 1 and {total}.")

    subset = ALL_TESTS[start_idx:]

    for num, name, fn in subset:
        print()
        print("─" * 70)
        print(f"  TEST {num}/{total}:  {name.strip()}")
        print("─" * 70)

        while True:
            choice = input("  Run (r) / Skip (s) / Exit (e): ").strip().lower()
            if choice in ("r", "run", "y", "yes", ""):
                await fn()
                break
            elif choice in ("s", "skip", "n", "no"):
                print("  → Skipped.")
                break
            elif choice in ("e", "exit", "q", "quit"):
                print("\n  Exiting test runner. Goodbye!\n")
                return
            else:
                print("  Invalid input. Enter r (run), s (skip), or e (exit).")

    print()
    print("=" * 70)
    print("  All tests complete!")
    print("=" * 70)
    print()


def _verify_tool_map_alignment() -> None:
    """Assert that _get_tool_map() keys exactly match implementations.__all__."""
    from matrx_ai.tools import implementations

    tool_map = _get_tool_map()
    expected = set(implementations.__all__)
    actual = set(tool_map.keys())
    missing = expected - actual
    extra = actual - expected
    if missing or extra:
        msg = []
        if missing:
            msg.append(f"Missing in tool_map: {sorted(missing)}")
        if extra:
            msg.append(f"Extra in tool_map: {sorted(extra)}")
        raise AssertionError("Tool map mismatch with implementations.__all__: " + "; ".join(msg))


if __name__ == "__main__":
    clear_terminal()
    _verify_tool_map_alignment()
    asyncio.run(_run_interactive())
    cleanup_async_resources()
