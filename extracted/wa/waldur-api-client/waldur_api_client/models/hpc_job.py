from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HpcJob")


@_attrs_define
class HpcJob:
    """
    Attributes:
        job_id (str):
        name (str):
        state (str):
        state_reason (Union[None, Unset, str]):
        exit_code (Union[None, Unset, int]):
        account (Union[None, Unset, str]):
        partition (Union[None, Unset, str]):
        user (Union[None, Unset, str]):
        nodes (Union[None, Unset, str]):
        allocation_nodes (Union[None, Unset, int]):
        working_directory (Union[None, Unset, str]):
        start_time (Union[None, Unset, int]):
        end_time (Union[None, Unset, int]):
        elapsed (Union[None, Unset, int]): Seconds
        time_limit (Union[None, Unset, int]): Seconds (FirecREST converts Slurm's minutes)
        submit_time (Union[None, Unset, int]):
        wait_seconds (Union[None, Unset, int]): From submission to start
        allocation_cpus (Union[None, Unset, int]):
        requested_memory_mb (Union[None, Unset, int]):
        cpu_time_seconds (Union[None, Unset, int]):
        cpu_hours (Union[None, Unset, float]): Allocated CPUs x elapsed time
        cpu_efficiency (Union[None, Unset, float]): CPU time / (CPUs x elapsed), 0..1; finished jobs only
        max_rss_mb (Union[None, Unset, int]):
        memory_efficiency (Union[None, Unset, float]): Peak RSS / requested memory, 0..1; finished jobs only
        allocation_gpus (Union[None, Unset, int]):
        gpu_hours (Union[None, Unset, float]): Allocated GPUs x elapsed time
        energy_kwh (Union[None, Unset, float]): Energy consumed; where accounting records the energy TRES
        mean_power_w (Union[None, Unset, int]): Energy / elapsed time, all of the job's nodes
    """

    job_id: str
    name: str
    state: str
    state_reason: Union[None, Unset, str] = UNSET
    exit_code: Union[None, Unset, int] = UNSET
    account: Union[None, Unset, str] = UNSET
    partition: Union[None, Unset, str] = UNSET
    user: Union[None, Unset, str] = UNSET
    nodes: Union[None, Unset, str] = UNSET
    allocation_nodes: Union[None, Unset, int] = UNSET
    working_directory: Union[None, Unset, str] = UNSET
    start_time: Union[None, Unset, int] = UNSET
    end_time: Union[None, Unset, int] = UNSET
    elapsed: Union[None, Unset, int] = UNSET
    time_limit: Union[None, Unset, int] = UNSET
    submit_time: Union[None, Unset, int] = UNSET
    wait_seconds: Union[None, Unset, int] = UNSET
    allocation_cpus: Union[None, Unset, int] = UNSET
    requested_memory_mb: Union[None, Unset, int] = UNSET
    cpu_time_seconds: Union[None, Unset, int] = UNSET
    cpu_hours: Union[None, Unset, float] = UNSET
    cpu_efficiency: Union[None, Unset, float] = UNSET
    max_rss_mb: Union[None, Unset, int] = UNSET
    memory_efficiency: Union[None, Unset, float] = UNSET
    allocation_gpus: Union[None, Unset, int] = UNSET
    gpu_hours: Union[None, Unset, float] = UNSET
    energy_kwh: Union[None, Unset, float] = UNSET
    mean_power_w: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_id = self.job_id

        name = self.name

        state = self.state

        state_reason: Union[None, Unset, str]
        if isinstance(self.state_reason, Unset):
            state_reason = UNSET
        else:
            state_reason = self.state_reason

        exit_code: Union[None, Unset, int]
        if isinstance(self.exit_code, Unset):
            exit_code = UNSET
        else:
            exit_code = self.exit_code

        account: Union[None, Unset, str]
        if isinstance(self.account, Unset):
            account = UNSET
        else:
            account = self.account

        partition: Union[None, Unset, str]
        if isinstance(self.partition, Unset):
            partition = UNSET
        else:
            partition = self.partition

        user: Union[None, Unset, str]
        if isinstance(self.user, Unset):
            user = UNSET
        else:
            user = self.user

        nodes: Union[None, Unset, str]
        if isinstance(self.nodes, Unset):
            nodes = UNSET
        else:
            nodes = self.nodes

        allocation_nodes: Union[None, Unset, int]
        if isinstance(self.allocation_nodes, Unset):
            allocation_nodes = UNSET
        else:
            allocation_nodes = self.allocation_nodes

        working_directory: Union[None, Unset, str]
        if isinstance(self.working_directory, Unset):
            working_directory = UNSET
        else:
            working_directory = self.working_directory

        start_time: Union[None, Unset, int]
        if isinstance(self.start_time, Unset):
            start_time = UNSET
        else:
            start_time = self.start_time

        end_time: Union[None, Unset, int]
        if isinstance(self.end_time, Unset):
            end_time = UNSET
        else:
            end_time = self.end_time

        elapsed: Union[None, Unset, int]
        if isinstance(self.elapsed, Unset):
            elapsed = UNSET
        else:
            elapsed = self.elapsed

        time_limit: Union[None, Unset, int]
        if isinstance(self.time_limit, Unset):
            time_limit = UNSET
        else:
            time_limit = self.time_limit

        submit_time: Union[None, Unset, int]
        if isinstance(self.submit_time, Unset):
            submit_time = UNSET
        else:
            submit_time = self.submit_time

        wait_seconds: Union[None, Unset, int]
        if isinstance(self.wait_seconds, Unset):
            wait_seconds = UNSET
        else:
            wait_seconds = self.wait_seconds

        allocation_cpus: Union[None, Unset, int]
        if isinstance(self.allocation_cpus, Unset):
            allocation_cpus = UNSET
        else:
            allocation_cpus = self.allocation_cpus

        requested_memory_mb: Union[None, Unset, int]
        if isinstance(self.requested_memory_mb, Unset):
            requested_memory_mb = UNSET
        else:
            requested_memory_mb = self.requested_memory_mb

        cpu_time_seconds: Union[None, Unset, int]
        if isinstance(self.cpu_time_seconds, Unset):
            cpu_time_seconds = UNSET
        else:
            cpu_time_seconds = self.cpu_time_seconds

        cpu_hours: Union[None, Unset, float]
        if isinstance(self.cpu_hours, Unset):
            cpu_hours = UNSET
        else:
            cpu_hours = self.cpu_hours

        cpu_efficiency: Union[None, Unset, float]
        if isinstance(self.cpu_efficiency, Unset):
            cpu_efficiency = UNSET
        else:
            cpu_efficiency = self.cpu_efficiency

        max_rss_mb: Union[None, Unset, int]
        if isinstance(self.max_rss_mb, Unset):
            max_rss_mb = UNSET
        else:
            max_rss_mb = self.max_rss_mb

        memory_efficiency: Union[None, Unset, float]
        if isinstance(self.memory_efficiency, Unset):
            memory_efficiency = UNSET
        else:
            memory_efficiency = self.memory_efficiency

        allocation_gpus: Union[None, Unset, int]
        if isinstance(self.allocation_gpus, Unset):
            allocation_gpus = UNSET
        else:
            allocation_gpus = self.allocation_gpus

        gpu_hours: Union[None, Unset, float]
        if isinstance(self.gpu_hours, Unset):
            gpu_hours = UNSET
        else:
            gpu_hours = self.gpu_hours

        energy_kwh: Union[None, Unset, float]
        if isinstance(self.energy_kwh, Unset):
            energy_kwh = UNSET
        else:
            energy_kwh = self.energy_kwh

        mean_power_w: Union[None, Unset, int]
        if isinstance(self.mean_power_w, Unset):
            mean_power_w = UNSET
        else:
            mean_power_w = self.mean_power_w

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_id": job_id,
                "name": name,
                "state": state,
            }
        )
        if state_reason is not UNSET:
            field_dict["state_reason"] = state_reason
        if exit_code is not UNSET:
            field_dict["exit_code"] = exit_code
        if account is not UNSET:
            field_dict["account"] = account
        if partition is not UNSET:
            field_dict["partition"] = partition
        if user is not UNSET:
            field_dict["user"] = user
        if nodes is not UNSET:
            field_dict["nodes"] = nodes
        if allocation_nodes is not UNSET:
            field_dict["allocation_nodes"] = allocation_nodes
        if working_directory is not UNSET:
            field_dict["working_directory"] = working_directory
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if elapsed is not UNSET:
            field_dict["elapsed"] = elapsed
        if time_limit is not UNSET:
            field_dict["time_limit"] = time_limit
        if submit_time is not UNSET:
            field_dict["submit_time"] = submit_time
        if wait_seconds is not UNSET:
            field_dict["wait_seconds"] = wait_seconds
        if allocation_cpus is not UNSET:
            field_dict["allocation_cpus"] = allocation_cpus
        if requested_memory_mb is not UNSET:
            field_dict["requested_memory_mb"] = requested_memory_mb
        if cpu_time_seconds is not UNSET:
            field_dict["cpu_time_seconds"] = cpu_time_seconds
        if cpu_hours is not UNSET:
            field_dict["cpu_hours"] = cpu_hours
        if cpu_efficiency is not UNSET:
            field_dict["cpu_efficiency"] = cpu_efficiency
        if max_rss_mb is not UNSET:
            field_dict["max_rss_mb"] = max_rss_mb
        if memory_efficiency is not UNSET:
            field_dict["memory_efficiency"] = memory_efficiency
        if allocation_gpus is not UNSET:
            field_dict["allocation_gpus"] = allocation_gpus
        if gpu_hours is not UNSET:
            field_dict["gpu_hours"] = gpu_hours
        if energy_kwh is not UNSET:
            field_dict["energy_kwh"] = energy_kwh
        if mean_power_w is not UNSET:
            field_dict["mean_power_w"] = mean_power_w

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_id = d.pop("job_id")

        name = d.pop("name")

        state = d.pop("state")

        def _parse_state_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        state_reason = _parse_state_reason(d.pop("state_reason", UNSET))

        def _parse_exit_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        exit_code = _parse_exit_code(d.pop("exit_code", UNSET))

        def _parse_account(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        account = _parse_account(d.pop("account", UNSET))

        def _parse_partition(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        partition = _parse_partition(d.pop("partition", UNSET))

        def _parse_user(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user = _parse_user(d.pop("user", UNSET))

        def _parse_nodes(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        nodes = _parse_nodes(d.pop("nodes", UNSET))

        def _parse_allocation_nodes(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        allocation_nodes = _parse_allocation_nodes(d.pop("allocation_nodes", UNSET))

        def _parse_working_directory(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        working_directory = _parse_working_directory(d.pop("working_directory", UNSET))

        def _parse_start_time(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        start_time = _parse_start_time(d.pop("start_time", UNSET))

        def _parse_end_time(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        end_time = _parse_end_time(d.pop("end_time", UNSET))

        def _parse_elapsed(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        elapsed = _parse_elapsed(d.pop("elapsed", UNSET))

        def _parse_time_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        time_limit = _parse_time_limit(d.pop("time_limit", UNSET))

        def _parse_submit_time(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        submit_time = _parse_submit_time(d.pop("submit_time", UNSET))

        def _parse_wait_seconds(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        wait_seconds = _parse_wait_seconds(d.pop("wait_seconds", UNSET))

        def _parse_allocation_cpus(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        allocation_cpus = _parse_allocation_cpus(d.pop("allocation_cpus", UNSET))

        def _parse_requested_memory_mb(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        requested_memory_mb = _parse_requested_memory_mb(d.pop("requested_memory_mb", UNSET))

        def _parse_cpu_time_seconds(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        cpu_time_seconds = _parse_cpu_time_seconds(d.pop("cpu_time_seconds", UNSET))

        def _parse_cpu_hours(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        cpu_hours = _parse_cpu_hours(d.pop("cpu_hours", UNSET))

        def _parse_cpu_efficiency(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        cpu_efficiency = _parse_cpu_efficiency(d.pop("cpu_efficiency", UNSET))

        def _parse_max_rss_mb(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_rss_mb = _parse_max_rss_mb(d.pop("max_rss_mb", UNSET))

        def _parse_memory_efficiency(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        memory_efficiency = _parse_memory_efficiency(d.pop("memory_efficiency", UNSET))

        def _parse_allocation_gpus(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        allocation_gpus = _parse_allocation_gpus(d.pop("allocation_gpus", UNSET))

        def _parse_gpu_hours(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        gpu_hours = _parse_gpu_hours(d.pop("gpu_hours", UNSET))

        def _parse_energy_kwh(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        energy_kwh = _parse_energy_kwh(d.pop("energy_kwh", UNSET))

        def _parse_mean_power_w(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        mean_power_w = _parse_mean_power_w(d.pop("mean_power_w", UNSET))

        hpc_job = cls(
            job_id=job_id,
            name=name,
            state=state,
            state_reason=state_reason,
            exit_code=exit_code,
            account=account,
            partition=partition,
            user=user,
            nodes=nodes,
            allocation_nodes=allocation_nodes,
            working_directory=working_directory,
            start_time=start_time,
            end_time=end_time,
            elapsed=elapsed,
            time_limit=time_limit,
            submit_time=submit_time,
            wait_seconds=wait_seconds,
            allocation_cpus=allocation_cpus,
            requested_memory_mb=requested_memory_mb,
            cpu_time_seconds=cpu_time_seconds,
            cpu_hours=cpu_hours,
            cpu_efficiency=cpu_efficiency,
            max_rss_mb=max_rss_mb,
            memory_efficiency=memory_efficiency,
            allocation_gpus=allocation_gpus,
            gpu_hours=gpu_hours,
            energy_kwh=energy_kwh,
            mean_power_w=mean_power_w,
        )

        hpc_job.additional_properties = d
        return hpc_job

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
