"""answer a retired tool name with what replaced it instead of a 404."""

from __future__ import annotations
import json
from typing import Any

import anyio
import anyio.to_thread
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from mcp.types import CallToolResult, TextContent
from ..delivery import accounting
from ...foundation.token_budget.token_budget import Budget, InvalidBudget, TokenizerUnavailable, count_tokens, serialize
from probe.mcp.server.limits import _limiters
from probe.mcp.server.tool_runner import _bounded_error_text


#: Names this server used to answer to, and the call that replaces each.
#:
#: These are NOT registered as tools. A registered stub would answer the problem
#: it exists for -- a caller holding a stale tool list -- at the cost of putting
#: six dead names into the `tools/list` of every NEW session forever, and tool
#: descriptions are context every session pays for whether or not it needs them.
#: `_RetiringMCP` below intercepts the CALL instead, so the guidance reaches the
#: only caller who asks for it and nobody else carries it.
#:
#: WHY A MESSAGE AND NOT AN ALIAS. An alias that quietly forwards keeps the old
#: vocabulary working, which means it keeps being used, which means the rename
#: never finishes -- and the previous three aliases (`get_metrics_grouped`,
#: `get_run_coordinates`, `export_metric_points`) are the evidence: they lived a
#: release and had to be deleted by hand anyway. A refusal that says exactly what
#: to call instead costs the caller one turn and ends the migration.
_RETIRED_TOOLS: dict[str, str] = {
    "browse_research": "browse",
    "get_entity": "entity",
    "read_metrics": "metrics",
    "get_metrics_grouped": 'metrics(mode="grouped", ...)',
    "get_run_coordinates": 'metrics(mode="coordinates", ...)',
    "export_metric_points": 'metrics(mode="points", ...)',
    # 2026-10-08: renamed outright, no alias (Richard's call). A refusal is not
    # an alias: the old name stays unlisted and never runs; its caller is told.
    "search_knowledge": "search",
}


def _retired_tool_message(name: str) -> str:
    """What a caller of a retired name is told.

    It names the replacement FIRST, because that is the only line an agent needs
    to recover inside the same turn. The reconnect instruction is second and is
    the one that actually matters for the common case: the tool list a session
    fetched at `initialize` is a snapshot, so a session that connected before the
    rename cannot see the new name no matter how current its installed package
    is. Telling that caller to upgrade would send them to fix the wrong thing.
    """
    replacement = _RETIRED_TOOLS[name]
    return (
        f"`{name}` no longer exists. Call `{replacement}` instead.\n\n"
        "If that name is not in your tool list, the list is from before the "
        "rename -- reconnect this MCP server (restarting the session is enough) "
        "and it will be there. If your SKILL text still names the old tools, "
        "upgrade with `pip install -U probe-research`."
    )


