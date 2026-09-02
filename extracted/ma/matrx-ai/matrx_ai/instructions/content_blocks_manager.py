"""Content-block loading for system instructions.

Canonical backing table: ``skill.render_definition`` (public.content_blocks was
canonicalized onto it in the 2026-07/08 render-blocks unification; the DB table
is retired). The public API here keeps the "content blocks" vocabulary because
that is what the SystemInstruction field (`content_blocks: list[str]`) and the
``<<MATRX>><<CONTENT_BLOCKS>>`` template syntax are named on the wire.
"""

import uuid
from typing import Any

from matrx_ai.db._registry import get_extra, get_model
from matrx_orm import BaseManager


def _get_RenderDefinitionDTO():
    return get_extra("RenderDefinitionDTO")


def _get_RenderDefinition():
    return get_model("RenderDefinition")


def is_valid_uuid(value):
    """Check if a string is a valid UUID."""
    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, AttributeError):
        return False


class ContentBlocksBase(BaseManager):
    view_class = None  # DTO is used by default

    def __init__(
        self,
        view_class: type[Any] | None = None,
        fetch_on_init_limit: int = 200,
        fetch_on_init_with_warnings_off: str = "YES_I_KNOW_WHAT_IM_DOING_TURN_OFF_WARNINGS_FOR_LIMIT_100",
    ):
        if view_class is not None:
            self.view_class = view_class
        super().__init__(
            _get_RenderDefinition(),
            dto_class=_get_RenderDefinitionDTO(),
            fetch_on_init_limit=fetch_on_init_limit,
            FETCH_ON_INIT_WITH_WARNINGS_OFF=fetch_on_init_with_warnings_off,
        )

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item) -> None:
        pass

    async def create_content_blocks(self, **data):
        return await self.create_item(**data)

    async def delete_content_blocks(self, id):
        return await self.delete_item(id)

    async def get_content_blocks_with_all_related(self, id):
        return await self.get_item_with_all_related(id)

    async def load_content_blocks_by_id(self, id):
        return await self.load_by_id(id)

    async def load_content_blocks(self, use_cache=True, **kwargs):
        return await self.load_item(use_cache, **kwargs)

    async def update_content_blocks(self, id, **updates):
        return await self.update_item(id, **updates)

    async def load_content_block(self, **kwargs):
        return await self.load_items(**kwargs)

    async def filter_content_block(self, **kwargs):
        return await self.filter_items(**kwargs)

    async def load_content_block_by_category_id(self, category_id):
        return await self.load_items(category_id=category_id)

    async def filter_content_block_by_category_id(self, category_id):
        return await self.filter_items(category_id=category_id)

    async def load_content_block_by_ids(self, ids):
        return await self.load_items_by_ids(ids)

    @property
    def active_content_blocks_ids(self):
        return self.active_item_ids


class ContentBlocksManager(ContentBlocksBase):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()

    async def _initialize_runtime_data(self, item) -> None:
        pass

    async def get_template_text(self, id_or_block_id: str):
        if is_valid_uuid(id_or_block_id):
            block = await self.add_active_by_id_or_not(id_or_block_id)
            if block:
                return block.template
            return None
        else:
            models = await self.load_items(block_id=id_or_block_id)
            if models:
                return models[0].template  # Return the first match
            return None


content_blocks_manager_instance = None


def get_content_blocks_manager():
    global content_blocks_manager_instance
    if content_blocks_manager_instance is None:
        content_blocks_manager_instance = ContentBlocksManager()
    return content_blocks_manager_instance


if __name__ == "__main__":
    import asyncio

    from matrx_utils import clear_terminal

    clear_terminal()
    block = asyncio.run(get_content_blocks_manager().get_template_text("flashcards"))
    print(block)
