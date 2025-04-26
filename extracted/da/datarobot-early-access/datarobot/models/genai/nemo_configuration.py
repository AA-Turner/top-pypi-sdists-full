#
# Copyright 2024 DataRobot, Inc. and its affiliates.
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

from typing import Any, Dict, Union

import trafaret as t

from datarobot.enums import enum_to_list, NemoLLMType
from datarobot.models.api_object import APIObject
from datarobot.models.genai.comparison_chat import get_entity_id
from datarobot.models.genai.playground import Playground
from datarobot.models.genai.playground_moderation_configuration import (
    moderation_configuration_without_id,
    ModerationConfigurationWithoutId,
)

nemo_llm_configuration = t.Dict(
    {
        t.Key("llm_type"): t.Enum(*enum_to_list(NemoLLMType)),
        t.Key("openai_api_key_id"): t.String,
        t.Key("openai_api_base", optional=True): t.Or(t.String, t.Null),
        t.Key("openai_api_deployment_id", optional=True): t.Or(t.String, t.Null),
    }
).ignore_extra("*")

nemo_file_contents = t.Dict(
    {
        t.Key("config_yaml_file_contents"): t.String,
        t.Key("flow_definition_file_contents"): t.String,
        t.Key("prompts_file_contents"): t.String,
    }
).ignore_extra("*")

nemo_file_contents_for_response = t.Dict(
    {
        t.Key("actions_file_contents"): t.String,
        t.Key("config_yaml_file_contents"): t.String,
        t.Key("flow_definition_file_contents"): t.String,
        t.Key("prompts_file_contents"): t.String,
    }
).ignore_extra("*")

nemo_configuration = t.Dict(
    {
        t.Key("prompt_pipeline_metric_name", optional=True): t.Or(t.String, t.Null),
        t.Key("prompt_pipeline_files", optional=True): t.Or(
            nemo_file_contents_for_response, t.Null
        ),
        t.Key("prompt_llm_configuration", optional=True): t.Or(nemo_llm_configuration, t.Null),
        t.Key("prompt_moderation_configuration", optional=True): t.Or(
            moderation_configuration_without_id, t.Null
        ),
        t.Key("prompt_pipeline_template_id", optional=True): t.Or(t.String, t.Null),
        t.Key("response_pipeline_metric_name", optional=True): t.Or(t.String, t.Null),
        t.Key("response_pipeline_files", optional=True): t.Or(
            nemo_file_contents_for_response, t.Null
        ),
        t.Key("response_llm_configuration", optional=True): t.Or(nemo_llm_configuration, t.Null),
        t.Key("response_moderation_configuration", optional=True): t.Or(
            moderation_configuration_without_id, t.Null
        ),
        t.Key("response_pipeline_template_id", optional=True): t.Or(t.String, t.Null),
        t.Key("blocked_terms_file_contents"): t.String,
    }
).ignore_extra("*")


class NemoLLMConfiguration(APIObject):
    """
    Configuration for the LLM model to be used for Nemo Pipeline.

    Attributes
    ----------
    llm_type : NemoLLMType
        The type of LLM model.
    openai_api_key_id : str
        The ID of the credential in the Datarobot credential manager for the API token.
    openai_api_base : Optional[str]
        The base URL for Azure OpenAI API.
    openai_api_deployment_id : Optional[str]
        The deployment ID for Azure OpenAI API.

    """

    _converter = nemo_llm_configuration

    def __init__(
        self,
        llm_type: NemoLLMType,
        openai_api_key_id: str,
        openai_api_base: Union[str, None] = None,
        openai_api_deployment_id: Union[str, None] = None,
    ):
        self.llm_type = llm_type
        self.openai_api_key_id = openai_api_key_id
        self.openai_api_base = openai_api_base
        self.openai_api_deployment_id = openai_api_deployment_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "llm_type": self.llm_type,
            "openai_api_key_id": self.openai_api_key_id,
            "openai_api_base": self.openai_api_base,
            "openai_api_deployment_id": self.openai_api_deployment_id,
        }


class NemoFileContents(APIObject):
    """
    String representation of the contents of files used in the Nemo Pipeline.
    This is the base user configurable values.

    Attributes
    ----------
    config_yaml_file_contents : str
        The contents of the config YAML file.
    flow_definition_file_contents : str
        The contents of the flow definition fle.
    prompts_file_contents : str
        The contents of the prompts file.
    """

    _converter = nemo_file_contents

    def __init__(
        self,
        config_yaml_file_contents: str,
        flow_definition_file_contents: str,
        prompts_file_contents: str,
    ):
        self.config_yaml_file_contents = config_yaml_file_contents
        self.flow_definition_file_contents = flow_definition_file_contents
        self.prompts_file_contents = prompts_file_contents

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def to_dict(self) -> dict[str, str]:
        return {
            "config_yaml_file_contents": self.config_yaml_file_contents,
            "flow_definition_file_contents": self.flow_definition_file_contents,
            "prompts_file_contents": self.prompts_file_contents,
        }


