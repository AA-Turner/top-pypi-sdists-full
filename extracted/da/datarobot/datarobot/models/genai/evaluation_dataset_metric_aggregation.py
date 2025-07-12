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

from datarobot.enums import AggregationType, enum_to_list
from datarobot.models.api_object import APIObject
from datarobot.models.genai.insights_configuration import InsightsConfiguration
from datarobot.utils.pagination import unpaginate

aggregation_value_trafaret = t.Dict(
    {
        t.Key("item"): t.String,
        t.Key("value"): t.Float,
    }
).ignore_extra("*")

evaluation_dataset_metric_aggregation_trafaret = t.Dict(
    {
        t.Key("llm_blueprint_id"): t.String,
        t.Key("evaluation_dataset_configuration_id"): t.String,
        t.Key("ootb_dataset_name"): t.Or(t.String, t.Null),
        t.Key("metric_name"): t.String(allow_blank=True),
        t.Key("deployment_id"): t.Or(t.String, t.Null),
        t.Key("dataset_id"): t.Or(t.String, t.Null),
        t.Key("dataset_name"): t.Or(t.String(allow_blank=True), t.Null),
        t.Key("chat_id"): t.String,
        t.Key("chat_name"): t.String(allow_blank=True),
        t.Key("aggregation_value"): t.Or(t.Float, t.List(aggregation_value_trafaret)),
        t.Key("aggregation_type"): t.Enum(*enum_to_list(AggregationType)),
        t.Key("creation_date"): t.String,
        t.Key("creation_user_id"): t.String,
        t.Key("tenant_id"): t.String,
        t.Key("custom_model_guard_id"): t.String,
    }
).ignore_extra("*")


