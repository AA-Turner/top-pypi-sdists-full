from django.utils.translation import gettext_lazy as _

from wbcore.menus import ItemPermission, MenuItem

NotificationTypeMenuItem = MenuItem(
    label=_("Notification Types"),
    endpoint="wbcore:notifications:notification_type_setting-list",
    permission=ItemPermission(permissions=["notifications.view_notificationtype"]),
)

NotificationMenuItem = MenuItem(
    label=_("Notifications"),
    endpoint="wbcore:notifications:notification-list",
    permission=ItemPermission(permissions=["notifications.view_notification"]),
)
