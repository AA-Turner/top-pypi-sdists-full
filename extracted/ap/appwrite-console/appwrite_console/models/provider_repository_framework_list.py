from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .provider_repository_framework import ProviderRepositoryFramework


class ProviderRepositoryFrameworkList(AppwriteModel):
    """
    Framework Provider Repositories List

    Attributes
    ----------
    total : float
        Total number of frameworkProviderRepositories that matched your query.
    frameworkproviderrepositories : List[ProviderRepositoryFramework]
        List of frameworkProviderRepositories.
    type : str
        Provider repository list type.
    """

    total: float = Field(..., alias='total')
    frameworkproviderrepositories: List[ProviderRepositoryFramework] = Field(..., alias='frameworkProviderRepositories')
    type: str = Field(..., alias='type')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'frameworkProviderRepositories' not in data and 'frameworkproviderrepositories' not in data:
            data['frameworkProviderRepositories'] = []
        if 'type' not in data:
            data['type'] = 'framework'
        return data
