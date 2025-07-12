#
# Copyright 2024-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.models.genai.chat_prompt import confidence_scores_trafaret, result_metadata_trafaret
from datarobot.models.genai.comparison_chat import get_entity_id
from datarobot.models.genai.llm_blueprint import vector_database_settings_trafaret
from datarobot.models.genai.playground import Playground
from datarobot.utils.pagination import unpaginate

trace_chat = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("name"): t.String,
    }
).ignore_extra("*")

datarobot_user = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("name"): t.String(allow_blank=True),
    }
).ignore_extra("*")

trace_metadata = t.Dict(
    {
        t.Key("users"): t.List(datarobot_user),
        t.Key("chats"): t.List(trace_chat),
    }
).ignore_extra("*")


prompt_trace = t.Dict(
    {
        t.Key("timestamp"): t.String,
        t.Key("user"): datarobot_user,
        t.Key("chat_prompt_id", optional=True): t.Or(t.String, t.Null),
        t.Key("use_case_id", optional=True): t.Or(t.String, t.Null),
        t.Key("comparison_prompt_id", optional=True): t.Or(t.String, t.Null),
        t.Key("llm_blueprint_id"): t.String,
        t.Key("llm_blueprint_name"): t.String,
        t.Key("llm_name", optional=True): t.Or(t.String, t.Null),
        t.Key("llm_vendor", optional=True): t.Or(t.String, t.Null),
        t.Key("llm_license", optional=True): t.Or(t.String, t.Null),
        t.Key("llm_settings", optional=True): t.Or(t.Dict().allow_extra("*"), t.Null),
        t.Key("chat_name", optional=True): t.Or(t.String, t.Null),
        t.Key("chat_id", optional=True): t.Or(t.String, t.Null),
        t.Key("vector_database_id", optional=True): t.Or(t.String, t.Null),
        t.Key("vector_database_settings", optional=True): t.Or(
            vector_database_settings_trafaret, t.Null
        ),
        t.Key("result_metadata", optional=True): t.Or(
            result_metadata_trafaret, t.Dict().allow_extra("*")
        ),
        t.Key("result_text", optional=True): t.Or(t.String, t.Null),
        t.Key("confidence_scores", optional=True): t.Or(confidence_scores_trafaret, t.Null),
        t.Key("text"): t.String,
        t.Key("execution_status"): t.String,
        t.Key("prompt_type", optional=True): t.Or(t.String, t.Null),
        t.Key("evaluation_dataset_configuration_id", optional=True): t.Or(t.String, t.Null),
        t.Key("warning", optional=True): t.Or(t.String, t.Null),
    }
).ignore_extra("*")


