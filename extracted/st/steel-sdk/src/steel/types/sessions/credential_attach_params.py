# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, Annotated, TypeAlias, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo

__all__ = ["CredentialAttachParams", "Binding", "BindingUnionMember1"]


class CredentialAttachParams(TypedDict, total=False):
    bindings: SequenceNotStr[Binding]
    """At most 100 bindings; KV bindings may specify allowedOrigins."""

    credential_ids: Annotated[SequenceNotStr[str], PropertyInfo(alias="credentialIds")]
    """Ids of credentials (Secrets of kind `credential`) in the session's project.

    Binding makes the session's lookup `explicit` for good.
    """


class BindingUnionMember1(TypedDict, total=False):
    allowed_origins: Required[Annotated[SequenceNotStr[str], PropertyInfo(alias="allowedOrigins")]]

    reference: Required[str]


Binding: TypeAlias = Union[str, BindingUnionMember1]
