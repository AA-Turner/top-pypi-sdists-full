"""Prompt blocks: reusable, always-current prompt sections an agent declares as ``{{<name>}}``."""

from matrx_ai.prompt_blocks.conditions import matches
from matrx_ai.prompt_blocks.errors import (
    PromptBlockError,
    PromptBlocksMissing,
    PromptBlockSourceUnavailable,
    PromptBlocksNotResolved,
)
from matrx_ai.prompt_blocks.models import BlockRow, ModelFacts, ResolvedBlock, SkillBody, VariantRow
from matrx_ai.prompt_blocks.resolve import add_block_tools, declared_names, resolve_declared_blocks
from matrx_ai.prompt_blocks.source import BlockSource, get_block_source, set_block_source

__all__ = [
    "BlockRow",
    "BlockSource",
    "ModelFacts",
    "PromptBlockError",
    "PromptBlockSourceUnavailable",
    "PromptBlocksMissing",
    "PromptBlocksNotResolved",
    "ResolvedBlock",
    "SkillBody",
    "VariantRow",
    "add_block_tools",
    "declared_names",
    "get_block_source",
    "matches",
    "resolve_declared_blocks",
    "set_block_source",
]
