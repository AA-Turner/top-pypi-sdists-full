from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SlackWebhookConfigRedacted")


@_attrs_define
class SlackWebhookConfigRedacted:
    """Redacted webhook configuration

    Attributes:
        masked_url (str): Masked Slack webhook URL with sensitive components redacted
    """

    masked_url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        masked_url = self.masked_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "masked_url": masked_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        masked_url = d.pop("masked_url")

        slack_webhook_config_redacted = cls(
            masked_url=masked_url,
        )

        slack_webhook_config_redacted.additional_properties = d
        return slack_webhook_config_redacted

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
