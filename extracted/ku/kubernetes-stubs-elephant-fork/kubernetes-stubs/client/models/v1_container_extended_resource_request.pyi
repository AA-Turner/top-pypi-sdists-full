import datetime
import typing

import kubernetes.client

class V1ContainerExtendedResourceRequest:
    container_name: str
    request_name: str
    resource_name: str
    
    def __init__(self, *, container_name: str, request_name: str, resource_name: str) -> None:
        ...
    def to_dict(self) -> V1ContainerExtendedResourceRequestDict:
        ...
class V1ContainerExtendedResourceRequestDict(typing.TypedDict, total=False):
    containerName: str
    requestName: str
    resourceName: str
