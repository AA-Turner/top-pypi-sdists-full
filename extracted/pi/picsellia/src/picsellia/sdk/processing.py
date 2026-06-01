import logging

import orjson
from beartype import beartype
from deprecation import deprecated

from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.types.enums import (
    Framework,
    InferenceType,
    ProcessingInputType,
    ProcessingType,
)
from picsellia.types.schemas import ProcessingSchema
from picsellia.utils import filter_payload

logger = logging.getLogger("picsellia")


class Processing(Dao):
    def __init__(self, connexion: Connection, data: dict):
        Dao.__init__(self, connexion, data)

    @property
    def name(self) -> str:
        """Name of this (Processing)"""
        return self._name

    @property
    def type(self) -> ProcessingType:
        """Type of this (Processing)"""
        return self._type

    @property
    def docker(self) -> str:
        """Docker image of this (Processing)"""
        return f"{self._docker_image}:{self._docker_tag}"

    def __str__(self):
        return f"{Colors.GREEN}Processing '{self.name}' {Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/processing/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> ProcessingSchema:
        schema = ProcessingSchema(**data)
        self._name = schema.name
        self._type = schema.type
        self._docker_image = schema.docker_image
        self._docker_tag = schema.docker_tag
        return schema

    @exception_handler
    @beartype
    def update(
        self,
        docker_image: str | None = None,
        docker_tag: str | None = None,
        description: str | None = None,
        default_parameters: dict | None = None,
        default_cpu: int | None = None,
        default_gpu: int | None = None,
    ) -> None:
        """Update docker_image, description or default_parameters of (Processing).

        Examples:
            ```python
            processing.update(docker_image='new-image', docker_tag='1.2.0')
            ```

        Arguments:
            docker_image (str, optional): New docker image of this (Processing). Defaults to None.
            docker_tag (str, optional): New docker tag of this (Processing). Defaults to None.
            description (str, optional): New description of the (Processing). Defaults to None.
            default_parameters (dict, optional): New default parameters of the (Processing). Defaults to None.
            default_cpu (str or InferenceType, optional): New default cpu of the (Processing). Defaults to None.
            default_gpu (str or InferenceType, optional): New default gpu of the (Processing). Defaults to None.
        """
        payload = {
            "docker_image": docker_image,
            "docker_tag": docker_tag,
            "description": description,
            "default_parameters": default_parameters,
            "default_cpu": default_cpu,
            "default_gpu": default_gpu,
        }
        self._update_processing(payload)
        logger.info(f"{self} updated")

    def _update_processing(self, payload: dict) -> None:
        filtered_payload = filter_payload(payload)
        r = self.connection.patch(
            f"/api/processing/{self.id}", data=orjson.dumps(filtered_payload)
        ).json()
        self.refresh(r)

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete this processing from the platform.

        :warning: **DANGER ZONE**: Be very careful here!

        Examples:
            ```python
            processing.delete()
            ```
        """
        self.connection.delete(f"/api/processing/{self.id}")
        logger.info(f"{self} deleted.")

    @exception_handler
    @beartype
    def list_processing_inputs(self) -> list[dict]:
        """
        List inputs of this processing.
        """
        r = self.connection.get(f"/api/processing/{self.id}/inputs")
        return r.json()["items"]

    @exception_handler
    @beartype
    def add_processing_input(
        self,
        name: str,
        input_type: ProcessingInputType,
        required: bool,
        inference_type_constraint: InferenceType | None,
        framework_constraint: Framework | None,
    ) -> dict:
        """
        Add an input to this processing. Inputs are checked on launch_processing(), they must match types and constraints.
        They are passed to the context of your processing in "inputs" key.
        """
        payload = {
            "name": name,
            "input_type": input_type,
            "required": required,
            "inference_type_constraint": inference_type_constraint,
            "framework_constraint": framework_constraint,
        }
        r = self.connection.post(
            f"/api/processing/{self.id}/inputs", data=orjson.dumps(payload)
        )
        return r.json()

    @exception_handler
    @beartype
    def update_processing_input(
        self,
        name: str,
        required: bool,
        inference_type_constraint: InferenceType | None,
        framework_constraint: Framework | None,
    ) -> dict:
        """
        Update an input of this processing.
        """
        payload = {
            "required": required,
            "inference_type_constraint": inference_type_constraint,
            "framework_constraint": framework_constraint,
        }
        r = self.connection.put(
            f"/api/processing/{self.id}/inputs/{name}", data=orjson.dumps(payload)
        )
        return r.json()

    @exception_handler
    @beartype
    def delete_processing_input(self, name: str) -> None:
        """
        Delete an input from this processing.
        """
        self.connection.delete(f"/api/processing/{self.id}/inputs/{name}")
        logger.info(f"Processing input {name} of {self} have been removed.")

    @exception_handler
    @beartype
    @deprecated(
        deprecated_in="6.29.0",
        details="In the new processing system, constraints are defined on Processing inputs. This method will update processing input that matches old system, but should not be used anymore.",
    )
    def create_dataset_version_processing_constraints(
        self,
        input_dataset_version_type: str | InferenceType | None = None,
        output_dataset_version_type: str | InferenceType | None = None,
        model_version_framework: str | Framework | None = None,
        model_version_type: str | InferenceType | None = None,
    ):
        """
        This method can only be used for processing running on DatasetVersion.
        So the type of this Processing must be one of:
            - PRE_ANNOTATION
            - DATA_AUGMENTATION
            - DATASET_VERSION_CREATION
            - AUTO_TAGGING
            - AUTO_ANNOTATION
        """

        # this is a blacklist to be future compatible
        if self.type in [
            ProcessingType.DATA_AUTO_TAGGING,
            ProcessingType.MODEL_COMPRESSION,
            ProcessingType.MODEL_CONVERSION,
        ]:
            raise TypeError(
                f"{self.type} processings cannot have this type of constraints"
            )

        payload = {
            "dataset_version_constraints": {
                "input_dataset_version_type": InferenceType.validate(
                    input_dataset_version_type
                )
                if input_dataset_version_type
                else None,
                "output_dataset_version_type": InferenceType.validate(
                    output_dataset_version_type
                )
                if output_dataset_version_type
                else None,
                "model_version_framework": Framework.validate(model_version_framework)
                if model_version_framework
                else None,
                "model_version_type": InferenceType.validate(model_version_type)
                if model_version_type
                else None,
            }
        }
        self._update_processing(payload)
        logger.info(f"Constraints added on {self}")

    @exception_handler
    @beartype
    @deprecated(
        deprecated_in="6.29.0",
        details="In the new processing system, constraints are defined on Processing inputs. This method will update processing input that matches old system, but should not be used anymore.",
    )
    def create_datalake_processing_constraints(
        self,
        model_version_framework: str | Framework | None = None,
        model_version_type: str | InferenceType | None = None,
    ):
        """
        This method can only be used for processing running on Datalake.
        So the type of this Processing must be one of:
            - DATA_AUTO_TAGGING
        """
        # this is a blacklist to be future compatible
        if self.type in [
            ProcessingType.PRE_ANNOTATION,
            ProcessingType.DATA_AUGMENTATION,
            ProcessingType.DATASET_VERSION_CREATION,
            ProcessingType.AUTO_TAGGING,
            ProcessingType.AUTO_ANNOTATION,
            ProcessingType.MODEL_COMPRESSION,
            ProcessingType.MODEL_CONVERSION,
        ]:
            raise TypeError(
                f"{self.type} processings cannot have this type of constraints"
            )

        payload = {
            "datalake_constraints": {
                "model_version_framework": Framework.validate(model_version_framework)
                if model_version_framework
                else None,
                "model_version_type": InferenceType.validate(model_version_type)
                if model_version_type
                else None,
            }
        }
        self._update_processing(payload)
        logger.info(f"Constraints added on {self}")
