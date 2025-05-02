import datetime
import typing

import kubernetes.client

class V1alpha3CELDeviceSelector:
    expression: str
    
    def __init__(self, *, expression: str) -> None:
        ...
    def to_dict(self) -> V1alpha3CELDeviceSelectorDict:
        ...
class V1alpha3CELDeviceSelectorDict(typing.TypedDict, total=False):
    expression: str
