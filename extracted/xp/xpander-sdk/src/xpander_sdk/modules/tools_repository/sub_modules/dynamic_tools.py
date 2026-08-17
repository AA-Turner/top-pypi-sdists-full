"""Dynamic tools: progressive tool disclosure for agents.

When ``agent.use_dynamic_tools`` is True *and* the agent has at least
``XPANDER_DYNAMIC_TOOLS_MIN_TOOLS`` (default 50) hideable tools, the agent's
full tool catalog is NOT loaded into the LLM context. Instead the agent gets
four small meta-tools that let it discover/inspect/run the hidden tools on
demand, plus an inline catalog hint in its instructions. This keeps the context
window lean — only the tools a given task actually needs end up fully loaded.
Below the threshold the whole catalog is cheaper to load than to search, so it
is attached directly; ``dynamic_tools_active`` is the single answer every
call site asks.

The four meta-tools (all ``xp_``-prefixed so they survive the always-loaded
filter and the context-optimizer ``startswith("xp")`` skip):

- ``xp_list_tools``   — paginated browse of the hidden catalog (names + desc).
- ``xp_search_tools`` — keyword ranking over the hidden catalog by intent.
- ``xp_get_tool``     — full schema + example for one hidden tool.
- ``xp_execute_tool`` — run a hidden tool by name with its arguments.

The three read-only meta-tools report their own activity — reaching a tool takes
three calls and the user should see all of them — and carry reasoning headers so
each row has a title. ``xp_execute_tool`` stays silent: the real tool it
dispatches reports itself, so reporting the wrapper would double up.

Everything model-facing here is written for agent readability: XML-style blocks
(consistent with the repo's existing prompt blocks) with ``<when>``/``<then>``
hints and concrete examples.
"""

import json
import os
import re
import uuid
from inspect import Parameter, Signature
from typing import Any, Callable, Dict, List, Optional, Union

from loguru import logger
from pydantic import BaseModel, Field, model_validator

from xpander_sdk.modules.tools_repository.utils.result_offload import (
    MIN_SAVE_CHARS,
    append_inline_notice,
    build_saved_result_pointer,
    save_result_to_workspace,
    serialize_tool_result,
)
from xpander_sdk.modules.tools_repository.utils.workspace_payload import (
    WorkspacePayloadError,
    has_workspace_path,
    resolve_workspace_payload,
)
from xpander_sdk.utils.agno_tool_resolution import register_dynamic_tools_repo
from xpander_sdk.utils.cache import cached_tool_json_schema
from xpander_sdk.utils.event_loop import run_sync

# --- Constants -------------------------------------------------------------- #

# Tool name prefixes that are NEVER hidden (workspace, schedule, compaction,
# MCP, and the meta-tools themselves all start with one of these).
DYNAMIC_TOOL_PREFIXES = ("xp", "mcp")

# Minimum hideable-tool count before dynamic mode engages. Below it the agent's
# flag alone is not enough: a small catalog costs less in context than the
# search/get/execute round-trips it would take to reach it.
DYNAMIC_TOOLS_MIN_TOOLS_ENV = "XPANDER_DYNAMIC_TOOLS_MIN_TOOLS"
DYNAMIC_TOOLS_MIN_TOOLS_DEFAULT = 50

# Max chars for a truncated catalog description.
TRUNCATED_DESC_LEN = 140

# Pagination / result-size limits.
DEFAULT_LIST_LIMIT = 30
DEFAULT_SEARCH_LIMIT = 7
MAX_PAGE_LIMIT = 100

# A search returning at most this many tools inlines their schemas, so the model
# can execute straight from the search result instead of paying a second
# round-trip per tool. Above it results stay summarized.
AUTO_FULL_SEARCH_RESULTS = 3

# Schemas one xp_get_tool call will read. Bounds the context a single call can
# pull in; a task needing more than this is browsing, not preparing a call.
MAX_SCHEMAS_PER_GET = 10

# Max hidden tools listed inline in the instruction hint before pointing the
# model at xp_list_tools for the rest.
HINT_CATALOG_CAP = 60

META_TOOL_NAMES = (
    "xp_list_tools",
    "xp_search_tools",
    "xp_get_tool",
    "xp_execute_tool",
)


# --- Filtering helpers ------------------------------------------------------ #


