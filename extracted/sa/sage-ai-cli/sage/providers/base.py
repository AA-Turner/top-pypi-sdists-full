"""Provider base types (minimal recovery skeleton)."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Message:
    """Immutable chat message — frozen to prevent accidental mutation of a
    history entry. If you need to amend a message, build a new one via
    `dataclasses.replace()` so the call-graph that holds references doesn't
    silently observe the change.
    """
    role: str
    content: str


@dataclass
class ModelInfo:
    id: str
    provider: str
    name: str
    local: bool = False
    description: str = ""
    pros: str = ""
    cons: str = ""


@dataclass
class ToolSpec:
    """Provider-agnostic description of a callable tool.

    Each provider's `format_tools` translates a list of these into the
    provider's wire-format tool descriptor (Gemini function_declarations,
    OpenAI tools, Anthropic XML, etc.).
    """

    name: str
    description: str
    parameters: dict = field(default_factory=dict)  # JSON-schema property map
    required: list = field(default_factory=list)


def default_sage_tools() -> list[ToolSpec]:
    """The four canonical sage tools as ToolSpec records.

    Matches the text-format READ:/SEARCH:/RUN:/FILE: protocol so models
    that prefer structured calls see the same tool surface.
    """
    return [
        ToolSpec(
            name="READ",
            description="Read a file from the project. Returns the file's contents.",
            parameters={"path": {"type": "string", "description": "Path to the file"}},
            required=["path"],
        ),
        ToolSpec(
            name="SEARCH",
            description="Search for a pattern (glob or grep) in the project.",
            parameters={"pattern": {"type": "string", "description": "Glob or text pattern"}},
            required=["pattern"],
        ),
        ToolSpec(
            name="RUN",
            description="Execute a shell command in the project's working directory.",
            parameters={"command": {"type": "string", "description": "Shell command"}},
            required=["command"],
        ),
        ToolSpec(
            name="FILE",
            description="Write or overwrite a file with the given content.",
            parameters={
                "path": {"type": "string", "description": "Path to write"},
                "content": {"type": "string", "description": "File contents"},
            },
            required=["path", "content"],
        ),
    ]


class ProviderBase:
    name: str = "base"

    def is_available(self) -> bool:
        return False

    def list_models(self) -> list[ModelInfo]:
        return []

    def generate(self, messages, model="", temperature=0.7, max_tokens=2048):
        raise NotImplementedError

    def stream(self, messages, model="", temperature=0.7, max_tokens=2048):
        raise NotImplementedError

    # ── Structured tool protocol (B5) ───────────────────────────────────

    def supports_tools(self) -> bool:
        """True iff this provider can be passed structured tool definitions
        instead of the free-text RUN:/READ:/SEARCH:/FILE: protocol.

        Default False — small/local models don't follow JSON tool grammar
        reliably and sage's text-format fallback is fine for them. Frontier
        providers (Gemini, OpenAI-compat with strong models) override to
        return True and provide a real `format_tools` implementation.
        """
        return False

    def format_tools(self, specs: list[ToolSpec]) -> dict:
        """Translate ToolSpec list into provider-specific tool descriptor.

        Returns a dict shaped for direct insertion into the provider's API
        payload. Default raises so callers don't silently send malformed
        tool specs.
        """
        raise NotImplementedError(
            f"{self.name} provider does not implement format_tools — check "
            "supports_tools() before calling format_tools()."
        )
