import datetime
import typing

import kubernetes.client

class V1ContainerRestartRuleOnExitCodes:
    operator: str
    values: typing.Optional[list[int]]
    
    def __init__(self, *, operator: str, values: typing.Optional[list[int]] = ...) -> None:
        ...
    def to_dict(self) -> V1ContainerRestartRuleOnExitCodesDict:
        ...
class V1ContainerRestartRuleOnExitCodesDict(typing.TypedDict, total=False):
    operator: str
    values: typing.Optional[list[int]]
