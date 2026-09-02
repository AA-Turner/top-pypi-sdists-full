from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.count_runnables_by_owner_response_200_counts import CountRunnablesByOwnerResponse200Counts


T = TypeVar("T", bound="CountRunnablesByOwnerResponse200")


@_attrs_define
class CountRunnablesByOwnerResponse200:
    """
    Attributes:
        counts (CountRunnablesByOwnerResponse200Counts): owner prefix (f/<folder> or u/<user>) to count
    """

    counts: "CountRunnablesByOwnerResponse200Counts"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        counts = self.counts.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "counts": counts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.count_runnables_by_owner_response_200_counts import CountRunnablesByOwnerResponse200Counts

        d = src_dict.copy()
        counts = CountRunnablesByOwnerResponse200Counts.from_dict(d.pop("counts"))

        count_runnables_by_owner_response_200 = cls(
            counts=counts,
        )

        count_runnables_by_owner_response_200.additional_properties = d
        return count_runnables_by_owner_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
