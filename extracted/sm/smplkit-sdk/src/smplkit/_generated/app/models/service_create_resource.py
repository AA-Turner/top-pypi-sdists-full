from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.service_create_resource_type import check_service_create_resource_type
from ..models.service_create_resource_type import ServiceCreateResourceType

if TYPE_CHECKING:
    from ..models.service import Service


T = TypeVar("T", bound="ServiceCreateResource")


@_attrs_define
class ServiceCreateResource:
    """JSON:API resource envelope for creating a service (id required).

    Example:
        {'attributes': {'name': 'User Service'}, 'id': 'user_service', 'type': 'service'}

    Attributes:
        id (str): Client-supplied resource id.
        type_ (ServiceCreateResourceType):
        attributes (Service): A service that contexts can be evaluated against — for example, a
            backend application or microservice in the customer's stack. Example: {'created_at': '2026-03-20T11:02:16.616Z',
            'name': 'User Service', 'updated_at': '2026-03-20T11:02:16.616Z'}.
    """

    id: str
    type_: ServiceCreateResourceType
    attributes: Service
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
        from ..models.service import Service

        d = dict(src_dict)
        id = d.pop("id")

        type_ = check_service_create_resource_type(d.pop("type"))

        attributes = Service.from_dict(d.pop("attributes"))

        service_create_resource = cls(
            id=id,
            type_=type_,
            attributes=attributes,
        )

        service_create_resource.additional_properties = d
        return service_create_resource

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