def is_always_loaded(tool: Any) -> bool:
    """Return True if the tool must stay fully loaded (never hidden)."""
    # MCP proxies carry an "mcp_tool_*" id but ARE the thing we hide behind the
    # meta-tools, so they must never count as always-loaded (unlike repo.list
    # tools whose "mcp"/"xp" prefix genuinely means always-loaded).
    if getattr(tool, "is_mcp_proxy", False):
        return False
    tid = tool.id or ""
    tname = tool.name or ""
    return tid.startswith(DYNAMIC_TOOL_PREFIXES) or tname.startswith(
        DYNAMIC_TOOL_PREFIXES
    )


def hidden_tools(all_tools: List[Any]) -> List[Any]:
    """Tools the meta-tools operate over (everything not always-loaded)."""
    return [t for t in all_tools if not is_always_loaded(t)]


def dynamic_tools_min_tools() -> int:
    """Hideable-tool count at or above which dynamic mode engages. 0 disables
    the size gate, leaving the agent flag as the only condition.

    Read per call, not at import: the worker injects secrets into os.environ
    during its lifespan, after this module is imported."""
    raw = os.getenv(DYNAMIC_TOOLS_MIN_TOOLS_ENV)
    if raw is None or not str(raw).strip():
        return DYNAMIC_TOOLS_MIN_TOOLS_DEFAULT
    try:
        return max(0, int(str(raw).strip()))
    except (TypeError, ValueError):
        logger.warning(
            f"Invalid {DYNAMIC_TOOLS_MIN_TOOLS_ENV}={raw!r}; "
            f"using {DYNAMIC_TOOLS_MIN_TOOLS_DEFAULT}"
        )
        return DYNAMIC_TOOLS_MIN_TOOLS_DEFAULT


def log_dynamic_tools_decision(agent: Any, repo: Any, active: bool) -> None:
    """State whether dynamic mode engaged for this run, and what decided it.

    Without it the only visible signal is the absence of the instruction hint,
    which is indistinguishable from the agent simply having no hideable tools —
    and once a size gate is in play, "why is this agent still offloading" has to
    be answerable from the log rather than by reading code."""
    try:
        flag = bool(getattr(agent, "use_dynamic_tools", False))
        hideable = len(hidden_tools(repo.dynamic_catalog))
        threshold = dynamic_tools_min_tools()

        if not flag:
            reason = "use_dynamic_tools is off for this agent"
        elif threshold <= 0:
            reason = f"size gate disabled ({DYNAMIC_TOOLS_MIN_TOOLS_ENV}=0)"
        elif active:
            reason = f"{hideable} hideable tools >= threshold {threshold}"
        else:
            reason = (
                f"only {hideable} hideable tools, under the threshold of {threshold} "
                f"- the full catalog is attached directly"
            )
        state = "ENABLED" if active else "DISABLED"
        logger.info(f"[dynamic-tools] {state}: {reason}")
    except Exception:
        pass


def reset_dynamic_run_state(repo: Any) -> None:
    """Drop the previous run's MCP proxies, toolkits and inspected-tool set.

    A worker reuses one repo across tasks, so leftovers would both leak into this
    run's catalog and inflate the count the size gate reads."""
    for attr in ("_dynamic_mcp_proxies", "_dynamic_mcp_toolkits", "_dynamic_inspected"):
        state = getattr(repo, attr, None)
        if state is not None:
            state.clear()


def dynamic_tools_active(agent: Any, repo: Any) -> bool:
    """True when the agent opted in AND its hideable catalog is large enough.

    Every decision point (tool filtering, meta-tool injection, the instruction
    hint, the MCP collapse) must route through this — a site reading the raw
    flag would disagree with the others whenever the size gate bites. The count
    only ever grows within a run (MCP proxies are appended once dynamic mode
    connects them), so the answer cannot flip from True back to False."""
    if not bool(getattr(agent, "use_dynamic_tools", False)):
        return False
    threshold = dynamic_tools_min_tools()
    if threshold <= 0:
        return True
    return len(hidden_tools(repo.dynamic_catalog)) >= threshold


# --- Keyword scoring -------------------------------------------------------- #

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> List[str]:
    return _TOKEN_RE.findall((text or "").lower())


def score_tool(query: str, tool: Any) -> float:
    """Keyword relevance of a tool to a query. Higher is better, 0 == no match.

    Name matches are weighted above description matches, with a bonus when the
    raw query string appears verbatim in the name or description.
    """
    q_tokens = set(_tokenize(query))
    if not q_tokens:
        return 0.0

    name = f"{tool.name or ''} {tool.id or ''}"
    desc = tool.description or ""
    name_tokens = set(_tokenize(name))
    desc_tokens = set(_tokenize(desc))

    score = 3.0 * len(q_tokens & name_tokens) + 1.0 * len(q_tokens & desc_tokens)

    q_lower = query.lower().strip()
    if q_lower and q_lower in name.lower():
        score += 4.0
    elif q_lower and q_lower in desc.lower():
        score += 1.5

    return score


