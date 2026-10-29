__lazy_modules__ = ["django.http"]

from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.menu.hooks import MenuItemHook
from allianceauth.services.hooks import UrlHook

from . import urls
from .managers import GroupManager

if TYPE_CHECKING:
    from django.http import HttpRequest


class GroupManagementMenuItem(MenuItemHook):
    """ This class ensures only authorized users will see the menu entry """

    def __init__(self) -> None:
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            text=_("Group Management"),
            classes="fa-solid fa-users-gear",
            url_name="groupmanagement:management",
            order=50,
            navactive=[
                "groupmanagement:management",  # group requests view
                "groupmanagement:membership",  # group membership view
                "groupmanagement:audit_log",  # group audit log view
            ],
        )

    def render(self, request: "HttpRequest") -> str:
        if GroupManager.can_manage_groups(request.user):
            app_count = GroupManager.pending_requests_count_for_user(request.user)
            self.count = app_count if app_count and app_count > 0 else None
            return MenuItemHook.render(self, request)
        return ""


"""
            <li class="d-flex m-2 p-2 pt-0 pb-0 mt-0 mb-0">
                <i class="fa-solid fa-users fa-fw align-self-center me-2"></i>
                <a class="nav-link flex-fill align-self-center {% navactive request 'groupmanagement:groups' %}" href="{% url 'groupmanagement:groups' %}">
                    {% translate "Groups" %}
                </a>
            </li>
"""


class GroupsMenuItem(MenuItemHook):
    def __init__(self) -> None:
        MenuItemHook.__init__(
            self,
            text=_("Groups"),
            classes="fa-solid fa-users",
            url_name="groupmanagement:groups",
            order=25,
            navactive=[
                "groupmanagement:groups",  # group list view
            ],
        )

    def render(self, request: "HttpRequest") -> str:
        return MenuItemHook.render(self, request)


@hooks.register("menu_item_hook")
def register_manager_menu() -> GroupManagementMenuItem:
    return GroupManagementMenuItem()


@hooks.register("menu_item_hook")
def register_groups_menu() -> GroupsMenuItem:
    return GroupsMenuItem()


@hooks.register("url_hook")
def register_urls() -> UrlHook:
    return UrlHook(urls, "group", r"^groups/")
