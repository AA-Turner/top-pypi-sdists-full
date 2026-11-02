from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_eval_dataset_json_body_scorers_item_kind import CreateEvalDatasetJsonBodyScorersItemKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateEvalDatasetJsonBodyScorersItem")


@_attrs_define
class CreateEvalDatasetJsonBodyScorersItem:
    """A scorer is a column of the results table, and it is always a runnable: an ai_agent resource sent the run to grade,
    or a script handed the run as an argument. `id` is assigned when the scorer is added to a dataset and never reused:
    it is what makes a column the same column across experiments when the scorer is renamed, and a delta is only ever
    computed between two scores carrying the same id. A scorer sent without an id is given one.

        Attributes:
            kind (CreateEvalDatasetJsonBodyScorersItemKind):
            path (str): The script, or the ai_agent resource used as a judge.
            id (Union[Unset, str]):
            name (Union[Unset, str]): Column header. Defaults to the last segment of the path.
            pass_if (Union[Unset, float]): A score at or above this counts as a pass, and the column reports a pass rate
                beside its mean. Applied when results are read rather than when they are produced, so moving the line re-reads
                every score already recorded instead of invalidating them.
    """

    kind: CreateEvalDatasetJsonBodyScorersItemKind
    path: str
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    pass_if: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        path = self.path
        id = self.id
        name = self.name
        pass_if = self.pass_if

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "path": path,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if pass_if is not UNSET:
            field_dict["pass_if"] = pass_if

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        kind = CreateEvalDatasetJsonBodyScorersItemKind(d.pop("kind"))

        path = d.pop("path")

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        pass_if = d.pop("pass_if", UNSET)

        create_eval_dataset_json_body_scorers_item = cls(
            kind=kind,
            path=path,
            id=id,
            name=name,
            pass_if=pass_if,
        )

        create_eval_dataset_json_body_scorers_item.additional_properties = d
        return create_eval_dataset_json_body_scorers_item

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
