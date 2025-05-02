import datetime
import typing

import kubernetes.client

class V1ExemptPriorityLevelConfiguration:
    lendable_percent: typing.Optional[int]
    nominal_concurrency_shares: typing.Optional[int]
    
    def __init__(self, *, lendable_percent: typing.Optional[int] = ..., nominal_concurrency_shares: typing.Optional[int] = ...) -> None:
        ...
    def to_dict(self) -> V1ExemptPriorityLevelConfigurationDict:
        ...
class V1ExemptPriorityLevelConfigurationDict(typing.TypedDict, total=False):
    lendablePercent: typing.Optional[int]
    nominalConcurrencyShares: typing.Optional[int]
