from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.assay_results_create_error_response_assay_results_item import (
    AssayResultsCreateErrorResponseAssayResultsItem,
)
from ..models.assay_results_create_error_response_errors_item import AssayResultsCreateErrorResponseErrorsItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayResultsCreateErrorResponse")


@attr.s(auto_attribs=True, repr=False)
class AssayResultsCreateErrorResponse:
    """  """

    _assay_results: Union[Unset, None, List[AssayResultsCreateErrorResponseAssayResultsItem]] = UNSET
    _errors: Union[Unset, List[AssayResultsCreateErrorResponseErrorsItem]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("assay_results={}".format(repr(self._assay_results)))
        fields.append("errors={}".format(repr(self._errors)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AssayResultsCreateErrorResponse({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        assay_results: Union[Unset, None, List[Any]] = UNSET
        if not isinstance(self._assay_results, Unset):
            if self._assay_results is None:
                assay_results = None
            else:
                assay_results = []
                for assay_results_item_data in self._assay_results:
                    assay_results_item = assay_results_item_data.to_dict()

                    assay_results.append(assay_results_item)

        errors: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._errors, Unset):
            errors = []
            for errors_item_data in self._errors:
                errors_item = errors_item_data.to_dict()

                errors.append(errors_item)

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

        def get_assay_results() -> Union[Unset, None, List[AssayResultsCreateErrorResponseAssayResultsItem]]:
            assay_results = []
            _assay_results = d.pop("assayResults")
            for assay_results_item_data in _assay_results or []:
                assay_results_item = AssayResultsCreateErrorResponseAssayResultsItem.from_dict(
                    assay_results_item_data, strict=False
                )

                assay_results.append(assay_results_item)

            return assay_results

        try:
            assay_results = get_assay_results()
        except KeyError:
            if strict:
                raise
            assay_results = cast(
                Union[Unset, None, List[AssayResultsCreateErrorResponseAssayResultsItem]], UNSET
            )

        def get_errors() -> Union[Unset, List[AssayResultsCreateErrorResponseErrorsItem]]:
            errors = []
            _errors = d.pop("errors")
            for errors_item_data in _errors or []:
                errors_item = AssayResultsCreateErrorResponseErrorsItem.from_dict(
                    errors_item_data, strict=False
                )

                errors.append(errors_item)

            return errors

        try:
            errors = get_errors()
        except KeyError:
            if strict:
                raise
            errors = cast(Union[Unset, List[AssayResultsCreateErrorResponseErrorsItem]], UNSET)

        assay_results_create_error_response = cls(
            assay_results=assay_results,
            errors=errors,
        )

        assay_results_create_error_response.additional_properties = d
        return assay_results_create_error_response

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
    def assay_results(self) -> Optional[List[AssayResultsCreateErrorResponseAssayResultsItem]]:
        if isinstance(self._assay_results, Unset):
            raise NotPresentError(self, "assay_results")
        return self._assay_results

    @assay_results.setter
    def assay_results(self, value: Optional[List[AssayResultsCreateErrorResponseAssayResultsItem]]) -> None:
        self._assay_results = value

    @assay_results.deleter
    def assay_results(self) -> None:
        self._assay_results = UNSET

    @property
    def errors(self) -> List[AssayResultsCreateErrorResponseErrorsItem]:
        if isinstance(self._errors, Unset):
            raise NotPresentError(self, "errors")
        return self._errors

    @errors.setter
    def errors(self, value: List[AssayResultsCreateErrorResponseErrorsItem]) -> None:
        self._errors = value

    @errors.deleter
    def errors(self) -> None:
        self._errors = UNSET
