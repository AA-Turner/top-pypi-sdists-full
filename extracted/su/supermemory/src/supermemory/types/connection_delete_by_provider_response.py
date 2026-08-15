# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = ["ConnectionDeleteByProviderResponse", "ConnectionDeleteByProviderResponseItem"]


class ConnectionDeleteByProviderResponseItem(BaseModel):
    id: str

    provider: str


ConnectionDeleteByProviderResponse: TypeAlias = List[ConnectionDeleteByProviderResponseItem]
