__lazy_modules__ = ["django.http"]

from typing import TYPE_CHECKING

from allianceauth import hooks
from allianceauth.menu.hooks import MenuItemHook
from allianceauth.services.hooks import UrlHook

from . import urls

if TYPE_CHECKING:
    from django.http import HttpRequest


class PermissionsTool(MenuItemHook):
    def __init__(self) -> None:
        MenuItemHook.__init__(
            self,
            'Permissions Audit',
            'fa-solid fa-id-card',
            'permissions_tool:overview',
            order=400,
            navactive=['permissions_tool:']
        )

    def render(self, request: "HttpRequest") -> str:
        if request.user.has_perm('permissions_tool.audit_permissions'):
            return MenuItemHook.render(self, request)
        return ''


@hooks.register('menu_item_hook')
def register_menu() -> PermissionsTool:
    return PermissionsTool()


@hooks.register('url_hook')
def register_url() -> UrlHook:
    return UrlHook(urls, 'permissions_tool', r'^permissions/')
