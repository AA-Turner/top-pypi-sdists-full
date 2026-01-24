from dataclasses import dataclass
from typing import Any, Dict, List
from unittest import TestCase

from pycarlo.features.metadata import (
    AssetFiltersContainer,
    FilterEffectType,
)


@dataclass
class AssetEntry:
    asset_type: str
    attributes: Dict[str, Any]


class TestAssetFiltering(TestCase):
    ASSETS = [
        AssetEntry("tableau_workbook_v2", {"id": "1", "name": "sales_dashboard"}),
        AssetEntry("tableau_workbook_v2", {"id": "2", "name": "marketing_report"}),
        AssetEntry("tableau_workbook_v2", {"id": "3", "name": "executive_summary"}),
        AssetEntry("jobs", {"id": "1", "name": "data_quality_check"}),
        AssetEntry("jobs", {"id": "2", "name": "scheduled_etl"}),
        AssetEntry("power_bi_workspace", {"id": "1", "name": "analytics_workspace"}),
        AssetEntry("power_bi_workspace", {"id": "2", "name": "finance_dashboard"}),
    ]

    def test_block_single_asset_by_name(self):
        # excludes only tableau_workbook_v2.sales_dashboard
        asset_filters = [
            {
                "asset_type": "tableau_workbook_v2",
                "rules": [
                    {
                        "effect": "block",
                        "conditions": [
                            {
                                "attribute_name": "name",
                                "value": "sales_dashboard",
                            }
                        ],
                    }
                ],
            }
        ]
        self._validate_blocked_assets(asset_filters, [0])

    def test_block_single_asset_by_id(self):
        asset_filters = [
            {
                "asset_type": "tableau_workbook_v2",
                "rules": [
                    {
                        "effect": "block",
                        "conditions": [
                            {
                                "attribute_name": "id",
                                "value": "3",
                            }
                        ],
                    }
                ],
            }
        ]
        self._validate_blocked_assets(asset_filters, [2])

    def test_multiple_conditions_are_anded(self):
        asset_filters = [
            {
                "asset_type": "tableau_workbook_v2",
                "rules": [
                    {
                        "conditions": [
                            {
                                "attribute_name": "name",
                                "value": "sales_dashboard",
                            },
                            {
                                "attribute_name": "id",
                                "value": "3",  # ID does not match name
                            },
                        ],
                    }
                ],
            }
        ]
        self._validate_blocked_assets(asset_filters, [])

    def test_multiple_filters_are_ored(self):
        asset_filters = [
            {
                "asset_type": "tableau_workbook_v2",
                "rules": [
                    {
                        "conditions": [
                            {
                                "attribute_name": "name",
                                "value": "sales_dashboard",
                            },
                        ],
                    },
                    {
                        "conditions": [
                            {
                                "attribute_name": "id",
                                "value": "3",
                            },
                        ],
                    },
                ],
            }
        ]
        self._validate_blocked_assets(asset_filters, [0, 2])

    def test_block_multi_assets(self):
        # excludes tableau_workbook_v2.marketing_report and jobs.data_quality_check
        asset_filters = [
            {
                "asset_type": "tableau_workbook_v2",
                "rules": [
                    {
                        "effect": "block",
                        "conditions": [
                            {
                                "attribute_name": "name",
                                "value": "marketing_report",
                            }
                        ],
                    }
                ],
            },
            {
                "asset_type": "jobs",
                "rules": [
                    {
                        "effect": "block",
                        "conditions": [
                            {
                                "attribute_name": "name",
                                "value": "data_quality_check",
                            }
                        ],
                    }
                ],
            },
        ]
        self._validate_blocked_assets(asset_filters, [1, 3])

    def test_block_single_asset_type(self):
        # excludes all assets of type tableau_workbook_v2
        asset_filters = [
            {
                "asset_type": "tableau_workbook_v2",
                "default_effect": FilterEffectType.BLOCK,
            }
        ]
        self._validate_blocked_assets(asset_filters, [0, 1, 2])

    def test_blocks_exact_match(self):
        asset_filters = [
            {
                "asset_type": "tableau_workbook_v2",
                "rules": [
                    {
                        "conditions": [
                            {
                                "attribute_name": "name",
                                "value": "sales_dashboard",
                            }
                        ],
                    }
                ],
            }
        ]

        limits = AssetFiltersContainer.from_dict(dict(asset_filters=asset_filters))
        self.assertFalse(limits.is_asset_blocked("jobs", {"name": "DATA_QUALITY_CHECK"}))
        self.assertTrue(limits.is_asset_blocked("tableau_workbook_v2", {"name": "sales_dashboard"}))
        self.assertTrue(
            limits.is_asset_blocked("tableau_workbook_v2", {"name": "SALES_DASHBOARD"})
        )  # case-insensitive

    def test_block_assets_prefix(self):
        asset_filters = [
            {
                "asset_type": "tableau_workbook_v2",
                "rules": [
                    {
                        "effect": "block",
                        "conditions": [
                            {
                                "attribute_name": "name",
                                "value": "sales_",
                                "comparison_type": "prefix",
                            }
                        ],
                    }
                ],
            }
        ]

        # Test individual assets
        limits = AssetFiltersContainer.from_dict(dict(asset_filters=asset_filters))
        self.assertFalse(
            limits.is_asset_blocked("tableau_workbook_v2", {"name": "marketing_report"})
        )
        self.assertTrue(limits.is_asset_blocked("tableau_workbook_v2", {"name": "sales_dashboard"}))
        self.assertTrue(limits.is_asset_blocked("tableau_workbook_v2", {"name": "sales_analytics"}))
        self.assertTrue(
            limits.is_asset_blocked("tableau_workbook_v2", {"name": "SALES_ANALYTICS"})
        )  # case-insensitive

    def test_block_assets_suffix(self):
        asset_filters = [
            {
                "asset_type": "jobs",
                "rules": [
                    {
                        "effect": "block",
                        "conditions": [
                            {
                                "attribute_name": "name",
                                "value": "_check",
                                "comparison_type": "suffix",
                            }
                        ],
                    }
                ],
            }
        ]

        # Test individual assets
        limits = AssetFiltersContainer.from_dict(dict(asset_filters=asset_filters))
        self.assertFalse(limits.is_asset_blocked("jobs", {"name": "scheduled_etl"}))
        self.assertTrue(limits.is_asset_blocked("jobs", {"name": "data_quality_check"}))
        self.assertTrue(
            limits.is_asset_blocked("jobs", {"name": "DATA_QUALITY_CHECK"})
        )  # case-insensitive

    def test_block_assets_substring(self):
        asset_filters = [
            {
                "asset_type": "power_bi_workspace",
                "rules": [
                    {
                        "effect": "block",
                        "conditions": [
                            {
                                "attribute_name": "name",
                                "value": "_work",
                                "comparison_type": "substring",
                            }
                        ],
                    }
                ],
            }
        ]

        # Test individual assets
        limits = AssetFiltersContainer.from_dict(dict(asset_filters=asset_filters))
        self.assertFalse(
            limits.is_asset_blocked("power_bi_workspace", {"name": "finance_dashboard"})
        )
        self.assertTrue(
            limits.is_asset_blocked("power_bi_workspace", {"name": "analytics_workspace"})
        )
        self.assertTrue(
            limits.is_asset_blocked("power_bi_workspace", {"name": "ANALYTICS_WORKSPACE"})
        )  # case-insensitive

    def test_block_asset_regex(self):
        # Test regex matching on asset_name only (asset_type always exact match)
        asset_filters = [
            {
                "asset_type": "tableau_workbook_v2",
                "rules": [
                    {
                        "effect": "block",
                        "conditions": [
                            {
                                "attribute_name": "name",
                                "value": "sales_.*",
                                "comparison_type": "regexp",
                            }
                        ],
                    }
                ],
            }
        ]

        # Test individual assets
        limits = AssetFiltersContainer.from_dict(dict(asset_filters=asset_filters))
        self.assertTrue(limits.is_asset_blocked("tableau_workbook_v2", {"name": "sales_dashboard"}))
        self.assertTrue(
            limits.is_asset_blocked("tableau_workbook_v2", {"name": "SALES_DASHBOARD"})
        )  # case-insensitive
        self.assertFalse(
            limits.is_asset_blocked("tableau_workbook_v2", {"name": "marketing_report"})
        )
        self.assertFalse(
            limits.is_asset_blocked("jobs", {"name": "data_quality_check"})
        )  # case-insensitive

    def test_no_filters(self):
        filtered_assets = self._filter_assets(self.ASSETS, AssetFiltersContainer())
        self.assertEqual(self.ASSETS, filtered_assets)

    def test_allow_single_workbook(self):
        # excludes all workbooks except tableau_workbook_v2.sales_dashboard
        asset_filters = [
            {
                "asset_type": "tableau_workbook_v2",
                "default_effect": "block",
                "rules": [
                    {
                        "effect": "allow",
                        "conditions": [
                            {
                                "attribute_name": "name",
                                "value": "sales_dashboard",
                            }
                        ],
                    }
                ],
            }
        ]

        self._validate_blocked_assets(asset_filters, [1, 2])

    def test_requires_asset_type(self):
        """Test that asset filter config requires asset_type."""
        asset_filters = [
            {
                "filters": [
                    {
                        "conditions": [
                            {
                                "attribute_name": "name",
                                "value": "sales",
                            }
                        ],
                    }
                ],
            }
        ]

        # Should raise ValueError when asset_type is None
        with self.assertRaises(ValueError):
            AssetFiltersContainer.from_dict(dict(asset_filters=asset_filters))

    def test_complex_filtering(self):
        # Complex filtering with multiple rules
        asset_filters = [
            {  # Block all power_bi_workspace assets
                "asset_type": "power_bi_workspace",
                "default_effect": "block",
            },
            {  # Block tableau_workbook_v2 assets with 'temp_' prefix
                "asset_type": "tableau_workbook_v2",
                "rules": [
                    {
                        "conditions": [
                            {
                                "attribute_name": "name",
                                "value": "temp_",
                                "comparison_type": "prefix",
                            }
                        ],
                    }
                ],
            },
            {  # Allow specific jobs assets
                "asset_type": "jobs",
                "default_effect": "block",
                "rules": [
                    {
                        "effect": "allow",
                        "conditions": [
                            {
                                "attribute_name": "name",
                                "value": "quality",
                                "comparison_type": "substring",
                            }
                        ],
                    }
                ],
            },
        ]

        limits = AssetFiltersContainer.from_dict(dict(asset_filters=asset_filters))
        # Test various assets
        self.assertFalse(
            limits.is_asset_blocked("tableau_workbook_v2", {"name": "sales_dashboard"})
        )  # Allowed
        self.assertTrue(
            limits.is_asset_blocked("tableau_workbook_v2", {"name": "temp_old_report"})
        )  # Blocked
        self.assertFalse(limits.is_asset_blocked("jobs", {"name": "data_quality_check"}))  # Allowed
        self.assertTrue(limits.is_asset_blocked("jobs", {"name": "scheduled_etl"}))  # Blocked
        self.assertTrue(
            limits.is_asset_blocked("power_bi_workspace", {"name": "analytics_workspace"})
        )  # Blocked

    def _validate_blocked_assets(
        self, asset_filters: List[dict], blocked_asset_indexes: List[int]
    ) -> None:
        limits = AssetFiltersContainer.from_dict(dict(asset_filters=asset_filters))
        expected_assets = [
            a for a in self.ASSETS if self.ASSETS.index(a) not in blocked_asset_indexes
        ]
        actual_assets = self._filter_assets(self.ASSETS, limits)
        self.assertEqual(expected_assets, actual_assets)

    @staticmethod
    def _filter_assets(assets: List[AssetEntry], limits: AssetFiltersContainer) -> List[AssetEntry]:
        return [a for a in assets if not limits.is_asset_blocked(a.asset_type, a.attributes)]
