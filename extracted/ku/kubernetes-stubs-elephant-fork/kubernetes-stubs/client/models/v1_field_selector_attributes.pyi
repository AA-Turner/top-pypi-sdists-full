import datetime
import typing

import kubernetes.client

class V1FieldSelectorAttributes:
    raw_selector: typing.Optional[str]
    requirements: typing.Optional[list[kubernetes.client.V1FieldSelectorRequirement]]
    
    def __init__(self, *, raw_selector: typing.Optional[str] = ..., requirements: typing.Optional[list[kubernetes.client.V1FieldSelectorRequirement]] = ...) -> None:
        ...
    def to_dict(self) -> V1FieldSelectorAttributesDict:
        ...
class V1FieldSelectorAttributesDict(typing.TypedDict, total=False):
    rawSelector: typing.Optional[str]
    requirements: typing.Optional[list[kubernetes.client.V1FieldSelectorRequirementDict]]
