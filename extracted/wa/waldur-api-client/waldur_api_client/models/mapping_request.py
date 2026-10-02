from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sub_net_mapping_request import SubNetMappingRequest
    from ..models.volume_type_mapping_request import VolumeTypeMappingRequest


T = TypeVar("T", bound="MappingRequest")


@_attrs_define
class MappingRequest:
    """
    Attributes:
        volume_types (Union[Unset, list['VolumeTypeMappingRequest']]):
        subnets (Union[Unset, list['SubNetMappingRequest']]):
        skip_connection_extnet (Union[Unset, bool]):  Default: False.
        sync_instance_ports (Union[Unset, bool]):  Default: False.
        networks (Union[Unset, list[UUID]]):
    """

    volume_types: Union[Unset, list["VolumeTypeMappingRequest"]] = UNSET
    subnets: Union[Unset, list["SubNetMappingRequest"]] = UNSET
    skip_connection_extnet: Union[Unset, bool] = False
    sync_instance_ports: Union[Unset, bool] = False
    networks: Union[Unset, list[UUID]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        volume_types: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.volume_types, Unset):
            volume_types = []
            for volume_types_item_data in self.volume_types:
                volume_types_item = volume_types_item_data.to_dict()
                volume_types.append(volume_types_item)

        subnets: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.subnets, Unset):
            subnets = []
            for subnets_item_data in self.subnets:
                subnets_item = subnets_item_data.to_dict()
                subnets.append(subnets_item)

        skip_connection_extnet = self.skip_connection_extnet

        sync_instance_ports = self.sync_instance_ports

        networks: Union[Unset, list[str]] = UNSET
        if not isinstance(self.networks, Unset):
            networks = []
            for networks_item_data in self.networks:
                networks_item = str(networks_item_data)
                networks.append(networks_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if volume_types is not UNSET:
            field_dict["volume_types"] = volume_types
        if subnets is not UNSET:
            field_dict["subnets"] = subnets
        if skip_connection_extnet is not UNSET:
            field_dict["skip_connection_extnet"] = skip_connection_extnet
        if sync_instance_ports is not UNSET:
            field_dict["sync_instance_ports"] = sync_instance_ports
        if networks is not UNSET:
            field_dict["networks"] = networks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sub_net_mapping_request import SubNetMappingRequest
        from ..models.volume_type_mapping_request import VolumeTypeMappingRequest

        d = dict(src_dict)
        volume_types = []
        _volume_types = d.pop("volume_types", UNSET)
        for volume_types_item_data in _volume_types or []:
            volume_types_item = VolumeTypeMappingRequest.from_dict(volume_types_item_data)

            volume_types.append(volume_types_item)

        subnets = []
        _subnets = d.pop("subnets", UNSET)
        for subnets_item_data in _subnets or []:
            subnets_item = SubNetMappingRequest.from_dict(subnets_item_data)

            subnets.append(subnets_item)

        skip_connection_extnet = d.pop("skip_connection_extnet", UNSET)

        sync_instance_ports = d.pop("sync_instance_ports", UNSET)

        networks = []
        _networks = d.pop("networks", UNSET)
        for networks_item_data in _networks or []:
            networks_item = UUID(networks_item_data)

            networks.append(networks_item)

        mapping_request = cls(
            volume_types=volume_types,
            subnets=subnets,
            skip_connection_extnet=skip_connection_extnet,
            sync_instance_ports=sync_instance_ports,
            networks=networks,
        )

        mapping_request.additional_properties = d
        return mapping_request

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
