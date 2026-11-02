import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.eval_dataset_scorers_item import EvalDatasetScorersItem


T = TypeVar("T", bound="EvalDataset")


@_attrs_define
class EvalDataset:
    """
    Attributes:
        path (str):
        created_at (datetime.datetime):
        created_by (str):
        edited_at (datetime.datetime):
        edited_by (str):
        summary (Union[Unset, str]):
        scorers (Union[Unset, List['EvalDatasetScorersItem']]): The columns of the results table, in display order.
    """

    path: str
    created_at: datetime.datetime
    created_by: str
    edited_at: datetime.datetime
    edited_by: str
    summary: Union[Unset, str] = UNSET
    scorers: Union[Unset, List["EvalDatasetScorersItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        created_at = self.created_at.isoformat()

        created_by = self.created_by
        edited_at = self.edited_at.isoformat()

        edited_by = self.edited_by
        summary = self.summary
        scorers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.scorers, Unset):
            scorers = []
            for scorers_item_data in self.scorers:
                scorers_item = scorers_item_data.to_dict()

                scorers.append(scorers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "created_at": created_at,
                "created_by": created_by,
                "edited_at": edited_at,
                "edited_by": edited_by,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary
        if scorers is not UNSET:
            field_dict["scorers"] = scorers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.eval_dataset_scorers_item import EvalDatasetScorersItem

        d = src_dict.copy()
        path = d.pop("path")

        created_at = isoparse(d.pop("created_at"))

        created_by = d.pop("created_by")

        edited_at = isoparse(d.pop("edited_at"))

        edited_by = d.pop("edited_by")

        summary = d.pop("summary", UNSET)

        scorers = []
        _scorers = d.pop("scorers", UNSET)
        for scorers_item_data in _scorers or []:
            scorers_item = EvalDatasetScorersItem.from_dict(scorers_item_data)

            scorers.append(scorers_item)

        eval_dataset = cls(
            path=path,
            created_at=created_at,
            created_by=created_by,
            edited_at=edited_at,
            edited_by=edited_by,
            summary=summary,
            scorers=scorers,
        )

        eval_dataset.additional_properties = d
        return eval_dataset

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
