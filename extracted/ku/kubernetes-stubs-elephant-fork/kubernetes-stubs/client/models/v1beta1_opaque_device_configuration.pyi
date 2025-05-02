import datetime
import typing

import kubernetes.client

class V1beta1OpaqueDeviceConfiguration:
    driver: str
    parameters: typing.Any
    
    def __init__(self, *, driver: str, parameters: typing.Any) -> None:
        ...
    def to_dict(self) -> V1beta1OpaqueDeviceConfigurationDict:
        ...
class V1beta1OpaqueDeviceConfigurationDict(typing.TypedDict, total=False):
    driver: str
    parameters: typing.Any
