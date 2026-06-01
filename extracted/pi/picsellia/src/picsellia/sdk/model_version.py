import logging
import os
from pathlib import Path
from uuid import UUID

import orjson
from beartype import beartype

import picsellia.exceptions as exceptions
import picsellia.utils as utils
from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.datalake import Datalake
from picsellia.sdk.job import Job
from picsellia.sdk.model_context import ModelContext
from picsellia.sdk.model_file import ModelFile
from picsellia.sdk.processing import Processing
from picsellia.sdk.tag import Tag, TagTarget
from picsellia.sdk.taggable import Taggable
from picsellia.types.enums import Framework, InferenceType, ObjectDataType
from picsellia.types.schemas import ModelVersionSchema

logger = logging.getLogger("picsellia")


class ModelVersion(Dao, Taggable):
    def __init__(self, connexion: Connection, data: dict):
        Dao.__init__(self, connexion, data)
        Taggable.__init__(self, TagTarget.MODEL_VERSION)

    @property
    def origin_name(self) -> str:
        """Name of origin of this (ModelVersion)"""
        return self._origin_name

    @property
    def origin_id(self) -> UUID:
        """UUID of the origin (Model) of this (ModelVersion)"""
        return self._origin_id

    @property
    def name(self) -> str:
        """Name of this (ModelVersion)"""
        return self._name

    @property
    def version(self) -> int:
        """Version number of this (ModelVersion)"""
        return self._version

    @property
    def type(self) -> InferenceType:
        """Type of this (ModelVersion)"""
        return self._type

    @property
    def framework(self) -> Framework:
        """Framework of this (ModelVersion)"""
        return self._framework

    @property
    def labels(self) -> dict | None:
        return self._labels

    def __str__(self):
        return f"{Colors.BLUE}Version {self.name} of Model '{self.origin_name}' with type {self.type.name} and framework {self.framework.name} {Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def get_resource_url_on_platform(self) -> str:
        """Get platform url of this resource.

        Examples:
            ```python
            print(model_version.get_resource_url_on_platform())
            >>> "https://app.picsellia.com/model/62cffb84-b92c-450c-bc37-8c4dd4d0f590"
            ```

        Returns:
            Url on Platform for this resource
        """

        return f"{self.connection.host}/model/version/{self.id}"

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/model/version/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> ModelVersionSchema:
        schema = ModelVersionSchema(**data)
        self._origin_name = schema.origin.name
        self._origin_id = schema.origin.id
        self._version = schema.version
        self._name = schema.name
        self._type = schema.type
        self._framework = schema.framework
        self._labels = schema.labels
        return schema

    @exception_handler
    @beartype
    def get_tags(self) -> list[Tag]:
        """Retrieve the tags of your model version.

        Examples:
            ```python
            tags = my_model_version.get_tags()
            assert tags[0].name == "my-model-version-1"
            ```

        Returns:
            A list of (Tag) objects
        """
        r = self.sync()
        return [Tag(self.connection, item) for item in r["tags"]]

    @exception_handler
    @beartype
    def update(
        self,
        labels: dict | None = None,
        docker_image_name: str | None = None,
        docker_flags: list[str] | None = None,
        thumb_object_name: str | None = None,
        notebook_link: str | None = None,
        base_parameters: dict | None = None,
        docker_env_variables: dict | None = None,
        framework: str | Framework | None = None,
        type: str | InferenceType | None = None,
        name: str | None = None,
        description: str | None = None,
        docker_tag: str | None = None,
    ) -> None:
        """Update this model version with some new infos.

        Examples:
            ```python
            model_v1.update(docker_image_name="docker.io/model1")
            ```

        Arguments:
            labels (dict, optional): Labels of this model version. Defaults to None.
            docker_image_name (str, optional): Docker image name of this model version. Defaults to None.
            docker_flags (list[str], optional): Docker flags of this model version. Defaults to None.
            thumb_object_name (str, optional): Thumbnail object name of this model version. Defaults to None.
            notebook_link (str, optional): Notebook link of this model version. Defaults to None.
            base_parameters (dict, optional): Base parameters of this model version. Defaults to None.
            docker_env_variables (dict, optional): Docker env variables of this model version. Defaults to None.
            framework (str or Framework, optional): Framework of this model version (tensorflow, pytorch, etc.). Defaults to None.
            type (str or InferenceType, optional): Type of this model version (classification, object_detection, segmentation). Defaults to None.
            name (str, optional): Name of this model version. Defaults to None.
            description (str, optional): Description of this model version. Defaults to None.
            docker_tag (str, optional): Docker tag of this model version. Defaults to None.
        """
        if framework:
            framework = Framework.validate(framework)

        if type:
            type = InferenceType.validate(type)

        if type and type not in [
            InferenceType.CLASSIFICATION,
            InferenceType.OBJECT_DETECTION,
            InferenceType.SEGMENTATION,
            InferenceType.KEYPOINT,
            InferenceType.POINT,
            InferenceType.LINE,
        ]:
            raise TypeError(f"Type '{type}' not supported yet for model version")

        payload = {
            "labels": labels,
            "docker_image": docker_image_name,
            "docker_flags": docker_flags,
            "thumbnail_object_name": thumb_object_name,
            "notebook_link": notebook_link,
            "parameters": base_parameters,
            "docker_env_variables": docker_env_variables,
            "type": type,
            "framework": framework,
            "name": name,
            "description": description,
            "docker_tag": docker_tag,
        }
        filtered_payload = utils.filter_payload(payload)
        r = self.connection.patch(
            f"/api/model/version/{self.id}",
            data=orjson.dumps(filtered_payload),
        ).json()
        self.refresh(r)

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete model version.

        Delete the model in Picsellia database

        Examples:
            ```python
            model_v1.delete()
            ```
        """
        self.connection.delete(f"/api/model/version/{self.id}")
        logger.info(f"{self} deleted.")

    @exception_handler
    @beartype
    def get_context(self) -> ModelContext:
        """Get ModelContext of this model

        Examples:
            ```python
            model_v1 = client.get_model(name="my-model").get_version(0)
            context = model_v1.get_context()
            context.get_infos()
            ```

        Returns:
            ModelContext objects that you can use and manipulate
        """
        try:
            r = self.connection.get(f"/api/model/version/{self.id}/context").json()
        except exceptions.ForbiddenError:
            r = self.connection.get(
                f"/api/model/version/{self.id}/public/context"
            ).json()

        return ModelContext(self.connection, r)

    @exception_handler
    @beartype
    def list_files(self) -> list[ModelFile]:
        """Get a list of ModelFile that were stored with this model

        Examples:
            ```python
            model_v1 = client.get_model(name="my-model").get_version(0)
            files = model_v1.list_files()
            files[0].download()
            ```

        Returns:
            A list of (ModelFile) that you can use and manipulate
        """
        r = self.connection.get(f"/api/model/version/{self.id}/modelfiles").json()
        return [ModelFile(self.connection, item) for item in r["items"]]

    @exception_handler
    @beartype
    def get_file(self, name: str) -> ModelFile:
        """Retrieve a ModelFile that were stored with this name into this model

        Examples:
            ```python
            model_v1 = client.get_model(name="my-model").get_version(0)
            file = model_v1.get_file("model-latest")
            file.download()
            ```

        Arguments:
            name (str): Name of the file you want to retrieve

        Returns:
            A (ModelFile) that you can use and manipulate
        """
        params = {"name": name}
        r = self.connection.get(
            f"/api/model/version/{self.id}/modelfiles/find", params=params
        ).json()
        return ModelFile(self.connection, r)

    @exception_handler
    @beartype
    def store(
        self,
        name: str,
        path: str | Path,
        do_zip: bool = False,
        replace: bool = False,
    ) -> ModelFile:
        """Store a file into picsellia storage and attach it to this model.

        Examples:
            ```python
            model.store("model-latest", "./lg_test_file.pb")
            ```
        Arguments:
            name (str): Name of file
            path (str or Path): Path of file to store
            do_zip (bool, optional): If true, zip directory to store it. Defaults to False.
            replace (bool, optional): If true, if a file with given name exists, it will be replaced. Defaults to False.

        Returns:
            A (ModelFile) object
        """
        if not os.path.exists(path):
            raise exceptions.FileNotFoundException(f"{path} not found")

        if do_zip:
            path = utils.zip_dir(path)

        filename = os.path.basename(path)
        object_name = self.connection.generate_model_version_object_name(
            filename, ObjectDataType.MODEL_FILE, self.id
        )
        _, is_large, _ = self.connection.upload_file(object_name, path)

        # Replacing file
        if replace:
            try:
                model_file = self.get_file(name)
                model_file.delete()
            except exceptions.ResourceNotFoundError:
                logger.debug(f"Model file `{name}` did not exist yet.")

        payload = {
            "name": name,
            "filename": filename,
            "object_name": object_name,
            "large": is_large,
        }
        r = self.connection.post(
            f"/api/model/version/{self.id}/modelfiles",
            data=orjson.dumps(payload),
        ).json()
        model_file = ModelFile(self.connection, r)
        logger.info(f"{model_file} stored for {self}")
        return model_file

    @exception_handler
    @beartype
    def deploy(
        self,
        name: str | None = None,
        target_datalake: Datalake | None = None,
        min_threshold: float | None = None,
    ):
        """Create a (Deployment) for a model.

        This method allows you to create a (Deployment) on Picsellia. You will then have
        access to the monitoring dashboard and the model management part!

        Examples:
            ```python
            model_version = client.get_model(name="my-awesome-model").get_version(0)
            deployment = model_version.deploy(name="my-awesome-deployment", min_threshold=0.5)
            ```

        Arguments:
            name (str): Name of your deployment. Defaults to a random name.
            min_threshold (float): Threshold of detection scores used by models when predicting. Defaults to 0.
            target_datalake (Datalake): Datalake to use when data are pushed into Picsellia.
                Defaults to organization default Datalake.


        Returns:
            A (Deployment)
        """
        from picsellia.sdk.deployment import Deployment

        payload = {
            "name": name,
            "min_threshold": min_threshold,
        }
        if target_datalake is not None:
            payload["target_datalake_id"] = target_datalake.id
        filtered_payload = utils.filter_payload(payload)
        r = self.connection.post(
            f"/api/model/version/{self.id}/deploy",
            data=orjson.dumps(filtered_payload),
        ).json()
        deployment = Deployment(self.connection, r)
        logger.info(f"{deployment} created")
        return deployment

    @exception_handler
    @beartype
    def launch_processing(
        self,
        processing: Processing,
        parameters: dict = None,
        cpu: int = None,
        gpu: int = None,
        inputs: dict | None = None,
    ) -> Job:
        """Launch given processing onto this model version. You can give specific cpu, gpu or parameters.

        You must set the "inputs" dict so it matches the inputs configuration defined in the platform.
        It will fail if inputs are not matching expected inputs.

        If not given, it will use default values specified in Processing.
        If processing cannot be launched on a ModelVersion it will raise before launching.

        Examples:
            ```python
            processing = client.get_processing("convert-to-pytorch")
            model_version.launch_processing(processing)
            ```

        Returns:
            A (Job) object
        """
        inputs = inputs or {}
        payload = {
            "processing_id": processing.id,
            "parameters": parameters,
            "cpu": cpu,
            "gpu": gpu,
            "inputs": inputs,
        }
        r = self.connection.post(
            f"/api/model/version/{self.id}/processing/launch",
            data=orjson.dumps(payload),
        ).json()
        return Job(self.connection, r, version=2)
