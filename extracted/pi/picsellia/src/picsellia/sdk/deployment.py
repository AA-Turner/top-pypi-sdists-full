import base64
import json
import logging
import mimetypes
import os
from datetime import date
from pathlib import Path
from typing import Any
from uuid import UUID

import orjson
import requests
from beartype import beartype
from deprecation import deprecated

from picsellia.colors import Colors
from picsellia.decorators import exception_handler, retry
from picsellia.exceptions import (
    BadConfigurationContinuousTrainingError,
    BadRequestError,
    ContentTypeUnknown,
    MonitorError,
    MonitoringConnectionError,
    NoDataError,
    NoShadowModel,
    PicselliaError,
    PredictionError,
    ResourceNotFoundError,
)
from picsellia.sdk.connection import Connection, JwtServiceConnection
from picsellia.sdk.dao import Dao
from picsellia.sdk.data import Data
from picsellia.sdk.datalake import Datalake
from picsellia.sdk.dataset import DatasetVersion
from picsellia.sdk.datasource import DataSource
from picsellia.sdk.label import Label
from picsellia.sdk.model_version import ModelVersion
from picsellia.sdk.predicted_asset import MultiPredictedAsset, PredictedAsset
from picsellia.sdk.project import Project
from picsellia.sdk.resource import Resource
from picsellia.sdk.review_campaign import ReviewCampaign
from picsellia.sdk.tag import Tag
from picsellia.sdk.taggable import Taggable
from picsellia.sdk.worker import Worker
from picsellia.services.lister.predicted_asset_lister import (
    PredictedAssetFilter,
    PredictedAssetLister,
)
from picsellia.types.enums import (
    ContinuousDeploymentPolicy,
    ContinuousTrainingTrigger,
    ContinuousTrainingType,
    InferenceType,
    ObjectDataType,
    ServiceMetrics,
    SupportedContentType,
    TagTarget,
    WorkerType,
)
from picsellia.types.schemas import DeploymentSchema, TargetDatalakeConnectorSchema
from picsellia.types.schemas_prediction import PredictionFormat

logger = logging.getLogger("picsellia")


