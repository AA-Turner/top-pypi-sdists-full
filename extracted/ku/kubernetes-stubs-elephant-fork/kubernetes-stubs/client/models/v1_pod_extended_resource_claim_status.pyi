import datetime
import typing

import kubernetes.client

class V1PodExtendedResourceClaimStatus:
    request_mappings: list[kubernetes.client.V1ContainerExtendedResourceRequest]
    resource_claim_name: str
    
    def __init__(self, *, request_mappings: list[kubernetes.client.V1ContainerExtendedResourceRequest], resource_claim_name: str) -> None:
        ...
    def to_dict(self) -> V1PodExtendedResourceClaimStatusDict:
        ...
class V1PodExtendedResourceClaimStatusDict(typing.TypedDict, total=False):
    requestMappings: list[kubernetes.client.V1ContainerExtendedResourceRequestDict]
    resourceClaimName: str
