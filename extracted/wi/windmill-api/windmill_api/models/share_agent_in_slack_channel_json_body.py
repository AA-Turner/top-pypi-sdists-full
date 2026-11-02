from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ShareAgentInSlackChannelJsonBody")


@_attrs_define
class ShareAgentInSlackChannelJsonBody:
    """
    Attributes:
        channel_id (str):
        channel_name (str):
        is_default (Union[Unset, bool]): whether the agent answers bot mentions in the channel that name no agent
    """

    channel_id: str
    channel_name: str
    is_default: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channel_id = self.channel_id
        channel_name = self.channel_name
        is_default = self.is_default

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channel_id": channel_id,
                "channel_name": channel_name,
            }
        )
        if is_default is not UNSET:
            field_dict["is_default"] = is_default

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        channel_id = d.pop("channel_id")

        channel_name = d.pop("channel_name")

        is_default = d.pop("is_default", UNSET)

        share_agent_in_slack_channel_json_body = cls(
            channel_id=channel_id,
            channel_name=channel_name,
            is_default=is_default,
        )

        share_agent_in_slack_channel_json_body.additional_properties = d
        return share_agent_in_slack_channel_json_body

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
