import datetime
import typing

import kubernetes.client

class V1DeviceTaintRule:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1DeviceTaintRuleSpec
    status: typing.Optional[kubernetes.client.V1DeviceTaintRuleStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1DeviceTaintRuleSpec, status: typing.Optional[kubernetes.client.V1DeviceTaintRuleStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1DeviceTaintRuleDict:
        ...
class V1DeviceTaintRuleDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1DeviceTaintRuleSpecDict
    status: typing.Optional[kubernetes.client.V1DeviceTaintRuleStatusDict]
