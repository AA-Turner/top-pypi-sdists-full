from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.assay_results_create_error_response_errors_item_fields import (
    AssayResultsCreateErrorResponseErrorsItemFields,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayResultsCreateErrorResponseErrorsItem")


@attr.s(auto_attribs=True, repr=False)
class AssayResultsCreateErrorResponseErrorsItem:
    """  """

    _fields: Union[Unset, AssayResultsCreateErrorResponseErrorsItemFields] = UNSET
    _global_: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("fields={}".format(repr(self._fields)))
        fields.append("global_={}".format(repr(self._global_)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AssayResultsCreateErrorResponseErrorsItem({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._fields, Unset):
            fields = self._fields.to_dict()

        global_: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._global_, Unset):
            global_ = self._global_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if fields is not UNSET:
            field_dict["fields"] = fields
        if global_ is not UNSET:
            field_dict["global"] = global_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_fields() -> Union[Unset, AssayResultsCreateErrorResponseErrorsItemFields]:
            fields: Union[Unset, Union[Unset, AssayResultsCreateErrorResponseErrorsItemFields]] = UNSET
            _fields = d.pop("fields")

            if not isinstance(_fields, Unset):
                fields = AssayResultsCreateErrorResponseErrorsItemFields.from_dict(_fields)

            return fields

        try:
            fields = get_fields()
        except KeyError:
            if strict:
                raise
            fields = cast(Union[Unset, AssayResultsCreateErrorResponseErrorsItemFields], UNSET)

        def get_global_() -> Union[Unset, List[str]]:
            global_ = cast(List[str], d.pop("global"))

            return global_

        try:
            global_ = get_global_()
        except KeyError:
            if strict:
                raise
            global_ = cast(Union[Unset, List[str]], UNSET)

        assay_results_create_error_response_errors_item = cls(
            fields=fields,
            global_=global_,
        )

        assay_results_create_error_response_errors_item.additional_properties = d
        return assay_results_create_error_response_errors_item

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
    def fields(self) -> AssayResultsCreateErrorResponseErrorsItemFields:
        if isinstance(self._fields, Unset):
            raise NotPresentError(self, "fields")
        return self._fields

    @fields.setter
    def fields(self, value: AssayResultsCreateErrorResponseErrorsItemFields) -> None:
        self._fields = value

    @fields.deleter
    def fields(self) -> None:
        self._fields = UNSET

    @property
    def global_(self) -> List[str]:
        if isinstance(self._global_, Unset):
            raise NotPresentError(self, "global_")
        return self._global_

    @global_.setter
    def global_(self, value: List[str]) -> None:
        self._global_ = value

    @global_.deleter
    def global_(self) -> None:
        self._global_ = UNSET
