__lazy_modules__ = ["django.db.models", "django.http"]

import logging
from typing import TYPE_CHECKING

from django.contrib import admin

from ...admin import ServicesUserAdmin
from . import __title__
from .auth_hooks import DiscordService
from .models import DiscordUser
from .utils import LoggerAddTag

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpRequest

logger = LoggerAddTag(logging.getLogger(__name__), __title__)


@admin.register(DiscordUser)
class DiscordUserAdmin(ServicesUserAdmin):
    search_fields = ServicesUserAdmin.search_fields + ('uid', 'username')
    list_display = ServicesUserAdmin.list_display + ('activated', '_username', '_uid')
    list_filter = ServicesUserAdmin.list_filter + ('activated',)
    ordering = ('-activated',)

    def delete_queryset(self, request: "HttpRequest", queryset: "QuerySet[DiscordUser]") -> None:
        for user in queryset:
            user.delete_user()

    @admin.display(description='Discord ID (UID)', ordering='uid')
    def _uid(self, obj: DiscordUser) -> int:
        return obj.uid

    @admin.display(description='Discord Username', ordering='username')
    def _username(self, obj: DiscordUser) -> str:
        return DiscordService.get_discord_username(
            username=obj.username, discriminator=obj.discriminator
        )
