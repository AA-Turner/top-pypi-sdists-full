#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Catalyst-style resolution rules for Spark Connect proto relations.

Each ResolutionRule declares the rel_type it targets (e.g. "filter") and is
registered in RESOLUTION_RULES.  map_relation calls try_resolve(rel) before
dispatching to the standard map_* handler, giving rules a chance to rewrite
the plan.

Rules receive the raw proto Relation and are responsible for resolving any
child relations they need (via map_relation, which caches by plan_id so the
subsequent handler call never re-does the work).  applies_to is the
authoritative gate: the first rule whose applies_to matches wins (no
chaining).  If its apply returns None or raises, the caller falls back to the
standard map_* handler, so there is always a safe fallback path.

To add a new rule:
1. Create a new file in this package (e.g. filter_my_rule.py).
2. Implement ResolutionRule.
3. Import the rule instance here and add it to RESOLUTION_RULES.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

if TYPE_CHECKING:
    pass


# ---------------------------------------------------------------------------
# Protocol
# ---------------------------------------------------------------------------


@runtime_checkable
class ResolutionRule(Protocol):
    """Interface for a single proto-level resolution / rewrite rule.

    Attributes:
        name: Human-readable rule name used in log messages.
        rel_type: The Relation.rel_type this rule handles (e.g. "filter").
            Used as the registry key; rules are only invoked for matching
            rel_types.
    """

    name: str
    rel_type: str

    def applies_to(self, rel: relation_proto.Relation) -> bool:
        """Return True when this rule should attempt to rewrite rel.

        Should be a cheap structural check on the proto tree only — no
        child resolution.
        """
        ...

    def apply(self, rel: relation_proto.Relation) -> DataFrameContainer | None:
        """Perform the rewrite and return a DataFrameContainer on success.

        Rules are responsible for resolving any child relations they need.
        Return None to decline (fall back to the normal mapping path).
        """
        ...


# ---------------------------------------------------------------------------
# Registry & dispatcher
# ---------------------------------------------------------------------------

RESOLUTION_RULES: dict[str, list[ResolutionRule]] = {}


def _register(rule: ResolutionRule) -> None:
    RESOLUTION_RULES.setdefault(rule.rel_type, []).append(rule)


def try_resolve(rel: relation_proto.Relation) -> DataFrameContainer | None:
    """Resolve rel using the first rule whose applies_to matches.

    There is no rule chaining: applies_to is the authoritative gate, so the
    first matching rule wins.  If its apply() returns None (a deeper decline)
    or raises, we fall back to the standard mapping path (return None) rather
    than trying subsequent rules.  Rules are checked in registration order.
    """
    from snowflake.snowpark_connect.utils.telemetry import telemetry

    rel_type = rel.WhichOneof("rel_type")
    if rel_type is None:
        return None
    for rule in RESOLUTION_RULES.get(rel_type, []):
        if not rule.applies_to(rel):
            continue
        try:
            result = rule.apply(rel)
        except Exception as exc:
            logger.warning(
                "Resolution rule %s failed; falling back to standard handler: %s",
                rule.name,
                exc,
            )
            telemetry.send_resolution_rule_telemetry(rule.name, rel_type, "error")
            return None
        outcome = "applied" if result is not None else "declined"
        if result is not None:
            logger.debug("Resolution rule %s applied to %s", rule.name, rel_type)
        telemetry.send_resolution_rule_telemetry(rule.name, rel_type, outcome)
        return result
    return None


# ---------------------------------------------------------------------------
# Rule registration
# ---------------------------------------------------------------------------
# Import here (not at top of module) to avoid triggering heavy imports before
# the server is initialized; each rule file uses lazy imports for map_* calls.

from snowflake.snowpark_connect.relation.resolution_rules.filter_hive_partition_pruning import (  # noqa: E402
    filter_over_hive_partitioned_read,
)
from snowflake.snowpark_connect.relation.resolution_rules.filter_resolve_missing_references import (  # noqa: E402
    resolve_missing_references_in_filter,
)
from snowflake.snowpark_connect.relation.resolution_rules.filter_subquery_alias import (  # noqa: E402
    filter_over_subquery_alias,
)
from snowflake.snowpark_connect.relation.resolution_rules.sort_over_aggregate import (  # noqa: E402
    resolve_sort_over_aggregate,
)

_register(resolve_missing_references_in_filter)
_register(filter_over_subquery_alias)
_register(filter_over_hive_partitioned_read)
_register(resolve_sort_over_aggregate)
