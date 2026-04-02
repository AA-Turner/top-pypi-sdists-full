from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blank_enum import BlankEnum
from ..models.direction_enum import DirectionEnum
from ..models.ethertype_enum import EthertypeEnum
from ..models.security_group_rule_protocol_enum import SecurityGroupRuleProtocolEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="RancherClusterSecurityGroupRuleRequest")


@_attrs_define
class RancherClusterSecurityGroupRuleRequest:
    """
    Attributes:
        ethertype (Union[Unset, EthertypeEnum]):
        direction (Union[Unset, DirectionEnum]):
        protocol (Union[BlankEnum, SecurityGroupRuleProtocolEnum, Unset]): The network protocol (TCP, UDP, ICMP, or
            empty for any protocol)
        from_port (Union[None, Unset, int]): Starting port number in the range (1-65535)
        to_port (Union[None, Unset, int]): Ending port number in the range (1-65535)
        cidr (Union[None, Unset, str]): CIDR notation for the source/destination network address range
        description (Union[Unset, str]):
    """

    ethertype: Union[Unset, EthertypeEnum] = UNSET
    direction: Union[Unset, DirectionEnum] = UNSET
    protocol: Union[BlankEnum, SecurityGroupRuleProtocolEnum, Unset] = UNSET
    from_port: Union[None, Unset, int] = UNSET
    to_port: Union[None, Unset, int] = UNSET
    cidr: Union[None, Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ethertype: Union[Unset, str] = UNSET
        if not isinstance(self.ethertype, Unset):
            ethertype = self.ethertype.value

        direction: Union[Unset, str] = UNSET
        if not isinstance(self.direction, Unset):
            direction = self.direction.value

        protocol: Union[Unset, str]
        if isinstance(self.protocol, Unset):
            protocol = UNSET
        elif isinstance(self.protocol, SecurityGroupRuleProtocolEnum):
            protocol = self.protocol.value
        else:
            protocol = self.protocol.value

        from_port: Union[None, Unset, int]
        if isinstance(self.from_port, Unset):
            from_port = UNSET
        else:
            from_port = self.from_port

        to_port: Union[None, Unset, int]
        if isinstance(self.to_port, Unset):
            to_port = UNSET
        else:
            to_port = self.to_port

        cidr: Union[None, Unset, str]
        if isinstance(self.cidr, Unset):
            cidr = UNSET
        else:
            cidr = self.cidr

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ethertype is not UNSET:
            field_dict["ethertype"] = ethertype
        if direction is not UNSET:
            field_dict["direction"] = direction
        if protocol is not UNSET:
            field_dict["protocol"] = protocol
        if from_port is not UNSET:
            field_dict["from_port"] = from_port
        if to_port is not UNSET:
            field_dict["to_port"] = to_port
        if cidr is not UNSET:
            field_dict["cidr"] = cidr
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _ethertype = d.pop("ethertype", UNSET)
        ethertype: Union[Unset, EthertypeEnum]
        if isinstance(_ethertype, Unset):
            ethertype = UNSET
        else:
            ethertype = EthertypeEnum(_ethertype)

        _direction = d.pop("direction", UNSET)
        direction: Union[Unset, DirectionEnum]
        if isinstance(_direction, Unset):
            direction = UNSET
        else:
            direction = DirectionEnum(_direction)

        def _parse_protocol(data: object) -> Union[BlankEnum, SecurityGroupRuleProtocolEnum, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                protocol_type_0 = SecurityGroupRuleProtocolEnum(data)

                return protocol_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            protocol_type_1 = BlankEnum(data)

            return protocol_type_1

        protocol = _parse_protocol(d.pop("protocol", UNSET))

        def _parse_from_port(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        from_port = _parse_from_port(d.pop("from_port", UNSET))

        def _parse_to_port(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        to_port = _parse_to_port(d.pop("to_port", UNSET))

        def _parse_cidr(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cidr = _parse_cidr(d.pop("cidr", UNSET))

        description = d.pop("description", UNSET)

        rancher_cluster_security_group_rule_request = cls(
            ethertype=ethertype,
            direction=direction,
            protocol=protocol,
            from_port=from_port,
            to_port=to_port,
            cidr=cidr,
            description=description,
        )

        rancher_cluster_security_group_rule_request.additional_properties = d
        return rancher_cluster_security_group_rule_request

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
