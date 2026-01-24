import datetime
import typing

import kubernetes.client

class V1OpaqueDeviceConfiguration:
    driver: str
    parameters: typing.Any
    
    def __init__(self, *, driver: str, parameters: typing.Any) -> None:
        ...
    def to_dict(self) -> V1OpaqueDeviceConfigurationDict:
        ...
class V1OpaqueDeviceConfigurationDict(typing.TypedDict, total=False):
    driver: str
    parameters: typing.Any
