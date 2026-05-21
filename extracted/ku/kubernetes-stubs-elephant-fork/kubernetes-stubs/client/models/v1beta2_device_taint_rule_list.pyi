import datetime
import typing

import kubernetes.client

class V1beta2DeviceTaintRuleList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1beta2DeviceTaintRule]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., items: list[kubernetes.client.V1beta2DeviceTaintRule], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2DeviceTaintRuleListDict:
        ...
class V1beta2DeviceTaintRuleListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1beta2DeviceTaintRuleDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
