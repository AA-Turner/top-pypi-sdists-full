from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_cost_limit_dto_scope import CreateCostLimitDtoScope
from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="CreateCostLimitDto")



@_attrs_define
class CreateCostLimitDto:
    """ Request body for creating a new cost limit. Each scope, problem, and amount triple must be unique within the
    environment.

        Example:
            {'scope': 'environment', 'limitUsd': 500}

        Attributes:
            scope (CreateCostLimitDtoScope): Whether this cap covers total environment spend or a single problem only. Must
                be the problem scope when a problem is referenced.
            limit_usd (float): Monthly USD spend cap. Must be positive with at most 2 decimal places. Example: 500.
            problem_id (UUID | Unset): Problem the cap applies to. Required for problem-scoped caps and omitted for
                environment-scoped caps.
     """

    scope: CreateCostLimitDtoScope
    limit_usd: float
    problem_id: UUID | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        scope = self.scope.value

        limit_usd = self.limit_usd

        problem_id: str | Unset = UNSET
        if not isinstance(self.problem_id, Unset):
            problem_id = str(self.problem_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "scope": scope,
            "limitUsd": limit_usd,
        })
        if problem_id is not UNSET:
            field_dict["problemId"] = problem_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        scope = CreateCostLimitDtoScope(d.pop("scope"))




        limit_usd = d.pop("limitUsd")

        _problem_id = d.pop("problemId", UNSET)
        problem_id: UUID | Unset
        if isinstance(_problem_id,  Unset):
            problem_id = UNSET
        else:
            problem_id = UUID(_problem_id)




        create_cost_limit_dto = cls(
            scope=scope,
            limit_usd=limit_usd,
            problem_id=problem_id,
        )


        create_cost_limit_dto.additional_properties = d
        return create_cost_limit_dto

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
