import json
from unittest import TestCase

from pycarlo.features.metadata import (
    FilterEffectType,
    FilterType,
    MetadataAllowBlockList,
    MetadataFilter,
    MetadataFiltersContainer,
)


class TestExpensiveCollectionFilters(TestCase):
    def test_empty_filters_defaults_to_allow(self):
        container = MetadataFiltersContainer()
        self.assertFalse(container.is_expensive_collection_filtered)
        self.assertTrue(
            container.is_expensive_collection_allowed(project="prj_1", dataset="ds_1", table="t_1")
        )

    def test_block_specific_table(self):
        container = MetadataFiltersContainer(
            expensive_collection_filters=MetadataAllowBlockList(
                filters=[
                    MetadataFilter(
                        project="prj_1",
                        dataset="ds_1",
                        table_name="t_audit",
                        effect=FilterEffectType.BLOCK,
                    ),
                ]
            )
        )
        self.assertTrue(container.is_expensive_collection_filtered)
        self.assertFalse(
            container.is_expensive_collection_allowed(
                project="prj_1", dataset="ds_1", table_name="t_audit"
            )
        )
        self.assertTrue(
            container.is_expensive_collection_allowed(
                project="prj_1", dataset="ds_1", table_name="t_orders"
            )
        )

    def test_block_whole_dataset(self):
        container = MetadataFiltersContainer(
            expensive_collection_filters=MetadataAllowBlockList(
                filters=[
                    MetadataFilter(
                        project="prj_1", dataset="ds_archive", effect=FilterEffectType.BLOCK
                    ),
                ]
            )
        )
        self.assertFalse(
            container.is_expensive_collection_allowed(
                project="prj_1", dataset="ds_archive", table_name="any_table"
            )
        )
        self.assertTrue(
            container.is_expensive_collection_allowed(
                project="prj_1", dataset="ds_active", table_name="any_table"
            )
        )

    def test_block_by_prefix(self):
        container = MetadataFiltersContainer(
            expensive_collection_filters=MetadataAllowBlockList(
                filters=[
                    MetadataFilter(
                        project="prj_1",
                        dataset="ds_1",
                        table_name="tmp_",
                        type=FilterType.PREFIX,
                        effect=FilterEffectType.BLOCK,
                    ),
                ]
            )
        )
        self.assertFalse(
            container.is_expensive_collection_allowed(
                project="prj_1", dataset="ds_1", table_name="tmp_staging"
            )
        )
        self.assertTrue(
            container.is_expensive_collection_allowed(
                project="prj_1", dataset="ds_1", table_name="orders"
            )
        )

    def test_block_by_regexp(self):
        container = MetadataFiltersContainer(
            expensive_collection_filters=MetadataAllowBlockList(
                filters=[
                    MetadataFilter(
                        project="prj_1",
                        dataset="ds_1",
                        table_name=".*_audit_log",
                        type=FilterType.REGEXP,
                        effect=FilterEffectType.BLOCK,
                    ),
                ]
            )
        )
        self.assertFalse(
            container.is_expensive_collection_allowed(
                project="prj_1", dataset="ds_1", table_name="orders_audit_log"
            )
        )
        self.assertTrue(
            container.is_expensive_collection_allowed(
                project="prj_1", dataset="ds_1", table_name="orders"
            )
        )

    def test_default_block_with_allow_rules(self):
        # Inverted pattern: collect expensive metadata only for explicitly allowed tables.
        container = MetadataFiltersContainer(
            expensive_collection_filters=MetadataAllowBlockList(
                default_effect=FilterEffectType.BLOCK,
                filters=[
                    MetadataFilter(
                        project="prj_1",
                        dataset="ds_critical",
                        effect=FilterEffectType.ALLOW,
                    ),
                ],
            )
        )
        self.assertTrue(
            container.is_expensive_collection_allowed(
                project="prj_1", dataset="ds_critical", table_name="any_table"
            )
        )
        self.assertFalse(
            container.is_expensive_collection_allowed(
                project="prj_1", dataset="ds_other", table_name="any_table"
            )
        )

    def test_case_insensitive(self):
        container = MetadataFiltersContainer(
            expensive_collection_filters=MetadataAllowBlockList(
                filters=[
                    MetadataFilter(
                        project="prj_1",
                        dataset="ds_archive",
                        effect=FilterEffectType.BLOCK,
                    ),
                ]
            )
        )
        self.assertFalse(
            container.is_expensive_collection_allowed(
                project="PRJ_1", dataset="DS_ARCHIVE", table_name="ANY"
            )
        )

    def test_independent_from_metadata_filters(self):
        # A table blocked from expensive collection is still allowed by metadata_filters,
        # and vice versa — the two lists are evaluated independently.
        container = MetadataFiltersContainer(
            metadata_filters=MetadataAllowBlockList(
                filters=[
                    MetadataFilter(
                        project="prj_1", dataset="staging", effect=FilterEffectType.BLOCK
                    ),
                ]
            ),
            expensive_collection_filters=MetadataAllowBlockList(
                filters=[
                    MetadataFilter(
                        project="prj_1", dataset="ds_archive", effect=FilterEffectType.BLOCK
                    ),
                ]
            ),
        )

        # Blocked from metadata collection entirely.
        self.assertFalse(container.is_dataset_allowed("prj_1", "staging"))
        # But not from expensive collection.
        self.assertTrue(
            container.is_expensive_collection_allowed(
                project="prj_1", dataset="staging", table_name="any"
            )
        )

        # Allowed in metadata collection.
        self.assertTrue(container.is_dataset_allowed("prj_1", "ds_archive"))
        # But blocked from expensive collection.
        self.assertFalse(
            container.is_expensive_collection_allowed(
                project="prj_1", dataset="ds_archive", table_name="any"
            )
        )

    def test_existing_jobs_unchanged_when_only_metadata_filters_configured(self):
        # A container with only metadata_filters set behaves identically to today —
        # expensive collection is allowed for every element by default.
        container = MetadataFiltersContainer(
            metadata_filters=MetadataAllowBlockList(
                filters=[
                    MetadataFilter(
                        project="prj_1", dataset="staging", effect=FilterEffectType.BLOCK
                    ),
                ]
            )
        )
        self.assertFalse(container.is_expensive_collection_filtered)
        self.assertTrue(
            container.is_expensive_collection_allowed(
                project="prj_1", dataset="ds_1", table_name="t_1"
            )
        )

    def test_serialization_round_trip(self):
        # Verify the new field round-trips through dataclasses_json serialization,
        # which is how job configs are persisted.
        original = MetadataFiltersContainer(
            expensive_collection_filters=MetadataAllowBlockList(
                filters=[
                    MetadataFilter(
                        project="prj_1",
                        dataset="ds_archive",
                        effect=FilterEffectType.BLOCK,
                    ),
                ]
            )
        )
        as_dict = original.to_dict()
        restored = MetadataFiltersContainer.from_dict(as_dict)
        self.assertTrue(restored.is_expensive_collection_filtered)
        self.assertFalse(
            restored.is_expensive_collection_allowed(
                project="prj_1", dataset="ds_archive", table_name="any"
            )
        )

    def test_deserialization_from_legacy_config(self):
        # A legacy job config that doesn't know about expensive_collection_filters
        # should deserialize cleanly and behave as no-op.
        legacy_config = {
            "metadata_filters": {
                "filters": [{"project": "prj_1", "dataset": "staging", "effect": "block"}],
                "default_effect": "allow",
            }
        }
        container = MetadataFiltersContainer.from_dict(legacy_config)
        self.assertFalse(container.is_expensive_collection_filtered)
        self.assertTrue(
            container.is_expensive_collection_allowed(
                project="prj_1", dataset="ds_1", table_name="t_1"
            )
        )

    def test_table_type_match(self):
        # table_type is part of the supported kwargs; verify it matches.
        container = MetadataFiltersContainer(
            expensive_collection_filters=MetadataAllowBlockList(
                filters=[
                    MetadataFilter(table_type="EXTERNAL", effect=FilterEffectType.BLOCK),
                ]
            )
        )
        self.assertFalse(
            container.is_expensive_collection_allowed(
                project="prj_1", dataset="ds_1", table_name="t_1", table_type="EXTERNAL"
            )
        )
        self.assertTrue(
            container.is_expensive_collection_allowed(
                project="prj_1", dataset="ds_1", table_name="t_1", table_type="MANAGED"
            )
        )

    def test_json_string_round_trip(self):
        # Beyond dict-level round-trip: confirm the JSON representation is stable.
        original = MetadataFiltersContainer(
            expensive_collection_filters=MetadataAllowBlockList(
                filters=[
                    MetadataFilter(
                        project="prj_1",
                        dataset="ds_archive",
                        effect=FilterEffectType.BLOCK,
                    ),
                ]
            )
        )
        as_json = original.to_json()
        # Sanity check the field name made it into the serialized form.
        self.assertIn("expensive_collection_filters", json.loads(as_json))
        restored = MetadataFiltersContainer.from_json(as_json)
        self.assertTrue(restored.is_expensive_collection_filtered)
