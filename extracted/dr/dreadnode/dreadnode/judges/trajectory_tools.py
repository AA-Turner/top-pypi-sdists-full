"""Trajectory-navigation Toolset exposed to an agentic outcome judge.

`TrajectoryViewer` exposes read-only tools over a (preloaded) `Trajectory` —
view the final assistant output, list tool-role messages, look up the
assistant message that planned a specific tool call, regex-search content.

It is a `Toolset` subclass — the dreadnode `Agent` accepts it directly in
its `tools=` list and discovers the `@tool_method`-decorated methods via
MRO walk.
"""

import re
import typing as t

from pydantic import ConfigDict

from dreadnode.agents.tools import ToolCall, Toolset, tool_method
from dreadnode.agents.trajectory import Trajectory
from dreadnode.generators.message import Message

# Cap individual tool returns so a judge can't blow its own context window by
# calling view_tool_calls() once on a 200-step trajectory. The judge can
# always narrow with regex search.
_MAX_RETURNED_MESSAGES = 50
_MAX_MESSAGE_CHARS = 4_000


def _truncate(text: str, *, limit: int = _MAX_MESSAGE_CHARS) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n…[truncated, {len(text) - limit} chars omitted]"


def _format_tool_call(call: ToolCall) -> str:
    args = call.arguments or ""
    return f"[tool_call_id={call.id}] tool={call.name} arguments={_truncate(args)}"


def _message_with_tool_calls(msg: Message) -> str:
    parts: list[str] = []
    if msg.content:
        parts.append(msg.content)
    for call in msg.tool_calls or []:
        parts.append(_format_tool_call(call))
    return "\n".join(parts)


class TrajectoryViewer(Toolset):
    """Read-only navigation tools over an agent-under-test trajectory.

    The trajectory is bound at construction time. All tools query the same
    snapshot — there is no streaming or pagination v1.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    trajectory: Trajectory

    @tool_method(name="view_final_output", catch=True)
    def view_final_output(self) -> str:
        """Returns the content of the final assistant message in the trajectory.

        Use this first to see how the agent concluded — what claim it made,
        what answer it gave, what files it pointed at.
        """
        messages = self.trajectory.messages
        for msg in reversed(messages):
            if msg.role == "assistant":
                content = msg.content or ""
                return _truncate(content) if content else "(empty assistant message)"
        return "No assistant messages in trajectory."

    @tool_method(name="view_tool_calls", catch=True)
    def view_tool_calls(
        self,
        limit: t.Annotated[
            int,
            "Maximum number of tool invocations to return (most recent first). Caps at 50.",
        ] = 25,
    ) -> list[str]:
        """Lists tool invocations and paired tool results in the trajectory.

        Returns the most recent `limit` tool invocations in reverse
        chronological order. Useful for seeing what tools the agent actually
        invoked, the arguments it passed, and what each call returned.
        """
        capped = max(1, min(limit, _MAX_RETURNED_MESSAGES))
        known_call_ids = {
            call.id for message in self.trajectory.messages for call in message.tool_calls or []
        }
        tool_results: dict[str, str] = {
            m.tool_call_id: m.content or ""
            for m in self.trajectory.messages
            if m.role == "tool" and m.tool_call_id
        }
        out: list[str] = []
        for msg in reversed(self.trajectory.messages):
            if msg.tool_calls:
                for call in reversed(msg.tool_calls):
                    result = tool_results.get(call.id)
                    entry = _format_tool_call(call)
                    if result is not None:
                        entry += f"\nresult={_truncate(result)}"
                    out.append(entry)
                    if len(out) >= capped:
                        return out
            elif msg.role == "tool":
                tag = f"[tool_call_id={msg.tool_call_id}]" if msg.tool_call_id else "[tool]"
                if msg.tool_call_id and msg.tool_call_id in known_call_ids:
                    continue
                out.append(f"{tag} result={_truncate(msg.content or '')}")
                if len(out) >= capped:
                    return out

        return out

    @tool_method(name="view_assistant_plan_for_tool_call", catch=True)
    def view_assistant_plan_for_tool_call(
        self,
        tool_call_id: t.Annotated[
            str,
            "The ID of the tool call whose assistant-side justification you want. "
            "IDs appear in `view_tool_calls()` output as `[tool_call_id=...]`.",
        ],
    ) -> str:
        """Returns the assistant message that invoked a specific tool call.

        Useful for checking whether the agent had a coherent reason for a
        tool call, or whether it was firing tools without a plan.
        """
        for msg in self.trajectory.messages:
            if not msg.tool_calls:
                continue
            for call in msg.tool_calls:
                if call.id == tool_call_id:
                    content = msg.content or "(no assistant content alongside this tool call)"
                    return _truncate(f"{content}\n{_format_tool_call(call)}")
        return f"Tool call {tool_call_id!r} not found in trajectory."

    @tool_method(name="regular_expression_search", catch=True)
    def regular_expression_search(
        self,
        query: t.Annotated[
            str,
            "Python regular expression. Case-sensitive. Searches across all "
            "message contents; returns matching messages with role + snippet.",
        ],
        limit: t.Annotated[int, "Maximum matches to return (caps at 50)."] = 20,
    ) -> list[str]:
        """Regex-search message contents and tool-call arguments.

        Use this to locate specific moments without re-reading the whole run:
        a flag string, a command, an error pattern, a domain.
        """
        try:
            pattern = re.compile(query)
        except re.error as exc:
            return [f"Invalid regex: {exc}"]

        capped = max(1, min(limit, _MAX_RETURNED_MESSAGES))
        results: list[str] = []
        for msg in self.trajectory.messages:
            content = _message_with_tool_calls(msg)
            if not content:
                continue
            if pattern.search(content):
                results.append(f"[{msg.role}] {_truncate(content)}")
                if len(results) >= capped:
                    break
        if not results:
            return [f"No matches for pattern {query!r}."]
        return results


__all__ = ["TrajectoryViewer"]
