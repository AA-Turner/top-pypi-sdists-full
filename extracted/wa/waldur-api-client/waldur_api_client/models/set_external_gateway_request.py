from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.set_external_gateway_request_external_fixed_ips_item import (
        SetExternalGatewayRequestExternalFixedIpsItem,
    )


T = TypeVar("T", bound="SetExternalGatewayRequest")


@_attrs_define
class SetExternalGatewayRequest:
    """
    Attributes:
        external_network_id (str): Backend ID (OpenStack UUID) of the external network.
        enable_snat (Union[None, Unset, bool]): Whether to enable SNAT on the gateway. None means use OpenStack default
            (True). Requires advanced permissions.
        external_fixed_ips (Union[Unset, list['SetExternalGatewayRequestExternalFixedIpsItem']]): List of fixed IP
            specifications for the gateway port. Each entry should have 'ip_address' and optionally 'subnet_id'. Requires
            advanced permissions.
    """

    external_network_id: str
    enable_snat: Union[None, Unset, bool] = UNSET
    external_fixed_ips: Union[Unset, list["SetExternalGatewayRequestExternalFixedIpsItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        external_network_id = self.external_network_id

        enable_snat: Union[None, Unset, bool]
        if isinstance(self.enable_snat, Unset):
            enable_snat = UNSET
        else:
            enable_snat = self.enable_snat

        external_fixed_ips: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.external_fixed_ips, Unset):
            external_fixed_ips = []
            for external_fixed_ips_item_data in self.external_fixed_ips:
                external_fixed_ips_item = external_fixed_ips_item_data.to_dict()
                external_fixed_ips.append(external_fixed_ips_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "external_network_id": external_network_id,
            }
        )
        if enable_snat is not UNSET:
            field_dict["enable_snat"] = enable_snat
        if external_fixed_ips is not UNSET:
            field_dict["external_fixed_ips"] = external_fixed_ips

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.set_external_gateway_request_external_fixed_ips_item import (
            SetExternalGatewayRequestExternalFixedIpsItem,
        )

        d = dict(src_dict)
        external_network_id = d.pop("external_network_id")

        def _parse_enable_snat(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        enable_snat = _parse_enable_snat(d.pop("enable_snat", UNSET))

        external_fixed_ips = []
        _external_fixed_ips = d.pop("external_fixed_ips", UNSET)
        for external_fixed_ips_item_data in _external_fixed_ips or []:
            external_fixed_ips_item = SetExternalGatewayRequestExternalFixedIpsItem.from_dict(
                external_fixed_ips_item_data
            )

            external_fixed_ips.append(external_fixed_ips_item)

        set_external_gateway_request = cls(
            external_network_id=external_network_id,
            enable_snat=enable_snat,
            external_fixed_ips=external_fixed_ips,
        )

        set_external_gateway_request.additional_properties = d
        return set_external_gateway_request

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
