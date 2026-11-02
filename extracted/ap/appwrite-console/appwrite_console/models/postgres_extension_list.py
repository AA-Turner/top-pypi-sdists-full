from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .postgres_extension import PostgresExtension


class PostgresExtensionList(AppwriteModel):
    """
    Postgres extensions list

    Attributes
    ----------
    total : float
        Total number of extensions that matched your query.
    extensions : List[PostgresExtension]
        List of extensions.
    """

    total: float = Field(..., alias='total')
    extensions: List[PostgresExtension] = Field(..., alias='extensions')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'extensions' not in data:
            data['extensions'] = []
        return data
