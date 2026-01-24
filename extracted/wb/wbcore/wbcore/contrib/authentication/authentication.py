import functools
from typing import TYPE_CHECKING

from django.conf import settings
from django.utils import timezone
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.authentication import TokenAuthentication as DRFTokenAuthentication
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings

from .models import Token

AUTH_HEADER_TYPES = api_settings.AUTH_HEADER_TYPES

if TYPE_CHECKING:
    from wbcore.contrib.authentication.models import User
else:
    from wbcore.contrib.authentication.models.users import User


class TokenAuthentication(DRFTokenAuthentication):
    """
    Short lived Token token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    model = Token

    # TODO: Find a way to improve typing in the next two methods, somehow pyright is not picking up self.model
    def authenticate_credentials(self, key) -> tuple[User, Token]:
        return super().authenticate_credentials(key)  # type: ignore

    def authenticate(self, request) -> tuple[User, Token] | None:
        authentication_res = super().authenticate(request)
        if authentication_res:
            authentication_res[1].check_validity_for_endpoint(request.resolver_match.view_name, timezone.now())  # type: ignore
        return authentication_res  # type: ignore


class QueryTokenAuthentication(TokenAuthentication):
    """
    Short lived Token token based authentication through query parameters.

    Clients should authenticate by passing the token key "token" as query parameters. For example:
        ?token=401f7ac837da42b97f613d789819ff93537bee6a
    Note, this is unsafe to use this authentication backend on unsecured connection
    """

    query_param_name = "token"

    # TODO: Find a way to improve typing in the next method, somehow pyright is not picking up self.model
    def authenticate(self, request) -> tuple[User, Token] | None:
        token = request.query_params.get(self.query_param_name)
        if not token:
            return None
        user, token = self.authenticate_credentials(token)
        token.check_validity_for_endpoint(request.resolver_match.view_name, timezone.now())
        return user, token  # type: ignore


class JWTCookieAuthentication(JWTAuthentication):
    def get_header(self, request: Request) -> bytes:
        if cookie_token := request.COOKIES.get(settings.JWT_COOKIE_KEY, None):
            return f"{AUTH_HEADER_TYPES[0]} {cookie_token}".encode(HTTP_HEADER_ENCODING)
        return super().get_header(request)


def inject_short_lived_token(view_name: str | None = None):
    """
    Decorator to wrap around additional resource function which return key value pair of resources and endpoint.
    The decorator will create for the user a short lived token only valid for the requested endpoint and inject it as query parameters

    The decorator expects a view_name (namespace:view_name) to be given otherwise, it will guess it from the resource endpoint (through the resolver)
    Args:
        view_name: Optional, view name to use instead of resolved the endpoint view name
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(serializer, instance, request, user, **kwargs):
            res = {}
            if view_name is None:
                return res
            for key, endpoint in func(serializer, instance, request, user, **kwargs).items():
                res[key] = Token.generate_shareable_link(endpoint, user, protected_view_name=view_name)
            return res

        return wrapper

    return decorator


def unauthenticated(request: "Request") -> dict[str, None]:
    return {"type": None}


def get_dev_user_from_settings(username_field_key: str) -> list[dict[str, str]]:
    if dev_user := getattr(settings, "DEV_USERS", []):
        users = list()
        for user in dev_user:
            username, password = user.split(":")
            users.append({username_field_key: username, "password": password})
        return users
    return []
