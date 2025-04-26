from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.assay_results_create_response_errors import AssayResultsCreateResponseErrors
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayResultsCreateResponse")


@attr.s(auto_attribs=True, repr=False)
class AssayResultsCreateResponse:
    """  """

    _assay_results: Union[Unset, List[str]] = UNSET
    _errors: Union[Unset, None, AssayResultsCreateResponseErrors] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("assay_results={}".format(repr(self._assay_results)))
        fields.append("errors={}".format(repr(self._errors)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AssayResultsCreateResponse({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        assay_results: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._assay_results, Unset):
            assay_results = self._assay_results

        errors: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._errors, Unset):
            errors = self._errors.to_dict() if self._errors else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if assay_results is not UNSET:
            field_dict["assayResults"] = assay_results
        if errors is not UNSET:
            field_dict["errors"] = errors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_assay_results() -> Union[Unset, List[str]]:
            assay_results = cast(List[str], d.pop("assayResults"))

            return assay_results

        try:
            assay_results = get_assay_results()
        except KeyError:
            if strict:
                raise
            assay_results = cast(Union[Unset, List[str]], UNSET)

        def get_errors() -> Union[Unset, None, AssayResultsCreateResponseErrors]:
            errors = None
            _errors = d.pop("errors")

            if _errors is not None and not isinstance(_errors, Unset):
                errors = AssayResultsCreateResponseErrors.from_dict(_errors)

            return errors

        try:
            errors = get_errors()
        except KeyError:
            if strict:
                raise
            errors = cast(Union[Unset, None, AssayResultsCreateResponseErrors], UNSET)

        assay_results_create_response = cls(
            assay_results=assay_results,
            errors=errors,
        )

        assay_results_create_response.additional_properties = d
        return assay_results_create_response

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
    def assay_results(self) -> List[str]:
        if isinstance(self._assay_results, Unset):
            raise NotPresentError(self, "assay_results")
        return self._assay_results

    @assay_results.setter
    def assay_results(self, value: List[str]) -> None:
        self._assay_results = value

    @assay_results.deleter
    def assay_results(self) -> None:
        self._assay_results = UNSET

    @property
    def errors(self) -> Optional[AssayResultsCreateResponseErrors]:
        if isinstance(self._errors, Unset):
            raise NotPresentError(self, "errors")
        return self._errors

    @errors.setter
    def errors(self, value: Optional[AssayResultsCreateResponseErrors]) -> None:
        self._errors = value

    @errors.deleter
    def errors(self) -> None:
        self._errors = UNSET
