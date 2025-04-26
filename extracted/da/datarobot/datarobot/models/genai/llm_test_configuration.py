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

from mypy_extensions import TypedDict
import trafaret as t

from datarobot.enums import enum_to_list, LLMTestConfigurationType, PromptSamplingStrategy
from datarobot.models.api_object import APIObject
from datarobot.models.genai.evaluation_dataset_configuration import (
    evaluation_dataset_configuration_trafaret,
    EvaluationDatasetConfiguration,
)
from datarobot.models.genai.insights_configuration import (
    insight_configuration_trafaret,
    InsightsConfiguration,
    InsightsConfigurationDict,
)
from datarobot.models.genai.playground import Playground
from datarobot.models.use_cases.use_case import UseCase
from datarobot.models.use_cases.utils import get_use_case_id, resolve_use_cases, UseCaseLike
from datarobot.utils.pagination import unpaginate


def get_entity_id(entity: Union[LLMTestConfiguration, Playground, UseCase, str]) -> str:
    """
    Get the entity ID from the entity parameter.

    Parameters
    ----------
    entity : ApiObject or str
        May be the entity ID or the entity name.

    Returns
    -------
    id : str
        Entity ID
    """
    if isinstance(entity, str):
        return entity

    return entity.id


class DatasetEvaluationDict(TypedDict):
    evaluation_name: str
    evaluation_dataset_configuration_id: Optional[str]
    evaluation_dataset_name: str
    ootb_dataset: Optional[OOTBDatasetDict]
    insight_configuration: InsightsConfigurationDict
    insight_grading_criteria: InsightGradingCriteriaDict
    max_num_prompts: Optional[int]
    prompt_sampling_strategy: Optional[PromptSamplingStrategy]


class DatasetEvaluationRequestDict(TypedDict):
    ootb_dataset_name: str
    evaluation_name: str
    evaluation_dataset_configuration_id: Optional[str]
    insight_configuration: InsightsConfigurationDict
    insight_grading_criteria: InsightGradingCriteriaDict
    max_num_prompts: Optional[int]
    prompt_sampling_strategy: Optional[PromptSamplingStrategy]


class OOTBDatasetDict(TypedDict):
    dataset_url: Optional[str]
    dataset_name: str
    prompt_column_name: str
    response_column_name: Optional[str]
    rows_count: int
    warning: Optional[str]


class InsightGradingCriteriaDict(TypedDict):
    pass_threshold: int


class LLMTestGradingCriteriaDict(TypedDict):
    pass_threshold: int


class DatasetIdentifierDict(TypedDict):
    dataset_name: str
    dataset_id: Optional[str]


class DatasetsCompatibilityDict(TypedDict):
    insight_name: str
    incompatible_datasets: List[DatasetIdentifierDict]


ootb_dataset_trafaret = t.Dict(
    {
        t.Key("dataset_url", optional=True): t.Or(t.String, t.Null),
        t.Key("dataset_name"): t.String,
        t.Key("prompt_column_name"): t.String,
        t.Key("response_column_name", optional=True): t.Or(t.String, t.Null),
        t.Key("rows_count"): t.Int,
        t.Key("warning", optional=True): t.Or(t.String, t.Null),
    }
).ignore_extra("*")


insight_grading_criteria_trafaret = t.Dict(
    {
        t.Key("pass_threshold"): t.Int,
    }
).ignore_extra("*")

llm_test_grading_criteria_trafaret = t.Dict(
    {
        t.Key("pass_threshold"): t.Int,
    }
).ignore_extra("*")


dataset_evaluation_trafaret = t.Dict(
    {
        t.Key("evaluation_name"): t.String(allow_blank=True),
        t.Key("evaluation_dataset_configuration_id", optional=True): t.Or(t.String, t.Null),
        t.Key("evaluation_dataset_name"): t.String(allow_blank=True),
        t.Key("ootb_dataset", optional=True): t.Or(ootb_dataset_trafaret, t.Null),
        t.Key("insight_configuration"): insight_configuration_trafaret,
        t.Key("insight_grading_criteria"): insight_grading_criteria_trafaret,
        t.Key("max_num_prompts", optional=True): t.Or(t.Int, t.Null),
        t.Key("prompt_sampling_strategy", optional=True): t.Or(
            t.Enum(*enum_to_list(PromptSamplingStrategy)), t.Null
        ),
    }
).ignore_extra("*")


