from typing import List, Optional

from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from pydantic import BaseModel, Field

from whiskerrag_types.model.retrieval import RetrievalConfig


class KnowledgeScope(BaseModel):
    space_ids: Optional[List[str]] = None
    auth_info: str


class ProResearchRequest(BaseModel):
    messages: List[ChatCompletionMessageParam] = Field(
        default=[],
        json_schema_extra={"description": "The messages to be sent to the agent."},
    )
    model: str = Field(
        default="wohu_qwen3_235b_a22b",
        json_schema_extra={
            "description": "The name of the language model to use for the agent's query generation."
        },
    )
    number_of_initial_queries: int = Field(
        default=3,
        json_schema_extra={
            "description": "The number of initial search queries to generate."
        },
    )

    max_research_loops: int = Field(
        default=2,
        json_schema_extra={
            "description": "The maximum number of research loops to perform."
        },
    )

    enable_knowledge_retrieval: bool = Field(
        default=True,
        json_schema_extra={
            "description": "Whether to enable knowledge retrieval functionality."
        },
    )

    enable_web_search: bool = Field(
        default=False,
        json_schema_extra={
            "description": "Whether to enable web search functionality."
        },
    )

    knowledge_scope_list: List[KnowledgeScope] = Field(
        default=[],
        json_schema_extra={"description": "List of knowledge scopes to search within."},
    )

    knowledge_retrieval_config: Optional[RetrievalConfig] = Field(
        default=None,
        json_schema_extra={"description": "Knowledge retrieval configuration."},
    )
