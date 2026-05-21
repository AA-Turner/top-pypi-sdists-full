import datetime
import typing

import kubernetes.client

class V1alpha2PodGroupResourceClaimStatus:
    name: str
    resource_claim_name: typing.Optional[str]
    
    def __init__(self, *, name: str, resource_claim_name: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha2PodGroupResourceClaimStatusDict:
        ...
class V1alpha2PodGroupResourceClaimStatusDict(typing.TypedDict, total=False):
    name: str
    resourceClaimName: typing.Optional[str]
