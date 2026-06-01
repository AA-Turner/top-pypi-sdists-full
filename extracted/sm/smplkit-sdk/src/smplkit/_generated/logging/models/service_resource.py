from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Literal

if TYPE_CHECKING:
    from ..models.service_attributes import ServiceAttributes


T = TypeVar("T", bound="ServiceResource")


@_attrs_define
class ServiceResource:
    """JSON:API resource envelope for a discovered service.

    `id` is the service name as reported by an SDK during bulk
    registration. The resource carries no additional attributes — it
    represents the existence of the service in the account's
    observations, nothing more.

        Example:
            {'attributes': {}, 'id': 'api-gateway', 'type': 'service'}

        Attributes:
            id (str):
            type_ (Literal['service']):
            attributes (ServiceAttributes | Unset): A discovered service has no attributes beyond its name (the `id`).
    """

    id: str
    type_: Literal["service"]
    attributes: ServiceAttributes | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_

        attributes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
            }
        )
        if attributes is not UNSET:
            field_dict["attributes"] = attributes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.service_attributes import ServiceAttributes

        d = dict(src_dict)
        id = d.pop("id")

        type_ = cast(Literal["service"], d.pop("type"))
        if type_ != "service":
            raise ValueError(f"type must match const 'service', got '{type_}'")

        _attributes = d.pop("attributes", UNSET)
        attributes: ServiceAttributes | Unset
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = ServiceAttributes.from_dict(_attributes)

        service_resource = cls(
            id=id,
            type_=type_,
            attributes=attributes,
        )

        service_resource.additional_properties = d
        return service_resource

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
