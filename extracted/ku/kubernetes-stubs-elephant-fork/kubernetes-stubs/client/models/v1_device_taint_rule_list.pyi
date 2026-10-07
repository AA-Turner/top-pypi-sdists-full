import datetime
import typing

import kubernetes.client

class V1DeviceTaintRuleList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1DeviceTaintRule]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., items: list[kubernetes.client.V1DeviceTaintRule], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...) -> None:
        ...
    def to_dict(self) -> V1DeviceTaintRuleListDict:
        ...
class V1DeviceTaintRuleListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1DeviceTaintRuleDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
