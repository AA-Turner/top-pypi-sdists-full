"""Filters for the menu app."""

__lazy_modules__ = ["allianceauth.menu.managers", "django.http"]

from typing import TYPE_CHECKING

from django.contrib import admin
from django.utils.translation import gettext_noop as _

from allianceauth.menu.models import MenuItem

if TYPE_CHECKING:
    from django.http import HttpRequest

    from allianceauth.menu.managers import MenuItemQuerySet


class MenuItemTypeListFilter(admin.SimpleListFilter):
    """Allow filtering admin changelist by menu item type."""

    title = _("type")
    parameter_name = "type"

    def lookups(self, request: "HttpRequest", model_admin: admin.ModelAdmin) -> list[tuple[str, str]]:
        return [(obj.value, obj.label.title()) for obj in MenuItem.MenuItemType]

    def queryset(self, request: "HttpRequest", queryset: "MenuItemQuerySet") -> "MenuItemQuerySet":
        if value := self.value():
            return queryset.annotate_item_type_2().filter(
                item_type_2=MenuItem.MenuItemType(value).value
            )

        return None
