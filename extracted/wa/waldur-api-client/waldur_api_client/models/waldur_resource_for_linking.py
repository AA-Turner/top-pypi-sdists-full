from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WaldurResourceForLinking")


@_attrs_define
class WaldurResourceForLinking:
    """
    Attributes:
        uuid (UUID):
        name (str):
        backend_id (str): Current backend_id (Arrow license reference if linked).
        project_name (str):
        offering_name (str):
        state (str):
    """

    uuid: UUID
    name: str
    backend_id: str
    project_name: str
    offering_name: str
    state: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        backend_id = self.backend_id

        project_name = self.project_name

        offering_name = self.offering_name

        state = self.state

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "backend_id": backend_id,
                "project_name": project_name,
                "offering_name": offering_name,
                "state": state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        backend_id = d.pop("backend_id")

        project_name = d.pop("project_name")

        offering_name = d.pop("offering_name")

        state = d.pop("state")

        waldur_resource_for_linking = cls(
            uuid=uuid,
            name=name,
            backend_id=backend_id,
            project_name=project_name,
            offering_name=offering_name,
            state=state,
        )

        waldur_resource_for_linking.additional_properties = d
        return waldur_resource_for_linking

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
