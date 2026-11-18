"""
Characterization tests that lock the behaviour of existing metadata filter rules.

SUP-845 changes how BLOCK rules are evaluated when they have a condition the caller can't
evaluate: an attribute the lookup doesn't supply (or the SQL column mapping doesn't map) at or
below the finest level the lookup does supply. Example: a (db, schema, table_name) rule checked
at schema level. Every other rule must keep behaving exactly as before. These tests make that
guarantee explicit:

- `_legacy_effect` / `_legacy_sql_conditions` are frozen copies of the evaluation logic as of
  pycarlo v0.12.459 (the version data-collector and monolith pin). They must not be updated
  alongside the production code.
- The matrix tests evaluate many rule sets against lookups at every level (and SQL column
  mappings modelled on data-collector's callers) and assert the real container returns the same
  answer as the frozen logic whenever no BLOCK rule is unevaluable. Only those unevaluable BLOCK
  rules are allowed to change behaviour.
"""

import itertools
from typing import Any, Callable, Dict, List, Optional, Tuple
from unittest import TestCase

from pycarlo.features.metadata import (
    FilterEffectType,
    FilterType,
    MetadataAllowBlockList,
    MetadataFilter,
    MetadataFiltersContainer,
)
from pycarlo.features.metadata.base_allow_block_list import FilterRule

_BLOCK = FilterEffectType.BLOCK
_ALLOW = FilterEffectType.ALLOW

# Hierarchy of metadata attributes, coarsest first. Defined here independently of the production
# code so the test does not share the implementation's notion of "finer".
_LEVELS = {"project": 0, "dataset": 1, "table_name": 2, "table_type": 2}


def _legacy_matches(rule: MetadataFilter, lookup: Dict[str, Any]) -> bool:
    # Frozen copy of FilterRule.matches (v0.12.459): conditions on attributes not supplied match.
    return all(
        c.attribute_name not in lookup
        or FilterRule._match(condition=c, value=lookup.get(c.attribute_name), force_regexp=False)
        for c in rule.conditions or []
    )


def _legacy_effect(
    filters: MetadataAllowBlockList,
    lookup: Dict[str, Any],
    condition: Optional[Callable[[MetadataFilter], bool]] = None,
) -> FilterEffectType:
    # Frozen copy of MetadataFiltersContainer._get_effect (v0.12.459).
    if not filters.filters or any(
        _legacy_matches(f, lookup) for f in filters.get_default_effect_rules(condition=condition)
    ):
        return filters.default_effect
    if any(_legacy_matches(f, lookup) for f in filters.get_other_effect_rules(condition=condition)):
        return filters.other_effect
    return filters.default_effect


def _legacy_whole_project_blocked(filters: MetadataAllowBlockList, project: str) -> bool:
    # Frozen copy of MetadataFiltersContainer.is_whole_project_blocked (v0.12.459).
    return (
        _legacy_effect(
            filters,
            {"project": project},
            condition=lambda f: not f.dataset or f.effect == _ALLOW,
        )
        == _BLOCK
    )


def _is_unevaluable_block_rule(f: MetadataFilter, available: Any) -> bool:
    """
    True if f is a BLOCK rule with a condition on an attribute that isn't available (not supplied
    in the lookup / not mapped to a SQL column) at or below the finest available level. Missing
    coarser attributes don't count.
    """
    levels = [_LEVELS[name] for name in available if name in _LEVELS]
    if not levels or f.effect != _BLOCK:
        return False
    finest = max(levels)
    return any(
        c.attribute_name not in available and _LEVELS.get(c.attribute_name, -1) >= finest
        for c in f.conditions or []
    )


def _has_block_rule_finer_than_lookup(filters: MetadataAllowBlockList, kwargs: Dict) -> bool:
    """True if a BLOCK rule can't be evaluated with the attributes supplied in the lookup."""
    return any(_is_unevaluable_block_rule(f, kwargs) for f in filters.filters)


