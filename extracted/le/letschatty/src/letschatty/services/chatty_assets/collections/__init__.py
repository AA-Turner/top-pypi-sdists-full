"""
Asset Collection Subclasses

This module provides pre-configured AssetCollection subclasses for each asset type.
These ensure consistency between the API and microservices by defining the collection
configuration (collection name, asset type, preview type, create_instance_method) once.
"""

from .product_collection import ProductCollection
from .tag_collection import TagCollection
from .user_collection import UserCollection
from .chat_collection import ChatCollection
from .chat_messages_collection import ChatMessagesCollection
from .client_collection import ClientCollection
from .chat_flow_state_collection import ChatFlowStateCollection
from .source_collection import SourceCollection
from .flow_collection import FlowCollection
from .sale_collection import SaleCollection
from .contact_point_collection import ContactPointCollection
from .ai_agent_collection import AiAgentCollection
from .fast_answer_collection import FastAnswerCollection
from .topic_collection import TopicCollection
from .filter_criteria_collection import FilterCriteriaCollection
from .ai_component_collection import AiComponentCollection
from .form_field_collection import FormFieldCollection
from .media_asset_collection import MediaAssetCollection

__all__ = [
    'ProductCollection',
    'TagCollection',
    'UserCollection',
    'ChatCollection',
    'ChatMessagesCollection',
    'ClientCollection',
    'ChatFlowStateCollection',
    'SourceCollection',
    'FlowCollection',
    'SaleCollection',
    'ContactPointCollection',
    'AiAgentCollection',
    'FastAnswerCollection',
    'TopicCollection',
    'FilterCriteriaCollection',
    'AiComponentCollection',
    'FormFieldCollection',
    'MediaAssetCollection',
]

