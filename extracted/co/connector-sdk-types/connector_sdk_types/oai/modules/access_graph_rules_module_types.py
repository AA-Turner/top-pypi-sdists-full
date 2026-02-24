import pydantic

from connector_sdk_types.generated.models.access_graph_entitlement_rule import (
    AccessGraphEntitlementRule,
)
from connector_sdk_types.generated.models.implied_access_rule import ImpliedAccessRule


class AccessGraphRulesSettings(pydantic.BaseModel):
    """
    Bundles the two graph-reduction rule lists that a connector can declare
    in its info response to reduce graph payload size.

    Pass an instance to Integration(access_graph_rules=...).
    """

    entitlement_rules: list[AccessGraphEntitlementRule] = pydantic.Field(
        default_factory=list,
        description=(
            "Rules declaring entitlements that automatically exist for every resource "
            "of a given type, allowing the connector to omit individual entitlement nodes."
        ),
    )
    implied_access_rules: list[ImpliedAccessRule] = pydantic.Field(
        default_factory=list,
        description=(
            "Rules declaring how entitlement access propagates along resource relationships."
        ),
    )


__all__ = ["AccessGraphRulesSettings", "AccessGraphEntitlementRule", "ImpliedAccessRule"]