def _has_project_level_table_block_rule(filters: MetadataAllowBlockList) -> bool:
    """True if a BLOCK rule without a dataset targets tables (table_name / table_type)."""
    return any(
        f.effect == _BLOCK
        and not f.dataset
        and (f.table_name is not None or f.table_type is not None)
        for f in filters.filters
    )


# A pool of rules covering the shapes customers use: whole projects, schemas, schema-only rules
# (no project), table and table_type rules, all comparison types, allow and block, mixed case.
_RULE_POOL: List[MetadataFilter] = [
    MetadataFilter(project="db1", effect=_BLOCK),
    MetadataFilter(project="DB", type=FilterType.PREFIX, effect=_BLOCK),
    MetadataFilter(project="db1", dataset="s1", effect=_BLOCK),
    MetadataFilter(dataset="S2", effect=_BLOCK),
    MetadataFilter(project="db2", dataset="s", type=FilterType.PREFIX, effect=_BLOCK),
    MetadataFilter(project="db1", dataset="(s1|other)", type=FilterType.REGEXP, effect=_BLOCK),
    MetadataFilter(
        project="db1",
        dataset="s1",
        table_name="(int_.*|_intermediate.*)",
        type=FilterType.REGEXP,
        effect=_BLOCK,
    ),
    MetadataFilter(project="db1", table_name="t1", effect=_BLOCK),
    MetadataFilter(table_name="_X", type=FilterType.SUFFIX, effect=_BLOCK),
    MetadataFilter(project="db1", dataset="s1", table_type="VIEW", effect=_BLOCK),
    MetadataFilter(project="db1", dataset="s1", effect=_ALLOW),
    MetadataFilter(project="db1", dataset="s1", table_name="t1", effect=_ALLOW),
    MetadataFilter(project="db2", effect=_ALLOW),
]

_PROJECTS = ["db1", "DB2", "db3"]
_DATASETS = ["s1", "S2", "s3"]
_TABLES = ["T1", "int_orders", "orders_x"]
_TABLE_TYPES = ["TABLE", "VIEW", None]


def _rule_sets() -> List[MetadataAllowBlockList]:
    rule_sets = []
    for size in range(0, 4):
        for combo in itertools.combinations(_RULE_POOL, size):
            for default_effect in (_ALLOW, _BLOCK):
                rule_sets.append(
                    MetadataAllowBlockList(filters=list(combo), default_effect=default_effect)
                )
    return rule_sets


def _lookups() -> List[Dict]:
    lookups: List[Dict] = []
    lookups += [{"project": p} for p in _PROJECTS]
    lookups += [{"dataset": d} for d in _DATASETS]  # Databricks single-catalog path
    lookups += [{"project": p, "dataset": d} for p in _PROJECTS for d in _DATASETS]
    lookups += [
        {"project": p, "dataset": d, "table_name": t}
        for p in _PROJECTS
        for d in _DATASETS
        for t in _TABLES
    ]
    lookups += [
        {"project": p, "dataset": d, "table_name": t, "table_type": tt}
        for p in _PROJECTS[:2]
        for d in _DATASETS[:2]
        for t in _TABLES
        for tt in _TABLE_TYPES
    ]
    return lookups


