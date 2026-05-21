import datetime
import typing

import kubernetes.client

class V1NodeAllocatableResourceClaimStatus:
    containers: typing.Optional[list[str]]
    resource_claim_name: str
    resources: dict[str, str]
    
    def __init__(self, *, containers: typing.Optional[list[str]] = ..., resource_claim_name: str, resources: dict[str, str]) -> None:
        ...
    def to_dict(self) -> V1NodeAllocatableResourceClaimStatusDict:
        ...
class V1NodeAllocatableResourceClaimStatusDict(typing.TypedDict, total=False):
    containers: typing.Optional[list[str]]
    resourceClaimName: str
    resources: dict[str, str]
