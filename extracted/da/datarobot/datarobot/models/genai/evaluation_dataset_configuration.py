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

from typing import List, Optional

import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.utils.pagination import unpaginate

evaluation_dataset_configuration_trafaret = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("name"): t.String(allow_blank=True),
        t.Key("size"): t.Int,
        t.Key("rows_count"): t.Int,
        t.Key("use_case_id"): t.String,
        t.Key("playground_id", optional=True): t.Or(t.String, t.Null),
        t.Key("dataset_id"): t.String,
        t.Key("dataset_name"): t.String(allow_blank=True),
        t.Key("prompt_column_name"): t.String,
        t.Key("response_column_name", optional=True): t.Or(t.String, t.Null),
        t.Key("tool_calls_column_name", optional=True): t.Or(t.String, t.Null),
        t.Key("agent_goals_column_name", optional=True): t.Or(t.String, t.Null),
        t.Key("user_name"): t.String(allow_blank=True),
        t.Key("correctness_enabled", optional=True): t.Or(t.Bool, t.Null),
        t.Key("creation_user_id"): t.String,
        t.Key("creation_date"): t.String,
        t.Key("tenant_id"): t.String,
        t.Key("execution_status"): t.String,
        t.Key("error_message", optional=True): t.Or(t.String, t.Null),
    }
).ignore_extra("*")


