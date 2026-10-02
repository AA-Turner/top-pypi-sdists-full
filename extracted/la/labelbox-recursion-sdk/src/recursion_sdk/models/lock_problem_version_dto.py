from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.lock_problem_version_dto_worldsim_solver import LockProblemVersionDtoWorldsimSolver





T = TypeVar("T", bound="LockProblemVersionDto")



@_attrs_define
class LockProblemVersionDto:
    """ Optional request body for locking a problem version.

        Example:
            {}

        Attributes:
            worldsim_solver (LockProblemVersionDtoWorldsimSolver | Unset): Worldsim solver authoring payload (MCP servers,
                world effects, simulated time, CUA env-config). When present, it is persisted on the locked version; each run
                forks a per-version solver child from the solver the environment resolves at that time.
     """

    worldsim_solver: LockProblemVersionDtoWorldsimSolver | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lock_problem_version_dto_worldsim_solver import LockProblemVersionDtoWorldsimSolver # noqa: PLC0415
        worldsim_solver: dict[str, Any] | Unset = UNSET
        if not isinstance(self.worldsim_solver, Unset):
            worldsim_solver = self.worldsim_solver.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if worldsim_solver is not UNSET:
            field_dict["worldsimSolver"] = worldsim_solver

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lock_problem_version_dto_worldsim_solver import LockProblemVersionDtoWorldsimSolver # noqa: PLC0415
        d = dict(src_dict)
        _worldsim_solver = d.pop("worldsimSolver", UNSET)
        worldsim_solver: LockProblemVersionDtoWorldsimSolver | Unset
        if isinstance(_worldsim_solver,  Unset):
            worldsim_solver = UNSET
        else:
            worldsim_solver = LockProblemVersionDtoWorldsimSolver.from_dict(_worldsim_solver)




        lock_problem_version_dto = cls(
            worldsim_solver=worldsim_solver,
        )


        lock_problem_version_dto.additional_properties = d
        return lock_problem_version_dto

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
