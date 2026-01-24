import datetime
import typing

import kubernetes.client

class V1CELDeviceSelector:
    expression: str
    
    def __init__(self, *, expression: str) -> None:
        ...
    def to_dict(self) -> V1CELDeviceSelectorDict:
        ...
class V1CELDeviceSelectorDict(typing.TypedDict, total=False):
    expression: str
