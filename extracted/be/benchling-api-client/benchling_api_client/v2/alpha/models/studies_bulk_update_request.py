from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.study_update import StudyUpdate
from ..types import UNSET, Unset

T = TypeVar("T", bound="StudiesBulkUpdateRequest")


@attr.s(auto_attribs=True, repr=False)
class StudiesBulkUpdateRequest:
    """  """

    _studies: Union[Unset, List[StudyUpdate]] = UNSET

    def __repr__(self):
        fields = []
        fields.append("studies={}".format(repr(self._studies)))
        return "StudiesBulkUpdateRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        studies: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._studies, Unset):
            studies = []
            for studies_item_data in self._studies:
                studies_item = studies_item_data.to_dict()

                studies.append(studies_item)

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if studies is not UNSET:
            field_dict["studies"] = studies

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_studies() -> Union[Unset, List[StudyUpdate]]:
            studies = []
            _studies = d.pop("studies")
            for studies_item_data in _studies or []:
                studies_item = StudyUpdate.from_dict(studies_item_data, strict=False)

                studies.append(studies_item)

            return studies

        try:
            studies = get_studies()
        except KeyError:
            if strict:
                raise
            studies = cast(Union[Unset, List[StudyUpdate]], UNSET)

        studies_bulk_update_request = cls(
            studies=studies,
        )

        return studies_bulk_update_request

    @property
    def studies(self) -> List[StudyUpdate]:
        if isinstance(self._studies, Unset):
            raise NotPresentError(self, "studies")
        return self._studies

    @studies.setter
    def studies(self, value: List[StudyUpdate]) -> None:
        self._studies = value

    @studies.deleter
    def studies(self) -> None:
        self._studies = UNSET
