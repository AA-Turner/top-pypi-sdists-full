from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from ..enums.detection_framework_type import DetectionFrameworkType
from .detection_variable import DetectionVariable


class DetectionFramework(AppwriteModel):
    """
    DetectionFramework

    Attributes
    ----------
    type : DetectionFrameworkType
        Repository detection type.
    variables : Optional[List[DetectionVariable]]
        Environment variables found in .env files
    framework : str
        Framework
    installcommand : str
        Site Install Command
    buildcommand : str
        Site Build Command
    outputdirectory : str
        Site Output Directory
    """

    type: DetectionFrameworkType = Field(..., alias='type')
    variables: Optional[List[DetectionVariable]] = Field(default=None, alias='variables')
    framework: str = Field(..., alias='framework')
    installcommand: str = Field(..., alias='installCommand')
    buildcommand: str = Field(..., alias='buildCommand')
    outputdirectory: str = Field(..., alias='outputDirectory')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'type' not in data:
            data['type'] = 'framework'
        if 'framework' not in data:
            data['framework'] = ''
        if 'installCommand' not in data and 'installcommand' not in data:
            data['installCommand'] = ''
        if 'buildCommand' not in data and 'buildcommand' not in data:
            data['buildCommand'] = ''
        if 'outputDirectory' not in data and 'outputdirectory' not in data:
            data['outputDirectory'] = ''
        return data
