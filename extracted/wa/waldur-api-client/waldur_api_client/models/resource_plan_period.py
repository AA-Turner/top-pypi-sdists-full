import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_component_usage import BaseComponentUsage


T = TypeVar("T", bound="ResourcePlanPeriod")


@_attrs_define
class ResourcePlanPeriod:
    """
    Attributes:
        uuid (UUID):
        plan_name (str):
        plan_uuid (UUID):
        components (list['BaseComponentUsage']):
        start (Union[None, Unset, datetime.datetime]):
        end (Union[None, Unset, datetime.datetime]):
    """

    uuid: UUID
    plan_name: str
    plan_uuid: UUID
    components: list["BaseComponentUsage"]
    start: Union[None, Unset, datetime.datetime] = UNSET
    end: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        plan_name = self.plan_name

        plan_uuid = str(self.plan_uuid)

        components = []
        for components_item_data in self.components:
            components_item = components_item_data.to_dict()
            components.append(components_item)

        start: Union[None, Unset, str]
        if isinstance(self.start, Unset):
            start = UNSET
        elif isinstance(self.start, datetime.datetime):
            start = self.start.isoformat()
        else:
            start = self.start

        end: Union[None, Unset, str]
        if isinstance(self.end, Unset):
            end = UNSET
        elif isinstance(self.end, datetime.datetime):
            end = self.end.isoformat()
        else:
            end = self.end

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "plan_name": plan_name,
                "plan_uuid": plan_uuid,
                "components": components,
            }
        )
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_component_usage import BaseComponentUsage

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        plan_name = d.pop("plan_name")

        plan_uuid = UUID(d.pop("plan_uuid"))

        components = []
        _components = d.pop("components")
        for components_item_data in _components:
            components_item = BaseComponentUsage.from_dict(components_item_data)

            components.append(components_item)

        def _parse_start(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_type_0 = isoparse(data)

                return start_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        start = _parse_start(d.pop("start", UNSET))

        def _parse_end(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_type_0 = isoparse(data)

                return end_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        end = _parse_end(d.pop("end", UNSET))

        resource_plan_period = cls(
            uuid=uuid,
            plan_name=plan_name,
            plan_uuid=plan_uuid,
            components=components,
            start=start,
            end=end,
        )

        resource_plan_period.additional_properties = d
        return resource_plan_period

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
