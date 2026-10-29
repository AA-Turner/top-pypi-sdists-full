__lazy_modules__ = ["django.http"]

from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.corputils import urls
from allianceauth.menu.hooks import MenuItemHook
from allianceauth.services.hooks import UrlHook

if TYPE_CHECKING:
    from django.http import HttpRequest


class CorpStats(MenuItemHook):
    def __init__(self) -> None:
        MenuItemHook.__init__(
            self,
            _('Corporation Stats'),
            'fa-solid fa-share-nodes',
            'corputils:view',
            navactive=['corputils:']
        )

    def render(self, request: "HttpRequest") -> str:
        if request.user.has_perm('corputils.view_corp_corpstats') or request.user.has_perm(
                'corputils.view_alliance_corpstats') or request.user.has_perm(
                'corputils.add_corpstats') or request.user.has_perm('corputils.view_state_corpstats'):
            return MenuItemHook.render(self, request)
        return ''


@hooks.register('menu_item_hook')
def register_menu() -> CorpStats:
    return CorpStats()


@hooks.register('url_hook')
def register_url() -> UrlHook:
    return UrlHook(urls, 'corputils', r'^corpstats/')
