import datetime
import typing

import kubernetes.client

class V1alpha1GroupVersionResource:
    group: typing.Optional[str]
    resource: typing.Optional[str]
    version: typing.Optional[str]
    
    def __init__(self, *, group: typing.Optional[str] = ..., resource: typing.Optional[str] = ..., version: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1GroupVersionResourceDict:
        ...
class V1alpha1GroupVersionResourceDict(typing.TypedDict, total=False):
    group: typing.Optional[str]
    resource: typing.Optional[str]
    version: typing.Optional[str]