class EvaluationDatasetMetricAggregation(APIObject):
    """Information about an evaluation dataset metric aggregation job.
      This job runs a metric against LLMs using an evaluation dataset and aggregates the results.

    Attributes
    ----------
    llm_blueprint_id : str
        The LLM blueprint ID.
    evaluation_dataset_configuration_id : str
        The evaluation dataset configuration ID.
    ootb_dataset_name : str | None
        The name of the Datarobot-provided dataset that does not require additional configuration.
    metric_name : str
        The name of the metric.
    deployment_id : str | None
        A deployment ID if the evaluation was run against a deployment.
    dataset_id : str | None
        The ID of the dataset used in the evaluation.
    dataset_name : str | None
        The name of the dataset used in the evaluation.
    chat_id : str
        The ID of the chat created to run the evaluation.
    chat_name : str
        The name of the chat that was created to run the evaluation.
    aggregation_value : float | List[Dict[str, float]]
        The aggregated metric result.
    aggregation_type : AggregationType
        The type of aggregation used for the metric results.
    creation_date : str
        The date the evaluation job was created.
    creation_user_id : str
        The ID of the user who created the evaluation job.
    tenant_id : str
        The ID of the tenant that owns the evaluation job.
    custom_model_guard_id : str | None
        The ID of the custom model's guard associated with the metric aggregation, if applicable.
    """

    _path = "api/v2/genai/evaluationDatasetMetricAggregations"
    _converter = evaluation_dataset_metric_aggregation_trafaret

    def __init__(
        self,
        llm_blueprint_id: str,
        evaluation_dataset_configuration_id: str,
        ootb_dataset_name: Optional[str],
        metric_name: str,
        deployment_id: Optional[str],
        dataset_id: Optional[str],
        dataset_name: Optional[str],
        chat_id: str,
        chat_name: str,
        aggregation_value: Union[float, List[Dict[str, float]]],
        aggregation_type: AggregationType,
        creation_date: str,
        creation_user_id: str,
        tenant_id: str,
        custom_model_guard_id: Optional[str] = None,
    ) -> None:
        self.llm_blueprint_id = llm_blueprint_id
        self.evaluation_dataset_configuration_id = evaluation_dataset_configuration_id
        self.ootb_dataset_name = ootb_dataset_name
        self.metric_name = metric_name
        self.deployment_id = deployment_id
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
        self.chat_id = chat_id
        self.chat_name = chat_name
        self.aggregation_value = aggregation_value
        self.aggregation_type = aggregation_type
        self.creation_date = creation_date
        self.creation_user_id = creation_user_id
        self.tenant_id = tenant_id
        self.custom_model_guard_id = custom_model_guard_id

    @classmethod
    def create(
        cls,
        chat_name: str,
        llm_blueprint_ids: List[str],
        evaluation_dataset_configuration_id: str,
        insights_configuration: list[InsightsConfiguration],
    ) -> Any:
        """
        Create a new evaluation dataset metric aggregation job.  The job will run the
        specified metric for the specified LLM blueprint IDs using the prompt-response pairs in
        the evaluation dataset.

        Parameters
        ----------
        chat_name : str
            The name of the chat that will be created to run the evaluation in.
        llm_blueprint_ids : List[str]
            The LLM blueprint IDs to evaluate.
        evaluation_dataset_configuration_id : str
            The ID evaluation dataset configuration to use during the evaluation.
        insights_configuration : List[InsightsConfiguration]
            The insights configurations to use during the evaluation.

        Returns
        -------
        str
            The ID of the evaluation dataset metric aggregation job.
        """
        payload = {
            "chat_name": chat_name,
            "llm_blueprint_ids": llm_blueprint_ids,
            "evaluation_dataset_configuration_id": evaluation_dataset_configuration_id,
            "insights_configuration": [insight.to_dict() for insight in insights_configuration],
        }
        url = f"{cls._client.domain}/{cls._path}/"
        response_data = cls._client.post(url, json=payload)
        return response_data.json()["jobId"]

    @classmethod
    def list(
        cls,
        llm_blueprint_ids: Optional[List[str]] = None,
        chat_ids: Optional[List[str]] = None,
        evaluation_dataset_configuration_ids: Optional[List[str]] = None,
        metric_names: Optional[List[str]] = None,
        aggregation_types: Optional[List[str]] = None,
        current_configuration_only: Optional[bool] = False,
        sort: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 100,
        non_errored_only: Optional[bool] = True,
    ) -> List[EvaluationDatasetMetricAggregation]:
        """List evaluation dataset metric aggregations.  The results will be filtered by the provided
        LLM blueprint IDs and chat IDs.

        Parameters
        ----------
        llm_blueprint_ids : List[str]
            The LLM blueprint IDs to filter on.
        chat_ids : List[str]
            The chat IDs to filter on.
        evaluation_dataset_configuration_ids : List[str]
            The evaluation dataset configuration IDs to filter on.
        metric_names : List[str]
            The metric names to filter on.
        aggregation_types : List[str]
            The aggregation types to filter on.
        current_configuration_only : Optional[bool]
            If True, only results that are associated with the current configuration of the LLM blueprint
            will be returned.  Defaults to False.
        sort : Optional[str]
            The field to sort on.  Defaults to None.
        offset : Optional[int]
            The offset to start at.  Defaults to 0.
        limit : Optional[int]
            The maximum number of results to return.  Defaults to 100.
        non_errored_only : Optional[bool]
            If True, only results that did not encounter an error will be returned.  Defaults to True.

        Returns
        -------
        List[EvaluationDatasetMetricAggregation]
            A list of evaluation dataset metric aggregations.
        """
        params = {
            "llm_blueprint_ids": llm_blueprint_ids,
            "chat_ids": chat_ids,
            "evaluation_dataset_configuration_ids": evaluation_dataset_configuration_ids,
            "metric_names": metric_names,
            "aggregation_types": aggregation_types,
            "current_configuration_only": current_configuration_only,
            "sort": sort,
            "offset": offset,
            "limit": limit,
            "non_errored_only": non_errored_only,
        }
        url = f"{cls._client.domain}/{cls._path}/"
        r_data = unpaginate(url, params, cls._client)
        return [cls.from_server_data(data) for data in r_data]

    @classmethod
    def delete(cls, llm_blueprint_ids: Optional[List[str]], chat_ids: Optional[List[str]]) -> None:
        """Delete the associated evaluation dataset metric aggregations.  Either llm_blueprint_ids
        or chat_ids must be provided.  If both are provided, only results matching both will be removed.

        Parameters
        ----------
        llm_blueprint_ids : List[str]
            The LLM blueprint IDs to filter on.
        chat_ids : List[str]
            The chat IDs to filter on.

        """
        if llm_blueprint_ids is None and chat_ids is None:
            raise ValueError("Either llm_blueprint_ids or chat_ids must be provided.")
        url = f"{cls._client.domain}/{cls._path}/"
        # parameters are camelcase here because delete doesn't seem to send them correctly otherwise.
        params = {
            "llmBlueprintIds": llm_blueprint_ids,
            "chatIds": chat_ids,
        }
        cls._client.delete(url, params=params)
