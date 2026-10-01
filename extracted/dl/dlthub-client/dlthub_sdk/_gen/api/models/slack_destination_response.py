from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypeVar,
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.slack_webhook_config_redacted import SlackWebhookConfigRedacted


T = TypeVar("T", bound="SlackDestinationResponse")


@_attrs_define
class SlackDestinationResponse:
    """
    Attributes:
        config (SlackWebhookConfigRedacted): Redacted webhook configuration
        date_added (datetime.datetime): When the destination was created
        date_updated (datetime.datetime): When the destination was last updated
        id (UUID): Unique ID of the destination
        name (str): Human-readable channel or destination name
        workspace_id (UUID): Workspace owning this destination
        kind (Literal['slack_webhook'] | Unset): Type of destination Default: 'slack_webhook'.
    """

    config: SlackWebhookConfigRedacted
    date_added: datetime.datetime
    date_updated: datetime.datetime
    id: UUID
    name: str
    workspace_id: UUID
    kind: Literal["slack_webhook"] | Unset = "slack_webhook"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config = self.config.to_dict()

        date_added = self.date_added.isoformat()

        date_updated = self.date_updated.isoformat()

        id = str(self.id)

        name = self.name

        workspace_id = str(self.workspace_id)

        kind = self.kind

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "config": config,
                "date_added": date_added,
                "date_updated": date_updated,
                "id": id,
                "name": name,
                "workspace_id": workspace_id,
            }
        )
        if kind is not UNSET:
            field_dict["kind"] = kind

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.slack_webhook_config_redacted import SlackWebhookConfigRedacted

        d = dict(src_dict)
        config = SlackWebhookConfigRedacted.from_dict(d.pop("config"))

        date_added = isoparse(d.pop("date_added"))

        date_updated = isoparse(d.pop("date_updated"))

        id = UUID(d.pop("id"))

        name = d.pop("name")

        workspace_id = UUID(d.pop("workspace_id"))

        kind = cast(Literal["slack_webhook"] | Unset, d.pop("kind", UNSET))
        if kind != "slack_webhook" and not isinstance(kind, Unset):
            raise ValueError(f"kind must match const 'slack_webhook', got '{kind}'")

        slack_destination_response = cls(
            config=config,
            date_added=date_added,
            date_updated=date_updated,
            id=id,
            name=name,
            workspace_id=workspace_id,
            kind=kind,
        )

        slack_destination_response.additional_properties = d
        return slack_destination_response

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
