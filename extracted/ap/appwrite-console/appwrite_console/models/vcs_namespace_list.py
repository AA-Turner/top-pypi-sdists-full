from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .vcs_namespace import VcsNamespace


class VcsNamespaceList(AppwriteModel):
    """
    VCS Namespaces List

    Attributes
    ----------
    total : float
        Total number of namespaces that matched your query.
    namespaces : List[VcsNamespace]
        List of namespaces.
    """

    total: float = Field(..., alias='total')
    namespaces: List[VcsNamespace] = Field(..., alias='namespaces')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'namespaces' not in data:
            data['namespaces'] = []
        return data
