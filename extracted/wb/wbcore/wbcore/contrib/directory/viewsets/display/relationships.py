from enum import Enum
from typing import Optional

from django.utils.translation import gettext as _

from wbcore.contrib.color.enums import WBColor
from wbcore.contrib.directory.models import ClientManagerRelationship
from wbcore.contrib.icons import WBIcon
from wbcore.metadata.configs import display as dp
from wbcore.metadata.configs.display.instance_display.shortcuts import (
    Display,
    create_simple_display,
)
from wbcore.metadata.configs.display.instance_display.utils import repeat_field
from wbcore.metadata.configs.display.view_config import DisplayViewConfig


class ClientManagerRelationshipColor(Enum):
    DRAFT = WBColor.RED_LIGHT.value
    PENDING = WBColor.YELLOW_LIGHT.value
    APPROVED = WBColor.GREEN_LIGHT.value
    PENDING_REMOVE = WBColor.YELLOW_DARK.value
    REMOVED = WBColor.GREY.value


class RelationshipDisplayConfig(DisplayViewConfig):
    def get_instance_display(self) -> Display:
        return create_simple_display([["from_entry", "to_entry", "relationship_type"]])

    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="relationship_type", label=_("Type")),
                dp.Field(key="from_entry", label=_("From")),
                dp.Field(key="to_entry", label=_("To")),
            ]
        )


class RelationshipEntryDisplay(DisplayViewConfig):
    def get_instance_display(self) -> Display:
        return create_simple_display([["relationship_type", "to_entry"]])

    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="relationship_type", label=_("Relationship Type")),
                dp.Field(key="to_entry", label=_("Relationship To")),
            ]
        )


class RelationshipTypeDisplayConfig(DisplayViewConfig):
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="title", label=_("Name")),
                dp.Field(key="counter_relationship", label=_("Counter Relationship")),
            ]
        )

    def get_instance_display(self) -> Display:
        return create_simple_display([["title", "counter_relationship"]])


class EmployerEmployeeRelationshipDisplayConfig(DisplayViewConfig):
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="employer", label=_("Employer")),
                dp.Field(key="employee", label=_("Employee")),
                dp.Field(key="primary", label=_("Company Is Primary Employer")),
                dp.Field(key="position", label=_("Position In Company")),
            ],
            legends=[
                dp.Legend(
                    key="primary",
                    items=[
                        dp.LegendItem(
                            icon=WBColor.GREEN_LIGHT.value,
                            label=_("Company Is Primary Employer"),
                            value=True,
                        ),
                    ],
                ),
            ],
            formatting=[
                dp.Formatting(
                    column="primary",
                    formatting_rules=[
                        dp.FormattingRule(
                            style={"backgroundColor": WBColor.GREEN_LIGHT.value},
                            condition=("==", True),
                        ),
                    ],
                )
            ],
        )

    def get_instance_display(self) -> Display:
        return create_simple_display(
            [
                ["employer", "employee"],
                ["primary", "position"],
            ]
        )


class EmployeeEmployerDisplayConfig(DisplayViewConfig):
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="employee", label=_("Employee")),
                dp.Field(key="primary", label=_("Company Is Primary Employer")),
                dp.Field(key="position", label=_("Position In Company")),
                dp.Field(key="position_name", label=_("Position Name")),
                dp.Field(key="employee_profile_pic", label=_("Profile Picture")),
            ],
            legends=[
                dp.Legend(
                    key="primary",
                    items=[
                        dp.LegendItem(
                            icon=WBColor.GREEN_LIGHT.value,
                            label=_("Company Is Primary Employer"),
                            value=True,
                        ),
                    ],
                ),
            ],
            formatting=[
                dp.Formatting(
                    column="primary",
                    formatting_rules=[
                        dp.FormattingRule(
                            style={"backgroundColor": WBColor.GREEN_LIGHT.value},
                            condition=("==", True),
                        ),
                    ],
                )
            ],
        )

    def get_instance_display(self) -> Display:
        return create_simple_display([[repeat_field(2, "employee")], ["primary", "position"]])


