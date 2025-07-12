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
from typing_extensions import TypedDict

from datarobot.enums import enum_to_list, ToolCallAccuracyArgumentComparisonMode
from datarobot.models.api_object import APIObject
from datarobot.models.genai.playground_moderation_configuration import (
    moderation_configuration_without_id,
    ModerationConfigurationWithoutId,
)
from datarobot.utils import from_api


def _get_obj(value: Union[Dict[str, Any], None], obj: Any) -> Any:
    return obj.from_server_data(value) if value is not None else None


class ToolCallAccuracySettingsDict(TypedDict):
    """Dictionary representation of the tool call accuracy settings."""

    argument_comparison: ToolCallAccuracyArgumentComparisonMode


class ExtraMetricSettingsDict(TypedDict):
    """Dictionary representation of the extra metrics settings."""

    tool_call_accuracy: Optional[ToolCallAccuracySettingsDict]


class ToolCallAccuracySettings(APIObject):
    """An object that represents the settings for tool call accuracy metrics.

    Attributes
    ----------
    argument_comparison : ToolCallAccuracyArgumentComparisonMode
        The mode for comparing arguments in tool calls.
    """

    _converter = t.Dict(
        {
            t.Key("argument_comparison"): t.Or(
                t.Enum(*enum_to_list(ToolCallAccuracyArgumentComparisonMode))
            ),
        }
    ).ignore_extra("*")

    def __init__(self, argument_comparison: ToolCallAccuracyArgumentComparisonMode):
        self.argument_comparison = argument_comparison

    def to_dict(self) -> ToolCallAccuracySettingsDict:
        return ToolCallAccuracySettingsDict(
            argument_comparison=self.argument_comparison,
        )


