from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.update_qa_config_body_dto_launcher_type_type_0 import UpdateQaConfigBodyDtoLauncherTypeType0
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.update_qa_config_body_dto_accelerator_type_0 import UpdateQaConfigBodyDtoAcceleratorType0
  from ..models.update_qa_config_body_dto_env_vars_type_0 import UpdateQaConfigBodyDtoEnvVarsType0
  from ..models.update_qa_config_body_dto_parameters_type_0 import UpdateQaConfigBodyDtoParametersType0





T = TypeVar("T", bound="UpdateQaConfigBodyDto")



@_attrs_define
class UpdateQaConfigBodyDto:
    """ Partial update payload for an existing QA config.

        Example:
            {'description': 'LLM critic that scores instruction quality, rubric coverage, atomicity, and verifiability.',
                'timeoutSeconds': 900, 'maxRetries': 2}

        Attributes:
            name (str | Unset): Updated display name of the QA config.
            description (None | str | Unset): Updated description; pass null to clear.
            cpu_milli (int | None | Unset): Updated CPU allocation in milli-CPUs; null clears. Example: 1000.
            memory_mib (int | None | Unset): Updated memory allocation in MiB; null clears. Example: 2048.
            timeout_seconds (int | None | Unset): Updated job timeout in seconds; null clears. Example: 600.
            accelerator (None | Unset | UpdateQaConfigBodyDtoAcceleratorType0): Updated accelerator configuration; pass null
                to clear.
            env_vars (None | Unset | UpdateQaConfigBodyDtoEnvVarsType0): Updated environment-variable map for the container;
                null clears.
            args (list[str] | None | Unset): Updated argument list for the container entrypoint; null clears.
            parameters (None | Unset | UpdateQaConfigBodyDtoParametersType0): Updated free-form parameter payload; null
                clears.
            launcher_type (None | Unset | UpdateQaConfigBodyDtoLauncherTypeType0): Updated launcher backend override; null
                falls back to the environment default.
            max_retries (int | None | Unset): Updated retry budget on failure; null clears. Applies to single-container QA
                kinds (standard, grading-oracle, metrics-validator), where a failed or unusable attempt is re-dispatched until
                the budget is spent. Ignored by the composite kinds (gtGradingOracle, standard-composite), which always run a
                single attempt. Example: 1.
            run_config_version_id (None | Unset | UUID): Patch the bound run-config-version. Pass null to clear the binding.
                When set, the QA submit path resolves the container image, environment variables, and arguments from this
                version instead of the legacy image fields.
     """

    name: str | Unset = UNSET
    description: None | str | Unset = UNSET
    cpu_milli: int | None | Unset = UNSET
    memory_mib: int | None | Unset = UNSET
    timeout_seconds: int | None | Unset = UNSET
    accelerator: None | Unset | UpdateQaConfigBodyDtoAcceleratorType0 = UNSET
    env_vars: None | Unset | UpdateQaConfigBodyDtoEnvVarsType0 = UNSET
    args: list[str] | None | Unset = UNSET
    parameters: None | Unset | UpdateQaConfigBodyDtoParametersType0 = UNSET
    launcher_type: None | Unset | UpdateQaConfigBodyDtoLauncherTypeType0 = UNSET
    max_retries: int | None | Unset = UNSET
    run_config_version_id: None | Unset | UUID = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.update_qa_config_body_dto_accelerator_type_0 import UpdateQaConfigBodyDtoAcceleratorType0 # noqa: PLC0415
        from ..models.update_qa_config_body_dto_env_vars_type_0 import UpdateQaConfigBodyDtoEnvVarsType0 # noqa: PLC0415
        from ..models.update_qa_config_body_dto_parameters_type_0 import UpdateQaConfigBodyDtoParametersType0 # noqa: PLC0415
        name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        cpu_milli: int | None | Unset
        if isinstance(self.cpu_milli, Unset):
            cpu_milli = UNSET
        else:
            cpu_milli = self.cpu_milli

        memory_mib: int | None | Unset
        if isinstance(self.memory_mib, Unset):
            memory_mib = UNSET
        else:
            memory_mib = self.memory_mib

        timeout_seconds: int | None | Unset
        if isinstance(self.timeout_seconds, Unset):
            timeout_seconds = UNSET
        else:
            timeout_seconds = self.timeout_seconds

        accelerator: dict[str, Any] | None | Unset
        if isinstance(self.accelerator, Unset):
            accelerator = UNSET
        elif isinstance(self.accelerator, UpdateQaConfigBodyDtoAcceleratorType0):
            accelerator = self.accelerator.to_dict()
        else:
            accelerator = self.accelerator

        env_vars: dict[str, Any] | None | Unset
        if isinstance(self.env_vars, Unset):
            env_vars = UNSET
        elif isinstance(self.env_vars, UpdateQaConfigBodyDtoEnvVarsType0):
            env_vars = self.env_vars.to_dict()
        else:
            env_vars = self.env_vars

        args: list[str] | None | Unset
        if isinstance(self.args, Unset):
            args = UNSET
        elif isinstance(self.args, list):
            args = self.args


        else:
            args = self.args

        parameters: dict[str, Any] | None | Unset
        if isinstance(self.parameters, Unset):
            parameters = UNSET
        elif isinstance(self.parameters, UpdateQaConfigBodyDtoParametersType0):
            parameters = self.parameters.to_dict()
        else:
            parameters = self.parameters

        launcher_type: None | str | Unset
        if isinstance(self.launcher_type, Unset):
            launcher_type = UNSET
        elif isinstance(self.launcher_type, UpdateQaConfigBodyDtoLauncherTypeType0):
            launcher_type = self.launcher_type.value
        else:
            launcher_type = self.launcher_type

        max_retries: int | None | Unset
        if isinstance(self.max_retries, Unset):
            max_retries = UNSET
        else:
            max_retries = self.max_retries

        run_config_version_id: None | str | Unset
        if isinstance(self.run_config_version_id, Unset):
            run_config_version_id = UNSET
        elif isinstance(self.run_config_version_id, UUID):
            run_config_version_id = str(self.run_config_version_id)
        else:
            run_config_version_id = self.run_config_version_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if cpu_milli is not UNSET:
            field_dict["cpuMilli"] = cpu_milli
        if memory_mib is not UNSET:
            field_dict["memoryMib"] = memory_mib
        if timeout_seconds is not UNSET:
            field_dict["timeoutSeconds"] = timeout_seconds
        if accelerator is not UNSET:
            field_dict["accelerator"] = accelerator
        if env_vars is not UNSET:
            field_dict["envVars"] = env_vars
        if args is not UNSET:
            field_dict["args"] = args
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if launcher_type is not UNSET:
            field_dict["launcherType"] = launcher_type
        if max_retries is not UNSET:
            field_dict["maxRetries"] = max_retries
        if run_config_version_id is not UNSET:
            field_dict["runConfigVersionId"] = run_config_version_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_qa_config_body_dto_accelerator_type_0 import UpdateQaConfigBodyDtoAcceleratorType0 # noqa: PLC0415
        from ..models.update_qa_config_body_dto_env_vars_type_0 import UpdateQaConfigBodyDtoEnvVarsType0 # noqa: PLC0415
        from ..models.update_qa_config_body_dto_parameters_type_0 import UpdateQaConfigBodyDtoParametersType0 # noqa: PLC0415
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))


        def _parse_cpu_milli(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        cpu_milli = _parse_cpu_milli(d.pop("cpuMilli", UNSET))


        def _parse_memory_mib(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        memory_mib = _parse_memory_mib(d.pop("memoryMib", UNSET))


        def _parse_timeout_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        timeout_seconds = _parse_timeout_seconds(d.pop("timeoutSeconds", UNSET))


        def _parse_accelerator(data: object) -> None | Unset | UpdateQaConfigBodyDtoAcceleratorType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                accelerator_type_0 = UpdateQaConfigBodyDtoAcceleratorType0.from_dict(data)



                return accelerator_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UpdateQaConfigBodyDtoAcceleratorType0, data)

        accelerator = _parse_accelerator(d.pop("accelerator", UNSET))


        def _parse_env_vars(data: object) -> None | Unset | UpdateQaConfigBodyDtoEnvVarsType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                env_vars_type_0 = UpdateQaConfigBodyDtoEnvVarsType0.from_dict(data)



                return env_vars_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UpdateQaConfigBodyDtoEnvVarsType0, data)

        env_vars = _parse_env_vars(d.pop("envVars", UNSET))


        def _parse_args(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                args_type_0 = cast(list[str], data)

                return args_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        args = _parse_args(d.pop("args", UNSET))


        def _parse_parameters(data: object) -> None | Unset | UpdateQaConfigBodyDtoParametersType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parameters_type_0 = UpdateQaConfigBodyDtoParametersType0.from_dict(data)



                return parameters_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UpdateQaConfigBodyDtoParametersType0, data)

        parameters = _parse_parameters(d.pop("parameters", UNSET))


        def _parse_launcher_type(data: object) -> None | Unset | UpdateQaConfigBodyDtoLauncherTypeType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                launcher_type_type_0 = UpdateQaConfigBodyDtoLauncherTypeType0(data)



                return launcher_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UpdateQaConfigBodyDtoLauncherTypeType0, data)

        launcher_type = _parse_launcher_type(d.pop("launcherType", UNSET))


        def _parse_max_retries(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_retries = _parse_max_retries(d.pop("maxRetries", UNSET))


        def _parse_run_config_version_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                run_config_version_id_type_0 = UUID(data)



                return run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        run_config_version_id = _parse_run_config_version_id(d.pop("runConfigVersionId", UNSET))


        update_qa_config_body_dto = cls(
            name=name,
            description=description,
            cpu_milli=cpu_milli,
            memory_mib=memory_mib,
            timeout_seconds=timeout_seconds,
            accelerator=accelerator,
            env_vars=env_vars,
            args=args,
            parameters=parameters,
            launcher_type=launcher_type,
            max_retries=max_retries,
            run_config_version_id=run_config_version_id,
        )

        return update_qa_config_body_dto