class TestMetadataFilterBehaviourLock(TestCase):
    RULE_SETS = _rule_sets()
    LOOKUPS = _lookups()

    def test_element_checks_unchanged_for_rules_at_or_above_lookup_level(self):
        compared = 0
        for filters in self.RULE_SETS:
            container = MetadataFiltersContainer(metadata_filters=filters)
            for kwargs in self.LOOKUPS:
                if _has_block_rule_finer_than_lookup(filters, kwargs):
                    continue
                compared += 1
                expected = _legacy_effect(filters, kwargs) == _ALLOW
                self.assertEqual(
                    expected,
                    container.is_metadata_element_allowed(**kwargs),
                    msg=f"filters={filters} lookup={kwargs}",
                )
        # Guard against the matrix silently becoming vacuous.
        self.assertGreater(compared, 20000)

    def test_dataset_checks_unchanged_for_rules_at_or_above_dataset_level(self):
        compared = 0
        for filters in self.RULE_SETS:
            container = MetadataFiltersContainer(metadata_filters=filters)
            for project, dataset in itertools.product(_PROJECTS, _DATASETS):
                kwargs = {"project": project, "dataset": dataset}
                if _has_block_rule_finer_than_lookup(filters, kwargs):
                    continue
                compared += 1
                self.assertEqual(
                    _legacy_effect(filters, kwargs) == _ALLOW,
                    container.is_dataset_allowed(project, dataset),
                    msg=f"filters={filters} lookup={kwargs}",
                )
        self.assertGreater(compared, 2000)

    def test_expensive_collection_checks_unchanged_for_rules_at_or_above_lookup_level(self):
        compared = 0
        for filters in self.RULE_SETS:
            container = MetadataFiltersContainer(expensive_collection_filters=filters)
            for kwargs in self.LOOKUPS:
                if _has_block_rule_finer_than_lookup(filters, kwargs):
                    continue
                compared += 1
                expected = not filters.filters or _legacy_effect(filters, kwargs) == _ALLOW
                self.assertEqual(
                    expected,
                    container.is_expensive_collection_allowed(**kwargs),
                    msg=f"filters={filters} lookup={kwargs}",
                )
        self.assertGreater(compared, 20000)

    def test_whole_project_blocked_unchanged_without_project_level_table_rules(self):
        compared = 0
        for filters in self.RULE_SETS:
            if _has_project_level_table_block_rule(filters):
                continue
            container = MetadataFiltersContainer(metadata_filters=filters)
            for project in _PROJECTS:
                compared += 1
                self.assertEqual(
                    _legacy_whole_project_blocked(filters, project),
                    container.is_whole_project_blocked(project),
                    msg=f"filters={filters} project={project}",
                )
        self.assertGreater(compared, 1000)

    def test_project_with_datasets_filtered_unchanged(self):
        for filters in self.RULE_SETS:
            container = MetadataFiltersContainer(metadata_filters=filters)
            for project in _PROJECTS:
                expected = bool(filters.filters) and any(
                    _legacy_matches(f, {"project": project}) and f.dataset is not None
                    for f in filters.filters
                )
                self.assertEqual(
                    expected,
                    container.is_project_with_datasets_filtered(project),
                    msg=f"filters={filters} project={project}",
                )

    def test_is_metadata_blocked_unchanged(self):
        for filters in self.RULE_SETS:
            container = MetadataFiltersContainer(metadata_filters=filters)
            expected = filters.default_effect == _BLOCK and all(
                f.effect == _BLOCK for f in filters.filters
            )
            self.assertEqual(expected, container.is_metadata_blocked, msg=f"filters={filters}")


def _sql_encoder(column: str, value: str, type: FilterType) -> str:
    if type == FilterType.REGEXP:
        return f"{column} REGEXP '^({value})$'"
    if type == FilterType.PREFIX:
        return f"{column} LIKE '{value}%'"
    if type == FilterType.SUFFIX:
        return f"{column} LIKE '%{value}'"
    if type == FilterType.SUBSTRING:
        return f"{column} LIKE '%{value}%'"
    return f"{column}='{value}'"


