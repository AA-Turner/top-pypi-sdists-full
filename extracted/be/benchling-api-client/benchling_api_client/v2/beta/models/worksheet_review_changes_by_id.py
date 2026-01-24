from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.worksheet_review_changes import WorksheetReviewChanges
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorksheetReviewChangesById")


@attr.s(auto_attribs=True, repr=False)
class WorksheetReviewChangesById:
    """  """

    _worksheet: Union[Unset, WorksheetReviewChanges] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("worksheet={}".format(repr(self._worksheet)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "WorksheetReviewChangesById({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        worksheet: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._worksheet, Unset):
            worksheet = self._worksheet.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if worksheet is not UNSET:
            field_dict["worksheet"] = worksheet

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_worksheet() -> Union[Unset, WorksheetReviewChanges]:
            worksheet: Union[Unset, Union[Unset, WorksheetReviewChanges]] = UNSET
            _worksheet = d.pop("worksheet")

            if not isinstance(_worksheet, Unset):
                worksheet = WorksheetReviewChanges.from_dict(_worksheet)

            return worksheet

        try:
            worksheet = get_worksheet()
        except KeyError:
            if strict:
                raise
            worksheet = cast(Union[Unset, WorksheetReviewChanges], UNSET)

        worksheet_review_changes_by_id = cls(
            worksheet=worksheet,
        )

        worksheet_review_changes_by_id.additional_properties = d
        return worksheet_review_changes_by_id

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

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def worksheet(self) -> WorksheetReviewChanges:
        """Contents include basic worksheet metadata along with its review changes, including any snapshot information if present."""
        if isinstance(self._worksheet, Unset):
            raise NotPresentError(self, "worksheet")
        return self._worksheet

    @worksheet.setter
    def worksheet(self, value: WorksheetReviewChanges) -> None:
        self._worksheet = value

    @worksheet.deleter
    def worksheet(self) -> None:
        self._worksheet = UNSET
