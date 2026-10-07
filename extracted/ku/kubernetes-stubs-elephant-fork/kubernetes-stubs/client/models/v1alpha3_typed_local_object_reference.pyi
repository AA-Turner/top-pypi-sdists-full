import datetime
import typing

import kubernetes.client

class V1alpha3TypedLocalObjectReference:
    api_group: typing.Optional[str]
    kind: str
    name: str
    
    def __init__(self, *, api_group: typing.Optional[str] = ..., kind: str, name: str) -> None:
        ...
    def to_dict(self) -> V1alpha3TypedLocalObjectReferenceDict:
        ...
class V1alpha3TypedLocalObjectReferenceDict(typing.TypedDict, total=False):
    apiGroup: typing.Optional[str]
    kind: str
    name: str
