from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from . import urls
from .models import LeaveOfAbsence


class LeaveOfAbsenceMenuItem(MenuItemHook):
    def __init__(self):
        MenuItemHook.__init__(
            self,
            _("Leave of Absence"),
            "fas fa-business-time fa-fw",
            "inactivity:index",
            navactive=["inactivity:"],
        )

    def render(self, request):
        if request.user.has_perm("inactivity:manage_requests"):
            app_count = LeaveOfAbsence.objects.unapproved_count()
            self.count = app_count if app_count and app_count > 0 else None
        if request.user.has_perm("inactivity.basic_access"):
            return MenuItemHook.render(self, request)
        return ""


@hooks.register("menu_item_hook")
def register_menu():
    return LeaveOfAbsenceMenuItem()


@hooks.register("url_hook")
def register_urls():
    return UrlHook(urls, "inactivity", r"^inactivity/")
