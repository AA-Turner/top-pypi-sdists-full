# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["SessionCredentials", "Binding", "BindingUnionMember1", "Credential"]


class BindingUnionMember1(BaseModel):
    allowed_origins: List[str] = FieldInfo(alias="allowedOrigins")

    reference: str


Binding: TypeAlias = Union[str, BindingUnionMember1]


class Credential(BaseModel):
    id: str
    """The credential's id (a Secret of kind `credential`)"""

    additional_origins: List[str] = FieldInfo(alias="additionalOrigins")
    """Other origins the credential may be filled on"""

    name: str
    """The credential's name"""

    namespace: str
    """The credential's namespace"""

    origin: str
    """The website origin the credential is for"""


class SessionCredentials(BaseModel):
    """The credentials a session is bound to"""

    bindings: List[Binding]
    """
    Bindings, including KV references with their allowed origins and soft-deleted
    targets.
    """

    credentials: List[Credential]
    """Live credentials bound to the session, oldest binding first. No values."""

    credentials_enabled: bool = FieldInfo(alias="credentialsEnabled")
    """Whether the session was created with a `credentials` configuration.

    Only then can credentials be attached; otherwise attach and replace answer 409
    `credentials_not_enabled`.
    """

    lookup: Literal["implicit", "explicit"]
    """`explicit`: the session fills only the credentials listed here.

    `implicit`: it fills credentials stored for its namespace and the page origin.
    """
