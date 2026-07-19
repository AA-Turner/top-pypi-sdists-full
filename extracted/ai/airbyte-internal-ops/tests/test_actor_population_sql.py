"""Regression tests for the actor-population SQL bind-parameter typing.

The `pg8000` driver sends each occurrence of a named bind parameter as a
separate, initially untyped positional parameter over Postgres' extended query
protocol. If `:rollout_created_at` appears in a bare predicate such as
`:rollout_created_at IS NOT NULL`, Postgres cannot infer that occurrence's type
and rejects the whole statement with `42P18: could not determine data type of
parameter`. `query_actor_population_by_org` then swallows the `SQLAlchemyError`
and returns an empty `ConnectorPopulation`, which renders every rollout tier
card as `0 of 0` even when actors are pinned.

Guard the fix by requiring every `:rollout_created_at` occurrence in the
population SQL to be wrapped in an explicit `CAST(... AS timestamptz)`, which
gives Postgres a concrete type for each positional parameter.
"""

import re

from airbyte_ops_mcp.prod_db_access import sql

_POPULATION_STATEMENTS = {
    "source": sql.SELECT_SOURCE_ACTOR_POPULATION_BY_ORG,
    "destination": sql.SELECT_DESTINATION_ACTOR_POPULATION_BY_ORG,
}

# A `CAST(:rollout_created_at AS timestamptz)` wrapper, tolerant of surrounding
# whitespace so a purely cosmetic reformat does not trip the guard. The type is
# pinned to `timestamptz` because that is what the gate comparison against
# `jobs.created_at` requires; a cast to any other type would not match.
_CAST_ROLLOUT_PARAM = re.compile(
    r"CAST\(\s*:rollout_created_at\s+AS\s+timestamptz\s*\)",
    re.IGNORECASE,
)


def test_population_sql_casts_every_rollout_created_at_bind() -> None:
    for label, statement in _POPULATION_STATEMENTS.items():
        text = str(statement.text)
        assert ":rollout_created_at" in text, f"{label} SQL lost the gate param"
        # Drop every cast-wrapped occurrence; any `:rollout_created_at` left over
        # is an untyped bind (e.g. a bare `:rollout_created_at IS NOT NULL`
        # predicate), which triggers Postgres 42P18 under pg8000.
        residual = _CAST_ROLLOUT_PARAM.sub("", text)
        assert ":rollout_created_at" not in residual, (
            f"{label} population SQL has an untyped `:rollout_created_at` "
            "occurrence; wrap every occurrence in `CAST(... AS timestamptz)` "
            "so pg8000's extended query protocol can type each positional "
            "parameter and Postgres does not fail with 42P18."
        )
