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

from typing import Any, Dict, List, Optional

import trafaret as t

from datarobot.enums import DEFAULT_MAX_WAIT
from datarobot.models.api_object import APIObject
from datarobot.models.recipe_operation import WranglingOperation
from datarobot.utils.waiters import wait_for_async_resolution


class InputParameters(APIObject):
    """Input parameters required to generate time series transformation plan."""

    _converter = t.Dict(
        {
            t.Key("forecast_distances"): t.List(t.Int(gt=0)),
            t.Key("feature_derivation_windows"): t.List(t.Int(gt=0), min_length=1),
            t.Key("target_column"): t.String,
            t.Key("datetime_partition_column"): t.String,
            t.Key("multiseries_id_column", optional=True): t.Or(t.String, t.Null),
            t.Key("baseline_periods", optional=True): t.Or(t.List(t.Int(gt=0)), t.Null),
            t.Key("max_lag_order", optional=True): t.Or(t.Int(gt=0), t.Null),
            t.Key("number_of_operations_to_use", optional=True): t.Or(t.Int(gte=0), t.Null),
            t.Key("do_not_derive_columns", optional=True): t.Or(
                t.List(t.String(allow_blank=False)), t.Null
            ),
            t.Key("known_in_advance_columns", optional=True): t.Or(
                t.List(t.String(allow_blank=False)), t.Null
            ),
            t.Key("exclude_low_info_columns", optional=True): t.Or(t.Bool, t.Null),
            t.Key("feature_reduction_threshold", optional=True): t.Or(t.Float(gt=0, lte=1), t.Null),
        }
    ).allow_extra("*")

    def __init__(
        self,
        forecast_distances: list[int],
        feature_derivation_windows: list[int],
        target_column: str,
        datetime_partition_column: str,
        multiseries_id_column: Optional[str] = None,
        baseline_periods: Optional[list[int]] = None,
        max_lag_order: Optional[int] = None,
        number_of_operations_to_use: Optional[int] = None,
        do_not_derive_columns: Optional[list[str]] = None,
        known_in_advance_columns: Optional[list[str]] = None,
        exclude_low_info_columns: Optional[bool] = None,
        feature_reduction_threshold: Optional[float] = None,
    ):
        """Initialize input parameters.

        Parameters
        ----------
        forecast_distances:
            A list of forecast distances, which define the number of rows into the future to predict.
        feature_derivation_windows:
            A list of rolling windows of past values, defined in terms of rows, that are used to derive features.
        target_column:
            The column to be used as the target for modeling. This parameter is required for generating
            naive features and for selecting the most important features to recommend.
        datetime_partition_column:
            The column that is used to order the data.
        multiseries_id_column:
            The series ID column, if present. This column partitions data to create a multiseries modeling project.
        baseline_periods:
            A list of periodicities used to calculate naive target features.
        max_lag_order:
            The maximum lag order. This value cannot be greater than the largest feature derivation window.
        do_not_derive_columns:
            Columns to exclude from derivation; for each excluded column, only the first lag is added to the
            transformation plan.
        known_in_advance_columns:
            Columns that are known in advance (future values are known). Values for these known
            columns must be specified at prediction time.
        exclude_low_info_columns:
            Sets whether to ignore columns with low signal in the given sample. True by default.
        feature_reduction_threshold:
             Sets the threshold for feature reduction.  For example, if the value is 0.9, features that cumulatively
             reach 90% of importance are returned (up to 200 features).
        number_of_operations_to_use:
            Sets whether a transformation plan is suggested after the specified number of operations.
            Use this setting when a time series operation is already applied to the recipe,
            but you want an alternative recommendation with different parameters.
            No more than one time series operation is allowed in the recipe.
        """
        self.forecast_distances = forecast_distances
        self.feature_derivation_windows = feature_derivation_windows
        self.target_column = target_column
        self.datetime_partition_column = datetime_partition_column
        self.multiseries_id_column = multiseries_id_column
        self.baseline_periods = baseline_periods
        self.max_lag_order = max_lag_order
        self.number_of_operations_to_use = number_of_operations_to_use
        self.do_not_derive_columns = do_not_derive_columns
        self.known_in_advance_columns = known_in_advance_columns
        self.exclude_low_info_columns = exclude_low_info_columns
        self.feature_reduction_threshold = feature_reduction_threshold


class TimeSeriesTransformationPlan(APIObject):
    """Data wrangling entity, which contains all information needed to transform dataset and generate SQL."""

    _path = "recipes/{recipe_id}/timeseriesTransformationPlans/"
    _converter = t.Dict(
        {
            t.Key("input_parameters"): InputParameters._converter,
            t.Key("suggested_operations"): t.List(WranglingOperation._converter),
            t.Key("status"): t.String,
            t.Key("id"): t.String,
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        input_parameters: InputParameters,
        suggested_operations: List[Dict[str, Any]],
        status: str,
    ) -> None:
        self.id = id
        self.status = status
        self.input_parameters = input_parameters
        self.suggested_operations = suggested_operations

    @classmethod
    def compute(
        cls, recipe_id: str, input_parameters: InputParameters, max_wait: int = DEFAULT_MAX_WAIT
    ) -> TimeSeriesTransformationPlan:
        """Compute time series transformation plan."""
        path = cls._path.format(recipe_id=recipe_id)
        response = cls._client.post(path, input_parameters)
        finished_url = wait_for_async_resolution(
            cls._client, response.headers["Location"], max_wait=max_wait
        )
        r_data = cls._client.get(finished_url).json()
        return TimeSeriesTransformationPlan.from_server_data(r_data)

    @classmethod
    def get_plan(cls, recipe_id: str, transformation_plan_id: str) -> TimeSeriesTransformationPlan:
        """Retrieve TimeSeriesTransformationPlan by id."""
        path = cls._path.format(recipe_id=recipe_id) + f"{transformation_plan_id}/"
        response = cls._client.get(path)
        return TimeSeriesTransformationPlan.from_server_data(response.json())
