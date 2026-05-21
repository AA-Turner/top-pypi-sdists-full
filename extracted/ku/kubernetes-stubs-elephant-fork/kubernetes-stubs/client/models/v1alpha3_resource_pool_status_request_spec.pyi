import datetime
import typing

import kubernetes.client

class V1alpha3ResourcePoolStatusRequestSpec:
    driver: str
    limit: typing.Optional[int]
    pool_name: typing.Optional[str]
    
    def __init__(self, *, driver: str, limit: typing.Optional[int] = ..., pool_name: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3ResourcePoolStatusRequestSpecDict:
        ...
class V1alpha3ResourcePoolStatusRequestSpecDict(typing.TypedDict, total=False):
    driver: str
    limit: typing.Optional[int]
    poolName: typing.Optional[str]
