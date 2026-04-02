"""Admin site for Inactivity."""

# pylint: disable = missing-class-docstring, missing-function-docstring

from django.conf import settings
from django.contrib import admin

from .models import InactivityPing, InactivityPingConfig, LeaveOfAbsence, Webhook


@admin.register(InactivityPingConfig)
class InactivityPingConfigAdmin(admin.ModelAdmin):
    list_display = ("name", "days", "_groups", "_states")
    filter_horizontal = ("groups", "states")

    def _groups(self, obj):
        return ", ".join(obj.groups.values_list("name", flat=True))

    def _states(self, obj):
        return (", ".join(obj.states.values_list("name", flat=True)),)


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ("name", "webhook_type", "url")
    filter_horizontal = ("ping_configs",)
    actions = ["send_test_message"]

    @admin.display(description="Send test message to selected webhooks")
    def send_test_message(self, request, queryset):
        for webhook in queryset:
            webhook.send_message("Test message from Inactivity app.")


if settings.DEBUG:

    @admin.register(InactivityPing)
    class InactivityPingAdmin(admin.ModelAdmin):
        list_display = (
            "timestamp",
            "user",
            "config",
        )
        list_filter = (
            ("user", admin.RelatedOnlyFieldListFilter),
            ("config", admin.RelatedOnlyFieldListFilter),
        )
        order = ["-timestamp"]

        def has_add_permission(self, request):
            return False

        def has_change_permission(self, request, obj=None):
            return False

    @admin.register(LeaveOfAbsence)
    class LeaveOfAbsenceAdmin(admin.ModelAdmin):
        list_display = ("pk", "start", "end", "user", "_status", "approver")
        ordering = ("-start",)
        actions = ["approve_leaveofabsence"]

        def get_queryset(self, request):
            qs = super().get_queryset(request)
            return qs.annotate_status().select_related("user", "approver")

        def _status(self, obj) -> bool:
            return obj.status

        @admin.display(description="Approve selected leave of absences")
        def approve_leaveofabsence(self, request, queryset):
            queryset.update(approver=request.user)

        def has_add_permission(self, request):
            return False

        def has_change_permission(self, request, obj=None):
            return False
