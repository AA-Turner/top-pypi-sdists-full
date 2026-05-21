import datetime
import typing

import kubernetes.client

class V1ListMeta:
    _continue: typing.Optional[str]
    remaining_item_count: typing.Optional[int]
    resource_version: typing.Optional[str]
    self_link: typing.Optional[str]
    shard_info: typing.Optional[kubernetes.client.V1ShardInfo]
    
    def __init__(self, *, _continue: typing.Optional[str] = ..., remaining_item_count: typing.Optional[int] = ..., resource_version: typing.Optional[str] = ..., self_link: typing.Optional[str] = ..., shard_info: typing.Optional[kubernetes.client.V1ShardInfo] = ...) -> None:
        ...
    def to_dict(self) -> V1ListMetaDict:
        ...
class V1ListMetaDict(typing.TypedDict, total=False):
    _continue: typing.Optional[str]
    remainingItemCount: typing.Optional[int]
    resourceVersion: typing.Optional[str]
    selfLink: typing.Optional[str]
    shardInfo: typing.Optional[kubernetes.client.V1ShardInfoDict]
