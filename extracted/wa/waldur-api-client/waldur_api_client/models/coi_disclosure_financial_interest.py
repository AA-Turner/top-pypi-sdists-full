from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.amount_range_enum import AmountRangeEnum
from ..models.entity_type_enum import EntityTypeEnum
from ..models.relationship_type_enum import RelationshipTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="COIDisclosureFinancialInterest")


@_attrs_define
class COIDisclosureFinancialInterest:
    """
    Attributes:
        uuid (UUID):
        entity_name (str):
        entity_type (EntityTypeEnum):
        relationship_type (RelationshipTypeEnum):
        amount_range (AmountRangeEnum):
        is_ongoing (Union[Unset, bool]):
        description (Union[Unset, str]):
    """

    uuid: UUID
    entity_name: str
    entity_type: EntityTypeEnum
    relationship_type: RelationshipTypeEnum
    amount_range: AmountRangeEnum
    is_ongoing: Union[Unset, bool] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        entity_name = self.entity_name

        entity_type = self.entity_type.value

        relationship_type = self.relationship_type.value

        amount_range = self.amount_range.value

        is_ongoing = self.is_ongoing

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "entity_name": entity_name,
                "entity_type": entity_type,
                "relationship_type": relationship_type,
                "amount_range": amount_range,
            }
        )
        if is_ongoing is not UNSET:
            field_dict["is_ongoing"] = is_ongoing
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        entity_name = d.pop("entity_name")

        entity_type = EntityTypeEnum(d.pop("entity_type"))

        relationship_type = RelationshipTypeEnum(d.pop("relationship_type"))

        amount_range = AmountRangeEnum(d.pop("amount_range"))

        is_ongoing = d.pop("is_ongoing", UNSET)

        description = d.pop("description", UNSET)

        coi_disclosure_financial_interest = cls(
            uuid=uuid,
            entity_name=entity_name,
            entity_type=entity_type,
            relationship_type=relationship_type,
            amount_range=amount_range,
            is_ongoing=is_ongoing,
            description=description,
        )

        coi_disclosure_financial_interest.additional_properties = d
        return coi_disclosure_financial_interest

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
