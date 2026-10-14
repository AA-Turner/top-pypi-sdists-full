import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.good_direction_enum import GoodDirectionEnum
from ..models.metric_kind_enum import MetricKindEnum
from ..models.offering_metric_state_enum import OfferingMetricStateEnum
from ..models.project_aggregation_enum import ProjectAggregationEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingMetric")


@_attrs_define
class OfferingMetric:
    """
    Attributes:
        uuid (UUID):
        offering (UUID):
        offering_name (str):
        definition (UUID):
        key (str): Name services report against. Cannot be changed.
        name (str):
        unit (str): UCUM unit, for example h, % or {learners}.
        kind (MetricKindEnum):
        good_direction (GoodDirectionEnum):
        attribute_keys (list[str]):
        state (OfferingMetricStateEnum):
        created (datetime.datetime):
        display_name (Union[Unset, str]): Empty shows the definition's name.
        project_aggregation (Union[Unset, ProjectAggregationEnum]):
    """

    uuid: UUID
    offering: UUID
    offering_name: str
    definition: UUID
    key: str
    name: str
    unit: str
    kind: MetricKindEnum
    good_direction: GoodDirectionEnum
    attribute_keys: list[str]
    state: OfferingMetricStateEnum
    created: datetime.datetime
    display_name: Union[Unset, str] = UNSET
    project_aggregation: Union[Unset, ProjectAggregationEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        offering = str(self.offering)

        offering_name = self.offering_name

        definition = str(self.definition)

        key = self.key

        name = self.name

        unit = self.unit

        kind = self.kind.value

        good_direction = self.good_direction.value

        attribute_keys = self.attribute_keys

        state = self.state.value

        created = self.created.isoformat()

        display_name = self.display_name

        project_aggregation: Union[Unset, str] = UNSET
        if not isinstance(self.project_aggregation, Unset):
            project_aggregation = self.project_aggregation.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "offering": offering,
                "offering_name": offering_name,
                "definition": definition,
                "key": key,
                "name": name,
                "unit": unit,
                "kind": kind,
                "good_direction": good_direction,
                "attribute_keys": attribute_keys,
                "state": state,
                "created": created,
            }
        )
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if project_aggregation is not UNSET:
            field_dict["project_aggregation"] = project_aggregation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        offering = UUID(d.pop("offering"))

        offering_name = d.pop("offering_name")

        definition = UUID(d.pop("definition"))

        key = d.pop("key")

        name = d.pop("name")

        unit = d.pop("unit")

        kind = MetricKindEnum(d.pop("kind"))

        good_direction = GoodDirectionEnum(d.pop("good_direction"))

        attribute_keys = cast(list[str], d.pop("attribute_keys"))

        state = OfferingMetricStateEnum(d.pop("state"))

        created = isoparse(d.pop("created"))

        display_name = d.pop("display_name", UNSET)

        _project_aggregation = d.pop("project_aggregation", UNSET)
        project_aggregation: Union[Unset, ProjectAggregationEnum]
        if isinstance(_project_aggregation, Unset):
            project_aggregation = UNSET
        else:
            project_aggregation = ProjectAggregationEnum(_project_aggregation)

        offering_metric = cls(
            uuid=uuid,
            offering=offering,
            offering_name=offering_name,
            definition=definition,
            key=key,
            name=name,
            unit=unit,
            kind=kind,
            good_direction=good_direction,
            attribute_keys=attribute_keys,
            state=state,
            created=created,
            display_name=display_name,
            project_aggregation=project_aggregation,
        )

        offering_metric.additional_properties = d
        return offering_metric

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
