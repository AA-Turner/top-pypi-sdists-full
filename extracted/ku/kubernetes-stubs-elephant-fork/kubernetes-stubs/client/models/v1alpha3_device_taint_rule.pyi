import datetime
import typing

import kubernetes.client

class V1alpha3DeviceTaintRule:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1alpha3DeviceTaintRuleSpec
    status: typing.Optional[kubernetes.client.V1alpha3DeviceTaintRuleStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1alpha3DeviceTaintRuleSpec, status: typing.Optional[kubernetes.client.V1alpha3DeviceTaintRuleStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3DeviceTaintRuleDict:
        ...
class V1alpha3DeviceTaintRuleDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1alpha3DeviceTaintRuleSpecDict
    status: typing.Optional[kubernetes.client.V1alpha3DeviceTaintRuleStatusDict]
