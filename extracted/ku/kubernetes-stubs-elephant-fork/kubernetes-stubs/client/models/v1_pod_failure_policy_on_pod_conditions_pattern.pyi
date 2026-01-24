import datetime
import typing

import kubernetes.client

class V1PodFailurePolicyOnPodConditionsPattern:
    status: typing.Optional[str]
    type: str
    
    def __init__(self, *, status: typing.Optional[str] = ..., type: str) -> None:
        ...
    def to_dict(self) -> V1PodFailurePolicyOnPodConditionsPatternDict:
        ...
class V1PodFailurePolicyOnPodConditionsPatternDict(typing.TypedDict, total=False):
    status: typing.Optional[str]
    type: str
