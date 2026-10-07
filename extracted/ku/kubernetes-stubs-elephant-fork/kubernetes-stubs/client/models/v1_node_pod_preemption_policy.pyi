import datetime
import typing

import kubernetes.client

class V1NodePodPreemptionPolicy:
    disable_resize_preemption: typing.Optional[list[str]]
    
    def __init__(self, *, disable_resize_preemption: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1NodePodPreemptionPolicyDict:
        ...
class V1NodePodPreemptionPolicyDict(typing.TypedDict, total=False):
    disableResizePreemption: typing.Optional[list[str]]
