import datetime
import typing

import kubernetes.client

class V1NodeRuntimeHandlerFeatures:
    recursive_read_only_mounts: typing.Optional[bool]
    user_namespaces: typing.Optional[bool]
    
    def __init__(self, *, recursive_read_only_mounts: typing.Optional[bool] = ..., user_namespaces: typing.Optional[bool] = ...) -> None:
        ...
    def to_dict(self) -> V1NodeRuntimeHandlerFeaturesDict:
        ...
class V1NodeRuntimeHandlerFeaturesDict(typing.TypedDict, total=False):
    recursiveReadOnlyMounts: typing.Optional[bool]
    userNamespaces: typing.Optional[bool]
