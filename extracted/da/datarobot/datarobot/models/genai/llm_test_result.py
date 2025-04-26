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

from typing import Any, Dict, List, Optional, Union

import trafaret as t

from datarobot.enums import AggregationType, enum_to_list, GradingResult
from datarobot.models.api_object import APIObject
from datarobot.models.genai.evaluation_dataset_metric_aggregation import aggregation_value_trafaret
from datarobot.models.genai.llm_blueprint import LLMBlueprint
from datarobot.models.genai.llm_test_configuration import (
    insight_grading_criteria_trafaret,
    InsightGradingCriteria,
    llm_test_grading_criteria_trafaret,
    LLMTestConfiguration,
    LLMTestGradingCriteria,
)
from datarobot.utils.pagination import unpaginate


def get_entity_id(entity: Union[LLMTestConfiguration, LLMBlueprint, LLMTestResult, str]) -> str:
    """
    Get the entity ID from the entity parameter.

    Parameters
    ----------
    entity : ApiObject or str
        May be entity ID or the entity.

    Returns
    -------
    id : str
        Entity ID
    """
    if isinstance(entity, str):
        return entity

    return entity.id


insight_evaluation_result_trafaret = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("llm_test_result_id"): t.String,
        t.Key("evaluation_dataset_configuration_id", optional=True): t.Or(t.String, t.Null),
        t.Key("evaluation_dataset_name"): t.String(allow_blank=True),
        t.Key("metric_name", optional=True): t.Or(t.String, t.Null),
        t.Key("chat_id"): t.String,
        t.Key("chat_name"): t.String(allow_blank=True),
        t.Key("aggregation_value", optional=True): t.Or(
            t.Float, t.List(aggregation_value_trafaret), t.Null
        ),
        t.Key("aggregation_type", optional=True): t.Or(
            t.Enum(*enum_to_list(AggregationType)), t.Null
        ),
        t.Key("grading_result", optional=True): t.Or(t.Enum(*enum_to_list(GradingResult)), t.Null),
        t.Key("execution_status"): t.String,
        t.Key("evaluation_name"): t.String(allow_blank=True),
        t.Key("insight_grading_criteria"): insight_grading_criteria_trafaret,
        t.Key("last_update_date"): t.String,
    }
).ignore_extra("*")


llm_test_result_trafaret = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("llm_test_configuration_id"): t.String,
        t.Key("llm_test_configuration_name"): t.String(allow_blank=True),
        t.Key("use_case_id"): t.String,
        t.Key("llm_blueprint_id"): t.String,
        t.Key("llm_blueprint_snapshot"): t.Dict().allow_extra("*"),
        t.Key("llm_test_grading_criteria"): llm_test_grading_criteria_trafaret,
        t.Key("grading_result", optional=True): t.Or(t.Enum(*enum_to_list(GradingResult)), t.Null),
        t.Key("pass_percentage", optional=True): t.Or(t.Float, t.Null),
        t.Key("execution_status"): t.String,
        t.Key("insight_evaluation_results"): t.List(insight_evaluation_result_trafaret),
        t.Key("creation_date"): t.String,
        t.Key("creation_user_id"): t.String,
        t.Key("creation_user_name"): t.String(allow_blank=True),
    }
).ignore_extra("*")


class InsightEvaluationResult(APIObject):
    """
    Metadata for a DataRobot GenAI insight evaluation result.

    Attributes
    ----------
    id : str
        The ID of the insight evaluation result.
    llm_test_result_id : str
        The ID of the LLM test result associated with this insight evaluation result.
    evaluation_dataset_configuration_id : str
        The ID of the evaluation dataset configuration.
    evaluation_dataset_name : str
        The name of the evaluation dataset.
    metric_name : str
        The name of the metric.
    chat_id : str
        The ID of the chat containing the prompts and responses.
    chat_name : str
        The name of the chat containing the prompts and responses.
    aggregation_type : AggregationType
        The type of aggregation used for the metric results.
    grading_result : GradingResult
        The overall grade for the LLM test.
    execution_status : str
        The execution status of the LLM test.
    evaluation_name : str
        The name of the evaluation.
    insight_grading_criteria: InsightGradingCriteria
        The criteria to grade the results.
    last_update_date : str
        The date the result was most recently updated.
    aggregation_value : float | List[Dict[str, float]] | None
        The aggregated metric result.
    """

    _converter = insight_evaluation_result_trafaret

    def __init__(
        self,
        id: str,
        llm_test_result_id: str,
        chat_id: str,
        chat_name: str,
        execution_status: str,
        evaluation_name: str,
        insight_grading_criteria: Dict[str, Any],
        last_update_date: str,
        evaluation_dataset_name: str,
        aggregation_value: Union[float, List[Dict[str, float]], None] = None,
        evaluation_dataset_configuration_id: Optional[str] = None,
        metric_name: Optional[str] = None,
        aggregation_type: Optional[AggregationType] = None,
        grading_result: Optional[GradingResult] = None,
    ):
        self.id = id
        self.llm_test_result_id = llm_test_result_id
        self.evaluation_dataset_configuration_id = evaluation_dataset_configuration_id
        self.metric_name = metric_name
        self.chat_id = chat_id
        self.chat_name = chat_name
        self.aggregation_type = aggregation_type
        self.grading_result = grading_result
        self.execution_status = execution_status
        self.evaluation_name = evaluation_name
        self.evaluation_dataset_name = evaluation_dataset_name
        self.insight_grading_criteria = InsightGradingCriteria.from_server_data(
            insight_grading_criteria
        )
        self.last_update_date = last_update_date
        self.aggregation_value = aggregation_value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"