class ExtraMetricSettings(APIObject):
    """An object that represents additional settings for OOTB metrics.

    Attributes
    ----------
    tool_call_accuracy : Optional[ToolCallAccuracySettings]
        The settings for tool call accuracy metrics, if applicable.
    """

    _converter = t.Dict(
        {
            t.Key("tool_call_accuracy"): t.Or(ToolCallAccuracySettings._converter, t.Null),
        }
    ).ignore_extra("*")

    def __init__(self, tool_call_accuracy: Optional[ToolCallAccuracySettings]):
        self.tool_call_accuracy = tool_call_accuracy

    @classmethod
    def from_data(cls, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> ExtraMetricSettings:
        """Properly convert composition classes."""
        converted_data = cls._converter.check(from_api(data))
        tool_call_accuracy = converted_data.get("tool_call_accuracy")
        converted_data["tool_call_accuracy"] = (
            ToolCallAccuracySettings.from_data(tool_call_accuracy) if tool_call_accuracy else None
        )
        return cls(**converted_data)

    def to_dict(self) -> ExtraMetricSettingsDict:
        result = ExtraMetricSettingsDict(
            tool_call_accuracy=(
                self.tool_call_accuracy.to_dict() if self.tool_call_accuracy is not None else None
            ),
        )
        return result


class OOTBMetricConfigurationRequest(APIObject):
    """
    An object that represents a request for an out-of-the-box (OOTB) metric.

    Attributes
    ----------
    ootb_metric_name : str
        The DataRobot-defined name of the OOTB metric.
    custom_ootb_metric_name : Optional[str]
        The custom OOTB metric name chosen by the user.
    llm_id : Optional[str]
        The ID of the LLM to use for `correctness` and `faithfulness` metrics.
    custom_model_llm_validation_id : Optional[str]
        The ID of the custom model LLM validation (if using a custom model LLM).
    moderation_configuration : Optional[ModerationConfigurationWithoutId]
        The moderation configuration to be associated with the OOTB metric.
    extra_metric_settings : Optional[ExtraMetricSettings]
        Additional settings for the OOTB metric.
    """

    _converter = t.Dict(
        {
            t.Key("ootb_metric_name"): t.String,
            t.Key("custom_ootb_metric_name", optional=True): t.Or(t.String, t.Null),
            t.Key("llm_id", optional=True): t.Or(t.String, t.Null),
            t.Key("custom_model_llm_validation_id", optional=True): t.Or(t.String, t.Null),
            t.Key("moderation_configuration", optional=True): t.Or(
                moderation_configuration_without_id, t.Null
            ),
            t.Key("extra_metric_settings", optional=True): t.Or(
                ExtraMetricSettings._converter, t.Null
            ),
        }
    ).ignore_extra("*")

    def __init__(
        self,
        ootb_metric_name: str,
        custom_ootb_metric_name: Optional[str] = None,
        llm_id: Optional[str] = None,
        custom_model_llm_validation_id: Optional[str] = None,
        moderation_configuration: Optional[Dict[str, Any]] = None,
        extra_metric_settings: Optional[ExtraMetricSettings] = None,
    ):

        self.ootb_metric_name = ootb_metric_name
        self.custom_ootb_metric_name = custom_ootb_metric_name
        self.llm_id = llm_id
        self.custom_model_llm_validation_id = custom_model_llm_validation_id
        self.moderation_configuration = _get_obj(
            moderation_configuration, ModerationConfigurationWithoutId
        )
        self.extra_metric_settings = extra_metric_settings

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(ootb_metric_name={self.ootb_metric_name})"

    @classmethod
    def from_data(
        cls, data: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> OOTBMetricConfigurationRequest:
        """Properly convert composition classes."""
        converted_data = cls._converter.check(from_api(data))
        extra_metric_settings = converted_data.get("extra_metric_settings")
        converted_data["extra_metric_settings"] = (
            ExtraMetricSettings.from_data(extra_metric_settings) if extra_metric_settings else None
        )
        return cls(**converted_data)

    def to_dict(self, uppercase_llm_key: bool = False) -> Dict[str, Any]:
        custom_model_llm_validation_id_key = (
            "custom_modelLLM_validation_id"
            if uppercase_llm_key
            else "custom_model_llm_validation_id"
        )
        return {
            "ootb_metric_name": self.ootb_metric_name,
            "custom_ootb_metric_name": self.custom_ootb_metric_name,
            "llm_id": self.llm_id,
            custom_model_llm_validation_id_key: self.custom_model_llm_validation_id,
            "moderation_configuration": (
                self.moderation_configuration.to_dict()
                if self.moderation_configuration is not None
                else None
            ),
            "extra_metric_settings": (
                self.extra_metric_settings.to_dict()
                if self.extra_metric_settings is not None
                else None
            ),
        }


class OOTBMetricConfigurationResponse(APIObject):
    """
    An object that represents a single OOTB metric.

    Attributes
    ----------
    ootb_metric_configuration_id : str
        The OOTB metric configuration ID.
    ootb_metric_name : str
        The DataRobot-defined name of the OOTB metric.
    execution_status : str
        The execution status of the OOTB metric.
    custom_ootb_metric_name : Optional[str]
        The custom OOTB metric name chosen by the user.
    llm_id : Optional[str]
        The ID of the LLM to use for `correctness` and `faithfulness` metrics.
    custom_model_llm_validation_id : Optional[str]
        The ID of the custom model LLM validation (if using a custom model LLM).
    moderation_configuration : Optional[ModerationConfigurationWithoutId]
        The moderation configuration to be associated with the OOTB metric.
    error_message : Optional[str]
        The error message associated with the OOTB metric configuration.
    error_resolution: Optional[list[str]]
        The error type associated with the insight error status.
    extra_metric_settings: Optional[Dict[str, Any]]
        Additional settings for the OOTB metric.
    """

    _converter = t.Dict(
        {
            t.Key("ootb_metric_configuration_id"): t.String,
            t.Key("ootb_metric_name"): t.String,
            t.Key("execution_status"): t.String,
            t.Key("custom_ootb_metric_name", optional=True): t.Or(t.String, t.Null),
            t.Key("llm_id", optional=True): t.Or(t.String, t.Null),
            t.Key("custom_model_llm_validation_id", optional=True): t.Or(t.String, t.Null),
            t.Key("moderation_configuration", optional=True): t.Or(
                moderation_configuration_without_id, t.Null
            ),
            t.Key("error_message", optional=True): t.Or(t.String(), t.Null),
            t.Key("error_resolution", optional=True): t.Or(t.List(t.String()), t.Null),
            t.Key("extra_metric_settings", optional=True): t.Or(
                ExtraMetricSettings._converter, t.Null
            ),
        }
    ).ignore_extra("*")
    _path = "api/v2/genai/ootbMetricConfigurations"

    def __init__(
        self,
        ootb_metric_configuration_id: str,
        ootb_metric_name: str,
        execution_status: str,
        custom_ootb_metric_name: Optional[str] = None,
        llm_id: Optional[str] = None,
        custom_model_llm_validation_id: Optional[str] = None,
        moderation_configuration: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
        error_resolution: Optional[List[str]] = None,
        extra_metric_settings: Optional[ExtraMetricSettings] = None,
    ):
        self.ootb_metric_configuration_id = ootb_metric_configuration_id
        self.ootb_metric_name = ootb_metric_name
        self.execution_status = execution_status
        self.custom_ootb_metric_name = custom_ootb_metric_name
        self.llm_id = llm_id
        self.custom_model_llm_validation_id = custom_model_llm_validation_id
        self.moderation_configuration = _get_obj(
            moderation_configuration, ModerationConfigurationWithoutId
        )
        self.error_message = error_message
        self.error_resolution = error_resolution
        self.extra_metric_settings = extra_metric_settings

    @classmethod
    def from_data(
        cls, data: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> OOTBMetricConfigurationResponse:
        """Properly convert composition classes."""
        converted_data = cls._converter.check(from_api(data))
        extra_metric_settings = converted_data.get("extra_metric_settings")
        converted_data["extra_metric_settings"] = (
            ExtraMetricSettings.from_data(extra_metric_settings) if extra_metric_settings else None
        )
        return cls(**converted_data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(ootb_metric_name={self.ootb_metric_name})"

    @classmethod
    def get(cls, ootb_metric_configuration_id: str) -> OOTBMetricConfigurationResponse:
        """Get the OOTB metric configuration."""
        response_data = cls._client.get(
            f"{cls._client.domain}/{cls._path}/{ootb_metric_configuration_id}/"
        )
        return cls.from_server_data(response_data.json())

    def delete(self) -> None:
        """Delete the OOTB metric configuration."""
        url = f"{self._client.domain}/{self._path}/{self.ootb_metric_configuration_id}/"
        self._client.delete(url)


class PlaygroundOOTBMetricConfiguration(APIObject):
    """OOTB metric configurations for a playground.

    Attributes
    ----------
    ootb_metric_configurations: (List[OOTBMetricConfigurationResponse]): The list of the OOTB metric configurations.
    """

    _converter = t.Dict(
        {
            t.Key("ootb_metric_configurations"): t.List(OOTBMetricConfigurationResponse._converter),
        }
    ).ignore_extra("*")
    path = "api/v2/genai/playgrounds/{playground_id}/ootbMetricConfigurations"

    def __init__(
        self,
        ootb_metric_configurations: List[Dict[str, Any]],
    ):
        self.ootb_metric_configurations = [
            OOTBMetricConfigurationResponse.from_server_data(config)
            for config in ootb_metric_configurations
        ]

    @classmethod
    def get(cls, playground_id: str) -> PlaygroundOOTBMetricConfiguration:
        """Get OOTB metric configurations for the playground."""
        response_data = cls._client.get(
            f"{cls._client.domain}/{cls.path.format(playground_id=playground_id)}/"
        )
        return cls.from_server_data(response_data.json())

    @classmethod
    def create(
        cls, playground_id: str, ootb_metric_configurations: list[OOTBMetricConfigurationRequest]
    ) -> PlaygroundOOTBMetricConfiguration:
        """Create a new OOTB metric configurations."""
        payload = {
            "ootb_metric_configurations": [
                config.to_dict(uppercase_llm_key=True) for config in ootb_metric_configurations
            ],
        }
        url = f"{cls._client.domain}/{cls.path.format(playground_id=playground_id)}/"
        response_data = cls._client.post(url, data=payload)
        return cls.from_server_data(response_data.json())
