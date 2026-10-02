from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.resolved_form_response_dto_resolved_type_0 import ResolvedFormResponseDtoResolvedType0





T = TypeVar("T", bound="ResolvedFormResponseDto")



@_attrs_define
class ResolvedFormResponseDto:
    """ Response wrapping the form that applies to the current scope after inheritance resolution.

        Example:
            {'resolved': {'form': {'id': '8f0a9cbe-5235-412f-b4b9-8241d4099661', 'title': 'Defect Severity Rubric',
                'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt': '2026-01-16T14:20:00.000Z'}, 'formVersion': {'id':
                '77e4ffc9-3d40-472c-b160-f163e02df324', 'formId': '8f0a9cbe-5235-412f-b4b9-8241d4099661', 'versionNumber': 1,
                'schema': {'data': {'type': 'object', 'required': ['severity'], 'properties': {'severity': {'type': 'string',
                'title': 'Defect severity', 'enum': ['none', 'minor', 'major', 'critical']}, 'notes': {'type': 'string',
                'title': 'Reviewer notes'}}}, 'ui': {'severity': {'ui:widget': 'radio'}, 'notes': {'ui:widget': 'textarea'}}},
                'publishedAt': '2026-01-16T14:20:00.000Z', 'publishedByUserId': '49dea803-7390-49c4-abb1-5629718fc9cd',
                'updatedByUserId': '49dea803-7390-49c4-abb1-5629718fc9cd', 'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt':
                '2026-01-16T14:20:00.000Z'}, 'scope': 'problem', 'ownerScope': 'organization'}}

        Attributes:
            resolved (None | ResolvedFormResponseDtoResolvedType0): The form resolved for the requested scope, or null when
                no form applies.
     """

    resolved: None | ResolvedFormResponseDtoResolvedType0





    def to_dict(self) -> dict[str, Any]:
        from ..models.resolved_form_response_dto_resolved_type_0 import ResolvedFormResponseDtoResolvedType0 # noqa: PLC0415
        resolved: dict[str, Any] | None
        if isinstance(self.resolved, ResolvedFormResponseDtoResolvedType0):
            resolved = self.resolved.to_dict()
        else:
            resolved = self.resolved


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "resolved": resolved,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resolved_form_response_dto_resolved_type_0 import ResolvedFormResponseDtoResolvedType0 # noqa: PLC0415
        d = dict(src_dict)
        def _parse_resolved(data: object) -> None | ResolvedFormResponseDtoResolvedType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                resolved_type_0 = ResolvedFormResponseDtoResolvedType0.from_dict(data)



                return resolved_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ResolvedFormResponseDtoResolvedType0, data)

        resolved = _parse_resolved(d.pop("resolved"))


        resolved_form_response_dto = cls(
            resolved=resolved,
        )

        return resolved_form_response_dto

