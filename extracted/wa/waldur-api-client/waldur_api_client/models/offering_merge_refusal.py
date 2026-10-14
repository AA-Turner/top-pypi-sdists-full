from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.offering_merge_issue import OfferingMergeIssue


T = TypeVar("T", bound="OfferingMergeRefusal")


@_attrs_define
class OfferingMergeRefusal:
    """
    Attributes:
        detail (str):
        missing_acknowledgements (Union[Unset, list[str]]):
        blockers (Union[Unset, list['OfferingMergeIssue']]):
    """

    detail: str
    missing_acknowledgements: Union[Unset, list[str]] = UNSET
    blockers: Union[Unset, list["OfferingMergeIssue"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        detail = self.detail

        missing_acknowledgements: Union[Unset, list[str]] = UNSET
        if not isinstance(self.missing_acknowledgements, Unset):
            missing_acknowledgements = self.missing_acknowledgements

        blockers: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.blockers, Unset):
            blockers = []
            for blockers_item_data in self.blockers:
                blockers_item = blockers_item_data.to_dict()
                blockers.append(blockers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "detail": detail,
            }
        )
        if missing_acknowledgements is not UNSET:
            field_dict["missing_acknowledgements"] = missing_acknowledgements
        if blockers is not UNSET:
            field_dict["blockers"] = blockers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_merge_issue import OfferingMergeIssue

        d = dict(src_dict)
        detail = d.pop("detail")

        missing_acknowledgements = cast(list[str], d.pop("missing_acknowledgements", UNSET))

        blockers = []
        _blockers = d.pop("blockers", UNSET)
        for blockers_item_data in _blockers or []:
            blockers_item = OfferingMergeIssue.from_dict(blockers_item_data)

            blockers.append(blockers_item)

        offering_merge_refusal = cls(
            detail=detail,
            missing_acknowledgements=missing_acknowledgements,
            blockers=blockers,
        )

        offering_merge_refusal.additional_properties = d
        return offering_merge_refusal

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
