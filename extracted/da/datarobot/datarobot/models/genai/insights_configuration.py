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

from mypy_extensions import TypedDict
import trafaret as t

from datarobot.enums import (
    AggregationType,
    enum_to_list,
    GuardConditionComparator,
    GuardType,
    InsightTypes,
)
from datarobot.models.api_object import APIObject
from datarobot.models.genai.ootb_metric_configuration import (
    ExtraMetricSettings,
    ExtraMetricSettingsDict,
)
from datarobot.models.genai.playground_moderation_configuration import (
    moderation_configuration_with_id,
    moderation_configuration_without_id,
)
from datarobot.utils import from_api


class InsightsConfigurationDict(TypedDict):
    """Dictionary representation of insights configuration."""

    insight_name: str
    insight_type: Optional[str]
    deployment_id: Optional[str]
    model_id: Optional[str]
    sidecar_model_metric_validation_id: Optional[str]
    custom_metric_id: Optional[str]
    evaluation_dataset_configuration_id: Optional[str]
    cost_configuration_id: Optional[str]
    result_unit: Optional[str]
    ootb_metric_id: Optional[str]
    ootb_metric_name: Optional[str]
    guard_conditions: Optional[List[Dict[str, Any]]]
    moderation_configuration: Optional[Dict[str, Any]]
    execution_status: Optional[str]
    error_message: Optional[str]
    error_resolution: Optional[str]
    nemo_metric_id: Optional[str]
    llm_id: Optional[str]
    custom_model_llm_validation_id: Optional[str]
    stage: Optional[str]
    aggregation_types: Optional[List[str]]
    sidecar_model_metric_metadata: Optional[Dict[str, Any]]
    guard_template_id: Optional[str]
    guard_configuration_id: Optional[str]
    model_package_registered_model_id: Optional[str]
    custom_model_guard: Optional[CustomModelGuardDict]
    extra_metric_settings: Optional[ExtraMetricSettingsDict]


class CustomModelGuardDict(TypedDict):
    """Dictionary representation of the custom model guard."""

    name: str
    type: str
    ootb_type: Optional[str]
    stage: Optional[str]


guard_conditions = t.Dict(
    {
        t.Key("comparator"): t.Enum(*enum_to_list(GuardConditionComparator)),
        t.Key("comparand"): t.Or(t.String, t.Float, t.Bool, t.List(t.String)),
    }
).ignore_extra("*")

sidecar_model_metric_metadata = t.Dict(
    {
        t.Key("prompt_column_name", optional=True): t.Or(t.String, t.Null),
        t.Key("response_column_name", optional=True): t.Or(t.String, t.Null),
        t.Key("target_column_name", optional=True): t.Or(t.String, t.Null),
        t.Key("expected_response_column_name", optional=True): t.Or(t.String, t.Null),
        t.Key("guard_type", optional=True): t.Or(t.Enum(*enum_to_list(GuardType)), t.Null),
    }
).ignore_extra("*")

custom_model_guard_trafaret = t.Dict(
    {
        t.Key("name"): t.String,
        t.Key("type"): t.String,
        t.Key("ootb_type", optional=True): t.Or(t.String, t.Null),
        t.Key("stage", optional=True): t.Or(t.String, t.Null),
    }
).ignore_extra("*")

insight_configuration_trafaret = t.Dict(
    {
        t.Key("insight_name"): t.String,
        t.Key("insight_type", optional=True): t.Or(t.Enum(*enum_to_list(InsightTypes)), t.Null),
        t.Key("deployment_id", optional=True): t.Or(t.String, t.Null),
        t.Key("model_id", optional=True): t.Or(t.String, t.Null),
        t.Key("sidecar_model_metric_validation_id", optional=True): t.Or(t.String, t.Null),
        t.Key("custom_metric_id", optional=True): t.Or(t.String, t.Null),
        t.Key("evaluation_dataset_configuration_id", optional=True): t.Or(t.String, t.Null),
        t.Key("cost_configuration_id", optional=True): t.Or(t.String, t.Null),
        t.Key("result_unit", optional=True): t.Or(t.String, t.Null),
        t.Key("ootb_metric_id", optional=True): t.Or(t.String, t.Null),
        t.Key("ootb_metric_name", optional=True): t.Or(t.String, t.Null),
        t.Key("guard_conditions", optional=True): t.Or(t.List(guard_conditions), t.Null),
        t.Key("moderation_configuration", optional=True): t.Or(
            moderation_configuration_with_id, moderation_configuration_without_id, t.Null
        ),
        t.Key("execution_status", optional=True): t.Or(t.String, t.Null),
        t.Key("error_message", optional=True): t.Or(t.String, t.Null),
        t.Key("error_resolution", optional=True): t.Or(t.String, t.Null),
        t.Key("nemo_metric_id", optional=True): t.Or(t.String, t.Null),
        t.Key("llm_id", optional=True): t.Or(t.String, t.Null),
        t.Key("custom_model_llm_validation_id", optional=True): t.Or(t.String, t.Null),
        t.Key("stage", optional=True): t.Or(t.String, t.Null),
        # additional data
        t.Key("aggregation_types", optional=True): t.Or(
            t.List(t.Enum(*enum_to_list(AggregationType))), t.Null
        ),
        t.Key("sidecar_model_metric_metadata", optional=True): t.Or(
            sidecar_model_metric_metadata, t.Null
        ),
        t.Key("guard_template_id", optional=True): t.Or(t.String, t.Null),
        t.Key("guard_configuration_id", optional=True): t.Or(t.String, t.Null),
        t.Key("model_package_registered_model_id", optional=True): t.Or(t.String, t.Null),
        t.Key("custom_model_guard", optional=True): t.Or(custom_model_guard_trafaret, t.Null),
        t.Key("extra_metric_settings", optional=True): t.Or(ExtraMetricSettings._converter, t.Null),
    }
).ignore_extra("*")

