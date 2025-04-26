from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.assay_runs_bulk_create_error_response_assay_runs_item import (
    AssayRunsBulkCreateErrorResponseAssayRunsItem,
)
from ..models.assay_runs_bulk_create_error_response_errors_item import (
    AssayRunsBulkCreateErrorResponseErrorsItem,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayRunsBulkCreateErrorResponse")


@attr.s(auto_attribs=True, repr=False)
class AssayRunsBulkCreateErrorResponse:
    """  """

    _assay_runs: Union[Unset, None, List[AssayRunsBulkCreateErrorResponseAssayRunsItem]] = UNSET
    _errors: Union[Unset, List[AssayRunsBulkCreateErrorResponseErrorsItem]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("assay_runs={}".format(repr(self._assay_runs)))
        fields.append("errors={}".format(repr(self._errors)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AssayRunsBulkCreateErrorResponse({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        assay_runs: Union[Unset, None, List[Any]] = UNSET
        if not isinstance(self._assay_runs, Unset):
            if self._assay_runs is None:
                assay_runs = None
            else:
                assay_runs = []
                for assay_runs_item_data in self._assay_runs:
                    assay_runs_item = assay_runs_item_data.to_dict()

                    assay_runs.append(assay_runs_item)

        errors: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._errors, Unset):
            errors = []
            for errors_item_data in self._errors:
                errors_item = errors_item_data.to_dict()

                errors.append(errors_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if assay_runs is not UNSET:
            field_dict["assayRuns"] = assay_runs
        if errors is not UNSET:
            field_dict["errors"] = errors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_assay_runs() -> Union[Unset, None, List[AssayRunsBulkCreateErrorResponseAssayRunsItem]]:
            assay_runs = []
            _assay_runs = d.pop("assayRuns")
            for assay_runs_item_data in _assay_runs or []:
                assay_runs_item = AssayRunsBulkCreateErrorResponseAssayRunsItem.from_dict(
                    assay_runs_item_data, strict=False
                )

                assay_runs.append(assay_runs_item)

            return assay_runs

        try:
            assay_runs = get_assay_runs()
        except KeyError:
            if strict:
                raise
            assay_runs = cast(Union[Unset, None, List[AssayRunsBulkCreateErrorResponseAssayRunsItem]], UNSET)

        def get_errors() -> Union[Unset, List[AssayRunsBulkCreateErrorResponseErrorsItem]]:
            errors = []
            _errors = d.pop("errors")
            for errors_item_data in _errors or []:
                errors_item = AssayRunsBulkCreateErrorResponseErrorsItem.from_dict(
                    errors_item_data, strict=False
                )

                errors.append(errors_item)

            return errors

        try:
            errors = get_errors()
        except KeyError:
            if strict:
                raise
            errors = cast(Union[Unset, List[AssayRunsBulkCreateErrorResponseErrorsItem]], UNSET)

        assay_runs_bulk_create_error_response = cls(
            assay_runs=assay_runs,
            errors=errors,
        )

        assay_runs_bulk_create_error_response.additional_properties = d
        return assay_runs_bulk_create_error_response

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
    def assay_runs(self) -> Optional[List[AssayRunsBulkCreateErrorResponseAssayRunsItem]]:
        if isinstance(self._assay_runs, Unset):
            raise NotPresentError(self, "assay_runs")
        return self._assay_runs

    @assay_runs.setter
    def assay_runs(self, value: Optional[List[AssayRunsBulkCreateErrorResponseAssayRunsItem]]) -> None:
        self._assay_runs = value

    @assay_runs.deleter
    def assay_runs(self) -> None:
        self._assay_runs = UNSET

    @property
    def errors(self) -> List[AssayRunsBulkCreateErrorResponseErrorsItem]:
        if isinstance(self._errors, Unset):
            raise NotPresentError(self, "errors")
        return self._errors

    @errors.setter
    def errors(self, value: List[AssayRunsBulkCreateErrorResponseErrorsItem]) -> None:
        self._errors = value

    @errors.deleter
    def errors(self) -> None:
        self._errors = UNSET