class _RetiringMCP(FastMCP):
    """A FastMCP that answers a retired name with instructions instead of a 404.

    `_setup_handlers` binds `self.call_tool`, so overriding it here is enough --
    the low-level server resolves the bound method through the MRO at dispatch.

    The default answer for an unregistered name is `Unknown tool: <name>`, which
    tells an agent that something is wrong and nothing about what to do next. The
    agent's usual recovery from that is to try a neighbouring name or give up,
    and a rename is the one failure where the correct next call is knowable
    exactly.
    """

    def add_tool(self, fn: Any, **kwargs: Any) -> None:
        # The transport has one canonical text channel, including future tools.
        # Leaving an inferred output schema would require a structured duplicate.
        kwargs["structured_output"] = False
        super().add_tool(fn, **kwargs)
        # An argument the schema does not declare must be REFUSED, not dropped:
        # pydantic's default silently discards extras, so an invented parameter
        # returns a confident answer to a different question (a lazy-loading
        # agent that never read the schema believed browse took `query`).
        # additionalProperties=false lets strict clients reject before the wire;
        # the registry backs the server-side check in call_tool for the rest.
        tool_name = kwargs.get("name") or fn.__name__
        tool = self._tool_manager.get_tool(tool_name)
        if tool is not None:
            tool.parameters["additionalProperties"] = False
            self._declared_params[tool_name] = frozenset(tool.parameters.get("properties", {}))

    _declared_params: dict[str, frozenset[str]]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._declared_params = {}
        super().__init__(*args, **kwargs)

    async def call_tool(  # type: ignore[override]
        self, name: str, arguments: dict[str, Any]
    ) -> Any:
        budget = Budget(512)
        try:
            budget = Budget(arguments.get("token_budget", 2000))
            if name == "entity":
                refs = arguments.get("refs")
                if not isinstance(refs, list) or not 1 <= len(refs) <= 20:
                    raise InvalidBudget(
                        "refs must be a LIST of 1-20 addresses ('ref' is browse's parameter; entity takes refs)"
                    )
                if any(not isinstance(ref, str) or not 1 <= len(ref) <= 256 for ref in refs):
                    raise InvalidBudget("Each reference must be a string of 1 to 256 characters")
            if name in _RETIRED_TOOLS:
                raise ToolError(_retired_tool_message(name))
            declared = self._declared_params.get(name)
            # token_budget is consumed by this wrapper for every tool, so a
            # future tool that does not declare it still gets bounded delivery.
            if declared is not None and not (declared | {"token_budget"}).issuperset(arguments):
                unknown = ", ".join(sorted(set(arguments) - declared - {"token_budget"}))
                raise ToolError(
                    f"{name} got unknown argument(s): {unknown} -- "
                    f"its parameters are: {', '.join(sorted(declared))}"
                )
            result = await super().call_tool(name, arguments)
            _, permits = _limiters()

            def final_text() -> list[TextContent]:
                if isinstance(result, CallToolResult):
                    content = result.content
                    if result.isError:
                        raise ToolError(
                            "Tool read failed; retry only after correcting the source error."
                        )
                else:
                    content = result[0] if isinstance(result, tuple) else result
                if not isinstance(content, (list, tuple)) or len(content) != 1:
                    raise ToolError("response_too_large: unexpected content; narrow the read.")
                block = content[0]
                if not isinstance(block, TextContent):
                    raise ToolError("Unsupported tool content; request a text read.")
                # A newly registered tool may not use _tool. The final boundary
                # still enforces its actual text; no structured duplicate escapes.
                try:
                    parsed = json.loads(block.text)
                except (ValueError, TypeError):
                    parsed = {"data": block.text}
                text = serialize(parsed)
                text_bytes = len(text.encode("utf-8"))
                if text_bytes > budget.byte_limit:
                    raise ToolError(
                        "response_too_large: narrow the read or request its continuation."
                    )
                reference_tokens = count_tokens(text)
                if reference_tokens > budget.token_limit:
                    raise ToolError(
                        "response_too_large: narrow the read or request its continuation."
                    )
                accounting.note_delivery(
                    reference_tokens=reference_tokens,
                    response_text_bytes=text_bytes,
                    token_budget=budget.token_limit,
                    has_continuation=bool(isinstance(parsed, dict) and parsed.get("next_cursor")),
                    stale_reason=(
                        "source_changed"
                        if isinstance(parsed, dict)
                        and isinstance(parsed.get("missing"), list)
                        and any(
                            isinstance(item, dict)
                            and isinstance(item.get("reason"), str)
                            and item["reason"].startswith(
                                ("ValidationError: source_changed:", "source_changed:")
                            )
                            for item in parsed["missing"]
                        )
                        else None
                    ),
                )
                return [TextContent(type="text", text=text)]

            return await anyio.to_thread.run_sync(final_text, limiter=permits)
        except TokenizerUnavailable:
            raise ToolError("Probe MCP tokenizer unavailable; repair the installation.") from None
        except Exception as exc:
            # Covers validation/unknown names and errors raised before a worker
            # result exists. Never echo an unbounded request or exception.
            message = _bounded_error_text(exc)
            try:
                minimum = Budget(512)
                while not minimum.fits_text(message) and message:
                    message = message[: len(message) // 2]
                accounting.note_delivery(
                    reference_tokens=count_tokens(message),
                    response_text_bytes=len(message.encode("utf-8")),
                    token_budget=budget.token_limit,
                    has_continuation=False,
                    stale_reason="source_changed" if "source_changed:" in message else None,
                )
            except TokenizerUnavailable:
                message = "Probe MCP tokenizer unavailable; repair the installation."
            raise ToolError(message or "Probe MCP read failed.") from None
