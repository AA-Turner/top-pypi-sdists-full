import json
from dataclasses import dataclass, field
from typing import Any, Literal, Optional

from google.genai.types import Part
from matrx_utils import vcprint


@dataclass
class CodeExecutionContent:
    type: Literal["code_execution"] = "code_execution"
    code: str = ""
    language: str = "python"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_google(self) -> dict[str, Any]:
        """Convert to Google Gemini format"""
        return {
            "executableCode": {
                "code": self.code,
                "language": self.language,
            }
        }

    def to_openai(self) -> dict[str, Any] | None:
        """Convert to OpenAI format - not supported"""
        # OpenAI doesn't support code execution content blocks
        vcprint({"type": self.type, "language": self.language, "code_preview": self.code[:120] if self.code else ""}, "CodeExecutionContent to_openai: code execution is not yet supported by OpenAI — dropping the content block", color="yellow")
        return None

    def to_anthropic(self) -> dict[str, Any] | None:
        """Convert to Anthropic format - not supported"""
        # Anthropic doesn't support code execution content blocks
        vcprint({"type": self.type, "language": self.language, "code_preview": self.code[:120] if self.code else ""}, "CodeExecutionContent to_anthropic: code execution is not yet supported by Anthropic — dropping the content block", color="yellow")
        return None

    def to_storage_dict(self) -> dict[str, Any]:
        """Serialize to storage format for database persistence (cx_message.content JSONB)."""
        result: dict[str, Any] = {"type": "code_exec"}
        if self.language:
            result["language"] = self.language
        if self.code:
            result["code"] = self.code
        # metadata used to be omitted here while the field stayed declared, so
        # anything ever set on it vanished on persist — the same silent-drop
        # shape that cost three production incidents in July (see the comment
        # in message_config.parse_content). Zero code_exec blocks exist today,
        # which is why this is a latent trap and not an outage.
        if self.metadata:
            result["metadata"] = self.metadata
        return result

    @classmethod
    def from_google(cls, part: Part) -> Optional["CodeExecutionContent"]:
        """Create CodeExecutionContent from Google Part object"""
        if hasattr(part, "executable_code") and part.executable_code:
            return cls(
                code=part.executable_code.code or "",
                language=part.executable_code.language or "python",
            )
        return None


@dataclass
class CodeExecutionResultContent:
    type: Literal["code_execution_result"] = "code_execution_result"
    outcome: str = "success"
    output: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_google(self) -> dict[str, Any]:
        """Convert to Google Gemini format"""
        return {
            "codeExecutionResult": {
                "outcome": self.outcome,
                "output": self.output,
            }
        }

    def to_openai(self) -> dict[str, Any] | None:
        """Convert to OpenAI format - not supported"""
        # OpenAI doesn't support code execution result content blocks
        vcprint({"type": self.type, "outcome": self.outcome, "output_preview": self.output[:120] if self.output else ""}, "CodeExecutionResultContent to_openai: code execution results are not yet supported by OpenAI — dropping the content block", color="yellow")
        return None

    def to_anthropic(self) -> dict[str, Any] | None:
        """Convert to Anthropic format - not supported"""
        # Anthropic doesn't support code execution result content blocks
        vcprint({"type": self.type, "outcome": self.outcome, "output_preview": self.output[:120] if self.output else ""}, "CodeExecutionResultContent to_anthropic: code execution results are not yet supported by Anthropic — dropping the content block", color="yellow")
        return None

    def to_storage_dict(self) -> dict[str, Any]:
        """Serialize to storage format for database persistence (cx_message.content JSONB)."""
        result: dict[str, Any] = {"type": "code_result"}
        if self.output:
            result["output"] = self.output
        if self.outcome:
            result["outcome"] = self.outcome
        if self.metadata:
            result["metadata"] = self.metadata
        return result

    @classmethod
    def from_google(cls, part: Part) -> Optional["CodeExecutionResultContent"]:
        """Create CodeExecutionResultContent from Google Part object"""
        if hasattr(part, "code_execution_result") and part.code_execution_result:
            return cls(
                outcome=part.code_execution_result.outcome or "success",
                output=part.code_execution_result.output or "",
            )
        return None


