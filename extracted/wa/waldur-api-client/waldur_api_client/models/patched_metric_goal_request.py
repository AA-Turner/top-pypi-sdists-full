from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.comparator_enum import ComparatorEnum
from ..models.metric_goal_period_enum import MetricGoalPeriodEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedMetricGoalRequest")


@_attrs_define
class PatchedMetricGoalRequest:
    """
    Attributes:
        offering_metric (Union[Unset, UUID]):
        project (Union[None, UUID, Unset]): Empty sets the offering's default goal.
        comparator (Union[Unset, ComparatorEnum]):
        value (Union[Unset, str]):
        period (Union[Unset, MetricGoalPeriodEnum]):
    """

    offering_metric: Union[Unset, UUID] = UNSET
    project: Union[None, UUID, Unset] = UNSET
    comparator: Union[Unset, ComparatorEnum] = UNSET
    value: Union[Unset, str] = UNSET
    period: Union[Unset, MetricGoalPeriodEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_metric: Union[Unset, str] = UNSET
        if not isinstance(self.offering_metric, Unset):
            offering_metric = str(self.offering_metric)

        project: Union[None, Unset, str]
        if isinstance(self.project, Unset):
            project = UNSET
        elif isinstance(self.project, UUID):
            project = str(self.project)
        else:
            project = self.project

        comparator: Union[Unset, str] = UNSET
        if not isinstance(self.comparator, Unset):
            comparator = self.comparator.value

        value = self.value

        period: Union[Unset, str] = UNSET
        if not isinstance(self.period, Unset):
            period = self.period.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if offering_metric is not UNSET:
            field_dict["offering_metric"] = offering_metric
        if project is not UNSET:
            field_dict["project"] = project
        if comparator is not UNSET:
            field_dict["comparator"] = comparator
        if value is not UNSET:
            field_dict["value"] = value
        if period is not UNSET:
            field_dict["period"] = period

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _offering_metric = d.pop("offering_metric", UNSET)
        offering_metric: Union[Unset, UUID]
        if isinstance(_offering_metric, Unset):
            offering_metric = UNSET
        else:
            offering_metric = UUID(_offering_metric)

        def _parse_project(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_type_0 = UUID(data)

                return project_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        project = _parse_project(d.pop("project", UNSET))

        _comparator = d.pop("comparator", UNSET)
        comparator: Union[Unset, ComparatorEnum]
        if isinstance(_comparator, Unset):
            comparator = UNSET
        else:
            comparator = ComparatorEnum(_comparator)

        value = d.pop("value", UNSET)

        _period = d.pop("period", UNSET)
        period: Union[Unset, MetricGoalPeriodEnum]
        if isinstance(_period, Unset):
            period = UNSET
        else:
            period = MetricGoalPeriodEnum(_period)

        patched_metric_goal_request = cls(
            offering_metric=offering_metric,
            project=project,
            comparator=comparator,
            value=value,
            period=period,
        )

        patched_metric_goal_request.additional_properties = d
        return patched_metric_goal_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
