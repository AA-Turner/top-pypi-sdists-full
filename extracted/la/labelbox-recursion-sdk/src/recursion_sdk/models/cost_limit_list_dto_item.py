from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.cost_limit_list_dto_item_scope import CostLimitListDtoItemScope
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="CostLimitListDtoItem")



@_attrs_define
class CostLimitListDtoItem:
    """ A monthly USD spend cap for an environment or a specific problem. When the cap is reached, new runs against that
    scope are gated until the next billing window.

        Attributes:
            id (UUID): Stable cost-limit identifier.
            environment_id (UUID): Environment this cost limit applies to.
            problem_id (None | UUID): Problem this cost limit applies to. Null for environment-scope limits that cover all
                problems in the environment.
            scope (CostLimitListDtoItemScope): Whether this cap covers total environment spend or a single problem only.
            limit_usd (float): Monthly USD spend cap. Once exceeded, new runs against the affected scope are gated. Example:
                500.
            created_at (datetime.datetime): Timestamp when the cost limit was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the cost limit was last updated (ISO-8601, UTC).
     """

    id: UUID
    environment_id: UUID
    problem_id: None | UUID
    scope: CostLimitListDtoItemScope
    limit_usd: float
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        environment_id = str(self.environment_id)

        problem_id: None | str
        if isinstance(self.problem_id, UUID):
            problem_id = str(self.problem_id)
        else:
            problem_id = self.problem_id

        scope = self.scope.value

        limit_usd = self.limit_usd

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "environmentId": environment_id,
            "problemId": problem_id,
            "scope": scope,
            "limitUsd": limit_usd,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        environment_id = UUID(d.pop("environmentId"))




        def _parse_problem_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                problem_id_type_0 = UUID(data)



                return problem_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        problem_id = _parse_problem_id(d.pop("problemId"))


        scope = CostLimitListDtoItemScope(d.pop("scope"))




        limit_usd = d.pop("limitUsd")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        cost_limit_list_dto_item = cls(
            id=id,
            environment_id=environment_id,
            problem_id=problem_id,
            scope=scope,
            limit_usd=limit_usd,
            created_at=created_at,
            updated_at=updated_at,
        )

        return cost_limit_list_dto_item

