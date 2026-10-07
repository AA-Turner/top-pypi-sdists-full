import datetime
import typing

import kubernetes.client

class V1alpha1EvictionRequestStatus:
    conditions: typing.Optional[list[kubernetes.client.V1Condition]]
    observed_generation: typing.Optional[int]
    
    def __init__(self, *, conditions: typing.Optional[list[kubernetes.client.V1Condition]] = ..., observed_generation: typing.Optional[int] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1EvictionRequestStatusDict:
        ...
class V1alpha1EvictionRequestStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[list[kubernetes.client.V1ConditionDict]]
    observedGeneration: typing.Optional[int]
