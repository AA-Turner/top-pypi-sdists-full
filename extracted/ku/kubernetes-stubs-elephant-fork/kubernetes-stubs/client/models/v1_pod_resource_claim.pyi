import datetime
import typing

import kubernetes.client

class V1PodResourceClaim:
    name: str
    resource_claim_name: typing.Optional[str]
    resource_claim_template_name: typing.Optional[str]
    
    def __init__(self, *, name: str, resource_claim_name: typing.Optional[str] = ..., resource_claim_template_name: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1PodResourceClaimDict:
        ...
class V1PodResourceClaimDict(typing.TypedDict, total=False):
    name: str
    resourceClaimName: typing.Optional[str]
    resourceClaimTemplateName: typing.Optional[str]
