from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class TemplateFramework(AppwriteModel):
    """
    Template Framework

    Attributes
    ----------
    key : str
        Parent framework key.
    name : str
        Framework Name.
    installcommand : str
        The install command used to install the dependencies.
    buildcommand : str
        The build command used to build the deployment.
    outputdirectory : str
        The output directory to store the build output.
    providerrootdirectory : str
        Path to site in VCS (Version Control System) repository
    buildruntime : str
        Runtime used during build step of template.
    adapter : str
        Site framework runtime
    fallbackfile : Optional[str]
        Fallback file for SPA. Only relevant for static serve runtime.
    """

    key: str = Field(..., alias='key')
    name: str = Field(..., alias='name')
    installcommand: str = Field(..., alias='installCommand')
    buildcommand: str = Field(..., alias='buildCommand')
    outputdirectory: str = Field(..., alias='outputDirectory')
    providerrootdirectory: str = Field(..., alias='providerRootDirectory')
    buildruntime: str = Field(..., alias='buildRuntime')
    adapter: str = Field(..., alias='adapter')
    fallbackfile: Optional[str] = Field(default=None, alias='fallbackFile')

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
        if 'installCommand' not in data and 'installcommand' not in data:
            data['installCommand'] = ''
        if 'buildCommand' not in data and 'buildcommand' not in data:
            data['buildCommand'] = ''
        if 'outputDirectory' not in data and 'outputdirectory' not in data:
            data['outputDirectory'] = ''
        if 'providerRootDirectory' not in data and 'providerrootdirectory' not in data:
            data['providerRootDirectory'] = ''
        if 'buildRuntime' not in data and 'buildruntime' not in data:
            data['buildRuntime'] = ''
        if 'adapter' not in data:
            data['adapter'] = ''
        return data
