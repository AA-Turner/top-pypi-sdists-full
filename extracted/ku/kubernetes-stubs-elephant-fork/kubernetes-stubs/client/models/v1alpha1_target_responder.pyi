import datetime
import typing

import kubernetes.client

class V1alpha1TargetResponder:
    name: str
    priority: int
    state: str
    
    def __init__(self, *, name: str, priority: int, state: str) -> None:
        ...
    def to_dict(self) -> V1alpha1TargetResponderDict:
        ...
class V1alpha1TargetResponderDict(typing.TypedDict, total=False):
    name: str
    priority: int
    state: str
