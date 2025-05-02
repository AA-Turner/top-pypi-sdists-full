import datetime
import typing

import kubernetes.client

class V1PriorityLevelConfigurationReference:
    name: str
    
    def __init__(self, *, name: str) -> None:
        ...
    def to_dict(self) -> V1PriorityLevelConfigurationReferenceDict:
        ...
class V1PriorityLevelConfigurationReferenceDict(typing.TypedDict, total=False):
    name: str
