# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["ApplicationAgentGraphEdge"]


class ApplicationAgentGraphEdge(BaseModel):
    from_node: str

    to_node: str
