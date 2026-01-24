from configurations import values
from django.conf import settings


class Maintenance:
    MAINTENANCE_MODE_STR: str | None = values.Value("False", environ_prefix=None)

    # We allow maintenance mode to be either True, False or None. In case of None, the specified Backend will take over.
    def MAINTENANCE_MODE(self) -> bool | None:  # noqa
        if value := self.MAINTENANCE_MODE_STR:
            normalized_value = value.strip().lower()
            if normalized_value in values.BooleanValue.true_values:
                return True
            elif normalized_value in values.BooleanValue.false_values:
                return False
        return None

    MAINTENANCE_MODE_STATE_BACKEND = values.Value(
        "maintenance_mode.backends.StaticStorageBackend", environ_prefix=None
    )
    MAINTENANCE_MODE_STATE_BACKEND_FALLBACK_VALUE = False
    MAINTENANCE_MODE_STATE_FILE_NAME = values.Value("maintenance_mode_state.txt", environ_prefix=None)

    MAINTENANCE_MODE_IGNORE_ADMIN_SITE = values.BooleanValue(True, environ_prefix=None)
    MAINTENANCE_MODE_IGNORE_ANONYMOUS_USER = False
    MAINTENANCE_MODE_IGNORE_AUTHENTICATED_USER = False
    MAINTENANCE_MODE_IGNORE_STAFF = values.BooleanValue(False, environ_prefix=None)
    MAINTENANCE_MODE_IGNORE_SUPERUSER = values.BooleanValue(True, environ_prefix=None)
    MAINTENANCE_MODE_IGNORE_IP_ADDRESSES = values.ListValue([], environ_prefix=None)

    MAINTENANCE_MODE_GET_CONTEXT = None
    MAINTENANCE_MODE_IGNORE_URLS = values.ListValue([], environ_prefix=None)

    MAINTENANCE_MODE_LOGOUT_AUTHENTICATED_USER = False
    MAINTENANCE_MODE_REDIRECT_URL = values.Value(None, environ_prefix=None)
    MAINTENANCE_MODE_RESPONSE_TYPE = values.Value("html", environ_prefix=None)
    MAINTENANCE_MODE_TEMPLATE = values.Value("errors/503.html", environ_prefix=None)

    MAINTENANCE_MODE_STATUS_CODE = values.IntegerValue(503, environ_prefix=None)
    MAINTENANCE_MODE_RETRY_AFTER = values.IntegerValue(3600, environ_prefix=None)  # 1 hour

    MAINTENANCE_MODE_IGNORE_TESTS = False
    MAINTENANCE_MODE_GET_CONTEXT = "wbcore.configurations.configurations.maintenance.get_context"

    MAINTENANCE_MODE_HEADER = values.Value("We're doing some maintenance", environ_prefix=None)
    MAINTENANCE_MODE_DESCRIPTION = values.Value(
        "Our site is currently undergoing scheduled maintenance and upgrades, but will return shortly. Thank for your patience",
        environ_prefix=None,
    )


def get_context(request=None):
    return {"header": settings.MAINTENANCE_MODE_HEADER, "description": settings.MAINTENANCE_MODE_DESCRIPTION}
