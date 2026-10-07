import datetime
import typing

import kubernetes.client

class V1alpha1EvictionRequestSpec:
    intent: str
    requester: str
    target: kubernetes.client.V1alpha1EvictionRequestTarget
    
    def __init__(self, *, intent: str, requester: str, target: kubernetes.client.V1alpha1EvictionRequestTarget) -> None:
        ...
    def to_dict(self) -> V1alpha1EvictionRequestSpecDict:
        ...
class V1alpha1EvictionRequestSpecDict(typing.TypedDict, total=False):
    intent: str
    requester: str
    target: kubernetes.client.V1alpha1EvictionRequestTargetDict
