import datetime
import typing

import kubernetes.client

class V1alpha1EvictionRequestTarget:
    pod: typing.Optional[kubernetes.client.V1alpha1EvictionRequestPodReference]
    
    def __init__(self, *, pod: typing.Optional[kubernetes.client.V1alpha1EvictionRequestPodReference] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1EvictionRequestTargetDict:
        ...
class V1alpha1EvictionRequestTargetDict(typing.TypedDict, total=False):
    pod: typing.Optional[kubernetes.client.V1alpha1EvictionRequestPodReferenceDict]
