"""Client for Analytics rules collection operations (async)."""

import sys

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

from .analytics_rule import AsyncAnalyticsRule
from .api_call import AsyncApiCall
from typesense.types.analytics import (
    AnalyticsRuleCreate,
    AnalyticsRuleSchema,
    AnalyticsRuleUpdate,
)


class AsyncAnalyticsRules(object):
    resource_path: typing.Final[str] = "/analytics/rules"

    def __init__(self, api_call: AsyncApiCall) -> None:
        self.api_call = api_call
        self.rules: typing.Dict[str, AsyncAnalyticsRule] = {}

    def __getitem__(self, rule_name: str) -> AsyncAnalyticsRule:
        if rule_name not in self.rules:
            self.rules[rule_name] = AsyncAnalyticsRule(self.api_call, rule_name)
        return self.rules[rule_name]

    async def create(self, rule: AnalyticsRuleCreate) -> AnalyticsRuleSchema:
        response: AnalyticsRuleSchema = await self.api_call.post(
            AsyncAnalyticsRules.resource_path,
            body=rule,
            as_json=True,
            entity_type=AnalyticsRuleSchema,
        )
        return response

    async def retrieve(
        self, *, rule_tag: typing.Union[str, None] = None
    ) -> typing.List[AnalyticsRuleSchema]:
        params: typing.Dict[str, str] = {}
        if rule_tag:
            params["rule_tag"] = rule_tag
        response: typing.List[AnalyticsRuleSchema] = await self.api_call.get(
            AsyncAnalyticsRules.resource_path,
            params=params if params else None,
            as_json=True,
            entity_type=typing.List[AnalyticsRuleSchema],
        )
        return response

    async def upsert(
        self, rule_name: str, update: AnalyticsRuleUpdate
    ) -> AnalyticsRuleSchema:
        response: AnalyticsRuleSchema = await self.api_call.put(
            "/".join([AsyncAnalyticsRules.resource_path, rule_name]),
            body=update,
            entity_type=AnalyticsRuleSchema,
        )
        return response
