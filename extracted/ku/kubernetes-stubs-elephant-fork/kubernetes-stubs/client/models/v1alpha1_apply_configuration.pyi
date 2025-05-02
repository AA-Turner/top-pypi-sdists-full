import datetime
import typing

import kubernetes.client

class V1alpha1ApplyConfiguration:
    expression: typing.Optional[str]
    
    def __init__(self, *, expression: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1ApplyConfigurationDict:
        ...
class V1alpha1ApplyConfigurationDict(typing.TypedDict, total=False):
    expression: typing.Optional[str]
