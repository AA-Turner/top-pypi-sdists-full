from __future__ import annotations

import enum
from itertools import chain
from typing import List

import betterproto

from bigeye_sdk.functions.casing import snake_case
from bigeye_sdk.generated.com.bigeye.models.generated import (
    MetricType,
    PredefinedMetric,
    PredefinedMetricName,
    AutothresholdSensitivity,
    FieldType,
    TimeIntervalType,
    LookbackType,
    AggregationType,
    DataNodeType,
    MetricTemplateParameterType,
    CatalogEntityType,
    WorkflowProcessingStatus,
    TableSortField,
    SortDirection,
    SchemaChangeOperation, IssuePriority, IssueSortField, IssueStatus, RelationshipType, IntegrationPartner,
)


def _remove_protobuf_type(
        protobuf_enum_cls: type(betterproto.Enum), member_name: str
) -> str:
    """
    Processes an enum type prefix or postfix out of an enum member name.

    >>> _remove_protobuf_type(AutothresholdSensitivity, AutothresholdSensitivity.AUTOTHRESHOLD_SENSITIVITY_MEDIUM.name)
    'MEDIUM'

    Args:
        protobuf_enum_cls: the specific protobuf enum class.
        member_name: the enum member to remove the protobuf type from.

    Returns:
        the member name with the type prefix or post fix returned.

    """
    l = [
        f"{_get_protobuf_type(protobuf_enum_cls)}_",  # Covers enums that fit protobuf enum naming convention.
        f"_{_get_protobuf_type(protobuf_enum_cls)}",  # Covers enums that fit Bigeyes old naming convention.
    ]

    for i in l:
        member_name = member_name.replace(i, "")

    return member_name


def _get_protobuf_type(protobuf_enum_cls: betterproto.Enum) -> str:
    """

    Args:
        protobuf_enum_cls: beterproto Enum class

    Returns:
        snake case enum type name
    """
    return f"{snake_case(protobuf_enum_cls.__name__).upper()}"


def datawatch_enum_facade(cls):
    """
    Decorator to add protobuf helpers.  Can be removed once beterproto fixes the enum naming convention issues.
    """

    def get_protobuf_type_prefix():
        return _get_protobuf_type(cls.__protobuf_enum_cls__)

    def to_datawatch_object(self):
        exception: Exception

        potential_enum_mbr_names: List[str] = [
            f"{cls.get_protobuf_type_prefix()}_{self.name}",  # Type name prefix
            f"{self.name}_{cls.get_protobuf_type_prefix()}",  # Type name postfix
            self.name,  # No type name in member name
        ]

        for i in potential_enum_mbr_names:
            try:
                return cls.__protobuf_enum_cls__.from_string(i)
            except Exception as ex:
                exception = ex

        raise exception

    def from_datawatch_object(member: betterproto.Enum) -> cls:
        # Handle case where member is an int instead of Enum object
        if isinstance(member, int):
            member = cls.__protobuf_enum_cls__(member)
        return cls(
            _remove_protobuf_type(cls.__protobuf_enum_cls__, member.name.__str__())
        )

    cls.get_protobuf_type_prefix = get_protobuf_type_prefix
    cls.to_datawatch_object = to_datawatch_object
    cls.from_datawatch_object = from_datawatch_object
    return cls


class MetricStatus(str, enum.Enum):
    HEALTHY = "HEALTHY"  # Query by this status will contain healthy metrics
    ALERTING = "ALERTING"  # Query by this status will contain alerting metrics
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"  # Query by this status will contain failed and unknown status metrics.


# TODO deprecate
class SimpleMetricCategory(str, enum.Enum):
    PREDEFINED = "PREDEFINED"
    TEMPLATE = "TEMPLATE"

    def factory(self, metric_name: str) -> MetricType:
        if self == SimpleMetricCategory.PREDEFINED:
            mt = MetricType()
            mt.predefined_metric = PredefinedMetric(
                PredefinedMetricName.from_string(metric_name)
            )
            return mt
        elif self == SimpleMetricCategory.TEMPLATE:
            raise Exception("Not yet supported for Simple Metric Templates.")

    @classmethod
    def get_simple_metric_category(cls, mt: MetricType) -> SimpleMetricCategory:
        mtd = (
            mt.to_dict()
        )  # TODO: this is the only way it would work.  beterproto has defaults that create 0 int placeholders.  Works for now but try a new way later.
        if "templateMetric" in mtd:
            return SimpleMetricCategory.TEMPLATE
        elif "predefinedMetric" in mtd:
            return SimpleMetricCategory.PREDEFINED

    @classmethod
    def get_metric_name(cls, mt: MetricType):
        smt = SimpleMetricCategory.get_simple_metric_category(mt)
        if smt == SimpleMetricCategory.PREDEFINED:
            return mt.predefined_metric.metric_name.name
        if smt == SimpleMetricCategory.TEMPLATE:
            return mt.template_metric.template_name


