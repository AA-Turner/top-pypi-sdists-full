from datetime import timedelta

from configurations import values


class Authentication:
    AUTHENTICATION_BACKENDS = (
        "django.contrib.auth.backends.ModelBackend",  # this is default
        "guardian.backends.ObjectPermissionBackend",
    )

    AUTH_PASSWORD_VALIDATORS = [
        {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

    JWT_AUTH = {"JWT_AUTH_COOKIE": "JWT"}
    JWT_ACCESS_TOKEN_LIFETIME = values.FloatValue(5 * 60, environ_prefix=None)  # in seconds
    JWT_REFRESH_TOKEN_LIFETIME = values.FloatValue(24 * 60 * 60, environ_prefix=None)  # in seconds
    JWT_SLIDING_TOKEN_LIFETIME = values.FloatValue(5 * 60, environ_prefix=None)  # in seconds
    JWT_SLIDING_TOKEN_REFRESH_LIFETIME = values.FloatValue(24 * 60 * 60, environ_prefix=None)  # in seconds
    JWT_COOKIE_KEY = values.Value("JWT-access", environ_prefix=None)

    @property
    def SIMPLE_JWT(self):  # noqa
        return {
            "ACCESS_TOKEN_LIFETIME": timedelta(seconds=self.JWT_ACCESS_TOKEN_LIFETIME),
            "REFRESH_TOKEN_LIFETIME": timedelta(seconds=self.JWT_REFRESH_TOKEN_LIFETIME),
            "ALGORITHM": "HS256",
            "SIGNING_KEY": self.SECRET_KEY,
            "ROTATE_REFRESH_TOKENS": False,
            "BLACKLIST_AFTER_ROTATION": True,
            "VERIFYING_KEY": None,
            "AUTH_HEADER_TYPES": ("Bearer",),
            "USER_ID_FIELD": "id",
            "USER_ID_CLAIM": "user_id",
            "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
            "TOKEN_TYPE_CLAIM": "token_type",
            "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
            "SLIDING_TOKEN_LIFETIME": timedelta(seconds=self.JWT_SLIDING_TOKEN_LIFETIME),
            "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(seconds=self.JWT_SLIDING_TOKEN_REFRESH_LIFETIME),
        }
