from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.resolved_form_response_dto_resolved_type_0_owner_scope_type_0 import ResolvedFormResponseDtoResolvedType0OwnerScopeType0
from ..models.resolved_form_response_dto_resolved_type_0_scope import ResolvedFormResponseDtoResolvedType0Scope
from typing import cast

if TYPE_CHECKING:
  from ..models.resolved_form_response_dto_resolved_type_0_form import ResolvedFormResponseDtoResolvedType0Form
  from ..models.resolved_form_response_dto_resolved_type_0_form_version import ResolvedFormResponseDtoResolvedType0FormVersion





T = TypeVar("T", bound="ResolvedFormResponseDtoResolvedType0")



@_attrs_define
class ResolvedFormResponseDtoResolvedType0:
    """ Form resolved for a specific problem after walking the problem-then-environment cascade.

        Attributes:
            form (ResolvedFormResponseDtoResolvedType0Form): The form record that won the scope resolution cascade.
            form_version (ResolvedFormResponseDtoResolvedType0FormVersion): The specific version of the form to use.
            scope (ResolvedFormResponseDtoResolvedType0Scope): Which scope level won the resolver cascade for this problem.
            owner_scope (None | ResolvedFormResponseDtoResolvedType0OwnerScopeType0): Higher-scope owner of the resolved
                bundle, or null when it is owned locally at its attached scope.
     """

    form: ResolvedFormResponseDtoResolvedType0Form
    form_version: ResolvedFormResponseDtoResolvedType0FormVersion
    scope: ResolvedFormResponseDtoResolvedType0Scope
    owner_scope: None | ResolvedFormResponseDtoResolvedType0OwnerScopeType0





    def to_dict(self) -> dict[str, Any]:
        from ..models.resolved_form_response_dto_resolved_type_0_form import ResolvedFormResponseDtoResolvedType0Form # noqa: PLC0415
        from ..models.resolved_form_response_dto_resolved_type_0_form_version import ResolvedFormResponseDtoResolvedType0FormVersion # noqa: PLC0415
        form = self.form.to_dict()

        form_version = self.form_version.to_dict()

        scope = self.scope.value

        owner_scope: None | str
        if isinstance(self.owner_scope, ResolvedFormResponseDtoResolvedType0OwnerScopeType0):
            owner_scope = self.owner_scope.value
        else:
            owner_scope = self.owner_scope


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "form": form,
            "formVersion": form_version,
            "scope": scope,
            "ownerScope": owner_scope,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resolved_form_response_dto_resolved_type_0_form import ResolvedFormResponseDtoResolvedType0Form # noqa: PLC0415
        from ..models.resolved_form_response_dto_resolved_type_0_form_version import ResolvedFormResponseDtoResolvedType0FormVersion # noqa: PLC0415
        d = dict(src_dict)
        form = ResolvedFormResponseDtoResolvedType0Form.from_dict(d.pop("form"))




        form_version = ResolvedFormResponseDtoResolvedType0FormVersion.from_dict(d.pop("formVersion"))




        scope = ResolvedFormResponseDtoResolvedType0Scope(d.pop("scope"))




        def _parse_owner_scope(data: object) -> None | ResolvedFormResponseDtoResolvedType0OwnerScopeType0:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                owner_scope_type_0 = ResolvedFormResponseDtoResolvedType0OwnerScopeType0(data)



                return owner_scope_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ResolvedFormResponseDtoResolvedType0OwnerScopeType0, data)

        owner_scope = _parse_owner_scope(d.pop("ownerScope"))


        resolved_form_response_dto_resolved_type_0 = cls(
            form=form,
            form_version=form_version,
            scope=scope,
            owner_scope=owner_scope,
        )

        return resolved_form_response_dto_resolved_type_0

