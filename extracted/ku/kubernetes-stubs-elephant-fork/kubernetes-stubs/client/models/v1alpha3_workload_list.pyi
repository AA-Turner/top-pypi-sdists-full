import datetime
import typing

import kubernetes.client

class V1alpha3WorkloadList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1alpha3Workload]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., items: list[kubernetes.client.V1alpha3Workload], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3WorkloadListDict:
        ...
class V1alpha3WorkloadListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1alpha3WorkloadDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