@datawatch_enum_facade
class SimplePredefinedMetricName(str, enum.Enum):
    """Programmatically provides a yaml serializable mapping from string value to PredefinedMetricName."""

    _ignore_ = "member cls"
    __protobuf_enum_cls__ = PredefinedMetricName
    cls = vars()
    for member in chain(list(__protobuf_enum_cls__)):
        cls[_remove_protobuf_type(__protobuf_enum_cls__, member.name)] = (
            _remove_protobuf_type(__protobuf_enum_cls__, member.name)
        )


@datawatch_enum_facade
class SimpleAutothresholdSensitivity(str, enum.Enum):
    """Programmatically provides a yaml serializable autothreshold from string value to AutothresholdSensitivity"""

    _ignore_ = "member cls"
    __protobuf_enum_cls__ = AutothresholdSensitivity
    cls = vars()
    for member in chain(list(__protobuf_enum_cls__)):
        cls[_remove_protobuf_type(__protobuf_enum_cls__, member.name)] = (
            _remove_protobuf_type(__protobuf_enum_cls__, member.name)
        )


@datawatch_enum_facade
class SimpleFieldType(str, enum.Enum):
    """Programmatically provides a yaml serializable mapping from string value to FieldType"""

    _ignore_ = "member cls"
    __protobuf_enum_cls__ = FieldType
    cls = vars()
    for member in list(__protobuf_enum_cls__):
        cls[_remove_protobuf_type(__protobuf_enum_cls__, member.name)] = (
            _remove_protobuf_type(__protobuf_enum_cls__, member.name)
        )


@datawatch_enum_facade
class SimpleTimeIntervalType(str, enum.Enum):
    """Programmatically provides a yaml serializable mapping from string value to TimeIntervalType"""

    _ignore_ = "member cls"
    __protobuf_enum_cls__ = TimeIntervalType
    cls = vars()
    for member in list(__protobuf_enum_cls__):
        cls[_remove_protobuf_type(__protobuf_enum_cls__, member.name)] = (
            _remove_protobuf_type(__protobuf_enum_cls__, member.name)
        )


@datawatch_enum_facade
class SimpleLookbackType(str, enum.Enum):
    """Programmatically provides a yaml serializable mapping from string value to LookbackType"""

    _ignore_ = "member cls"
    __protobuf_enum_cls__ = LookbackType
    cls = vars()
    for member in list(__protobuf_enum_cls__):
        cls[_remove_protobuf_type(__protobuf_enum_cls__, member.name)] = (
            _remove_protobuf_type(__protobuf_enum_cls__, member.name)
        )


@datawatch_enum_facade
class SimpleAggregationType(str, enum.Enum):
    """Programmatically provides a yaml serializable mapping from string value to AggregationType"""

    _ignore_ = "member cls"
    __protobuf_enum_cls__ = AggregationType
    cls = vars()
    for member in list(__protobuf_enum_cls__):
        cls[_remove_protobuf_type(__protobuf_enum_cls__, member.name)] = (
            _remove_protobuf_type(__protobuf_enum_cls__, member.name)
        )


@datawatch_enum_facade
class SimpleDataNodeType(str, enum.Enum):
    """Programmatically provides a yaml serializable mapping from string value to DataNodeType"""

    _ignore_ = "member cls"
    __protobuf_enum_cls__ = DataNodeType
    cls = vars()
    for member in list(__protobuf_enum_cls__):
        cls[_remove_protobuf_type(__protobuf_enum_cls__, member.name)] = (
            _remove_protobuf_type(__protobuf_enum_cls__, member.name)
        )


@datawatch_enum_facade
class SimpleMetricTemplateParameterType(str, enum.Enum):
    """Programmatically provides a yaml serializable mapping from string value to MetricTemplateParameterType"""

    _ignore_ = "member cls"
    __protobuf_enum_cls__ = MetricTemplateParameterType
    cls = vars()
    for member in list(__protobuf_enum_cls__):
        if "UNSPECIFIED" not in member.name:
            cls[_remove_protobuf_type(__protobuf_enum_cls__, member.name)] = (
                _remove_protobuf_type(__protobuf_enum_cls__, member.name)
            )


@datawatch_enum_facade
class SimpleCatalogEntityType(str, enum.Enum):
    """Programmatically provides a yaml serializable mapping from string value to MetricTemplateParameterType"""

    _ignore_ = "member cls"
    __protobuf_enum_cls__ = CatalogEntityType
    cls = vars()
    for member in list(__protobuf_enum_cls__):
        cls[_remove_protobuf_type(__protobuf_enum_cls__, member.name)] = (
            _remove_protobuf_type(__protobuf_enum_cls__, member.name)
        )


