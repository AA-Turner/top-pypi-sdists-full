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

from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

import dateutil
import trafaret as t

from datarobot.enums import DEFAULT_MAX_WAIT, ExportStatus
from datarobot.models.api_object import APIObject
from datarobot.models.dataset import Dataset
from datarobot.utils import datetime_to_string, from_api
from datarobot.utils.pagination import unpaginate
from datarobot.utils.waiters import wait_for_async_resolution

if TYPE_CHECKING:
    from mypy_extensions import TypedDict

    class Period(TypedDict, total=False):
        start: datetime
        end: datetime

    class ExportError(TypedDict, total=False):
        message: str

    class ExportDataset(TypedDict, total=False):
        id: str
        name: str

    class ExportBatches(TypedDict, total=False):
        batch_id: str
        batch_name: str


class PredictionDataExport(APIObject):
    """A prediction data export.

    .. versionadded:: v3.4

    Attributes
    ----------
    id: str
        The ID of the prediction data export.
    model_id: str
        The ID of the model (or null if not specified).
    created_at: datetime
        Prediction data export creation timestamp.
    period: Period
        A prediction data time range definition.
    status: ExportStatus
       A prediction data export processing state.
    error: ExportError
       Error description, appears when prediction data export job failed (status is FAILED).
    batches: ExportBatches
       Metadata associated with exported batch.
    deployment_id: str
        The ID of the deployment.
    """

    _path = "deployments/{}/predictionDataExports/"
    _converter = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("model_id"): t.String(),
            t.Key("created_at"): t.String() >> dateutil.parser.parse,
            t.Key("period"): t.Dict(
                {
                    t.Key("start"): t.String >> dateutil.parser.parse,
                    t.Key("end"): t.String >> dateutil.parser.parse,
                }
            ),
            t.Key("status"): t.String(),
            t.Key("error", optional=True, default=None): t.Or(
                t.Dict().allow_extra("*"),
                t.Null,
            ),
            t.Key("data", optional=True): t.Or(
                t.List(t.Dict().allow_extra("*")),
                t.Null,
            ),
            t.Key("batches", optional=True, default=None): t.Or(
                t.Dict().allow_extra("*"),
                t.Null,
            ),
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        period: Period,
        created_at: datetime,
        model_id: str,
        status: ExportStatus,
        data: Optional[List[ExportDataset]] = None,
        error: Optional[ExportError] = None,
        batches: Optional[ExportBatches] = None,
        deployment_id: Optional[str] = None,
    ):
        self.id = id
        self.period = period
        self.created_at = created_at
        self.model_id = model_id
        self.status = status
        self.data = data
        self.error = error
        self.batches = batches
        self.deployment_id = deployment_id

    def __repr__(self) -> str:
        return "PredictionDataExport({})".format(self.id)

    @classmethod
    def list(
        cls,
        deployment_id: str,
        status: Optional[ExportStatus] = None,
        model_id: Optional[str] = None,
        batch: Optional[bool] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 100,
    ) -> List[PredictionDataExport]:
        """Retrieve a list of prediction data exports.

        Parameters
        ----------
        deployment_id: str
            The ID of the deployment.
        model_id: Optional[str]
            The ID of the model used for prediction data export.
        status: Optional[ExportStatus]
            A prediction data export processing state.
        batch: Optional[bool]
            If true, only return batch exports.
            If false, only return real-time exports.
            If not provided, return both real-time and batch exports.
        limit: Optional[int]
            The maximum number of objects to return. The default is 100 (0 means no limit).
        offset: Optional[int]
            The starting offset of the results. The default is 0.

        Returns
        -------
        prediction_data_exports: list
            A list of PredictionDataExport objects.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import PredictionDataExport

            prediction_data_exports = PredictionDataExport.list(deployment_id='5c939e08962d741e34f609f0')
        """
        path = cls._path.format(deployment_id)

        params: Dict[str, Any] = {}
        if model_id:
            params["modelId"] = model_id
        if status:
            params["status"] = status
        if batch:
            params["batch"] = batch

        if limit == 0:  # unlimited results
            r_data = unpaginate(path, params, cls._client)
        else:
            params["offset"] = offset
            params["limit"] = limit
            response = cls._client.get(path, params=params).json()
            r_data = response["data"]

        prediction_data_exports = [
            cls.from_server_data(from_api(d, keep_null_keys=True)) for d in r_data
        ]
        for data_export in prediction_data_exports:
            data_export.deployment_id = deployment_id
        return prediction_data_exports

    @classmethod
    def get(
        cls,
        deployment_id: str,
        export_id: str,
    ) -> PredictionDataExport:
        """Retrieve a single prediction data export.

        Parameters
        ----------
        deployment_id: str
            The ID of the deployment.
        export_id: str
            The ID of the prediction data export.

        Returns
        -------
        prediction_data_export: PredictionDataExport
            A prediction data export.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import PredictionDataExport

            prediction_data_export = PredictionDataExport.get(
                deployment_id='5c939e08962d741e34f609f0', export_id='65fbe59aaa3f847bd5acc75b'
                )
        """
        path = "{}{}/".format(cls._path.format(deployment_id), export_id)
        data = cls._client.get(path).json()
        case_converted = from_api(data, keep_null_keys=True)
        prediction_data_export = cls.from_data(case_converted)
        prediction_data_export.deployment_id = deployment_id
        return prediction_data_export

    @classmethod
    def create(
        cls,
        deployment_id: str,
        start: Union[datetime, str],
        end: Union[datetime, str],
        model_id: Optional[str] = None,
        batch_ids: Optional[List[str]] = None,
        max_wait: int = DEFAULT_MAX_WAIT,
    ) -> PredictionDataExport:
        """Create a deployment prediction data export.
        Waits until ready and fetches PredictionDataExport after the export finishes. This method is blocking.

        Parameters
        ----------
        deployment_id: str
            The ID of the deployment.
        start: Union[datetime, str]
            Inclusive start of the time range.
        end: Union[datetime, str]
            Exclusive end of the time range.
        model_id: Optional[str]
            The ID of the model.
        batch_ids: Optional[List[str]]
            IDs of batches to export. Null for real-time data exports.
        max_wait: int,
            Seconds to wait for successful resolution.

        Returns
        -------
        prediction_data_export: PredictionDataExport
            A prediction data export.

        Examples
        --------
        .. code-block:: python

            from datetime import datetime, timedelta
            from datarobot.models.deployment import PredictionDataExport

            now=datetime.now()
            prediction_data_export = PredictionDataExport.create(
                deployment_id='5c939e08962d741e34f609f0', start=now - timedelta(days=7), end=now
                )
        """
        payload = {
            "start": start if isinstance(start, str) else datetime_to_string(start),
            "end": end if isinstance(end, str) else datetime_to_string(end),
            "batchIds": batch_ids,
        }
        if model_id:
            payload["modelId"] = model_id
        if batch_ids:
            payload["batchIds"] = batch_ids
        path = cls._path.format(deployment_id)
        response = cls._client.post(path, json=payload)
        retrieve_url = wait_for_async_resolution(
            cls._client, response.headers["Location"], max_wait
        )
        response = cls._client.get(retrieve_url)
        export_id = response.json()["id"]
        return cls.get(deployment_id, export_id)

    def fetch_data(self) -> List[Dataset]:
        """Return data from prediction export as datarobot Dataset.

        Returns
        -------
        prediction_datasets: List[Dataset]
            List of datasets for a given export, most often it is just one.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import PredictionDataExport

            prediction_data_export = PredictionDataExport.get(
                deployment_id='5c939e08962d741e34f609f0', export_id='65fbe59aaa3f847bd5acc75b'
                )
            prediction_datasets = prediction_data_export.fetch_data()
        """
        if not self.data:
            raise ValueError("No datasets found for prediction export.")
        datasets = [Dataset.get(item["id"]) for item in self.data]
        return datasets


