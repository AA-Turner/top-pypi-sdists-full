import datetime
import typing

import kubernetes.client

class V1NodeAllocatableResourceClaimStatus:
    containers: typing.Optional[list[str]]
    mapping: typing.Optional[list[kubernetes.client.V1NodeAllocatableMappedResources]]
    overhead: typing.Optional[list[kubernetes.client.V1NodeAllocatableOverheadResources]]
    resource_claim_name: str
    
    def __init__(self, *, containers: typing.Optional[list[str]] = ..., mapping: typing.Optional[list[kubernetes.client.V1NodeAllocatableMappedResources]] = ..., overhead: typing.Optional[list[kubernetes.client.V1NodeAllocatableOverheadResources]] = ..., resource_claim_name: str) -> None:
        ...
    def to_dict(self) -> V1NodeAllocatableResourceClaimStatusDict:
        ...
class V1NodeAllocatableResourceClaimStatusDict(typing.TypedDict, total=False):
    containers: typing.Optional[list[str]]
    mapping: typing.Optional[list[kubernetes.client.V1NodeAllocatableMappedResourcesDict]]
    overhead: typing.Optional[list[kubernetes.client.V1NodeAllocatableOverheadResourcesDict]]
    resourceClaimName: str
