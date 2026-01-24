import os
from datetime import timedelta
from typing import Dict

from configurations import values
from django.conf import settings
from rest_framework.request import Request
from rest_framework.reverse import reverse


class AuthenticationConfigurationMixin:
    WBCORE_DEFAULT_USER_NAME = "wbcore.contrib.authentication.configurations.get_user_name"
    WBCORE_DEFAULT_AUTH_CONFIG = "wbcore.contrib.authentication.configurations.auth_method"
    AUTH_USER_MODEL = "authentication.User"
    DEFAULT_FROM_EMAIL = values.Value("no-reply@stainly-bench.com", environ_prefix=None)


def resolve_profile(request: Request) -> Dict:
    """Returns two endpoints, one for the profile image and one for the profile widget"""

    return {
        "image": "https://image.freepik.com/free-vector/businessman-profile-cartoon_18591-58479.jpg",
        "endpoint": reverse("wbcore:authentication:userprofile-detail", args=[request.user.id], request=request),
    }


def auth_method(request):
    from wbcore.contrib.authentication.authentication import get_dev_user_from_settings

    access = settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME", timedelta(minutes=5))
    refresh = settings.SIMPLE_JWT.get("REFRESH_TOKEN_LIFETIME", timedelta(days=1))

    config = {
        "type": "JWT",
        "config": {
            "token": reverse("wbcore:authentication:token_obtain_pair", request=request),
            "refresh": reverse("wbcore:authentication:token_refresh", request=request),
            "verify": reverse("wbcore:authentication:token_verify", request=request),
            "token_lifetime": {"access": access, "refresh": refresh},
            "username_field_key": "email",
            "username_field_label": "E-Mail",
            "cookie_key": settings.JWT_COOKIE_KEY,
        },
    }
    if users := get_dev_user_from_settings("email"):
        config["dev_users"] = users

    if "WB_SHOW_RESET_PASSWORD" in os.environ:
        config["config"]["reset_password"] = {
            "endpoint": reverse("wbcore:authentication:reset_password_email", request=request),
            "key": "email",
            "success_message": "An e-mail has been sent to your address with instructions to reset your password.",
        }

    return config


def get_user_name(user):
    return f"{user.profile.first_name} {user.profile.last_name}"
