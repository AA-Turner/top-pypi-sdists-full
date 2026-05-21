import datetime
import typing

import kubernetes.client

class V1beta2DeviceTaintRule:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1beta2DeviceTaintRuleSpec
    status: typing.Optional[kubernetes.client.V1beta2DeviceTaintRuleStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1beta2DeviceTaintRuleSpec, status: typing.Optional[kubernetes.client.V1beta2DeviceTaintRuleStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2DeviceTaintRuleDict:
        ...
class V1beta2DeviceTaintRuleDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1beta2DeviceTaintRuleSpecDict
    status: typing.Optional[kubernetes.client.V1beta2DeviceTaintRuleStatusDict]
