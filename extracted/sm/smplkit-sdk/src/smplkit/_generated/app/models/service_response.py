from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.service_resource import ServiceResource


T = TypeVar("T", bound="ServiceResponse")


@_attrs_define
class ServiceResponse:
    """JSON:API single-resource response envelope for a service.

    Attributes:
        data (ServiceResource): JSON:API resource envelope for a service.

            The caller supplies ``id`` (the service's key) on create. Example: {'attributes': {'created_at':
            '2026-03-20T11:02:16.616Z', 'name': 'User Service', 'updated_at': '2026-03-20T11:02:16.616Z'}, 'id':
            'user_service', 'type': 'service'}.
    """

    data: ServiceResource
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
        from ..models.service_resource import ServiceResource

        d = dict(src_dict)
        data = ServiceResource.from_dict(d.pop("data"))

        service_response = cls(
            data=data,
        )

        service_response.additional_properties = d
        return service_response

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
