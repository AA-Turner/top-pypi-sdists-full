import datetime
import typing

import kubernetes.client

class V1alpha3WorkloadPodGroupResourceClaim:
    name: str
    resource_claim_name: typing.Optional[str]
    resource_claim_template_name: typing.Optional[str]
    
    def __init__(self, *, name: str, resource_claim_name: typing.Optional[str] = ..., resource_claim_template_name: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3WorkloadPodGroupResourceClaimDict:
        ...
class V1alpha3WorkloadPodGroupResourceClaimDict(typing.TypedDict, total=False):
    name: str
    resourceClaimName: typing.Optional[str]
    resourceClaimTemplateName: typing.Optional[str]
