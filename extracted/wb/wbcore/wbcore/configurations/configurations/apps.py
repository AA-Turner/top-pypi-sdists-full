class Apps:
    _BASE_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "rest_framework",
        "django_filters",
        "dynamic_preferences",
        "dynamic_preferences.users.apps.UserPreferencesConfig",
        "django_extensions",
        "corsheaders",
        "reversion",
        "reversion_compare",
        "guardian",
        "ordered_model",
        "wbcore",
        "wbcore.contrib.agenda",
        "wbcore.contrib.directory",
        "wbcore.contrib.authentication",
        "wbcore.contrib.content_type",
        "wbcore.contrib.notifications",
        "wbcore.contrib.io",
        "wbcore.contrib.currency",
        "wbcore.contrib.geography",
        "wbcore.contrib.tags",
        "wbcore.contrib.documents",
        "wbcore.contrib.workflow",
        "wbcore.contrib.color",
        "wbcore.contrib.guardian",
        "django_celery_beat",
        "modeltrans",
        "maintenance_mode",
    ]

    def _get_additional_and_wb_apps(self):
        return getattr(self, "ADDITIONAL_APPS", []) + getattr(self, "WB_ENDPOINTS", [])

    @property
    def INSTALLED_APPS(self):  # noqa
        return self._BASE_APPS + self._get_additional_and_wb_apps()


class DevApps(Apps):
    @property
    def INSTALLED_APPS(self):  # noqa
        apps = self._BASE_APPS

        if self.DEBUG:
            apps.append("debug_toolbar")

        apps.extend(self._get_additional_and_wb_apps())
        return apps
