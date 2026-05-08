#
# Copyright 2023-2026 DataRobot, Inc. and its affiliates.
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

from typing import Any, Dict, List, Optional, Tuple, Union

import trafaret as t

from datarobot._compat import Literal, TypedDict
from datarobot.models.api_object import APIObject
from datarobot.models.genai.custom_model_validation import get_entity_id
from datarobot.models.genai.playground import Playground
from datarobot.models.use_cases.utils import UseCaseLike, resolve_use_cases
from datarobot.utils.pagination import unpaginate
from datarobot.utils.waiters import wait_for_async_resolution

DirectionType = Literal["maximize", "minimize"]
ObjectiveType = Literal[
    "correctness",
    "latency",
    "citations",
    "rouge_1",
    "faithfulness",
    "prompt_tokens",
    "response_tokens",
    "document_tokens",
    "all_tokens",
    "jailbreak_violation",
    "toxicity_violation",
    "pii_violation",
]


class LlmConfig(TypedDict, total=False):
    llm_names: List[str]
    temperature_min: float
    temperature_max: float
    temperature_step: float
    top_p_min: float
    top_p_max: float
    top_p_step: float


class ChunkingParameters(TypedDict, total=False):
    embedding_model_names: List[str]
    chunking_methods: List[str]
    chunk_size_min_exp: int
    chunk_size_max_exp: int
    chunk_overlap_percentage_min: float
    chunk_overlap_percentage_max: float
    chunk_overlap_percentage_step: float


class VectorDatabaseSettings(TypedDict, total=False):
    retrievers: List[str]
    add_neighbor_chunks: List[bool]
    max_document_retrieved_per_prompt_min: int
    max_document_retrieved_per_prompt_max: int
    max_document_retrieved_per_prompt_step: int
    retrieval_modes: List[str]
    max_mmr_lambda_min: float
    max_mmr_lambda_max: float
    max_mmr_lambda_step: float
    chunking_methods: List[str]
    chunk_size_min_exp: int
    chunk_size_max_exp: int
    chunk_overlap_percentage_min: float
    chunk_overlap_percentage_max: float
    chunk_overlap_percentage_step: float


class SearchSpaceDict(TypedDict):
    llm_config: LlmConfig
    chunking_parameters: ChunkingParameters
    vector_database_settings: VectorDatabaseSettings


search_direction_trafaret = t.Enum("maximize", "minimize")
search_objective_trafaret = t.Enum(
    "correctness",
    "latency",
    "citations",
    "rouge_1",
    "faithfulness",
    "prompt_tokens",
    "response_tokens",
    "document_tokens",
    "all_tokens",
    "jailbreak_violation",
    "toxicity_violation",
    "pii_violation",
)

llm_config_trafaret = t.Dict({
    t.Key("llm_names"): t.List(t.String),
    t.Key("temperature_min", default=0.0): t.Float,
    t.Key("temperature_max", default=1.0): t.Float,
    t.Key("temperature_step", default=0.05): t.Float,
    t.Key("top_p_min", default=0.0): t.Float,
    t.Key("top_p_max", default=1.0): t.Float,
    t.Key("top_p_step", default=0.05): t.Float,
})

chunking_parameters_config_trafaret = t.Dict({
    t.Key("embedding_model_names"): t.List(t.String),
    t.Key("chunking_methods", default=["recursive"]): t.List(t.String),
    t.Key("chunk_size_min_exp", default=7): t.Int,
    t.Key("chunk_size_max_exp", default=8): t.Int,
    t.Key("chunk_overlap_percentage_min", default=0.0): t.Float,
    t.Key("chunk_overlap_percentage_max", default=50.0): t.Float,
    t.Key("chunk_overlap_percentage_step", default=10.0): t.Float,
})


