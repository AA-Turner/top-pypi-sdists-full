from configurations import values
from corsheaders.defaults import default_headers


class Network:
    ALLOWED_HOSTS = values.ListValue(["*"], environ_prefix=None)
    CORS_ALLOW_ALL_ORIGINS = values.BooleanValue(True, environ_prefix=None)
    CORS_ALLOWED_ORIGINS = values.ListValue([], environ_prefix=None)
    CORS_ALLOW_HEADERS = list(default_headers) + ["WB-DISPLAY-IDENTIFIER"]
    DATA_UPLOAD_MAX_MEMORY_SIZE = values.IntegerValue(2621440, environ_prefix=None)
    DATA_UPLOAD_MAX_NUMBER_FIELDS = values.IntegerValue(1000, environ_prefix=None)
    DATA_UPLOAD_MAX_NUMBER_FILES = values.IntegerValue(100, environ_prefix=None)


class SSLNetwork(Network):
    SECURE_SSL_REDIRECT = values.BooleanValue(True, environ_prefix=None)
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = values.BooleanValue(True, environ_prefix=None)
    CSRF_COOKIE_SECURE = values.BooleanValue(True, environ_prefix=None)
