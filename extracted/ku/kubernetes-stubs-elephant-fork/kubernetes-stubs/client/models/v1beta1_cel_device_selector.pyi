import datetime
import typing

import kubernetes.client

class V1beta1CELDeviceSelector:
    expression: str
    
    def __init__(self, *, expression: str) -> None:
        ...
    def to_dict(self) -> V1beta1CELDeviceSelectorDict:
        ...
class V1beta1CELDeviceSelectorDict(typing.TypedDict, total=False):
    expression: str
