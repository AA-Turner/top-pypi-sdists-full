# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["ApplicationEdge"]


class ApplicationEdge(BaseModel):
    from_field: str

    from_node: str

    to_field: str

    to_node: str
