import datetime
import typing

import kubernetes.client

class V1beta1PodGroupStatus:
    conditions: typing.Optional[list[kubernetes.client.V1Condition]]
    resource_claim_statuses: typing.Optional[list[kubernetes.client.V1beta1PodGroupResourceClaimStatus]]
    
    def __init__(self, *, conditions: typing.Optional[list[kubernetes.client.V1Condition]] = ..., resource_claim_statuses: typing.Optional[list[kubernetes.client.V1beta1PodGroupResourceClaimStatus]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1PodGroupStatusDict:
        ...
class V1beta1PodGroupStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[list[kubernetes.client.V1ConditionDict]]
    resourceClaimStatuses: typing.Optional[list[kubernetes.client.V1beta1PodGroupResourceClaimStatusDict]]
