#
# Copyright 2026 DataRobot, Inc. and its affiliates.
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

from datarobot._experimental.models.enums import (
    CustomLossesModelType,
    CustomMetricsLossesTargetType,
)
from datarobot.enums import enum_to_list
from datarobot.models.api_object import APIObject
from datarobot.utils import camelize


class CustomMetric:
    """
    Class contains information about custom metric for each item in
    the custom metrics list in custom metrics and losses metadata.
    """

    converter = t.Dict({
        t.Key("name"): t.String(),
        t.Key("label"): t.String(),
        t.Key("lower_is_better", optional=True): t.Bool(),
        t.Key("description", optional=True): t.String(),
        t.Key("target_type"): t.Enum(*enum_to_list(CustomMetricsLossesTargetType)),
        t.Key("entry_point"): t.String(),
        t.Key("primary_metric"): t.Bool(),
        t.Key("use_weights", optional=True): t.Bool(),
    }).allow_extra("*")

    def __init__(
        self,
        name: str,
        label: str,
        target_type: str,
        entry_point: str,
        primary_metric: bool,
        lower_is_better: Optional[bool] = True,
        description: Optional[str] = "Untitled",
        use_weights: Optional[bool] = False,
    ) -> None:
        """Initiate an custom metric.

        Params
        ------
        name : str
            Custom metrics function name. Must match the python code function name.
        label : str
            Custom metrics UI label. Will appear in metrics list in UI screen.
        target_type : str
            Custom metric target type. For example Binary, Regression, or Multiclass.
        entry_point : str
            Custom metric function entry point in the python code on LRS.
        primary_metric : bool
            Indicates whether this metric is used for project gridsearch hyperparameter search.
        lower_is_better : bool (default True)
            Indicates whether to maximize or minimize the metric function.
        description : str (default Untitled)
            Custom metric description.
        use_weights : bool (default False)
            Indicates whether this metric is using weights.
        """
        self.name = name
        self.label = label
        self.lower_is_better = lower_is_better
        self.description = description
        self.target_type = target_type
        self.entry_point = entry_point
        self.primary_metric = primary_metric
        self.use_weights = use_weights

    def to_dict(self, camel_type: Optional[bool] = False) -> Dict[str, Any]:
        """Convert class to dictionary in api format"""
        data_dict = {
            "name": self.name,
            "label": self.label,
            "lower_is_better": self.lower_is_better,
            "description": self.description,
            "target_type": self.target_type,
            "entry_point": self.entry_point,
            "primary_metric": self.primary_metric,
            "use_weights": self.use_weights,
        }
        if camel_type:
            data_dict = {camelize(key): val for key, val in data_dict.items()}
        return data_dict


class CustomLoss:
    """
    Class contains information about custom loss for each item in
    the custom losses list in custom metrics and losses metadata.
    """

    converter = t.Dict({
        t.Key("name"): t.String(),
        t.Key("label"): t.String(),
        t.Key("description", optional=True): t.String(),
        t.Key("target_type"): t.Enum(*enum_to_list(CustomMetricsLossesTargetType)),
        t.Key("entry_point"): t.String(),
        t.Key("use_weights", optional=True): t.Bool(),
        t.Key("use_offset", optional=True): t.Bool(),
        t.Key("model_type", optional=True): t.Enum(*enum_to_list(CustomLossesModelType)),
    }).allow_extra("*")

    def __init__(
        self,
        name: str,
        label: str,
        target_type: str,
        entry_point: str,
        model_type: Optional[str] = "xgboost",
        description: Optional[str] = "Untitled",
        use_weights: Optional[bool] = False,
        use_offset: Optional[bool] = False,
    ) -> None:
        """Initiate an custom metric.

        Params
        ------
        name : str
            Custom loss function name. Must match the python code function name.
        label : str
            Custom loss UI label. Will appear in metrics list in UI screen.
        target_type : str
            Custom loss target type. For example Binary, Regression, or Multiclass.
        entry_point : str
            Custom loss function entry point in the python code on LRS.
        model_type : str
            Specifies what model family this loss function applies.
        description : str (default Untitled)
            Custom loss description.
        use_weights : bool (default False)
            Indicates whether this loss is using weights.
        use_offset : bool (default False)
            Indicates whether this loss is using offset.
        """
        self.name = name
        self.label = label
        self.description = description
        self.target_type = target_type
        self.entry_point = entry_point
        self.use_weights = use_weights
        self.use_offset = use_offset
        self.model_type = model_type

    def to_dict(self, camel_type: Optional[bool] = False) -> Dict[str, Any]:
        """Convert class to dictionary"""
        data_dict = {
            "name": self.name,
            "label": self.label,
            "description": self.description,
            "target_type": self.target_type,
            "entry_point": self.entry_point,
            "use_weights": self.use_weights,
            "use_offset": self.use_offset,
            "model_type": self.model_type,
        }
        if camel_type:
            data_dict = {camelize(key): val for key, val in data_dict.items()}
        return data_dict


