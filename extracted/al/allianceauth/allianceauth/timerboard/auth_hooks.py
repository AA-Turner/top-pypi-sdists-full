__lazy_modules__ = ["django.http"]

from typing import TYPE_CHECKING

from allianceauth import hooks
from allianceauth.menu.hooks import MenuItemHook
from allianceauth.services.hooks import UrlHook
from allianceauth.timerboard.views import dashboard_timers

from . import urls

if TYPE_CHECKING:
    from django.http import HttpRequest


class TimerboardMenu(MenuItemHook):
    def __init__(self) -> None:
        MenuItemHook.__init__(
            self, 'Structure Timers',
            'fa-regular fa-clock',
            'timerboard:view',
            navactive=['timerboard:']
        )

    def render(self, request: "HttpRequest") -> str:
        if request.user.has_perm('auth.timer_view'):
            return MenuItemHook.render(self, request)
        return ''


@hooks.register('menu_item_hook')
def register_menu() -> TimerboardMenu:
    return TimerboardMenu()


@hooks.register('url_hook')
def register_url() -> UrlHook:
    return UrlHook(urls, 'timerboard', r'^timers/')


class NextTimersHook(hooks.DashboardItemHook):
    def __init__(self) -> None:  #TODO add the view permms so if they cant see it is not rendered
        hooks.DashboardItemHook.__init__(
            self,
            dashboard_timers,
            7
        )


@hooks.register('dashboard_hook')
def register_groups_hook() -> NextTimersHook:
    return NextTimersHook()
