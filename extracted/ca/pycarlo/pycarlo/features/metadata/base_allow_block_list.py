import enum
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Generic, List, Optional, TypeVar

from dataclasses_json import DataClassJsonMixin

from pycarlo.common import get_logger

logger = get_logger(__name__)

# For documentation and samples check the link below:
# https://www.notion.so/montecarlodata/Catalog-Schema-Filtering-59edd6eff7f74c94ab6bfca75d2e3ff1


def _exclude_none_values(value: Any) -> bool:
    return value is None


class FilterEffectType(enum.Enum):
    BLOCK = "block"
    ALLOW = "allow"


RuleEffect = FilterEffectType


class FilterType(enum.Enum):
    EXACT_MATCH = "exact_match"
    PREFIX = "prefix"
    SUFFIX = "suffix"
    SUBSTRING = "substring"
    REGEXP = "regexp"


ComparisonType = FilterType

# Type variable for the filter class
FilterRuleT = TypeVar("FilterRuleT", bound="FilterRule")


@dataclass
class RuleCondition(DataClassJsonMixin):
    attribute_name: str
    value: str
    comparison_type: ComparisonType = ComparisonType.EXACT_MATCH


@dataclass
class FilterRule(DataClassJsonMixin):
    """
    Base class for all filter types. Provides common filtering logic that can be
    shared between different filter implementations (e.g., metadata filters, asset filters).
    """

    conditions: Optional[List[RuleCondition]] = field(default_factory=list)
    effect: RuleEffect = RuleEffect.BLOCK

    def matches(self, force_regexp: bool = False, **kwargs: Any) -> bool:
        """
        Returns True if all properties specified in kwargs match the conditions specified in
        properties of the same name in this object.
        If any of the conditions (for example self.field) is None, that condition will be matched.
        """
        if not kwargs:
            raise ValueError("At least one field needs to be specified for matching")

        # kwargs must match the field names in this class, if any of them do not,
        # invalidate the filter.
        try:
            return all(
                condition.attribute_name not in kwargs
                or self._match(
                    condition=condition,
                    value=kwargs.get(condition.attribute_name),
                    force_regexp=force_regexp,
                )
                for condition in self.conditions or []
            )
        except AttributeError:
            return False

    @classmethod
    def _match(cls, condition: RuleCondition, value: Optional[str], force_regexp: bool) -> bool:
        # Field not specified on this object, e.g. self.field=None, which matches everything
        if value is None:
            return False

        # The comparison is performed case-insensitive (check BaseFilter._safe_match)
        # We can use LOWER here since it is part of standard SQL (like AND/OR/NOT), so including it
        # here is a way to make sure that all comparisons are case-insensitive in the SQL sentences
        # for all engines. Added option to not always LOWER since customers do have lower/upper case
        # databases logged in MC
        filter_value = condition.value.lower()
        value = value.lower()

        if force_regexp or condition.comparison_type == FilterType.REGEXP:
            regexp = f"^{filter_value}$"
            return re.match(regexp, value) is not None
        elif condition.comparison_type == FilterType.PREFIX:
            return value.startswith(filter_value)
        elif condition.comparison_type == FilterType.SUFFIX:
            return value.endswith(filter_value)
        elif condition.comparison_type == FilterType.SUBSTRING:
            return filter_value in value
        else:  # filter_type == FilterType.EXACT_MATCH
            return filter_value == value


@dataclass
class BaseAllowBlockList(Generic[FilterRuleT], DataClassJsonMixin):
    rules: Optional[List[FilterRuleT]] = field(default_factory=list)
    default_effect: RuleEffect = RuleEffect.ALLOW

    @property
    def other_effect(self) -> RuleEffect:
        return RuleEffect.ALLOW if self.default_effect == RuleEffect.BLOCK else RuleEffect.BLOCK

    def get_default_effect_rules(
        self, condition: Optional[Callable[[FilterRuleT], bool]] = None
    ) -> List[FilterRuleT]:
        return list(
            filter(
                lambda f: f.effect == self.default_effect and (condition is None or condition(f)),
                self.rules or [],
            )
        )

    def get_other_effect_rules(
        self, condition: Optional[Callable[[FilterRuleT], bool]] = None
    ) -> List[FilterRuleT]:
        return list(
            filter(
                lambda f: f.effect != self.default_effect and (condition is None or condition(f)),
                self.rules or [],
            )
        )