class ActualsDataExport(APIObject):
    """An actuals data export.

    .. versionadded:: v3.4

    Attributes
    ----------
    id: str
        The ID of the actuals data export.
    model_id: str
        The ID of the model (or null if not specified).
    created_at: datetime
        Actuals data export creation timestamp.
    period: Period
        A actuals data time range definition.
    status: ExportStatus
       A data export processing state.
    error: ExportError
       Error description, appears when actuals data export job failed (status is FAILED).
    only_matched_predictions: bool
        If true, exports actuals with matching predictions only.
    deployment_id: str
        The ID of the deployment.
    """

    _path = "deployments/{}/actualsDataExports/"
    _converter = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("model_id"): t.String(),
            t.Key("created_at"): t.String() >> dateutil.parser.parse,
            t.Key("period"): t.Dict(
                {
                    t.Key("start"): t.String >> dateutil.parser.parse,
                    t.Key("end"): t.String >> dateutil.parser.parse,
                }
            ),
            t.Key("status"): t.String(),
            t.Key("error", optional=True, default=None): t.Or(
                t.Dict().allow_extra("*"),
                t.Null,
            ),
            t.Key("data", optional=True): t.Or(
                t.List(t.Dict().allow_extra("*")),
                t.Null,
            ),
            t.Key("only_matched_predictions", optional=True, default=True): t.Bool(),
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        period: Period,
        created_at: datetime,
        model_id: str,
        status: ExportStatus,
        data: Optional[List[ExportDataset]] = None,
        error: Optional[ExportError] = None,
        only_matched_predictions: Optional[bool] = None,
        deployment_id: Optional[str] = None,
    ):
        self.id = id
        self.period = period
        self.created_at = created_at
        self.model_id = model_id
        self.status = status
        self.data = data
        self.error = error
        self.only_matched_predictions = only_matched_predictions
        self.deployment_id = deployment_id

    def __repr__(self) -> str:
        return "ActualsDataExport({})".format(self.id)

    @classmethod
    def list(
        cls,
        deployment_id: str,
        status: Optional[ExportStatus] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 100,
    ) -> List[ActualsDataExport]:
        """Retrieve a list of actuals data exports.

        Parameters
        ----------
        deployment_id: str
            The ID of the deployment.
        status: Optional[ExportStatus]
            Actuals data export processing state.
        limit: Optional[int]
            The maximum number of objects to return. The default is 100 (0 means no limit).
        offset: Optional[int]
            The starting offset of the results. The default is 0.

        Returns
        -------
        actuals_data_exports: list
            A list of ActualsDataExport objects.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import ActualsDataExport

            actuals_data_exports = ActualsDataExport.list(deployment_id='5c939e08962d741e34f609f0')
        """
        path = cls._path.format(deployment_id)

        params: Dict[str, Any] = {}
        if status:
            params["status"] = status

        if limit == 0:  # unlimited results
            r_data = unpaginate(path, params, cls._client)
        else:
            params["offset"] = offset
            params["limit"] = limit
            response = cls._client.get(path, params=params).json()
            r_data = response["data"]

        actuals_data_exports = [
            cls.from_server_data(from_api(d, keep_null_keys=True)) for d in r_data
        ]
        for data_export in actuals_data_exports:
            data_export.deployment_id = deployment_id
        return actuals_data_exports

    @classmethod
    def get(
        cls,
        deployment_id: str,
        export_id: str,
    ) -> ActualsDataExport:
        """Retrieve a single actuals data export.

        Parameters
        ----------
        deployment_id: str
            The ID of the deployment.
        export_id: str
            The ID of the actuals data export.

        Returns
        -------
        actuals_data_export: ActualsDataExport
            An actuals data export.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import ActualsDataExport

            actuals_data_export = ActualsDataExport.get(
                deployment_id='5c939e08962d741e34f609f0', export_id='65fb0a6c9bb187781cfdea36'
                )
        """
        path = "{}{}/".format(cls._path.format(deployment_id), export_id)
        data = cls._client.get(path).json()
        case_converted = from_api(data, keep_null_keys=True)
        actuals_data_export = cls.from_data(case_converted)
        actuals_data_export.deployment_id = deployment_id
        return actuals_data_export

    @classmethod
    def create(
        cls,
        deployment_id: str,
        start: Union[datetime, str],
        end: Union[datetime, str],
        model_id: Optional[str] = None,
        only_matched_predictions: Optional[bool] = None,
        max_wait: int = DEFAULT_MAX_WAIT,
    ) -> ActualsDataExport:
        """Create a deployment actuals data export.
        Waits until ready and fetches ActualsDataExport after the export finishes. This method is blocking.

        Parameters
        ----------
        deployment_id: str
            The ID of the deployment.
        start: Union[datetime, str]
            Inclusive start of the time range.
        end: Union[datetime, str]
            Exclusive end of the time range.
        model_id: Optional[str]
            The ID of the model.
        only_matched_predictions: Optional[bool]
            If true, exports actuals with matching predictions only.
        max_wait: int
            Seconds to wait for successful resolution.

        Returns
        -------
        actuals_data_export: ActualsDataExport
            An actuals data export.

        Examples
        --------
        .. code-block:: python

            from datetime import datetime, timedelta
            from datarobot.models.deployment import ActualsDataExport

            now=datetime.now()
            actuals_data_export = ActualsDataExport.create(
                deployment_id='5c939e08962d741e34f609f0', start=now - timedelta(days=7), end=now
                )
        """
        payload: Dict[str, Any] = {
            "start": start if isinstance(start, str) else datetime_to_string(start),
            "end": end if isinstance(end, str) else datetime_to_string(end),
        }
        if model_id:
            payload["modelId"] = model_id
        if only_matched_predictions:
            payload["onlyMatchedPredictions"] = only_matched_predictions
        path = cls._path.format(deployment_id)
        response = cls._client.post(path, json=payload)
        retrieve_url = wait_for_async_resolution(
            cls._client, response.headers["Location"], max_wait
        )
        response = cls._client.get(retrieve_url)
        export_id = response.json()["id"]
        return cls.get(deployment_id, export_id)

    def fetch_data(self) -> List[Dataset]:
        """Return data from actuals export as datarobot Dataset.

        Returns
        -------
        actuals_datasets: List[Dataset]
            List of datasets for a given export, most often it is just one.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import ActualsDataExport

            actuals_data_export = ActualsDataExport.get(
                deployment_id='5c939e08962d741e34f609f0', export_id='65fb0a6c9bb187781cfdea36'
                )
            actuals_datasets = actuals_data_export.fetch_data()
        """
        if not self.data:
            raise ValueError("No datasets found for actuals export.")
        datasets = [Dataset.get(item["id"]) for item in self.data]
        return datasets


