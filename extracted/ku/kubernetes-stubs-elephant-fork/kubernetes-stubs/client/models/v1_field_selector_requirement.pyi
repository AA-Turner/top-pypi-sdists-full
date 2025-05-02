import datetime
import typing

import kubernetes.client

class V1FieldSelectorRequirement:
    key: str
    operator: str
    values: typing.Optional[list[str]]
    
    def __init__(self, *, key: str, operator: str, values: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1FieldSelectorRequirementDict:
        ...
class V1FieldSelectorRequirementDict(typing.TypedDict, total=False):
    key: str
    operator: str
    values: typing.Optional[list[str]]
