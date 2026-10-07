import datetime
import typing

import kubernetes.client

class V1alpha1EvictionSpec:
    target: kubernetes.client.V1alpha1EvictionTarget
    
    def __init__(self, *, target: kubernetes.client.V1alpha1EvictionTarget) -> None:
        ...
    def to_dict(self) -> V1alpha1EvictionSpecDict:
        ...
class V1alpha1EvictionSpecDict(typing.TypedDict, total=False):
    target: kubernetes.client.V1alpha1EvictionTargetDict
