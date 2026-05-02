"""
Read-only Assets Collections Container

This module provides a singleton container class that gives microservices
read-only access to asset data using pre-configured AssetCollection subclasses.
Perfect for services that only need to read asset data without CRUD operations.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Any
import logging

# Import base components
from ...models.data_base.mongo_connection import MongoConnection
from ...models.base_models.singleton import SingletonMeta

# Import pre-configured collection subclasses
from .collections import (
    ProductCollection,
    TagCollection,
    UserCollection,
    ChatCollection,
    SourceCollection,
    FlowCollection,
    SaleCollection,
    ContactPointCollection,
    AiAgentCollection,
    FilterCriteriaCollection,
    AiComponentCollection
)

# Import asset models for type hints
from ...models.company.assets.product import Product
from ...models.company.assets.tag import Tag
from ...models.company.assets.users.user import User
from ...models.chat.chat import Chat
from ...models.analytics.sources import SourceBase
from ...models.company.assets.flow import FlowPreview
from ...models.company.assets.sale import Sale
from ...models.company.assets.contact_point import ContactPoint
from ...models.company.assets.ai_agents_v2.chatty_ai_agent import ChattyAIAgent
from ...models.company.assets.filter_criteria import FilterCriteria

if TYPE_CHECKING:
    pass

logger = logging.getLogger("AssetsCollections")


class AssetsCollections(metaclass=SingletonMeta):
    """
    Read-only singleton container for accessing asset collections across microservices.

    This class provides simple read access to various asset types without the overhead
    of the full AssetService (no caching, no events, no write operations).

    Usage:
        assets = AssetsCollections(connection)
        product = assets.get_product_by_id(product_id)
        tag = assets.get_tag_by_id(tag_id)
    """

    def __init__(self, connection: MongoConnection):
        """
        Initialize all asset collections using pre-configured collection subclasses.

        Args:
            connection: MongoConnection instance to use for database access
        """
        logger.debug("Initializing AssetsCollections")

        # Initialize all collections using pre-configured subclasses
        # Each collection subclass already knows its collection name, asset type,
        # preview type, and create_instance_method
        self.products = ProductCollection(connection)
        self.tags = TagCollection(connection)
        self.users = UserCollection(connection)
        self.chats = ChatCollection(connection)
        self.sources = SourceCollection(connection)
        self.flows = FlowCollection(connection)
        self.sales = SaleCollection(connection)
        self.contact_points = ContactPointCollection(connection)
        self.ai_agents = AiAgentCollection(connection)
        self.filter_criterias = FilterCriteriaCollection(connection)
        self.ai_components = AiComponentCollection(connection)

        logger.debug("AssetsCollections initialized successfully")

    # Convenience getter methods for easy access

    async def get_product_by_id(self, id: str) -> Product:
        """Get a product by ID."""
        return await self.products.get_by_id(id)

    async def get_tag_by_id(self, id: str) -> Tag:
        """Get a tag by ID."""
        return await self.tags.get_by_id(id)

    async def get_user_by_id(self, id: str) -> User:
        """Get a user by ID."""
        return await self.users.get_by_id(id)

    async def get_chat_by_id(self, id: str) -> Chat:
        """Get a chat by ID."""
        return await self.chats.get_by_id(id)

    async def get_source_by_id(self, id: str) -> SourceBase:
        """Get a source by ID."""
        return await self.sources.get_by_id(id)

    async def get_flow_by_id(self, id: str) -> FlowPreview:
        """Get a flow by ID."""
        return await self.flows.get_by_id(id)

    async def get_sale_by_id(self, id: str) -> Sale:
        """Get a sale by ID."""
        return await self.sales.get_by_id(id)

    async def get_contact_point_by_id(self, id: str) -> ContactPoint:
        """Get a contact point by ID."""
        return await self.contact_points.get_by_id(id)

    async def get_ai_agent_by_id(self, id: str) -> ChattyAIAgent:
        """Get an AI agent by ID."""
        return await self.ai_agents.get_by_id(id)

    async   def get_filter_criteria_by_id(self, id: str) -> FilterCriteria:
        """Get a filter criteria by ID."""
        return await self.filter_criterias.get_by_id(id)

    async def get_filter_criterias_by_ids(self, ids: list[str]) -> list[FilterCriteria]:
        """Get multiple filter criterias by their IDs in a single query."""
        return await self.filter_criterias.get_by_ids(ids=ids)

    async def get_ai_components_by_ids(self, ids: list[str]) -> list[Any]:
        """Get multiple AI components by their IDs in a single query."""
        return await self.ai_components.get_by_ids(ids=ids)

