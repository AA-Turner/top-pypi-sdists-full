import datetime
import typing

import kubernetes.client

class V1alpha1Requester:
    intent: str
    name: str
    
    def __init__(self, *, intent: str, name: str) -> None:
        ...
    def to_dict(self) -> V1alpha1RequesterDict:
        ...
class V1alpha1RequesterDict(typing.TypedDict, total=False):
    intent: str
    name: str
