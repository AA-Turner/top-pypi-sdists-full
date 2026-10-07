import datetime
import typing

import kubernetes.client

class V1alpha1EvictionPodReference:
    name: str
    uid: str
    
    def __init__(self, *, name: str, uid: str) -> None:
        ...
    def to_dict(self) -> V1alpha1EvictionPodReferenceDict:
        ...
class V1alpha1EvictionPodReferenceDict(typing.TypedDict, total=False):
    name: str
    uid: str
