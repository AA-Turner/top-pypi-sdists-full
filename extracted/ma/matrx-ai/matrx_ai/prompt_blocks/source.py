"""The host seam: where block rows, skill bodies and model facts come from.

SERVER host: ORM reads (aidream). CLIENT host (matrx-local): ``GET /prompt-blocks/resolve``.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from matrx_ai.prompt_blocks.models import BlockRow, ModelFacts, SkillBody


@runtime_checkable
class BlockSource(Protocol):
    async def candidates(
        self, names: list[str], *, organization_id: str | None, personal_user_id: str | None
    ) -> list[BlockRow]:
        """Every live row for ``names`` at the personal (only when ``personal_user_id``),
        run-organization and system levels, each tagged with its ``level``."""
        ...

    async def skill(self, skill_id: str) -> SkillBody | None: ...

    async def model_facts(self, model: str) -> ModelFacts | None: ...

    async def personal_rung_enabled(self, organization_id: str | None) -> bool: ...


_SOURCE: dict[str, BlockSource | None] = {"source": None}


def set_block_source(source: BlockSource | None) -> None:
    _SOURCE["source"] = source


def get_block_source() -> BlockSource | None:
    return _SOURCE["source"]
