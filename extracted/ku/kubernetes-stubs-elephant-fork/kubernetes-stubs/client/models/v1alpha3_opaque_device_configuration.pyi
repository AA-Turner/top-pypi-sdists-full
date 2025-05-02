import datetime
import typing

import kubernetes.client

class V1alpha3OpaqueDeviceConfiguration:
    driver: str
    parameters: typing.Any
    
    def __init__(self, *, driver: str, parameters: typing.Any) -> None:
        ...
    def to_dict(self) -> V1alpha3OpaqueDeviceConfigurationDict:
        ...
class V1alpha3OpaqueDeviceConfigurationDict(typing.TypedDict, total=False):
    driver: str
    parameters: typing.Any