class TrainingDataExport(APIObject):
    """A training data export.

    .. versionadded:: v3.4

    Attributes
    ----------
    id: str
        The ID of the training data export.
    model_id: str
        The ID of the model (or null if not specified).
    model_package_id: str
        The ID of the model package.
    created_at: datetime
        Training data export creation timestamp.
    deployment_id: str
        The ID of the deployment.
    """

    _path = "deployments/{}/trainingDataExports/"
    _converter = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("model_id"): t.String(),
            t.Key("model_package_id"): t.String(),
            t.Key("created_at"): t.String() >> dateutil.parser.parse,
            t.Key("data", optional=True): t.Or(
                t.Dict().allow_extra("*"),
                t.Null,
            ),
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        created_at: datetime,
        model_id: str,
        model_package_id: str,
        data: Optional[ExportDataset] = None,
        deployment_id: Optional[str] = None,
    ):
        self.id = id
        self.data = data
        self.created_at = created_at
        self.model_id = model_id
        self.model_package_id = model_package_id
        self.deployment_id = deployment_id

    def __repr__(self) -> str:
        return "TrainingDataExport({})".format(self.id)

    @classmethod
    def list(
        cls,
        deployment_id: str,
    ) -> List[TrainingDataExport]:
        """Retrieve a list of successful training data exports.

        Parameters
        ----------
        deployment_id: str
            The ID of the deployment.

        Returns
        -------
        training_data_exports: list
            A list of TrainingDataExport objects.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import TrainingDataExport

            training_data_exports = TrainingDataExport.list(deployment_id='5c939e08962d741e34f609f0')
        """
        path = cls._path.format(deployment_id)
        data = cls._client.get(path).json()["data"]
        training_data_exports = [
            cls.from_server_data(from_api(d, keep_null_keys=True)) for d in data
        ]
        for data_export in training_data_exports:
            data_export.deployment_id = deployment_id
        return training_data_exports

    @classmethod
    def get(
        cls,
        deployment_id: str,
        export_id: str,
    ) -> TrainingDataExport:
        """Retrieve a single training data export.

        Parameters
        ----------
        deployment_id: str
            The ID of the deployment.
        export_id: str
            The ID of the training data export.

        Returns
        -------
        training_data_export: TrainingDataExport
            A training data export.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import TrainingDataExport
            training_data_export = TrainingDataExport.get(
                deployment_id='5c939e08962d741e34f609f0', export_id='65fbf2356124f1daa3acc522'
                )
        """
        path = "{}{}/".format(cls._path.format(deployment_id), export_id)
        data = cls._client.get(path).json()
        case_converted = from_api(data, keep_null_keys=True)
        training_data_export = cls.from_data(case_converted)
        training_data_export.deployment_id = deployment_id
        return training_data_export

    @classmethod
    def create(
        cls,
        deployment_id: str,
        model_id: Optional[str] = None,
        max_wait: int = DEFAULT_MAX_WAIT,
    ) -> str:
        """Create a single training data export.
        Waits until ready and fetches TrainingDataExport after the export finishes. This method is blocking.

        Parameters
        ----------
        deployment_id: str
            The ID of the deployment.
        model_id: Optional[str]
            The ID of the model.
        max_wait: int
            Seconds to wait for successful resolution.

        Returns
        -------
        dataset_id: str
            A created dataset with training data.

         Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import TrainingDataExport
            dataset_id = TrainingDataExport.create(deployment_id='5c939e08962d741e34f609f0')
        """
        payload = {}
        if model_id:
            payload["modelId"] = model_id
        path = cls._path.format(deployment_id)
        response = cls._client.post(path, json=payload)
        retrieve_url = wait_for_async_resolution(
            cls._client, response.headers["Location"], max_wait
        )
        response = cls._client.get(retrieve_url)
        dataset_id = response.json()["datasetId"]
        return dataset_id  # type: ignore[no-any-return]

    def fetch_data(self) -> Dataset:
        """Return data from training data export as datarobot Dataset.

        Returns
        -------
        training_dataset: Dataset
            A datasets for a given export.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import TrainingDataExport

            training_data_export = TrainingDataExport.get(
                deployment_id='5c939e08962d741e34f609f0', export_id='65fbf2356124f1daa3acc522'
                )
            training_data_export = training_data_export.fetch_data()
        """
        if not self.data:
            raise ValueError("No datasets found for training data export.")
        dataset = Dataset.get(self.data["id"])
        return dataset


