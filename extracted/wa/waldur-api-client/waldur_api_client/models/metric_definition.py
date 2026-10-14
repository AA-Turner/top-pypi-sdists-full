import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.good_direction_enum import GoodDirectionEnum
from ..models.metric_definition_state_enum import MetricDefinitionStateEnum
from ..models.metric_kind_enum import MetricKindEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetricDefinition")


@_attrs_define
class MetricDefinition:
    """
    Attributes:
        uuid (UUID):
        key (str): Name services report against. Cannot be changed.
        name (str):
        owner_customer_name (str):
        created (datetime.datetime):
        description (Union[Unset, str]):
        unit (Union[Unset, str]): UCUM unit, for example h, % or {learners}.
        kind (Union[Unset, MetricKindEnum]):
        good_direction (Union[Unset, GoodDirectionEnum]):
        attribute_keys (Union[Unset, list[str]]):
        max_attribute_values (Union[Unset, int]): Distinct values one attribute may take per resource.
        retention_policy (Union[None, UUID, Unset]):
        owner_customer (Union[None, UUID, Unset]): Service provider the definition is private to; empty is global.
        state (Union[Unset, MetricDefinitionStateEnum]):
    """

    uuid: UUID
    key: str
    name: str
    owner_customer_name: str
    created: datetime.datetime
    description: Union[Unset, str] = UNSET
    unit: Union[Unset, str] = UNSET
    kind: Union[Unset, MetricKindEnum] = UNSET
    good_direction: Union[Unset, GoodDirectionEnum] = UNSET
    attribute_keys: Union[Unset, list[str]] = UNSET
    max_attribute_values: Union[Unset, int] = UNSET
    retention_policy: Union[None, UUID, Unset] = UNSET
    owner_customer: Union[None, UUID, Unset] = UNSET
    state: Union[Unset, MetricDefinitionStateEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        key = self.key

        name = self.name

        owner_customer_name = self.owner_customer_name

        created = self.created.isoformat()

        description = self.description

        unit = self.unit

        kind: Union[Unset, str] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        good_direction: Union[Unset, str] = UNSET
        if not isinstance(self.good_direction, Unset):
            good_direction = self.good_direction.value

        attribute_keys: Union[Unset, list[str]] = UNSET
        if not isinstance(self.attribute_keys, Unset):
            attribute_keys = self.attribute_keys

        max_attribute_values = self.max_attribute_values

        retention_policy: Union[None, Unset, str]
        if isinstance(self.retention_policy, Unset):
            retention_policy = UNSET
        elif isinstance(self.retention_policy, UUID):
            retention_policy = str(self.retention_policy)
        else:
            retention_policy = self.retention_policy

        owner_customer: Union[None, Unset, str]
        if isinstance(self.owner_customer, Unset):
            owner_customer = UNSET
        elif isinstance(self.owner_customer, UUID):
            owner_customer = str(self.owner_customer)
        else:
            owner_customer = self.owner_customer

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "key": key,
                "name": name,
                "owner_customer_name": owner_customer_name,
                "created": created,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if unit is not UNSET:
            field_dict["unit"] = unit
        if kind is not UNSET:
            field_dict["kind"] = kind
        if good_direction is not UNSET:
            field_dict["good_direction"] = good_direction
        if attribute_keys is not UNSET:
            field_dict["attribute_keys"] = attribute_keys
        if max_attribute_values is not UNSET:
            field_dict["max_attribute_values"] = max_attribute_values
        if retention_policy is not UNSET:
            field_dict["retention_policy"] = retention_policy
        if owner_customer is not UNSET:
            field_dict["owner_customer"] = owner_customer
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        key = d.pop("key")

        name = d.pop("name")

        owner_customer_name = d.pop("owner_customer_name")

        created = isoparse(d.pop("created"))

        description = d.pop("description", UNSET)

        unit = d.pop("unit", UNSET)

        _kind = d.pop("kind", UNSET)
        kind: Union[Unset, MetricKindEnum]
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = MetricKindEnum(_kind)

        _good_direction = d.pop("good_direction", UNSET)
        good_direction: Union[Unset, GoodDirectionEnum]
        if isinstance(_good_direction, Unset):
            good_direction = UNSET
        else:
            good_direction = GoodDirectionEnum(_good_direction)

        attribute_keys = cast(list[str], d.pop("attribute_keys", UNSET))

        max_attribute_values = d.pop("max_attribute_values", UNSET)

        def _parse_retention_policy(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                retention_policy_type_0 = UUID(data)

                return retention_policy_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        retention_policy = _parse_retention_policy(d.pop("retention_policy", UNSET))

        def _parse_owner_customer(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                owner_customer_type_0 = UUID(data)

                return owner_customer_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        owner_customer = _parse_owner_customer(d.pop("owner_customer", UNSET))

        _state = d.pop("state", UNSET)
        state: Union[Unset, MetricDefinitionStateEnum]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = MetricDefinitionStateEnum(_state)

        metric_definition = cls(
            uuid=uuid,
            key=key,
            name=name,
            owner_customer_name=owner_customer_name,
            created=created,
            description=description,
            unit=unit,
            kind=kind,
            good_direction=good_direction,
            attribute_keys=attribute_keys,
            max_attribute_values=max_attribute_values,
            retention_policy=retention_policy,
            owner_customer=owner_customer,
            state=state,
        )

        metric_definition.additional_properties = d
        return metric_definition

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
