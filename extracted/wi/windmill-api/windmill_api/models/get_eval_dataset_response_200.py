import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_eval_dataset_response_200_scorers_item import GetEvalDatasetResponse200ScorersItem


T = TypeVar("T", bound="GetEvalDatasetResponse200")


@_attrs_define
class GetEvalDatasetResponse200:
    """
    Attributes:
        path (str):
        created_at (datetime.datetime):
        created_by (str):
        edited_at (datetime.datetime):
        edited_by (str):
        summary (Union[Unset, str]):
        scorers (Union[Unset, List['GetEvalDatasetResponse200ScorersItem']]): The columns of the results table, in
            display order.
    """

    path: str
    created_at: datetime.datetime
    created_by: str
    edited_at: datetime.datetime
    edited_by: str
    summary: Union[Unset, str] = UNSET
    scorers: Union[Unset, List["GetEvalDatasetResponse200ScorersItem"]] = UNSET
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
        from ..models.get_eval_dataset_response_200_scorers_item import GetEvalDatasetResponse200ScorersItem

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
            scorers_item = GetEvalDatasetResponse200ScorersItem.from_dict(scorers_item_data)

            scorers.append(scorers_item)

        get_eval_dataset_response_200 = cls(
            path=path,
            created_at=created_at,
            created_by=created_by,
            edited_at=edited_at,
            edited_by=edited_by,
            summary=summary,
            scorers=scorers,
        )

        get_eval_dataset_response_200.additional_properties = d
        return get_eval_dataset_response_200

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
