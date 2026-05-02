# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["ApplicationSchemaRetrieveParams"]


class ApplicationSchemaRetrieveParams(TypedDict, total=False):
    version: Required[Literal["OFFLINE", "V0", "AGENTS_SERVICE"]]
    """
    An enum representing the version states of an application and its nodes'
    schemas. Attributes: V0: The initial version of an application schema.
    AGENTS_SERVICE: Application schema references egp_services definition. OFFLINE:
    Application schema for applications that do not run on SGP directly.
    """
