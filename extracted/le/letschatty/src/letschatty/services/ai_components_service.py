from letschatty.models.company.assets.ai_agents_v2.follow_up_strategy import FollowUpStrategy
from letschatty.models.company.assets.ai_agents_v2.context_item import ContextItem
from letschatty.models.company.assets.ai_agents_v2.chat_example import ChatExample
from letschatty.models.base_models.ai_agent_component import AiAgentComponent
from letschatty.models.company.assets.filter_criteria import FilterCriteria

from letschatty.models.company.assets.ai_agents_v2.faq import FAQ
from letschatty.models.utils.custom_exceptions.custom_exceptions import AlreadyCompleted
from letschatty.models.utils.types.identifier import StrObjectId
from typing import Any
from letschatty.models.base_models.ai_agent_component import AiAgentComponentType
import logging
logger = logging.getLogger("AI_COMPONENTS_SERVICE")

class AiComponentsService:

    @staticmethod
    def instantiate_component(component_data: dict) -> Any:

        type = component_data.get("type")
        if type == AiAgentComponentType.FOLLOW_UP_STRATEGY:
            return AiComponentsService.instantiate_follow_up_strategy(component_data)
        elif type == AiAgentComponentType.CONTEXT:
            return AiComponentsService.instantiate_context(component_data)
        elif type == AiAgentComponentType.CHAT_EXAMPLE:
            return AiComponentsService.instantiate_chat_example(component_data)
        elif type == AiAgentComponentType.FAQ:
            return AiComponentsService.instantiate_faq(component_data)
        else:
            raise ValueError(f"Invalid component type: {type}")

    @staticmethod
    def instantiate_follow_up_strategy(component_data: dict) -> FollowUpStrategy:
        return FollowUpStrategy(**component_data)

    @staticmethod
    def instantiate_context(component_data: dict) -> ContextItem:
        return ContextItem(**component_data)

    @staticmethod
    def instantiate_chat_example(component_data: dict) -> ChatExample:
        return ChatExample(**component_data)

    @staticmethod
    def instantiate_faq(component_data: dict) -> FAQ:
        return FAQ(**component_data)

    @staticmethod
    def add_filter_criteria(component: AiAgentComponent, filter_criteria: FilterCriteria) -> None:
        logger.debug(f"Adding filter criteria {filter_criteria.name} ({filter_criteria.id}) to component {component.name} ({component.id})")
        component.filter_criteria.append(filter_criteria.id)

    @staticmethod
    def remove_filter_criteria(component: AiAgentComponent, filter_criteria_id: StrObjectId) -> None:
        try:
            logger.debug(f"Removing filter criteria {filter_criteria_id} from component {component.name} ({component.id})")
            component.filter_criteria.remove(filter_criteria_id)
        except ValueError:
            logger.debug(f"Filter criteria {filter_criteria_id} not found in component {component.name} ({component.id}) - returning 200")
            raise AlreadyCompleted(f"Filter criteria {filter_criteria_id} not found in component {component.id}")
