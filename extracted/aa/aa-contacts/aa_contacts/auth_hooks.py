from typing import Literal

from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook
from django.utils.translation import gettext_lazy as _

from . import urls
from .models import StandingFilter


class AAContactsHook(MenuItemHook):
    def __init__(self) -> None:
        super().__init__(
            _("Contacts"),
            "fas fa-address-book",
            "aa_contacts:index",
            navactive=["aa_contacts:"],
        )


@hooks.register("menu_item_hook")
def register_menu() -> AAContactsHook:
    return AAContactsHook()


@hooks.register("url_hook")
def register_urls() -> UrlHook:
    return UrlHook(urls, "aa_contacts", r"^contacts/")


@hooks.register("charlink")
def register_charlink_hook() -> Literal["aa_contacts.charlink_hook"]:
    return "aa_contacts.charlink_hook"


@hooks.register("secure_group_filters")
def filters() -> list[type[StandingFilter]]:
    return [StandingFilter]
