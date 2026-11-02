from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from ..enums.detection_runtime_type import DetectionRuntimeType
from .detection_variable import DetectionVariable


class DetectionRuntime(AppwriteModel):
    """
    DetectionRuntime

    Attributes
    ----------
    type : DetectionRuntimeType
        Repository detection type.
    variables : Optional[List[DetectionVariable]]
        Environment variables found in .env files
    runtime : str
        Runtime
    entrypoint : str
        Function Entrypoint
    commands : str
        Function install and build commands
    """

    type: DetectionRuntimeType = Field(..., alias='type')
    variables: Optional[List[DetectionVariable]] = Field(default=None, alias='variables')
    runtime: str = Field(..., alias='runtime')
    entrypoint: str = Field(..., alias='entrypoint')
    commands: str = Field(..., alias='commands')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'type' not in data:
            data['type'] = 'runtime'
        if 'runtime' not in data:
            data['runtime'] = ''
        if 'entrypoint' not in data:
            data['entrypoint'] = ''
        if 'commands' not in data:
            data['commands'] = ''
        return data