class Deployment(Dao, Taggable, Resource):
    def __init__(self, connexion: Connection, data: dict):
        Dao.__init__(self, connexion, data)
        Taggable.__init__(self, TagTarget.DEPLOYMENT)
        Resource.__init__(self, "deployment")

        # lazy loading of target datalake connector
        self._target_datalake_connector = None

        deployment = self.refresh(data)
        if deployment.oracle_host is not None:
            try:
                self._oracle_connection = JwtServiceConnection(
                    deployment.oracle_host,
                    {
                        "api_token": self.connection.api_token,
                        "deployment_id": str(self.id),
                    },
                    login_path="/api/auth/login",
                )
                if self._oracle_connection.jwt is None:  # pragma: no cover
                    raise PicselliaError("Cannot authenticate to oracle")

                logging.info(
                    f"Connected with monitoring service at {deployment.oracle_host}"
                )
            except Exception as e:
                logger.error(
                    f"Could not bind {self} with our monitoring service at {deployment.oracle_host} because : {e}"
                )
                self._oracle_connection.session.close()
                self._oracle_connection = None
        else:  # pragma: no cover
            self._oracle_connection = None

        if deployment.serving_host is not None:
            try:
                self._serving_connection = JwtServiceConnection(
                    deployment.serving_host,
                    {
                        "api_token": self.connection.api_token,
                        "deployment_id": str(self.id),
                    },
                    login_path="/api/login",
                )
                if self._serving_connection.jwt is None:  # pragma: no cover
                    raise PicselliaError("Cannot authenticate to serving")
                logging.info(
                    f"Connected with serving service at {deployment.serving_host}"
                )
            except Exception as e:
                logger.error(
                    f"Could not bind {self} with our serving service at {deployment.serving_host} because : {e}"
                )
                self._serving_connection.session.close()
                self._serving_connection = None
        else:  # pragma: no cover
            self._serving_connection = None

    @property
    def name(self) -> str:
        """Name of this (Deployment)"""
        return self._name

    @property
    def type(self) -> InferenceType:
        """Type of this (Deployment)"""
        return self._type

    @property
    @deprecated(
        deprecated_in="6.29.0",
        details="You should use connection property instead of this one.",
    )
    def oracle_connexion(self) -> JwtServiceConnection:
        """deprecated"""
        return self.oracle_connection

    @property
    def oracle_connection(self) -> JwtServiceConnection:
        assert self._oracle_connection is not None, (
            "You can't use this function with this deployment. Please contact the support."
        )
        return self._oracle_connection

    @property
    @deprecated(
        deprecated_in="6.29.0",
        details="You should use connection property instead of this one.",
    )
    def serving_connexion(self) -> JwtServiceConnection:
        """deprecated"""
        return self.serving_connection

    @property
    def serving_connection(self) -> JwtServiceConnection:
        assert self._serving_connection is not None, (
            "You can't use this function with this deployment. Please contact the support."
        )
        return self._serving_connection

    def __str__(self):
        return f"{Colors.CYAN}Deployment '{self.name}' {Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> DeploymentSchema:
        schema = DeploymentSchema(**data)
        self._name = schema.name
        self._type = schema.type
        self._review_campaign_id = schema.review_campaign_id
        return schema

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/deployment/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def get_tags(self) -> list[Tag]:
        """Retrieve the tags of your deployment.

        Examples:
            ```python
            tags = deployment.get_tags()
            assert tags[0].name == "cool"
            ```

        Returns:
            A list of (Tag) objects
        """
        r = self.sync()
        return [Tag(self.connection, item) for item in r["tags"]]

    @exception_handler
    @beartype
    @retry((requests.ConnectionError, MonitoringConnectionError))
    def retrieve_information(self) -> dict:
        """Retrieve some information about this deployment from service.

        Examples:
            ```python
            my_deployment.retrieve_information()
            ```
        Returns:
            A dict with information about this deployment
        """
        response = self.oracle_connection.get(path=f"/api/deployment/{self.id}")
        if response.status_code > 500:
            raise MonitoringConnectionError()
        return response.json()

    @exception_handler
    @beartype
    def update(
        self,
        name: str | None = None,
        target_datalake: Datalake | None = None,
        min_threshold: float | None = None,
        sample_rate: float | None = None,
    ) -> None:
        """Update this deployment with a new name, another target datalake or a minimum threshold

        Examples:
            ```python
            a_tag.update(name="new name", min_threshold=0.4)
            ```
        Arguments:
            name (str, optional): New name of the deployment
            target_datalake (Datalake, optional): Datalake where data will be uploaded on new prediction
            min_threshold (float, optional): Minimum confidence threshold.
                    Serving will filter detection boxes or masks that have a detection score lower than this threshold
            sample_rate (float, optional): If less than 1, monitoring service will not send all images to platform,
                    but will still compute metrics.
        """
        payload = {}
        if name is not None:
            payload["name"] = name

        if min_threshold is not None:
            payload["min_threshold"] = min_threshold

        if target_datalake is not None:
            payload["target_datalake_id"] = target_datalake.id

        if sample_rate is not None:
            payload["sample_rate"] = sample_rate

        r = self.connection.patch(
            f"/api/deployment/{self.id}", data=orjson.dumps(payload)
        ).json()
        self.refresh(r)
        logger.info(f"{self} updated")

    @exception_handler
    @beartype
    def delete(self, force_delete: bool = False) -> None:
        self.connection.delete(
            f"/api/deployment/{self.id}", params={"force_delete": force_delete}
        )
        logger.info(f"{self} deleted.")

    @exception_handler
    @beartype
    def set_model(self, model_version: ModelVersion) -> None:
        """Set the model version to use for this deployment

        Examples:
            ```python
            model_version = client.get_model("my-model").get_version("latest")
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            deployment.set_model(model_version)
            ```
        Arguments:
            model_version (ModelVersion): a (ModelVersion) to use
        """
        payload = {"model_version_id": model_version.id}

        self.connection.post(
            f"/api/deployment/{self.id}/model", data=orjson.dumps(payload)
        ).json()
        logger.info(f"{self} model is now {model_version}")

    @exception_handler
    @beartype
    def get_model_version(self) -> ModelVersion:
        """Retrieve currently used model version

        Examples:
            ```python
            model_version = deployment.get_model_version()
            ```

        Returns:
            A (ModelVersion) object
        """
        r = self.sync()

        r = self.connection.get(f"/api/model/version/{r['model_version_id']}").json()
        return ModelVersion(self.connection, r)

    @exception_handler
    @beartype
    def set_shadow_model(self, shadow_model_version: ModelVersion) -> None:
        """Set the shadow model version to use for this deployment

        Examples:
            ```python
            shadow_model_version = client.get_model("my-model").get_version("latest")
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            deployment.set_shadow_model(shadow_model_version)
            ```

        Arguments:
            shadow_model_version (ModelVersion): a (ModelVersion) to use
        """
        payload = {"model_version_id": shadow_model_version.id}

        self.connection.post(
            f"/api/deployment/{self.id}/shadow", data=orjson.dumps(payload)
        ).json()
        logger.info(f"{self} shadow model is now {shadow_model_version}")

    @exception_handler
    @beartype
    def get_shadow_model(self) -> ModelVersion:
        """Retrieve currently used shadow model version

        Examples:
            ```python
            shadow_model = deployment.get_shadow_model()
            ```

        Returns:
            A (ModelVersion) object
        """
        r = self.sync()
        if "shadow_model_version_id" not in r or r["shadow_model_version_id"] is None:
            raise NoShadowModel("This deployment has no shadow model")

        r = self.connection.get(
            f"/api/model/version/{r['shadow_model_version_id']}"
        ).json()
        return ModelVersion(self.connection, r)

    @exception_handler
    @beartype
    def list_labels(self) -> list[Label]:
        """Get all labels of a Deployment.

        It will retrieve a list of label objects.

        Labels are created when (Deployment) is created, they cannot be updated or deleted.

        Examples:
            ```python
            labels = deployment.list_labels()
            assert labels[0].name == "person"
            ```

        Returns:
            List of (Label)
        """
        r = self.connection.get(f"/api/deployment/{self.id}/labels").json()
        return [
            Label(self.connection, item, deployment_id=self._id) for item in r["items"]
        ]

    @exception_handler
    @beartype
    def predict(
        self,
        file_path: str | Path,
        tags: str | Tag | list[Tag | str] | None = None,
        source: str | DataSource | None = None,
        metadata: dict | None = None,
        monitor: bool = True,
        upload_dir: str | None = None,
        custom_metadata: dict | None = None,
        postprocess: bool = True,
    ) -> dict:
        """Run a prediction on our Serving platform

        Examples:
            ```python
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            deployment.predict('image_420.png', tags=["gonna", "give"], source="camera-1")
            ```
        Arguments:
            file_path (str or Path): path to the image to predict.
            tags (str, (Tag), list[str | Tag], optional): a list of tag to add to the data that will be created on the platform.
            source (str or DataSource, optional): a source to attach to the data that will be created on the platform.
            metadata (dict, optional): metadata to attach to the data that will be created on the platform.
            monitor (bool, optional): if True, will send prediction on Picsellia and our monitoring service. Defaults to True.
            upload_dir (str, optional): This parameter can only be used with private object-storages. Specify this parameter to prefix the object name of the data. Filename will still contain a generated uuid4
            custom_metadata (dict, optional): custom_metadata to attach to the data that will be created on the platform.

        Returns:
            A (dict) with information of the prediction
        """
        with open(file_path, "rb") as file:
            file_data = file.read()
            filename = Path(file_path).name
            return self.predict_bytes(
                filename=filename,
                raw_image=file_data,
                tags=tags,
                source=source,
                metadata=metadata,
                monitor=monitor,
                upload_dir=upload_dir,
                custom_metadata=custom_metadata,
                postprocess=postprocess,
            )

    @exception_handler
    @beartype
    @retry((requests.ConnectionError, MonitoringConnectionError))
    def predict_bytes(
        self,
        filename: str,
        raw_image: bytes,
        tags: str | Tag | list[Tag | str] | None = None,
        source: str | DataSource | None = None,
        metadata: dict | None = None,
        monitor: bool = True,
        upload_dir: str | None = None,
        custom_metadata: dict | None = None,
        postprocess: bool = True,
    ) -> dict:
        """Run a prediction on our Serving platform with bytes of an image

        Examples:
            ```python
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            filename = "frame.png"
            with open(filename, 'rb') as img:
                img_bytes = img.read()
            deployment.predict_bytes(filename, img_bytes, tags=["tag1", "tag2"], source="camera-1")
            ```

        Arguments:
            filename (str): filename of the image.
            raw_image (bytes): bytes of the image to predict.
            tags (str, (Tag), list[str | Tag], optional): a list of tag to add to the data that will be created on the platform.
            source (str or DataSource, optional): a source to attach to the data that will be created on the platform.
            metadata (dict, optional): metadata to attach to the data that will be created on the platform.
            monitor (bool, optional): if True, will send prediction on Picsellia and our monitoring service. Defaults to True.
            upload_dir (str, optional): This parameter can only be used with private object-storages. Specify this parameter to prefix the object name of the data. Filename will still contain a generated uuid4
            custom_metadata (dict, optional): custom_metadata to attach to the data that will be created on the platform.

        Returns:
            A (dict) with information of the prediction
        """
        payload = self._prepare_payload_for_prediction(
            tags, source, monitor, upload_dir, postprocess
        )
        files = {"media": (filename, raw_image)}

        # as a dict cannot be sent into a multipart upload, we need to stringify it for the serving
        if metadata:
            payload["metadata"] = json.dumps(metadata)
        if custom_metadata:
            payload["custom_metadata"] = json.dumps(custom_metadata)

        response = self.serving_connection.post(
            path=f"/api/deployments/{self.id}/predict",
            data=payload,
            files=files,
        )
        if response.status_code > 500:
            raise MonitoringConnectionError()

        if response.status_code != 200:  # pragma: no cover
            raise PredictionError(f"Could not predict because {response.text}")

        return response.json()

    @exception_handler
    @beartype
    @retry((requests.ConnectionError, MonitoringConnectionError))
    def predict_cloud_image(
        self,
        object_name: str,
        tags: str | Tag | list[Tag | str] | None = None,
        source: str | DataSource | None = None,
        metadata: dict | None = None,
        monitor: bool = True,
        custom_metadata: dict | None = None,
        postprocess: bool = True,
    ) -> dict:
        """Run a prediction on our Serving platform, using object_name of a cloud object stored in your object storage.
        Your image MUST be stored in the storage used in the datalake linked to this deployment (the target datalake)
        If your image is already a data in your target datalake, it MUST NOT have been processed by this deployment,
            also, in this case, given source and metadata won't be used.

        Examples:
            ```python
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            object_name = "directory/s3/object-name.jpeg"
            deployment.predict_cloud_image(object_name, tags=["tag1", "tag2"], source="camera-1")
            ```

        Arguments:
            object_name (str): object name of the cloud image.
            tags (str, (Tag), list[str | Tag], optional): a list of tag to add to the data that will be created on the platform.
            source (str or DataSource, optional): a source to attach to the data that will be created on the platform.
            metadata (dict, optional): metadata to attach to the data that will be created on the platform.
            monitor (bool, optional): if True, will send prediction on Picsellia and our monitoring service. Defaults to True.
            custom_metadata (dict, optional): custom_metadata to attach to the data that will be created on the platform.

        Returns:
            A (dict) with information of the prediction
        """
        payload = self._prepare_payload_for_prediction(
            tags, source, monitor, upload_dir=None, postprocess=postprocess
        )
        if metadata:
            payload["metadata"] = metadata

        if custom_metadata:
            payload["custom_metadata"] = custom_metadata

        target_datalake_connector = self._fetch_target_datalake_connector()
        payload["cloud_image"] = {
            "connector_id": target_datalake_connector.id,
            "client_type": target_datalake_connector.client_type,
            "bucket_name": target_datalake_connector.bucket_name,
            "object_name": object_name,
        }

        response = self.serving_connection.post(
            path=f"/api/v2/deployments/{self.id}/predict",
            data=orjson.dumps(payload),
        )
        if response.status_code > 500:
            raise MonitoringConnectionError()

        if response.status_code != 200:  # pragma: no cover
            raise PredictionError(f"Could not predict because {response.text}")

        return response.json()

    @exception_handler
    @beartype
    def predict_data(
        self,
        data: Data,
        tags: str | Tag | list[Tag | str] | None = None,
        monitor: bool = True,
        postprocess: bool = True,
    ) -> dict:
        """Run a prediction on our Serving platform, using data.
        Your data must already be stored in the datalake used by the deployment (the target datalake).
        If there already is a prediction in this deployment linked to this data, it will be dismissed.

        Specified tags will be added to the ones already existing on the Data.

        Examples:
            ```python
            datalake = client.get_datalake(name="target-datalake")
            data = datalake.list_data(limit=1)[0]
            deployment = client.get_deployment(name="awesome-deploy")
            deployment.predict_data(data, tags=["tag1", "tag2"], monitor=False)
            ```

        Arguments:
            data (Data): object that you want to predict on.
            tags (str, (Tag), list[str | Tag], optional): a list of tag to add to the data
            monitor (bool, optional): if True, will send prediction on Picsellia and our monitoring service. Defaults to True.

        Returns:
            A (dict) with information of the prediction
        """
        return self.predict_cloud_image(
            data.object_name, tags=tags, monitor=monitor, postprocess=postprocess
        )

    @beartype
    @retry((requests.ConnectionError, MonitoringConnectionError))
    def predict_shadow(
        self, predicted_asset: PredictedAsset, monitor: bool = True
    ) -> dict:
        """Add a shadow prediction on a predicted asset.
        It will call our Serving platform, returning predictions coming from shadow model.
        If monitor is true, it will go to our monitoring service, then it will be added on the platform.

        Examples:
            ```python
            deployment = client.get_deployment(name="awesome-deploy")
            predicted_asset = deployment.list_predicted_assets(limit=1)[0]
            deployment.predict_shadow(predicted_asset, monitor=False)
            ```

        Arguments:
            predicted_asset (PredictedAsset): shadow model will predict on this asset.
            monitor (bool, optional): if True, will send prediction on Picsellia and our monitoring service. Defaults to True.

        Returns:
            A (dict) with prediction shapes
        """
        target_datalake_connector = self._fetch_target_datalake_connector()
        payload = {
            "prediction_id": predicted_asset.oracle_prediction_id,
            "monitor": monitor,
            "cloud_image": {
                "connector_id": target_datalake_connector.id,
                "client_type": target_datalake_connector.client_type,
                "bucket_name": target_datalake_connector.bucket_name,
                "object_name": predicted_asset.object_name,
            },
        }
        response = self.serving_connection.post(
            path=f"/api/v2/deployments/{self.id}/predict/shadow",
            data=orjson.dumps(payload),
        )
        if response.status_code > 500:
            raise MonitoringConnectionError

        if response.status_code != 200:  # pragma: no cover
            raise PredictionError(f"Could not predict shadow because {response.text}")

        return response.json()

    def _fetch_target_datalake_connector(
        self, force_refresh: bool = False
    ) -> TargetDatalakeConnectorSchema:
        if self._target_datalake_connector and not force_refresh:
            return self._target_datalake_connector

        r = self.connection.get(f"/api/deployment/{self.id}/datalake/connector").json()
        self._target_datalake_connector = TargetDatalakeConnectorSchema(**r)
        return self._target_datalake_connector

    @staticmethod
    def _prepare_payload_for_prediction(
        tags: str | Tag | list[Tag | str] | None,
        source: str | DataSource | None,
        monitor: bool,
        upload_dir: str | None,
        postprocess: bool = True,
    ) -> dict[str, Any]:
        sent_tags = []
        if tags:
            if isinstance(tags, str) or isinstance(tags, Tag):
                tags = [tags]

            for tag in tags:
                if isinstance(tag, Tag):
                    sent_tags.append(tag.name)
                else:
                    sent_tags.append(tag)

        if isinstance(source, DataSource):
            source = source.name

        payload: dict[str, Any] = {
            "tags": sent_tags,
            "monitor": monitor,
            "postprocess": postprocess,
        }
        if source:
            payload["source"] = source
        if upload_dir:
            payload["upload_dir"] = upload_dir
        return payload

    @exception_handler
    @beartype
    def setup_feedback_loop(
        self, dataset_version: DatasetVersion | None = None
    ) -> None:
        """Set up the Feedback Loop for a Deployment.
        You can specify one Dataset Version to attach to it or use the
        attach_dataset_to_feedback_loop() afterward,so you can add multiple ones.
        This is a great option to increase your training set with quality data.

        Examples:
            ```python
            dataset_version = client.get_dataset("my-dataset").get_version("latest")
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            deployment.setup_feedback_loop(dataset_version)
            ```

        Arguments:
            dataset_version (DatasetVersion, optional): This parameter is deprecated. Use attach_dataset_to_feedback_loop() instead.
        """
        self.connection.post(
            f"/api/deployment/{self.id}/pipeline/fl/setup", data=orjson.dumps({})
        )
        logger.info(f"Feedback loop set for {self}")

        if dataset_version:
            self.attach_dataset_version_to_feedback_loop(dataset_version)
            logger.warning(
                "`dataset_version` parameter will be deprecated in future versions. "
                "Please call the attach_dataset_version_to_feedback_loop() after setup with the desired "
                "Dataset Version instead"
            )

    @exception_handler
    @beartype
    def attach_dataset_version_to_feedback_loop(
        self, dataset_version: DatasetVersion
    ) -> None:
        """Attach a Dataset Version to a previously configured feedback-loop.

        Examples:
            ```python
            dataset_versions = client.get_dataset("my-dataset").list_versions()
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            deployment.setup_feedback_loop()
            for dataset_version in dataset_versions:
                deployment.attach_dataset_version_to_feedback_loop(dataset_version)
            ```

        Arguments:
            dataset_version (DatasetVersion): a (DatasetVersion) to attach
        """
        payload = {
            "dataset_version_id": dataset_version.id,
        }
        self.connection.post(
            f"/api/deployment/{self.id}/fl/datasets",
            data=orjson.dumps(payload),
        )

    @exception_handler
    @beartype
    def detach_dataset_version_from_feedback_loop(
        self, dataset_version: DatasetVersion
    ) -> None:
        """Detach a Dataset Version from a previously configured feedback-loop.

        Examples:
            ```python
            dataset_versions = client.get_dataset("my-dataset").list_versions()
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            deployment.setup_feedback_loop()
            for dataset_version in dataset_versions:
                deployment.attach_dataset_version_to_feedback_loop(dataset_version)
            deployment.detach_dataset_version_from_feedback_loop(dataset_versions[0])
            ```

        Arguments:
            dataset_version (DatasetVersion): a (DatasetVersion) to detach
        """

        payload = {"ids": [dataset_version.id]}
        self.connection.delete(
            f"/api/deployment/{self.id}/fl/datasets",
            data=orjson.dumps(payload),
        )

    @exception_handler
    @beartype
    def list_feedback_loop_datasets(self) -> list[DatasetVersion]:
        """List the Dataset Versions attached to the feedback-loop

        Examples:
            ```python
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            dataset_versions = deployment.list_feedback_loop_datasets()
            ```
        Returns:
            A list of (DatasetVersion)
        """
        r = self.connection.get(f"/api/deployment/{self.id}/fl/datasets").json()
        return [
            DatasetVersion(self.connection, item["dataset_version"])
            for item in r["items"]
        ]

    @exception_handler
    @beartype
    def toggle_feedback_loop(self, active: bool) -> None:
        """Toggle feedback loop for this deployment

        Examples:
            ```python
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            deployment.toggle_feedback_loop(
                True
            )
            ```
        Arguments:
            active (bool): (des)activate feedback loop
        """
        payload = {"active": active}
        self.connection.put(
            f"/api/deployment/{self.id}/pipeline/fl",
            data=orjson.dumps(payload),
        )
        logger.info(
            f"Feedback loop for {self} is now {'active' if active else 'deactivated'}"
        )

    @exception_handler
    @beartype
    def set_training_data(self, dataset_version: DatasetVersion) -> None:
        """This will give the training data reference to the deployment,
         so we can compute metrics based on this training data distribution in our Monitoring service

        Examples:
            ```python
            dataset_version = client.get_dataset("my-dataset").get_version("latest")
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            deployment.set_training_data(dataset_version)
            ```
        Arguments:
            dataset_version (DatasetVersion): a (DatasetVersion)
        """
        payload = {
            "dataset_version_id": dataset_version.id,
        }
        self.connection.post(
            f"/api/deployment/{self.id}/pipeline/td/setup",
            data=orjson.dumps(payload),
        )
        logger.info(f"Training Data set for {self} from {dataset_version}")

    @exception_handler
    @beartype
    def check_training_data_metrics_status(self) -> str:
        """Refresh the status of the metrics compute over the training data distribution.
        Set up can take some time, so you can check current state with this method.

        Examples:
            ```python
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            deployment.check_training_data_metrics_status()
            ```
        Returns:
            A string with the status of the metrics compute over the training data distribution
        """
        r = self.connection.get(f"/api/deployment/{self.id}/pipeline/td/check").json()
        status = r["status"]
        logger.info(f"Training Data status is {status}")
        return status

    @exception_handler
    @beartype
    def disable_training_data_reference(self) -> None:
        """Disable the reference to the training data in this Deployment.
        This means that you will not be able to see supervised metrics from the dashboard anymore.

        Examples:
            ```python
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            deployment.disable_training_data_reference()
            ```
        """
        self.connection.put(f"/api/deployment/{self.id}/pipeline/td/disable")
        logger.info(f"Training Data for {self} is disabled.")

    @exception_handler
    @beartype
    def setup_continuous_training(
        self,
        project: Project,
        dataset_version: DatasetVersion | None = None,
        model_version: ModelVersion | None = None,
        trigger: str | ContinuousTrainingTrigger = None,
        threshold: int | None = None,
        experiment_parameters: dict | None = None,
        scan_config: dict | None = None,
    ) -> None:
        """Initialize and activate the continuous training features of picsellia. 🥑
           A Training will be triggered using the attached dataset versions
           whenever your Deployment pipeline hit the trigger.
           You can call attach_dataset_version_to_continuous_training() method afterward.
           You can launch a continuous training via Experiment with parameter `experiment_parameters`
           You cannot launch a continuous training via Scan at the moment

        Examples:
            We want to set up a continuous training pipeline that will be trigger
            every 150 new predictions reviewed by your team.
            We will use the same training parameters as those used when building the first model.

            ```python
            deployment = client.get_deployment("awesome-deploy")
            project = client.get_project(name="my-project")
            dataset_version = project.get_dataset(name="my-dataset").get_version("latest")
            model_version = client.get_model(name="my-model").get_version(0)
            experiment = model_version.get_source_experiment()
            experiment_parameters = experiment.get_log('parameters')
            deployment.setup_continuous_training(
                project, threshold=150, experiment_parameters=experiment_parameters
            )
            deployment.attach_continuous
            ```
        Arguments:
            project (Project): The project that will host your pipeline.
            dataset_version (DatasetVersion, deprecated): This parameter is deprecated and is not used anymore.
            model_version (ModelVersion, deprecated): This parameter is deprecated and is not used anymore.
            threshold (int): Number of images that need to be review to trigger the training.
            trigger (ContinuousTrainingTrigger): Type of trigger to use when there is enough reviews.
            experiment_parameters (dict, optional):  Training parameters. Defaults to None.
        """
        payload: dict[str, Any] = {"project_id": project.id}

        if model_version:
            logger.warning(
                "`model_version` parameter is no longer used. "
                "Continuous Training will be configured with deployment's model version"
            )

        if dataset_version:
            logger.warning(
                "`dataset_version` parameter will be deprecated in future versions. "
                "Please call the attach_dataset_version_to_continuous_training() after setup with the desired "
                "Dataset Versions instead"
            )
        if trigger is not None and threshold is not None:
            payload["trigger"] = ContinuousTrainingTrigger.validate(trigger)
            payload["threshold"] = threshold

        if scan_config:
            logger.warning("`scan_config` parameter is no longer used.")

        if not experiment_parameters:
            raise BadConfigurationContinuousTrainingError(
                "You need to give `experiment_parameters`"
            )

        payload["training_type"] = ContinuousTrainingType.EXPERIMENT
        payload["experiment_parameters"] = experiment_parameters

        self.connection.post(
            f"/api/deployment/{self.id}/pipeline/ct",
            data=orjson.dumps(payload),
        )
        logger.info(f"Continuous training setup for {self}\n")

    @exception_handler
    @beartype
    def attach_dataset_version_to_continuous_training(
        self, alias: str, dataset_version: DatasetVersion
    ):
        """Attach a Dataset Version to a previously configured continuous training.

        Examples:
            ```python
            dataset_versions = client.get_dataset("my-dataset").list_versions()
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            deployment.setup_continuous_training(...)
            aliases = ["train", "test", "eval"]
            for i, dataset_version in enumerate(dataset_versions):
                deployment.attach_dataset_version_to_continuous_training(aliases[i], dataset_version)
            ```
        Arguments:
            alias (str): Alias of attached dataset
            dataset_version (DatasetVersion): A dataset version to attach to the Continuous Training.
        """
        payload = {"dataset_version_id": dataset_version.id, "name": alias}
        self.connection.post(
            f"/api/deployment/{self.id}/ct/datasets",
            data=orjson.dumps(payload),
        )
        logger.info(
            f"{dataset_version} attached to Continuous training of {self} with alias {alias}"
        )

    @exception_handler
    @beartype
    def detach_dataset_version_from_continuous_training(
        self, dataset_version: DatasetVersion
    ) -> None:
        """Detach a Dataset Versions to a previously configured continuous training.

        Examples:
            ```python
            dataset_versions = client.get_dataset("my-dataset").list_versions()
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            deployment.setup_continuous_training()
            for dataset_version in dataset_versions:
                deployment.attach_dataset_version_to_continuous_training(dataset_version)
            deployment.detach_dataset_version_from_continuous_training(dataset_versions[0])
            ```

        Arguments:
            dataset_version (DatasetVersion): a (DatasetVersion) to detach from Continuous Training settings
        """

        payload = {"ids": [dataset_version.id]}
        self.connection.delete(
            f"/api/deployment/{self.id}/ct/datasets",
            data=orjson.dumps(payload),
        )

    @exception_handler
    @beartype
    def toggle_continuous_training(self, active: bool) -> None:
        """Toggle continuous training for this deployment

        Examples:
            ```python
            deployment = client.get_deployment("awesome-deploy")
            deployment.toggle_continuous_training(active=False)
            ```

        Arguments:
            active (bool): (des)activate continuous training
        """
        payload = {"active": active}
        self.connection.put(
            f"/api/deployment/{self.id}/pipeline/ct",
            data=orjson.dumps(payload),
        )
        logger.info(
            f"Continuous training for {self} is now {'active' if active else 'deactivated'}"
        )

    @exception_handler
    @beartype
    def setup_continuous_deployment(
        self, policy: ContinuousDeploymentPolicy | str
    ) -> None:
        """Set up the continuous deployment for this pipeline

        Examples:
            ```python
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            deployment.setup_continuous_deployment(ContinuousDeploymentPolicy.DEPLOY_MANUAL)
            ```
        Arguments:
            policy (ContinuousDeploymentPolicy): policy to use
        """
        payload = {"policy": ContinuousDeploymentPolicy.validate(policy)}
        self.connection.post(
            f"/api/deployment/{self.id}/pipeline/cd",
            data=orjson.dumps(payload),
        )
        logger.info(f"Continuous deployment setup for {self} with policy {policy}\n")

    @exception_handler
    @beartype
    def toggle_continuous_deployment(self, active: bool) -> None:
        """Toggle continuous deployment for this deployment

        Examples:
            ```python
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            deployment.toggle_continuous_deployment(
                dataset
            )
            ```
        Arguments:
            active (bool): (des)activate continuous deployment
        """
        payload = {"active": active}
        self.connection.put(
            f"/api/deployment/{self.id}/pipeline/cd",
            data=orjson.dumps(payload),
        )
        logger.info(
            f"Continuous deployment for {self} is now {'active' if active else 'deactivated'}"
        )

    @exception_handler
    @beartype
    @retry((requests.ConnectionError, MonitoringConnectionError))
    def get_stats(
        self,
        service: ServiceMetrics,
        model_version: ModelVersion | None = None,
        from_timestamp: float | None = None,
        to_timestamp: float | None = None,
        since: int | None = None,
        includes: list[str] | None = None,
        excludes: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> dict:
        """Retrieve stats of this deployment stored in Picsellia environment.

        Mandatory param is "service" an enum of type ServiceMetrics. Values possibles are :
            PREDICTIONS_OUTLYING_SCORE
            PREDICTIONS_DATA
            REVIEWS_OBJECT_DETECTION_STATS
            REVIEWS_CLASSIFICATION_STATS
            REVIEWS_LABEL_DISTRIBUTION_STATS

            AGGREGATED_LABEL_DISTRIBUTION
            AGGREGATED_OBJECT_DETECTION_STATS
            AGGREGATED_PREDICTIONS_DATA
            AGGREGATED_DRIFTING_PREDICTIONS

        For aggregation, computation may not have been done by the past.
        You will need to force computation of these aggregations and retrieve them again.


        Examples:
            ```python
            my_deployment.get_stats(ServiceMetrics.PREDICTIONS_DATA)
            my_deployment.get_stats(ServiceMetrics.AGGREGATED_DRIFTING_PREDICTIONS, since=3600)
            my_deployment.get_stats(ServiceMetrics.AGGREGATED_LABEL_DISTRIBUTION, model_version=my_model)
            ```

        Arguments:
            service (str): service queried
            model_version (ModelVersion, optional): Model that shall be used when retrieving data.
                Defaults to None.
            from_timestamp (float, optional): System will only retrieve prediction data after this timestamp.
                Defaults to None.
            to_timestamp (float, optional): System will only retrieve prediction data before this timestamp.
                Defaults to None.
            since (int, optional): System will only retrieve prediction data that are in the last seconds.
                Defaults to None.
            includes (list[str], optional): Research will include these ids and excludes others.
                Defaults to None.
            excludes (list[str], optional): Research will exclude these ids.
                Defaults to None.
            tags (list[str], optional): Research will be done filtering by tags.
                Defaults to None.

        Returns:
            A dict with queried statistics about the service you asked
        """
        query_filter = self._build_filter(
            service=service.service,
            model_version=model_version,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
            since=since,
            includes=includes,
            excludes=excludes,
            tags=tags,
        )

        if service.is_aggregation:
            response = self.oracle_connection.get(
                path=f"/api/deployment/{self.id}/stats", params=query_filter
            )
            if response.status_code > 500:
                raise MonitoringConnectionError()
            content = response.json()
            if "infos" in content and "info" in content["infos"]:
                logger.info("This computation is outdated or has never been done.")
                logger.info(
                    "You can compute it again by calling launch_computation with exactly the same params."
                )
            return content
        else:
            response = self.oracle_connection.get(
                path=f"/api/deployment/{self.id}/predictions/stats",
                params=query_filter,
            )
            if response.status_code > 500:
                raise MonitoringConnectionError()
            return response.json()

    @staticmethod
    def _build_filter(
        service: str,
        model_version: ModelVersion | None = None,
        from_timestamp: float | None = None,
        to_timestamp: float | None = None,
        since: int | None = None,
        includes: list[str] | None = None,
        excludes: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> dict[str, Any]:
        query_filter: dict[str, Any] = {"service": service}

        if model_version is not None:
            query_filter["model_id"] = model_version.id

        if from_timestamp is not None:
            query_filter["from_timestamp"] = from_timestamp

        if to_timestamp is not None:
            query_filter["to_timestamp"] = to_timestamp

        if since is not None:
            query_filter["since"] = since

        if includes is not None:
            query_filter["includes"] = includes

        if excludes is not None:
            query_filter["excludes"] = excludes

        if tags is not None:
            query_filter["tags"] = tags

        return query_filter

    @exception_handler
    @beartype
    def monitor(
        self,
        image_path: str | Path,
        latency: float,
        height: int,
        width: int,
        prediction: PredictionFormat,
        source: str | None = None,
        tags: list[str] | None = None,
        timestamp: float | None = None,
        model_version: ModelVersion | None = None,
        shadow_model_version: ModelVersion | None = None,
        shadow_latency: float | None = None,
        shadow_raw_predictions: PredictionFormat | None = None,
        shadow_prediction: PredictionFormat | None = None,
        content_type: SupportedContentType | str | None = None,
        metadata: dict | None = None,
        upload_dir: str | None = None,
        custom_metadata: dict | None = None,
        sample: bool | None = None,
        custom_metrics: dict | None = None,
    ) -> dict:
        """Send a prediction for this deployment on our monitoring service.

        :warning: Signature of this method has been recently changed and can break some methods :
        - model_version and shadow_model_version are not used anymore : system will use what's currently being monitored in this deployment
        - shadow_raw_predictions has been renamed to shadow_prediction

        Arguments:
            image_path (str or Path): image path
            latency (float): latency used by model to compute your prediction
            height (int): height of image
            width (int): width of image
            prediction (PredictionFormat): data of your prediction, can be a Classification, a Segmentation or an ObjectDetection Format.
                DetectionPredictionFormat, ClassificationPredictionFormat and SegmentationPredictionFormat:
                    detection_classes (list[int]): list of classes
                    detection_scores (list[float]): list of scores of predictions
                DetectionPredictionFormat and SegmentationPredictionFormat:
                    detection_boxes (list[list[int]]): list of bboxes representing rectangles of your shapes. bboxes are formatted as
                                                            [top, left, bottom, right]
                SegmentationPredictionFormat:
                    detection_masks  list[list[list[int]]]): list of polygon shapes, each element corresponds to a distinct shape and is a list of the coordinates
                                                            one polygon will look like [[x1, y1], [x2, y2], [x3, y3], [x4, y4], ...]
                LinePredictionFormat:
                    lines (list[list[int]]): list of line shapes, each element corresponds to a distinct shape and is a list of the coordinates
                                                            one line will look like [[x1, y1], [x2, y2], [x3, y3], [x4, y4], ...]
                PointPredictionFormat:
                    points (list[list[int]]): list of point shapes, each element corresponds to a distinct point and is the coordinates
                                                            a point will look like [x, y]

            source (str, optional): (Data) will have this source in Picsellia. Defaults to None.
            tags (list[str], optional): tags that can give some metadata to your prediction. Defaults to None.
            timestamp (float, optional): timestamp of your prediction. Defaults to timestamp of monitoring service on reception.
            shadow_latency (float, optional): latency used by shadow model to compute prediction
            shadow_prediction (PredictionFormat, optional): data of your prediction made by shadow model.
            content_type (str, optional): if given, we won't try to infer content type with mimetype library
            metadata (dict, optional): (Data) will have this metadata in Picsellia. Defaults to None.
            upload_dir (str, optional): This parameter can only be used with private object-storages. Specify this parameter to prefix the object name of the data. Filename will still contain a generated uuid4
            custom_metadata (dict, optional): (Data) will have this custom_metadata in Picsellia. Defaults to None.
            sample (bool, optional): control sample policy by using this field.
                    If True, the Data and the Prediction will be stored under the Deployment (no matter the sample_rate).
                    If False, the Data and the Prediction won't be stored, monitoring metrics WILL still be computed.
                    If unset, we will store the Data and Prediction according to the sample_rate (if existing).
            custom_metrics (dict, optional): (PredictedAsset) will have this custom_metrics in Picsellia. Defaults to None.
        Returns:
            a dict of data returned by our monitoring service
        """
        if model_version:  # pragma: no cover
            logger.warning(
                "'model_version' will soon be removed. It is not used anymore"
            )

        if shadow_model_version:  # pragma: no cover
            logger.warning(
                "'shadow_model_version' will soon be removed. It is not used anymore"
            )

        if shadow_raw_predictions and not shadow_prediction:  # pragma: no cover
            logger.warning(
                "'shadow_raw_predictions' parameter will soon be removed. Please use 'shadow_prediction'"
            )
            shadow_prediction = shadow_raw_predictions

        if not content_type:
            content_type = mimetypes.guess_type(image_path, strict=False)[0]
            if content_type is None:  # pragma: no cover
                raise ContentTypeUnknown(
                    f"Content type of {image_path} could not be inferred"
                )

        # Open image, encode it into base64, read filename and content type.
        with open(image_path, "rb") as img_file:
            raw_image = img_file.read()
            filename = Path(image_path).name

        return self.monitor_bytes(
            raw_image,
            content_type,
            filename,
            latency,
            height,
            width,
            prediction,
            source,
            tags,
            timestamp,
            shadow_latency,
            shadow_prediction,
            metadata,
            upload_dir,
            custom_metadata,
            sample,
            custom_metrics,
        )

    @exception_handler
    @beartype
    def monitor_bytes(
        self,
        raw_image: bytes,
        content_type: SupportedContentType | str,
        filename: str,
        latency: float,
        height: int,
        width: int,
        prediction: PredictionFormat,
        source: str | None = None,
        tags: list[str] | None = None,
        timestamp: float | None = None,
        shadow_latency: float | None = None,
        shadow_prediction: PredictionFormat | None = None,
        metadata: dict | None = None,
        upload_dir: str | None = None,
        custom_metadata: dict | None = None,
        sample: bool | None = None,
        custom_metrics: dict | None = None,
    ) -> dict:
        """Send a prediction for this deployment on our monitoring service.
        You can use this method instead of monitor() if you have a bytes image and not an image file.
        We will convert it into base 64 as utf8 string and send it to the monitoring service.

        Arguments:
            raw_image (bytes): raw image in bytes
            content_type (SupportedContentType or str): content type of image, only 'image/jpeg' or 'image/png' currently supported
            filename (str): filename of image
            latency (float): latency used by model to compute your prediction
            height (int): height of image
            width (int): width of image
            prediction (PredictionFormat): data of your prediction, can be a Classification, a Segmentation or an ObjectDetection Format.
                DetectionPredictionFormat, ClassificationPredictionFormat and SegmentationPredictionFormat:
                    detection_classes (list[int]): list of classes
                    detection_scores (list[float]): list of scores of predictions
                DetectionPredictionFormat:
                    detection_boxes (list[list[int]]): list of bboxes representing rectangles of your shapes. bboxes are formatted as
                                                            [top, left, bottom, right]
                SegmentationPredictionFormat:
                    detection_masks (list[list[int]]): list of polygons of your shapes. each polygon is a list of points with coordinates flattened
                                                            [x1, y1, x2, y2, x3, y3, x4, y4, ..]

            source (str, optional): source that can give some metadata to your prediction. Defaults to None.
            tags (list[str], optional): tags that can give some metadata to your prediction. Defaults to None.
            timestamp (float, optional): timestamp of your prediction. Defaults to timestamp of monitoring service on reception.
            shadow_latency (float, optional): latency used by shadow model to compute prediction
            shadow_prediction (PredictionFormat, optional): data of your prediction made by shadow model.
            metadata (dict, optional): (Data) will have this metadata in Picsellia. Defaults to None.
            upload_dir (str, optional): This parameter can only be used with private object-storages. Specify this parameter to prefix the object name of the data. Filename will still contain a generated uuid4
            custom_metadata (dict, optional): (Data) will have this custom_metadata in Picsellia. Defaults to None.
            sample (bool, optional): control sample policy by using this field.
                    If True, the Data and the Prediction will be stored under the Deployment (no matter the sample_rate).
                    If False, the Data and the Prediction won't be stored, monitoring metrics WILL still be computed.
                    If unset, we will store the Data and Prediction according to the sample_rate (if existing).
            custom_metrics (dict, optional): (PredictedAsset) will have this custom_metrics in Picsellia. Defaults to None.
        Returns:
            a dict of data returned by our monitoring service
        """
        payload = self._prepare_payload_monitor(
            filename,
            latency,
            height,
            width,
            prediction,
            content_type,
            source,
            tags,
            timestamp,
            shadow_latency,
            shadow_prediction,
            metadata,
            upload_dir,
            custom_metadata,
            sample,
            custom_metrics,
        )
        # Convert bytes into a base 64 string
        payload["image"] = base64.b64encode(raw_image).decode("utf-8")
        return self._request_monitor(payload)

    @exception_handler
    @beartype
    def monitor_cloud_image(
        self,
        object_name: str,
        latency: float,
        height: int,
        width: int,
        prediction: PredictionFormat,
        content_type: SupportedContentType | str,
        source: str | None = None,
        tags: list[str] | None = None,
        timestamp: float | None = None,
        shadow_latency: float | None = None,
        shadow_prediction: PredictionFormat | None = None,
        metadata: dict | None = None,
        custom_metadata: dict | None = None,
        sample: bool | None = None,
        custom_metrics: dict | None = None,
    ) -> dict:
        """Monitor an image on our monitoring platform, using object_name of a cloud object stored in your object storage.

        Arguments:
            object_name (str): object name of the cloud image.
            latency (float): latency used by model to compute your prediction
            height (int): height of image
            width (int): width of image
            prediction (PredictionFormat): data of your prediction, can be a Classification, a Segmentation or an ObjectDetection Format.
                DetectionPredictionFormat, ClassificationPredictionFormat and SegmentationPredictionFormat:
                    detection_classes (list[int]): list of classes
                    detection_scores (list[float]): list of scores of predictions
                DetectionPredictionFormat and SegmentationPredictionFormat:
                    detection_boxes (list[list[int]]): list of bboxes representing rectangles of your shapes. bboxes are formatted as
                                                            [top, left, bottom, right]
                SegmentationPredictionFormat:
                    detection_masks (list[list[int]]): list of polygons of your shapes. each polygon is a list of points with coordinates flattened
                                                            [x1, y1, x2, y2, x3, y3, x4, y4, ..]

            source (str, optional): (Data) will have this source in Picsellia. Defaults to None.
            tags (list[str], optional): tags that can give some metadata to your prediction. Defaults to None.
            timestamp (float, optional): timestamp of your prediction. Defaults to timestamp of monitoring service on reception.
            shadow_latency (float, optional): latency used by shadow model to compute prediction
            shadow_prediction (PredictionFormat, optional): data of your prediction made by shadow model.
            content_type (str, optional): if given, we won't try to infer content type with mimetype library
            metadata (dict, optional): (Data) will have this metadata in Picsellia. Defaults to None.
            custom_metadata (dict, optional): (Data) will have this custom_metadata in Picsellia. Defaults to None.
            sample (bool, optional): control sample policy by using this field.
                    If True, the Data and the Prediction will be stored under the Deployment (no matter the sample_rate).
                    If False, the Data and the Prediction won't be stored, monitoring metrics WILL still be computed.
                    If unset, we will store the Data and Prediction according to the sample_rate (if existing).
            custom_metrics (dict, optional): (PredictedAsset) will have this custom_metrics in Picsellia. Defaults to None.
        Returns:
            a dict of data returned by our monitoring service
        """
        filename = os.path.basename(object_name)
        payload = self._prepare_payload_monitor(
            filename,
            latency,
            height,
            width,
            prediction,
            content_type,
            source,
            tags,
            timestamp,
            shadow_latency,
            shadow_prediction,
            metadata,
            upload_dir=None,
            custom_metadata=custom_metadata,
            sample=sample,
            custom_metrics=custom_metrics,
        )

        target_datalake_connector = self._fetch_target_datalake_connector()
        payload["cloud_image"] = {
            "connector_id": target_datalake_connector.id,
            "client_type": target_datalake_connector.client_type,
            "bucket_name": target_datalake_connector.bucket_name,
            "object_name": object_name,
        }

        return self._request_monitor(payload)

    @exception_handler
    @beartype
    def monitor_data(
        self,
        data: Data,
        latency: float,
        height: int,
        width: int,
        prediction: PredictionFormat,
        tags: list[str] | None = None,
        timestamp: float | None = None,
        shadow_latency: float | None = None,
        shadow_prediction: PredictionFormat | None = None,
        sample: bool | None = None,
        custom_metrics: dict | None = None,
    ) -> dict:
        """Monitor an image on our monitoring platform
        Your data must already be stored in the datalake used by the deployment (the target datalake).
        If there already is a prediction in this deployment linked to this data, it will be dismissed.

        Arguments:
            data (Data): data to monitor
            latency (float): latency used by model to compute your prediction
            height (int): height of image
            width (int): width of image
            prediction (PredictionFormat): data of your prediction, can be a Classification, a Segmentation or an ObjectDetection Format.
                DetectionPredictionFormat, ClassificationPredictionFormat and SegmentationPredictionFormat:
                    detection_classes (list[int]): list of classes
                    detection_scores (list[float]): list of scores of predictions
                DetectionPredictionFormat and SegmentationPredictionFormat:
                    detection_boxes (list[list[int]]): list of bboxes representing rectangles of your shapes. bboxes are formatted as
                                                            [top, left, bottom, right]
                SegmentationPredictionFormat:
                    detection_masks (list[list[int]]): list of polygons of your shapes. each polygon is a list of points with coordinates flattened
                                                            [x1, y1, x2, y2, x3, y3, x4, y4, ..]

            tags (list[str], optional): tags that can give some metadata to your prediction. Defaults to None.
            timestamp (float, optional): timestamp of your prediction. Defaults to timestamp of monitoring service on reception.
            shadow_latency (float, optional): latency used by shadow model to compute prediction
            shadow_prediction (PredictionFormat, optional): data of your prediction made by shadow model.
            sample (bool, optional): control sample policy by using this field.
                    If True, the Data and the Prediction will be stored under the Deployment (no matter the sample_rate).
                    If False, the Data and the Prediction won't be stored, monitoring metrics WILL still be computed.
                    If unset, we will store the Data and Prediction according to the sample_rate (if existing).
            custom_metrics (dict, optional): (PredictedAsset) will have this custom_metrics in Picsellia. Defaults to None.

        Returns:
            a dict of data returned by our monitoring service
        """
        return self.monitor_cloud_image(
            data.object_name,
            latency,
            height,
            width,
            prediction,
            data.content_type,
            source=None,
            tags=tags,
            timestamp=timestamp,
            shadow_latency=shadow_latency,
            shadow_prediction=shadow_prediction,
            metadata=None,
            custom_metadata=None,
            sample=sample,
            custom_metrics=custom_metrics,
        )

    def _prepare_payload_monitor(  # noqa: C901
        self,
        filename: str,
        latency: float,
        height: int,
        width: int,
        prediction: PredictionFormat,
        content_type: SupportedContentType | str,
        source: str | None,
        tags: list[str] | None,
        timestamp: float | None,
        shadow_latency: float | None,
        shadow_prediction: PredictionFormat | None,
        metadata: dict | None,
        upload_dir: str | None,
        custom_metadata: dict | None,
        sample: bool | None,
        custom_metrics: dict | None,
    ):
        if prediction.model_type != self.type:
            raise BadRequestError(
                f"Prediction shape of this type {prediction.model_type} cannot be used with this model {self.type}"
            )

        try:
            content_type = SupportedContentType.validate(content_type)
        except TypeError:
            raise ContentTypeUnknown(
                f"Content type {content_type} is not supported : {SupportedContentType.values()}"
            )

        payload = {
            "filename": filename,
            "content_type": content_type.value,
            "height": height,
            "width": width,
            "raw_predictions": prediction.model_dump(),
            "latency": latency,
        }

        if source is not None:
            payload["source"] = source

        if tags is not None:
            payload["tags"] = tags

        if metadata is not None:
            payload["metadata"] = metadata

        if custom_metadata is not None:
            payload["custom_metadata"] = custom_metadata

        if timestamp is not None:
            payload["timestamp"] = timestamp

        if upload_dir is not None:
            payload["upload_dir"] = upload_dir

        if shadow_prediction is not None:
            if shadow_latency is None:
                raise BadRequestError(
                    "Shadow latency and shadow raw predictions shall be defined if you want to push a shadow result"
                )
            if shadow_prediction.model_type != self.type:
                raise BadRequestError(
                    f"Prediction shape of this type {prediction.model_type} cannot be used with this model {self.type}"
                )

            payload["shadow_latency"] = shadow_latency
            payload["shadow_raw_predictions"] = shadow_prediction.model_dump()

        if sample is not None:
            payload["sample"] = sample

        if custom_metrics is not None:
            payload["custom_metrics"] = custom_metrics

        return payload

    @retry((requests.ConnectionError, MonitoringConnectionError))
    def _request_monitor(self, payload: dict) -> dict:
        response = self.oracle_connection.post(
            path=f"/api/deployment/{self.id}/predictions",
            data=orjson.dumps(payload),
        )
        if response.status_code > 500:
            raise MonitoringConnectionError()

        if response.status_code == 409:
            error = response.json()["message"]
            raise MonitorError(f"This data has already been processed : {error}")

        if response.status_code != 201:  # pragma: no cover
            raise MonitorError(
                f"Our monitoring service could not handle your prediction: {response.status_code}.\n Error : {response.text}"
            )

        return response.json()

    @exception_handler
    @beartype
    def monitor_shadow(
        self,
        predicted_asset: PredictedAsset,
        shadow_latency: float,
        shadow_prediction: PredictionFormat,
    ) -> None:
        """Add a shadow prediction on an existing PredictedAsset.
        You can call monitor_shadow_from_oracle_prediction_id() if you only have oracle_prediction_id

        Arguments:
            predicted_asset (PredictedAsset): asset already processed on which to add shadow_prediction
            shadow_latency (float): latency used by shadow model to compute prediction
            shadow_prediction (PredictionFormat): data of your prediction made by shadow model
        """
        return self.monitor_shadow_from_oracle_prediction_id(
            predicted_asset.oracle_prediction_id, shadow_latency, shadow_prediction
        )

    @exception_handler
    @beartype
    @retry((requests.ConnectionError, MonitoringConnectionError))
    def monitor_shadow_from_oracle_prediction_id(
        self,
        oracle_prediction_id: str | UUID,
        shadow_latency: float,
        shadow_prediction: PredictionFormat,
    ) -> None:
        """Add a shadow prediction on an existing PredictedAsset, from the oracle_prediction_id

        Arguments:
            oracle_prediction_id (str or UUID): oracle_prediction_id that was returned on monitor()
            shadow_latency (float): latency used by shadow model to compute prediction
            shadow_prediction (PredictionFormat): data of your prediction made by shadow model
        """
        payload = {
            "shadow_raw_predictions": shadow_prediction.model_dump(),
            "shadow_latency": shadow_latency,
        }
        response = self.oracle_connection.post(
            path=f"/api/prediction/{oracle_prediction_id}/shadow",
            data=orjson.dumps(payload),
        )
        if response.status_code > 500:
            raise MonitoringConnectionError()

        if response.status_code == 409:
            error = response.json()["message"]
            raise MonitorError(
                f"This prediction has already been shadow processed : {error}"
            )

        if response.status_code != 201:  # pragma: no cover
            raise MonitorError(
                f"Our monitoring service could not handle your shadow prediction: {response.status_code}. Check {response.text}"
            )

    @exception_handler
    @beartype
    def find_predicted_asset(
        self,
        id: str | UUID | None = None,
        oracle_prediction_id: str | UUID | None = None,
        object_name: str | None = None,
        filename: str | None = None,
        data_id: str | UUID | None = None,
    ) -> PredictedAsset:
        """Find a PredictedAsset of this deployment.

        Examples:
            ```python
            oracle_prediction_id = deployment.monitor(path, latency, height, width, prediction_data)["id"]
            predicted_asset = deployment.find_predicted_asset(oracle_prediction_id=oracle_prediction_id)
            deployment.monitor_shadow(predicted_asset, shadow_latency, shadow_prediction_data)
            ```
         Arguments:
            id (UUID, optional): id of PredictedAsset to fetch. Defaults to None.
            oracle_prediction_id (UUID, optional): id of the prediction in our monitoring system. Defaults to None.
            filename (str, optional): filename of the data. Defaults to None.
            object_name (str, optional): object_name of the data. Defaults to None.
            data_id (UUID, optional): id of the data related to this PredictedAsset. Defaults to None.

        Raises:
            If no asset match the query, it will raise a NotFoundError.
            In some case, it can raise an InvalidQueryError,
                it might be because the platform stores 2 assets matching this query (for example if filename is duplicated)

        Returns:
            The (PredictedAsset) found
        """
        if (
            not id
            and not oracle_prediction_id
            and not object_name
            and not filename
            and not data_id
        ):
            raise AssertionError(
                "Please select at least one criteria to find a predicted asset"
            )

        params: dict[str, Any] = {}
        if id:
            params["id"] = id

        if oracle_prediction_id:
            params["oracle_prediction_id"] = oracle_prediction_id

        if object_name:
            params["object_name"] = object_name

        if filename:
            params["filename"] = filename

        if data_id:
            params["data_id"] = data_id

        r = self.connection.get(
            f"/api/deployment/{self.id}/predictedassets/find", params=params
        ).json()
        return PredictedAsset(self.connection, self.id, r)

    @exception_handler
    @beartype
    def list_predicted_assets(
        self,
        limit: int | None = None,
        offset: int | None = None,
        page_size: int | None = None,
        order_by: list[str] | None = None,
        q: str | None = None,
        assignment_status: str | None = None,
        assignment_step_id: UUID | None = None,
        assignment_user_id: str | UUID | None = None,
        custom_metadata: dict | None = None,
    ) -> MultiPredictedAsset:
        """List (PredictedAsset) of this (Deployment)

        Examples:
            ```python
            assets = deployment.list_predicted_assets()
            ```

        Arguments:
            limit (int, optional): the number of assets that will be retrieved
            offset (int, optional): from where to start accessing the assets. you will retrieve offset:offset+limit assets from the whole list.
            page_size (int, optional): deprecated.
            order_by (str, optional): what property to sort on. Defaults to descending created_at.
            q (str, optional): a query using the Picsellia Query Language. Defaults to None
            assignment_status (str, optional): only with campaigns. It's the desired status for the last assignments linked to your (PredictedAsset).
            assignment_step_id (UUID, optional): only with campaigns. It's the desired step of the assignment you want to retrieve.
            assignment_user_id (UUID, optional): only with Campaigns. It's the desired user assigned to the assignments you want to retrieve.
            custom_metadata: (dict, optional): filter based on the custom_metadata linked to the asset's Data. Defaults to None
        Returns:
            A (MultiAsset) object that wraps some (Asset) that you can manipulate.
        """
        if page_size:
            logger.warning("page_size is deprecated and not used anymore.")

        filters = PredictedAssetFilter.model_validate(
            {
                "limit": limit,
                "offset": offset,
                "order_by": order_by,
                "query": q,
                "assignment_status": assignment_status,
                "assignment_step_id": assignment_step_id,
                "assignment_user_id": assignment_user_id,
                "custom_metadata": custom_metadata,
            }
        )
        assets = PredictedAssetLister(self.connection, self.id).list_items(filters)

        if len(assets) == 0:
            raise NoDataError("No predicted asset retrieved")

        return MultiPredictedAsset(self.connection, self.id, assets)

    @exception_handler
    @beartype
    @deprecated(
        deprecated_in="6.24.0",
        removed_in="6.27.0",
        details="This method should not be called anymore. Instead use list_users()",
    )
    def list_workers(self) -> list[Worker]:
        """List all workers of this deployment

        Examples:
            ```python
            deployment.list_workers()
            ```

        Returns:
            List of (Worker) objects
        """
        return [
            Worker(
                self.connection,
                {"id": item.id, "username": item.username, "user_id": item.id},
                WorkerType.DEPLOYMENT,
            )
            for item in self.list_users()
        ]

    @exception_handler
    @beartype
    def create_campaign(
        self,
        description: str | None = None,
        instructions_file_path: str | None = None,
        instructions_text: str | None = None,
        end_date: date | None = None,
        auto_add_new_assets: bool | None = False,
        auto_close_on_completion: bool | None = False,
    ) -> ReviewCampaign:
        """Create campaign on a deployment.

        Examples:
            ```python
            foo_deployment.create_campaign()
            ```
        Arguments:
            description (str, optional): Description of the campaign. Defaults to None.
            instructions_file_path (str, optional): Instructions file path. Defaults to None.
            instructions_text (str, optional): Instructions text. Defaults to None.
            end_date (date, optional): End date of the campaign. Defaults to None.
            auto_add_new_assets (bool, optional): If true, new assets of this deployment will be added as a task
                                                    in the campaign. Defaults to False.
            auto_close_on_completion (bool, optional): If true, campaign will be close when all tasks will be done.
                                                        Defaults to False.

        Returns:
            A (ReviewCampaign) object
        """
        payload = {
            "description": description,
            "instructions_text": instructions_text,
            "end_date": end_date,
            "auto_add_new_assets": auto_add_new_assets,
            "auto_close_on_completion": auto_close_on_completion,
        }

        if instructions_file_path:
            instructions_file_name = os.path.basename(instructions_file_path)
            object_name = self.connection.generate_deployment_object_name(
                instructions_file_name,
                ObjectDataType.REVIEW_CAMPAIGN_FILE,
                deployment_id=self.id,
            )
            self.connection.upload_file(object_name, instructions_file_path)
            payload["instructions_object_name"] = object_name

        r = self.connection.post(
            f"/api/deployment/{self.id}/campaigns",
            data=orjson.dumps(payload),
        ).json()
        campaign = ReviewCampaign(self.connection, r)
        self._review_campaign_id = campaign.id
        logger.info(f"{campaign} has been created to {self}")
        return campaign

    @exception_handler
    @beartype
    def get_campaign(self) -> ReviewCampaign:
        """Get campaign of a dataset version.

        Examples:
            ```python
            foo_deployment.get_campaign()
            ```

        Returns:
            A (ReviewCampaign) object
        """
        if not self._review_campaign_id:
            self.sync()

        if not self._review_campaign_id:
            raise NoDataError("There is no review campaign defined in this deployment")

        try:
            r = self.connection.get(
                f"/api/campaigns/review/{self._review_campaign_id}"
            ).json()
        except ResourceNotFoundError:
            self._review_campaign_id = None
            raise

        return ReviewCampaign(self.connection, r)