llm_test_configuration_trafaret = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("name"): t.String(allow_blank=True),
        t.Key("description"): t.String(allow_blank=True),
        t.Key("dataset_evaluations"): t.List(dataset_evaluation_trafaret),
        t.Key("use_case_id", optional=True): t.Or(t.String, t.Null),
        t.Key("creation_date", optional=True): t.Or(t.String, t.Null),
        t.Key("creation_user_id", optional=True): t.Or(t.String, t.Null),
        t.Key("llm_test_grading_criteria"): llm_test_grading_criteria_trafaret,
        t.Key("is_out_of_the_box_test_configuration"): t.Bool,
        t.Key("warnings", optional=True): t.List(t.Dict().allow_extra("*")),
    }
).ignore_extra("*")

dataset_identifier_trafaret = t.Dict(
    {
        t.Key("dataset_name"): t.String(allow_blank=True),
        t.Key("dataset_id", optional=True): t.Or(t.String, t.Null),
    }
).ignore_extra("*")

insight_to_eval_datasets_compatibility_trafaret = t.Dict(
    {
        t.Key("insight_name"): t.String,
        t.Key("incompatible_datasets"): t.List(dataset_identifier_trafaret),
    }
).ignore_extra("*")

llm_test_configuration_supported_insights_trafaret = t.Dict(
    {
        t.Key("supported_insight_configurations"): t.List(insight_configuration_trafaret),
        t.Key("datasets_compatibility"): t.List(insight_to_eval_datasets_compatibility_trafaret),
    }
).ignore_extra("*")


class DatasetIdentifier(APIObject):
    """
    Metadata for a DataRobot GenAI dataset identifier.

    Attributes
    ----------
    dataset_name: str
        The name of the dataset.
    dataset_id: str or None, optional
        The ID of the dataset.
    """

    _converter = dataset_identifier_trafaret

    def __init__(
        self,
        dataset_name: str,
        dataset_id: Optional[str] = None,
    ):
        self.dataset_name = dataset_name
        self.dataset_id = dataset_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(dataset_name={self.dataset_name})"

    def to_dict(self) -> DatasetIdentifierDict:
        return {
            "dataset_name": self.dataset_name,
            "dataset_id": self.dataset_id,
        }


class DatasetsCompatibility(APIObject):
    """
    Metadata for a DataRobot GenAI LLM test configuration supported insights datasets compatibility.

    Attributes
    ----------
    insight_name: str
        The name of the insight.
    incompatible_datasets: list[DatasetIdentifier]
        The incompatible datasets for the insight.
    """

    _converter = insight_to_eval_datasets_compatibility_trafaret

    def __init__(
        self,
        insight_name: str,
        incompatible_datasets: List[Dict[str, Any]],
    ):
        self.insight_name = insight_name
        self.incompatible_datasets = [
            DatasetIdentifier.from_server_data(dataset_identifier)
            for dataset_identifier in incompatible_datasets
        ]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(insight_name={self.insight_name})"

    def to_dict(self) -> DatasetsCompatibilityDict:
        return {
            "insight_name": self.insight_name,
            "incompatible_datasets": [dataset.to_dict() for dataset in self.incompatible_datasets],
        }


class NonOOTBDataset(APIObject):
    """
    Metadata for a DataRobot GenAI non out-of-the-box (OOTB) LLM compliance test dataset.
    """

    _path = "api/v2/genai/llmTestConfigurations/nonOotbDatasets"

    _converter = evaluation_dataset_configuration_trafaret

    def __init__(
        self,
        **kwargs: Any,
    ):
        self.non_ootb_dataset = EvaluationDatasetConfiguration(**kwargs)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.non_ootb_dataset.id}, "
            f"dataset_id={self.non_ootb_dataset.dataset_id})"
        )

    @classmethod
    def list(
        cls,
        use_case: Optional[Union[UseCase, str]] = None,
    ) -> List[NonOOTBDataset]:
        """
        List all non out-of-the-box datasets available to the user.

        Returns
        -------
        non_ootb_datasets : list[NonOOTBDataset]
            Returns a list of non out-of-the-box datasets.
        """
        url = f"{cls._client.domain}/{cls._path}/"
        params = resolve_use_cases(use_cases=use_case, params={}, use_case_key="use_case_id")
        r_data = unpaginate(url, params, cls._client)
        return [cls.from_server_data(data) for data in r_data]


