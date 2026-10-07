import datetime
import typing

import kubernetes.client

class V1beta1PodGroupResourceClaimStatus:
    name: str
    resource_claim_name: typing.Optional[str]
    
    def __init__(self, *, name: str, resource_claim_name: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1PodGroupResourceClaimStatusDict:
        ...
class V1beta1PodGroupResourceClaimStatusDict(typing.TypedDict, total=False):
    name: str
    resourceClaimName: typing.Optional[str]
