import datetime
import typing

import kubernetes.client

class V1beta1ParamRef:
    name: typing.Optional[str]
    namespace: typing.Optional[str]
    parameter_not_found_action: typing.Optional[str]
    selector: typing.Optional[kubernetes.client.V1LabelSelector]
    
    def __init__(self, *, name: typing.Optional[str] = ..., namespace: typing.Optional[str] = ..., parameter_not_found_action: typing.Optional[str] = ..., selector: typing.Optional[kubernetes.client.V1LabelSelector] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1ParamRefDict:
        ...
class V1beta1ParamRefDict(typing.TypedDict, total=False):
    name: typing.Optional[str]
    namespace: typing.Optional[str]
    parameterNotFoundAction: typing.Optional[str]
    selector: typing.Optional[kubernetes.client.V1LabelSelectorDict]