class TestMetadataFilterSqlBehaviourLock(TestCase):
    """
    Pinned get_sql_conditions outputs for readable spot checks alongside the matrix tests below.
    Two pins were changed on purpose by SUP-845 (marked inline); any other change is a regression.
    """

    SNOWFLAKE_MAPPING = {"dataset": "TABLE_SCHEMA", "table_name": "TABLE_NAME"}
    REDSHIFT_MAPPING = {"project": '"database"', "dataset": '"schema"'}

    CASES: List[Tuple[List[MetadataFilter], FilterEffectType, Dict, Optional[str], str]] = [
        (
            [MetadataFilter(project="db1", dataset="s1", effect=_BLOCK)],
            _ALLOW,
            SNOWFLAKE_MAPPING,
            "db1",
            "(NOT(LOWER(TABLE_SCHEMA)='s1'))",
        ),
        (
            [
                MetadataFilter(
                    project="db1",
                    dataset="s1",
                    table_name="(int_.*|_intermediate.*)",
                    type=FilterType.REGEXP,
                    effect=_BLOCK,
                )
            ],
            _ALLOW,
            SNOWFLAKE_MAPPING,
            "db1",
            "(NOT(LOWER(TABLE_SCHEMA)='s1' AND "
            "LOWER(TABLE_NAME) REGEXP '^((int_.*|_intermediate.*))$'))",
        ),
        (
            # SUP-845 intended change: was "(NOT(LOWER(TABLE_SCHEMA)='s1'))", which excluded the
            # whole schema because table_type has no column in this mapping.
            [MetadataFilter(project="db1", dataset="s1", table_type="VIEW", effect=_BLOCK)],
            _ALLOW,
            SNOWFLAKE_MAPPING,
            "db1",
            "(1=1)",
        ),
        (
            [
                MetadataFilter(project="db1", dataset="s1", effect=_ALLOW),
                MetadataFilter(project="db1", dataset="s", type=FilterType.PREFIX, effect=_BLOCK),
            ],
            _ALLOW,
            SNOWFLAKE_MAPPING,
            "db1",
            "(((LOWER(TABLE_SCHEMA)='s1')) OR (NOT(LOWER(TABLE_SCHEMA) LIKE 's%')))",
        ),
        (
            # SUP-845 intended change: was "(NOT(LOWER(\"database\")='db1' AND
            # LOWER(\"schema\")='s1'))", which excluded the whole schema because table_name has
            # no column in this mapping.
            [MetadataFilter(project="db1", dataset="s1", table_name="t1", effect=_BLOCK)],
            _ALLOW,
            REDSHIFT_MAPPING,
            None,
            "(1=1)",
        ),
        (
            [MetadataFilter(project="db1", dataset="s1", effect=_ALLOW)],
            _BLOCK,
            REDSHIFT_MAPPING,
            None,
            "((LOWER(\"database\")='db1' AND LOWER(\"schema\")='s1'))",
        ),
    ]

    def test_sql_conditions_unchanged(self):
        for filters, default_effect, mapping, project, expected in self.CASES:
            container = MetadataFiltersContainer(
                metadata_filters=MetadataAllowBlockList(
                    filters=filters, default_effect=default_effect
                )
            )
            self.assertEqual(
                expected,
                container.get_sql_conditions(mapping, _sql_encoder, project=project),
                msg=f"filters={filters} mapping={mapping} project={project}",
            )


def _without_finer_block_rules(
    filters: MetadataAllowBlockList, kwargs: Dict
) -> MetadataAllowBlockList:
    """The rule set with only the BLOCK rules that can't be evaluated for the lookup removed."""
    return MetadataAllowBlockList(
        filters=[f for f in filters.filters if not _is_unevaluable_block_rule(f, kwargs)],
        default_effect=filters.default_effect,
    )


def _without_project_level_table_block_rules(
    filters: MetadataAllowBlockList,
) -> MetadataAllowBlockList:
    reduced = MetadataAllowBlockList(
        filters=[
            f
            for f in filters.filters
            if not (
                f.effect == _BLOCK
                and not f.dataset
                and (f.table_name is not None or f.table_type is not None)
            )
        ],
        default_effect=filters.default_effect,
    )
    return reduced


