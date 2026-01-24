from typing import Optional

from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

from wbcore.contrib.color.enums import WBColor
from wbcore.metadata.configs import display as dp
from wbcore.metadata.configs.display.instance_display.shortcuts import Display
from wbcore.metadata.configs.display.view_config import DisplayViewConfig


class DocumentModelDisplay(DisplayViewConfig):
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="name", label=_("Name")),
                dp.Field(key="document_type", label=_("Type")),
                dp.Field(key="permission_type", label=_("Permission")),
                dp.Field(key="valid_from", label=_("Valid From")),
                dp.Field(key="valid_until", label=_("Valid Until")),
                dp.Field(key="updated", label=_("Updated")),
            ],
            legends=[
                dp.Legend(
                    key="system_created",
                    items=[
                        dp.LegendItem(
                            icon=WBColor.YELLOW_LIGHT.value,
                            label=gettext_lazy("Created By System"),
                            value=True,
                        ),
                    ],
                ),
            ],
            formatting=[
                dp.Formatting(
                    column="system_created",
                    formatting_rules=[
                        dp.FormattingRule(
                            style={"backgroundColor": WBColor.YELLOW_LIGHT.value},
                            condition=("==", True),
                        ),
                    ],
                ),
            ],
        )

    def get_instance_display(self) -> Display:
        return Display(
            pages=[
                dp.Page(
                    title="Main Information",
                    layouts={
                        dp.default(): dp.Layout(
                            grid_template_areas=[
                                ["file", "file", "file"],
                                ["name", "document_type", "permission_type"],
                                ["created", "updated", "system_created"],
                                ["valid_from", "valid_until", "."],
                                [
                                    "description",
                                    "description",
                                    "description",
                                ],
                            ],
                            grid_template_columns=[dp.repeat_field(3, "1fr")],
                        )
                    },
                ),
                dp.Page(
                    title="Connected Items",
                    layouts={
                        dp.default(): dp.Layout(
                            grid_template_areas=[["relationships"]],
                            grid_template_columns=[dp.Style.fr(1)],
                            grid_template_rows=[dp.Style.fr(1)],
                            inlines=[dp.Inline(key="relationships", endpoint="relationships")],
                        )
                    },
                ),
                dp.Page(
                    title="Sharable Links",
                    layouts={
                        dp.default(): dp.Layout(
                            grid_template_areas=[["shareable_links"]],
                            grid_template_columns=[dp.Style.fr(1)],
                            grid_template_rows=[dp.Style.fr(1)],
                            inlines=[dp.Inline(key="shareable_links", endpoint="shareable_links")],
                        )
                    },
                ),
            ]
        )
