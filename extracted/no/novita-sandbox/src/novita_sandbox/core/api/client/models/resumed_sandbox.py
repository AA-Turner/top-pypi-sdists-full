from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_network_config import SandboxNetworkConfig

T = TypeVar("T", bound="ResumedSandbox")


@_attrs_define
class ResumedSandbox:
    """
    Attributes:
        auto_pause (Union[Unset, bool]): Automatically pauses the sandbox after the timeout
        network (Union[Unset, SandboxNetworkConfig]):
        secure (Union[Unset, bool]): Secure all system communication with sandbox
        timeout (Union[Unset, int]): Time to live for the sandbox in seconds. Default: 15.
    """

    auto_pause: Union[Unset, bool] = UNSET
    network: Union[Unset, "SandboxNetworkConfig"] = UNSET
    secure: Union[Unset, bool] = UNSET
    timeout: Union[Unset, int] = 15
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        auto_pause = self.auto_pause

        network: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.network, Unset):
            network = self.network.to_dict()

        secure = self.secure

        timeout = self.timeout

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if auto_pause is not UNSET:
            field_dict["autoPause"] = auto_pause
        if network is not UNSET:
            field_dict["network"] = network
        if secure is not UNSET:
            field_dict["secure"] = secure
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_network_config import SandboxNetworkConfig

        d = dict(src_dict)
        auto_pause = d.pop("autoPause", UNSET)

        _network = d.pop("network", UNSET)
        network: Union[Unset, SandboxNetworkConfig]
        if isinstance(_network, Unset):
            network = UNSET
        else:
            network = SandboxNetworkConfig.from_dict(_network)

        secure = d.pop("secure", UNSET)

        timeout = d.pop("timeout", UNSET)

        resumed_sandbox = cls(
            auto_pause=auto_pause,
            network=network,
            secure=secure,
            timeout=timeout,
        )

        resumed_sandbox.additional_properties = d
        return resumed_sandbox

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
