from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.free_form_text_form_field_canned_responses_behavior import (
    FreeFormTextFormFieldCannedResponsesBehavior,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="FreeFormTextFormFieldCannedResponses")


@attr.s(auto_attribs=True, repr=False)
class FreeFormTextFormFieldCannedResponses:
    """  """

    _behavior: Union[Unset, FreeFormTextFormFieldCannedResponsesBehavior] = UNSET
    _values: Union[Unset, List[str]] = UNSET

    def __repr__(self):
        fields = []
        fields.append("behavior={}".format(repr(self._behavior)))
        fields.append("values={}".format(repr(self._values)))
        return "FreeFormTextFormFieldCannedResponses({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        behavior: Union[Unset, int] = UNSET
        if not isinstance(self._behavior, Unset):
            behavior = self._behavior.value

        values: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._values, Unset):
            values = self._values

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if behavior is not UNSET:
            field_dict["behavior"] = behavior
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_behavior() -> Union[Unset, FreeFormTextFormFieldCannedResponsesBehavior]:
            behavior = UNSET
            _behavior = d.pop("behavior")
            if _behavior is not None and _behavior is not UNSET:
                try:
                    behavior = FreeFormTextFormFieldCannedResponsesBehavior(_behavior)
                except ValueError:
                    behavior = FreeFormTextFormFieldCannedResponsesBehavior.of_unknown(_behavior)

            return behavior

        try:
            behavior = get_behavior()
        except KeyError:
            if strict:
                raise
            behavior = cast(Union[Unset, FreeFormTextFormFieldCannedResponsesBehavior], UNSET)

        def get_values() -> Union[Unset, List[str]]:
            values = cast(List[str], d.pop("values"))

            return values

        try:
            values = get_values()
        except KeyError:
            if strict:
                raise
            values = cast(Union[Unset, List[str]], UNSET)

        free_form_text_form_field_canned_responses = cls(
            behavior=behavior,
            values=values,
        )

        return free_form_text_form_field_canned_responses

    @property
    def behavior(self) -> FreeFormTextFormFieldCannedResponsesBehavior:
        if isinstance(self._behavior, Unset):
            raise NotPresentError(self, "behavior")
        return self._behavior

    @behavior.setter
    def behavior(self, value: FreeFormTextFormFieldCannedResponsesBehavior) -> None:
        self._behavior = value

    @behavior.deleter
    def behavior(self) -> None:
        self._behavior = UNSET

    @property
    def values(self) -> List[str]:
        if isinstance(self._values, Unset):
            raise NotPresentError(self, "values")
        return self._values

    @values.setter
    def values(self, value: List[str]) -> None:
        self._values = value

    @values.deleter
    def values(self) -> None:
        self._values = UNSET
