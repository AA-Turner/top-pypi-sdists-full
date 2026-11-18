from dataclasses import dataclass
from typing import List, Optional
from unittest import TestCase

from pycarlo.features.metadata import (
    FilterEffectType,
    FilterType,
    MetadataAllowBlockList,
    MetadataFilter,
    MetadataFiltersContainer,
)


@dataclass
class DatasetEntry:
    project: str
    dataset: str


def _redshift_encoder(column: str, value: str, type: FilterType) -> str:
    if type == FilterType.REGEXP:
        op = "~"
        encoded_value = f"'^({value})$'"
    elif type == FilterType.PREFIX:
        op = " LIKE "
        encoded_value = f"'{value}%'"
    elif type == FilterType.SUFFIX:
        op = " LIKE "
        encoded_value = f"'%{value}'"
    elif type == FilterType.SUBSTRING:
        op = " LIKE "
        encoded_value = f"'%{value}%'"
    else:
        op = "="
        encoded_value = f"'{value}'"
    return f"{column}{op}{encoded_value}"


class TestDatasetFiltering(TestCase):
    DATASETS = [
        DatasetEntry("project_1", "dataset_1"),
        DatasetEntry("project_1", "dataset_2"),
        DatasetEntry("project_1", "dataset_3"),
        DatasetEntry("project_2", "dataset_1"),
        DatasetEntry("project_2", "dataset_2"),
        DatasetEntry("project_2", "dataset_3"),
        DatasetEntry("project_2", "dataset_4"),
    ]
    DATASETS_FOR_REGEXP = [
        DatasetEntry("project_1", "dataset_1"),
        DatasetEntry("project_1", "dataset_2"),
        DatasetEntry("project_2", "dataset_1"),
        DatasetEntry("project_2", "ds_2"),
        DatasetEntry("prj_3", "ds_1"),
        DatasetEntry("prj_3", "ds_2"),
        DatasetEntry("prj_3", "ds_3"),
        DatasetEntry("prj_3", "foobar_1"),
        DatasetEntry("prj_3", "foobar_3"),
    ]
    DATASETS_FOR_PREFIX = [
        DatasetEntry("project", "ds_1"),
        DatasetEntry("project", "ds_2"),
        *DATASETS_FOR_REGEXP,
    ]

    def test_block_single_dataset(self):
        # excludes only project_1.dataset_2
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_1", dataset="dataset_2", effect=FilterEffectType.BLOCK
                ),
            ]
        )
        self._validate_blocked_datasets(
            filters, [DatasetEntry(project="project_1", dataset="dataset_2")]
        )

    def test_block_multi_datasets(self):
        # excludes project_1.dataset_3 and project_2.dataset_1
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_1", dataset="dataset_3", effect=FilterEffectType.BLOCK
                ),
                MetadataFilter(
                    project="project_2", dataset="dataset_1", effect=FilterEffectType.BLOCK
                ),
            ]
        )
        limits = self._validate_blocked_datasets(
            filters,
            [
                DatasetEntry(project="project_1", dataset="dataset_3"),
                DatasetEntry(project="project_2", dataset="dataset_1"),
            ],
        )
        self.assertFalse(limits.is_whole_project_blocked("project_1"))
        self.assertFalse(limits.is_whole_project_blocked("project_2"))

    def test_block_single_project(self):
        # excludes all datasets in project_1
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(project="project_1", effect=FilterEffectType.BLOCK),
            ]
        )
        blocked = list(filter(lambda d: d.project == "project_1", self.DATASETS))
        limits = self._validate_blocked_datasets(filters, blocked)
        self.assertTrue(limits.is_whole_project_blocked("project_1"))
        self.assertFalse(limits.is_whole_project_blocked("project_2"))

    def test_block_second_project(self):
        # excludes all datasets in project_2
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(project="project_2", effect=FilterEffectType.BLOCK),
            ]
        )
        blocked = list(filter(lambda d: d.project == "project_2", self.DATASETS))
        limits = self._validate_blocked_datasets(filters, blocked)
        self.assertFalse(limits.is_whole_project_blocked("project_1"))
        self.assertTrue(limits.is_whole_project_blocked("project_2"))

    def test_block_single_project_regexp(self):
        # excludes all datasets in prj_3
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="prj_.*", type=FilterType.REGEXP, effect=FilterEffectType.BLOCK
                ),
            ]
        )
        blocked = list(filter(lambda d: d.project.startswith("prj_"), self.DATASETS_FOR_REGEXP))
        limits = self._validate_blocked_datasets(filters, blocked)
        self.assertFalse(limits.is_whole_project_blocked("project_1"))
        self.assertFalse(limits.is_whole_project_blocked("project_2"))
        self.assertTrue(limits.is_whole_project_blocked("prj_3"))

    def test_block_datasets_prefix(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project",
                    dataset="ds_",
                    type=FilterType.PREFIX,
                    effect=FilterEffectType.BLOCK,
                ),
                MetadataFilter(
                    project="prj_3",
                    dataset="ds_",
                    type=FilterType.PREFIX,
                    effect=FilterEffectType.BLOCK,
                ),
            ]
        )
        self._validate_dataset_prefix(filters)

    def test_block_datasets_suffix(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_2",
                    dataset="_2",
                    type=FilterType.SUFFIX,
                    effect=FilterEffectType.BLOCK,
                ),
                MetadataFilter(
                    project="prj_3",
                    dataset="_2",
                    type=FilterType.SUFFIX,
                    effect=FilterEffectType.BLOCK,
                ),
            ]
        )
        self._validate_dataset_suffix(filters)

    def test_block_datasets_substring(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="prj_3",
                    dataset="bar",
                    type=FilterType.SUBSTRING,
                    effect=FilterEffectType.BLOCK,
                ),
            ]
        )
        self._validate_dataset_substring(filters)

    def _validate_dataset_prefix(self, filters: MetadataAllowBlockList):
        blocked = [
            DatasetEntry("project", "ds_1"),
            DatasetEntry("project", "ds_2"),
            DatasetEntry("prj_3", "ds_1"),
            DatasetEntry("prj_3", "ds_2"),
            DatasetEntry("prj_3", "ds_3"),
        ]
        limits = self._validate_blocked_datasets(
            filters=filters, blocked_datasets=blocked, datasets=self.DATASETS_FOR_PREFIX
        )
        self.assertFalse(limits.is_whole_project_blocked("project_1"))
        self.assertFalse(limits.is_whole_project_blocked("project_2"))
        self.assertFalse(limits.is_whole_project_blocked("prj_3"))
        self.assertFalse(limits.is_whole_project_blocked("new_project"))

        self.assertTrue(limits.is_dataset_allowed("project_2", "dataset_1"))
        self.assertFalse(limits.is_dataset_allowed("project", "ds_1"))
        self.assertFalse(limits.is_dataset_allowed("project", "ds_2"))
        self.assertFalse(limits.is_dataset_allowed("prj_3", "ds_1"))
        self.assertFalse(limits.is_dataset_allowed("prj_3", "ds_2"))

    def _validate_dataset_suffix(self, filters: MetadataAllowBlockList):
        blocked = list(filter(lambda d: d.dataset.endswith("ds_2"), self.DATASETS_FOR_REGEXP))
        limits = self._validate_blocked_datasets(
            filters=filters, blocked_datasets=blocked, datasets=self.DATASETS_FOR_REGEXP
        )
        self.assertFalse(limits.is_whole_project_blocked("project_1"))
        self.assertFalse(limits.is_whole_project_blocked("project_2"))
        self.assertFalse(limits.is_whole_project_blocked("prj_3"))
        self.assertFalse(limits.is_whole_project_blocked("new_project"))

        self.assertTrue(limits.is_dataset_allowed("project_2", "dataset_1"))
        self.assertFalse(limits.is_dataset_allowed("project_2", "ds_2"))
        self.assertTrue(limits.is_dataset_allowed("prj_3", "ds_1"))
        self.assertFalse(limits.is_dataset_allowed("prj_3", "ds_2"))
        self.assertTrue(limits.is_dataset_allowed("prj_3", "ds_3"))

    def _validate_dataset_substring(self, filters: MetadataAllowBlockList):
        blocked = list(filter(lambda d: "bar" in d.dataset, self.DATASETS_FOR_REGEXP))
        limits = self._validate_blocked_datasets(
            filters=filters, blocked_datasets=blocked, datasets=self.DATASETS_FOR_REGEXP
        )

        self.assertFalse(limits.is_whole_project_blocked("project_1"))
        self.assertFalse(limits.is_whole_project_blocked("project_2"))
        self.assertFalse(limits.is_whole_project_blocked("prj_3"))
        self.assertFalse(limits.is_whole_project_blocked("new_project"))

        self.assertTrue(limits.is_dataset_allowed("project_2", "dataset_1"))
        self.assertTrue(limits.is_dataset_allowed("project_2", "ds_2"))
        self.assertTrue(limits.is_dataset_allowed("prj_3", "ds_1"))
        self.assertTrue(limits.is_dataset_allowed("prj_3", "ds_2"))
        self.assertTrue(limits.is_dataset_allowed("prj_3", "ds_3"))
        self.assertFalse(limits.is_dataset_allowed("prj_3", "foobar_1"))
        self.assertFalse(limits.is_dataset_allowed("prj_3", "foobar_3"))

    def test_no_filters(self):
        expected_datasets = self.DATASETS.copy()
        filtered_datasets = self._filter_datasets(self.DATASETS, MetadataFiltersContainer())
        self.assertEqual(expected_datasets, filtered_datasets)

    def test_allow_single_dataset(self):
        # excludes all datasets in project_1
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_2", dataset="dataset_4", effect=FilterEffectType.ALLOW
                )
            ],
            default_effect=FilterEffectType.BLOCK,
        )
        limits = self._validate_allowed_datasets(
            filters, [DatasetEntry(project="project_2", dataset="dataset_4")]
        )

        self.assertTrue(limits.is_whole_project_blocked("project_1"))
        self.assertFalse(limits.is_whole_project_blocked("project_2"))

    def test_allow_second_project(self):
        # excludes all datasets in project_1
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(project="project_2", effect=FilterEffectType.ALLOW),
            ],
            default_effect=FilterEffectType.BLOCK,
        )
        allowed = list(filter(lambda d: d.project == "project_2", self.DATASETS))
        limits = self._validate_allowed_datasets(filters, allowed)

        self.assertTrue(limits.is_whole_project_blocked("project_1"))
        self.assertFalse(limits.is_whole_project_blocked("project_2"))

    def test_sql_query_block_single_project(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(project="project_2", effect=FilterEffectType.BLOCK),
            ]
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertTrue(limits.is_metadata_filtered)

        conditions = limits.get_sql_conditions(
            {"project": "database", "dataset": "schema"}, _redshift_encoder
        )
        self.assertEqual("(NOT(LOWER(database)='project_2'))", conditions)

    def test_sql_query_block_project_prefix(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="prj_", type=FilterType.PREFIX, effect=FilterEffectType.BLOCK
                ),
            ]
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertTrue(limits.is_metadata_filtered)

        conditions = limits.get_sql_conditions(
            {"project": "database", "dataset": "schema"}, _redshift_encoder
        )
        self.assertEqual("(NOT(LOWER(database) LIKE 'prj_%'))", conditions)

    def test_sql_query_block_project_dataset_prefix(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_name",
                    dataset="ds_",
                    type=FilterType.PREFIX,
                    effect=FilterEffectType.BLOCK,
                ),
            ]
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertTrue(limits.is_metadata_filtered)

        conditions = limits.get_sql_conditions(
            {"project": "database", "dataset": "schema"}, _redshift_encoder
        )
        self.assertEqual(
            "(NOT(LOWER(database)='project_name' AND LOWER(schema) LIKE 'ds_%'))", conditions
        )

    def test_sql_query_block_single_dataset(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_2", dataset="dataset_1", effect=FilterEffectType.BLOCK
                ),
            ]
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions(
            {"project": "database", "dataset": "schema"}, _redshift_encoder
        )
        self.assertEqual(
            "(NOT(LOWER(database)='project_2' AND LOWER(schema)='dataset_1'))", conditions
        )

    def test_sql_query_block_single_project_case_sensitive(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="PROJECT_2", dataset="dataset_1", effect=FilterEffectType.BLOCK
                ),
            ]
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions(
            {"project": "database", "dataset": "schema"}, _redshift_encoder
        )
        self.assertEqual(
            "(NOT(LOWER(database)='project_2' AND LOWER(schema)='dataset_1'))", conditions
        )

    def test_sql_query_block_datasets_regexp(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_2",
                    dataset="dataset_.+",
                    type=FilterType.REGEXP,
                    effect=FilterEffectType.BLOCK,
                ),
            ]
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions(
            {"project": "database", "dataset": "schema"}, _redshift_encoder
        )
        self.assertEqual(
            "(NOT(LOWER(database)='project_2' AND LOWER(schema)~'^(dataset_.+)$'))", conditions
        )

    def test_sql_query_block_datasets_regexp_with_exception(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_2",
                    dataset="dataset_.+",
                    type=FilterType.REGEXP,
                    effect=FilterEffectType.BLOCK,
                ),
                MetadataFilter(
                    project="project_2", dataset="dataset_10", effect=FilterEffectType.ALLOW
                ),
            ]
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions(
            {"project": "database", "dataset": "schema"}, _redshift_encoder
        )
        self.assertEqual(
            "(((LOWER(database)='project_2' AND LOWER(schema)='dataset_10')) OR "
            "(NOT(LOWER(database)='project_2' AND LOWER(schema)~'^(dataset_.+)$')))",
            conditions,
        )

    def test_sql_query_project_block_single_dataset(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_2", dataset="dataset_1", effect=FilterEffectType.BLOCK
                ),
                MetadataFilter(
                    project="project_1", dataset="dataset_2", effect=FilterEffectType.BLOCK
                ),
            ]
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions(
            project="project_2",
            column_mapping={"project": "database", "dataset": "schema"},
            encoder=_redshift_encoder,
        )
        self.assertEqual(
            "(NOT(LOWER(database)='project_2' AND LOWER(schema)='dataset_1'))", conditions
        )

    def test_sql_query_project_block_nothing(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_1", dataset="dataset_2", effect=FilterEffectType.BLOCK
                ),
            ]
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertFalse(limits.is_project_with_datasets_filtered("project_2"))
        conditions = limits.get_sql_conditions(
            project="project_2",
            column_mapping={"project": "database", "dataset": "schema"},
            encoder=_redshift_encoder,
        )
        self.assertIsNone(conditions)

    def test_sql_query_block_multi_datasets(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_2", dataset="dataset_1", effect=FilterEffectType.BLOCK
                ),
                MetadataFilter(
                    project="project_1", dataset="dataset_2", effect=FilterEffectType.BLOCK
                ),
            ]
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions(
            {"project": "database", "dataset": "schema"}, _redshift_encoder
        )
        self.assertEqual(
            "("
            "NOT(LOWER(database)='project_2' AND LOWER(schema)='dataset_1') AND "
            "NOT(LOWER(database)='project_1' AND LOWER(schema)='dataset_2')"
            ")",
            conditions,
        )

    def test_sql_query_allow_multi_datasets(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_2", dataset="dataset_1", effect=FilterEffectType.ALLOW
                ),
                MetadataFilter(
                    project="project_1", dataset="dataset_2", effect=FilterEffectType.ALLOW
                ),
            ],
            default_effect=FilterEffectType.BLOCK,
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions(
            {"project": "database", "dataset": "schema"}, _redshift_encoder
        )
        self.assertEqual(
            "("
            "(LOWER(database)='project_2' AND LOWER(schema)='dataset_1') OR "
            "(LOWER(database)='project_1' AND LOWER(schema)='dataset_2')"
            ")",
            conditions,
        )

    def test_sql_query_block_case_insensitive(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="PROJECT_", effect=FilterEffectType.BLOCK, type=FilterType.PREFIX
                ),
            ]
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertTrue(limits.is_metadata_filtered)

        conditions = limits.get_sql_conditions(
            {"project": "database", "dataset": "schema"}, _redshift_encoder, force_lowercase=False
        )
        self.assertEqual(
            "(NOT(database LIKE 'PROJECT_%'))",
            conditions,
        )

    def test_sql_query_block_datasets_prefix(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_2",
                    dataset="dataset_",
                    type=FilterType.PREFIX,
                    effect=FilterEffectType.BLOCK,
                ),
            ]
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions(
            {"project": "database", "dataset": "schema"}, _redshift_encoder
        )
        self.assertEqual(
            "(NOT(LOWER(database)='project_2' AND LOWER(schema) LIKE 'dataset_%'))", conditions
        )

    def test_sql_query_block_datasets_suffix(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_2",
                    dataset="_2",
                    type=FilterType.SUFFIX,
                    effect=FilterEffectType.BLOCK,
                ),
            ]
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions(
            {"project": "database", "dataset": "schema"}, _redshift_encoder
        )
        self.assertEqual(
            "(NOT(LOWER(database)='project_2' AND LOWER(schema) LIKE '%_2'))", conditions
        )

    def test_sql_query_block_datasets_suffix_without_project(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(dataset="_2", type=FilterType.SUFFIX, effect=FilterEffectType.BLOCK),
            ]
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions(
            {"project": "database", "dataset": "schema"}, _redshift_encoder
        )
        self.assertEqual("(NOT(LOWER(schema) LIKE '%_2'))", conditions)

    def test_sql_query_block_datasets_substring(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_2",
                    dataset="s_2",
                    type=FilterType.SUBSTRING,
                    effect=FilterEffectType.BLOCK,
                ),
            ]
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions(
            {"project": "database", "dataset": "schema"}, _redshift_encoder
        )
        self.assertEqual(
            "(NOT(LOWER(database)='project_2' AND LOWER(schema) LIKE '%s_2%'))", conditions
        )

    def test_sql_block_table_prefix(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_2",
                    dataset="s_2",
                    table_name="tab",
                    type=FilterType.PREFIX,
                    effect=FilterEffectType.BLOCK,
                ),
            ]
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions(
            {"project": "database", "dataset": "schema", "table_name": "table_name"},
            _redshift_encoder,
        )
        self.assertEqual(
            "(NOT(LOWER(database)='project_2' AND LOWER(schema)='s_2' "
            "AND LOWER(table_name) LIKE 'tab%'))",
            conditions,
        )

    def test_whole_project_blocked(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_2", dataset="dataset_1", effect=FilterEffectType.BLOCK
                ),
            ],
            default_effect=FilterEffectType.BLOCK,
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertTrue(limits.is_metadata_blocked)
        self.assertTrue(limits.is_whole_project_blocked("project_2"))

        query = limits.get_sql_conditions(
            {"project": "database", "dataset": "schema"}, _redshift_encoder
        )
        self.assertEqual(query, "(NOT(LOWER(database)='project_2' AND LOWER(schema)='dataset_1'))")

    def test_no_matching_mappings(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(project="allowed_project", effect=FilterEffectType.ALLOW),
            ],
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        query = limits.get_sql_conditions(
            {
                "dataset": "TABLE_SCHEMA",
                "table_name": "TABLE_NAME",
            },
            _redshift_encoder,
        )
        self.assertIsNone(query)

    def test_case_insensitive_comparison_exact_match(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_2", effect=FilterEffectType.BLOCK, type=FilterType.EXACT_MATCH
                ),
            ]
        )

        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertTrue(limits.is_whole_project_blocked("PROJECT_2"))
        self.assertFalse(limits.is_whole_project_blocked("PROJECT_3"))

    def test_case_insensitive_comparison_prefix(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="project_", effect=FilterEffectType.BLOCK, type=FilterType.PREFIX
                ),
            ]
        )

        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertTrue(limits.is_whole_project_blocked("PROJECT_1"))
        self.assertFalse(limits.is_whole_project_blocked("OTHER_PROJECT"))

    def test_case_insensitive_comparison_regex(self):
        filters = MetadataAllowBlockList(
            filters=[
                MetadataFilter(
                    project="[a-z]+_[1-9]+", effect=FilterEffectType.BLOCK, type=FilterType.REGEXP
                ),
            ]
        )

        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertTrue(limits.is_whole_project_blocked("PROJECT_1"))
        self.assertFalse(limits.is_whole_project_blocked("PROJECT_"))

    def _validate_allowed_datasets(
        self,
        filters: MetadataAllowBlockList,
        expected_datasets: List,
        datasets: Optional[List] = None,
    ) -> MetadataFiltersContainer:
        limits = MetadataFiltersContainer(metadata_filters=filters)
        filtered_datasets = self._filter_datasets(datasets or self.DATASETS, limits)
        self.assertEqual(expected_datasets, filtered_datasets)
        return limits

    def _validate_blocked_datasets(
        self,
        filters: MetadataAllowBlockList,
        blocked_datasets: List,
        datasets: Optional[List] = None,
    ) -> MetadataFiltersContainer:
        expected_datasets = list(
            filter(lambda d: d not in blocked_datasets, (datasets or self.DATASETS))
        )
        limits = MetadataFiltersContainer(metadata_filters=filters)
        filtered_datasets = self._filter_datasets(datasets or self.DATASETS, limits)
        self.assertEqual(expected_datasets, filtered_datasets)
        return limits

    @staticmethod
    def _filter_datasets(
        datasets: List[DatasetEntry], limits: MetadataFiltersContainer
    ) -> List[DatasetEntry]:
        return [d for d in datasets if limits.is_dataset_allowed(d.project, d.dataset)]


