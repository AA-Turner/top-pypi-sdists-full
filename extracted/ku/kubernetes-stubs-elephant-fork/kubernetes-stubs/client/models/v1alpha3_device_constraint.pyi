import datetime
import typing

import kubernetes.client

class V1alpha3DeviceConstraint:
    match_attribute: typing.Optional[str]
    requests: typing.Optional[list[str]]
    
    def __init__(self, *, match_attribute: typing.Optional[str] = ..., requests: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3DeviceConstraintDict:
        ...
class V1alpha3DeviceConstraintDict(typing.TypedDict, total=False):
    matchAttribute: typing.Optional[str]
    requests: typing.Optional[list[str]]