# --- Rendering -------------------------------------------------------------- #


def _xml_escape(text: str) -> str:
    return (
        (text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _xml_escape_text(text: str) -> str:
    """Escape only the element-text-sensitive characters (``&``/``<``/``>``),
    leaving quotes intact so embedded JSON stays copy-paste friendly."""
    return (text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _mcp_attrs(tool: Any) -> str:
    """XML attributes naming an MCP proxy's source server (server + url), so the
    model knows which MCP server a tool comes from. Empty for xpander tools."""
    if not getattr(tool, "is_mcp_proxy", False):
        return ""
    parts = []
    server_name = getattr(tool, "server_name", None)
    server_url = getattr(tool, "server_url", None)
    if server_name:
        parts.append(f' server="{_xml_escape(str(server_name))}"')
    if server_url:
        parts.append(f' url="{_xml_escape(str(server_url))}"')
    return "".join(parts)


def _truncate(text: str, limit: int = TRUNCATED_DESC_LEN) -> str:
    collapsed = " ".join((text or "").split())
    if len(collapsed) <= limit:
        return _xml_escape(collapsed)
    return _xml_escape(collapsed[: limit - 1].rstrip() + "…")


def _resolve_ref(node: Dict[str, Any], defs: Dict[str, Any]) -> Dict[str, Any]:
    """Follow a JSON-schema ``$ref`` into ``$defs`` (one hop is enough here)."""
    ref = node.get("$ref")
    if ref:
        key = ref.split("/")[-1]
        return defs.get(key, {})
    return node


def _example_for(node: Dict[str, Any], defs: Dict[str, Any], depth: int = 0) -> Any:
    """Best-effort example value for a JSON-schema node, resolving $ref/anyOf
    and recursing into the real nested object structure (body_params, headers…).
    Placeholders convey SHAPE; the full <schema> carries the exact contract."""
    # Depth cap: a self-referential schema ($ref back into an ancestor) would
    # otherwise recurse until RecursionError, which render_tool swallows and
    # then drops the schema — leaving the tool uninspectable (and so uncallable
    # under the schema gate). Bail out with a placeholder instead.
    if depth > 6:
        return "..."

    node = _resolve_ref(node, defs)

    if "anyOf" in node:
        opts = [o for o in node["anyOf"] if o.get("type") != "null"]
        return _example_for(opts[0], defs, depth) if opts else None

    node_type = node.get("type")
    if node_type == "object" or "properties" in node:
        props = node.get("properties") or {}
        required = set(node.get("required") or [])
        out: Dict[str, Any] = {}
        for key, sub in props.items():
            # Required fields always; otherwise only the first couple so the
            # example stays small but still shows the key inputs.
            if required and key not in required and len(out) >= 2:
                continue
            out[key] = _example_for(sub, defs, depth + 1)
        return out
    if node_type == "array":
        return [_example_for(node.get("items") or {}, defs, depth + 1)]
    if node_type == "integer" or node_type == "number":
        return 0
    if node_type == "boolean":
        return True
    return "..."


def _example_arguments(schema_json: Dict[str, Any]) -> Dict[str, Any]:
    """Example ``arguments`` for xp_execute_tool — the tool's own input object
    (its payload contents: body_params / query_params / headers …)."""
    defs = schema_json.get("$defs") or {}
    example = _example_for(schema_json, defs)
    return example if isinstance(example, dict) else {}


def render_tool(tool: Any, full_schema: bool = False) -> str:
    """XML-style render of one tool for the LLM. ``name`` is the canonical tool
    id (what you pass to xp_get_tool / xp_execute_tool), never the verbose
    display name."""
    name = _xml_escape(tool.id)
    desc = _truncate(tool.description or tool.name or tool.id, limit=300)
    parts = [f'<tool name="{name}"{_mcp_attrs(tool)}>', f"  <desc>{desc}</desc>"]

    if full_schema:
        try:
            if getattr(tool, "is_mcp_proxy", False):
                # MCP tools carry a raw JSON-schema dict (no pydantic class) and
                # take FLAT args — the example falls out of the raw inputSchema.
                schema_json = tool.raw_json_schema or {"type": "object", "properties": {}}
            else:
                schema_json = cached_tool_json_schema(tool.schema, "serialization")
            # Show the actual xp_execute_tool call shape so the model passes the
            # correct nested envelope (body_params/headers) on the first try.
            example = {"name": tool.id, "arguments": _example_arguments(schema_json)}
            example_text = _xml_escape_text(json.dumps(example))
            schema_text = _xml_escape_text(json.dumps(schema_json))
            parts.append(f"  <execute_example>{example_text}</execute_example>")
            parts.append(f"  <schema>{schema_text}</schema>")
        except Exception:
            # Schema generation is best-effort; never break discovery on it.
            pass

    parts.append("</tool>")
    return "\n".join(parts)


# --- Meta-tool payload models ----------------------------------------------- #


class _MetaToolReasoning(BaseModel):
    """The user-visible reasoning shown on a discovery call's activity row."""

    toolcallreasoningtitle: str = Field(
        ...,
        description=(
            "The concrete action this call performs (max 5 words). If you cannot "
            'name one, you already have what you need — answer now. Example: '
            '"Find an issue-tracker tool".'
        ),
    )
    toolcallreasoningdescription: Optional[str] = Field(
        None,
        description=(
            "One-sentence markdown summary of the action and goal (max 100 "
            'characters). Example: "Look for a tool that can create a Jira issue."'
        ),
    )


class _MetaToolPayload(BaseModel):
    """Base for the read-only meta-tools: carries the reasoning headers.

    ``headers`` is required so the model reliably fills it, but a call that
    omits it is repaired rather than rejected — a validation error here would
    cost a turn, and the report path synthesizes a title from the arguments."""

    headers: _MetaToolReasoning = Field(
        ...,
        description="Why you are making this call — shown to the user.",
    )

    @model_validator(mode="before")
    @classmethod
    def _tolerate_missing_headers(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        headers = data.get("headers")
        if isinstance(headers, _MetaToolReasoning):
            return data
        if not isinstance(headers, dict):
            return {**data, "headers": {"toolcallreasoningtitle": ""}}
        if headers.get("toolcallreasoningtitle") is None:
            return {**data, "headers": {**headers, "toolcallreasoningtitle": ""}}
        return data


class _ListToolsPayload(_MetaToolPayload):
    cursor: int = Field(
        0,
        description="0-based start index. Pass the next_cursor from the previous page.",
    )
    limit: int = Field(
        DEFAULT_LIST_LIMIT,
        description=f"Max tools to return (1-{MAX_PAGE_LIMIT}).",
    )


class _SearchToolsPayload(_MetaToolPayload):
    query: str = Field(
        ...,
        description="What you need in plain words, e.g. 'create a jira issue'.",
    )
    limit: int = Field(DEFAULT_SEARCH_LIMIT, description="Max results to return.")
    detail: str = Field(
        "summary",
        description="'summary' for name+description, 'full' to also include the JSON schema.",
    )


class _GetToolPayload(_MetaToolPayload):
    name: Union[str, List[str]] = Field(
        ...,
        description=(
            "Exact tool id from list/search results. Pass a list to read several "
            f"schemas in this one call (up to {MAX_SCHEMAS_PER_GET})."
        ),
    )


class _ExecuteToolPayload(BaseModel):
    name: str = Field(..., description="Exact tool name to run (from search/get).")
    arguments: Dict[str, Any] = Field(
        default_factory=dict,
        description="The tool's own input object (its payload contents).",
    )
    save_output_to_file: bool = Field(
        False,
        description=(
            "Set true ONLY when you expect a HUGE output you don't need to read "
            "inline: the raw result is written to a workspace file and you get "
            "back its path plus a short preview instead. Read it later with "
            "xpworkspace-grep/file-read/bash. Default false (result returned inline)."
        ),
    )


# --- Meta-tool descriptions (AI-optimized, XML hints) ----------------------- #

_LIST_DESC = (
    "List available tools, paginated. <when>You want to browse what exists.</when> "
    "<then>Read names, xp_get_tool a name for its schema, then xp_execute_tool to run it.</then> "
    "Returns a page plus a <page .../> footer carrying next_cursor when more remain. "
    "Wrap arguments in a `payload` object."
)
_SEARCH_DESC = (
    "Find tools by intent. <when>Before any external action when no loaded tool fits.</when> "
    "<then>Pick the best result by its `name` (the tool id). A narrow search returns each "
    "match with its full schema — when the result already shows the schema, call "
    "xp_execute_tool with it directly. Call xp_get_tool only for a match returned as a "
    "summary.</then> "
    "Set detail='full' to force schemas on a wide result set. Wrap arguments in a `payload` object."
)
_GET_DESC = (
    "Get a tool's full schema and a ready-to-copy execute example. "
    "<when>Before xp_execute_tool for a tool whose schema you have not seen yet — never guess "
    "a tool's arguments. Skip it when the search result already carried the schema.</when> "
    "<then>Needing several schemas is still ONE call: pass them as a list, "
    '`name: ["tool_a", "tool_b"]`, and every schema comes back together.</then> '
    "`name` is the tool id from search/list. Wrap arguments in a `payload` object."
)
_EXECUTE_DESC = (
    "Run a tool by id with its arguments. "
    "<when>ONLY after xp_get_tool for this exact tool — execution is REFUSED until you have "
    "read its schema, since you cannot know its arguments otherwise.</when> "
    "`arguments` is the tool's own input object — match the schema exactly. Most tools want the "
    'FULL nested envelope the schema shows (e.g. {"body_params": {...}, "headers": {...}}), NOT '
    "flattened fields; but MCP tools (name starts with `mcp_tool_`) take FLAT args as their schema "
    "shows, with no body_params wrapper. `name` is the tool id. Wrap arguments in a `payload` object. "
    "Set save_output_to_file=true ONLY for outputs you expect to be huge and do not need inline — "
    "you get a workspace file path plus a preview instead of the full result."
)


# --- Meta-tool implementations (pure) --------------------------------------- #


def _as_dict(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, BaseModel):
        return payload.model_dump(exclude_none=True)
    if isinstance(payload, dict):
        return payload
    return {}


def _list_impl(repo: Any, data: Dict[str, Any], inspected: set) -> str:
    cursor = max(0, int(data.get("cursor", 0) or 0))
    limit = max(
        1,
        min(
            int(data.get("limit", DEFAULT_LIST_LIMIT) or DEFAULT_LIST_LIMIT),
            MAX_PAGE_LIMIT,
        ),
    )

    tools = hidden_tools(repo.dynamic_catalog)
    total = len(tools)
    page = tools[cursor : cursor + limit]

    entries = "\n".join(
        f'  <tool name="{_xml_escape(t.id)}"{_mcp_attrs(t)}>{_truncate(t.description or "")}</tool>'
        for t in page
    )
    next_cursor = cursor + limit
    footer = f'cursor="{cursor}" limit="{limit}" returned="{len(page)}" total="{total}"'
    if next_cursor < total:
        footer += f' next_cursor="{next_cursor}"'

    body = entries if entries else "  <empty/>"
    return f"<tools>\n{body}\n  <page {footer}/>\n</tools>"


def _search_impl(repo: Any, data: Dict[str, Any], inspected: set) -> str:
    query = str(data.get("query", "") or "").strip()
    limit = max(
        1,
        min(
            int(data.get("limit", DEFAULT_SEARCH_LIMIT) or DEFAULT_SEARCH_LIMIT),
            MAX_PAGE_LIMIT,
        ),
    )
    full = str(data.get("detail", "summary") or "summary").lower() == "full"

    if not query:
        return (
            '<no_matches reason="empty_query">'
            "Provide a 'query' describing the capability you need."
            "</no_matches>"
        )

    tools = hidden_tools(repo.dynamic_catalog)
    scored = [(score_tool(query, t), t) for t in tools]
    scored = [(s, t) for s, t in scored if s > 0]
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [t for _, t in scored[:limit]]

    if not top:
        sample = ", ".join((t.name or t.id) for t in tools[:8])
        return (
            f'<no_matches query="{_xml_escape(query)}">'
            f"No tool matched. Try broader terms. "
            f"Sample available tools: {_xml_escape(sample)}. "
            f"Or call xp_list_tools to browse.</no_matches>"
        )

    # A short result set is cheaper to hand over whole than to make the model
    # fetch one schema at a time: reaching a tool took search + get + execute,
    # and the get carried the same schema this can inline for a few hundred
    # tokens. Wide result sets stay summarized so a vague query cannot dump the
    # catalog into context.
    if not full and len(top) <= AUTO_FULL_SEARCH_RESULTS:
        full = True

    # detail='full' reveals each tool's schema, so those count as inspected and
    # become eligible for xp_execute_tool without a separate xp_get_tool call.
    if full:
        inspected.update(t.id for t in top)

    logger.info(
        f"[dynamic-tools] search query={query!r} hits={len(top)} schemas_inlined={full}"
    )
    entries = "\n".join(render_tool(t, full_schema=full) for t in top)
    return f'<results query="{_xml_escape(query)}" count="{len(top)}">\n{entries}\n</results>'


def _requested_names(data: Dict[str, Any]) -> List[str]:
    """Tool ids asked for, from either ``name`` or ``names``, in order and deduped.

    ``name`` accepts a list too: a model told it can read several will put them
    there as often as it uses the plural field."""
    raw: List[Any] = []
    for key in ("name", "names"):
        value = data.get(key)
        if isinstance(value, (list, tuple, set)):
            raw.extend(value)
        elif value is not None:
            raw.append(value)

    seen: Dict[str, None] = {}
    for item in raw:
        text = str(item or "").strip()
        if text and text not in seen:
            seen[text] = None
    return list(seen)[:MAX_SCHEMAS_PER_GET]


def _render_one(repo: Any, name: str, inspected: set) -> str:
    tool = repo.get_tool_by_id(name) or repo.get_tool_by_name(name)
    if not tool:
        return (
            f'<not_found name="{_xml_escape(name)}">'
            "No such tool. Call xp_search_tools first to find the exact name."
            "</not_found>"
        )
    # Mark inspected: the model has now seen this tool's schema and may execute it.
    inspected.add(tool.id)
    return render_tool(tool, full_schema=True)


def _get_impl(repo: Any, data: Dict[str, Any], inspected: set) -> str:
    names = _requested_names(data)
    if not names:
        return (
            '<not_found name="">'
            "Pass the tool id in `name` — one id, or several to read together. "
            "Call xp_search_tools first to find it."
            "</not_found>"
        )
    logger.info(f"[dynamic-tools] get schemas={len(names)} names={names}")
    if len(names) > 1:
        entries = "\n".join(_render_one(repo, n, inspected) for n in names)
        return f'<tools count="{len(names)}">\n{entries}\n</tools>'
    return _render_one(repo, names[0], inspected)


async def _execute_impl(repo: Any, data: Dict[str, Any], inspected: set) -> Any:
    name = str(data.get("name", "") or "").strip()
    arguments = data.get("arguments") or {}
    # Sibling of `arguments`, so it can never leak into the inner tool payload.
    save_to_file = bool(data.get("save_output_to_file") or False)

    tool = repo.get_tool_by_id(name) or repo.get_tool_by_name(name)
    if not tool:
        return (
            f'<not_found name="{_xml_escape(name)}">'
            "No such tool. Call xp_search_tools first to find the exact name."
            "</not_found>"
        )

    # Hard gate: refuse to run a tool whose schema the model has not fetched.
    # You cannot call a tool correctly without its schema — force xp_get_tool first.
    if tool.id not in inspected:
        return (
            f'<schema_required name="{_xml_escape(tool.id)}">'
            f"You have not read this tool's schema yet, so you cannot know its "
            f'arguments. Call xp_get_tool with name="{_xml_escape(tool.id)}" '
            f"FIRST, then xp_execute_tool with arguments matching that schema."
            "</schema_required>"
        )

    cfg = repo.configuration
    state = getattr(cfg, "state", None)
    agent = getattr(state, "agent", None)
    task = getattr(state, "task", None)

    # MCP proxies dispatch through their live agno session (not the xpander HTTP
    # path), take flat args (no workspace_path/body_params envelope), and the
    # meta-tool path bypasses the agno hook — so report activity ourselves.
    if getattr(tool, "is_mcp_proxy", False):
        result, is_error = await _execute_mcp_proxy(tool, arguments, task)
        return await _maybe_save_result(
            result=result,
            is_error=is_error,
            save_to_file=save_to_file,
            tool_id=tool.id,
            agent=agent,
            configuration=cfg,
        )

    # Parity with the agno-hook path: resolve workspace_path offloads here too,
    # otherwise schema validation rejects the empty inline body_params.
    if has_workspace_path(arguments):
        try:
            arguments = await resolve_workspace_payload(
                agent_id=getattr(agent, "id", None),
                configuration=cfg,
                task_id=getattr(task, "id", None) if task else None,
                arguments=arguments,
            )
        except WorkspacePayloadError as exc:
            return (
                f'<workspace_payload_error name="{_xml_escape(tool.id)}">'
                f"{_xml_escape_text(exc.description)}"
                "</workspace_payload_error>"
            )

    # Activity already carries the FULL result (report_activity=True), so the UI
    # stays complete even when the LLM only gets a saved-file pointer.
    result = await tool.ainvoke(
        agent_id=getattr(agent, "id", None),
        agent_version=getattr(agent, "version", None),
        payload=arguments,
        configuration=cfg,
        task_id=getattr(task, "id", None) if task else None,
        report_activity=True,
    )
    return await _maybe_save_result(
        result=result,
        is_error=bool(getattr(result, "is_error", False)),
        save_to_file=save_to_file,
        tool_id=tool.id,
        agent=agent,
        configuration=cfg,
    )


async def _maybe_save_result(
    *,
    result: Any,
    is_error: bool,
    save_to_file: bool,
    tool_id: str,
    agent: Any,
    configuration: Any,
) -> Any:
    """Honor ``save_output_to_file``: offload the result to a plaintext workspace
    file and return a pointer — or fall back inline (never lose data, never bury
    an error in a file, never fail a call the tool itself completed)."""
    if not save_to_file:
        return result
    if is_error:
        return result
    if not getattr(agent, "workspace_tools_enabled", True) or not getattr(
        agent, "id", None
    ):
        return append_inline_notice(
            result,
            "[save_output_to_file ignored: workspace not available for this agent; "
            "full result returned inline]",
        )
    content = serialize_tool_result(result)
    if len(content) < MIN_SAVE_CHARS:
        return append_inline_notice(
            result,
            "[save_output_to_file ignored: result small enough to return inline]",
        )
    try:
        path = await save_result_to_workspace(
            configuration=configuration, agent_id=agent.id, content=content
        )
    except Exception as exc:
        logger.warning(
            f"[dynamic-tools] save_output_to_file write failed for {tool_id}: {exc}"
        )
        return append_inline_notice(
            result, "[save_output_to_file failed; full result returned inline]"
        )
    return build_saved_result_pointer(tool_id=tool_id, path=path, content=content)


async def _execute_mcp_proxy(
    tool: Any, arguments: Dict[str, Any], task: Any
) -> tuple:
    """Run an MCP proxy via its live agno session, surfacing the real MCP tool in
    the activity log (the meta-tool path bypasses the agno hook, so nothing else
    reports it). Reporting is best-effort and never blocks the tool result.

    Returns ``(result, is_error)``; activity always carries the full result."""
    report_request = report_result = None
    if task is not None and getattr(task, "id", None):
        try:
            from xpander_sdk.modules.backend.utils.tool_call_events import (
                report_tool_call_request,
                report_tool_call_result,
            )

            report_request, report_result = (
                report_tool_call_request,
                report_tool_call_result,
            )
        except Exception:
            pass

    request_id = uuid.uuid4().hex
    if report_request:
        try:
            await report_request(
                task=task,
                request_id=request_id,
                operation_id=tool.id,
                tool_name=tool.id,
                payload=arguments,
            )
        except Exception:
            pass

    is_error = False
    try:
        result = await tool.ainvoke(arguments)
    except Exception as exc:
        is_error = True
        result = f"Error executing MCP tool '{tool.id}': {exc}"
    else:
        # agno reports MCP failures in-band as content prefixed "Error from MCP tool".
        if isinstance(result, str) and result.lstrip().startswith("Error from MCP tool"):
            is_error = True

    if report_result:
        try:
            await report_result(
                task=task,
                request_id=request_id,
                operation_id=tool.id,
                tool_name=tool.id,
                payload=arguments,
                result=result,
                is_error=is_error,
            )
        except Exception:
            pass

    return result, is_error


# --- Meta-tool callable assembly -------------------------------------------- #


def _finalize(
    fn: Callable, name: str, description: str, payload_model: type
) -> Callable:
    """Attach the metadata agno reads to expose the callable as a tool."""
    fn.__name__ = name
    fn.__doc__ = description
    payload_param = Parameter(
        name="payload",
        kind=Parameter.POSITIONAL_OR_KEYWORD,
        annotation=payload_model,
    )
    fn.__signature__ = Signature([payload_param], return_annotation=Any)
    fn.__annotations__ = {"payload": payload_model, "return": Any}
    return fn


def _build_readonly(
    repo: Any,
    is_async: bool,
    name: str,
    description: str,
    model: type,
    impl: Callable[[Any, Dict[str, Any], set], str],
    inspected: set,
) -> Callable:
    if is_async:

        async def tool_function(payload: Any) -> Any:
            return impl(repo, _as_dict(payload), inspected)

    else:

        def tool_function(payload: Any) -> Any:
            return impl(repo, _as_dict(payload), inspected)

    return _finalize(tool_function, name, description, model)


def _build_execute(repo: Any, is_async: bool, inspected: set) -> Callable:
    if is_async:

        async def tool_function(payload: Any) -> Any:
            return await _execute_impl(repo, _as_dict(payload), inspected)

    else:

        def tool_function(payload: Any) -> Any:
            return run_sync(_execute_impl(repo, _as_dict(payload), inspected))

    return _finalize(
        tool_function, "xp_execute_tool", _EXECUTE_DESC, _ExecuteToolPayload
    )


def build_meta_tools(repo: Any) -> List[Callable]:
    """Build the four dynamic meta-tool callables bound to ``repo``.

    The four tools share the repo-scoped ``_dynamic_inspected`` set: a tool
    becomes executable only after the model has seen its schema via xp_get_tool
    (or xp_search_tools detail='full'). xp_execute_tool hard-refuses the rest.
    The set lives on the repo (not in this closure) so the gate survives any
    re-materialization of the non-cached ``functions`` property within a run."""
    # a hidden id called directly must be resolvable back into xp_execute_tool
    register_dynamic_tools_repo(repo)
    is_async = bool(repo.is_async)
    inspected: set = repo._dynamic_inspected
    return [
        _build_readonly(
            repo,
            is_async,
            "xp_list_tools",
            _LIST_DESC,
            _ListToolsPayload,
            _list_impl,
            inspected,
        ),
        _build_readonly(
            repo,
            is_async,
            "xp_search_tools",
            _SEARCH_DESC,
            _SearchToolsPayload,
            _search_impl,
            inspected,
        ),
        _build_readonly(
            repo,
            is_async,
            "xp_get_tool",
            _GET_DESC,
            _GetToolPayload,
            _get_impl,
            inspected,
        ),
        _build_execute(repo, is_async, inspected),
    ]


# --- Instruction hint ------------------------------------------------------- #


def build_dynamic_tools_hint(repo: Any) -> str:
    """The <dynamic_tools> system-prompt block: workflow, rules, inline catalog.

    Returns "" when there are no hidden tools (nothing to disclose)."""
    tools = hidden_tools(repo.dynamic_catalog)
    total = len(tools)
    if total == 0:
        return ""

    shown = tools[:HINT_CATALOG_CAP]
    catalog = "\n".join(
        f'  <tool name="{_xml_escape(t.id)}"{_mcp_attrs(t)}>{_truncate(t.description or "")}</tool>'
        for t in shown
    )
    overflow = ""
    if total > len(shown):
        overflow = f"\n  <!-- {total - len(shown)} more tools; call xp_list_tools to page the rest -->"

    return f"""

<dynamic_tools>
Your full tool library ({total} tools) is NOT loaded into context. Only xp*/knowledge tools are directly callable; everything else — including MCP server tools (name starts with `mcp_tool_`) — is reached through the meta-tools below.
<workflow>
1. xp_search_tools(query) — find candidates by intent (or xp_list_tools to browse). A narrow search
   returns each match WITH its schema; when it does, go straight to step 3.
2. xp_get_tool(name) — only for a match that came back as a summary: reads its schema + a
   ready-to-copy execute example. Need several? Pass a LIST — xp_get_tool(name=["a","b"])
   returns every schema in one call, so two tools cost one step, not two.
3. xp_execute_tool(name, arguments) — run it, with `arguments` matching the schema exactly.
</workflow>
<rules>
- Search FIRST. Never assume a tool is missing because it isn't loaded — search for it.
- One search is usually enough: query the capability you need, then execute the best match.
- Batch the read-only steps. A task needing several tools reads them together — one
  xp_get_tool with a list of names — and only then starts executing.
- `name` is the tool id shown in search/list/catalog — use it verbatim for xp_get_tool and xp_execute_tool.
- Work from a schema you have actually seen — from the search result when it carried one, from
  xp_get_tool otherwise. Never guess a tool's arguments — match the schema exactly:
  most tools want the FULL nested envelope (e.g. {{"body_params": {{...}}, "headers": {{...}}}}), but MCP
  tools (`mcp_tool_*`) take FLAT args with no body_params wrapper — copy the shape their schema shows.
- xp*/knowledge tools are already available directly; no search needed for those. MCP tools are NOT
  directly loaded — search/get them like any other hidden tool.
- For expected-HUGE outputs you only need to grep/inspect (transcriptions, big exports), pass
  save_output_to_file=true to xp_execute_tool: the result lands in a plaintext workspace file you
  read with xpworkspace-grep/file-read/bash instead of flooding your context.
</rules>
<catalog>
{catalog}{overflow}
</catalog>
Reminder: before any external action you do not already have a loaded tool for, call xp_search_tools first.
</dynamic_tools>
"""
