from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.assay_runs_bulk_create_response_errors import AssayRunsBulkCreateResponseErrors
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayRunsBulkCreateResponse")


@attr.s(auto_attribs=True, repr=False)
class AssayRunsBulkCreateResponse:
    """  """

    _assay_runs: Union[Unset, List[str]] = UNSET
    _errors: Union[Unset, None, AssayRunsBulkCreateResponseErrors] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("assay_runs={}".format(repr(self._assay_runs)))
        fields.append("errors={}".format(repr(self._errors)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AssayRunsBulkCreateResponse({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        assay_runs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._assay_runs, Unset):
            assay_runs = self._assay_runs

        errors: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._errors, Unset):
            errors = self._errors.to_dict() if self._errors else None

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

        def get_assay_runs() -> Union[Unset, List[str]]:
            assay_runs = cast(List[str], d.pop("assayRuns"))

            return assay_runs

        try:
            assay_runs = get_assay_runs()
        except KeyError:
            if strict:
                raise
            assay_runs = cast(Union[Unset, List[str]], UNSET)

        def get_errors() -> Union[Unset, None, AssayRunsBulkCreateResponseErrors]:
            errors = None
            _errors = d.pop("errors")

            if _errors is not None and not isinstance(_errors, Unset):
                errors = AssayRunsBulkCreateResponseErrors.from_dict(_errors)

            return errors

        try:
            errors = get_errors()
        except KeyError:
            if strict:
                raise
            errors = cast(Union[Unset, None, AssayRunsBulkCreateResponseErrors], UNSET)

        assay_runs_bulk_create_response = cls(
            assay_runs=assay_runs,
            errors=errors,
        )

        assay_runs_bulk_create_response.additional_properties = d
        return assay_runs_bulk_create_response

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
    def assay_runs(self) -> List[str]:
        if isinstance(self._assay_runs, Unset):
            raise NotPresentError(self, "assay_runs")
        return self._assay_runs

    @assay_runs.setter
    def assay_runs(self, value: List[str]) -> None:
        self._assay_runs = value

    @assay_runs.deleter
    def assay_runs(self) -> None:
        self._assay_runs = UNSET

    @property
    def errors(self) -> Optional[AssayRunsBulkCreateResponseErrors]:
        if isinstance(self._errors, Unset):
            raise NotPresentError(self, "errors")
        return self._errors

    @errors.setter
    def errors(self, value: Optional[AssayRunsBulkCreateResponseErrors]) -> None:
        self._errors = value

    @errors.deleter
    def errors(self) -> None:
        self._errors = UNSET
