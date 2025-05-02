import datetime
import typing

import kubernetes.client

class V1beta1ResourcePool:
    generation: int
    name: str
    resource_slice_count: int
    
    def __init__(self, *, generation: int, name: str, resource_slice_count: int) -> None:
        ...
    def to_dict(self) -> V1beta1ResourcePoolDict:
        ...
class V1beta1ResourcePoolDict(typing.TypedDict, total=False):
    generation: int
    name: str
    resourceSliceCount: int
