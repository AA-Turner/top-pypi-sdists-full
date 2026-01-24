import os

from configurations import values


class Base:
    DEBUG = values.BooleanValue(True, environ_prefix=None)
    SECRET_KEY = values.Value("THIS-IS-NOT-A-SECRET-KEY", environ_prefix=None)
    SITE_ID = values.IntegerValue(1, environ_prefix=None)

    @property
    def PROJECT_NAME(self):  # noqa
        if settings_module := os.environ.get("DJANGO_SETTINGS_MODULE", None):
            return settings_module.split(".")[0]
        return None
