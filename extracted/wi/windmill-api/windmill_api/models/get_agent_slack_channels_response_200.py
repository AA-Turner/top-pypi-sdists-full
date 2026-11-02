from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_agent_slack_channels_response_200_channels_item import (
        GetAgentSlackChannelsResponse200ChannelsItem,
    )


T = TypeVar("T", bound="GetAgentSlackChannelsResponse200")


@_attrs_define
class GetAgentSlackChannelsResponse200:
    """
    Attributes:
        signing_secret_set (bool): agents answer in Slack only when the server has the Slack app's signing secret
            (SLACK_SIGNING_SECRET)
        missing_scopes (List[str]): agent scopes the workspace's Slack connection lacks, so it must be reconnected with
            AI agents enabled
        anyone (bool): whether anyone in its channels can ask it (its slack_anyone, kept only while it runs on behalf of
            someone), rather than workspace members only
        can_share (bool): whether the caller can change the agent's channels, as anyone who can edit it can
        channels (List['GetAgentSlackChannelsResponse200ChannelsItem']):
        slack_team_name (Union[Unset, str]): the connected Slack workspace; absent when Slack is not connected
        bot_name (Union[Unset, str]): the bot's Slack handle; absent when Slack can't be reached
        runs_as (Union[Unset, str]): who the agent runs as (its on_behalf_of); absent unless it runs on behalf of
            someone
    """

    signing_secret_set: bool
    missing_scopes: List[str]
    anyone: bool
    can_share: bool
    channels: List["GetAgentSlackChannelsResponse200ChannelsItem"]
    slack_team_name: Union[Unset, str] = UNSET
    bot_name: Union[Unset, str] = UNSET
    runs_as: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        signing_secret_set = self.signing_secret_set
        missing_scopes = self.missing_scopes

        anyone = self.anyone
        can_share = self.can_share
        channels = []
        for channels_item_data in self.channels:
            channels_item = channels_item_data.to_dict()

            channels.append(channels_item)

        slack_team_name = self.slack_team_name
        bot_name = self.bot_name
        runs_as = self.runs_as

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "signing_secret_set": signing_secret_set,
                "missing_scopes": missing_scopes,
                "anyone": anyone,
                "can_share": can_share,
                "channels": channels,
            }
        )
        if slack_team_name is not UNSET:
            field_dict["slack_team_name"] = slack_team_name
        if bot_name is not UNSET:
            field_dict["bot_name"] = bot_name
        if runs_as is not UNSET:
            field_dict["runs_as"] = runs_as

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_agent_slack_channels_response_200_channels_item import (
            GetAgentSlackChannelsResponse200ChannelsItem,
        )

        d = src_dict.copy()
        signing_secret_set = d.pop("signing_secret_set")

        missing_scopes = cast(List[str], d.pop("missing_scopes"))

        anyone = d.pop("anyone")

        can_share = d.pop("can_share")

        channels = []
        _channels = d.pop("channels")
        for channels_item_data in _channels:
            channels_item = GetAgentSlackChannelsResponse200ChannelsItem.from_dict(channels_item_data)

            channels.append(channels_item)

        slack_team_name = d.pop("slack_team_name", UNSET)

        bot_name = d.pop("bot_name", UNSET)

        runs_as = d.pop("runs_as", UNSET)

        get_agent_slack_channels_response_200 = cls(
            signing_secret_set=signing_secret_set,
            missing_scopes=missing_scopes,
            anyone=anyone,
            can_share=can_share,
            channels=channels,
            slack_team_name=slack_team_name,
            bot_name=bot_name,
            runs_as=runs_as,
        )

        get_agent_slack_channels_response_200.additional_properties = d
        return get_agent_slack_channels_response_200

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
