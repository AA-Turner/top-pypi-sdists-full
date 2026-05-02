"""
Local Lambda events for the trigger embedding system.

CreateTriggerEvent   — create a brand-new trigger phrase with its linked assets.
UpdateTriggerEvent   — update an existing trigger's phrase and/or linked assets.
DeleteTriggerEvent   — permanently delete a trigger document.
EvaluateTriggerEvent — score all company assets against a phrase (read-only).
GetTriggersEvent     — return all triggers for a company with their linked assets.
"""
from enum import StrEnum
from typing import List, Literal, Optional
from pydantic import BaseModel
from src.models.chatty_trigger import AssetReference


class TriggerEventType(StrEnum):
    CREATE       = "create_trigger"
    UPDATE       = "update_trigger"
    DELETE       = "delete_trigger"
    EVALUATE     = "evaluate_trigger"
    GET_TRIGGERS = "get_triggers"


# Kept for backwards-compatible imports in event_identifier_helper / lambda_function
CREATE_TRIGGER_TYPE       = TriggerEventType.CREATE
UPDATE_TRIGGER_TYPE       = TriggerEventType.UPDATE
DELETE_TRIGGER_TYPE       = TriggerEventType.DELETE
EVALUATE_TRIGGER_TYPE     = TriggerEventType.EVALUATE
GET_TRIGGERS_TYPE         = TriggerEventType.GET_TRIGGERS


class CreateTriggerEvent(BaseModel):
    """
    Create a new trigger and embed its phrase.
    The Lambda generates a new ObjectId for the document.
    """
    type: Literal[TriggerEventType.CREATE] = TriggerEventType.CREATE
    company_id: str
    ai_agent_id: Optional[str] = None
    name: str
    phrase: str
    assets: List[AssetReference]


class UpdateTriggerEvent(BaseModel):
    """
    Update an existing trigger's phrase and/or linked assets.
    Re-embeds the phrase and fully replaces the assets list.
    """
    type: Literal[TriggerEventType.UPDATE] = TriggerEventType.UPDATE
    trigger_id: str
    company_id: str
    ai_agent_id: Optional[str] = None
    name: str
    phrase: str
    assets: List[AssetReference]


class DeleteTriggerEvent(BaseModel):
    """
    Permanently delete a trigger document by its ID.
    """
    type: Literal[TriggerEventType.DELETE] = TriggerEventType.DELETE
    trigger_id: str
    company_id: str


class EvaluateTriggerEvent(BaseModel):
    """
    Read-only. Embed a phrase on the fly and return all company assets ranked
    by similarity score (max of content embedding and any stored trigger embeddings).

    - ai_agent_id: AI components are filtered strictly to that agent,
      and each AI component result carries `active_for_ai_agent` (bool).
    - filter_criteria_ids: when set, only AI components that are always-on
      (empty filter_criteria list) OR have at least one matching filter criteria
      ID are considered. Products and fast answers are not pre-filtered.
    """
    type: Literal[TriggerEventType.EVALUATE] = TriggerEventType.EVALUATE
    company_id: str
    ai_agent_id: str
    filter_criteria_ids: Optional[List[str]] = None
    phrase: str


class GetTriggersEvent(BaseModel):
    """
    Read-only. Return all triggers for a company with their phrase and linked assets.
    When ai_agent_id is provided, only triggers scoped to that agent are returned.
    No embedding computation is performed.
    """
    type: Literal[TriggerEventType.GET_TRIGGERS] = TriggerEventType.GET_TRIGGERS
    company_id: str
    ai_agent_id: Optional[str] = None