class EvaluationDatasetConfiguration(APIObject):
    """
    An evaluation dataset configuration used to evaluate the performance of LLMs.

    Attributes
    ----------
    id : str
        The evaluation dataset configuration ID.
    name : str
        The name of the evaluation dataset configuration.
    size : int
        The size of the evaluation dataset (in bytes).
    rows_count : int
        The row count of the evaluation dataset.
    use_case_id : str
        The ID of the Use Case associated with the evaluation dataset configuration.
    playground_id : Optional[str]
        The ID of the playground associated with the evaluation dataset configuration.
    dataset_id : str
        The ID of the evaluation dataset.
    dataset_name : str
        The name of the evaluation dataset.
    prompt_column_name : str
        The name of the dataset column containing the prompt text.
    response_column_name : Optional[str]
        The name of the dataset column containing the response text.
    tool_calls_column_name : Optional[str]
        The name of the dataset column containing the expected tool calls.  It is required to evaluate
        the tool call accuracy metric for agentic workflows.
    agent_goals_column_name : Optional[str]
        The name of the dataset column containing the expected agent goals. It is required to
        evaluate the agent goal accuracy with reference metrics for agentic workflows.
    correctness_enabled : Optional[bool]
        Whether correctness is enabled for the evaluation dataset configuration.
    creation_user_id : str
        The ID of the user who created the evaluation dataset configuration.
    creation_date : str
        The creation date of the evaluation dataset configuration (ISO-8601 formatted).
    tenant_id : str
        The ID of the DataRobot tenant this evaluation dataset configuration belongs to.
    execution_status : str
        The execution status of the evaluation dataset configuration.
    error_message : Optional[str]
        The error message associated with the evaluation dataset configuration.
    """

    _path = "api/v2/genai/evaluationDatasetConfigurations"
    _converter = evaluation_dataset_configuration_trafaret

    def __init__(
        self,
        id: str,
        name: str,
        size: int,
        rows_count: int,
        use_case_id: str,
        dataset_id: str,
        dataset_name: str,
        prompt_column_name: str,
        user_name: str,
        creation_user_id: str,
        creation_date: str,
        tenant_id: str,
        execution_status: str,
        playground_id: Optional[str] = None,
        response_column_name: Optional[str] = None,
        tool_calls_column_name: Optional[str] = None,
        agent_goals_column_name: Optional[str] = None,
        correctness_enabled: Optional[bool] = None,
        error_message: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.size = size
        self.rows_count = rows_count
        self.use_case_id = use_case_id
        self.playground_id = playground_id
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
        self.prompt_column_name = prompt_column_name
        self.response_column_name = response_column_name
        self.tool_calls_column_name = tool_calls_column_name
        self.prompt_column_name = prompt_column_name
        self.agent_goals_column_name = agent_goals_column_name
        self.user_name = user_name
        self.correctness_enabled = correctness_enabled
        self.creation_user_id = creation_user_id
        self.creation_date = creation_date
        self.tenant_id = tenant_id
        self.execution_status = execution_status
        self.error_message = error_message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, dataset_id={self.dataset_id})"

    @classmethod
    def get(cls, id: str) -> EvaluationDatasetConfiguration:
        """Get an evaluation dataset configuration by ID.

        Parameters
        ----------
        id: str
            The evaluation dataset configuration ID to fetch.

        Returns
        -------
        evaluation_dataset_configuration: EvaluationDatasetConfiguration
            The evaluation dataset configuration.
        """
        url = f"{cls._client.domain}/{cls._path}/{id}/"
        response_data = cls._client.get(url)
        return cls.from_server_data(response_data.json())

    @classmethod
    def list(
        cls,
        use_case_id: str,
        playground_id: str,
        evaluation_dataset_configuration_id: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 100,
        sort: Optional[str] = None,
        search: Optional[str] = None,
        correctness_only: Optional[bool] = False,
        completed_only: Optional[bool] = False,
    ) -> List[EvaluationDatasetConfiguration]:
        """List all evaluation dataset configurations for a Use Case.

        Parameters
        ----------
        use_case_id: str
            The ID of the Use Case that evaluation datasets are returned for.
        playground_id: str
            The ID of the playground that evaluation datasets are returned for. Default is None.
        evaluation_dataset_configuration_id: Optional[str]
            The ID of the evaluation dataset configuration to fetch. Default is None.
        offset: Optional[int]
            The offset to start fetching evaluation datasets from. Default is 0.
        limit: Optional[int]
            The maximum number of evaluation datasets to return. Default is 100.
        sort: Optional[str]
            The order of return for evaluation datasets. Default is None, which returns sorting
            by creation time.
        search: Optional[str]
            A search term that filters results so that only evaluation datasets with names
            matching the string are returned. Default is None.
        correctness_only: Optional[bool]
            Whether to return only completed datasets (particularly applicable to completion of generated
            synthetic datasets). Default is False.
        completed_only: Optional[bool]
            Whether to return only completed datasets. Default is False.

        Returns
        -------
        evaluation_dataset_configurations: List[EvaluationDatasetConfiguration]
            A list of evaluation dataset configurations.
        """
        params = {
            "use_case_id": use_case_id,
            "playground_id": playground_id,
            "evaluation_dataset_configuration_id": evaluation_dataset_configuration_id,
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "search": search,
            "correctness_only": correctness_only,
            "completed_only": completed_only,
        }
        url = f"{cls._client.domain}/{cls._path}/"
        r_data = unpaginate(url, params, cls._client)
        return [cls.from_server_data(data) for data in r_data]

    @classmethod
    def create(
        cls,
        name: str,
        use_case_id: str,
        dataset_id: str,
        prompt_column_name: str,
        playground_id: str,
        is_synthetic_dataset: bool = False,
        response_column_name: Optional[str] = None,
        tool_calls_column_name: Optional[str] = None,
        agent_goals_column_name: Optional[str] = None,
    ) -> EvaluationDatasetConfiguration:
        """Create an evaluation dataset configuration for an existing dataset.

        Parameters
        ----------
        name: str
            The name of the evaluation dataset configuration.
        use_case_id: str
            The Use Case ID that the evaluation dataset configuration will be added to.
        dataset_id: str
            An ID, to add to the configuration, that identifies the evaluation dataset.
        playground_id: str
            The ID of the playground that the evaluation dataset configuration will be added to.
            Default is None.
        prompt_column_name: str
            The name of the prompt column in the dataset.
        response_column_name: str
            The name of the response column in the dataset.
        tool_calls_column_name : Optional[str]
            The name of the dataset column containing the expected tool calls.  It is required to evaluate
            the tool call accuracy metric for agentic workflows.
        agent_goals_column_name : Optional[str]
            The name of the dataset column containing the expected agent goals. It is required to
            evaluate the agent goal accuracy with reference metrics for agentic workflows.
        is_synthetic_dataset: bool
            Whether the evaluation dataset is synthetic.


        Returns
        -------
        evaluation_dataset_configuration : EvaluationDatasetConfiguration
            The created evaluation dataset configuration.

        """
        url = f"{cls._client.domain}/{cls._path}/"
        payload = {
            "name": name,
            "use_case_id": use_case_id,
            "dataset_id": dataset_id,
            "prompt_column_name": prompt_column_name,
            "response_column_name": response_column_name,
            "is_synthetic_dataset": is_synthetic_dataset,
            "playground_id": playground_id,
            "tool_calls_column_name": tool_calls_column_name,
            "agent_goals_column_name": agent_goals_column_name,
        }
        response = cls._client.post(url, data=payload)
        return cls.from_server_data(response.json())

    def update(
        self,
        name: Optional[str] = None,
        dataset_id: Optional[str] = None,
        prompt_column_name: Optional[str] = None,
        response_column_name: Optional[str] = None,
        tool_calls_column_name: Optional[str] = None,
        agent_goals_column_name: Optional[str] = None,
    ) -> EvaluationDatasetConfiguration:
        """Update the evaluation dataset configuration.

        Parameters
        ----------
        name: Optional[str]
            The name of the evaluation dataset configuration.
        dataset_id: Optional[str]
            The ID of the dataset used in this configuration.
        prompt_column_name : Optional[str]
            The name of the prompt column in the dataset.
        response_column_name : Optional[str]
            The name of the response column in the dataset.
        tool_calls_column_name : Optional[str]
            The name of the dataset column containing the expected tool calls.  It is required to evaluate
            the tool call accuracy metric for agentic workflows.
        agent_goals_column_name : Optional[str]
            The name of the dataset column containing the expected agent goals. It is required to
            evaluate the agent goal accuracy with reference metrics for agentic workflows.

        Returns
        -------
        evaluation_dataset_configuration : EvaluationDatasetConfiguration
            The updated evaluation dataset configuration.

        """
        payload = {
            "name": name,
            "dataset_id": dataset_id,
            "prompt_column_name": prompt_column_name,
            "response_column_name": response_column_name,
            "tool_calls_column_name": tool_calls_column_name,
            "agent_goals_column_name": agent_goals_column_name,
        }
        url = f"{self._client.domain}/{self._path}/{self.id}/"
        response = self._client.patch(url, data=payload)
        return self.from_server_data(response.json())

    def delete(self) -> None:
        """Delete the evaluation dataset configuration.

        Returns
        -------
        None
        """
        url = f"{self._client.domain}/{self._path}/{self.id}/"
        self._client.delete(url)
