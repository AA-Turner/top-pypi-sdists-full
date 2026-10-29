from django.contrib import admin

from .models import ImpersonationLog


@admin.register(ImpersonationLog)
class ImpersonationLogAdmin(admin.ModelAdmin):
    """Read only, so the audit trail can't be edited from the admin site."""
    list_display = ('started', 'ended', 'impersonator_username', 'target_username')
    list_filter = ('started',)
    search_fields = ('impersonator_username', 'target_username')
    date_hierarchy = 'started'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