class CustomMetricsLossesMetadata(APIObject):
    """
    Class that allows users to setup the custom metrics metadata

    Every project can contains only one unique metadata.
    This class allows interactively validate the custom metrics and losses
    before setting target on specific project.

    This session is client-side only and is not persistent.
    """

    _converter = t.Dict({
        t.Key("id", optional=True): str,
        t.Key("project_id"): str,
        t.Key("custom_metrics_losses_catalog_id"): str,
        t.Key("base_image_id", optional=True): str,
        t.Key("metrics"): t.List(CustomMetric.converter, min_length=0),
        t.Key("losses"): t.List(CustomLoss.converter, min_length=0),
        t.Key("selected_metrics", optional=True): t.List(CustomMetric.converter, min_length=0),
        t.Key("selected_losses", optional=True): t.List(CustomLoss.converter, min_length=0),
        t.Key("is_target_set", optional=True): t.Bool(),
    }).allow_extra("*")

    def __init__(
        self,
        project_id: str,
        custom_metrics_losses_catalog_id: str,
        metrics: List[Dict[str, Any]],
        losses: Optional[List[Dict[str, Any]]] = None,
        id: Optional[str] = None,
        base_image_id: Optional[str] = None,
        selected_metrics: Optional[List[Dict[str, Any]]] = None,
        selected_losses: Optional[List[Dict[str, Any]]] = None,
        is_target_set: Optional[bool] = False,
    ) -> None:
        """Initiate an custom metrics metadata.

        Params
        ------
        project_id : str
            The project ID that the custom metrics is used.
        custom_metrics_losses_catalog_id : str (default None)
            The catalog item ID that was created with the files API.
        metrics : list(CustomMetric)
            List of custom metrics.
        losses : list(CustomLoss)
            List of custom losses.
        id : str
            The ID of this custom metrics metadata.
        base_image_id : str (default None)
            The base image ID.
        selected_metrics : list(CustomMetric) (default None)
            List of selected custom metrics.
        selected_losses : list(CustomLoss) (default None)
            List of selected custom losses.
        is_target_set : bool (default False)
            Indicates whether the target was set in metadata during project creation.
        """
        self._set_values(
            project_id=project_id,
            custom_metrics_losses_catalog_id=custom_metrics_losses_catalog_id,
            metrics=metrics,
            losses=losses,
            id=id,
            base_image_id=base_image_id,
            selected_metrics=selected_metrics,
            selected_losses=selected_losses,
            is_target_set=is_target_set,
        )

    def _set_values(
        self,
        project_id: str,
        custom_metrics_losses_catalog_id: str,
        metrics: List[Dict[str, Any]],
        losses: Optional[List[Dict[str, Any]]] = None,
        id: Optional[str] = None,
        base_image_id: Optional[str] = None,
        selected_metrics: Optional[List[Dict[str, Any]]] = None,
        selected_losses: Optional[List[Dict[str, Any]]] = None,
        is_target_set: Optional[bool] = False,
    ) -> None:
        """helper to deal with some extra logic"""
        self.id = id
        self.project_id = project_id
        self.custom_metrics_losses_catalog_id = custom_metrics_losses_catalog_id
        self.base_image_id = base_image_id
        self.is_target_set = is_target_set
        metrics = metrics if metrics is not None else []
        losses = losses if losses is not None else []
        selected_metrics = selected_metrics if selected_metrics is not None else []
        selected_losses = selected_losses if selected_losses is not None else []
        self.metrics = [CustomMetric(**metric) for metric in metrics]
        self.losses = [CustomLoss(**loss) for loss in losses]
        self.selected_metrics = [CustomMetric(**metric) for metric in selected_metrics]
        self.selected_losses = [CustomLoss(**loss) for loss in selected_losses]

    def list_metrics_names(self, target_type: Optional[str] = None) -> List[str]:
        """returns names of metrics by target type if specified

        Params
        ------
        target_type : str
            The project type with values in CUSTOM_METRICS_LOSSES_TARGET_TYPES.
        """

        if target_type is None:
            return [metric.name for metric in self.metrics]
        if target_type not in enum_to_list(CustomMetricsLossesTargetType):
            msg = f"Unknown target type {target_type}."
            raise ValueError(msg)
        return [metric.name for metric in self.metrics if metric.target_type == target_type]

    def list_losses_names(self, target_type: Optional[str] = None) -> List[str]:
        """returns names of losses by target type if specified

        Params
        ------
        target_type : str
            The project type with values in CUSTOM_METRICS_LOSSES_TARGET_TYPES.

        Raises
        ------
        ValueError
            Raised if an target type is invalid.
        """
        if target_type is None:
            return [loss.name for loss in self.losses]
        if target_type not in enum_to_list(CustomMetricsLossesTargetType):
            msg = f"Unknown target type {target_type}"
            raise ValueError(msg)
        return [loss.name for loss in self.losses if loss.target_type == target_type]

    def to_dict(self, camel_type: Optional[bool] = False) -> Dict[str, Any]:
        """Convert class to dictionary"""
        data_dict = {
            "id": self.id,
            "project_id": self.project_id,
            "custom_metrics_losses_catalog_id": self.custom_metrics_losses_catalog_id,
            "base_image_id": self.base_image_id,
            "metrics": [metric.to_dict(camel_type=camel_type) for metric in self.metrics],
            "losses": [loss.to_dict(camel_type=camel_type) for loss in self.losses],
            "selected_metrics": [metric.to_dict(camel_type=camel_type) for metric in self.selected_metrics],
            "selected_losses": [loss.to_dict(camel_type=camel_type) for loss in self.selected_losses],
            "is_target_set": self.is_target_set,
        }
        if camel_type:
            data_dict = {camelize(key): val for key, val in data_dict.items()}
        return data_dict

    @classmethod
    def get(cls, project_id: str) -> "CustomMetricsLossesMetadata":
        """Get the metadata using project id

        Params
        ------
        project_id : str
            The ID of the project that record belongs.
        """
        url = f"projects/{project_id}/customMetricsLosses/"
        response = cls._client.get(url)
        return cls.from_server_data(response.json())

    def update_selected_metrics_losses(
        self,
        selected_metrics_names: List[str],
        primary_metric_name: Optional[str] = None,
        selected_losses_names: Optional[List[str]] = None,
    ) -> None:
        """Update selections for custom metrics and losses

        Params
        ------
        selected_metrics_names : list(str)
            The names of the metrics to be used to calculate scores.
        primary_metric_name : str (default=None)
            The name of the metric to be used for hyperparameters search.
            If it is not specified then all selected metrics will have their
            primary metric field set to False.
        selected_losses_names : list(str) (default=None)
            The names of the losses to be used to optimize some models.

        Raises
        ------
        ValueError
            Raised if an names are not found in the metrics and losses.
        """

        url = f"projects/{self.project_id}/customMetricsLosses/"
        # validate the names
        all_metrics_names = [metric.name for metric in self.metrics]
        all_losses_names = [loss.name for loss in self.losses]
        if primary_metric_name is not None:
            if primary_metric_name not in all_metrics_names:
                msg = f"The primary metric {primary_metric_name} was not found"
                raise ValueError(msg)
            if primary_metric_name not in selected_metrics_names:
                msg = f"The primary metric {primary_metric_name} was not found in selected list"
                raise ValueError(msg)
        for metric in selected_metrics_names:
            if metric not in all_metrics_names:
                msg = f"The metric {metric} was not found"
                raise ValueError(msg)
        if selected_losses_names is not None:
            for loss in selected_losses_names:
                if loss not in all_losses_names:
                    msg = f"The loss {loss} was not found"
                    raise ValueError(msg)
        selected_metrics = []
        for metric_cls in self.metrics:
            if metric_cls.name in selected_metrics_names:
                selected_metric = metric_cls.to_dict(camel_type=True)
                if primary_metric_name and metric_cls.name == primary_metric_name:
                    selected_metric["primaryMetric"] = True
                else:
                    selected_metric["primaryMetric"] = False
                selected_metrics.append(selected_metric)
        payload = {"selectedMetrics": selected_metrics}
        selected_losses: List[Dict[str, Any]] = []
        if selected_losses_names is not None:
            for loss_cls in self.losses:
                if loss_cls.name in selected_losses_names:
                    selected_losses.append(loss_cls.to_dict(camel_type=True))
            payload["selectedLosses"] = selected_losses
        response = self._client.patch(url, data=payload)
        safe_data = self.from_server_data(response.json()).to_dict()
        self._set_values(**safe_data)

    @classmethod
    def create_from_catalog_id(
        cls,
        project_id: str,
        custom_metrics_losses_catalog_id: str,
        base_image_id: Optional[str] = None,
        can_overwrite: Optional[bool] = None,
    ) -> dict[str, Any]:
        """create new record using uploaded files with catalog id

        Params
        ------
        project_id : str
            The ID of the project that record belongs.
        custom_metrics_losses_catalog_id : str
            The ID of the files that have been uploaded to catalog.
        base_image_id : str (default None)
            The ID of the base image that user will use with LRS.
        can_overwrite : str (default False)
            If specified allows to create the new record even the old exists.
            The old record would be deleted.

        Return
        ------
        returns dictionary with record id

        """
        url = f"projects/{project_id}/customMetricsLosses/"
        payload: Dict[str, Any] = {}
        payload["customMetricsLossesCatalogId"] = custom_metrics_losses_catalog_id
        if base_image_id is not None:
            payload["baseImageId"] = base_image_id
        if can_overwrite is not None:
            payload["canOverwrite"] = can_overwrite
        response = cls._client.post(url, data=payload)
        # return here just id
        return {"id": response.json()["id"]}