class DataQualityExport(APIObject):
    """A data quality export record.

    .. versionadded:: v3.6

    Attributes
    ----------
    association_id: str
        The association ID of the data quality export.
    timestamp: datetime
        The data quality export creation timestamp.
    deployment_id: str
        The ID of the deployment.
    prompt: Optional[str]
        The LLM prompt of the data quality export.
    predicted_value: str
        The predicted value of the data quality export.
    actual_value: Optional[str]
        The actual value (if available) of the data quality export.
    context: List[Dict[str, str]]
        Context data (context and link data) for the contexts associated with the data quality export.
    metrics: List[Dict[str, Any]]
         Custom-metrics data for the data quality export.
    """

    _path = "deployments/{}/dataQualityView/"
    _converter = t.Dict(
        {
            t.Key("association_id"): t.String(),
            t.Key("timestamp"): t.String() >> dateutil.parser.parse,
            t.Key("prompt", optional=True, default=None): t.Or(t.Null, t.String()),
            t.Key("predicted_value", optional=True, default=None): t.Or(t.Null, t.String()),
            t.Key("actual_value", optional=True, default=None): t.Or(t.Null, t.String()),
            t.Key("context"): t.List(
                t.Dict().allow_extra("*"),
            ),
            t.Key("metrics"): t.List(
                t.Dict().allow_extra("*"),
            ),
        }
    ).allow_extra("*")

    def __init__(
        self,
        association_id: str,
        timestamp: datetime,
        prompt: Optional[str],
        predicted_value: str,
        actual_value: Optional[str] = None,
        context: Optional[List[Dict[str, str]]] = None,
        metrics: Optional[List[Dict[str, Any]]] = None,
        deployment_id: Optional[str] = None,
    ):
        self.deployment_id = deployment_id
        self.association_id = association_id
        self.timestamp = timestamp
        self.prompt = prompt
        self.predicted_value = predicted_value
        self.actual_value = actual_value
        self.context = context
        self.metrics = metrics

    def __repr__(self) -> str:
        return "DataQualityExport({})".format(self.association_id)

    @classmethod
    def list(
        cls,
        deployment_id: str,
        start: Union[str, datetime],
        end: Union[str, datetime],
        model_id: Optional[str] = None,
        prediction_pattern: Optional[str] = None,
        prompt_pattern: Optional[str] = None,
        actual_pattern: Optional[str] = None,
        order_by: Optional[str] = None,
        order_metric: Optional[str] = None,
        filter_metric: Optional[str] = None,
        filter_value: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 100,
    ) -> List[DataQualityExport]:
        """Retrieve a list of data-quality export records for a given deployment.

        .. versionadded:: v3.6

        Parameters
        ----------
        deployment_id: str
            The ID of the deployment.
        start: Union[str, datetime]
            The earliest time of the objects to return.
        end: Union[str, datetime]
            The latest time of the objects to return.
        model_id: Optional[str]
            The ID of the model.
        prediction_pattern: Optional[str]
            The keywords to search in a predicted value for a text generation target.
        prompt_pattern: Optional[str]
            The keywords to search in a prompt value for a text generation target.
        actual_pattern: Optional[str]
            The keywords to search in an actual value for a text generation target.
        order_by: Optional[str]
            The field to sort by (e.g. associationId, timestamp, or customMetrics). Use a leading '-'
            to indicate descending order. When ordering by a custom-metric, must also specify 'order_metric'.
            The default is None, which equates to '-timestamp'.
        order_metric: Optional[str]
            When 'order_by' is a custom-metric, this specifies the custom-metric name or ID to use for ordering.
            The default is None.
        filter_metric: Optional[str]
            Specifies the metric name or ID to use for matching. Must also use 'filter_value' to specify
            the value that must be matched. The default is None.
        filter_value: Optional[str]
            Specifies the value associated with 'filter_metric' that must be matched. The default
            is None.
        offset: Optional[int]
            The starting offset of the results. The default is 0.
        limit: Optional[int]
            The maximum number of objects to return. The default is 100 (which is maximum).

        Returns
        -------
        data_quality_exports: list
            A list of DataQualityExport objects.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import DataQualityExport

            data_quality_exports = DataQualityExport.list(
                deployment_id='5c939e08962d741e34f609f0', start_time='2024-07-01', end_time='2024-08-01
            )
        """
        path = cls._path.format(deployment_id)
        params: Dict[str, Any] = {
            "start": start if isinstance(start, str) else datetime_to_string(start),
            "end": end if isinstance(end, str) else datetime_to_string(end),
        }
        if model_id:
            params["modelId"] = model_id
        if prediction_pattern:
            params["predictionPattern"] = prediction_pattern
        if prompt_pattern:
            params["promptPattern"] = prompt_pattern
        if actual_pattern:
            params["actualPattern"] = actual_pattern
        if order_by:
            params["orderBy"] = order_by
        if order_metric:
            params["orderMetric"] = order_metric
        if filter_metric:
            params["filterMetric"] = filter_metric
        if filter_value is not None:
            params["filterValue"] = filter_value

        if limit == 0:  # unlimited results
            r_data = unpaginate(path, params, cls._client)
        else:
            params["offset"] = offset
            params["limit"] = limit
            response = cls._client.get(path, params=params).json()
            r_data = response["data"]

        data_quality_exports = [
            cls.from_server_data(from_api(d, keep_null_keys=True)) for d in r_data
        ]
        for data_export in data_quality_exports:
            data_export.deployment_id = deployment_id
        return data_quality_exports
