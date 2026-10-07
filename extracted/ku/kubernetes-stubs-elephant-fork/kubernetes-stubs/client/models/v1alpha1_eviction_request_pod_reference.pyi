import datetime
import typing

import kubernetes.client

class V1alpha1EvictionRequestPodReference:
    name: str
    uid: str
    
    def __init__(self, *, name: str, uid: str) -> None:
        ...
    def to_dict(self) -> V1alpha1EvictionRequestPodReferenceDict:
        ...
class V1alpha1EvictionRequestPodReferenceDict(typing.TypedDict, total=False):
    name: str
    uid: str
