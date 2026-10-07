import datetime
import typing

import kubernetes.client

class V1beta1PodGroupResourceClaim:
    name: str
    resource_claim_name: typing.Optional[str]
    resource_claim_template_name: typing.Optional[str]
    
    def __init__(self, *, name: str, resource_claim_name: typing.Optional[str] = ..., resource_claim_template_name: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1PodGroupResourceClaimDict:
        ...
class V1beta1PodGroupResourceClaimDict(typing.TypedDict, total=False):
    name: str
    resourceClaimName: typing.Optional[str]
    resourceClaimTemplateName: typing.Optional[str]
