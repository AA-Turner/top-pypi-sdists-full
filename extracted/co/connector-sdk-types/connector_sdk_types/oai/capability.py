import typing as t

from pydantic import BaseModel

BaseModelType = t.TypeVar("BaseModelType", bound=BaseModel)


class Request(t.Protocol):
    """
    A generic request to any capability.

    Useful as a type for calling request helpers on, e.g. get_token_auth, get_settings.

    Will match all AuthenticatedRequest capability inputs.
    """

    auth: t.Any
    """
    The connector_sdk_types.generated.AuthCredential attached to this request.
    """

    credentials: t.Any

    request: t.Any
    """
    The payload of this request. The type depends on the request type.
    """

    page: t.Any
    """
    Page data. May be None
    """

    include_raw_data: bool | None = None

    settings: t.Any
    """
    User-configured settings for the integration.
    """


class AuthRequest(t.Protocol):
    """
    A request being used as part of an authentication flow.

    These requests must have settings, but they don't have credentials.
    """

    request: t.Any
    """
    The payload of this request
    """

    page: t.Any
    """
    Page data. May be None
    """

    include_raw_data: bool | None = None

    settings: t.Any
    """
    User-configured settings for the integration.
    """
