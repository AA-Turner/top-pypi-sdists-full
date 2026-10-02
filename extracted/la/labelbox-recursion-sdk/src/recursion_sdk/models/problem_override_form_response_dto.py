from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.problem_override_form_response_dto_owner_scope_type_0 import ProblemOverrideFormResponseDtoOwnerScopeType0
from typing import cast

if TYPE_CHECKING:
  from ..models.problem_override_form_response_dto_form_type_0 import ProblemOverrideFormResponseDtoFormType0





T = TypeVar("T", bound="ProblemOverrideFormResponseDto")



@_attrs_define
class ProblemOverrideFormResponseDto:
    """ Response describing the form override attached at the problem scope, along with its higher-scope owner marker.

        Example:
            {'form': {'id': '8f0a9cbe-5235-412f-b4b9-8241d4099661', 'title': 'Defect Severity Rubric', 'createdAt':
                '2026-01-15T09:30:00.000Z', 'updatedAt': '2026-01-16T14:20:00.000Z'}, 'ownerScope': 'organization'}

        Attributes:
            form (None | ProblemOverrideFormResponseDtoFormType0): The attached form bundle, or null when none is attached.
            owner_scope (None | ProblemOverrideFormResponseDtoOwnerScopeType0): Higher-scope owner of the bundle, or null
                when none is attached or when it is owned locally.
     """

    form: None | ProblemOverrideFormResponseDtoFormType0
    owner_scope: None | ProblemOverrideFormResponseDtoOwnerScopeType0





    def to_dict(self) -> dict[str, Any]:
        from ..models.problem_override_form_response_dto_form_type_0 import ProblemOverrideFormResponseDtoFormType0 # noqa: PLC0415
        form: dict[str, Any] | None
        if isinstance(self.form, ProblemOverrideFormResponseDtoFormType0):
            form = self.form.to_dict()
        else:
            form = self.form

        owner_scope: None | str
        if isinstance(self.owner_scope, ProblemOverrideFormResponseDtoOwnerScopeType0):
            owner_scope = self.owner_scope.value
        else:
            owner_scope = self.owner_scope


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "form": form,
            "ownerScope": owner_scope,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.problem_override_form_response_dto_form_type_0 import ProblemOverrideFormResponseDtoFormType0 # noqa: PLC0415
        d = dict(src_dict)
        def _parse_form(data: object) -> None | ProblemOverrideFormResponseDtoFormType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                form_type_0 = ProblemOverrideFormResponseDtoFormType0.from_dict(data)



                return form_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProblemOverrideFormResponseDtoFormType0, data)

        form = _parse_form(d.pop("form"))


        def _parse_owner_scope(data: object) -> None | ProblemOverrideFormResponseDtoOwnerScopeType0:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                owner_scope_type_0 = ProblemOverrideFormResponseDtoOwnerScopeType0(data)



                return owner_scope_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProblemOverrideFormResponseDtoOwnerScopeType0, data)

        owner_scope = _parse_owner_scope(d.pop("ownerScope"))


        problem_override_form_response_dto = cls(
            form=form,
            owner_scope=owner_scope,
        )

        return problem_override_form_response_dto

