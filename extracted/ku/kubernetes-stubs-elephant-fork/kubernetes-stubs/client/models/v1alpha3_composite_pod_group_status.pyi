import datetime
import typing

import kubernetes.client

class V1alpha3CompositePodGroupStatus:
    conditions: typing.Optional[list[kubernetes.client.V1Condition]]
    
    def __init__(self, *, conditions: typing.Optional[list[kubernetes.client.V1Condition]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3CompositePodGroupStatusDict:
        ...
class V1alpha3CompositePodGroupStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[list[kubernetes.client.V1ConditionDict]]
