from configurations import Configuration, values

from wbcore.configurations import configurations
from wbcore.contrib.agenda.configurations import AgendaConfigurationMixin
from wbcore.contrib.authentication.configurations import (
    AuthenticationConfigurationMixin,
)
from wbcore.contrib.directory.configurations import DirectoryConfigurationMixin
from wbcore.contrib.io.configurations import ImportExportBaseConfiguration
from wbcore.contrib.notifications.configurations import NotificationConfiguration
from wbcore.contrib.permission.configurations import PermissionConfiguration


class DevBaseConfiguration(
    AgendaConfigurationMixin,
    AuthenticationConfigurationMixin,
    ImportExportBaseConfiguration,
    DirectoryConfigurationMixin,
    NotificationConfiguration,
    configurations.Base,
    configurations.DevApps,
    configurations.S3Media,
    configurations.Network,
    configurations.Restframework,
    configurations.ConsoleEmail,
    configurations.Templates,
    configurations.Authentication,
    configurations.DevMiddleware,
    configurations.LocalStaticfiles,
    PermissionConfiguration,
    configurations.WBCore,
    configurations.Celery,
    configurations.I18NL10N,
    configurations.Maintenance,
    configurations.Cache,
    Configuration,
):
    DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
    DEV_USER = values.Value(None, environ_prefix=None)
    ADD_REVERSION_ADMIN = True


class ProductionBaseConfiguration(
    configurations.Uvicorn, configurations.SSLNetwork, configurations.S3Staticfiles, DevBaseConfiguration
):
    pass
