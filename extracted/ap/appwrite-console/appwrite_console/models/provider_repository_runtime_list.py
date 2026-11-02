from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .provider_repository_runtime import ProviderRepositoryRuntime


class ProviderRepositoryRuntimeList(AppwriteModel):
    """
    Runtime Provider Repositories List

    Attributes
    ----------
    total : float
        Total number of runtimeProviderRepositories that matched your query.
    runtimeproviderrepositories : List[ProviderRepositoryRuntime]
        List of runtimeProviderRepositories.
    type : str
        Provider repository list type.
    """

    total: float = Field(..., alias='total')
    runtimeproviderrepositories: List[ProviderRepositoryRuntime] = Field(..., alias='runtimeProviderRepositories')
    type: str = Field(..., alias='type')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'runtimeProviderRepositories' not in data and 'runtimeproviderrepositories' not in data:
            data['runtimeProviderRepositories'] = []
        if 'type' not in data:
            data['type'] = 'runtime'
        return data
