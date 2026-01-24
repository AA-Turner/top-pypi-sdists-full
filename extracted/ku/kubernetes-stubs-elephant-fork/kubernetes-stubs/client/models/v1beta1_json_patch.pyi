import datetime
import typing

import kubernetes.client

class V1beta1JSONPatch:
    expression: typing.Optional[str]
    
    def __init__(self, *, expression: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1JSONPatchDict:
        ...
class V1beta1JSONPatchDict(typing.TypedDict, total=False):
    expression: typing.Optional[str]
