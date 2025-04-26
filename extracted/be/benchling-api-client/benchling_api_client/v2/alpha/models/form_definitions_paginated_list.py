from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.form_definition import FormDefinition
from ..types import UNSET, Unset

T = TypeVar("T", bound="FormDefinitionsPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class FormDefinitionsPaginatedList:
    """  """

    _form_definitions: Union[Unset, List[FormDefinition]] = UNSET
    _next_token: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("form_definitions={}".format(repr(self._form_definitions)))
        fields.append("next_token={}".format(repr(self._next_token)))
        return "FormDefinitionsPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        form_definitions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._form_definitions, Unset):
            form_definitions = []
            for form_definitions_item_data in self._form_definitions:
                form_definitions_item = form_definitions_item_data.to_dict()

                form_definitions.append(form_definitions_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if form_definitions is not UNSET:
            field_dict["formDefinitions"] = form_definitions
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_form_definitions() -> Union[Unset, List[FormDefinition]]:
            form_definitions = []
            _form_definitions = d.pop("formDefinitions")
            for form_definitions_item_data in _form_definitions or []:
                form_definitions_item = FormDefinition.from_dict(form_definitions_item_data, strict=False)

                form_definitions.append(form_definitions_item)

            return form_definitions

        try:
            form_definitions = get_form_definitions()
        except KeyError:
            if strict:
                raise
            form_definitions = cast(Union[Unset, List[FormDefinition]], UNSET)

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        form_definitions_paginated_list = cls(
            form_definitions=form_definitions,
            next_token=next_token,
        )

        return form_definitions_paginated_list

    @property
    def form_definitions(self) -> List[FormDefinition]:
        if isinstance(self._form_definitions, Unset):
            raise NotPresentError(self, "form_definitions")
        return self._form_definitions

    @form_definitions.setter
    def form_definitions(self, value: List[FormDefinition]) -> None:
        self._form_definitions = value

    @form_definitions.deleter
    def form_definitions(self) -> None:
        self._form_definitions = UNSET

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
