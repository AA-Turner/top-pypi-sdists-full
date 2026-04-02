from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ImportRemoteGroupRequest")


@_attrs_define
class ImportRemoteGroupRequest:
    """
    Attributes:
        offering_uuid (UUID):
        role_uuid (UUID):
        remote_group_id (str):
        resource_uuid (Union[None, UUID, Unset]):
        scope_id (Union[Unset, str]):  Default: ''.
    """

    offering_uuid: UUID
    role_uuid: UUID
    remote_group_id: str
    resource_uuid: Union[None, UUID, Unset] = UNSET
    scope_id: Union[Unset, str] = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_uuid = str(self.offering_uuid)

        role_uuid = str(self.role_uuid)

        remote_group_id = self.remote_group_id

        resource_uuid: Union[None, Unset, str]
        if isinstance(self.resource_uuid, Unset):
            resource_uuid = UNSET
        elif isinstance(self.resource_uuid, UUID):
            resource_uuid = str(self.resource_uuid)
        else:
            resource_uuid = self.resource_uuid

        scope_id = self.scope_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_uuid": offering_uuid,
                "role_uuid": role_uuid,
                "remote_group_id": remote_group_id,
            }
        )
        if resource_uuid is not UNSET:
            field_dict["resource_uuid"] = resource_uuid
        if scope_id is not UNSET:
            field_dict["scope_id"] = scope_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offering_uuid = UUID(d.pop("offering_uuid"))

        role_uuid = UUID(d.pop("role_uuid"))

        remote_group_id = d.pop("remote_group_id")

        def _parse_resource_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resource_uuid_type_0 = UUID(data)

                return resource_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        resource_uuid = _parse_resource_uuid(d.pop("resource_uuid", UNSET))

        scope_id = d.pop("scope_id", UNSET)

        import_remote_group_request = cls(
            offering_uuid=offering_uuid,
            role_uuid=role_uuid,
            remote_group_id=remote_group_id,
            resource_uuid=resource_uuid,
            scope_id=scope_id,
        )

        import_remote_group_request.additional_properties = d
        return import_remote_group_request

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
