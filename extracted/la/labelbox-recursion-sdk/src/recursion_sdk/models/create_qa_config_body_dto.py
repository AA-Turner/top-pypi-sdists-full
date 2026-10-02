from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_qa_config_body_dto_launcher_type import CreateQaConfigBodyDtoLauncherType
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.create_qa_config_body_dto_accelerator_type_0 import CreateQaConfigBodyDtoAcceleratorType0
  from ..models.create_qa_config_body_dto_env_vars import CreateQaConfigBodyDtoEnvVars
  from ..models.create_qa_config_body_dto_parameters import CreateQaConfigBodyDtoParameters





T = TypeVar("T", bound="CreateQaConfigBodyDto")



@_attrs_define
class CreateQaConfigBodyDto:
    """ Payload for creating a new QA config inside an environment.

        Example:
            {'name': 'semantic-critic-review', 'description': 'LLM critic that scores problem instruction quality, rubric
                coverage, and atomicity.', 'runConfigVersionId': '9a1c2e3d-4b5f-4a6c-8d7e-1f2a3b4c5d6e', 'cpuMilli': 1000,
                'memoryMib': 2048, 'timeoutSeconds': 600, 'envVars': {'LOG_LEVEL': 'info'}, 'args': ['--strict'], 'parameters':
                {'prompt': 'Evaluate the problem for instruction quality and rubric coverage.'}, 'launcherType': 'modal',
                'maxRetries': 1}

        Attributes:
            name (str): Display name of the QA config; unique within the environment.
            description (str | Unset): Optional free-form description of what this QA config evaluates.
            cpu_milli (int | Unset): CPU allocation for the QA container in milli-CPUs. Example: 1000.
            memory_mib (int | Unset): Memory allocation for the QA container in MiB. Example: 2048.
            timeout_seconds (int | Unset): Hard timeout for the QA job in seconds. Example: 600.
            accelerator (CreateQaConfigBodyDtoAcceleratorType0 | None | Unset): Optional accelerator configuration to attach
                to the QA container.
            env_vars (CreateQaConfigBodyDtoEnvVars | Unset): Environment variables (name to value) injected into the QA
                container.
            args (list[str] | Unset): Command-line arguments passed to the QA container entrypoint.
            parameters (CreateQaConfigBodyDtoParameters | Unset): Free-form parameters serialized to a parameters JSON file
                mounted into the container.
            launcher_type (CreateQaConfigBodyDtoLauncherType | Unset): Optional launcher backend override; defaults to the
                environment-level setting when unset.
            max_retries (int | Unset): Maximum number of automatic retries on failure. Applies to single-container QA kinds
                (standard, grading-oracle, metrics-validator), where a failed or unusable attempt is re-dispatched until the
                budget is spent. Ignored by the composite kinds (gtGradingOracle, standard-composite), which always run a single
                attempt. Example: 1.
            built_in_key (str | Unset): Reference to a built-in QA template; when set, the QA config inherits that template
                behavior.
            run_config_version_id (UUID | Unset): Locked run-config-version bound to this QA config. When set, the QA submit
                path resolves the container image, environment variables, and arguments from this version instead of the legacy
                image fields on the row.
     """

    name: str
    description: str | Unset = UNSET
    cpu_milli: int | Unset = UNSET
    memory_mib: int | Unset = UNSET
    timeout_seconds: int | Unset = UNSET
    accelerator: CreateQaConfigBodyDtoAcceleratorType0 | None | Unset = UNSET
    env_vars: CreateQaConfigBodyDtoEnvVars | Unset = UNSET
    args: list[str] | Unset = UNSET
    parameters: CreateQaConfigBodyDtoParameters | Unset = UNSET
    launcher_type: CreateQaConfigBodyDtoLauncherType | Unset = UNSET
    max_retries: int | Unset = UNSET
    built_in_key: str | Unset = UNSET
    run_config_version_id: UUID | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_qa_config_body_dto_accelerator_type_0 import CreateQaConfigBodyDtoAcceleratorType0 # noqa: PLC0415
        from ..models.create_qa_config_body_dto_env_vars import CreateQaConfigBodyDtoEnvVars # noqa: PLC0415
        from ..models.create_qa_config_body_dto_parameters import CreateQaConfigBodyDtoParameters # noqa: PLC0415
        name = self.name

        description = self.description

        cpu_milli = self.cpu_milli

        memory_mib = self.memory_mib

        timeout_seconds = self.timeout_seconds

        accelerator: dict[str, Any] | None | Unset
        if isinstance(self.accelerator, Unset):
            accelerator = UNSET
        elif isinstance(self.accelerator, CreateQaConfigBodyDtoAcceleratorType0):
            accelerator = self.accelerator.to_dict()
        else:
            accelerator = self.accelerator

        env_vars: dict[str, Any] | Unset = UNSET
        if not isinstance(self.env_vars, Unset):
            env_vars = self.env_vars.to_dict()

        args: list[str] | Unset = UNSET
        if not isinstance(self.args, Unset):
            args = self.args



        parameters: dict[str, Any] | Unset = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        launcher_type: str | Unset = UNSET
        if not isinstance(self.launcher_type, Unset):
            launcher_type = self.launcher_type.value


        max_retries = self.max_retries

        built_in_key = self.built_in_key

        run_config_version_id: str | Unset = UNSET
        if not isinstance(self.run_config_version_id, Unset):
            run_config_version_id = str(self.run_config_version_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
        })
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
        if built_in_key is not UNSET:
            field_dict["builtInKey"] = built_in_key
        if run_config_version_id is not UNSET:
            field_dict["runConfigVersionId"] = run_config_version_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_qa_config_body_dto_accelerator_type_0 import CreateQaConfigBodyDtoAcceleratorType0 # noqa: PLC0415
        from ..models.create_qa_config_body_dto_env_vars import CreateQaConfigBodyDtoEnvVars # noqa: PLC0415
        from ..models.create_qa_config_body_dto_parameters import CreateQaConfigBodyDtoParameters # noqa: PLC0415
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description", UNSET)

        cpu_milli = d.pop("cpuMilli", UNSET)

        memory_mib = d.pop("memoryMib", UNSET)

        timeout_seconds = d.pop("timeoutSeconds", UNSET)

        def _parse_accelerator(data: object) -> CreateQaConfigBodyDtoAcceleratorType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                accelerator_type_0 = CreateQaConfigBodyDtoAcceleratorType0.from_dict(data)



                return accelerator_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CreateQaConfigBodyDtoAcceleratorType0 | None | Unset, data)

        accelerator = _parse_accelerator(d.pop("accelerator", UNSET))


        _env_vars = d.pop("envVars", UNSET)
        env_vars: CreateQaConfigBodyDtoEnvVars | Unset
        if isinstance(_env_vars,  Unset):
            env_vars = UNSET
        else:
            env_vars = CreateQaConfigBodyDtoEnvVars.from_dict(_env_vars)




        args = cast(list[str], d.pop("args", UNSET))


        _parameters = d.pop("parameters", UNSET)
        parameters: CreateQaConfigBodyDtoParameters | Unset
        if isinstance(_parameters,  Unset):
            parameters = UNSET
        else:
            parameters = CreateQaConfigBodyDtoParameters.from_dict(_parameters)




        _launcher_type = d.pop("launcherType", UNSET)
        launcher_type: CreateQaConfigBodyDtoLauncherType | Unset
        if isinstance(_launcher_type,  Unset):
            launcher_type = UNSET
        else:
            launcher_type = CreateQaConfigBodyDtoLauncherType(_launcher_type)




        max_retries = d.pop("maxRetries", UNSET)

        built_in_key = d.pop("builtInKey", UNSET)

        _run_config_version_id = d.pop("runConfigVersionId", UNSET)
        run_config_version_id: UUID | Unset
        if isinstance(_run_config_version_id,  Unset):
            run_config_version_id = UNSET
        else:
            run_config_version_id = UUID(_run_config_version_id)




        create_qa_config_body_dto = cls(
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
            built_in_key=built_in_key,
            run_config_version_id=run_config_version_id,
        )

        return create_qa_config_body_dto

