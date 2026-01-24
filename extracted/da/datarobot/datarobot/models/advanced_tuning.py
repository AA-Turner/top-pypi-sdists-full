#
# Copyright 2021-2025 DataRobot, Inc. and its affiliates.
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

from copy import deepcopy
from pprint import pformat
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, cast

import trafaret as t

from datarobot.enums import GridSearchAlgorithm, GridSearchSearchType, enum_to_list
from datarobot.models.api_object import APIObject

if TYPE_CHECKING:
    from datarobot.models.model import AdvancedTuningParamsType, Model, TuningParametersType
    from datarobot.models.modeljob import ModelJob

    class AugmentedTuningParametersType(TuningParametersType):
        value: Union[None, int, float, str, List[str]]


class NoParametersFoundException(Exception):
    """No parameters were found that matched the specified filter"""


class NonUniqueParametersException(Exception):
    """Multiple parameters were found that matched the specified filter"""

    def __init__(self, keys: Dict[str, Any], matching_params: List[TuningParametersType]) -> None:
        """Construct a NonUniqueParametersException

        Params
        ------
        keys : dict
            Keys used for filtering
        matching_params : list(dict)
            Parameters that matched the specified filter
        """
        self.matching_params = matching_params

        # Strip non-identifying fields from params for display purposes,
        # to make the error message more concise
        non_identifying_fields = {"defaultValue", "currentValue", "constraints"}
        filtered_params = [
            {key: value for key, value in param.items() if key not in non_identifying_fields}
            for param in matching_params
        ]

        message = dedent(
            """\
            Multiple matching parameters found for the specified keys.
            Keys: {}
            Parameters:
            {}"""
        ).format(pformat(keys), pformat(filtered_params))
        super().__init__(message)


class GridSearchArguments(APIObject):
    """
    Grid search arguments

    Attributes
    ----------
    search_type : GridSearchSearchType
        The type of grid search to be performed. If not specified, DataRobot performs Smart Search.
    algorithm : GridSearchAlgorithm (optional)
        The algorithm to apply when running the grid search.
        This is only applicable if the search type is specified and the search determines which algorithm to use.
        The following are the valid combinations of search type and algorithm:
        ------------------------------------------------------------
        | GridSearchSearchType.SMART | GridSearchAlgorithm.PATTERN_SEARCH (default) |
        | GridSearchSearchType.SMART | GridSearchAlgorithm.ACCELERATED_SEARCH |
        | GridSearchSearchType.BAYESIAN | GridSearchAlgorithm.TPE_SEARCH (default) |
        | GridSearchSearchType.BAYESIAN | GridSearchAlgorithm.GAUSSIAN_SEARCH |
        | GridSearchSearchType.BRUTE_FORCE | GridSearchAlgorithm.EXHAUSTIVE_SEARCH (default) |
        | GridSearchSearchType.BRUTE_FORCE | GridSearchAlgorithm.GREEDY_EXHAUSTIVE_SEARCH |
        ------------------------------------------------------------
    batch_size : int (optional)
        The number of iterations to perform in each batch.
    max_iterations : int (optional)
        Sets the maximum number of iterations to perform.
    random_state : int (optional)
        The random state/seed used for the grid search.
    wall_clock_time_limit : int (optional)
       The wall clock time limit, in seconds. The model with the best score, at this point, is selected.
    """

    _converter = t.Dict({
        t.Key("grid_search_arguments", optional=True): t.List(
            t.Dict({
                t.Key("search_type", optional=True): t.Enum(*enum_to_list(GridSearchSearchType)),
                t.Key("algorithm", optional=True): t.Enum(*enum_to_list(GridSearchAlgorithm)),
                t.Key("batch_size", optional=True): t.Int(),
                t.Key("max_iterations", optional=True): t.Int(),
                t.Key("random_state", optional=True): t.Int(),
                t.Key("wall_clock_time_limit", optional=True): t.Int(),
            })
        ),
    }).allow_extra("*")

    def __init__(
        self,
        search_type: Optional[GridSearchSearchType] = None,
        algorithm: Optional[GridSearchAlgorithm] = None,
        batch_size: Optional[int] = None,
        max_iterations: Optional[int] = None,
        random_state: Optional[int] = None,
        wall_clock_time_limit: Optional[int] = None,
    ) -> None:
        self.search_type = search_type if search_type else GridSearchSearchType.SMART
        self.algorithm = algorithm
        self.batch_size = batch_size
        self.max_iterations = max_iterations
        self.random_state = random_state
        self.wall_clock_time_limit = wall_clock_time_limit

    def to_api_payload(self) -> Dict[str, Any]:
        """Convert the GridSearchArguments to an API payload"""
        payload: Dict[str, Any] = {}
        if self.search_type:
            payload["searchType"] = self.search_type
        if self.algorithm:
            payload["algorithm"] = self.algorithm
        if self.batch_size:
            payload["batchSize"] = self.batch_size
        if self.max_iterations:
            payload["maxIterations"] = self.max_iterations
        if self.random_state:
            payload["randomState"] = self.random_state
        if self.wall_clock_time_limit:
            payload["wallClockTimeLimit"] = self.wall_clock_time_limit
        return payload


