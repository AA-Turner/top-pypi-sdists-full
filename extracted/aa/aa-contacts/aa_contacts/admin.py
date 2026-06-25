from django.apps import apps
from django.contrib import admin

from .models import (
    AllianceContact,
    AllianceContactServerLink,
    CorporationContact,
    CorporationContactServerLink,
    StandingFilter,
)


class ReadOnlyServerLinkInline(admin.TabularInline):
    extra = 0
    fields = ("name", "url", "password", "color")
    readonly_fields = fields
    can_delete = False
    show_change_link = False

    def has_add_permission(self, request, obj):  # noqa: ARG002
        return False


class AllianceContactServerLinkInline(ReadOnlyServerLinkInline):
    model = AllianceContactServerLink


class CorporationContactServerLinkInline(ReadOnlyServerLinkInline):
    model = CorporationContactServerLink


@admin.register(AllianceContact)
class AllianceContactAdmin(admin.ModelAdmin):
    exclude = ("contact_id",)
    readonly_fields = ("alliance", "contact_type", "standing", "labels")
    inlines = (AllianceContactServerLinkInline,)


@admin.register(CorporationContact)
class CorporationContactAdmin(admin.ModelAdmin):
    exclude = ("contact_id",)
    readonly_fields = (
        "corporation",
        "contact_type",
        "standing",
        "labels",
        "is_watched",
    )
    inlines = (CorporationContactServerLinkInline,)


class StandingFilterAdmin(admin.ModelAdmin):
    raw_id_fields = ("corporations", "alliances")


if apps.is_installed("securegroups"):
    admin.site.register(StandingFilter, StandingFilterAdmin)