class TestFinerBlockRulesAreTheOnlyChange(TestCase):
    """
    SUP-845 specification over the same matrix, including mixed rule sets: the result must equal
    the frozen v0.12.459 result after removing only the BLOCK rules that target a level finer than
    the lookup. Every other rule in the set keeps its exact effect.
    """

    RULE_SETS = _rule_sets()
    LOOKUPS = _lookups()

    def test_element_checks_ignore_only_finer_block_rules(self):
        changed = 0
        for filters in self.RULE_SETS:
            container = MetadataFiltersContainer(metadata_filters=filters)
            for kwargs in self.LOOKUPS:
                expected = _legacy_effect(_without_finer_block_rules(filters, kwargs), kwargs)
                if expected != _legacy_effect(filters, kwargs):
                    changed += 1
                self.assertEqual(
                    expected == _ALLOW,
                    container.is_metadata_element_allowed(**kwargs),
                    msg=f"filters={filters} lookup={kwargs}",
                )
        # The bug cases exist in the matrix, so some results must differ from v0.12.459.
        self.assertGreater(changed, 0)

    def test_expensive_collection_checks_ignore_only_finer_block_rules(self):
        for filters in self.RULE_SETS:
            container = MetadataFiltersContainer(expensive_collection_filters=filters)
            for kwargs in self.LOOKUPS:
                expected = not filters.filters or (
                    _legacy_effect(_without_finer_block_rules(filters, kwargs), kwargs) == _ALLOW
                )
                self.assertEqual(
                    expected,
                    container.is_expensive_collection_allowed(**kwargs),
                    msg=f"filters={filters} lookup={kwargs}",
                )

    def test_whole_project_blocked_ignores_only_table_block_rules(self):
        for filters in self.RULE_SETS:
            container = MetadataFiltersContainer(metadata_filters=filters)
            reduced = _without_project_level_table_block_rules(filters)
            for project in _PROJECTS:
                self.assertEqual(
                    _legacy_whole_project_blocked(reduced, project),
                    container.is_whole_project_blocked(project),
                    msg=f"filters={filters} project={project}",
                )


# --- SQL path -----------------------------------------------------------------------------------


def _legacy_sql_field_condition(f: MetadataFilter, column_mapping: Dict[str, str]) -> str:
    # Frozen copy of MetadataFiltersContainer._get_sql_field_condition (v0.12.459), lowercase on.
    conditions = " AND ".join(
        _sql_encoder(
            f"LOWER({column})",
            getattr(f, name).lower(),
            f.type if name == f.filter_type_target_field() else FilterType.EXACT_MATCH,
        )
        for (name, column) in column_mapping.items()
        if getattr(f, name) is not None
    )
    if not conditions:
        return ""
    return f"NOT({conditions})" if f.effect == _BLOCK else f"({conditions})"


def _legacy_sql_conditions(
    filters: MetadataAllowBlockList,
    column_mapping: Dict[str, str],
    project: Optional[str],
    skip_project_guard: bool = False,
) -> Optional[str]:
    # Frozen copy of MetadataFiltersContainer.get_sql_conditions (v0.12.459).
    # skip_project_guard lets the spec evaluate a reduced rule set after the guard was already
    # decided on the full set.
    if not filters.filters:
        return None
    if (
        not skip_project_guard
        and project
        and not any(
            _legacy_matches(f, {"project": project}) and f.dataset is not None
            for f in filters.filters
        )
    ):
        return None

    def project_condition(f: MetadataFilter) -> bool:
        return not project or _legacy_matches(f, {"project": project})

    default_op = " OR " if filters.default_effect == _ALLOW else " AND "
    other_op = " AND " if filters.default_effect == _ALLOW else " OR "
    default_conditions = default_op.join(
        _legacy_sql_field_condition(f, column_mapping)
        for f in filters.get_default_effect_rules(condition=project_condition)
    )
    other_conditions = other_op.join(
        _legacy_sql_field_condition(f, column_mapping)
        for f in filters.get_other_effect_rules(condition=project_condition)
    )
    if default_conditions and other_conditions:
        return f"(({default_conditions}){default_op}({other_conditions}))"
    if default_conditions:
        return f"({default_conditions})"
    if other_conditions:
        return f"({other_conditions})"
    return None


# Column mappings modelled on data-collector's callers: (mapping, called with a project?).
_SQL_MAPPINGS: List[Tuple[Dict[str, str], bool]] = [
    ({"dataset": "TABLE_SCHEMA", "table_name": "TABLE_NAME"}, True),  # Snowflake tables query
    ({"project": '"database"', "dataset": '"schema"'}, False),  # Redshift
    ({"dataset": '"schemaname"'}, True),  # Redshift per-database views
    ({"dataset": "DBS.NAME"}, True),  # hive_mysql
    ({"project": "db", "dataset": "sch", "table_name": "tbl"}, False),  # every column mapped
]


