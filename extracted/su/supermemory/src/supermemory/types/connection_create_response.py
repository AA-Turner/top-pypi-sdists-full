# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ConnectionCreateResponse"]


class ConnectionCreateResponse(BaseModel):
    id: str

    auth_link: Optional[str] = FieldInfo(alias="authLink", default=None)

    expires_in: Optional[str] = FieldInfo(alias="expiresIn", default=None)

    redirects_to: Optional[str] = FieldInfo(alias="redirectsTo", default=None)