vector_database_config_trafaret = t.Dict({
    t.Key("retrievers"): t.List(t.String),
    t.Key("add_neighbor_chunks", default=[True, False]): t.List(t.Bool),
    t.Key("max_document_retrieved_per_prompt_min", default=1): t.Int,
    t.Key("max_document_retrieved_per_prompt_max", default=10): t.Int,
    t.Key("max_document_retrieved_per_prompt_step", default=1): t.Int,
    t.Key("retrieval_modes"): t.List(t.String),
    t.Key("max_mmr_lambda_min", default=0.0): t.Float,
    t.Key("max_mmr_lambda_max", default=1.0): t.Float,
    t.Key("max_mmr_lambda_step", default=0.1): t.Float,
    t.Key("chunking_methods", default=["recursive"]): t.List(t.String),
    t.Key("chunk_size_min_exp", default=7): t.Int,
    t.Key("chunk_size_max_exp", default=8): t.Int,
    t.Key("chunk_overlap_percentage_min", default=0.0): t.Float,
    t.Key("chunk_overlap_percentage_max", default=50.0): t.Float,
    t.Key("chunk_overlap_percentage_step", default=10.0): t.Float,
})

search_space_trafaret = t.Dict({
    t.Key("llm_config"): llm_config_trafaret,
    t.Key("chunking_parameters"): chunking_parameters_config_trafaret,
    t.Key("vector_database_settings"): vector_database_config_trafaret,
})


agentic_search_request_trafaret = t.Dict({
    t.Key("use_case_id"): t.String,
    t.Key("playground_id"): t.String,
    t.Key("grounding_dataset_id"): t.String,
    t.Key("eval_dataset_id"): t.String,
    t.Key("num_trials"): t.Int,
    t.Key("num_concurrent_trials"): t.Int,
    t.Key("optimization_objectives"): t.List(t.Tuple(search_objective_trafaret, search_direction_trafaret)),
    t.Key("search_space"): search_space_trafaret,
    t.Key("name"): t.String,
})

job_status_trafaret = t.Enum("RUNNING", "COMPLETED", "FAILED")

# Null values are dropped during camelCase→snake_case conversion.
# Hence add default=None to all nullable trafaret keys
pareto_frontier_point_traferet = t.Dict({
    t.Key("datetime_start"): t.String,
    t.Key("datetime_complete"): t.String,
    t.Key("llm_blueprint_name", default=None): t.Or(t.String, t.Null),
    t.Key("llm_blueprint_id", default=None): t.Or(t.String, t.Null),
    t.Key("vector_database_id", default=None): t.Or(t.String, t.Null),
    t.Key("values"): t.List(t.Float),
    t.Key("search_parameters"): t.Dict(allow_extra=["*"]),
})

history_point_trafaret = t.Dict({
    t.Key("llm_blueprint_id", default=None): t.Or(t.String, t.Null),
    t.Key("vector_database_id", default=None): t.Or(t.String, t.Null),
    t.Key("values"): t.List(t.Float),
    t.Key("search_parameters"): t.Dict(allow_extra=["*"]),
})

search_study_response_trafaret = t.Dict({
    t.Key("search_space", default=None): t.Or(search_space_trafaret, t.Null),
    t.Key("use_case_id"): t.String,
    t.Key("grounding_dataset_id"): t.String,
    t.Key("eval_dataset_id"): t.String,
    t.Key("grounding_dataset_name"): t.String,
    t.Key("eval_dataset_name"): t.String,
    t.Key("user_id"): t.String,
    t.Key("user_name"): t.String,
    t.Key("num_trials"): t.Int,
    t.Key("num_concurrent_trials"): t.Int,
    t.Key("optimization_objectives"): t.List(t.Tuple(search_objective_trafaret, search_direction_trafaret)),
    t.Key("playground_id"): t.String,
    t.Key("temp_playground_id", default=None): t.Or(t.String, t.Null),
    t.Key("pareto_front", default=None): t.Or(t.List(pareto_frontier_point_traferet), t.Null),
    t.Key("datetime_start"): t.String,
    t.Key("datetime_end", default=None): t.Or(t.String, t.Null),
    t.Key("study_status"): job_status_trafaret,
    t.Key("search_study_id"): t.String,
    t.Key("name"): t.String,
    t.Key("job_id", default=None): t.Or(t.String, t.Null),
    t.Key("trials_running", default=None): t.Or(t.Int, t.Null),
    t.Key("trials_failed", default=None): t.Or(t.Int, t.Null),
    t.Key("trials_success", default=None): t.Or(t.Int, t.Null),
    t.Key("all_trials", default=None): t.Or(t.List(history_point_trafaret), t.Null),
    t.Key("existing_blueprint_ids", default=None): t.Or(t.List(t.String), t.Null),
    t.Key("eval_results", default=None): t.Or(t.List(t.Any), t.Null),
    t.Key("error_message", default=None): t.Or(t.String, t.Null),
})


