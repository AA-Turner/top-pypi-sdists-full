import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.backend_type_enum import BackendTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.provider_helpdesk_settings import ProviderHelpdeskSettings


T = TypeVar("T", bound="ProviderHelpdesk")


@_attrs_define
class ProviderHelpdesk:
    """
    Attributes:
        url (str):
        uuid (UUID):
        service_provider (UUID):
        service_provider_name (str):
        health_status (str):
        last_health_check (Union[None, datetime.datetime]):
        failed_routing_count (int):
        created (datetime.datetime):
        modified (datetime.datetime):
        backend_type (Union[Unset, BackendTypeEnum]):
        settings (Union[Unset, ProviderHelpdeskSettings]): Backend-specific configuration.
        is_active (Union[Unset, bool]):
        webhook_secret (Union[Unset, str]):
        notification_email (Union[Unset, str]): Primary email for notifications.
        notify_on_new_ticket (Union[Unset, bool]):
        notify_on_comment (Union[Unset, bool]):
        notify_on_escalation (Union[Unset, bool]):
        notify_on_sla_warning (Union[Unset, bool]):
    """

    url: str
    uuid: UUID
    service_provider: UUID
    service_provider_name: str
    health_status: str
    last_health_check: Union[None, datetime.datetime]
    failed_routing_count: int
    created: datetime.datetime
    modified: datetime.datetime
    backend_type: Union[Unset, BackendTypeEnum] = UNSET
    settings: Union[Unset, "ProviderHelpdeskSettings"] = UNSET
    is_active: Union[Unset, bool] = UNSET
    webhook_secret: Union[Unset, str] = UNSET
    notification_email: Union[Unset, str] = UNSET
    notify_on_new_ticket: Union[Unset, bool] = UNSET
    notify_on_comment: Union[Unset, bool] = UNSET
    notify_on_escalation: Union[Unset, bool] = UNSET
    notify_on_sla_warning: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        service_provider = str(self.service_provider)

        service_provider_name = self.service_provider_name

        health_status = self.health_status

        last_health_check: Union[None, str]
        if isinstance(self.last_health_check, datetime.datetime):
            last_health_check = self.last_health_check.isoformat()
        else:
            last_health_check = self.last_health_check

        failed_routing_count = self.failed_routing_count

        created = self.created.isoformat()

        modified = self.modified.isoformat()

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
                "url": url,
                "uuid": uuid,
                "service_provider": service_provider,
                "service_provider_name": service_provider_name,
                "health_status": health_status,
                "last_health_check": last_health_check,
                "failed_routing_count": failed_routing_count,
                "created": created,
                "modified": modified,
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
        from ..models.provider_helpdesk_settings import ProviderHelpdeskSettings

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        service_provider = UUID(d.pop("service_provider"))

        service_provider_name = d.pop("service_provider_name")

        health_status = d.pop("health_status")

        def _parse_last_health_check(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_health_check_type_0 = isoparse(data)

                return last_health_check_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_health_check = _parse_last_health_check(d.pop("last_health_check"))

        failed_routing_count = d.pop("failed_routing_count")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        _backend_type = d.pop("backend_type", UNSET)
        backend_type: Union[Unset, BackendTypeEnum]
        if isinstance(_backend_type, Unset):
            backend_type = UNSET
        else:
            backend_type = BackendTypeEnum(_backend_type)

        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, ProviderHelpdeskSettings]
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = ProviderHelpdeskSettings.from_dict(_settings)

        is_active = d.pop("is_active", UNSET)

        webhook_secret = d.pop("webhook_secret", UNSET)

        notification_email = d.pop("notification_email", UNSET)

        notify_on_new_ticket = d.pop("notify_on_new_ticket", UNSET)

        notify_on_comment = d.pop("notify_on_comment", UNSET)

        notify_on_escalation = d.pop("notify_on_escalation", UNSET)

        notify_on_sla_warning = d.pop("notify_on_sla_warning", UNSET)

        provider_helpdesk = cls(
            url=url,
            uuid=uuid,
            service_provider=service_provider,
            service_provider_name=service_provider_name,
            health_status=health_status,
            last_health_check=last_health_check,
            failed_routing_count=failed_routing_count,
            created=created,
            modified=modified,
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

        provider_helpdesk.additional_properties = d
        return provider_helpdesk

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
