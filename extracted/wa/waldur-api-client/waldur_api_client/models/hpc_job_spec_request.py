from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.hpc_job_file_request import HpcJobFileRequest
    from ..models.hpc_job_spec_request_environment import HpcJobSpecRequestEnvironment


T = TypeVar("T", bound="HpcJobSpecRequest")


@_attrs_define
class HpcJobSpecRequest:
    """
    Attributes:
        name (str):
        commands (str): Shell commands the job runs.
        partition (Union[Unset, str]):  Default: ''.
        qos (Union[Unset, str]):  Default: ''.
        nodes (Union[Unset, int]):  Default: 1.
        ntasks_per_node (Union[Unset, int]):  Default: 1.
        cpus_per_task (Union[Unset, int]):  Default: 1.
        memory_mb (Union[None, Unset, int]):
        time_limit_minutes (Union[Unset, int]):  Default: 60.
        gpus_per_node (Union[Unset, int]):  Default: 0.
        modules (Union[Unset, list[str]]): Setup lines, e.g. 'module load GROMACS/2024.1-foss-2023b'.
        working_directory (Union[Unset, str]):  Default: ''.
        environment (Union[Unset, HpcJobSpecRequestEnvironment]):
        files (Union[Unset, list['HpcJobFileRequest']]): Files written into the working directory before the commands
            run, such as the program the job runs.
    """

    name: str
    commands: str
    partition: Union[Unset, str] = ""
    qos: Union[Unset, str] = ""
    nodes: Union[Unset, int] = 1
    ntasks_per_node: Union[Unset, int] = 1
    cpus_per_task: Union[Unset, int] = 1
    memory_mb: Union[None, Unset, int] = UNSET
    time_limit_minutes: Union[Unset, int] = 60
    gpus_per_node: Union[Unset, int] = 0
    modules: Union[Unset, list[str]] = UNSET
    working_directory: Union[Unset, str] = ""
    environment: Union[Unset, "HpcJobSpecRequestEnvironment"] = UNSET
    files: Union[Unset, list["HpcJobFileRequest"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        commands = self.commands

        partition = self.partition

        qos = self.qos

        nodes = self.nodes

        ntasks_per_node = self.ntasks_per_node

        cpus_per_task = self.cpus_per_task

        memory_mb: Union[None, Unset, int]
        if isinstance(self.memory_mb, Unset):
            memory_mb = UNSET
        else:
            memory_mb = self.memory_mb

        time_limit_minutes = self.time_limit_minutes

        gpus_per_node = self.gpus_per_node

        modules: Union[Unset, list[str]] = UNSET
        if not isinstance(self.modules, Unset):
            modules = self.modules

        working_directory = self.working_directory

        environment: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.environment, Unset):
            environment = self.environment.to_dict()

        files: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()
                files.append(files_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "commands": commands,
            }
        )
        if partition is not UNSET:
            field_dict["partition"] = partition
        if qos is not UNSET:
            field_dict["qos"] = qos
        if nodes is not UNSET:
            field_dict["nodes"] = nodes
        if ntasks_per_node is not UNSET:
            field_dict["ntasks_per_node"] = ntasks_per_node
        if cpus_per_task is not UNSET:
            field_dict["cpus_per_task"] = cpus_per_task
        if memory_mb is not UNSET:
            field_dict["memory_mb"] = memory_mb
        if time_limit_minutes is not UNSET:
            field_dict["time_limit_minutes"] = time_limit_minutes
        if gpus_per_node is not UNSET:
            field_dict["gpus_per_node"] = gpus_per_node
        if modules is not UNSET:
            field_dict["modules"] = modules
        if working_directory is not UNSET:
            field_dict["working_directory"] = working_directory
        if environment is not UNSET:
            field_dict["environment"] = environment
        if files is not UNSET:
            field_dict["files"] = files

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.hpc_job_file_request import HpcJobFileRequest
        from ..models.hpc_job_spec_request_environment import HpcJobSpecRequestEnvironment

        d = dict(src_dict)
        name = d.pop("name")

        commands = d.pop("commands")

        partition = d.pop("partition", UNSET)

        qos = d.pop("qos", UNSET)

        nodes = d.pop("nodes", UNSET)

        ntasks_per_node = d.pop("ntasks_per_node", UNSET)

        cpus_per_task = d.pop("cpus_per_task", UNSET)

        def _parse_memory_mb(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        memory_mb = _parse_memory_mb(d.pop("memory_mb", UNSET))

        time_limit_minutes = d.pop("time_limit_minutes", UNSET)

        gpus_per_node = d.pop("gpus_per_node", UNSET)

        modules = cast(list[str], d.pop("modules", UNSET))

        working_directory = d.pop("working_directory", UNSET)

        _environment = d.pop("environment", UNSET)
        environment: Union[Unset, HpcJobSpecRequestEnvironment]
        if isinstance(_environment, Unset):
            environment = UNSET
        else:
            environment = HpcJobSpecRequestEnvironment.from_dict(_environment)

        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in _files or []:
            files_item = HpcJobFileRequest.from_dict(files_item_data)

            files.append(files_item)

        hpc_job_spec_request = cls(
            name=name,
            commands=commands,
            partition=partition,
            qos=qos,
            nodes=nodes,
            ntasks_per_node=ntasks_per_node,
            cpus_per_task=cpus_per_task,
            memory_mb=memory_mb,
            time_limit_minutes=time_limit_minutes,
            gpus_per_node=gpus_per_node,
            modules=modules,
            working_directory=working_directory,
            environment=environment,
            files=files,
        )

        hpc_job_spec_request.additional_properties = d
        return hpc_job_spec_request

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