class SearchStudy(APIObject):
    """
    Metadata for a DataRobot syftr search study.

    Parameters
    ----------
    search_space : Optional[Dict[str, Any]]
        Search space configuration used for the study.
    use_case_id : str
        The ID of the use case the search study is linked to.
    grounding_dataset_id : str
        The ID of the dataset used to build vector databases.
    eval_dataset_id : str
        The ID of the evaluation dataset.
    grounding_dataset_name : str
        The name of the grounding dataset.
    eval_dataset_name : str
        The name of the evaluation dataset.
    user_id : str
        The ID of the user.
    user_name : str
        The name of the user who ran the study.
    num_trials : int
        The number of search trials to sample.
    num_concurrent_trials : int
        The number of simultaneously running trials.
    optimization_objectives : List[Tuple[str, str]]
        Optimization objectives of the study, defined as (objective, direction) pairs.
    playground_id : str
        The ID of the associated playground.
    temp_playground_id : Optional[str]
        The ID of the temporary playground.
    pareto_front : Optional[List[Dict[str, Any]]]
        Pareto frontier of the study.
    datetime_start : str
        Study start time.
    datetime_end : Optional[str]
        Study end time.
    study_status : str
        Status of the study (e.g., RUNNING, COMPLETED, FAILED).
    search_study_id : str
        The ID of the search study.
    name : str
        Name of the search study.
    job_id : Optional[str]
        The ID of the worker job (UUID4).
    trials_running : Optional[int]
        Number of currently running trials.
    trials_failed : Optional[int]
        Number of failed trials.
    trials_success : Optional[int]
        Number of completed trials.
    all_trials : Optional[List[Dict[str, Any]]]
        Trials history.
    existing_blueprint_ids : Optional[List[str]]
        IDs of existing LLM blueprints for comparative evaluation.
    eval_results : Optional[List[Any]]
        Results of the comparative evaluation.
    error_message : Optional[str]
        Error message if the study fails.
    """

    _path = "api/v2/genai/syftrSearch"

    _converter = search_study_response_trafaret

    def __init__(
        self,
        search_space: Optional[Dict[str, Any]],
        use_case_id: str,
        grounding_dataset_id: str,
        eval_dataset_id: str,
        grounding_dataset_name: str,
        eval_dataset_name: str,
        user_id: str,
        user_name: str,
        num_trials: int,
        num_concurrent_trials: int,
        optimization_objectives: List[Tuple[str, str]],
        playground_id: str,
        temp_playground_id: Optional[str],
        pareto_front: Optional[List[Dict[str, Any]]],
        datetime_start: str,
        datetime_end: Optional[str],
        study_status: str,
        search_study_id: str,
        name: str,
        job_id: Optional[str],
        trials_running: Optional[int],
        trials_failed: Optional[int],
        trials_success: Optional[int],
        all_trials: Optional[List[Dict[str, Any]]],
        existing_blueprint_ids: Optional[List[str]],
        eval_results: Optional[List[Any]],
        error_message: Optional[str],
    ):
        self.search_space = search_space
        self.use_case_id = use_case_id
        self.grounding_dataset_id = grounding_dataset_id
        self.eval_dataset_id = eval_dataset_id
        self.grounding_dataset_name = grounding_dataset_name
        self.eval_dataset_name = eval_dataset_name
        self.user_id = user_id
        self.user_name = user_name
        self.num_trials = num_trials
        self.num_concurrent_trials = num_concurrent_trials
        self.optimization_objectives = optimization_objectives
        self.playground_id = playground_id
        self.temp_playground_id = temp_playground_id
        self.pareto_front = pareto_front
        self.datetime_start = datetime_start
        self.datetime_end = datetime_end
        self.study_status = study_status
        self.search_study_id = search_study_id
        self.name = name
        self.job_id = job_id
        self.trials_running = trials_running
        self.trials_failed = trials_failed
        self.trials_success = trials_success
        self.all_trials = all_trials
        self.existing_blueprint_ids = existing_blueprint_ids
        self.eval_results = eval_results
        self.error_message = error_message

    @classmethod
    def create(
        cls,
        use_case_id: str,
        playground_id: str,
        grounding_dataset_id: str,
        eval_dataset_id: str,
        num_trials: int,
        num_concurrent_trials: int,
        optimization_objectives: List[Tuple[ObjectiveType, DirectionType]],
        search_space: SearchSpaceDict,
        name: str,
    ) -> SearchStudy:
        """
        Create a new search search study with the specified parameters.

        Parameters
        ----------
        use_case_id : str
            The ID of the use case the search study is linked to.
        playground_id : str
            The ID of the existing playground associated with the search.
        grounding_dataset_id : str
            The ID of the dataset used to build vector databases.
        eval_dataset_id : str
            The ID of the evaluation dataset.
        num_trials : int
            The number of search trials to sample.
        num_concurrent_trials : int
            The number of simultaneously running trials.
        optimization_objectives : List[Tuple[ObjectiveType, DirectionType]]
            Optimization objectives of the study, defined as (objective, direction) pairs.
        search_space : SearchSpaceDict
            Search space configuration for the search.

        Returns
        -------
        search study : SearchStudy
            The created search study.
        """
        payload = agentic_search_request_trafaret.check({
            "use_case_id": use_case_id,
            "playground_id": playground_id,
            "grounding_dataset_id": grounding_dataset_id,
            "eval_dataset_id": eval_dataset_id,
            "num_trials": num_trials,
            "num_concurrent_trials": num_concurrent_trials,
            "optimization_objectives": optimization_objectives,
            "search_space": search_space,
            "name": name,
        })
        r_data = cls._client.post(f"{cls._client.domain}/{cls._path}/", data=payload)
        location = wait_for_async_resolution(cls._client, r_data.headers["Location"])
        return cls.from_location(location)

    @classmethod
    def get(cls, search_study_id: str) -> SearchStudy:
        """
        Read an existing search study.

        Parameters
        ----------
        search_study_id : str
            ID of the search study used for creation.

        Returns
        -------
        search study : SearchStudy
            The created search study database.
        """
        search_data = cls._client.get(f"{cls._client.domain}/{cls._path}/{search_study_id}/")
        return cls.from_server_data(search_data.json())

    @classmethod
    def list(
        cls,
        use_case: UseCaseLike,
        playground: Optional[Union[Playground, str]] = None,
        offset: int = 0,
        limit: int = 200,
        search: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> List[SearchStudy]:
        """
        List all syftr search studies associated with a specific use case available to the user.

        Parameters
        ----------
        use_case : UseCaseLike
            The returned search studies are filtered to those associated with a specific Use
            Case(s) if specified or can be inferred from the context.
            Accepts either the entity or the ID.
        playground : Optional[Union[Playground, str]], optional
            The returned search studies are filtered to those associated with a specific playground
            if it is specified. Accepts either the entity or the ID.
        search : Optional[str]
            String for filtering search studies.
            Search studies that contain the string in name will be returned.
            If not specified, all search studies  will be returned.
        sort : Optional[str]
            Property to sort search studies by.
            Prefix the attribute name with a dash to sort in descending order,
            e.g., sort='-creationDate'.
            Currently supported options are  "name".

        Returns
        -------
        search studies : list[SearchStudy]
            A list of search studies available to the user.
        """
        params = {
            "search": search,
            "sort": sort,
            "offset": offset,
            "limit": limit,
            "playground_id": get_entity_id(playground) if playground else None,
        }
        params = resolve_use_cases(use_cases=use_case, params=params, use_case_key="use_case_id")
        url = f"{cls._client.domain}/{cls._path}/"
        r_data = unpaginate(url, params, cls._client)
        return [cls.from_server_data(data) for data in r_data]

    def delete(self) -> None:
        """
        Delete the search study and all its related artifacts.
        """
        url = f"{self._client.domain}/{self._path}/{self.search_study_id}/"
        response_data = self._client.delete(url)
        wait_for_async_resolution(self._client, response_data.headers["Location"])
