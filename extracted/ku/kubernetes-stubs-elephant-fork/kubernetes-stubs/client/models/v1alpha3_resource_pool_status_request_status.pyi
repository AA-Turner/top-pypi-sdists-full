import datetime
import typing

import kubernetes.client

class V1alpha3ResourcePoolStatusRequestStatus:
    conditions: typing.Optional[list[kubernetes.client.V1Condition]]
    pool_count: int
    pools: typing.Optional[list[kubernetes.client.V1alpha3PoolStatus]]
    
    def __init__(self, *, conditions: typing.Optional[list[kubernetes.client.V1Condition]] = ..., pool_count: int, pools: typing.Optional[list[kubernetes.client.V1alpha3PoolStatus]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3ResourcePoolStatusRequestStatusDict:
        ...
class V1alpha3ResourcePoolStatusRequestStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[list[kubernetes.client.V1ConditionDict]]
    poolCount: int
    pools: typing.Optional[list[kubernetes.client.V1alpha3PoolStatusDict]]
