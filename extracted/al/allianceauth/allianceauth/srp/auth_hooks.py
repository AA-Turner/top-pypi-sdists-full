__lazy_modules__ = ["django.http"]

from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.menu.hooks import MenuItemHook
from allianceauth.services.hooks import UrlHook

from . import urls
from .managers import SRPManager

if TYPE_CHECKING:
    from django.http import HttpRequest


class SrpMenu(MenuItemHook):
    def __init__(self) -> None:
        MenuItemHook.__init__(
            self, _('Ship Replacement'),
            'fa-regular fa-money-bill-1',
            'srp:management',
            navactive=['srp:']
        )

    def render(self, request: "HttpRequest") -> str:
        if request.user.has_perm('srp.access_srp'):
            app_count = SRPManager.pending_requests_count_for_user(request.user)
            self.count = app_count if app_count and app_count > 0 else None
            return MenuItemHook.render(self, request)
        return ''


@hooks.register('menu_item_hook')
def register_menu() -> SrpMenu:
    return SrpMenu()


@hooks.register('url_hook')
def register_url() -> UrlHook:
    return UrlHook(urls, 'srp', r'^srp/')
