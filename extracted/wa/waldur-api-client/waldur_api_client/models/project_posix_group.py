from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.project_posix_group_kind_enum import ProjectPosixGroupKindEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.service_provider_project_group_offering import ServiceProviderProjectGroupOffering


T = TypeVar("T", bound="ProjectPosixGroup")


@_attrs_define
class ProjectPosixGroup:
    """
    Attributes:
        kind (ProjectPosixGroupKindEnum):
        gid (Union[None, int]):
        offering_uuid (Union[None, str]):
        offering_name (Union[None, str]):
        provider_name (str):
        role (Union[None, str]):
        scope_type (Union[None, str]):
        scope_name (Union[None, str]):
        scope_uuid (Union[None, str]):
        group_uuid (Union[None, Unset, str]):
        group_name (Union[None, Unset, str]):
        service_provider_uuid (Union[None, Unset, str]):
        in_use (Union[None, Unset, bool]):
        offerings (Union[Unset, list['ServiceProviderProjectGroupOffering']]):
        members (Union[Unset, list[str]]):
        member_count (Union[None, Unset, int]):
    """

    kind: ProjectPosixGroupKindEnum
    gid: Union[None, int]
    offering_uuid: Union[None, str]
    offering_name: Union[None, str]
    provider_name: str
    role: Union[None, str]
    scope_type: Union[None, str]
    scope_name: Union[None, str]
    scope_uuid: Union[None, str]
    group_uuid: Union[None, Unset, str] = UNSET
    group_name: Union[None, Unset, str] = UNSET
    service_provider_uuid: Union[None, Unset, str] = UNSET
    in_use: Union[None, Unset, bool] = UNSET
    offerings: Union[Unset, list["ServiceProviderProjectGroupOffering"]] = UNSET
    members: Union[Unset, list[str]] = UNSET
    member_count: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        gid: Union[None, int]
        gid = self.gid

        offering_uuid: Union[None, str]
        offering_uuid = self.offering_uuid

        offering_name: Union[None, str]
        offering_name = self.offering_name

        provider_name = self.provider_name

        role: Union[None, str]
        role = self.role

        scope_type: Union[None, str]
        scope_type = self.scope_type

        scope_name: Union[None, str]
        scope_name = self.scope_name

        scope_uuid: Union[None, str]
        scope_uuid = self.scope_uuid

        group_uuid: Union[None, Unset, str]
        if isinstance(self.group_uuid, Unset):
            group_uuid = UNSET
        else:
            group_uuid = self.group_uuid

        group_name: Union[None, Unset, str]
        if isinstance(self.group_name, Unset):
            group_name = UNSET
        else:
            group_name = self.group_name

        service_provider_uuid: Union[None, Unset, str]
        if isinstance(self.service_provider_uuid, Unset):
            service_provider_uuid = UNSET
        else:
            service_provider_uuid = self.service_provider_uuid

        in_use: Union[None, Unset, bool]
        if isinstance(self.in_use, Unset):
            in_use = UNSET
        else:
            in_use = self.in_use

        offerings: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.offerings, Unset):
            offerings = []
            for offerings_item_data in self.offerings:
                offerings_item = offerings_item_data.to_dict()
                offerings.append(offerings_item)

        members: Union[Unset, list[str]] = UNSET
        if not isinstance(self.members, Unset):
            members = self.members

        member_count: Union[None, Unset, int]
        if isinstance(self.member_count, Unset):
            member_count = UNSET
        else:
            member_count = self.member_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "gid": gid,
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "provider_name": provider_name,
                "role": role,
                "scope_type": scope_type,
                "scope_name": scope_name,
                "scope_uuid": scope_uuid,
            }
        )
        if group_uuid is not UNSET:
            field_dict["group_uuid"] = group_uuid
        if group_name is not UNSET:
            field_dict["group_name"] = group_name
        if service_provider_uuid is not UNSET:
            field_dict["service_provider_uuid"] = service_provider_uuid
        if in_use is not UNSET:
            field_dict["in_use"] = in_use
        if offerings is not UNSET:
            field_dict["offerings"] = offerings
        if members is not UNSET:
            field_dict["members"] = members
        if member_count is not UNSET:
            field_dict["member_count"] = member_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.service_provider_project_group_offering import ServiceProviderProjectGroupOffering

        d = dict(src_dict)
        kind = ProjectPosixGroupKindEnum(d.pop("kind"))

        def _parse_gid(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        gid = _parse_gid(d.pop("gid"))

        def _parse_offering_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        offering_uuid = _parse_offering_uuid(d.pop("offering_uuid"))

        def _parse_offering_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        offering_name = _parse_offering_name(d.pop("offering_name"))

        provider_name = d.pop("provider_name")

        def _parse_role(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        role = _parse_role(d.pop("role"))

        def _parse_scope_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        scope_type = _parse_scope_type(d.pop("scope_type"))

        def _parse_scope_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        scope_name = _parse_scope_name(d.pop("scope_name"))

        def _parse_scope_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        scope_uuid = _parse_scope_uuid(d.pop("scope_uuid"))

        def _parse_group_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        group_uuid = _parse_group_uuid(d.pop("group_uuid", UNSET))

        def _parse_group_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        group_name = _parse_group_name(d.pop("group_name", UNSET))

        def _parse_service_provider_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        service_provider_uuid = _parse_service_provider_uuid(d.pop("service_provider_uuid", UNSET))

        def _parse_in_use(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        in_use = _parse_in_use(d.pop("in_use", UNSET))

        offerings = []
        _offerings = d.pop("offerings", UNSET)
        for offerings_item_data in _offerings or []:
            offerings_item = ServiceProviderProjectGroupOffering.from_dict(offerings_item_data)

            offerings.append(offerings_item)

        members = cast(list[str], d.pop("members", UNSET))

        def _parse_member_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        member_count = _parse_member_count(d.pop("member_count", UNSET))

        project_posix_group = cls(
            kind=kind,
            gid=gid,
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            provider_name=provider_name,
            role=role,
            scope_type=scope_type,
            scope_name=scope_name,
            scope_uuid=scope_uuid,
            group_uuid=group_uuid,
            group_name=group_name,
            service_provider_uuid=service_provider_uuid,
            in_use=in_use,
            offerings=offerings,
            members=members,
            member_count=member_count,
        )

        project_posix_group.additional_properties = d
        return project_posix_group

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
