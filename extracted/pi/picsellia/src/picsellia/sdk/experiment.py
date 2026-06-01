import logging
import os
from pathlib import Path
from typing import Any
from uuid import UUID

import orjson
from beartype import beartype
from deprecation import deprecated

from picsellia import exceptions, utils
from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.exceptions import (
    BadRequestError,
    ResourceConflictError,
    ResourceNotFoundError,
)
from picsellia.sdk.artifact import Artifact
from picsellia.sdk.asset import Asset, MultiAsset
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.dataset_version import DatasetVersion
from picsellia.sdk.evaluation import Evaluation, MultiEvaluation
from picsellia.sdk.job import Job
from picsellia.sdk.label import Label
from picsellia.sdk.log import Log, LogType
from picsellia.sdk.logging_file import LoggingFile
from picsellia.sdk.model import Model
from picsellia.sdk.model_version import ModelVersion
from picsellia.sdk.worker import Worker
from picsellia.services.training import TrainingService
from picsellia.types.enums import (
    AddEvaluationType,
    AnnotationStatus,
    ExperimentStatus,
    InferenceType,
    JobStatus,
    ObjectDataType,
)
from picsellia.types.schemas import ExperimentSchema, LogDataType

logger = logging.getLogger("picsellia")


class Experiment(Dao):
    def __init__(self, connexion: Connection, data: dict) -> None:
        Dao.__init__(self, connexion, data)

    @property
    def name(self) -> str:
        """Name of this (Experiment)"""
        return self._name

    @property
    def project_id(self) -> UUID:
        """Project id of this (Experiment)"""
        return self._project_id

    @property
    def status(self) -> ExperimentStatus:
        """Status of this (Experiment)"""
        return self._status

    @property
    def base_dir(self):
        return self.name

    @property
    def metrics_dir(self):
        return os.path.join(self.base_dir, "metrics")

    @property
    def png_dir(self):
        return os.path.join(self.base_dir, "images")

    @property
    def checkpoint_dir(self):
        return os.path.join(self.base_dir, "checkpoint")

    @property
    def record_dir(self):
        return os.path.join(self.base_dir, "records")

    @property
    def config_dir(self):
        return os.path.join(self.base_dir, "config")

    @property
    def results_dir(self):
        return os.path.join(self.base_dir, "results")

    @property
    def exported_model_dir(self):
        return os.path.join(self.base_dir, "exported_model")

    def __str__(self):
        return f"{Colors.BLUE}Experiment '{self.name}' {Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def get_resource_url_on_platform(self) -> str:
        """Get platform url of this resource.

        Examples:
            ```python
            print(experiment.get_resource_url_on_platform())
            >>> "https://app.picsellia.com/experiment/62cffb84-b92c-450c-bc37-8c4dd4d0f590"
            ```

        Returns:
            Url on Platform for this resource
        """

        return f"{self.connection.host}/experiment/{self.id}"

    @exception_handler
    @beartype
    def refresh(self, data: dict):
        schema = ExperimentSchema(**data)
        self._name = schema.name
        self._project_id = schema.project_id
        self._status = schema.status
        return schema

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/experiment/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def update(
        self,
        name: str | None = None,
        description: str | None = None,
        base_experiment: "Experiment | None" = None,
        base_model_version: "ModelVersion | None" = None,
        status: ExperimentStatus | str | None = None,
    ) -> None:
        """Update this experiment with a given name, description, a base experiment, a base model version or a status.

        Examples:
            ```python
            my_experiment.update(description="First try Yolov5")
            ```

        Arguments:
            name (str, optional): Name of the experiment. Defaults to None.
            description (str, optional): Description of the experiment. Defaults to None.
            base_experiment (Experiment, optional): deprecated.
            base_model_version (ModelVersion, optional): deprecated.
            status (ExperimentStatus or str, optional): Status of the experiment. Defaults to None.
        """
        payload: dict[str, Any] = {"name": name, "description": description}

        if status:
            payload["status"] = ExperimentStatus.validate(status)

        if base_experiment:
            logger.warning(
                "base_experiment parameter is deprecated and cannot be used anymore. Please call attach_experiment()"
            )

        if base_model_version:
            logger.warning(
                "base_model_version parameter is deprecated and cannot be used anymore. Please call attach_model_version()"
            )

        filtered_payload = utils.filter_payload(payload)
        r = self.connection.patch(
            f"/api/experiment/{self.id}", data=orjson.dumps(filtered_payload)
        ).json()
        self.refresh(r)

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete this experiment.

        Examples:
            ```python
            my_experiment.delete()
            ```
        """
        self.connection.delete(f"/api/experiment/{self.id}")

    @exception_handler
    @beartype
    def list_artifacts(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
    ) -> list[Artifact]:
        """List artifacts stored in the experiment.

        Examples:
            ```python
            artifacts = my_experiment.list_artifacts()
            ```

        Arguments:
            limit (int, optional): limit of artifacts to retrieve. Defaults to None.
            offset (int, optional): offset to start retrieving artifacts. Defaults to None.
            order_by (list[str], optional): fields to order by. Defaults to None.

        Returns:
            A list of (Artifact) objects that you can manipulate
        """
        return TrainingService(self.connection, self.id).list_artifacts(
            limit, offset, order_by
        )

    @exception_handler
    @beartype
    def delete_all_artifacts(self) -> None:
        """Delete all stored artifacts for experiment

        :warning: **DANGER ZONE**: This will definitely remove the artifacts from our servers

        Examples:
            ```python
            experiment.delete_all_artifacts()
            ```
        """
        artifact_ids = self.connection.get(
            f"/api/experiment/{self.id}/artifacts/ids"
        ).json()
        payload = {"ids": artifact_ids}
        self.connection.delete(
            f"/api/experiment/{self.id}/artifacts", data=orjson.dumps(payload)
        )

    @exception_handler
    @beartype
    def create_artifact(
        self, name: str, filename: str, object_name: str, large: bool = False
    ) -> Artifact:
        """Create an artifact for this experiment.

        Examples:
            ```python
            self.create_artifact(name="a_file", filename="file.png", object_name="some_file_in_s3.png", large=False)
            ```
        Arguments:
            name (str): name of the artifact.
            filename (str): filename.
            object_name (str): s3 object name.
            large (bool, optional): >5Mb or not. Defaults to False.

        Returns:
            An (Artifact) object
        """
        payload = {
            "name": name,
            "filename": filename,
            "object_name": object_name,
            "large": large,
        }
        r = self.connection.post(
            f"/api/experiment/{self.id}/artifacts", data=orjson.dumps(payload)
        ).json()
        return Artifact(self.connection, r)

    @exception_handler
    @beartype
    def _create_or_update_file(
        self, name: str, filename: str, object_name: str, large: bool
    ) -> Artifact:
        try:
            stored = self.get_artifact(name)
            stored.update(
                name=name, filename=filename, object_name=object_name, large=large
            )
            return stored
        except exceptions.ResourceNotFoundError:
            return self.create_artifact(
                name=name, filename=filename, object_name=object_name, large=large
            )

    @exception_handler
    @beartype
    def store(
        self, name: str, path: str | Path | None = None, do_zip: bool = False
    ) -> Artifact:
        """Store an artifact and attach it to the experiment.

        Examples:
            ```python
            # Zip and store a folder as an artifact for the experiment
            # you can choose an arbitrary name or refer to our 'namespace'
            # for certain artifacts to have a custom behavior

            trained_model_path = "my_experiment/saved_model"
            experiment.store("model-latest", trained_model_path, do_zip=True)
            ```
        Arguments:
            name (str): name for the artifact. Defaults to "".
            path (str or Path): path to the file or folder. Defaults to None.
            do_zip (bool, optional): Whether to compress the file to a zip file. Defaults to False.

        Raises:
            FileNotFoundException: No file found at the given path

        Returns:
            An (Artifact) object
        """
        if path is None:  # pragma: no cover
            return self.store_local_artifact(name)

        if do_zip:
            path = utils.zip_dir(path)

        filename = os.path.basename(path)
        object_name = self.connection.generate_experiment_object_name(
            filename, ObjectDataType.ARTIFACT, self.id
        )
        _, is_large, _ = self.connection.upload_file(object_name, path)

        return self._create_or_update_file(
            name=name, filename=filename, object_name=object_name, large=is_large
        )

    @exception_handler
    @beartype
    def store_local_artifact(self, name: str) -> Artifact:  # pragma: no cover
        """Store an artifact in platform that is locally stored

        This artifact shall have the name: config, checkpoint-data-latest, checkpoint-index-latest or model-latest

        It will look for special file into current directory.

        Examples:
            ```python
            my_experiment.store_local_artifact("model-latest")
            ```
        Arguments:
            name (str): Name of the artifact to store

        Returns:
            An (Artifact) object
        """
        assert (
            name == "config"
            or name == "checkpoint-data-latest"
            or name == "checkpoint-index-latest"
            or name == "model-latest"
        ), "This name cannot be used to store an artifact"

        if name == "config":
            filename = "pipeline.config"
            path = os.path.join(self.config_dir, filename)
            if not os.path.isfile(path):
                raise FileNotFoundError(f"{path} not found")

        elif name == "checkpoint-data-latest":
            file_list = os.listdir(self.checkpoint_dir)
            ckpt_id = max(
                [int(p.split("-")[1].split(".")[0]) for p in file_list if "index" in p]
            )
            filename = None
            for f in file_list:
                if f"{ckpt_id}.data" in f:
                    filename = f
                    break
            if filename is None:
                raise exceptions.ResourceNotFoundError(
                    "Could not find matching data file with index"
                )
            path = os.path.join(self.checkpoint_dir, filename)

        elif name == "checkpoint-index-latest":
            file_list = os.listdir(self.checkpoint_dir)
            ckpt_id = max(
                [int(p.split("-")[1].split(".")[0]) for p in file_list if "index" in p]
            )
            filename = f"ckpt-{ckpt_id}.index"
            path = os.path.join(self.checkpoint_dir, filename)

        elif name == "model-latest":  # pragma: no cover
            file_path = os.path.join(self.exported_model_dir, "saved_model")
            path = utils.zip_dir(file_path)
            filename = "saved_model.zip"

        else:
            raise RuntimeError("unreachable code")

        object_name = self.connection.generate_experiment_object_name(
            filename, ObjectDataType.ARTIFACT, self.id
        )
        _, is_large, _ = self.connection.upload_file(object_name, path)

        return self._create_or_update_file(
            name=name, filename=filename, object_name=object_name, large=is_large
        )

    @exception_handler
    @beartype
    def get_base_model_version(self) -> ModelVersion:
        """Retrieve the base model version of this experiment.

        Examples:
            ```python
            model_version = experiment.get_base_model_version()
            ```

        Returns:
            A (ModelVersion) object representing the base model.
        """
        r = self.sync()
        if r["base_model_version_id"] is None:
            raise exceptions.NoBaseModelVersionError(
                "There is no base model for this experiment."
            )
        r = self.connection.get(
            f"/api/model/version/{r['base_model_version_id']}"
        ).json()
        return ModelVersion(self.connection, r)

    @exception_handler
    @beartype
    def get_base_experiment(self) -> "Experiment":
        """Retrieve the base experiment of this experiment.

        Examples:
            ```python
            previous = experiment.get_base_experiment()
            ```

        Returns:
            An (Experiment) object representing the base experiment.
        """
        base_experiment_id = self.sync()["base_experiment_id"]
        if not base_experiment_id:
            raise exceptions.NoBaseExperimentError(
                "There is no base experiment for this experiment"
            )
        r = self.connection.get(f"/api/experiment/{base_experiment_id}").json()
        return Experiment(self.connection, r)

    @exception_handler
    @beartype
    def get_artifact(self, name: str) -> Artifact:
        """Retrieve an artifact from its name in this experiment.

        Examples:
            ```python
            model_artifact = experiment.get_artifact("model-latest")
            assert model_artifact.name == "model-latest"
            assert model_artifact.object_name == "d67924a0-7757-48ed-bf7a-322b745e917e/saved_model.zip"
            ```
        Arguments:
            name (str): Name of the artifact to retrieve

        Returns:
            An (Artifact) object
        """
        params = {"name": name}
        r = self.connection.get(
            f"/api/experiment/{self.id}/artifacts/find", params=params
        ).json()
        return Artifact(self.connection, r)

    @exception_handler
    @beartype
    def list_logs(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
    ) -> list:
        """List everything that has been logged.

        List everything that has been logged to an experiment.

        Examples:
            ```python
            logs = experiment.list_logs()
            assert logs[0].type == LogType.Table
            assert logs[0].data == {"batch_size":4, "epochs":1000}
            ```

        Arguments:
            limit (int, optional): limit of logs to retrieve. Defaults to None.
            offset (int, optional): offset to start retrieving logs. Defaults to None.
            order_by (list[str], optional): fields to order by. Defaults to None.

        Returns:
            A list of (Log) objects
        """
        return TrainingService(self.connection, self.id).list_logs(
            limit, offset, order_by
        )

    @exception_handler
    @beartype
    def delete_all_logs(self) -> None:
        """Delete everything that has been logged.

        Delete everything that has been logged into this experiment.

        Examples:
            ```python
            experiment.delete_all_logs()
            ```
        """
        log_ids = self.connection.get(f"/api/experiment/{self.id}/logs/ids").json()
        payload = {"ids": log_ids}
        self.connection.delete(
            f"/api/experiment/{self.id}/logs", data=orjson.dumps(payload)
        )

    @exception_handler
    @beartype
    def get_log(self, name: str) -> Log:
        """Retrieve a log from its name in this experiment.

        Examples:
            ```python
            parameters = experiment.get_log("parameters")
            assert log.parameters == { "batch_size":4, "epochs":1000}
            ```
        Arguments:
            name (str): name of the log to retrieve

        Returns:
            A (Log) object
        """
        return TrainingService(self.connection, self.id).get_log(name)

    @exception_handler
    @beartype
    def log(
        self,
        name: str,
        data: LogDataType,
        type: LogType | str,
        replace: bool = True,
    ) -> Log:
        """Record some data in an experiment.

        It will create a (Log) object, that you can manipulate in SDK.
        All logs are displayed in experiment view on Picsellia.

        If a (Log) with this name already exists, it will be updated unless parameter replace is set to False.

        If it is a LogType LINE and replace is True, then it will append data at the end of stored data.
        If you want to replace a line, delete this log and create another one.


        Examples:
            ```python
            parameters = {
                "batch_size":4,
                "epochs":1000
            }
            exp.log("parameters", parameters, type=LogType.TABLE)
            ```
        Arguments:
            name (str): Name of the log.
            data (Any): Data to be saved.
            type (LogType, optional): Type of the data to log.
                                  This will condition how it is displayed in the experiment dashboard. Defaults to None.
            replace (bool, optional): If true and log already exists and it is not a line, it will replace log data.
                                      Defaults to True.

        Raises:
            Exception: Impossible to upload the file when logging an image.

        Returns:
            A (Log) object
        """
        log_type = LogType.validate(type)

        if log_type == LogType.IMAGE:
            if not replace:
                # Assert log does not exist before pushing image into S3
                try:
                    self.get_log(name=name)
                    raise ResourceConflictError(
                        message="A log image with this name already exists. "
                        "If you want to replace it please give parameter replace=False"
                    )
                except ResourceNotFoundError:
                    pass

            if not isinstance(data, str):
                raise BadRequestError(
                    message="For log image, you need to give a path as data"
                )

            path = data
            filename = os.path.basename(path)
            object_name = self.connection.generate_experiment_object_name(
                filename, ObjectDataType.LOG_IMAGE, self.id
            )
            _, large, _ = self.connection.upload_file(object_name, path)
            data = {
                "object_name": object_name,
                "large": large,
                "filename": filename,
                "name": filename,
            }

        params = {"raise_on_conflict": (not replace)}
        payload = {"name": name, "data": data, "type": log_type.name}
        r = self.connection.post(
            f"/api/experiment/{self.id}/logs", params=params, data=orjson.dumps(payload)
        ).json()
        return Log(self.connection, r)

    @exception_handler
    @beartype
    def log_parameters(self, parameters: dict) -> Log:
        """Record parameters of an experiment into Picsellia.

        If parameters were already setup, it will be replaced.

        Examples:
            ```python
            parameters = {
                "batch_size":4,
                "epochs":1000
            }
            exp.log_parameters(parameters)
            ```
        Arguments:
            parameters (Any): Parameters to be saved.

        Returns:
            A (Log) object
        """
        return self.log("parameters", parameters, type=LogType.TABLE)

    @exception_handler
    @beartype
    def store_logging_file(self, path: str | Path) -> LoggingFile:
        """Store a logging file for this experiment.

        Examples:
            ```python
            experiment.store_logging_file("logs.txt")
            ```
        Arguments:
            path (str or Path): path to the file or folder.

        Raises:
            FileNotFoundException: No file found at the given path

        Returns:
            A (LoggingFile) object
        """
        if not os.path.exists(path):
            raise exceptions.FileNotFoundException(f"{path} not found")

        filename = os.path.basename(path)
        object_name = self.connection.generate_experiment_object_name(
            filename, ObjectDataType.LOGGING, self.id
        )
        _, is_large, _ = self.connection.upload_file(object_name, path)

        payload = {"object_name": object_name}

        r = self.connection.post(
            f"/api/experiment/{self.id}/logging/save",
            data=orjson.dumps(payload),
        ).json()
        return LoggingFile(self.connection, r)

    @exception_handler
    @beartype
    def get_logging_file(self) -> LoggingFile:
        """Retrieve logging file of this experiment.

        Examples:
            ```python
            logging_file = experiment.get_logging_file()
            logging_file.download()
            ```

        Returns:
            A (LoggingFile) object
        """
        r = self.connection.get(f"/api/experiment/{self.id}/logging").json()
        return LoggingFile(self.connection, r)

    @exception_handler
    @beartype
    def send_logging(
        self,
        log: str | list,
        part: str,
        final: bool = False,
        special: str | bool | list = False,
    ) -> None:
        """Send a logging experiment to the experiment.

        Examples:
            ```python
            experiment.send_logging("Hello World", "Hello", final=True)
            ```

        Arguments:
            log (str): Log content
            part (str): Logging Part
            final (bool, optional): True if Final line. Defaults to False.
            special (bool, optional): True if special log. Defaults to False.
        """
        if not hasattr(self, "line_nb"):
            self.line_nb = 0

        to_send = {
            "line_nb": self.line_nb,
            "log": log,
            "final": final,
            "part": part,
            "special": special,
        }
        self.line_nb += 1
        self.connection.post(
            f"/api/experiment/{self.id}/logging",
            data=orjson.dumps(to_send),
        )

    @exception_handler
    @beartype
    def start_logging_chapter(self, name: str) -> None:
        """Print a log entry to the log.

        Examples:
            ```python
            experiment.start_logging_chapter("Training")
            ```

        Arguments:
            name (str): Chapter name
        """
        utils.print_start_chapter_name(name)
        utils.print_line_return()

    @exception_handler
    @beartype
    def start_logging_buffer(self, length: int = 1) -> None:
        """Start logging buffer.

        Examples:
            ```python
            experiment.start_logging_buffer()
            ```

        Arguments:
            length (int, optional): Buffer length. Defaults to 1.
        """
        utils.print_logging_buffer(length)
        self.buffer_length = length

    @exception_handler
    @beartype
    def end_logging_buffer(self) -> None:
        """End the logging buffer.

        Examples:
            ```python
            experiment.end_logging_buffer()
            ```
        """
        utils.print_logging_buffer(self.buffer_length)

    @exception_handler
    @beartype
    def update_job_status(self, status: JobStatus | str) -> None:
        """Update the job status of this experiment.

        Examples:
            ```python
            experiment.update_job_status(JobStatus.FAILED)
            ```

        Arguments:
            status (JobStatus): Status to send
        """
        to_send = {
            "status": JobStatus.validate(status),
        }
        self.connection.patch(
            f"/api/experiment/{self.id}/job/status",
            data=orjson.dumps(to_send),
        )

    @exception_handler
    @beartype
    def export_as_model(self, name: str) -> ModelVersion:
        """Publish an Experiment as a ModelVersion to your registry.
           A Model with given name will be created, and its first version will be the exported experiment

        Examples:
            ```python
            model_version = experiment.export_as_model("awesome-model")
            ```
        Arguments:
            name (str): Target Name for the model in the registry.

        Returns:
            A (ModelVersion) just created from the experiment
        """
        payload = {"name": name}
        r = self.connection.post(
            f"/api/experiment/{self.id}/publish", data=orjson.dumps(payload)
        ).json()
        model_version = ModelVersion(self.connection, r)
        logger.info(f"Experiment published as {model_version}")
        return model_version

    @exception_handler
    @beartype
    def export_in_existing_model(self, existing_model: Model) -> ModelVersion:
        """Publish an Experiment as a (ModelVersion) of given already existing (Model)

        Examples:
            ```python
            my_model = client.get_model("foo_model")
            model_version = experiment.export_in_existing_model(my_model)
            ```
        Arguments:
            existing_model ((Model)): Model in the registry were this experiment should be exported.

        Returns:
            A (ModelVersion) just created from the experiment
        """
        payload = {"model_id": existing_model.id}
        r = self.connection.post(
            f"/api/experiment/{self.id}/publish/version", data=orjson.dumps(payload)
        ).json()
        model_version = ModelVersion(self.connection, r)
        logger.info(f"Experiment published as {model_version} in {existing_model}")
        return model_version

    @exception_handler
    @beartype
    def launch(self, gpus: int = 1) -> Job:
        """Launch a job on a remote environment with this experiment.

        :information-source: The remote environment has to be setup prior launching the experiment.
        It defaults to our remote training engine.

        Examples:
            ```python
            experiment.launch()
            ```
        Arguments:
            gpus (int, optional): Number of GPU to use for the training. Defaults to 1.
        """
        payload = {
            "gpus": gpus,
        }

        r = self.connection.post(
            f"/api/experiment/{self.id}/launch", data=orjson.dumps(payload)
        ).json()
        logger.info("Job launched successfully")
        return Job(self.connection, r, 2)

    def _setup_dirs(self):
        """Create the directories for the project."""
        if not os.path.isdir(self.name):
            logger.debug(
                "No directory for this project has been found, creating directory and sub-directories..."
            )
            os.mkdir(self.name)

        self._create_dir(self.base_dir)
        self._create_dir(self.png_dir)
        self._create_dir(self.checkpoint_dir)
        self._create_dir(self.metrics_dir)
        self._create_dir(self.record_dir)
        self._create_dir(self.config_dir)
        self._create_dir(self.results_dir)
        self._create_dir(self.exported_model_dir)

    @exception_handler
    @beartype
    def _create_dir(self, dir_name: str) -> None:
        """Create a directory if it does not exist.

        Arguments:
            dir_name (str): [directory name]
        """
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)

    @exception_handler
    @beartype
    def download_artifacts(self, with_tree: bool):
        """
        Download all artifacts from the experiment to the local directory.

        Examples:
            ```python
            experiment.download_artifacts(with_tree=True)
            ```

        Arguments:
            with_tree: If True, the artifacts will be downloaded in a tree structure.

        """
        if with_tree:
            self._setup_dirs()
            self._download_artifacts_with_tree_for_experiment()
        else:
            self._download_artifacts_without_tree_for_experiment()

    @exception_handler
    @beartype
    def _download_artifacts_with_tree_for_experiment(self):
        for artifact in self.list_artifacts():
            if artifact.name == "checkpoint-data-latest":  # pragma: no cover
                target_path = self.checkpoint_dir
            elif artifact.name == "checkpoint-index-latest":  # pragma: no cover
                target_path = self.checkpoint_dir
            elif artifact.name == "model-latest":  # pragma: no cover
                target_path = self.exported_model_dir
            elif artifact.name == "config":  # pragma: no cover
                target_path = self.config_dir
            else:
                target_path = self.base_dir

            artifact.download(target_path=target_path, force_replace=True)

    @exception_handler
    @beartype
    def _download_artifacts_without_tree_for_experiment(self):
        self._create_dir(self.base_dir)
        for artifact in self.list_artifacts():
            artifact.download(target_path=self.base_dir, force_replace=True)

    @exception_handler
    @beartype
    def set_base_experiment(self, base_experiment: "Experiment") -> None:
        """Set a base experiment to this experiment. Experiment must not be the same, and must be in the same project.

        If no "parameters" Log exists on this experiment, it will copy the base_experiment "parameters" (Log).
        If no "labelmap" Log exists on this experiment, it will copy the base_experiment "labelmap" (Log).
        If there are no Artifacts stored for this experiment, it will copy all the base_experiment (Artifact)
        If no base_model_version is set on this experiment, it will set the reference to base_experiment.model_version.

        Examples:
            ```python
            base_experiment = client.get_experiment_by_id("7b838580-fa66-4faa-bbc7-23cb70421fbd")
            my_experiment.set_base_experiment(base_experiment)
            ```
        Arguments:
            base_experiment (Experiment): An experiment to set as base experiment.
        """
        payload = {"base_experiment_id": base_experiment.id}
        self.connection.post(
            f"/api/experiment/{self.id}/experiment", data=orjson.dumps(payload)
        )
        logger.info(f"{base_experiment} successfully set as base experiment to {self}")

    @exception_handler
    @beartype
    def set_base_model_version(
        self,
        base_model_version: "ModelVersion",
        attach_parameters: bool | None = None,
    ) -> None:
        """Set a base experiment to this experiment.

        If no "labelmap" Log exists on this experiment, it will copy the base_model_version "labelmap" (Log).
        If there are no Artifacts stored for this experiment, it will copy all the base_model_version (ModelFile)

        If attach_parameters is True, it will copy the base_model_version parameters inside a "parameters" Log.
        If attach_parameters is False, it will do nothing for parameters.
        If attach_parameters is None, it will copy the base_model_version parameters inside a "parameters" Log ONLY if there was no prior "parameters" Log on this experiment.

        Examples:
            ```python
            base_model_version = client.get_model_version_by_id("f91c4f26-e956-4a4f-ac75-d8371cf9928c")
            # This will copy parameters only if there were no parameters inside experiment.
            experiment.set_base_model_version(base_model_version)
            ```
        Arguments:
            base_model_version (ModelVersion): A model version to set as base model_version.
            attach_parameters (bool, optional): Define the behavior for parameters. Defaults to None.
        """
        payload = {
            "model_version_id": base_model_version.id,
            "do_attach_base_parameters": attach_parameters,
        }
        self.connection.post(
            f"/api/experiment/{self.id}/model", data=orjson.dumps(payload)
        )
        logger.info(
            f"{base_model_version} successfully set as base model version to {self}"
        )

    @exception_handler
    @beartype
    @deprecated(
        deprecated_in="6.29.0",
        removed_in="7.0.0",
        details="This method should not be called anymore. Instead use set_base_model_version()",
    )
    def attach_model_version(
        self, model_version: ModelVersion, do_attach_base_parameters: bool = True
    ) -> None:
        """Be careful, this method is deprecated and will override base parameters of experiment if do_attach_base_parameters is not given"""
        return self.set_base_model_version(model_version, do_attach_base_parameters)

    @exception_handler
    @beartype
    def attach_dataset(self, name: str, dataset_version: DatasetVersion) -> None:
        """Attach a dataset version to this experiment.

        Retrieve or create a dataset version and attach it to this experiment.

        Examples:
            ```python
            foo_dataset = client.get_dataset("foo").get_version("first")
            my_experiment.attach_dataset("training", foo_dataset)
            ```
        Arguments:
            name (str): Name to label this attached dataset. Use it like a descriptor of the attachment.
            dataset_version (DatasetVersion): A dataset version to attach to the experiment.
        """
        payload = {"name": name, "dataset_version_id": dataset_version.id}
        self.connection.post(
            f"/api/experiment/{self.id}/datasets", data=orjson.dumps(payload)
        )
        logger.info(f"{dataset_version} successfully attached to {self}")

    @exception_handler
    @beartype
    def detach_dataset(self, dataset_version: DatasetVersion) -> None:
        """Detach a dataset version from this experiment.

        Examples:
            ```python
            foo_dataset = client.get_dataset("foo").get_version("first")
            my_experiment.attach_dataset(foo_dataset)
            my_experiment.detach_dataset(foo_dataset)
            ```
        Arguments:
            dataset_version (DatasetVersion): A dataset version to attach to the experiment.
        """
        payload = {"ids": [dataset_version.id]}
        self.connection.delete(
            f"/api/experiment/{self.id}/datasets", data=orjson.dumps(payload)
        )
        logger.info(f"{dataset_version} was successfully detached from {self}")

    @exception_handler
    @beartype
    @deprecated(
        deprecated_in="6.27.0",
        details="get_attached_dataset_versions can be used instead of this endpoint",
    )
    def list_attached_dataset_versions(self) -> list[DatasetVersion]:
        """Retrieve all dataset versions attached to this experiment

        Examples:
            ```python
            datasets = my_experiment.list_attached_dataset_versions()
            ```

        Returns:
            A list of (DatasetVersion) object attached to this experiment
        """
        return list(self.get_attached_dataset_versions().values())

    @exception_handler
    @beartype
    def get_attached_dataset_versions(self) -> dict[str, DatasetVersion]:
        """Retrieve all dataset versions attached to this experiment, in a dict where keys are aliases

        Examples:
            ```python
            datasets = my_experiment.get_attached_dataset_versions()
            ```

        Returns:
            A dict matching alias and (DatasetVersion) object attached to this experiment
        """
        r = self.connection.get(f"/api/experiment/{self.id}/datasets").json()
        return {
            item["name"]: DatasetVersion(self.connection, item["dataset_version"])
            for item in r["items"]
        }

    @exception_handler
    @beartype
    def get_dataset(self, name: str) -> DatasetVersion:
        """Retrieve the dataset version attached to this experiment with given name

        Examples:
            ```python
            dataset: Dataset = my_experiment.get_dataset('train')
            dataset_version: DatasetVersion = dataset.get_version("latest")
            pics = dataset.list_assets()
            annotations = dataset.list_annotations()
            ```

        Arguments:
            name (str): Name of the dataset version in the experiment

        Returns:
            A (DatasetVersion) object attached to this experiment
        """
        params = {"name": name}
        r = self.connection.get(
            f"/api/experiment/{self.id}/datasets/find", params=params
        ).json()
        return DatasetVersion(self.connection, r["dataset_version"])

    @exception_handler
    @beartype
    def run_train_test_split_on_dataset(
        self, name: str, prop: float = 0.8, random_seed: Any | None = None
    ) -> tuple[MultiAsset, MultiAsset, dict[str, list], dict[str, list], list[Label]]:
        """Run a train test split on a dataset attached to this experiment.

        Examples:
            ```python
            dataset: DatasetVersion = my_experiment.get_dataset('train')
            pics = dataset.list_assets()
            annotations = dataset.list_annotations()
            ```

        Arguments:
            name (str): Name of the dataset version in the experiment
            prop (float): Proportion of the dataset to use for training
            random_seed (int): Random seed to use for the split

        Returns:
            A tuple containing:
                - train_assets (MultiAsset): assets to use for training
                - eval_assets (MultiAsset): assets to use for evaluation
                - train_label_count (dict): number of assets per label in train set
                - eval_label_count (dict): number of assets per label in eval set
                - labels (list[Label]): list of labels in the dataset
        """
        dataset = self.get_dataset(name)
        (
            train_assets,
            eval_assets,
            train_label_count,
            eval_label_count,
            labels,
        ) = dataset.train_test_split(prop, random_seed)
        # TODO: Log those values
        return train_assets, eval_assets, train_label_count, eval_label_count, labels

    @exception_handler
    @beartype
    def add_evaluation(
        self,
        asset: Asset,
        add_type: str | AddEvaluationType = AddEvaluationType.REPLACE,
        rectangles: list[tuple[int, int, int, int, Label, float]] | None = None,
        polygons: list[tuple[list[list[int]], Label, float]] | None = None,
        classifications: list[tuple[Label, float]] | None = None,
        keypoints: list[tuple[list[list[int]], Label, float]] | None = None,
    ):
        """Add an evaluation of the asset by this experiment.

        By default, if given asset had already been evaluated, evaluation will be replaced.
        You can add different shapes but will only be able to compute evaluation metrics on one kind of inference type.

        Examples:
            ```python
            asset = dataset_version.find_asset(filename="asset-1.png")
            experiment.add_evaluation(asset, rectangles=[(10, 20, 30, 40, label_cat, 0.8), (50, 60, 20, 30, label_dog, 0.7)])
            job = experiment.compute_evaluations_metrics(InferenceType.OBJECT_DETECTION)
            job.wait_for_done()
            ```
        Arguments:
            asset (Asset): asset to add evaluation on
            add_type (str ou AddEvaluationType): replace or keep old evaluation, defaults to
            rectangles (optional): list of tuples representing rectangles with scores
            polygons  (optional): list of tuples representing polygons with scores
            classifications (optional): list of tuples representing classifications with scores
            keypoints (optional): list of tuples representing keypoints with scores
        """
        if (
            rectangles is None
            and classifications is None
            and polygons is None
            and keypoints is None
        ):
            raise ValueError(
                "Please give parameter 'rectangles', 'classifications', 'keypoints' or 'polygons'"
            )

        import_type = AddEvaluationType.validate(add_type)
        payload = {"import_type": import_type}
        payload_evaluation: dict[str, Any] = {"asset_id": asset.id}
        if rectangles is not None:
            payload_evaluation["rectangles"] = [
                {
                    "x": rectangle[0],
                    "y": rectangle[1],
                    "w": rectangle[2],
                    "h": rectangle[3],
                    "label_id": rectangle[4].id,
                    "score": rectangle[5],
                }
                for rectangle in rectangles
            ]

        if polygons is not None:
            payload_evaluation["polygons"] = [
                {"polygon": polygon[0], "label_id": polygon[1].id, "score": polygon[2]}
                for polygon in polygons
            ]
        if classifications is not None:
            payload_evaluation["classifications"] = [
                {"label_id": classification[0].id, "score": classification[1]}
                for classification in classifications
            ]
        if keypoints is not None:
            payload_evaluation["keypoints"] = [
                {
                    "keypoints": keypoint[0],
                    "label_id": keypoint[1].id,
                    "score": keypoint[2],
                }
                for keypoint in keypoints
            ]
        payload["evaluations"] = [payload_evaluation]

        self.connection.post(
            f"/api/experiment/{self.id}/evaluations", data=orjson.dumps(payload)
        )

    @exception_handler
    @beartype
    def list_evaluations(
        self,
        limit: int | None = None,
        offset: int | None = None,
        page_size: int | None = None,
        order_by: list[str] | None = None,
        q: str | None = None,
    ) -> MultiEvaluation:
        """List evaluations of this experiment.
        It will retrieve all evaluations made by this experiment.
        You will then be able to manipulate them.

         Arguments:
            limit (int, optional): if given, will limit the number of evaluations returned
            offset (int, optional): if given, will return evaluations that would have been returned
                                    after this offset in given order
            page_size (int, optional): page size when returning evaluations paginated, can change performance
            order_by (list[str], optional): if not empty, will order evaluations by fields given in this parameter
            q (str, optional): if given, will try to apply query to filter evaluations

        Returns:
            A (MultiEvaluation)
        """
        if page_size:
            logger.warning("page_size is deprecated and not used anymore.")
        return TrainingService(self.connection, self.id).list_evaluations(
            limit, offset, order_by, q
        )

    @exception_handler
    @beartype
    def compute_evaluations_metrics(
        self,
        inference_type: InferenceType,
        evaluations: (
            list[str | UUID] | list[Evaluation] | MultiEvaluation | None
        ) = None,
        worker: Worker | None = None,
        status: AnnotationStatus | None = None,
    ) -> Job:
        """Compute evaluation metrics across evaluations added to this experiment.
        Picsellia will compute coco metrics on each evaluation and compare to existing annotations.

        Workers parameter is deprecated and cannot be used anymore. It will be removed in 6.27

        Examples:
            ```python
            experiment.add_evaluation(rectangles=[(10, 20, 30, 40, label_cat, 0.8), (50, 60, 20, 30, label_dog, 0.7)])
            experiment.compute_evaluations_metrics(InferenceType.OBJECT_DETECTION)
            ```

        Arguments
            inference_type (InferenceType): Type of shapes pushed as evaluations.
            evaluations (MultiEvaluation or list of UUID or Evaluation, optional): Run coco evaluation on only given ids
            status (AnnotationStatus, optional): Existing annotations will be filtered to only retrieve those that have this status.

        Returns:
            A (Job) that you can wait for done.
        """

        payload = {"inference_type": inference_type}

        if evaluations:
            evaluation_ids = []
            for evaluation in evaluations:
                if isinstance(evaluation, Evaluation):
                    evaluation_ids.append(evaluation.id)
                else:
                    evaluation_ids.append(evaluation)

            payload["evaluation_ids"] = evaluation_ids

        if worker:
            logger.warning("worker is deprecated and should not be used anymore.")

        if status:
            payload["status"] = status

        r = self.connection.post(
            f"/api/experiment/{self.id}/evaluate", data=orjson.dumps(payload)
        ).json()
        return Job(self.connection, r, version=1)
