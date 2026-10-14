import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.sram_group_kind_enum import SramGroupKindEnum

T = TypeVar("T", bound="SramGroup")


@_attrs_define
class SramGroup:
    """
    Attributes:
        uuid (UUID):
        external_id (str):
        display_name (str):
        urn (str): SRAM global URN: '<organisation>:<co>' or '<organisation>:<co>:<group>'.
        kind (SramGroupKindEnum):
        description (str):
        labels (list[str]):
        customer_uuid (Union[None, UUID]):
        customer_name (Union[None, str]):
        role_uuid (Union[None, UUID]):
        role_name (Union[None, str]):
        member_count (int):
        created (datetime.datetime):
        modified (datetime.datetime):
    """

    uuid: UUID
    external_id: str
    display_name: str
    urn: str
    kind: SramGroupKindEnum
    description: str
    labels: list[str]
    customer_uuid: Union[None, UUID]
    customer_name: Union[None, str]
    role_uuid: Union[None, UUID]
    role_name: Union[None, str]
    member_count: int
    created: datetime.datetime
    modified: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        external_id = self.external_id

        display_name = self.display_name

        urn = self.urn

        kind = self.kind.value

        description = self.description

        labels = self.labels

        customer_uuid: Union[None, str]
        if isinstance(self.customer_uuid, UUID):
            customer_uuid = str(self.customer_uuid)
        else:
            customer_uuid = self.customer_uuid

        customer_name: Union[None, str]
        customer_name = self.customer_name

        role_uuid: Union[None, str]
        if isinstance(self.role_uuid, UUID):
            role_uuid = str(self.role_uuid)
        else:
            role_uuid = self.role_uuid

        role_name: Union[None, str]
        role_name = self.role_name

        member_count = self.member_count

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "external_id": external_id,
                "display_name": display_name,
                "urn": urn,
                "kind": kind,
                "description": description,
                "labels": labels,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "role_uuid": role_uuid,
                "role_name": role_name,
                "member_count": member_count,
                "created": created,
                "modified": modified,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        external_id = d.pop("external_id")

        display_name = d.pop("display_name")

        urn = d.pop("urn")

        kind = SramGroupKindEnum(d.pop("kind"))

        description = d.pop("description")

        labels = cast(list[str], d.pop("labels"))

        def _parse_customer_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                customer_uuid_type_0 = UUID(data)

                return customer_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        customer_uuid = _parse_customer_uuid(d.pop("customer_uuid"))

        def _parse_customer_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        customer_name = _parse_customer_name(d.pop("customer_name"))

        def _parse_role_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                role_uuid_type_0 = UUID(data)

                return role_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        role_uuid = _parse_role_uuid(d.pop("role_uuid"))

        def _parse_role_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        role_name = _parse_role_name(d.pop("role_name"))

        member_count = d.pop("member_count")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        sram_group = cls(
            uuid=uuid,
            external_id=external_id,
            display_name=display_name,
            urn=urn,
            kind=kind,
            description=description,
            labels=labels,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            role_uuid=role_uuid,
            role_name=role_name,
            member_count=member_count,
            created=created,
            modified=modified,
        )

        sram_group.additional_properties = d
        return sram_group

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
