import datetime
import typing

import kubernetes.client

class V1LimitResponse:
    queuing: typing.Optional[kubernetes.client.V1QueuingConfiguration]
    type: str
    
    def __init__(self, *, queuing: typing.Optional[kubernetes.client.V1QueuingConfiguration] = ..., type: str) -> None:
        ...
    def to_dict(self) -> V1LimitResponseDict:
        ...
class V1LimitResponseDict(typing.TypedDict, total=False):
    queuing: typing.Optional[kubernetes.client.V1QueuingConfigurationDict]
    type: str
