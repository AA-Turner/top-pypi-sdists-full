from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.duplicate_offering_merge_plan import DuplicateOfferingMergePlan


T = TypeVar("T", bound="DuplicateOfferingRemediation")


@_attrs_define
class DuplicateOfferingRemediation:
    """
    Attributes:
        tenant_id (int):
        offering_type (str):
        keeper_id (int):
        keeper_name (str):
        dry_run (bool):
        duplicates (list['DuplicateOfferingMergePlan']):
        blockers (list[str]):
    """

    tenant_id: int
    offering_type: str
    keeper_id: int
    keeper_name: str
    dry_run: bool
    duplicates: list["DuplicateOfferingMergePlan"]
    blockers: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tenant_id = self.tenant_id

        offering_type = self.offering_type

        keeper_id = self.keeper_id

        keeper_name = self.keeper_name

        dry_run = self.dry_run

        duplicates = []
        for duplicates_item_data in self.duplicates:
            duplicates_item = duplicates_item_data.to_dict()
            duplicates.append(duplicates_item)

        blockers = self.blockers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tenant_id": tenant_id,
                "offering_type": offering_type,
                "keeper_id": keeper_id,
                "keeper_name": keeper_name,
                "dry_run": dry_run,
                "duplicates": duplicates,
                "blockers": blockers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.duplicate_offering_merge_plan import DuplicateOfferingMergePlan

        d = dict(src_dict)
        tenant_id = d.pop("tenant_id")

        offering_type = d.pop("offering_type")

        keeper_id = d.pop("keeper_id")

        keeper_name = d.pop("keeper_name")

        dry_run = d.pop("dry_run")

        duplicates = []
        _duplicates = d.pop("duplicates")
        for duplicates_item_data in _duplicates:
            duplicates_item = DuplicateOfferingMergePlan.from_dict(duplicates_item_data)

            duplicates.append(duplicates_item)

        blockers = cast(list[str], d.pop("blockers"))

        duplicate_offering_remediation = cls(
            tenant_id=tenant_id,
            offering_type=offering_type,
            keeper_id=keeper_id,
            keeper_name=keeper_name,
            dry_run=dry_run,
            duplicates=duplicates,
            blockers=blockers,
        )

        duplicate_offering_remediation.additional_properties = d
        return duplicate_offering_remediation

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
