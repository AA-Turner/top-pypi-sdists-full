import datetime
import typing

import kubernetes.client

class V1ContainerRestartRule:
    action: str
    exit_codes: typing.Optional[kubernetes.client.V1ContainerRestartRuleOnExitCodes]
    
    def __init__(self, *, action: str, exit_codes: typing.Optional[kubernetes.client.V1ContainerRestartRuleOnExitCodes] = ...) -> None:
        ...
    def to_dict(self) -> V1ContainerRestartRuleDict:
        ...
class V1ContainerRestartRuleDict(typing.TypedDict, total=False):
    action: str
    exitCodes: typing.Optional[kubernetes.client.V1ContainerRestartRuleOnExitCodesDict]
