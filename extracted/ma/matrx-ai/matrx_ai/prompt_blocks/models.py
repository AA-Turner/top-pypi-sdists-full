"""Plain shapes the BlockSource hands the resolver."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

Level = Literal["personal", "organization", "system"]
LEVEL_ORDER: tuple[Level, ...] = ("personal", "organization", "system")


@dataclass(frozen=True)
class VariantRow:
    id: str
    label: str
    condition: dict[str, Any]
    content: str
    sort_order: int = 0


@dataclass(frozen=True)
class BlockRow:
    id: str
    name: str
    level: Level
    content: str
    source_kind: str = "authored"
    source_ref: str | None = None
    bound_tool: str | None = None
    variants: tuple[VariantRow, ...] = ()


@dataclass(frozen=True)
class SkillBody:
    skill_id: str
    body: str
    allowed_tools: tuple[str, ...] = ()
    disable_auto_invocation: bool = False


@dataclass(frozen=True)
class ModelFacts:
    """The effective model as the condition grammar sees it."""

    name: str
    provider: str | None = None
    latest: bool = False
    names: frozenset[str] = field(default_factory=frozenset)  # model name, id and alias names


@dataclass
class ResolvedBlock:
    name: str
    text: str
    level: Level
    block_id: str
    variant_id: str | None
    source_kind: str
    bound_tool: str | None
    skill_id: str | None = None
    #: Why the block sends nothing, said out loud (Model view, log); ``None`` when it is on.
    off: str | None = None

    def report(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "level": self.level,
            "block_id": self.block_id,
            "variant_id": self.variant_id,
            "source_kind": self.source_kind,
            "bound_tool": self.bound_tool,
            "skill_id": self.skill_id,
            "chars": len(self.text),
            "off": self.off,
        }
