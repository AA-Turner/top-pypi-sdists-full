from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .template_runtime import TemplateRuntime
from .template_variable import TemplateVariable


class TemplateFunction(AppwriteModel):
    """
    Template Function

    Attributes
    ----------
    icon : str
        Function Template Icon.
    id : str
        Function Template ID.
    name : str
        Function Template Name.
    tagline : str
        Function Template Tagline.
    permissions : List[Any]
        Execution permissions.
    events : List[Any]
        Function trigger events.
    cron : str
        Function execution schedult in CRON format.
    timeout : float
        Function execution timeout in seconds.
    usecases : List[Any]
        Function use cases.
    runtimes : List[TemplateRuntime]
        List of runtimes that can be used with this template.
    instructions : str
        Function Template Instructions.
    vcsprovider : str
        VCS (Version Control System) Provider.
    providerrepositoryid : str
        VCS (Version Control System) Repository ID
    providerowner : str
        VCS (Version Control System) Owner.
    providerversion : str
        VCS (Version Control System) branch version (tag).
    variables : List[TemplateVariable]
        Function variables.
    scopes : List[Any]
        Function scopes.
    """

    icon: str = Field(..., alias='icon')
    id: str = Field(..., alias='id')
    name: str = Field(..., alias='name')
    tagline: str = Field(..., alias='tagline')
    permissions: List[Any] = Field(..., alias='permissions')
    events: List[Any] = Field(..., alias='events')
    cron: str = Field(..., alias='cron')
    timeout: float = Field(..., alias='timeout')
    usecases: List[Any] = Field(..., alias='useCases')
    runtimes: List[TemplateRuntime] = Field(..., alias='runtimes')
    instructions: str = Field(..., alias='instructions')
    vcsprovider: str = Field(..., alias='vcsProvider')
    providerrepositoryid: str = Field(..., alias='providerRepositoryId')
    providerowner: str = Field(..., alias='providerOwner')
    providerversion: str = Field(..., alias='providerVersion')
    variables: List[TemplateVariable] = Field(..., alias='variables')
    scopes: List[Any] = Field(..., alias='scopes')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'icon' not in data:
            data['icon'] = ''
        if 'id' not in data:
            data['id'] = ''
        if 'name' not in data:
            data['name'] = ''
        if 'tagline' not in data:
            data['tagline'] = ''
        if 'permissions' not in data:
            data['permissions'] = []
        if 'events' not in data:
            data['events'] = []
        if 'cron' not in data:
            data['cron'] = ''
        if 'timeout' not in data:
            data['timeout'] = 15
        if 'useCases' not in data and 'usecases' not in data:
            data['useCases'] = []
        if 'runtimes' not in data:
            data['runtimes'] = []
        if 'instructions' not in data:
            data['instructions'] = ''
        if 'vcsProvider' not in data and 'vcsprovider' not in data:
            data['vcsProvider'] = ''
        if 'providerRepositoryId' not in data and 'providerrepositoryid' not in data:
            data['providerRepositoryId'] = ''
        if 'providerOwner' not in data and 'providerowner' not in data:
            data['providerOwner'] = ''
        if 'providerVersion' not in data and 'providerversion' not in data:
            data['providerVersion'] = ''
        if 'variables' not in data:
            data['variables'] = []
        if 'scopes' not in data:
            data['scopes'] = []
        return data
