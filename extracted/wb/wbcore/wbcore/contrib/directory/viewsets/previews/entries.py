from contextlib import suppress

from django.utils.translation import gettext as _

from wbcore.contrib.icons import WBIcon
from wbcore.metadata.configs import buttons as bt
from wbcore.metadata.configs.display.instance_display.shortcuts import (
    Display,
    create_simple_display,
)
from wbcore.metadata.configs.preview import PreviewViewConfig


class EntryPreviewConfig(PreviewViewConfig):
    def get_display(self) -> Display:
        fields = [
            ["computed_str"],
            ["primary_email"],
            ["primary_telephone"],
            ["primary_manager_name"],
        ]
        with suppress(Exception):
            entry = self.view.get_object()
            if entry.profile_image:
                fields.insert(0, "profile_image")

        return create_simple_display(fields)

    def get_buttons(self):
        return [
            bt.WidgetButton(key="activity", icon=WBIcon.CALENDAR.icon, label=_("Show all activities")),
        ]