class OOTBDataset(APIObject):
    """
    Metadata for a DataRobot GenAI out-of-the-box LLM compliance test dataset.

    Attributes
    ----------
    dataset_name: str
        The name of the dataset.
    prompt_column_name : str
        The name of the prompt column.
    response_column_name: str or None, optional
        The name of the response column, if any.
    dataset_url: str or None, optional
        The URL of the dataset.
    rows_count: int
        The number of rows in the dataset.
    warning: str or None, optional
        A warning message regarding the contents of the dataset, if any.
    """

    _path = "api/v2/genai/llmTestConfigurations/ootbDatasets"

    _converter = ootb_dataset_trafaret

    def __init__(
        self,
        dataset_name: str,
        prompt_column_name: str,
        rows_count: int,
        dataset_url: Optional[str] = None,
        response_column_name: Optional[str] = None,
        warning: Optional[str] = None,
    ):
        self.dataset_url = dataset_url
        self.dataset_name = dataset_name
        self.prompt_column_name = prompt_column_name
        self.response_column_name = response_column_name
        self.rows_count = rows_count
        self.warning = warning

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(dataset_url={self.dataset_url})"

    def to_dict(self) -> OOTBDatasetDict:
        return {
            "dataset_url": self.dataset_url,
            "dataset_name": self.dataset_name,
            "prompt_column_name": self.prompt_column_name,
            "response_column_name": self.response_column_name,
            "rows_count": self.rows_count,
            "warning": self.warning,
        }

    @classmethod
    def list(
        cls,
    ) -> List[OOTBDataset]:
        """
        List all out-of-the-box datasets available to the user.

        Returns
        -------
        ootb_datasets : list[OOTBDataset]
            Returns a list of out-of-the-box datasets.
        """
        url = f"{cls._client.domain}/{cls._path}/"
        r_data = unpaginate(url, None, cls._client)
        return [cls.from_server_data(data) for data in r_data]


class LLMTestGradingCriteria(APIObject):
    """
    Metadata for a GenAI LLM test grading criteria.

    Attributes
    ----------
    pass_threshold: int
        The threshold to pass the test.
    """

    _converter = insight_grading_criteria_trafaret

    def __init__(
        self,
        pass_threshold: int,
    ):
        self.pass_threshold = pass_threshold

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(pass_threshold={self.pass_threshold})"

    def to_dict(self) -> LLMTestGradingCriteriaDict:
        return {
            "pass_threshold": self.pass_threshold,
        }


class InsightGradingCriteria(APIObject):
    """
    Metadata for a GenAI LLM test insight grading criteria.

    Attributes
    ----------
    pass_threshold: int
        The threshold to pass the test.
    """

    _converter = insight_grading_criteria_trafaret

    def __init__(
        self,
        pass_threshold: int,
    ):
        self.pass_threshold = pass_threshold

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(pass_threshold={self.pass_threshold})"

    def to_dict(self) -> InsightGradingCriteriaDict:
        return {
            "pass_threshold": self.pass_threshold,
        }


class DatasetEvaluation(APIObject):
    """
    Metadata for a DataRobot GenAI dataset evaluation.

    Attributes
    ----------
    evaluation_name: str
        The name of the evaluation.
    evaluation_dataset_configuration_id: str or None, optional
        The ID of the evaluation dataset configuration for custom datasets.
    evaluation_dataset_name: str
        The name of the evaluation dataset.
    ootb_dataset: OOTBDataset or None, optional
        Out-of-the-box dataset.
    insight_configuration: InsightsConfiguration
        The insight to calculate for this dataset.
    insight_grading_criteria: InsightGradingCriteria
        The criteria to use for grading the results.
    max_num_prompts: int
        The maximum number of prompts to use for the evaluation.
    prompt_sampling_strategy: PromptSamplingStrategy
        The prompt sampling strategy for the dataset evaluation.
    """

    _converter = dataset_evaluation_trafaret

    def __init__(
        self,
        evaluation_name: str,
        insight_configuration: Dict[str, Any],
        insight_grading_criteria: Dict[str, Any],
        evaluation_dataset_name: str,
        max_num_prompts: Optional[int] = None,
        prompt_sampling_strategy: Optional[PromptSamplingStrategy] = None,
        evaluation_dataset_configuration_id: Optional[str] = None,
        ootb_dataset: Optional[Dict[str, Any]] = None,
    ):
        self.evaluation_name = evaluation_name
        self.evaluation_dataset_name = evaluation_dataset_name
        self.evaluation_dataset_configuration_id = evaluation_dataset_configuration_id
        self.ootb_dataset = OOTBDataset.from_server_data(ootb_dataset) if ootb_dataset else None
        self.insight_configuration = InsightsConfiguration.from_server_data(insight_configuration)
        self.insight_grading_criteria = InsightGradingCriteria.from_server_data(
            insight_grading_criteria
        )
        self.max_num_prompts = max_num_prompts
        self.prompt_sampling_strategy = prompt_sampling_strategy

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(evaluation_name={self.evaluation_name})"

    def to_dict(self) -> DatasetEvaluationDict:
        return {
            "evaluation_name": self.evaluation_name,
            "evaluation_dataset_configuration_id": self.evaluation_dataset_configuration_id,
            "evaluation_dataset_name": self.evaluation_dataset_name,
            "ootb_dataset": self.ootb_dataset.to_dict() if self.ootb_dataset else None,
            "insight_configuration": self.insight_configuration.to_dict(),
            "insight_grading_criteria": self.insight_grading_criteria.to_dict(),
            "max_num_prompts": self.max_num_prompts,
            "prompt_sampling_strategy": self.prompt_sampling_strategy,
        }