class TestTableScopedBlockRules(TestCase):
    """
    SUP-845: a BLOCK rule that targets tables (table_name / table_type) must only block the
    matching tables. Checks at schema or database level must not treat it as blocking the whole
    schema or database.
    """

    @staticmethod
    def _container(
        *filters: MetadataFilter, default_effect: FilterEffectType = FilterEffectType.ALLOW
    ) -> MetadataFiltersContainer:
        return MetadataFiltersContainer(
            metadata_filters=MetadataAllowBlockList(
                filters=list(filters), default_effect=default_effect
            )
        )

    def test_table_regexp_block_rule_does_not_block_schema(self):
        # Reproduction from the ticket, as stored by modifyCollectionBlockList (lowercase rule,
        # uppercase Snowflake identifiers).
        container = MetadataFiltersContainer.from_dict(
            {
                "metadata_filters": {
                    "filters": [
                        {
                            "project": "cleansed",
                            "dataset": "accountsdb",
                            "table_name": "(int_.*|_intermediate.*)",
                            "type": "regexp",
                            "effect": "block",
                        }
                    ]
                }
            }
        )
        self.assertTrue(container.is_dataset_allowed(project="CLEANSED", dataset="ACCOUNTSDB"))
        self.assertFalse(container.is_whole_project_blocked("CLEANSED"))
        self.assertTrue(
            container.is_metadata_element_allowed(
                project="CLEANSED", dataset="ACCOUNTSDB", table_name="ORDERS", table_type="TABLE"
            )
        )
        self.assertFalse(
            container.is_metadata_element_allowed(
                project="CLEANSED", dataset="ACCOUNTSDB", table_name="INT_X", table_type="TABLE"
            )
        )
        self.assertFalse(
            container.is_metadata_element_allowed(
                project="CLEANSED", dataset="ACCOUNTSDB", table_name="_INTERMEDIATE_Y"
            )
        )

    def test_table_type_block_rule_does_not_block_schema(self):
        container = self._container(
            MetadataFilter(
                project="db", dataset="s", table_type="VIEW", effect=FilterEffectType.BLOCK
            )
        )
        self.assertTrue(container.is_dataset_allowed(project="db", dataset="s"))
        self.assertFalse(
            container.is_metadata_element_allowed(
                project="db", dataset="s", table_name="v", table_type="VIEW"
            )
        )
        self.assertTrue(
            container.is_metadata_element_allowed(
                project="db", dataset="s", table_name="t", table_type="TABLE"
            )
        )

    def test_table_block_rule_without_dataset_does_not_block_database(self):
        container = self._container(
            MetadataFilter(project="db", table_name="t1", effect=FilterEffectType.BLOCK)
        )
        self.assertFalse(container.is_whole_project_blocked("db"))
        self.assertTrue(container.is_dataset_allowed(project="db", dataset="s"))
        self.assertFalse(
            container.is_metadata_element_allowed(project="db", dataset="s", table_name="t1")
        )
        self.assertTrue(
            container.is_metadata_element_allowed(project="db", dataset="s", table_name="t2")
        )

    def test_table_block_rule_without_project_does_not_block_every_database(self):
        container = self._container(
            MetadataFilter(table_name="tmp_", type=FilterType.PREFIX, effect=FilterEffectType.BLOCK)
        )
        self.assertFalse(container.is_whole_project_blocked("db"))
        self.assertTrue(container.is_dataset_allowed(project="db", dataset="s"))
        self.assertFalse(
            container.is_metadata_element_allowed(project="db", dataset="s", table_name="tmp_1")
        )

    def test_table_block_rule_with_schema_only_lookup(self):
        # Databricks single-catalog path checks schemas without a catalog.
        container = self._container(
            MetadataFilter(dataset="s", table_name="t1", effect=FilterEffectType.BLOCK)
        )
        self.assertTrue(container.is_metadata_element_allowed(dataset="s"))

    def test_schema_block_rule_with_schema_only_lookup_still_blocks(self):
        # Unchanged: a schema rule still applies when the catalog isn't supplied.
        container = self._container(
            MetadataFilter(project="db", dataset="s", effect=FilterEffectType.BLOCK)
        )
        self.assertFalse(container.is_metadata_element_allowed(dataset="s"))

    def test_schema_block_rule_still_blocks_schema_next_to_table_rule(self):
        container = self._container(
            MetadataFilter(project="db", dataset="s1", effect=FilterEffectType.BLOCK),
            MetadataFilter(
                project="db", dataset="s2", table_name="t", effect=FilterEffectType.BLOCK
            ),
        )
        self.assertFalse(container.is_dataset_allowed(project="db", dataset="s1"))
        self.assertTrue(container.is_dataset_allowed(project="db", dataset="s2"))

    def test_default_block_explicit_table_block_does_not_override_schema_allow(self):
        # Block-by-default list: an explicit table block rule must not hide the schema that an
        # allow rule lets through; it should only block its own table.
        container = self._container(
            MetadataFilter(project="db", dataset="s", effect=FilterEffectType.ALLOW),
            MetadataFilter(
                project="db", dataset="s", table_name="t", effect=FilterEffectType.BLOCK
            ),
            default_effect=FilterEffectType.BLOCK,
        )
        self.assertTrue(container.is_dataset_allowed(project="db", dataset="s"))
        self.assertFalse(
            container.is_metadata_element_allowed(project="db", dataset="s", table_name="t")
        )
        self.assertTrue(
            container.is_metadata_element_allowed(project="db", dataset="s", table_name="other")
        )

    def test_default_block_table_allow_rule_still_lets_schema_through(self):
        # Unchanged: allow rules stay permissive at coarser levels.
        container = self._container(
            MetadataFilter(
                project="db", dataset="s", table_name="t", effect=FilterEffectType.ALLOW
            ),
            default_effect=FilterEffectType.BLOCK,
        )
        self.assertFalse(container.is_whole_project_blocked("db"))
        self.assertTrue(container.is_dataset_allowed(project="db", dataset="s"))
        self.assertTrue(
            container.is_metadata_element_allowed(project="db", dataset="s", table_name="t")
        )
        self.assertFalse(
            container.is_metadata_element_allowed(project="db", dataset="s", table_name="other")
        )
        self.assertFalse(container.is_dataset_allowed(project="db", dataset="other"))

    def test_expensive_collection_table_block_rule_does_not_block_schema(self):
        container = MetadataFiltersContainer(
            expensive_collection_filters=MetadataAllowBlockList(
                filters=[
                    MetadataFilter(
                        project="db", dataset="s", table_name="t", effect=FilterEffectType.BLOCK
                    )
                ]
            )
        )
        self.assertTrue(container.is_expensive_collection_allowed(project="db", dataset="s"))
        self.assertFalse(
            container.is_expensive_collection_allowed(project="db", dataset="s", table_name="t")
        )

    def test_table_type_block_rule_ignored_when_lookup_has_no_table_type(self):
        # Databricks' expensive-collection check passes table_name but not table_type; a
        # table_type rule can't be evaluated there and must not block every table.
        container = MetadataFiltersContainer(
            expensive_collection_filters=MetadataAllowBlockList(
                filters=[MetadataFilter(table_type="EXTERNAL", effect=FilterEffectType.BLOCK)]
            )
        )
        self.assertTrue(
            container.is_expensive_collection_allowed(project="db", dataset="s", table_name="t")
        )
        self.assertFalse(
            container.is_expensive_collection_allowed(
                project="db", dataset="s", table_name="t", table_type="EXTERNAL"
            )
        )

    def test_table_type_metadata_rule_ignored_when_lookup_has_no_table_type(self):
        container = self._container(
            MetadataFilter(
                project="db", dataset="s", table_type="VIEW", effect=FilterEffectType.BLOCK
            )
        )
        self.assertTrue(
            container.is_metadata_element_allowed(project="db", dataset="s", table_name="v")
        )
        self.assertFalse(
            container.is_metadata_element_allowed(
                project="db", dataset="s", table_name="v", table_type="VIEW"
            )
        )

    def test_table_name_block_rule_still_applies_when_table_type_also_passed(self):
        # Unchanged: a table_name rule is evaluable whenever table_name is supplied.
        container = self._container(
            MetadataFilter(project="db", dataset="s", table_name="t", effect=FilterEffectType.BLOCK)
        )
        self.assertFalse(
            container.is_metadata_element_allowed(
                project="db", dataset="s", table_name="t", table_type="TABLE"
            )
        )