def _sql_lookups() -> List[Tuple[Dict[str, str], Optional[str]]]:
    lookups: List[Tuple[Dict[str, str], Optional[str]]] = []
    for mapping, with_project in _SQL_MAPPINGS:
        projects: List[Optional[str]] = list(_PROJECTS) if with_project else [None]
        lookups += [(mapping, project) for project in projects]
    return lookups


def _inexpressible_block_rules(
    filters: MetadataAllowBlockList, column_mapping: Dict[str, str], project: Optional[str]
) -> List[MetadataFilter]:
    """
    BLOCK rules (relevant to the project) with a condition on an unmapped attribute at or below
    the finest mapped level, i.e. a part the SQL can't express (missing coarser columns are fine).
    """
    return [
        f
        for f in filters.filters
        if (not project or _legacy_matches(f, {"project": project}))
        and _is_unevaluable_block_rule(f, column_mapping)
    ]


class TestMetadataFilterSqlMatrixBehaviourLock(TestCase):
    """
    get_sql_conditions must return exactly the v0.12.459 SQL wherever no relevant BLOCK rule has
    a part the column mapping can't express.
    """

    RULE_SETS = _rule_sets()
    LOOKUPS = _sql_lookups()

    def test_sql_unchanged_when_every_block_rule_is_expressible(self):
        compared = 0
        for filters in self.RULE_SETS:
            container = MetadataFiltersContainer(metadata_filters=filters)
            for mapping, project in self.LOOKUPS:
                if _inexpressible_block_rules(filters, mapping, project):
                    continue
                compared += 1
                self.assertEqual(
                    _legacy_sql_conditions(filters, mapping, project),
                    container.get_sql_conditions(mapping, _sql_encoder, project=project),
                    msg=f"filters={filters} mapping={mapping} project={project}",
                )
        self.assertGreater(compared, 5000)


class TestInexpressibleBlockRulesAreTheOnlySqlChange(TestCase):
    """
    SUP-845 SQL specification: the SQL must equal v0.12.459 with only the inexpressible BLOCK
    rules removed. Where v0.12.459 returned a condition and that removal leaves none, an
    always-true (default ALLOW) or always-false (default BLOCK) condition is returned so callers
    that concatenate the result into a query still get valid SQL. The up-front None returns are
    kept: no filters, or no dataset rule for the project (callers check
    is_project_with_datasets_filtered first).
    """

    RULE_SETS = _rule_sets()
    LOOKUPS = _sql_lookups()

    def test_sql_ignores_only_inexpressible_block_rules(self):
        changed = 0
        for filters in self.RULE_SETS:
            container = MetadataFiltersContainer(metadata_filters=filters)
            for mapping, project in self.LOOKUPS:
                removed = _inexpressible_block_rules(filters, mapping, project)
                reduced = MetadataAllowBlockList(
                    filters=[f for f in filters.filters if f not in removed],
                    default_effect=filters.default_effect,
                )
                returns_none_up_front = not filters.filters or bool(
                    project
                    and not any(
                        _legacy_matches(f, {"project": project}) and f.dataset is not None
                        for f in filters.filters
                    )
                )
                expected = (
                    None
                    if returns_none_up_front
                    else _legacy_sql_conditions(reduced, mapping, project, skip_project_guard=True)
                )
                if removed and expected is None and not returns_none_up_front:
                    expected = "(1=1)" if filters.default_effect == _ALLOW else "(1=0)"
                if expected != _legacy_sql_conditions(filters, mapping, project):
                    changed += 1
                self.assertEqual(
                    expected,
                    container.get_sql_conditions(mapping, _sql_encoder, project=project),
                    msg=f"filters={filters} mapping={mapping} project={project}",
                )
        self.assertGreater(changed, 0)