class LLMTestConfigurationSupportedInsights(APIObject):
    """
    Metadata for a DataRobot GenAI LLM test configuration supported insights.

    Attributes
    ----------
    supported_insight_configurations : list[InsightsConfiguration]
        The supported insights for LLM test configurations.
    """

    _path = "api/v2/genai/llmTestConfigurations/supportedInsights"

    _converter = llm_test_configuration_supported_insights_trafaret

    def __init__(
        self,
        supported_insight_configurations: List[Dict[str, Any]],
        datasets_compatibility: List[Dict[str, Any]],
    ):
        self.supported_insight_configurations = [
            InsightsConfiguration.from_server_data(insight_configuration)
            for insight_configuration in supported_insight_configurations
        ]
        self.datasets_compatibility = [
            DatasetsCompatibility.from_server_data(dataset_compatibility)
            for dataset_compatibility in datasets_compatibility
        ]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(supported_insight_configurations={self.supported_insight_configurations})"

    @classmethod
    def list(
        cls,
        use_case: Optional[Union[UseCase, str]] = None,
        playground: Optional[Union[Playground, str]] = None,
    ) -> LLMTestConfigurationSupportedInsights:
        """
        List all supported insights for a LLM test configuration.

        Parameters
        ----------
        use_case : Optional[Union[UseCase, str]], optional
            Returns only those supported insight configurations
            associated with a particular Use Case, specified by
            either the Use Case name or ID.
        playground : Optional[Union[Playground, str]], optional
            Returns only those supported insight configurations
            associated with a particular playground, specified by
            either the Playground or ID.

        Returns
        -------
        llm_test_configuration_supported_insights : LLMTestConfigurationSupportedInsights
            Returns the supported insight configurations for the
            LLM test configuration.
        """
        params = {
            "playground_id": get_entity_id(playground) if playground else None,
            "use_case_id": get_entity_id(use_case) if use_case else None,
        }
        url = f"{cls._client.domain}/{cls._path}/"
        r_data = cls._client.get(url, params=params)
        return cls.from_server_data(r_data.json())


