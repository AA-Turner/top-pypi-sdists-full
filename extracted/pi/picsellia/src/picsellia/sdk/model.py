import logging

import orjson
from beartype import beartype

import picsellia.utils as utils
from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.model_version import ModelVersion
from picsellia.sdk.tag import Tag, TagTarget
from picsellia.sdk.taggable import Taggable
from picsellia.types.enums import Framework, InferenceType
from picsellia.types.schemas import ModelSchema

logger = logging.getLogger("picsellia")


class Model(Dao, Taggable):
    def __init__(self, connexion: Connection, data: dict):
        Dao.__init__(self, connexion, data)
        Taggable.__init__(self, TagTarget.MODEL)

    @property
    def name(self) -> str:
        """Name of this (Model)"""
        return self._name

    @property
    def private(self) -> bool:
        """Privacy of this (Model)"""
        return self._private

    def __str__(self):
        is_private = "" if self._private else "[PUBLIC]"
        return f"{Colors.BLUE}{is_private} Model '{self.name}' {Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def get_resource_url_on_platform(self) -> str:
        """Get platform url of this resource.

        Examples:
            ```python
            print(model.get_resource_url_on_platform())
            >>> "https://app.picsellia.com/model/62cffb84-b92c-450c-bc37-8c4dd4d0f590"
            ```

        Returns:
            Url on Platform for this resource
        """

        return f"{self.connection.host}/model/{self.id}"

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/model/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def refresh(self, data: dict):
        schema = ModelSchema(**data)
        self._name = schema.name
        self._private = schema.private
        return schema

    @exception_handler
    @beartype
    def update(
        self,
        name: str | None = None,
        framework: str | Framework | None = None,
        private: bool | None = None,
        description: str | None = None,
        type: str | InferenceType | None = None,
    ) -> None:
        """Update a model with a new name, framework, privacy, description or type

        Examples:
            ```python
            model.update(description="Very cool model")
            ```

        Arguments:
            name (str): New name of the model
            framework (str, Framework): New framework of the model
            private (bool): New privacy of the model
            description (str): New description of the model
            type (str, InferenceType): New type of the model
        """
        if type:
            logging.warning(
                "'type' parameter is deprecated and will be removed in future versions. "
                "If you want to give a type to your model version, call update() on ModelVersion."
            )

        if framework:
            logging.warning(
                "'framework' parameter is deprecated and will be removed in future versions. "
                "If you want to give a framework to your model version, call update() on your ModelVersion."
            )

        if private is not None:
            logging.warning(
                "'private' parameter is deprecated and will be removed in future versions. "
                "You cannot update privacy of a model anymore."
            )

        payload = {
            "name": name,
            "description": description,
        }
        filtered_payload = utils.filter_payload(payload)
        r = self.connection.patch(
            f"/api/model/{self.id}", data=orjson.dumps(filtered_payload)
        ).json()
        self.refresh(r)
        logger.info(f"{self} updated.")

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete model.

        Delete the model in Picsellia database

        Examples:
            ```python
            model.delete()
            ```
        """
        self.connection.delete(f"/api/model/{self.id}")
        logger.info(f"{self} deleted.")

    @exception_handler
    @beartype
    def get_tags(self) -> list[Tag]:
        """Retrieve the tags of your model.

        Examples:
            ```python
            tags = my_model.get_tags()
            assert tags[0].name == "my-model-1"
            ```

        Returns:
            A list of (Tag) object
        """
        r = self.sync()
        return [Tag(self.connection, item) for item in r["tags"]]

    @exception_handler
    @beartype
    def create_version(
        self,
        docker_image_name: str | None = None,
        docker_flags: list[str] | None = None,
        thumb_object_name: str | None = None,
        notebook_link: str | None = None,
        labels: dict | None = None,
        base_parameters: dict | None = None,
        docker_env_variables: dict | None = None,
        name: str | None = None,
        framework: str | Framework | None = None,
        type: str | InferenceType | None = None,
        description: str | None = None,
        docker_tag: str | None = None,
    ) -> ModelVersion:
        """Create a version of a model.

        The version number of this model will be defined by the platform. It is incremented automatically.

        Examples:
            ```python
            model_v0 = model.create_version(labels={"1": "cat", "2": "dog"}, framework=Framework.TENSORFLOW, type=InferenceType.OBJECT_DETECTION)
            ```

        Arguments:
            docker_image_name (str, optional): Docker image name of this version. Defaults to None.
            docker_flags (list[str], optional): Docker flags of this version. Defaults to None.
            thumb_object_name (str, optional): Thumbnail object name of this version. Defaults to None.
            notebook_link (str, optional): Notebook link of this version. Defaults to None.
            labels (dict, optional): Labels of this version. Defaults to None.
            base_parameters (dict, optional): Base parameters of this version. Defaults to None.
            docker_env_variables (dict, optional): Docker environment variables of this version. Defaults to None.
            name (str, optional): Name of this version. Defaults to None.
            framework (str, Framework, optional): Framework of this version (tensorflow, pytorch, etc.). Defaults to None.
            type (str, InferenceType, optional): Type of this version (classification, object_detection, segmentation). Defaults to None.
            description (str, optional): Description of this version. Defaults to None.
            docker_tag (str, optional): Docker tag of this version. Defaults to None.

        Returns:
            A (ModelVersion) object
        """
        if framework:
            framework = Framework.validate(framework)

        if type:
            type = InferenceType.validate(type)

        if type and type not in [
            InferenceType.CLASSIFICATION,
            InferenceType.OBJECT_DETECTION,
            InferenceType.SEGMENTATION,
            InferenceType.LINE,
            InferenceType.POINT,
            InferenceType.KEYPOINT,
        ]:
            raise TypeError(f"Type '{type}' not supported yet for model version")

        payload = {
            "name": name,
            "type": type,
            "framework": framework,
            "docker_image": docker_image_name,
            "docker_flags": docker_flags,
            "thumbnail_object_name": thumb_object_name,
            "notebook_link": notebook_link,
            "labels": labels,
            "parameters": base_parameters,
            "docker_env_variables": docker_env_variables,
            "description": description,
            "docker_tag": docker_tag,
        }
        filtered_payload = utils.filter_payload(payload)
        r = self.connection.post(
            f"/api/model/{self.id}/versions",
            data=orjson.dumps(filtered_payload),
        ).json()
        return ModelVersion(self.connection, r)

    @exception_handler
    @beartype
    def get_version(self, version: int | str) -> ModelVersion:
        """Retrieve a version of a model from its version or its name

        Examples:
            ```python
            # Assuming model is a Model without version
            model_version_a = model.create_version("first-version")
            model_version_b = model.get_version(0)
            model_version_c = model.get_version("first-version")
            assert model_version_a == model_version_b
            assert model_version_a == model_version_c
            ```

        Arguments:
            version (int, str): Version number or name of the version

        Returns:
            A (ModelVersion) object
        """
        if isinstance(version, str):
            params = {"name": version}
        else:
            params = {"version": version}
        r = self.connection.get(
            f"/api/model/{self.id}/versions/find", params=params
        ).json()
        return ModelVersion(self.connection, r)

    @exception_handler
    @beartype
    def list_versions(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
    ) -> list[ModelVersion]:
        """List versions of this model.

        Examples:
            ```python
            versions = model.list_versions()
            ```

        Arguments:
            limit (int, optional): Limit of versions to retrieve. Defaults to None.
            offset (int, optional): Offset to start retrieving versions. Defaults to None.
            order_by (list[str], optional): fields to order by. Defaults to None.

        Returns:
            A list of (ModelVersion) object of this model
        """
        params = {"limit": limit, "offset": offset, "order_by": order_by}
        params = utils.filter_payload(params)
        r = self.connection.get(f"/api/model/{self.id}/versions", params=params).json()
        return [ModelVersion(self.connection, item) for item in r["items"]]
