import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.notification_context_schema import NotificationContextSchema
    from ..models.notification_template_detail_serializers import NotificationTemplateDetailSerializers


T = TypeVar("T", bound="Notification")


@_attrs_define
class Notification:
    """
    Attributes:
        uuid (UUID):
        url (str):
        key (str):
        enabled (bool): Indicates if notification is enabled or disabled
        created (datetime.datetime):
        templates (list['NotificationTemplateDetailSerializers']):
        context_schema (NotificationContextSchema): Finds the notification definition in the global NOTIFICATIONS
            dictionary and returns its 'context' schema.
        description (Union[Unset, str]):
    """

    uuid: UUID
    url: str
    key: str
    enabled: bool
    created: datetime.datetime
    templates: list["NotificationTemplateDetailSerializers"]
    context_schema: "NotificationContextSchema"
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        key = self.key

        enabled = self.enabled

        created = self.created.isoformat()

        templates = []
        for templates_item_data in self.templates:
            templates_item = templates_item_data.to_dict()
            templates.append(templates_item)

        context_schema = self.context_schema.to_dict()

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "key": key,
                "enabled": enabled,
                "created": created,
                "templates": templates,
                "context_schema": context_schema,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.notification_context_schema import NotificationContextSchema
        from ..models.notification_template_detail_serializers import NotificationTemplateDetailSerializers

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        key = d.pop("key")

        enabled = d.pop("enabled")

        created = isoparse(d.pop("created"))

        templates = []
        _templates = d.pop("templates")
        for templates_item_data in _templates:
            templates_item = NotificationTemplateDetailSerializers.from_dict(templates_item_data)

            templates.append(templates_item)

        context_schema = NotificationContextSchema.from_dict(d.pop("context_schema"))

        description = d.pop("description", UNSET)

        notification = cls(
            uuid=uuid,
            url=url,
            key=key,
            enabled=enabled,
            created=created,
            templates=templates,
            context_schema=context_schema,
            description=description,
        )

        notification.additional_properties = d
        return notification

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