class LLMTestConfiguration(APIObject):
    """
    Metadata for a DataRobot GenAI LLM test configuration.

    Attributes
    ----------
    id : str
        The LLM test configuration ID.
    name : str
        The LLM test configuration name.
    description : str
        The LLM test configuration description.
    dataset_evaluations : list[DatasetEvaluation]
        The dataset/insight combinations that make up the LLM test configuration.
    llm_test_grading_criteria : LLMTestGradingCriteria
        The criteria used to grade the result of the LLM test configuration.
    is_out_of_the_box_test_configuration : bool
        Whether this is an out-of-the-box configuration.
    use_case_id : Optional[str]
        The ID of the linked Use Case, if any.
    creation_date : Optional[str]
        The date the LLM test configuration was created, if any.
    creation_user_id : Optional[str]
        The ID of the creating user, if any.
    warnings: Optional[list[Dict[str, str]]]
        The warnings for the LLM test configuration, if any.
    """

    _path = "api/v2/genai/llmTestConfigurations"

    _converter = llm_test_configuration_trafaret

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        dataset_evaluations: List[Dict[str, Any]],
        llm_test_grading_criteria: Dict[str, Any],
        is_out_of_the_box_test_configuration: bool,
        use_case_id: Optional[str] = None,
        creation_date: Optional[str] = None,
        creation_user_id: Optional[str] = None,
        warnings: Optional[List[Dict[str, str]] | None] = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.use_case_id = use_case_id
        self.dataset_evaluations = [
            DatasetEvaluation.from_server_data(dataset_evaluation)
            for dataset_evaluation in dataset_evaluations
        ]
        self.llm_test_grading_criteria = LLMTestGradingCriteria.from_server_data(
            llm_test_grading_criteria
        )
        self.creation_date = creation_date
        self.creation_user_id = creation_user_id
        self.is_out_of_the_box_test_configuration = is_out_of_the_box_test_configuration
        self.warnings = warnings or []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"

    @classmethod
    def create(
        cls,
        name: str,
        dataset_evaluations: List[DatasetEvaluationRequestDict],
        llm_test_grading_criteria: LLMTestGradingCriteria,
        use_case: Optional[Union[UseCase, str]] = None,
        description: Optional[str] = None,
    ) -> LLMTestConfiguration:
        """
        Creates a new LLM test configuration.

        Parameters
        ----------
        name : str
            The LLM test configuration name.
        dataset_evaluations : list[DatasetEvaluationRequestDict]
            The LLM test dataset evaluation requests.
        llm_test_grading_criteria : LLMTestGradingCriteria
            The LLM test grading criteria.
        use_case : Optional[Union[UseCase, str]], optional
            Use case to link to the created llm test configuration.
        description : Optional[str]
            The LLM test configuration description. If None, the default,
            description returns an empty string.

        Returns
        -------
        llm_test_configuration : LLMTestConfiguration
            The created LLM test configuration.
        """
        payload: Dict[str, Any] = {
            "name": name,
            "use_case_id": get_use_case_id(use_case, is_required=True),
            "dataset_evaluations": dataset_evaluations,
            "llm_test_grading_criteria": llm_test_grading_criteria.to_dict(),
        }
        if description:
            payload["description"] = description

        url = f"{cls._client.domain}/{cls._path}/"
        r_data = cls._client.post(url, json=payload)
        return cls.from_server_data(r_data.json())

    @classmethod
    def get(
        cls,
        llm_test_configuration: Union[LLMTestConfiguration, str],
    ) -> LLMTestConfiguration:
        """
        Retrieve a single LLM Test configuration.

        Parameters
        ----------
        llm_test_configuration : LLMTestConfiguration or str
            The LLM test configuration to retrieve, either LLMTestConfiguration or LLMTestConfiguration ID.

        Returns
        -------
        llm_test_configuration : LLMTestConfiguration
            The requested LLM Test configuration.
        """
        url = f"{cls._client.domain}/{cls._path}/{get_entity_id(llm_test_configuration)}/"
        r_data = cls._client.get(url)
        return cls.from_server_data(r_data.json())

    @classmethod
    def list(
        cls,
        use_case: Optional[UseCaseLike] = None,
        test_config_type: Optional[LLMTestConfigurationType] = None,
    ) -> List[LLMTestConfiguration]:
        """
        List all LLM test configurations available to the user. If a Use Case is specified,
        results are restricted to only those configurations associated with that Use Case.

        Parameters
        ----------
        use_case : Optional[UseCaseLike], optional
            Returns only those configurations associated with a particular Use Case,
            specified by either the Use Case name or ID.
        test_config_type : Optional[LLMTestConfigurationType], optional
            Returns only configurations of the specified type. If not specified,
            the custom test configurations are returned.

        Returns
        -------
        llm_test_configurations : list[LLMTestConfiguration]
            Returns a list of LLM test configurations.
        """
        params = {}
        if test_config_type:
            params["test_config_type"] = test_config_type
        params = resolve_use_cases(use_cases=use_case, params=params, use_case_key="use_case_id")
        url = f"{cls._client.domain}/{cls._path}/"
        r_data = unpaginate(url, params, cls._client)
        return [cls.from_server_data(data) for data in r_data]

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        dataset_evaluations: Optional[List[DatasetEvaluationRequestDict]] = None,
        llm_test_grading_criteria: Optional[LLMTestGradingCriteria] = None,
    ) -> LLMTestConfiguration:
        """
        Update the LLM test configuration.

        Parameters
        ----------
        name : Optional[str]
            The new LLM test configuration name.
        description : Optional[str]
            The new LLM test configuration description.
        dataset_evaluations : list[DatasetEvaluationRequestDict], optional
            The new dataset evaluation requests.
        llm_test_grading_criteria : LLMTestGradingCriteria, optional
            The new grading criteria.

        Returns
        -------
        llm_test_configuration : LLMTestConfiguration
            The updated LLM test configuration.
        """
        payload: Dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if dataset_evaluations is not None:
            payload["dataset_evaluations"] = dataset_evaluations
        if llm_test_grading_criteria is not None:
            payload["llm_test_grading_criteria"] = llm_test_grading_criteria.to_dict()
        url = f"{self._client.domain}/{self._path}/{self.id}/"
        r_data = self._client.patch(url, json=payload)
        return self.from_server_data(r_data.json())

    def delete(self) -> None:
        """
        Delete a single LLM test configuration.
        """
        url = f"{self._client.domain}/{self._path}/{self.id}/"
        self._client.delete(url)
