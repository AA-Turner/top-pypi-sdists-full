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

    from openai.types.responses import (
        ResponseFunctionWebSearch as OpenAIResponseFunctionWebSearch,
    )

    def get_output(self) -> str | None:
        return json.dumps(self.action)

    @classmethod
    def from_openai(
        cls, content_item: OpenAIResponseFunctionWebSearch
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
