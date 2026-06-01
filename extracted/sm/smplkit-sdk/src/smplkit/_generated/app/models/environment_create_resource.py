from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.environment_create_resource_type import check_environment_create_resource_type
from ..models.environment_create_resource_type import EnvironmentCreateResourceType

if TYPE_CHECKING:
    from ..models.environment import Environment


T = TypeVar("T", bound="EnvironmentCreateResource")


@_attrs_define
class EnvironmentCreateResource:
    """JSON:API resource envelope for creating an environment (id required).

    Example:
        {'attributes': {'name': 'Production'}, 'id': 'production', 'type': 'environment'}

    Attributes:
        id (str): Client-supplied resource id.
        type_ (EnvironmentCreateResourceType):
        attributes (Environment): A named deployment context — for example, `production`, `staging`, or
            `development`. Resources scoped to an environment (such as config items
            and feature flags) are evaluated against environment-specific values. Example: {'classification': 'STANDARD',
            'color': '#2ecc71', 'created_at': '2026-03-20T11:02:16.616Z', 'managed': True, 'name': 'Production',
            'updated_at': '2026-03-20T11:02:16.616Z'}.
    """

    id: str
    type_: EnvironmentCreateResourceType
    attributes: Environment
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_: str = self.type_

        attributes = self.attributes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
                "attributes": attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.environment import Environment

        d = dict(src_dict)
        id = d.pop("id")

        type_ = check_environment_create_resource_type(d.pop("type"))

        attributes = Environment.from_dict(d.pop("attributes"))

        environment_create_resource = cls(
            id=id,
            type_=type_,
            attributes=attributes,
        )

        environment_create_resource.additional_properties = d
        return environment_create_resource

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
