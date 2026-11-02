"""
Pre-configured Asset Services

This module provides ready-to-use AssetService subclasses for each asset type.
These services include the collection configuration and default cache settings.

API implementations can extend these to add business logic (events, validation, etc.)
"""

from .product_service import ProductService
from .tag_service import TagService
from .user_service import UserService
from .chat_service import ChatAssetService
from .source_service import SourceService
from .flow_service import FlowService
from .sale_service import SaleService
from .contact_point_service import ContactPointService
from .ai_agent_service import AiAgentService
from .fast_answer_service import FastAnswerService
from .topic_service import TopicService
from .filter_criteria_service import FilterCriteriaService

__all__ = [
    'ProductService',
    'TagService',
    'UserService',
    'ChatAssetService',
    'SourceService',
    'FlowService',
    'SaleService',
    'ContactPointService',
    'AiAgentService',
    'FastAnswerService',
    'TopicService',
    'FilterCriteriaService',
]

