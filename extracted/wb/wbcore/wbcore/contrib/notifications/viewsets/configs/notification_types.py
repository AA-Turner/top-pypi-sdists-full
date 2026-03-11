from wbcore.contrib.icons import WBIcon
from wbcore.enums import Unit
from wbcore.metadata.configs.display import Field, Legend, LegendItem, ListDisplay
from wbcore.metadata.configs.display.instance_display import Display
from wbcore.metadata.configs.display.instance_display.shortcuts import (
    create_simple_display,
)
from wbcore.metadata.configs.display.view_config import DisplayViewConfig
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class NotificationTypeSettingDisplayConfig(DisplayViewConfig):
    def get_list_display(self) -> ListDisplay:
        return ListDisplay(
            fields=[
                Field(key="locked_icon", label=" ", width=Unit.PIXEL(40)),
                Field(key="notification_type", label="Notification", width=Unit.PIXEL(250)),
                Field(key="help_text", label="Help Text", width=Unit.PIXEL(500)),
                Field(
                    key=None,
                    label="Parameter",
                    open_by_default=True,
                    children=[
                        Field(key="enable_email", label="E-Mail", width=Unit.PIXEL(100)),
                        Field(key="enable_mobile", label="Mobile", width=Unit.PIXEL(100)),
                        Field(key="enable_web", label="Web", width=Unit.PIXEL(100), show="open"),
                        Field(key="frequency", label="Frequency", width=Unit.PIXEL(200)),
                    ],
                ),
            ],
            legends=[
                Legend(
                    items=[
                        LegendItem(
                            icon=WBIcon.LOCK.icon,
                            label="Locked",
                        ),
                    ],
                )
            ],
        )

    def get_instance_display(self) -> Display:
        return create_simple_display(
            [
                ["notification_type", "notification_type", "frequency"],
                ["enable_web", "enable_mobile", "enable_email"],
            ]
        )


class NotificationTypeSettingEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_update_endpoint(self):
        return "{{_update_url}}"
