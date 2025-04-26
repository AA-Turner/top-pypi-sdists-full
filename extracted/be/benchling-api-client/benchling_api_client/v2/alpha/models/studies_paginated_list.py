from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.study import Study
from ..types import UNSET, Unset

T = TypeVar("T", bound="StudiesPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class StudiesPaginatedList:
    """  """

    _studies: Union[Unset, List[Study]] = UNSET
    _next_token: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("studies={}".format(repr(self._studies)))
        fields.append("next_token={}".format(repr(self._next_token)))
        return "StudiesPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        studies: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._studies, Unset):
            studies = []
            for studies_item_data in self._studies:
                studies_item = studies_item_data.to_dict()

                studies.append(studies_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if studies is not UNSET:
            field_dict["studies"] = studies
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_studies() -> Union[Unset, List[Study]]:
            studies = []
            _studies = d.pop("studies")
            for studies_item_data in _studies or []:
                studies_item = Study.from_dict(studies_item_data, strict=False)

                studies.append(studies_item)

            return studies

        try:
            studies = get_studies()
        except KeyError:
            if strict:
                raise
            studies = cast(Union[Unset, List[Study]], UNSET)

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        studies_paginated_list = cls(
            studies=studies,
            next_token=next_token,
        )

        return studies_paginated_list

    @property
    def studies(self) -> List[Study]:
        if isinstance(self._studies, Unset):
            raise NotPresentError(self, "studies")
        return self._studies

    @studies.setter
    def studies(self, value: List[Study]) -> None:
        self._studies = value

    @studies.deleter
    def studies(self) -> None:
        self._studies = UNSET

    @property
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET
