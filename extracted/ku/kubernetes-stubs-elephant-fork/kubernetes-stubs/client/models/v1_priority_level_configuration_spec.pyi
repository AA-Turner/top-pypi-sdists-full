import datetime
import typing

import kubernetes.client

class V1PriorityLevelConfigurationSpec:
    exempt: typing.Optional[kubernetes.client.V1ExemptPriorityLevelConfiguration]
    limited: typing.Optional[kubernetes.client.V1LimitedPriorityLevelConfiguration]
    type: str
    
    def __init__(self, *, exempt: typing.Optional[kubernetes.client.V1ExemptPriorityLevelConfiguration] = ..., limited: typing.Optional[kubernetes.client.V1LimitedPriorityLevelConfiguration] = ..., type: str) -> None:
        ...
    def to_dict(self) -> V1PriorityLevelConfigurationSpecDict:
        ...
class V1PriorityLevelConfigurationSpecDict(typing.TypedDict, total=False):
    exempt: typing.Optional[kubernetes.client.V1ExemptPriorityLevelConfigurationDict]
    limited: typing.Optional[kubernetes.client.V1LimitedPriorityLevelConfigurationDict]
    type: str
