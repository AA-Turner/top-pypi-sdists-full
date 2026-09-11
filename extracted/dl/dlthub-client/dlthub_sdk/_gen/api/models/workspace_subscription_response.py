from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.configurable_notification_event_type import (
    ConfigurableNotificationEventType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.email_subscription_response import EmailSubscriptionResponse


T = TypeVar("T", bound="WorkspaceSubscriptionResponse")


@_attrs_define
class WorkspaceSubscriptionResponse:
    """
    Attributes:
        display_label (str): Human-readable name for the subscribed event
        event_type (ConfigurableNotificationEventType): The configurable event this subscription covers
        workspace_id (UUID): The workspace this subscription belongs to
        email (EmailSubscriptionResponse | None | Unset): Email-channel config; null when email is not configured
    """

    display_label: str
    event_type: ConfigurableNotificationEventType
    workspace_id: UUID
    email: EmailSubscriptionResponse | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.email_subscription_response import EmailSubscriptionResponse

        display_label = self.display_label

        event_type = self.event_type.value

        workspace_id = str(self.workspace_id)

        email: dict[str, Any] | None | Unset
        if isinstance(self.email, Unset):
            email = UNSET
        elif isinstance(self.email, EmailSubscriptionResponse):
            email = self.email.to_dict()
        else:
            email = self.email

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "display_label": display_label,
                "event_type": event_type,
                "workspace_id": workspace_id,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.email_subscription_response import EmailSubscriptionResponse

        d = dict(src_dict)
        display_label = d.pop("display_label")

        event_type = ConfigurableNotificationEventType(d.pop("event_type"))

        workspace_id = UUID(d.pop("workspace_id"))

        def _parse_email(data: object) -> EmailSubscriptionResponse | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                email_type_0 = EmailSubscriptionResponse.from_dict(data)

                return email_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EmailSubscriptionResponse | None | Unset, data)

        email = _parse_email(d.pop("email", UNSET))

        workspace_subscription_response = cls(
            display_label=display_label,
            event_type=event_type,
            workspace_id=workspace_id,
            email=email,
        )

        workspace_subscription_response.additional_properties = d
        return workspace_subscription_response

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
