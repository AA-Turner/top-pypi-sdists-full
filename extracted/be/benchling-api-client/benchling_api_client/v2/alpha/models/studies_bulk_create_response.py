from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.study import Study
from ..types import UNSET, Unset

T = TypeVar("T", bound="StudiesBulkCreateResponse")


@attr.s(auto_attribs=True, repr=False)
class StudiesBulkCreateResponse:
    """  """

    _studies: Union[Unset, List[Study]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("studies={}".format(repr(self._studies)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "StudiesBulkCreateResponse({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        studies: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._studies, Unset):
            studies = []
            for studies_item_data in self._studies:
                studies_item = studies_item_data.to_dict()

                studies.append(studies_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if studies is not UNSET:
            field_dict["studies"] = studies

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

        studies_bulk_create_response = cls(
            studies=studies,
        )

        studies_bulk_create_response.additional_properties = d
        return studies_bulk_create_response

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
    def studies(self) -> List[Study]:
        """ The created studies """
        if isinstance(self._studies, Unset):
            raise NotPresentError(self, "studies")
        return self._studies

    @studies.setter
    def studies(self, value: List[Study]) -> None:
        self._studies = value

    @studies.deleter
    def studies(self) -> None:
        self._studies = UNSET
