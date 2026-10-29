"""Admin site for admin status applicaton"""

__lazy_modules__ = ["django.http"]

from typing import TYPE_CHECKING

from django.contrib import admin

from allianceauth.admin_status.models import ApplicationAnnouncement

if TYPE_CHECKING:
    from django.http import HttpRequest


@admin.register(ApplicationAnnouncement)
class ApplicationAnnouncementAdmin(admin.ModelAdmin):
    list_display = ["application_name", "announcement_number", "announcement_text", "hide_announcement"]
    list_filter = ["hide_announcement"]
    ordering = ["application_name", "announcement_number"]
    readonly_fields = ["application_name", "announcement_number", "announcement_text", "announcement_url"]
    fields = ["application_name", "announcement_number", "announcement_text", "announcement_url", "hide_announcement"]

    def has_add_permission(self, request: "HttpRequest") -> bool:
        return False

    def has_delete_permission(self, request: "HttpRequest", obj: ApplicationAnnouncement | None = None) -> bool:
        return False
