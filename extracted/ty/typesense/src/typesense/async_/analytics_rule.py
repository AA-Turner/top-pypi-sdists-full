"""Per-rule client for Analytics rules operations (async)."""

from .api_call import AsyncApiCall
from typesense.types.analytics import AnalyticsRuleSchema


class AsyncAnalyticsRule:
    def __init__(self, api_call: AsyncApiCall, rule_name: str) -> None:
        self.api_call = api_call
        self.rule_name = rule_name

    @property
    def _endpoint_path(self) -> str:
        from .analytics_rules import AsyncAnalyticsRules

        return "/".join([AsyncAnalyticsRules.resource_path, self.rule_name])

    async def retrieve(self) -> AnalyticsRuleSchema:
        response: AnalyticsRuleSchema = await self.api_call.get(
            self._endpoint_path,
            as_json=True,
            entity_type=AnalyticsRuleSchema,
        )
        return response

    async def delete(self) -> AnalyticsRuleSchema:
        response: AnalyticsRuleSchema = await self.api_call.delete(
            self._endpoint_path,
            entity_type=AnalyticsRuleSchema,
        )
        return response
