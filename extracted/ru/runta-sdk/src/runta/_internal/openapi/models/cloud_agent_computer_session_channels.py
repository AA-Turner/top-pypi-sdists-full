from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.cloud_agent_vnc_session_channel import CloudAgentVncSessionChannel


T = TypeVar("T", bound="CloudAgentComputerSessionChannels")


@_attrs_define
class CloudAgentComputerSessionChannels:
    """Transports that this Runta session authorizes. VNC is available now. Additional computer-use transports can use the
    same session envelope.

        Attributes:
            vnc (CloudAgentVncSessionChannel):
    """

    vnc: CloudAgentVncSessionChannel

    def to_dict(self) -> dict[str, Any]:
        vnc = self.vnc.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "vnc": vnc,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cloud_agent_vnc_session_channel import CloudAgentVncSessionChannel

        d = dict(src_dict)
        vnc = CloudAgentVncSessionChannel.from_dict(d.pop("vnc"))

        cloud_agent_computer_session_channels = cls(
            vnc=vnc,
        )

        return cloud_agent_computer_session_channels
