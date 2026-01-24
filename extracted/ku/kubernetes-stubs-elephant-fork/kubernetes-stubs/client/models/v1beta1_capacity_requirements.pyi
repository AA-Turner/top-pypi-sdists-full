import datetime
import typing

import kubernetes.client

class V1beta1CapacityRequirements:
    requests: typing.Optional[dict[str, str]]
    
    def __init__(self, *, requests: typing.Optional[dict[str, str]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1CapacityRequirementsDict:
        ...
class V1beta1CapacityRequirementsDict(typing.TypedDict, total=False):
    requests: typing.Optional[dict[str, str]]
