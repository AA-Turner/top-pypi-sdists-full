from dataclasses import dataclass, field
from typing import Dict, List

from dataclasses_json import DataClassJsonMixin

from .asset_allow_block_list import AssetAllowBlockList
from .base_allow_block_list import FilterEffectType

# Mapping of resource types to their supported asset types for collection preferences.
# This is used for validating asset collection preferences.
# When support for filtering an asset type is implemented in the DC, it should be added here.
# The reason it is here instead of in Monolith, is so that it can be referenced by the CLI.
# The pycarlo version in CLI and monolith should be updated after updating this and releasing a
# new version.
ASSET_TYPE_ATTRIBUTES = {"tableau": {"project": ["name"], "workbook": ["name", "luid"]}}


@dataclass
class AssetFiltersContainer(DataClassJsonMixin):
    """
    Simple container for asset filtering that focuses on in-memory filtering for REST APIs.

    This class provides basic asset filtering functionality without SQL generation complexity.
    It's designed for the initial phase where assets are collected via REST APIs rather than
    SQL queries.

    Example usage:
        # Block all external assets
        filters = AssetAllowBlockList(
            filters=[AssetFilter(asset_type="external", effect=FilterEffectType.BLOCK)]
        )
        container = AssetFiltersContainer(asset_filters=filters)

        # Check if an asset is blocked
        is_blocked = container.is_asset_blocked("external", "my_table")  # True
        is_blocked = container.is_asset_blocked("table", "users")        # False
    """

    asset_filters: List[AssetAllowBlockList] = field(default_factory=list)

    def is_asset_type_filtered(self, asset_type: str) -> bool:
        """Returns True if any filters are configured for the given asset type."""
        return bool(self._get_asset_filters(asset_type))

    def is_asset_blocked(self, asset_type: str, attributes: Dict[str, str]) -> bool:
        """
        Returns True if the specified asset is blocked by the current filters.

        Args:
          asset_type: The type of asset (e.g., 'tableau_workbook_v2', 'jobs', 'power_bi_workspace')
          attributes: A dictionary representing the attributes of the asset

        Returns:
          True if the asset is blocked, False if it's allowed
        """
        asset_filters = self._get_asset_filters(asset_type)

        is_blocked = False

        for asset_filter in asset_filters:
            default_effect_matches = asset_filter.get_default_effect_rules(
                lambda f: f.matches(force_regexp=False, **attributes)
            )
            if default_effect_matches:
                is_blocked = asset_filter.default_effect == FilterEffectType.BLOCK
            else:
                other_effect_matches = asset_filter.get_other_effect_rules(
                    lambda f: f.matches(force_regexp=False, **attributes)
                )
                if other_effect_matches:
                    is_blocked = asset_filter.other_effect == FilterEffectType.BLOCK
                else:
                    # No matches, use default effect
                    is_blocked = asset_filter.default_effect == FilterEffectType.BLOCK

        return is_blocked

    def _get_asset_filters(self, asset_type: str) -> List[AssetAllowBlockList]:
        return [f for f in self.asset_filters if f.asset_type == asset_type]
