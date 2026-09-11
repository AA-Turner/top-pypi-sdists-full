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
    from ..models.email_action_config import EmailActionConfig


T = TypeVar("T", bound="EmailAlertActionInput")


@_attrs_define
class EmailAlertActionInput:
    """
    Attributes:
        action (Literal['email.send'] | Unset): Email delivery action Default: 'email.send'.
        config (EmailActionConfig | Unset): Configuration for email action
        is_enabled (bool | Unset): Whether this action is active Default: True.
    """

    action: Literal["email.send"] | Unset = "email.send"
    config: EmailActionConfig | Unset = UNSET
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
        from ..models.email_action_config import EmailActionConfig

        d = dict(src_dict)
        action = cast(Literal["email.send"] | Unset, d.pop("action", UNSET))
        if action != "email.send" and not isinstance(action, Unset):
            raise ValueError(f"action must match const 'email.send', got '{action}'")

        _config = d.pop("config", UNSET)
        config: EmailActionConfig | Unset
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = EmailActionConfig.from_dict(_config)

        is_enabled = d.pop("is_enabled", UNSET)

        email_alert_action_input = cls(
            action=action,
            config=config,
            is_enabled=is_enabled,
        )

        email_alert_action_input.additional_properties = d
        return email_alert_action_input

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
