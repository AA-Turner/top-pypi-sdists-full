from configurations import values


class Restframework:
    REST_FRAMEWORK_ANON_THROTTLE_RATES = values.IntegerValue(60, environ_prefix=None)
    REST_FRAMEWORK_THROTTLE_PERIOD = values.Value("hour", environ_prefix=None)
    REST_FRAMEWORK_USER_THROTTLE_RATES = values.IntegerValue(5000, environ_prefix=None)

    def REST_FRAMEWORK(self):  # noqa
        rest_framework = {
            "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
            "PAGE_SIZE": 25,
            "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
            "DEFAULT_AUTHENTICATION_CLASSES": (
                "rest_framework_simplejwt.authentication.JWTAuthentication",
                "wbcore.contrib.authentication.authentication.TokenAuthentication",
            ),
            "DEFAULT_PERMISSION_CLASSES": (
                "rest_framework.permissions.IsAuthenticated",
                "wbcore.permissions.permissions.RestAPIModelPermissions",
            ),
            "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
            "DEFAULT_THROTTLE_CLASSES": [
                "rest_framework.throttling.AnonRateThrottle",
                "rest_framework.throttling.UserRateThrottle",
            ],
            "DEFAULT_THROTTLE_RATES": {
                "anon": f"{self.REST_FRAMEWORK_ANON_THROTTLE_RATES}/{self.REST_FRAMEWORK_THROTTLE_PERIOD}",
                "user": f"{self.REST_FRAMEWORK_USER_THROTTLE_RATES}/{self.REST_FRAMEWORK_THROTTLE_PERIOD}",
            },
            "COERCE_DECIMAL_TO_STRING": False,  # DRF default to True, we default to False to automatically cast decimal into float. Dev can decide to still not coerce decimal to string directly in the serializer
        }
        if self.DEBUG:
            rest_framework["DEFAULT_AUTHENTICATION_CLASSES"] = (
                "rest_framework_simplejwt.authentication.JWTAuthentication",
                "wbcore.contrib.authentication.authentication.TokenAuthentication",
                "rest_framework.authentication.SessionAuthentication",
            )
            rest_framework["DEFAULT_RENDERER_CLASSES"] = (
                "rest_framework.renderers.JSONRenderer",
                "wbcore.utils.renderers.BrowsableAPIRendererWithoutForms",
            )
        return rest_framework
