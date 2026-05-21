import datetime
import typing

import kubernetes.client

class V1PodSchedulingGroup:
    pod_group_name: typing.Optional[str]
    
    def __init__(self, *, pod_group_name: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1PodSchedulingGroupDict:
        ...
class V1PodSchedulingGroupDict(typing.TypedDict, total=False):
    podGroupName: typing.Optional[str]
