from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.bad_request_error_error import BadRequestErrorError
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListingError")


@attr.s(auto_attribs=True, repr=False)
class ListingError:
    """  """

    _invalid_ids: Union[Unset, List[str]] = UNSET
    _error: Union[Unset, BadRequestErrorError] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("invalid_ids={}".format(repr(self._invalid_ids)))
        fields.append("error={}".format(repr(self._error)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "ListingError({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        invalid_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._invalid_ids, Unset):
            invalid_ids = self._invalid_ids

        error: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._error, Unset):
            error = self._error.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if invalid_ids is not UNSET:
            field_dict["invalidIds"] = invalid_ids
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_invalid_ids() -> Union[Unset, List[str]]:
            invalid_ids = cast(List[str], d.pop("invalidIds"))

            return invalid_ids

        try:
            invalid_ids = get_invalid_ids()
        except KeyError:
            if strict:
                raise
            invalid_ids = cast(Union[Unset, List[str]], UNSET)

        def get_error() -> Union[Unset, BadRequestErrorError]:
            error: Union[Unset, Union[Unset, BadRequestErrorError]] = UNSET
            _error = d.pop("error")

            if not isinstance(_error, Unset):
                error = BadRequestErrorError.from_dict(_error)

            return error

        try:
            error = get_error()
        except KeyError:
            if strict:
                raise
            error = cast(Union[Unset, BadRequestErrorError], UNSET)

        listing_error = cls(
            invalid_ids=invalid_ids,
            error=error,
        )

        listing_error.additional_properties = d
        return listing_error

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
    def invalid_ids(self) -> List[str]:
        if isinstance(self._invalid_ids, Unset):
            raise NotPresentError(self, "invalid_ids")
        return self._invalid_ids

    @invalid_ids.setter
    def invalid_ids(self, value: List[str]) -> None:
        self._invalid_ids = value

    @invalid_ids.deleter
    def invalid_ids(self) -> None:
        self._invalid_ids = UNSET

    @property
    def error(self) -> BadRequestErrorError:
        if isinstance(self._error, Unset):
            raise NotPresentError(self, "error")
        return self._error

    @error.setter
    def error(self, value: BadRequestErrorError) -> None:
        self._error = value

    @error.deleter
    def error(self) -> None:
        self._error = UNSET
