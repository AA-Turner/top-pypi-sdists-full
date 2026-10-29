__lazy_modules__ = ["django.http"]

from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.menu.hooks import MenuItemHook
from allianceauth.services.hooks import UrlHook

from . import urls
from .models import Application

if TYPE_CHECKING:
    from django.http import HttpRequest


class ApplicationsMenu(MenuItemHook):
    def __init__(self) -> None:
        MenuItemHook.__init__(
            self,
            _('Applications'),
            'fa-regular fa-file',
            'hrapplications:index',
            navactive=['hrapplications:'])

    def render(self, request: "HttpRequest") -> str:
        app_count = Application.objects.pending_requests_count_for_user(request.user)
        self.count = app_count if app_count and app_count > 0 else None
        return MenuItemHook.render(self, request)


@hooks.register('menu_item_hook')
def register_menu() -> ApplicationsMenu:
    return ApplicationsMenu()


class ApplicationsUrls(UrlHook):
    def __init__(self) -> None:
        UrlHook.__init__(self, urls, 'hrapplications', r'^hr/')


@hooks.register('url_hook')
def register_url() -> ApplicationsUrls:
    return ApplicationsUrls()
