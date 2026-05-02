"""Map from ``CompanyAssetType`` to the concrete ``ChattyAssetModel`` subclass.

Used by event consumers (notably ``asset-embedding-worker``) to upgrade the
raw ``asset`` dict carried inside an ``AssetEvent`` into the correct typed
pydantic instance so they can call model methods like ``embedding_chunks()``
instead of poking at dict internals.

Kept in its own module to avoid import cycles: event classes import from here
at call time via ``_registry()``.
"""

from __future__ import annotations

from typing import Type

from ...base_models.chatty_asset_model import ChattyAssetModel
from .company_assets import CompanyAssetType


def _registry() -> dict[CompanyAssetType, Type[ChattyAssetModel]]:
    """Resolve the registry lazily to keep module import cheap and cycle-free."""
    # Local imports — these models live in sibling packages and some of them
    # import back toward this module graph.
    from .ai_agents_v2.chat_example import ChatExample
    from .ai_agents_v2.context_item import ContextItem
    from .ai_agents_v2.instruction import Instruction
    from .chatty_fast_answers.chatty_fast_answer import ChattyFastAnswer
    from .flow import FlowPreview
    from .product import Product
    from .tag import Tag
    from ..CRM.funnel import Funnel

    return {
        CompanyAssetType.AI_AGENT_CONTEXT: ContextItem,
        CompanyAssetType.AI_AGENT_CHAT_EXAMPLE: ChatExample,
        CompanyAssetType.AI_AGENT_INSTRUCTION: Instruction,
        CompanyAssetType.FAST_ANSWERS: ChattyFastAnswer,
        CompanyAssetType.WORKFLOWS: FlowPreview,
        CompanyAssetType.PRODUCTS: Product,
        CompanyAssetType.TAGS: Tag,
        CompanyAssetType.FUNNELS: Funnel,
    }


def get_asset_model_class(asset_type: CompanyAssetType) -> Type[ChattyAssetModel] | None:
    """Return the concrete model class for ``asset_type``, or ``None`` if unmapped.

    Unmapped types are intentionally allowed — not every ``CompanyAssetType``
    participates in embedding-driven retrieval yet (e.g. ``USERS``, ``CHATS``),
    and callers treat ``None`` as "skip this event".
    """
    return _registry().get(asset_type)
