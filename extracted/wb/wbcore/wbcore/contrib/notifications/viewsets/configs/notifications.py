from django.utils.translation import gettext as _
from rest_framework.reverse import reverse
from wbcore.contrib.icons.icons import WBIcon
from wbcore.contrib.notifications.models import Notification
from wbcore.metadata.configs.buttons.buttons import (
    ActionButton,
    HyperlinkButton,
    RequestType,
    WidgetButton,
)
from wbcore.metadata.configs.buttons.view_config import ButtonViewConfig
from wbcore.metadata.configs.display import Field, ListDisplay
from wbcore.metadata.configs.display.instance_display import Display
from wbcore.metadata.configs.display.instance_display.shortcuts import (
    create_simple_display,
)
from wbcore.metadata.configs.display.view_config import DisplayViewConfig


class NotificationButtonConfig(ButtonViewConfig):
    def get_custom_buttons(self) -> set[ActionButton]:
        if not self.view.kwargs.get("pk", None):
            return {
                ActionButton(
                    weight=0,
                    method=RequestType.PATCH,
                    action_label=_("Reading all notifications"),
                    endpoint=reverse("wbcore:notifications:notification-read-all", request=self.request),
                    description_fields=_("Do you want to mark notifications as read?"),
                    label=_("Mark all read"),
                    icon=WBIcon.VIEW.icon,
                    identifiers=["notifications:notification"],
                ),
                ActionButton(
                    weight=1,
                    method=RequestType.PATCH,
                    action_label=_("Deleting all read notifications"),
                    endpoint=reverse("wbcore:notifications:notification-delete-all-read", request=self.request),
                    description_fields=_("Do you want delete all read notifications?"),
                    label=_("Delete all read"),
                    icon=WBIcon.DELETE.icon,
                    identifiers=["notifications:notification"],
                ),
            }
        return set()

    def get_custom_instance_buttons(self) -> set[WidgetButton]:
        resource_button_label = _("Open Resource")
        if pk := self.view.kwargs.get("pk", None):
            notification = Notification.objects.get(id=pk)
            resource_button_label = notification.notification_type.resource_button_label

        return {
            WidgetButton(
                title=resource_button_label,
                label=resource_button_label,
                icon=WBIcon.LINK.icon,
                key="open_internal_resource",
            ),
            HyperlinkButton(
                title=resource_button_label,
                label=resource_button_label,
                icon=WBIcon.LINK.icon,
                key="open_external_resource",
            ),
        }

    def get_custom_list_instance_buttons(self) -> set[WidgetButton]:
        return self.get_custom_instance_buttons()


class NotificationDisplayConfig(DisplayViewConfig):
    def get_list_display(self) -> ListDisplay:
        return ListDisplay(
            fields=[
                Field(key="notification_type", label="Type"),
                Field(key="title", label="Title"),
                Field(key="body", label="body"),
                Field(
                    key=None,
                    label="Info",
                    children=[
                        Field(key="sent_email", label="Email"),
                        Field(key="sent_web", label="Web"),
                        Field(key="sent_mobile", label="Mobile"),
                        Field(key="read", label="Read"),
                    ],
                ),
            ],
        )

    def get_instance_display(self) -> Display:
        return create_simple_display(
            [
                ["notification_type", ".", "."],
                ["title", "title", "read"],
                ["sent_email", "sent_web", "sent_mobile"],
                ["body", "body", "body"],
            ]
        )
