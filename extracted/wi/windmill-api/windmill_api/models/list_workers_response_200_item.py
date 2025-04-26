import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListWorkersResponse200Item")


@_attrs_define
class ListWorkersResponse200Item:
    """
    Attributes:
        worker (str):
        worker_instance (str):
        started_at (datetime.datetime):
        ip (str):
        jobs_executed (int):
        worker_group (str):
        wm_version (str):
        last_ping (Union[Unset, float]):
        custom_tags (Union[Unset, List[str]]):
        last_job_id (Union[Unset, str]):
        last_job_workspace_id (Union[Unset, str]):
        occupancy_rate (Union[Unset, float]):
        occupancy_rate_15s (Union[Unset, float]):
        occupancy_rate_5m (Union[Unset, float]):
        occupancy_rate_30m (Union[Unset, float]):
        memory (Union[Unset, float]):
        vcpus (Union[Unset, float]):
        memory_usage (Union[Unset, float]):
        wm_memory_usage (Union[Unset, float]):
    """

    worker: str
    worker_instance: str
    started_at: datetime.datetime
    ip: str
    jobs_executed: int
    worker_group: str
    wm_version: str
    last_ping: Union[Unset, float] = UNSET
    custom_tags: Union[Unset, List[str]] = UNSET
    last_job_id: Union[Unset, str] = UNSET
    last_job_workspace_id: Union[Unset, str] = UNSET
    occupancy_rate: Union[Unset, float] = UNSET
    occupancy_rate_15s: Union[Unset, float] = UNSET
    occupancy_rate_5m: Union[Unset, float] = UNSET
    occupancy_rate_30m: Union[Unset, float] = UNSET
    memory: Union[Unset, float] = UNSET
    vcpus: Union[Unset, float] = UNSET
    memory_usage: Union[Unset, float] = UNSET
    wm_memory_usage: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        worker = self.worker
        worker_instance = self.worker_instance
        started_at = self.started_at.isoformat()

        ip = self.ip
        jobs_executed = self.jobs_executed
        worker_group = self.worker_group
        wm_version = self.wm_version
        last_ping = self.last_ping
        custom_tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.custom_tags, Unset):
            custom_tags = self.custom_tags

        last_job_id = self.last_job_id
        last_job_workspace_id = self.last_job_workspace_id
        occupancy_rate = self.occupancy_rate
        occupancy_rate_15s = self.occupancy_rate_15s
        occupancy_rate_5m = self.occupancy_rate_5m
        occupancy_rate_30m = self.occupancy_rate_30m
        memory = self.memory
        vcpus = self.vcpus
        memory_usage = self.memory_usage
        wm_memory_usage = self.wm_memory_usage

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "worker": worker,
                "worker_instance": worker_instance,
                "started_at": started_at,
                "ip": ip,
                "jobs_executed": jobs_executed,
                "worker_group": worker_group,
                "wm_version": wm_version,
            }
        )
        if last_ping is not UNSET:
            field_dict["last_ping"] = last_ping
        if custom_tags is not UNSET:
            field_dict["custom_tags"] = custom_tags
        if last_job_id is not UNSET:
            field_dict["last_job_id"] = last_job_id
        if last_job_workspace_id is not UNSET:
            field_dict["last_job_workspace_id"] = last_job_workspace_id
        if occupancy_rate is not UNSET:
            field_dict["occupancy_rate"] = occupancy_rate
        if occupancy_rate_15s is not UNSET:
            field_dict["occupancy_rate_15s"] = occupancy_rate_15s
        if occupancy_rate_5m is not UNSET:
            field_dict["occupancy_rate_5m"] = occupancy_rate_5m
        if occupancy_rate_30m is not UNSET:
            field_dict["occupancy_rate_30m"] = occupancy_rate_30m
        if memory is not UNSET:
            field_dict["memory"] = memory
        if vcpus is not UNSET:
            field_dict["vcpus"] = vcpus
        if memory_usage is not UNSET:
            field_dict["memory_usage"] = memory_usage
        if wm_memory_usage is not UNSET:
            field_dict["wm_memory_usage"] = wm_memory_usage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        worker = d.pop("worker")

        worker_instance = d.pop("worker_instance")

        started_at = isoparse(d.pop("started_at"))

        ip = d.pop("ip")

        jobs_executed = d.pop("jobs_executed")

        worker_group = d.pop("worker_group")

        wm_version = d.pop("wm_version")

        last_ping = d.pop("last_ping", UNSET)

        custom_tags = cast(List[str], d.pop("custom_tags", UNSET))

        last_job_id = d.pop("last_job_id", UNSET)

        last_job_workspace_id = d.pop("last_job_workspace_id", UNSET)

        occupancy_rate = d.pop("occupancy_rate", UNSET)

        occupancy_rate_15s = d.pop("occupancy_rate_15s", UNSET)

        occupancy_rate_5m = d.pop("occupancy_rate_5m", UNSET)

        occupancy_rate_30m = d.pop("occupancy_rate_30m", UNSET)

        memory = d.pop("memory", UNSET)

        vcpus = d.pop("vcpus", UNSET)

        memory_usage = d.pop("memory_usage", UNSET)

        wm_memory_usage = d.pop("wm_memory_usage", UNSET)

        list_workers_response_200_item = cls(
            worker=worker,
            worker_instance=worker_instance,
            started_at=started_at,
            ip=ip,
            jobs_executed=jobs_executed,
            worker_group=worker_group,
            wm_version=wm_version,
            last_ping=last_ping,
            custom_tags=custom_tags,
            last_job_id=last_job_id,
            last_job_workspace_id=last_job_workspace_id,
            occupancy_rate=occupancy_rate,
            occupancy_rate_15s=occupancy_rate_15s,
            occupancy_rate_5m=occupancy_rate_5m,
            occupancy_rate_30m=occupancy_rate_30m,
            memory=memory,
            vcpus=vcpus,
            memory_usage=memory_usage,
            wm_memory_usage=wm_memory_usage,
        )

        list_workers_response_200_item.additional_properties = d
        return list_workers_response_200_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