@dataclass
class WebSearchCallContent:
    type: Literal["web_search_call"] = "web_search_call"
    id: str = ""
    status: str = ""
    action: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def get_output(self) -> str | None:
        return json.dumps(self.action)

    @classmethod
    def from_openai(
        cls, content_item: Any
    ) -> Optional["WebSearchCallContent"]:
        id = content_item.id
        status = content_item.status
        action = content_item.action
        metadata = content_item.model_dump(exclude={"id", "status", "action"})
        return cls(
            id=id,
            status=status,
            action=action,
            metadata=metadata,
        )

    def to_openai(self) -> dict[str, Any] | None:
        """WebSearchCallContent is an ephemeral audit record — it cannot be forwarded to any provider."""
        vcprint({"id": self.id, "status": self.status, "action": self.action}, "WebSearchCallContent to_openai: web search call records cannot be forwarded to providers — dropping the content block", color="yellow")
        return None

    def to_anthropic(self) -> dict[str, Any] | None:
        """WebSearchCallContent is an ephemeral audit record — it cannot be forwarded to any provider."""
        vcprint({"id": self.id, "status": self.status, "action": self.action}, "WebSearchCallContent to_anthropic: web search call records cannot be forwarded to providers — dropping the content block", color="yellow")
        return None

    def to_google(self) -> dict[str, Any] | None:
        """WebSearchCallContent is an ephemeral audit record — it cannot be forwarded to any provider."""
        vcprint({"id": self.id, "status": self.status, "action": self.action}, "WebSearchCallContent to_google: web search call records cannot be forwarded to providers — dropping the content block", color="yellow")
        return None

    def to_storage_dict(self) -> dict[str, Any]:
        """Serialize to storage format for database persistence (cx_message.content JSONB)."""
        result: dict[str, Any] = {"type": "web_search"}
        if self.id:
            result["id"] = self.id
        if self.status:
            result["status"] = self.status
        if self.action:
            result["metadata"] = {"action": self.action}
        return result


def _strip_none(value: Any) -> Any:
    """Drop ``None``-valued keys recursively. The SDK's ``model_dump`` emits every
    optional field (``cache_control: None``, ``page_age: None``); Anthropic wants the
    block back as it was on the wire, and a literal ``null`` is not that."""
    if isinstance(value, dict):
        return {k: _strip_none(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [_strip_none(v) for v in value]
    return value


@dataclass
class HostedToolContent:
    """A provider-HOSTED tool block, carried verbatim so the turn can be replayed.

    Anthropic runs its own ``web_search`` inside the assistant turn and returns
    ``server_tool_use`` + ``web_search_tool_result`` blocks interleaved with the
    model's ``thinking`` and ``tool_use`` blocks. When the model then calls one
    of OUR tools in the same turn, the executor re-sends that assistant message
    with the tool result appended — and Anthropic requires the latest assistant
    message to come back block-for-block as it was produced. Until 2026-09-14
    ``from_anthropic_content`` dropped the hosted blocks (they must never reach
    the LOCAL executor, which was the only concern at the time), so the resent
    message read ``[thinking, thinking, tool_use]`` instead of ``[thinking,
    server_tool_use, web_search_tool_result, thinking, tool_use]`` and Anthropic
    refused it: "`thinking` or `redacted_thinking` blocks in the latest
    assistant message cannot be modified" (commerce-intake research, live
    2026-09-14; the same class in chat on 2026-08-21 and the builder on
    2026-08-26 — every time an agent with hosted search also had local tools).

    This block is provider state, not a call: the local executor never
    dispatches it (it is not a ``ToolCallContent``), ``to_anthropic`` returns
    the block verbatim, and every other provider drops it — a hosted block only
    means something to the provider that produced it.
    """

    type: Literal["hosted_tool"] = "hosted_tool"
    provider: str = ""
    block: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def block_type(self) -> str:
        return str(self.block.get("type", "") or "")

    def get_output(self) -> str | None:
        return None

    @classmethod
    def from_anthropic(cls, block: dict[str, Any]) -> "HostedToolContent":
        return cls(provider="anthropic", block=_strip_none(dict(block)))

    def to_anthropic(self) -> dict[str, Any] | None:
        if self.provider == "anthropic" and self.block:
            return _strip_none(dict(self.block))
        return None

    def to_openai(self) -> dict[str, Any] | None:
        """A hosted block belongs to the provider that produced it; another provider
        cannot consume it, so it is dropped — and said so."""
        vcprint(
            {"provider": self.provider, "block_type": self.block_type},
            "HostedToolContent to_openai: provider-hosted tool block dropped (only its "
            "own provider can replay it)",
            color="cyan",
            verbose=True,
        )
        return None

    def to_google(self) -> dict[str, Any] | None:
        vcprint(
            {"provider": self.provider, "block_type": self.block_type},
            "HostedToolContent to_google: provider-hosted tool block dropped (only its "
            "own provider can replay it)",
            color="cyan",
            verbose=True,
        )
        return None

    def to_storage_dict(self) -> dict[str, Any]:
        """Serialize to storage format for database persistence (cx_message.content JSONB)."""
        result: dict[str, Any] = {
            "type": "hosted_tool",
            "provider": self.provider,
            "block": _strip_none(dict(self.block)),
        }
        if self.metadata:
            result["metadata"] = dict(self.metadata)
        return result