class PromptTrace(APIObject):
    """
    Prompt trace contains aggregated information about a prompt execution.

    Attributes
    ----------
    timestamp : str
        The timestamp of the trace (ISO 8601 formatted).
    user : dict
        The user who submitted the prompt.
    chat_prompt_id : str
        The ID of the chat prompt associated with the trace.
    use_case_id : str
        The ID of the Use Case the playground is in.
    comparison_prompt_id : str
        The ID of the comparison prompts associated with the trace.
    llm_blueprint_id : str
        The ID of the LLM blueprint that the prompt was submitted to.
    llm_blueprint_name: str
        The name of the LLM blueprint.
    llm_name : str
        The name of the LLM in the LLM blueprint.
    llm_vendor : str
        The vendor name of the LLM.
    llm_license : str
        What type of license the LLM has.
    llm_settings : dict or None
        The LLM settings for the LLM blueprint. The specific keys allowed and the
        constraints on the values are defined in the response from `LLMDefinition.list`,
        but this typically has dict fields. Either:
        - system_prompt - The system prompt that influences the LLM responses.
        - max_completion_length - The maximum number of tokens in the completion.
        - temperature - Controls the variability in the LLM response.
        - top_p - Sets whether the model considers next tokens with top_p probability mass.
        or
        - system_prompt - The system prompt that influences the LLM responses.
        - validation_id - The ID of the external model LLM validation.
        - external_llm_context_size - The external LLM's context size, in tokens,
        for external model-based LLM blueprints.
    chat_name: str or None
        The name of the chat associated with the Trace.
    chat_id: str or None
        The ID of the chat associated with the Trace.
    vector_database_id : str or None
        ID of the vector database associated with the LLM blueprint, if any.
    vector_database_settings : VectorDatabaseSettings or None
        The settings for the vector database associated with the LLM blueprint, if any.
    result_metadata : ResultMetadata or None
        Metadata for the result of the prompt submission.
    result_text: str or None
        The result text from the prompt submission.
    confidence_scores: ConfidenceScores or None
        The confidence scores if there is a vector database associated with the prompt.
    text: str
        The prompt text submitted to the LLM.
    execution_status: str
        The execution status of the chat prompt.
    prompt_type: str or None
        The type of prompting strategy, for example history aware.
    evaluation_dataset_configuration_id: str or None
        The ID of the evaluation dataset configuration associated with the trace.
    warning: str or None
        Any warnings associated with the trace.
    """

    _path = "api/v2/genai/playgrounds/{}/trace/"
    _export_path = "api/v2/genai/playgrounds/{}/traceDatasets/"

    _converter = prompt_trace

    def __init__(
        self,
        timestamp: str,
        user: Dict[str, str],
        use_case_id: str,
        llm_blueprint_id: str,
        llm_blueprint_name: str,
        text: str,
        execution_status: str,
        llm_name: Optional[str] = None,
        llm_vendor: Optional[str] = None,
        llm_license: Optional[str] = None,
        chat_prompt_id: Optional[str] = None,
        comparison_prompt_id: Optional[str] = None,
        llm_settings: Optional[Dict[str, Any]] = None,
        chat_name: Optional[str] = None,
        chat_id: Optional[str] = None,
        vector_database_id: Optional[str] = None,
        vector_database_settings: Optional[Dict[str, Any]] = None,
        result_metadata: Optional[Dict[str, Any]] = None,
        result_text: Optional[str] = None,
        confidence_scores: Optional[Dict[str, float]] = None,
        prompt_type: Optional[str] = None,
        evaluation_dataset_configuration_id: Optional[str] = None,
        warning: Optional[str] = None,
    ):
        self.timestamp = timestamp
        self.user = user
        self.chat_prompt_id = (chat_prompt_id,)
        self.use_case_id = use_case_id
        self.comparison_prompt_id = comparison_prompt_id
        self.llm_blueprint_id = llm_blueprint_id
        self.llm_blueprint_name = llm_blueprint_name
        self.llm_name = llm_name
        self.llm_vendor = llm_vendor
        self.llm_license = llm_license
        self.llm_settings = llm_settings
        self.chat_name = chat_name
        self.chat_id = chat_id
        self.vector_database_id = vector_database_id
        self.vector_database_settings = vector_database_settings
        self.result_metadata = result_metadata
        self.result_text = result_text
        self.confidence_scores = confidence_scores
        self.text = text
        self.execution_status = execution_status
        self.prompt_type = prompt_type
        self.evaluation_dataset_configuration_id = evaluation_dataset_configuration_id
        self.warning = warning

    @classmethod
    def list(cls, playground: Union[str, Playground]) -> List[PromptTrace]:
        """
        List all prompt traces for a playground.

        Parameters
        ----------
        playground: str
            The ID of the playground to list prompt traces for.

        Returns
        -------
        prompt_traces: list[PromptTrace]
            List of prompt traces for the playground.
        """
        playground_id = get_entity_id(playground)
        url = f"{cls._client.domain}/{cls._path.format(playground_id)}"
        response = unpaginate(url, None, cls._client)
        return [cls.from_server_data(trace) for trace in response]

    @classmethod
    def export_to_ai_catalog(cls, playground: Union[str, Playground]) -> Any:
        """
        Export prompt traces to AI Catalog as a CSV.

        Parameters
        ----------
        playground: str
            The ID of the playground to export prompt traces for.

        Returns
        -------
        status_url: str
            The URL where the status of the job can be monitored
        """
        playground_id = get_entity_id(playground)
        url = f"{cls._client.domain}/{cls._export_path.format(playground_id)}"
        response = cls._client.post(url)
        return response.headers["Location"]


class TraceMetadata(APIObject):
    """
    Trace metadata contains information about all the users and chats that are relevant to
    this playground.

    Attributes
    ----------
    users : list[dict]
        The users who submitted the prompt.
    """

    _path = "api/v2/genai/playgrounds/{}/trace/metadata/"

    _converter = trace_metadata

    def __init__(self, users: List[Dict[str, str]], chats: List[Dict[str, str]]):
        self.users = users
        self.chats = chats

    @classmethod
    def get(cls, playground: Union[str, Playground]) -> TraceMetadata:
        """
        Get trace metadata for a playground.

        Parameters
        ----------
        playground: str
            The ID of the playground to get trace metadata for.

        Returns
        -------
        trace_metadata: TraceMetadata
            The trace metadata for the playground.
        """
        playground_id = get_entity_id(playground)
        url = f"{cls._client.domain}/{cls._path.format(playground_id)}"
        response = cls._client.get(url)
        return cls.from_server_data(response.json())
