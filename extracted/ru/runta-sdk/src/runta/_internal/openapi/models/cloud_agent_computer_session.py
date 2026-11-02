from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.cloud_agent_computer_session_channels import (
        CloudAgentComputerSessionChannels,
    )


T = TypeVar("T", bound="CloudAgentComputerSession")


@_attrs_define
class CloudAgentComputerSession:
    """
    Attributes:
        agent_id (str):
        runtime_id (str):
        expires_at (datetime.datetime):
        channels (CloudAgentComputerSessionChannels): Extensible set of transports authorized by this Runta session. VNC
            is available now; computer-use transports can be added without changing the session envelope.
    """

    agent_id: str
    runtime_id: str
    expires_at: datetime.datetime
    channels: CloudAgentComputerSessionChannels

    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        runtime_id = self.runtime_id

        expires_at = self.expires_at.isoformat()

        channels = self.channels.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "agent_id": agent_id,
                "runtime_id": runtime_id,
                "expires_at": expires_at,
                "channels": channels,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cloud_agent_computer_session_channels import (
            CloudAgentComputerSessionChannels,
        )

        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        runtime_id = d.pop("runtime_id")

        expires_at = datetime.datetime.fromisoformat(
            d.pop("expires_at").replace("Z", "+00:00")
        )

        channels = CloudAgentComputerSessionChannels.from_dict(d.pop("channels"))

        cloud_agent_computer_session = cls(
            agent_id=agent_id,
            runtime_id=runtime_id,
            expires_at=expires_at,
            channels=channels,
        )

        return cloud_agent_computer_session
