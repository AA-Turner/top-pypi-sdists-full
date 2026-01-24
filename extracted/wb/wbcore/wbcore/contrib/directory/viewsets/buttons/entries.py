from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from rest_framework.reverse import reverse

from wbcore.contrib.icons import WBIcon
from wbcore.enums import RequestType
from wbcore.metadata.configs import buttons as bt
from wbcore.metadata.configs.buttons.view_config import ButtonViewConfig


class EntryModelButtonConfig(ButtonViewConfig):
    CRM_BUTTONS = ()

    def get_custom_list_instance_buttons(self):
        return {
            bt.DropDownButton(
                label=_("Quick Action"),
                icon=WBIcon.UNFOLD.icon,
                buttons=(
                    bt.WidgetButton(key="employees", label=_("Employees"), icon=WBIcon.PEOPLE.icon, weight=2),
                    bt.WidgetButton(
                        key="manager", label=_("Relationship Managers"), icon=WBIcon.SUPERVISE.icon, weight=3
                    ),
                ),
                weight=1,
            )
        }

    def get_custom_instance_buttons(self):
        return {
            bt.WidgetButton(key="employees", label=_("Employees"), icon=WBIcon.PEOPLE.icon, weight=2),
            bt.WidgetButton(key="manager", label=_("Relationship Managers"), icon=WBIcon.SUPERVISE.icon, weight=3),
        }


class PersonModelButtonConfig(EntryModelButtonConfig):
    CRM_BUTTONS = EntryModelButtonConfig.CRM_BUTTONS + (
        bt.WidgetButton(key="client", label=gettext_lazy("Clients"), icon=WBIcon.PEOPLE.icon),
        bt.WidgetButton(
            key="manager", label=gettext_lazy("Relationship Managers"), icon=WBIcon.SUPERVISE.icon, weight=3
        ),
    )

    def get_custom_instance_buttons(self):
        return {
            bt.WidgetButton(key="employers", label=_("Employers"), icon=WBIcon.WORK.icon, weight=2),
            bt.DropDownButton(label=_("Client/Manager"), icon=WBIcon.UNFOLD.icon, buttons=self.CRM_BUTTONS, weight=3),
        }


class CompanyModelButtonConfig(EntryModelButtonConfig):
    CRM_BUTTONS = EntryModelButtonConfig.CRM_BUTTONS + (
        bt.WidgetButton(key="employees", label=gettext_lazy("Employees"), icon=WBIcon.PEOPLE.icon),
    )


class EmployeeCompanyModelButtonConfig(ButtonViewConfig):
    def get_custom_buttons(self):
        if not self.view.kwargs.get("pk", None):
            base_url = reverse("wbcore:directory:person-list", args=[], request=self.request)
            return {
                bt.WidgetButton(
                    endpoint=f"{base_url}?employers={self.view.kwargs.get('company_id')}",
                    label=_("New Person"),
                    icon=WBIcon.PERSON_ADD.icon,
                    new_mode=True,
                )
            }
        return {}

    def get_custom_list_instance_buttons(self):
        return {
            bt.ActionButton(
                method=RequestType.PATCH,
                identifiers=("directory:employeremployee",),
                key="delete",
                label=_("Delete Relationship"),
                icon=WBIcon.DELETE.icon,
                description_fields=_("<p> Are you sure you want to delete the relationship? </p>"),
                title=_("Delete Relationship"),
                action_label=_("Deletion"),
            ),
            bt.WidgetButton(
                key="eer_relationship_instance", label=_("Relationship Instance"), icon=WBIcon.GROUPS.icon
            ),
        }


class EmployerPersonModelButtonConfig(ButtonViewConfig):
    def get_custom_buttons(self):
        if not self.view.kwargs.get("pk", None):
            base_url = reverse("wbcore:directory:company-list", args=[], request=self.request)
            return {
                bt.WidgetButton(
                    endpoint=f"{base_url}?employees={self.view.kwargs.get('person_id')}",
                    label=_("New Company"),
                    icon=WBIcon.ADD.icon,
                    new_mode=True,
                )
            }
        return {}

    def get_custom_list_instance_buttons(self):
        return {
            bt.ActionButton(
                method=RequestType.PATCH,
                identifiers=("directory:employeremployee",),
                key="delete",
                label=_("Delete Relationship"),
                icon=WBIcon.DELETE.icon,
                description_fields=_("<p> Are you sure you want to delete the relationship? </p>"),
                title=_("Delete Relationship"),
                action_label=_("Deletion"),
            ),
            bt.WidgetButton(
                key="eer_relationship_instance", label=_("Relationship Instance"), icon=WBIcon.GROUPS.icon
            ),
        }
