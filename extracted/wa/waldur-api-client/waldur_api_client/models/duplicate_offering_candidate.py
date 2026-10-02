from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DuplicateOfferingCandidate")


@_attrs_define
class DuplicateOfferingCandidate:
    """
    Attributes:
        id (int):
        uuid (UUID):
        name (str):
        state (str):
        active_resources (int):
        total_resources (int):
        is_recommended_keeper (bool):
    """

    id: int
    uuid: UUID
    name: str
    state: str
    active_resources: int
    total_resources: int
    is_recommended_keeper: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        uuid = str(self.uuid)

        name = self.name

        state = self.state

        active_resources = self.active_resources

        total_resources = self.total_resources

        is_recommended_keeper = self.is_recommended_keeper

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "uuid": uuid,
                "name": name,
                "state": state,
                "active_resources": active_resources,
                "total_resources": total_resources,
                "is_recommended_keeper": is_recommended_keeper,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        state = d.pop("state")

        active_resources = d.pop("active_resources")

        total_resources = d.pop("total_resources")

        is_recommended_keeper = d.pop("is_recommended_keeper")

        duplicate_offering_candidate = cls(
            id=id,
            uuid=uuid,
            name=name,
            state=state,
            active_resources=active_resources,
            total_resources=total_resources,
            is_recommended_keeper=is_recommended_keeper,
        )

        duplicate_offering_candidate.additional_properties = d
        return duplicate_offering_candidate

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
