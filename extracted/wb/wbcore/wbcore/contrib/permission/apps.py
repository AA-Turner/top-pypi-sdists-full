from django.apps import AppConfig
from django.db.models.signals import post_migrate


class PermissionAppConfig(AppConfig):
    name = "wbcore.contrib.permission"
    label = "wbcore_permission"

    def ready(self):
        from wbcore.contrib.permission.management import refresh_internal_users

        post_migrate.connect(
            refresh_internal_users,
            dispatch_uid="permission.refresh_internal_users",
        )
