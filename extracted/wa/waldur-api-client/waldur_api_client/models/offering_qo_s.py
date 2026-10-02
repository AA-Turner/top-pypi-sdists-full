import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingQoS")


@_attrs_define
class OfferingQoS:
    """
    Attributes:
        uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        offering (UUID):
        offering_name (str):
        name (str): Name of the SLURM QOS.
        description (Union[Unset, str]):
        max_nodes (Union[None, Unset, int]): Maximum nodes per job
        min_nodes (Union[None, Unset, int]): Minimum nodes per job
        default_time (Union[None, Unset, int]): Default time limit in minutes
        max_time (Union[None, Unset, int]): Maximum wall time in minutes
        grace_time (Union[None, Unset, int]): Preemption grace time in seconds
        priority (Union[None, Unset, int]): Scheduling priority
        grp_tres (Union[Unset, str]): Aggregate TRES the QOS may allocate at once (GrpTRES)
        max_tres_per_job (Union[Unset, str]): Max TRES per job (MaxTRESPerJob)
        max_tres_per_node (Union[Unset, str]): Max TRES per node (MaxTRESPerNode)
        max_tres_per_user (Union[Unset, str]): Max TRES per user (MaxTRESPerUser)
        min_tres_per_job (Union[Unset, str]): Min TRES per job (MinTRESPerJob)
        flags (Union[Unset, str]): Comma-separated QOS flags (e.g. DenyOnLimit, OverPartQOS)
    """

    uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    offering: UUID
    offering_name: str
    name: str
    description: Union[Unset, str] = UNSET
    max_nodes: Union[None, Unset, int] = UNSET
    min_nodes: Union[None, Unset, int] = UNSET
    default_time: Union[None, Unset, int] = UNSET
    max_time: Union[None, Unset, int] = UNSET
    grace_time: Union[None, Unset, int] = UNSET
    priority: Union[None, Unset, int] = UNSET
    grp_tres: Union[Unset, str] = UNSET
    max_tres_per_job: Union[Unset, str] = UNSET
    max_tres_per_node: Union[Unset, str] = UNSET
    max_tres_per_user: Union[Unset, str] = UNSET
    min_tres_per_job: Union[Unset, str] = UNSET
    flags: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        offering = str(self.offering)

        offering_name = self.offering_name

        name = self.name

        description = self.description

        max_nodes: Union[None, Unset, int]
        if isinstance(self.max_nodes, Unset):
            max_nodes = UNSET
        else:
            max_nodes = self.max_nodes

        min_nodes: Union[None, Unset, int]
        if isinstance(self.min_nodes, Unset):
            min_nodes = UNSET
        else:
            min_nodes = self.min_nodes

        default_time: Union[None, Unset, int]
        if isinstance(self.default_time, Unset):
            default_time = UNSET
        else:
            default_time = self.default_time

        max_time: Union[None, Unset, int]
        if isinstance(self.max_time, Unset):
            max_time = UNSET
        else:
            max_time = self.max_time

        grace_time: Union[None, Unset, int]
        if isinstance(self.grace_time, Unset):
            grace_time = UNSET
        else:
            grace_time = self.grace_time

        priority: Union[None, Unset, int]
        if isinstance(self.priority, Unset):
            priority = UNSET
        else:
            priority = self.priority

        grp_tres = self.grp_tres

        max_tres_per_job = self.max_tres_per_job

        max_tres_per_node = self.max_tres_per_node

        max_tres_per_user = self.max_tres_per_user

        min_tres_per_job = self.min_tres_per_job

        flags = self.flags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "created": created,
                "modified": modified,
                "offering": offering,
                "offering_name": offering_name,
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if max_nodes is not UNSET:
            field_dict["max_nodes"] = max_nodes
        if min_nodes is not UNSET:
            field_dict["min_nodes"] = min_nodes
        if default_time is not UNSET:
            field_dict["default_time"] = default_time
        if max_time is not UNSET:
            field_dict["max_time"] = max_time
        if grace_time is not UNSET:
            field_dict["grace_time"] = grace_time
        if priority is not UNSET:
            field_dict["priority"] = priority
        if grp_tres is not UNSET:
            field_dict["grp_tres"] = grp_tres
        if max_tres_per_job is not UNSET:
            field_dict["max_tres_per_job"] = max_tres_per_job
        if max_tres_per_node is not UNSET:
            field_dict["max_tres_per_node"] = max_tres_per_node
        if max_tres_per_user is not UNSET:
            field_dict["max_tres_per_user"] = max_tres_per_user
        if min_tres_per_job is not UNSET:
            field_dict["min_tres_per_job"] = min_tres_per_job
        if flags is not UNSET:
            field_dict["flags"] = flags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        offering = UUID(d.pop("offering"))

        offering_name = d.pop("offering_name")

        name = d.pop("name")

        description = d.pop("description", UNSET)

        def _parse_max_nodes(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_nodes = _parse_max_nodes(d.pop("max_nodes", UNSET))

        def _parse_min_nodes(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        min_nodes = _parse_min_nodes(d.pop("min_nodes", UNSET))

        def _parse_default_time(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        default_time = _parse_default_time(d.pop("default_time", UNSET))

        def _parse_max_time(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_time = _parse_max_time(d.pop("max_time", UNSET))

        def _parse_grace_time(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        grace_time = _parse_grace_time(d.pop("grace_time", UNSET))

        def _parse_priority(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        priority = _parse_priority(d.pop("priority", UNSET))

        grp_tres = d.pop("grp_tres", UNSET)

        max_tres_per_job = d.pop("max_tres_per_job", UNSET)

        max_tres_per_node = d.pop("max_tres_per_node", UNSET)

        max_tres_per_user = d.pop("max_tres_per_user", UNSET)

        min_tres_per_job = d.pop("min_tres_per_job", UNSET)

        flags = d.pop("flags", UNSET)

        offering_qo_s = cls(
            uuid=uuid,
            created=created,
            modified=modified,
            offering=offering,
            offering_name=offering_name,
            name=name,
            description=description,
            max_nodes=max_nodes,
            min_nodes=min_nodes,
            default_time=default_time,
            max_time=max_time,
            grace_time=grace_time,
            priority=priority,
            grp_tres=grp_tres,
            max_tres_per_job=max_tres_per_job,
            max_tres_per_node=max_tres_per_node,
            max_tres_per_user=max_tres_per_user,
            min_tres_per_job=min_tres_per_job,
            flags=flags,
        )

        offering_qo_s.additional_properties = d
        return offering_qo_s

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
