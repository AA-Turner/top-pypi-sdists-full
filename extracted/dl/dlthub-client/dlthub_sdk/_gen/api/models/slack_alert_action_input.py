from __future__ import annotations

from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.slack_post_config import SlackPostConfig


T = TypeVar("T", bound="SlackAlertActionInput")


@_attrs_define
class SlackAlertActionInput:
    """
    Attributes:
        action (Literal['slack.post'] | Unset): Slack delivery action Default: 'slack.post'.
        config (SlackPostConfig | Unset): Configuration for Slack action
        is_enabled (bool | Unset): Whether this action is active Default: True.
    """

    action: Literal["slack.post"] | Unset = "slack.post"
    config: SlackPostConfig | Unset = UNSET
    is_enabled: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action = self.action

        config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        is_enabled = self.is_enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if action is not UNSET:
            field_dict["action"] = action
        if config is not UNSET:
            field_dict["config"] = config
        if is_enabled is not UNSET:
            field_dict["is_enabled"] = is_enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.slack_post_config import SlackPostConfig

        d = dict(src_dict)
        action = cast(Literal["slack.post"] | Unset, d.pop("action", UNSET))
        if action != "slack.post" and not isinstance(action, Unset):
            raise ValueError(f"action must match const 'slack.post', got '{action}'")

        _config = d.pop("config", UNSET)
        config: SlackPostConfig | Unset
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = SlackPostConfig.from_dict(_config)

        is_enabled = d.pop("is_enabled", UNSET)

        slack_alert_action_input = cls(
            action=action,
            config=config,
            is_enabled=is_enabled,
        )

        slack_alert_action_input.additional_properties = d
        return slack_alert_action_input

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
