from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.create_compute_request_dto_accelerator import CreateComputeRequestDtoAccelerator
  from ..models.create_compute_request_dto_env import CreateComputeRequestDtoEnv
  from ..models.create_compute_request_dto_mounts_item import CreateComputeRequestDtoMountsItem





T = TypeVar("T", bound="CreateComputeRequestDto")



@_attrs_define
class CreateComputeRequestDto:
    """ Request body for launching a new compute (container pod) inside an environment.

        Example:
            {'environmentId': '784e2386-e297-4f9d-a886-838422383b65', 'name': 'vision-agent-dev', 'containerImage': 'us-
                docker.pkg.dev/example-project/recursion-agents/vision-agent:1.4.2', 'cpuMilli': 2000, 'memoryMib': 4096,
                'timeoutSeconds': 3600, 'idleStopAfterSeconds': 14400, 'stoppedDeleteAfterSeconds': 604800, 'pvcSizeGi': 20,
                'httpPort': 8080, 'env': {'MODEL_PROVIDER': 'anthropic', 'LOG_LEVEL': 'info'}, 'runConfigVersionId':
                '39088cb6-ca62-4544-a074-fc66e10807ad'}

        Attributes:
            environment_id (UUID): Environment that owns the new compute.
            name (str): Human-readable compute name shown in the UI and logs.
            container_image (str): Fully-qualified container image reference (registry/path:tag or digest) to launch.
            cpu_milli (int | Unset): CPU request in milli-cores (e.g. 1000 = 1 vCPU). Falls back to the platform default
                when omitted.
            memory_mib (int | Unset): Memory request in MiB. Falls back to the platform default when omitted.
            timeout_seconds (int | Unset): Maximum lifetime of the compute in seconds before it is forcefully terminated.
            idle_stop_after_seconds (int | Unset): Seconds of inactivity before stopping the compute; maximum 30 days.
            stopped_delete_after_seconds (int | Unset): Seconds stopped before deleting the compute and volume; maximum 30
                days.
            accelerator (CreateComputeRequestDtoAccelerator | Unset): Optional GPU accelerator to attach to the compute.
            privileged (bool | Unset): Whether the container runs in privileged mode. Requires elevated permissions.
            nested_virt (bool | Unset): Whether to request KVM-backed nested virtualization. Requires privileged=true.
            pvc_size_gi (int | Unset): Size of the attached persistent volume claim in GiB.
            http_port (int | Unset): TCP port the container exposes for HTTP access. Required to mint a redemption URL.
            env (CreateComputeRequestDtoEnv | Unset): Environment variables injected into the container at launch.
            mounts (list[CreateComputeRequestDtoMountsItem] | Unset): Additional volume mounts (e.g. shared dataset volumes)
                to attach to the compute.
            run_config_version_id (UUID | Unset): Optional run-config version ID that produced this compute. Used to inherit
                secrets and config.
     """

    environment_id: UUID
    name: str
    container_image: str
    cpu_milli: int | Unset = UNSET
    memory_mib: int | Unset = UNSET
    timeout_seconds: int | Unset = UNSET
    idle_stop_after_seconds: int | Unset = UNSET
    stopped_delete_after_seconds: int | Unset = UNSET
    accelerator: CreateComputeRequestDtoAccelerator | Unset = UNSET
    privileged: bool | Unset = UNSET
    nested_virt: bool | Unset = UNSET
    pvc_size_gi: int | Unset = UNSET
    http_port: int | Unset = UNSET
    env: CreateComputeRequestDtoEnv | Unset = UNSET
    mounts: list[CreateComputeRequestDtoMountsItem] | Unset = UNSET
    run_config_version_id: UUID | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_compute_request_dto_accelerator import CreateComputeRequestDtoAccelerator # noqa: PLC0415
        from ..models.create_compute_request_dto_env import CreateComputeRequestDtoEnv # noqa: PLC0415
        from ..models.create_compute_request_dto_mounts_item import CreateComputeRequestDtoMountsItem # noqa: PLC0415
        environment_id = str(self.environment_id)

        name = self.name

        container_image = self.container_image

        cpu_milli = self.cpu_milli

        memory_mib = self.memory_mib

        timeout_seconds = self.timeout_seconds

        idle_stop_after_seconds = self.idle_stop_after_seconds

        stopped_delete_after_seconds = self.stopped_delete_after_seconds

        accelerator: dict[str, Any] | Unset = UNSET
        if not isinstance(self.accelerator, Unset):
            accelerator = self.accelerator.to_dict()

        privileged = self.privileged

        nested_virt = self.nested_virt

        pvc_size_gi = self.pvc_size_gi

        http_port = self.http_port

        env: dict[str, Any] | Unset = UNSET
        if not isinstance(self.env, Unset):
            env = self.env.to_dict()

        mounts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.mounts, Unset):
            mounts = []
            for mounts_item_data in self.mounts:
                mounts_item = mounts_item_data.to_dict()
                mounts.append(mounts_item)



        run_config_version_id: str | Unset = UNSET
        if not isinstance(self.run_config_version_id, Unset):
            run_config_version_id = str(self.run_config_version_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "environmentId": environment_id,
            "name": name,
            "containerImage": container_image,
        })
        if cpu_milli is not UNSET:
            field_dict["cpuMilli"] = cpu_milli
        if memory_mib is not UNSET:
            field_dict["memoryMib"] = memory_mib
        if timeout_seconds is not UNSET:
            field_dict["timeoutSeconds"] = timeout_seconds
        if idle_stop_after_seconds is not UNSET:
            field_dict["idleStopAfterSeconds"] = idle_stop_after_seconds
        if stopped_delete_after_seconds is not UNSET:
            field_dict["stoppedDeleteAfterSeconds"] = stopped_delete_after_seconds
        if accelerator is not UNSET:
            field_dict["accelerator"] = accelerator
        if privileged is not UNSET:
            field_dict["privileged"] = privileged
        if nested_virt is not UNSET:
            field_dict["nestedVirt"] = nested_virt
        if pvc_size_gi is not UNSET:
            field_dict["pvcSizeGi"] = pvc_size_gi
        if http_port is not UNSET:
            field_dict["httpPort"] = http_port
        if env is not UNSET:
            field_dict["env"] = env
        if mounts is not UNSET:
            field_dict["mounts"] = mounts
        if run_config_version_id is not UNSET:
            field_dict["runConfigVersionId"] = run_config_version_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_compute_request_dto_accelerator import CreateComputeRequestDtoAccelerator # noqa: PLC0415
        from ..models.create_compute_request_dto_env import CreateComputeRequestDtoEnv # noqa: PLC0415
        from ..models.create_compute_request_dto_mounts_item import CreateComputeRequestDtoMountsItem # noqa: PLC0415
        d = dict(src_dict)
        environment_id = UUID(d.pop("environmentId"))




        name = d.pop("name")

        container_image = d.pop("containerImage")

        cpu_milli = d.pop("cpuMilli", UNSET)

        memory_mib = d.pop("memoryMib", UNSET)

        timeout_seconds = d.pop("timeoutSeconds", UNSET)

        idle_stop_after_seconds = d.pop("idleStopAfterSeconds", UNSET)

        stopped_delete_after_seconds = d.pop("stoppedDeleteAfterSeconds", UNSET)

        _accelerator = d.pop("accelerator", UNSET)
        accelerator: CreateComputeRequestDtoAccelerator | Unset
        if isinstance(_accelerator,  Unset):
            accelerator = UNSET
        else:
            accelerator = CreateComputeRequestDtoAccelerator.from_dict(_accelerator)




        privileged = d.pop("privileged", UNSET)

        nested_virt = d.pop("nestedVirt", UNSET)

        pvc_size_gi = d.pop("pvcSizeGi", UNSET)

        http_port = d.pop("httpPort", UNSET)

        _env = d.pop("env", UNSET)
        env: CreateComputeRequestDtoEnv | Unset
        if isinstance(_env,  Unset):
            env = UNSET
        else:
            env = CreateComputeRequestDtoEnv.from_dict(_env)




        _mounts = d.pop("mounts", UNSET)
        mounts: list[CreateComputeRequestDtoMountsItem] | Unset = UNSET
        if _mounts is not UNSET:
            mounts = []
            for mounts_item_data in _mounts:
                mounts_item = CreateComputeRequestDtoMountsItem.from_dict(mounts_item_data)



                mounts.append(mounts_item)


        _run_config_version_id = d.pop("runConfigVersionId", UNSET)
        run_config_version_id: UUID | Unset
        if isinstance(_run_config_version_id,  Unset):
            run_config_version_id = UNSET
        else:
            run_config_version_id = UUID(_run_config_version_id)




        create_compute_request_dto = cls(
            environment_id=environment_id,
            name=name,
            container_image=container_image,
            cpu_milli=cpu_milli,
            memory_mib=memory_mib,
            timeout_seconds=timeout_seconds,
            idle_stop_after_seconds=idle_stop_after_seconds,
            stopped_delete_after_seconds=stopped_delete_after_seconds,
            accelerator=accelerator,
            privileged=privileged,
            nested_virt=nested_virt,
            pvc_size_gi=pvc_size_gi,
            http_port=http_port,
            env=env,
            mounts=mounts,
            run_config_version_id=run_config_version_id,
        )


        create_compute_request_dto.additional_properties = d
        return create_compute_request_dto

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