class TestTableScopedBlockRulesSql(TestCase):
    """
    SUP-845: get_sql_conditions must not turn a BLOCK rule into a whole-schema exclusion when the
    column mapping can't express its table part (no table_name / table_type column).
    """

    REDSHIFT_MAPPING = {"project": '"database"', "dataset": '"schema"'}
    SNOWFLAKE_SCHEMA_MAPPING = {"dataset": "TABLE_SCHEMA", "table_name": "TABLE_NAME"}
    HIVE_MAPPING = {"dataset": "DBS.NAME"}

    @staticmethod
    def _container(
        *filters: MetadataFilter, default_effect: FilterEffectType = FilterEffectType.ALLOW
    ) -> MetadataFiltersContainer:
        return MetadataFiltersContainer(
            metadata_filters=MetadataAllowBlockList(
                filters=list(filters), default_effect=default_effect
            )
        )

    def test_redshift_table_block_rule_does_not_exclude_schema(self):
        container = self._container(
            MetadataFilter(project="db", dataset="s", table_name="t", effect=FilterEffectType.BLOCK)
        )
        self.assertEqual(
            "(1=1)", container.get_sql_conditions(self.REDSHIFT_MAPPING, _redshift_encoder)
        )

    def test_redshift_schema_rule_kept_next_to_table_rule(self):
        container = self._container(
            MetadataFilter(project="db", dataset="s1", effect=FilterEffectType.BLOCK),
            MetadataFilter(
                project="db", dataset="s2", table_name="t", effect=FilterEffectType.BLOCK
            ),
        )
        self.assertEqual(
            "(NOT(LOWER(\"database\")='db' AND LOWER(\"schema\")='s1'))",
            container.get_sql_conditions(self.REDSHIFT_MAPPING, _redshift_encoder),
        )

    def test_hive_table_block_rule_does_not_exclude_schema(self):
        container = self._container(
            MetadataFilter(
                project="cat", dataset="s", table_name="t", effect=FilterEffectType.BLOCK
            )
        )
        self.assertEqual(
            "(1=1)",
            container.get_sql_conditions(self.HIVE_MAPPING, _redshift_encoder, project="cat"),
        )

    def test_snowflake_table_type_block_rule_does_not_exclude_schema(self):
        container = self._container(
            MetadataFilter(
                project="db", dataset="s", table_type="VIEW", effect=FilterEffectType.BLOCK
            )
        )
        self.assertEqual(
            "(1=1)",
            container.get_sql_conditions(
                self.SNOWFLAKE_SCHEMA_MAPPING, _redshift_encoder, project="db"
            ),
        )

    def test_snowflake_table_name_block_rule_unchanged(self):
        # Already correct: the table_name column is mapped, so the rule is expressed per table.
        container = self._container(
            MetadataFilter(
                project="db",
                dataset="s",
                table_name="int_",
                type=FilterType.PREFIX,
                effect=FilterEffectType.BLOCK,
            )
        )
        self.assertEqual(
            "(NOT(LOWER(TABLE_SCHEMA)='s' AND LOWER(TABLE_NAME) LIKE 'int_%'))",
            container.get_sql_conditions(
                self.SNOWFLAKE_SCHEMA_MAPPING, _redshift_encoder, project="db"
            ),
        )

    def test_table_allow_rule_unchanged(self):
        # ALLOW rules stay permissive: the table part is dropped and the schema is allowed.
        container = self._container(
            MetadataFilter(
                project="db", dataset="s", table_name="t", effect=FilterEffectType.ALLOW
            ),
            default_effect=FilterEffectType.BLOCK,
        )
        self.assertEqual(
            "((LOWER(\"database\")='db' AND LOWER(\"schema\")='s'))",
            container.get_sql_conditions(self.REDSHIFT_MAPPING, _redshift_encoder),
        )

    def test_default_block_table_block_rule_does_not_hide_allowed_schema(self):
        container = self._container(
            MetadataFilter(project="db", dataset="s", effect=FilterEffectType.ALLOW),
            MetadataFilter(
                project="db", dataset="s", table_name="t", effect=FilterEffectType.BLOCK
            ),
            default_effect=FilterEffectType.BLOCK,
        )
        self.assertEqual(
            "((LOWER(\"database\")='db' AND LOWER(\"schema\")='s'))",
            container.get_sql_conditions(self.REDSHIFT_MAPPING, _redshift_encoder),
        )

    def test_no_rules_for_project_still_returns_none(self):
        # Unchanged: callers check is_project_with_datasets_filtered before using the result.
        container = self._container(
            MetadataFilter(project="db", dataset="s", table_name="t", effect=FilterEffectType.BLOCK)
        )
        self.assertIsNone(
            container.get_sql_conditions(self.HIVE_MAPPING, _redshift_encoder, project="other")
        )

    def test_default_block_inexpressible_rules_return_always_false(self):
        # Block-by-default list whose only rules can't be expressed: nothing is allowed, and the
        # result is still valid SQL for callers that concatenate it.
        container = self._container(
            MetadataFilter(
                project="db", dataset="s", table_name="t", effect=FilterEffectType.BLOCK
            ),
            default_effect=FilterEffectType.BLOCK,
        )
        self.assertEqual(
            "(1=0)", container.get_sql_conditions(self.REDSHIFT_MAPPING, _redshift_encoder)
        )

    def test_inexpressible_rule_for_another_project_does_not_add_fallback(self):
        # Only rules relevant to the requested project count: the db1 schema rule is kept as-is
        # and the db2 table rule doesn't turn the result into (1=1).
        container = self._container(
            MetadataFilter(project="db1", dataset="s1", effect=FilterEffectType.BLOCK),
            MetadataFilter(
                project="db2", dataset="s2", table_name="t", effect=FilterEffectType.BLOCK
            ),
        )
        self.assertEqual(
            "(NOT(LOWER(DBS.NAME)='s1'))",
            container.get_sql_conditions(self.HIVE_MAPPING, _redshift_encoder, project="db1"),
        )
