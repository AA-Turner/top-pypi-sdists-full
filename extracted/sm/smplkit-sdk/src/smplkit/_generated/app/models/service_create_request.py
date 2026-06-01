from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.service_create_resource import ServiceCreateResource


T = TypeVar("T", bound="ServiceCreateRequest")


@_attrs_define
class ServiceCreateRequest:
    """JSON:API request envelope for creating a service.

    Distinct from :class:`ServiceRequest` because create requires
    caller-supplied ``data.id`` while update does not.

        Attributes:
            data (ServiceCreateResource): JSON:API resource envelope for creating a service (id required). Example:
                {'attributes': {'name': 'User Service'}, 'id': 'user_service', 'type': 'service'}.
    """

    data: ServiceCreateResource
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
        from ..models.service_create_resource import ServiceCreateResource

        d = dict(src_dict)
        data = ServiceCreateResource.from_dict(d.pop("data"))

        service_create_request = cls(
            data=data,
        )

        service_create_request.additional_properties = d
        return service_create_request

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
