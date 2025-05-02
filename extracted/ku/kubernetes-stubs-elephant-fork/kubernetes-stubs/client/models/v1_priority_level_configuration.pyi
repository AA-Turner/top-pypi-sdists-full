import datetime
import typing

import kubernetes.client

class V1PriorityLevelConfiguration:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1PriorityLevelConfigurationSpec]
    status: typing.Optional[kubernetes.client.V1PriorityLevelConfigurationStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1PriorityLevelConfigurationSpec] = ..., status: typing.Optional[kubernetes.client.V1PriorityLevelConfigurationStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1PriorityLevelConfigurationDict:
        ...
class V1PriorityLevelConfigurationDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1PriorityLevelConfigurationSpecDict]
    status: typing.Optional[kubernetes.client.V1PriorityLevelConfigurationStatusDict]
