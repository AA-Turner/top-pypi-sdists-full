import datetime
import typing

import kubernetes.client

class V1ResourceAttributes:
    field_selector: typing.Optional[kubernetes.client.V1FieldSelectorAttributes]
    group: typing.Optional[str]
    label_selector: typing.Optional[kubernetes.client.V1LabelSelectorAttributes]
    name: typing.Optional[str]
    namespace: typing.Optional[str]
    resource: typing.Optional[str]
    subresource: typing.Optional[str]
    verb: typing.Optional[str]
    version: typing.Optional[str]
    
    def __init__(self, *, field_selector: typing.Optional[kubernetes.client.V1FieldSelectorAttributes] = ..., group: typing.Optional[str] = ..., label_selector: typing.Optional[kubernetes.client.V1LabelSelectorAttributes] = ..., name: typing.Optional[str] = ..., namespace: typing.Optional[str] = ..., resource: typing.Optional[str] = ..., subresource: typing.Optional[str] = ..., verb: typing.Optional[str] = ..., version: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1ResourceAttributesDict:
        ...
class V1ResourceAttributesDict(typing.TypedDict, total=False):
    fieldSelector: typing.Optional[kubernetes.client.V1FieldSelectorAttributesDict]
    group: typing.Optional[str]
    labelSelector: typing.Optional[kubernetes.client.V1LabelSelectorAttributesDict]
    name: typing.Optional[str]
    namespace: typing.Optional[str]
    resource: typing.Optional[str]
    subresource: typing.Optional[str]
    verb: typing.Optional[str]
    version: typing.Optional[str]
