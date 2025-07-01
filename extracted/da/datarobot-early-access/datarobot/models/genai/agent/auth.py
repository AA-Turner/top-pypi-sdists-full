#
# Copyright 2023-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from contextvars import ContextVar
from enum import Enum
from functools import wraps
import inspect
from typing import Any, Callable, Dict, Optional, TypeVar

from typing_extensions import ParamSpec

from datarobot.auth.datarobot.oauth import SyncOAuth as DataRobotOAuthClient
from datarobot.auth.identity import Identity
from datarobot.auth.session import AuthCtx

authorization_context_var: ContextVar[Dict[str, Any]] = ContextVar("authorization_context")


def set_authorization_context(authorization_context: Dict[str, Any]) -> None:
    authorization_context_var.set(authorization_context)


def get_authorization_context() -> Dict[str, Any]:
    return authorization_context_var.get()


class ToolAuth(Enum):
    OBO = "on-behalf-of"

    def __str__(self) -> str:
        return f"{self.name} ({self.value})"


P = ParamSpec("P")
T = TypeVar("T")


def is_injection_possible(func: Callable[..., Any], parameter_name: str) -> bool:
    """Check if a parameter can be injected into the function."""
    sig = inspect.signature(func)
    parameters = sig.parameters
    return parameter_name in parameters or inspect.Parameter.VAR_KEYWORD in parameters.values()


def datarobot_tool_auth(
    func: Optional[Callable[..., Any]] = None,
    *,
    type: ToolAuth = ToolAuth.OBO,
    provider: Optional[str] = None,
) -> Callable[..., Any]:
    """
    Decorator to generate and inject OAuth access token into the function.

    Parameters
    ----------
    func : Callable, optional
        The function to wrap
    type : ToolAuth, default=ToolAuth.OBO
        The type of authorization e.g., OBO (on-behalf-of).
    provider : str, optional
        The name of the OAuth provider.

    Returns
    -------
    Callable
        The decorated function with the injected token.
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            if not is_injection_possible(func, "token"):
                raise ValueError(
                    f"Token injection is not possible for function {func.__name__}. "
                    f"Ensure the function has a 'token' parameter or accepts `**kwargs`."
                )
            kwargs["token"] = OAuthAccessTokenProvider().get_token(type, provider)
            return func(*args, **kwargs)

        return wrapper

    # Make decorator work also without parenthesis
    if callable(func):
        return decorator(func)

    return decorator


class OAuthAccessTokenProvider:
    """
    Manages OAuth access tokens using DataRobot-based authentication.
    """

    def __init__(self, auth_ctx: Optional[AuthCtx[Any]] = None) -> None:
        self.auth_ctx = auth_ctx or AuthCtx(**get_authorization_context())

    def _get_identity(self, provider_type: Optional[str]) -> Identity:
        """Retrieve the appropriate identity from the authentication context."""
        if not provider_type:
            if len(self.auth_ctx.identities) > 1:
                raise ValueError(
                    "The 'provider' parameter is required when there are multiple identities. "
                    "Please specify the provider to select the appropriate identity."
                )
            return self.auth_ctx.identities[0]

        for identity in self.auth_ctx.identities:
            if identity.provider_type == provider_type:
                return identity

        raise ValueError(f"No identity found for provider '{provider_type}'.")

    def get_token(self, auth_type: ToolAuth, provider_type: Optional[str] = None) -> str:
        """Get OAuth access token using the specified method."""
        identity = self._get_identity(provider_type)
        oauth_client = DataRobotOAuthClient()

        supported_auth_types = ", ".join(str(t) for t in ToolAuth)

        if auth_type == ToolAuth.OBO:
            token_data = oauth_client.refresh_access_token(
                identity_id=identity.provider_identity_id
            )
            return token_data.access_token

        raise ValueError(
            f"Unsupported tool auth type: {auth_type}. Please "
            f"use one of supported ones: {supported_auth_types}"
        )
