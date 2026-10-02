import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.offering_profile_role import OfferingProfileRole


T = TypeVar("T", bound="OfferingProfile")


@_attrs_define
class OfferingProfile:
    """
    Attributes:
        uuid (UUID):
        name (str):
        roles (list['OfferingProfileRole']):
        offerings_count (int):
        created (datetime.datetime):
        modified (datetime.datetime):
        description (Union[Unset, str]):
    """

    uuid: UUID
    name: str
    roles: list["OfferingProfileRole"]
    offerings_count: int
    created: datetime.datetime
    modified: datetime.datetime
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        roles = []
        for roles_item_data in self.roles:
            roles_item = roles_item_data.to_dict()
            roles.append(roles_item)

        offerings_count = self.offerings_count

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "roles": roles,
                "offerings_count": offerings_count,
                "created": created,
                "modified": modified,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_profile_role import OfferingProfileRole

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        roles = []
        _roles = d.pop("roles")
        for roles_item_data in _roles:
            roles_item = OfferingProfileRole.from_dict(roles_item_data)

            roles.append(roles_item)

        offerings_count = d.pop("offerings_count")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        description = d.pop("description", UNSET)

        offering_profile = cls(
            uuid=uuid,
            name=name,
            roles=roles,
            offerings_count=offerings_count,
            created=created,
            modified=modified,
            description=description,
        )

        offering_profile.additional_properties = d
        return offering_profile

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
