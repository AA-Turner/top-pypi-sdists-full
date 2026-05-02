from __future__ import annotations
from zoneinfo import ZoneInfo
from letschatty.models.base_models.ai_agent_component import AiAgentComponentType
from letschatty.models.company.assets.ai_agents_v2.knowleadge_base_components import KnowleadgeBaseComponent
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Any, ClassVar, Optional
from enum import StrEnum
from typing import Dict
from letschatty.models.base_models.ai_agent_component import AiAgentComponent
from letschatty.models.utils.types.identifier import StrObjectId
from letschatty.models.company.assets.ai_agents_v2.chat_example import ChatExample, ExampleElement

import logging

logger = logging.getLogger("chat_example_test")

class ChatExampleTestCaseStatus(StrEnum):
    """Status of a chat example test"""
    RUNNING = "running"
    FAILED = "failed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    PENDING = "pending"

class ChatExampleTestCase(AiAgentComponent):
    """Example conversation for training the AI agent"""
    content: List[ExampleElement] = Field(..., default_factory=list, description="Sequence of elements in this example")
    chat_example_id: StrObjectId = Field(..., description="The id of the chat example")
    accuracy: Optional[float] = Field(default=None, description="The accuracy of the example")
    status: ChatExampleTestCaseStatus = Field(default=ChatExampleTestCaseStatus.PENDING, description="The status of the example test")
    start_time: Optional[datetime] = Field(default=None, description="The start time of the example test")
    end_time: Optional[datetime] = Field(default=None, description="The end time of the example test")
    ai_agent_id: StrObjectId = Field(..., description="The id of the ai agent")
    comments: Optional[str] = Field(default=None, description="The comments of the example test")
    last_processed_interaction_index: int = Field(default=0, description="The index of the interaction in the chat example that was last processed")
    is_training_example: bool = Field(description="Whether the test case is a training example")
    knowleadge_base: List[KnowleadgeBaseComponent] = Field(default_factory=list, description="The knowleadge base of the test case", alias="knowledge_base")

    @classmethod
    def from_chat_example(cls, chat_example: ChatExample, ai_agent_id: StrObjectId) -> List[ChatExampleTestCase]:
        """Create a test case from a chat example"""
        logger.debug(f"Creating test cases from chat example {chat_example.name} {chat_example.id} for ai agent {ai_agent_id}")
        test_cases = []
        if not chat_example.filter_criteria:
            logger.debug(f"Creating test case from chat example {chat_example.name} {chat_example.id} for ai agent {ai_agent_id} and no filter criteria")
            test_case = cls.from_chat_example_and_filter_criteria(chat_example, ai_agent_id=ai_agent_id, filter_criteria_id=None)
            test_cases.append(test_case)
            return test_cases
        for filter_criteria_id in chat_example.filter_criteria:
            logger.debug(f"creating test case from chat example {chat_example.name} {chat_example.id} for ai agent {ai_agent_id} and filter criteria {filter_criteria_id}")
            test_case = cls.from_chat_example_and_filter_criteria(chat_example, ai_agent_id=ai_agent_id, filter_criteria_id=filter_criteria_id)
            test_cases.append(test_case)
        logger.debug(f"Created {len(test_cases)} test cases from chat example {chat_example.name} {chat_example.id} for ai agent {ai_agent_id}")
        return test_cases

    @classmethod
    def from_chat_example_and_filter_criteria(cls, chat_example: ChatExample, ai_agent_id: StrObjectId, filter_criteria_id: Optional[StrObjectId]) -> ChatExampleTestCase:
        """Create a test case from a chat example and a filter criteria"""
        return cls(
            chat_example_id=chat_example.id,
            ai_agent_id=ai_agent_id,
            filter_criteria=[filter_criteria_id] if filter_criteria_id else [],
            status=ChatExampleTestCaseStatus.PENDING,
            start_time=None,
            end_time=None,
            company_id=chat_example.company_id,
            name=chat_example.name,
            updated_at=datetime.now(ZoneInfo("UTC")),
            created_at=datetime.now(ZoneInfo("UTC")),
            type=AiAgentComponentType.TEST_CASE,
            is_training_example=chat_example.is_training_example
        )

    @property
    def filter_criteria_id(self) -> Optional[StrObjectId]:
        return self.filter_criteria[0] if self.filter_criteria else None