insights_trafaret = t.Dict(
    {
        t.Key("playground_id"): t.String,
        t.Key("insights_configuration"): t.List(insight_configuration_trafaret),
        t.Key("creation_date"): t.String,
        t.Key("creation_user_id"): t.String,
        t.Key("last_update_date"): t.String,
        t.Key("last_update_user_id"): t.String,
        t.Key("tenant_id"): t.String,
    }
).ignore_extra("*")


class InsightsConfiguration(APIObject):
    """
    Configuration information for a specific insight.

    Attributes
    ----------
    insight_name : str
        The name of the insight.
    insight_type : InsightTypes, optional
        The type of the insight.
    deployment_id : Optional[str]
        The deployment ID the insight is applied to.
    model_id : Optional[str]
        The model ID for the insight.
    sidecar_model_metric_validation_id : Optional[str]
        Validation ID for the sidecar model metric.
    custom_metric_id : Optional[str]
        The ID for a custom model metric.
    evaluation_dataset_configuration_id : Optional[str]
        The ID for the evaluation dataset configuration.
    cost_configuration_id : Optional[str]
        The ID for the cost configuration information.
    result_unit : Optional[str]
        The unit of the result, for example "USD".
    ootb_metric_id : Optional[str]
        The ID of the Datarobot-provided metric that does not require additional configuration.
    ootb_metric_name : Optional[str]
        The name of the Datarobot-provided metric that does not require additional configuration.
    guard_conditions : list[dict], optional
        The guard conditions to be used with the insight.
    moderation_configuration : dict, optional
        The moderation configuration for the insight.
    execution_status : Optional[str]
        The execution status of the insight.
    error_message : Optional[str]
        The error message for the insight, for example if it is missing specific configuration
        for deployed models.
    error_resolution : Optional[str]
        An indicator of which field must be edited to resolve an error state.
    nemo_metric_id : Optional[str]
        The ID for the NEMO metric.
    llm_id : Optional[str]
        The LLM ID for OOTB metrics that use LLMs.
    custom_model_llm_validation_id : Optional[str]
        The ID for the custom model LLM validation if using a custom model LLM for OOTB metrics.
    aggregation_types : list[str], optional
        The aggregation types to be used for the insight.
    stage : Optional[str]
        The stage (prompt or response) when the metric is calculated.
    sidecar_model_metric_metadata : dict, optional
        Metadata specific to sidecar model metrics.
    guard_template_id : Optional[str]
        The ID for the guard template that applies to the insight.
    guard_configuration_id : Optional[str]
        The ID for the guard configuration that applies to the insight.
    model_package_registered_model_id : Optional[str]
        The ID of the registered model package associated with `deploymentId`.
    custom_model_guard : Optional[CustomModelGuard]
        The custom model guard configuration, if applicable.
    extra_metric_settings : Optional[ExtraMetricSettings]
        Additional settings for the insight.
    """

    _converter = insight_configuration_trafaret

    def __init__(
        self,
        insight_name: str,
        insight_type: Optional[str] = None,
        deployment_id: Optional[str] = None,
        model_id: Optional[str] = None,
        sidecar_model_metric_validation_id: Optional[str] = None,
        custom_metric_id: Optional[str] = None,
        evaluation_dataset_configuration_id: Optional[str] = None,
        cost_configuration_id: Optional[str] = None,
        result_unit: Optional[str] = None,
        ootb_metric_id: Optional[str] = None,
        ootb_metric_name: Optional[str] = None,
        guard_conditions: Optional[List[Dict[str, Any]]] = None,
        moderation_configuration: Optional[Dict[str, Any]] = None,
        execution_status: Optional[str] = None,
        error_message: Optional[str] = None,
        error_resolution: Optional[str] = None,
        nemo_metric_id: Optional[str] = None,
        llm_id: Optional[str] = None,
        custom_model_llm_validation_id: Optional[str] = None,
        stage: Optional[str] = None,
        aggregation_types: Optional[List[str]] = None,
        sidecar_model_metric_metadata: Optional[Dict[str, Any]] = None,
        guard_template_id: Optional[str] = None,
        guard_configuration_id: Optional[str] = None,
        model_package_registered_model_id: Optional[str] = None,
        custom_model_guard: Optional[CustomModelGuard] = None,
        extra_metric_settings: Optional[ExtraMetricSettings] = None,
    ):
        self.insight_name = insight_name
        self.insight_type = insight_type
        self.deployment_id = deployment_id
        self.model_id = model_id
        self.sidecar_model_metric_validation_id = sidecar_model_metric_validation_id
        self.custom_metric_id = custom_metric_id
        self.evaluation_dataset_configuration_id = evaluation_dataset_configuration_id
        self.cost_configuration_id = cost_configuration_id
        self.result_unit = result_unit
        self.ootb_metric_id = ootb_metric_id
        self.ootb_metric_name = ootb_metric_name
        self.guard_conditions = guard_conditions
        self.moderation_configuration = moderation_configuration
        self.execution_status = execution_status
        self.error_message = error_message
        self.error_resolution = error_resolution
        self.nemo_metric_id = nemo_metric_id
        self.llm_id = llm_id
        self.custom_model_llm_validation_id = custom_model_llm_validation_id
        self.stage = stage
        self.aggregation_types = aggregation_types
        self.sidecar_model_metric_metadata = sidecar_model_metric_metadata
        self.guard_template_id = guard_template_id
        self.guard_configuration_id = guard_configuration_id
        self.model_package_registered_model_id = model_package_registered_model_id
        self.custom_model_guard = custom_model_guard
        self.extra_metric_settings = extra_metric_settings

    @classmethod
    def from_data(cls, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> InsightsConfiguration:
        """Properly convert composition classes."""
        converted_data = cls._converter.check(from_api(data))

        custom_model_guard = converted_data.get("custom_model_guard")
        converted_data["custom_model_guard"] = (
            CustomModelGuard.from_data(custom_model_guard) if custom_model_guard else None
        )

        extra_metric_settings = converted_data.get("extra_metric_settings")
        converted_data["extra_metric_settings"] = (
            ExtraMetricSettings.from_data(extra_metric_settings) if extra_metric_settings else None
        )
        return cls(**converted_data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.insight_name}, model_id={self.model_id})"

    def to_dict(self) -> InsightsConfigurationDict:
        return InsightsConfigurationDict(
            insight_name=self.insight_name,
            insight_type=self.insight_type,
            deployment_id=self.deployment_id,
            model_id=self.model_id,
            sidecar_model_metric_validation_id=self.sidecar_model_metric_validation_id,
            custom_metric_id=self.custom_metric_id,
            evaluation_dataset_configuration_id=self.evaluation_dataset_configuration_id,
            cost_configuration_id=self.cost_configuration_id,
            result_unit=self.result_unit,
            ootb_metric_id=self.ootb_metric_id,
            ootb_metric_name=self.ootb_metric_name,
            guard_conditions=self.guard_conditions,
            moderation_configuration=self.moderation_configuration,
            execution_status=self.execution_status,
            error_message=self.error_message,
            error_resolution=self.error_resolution,
            nemo_metric_id=self.nemo_metric_id,
            llm_id=self.llm_id,
            custom_model_llm_validation_id=self.custom_model_llm_validation_id,
            stage=self.stage,
            aggregation_types=self.aggregation_types,
            sidecar_model_metric_metadata=self.sidecar_model_metric_metadata,
            guard_template_id=self.guard_template_id,
            guard_configuration_id=self.guard_configuration_id,
            model_package_registered_model_id=self.model_package_registered_model_id,
            custom_model_guard=(
                self.custom_model_guard.to_dict() if self.custom_model_guard else None
            ),
            extra_metric_settings=(
                self.extra_metric_settings.to_dict() if self.extra_metric_settings else None
            ),
        )


class CustomModelGuard(APIObject):
    """
    Configuration information for a guard.

    Attributes
    ----------
    name : str
        Name of the guard.
    type : str
        Type of the guard.
    ootb_type : Optional[str]
        Out of the box type of the guard, if applicable.
    stage : Optional[str]
        Stage at which the guard is applied (e.g., prompt, response).
    """

    _converter = custom_model_guard_trafaret

    def __init__(
        self,
        name: str,
        type: str,
        ootb_type: Optional[str] = None,
        stage: Optional[str] = None,
    ):
        self.name = name
        self.type = type
        self.ootb_type = ootb_type
        self.stage = stage

    def to_dict(self) -> CustomModelGuardDict:
        return CustomModelGuardDict(
            name=self.name,
            type=self.type,
            ootb_type=self.ootb_type,
            stage=self.stage,
        )
