from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.env_form_bundle_response_dto_owner_scope_type_0 import EnvFormBundleResponseDtoOwnerScopeType0
from typing import cast

if TYPE_CHECKING:
  from ..models.env_form_bundle_response_dto_form_type_0 import EnvFormBundleResponseDtoFormType0





T = TypeVar("T", bound="EnvFormBundleResponseDto")



@_attrs_define
class EnvFormBundleResponseDto:
    """ Response describing the form currently attached at the environment scope, along with its higher-scope owner marker.

        Example:
            {'form': {'id': '8f0a9cbe-5235-412f-b4b9-8241d4099661', 'title': 'Defect Severity Rubric', 'createdAt':
                '2026-01-15T09:30:00.000Z', 'updatedAt': '2026-01-16T14:20:00.000Z'}, 'ownerScope': 'organization'}

        Attributes:
            form (EnvFormBundleResponseDtoFormType0 | None): The attached form bundle, or null when none is attached.
            owner_scope (EnvFormBundleResponseDtoOwnerScopeType0 | None): Higher-scope owner of the bundle, or null when
                none is attached or when it is owned locally.
     """

    form: EnvFormBundleResponseDtoFormType0 | None
    owner_scope: EnvFormBundleResponseDtoOwnerScopeType0 | None





    def to_dict(self) -> dict[str, Any]:
        from ..models.env_form_bundle_response_dto_form_type_0 import EnvFormBundleResponseDtoFormType0 # noqa: PLC0415
        form: dict[str, Any] | None
        if isinstance(self.form, EnvFormBundleResponseDtoFormType0):
            form = self.form.to_dict()
        else:
            form = self.form

        owner_scope: None | str
        if isinstance(self.owner_scope, EnvFormBundleResponseDtoOwnerScopeType0):
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
        from ..models.env_form_bundle_response_dto_form_type_0 import EnvFormBundleResponseDtoFormType0 # noqa: PLC0415
        d = dict(src_dict)
        def _parse_form(data: object) -> EnvFormBundleResponseDtoFormType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                form_type_0 = EnvFormBundleResponseDtoFormType0.from_dict(data)



                return form_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EnvFormBundleResponseDtoFormType0 | None, data)

        form = _parse_form(d.pop("form"))


        def _parse_owner_scope(data: object) -> EnvFormBundleResponseDtoOwnerScopeType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                owner_scope_type_0 = EnvFormBundleResponseDtoOwnerScopeType0(data)



                return owner_scope_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EnvFormBundleResponseDtoOwnerScopeType0 | None, data)

        owner_scope = _parse_owner_scope(d.pop("ownerScope"))


        env_form_bundle_response_dto = cls(
            form=form,
            owner_scope=owner_scope,
        )

        return env_form_bundle_response_dto

