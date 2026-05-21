import datetime
import typing

import kubernetes.client

class V1alpha2PodGroupStatus:
    conditions: typing.Optional[list[kubernetes.client.V1Condition]]
    resource_claim_statuses: typing.Optional[list[kubernetes.client.V1alpha2PodGroupResourceClaimStatus]]
    
    def __init__(self, *, conditions: typing.Optional[list[kubernetes.client.V1Condition]] = ..., resource_claim_statuses: typing.Optional[list[kubernetes.client.V1alpha2PodGroupResourceClaimStatus]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha2PodGroupStatusDict:
        ...
class V1alpha2PodGroupStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[list[kubernetes.client.V1ConditionDict]]
    resourceClaimStatuses: typing.Optional[list[kubernetes.client.V1alpha2PodGroupResourceClaimStatusDict]]