class LLMTestResult(APIObject):
    """
    Metadata for a DataRobot GenAI LLM test result.

    Attributes
    ----------
    id : str
        The LLM test result ID.
    llm_test_configuration_id : str
        The LLM test configuration ID associated with this LLM test result.
    llm_test_configuration_name : str
        The LLM test configuration name associated with this LLM test result.
    use_case_id : str
        The ID of the Use Case associated with this LLM test result.
    llm_blueprint_id : str
        The ID of the LLM blueprint for this LLM test result.
    llm_test_grading_criteria : LLMTestGradingCriteria
        The criteria used to grade the result of the LLM test configuration.
    grading_result : GradingResult
        The overall grading result for the LLM test.
    pass_percentage : float
        The percentage of insight evaluation results that passed the grading criteria.
    execution_status : str
        The execution status of the job that evaluated the LLM test result.
    insight_evaluation_result : list[InsightEvaluationResult]
        The results for the individual insights that make up the LLM test result.
    creation_date : str
        The date of the LLM test result.
    creation_user_id : str
        The ID of the user who executed the LLM test.
    creation_user_name: str
        The name of the user who executed the LLM test.
    """

    _path = "api/v2/genai/llmTestResults"

    _converter = llm_test_result_trafaret

    def __init__(
        self,
        id: str,
        llm_test_configuration_id: str,
        llm_test_configuration_name: str,
        use_case_id: str,
        llm_blueprint_id: str,
        llm_blueprint_snapshot: Dict[str, Any],
        llm_test_grading_criteria: Dict[str, Any],
        execution_status: str,
        insight_evaluation_results: List[Dict[str, Any]],
        creation_date: str,
        creation_user_id: str,
        creation_user_name: str,
        pass_percentage: Optional[float] = None,
        grading_result: Optional[GradingResult] = None,
    ):
        self.id = id
        self.llm_test_configuration_id = llm_test_configuration_id
        self.llm_test_configuration_name = llm_test_configuration_name
        self.use_case_id = use_case_id
        self.llm_blueprint_id = llm_blueprint_id
        self.llm_test_grading_criteria = LLMTestGradingCriteria.from_server_data(
            llm_test_grading_criteria
        )
        self.pass_percentage = pass_percentage
        self.execution_status = execution_status
        self.llm_blueprint_snapshot = llm_blueprint_snapshot
        self.insight_evaluation_results = [
            InsightEvaluationResult.from_server_data(result)
            for result in insight_evaluation_results
        ]
        self.creation_date = creation_date
        self.creation_user_id = creation_user_id
        self.creation_user_name = creation_user_name
        self.grading_result = grading_result

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    @classmethod
    def create(
        cls,
        llm_test_configuration: Union[LLMTestConfiguration, str],
        llm_blueprint: Union[LLMBlueprint, str],
    ) -> LLMTestResult:
        """
        Create a new LLMTestResult. This executes the LLM test configuration using the
        specified LLM blueprint. To check the status of the LLM test, use the
        `LLMTestResult.get` method with the returned ID.

        Parameters
        ----------
        llm_test_configuration : LLMTestConfiguration or str
            The LLM test configuration to execute, either `LLMTestConfiguration` or
            the LLM test configuration ID.
        llm_blueprint : LLMBlueprint or str
            The LLM blueprint to test, either `LLMBlueprint` or
            the LLM blueprint ID.

        Returns
        -------
        llm_test_result : LLMTestResult
            The created LLM test result.
        """
        payload = {
            "llm_test_configuration_id": get_entity_id(llm_test_configuration),
            "llm_blueprint_id": get_entity_id(llm_blueprint),
        }

        url = f"{cls._client.domain}/{cls._path}/"
        r_data = cls._client.post(url, json=payload)
        return cls.from_server_data(r_data.json())

    @classmethod
    def get(cls, llm_test_result: Union[LLMTestResult, str]) -> LLMTestResult:
        """
        Retrieve a single LLM test result.

        Parameters
        ----------
        llm_test_result : LLMTestResult or str
            The LLM test result to retrieve, specified by either LLM test result or test ID.

        Returns
        -------
        llm_test_result : LLMTestResult
            The requested LLM test result.
        """
        url = f"{cls._client.domain}/{cls._path}/{get_entity_id(llm_test_result)}/"
        r_data = cls._client.get(url)
        return cls.from_server_data(r_data.json())

    @classmethod
    def list(
        cls,
        llm_test_configuration: Optional[Union[LLMTestConfiguration, str]] = None,
        llm_blueprint: Optional[Union[LLMBlueprint, str]] = None,
    ) -> List[LLMTestResult]:
        """
        List all LLM test results available to the user. If the LLM test configuration or LLM
        blueprint is specified, results are restricted to only those LLM test results associated
        with the LLM test configuration or LLM blueprint.

        Parameters
        ----------
        llm_test_configuration : Optional[Union[LLMTestConfiguration, str]]
            The returned LLM test results are filtered to those associated with a specific
            LLM test configuration, if specified.
        llm_blueprint : Optional[Union[LLMBlueprint, str]]
            The returned LLM test results, filtered by those associated with a specific
            LLM blueprint, if specified.

        Returns
        -------
        llm_test_results : List[LLMTestResult]
            Returns a list of LLM test results.
        """

        params = {}
        if llm_test_configuration:
            params["llm_test_configuration_id"] = get_entity_id(llm_test_configuration)
        if llm_blueprint:
            params["llm_blueprint_id"] = get_entity_id(llm_blueprint)
        url = f"{cls._client.domain}/{cls._path}/"
        r_data = unpaginate(url, params, cls._client)
        return [cls.from_server_data(data) for data in r_data]

    def delete(self) -> None:
        """
        Delete a single LLM test result.
        """
        url = f"{self._client.domain}/{self._path}/{self.id}/"
        self._client.delete(url)
