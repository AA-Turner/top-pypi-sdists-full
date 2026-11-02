from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListSlackAgentChannelsResponse200Item")


@_attrs_define
class ListSlackAgentChannelsResponse200Item:
    """
    Attributes:
        channel_id (str):
        channel_name (str):
        agent_path (str):
        is_default (bool): whether the agent answers bot mentions in the channel that name no agent
    """

    channel_id: str
    channel_name: str
    agent_path: str
    is_default: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channel_id = self.channel_id
        channel_name = self.channel_name
        agent_path = self.agent_path
        is_default = self.is_default

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channel_id": channel_id,
                "channel_name": channel_name,
                "agent_path": agent_path,
                "is_default": is_default,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        channel_id = d.pop("channel_id")

        channel_name = d.pop("channel_name")

        agent_path = d.pop("agent_path")

        is_default = d.pop("is_default")

        list_slack_agent_channels_response_200_item = cls(
            channel_id=channel_id,
            channel_name=channel_name,
            agent_path=agent_path,
            is_default=is_default,
        )

        list_slack_agent_channels_response_200_item.additional_properties = d
        return list_slack_agent_channels_response_200_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
