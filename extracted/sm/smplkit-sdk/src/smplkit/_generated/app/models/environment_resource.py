from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.environment_resource_type import check_environment_resource_type
from ..models.environment_resource_type import EnvironmentResourceType
from typing import cast

if TYPE_CHECKING:
    from ..models.environment import Environment


T = TypeVar("T", bound="EnvironmentResource")


@_attrs_define
class EnvironmentResource:
    """JSON:API resource envelope for an environment.

    `id` must not be specified for create requests (the server assigns it).

        Example:
            {'attributes': {'classification': 'STANDARD', 'color': '#2ecc71', 'created_at': '2026-03-20T11:02:16.616Z',
                'managed': True, 'name': 'Production', 'updated_at': '2026-03-20T11:02:16.616Z'}, 'id': 'production', 'type':
                'environment'}

        Attributes:
            type_ (EnvironmentResourceType):
            attributes (Environment): A named deployment context — for example, `production`, `staging`, or
                `development`. Resources scoped to an environment (such as config items
                and feature flags) are evaluated against environment-specific values. Example: {'classification': 'STANDARD',
                'color': '#2ecc71', 'created_at': '2026-03-20T11:02:16.616Z', 'managed': True, 'name': 'Production',
                'updated_at': '2026-03-20T11:02:16.616Z'}.
            id (None | str | Unset):
    """

    type_: EnvironmentResourceType
    attributes: Environment
    id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        attributes = self.attributes.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.environment import Environment

        d = dict(src_dict)
        type_ = check_environment_resource_type(d.pop("type"))

        attributes = Environment.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        environment_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        environment_resource.additional_properties = d
        return environment_resource

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
