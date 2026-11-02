from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .console_key_scope import ConsoleKeyScope


class ConsoleKeyScopeList(AppwriteModel):
    """
    Console Key Scopes List

    Attributes
    ----------
    total : float
        Total number of key scopes exposed by the server.
    scopes : List[ConsoleKeyScope]
        List of key scopes, each with its ID and description.
    """

    total: float = Field(..., alias='total')
    scopes: List[ConsoleKeyScope] = Field(..., alias='scopes')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'scopes' not in data:
            data['scopes'] = []
        return data
