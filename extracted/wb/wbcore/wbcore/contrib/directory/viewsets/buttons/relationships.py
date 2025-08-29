from django.utils.translation import gettext as _
from rest_framework.reverse import reverse

from wbcore.contrib.directory.models import ClientManagerRelationship
from wbcore.contrib.directory.permissions import IsClientManagerRelationshipAdmin
from wbcore.contrib.icons import WBIcon
from wbcore.enums import RequestType
from wbcore.metadata.configs import buttons as bt
from wbcore.metadata.configs.buttons.view_config import ButtonViewConfig


class EmployerEmployeeRelationshipButtonConfig(ButtonViewConfig):
    def get_custom_buttons(self):
        if not self.new_mode:
            if employer_id := self.view.kwargs.get("employer_id", None):
                base_url = reverse("wbcore:directory:person-list", args=[], request=self.request)
                return {
                    bt.WidgetButton(
                        endpoint=f"{base_url}?employers={employer_id}",
                        label=_("New Person"),
                        icon=WBIcon.PERSON_ADD.icon,
                        new_mode=True,
                    )
                }
            if employee_id := self.view.kwargs.get("employee_id", None):
                base_url = reverse("wbcore:directory:company-list", args=[], request=self.request)
                return {
                    bt.WidgetButton(
                        endpoint=f"{base_url}?employees={employee_id}",
                        label=_("New Company"),
                        icon=WBIcon.ADD.icon,
                        new_mode=True,
                    )
                }
        return {}


class ClientManagerRelationshipButtonConfig(ButtonViewConfig):
    def get_custom_buttons(self):
        buttons = set()
        if (
            IsClientManagerRelationshipAdmin().has_permission(self.request, self.view)
            and ClientManagerRelationship.objects.filter(
                status__in=[
                    ClientManagerRelationship.Status.PENDINGADD,
                    ClientManagerRelationship.Status.PENDINGREMOVE,
                ]
            ).exists()
        ):
            buttons.add(
                bt.ActionButton(
                    method=RequestType.PATCH,
                    identifiers=("directory:clientmanagerrelationship",),
                    endpoint=reverse("wbcore:directory:clientmanagerrelationship-approveallpendingrequests"),
                    label=_("Approve All Pending Requests"),
                    icon=WBIcon.APPROVE.icon,
                    description_fields=_(
                        "<p> Are you sure you want to approve all pending (add and remove) requests ? </p>"
                    ),
                    title=_("Approve All Pending Requests"),
                    action_label=_("Approved"),
                )
            )
        return buttons