@datawatch_enum_facade
class SimpleWorkflowProcessingStatus(str, enum.Enum):
    """Programmatically provides a yaml serializable mapping from string value to WorkflowProcessingStatus"""

    _ignore_ = "member cls"
    __protobuf_enum_cls__ = WorkflowProcessingStatus
    cls = vars()
    for member in list(__protobuf_enum_cls__):
        cls[_remove_protobuf_type(__protobuf_enum_cls__, member.name)] = (
            _remove_protobuf_type(__protobuf_enum_cls__, member.name)
        )


@datawatch_enum_facade
class SimpleTableSortField(str, enum.Enum):
    """Programmatically provides a yaml serializable mapping from string value to TableSortField"""

    _ignore_ = "member cls"
    __protobuf_enum_cls__ = TableSortField
    cls = vars()
    for member in list(__protobuf_enum_cls__):
        cls[_remove_protobuf_type(__protobuf_enum_cls__, member.name)] = (
            _remove_protobuf_type(__protobuf_enum_cls__, member.name)
        )


@datawatch_enum_facade
class SimpleIssueSortField(str, enum.Enum):
    """Programmatically provides a yaml serializable mapping from string value to IssueSortField"""

    _ignore_ = "member cls"
    __protobuf_enum_cls__ = IssueSortField
    cls = vars()
    for member in list(__protobuf_enum_cls__):
        cls[_remove_protobuf_type(__protobuf_enum_cls__, member.name)] = (
            _remove_protobuf_type(__protobuf_enum_cls__, member.name)
        )


@datawatch_enum_facade
class SimpleSortDirection(str, enum.Enum):
    """Programmatically provides a yaml serializable mapping from string value to SortDirection"""

    _ignore_ = "member cls"
    __protobuf_enum_cls__ = SortDirection
    cls = vars()
    for member in list(__protobuf_enum_cls__):
        cls[_remove_protobuf_type(__protobuf_enum_cls__, member.name)] = (
            _remove_protobuf_type(__protobuf_enum_cls__, member.name)
        )


@datawatch_enum_facade
class SimpleSchemaChangeOperation(str, enum.Enum):
    """Programmatically provides a yaml serializable mapping from string value to SchemaChangeOperation"""

    _ignore_ = "member cls"
    __protobuf_enum_cls__ = SchemaChangeOperation
    cls = vars()
    for member in list(__protobuf_enum_cls__):
        if "UNSPECIFIED" not in member.name:
            cls[_remove_protobuf_type(__protobuf_enum_cls__, member.name)] = (
                _remove_protobuf_type(__protobuf_enum_cls__, member.name)
            )


@datawatch_enum_facade
class SimpleIssuePriority(str, enum.Enum):
    """Programmatically provides a yaml serializable mapping from string value to IssuePriority"""

    _ignore_ = "member cls"
    __protobuf_enum_cls__ = IssuePriority
    cls = vars()
    for member in list(__protobuf_enum_cls__):
        if "UNSPECIFIED" not in member.name:
            cls[_remove_protobuf_type(__protobuf_enum_cls__, member.name)] = (
                _remove_protobuf_type(__protobuf_enum_cls__, member.name)
            )


@datawatch_enum_facade
class SimpleIssueStatus(str, enum.Enum):
    """Programmatically provides a yaml serializable mapping from string value to IssueStatus"""

    _ignore_ = "member cls"
    __protobuf_enum_cls__ = IssueStatus
    cls = vars()
    for member in list(__protobuf_enum_cls__):
        cls[_remove_protobuf_type(__protobuf_enum_cls__, member.name)] = (
            _remove_protobuf_type(__protobuf_enum_cls__, member.name)
        )


@datawatch_enum_facade
class SimpleIntegrationPartner(str, enum.Enum):
    """Programmatically provides a yaml serializable mapping from string value to IntegrationPartner"""

    _ignore_ = "member cls"
    __protobuf_enum_cls__ = IntegrationPartner
    cls = vars()
    for member in list(__protobuf_enum_cls__):
        cls[_remove_protobuf_type(__protobuf_enum_cls__, member.name)] = (
            _remove_protobuf_type(__protobuf_enum_cls__, member.name)
        )


@datawatch_enum_facade
class SimpleMetricTemplateFieldType(str, enum.Enum):
    BOOLEAN = SimpleFieldType.BOOLEAN
    NUMERIC = SimpleFieldType.NUMERIC


@datawatch_enum_facade
class SimpleDbtTestToMetricType(str, enum.Enum):
    not_null = SimplePredefinedMetricName.COUNT_NULL
    unique = SimplePredefinedMetricName.COUNT_DUPLICATES
    accepted_values = SimplePredefinedMetricName.PERCENT_VALUE_IN_LIST
