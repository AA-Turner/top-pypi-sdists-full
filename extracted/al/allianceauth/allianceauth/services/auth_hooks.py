__lazy_modules__ = ["django.http"]

from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _

from allianceauth import hooks

from ..menu.hooks import MenuItemHook
from .hooks import ServicesHook

if TYPE_CHECKING:
    from django.http import HttpRequest


class Services(MenuItemHook):
    def __init__(self) -> None:
        MenuItemHook.__init__(
            self,
            _('Services'),
            'fa-solid fa-gears',
            'services:services', 100
        )

    def render(self, request: "HttpRequest") -> str:
        for svc in ServicesHook.get_services():
            if svc.service_active_for_user(request.user):
                return MenuItemHook.render(self, request)
        return ''


@hooks.register('menu_item_hook')
def register_menu() -> Services:
    return Services()
