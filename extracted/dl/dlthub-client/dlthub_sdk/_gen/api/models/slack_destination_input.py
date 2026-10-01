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
    from ..models.slack_webhook_config import SlackWebhookConfig


T = TypeVar("T", bound="SlackDestinationInput")


@_attrs_define
class SlackDestinationInput:
    """
    Attributes:
        config (SlackWebhookConfig): Webhook configuration
        name (str): Human-readable channel or destination name
        kind (Literal['slack_webhook'] | Unset): Type of destination Default: 'slack_webhook'.
    """

    config: SlackWebhookConfig
    name: str
    kind: Literal["slack_webhook"] | Unset = "slack_webhook"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config = self.config.to_dict()

        name = self.name

        kind = self.kind

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "config": config,
                "name": name,
            }
        )
        if kind is not UNSET:
            field_dict["kind"] = kind

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.slack_webhook_config import SlackWebhookConfig

        d = dict(src_dict)
        config = SlackWebhookConfig.from_dict(d.pop("config"))

        name = d.pop("name")

        kind = cast(Literal["slack_webhook"] | Unset, d.pop("kind", UNSET))
        if kind != "slack_webhook" and not isinstance(kind, Unset):
            raise ValueError(f"kind must match const 'slack_webhook', got '{kind}'")

        slack_destination_input = cls(
            config=config,
            name=name,
            kind=kind,
        )

        slack_destination_input.additional_properties = d
        return slack_destination_input

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
