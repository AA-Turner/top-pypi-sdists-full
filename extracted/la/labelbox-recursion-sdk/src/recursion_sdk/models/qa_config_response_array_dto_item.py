from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.qa_config_response_array_dto_item_accelerator_type_0 import QaConfigResponseArrayDtoItemAcceleratorType0
  from ..models.qa_config_response_array_dto_item_env_vars_type_0 import QaConfigResponseArrayDtoItemEnvVarsType0
  from ..models.qa_config_response_array_dto_item_files_item import QaConfigResponseArrayDtoItemFilesItem
  from ..models.qa_config_response_array_dto_item_parameters_type_0 import QaConfigResponseArrayDtoItemParametersType0





T = TypeVar("T", bound="QaConfigResponseArrayDtoItem")



@_attrs_define
class QaConfigResponseArrayDtoItem:
    """ Persistent QA config describing how to run a QA evaluation container for an environment.

        Attributes:
            id (UUID): Stable QA-config identifier (UUID).
            environment_id (UUID): Stable environment identifier (UUID).
            name (str): Display name of the QA config.
            description (None | str): Free-form description of the QA config.
            container_image (None | str): Container image reference used by this QA config; null when an image identifier
                resolves the image instead.
            image_id (None | str): Image registry identifier of the QA container; null when a container image reference is
                set instead.
            cpu_milli (float | None): CPU allocation in milli-CPUs.
            memory_mib (float | None): Memory allocation in MiB.
            timeout_seconds (float | None): Hard timeout in seconds for the QA job.
            accelerator (None | QaConfigResponseArrayDtoItemAcceleratorType0): Accelerator configuration, or null when no
                accelerator is attached.
            env_vars (None | QaConfigResponseArrayDtoItemEnvVarsType0): Environment variables injected into the QA
                container.
            args (list[str]): Command-line arguments passed to the QA container entrypoint; empty when none are configured.
            parameters (None | QaConfigResponseArrayDtoItemParametersType0): Free-form parameters serialized to a parameters
                JSON file for the container.
            launcher_type (None | str): Launcher backend used to execute this QA config.
            max_retries (float): Maximum number of automatic retries on failure. Applies to single-container QA kinds
                (standard, grading-oracle, metrics-validator), where a failed or unusable attempt is re-dispatched until the
                budget is spent. Ignored by the composite kinds (gtGradingOracle, standard-composite), which always run a single
                attempt.
            built_in_key (None | str): Reference to a built-in QA template, or null for user-defined configs.
            run_config_version_id (None | UUID): Locked run-config-version bound to this QA config, or null when no binding
                exists.
            files (list[QaConfigResponseArrayDtoItemFilesItem]): Files attached to this QA config and mounted into the
                container at run time.
            created_at (str): Timestamp when the QA config was created (ISO-8601, UTC).
            updated_at (str): Timestamp when the QA config was last updated (ISO-8601, UTC).
     """

    id: UUID
    environment_id: UUID
    name: str
    description: None | str
    container_image: None | str
    image_id: None | str
    cpu_milli: float | None
    memory_mib: float | None
    timeout_seconds: float | None
    accelerator: None | QaConfigResponseArrayDtoItemAcceleratorType0
    env_vars: None | QaConfigResponseArrayDtoItemEnvVarsType0
    args: list[str]
    parameters: None | QaConfigResponseArrayDtoItemParametersType0
    launcher_type: None | str
    max_retries: float
    built_in_key: None | str
    run_config_version_id: None | UUID
    files: list[QaConfigResponseArrayDtoItemFilesItem]
    created_at: str
    updated_at: str





    def to_dict(self) -> dict[str, Any]:
        from ..models.qa_config_response_array_dto_item_accelerator_type_0 import QaConfigResponseArrayDtoItemAcceleratorType0 # noqa: PLC0415
        from ..models.qa_config_response_array_dto_item_env_vars_type_0 import QaConfigResponseArrayDtoItemEnvVarsType0 # noqa: PLC0415
        from ..models.qa_config_response_array_dto_item_files_item import QaConfigResponseArrayDtoItemFilesItem # noqa: PLC0415
        from ..models.qa_config_response_array_dto_item_parameters_type_0 import QaConfigResponseArrayDtoItemParametersType0 # noqa: PLC0415
        id = str(self.id)

        environment_id = str(self.environment_id)

        name = self.name

        description: None | str
        description = self.description

        container_image: None | str
        container_image = self.container_image

        image_id: None | str
        image_id = self.image_id

        cpu_milli: float | None
        cpu_milli = self.cpu_milli

        memory_mib: float | None
        memory_mib = self.memory_mib

        timeout_seconds: float | None
        timeout_seconds = self.timeout_seconds

        accelerator: dict[str, Any] | None
        if isinstance(self.accelerator, QaConfigResponseArrayDtoItemAcceleratorType0):
            accelerator = self.accelerator.to_dict()
        else:
            accelerator = self.accelerator

        env_vars: dict[str, Any] | None
        if isinstance(self.env_vars, QaConfigResponseArrayDtoItemEnvVarsType0):
            env_vars = self.env_vars.to_dict()
        else:
            env_vars = self.env_vars

        args = self.args



        parameters: dict[str, Any] | None
        if isinstance(self.parameters, QaConfigResponseArrayDtoItemParametersType0):
            parameters = self.parameters.to_dict()
        else:
            parameters = self.parameters

        launcher_type: None | str
        launcher_type = self.launcher_type

        max_retries = self.max_retries

        built_in_key: None | str
        built_in_key = self.built_in_key

        run_config_version_id: None | str
        if isinstance(self.run_config_version_id, UUID):
            run_config_version_id = str(self.run_config_version_id)
        else:
            run_config_version_id = self.run_config_version_id

        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)



        created_at = self.created_at

        updated_at = self.updated_at


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "environmentId": environment_id,
            "name": name,
            "description": description,
            "containerImage": container_image,
            "imageId": image_id,
            "cpuMilli": cpu_milli,
            "memoryMib": memory_mib,
            "timeoutSeconds": timeout_seconds,
            "accelerator": accelerator,
            "envVars": env_vars,
            "args": args,
            "parameters": parameters,
            "launcherType": launcher_type,
            "maxRetries": max_retries,
            "builtInKey": built_in_key,
            "runConfigVersionId": run_config_version_id,
            "files": files,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.qa_config_response_array_dto_item_accelerator_type_0 import QaConfigResponseArrayDtoItemAcceleratorType0 # noqa: PLC0415
        from ..models.qa_config_response_array_dto_item_env_vars_type_0 import QaConfigResponseArrayDtoItemEnvVarsType0 # noqa: PLC0415
        from ..models.qa_config_response_array_dto_item_files_item import QaConfigResponseArrayDtoItemFilesItem # noqa: PLC0415
        from ..models.qa_config_response_array_dto_item_parameters_type_0 import QaConfigResponseArrayDtoItemParametersType0 # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        environment_id = UUID(d.pop("environmentId"))




        name = d.pop("name")

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))


        def _parse_container_image(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        container_image = _parse_container_image(d.pop("containerImage"))


        def _parse_image_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        image_id = _parse_image_id(d.pop("imageId"))


        def _parse_cpu_milli(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        cpu_milli = _parse_cpu_milli(d.pop("cpuMilli"))


        def _parse_memory_mib(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        memory_mib = _parse_memory_mib(d.pop("memoryMib"))


        def _parse_timeout_seconds(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        timeout_seconds = _parse_timeout_seconds(d.pop("timeoutSeconds"))


        def _parse_accelerator(data: object) -> None | QaConfigResponseArrayDtoItemAcceleratorType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                accelerator_type_0 = QaConfigResponseArrayDtoItemAcceleratorType0.from_dict(data)



                return accelerator_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | QaConfigResponseArrayDtoItemAcceleratorType0, data)

        accelerator = _parse_accelerator(d.pop("accelerator"))


        def _parse_env_vars(data: object) -> None | QaConfigResponseArrayDtoItemEnvVarsType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                env_vars_type_0 = QaConfigResponseArrayDtoItemEnvVarsType0.from_dict(data)



                return env_vars_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | QaConfigResponseArrayDtoItemEnvVarsType0, data)

        env_vars = _parse_env_vars(d.pop("envVars"))


        args = cast(list[str], d.pop("args"))


        def _parse_parameters(data: object) -> None | QaConfigResponseArrayDtoItemParametersType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parameters_type_0 = QaConfigResponseArrayDtoItemParametersType0.from_dict(data)



                return parameters_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | QaConfigResponseArrayDtoItemParametersType0, data)

        parameters = _parse_parameters(d.pop("parameters"))


        def _parse_launcher_type(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        launcher_type = _parse_launcher_type(d.pop("launcherType"))


        max_retries = d.pop("maxRetries")

        def _parse_built_in_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        built_in_key = _parse_built_in_key(d.pop("builtInKey"))


        def _parse_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                run_config_version_id_type_0 = UUID(data)



                return run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        run_config_version_id = _parse_run_config_version_id(d.pop("runConfigVersionId"))


        files = []
        _files = d.pop("files")
        for files_item_data in (_files):
            files_item = QaConfigResponseArrayDtoItemFilesItem.from_dict(files_item_data)



            files.append(files_item)


        created_at = d.pop("createdAt")

        updated_at = d.pop("updatedAt")

        qa_config_response_array_dto_item = cls(
            id=id,
            environment_id=environment_id,
            name=name,
            description=description,
            container_image=container_image,
            image_id=image_id,
            cpu_milli=cpu_milli,
            memory_mib=memory_mib,
            timeout_seconds=timeout_seconds,
            accelerator=accelerator,
            env_vars=env_vars,
            args=args,
            parameters=parameters,
            launcher_type=launcher_type,
            max_retries=max_retries,
            built_in_key=built_in_key,
            run_config_version_id=run_config_version_id,
            files=files,
            created_at=created_at,
            updated_at=updated_at,
        )

        return qa_config_response_array_dto_item

