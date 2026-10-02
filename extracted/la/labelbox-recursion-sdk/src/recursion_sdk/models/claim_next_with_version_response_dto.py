from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.claim_next_with_version_response_dto_problem import ClaimNextWithVersionResponseDtoProblem
  from ..models.claim_next_with_version_response_dto_version import ClaimNextWithVersionResponseDtoVersion





T = TypeVar("T", bound="ClaimNextWithVersionResponseDto")



@_attrs_define
class ClaimNextWithVersionResponseDto:
    """ Response for claim-next-with-version, bundling the problem, its initial version, and a created flag.

        Attributes:
            problem (ClaimNextWithVersionResponseDtoProblem): The claimed problem.
            version (ClaimNextWithVersionResponseDtoVersion): The initial version associated with the claimed problem.
            created (bool): True when a new problem was created (201); false when an existing one was returned (200).
     """

    problem: ClaimNextWithVersionResponseDtoProblem
    version: ClaimNextWithVersionResponseDtoVersion
    created: bool





    def to_dict(self) -> dict[str, Any]:
        from ..models.claim_next_with_version_response_dto_problem import ClaimNextWithVersionResponseDtoProblem # noqa: PLC0415
        from ..models.claim_next_with_version_response_dto_version import ClaimNextWithVersionResponseDtoVersion # noqa: PLC0415
        problem = self.problem.to_dict()

        version = self.version.to_dict()

        created = self.created


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "problem": problem,
            "version": version,
            "created": created,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.claim_next_with_version_response_dto_problem import ClaimNextWithVersionResponseDtoProblem # noqa: PLC0415
        from ..models.claim_next_with_version_response_dto_version import ClaimNextWithVersionResponseDtoVersion # noqa: PLC0415
        d = dict(src_dict)
        problem = ClaimNextWithVersionResponseDtoProblem.from_dict(d.pop("problem"))




        version = ClaimNextWithVersionResponseDtoVersion.from_dict(d.pop("version"))




        created = d.pop("created")

        claim_next_with_version_response_dto = cls(
            problem=problem,
            version=version,
            created=created,
        )

        return claim_next_with_version_response_dto

