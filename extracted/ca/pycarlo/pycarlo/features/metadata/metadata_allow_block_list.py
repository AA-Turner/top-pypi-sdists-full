from dataclasses import dataclass, field
from functools import cached_property
from typing import FrozenSet, Iterable, List, Optional

from dataclasses_json import config, dataclass_json

from pycarlo.common import get_logger
from pycarlo.features.metadata.base_allow_block_list import (
    BaseAllowBlockList,
    ComparisonType,
    FilterRule,
    FilterType,
    RuleCondition,
)

logger = get_logger(__name__)

# For documentation and samples check the link below:
# https://www.notion.so/montecarlodata/Catalog-Schema-Filtering-59edd6eff7f74c94ab6bfca75d2e3ff1

# Metadata hierarchy, coarsest first. table_name and table_type both describe a table.
METADATA_ATTRIBUTE_LEVELS = {"project": 0, "dataset": 1, "table_name": 2, "table_type": 2}


@dataclass_json
@dataclass
class MetadataFilter(FilterRule):
    type: FilterType = FilterType.EXACT_MATCH

    # we're using exclude=_exclude_none_values to prevent these properties to be serialized to json
    # when None, to keep the json doc simpler
    project: Optional[str] = field(metadata=config(exclude=lambda x: x is None), default=None)
    dataset: Optional[str] = field(metadata=config(exclude=lambda x: x is None), default=None)
    table_type: Optional[str] = field(metadata=config(exclude=lambda x: x is None), default=None)
    table_name: Optional[str] = field(metadata=config(exclude=lambda x: x is None), default=None)

    def __post_init__(self):
        # For backwards compatibility, we now create a set of conditions based on the
        # metadata-specific fields.
        self.conditions = self.conditions or []
        if self.table_name is not None:
            is_target_field = self.filter_type_target_field() == "table_name"
            condition = RuleCondition(
                comparison_type=self.type if is_target_field else ComparisonType.EXACT_MATCH,
                attribute_name="table_name",
                value=self.table_name,
            )
            self.conditions.append(condition)

        if self.dataset is not None:
            is_target_field = self.filter_type_target_field() == "dataset"
            condition = RuleCondition(
                comparison_type=self.type if is_target_field else ComparisonType.EXACT_MATCH,
                attribute_name="dataset",
                value=self.dataset,
            )
            self.conditions.append(condition)

        if self.project is not None:
            is_target_field = self.filter_type_target_field() == "project"
            condition = RuleCondition(
                comparison_type=self.type if is_target_field else ComparisonType.EXACT_MATCH,
                attribute_name="project",
                value=self.project,
            )
            self.conditions.append(condition)

        if self.table_type is not None:
            condition = RuleCondition(
                comparison_type=ComparisonType.EXACT_MATCH,
                attribute_name="table_type",
                value=self.table_type,
            )
            self.conditions.append(condition)

    def filter_type_target_field(self) -> str:
        """
        The field that is evaluated using filter type. Other fields should be
        compared using exact match.
        """
        if self.table_name is not None:
            return "table_name"
        if self.dataset is not None:
            return "dataset"
        if self.project is not None:
            return "project"

        logger.exception("Invalid filter, missing target values")
        return ""

    @cached_property
    def condition_attribute_names(self) -> FrozenSet[str]:
        """
        Names of the attributes this filter has conditions on. Cached because it's checked on
        every lookup; conditions are built in __post_init__ and not changed afterwards.
        """
        return frozenset(c.attribute_name for c in self.conditions or [])


def unevaluable_attributes(available: Iterable[str]) -> FrozenSet[str]:
    """
    Hierarchy attributes that a filter condition can't be evaluated against, given the available
    attributes (those supplied in a lookup, or mapped to a SQL column): the ones not available
    at or below the finest available level. Missing coarser attributes are not included, e.g. a
    dataset-only lookup can still evaluate a (project, dataset) filter permissively.
    Empty when no hierarchy attribute is available.
    """
    available = set(available)
    levels = [
        METADATA_ATTRIBUTE_LEVELS[name] for name in available if name in METADATA_ATTRIBUTE_LEVELS
    ]
    if not levels:
        return frozenset()
    finest_level = max(levels)
    return frozenset(
        name
        for name, level in METADATA_ATTRIBUTE_LEVELS.items()
        if level >= finest_level and name not in available
    )


@dataclass_json
@dataclass
class MetadataAllowBlockList(BaseAllowBlockList[MetadataFilter]):
    filters: List[MetadataFilter] = field(default_factory=list)

    def __post_init__(self):
        self.rules = self.filters
