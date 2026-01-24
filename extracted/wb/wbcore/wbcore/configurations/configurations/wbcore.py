from configurations import values
from django.utils.translation import gettext_lazy as _
from markdown.extensions.tables import TableExtension

from wbcore.fsm.markdown_extensions import FSMExtension


class WBCore:
    CDN_BASE_ENDPOINT_URL = values.URLValue(
        "https://stainly-cdn.fra1.cdn.digitaloceanspaces.com/static", environ_prefix=None
    )

    FRONTEND_VERSION = values.Value("2.6.3", environ_prefix=None)
    FRONTEND_TEMPLATE = "wbcore/frontend.html"
    FRONTEND_MENU_CALENDAR = None

    BASE_ENDPOINT_URL = values.Value("", environ_prefix=None)

    BETA_BUTTON_VERSION = values.Value(None, environ_prefix=None)
    BETA_BUTTON_URL = values.URLValue(None, environ_prefix=None)
    BETA_BUTTON_TEXT = values.Value(_("Check out our upcoming beta version"), environ_prefix=None)

    WBCORE_MARKDOWN_TEMPLATE_TAGS = []
    WBCORE_MARKDOWN_EXTENSIONS = [
        TableExtension(),
        FSMExtension(),
    ]

    WBCORE_NOTIFICATION_TEMPLATE = values.Value("notifications/email_template.html", environ_prefix=None)
    WBCORE_NOTIFICATION_EMAIL_FROM = values.Value("no-reply@stainly-bench.com", environ_prefix=None)

    WBCORE_PLOTLY_CDN_URL = values.Value("https://cdn.plot.ly/plotly-latest.min.js", environ_prefix=None)
    WBCORE_EXTRA_CDN_URLS = values.ListValue([], environ_prefix=None)
    WBCORE_EXTRA_CSS_URLS = values.ListValue([], environ_prefix=None)
    WBCORE_PROFILE = values.Value("wbcore.contrib.authentication.configuration.resolve_profile", environ_prefix=None)
    WBCORE_DEFAULT_FRONTEND_USER_CONFIGURATION_ORDER = values.ListValue(["config__order"], environ_prefix=None)
    WBCORE_ADDITIONAL_DEFAULT_MODELVIEW_ATTRIBUTES = values.ListValue([], environ_prefix=None)
    WBCORE_NEW_NOTIFICATION_SYSTEM = values.BooleanValue(False, environ_prefix=None)

    DATA_UPLOAD_MAX_NUMBER_FIELDS = values.IntegerValue(2000, environ_prefix=None)
    WBCORE_IDLE_TIME = values.IntegerValue(30 * 60, environ_prefix=None)  # value in seconds
    WBCORE_IDLE_WARNING_TIME = values.IntegerValue(90, environ_prefix=None)  # value in seconds

    MESSAGE_STORAGE = "wbcore.messages.route_message_storage"

    @property
    def FRONTEND_CONTEXT(self):  # noqa
        base_url = f"{self.CDN_BASE_ENDPOINT_URL}/{self.FRONTEND_VERSION}/"
        return {
            "TITLE": "Workbench",
            "FONT_URL": "https://fonts.googleapis.com/css?family=Roboto:400,400i,500,500i,700,900&display=swap",
            "CDN_URLS": [self.WBCORE_PLOTLY_CDN_URL, *self.WBCORE_EXTRA_CDN_URLS],
            "CSS_URLS": self.WBCORE_EXTRA_CSS_URLS,
            "CONFIG_URL": "/wbcore/config/",
            "FAVICON_URL": f"{self.CDN_BASE_ENDPOINT_URL}/favicon.ico",
            "JS_URL": f"{base_url}main.js",
            "CSS_URL": f"{base_url}main.css",
            "JS_RUNTIME_URL": f"{base_url}runtime.js",
            "IDLE_TIME": self.WBCORE_IDLE_TIME * 1000,  # convert it into milliseconds
            "IDLE_WARNING_TIME": self.WBCORE_IDLE_WARNING_TIME * 1000,  # convert it into milliseconds
        }
