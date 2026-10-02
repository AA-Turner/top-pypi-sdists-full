from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.identity_bridge_user_status_attribute_sources import IdentityBridgeUserStatusAttributeSources


T = TypeVar("T", bound="IdentityBridgeUserStatus")


@_attrs_define
class IdentityBridgeUserStatus:
    """
    Attributes:
        active_isds (list[str]):
        managed_isds (list[str]):
        attribute_sources (IdentityBridgeUserStatusAttributeSources):
        stale_attributes (list[str]):
        effective_bridge_fields (list[str]):
        is_federated (bool):
    """

    active_isds: list[str]
    managed_isds: list[str]
    attribute_sources: "IdentityBridgeUserStatusAttributeSources"
    stale_attributes: list[str]
    effective_bridge_fields: list[str]
    is_federated: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        active_isds = self.active_isds

        managed_isds = self.managed_isds

        attribute_sources = self.attribute_sources.to_dict()

        stale_attributes = self.stale_attributes

        effective_bridge_fields = self.effective_bridge_fields

        is_federated = self.is_federated

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "active_isds": active_isds,
                "managed_isds": managed_isds,
                "attribute_sources": attribute_sources,
                "stale_attributes": stale_attributes,
                "effective_bridge_fields": effective_bridge_fields,
                "is_federated": is_federated,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.identity_bridge_user_status_attribute_sources import IdentityBridgeUserStatusAttributeSources

        d = dict(src_dict)
        active_isds = cast(list[str], d.pop("active_isds"))

        managed_isds = cast(list[str], d.pop("managed_isds"))

        attribute_sources = IdentityBridgeUserStatusAttributeSources.from_dict(d.pop("attribute_sources"))

        stale_attributes = cast(list[str], d.pop("stale_attributes"))

        effective_bridge_fields = cast(list[str], d.pop("effective_bridge_fields"))

        is_federated = d.pop("is_federated")

        identity_bridge_user_status = cls(
            active_isds=active_isds,
            managed_isds=managed_isds,
            attribute_sources=attribute_sources,
            stale_attributes=stale_attributes,
            effective_bridge_fields=effective_bridge_fields,
            is_federated=is_federated,
        )

        identity_bridge_user_status.additional_properties = d
        return identity_bridge_user_status

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
