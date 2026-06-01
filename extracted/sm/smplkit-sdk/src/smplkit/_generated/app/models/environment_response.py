from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.environment_resource import EnvironmentResource


T = TypeVar("T", bound="EnvironmentResponse")


@_attrs_define
class EnvironmentResponse:
    """JSON:API single-resource response envelope for an environment.

    Attributes:
        data (EnvironmentResource): JSON:API resource envelope for an environment.

            `id` must not be specified for create requests (the server assigns it). Example: {'attributes':
            {'classification': 'STANDARD', 'color': '#2ecc71', 'created_at': '2026-03-20T11:02:16.616Z', 'managed': True,
            'name': 'Production', 'updated_at': '2026-03-20T11:02:16.616Z'}, 'id': 'production', 'type': 'environment'}.
    """

    data: EnvironmentResource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.environment_resource import EnvironmentResource

        d = dict(src_dict)
        data = EnvironmentResource.from_dict(d.pop("data"))

        environment_response = cls(
            data=data,
        )

        environment_response.additional_properties = d
        return environment_response

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
