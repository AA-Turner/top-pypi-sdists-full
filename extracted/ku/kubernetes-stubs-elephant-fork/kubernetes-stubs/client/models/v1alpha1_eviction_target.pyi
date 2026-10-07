import datetime
import typing

import kubernetes.client

class V1alpha1EvictionTarget:
    pod: typing.Optional[kubernetes.client.V1alpha1EvictionPodReference]
    
    def __init__(self, *, pod: typing.Optional[kubernetes.client.V1alpha1EvictionPodReference] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1EvictionTargetDict:
        ...
class V1alpha1EvictionTargetDict(typing.TypedDict, total=False):
    pod: typing.Optional[kubernetes.client.V1alpha1EvictionPodReferenceDict]