class AdvancedTuningSession:
    """A session enabling users to configure and run advanced tuning for a model.

    Every model contains a set of one or more tasks.  Every task contains a set of
    zero or more parameters.  This class allows tuning the values of each parameter
    on each task of a model, before running that model.

    This session is client-side only and is not persistent.
    Only the final model, constructed when `run` is called, is persisted on the DataRobot server.

    Attributes
    ----------
    description : str
        Description for the new advance-tuned model.
        Defaults to the same description as the base model.
    """

    def __init__(self, model: Model, grid_search_arguments: Optional[GridSearchArguments] = None) -> None:
        """Initiate an Advanced Tuning session.

        Params
        ------
        model : datarobot.models.model.Model
        grid_search_arguments : datarobot.models.advanced_tuning.GridSearchArguments
            Grid search arguments
        """
        self._new_values: Dict[str, Union[int, float, str, List[str]]] = {}
        self._grid_search_arguments = grid_search_arguments
        self._model = model

        param_info = model.get_advanced_tuning_parameters()
        self._available_params = param_info["tuning_parameters"]
        self.description = param_info.get("tuning_description")

    def _get_parameter_id(
        self,
        task_name: Optional[str] = None,
        parameter_name: Optional[str] = None,
        parameter_id: Optional[str] = None,
    ) -> str:
        """Return the ID of the one parameter that matches the specified fields.

        Returns
        -------
        str

        Raises
        ------
        NoParametersFoundException
            if no matching parameters are found.
        NonUniqueParametersException
            if multiple parameters matched the specified filtering criteria
        """
        filtered_params = (x for x in self._available_params)
        if parameter_id:
            # Should be unique but filter normally just in case it's ever not unique
            filtered_params = (x for x in filtered_params if x["parameter_id"] == parameter_id)
        if parameter_name:
            filtered_params = (x for x in filtered_params if x["parameter_name"] == parameter_name)
        if task_name:
            filtered_params = (x for x in filtered_params if x["task_name"] == task_name)

        filtered_params_list = list(filtered_params)

        if len(filtered_params_list) == 0:
            raise NoParametersFoundException(
                "No parameters found with task_name of {} and parameter_name of {}".format(
                    repr(task_name) if task_name else "(unspecified)",
                    repr(parameter_name) if parameter_name else "(unspecified)",
                )
            )

        if len(filtered_params_list) > 1:
            key = {}
            if task_name:
                key["task_name"] = task_name
            if parameter_name:
                key["parameter_name"] = parameter_name
            if parameter_id:
                key["parameter_id"] = parameter_id
            raise NonUniqueParametersException(key, filtered_params_list)

        return filtered_params_list[0]["parameter_id"]

    def get_task_names(self) -> List[str]:
        """Get the list of task names that are available for this model

        Returns
        -------
        list(str)
            List of task names
        """
        return sorted({x["task_name"] for x in self._available_params})

    def get_parameter_names(self, task_name: str) -> List[str]:
        """Get the list of parameter names available for a specific task

        Returns
        -------
        list(str)
            List of parameter names
        """
        return [x["parameter_name"] for x in self._available_params if x["task_name"] == task_name]

    def set_parameter(
        self,
        value: Union[int, float, str, List[str]],
        task_name: Optional[str] = None,
        parameter_name: Optional[str] = None,
        parameter_id: Optional[str] = None,
    ) -> None:
        """Set the value of a parameter to be used

        The caller must supply enough of the optional arguments to this function
        to uniquely identify the parameter that is being set.
        For example, a less-common parameter name such as
        'building_block__complementary_error_function' might only be used once (if at all)
        by a single task in a model.  In which case it may be sufficient to simply specify
        'parameter_name'.  But a more-common name such as 'random_seed' might be used by
        several of the model's tasks, and it may be necessary to also specify 'task_name'
        to clarify which task's random seed is to be set.
        This function only affects client-side state. It will not check that the new parameter
        value(s) are valid.

        Parameters
        ----------
        task_name : str
            Name of the task whose parameter needs to be set
        parameter_name : str
            Name of the parameter to set
        parameter_id : str
            ID of the parameter to set
        value : int, float, list, or str
            New value for the parameter, with legal values determined by the parameter being set

        Raises
        ------
        NoParametersFoundException
            if no matching parameters are found.
        NonUniqueParametersException
            if multiple parameters matched the specified filtering criteria
        """
        parameter_id = self._get_parameter_id(
            task_name=task_name, parameter_name=parameter_name, parameter_id=parameter_id
        )

        self._new_values[parameter_id] = value

    def _add_value_to_param(self, param: TuningParametersType) -> AugmentedTuningParametersType:
        """Given a 'param' dict, add a new user-specified value (if any) and return"""
        new_param = cast("AugmentedTuningParametersType", deepcopy(param))
        new_param["value"] = self._new_values.get(param["parameter_id"])
        return new_param

    def get_parameters(self) -> AdvancedTuningParamsType:
        """Returns the set of parameters available to this model

        The returned parameters have one additional key, "value", reflecting any new values that
        have been set in this AdvancedTuningSession.  When the session is run, "value" will be used,
        or if it is unset, "current_value".


        Returns
        -------
        parameters : dict
            "Parameters" dictionary, same as specified on `Model.get_advanced_tuning_params`.

        An additional field is added per parameter to the 'tuning_parameters' list in the dictionary:

        value : int, float, list, or str
            The current value of the parameter.  `None` if none has been specified.
        """

        return {
            "tuning_description": self.description,
            "tuning_parameters": [self._add_value_to_param(param) for param in self._available_params],
        }

    def run(self) -> ModelJob:
        """Submit this model for Advanced Tuning.

        Returns
        -------
        datarobot.models.modeljob.ModelJob
            The created job to build the model
        """
        return self._model.advanced_tune(self._new_values, self.description, self._grid_search_arguments)
