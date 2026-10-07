import datetime
import typing

import kubernetes.client

class V1NodeAllocatableMappedResources:
    name: str
    quantity: str
    
    def __init__(self, *, name: str, quantity: str) -> None:
        ...
    def to_dict(self) -> V1NodeAllocatableMappedResourcesDict:
        ...
class V1NodeAllocatableMappedResourcesDict(typing.TypedDict, total=False):
    name: str
    quantity: str