class EmployerEmployeeDisplayConfig(DisplayViewConfig):
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="employer", label=_("Employer")),
                dp.Field(key="primary", label=_("Company Is Primary Employer")),
                dp.Field(key="position", label=_("Position In Company")),
                dp.Field(key="position_name", label=_("Position Name")),
                dp.Field(key="employer_profile_pic", label=_("Profile Picture")),
            ],
            legends=[
                dp.Legend(
                    key="primary",
                    items=[
                        dp.LegendItem(
                            icon=WBColor.GREEN_LIGHT.value,
                            label=_("Company Is Primary Employer"),
                            value=True,
                        ),
                    ],
                ),
            ],
            formatting=[
                dp.Formatting(
                    column="primary",
                    formatting_rules=[
                        dp.FormattingRule(
                            style={"backgroundColor": WBColor.GREEN_LIGHT.value},
                            condition=("==", True),
                        ),
                    ],
                )
            ],
        )

    def get_instance_display(self) -> Display:
        return create_simple_display([[repeat_field(2, "employer")], ["primary", "position"]])


class ClientManagerModelDisplay(DisplayViewConfig):
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        fields = [
            dp.Field(key="client", label=_("Client")),
            dp.Field(key="relationship_manager", label=_("Relationship Manager")),
            dp.Field(key="created", label=_("Created")),
        ]
        if "client" in self.request.GET:
            fields = fields[1:]
        elif "relationship_manager" in self.request.GET:
            fields = fields[0::2]

        return dp.ListDisplay(
            fields=fields,
            legends=[
                dp.Legend(
                    key="status",
                    items=[
                        dp.LegendItem(
                            icon=ClientManagerRelationshipColor.DRAFT.value,
                            label=ClientManagerRelationship.Status.DRAFT.label,
                            value=ClientManagerRelationship.Status.DRAFT.name,
                        ),
                        dp.LegendItem(
                            icon=ClientManagerRelationshipColor.PENDING.value,
                            label=ClientManagerRelationship.Status.PENDINGADD.label,
                            value=ClientManagerRelationship.Status.PENDINGADD.name,
                        ),
                        dp.LegendItem(
                            icon=ClientManagerRelationshipColor.APPROVED.value,
                            label=ClientManagerRelationship.Status.APPROVED.label,
                            value=ClientManagerRelationship.Status.APPROVED.name,
                        ),
                        dp.LegendItem(
                            icon=ClientManagerRelationshipColor.PENDING_REMOVE.value,
                            label=ClientManagerRelationship.Status.PENDINGREMOVE.label,
                            value=ClientManagerRelationship.Status.PENDINGREMOVE.name,
                        ),
                        dp.LegendItem(
                            icon=ClientManagerRelationshipColor.REMOVED.value,
                            label=ClientManagerRelationship.Status.REMOVED.label,
                            value=ClientManagerRelationship.Status.REMOVED.name,
                        ),
                    ],
                ),
                dp.Legend(
                    key="primary",
                    items=[
                        dp.LegendItem(icon=WBIcon.FAVORITE.icon, label=_("Primary"), value=True),
                    ],
                ),
            ],
            formatting=[
                dp.Formatting(
                    column="status",
                    formatting_rules=[
                        dp.FormattingRule(
                            style={"backgroundColor": WBColor.YELLOW_LIGHT.value},
                            condition=("==", ClientManagerRelationship.Status.PENDINGADD.name),
                        ),
                        dp.FormattingRule(
                            style={"backgroundColor": WBColor.YELLOW_DARK.value},
                            condition=("==", ClientManagerRelationship.Status.PENDINGREMOVE.name),
                        ),
                        dp.FormattingRule(
                            style={"backgroundColor": WBColor.GREEN_LIGHT.value},
                            condition=("==", ClientManagerRelationship.Status.APPROVED.name),
                        ),
                        dp.FormattingRule(
                            style={"backgroundColor": WBColor.RED_LIGHT.value},
                            condition=("==", ClientManagerRelationship.Status.DRAFT.name),
                        ),
                        dp.FormattingRule(
                            style={"backgroundColor": WBColor.GREY.value},
                            condition=("==", ClientManagerRelationship.Status.REMOVED.name),
                        ),
                    ],
                )
            ],
        )

    def get_instance_display(self) -> Display:
        fields = []
        if "pk" not in self.view.kwargs:
            fields.append([repeat_field(2, "primary")])

        else:
            fields.append(["status", "primary"])

        if "client" in self.request.GET:
            fields.append(["relationship_manager", "."])
        else:
            fields.append(["client", "relationship_manager"])

        return create_simple_display(fields)


class UserIsClientDisplayConfig(DisplayViewConfig):
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="relationship_manager_name", label=_("Name")),
                dp.Field(key="relationship_manager_email", label=_("Telephone")),
                dp.Field(key="relationship_manager_phone_number", label=_("Email")),
            ]
        )
