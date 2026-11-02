from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .template_framework import TemplateFramework
from .template_variable import TemplateVariable


class TemplateSite(AppwriteModel):
    """
    Template Site

    Attributes
    ----------
    key : str
        Site Template ID.
    name : str
        Site Template Name.
    tagline : str
        Short description of template
    demourl : Optional[str]
        URL hosting a template demo.
    screenshotdark : str
        File URL with preview screenshot in dark theme preference.
    screenshotlight : str
        File URL with preview screenshot in light theme preference.
    usecases : List[Any]
        Site use cases.
    frameworks : List[TemplateFramework]
        List of frameworks that can be used with this template.
    vcsprovider : str
        VCS (Version Control System) Provider.
    providerrepositoryid : str
        VCS (Version Control System) Repository ID
    providerowner : str
        VCS (Version Control System) Owner.
    providerversion : str
        VCS (Version Control System) branch version (tag).
    variables : List[TemplateVariable]
        Site variables.
    """

    key: str = Field(..., alias='key')
    name: str = Field(..., alias='name')
    tagline: str = Field(..., alias='tagline')
    demourl: Optional[str] = Field(default=None, alias='demoUrl')
    screenshotdark: str = Field(..., alias='screenshotDark')
    screenshotlight: str = Field(..., alias='screenshotLight')
    usecases: List[Any] = Field(..., alias='useCases')
    frameworks: List[TemplateFramework] = Field(..., alias='frameworks')
    vcsprovider: str = Field(..., alias='vcsProvider')
    providerrepositoryid: str = Field(..., alias='providerRepositoryId')
    providerowner: str = Field(..., alias='providerOwner')
    providerversion: str = Field(..., alias='providerVersion')
    variables: List[TemplateVariable] = Field(..., alias='variables')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'key' not in data:
            data['key'] = ''
        if 'name' not in data:
            data['name'] = ''
        if 'tagline' not in data:
            data['tagline'] = ''
        if 'screenshotDark' not in data and 'screenshotdark' not in data:
            data['screenshotDark'] = ''
        if 'screenshotLight' not in data and 'screenshotlight' not in data:
            data['screenshotLight'] = ''
        if 'useCases' not in data and 'usecases' not in data:
            data['useCases'] = []
        if 'frameworks' not in data:
            data['frameworks'] = []
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
        return data
