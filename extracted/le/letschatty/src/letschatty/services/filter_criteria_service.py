from letschatty.models.company.assets.filter_criteria import FilterCriteria, Attribute, AttributeType
from letschatty.models.chat.chat import Chat
from typing import List, Type
from letschatty.models.chat.quality_scoring import QualityScore
import logging
logger = logging.getLogger("FilterCriteriaService")

class FilterCriteriaService:

    @staticmethod
    def chat_matches_any_filter_criteria(filter_criterias: List[FilterCriteria], chat:Chat) -> bool:
        if not filter_criterias:
            return True
        logger.debug(f"Validating {len(filter_criterias)} filter criterias for chat: {chat.id} | client {chat.client.name}")
        chat_matches_any_filter_criteria = any(FilterCriteriaService._are_ALL_AND_filter_matched(filter_criteria, chat) for filter_criteria in filter_criterias)
        if chat_matches_any_filter_criteria:
            logger.debug(f"Chat matches at least one filter criteria")
        else:
            logger.debug(f"Chat does not match any filter criteria")
        return chat_matches_any_filter_criteria

    @staticmethod
    def matching_score_filter_criteria(filter_criterias: List[FilterCriteria], chat:Chat) -> int:
        if not filter_criterias:
            logger.debug(f"No filter criterias found, considered default follow up strategy")
            return 1
        if not any(FilterCriteriaService._are_ALL_AND_filter_matched(filter_criteria, chat) for filter_criteria in filter_criterias):
            logger.debug(f"Chat does not match any filter criteria")
            return 0
        matching_score = 1 #is the score for the default follow up strategy
        for filter_criteria in filter_criterias:
            if FilterCriteriaService._are_ALL_AND_filter_matched(filter_criteria, chat):
                matching_score += 1
        return matching_score

    @staticmethod
    def _is_ANY_OR_filter_matched(or_filters: List[Attribute], chat:Chat) -> bool:
        if not or_filters:
            logger.debug(f"No OR filters found for chat: {chat.id} | client {chat.client.name}")
            return True
        if not any(FilterCriteriaService._is_item_related_to_chat(or_filter, chat) for or_filter in or_filters):
            logger.debug(f"None of the OR attributes matched")
            return False
        logger.debug(f"At least one of the OR attributes matched")
        return True

    @staticmethod
    def _are_ALL_AND_filter_matched(filter_criteria: FilterCriteria, chat:Chat) -> bool:
        logger.debug(f"Validating filter criteria: {filter_criteria.name} for chat: {chat.id} | client {chat.client.name}")
        if not filter_criteria.filters:
            logger.debug(f"No filters found for filter criteria: {filter_criteria.name}")
            return True
        if not all(FilterCriteriaService._is_ANY_OR_filter_matched(or_filters, chat) for or_filters in filter_criteria.filters):
            logger.debug(f"All required AND filters were not matched for filter criteria: {filter_criteria.name}")
            return False
        logger.debug(f"All required AND filters were matched for filter criteria: {filter_criteria.name}")
        return True

    @staticmethod
    def _is_item_related_to_chat(attribute : Attribute, chat:Chat) -> bool:
        if attribute.attribute_type == AttributeType.TAGS:
            return attribute.attribute_id in chat.assigned_tag_ids
        if attribute.attribute_type == AttributeType.PRODUCTS:
            return attribute.attribute_id in chat.assigned_product_ids or attribute.attribute_id in chat.bought_product_ids
        if attribute.attribute_type == AttributeType.SOURCES:
            return attribute.attribute_id in chat.assigned_source_ids
        if attribute.attribute_type == AttributeType.QUALITY_SCORE:
            return QualityScore(chat.client.lead_quality) == QualityScore(attribute.attribute_id)
        if attribute.attribute_type == AttributeType.SALES:
            return attribute.attribute_id in chat.bought_product_ids
        if attribute.attribute_type == AttributeType.BUSINESS_AREAS:
            raise NotImplementedError("Business areas are not supported yet")
        if attribute.attribute_type == AttributeType.FUNNELS:
            raise NotImplementedError("Funnels are not supported yet")
        return False


    @staticmethod
    def instantiate_filter_criteria(filter_criteria_data: dict) -> FilterCriteria:
        return FilterCriteria(**filter_criteria_data)