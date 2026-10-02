from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.backend_type_enum import BackendTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.provider_helpdesk_request_settings import ProviderHelpdeskRequestSettings


T = TypeVar("T", bound="ProviderHelpdeskRequest")


@_attrs_define
class ProviderHelpdeskRequest:
    """
    Attributes:
        service_provider (UUID):
        backend_type (Union[Unset, BackendTypeEnum]):
        settings (Union[Unset, ProviderHelpdeskRequestSettings]): Backend-specific configuration.
        is_active (Union[Unset, bool]):
        webhook_secret (Union[Unset, str]):
        notification_email (Union[Unset, str]): Primary email for notifications.
        notify_on_new_ticket (Union[Unset, bool]):
        notify_on_comment (Union[Unset, bool]):
        notify_on_escalation (Union[Unset, bool]):
        notify_on_sla_warning (Union[Unset, bool]):
    """

    service_provider: UUID
    backend_type: Union[Unset, BackendTypeEnum] = UNSET
    settings: Union[Unset, "ProviderHelpdeskRequestSettings"] = UNSET
    is_active: Union[Unset, bool] = UNSET
    webhook_secret: Union[Unset, str] = UNSET
    notification_email: Union[Unset, str] = UNSET
    notify_on_new_ticket: Union[Unset, bool] = UNSET
    notify_on_comment: Union[Unset, bool] = UNSET
    notify_on_escalation: Union[Unset, bool] = UNSET
    notify_on_sla_warning: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_provider = str(self.service_provider)

        backend_type: Union[Unset, str] = UNSET
        if not isinstance(self.backend_type, Unset):
            backend_type = self.backend_type.value

        settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        is_active = self.is_active

        webhook_secret = self.webhook_secret

        notification_email = self.notification_email

        notify_on_new_ticket = self.notify_on_new_ticket

        notify_on_comment = self.notify_on_comment

        notify_on_escalation = self.notify_on_escalation

        notify_on_sla_warning = self.notify_on_sla_warning

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_provider": service_provider,
            }
        )
        if backend_type is not UNSET:
            field_dict["backend_type"] = backend_type
        if settings is not UNSET:
            field_dict["settings"] = settings
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if webhook_secret is not UNSET:
            field_dict["webhook_secret"] = webhook_secret
        if notification_email is not UNSET:
            field_dict["notification_email"] = notification_email
        if notify_on_new_ticket is not UNSET:
            field_dict["notify_on_new_ticket"] = notify_on_new_ticket
        if notify_on_comment is not UNSET:
            field_dict["notify_on_comment"] = notify_on_comment
        if notify_on_escalation is not UNSET:
            field_dict["notify_on_escalation"] = notify_on_escalation
        if notify_on_sla_warning is not UNSET:
            field_dict["notify_on_sla_warning"] = notify_on_sla_warning

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.provider_helpdesk_request_settings import ProviderHelpdeskRequestSettings

        d = dict(src_dict)
        service_provider = UUID(d.pop("service_provider"))

        _backend_type = d.pop("backend_type", UNSET)
        backend_type: Union[Unset, BackendTypeEnum]
        if isinstance(_backend_type, Unset):
            backend_type = UNSET
        else:
            backend_type = BackendTypeEnum(_backend_type)

        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, ProviderHelpdeskRequestSettings]
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = ProviderHelpdeskRequestSettings.from_dict(_settings)

        is_active = d.pop("is_active", UNSET)

        webhook_secret = d.pop("webhook_secret", UNSET)

        notification_email = d.pop("notification_email", UNSET)

        notify_on_new_ticket = d.pop("notify_on_new_ticket", UNSET)

        notify_on_comment = d.pop("notify_on_comment", UNSET)

        notify_on_escalation = d.pop("notify_on_escalation", UNSET)

        notify_on_sla_warning = d.pop("notify_on_sla_warning", UNSET)

        provider_helpdesk_request = cls(
            service_provider=service_provider,
            backend_type=backend_type,
            settings=settings,
            is_active=is_active,
            webhook_secret=webhook_secret,
            notification_email=notification_email,
            notify_on_new_ticket=notify_on_new_ticket,
            notify_on_comment=notify_on_comment,
            notify_on_escalation=notify_on_escalation,
            notify_on_sla_warning=notify_on_sla_warning,
        )

        provider_helpdesk_request.additional_properties = d
        return provider_helpdesk_request

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
