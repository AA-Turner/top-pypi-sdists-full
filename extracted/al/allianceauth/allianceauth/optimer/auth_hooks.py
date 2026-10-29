__lazy_modules__ = ["django.http"]

from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.menu.hooks import MenuItemHook
from allianceauth.optimer.views import dashboard_ops
from allianceauth.services.hooks import UrlHook

from . import urls

if TYPE_CHECKING:
    from django.http import HttpRequest


class OpTimerboardMenu(MenuItemHook):
    def __init__(self) -> None:
        MenuItemHook.__init__(
            self, _('Fleet Operations'),
            'fa-solid fa-exclamation',
            'optimer:view',
            navactive=['optimer:']
        )

    def render(self, request: "HttpRequest") -> str:
        if request.user.has_perm('auth.optimer_view'):
            return MenuItemHook.render(self, request)
        return ''


@hooks.register('menu_item_hook')
def register_menu() -> OpTimerboardMenu:
    return OpTimerboardMenu()


@hooks.register('url_hook')
def register_url() -> UrlHook:
    return UrlHook(urls, 'optimer', r'^optimer/')


class NextOpsHook(hooks.DashboardItemHook):
    def __init__(self) -> None: #TODO add the view perms so if they cant see it is not rendered
        hooks.DashboardItemHook.__init__(
            self,
            dashboard_ops,
            6
        )


@hooks.register('dashboard_hook')
def register_groups_hook() -> NextOpsHook:
    return NextOpsHook()
