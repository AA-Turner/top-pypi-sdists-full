from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID






T = TypeVar("T", bound="ComputeAlreadyActiveBodyDtoDetails")



@_attrs_define
class ComputeAlreadyActiveBodyDtoDetails:
    """ Identifiers clients use to resume or inspect the compute that is already active.

        Attributes:
            existing_compute_id (UUID): Identifier of the compute the caller already holds in this environment.
            run_config_version_id (None | UUID): Run-config version the existing compute was created from; null when none
                was associated.
     """

    existing_compute_id: UUID
    run_config_version_id: None | UUID





    def to_dict(self) -> dict[str, Any]:
        existing_compute_id = str(self.existing_compute_id)

        run_config_version_id: None | str
        if isinstance(self.run_config_version_id, UUID):
            run_config_version_id = str(self.run_config_version_id)
        else:
            run_config_version_id = self.run_config_version_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "existingComputeId": existing_compute_id,
            "runConfigVersionId": run_config_version_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        existing_compute_id = UUID(d.pop("existingComputeId"))




        def _parse_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                run_config_version_id_type_0 = UUID(data)



                return run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        run_config_version_id = _parse_run_config_version_id(d.pop("runConfigVersionId"))


        compute_already_active_body_dto_details = cls(
            existing_compute_id=existing_compute_id,
            run_config_version_id=run_config_version_id,
        )

        return compute_already_active_body_dto_details

