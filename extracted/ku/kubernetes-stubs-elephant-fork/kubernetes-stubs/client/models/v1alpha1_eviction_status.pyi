import datetime
import typing

import kubernetes.client

class V1alpha1EvictionStatus:
    conditions: typing.Optional[list[kubernetes.client.V1Condition]]
    observed_generation: typing.Optional[int]
    requesters: typing.Optional[list[kubernetes.client.V1alpha1Requester]]
    responders: typing.Optional[list[kubernetes.client.V1alpha1ResponderStatus]]
    target_responders: typing.Optional[list[kubernetes.client.V1alpha1TargetResponder]]
    
    def __init__(self, *, conditions: typing.Optional[list[kubernetes.client.V1Condition]] = ..., observed_generation: typing.Optional[int] = ..., requesters: typing.Optional[list[kubernetes.client.V1alpha1Requester]] = ..., responders: typing.Optional[list[kubernetes.client.V1alpha1ResponderStatus]] = ..., target_responders: typing.Optional[list[kubernetes.client.V1alpha1TargetResponder]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1EvictionStatusDict:
        ...
class V1alpha1EvictionStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[list[kubernetes.client.V1ConditionDict]]
    observedGeneration: typing.Optional[int]
    requesters: typing.Optional[list[kubernetes.client.V1alpha1RequesterDict]]
    responders: typing.Optional[list[kubernetes.client.V1alpha1ResponderStatusDict]]
    targetResponders: typing.Optional[list[kubernetes.client.V1alpha1TargetResponderDict]]
