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

from typing import Any, Dict, List, Optional, Union, cast

import trafaret as t

from datarobot._compat import String
from datarobot.models.confusion_chart import ConfusionChartTrafaret
from datarobot.utils.pagination import unpaginate

from ..api_object import APIObject
from .external_scores import DEFAULT_BATCH_SIZE


class ExternalConfusionChart(APIObject):
    """ Confusion chart for the model and prediction dataset with target.

    .. versionadded:: v2.21


    ``ClassMetrics`` is a dict containing the following:

        * ``class_name`` (string) name of the class
        * ``actual_count`` (int) number of times this class is seen in the validation data
        * ``predicted_count`` (int) number of times this class has been predicted for the \
          validation data
        * ``f1`` (float) F1 score
        * ``recall`` (float) recall score
        * ``precision`` (float) precision score
        * ``was_actual_percentages`` (list of dict) one vs all actual percentages in format \
          specified below.
            * ``other_class_name`` (string) the name of the other class
            * ``percentage`` (float) the percentage of the times this class was predicted when is \
              was actually class (from 0 to 1)
        * ``was_predicted_percentages`` (list of dict) one vs all predicted percentages in format \
          specified below.
            * ``other_class_name`` (string) the name of the other class
            * ``percentage`` (float) the percentage of the times this class was actual predicted \
              (from 0 to 1)
        * ``confusion_matrix_one_vs_all`` (list of list) 2d list representing 2x2 one vs all matrix.
            * This represents the True/False Negative/Positive rates as integer for each class. \
              The data structure looks like:
            * ``[ [ True Negative, False Positive ], [ False Negative, True Positive ] ]``

    Attributes
    ----------
    dataset_id: str
        ID of the external dataset with target
    model_id: str
        ID of the model this confusion chart represents
    raw_data : dict
        All of the raw data for the Confusion Chart
    confusion_matrix : list of list
        The NxN confusion matrix
    classes : list
        The names of each of the classes
    class_metrics : list of dicts
        List of dicts with schema described as ``ClassMetrics`` above.

    """

    _path = "projects/{project_id}/models/{model_id}/datasetConfusionCharts/"
    _single_chart_path = "projects/{project_id}/models/{model_id}/datasetConfusionCharts/{dataset_id}/"
    _metadata_path = "projects/{project_id}/models/{model_id}/datasetConfusionCharts/{dataset_id}/metadata/"
    _converter = t.Dict({t.Key("dataset_id"): String(), t.Key("data"): ConfusionChartTrafaret}).ignore_extra("*")

    def __init__(self, dataset_id: str, data: Dict[str, Any]) -> None:
        self.dataset_id = dataset_id
        self.raw_data = data
        self.class_metrics = data["class_metrics"]
        self.confusion_matrix = data["confusion_matrix"]
        self.classes = data["classes"]

    def __repr__(self) -> str:
        return "ExternalConfusionChart(dataset_id={}, classes={})".format(self.dataset_id, self.classes)

    @classmethod
    def list(
        cls, project_id: str, model_id: str, dataset_id: Optional[str] = None, offset: int = 0, limit: int = 100
    ) -> List[ExternalConfusionChart]:
        """Retrieve list of the confusion charts for the model.

        Parameters
        ----------
        project_id: str
            ID of the project
        model_id: str
            ID of the model to retrieve a chart from
        dataset_id: Optional[str]
            If specified, only confusion chart for this dataset will be retrieved
        offset: Optional[int]
            This many results will be skipped, default: 0
        limit: Optional[int]
            At most this many results are returned, default: 100, max 1000.
            To return all results, specify 0

        Returns
        -------
            A list of :py:class:`ExternalConfusionChart <datarobot.ExternalConfusionChart>` objects
        """
        url = cls._path.format(project_id=project_id, model_id=model_id)
        params: Dict[str, Union[int, str]] = {"limit": limit, "offset": offset}
        if dataset_id:
            params["datasetId"] = dataset_id
        if limit == 0:  # unlimited results
            params["limit"] = DEFAULT_BATCH_SIZE
            return [cls.from_server_data(entry) for entry in unpaginate(url, params, cls._client)]
        r_data = cls._client.get(url, params=params).json()
        return [cls.from_server_data(item) for item in r_data["data"]]

    @classmethod
    def get(cls, project_id: str, model_id: str, dataset_id: str) -> ExternalConfusionChart:
        """Retrieve confusion chart for the model and external dataset.

        Parameters
        ----------
        project_id: str
            Project ID
        model_id: str
            Model ID
        dataset_id: str
            External dataset ID with target

        Returns
        -------
            :py:class:`ExternalConfusionChart <datarobot.ExternalConfusionChart>` object

        """
        if dataset_id is None:
            raise ValueError("dataset_id must be specified")
        url = cls._single_chart_path.format(project_id=project_id, model_id=model_id, dataset_id=dataset_id)

        confusion_chart = cls._client.get(url).json()
        metadata = cls._get_metadata(project_id=project_id, model_id=model_id, dataset_id=dataset_id)
        confusion_chart["data"]["classes"] = metadata["classNames"]
        return cls.from_server_data(confusion_chart)

    @classmethod
    def _get_metadata(cls, project_id: str, model_id: str, dataset_id: str) -> Dict[str, Any]:
        """Retrieve confusion chart metadata.

        Parameters
        ----------
        project_id: str
            Project ID
        model_id: str
            Model ID
        dataset_id: str
            External dataset ID with target

        Returns
        -------
            metadata : dict
                Metadata of the confusion chart

        """
        url = cls._metadata_path.format(project_id=project_id, model_id=model_id, dataset_id=dataset_id)
        return cast(Dict[str, Any], cls._client.get(url).json())
