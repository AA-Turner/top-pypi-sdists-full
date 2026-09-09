from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_network_config import SandboxNetworkConfig

T = TypeVar("T", bound="ConnectSandbox")


@_attrs_define
class ConnectSandbox:
    """
    Attributes:
        allow_public_traffic (Union[Unset, bool]): Specify whether sandbox URLs are publicly accessible without a traffic access token.
        network (Union[Unset, SandboxNetworkConfig]):
        secure (Union[Unset, bool]): Secure all system communication with sandbox
        timeout (int): Timeout in seconds from the current time after which the sandbox should expire
    """

    timeout: int
    allow_public_traffic: Union[Unset, bool] = UNSET
    network: Union[Unset, "SandboxNetworkConfig"] = UNSET
    secure: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allow_public_traffic = self.allow_public_traffic

        network: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.network, Unset):
            network = self.network.to_dict()

        secure = self.secure
        timeout = self.timeout

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timeout": timeout,
            }
        )
        if allow_public_traffic is not UNSET:
            field_dict["allowPublicTraffic"] = allow_public_traffic
        if network is not UNSET:
            field_dict["network"] = network
        if secure is not UNSET:
            field_dict["secure"] = secure

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_network_config import SandboxNetworkConfig

        d = dict(src_dict)
        allow_public_traffic = d.pop("allowPublicTraffic", UNSET)

        _network = d.pop("network", UNSET)
        network: Union[Unset, SandboxNetworkConfig]
        if isinstance(_network, Unset):
            network = UNSET
        else:
            network = SandboxNetworkConfig.from_dict(_network)

        secure = d.pop("secure", UNSET)

        timeout = d.pop("timeout")

        connect_sandbox = cls(
            timeout=timeout,
            allow_public_traffic=allow_public_traffic,
            network=network,
            secure=secure,
        )

        connect_sandbox.additional_properties = d
        return connect_sandbox

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
