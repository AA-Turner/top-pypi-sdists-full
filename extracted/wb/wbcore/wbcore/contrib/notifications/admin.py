from datetime import date, timedelta

from django.contrib import admin

from wbcore.contrib.notifications.models.notifications import (
    send_notification_as_task,
)

from .models import (
    Notification,
    NotificationType,
    NotificationTypeSetting,
    NotificationUserToken,
)


@admin.register(Notification)
class NotificationModelAdmin(admin.ModelAdmin):
    search_fields = ["title", "body"]

    list_display = [
        "title",
        "user",
        "notification_type",
        "endpoint",
        "sent_email",
        "sent_mobile",
        "sent_web",
        "read",
        "created",
    ]

    @admin.action(description="Send Web Notification")
    def send_notification(self, request, queryset):
        for notification in queryset:
            send_notification_as_task.delay(notification.id)

    actions = [send_notification]


@admin.register(NotificationUserToken)
class NotificationUserTokenModelAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "device_type", "updated")

    @admin.action(description="Remove all stale tokens")
    def remove_stale_tokens(self, request, queryset):
        cutoff_date = date.today() - timedelta(days=60)
        queryset.filter(updated__date__lte=cutoff_date).delete()

    actions = [remove_stale_tokens]


@admin.register(NotificationTypeSetting)
class NotificationTypeSettingModelAdmin(admin.ModelAdmin):
    list_display = ("notification_type", "user", "enable_web", "enable_mobile", "enable_email", "frequency")


@admin.register(NotificationType)
class NotificationTypeModelAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "title",
        "contenttype",
        "default_enable_web",
        "default_enable_mobile",
        "default_enable_email",
        "is_lock",
        "is_important",
    )