class NemoFileContentsResponse(APIObject):
    """
    String representation of the contents of files used in the Nemo Pipeline.
    This is the files actually used by nemo, with the included actions python file.

    Attributes
    ----------
    actions_file_contents : str
        The contents of the actions python file.
    config_yaml_file_contents : str
        The contents of the config YAML file.
    flow_definition_file_contents : str
        The contents of the flow definition fle.
    prompts_file_contents : str
        The contents of the prompts file.
    """

    _converter = nemo_file_contents_for_response

    def __init__(
        self,
        actions_file_contents: str,
        config_yaml_file_contents: str,
        flow_definition_file_contents: str,
        prompts_file_contents: str,
    ):
        self.actions_file_contents = actions_file_contents
        self.config_yaml_file_contents = config_yaml_file_contents
        self.flow_definition_file_contents = flow_definition_file_contents
        self.prompts_file_contents = prompts_file_contents

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def to_dict(self) -> dict[str, str]:
        return {
            "actions_file_contents": self.actions_file_contents,
            "config_yaml_file_contents": self.config_yaml_file_contents,
            "flow_definition_file_contents": self.flow_definition_file_contents,
            "prompts_file_contents": self.prompts_file_contents,
        }


class NemoConfiguration(APIObject):
    """
    Configuration for the Nemo Pipeline.

    Attributes
    ----------
    prompt_pipeline_metric_name : Optional[str]
        The name of the metric for the prompt pipeline.
    prompt_pipeline_files : NemoFileContentsResponse, optional
        The files used in the prompt pipeline.
    prompt_llm_configuration : NemoLLMConfiguration, optional
        The LLM configuration for the prompt pipeline.
    prompt_moderation_configuration : ModerationConfigurationWithoutID, optional
        The moderation configuration for the prompt pipeline.
    prompt_pipeline_template_id : Optional[str]
        The ID of the prompt pipeline template. This parameter defines the actions.py file.
    response_pipeline_metric_name : Optional[str]
        The name of the metric for the response pipeline.
    response_pipeline_files : NemoFileContentsResponse, optional
        The files used in the response pipeline.
    response_llm_configuration : NemoLLMConfiguration, optional
        The LLM configuration for the response pipeline.
    response_moderation_configuration : ModerationConfigurationWithoutID, optional
        The moderation configuration for the response pipeline.
    response_pipeline_template_id : Optional[str]
        The ID of the response pipeline template. This parameter defines the actions.py file.
    blocked_terms_file_contents : str
        The contents of the blocked terms file.  This is shared between the prompt and response pipelines.
    """

    _path = "api/v2/genai/playgrounds/{}/nemoConfiguration/"

    _converter = nemo_configuration
    schema = _converter

    def __init__(
        self,
        blocked_terms_file_contents: str,
        prompt_pipeline_metric_name: Union[str, None] = None,
        prompt_pipeline_files: Union[Dict[str, str], None] = None,
        prompt_llm_configuration: Union[Dict[str, Any], None] = None,
        prompt_moderation_configuration: Union[Dict[str, Any], None] = None,
        prompt_pipeline_template_id: Union[str, None] = None,
        response_pipeline_metric_name: Union[str, None] = None,
        response_pipeline_files: Union[Dict[str, str], None] = None,
        response_llm_configuration: Union[Dict[str, Any], None] = None,
        response_moderation_configuration: Union[Dict[str, Any], None] = None,
        response_pipeline_template_id: Union[str, None] = None,
    ):
        def _get_obj(value: Union[Dict[str, Any], None], obj: Any) -> Any:
            return obj.from_server_data(value) if value is not None else None

        self.prompt_pipeline_metric_name = prompt_pipeline_metric_name
        self.prompt_pipeline_files = _get_obj(prompt_pipeline_files, NemoFileContentsResponse)
        self.prompt_llm_configuration = _get_obj(prompt_llm_configuration, NemoLLMConfiguration)
        self.prompt_moderation_configuration = _get_obj(
            prompt_moderation_configuration, ModerationConfigurationWithoutId
        )
        self.prompt_pipeline_template_id = prompt_pipeline_template_id
        self.response_pipeline_metric_name = response_pipeline_metric_name
        self.response_pipeline_files = _get_obj(response_pipeline_files, NemoFileContentsResponse)
        self.response_llm_configuration = _get_obj(response_llm_configuration, NemoLLMConfiguration)
        self.response_moderation_configuration = _get_obj(
            response_moderation_configuration, ModerationConfigurationWithoutId
        )
        self.response_pipeline_template_id = response_pipeline_template_id
        self.blocked_terms_file_contents = blocked_terms_file_contents

    @classmethod
    def get(cls, playground: Union[str, Playground]) -> NemoConfiguration:
        """
        Get the Nemo configuration for a playground.

        Parameters
        ----------
        playground: str or Playground
            The playground to get the configuration for

        Returns
        -------
        NemoConfiguration
            The Nemo configuration for the playground.

        """
        playground_id = get_entity_id(playground)
        url = f"{cls._client.domain}/{cls._path.format(playground_id)}"
        response = cls._client.get(url)
        return cls.from_server_data(response.json())

    @classmethod
    def upsert(
        cls,
        playground: Union[str, Playground],
        blocked_terms_file_contents: str,
        prompt_pipeline_metric_name: Union[str, None] = None,
        prompt_pipeline_files: Union[NemoFileContents, None] = None,
        prompt_llm_configuration: Union[NemoLLMConfiguration, None] = None,
        prompt_moderation_configuration: Union[ModerationConfigurationWithoutId, None] = None,
        prompt_pipeline_template_id: Union[str, None] = None,
        response_pipeline_metric_name: Union[str, None] = None,
        response_pipeline_files: Union[NemoFileContents, None] = None,
        response_llm_configuration: Union[NemoLLMConfiguration, None] = None,
        response_moderation_configuration: Union[ModerationConfigurationWithoutId, None] = None,
        response_pipeline_template_id: Union[str, None] = None,
    ) -> NemoConfiguration:
        """
        Create or update the nemo configuration for a playground.

        Parameters
        ----------
        playground: str or Playground
            The playground for the configuration
        blocked_terms_file_contents: str
            The contents of the blocked terms file.
        prompt_pipeline_metric_name: Optional[str]
            The name of the metric for the prompt pipeline.
        prompt_pipeline_files: NemoFileContents, optional
            The files used in the prompt pipeline.
        prompt_llm_configuration: NemoLLMConfiguration, optional
            The LLM configuration for the prompt pipeline.
        prompt_moderation_configuration: ModerationConfigurationWithoutID, optional
            The moderation configuration for the prompt pipeline.
        prompt_pipeline_template_id: Optional[str]
            The ID of the prompt pipeline template, this will define the action.py file.
        response_pipeline_metric_name: Optional[str]
            The name of the metric for the response pipeline.
        response_pipeline_files: NemoFileContents, optional
            The files used in the response pipeline.
        response_llm_configuration: NemoLLMConfiguration, optional
            The LLM configuration for the response pipeline.
        response_moderation_configuration: ModerationConfigurationWithoutID, optional
            The moderation configuration for the response pipeline.
        response_pipeline_template_id: Optional[str]
            The ID of the response pipeline template, this will define the action.py file.

        Returns
        -------
        NemoConfiguration
            The Nemo configuration for the playground.
        """

        def _get_dict(
            value: Union[
                NemoFileContents, NemoLLMConfiguration, ModerationConfigurationWithoutId, None
            ]
        ) -> Union[Dict[str, Any], None]:
            return value.to_dict() if value is not None else None

        playground_id = get_entity_id(playground)
        url = f"{cls._client.domain}/{cls._path.format(playground_id)}"
        data = {
            "blocked_terms_file_contents": blocked_terms_file_contents,
            "prompt_pipeline_metric_name": prompt_pipeline_metric_name,
            "prompt_pipeline_files": _get_dict(prompt_pipeline_files),
            "prompt_llm_configuration": _get_dict(prompt_llm_configuration),
            "prompt_moderation_configuration": _get_dict(prompt_moderation_configuration),
            "prompt_pipeline_template_id": prompt_pipeline_template_id,
            "response_pipeline_metric_name": response_pipeline_metric_name,
            "response_pipeline_files": _get_dict(response_pipeline_files),
            "response_llm_configuration": _get_dict(response_llm_configuration),
            "response_moderation_configuration": _get_dict(response_moderation_configuration),
            "response_pipeline_template_id": response_pipeline_template_id,
        }
        response = cls._client.post(url, json=data)
        return cls.from_server_data(response.json())
