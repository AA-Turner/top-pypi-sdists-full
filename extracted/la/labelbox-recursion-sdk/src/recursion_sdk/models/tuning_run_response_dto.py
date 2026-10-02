from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.tuning_run_response_dto_status import TuningRunResponseDtoStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.tuning_run_response_dto_organization_names import TuningRunResponseDtoOrganizationNames





T = TypeVar("T", bound="TuningRunResponseDto")



@_attrs_define
class TuningRunResponseDto:
    """ A background job tracked by the jobs_v2 framework. Scope ids are denormalized from the link tables for read
    convenience.

        Example:
            {'id': '11111111-1111-4111-8111-111111111111', 'parentJobId': None, 'userId':
                '11111111-1111-4111-8111-111111111111', 'type': 'run_config_run', 'name': 'grpo-trainer-run', 'status':
                'executing', 'payload': {}, 'externalState': None, 'output': None, 'errorMessage': None, 'attempts': 1,
                'maxAttempts': 1, 'scheduledAt': '2026-01-01T00:00:00.000Z', 'pollAfter': None, 'startedAt':
                '2026-01-01T00:00:01.000Z', 'completedAt': None, 'createdAt': '2026-01-01T00:00:00.000Z', 'updatedAt':
                '2026-01-01T00:00:01.000Z'}

        Attributes:
            id (UUID): Stable jobs_v2 identifier (UUID). One row per background-work unit in the generic, strategy-driven
                job framework.
            parent_job_id (None | UUID): Parent jobs_v2 id when this row was spawned as a child via a waiting_children
                result. Null for root jobs.
            user_id (UUID): The user that created this job. Not a scope handle.
            type_ (str): Discriminator mapping to a registered strategy bundle (e.g. taiga_send, taiga_run_problem_version).
            name (None | str): Optional human-readable label shown in lists.
            status (TuningRunResponseDtoStatus): Lifecycle state of a jobs_v2 row. Claimable: pending, waiting_external
                (gated by poll_after), aggregating. Parked: executing, waiting_children, cancelling. Terminal: completed,
                failed, cancelled.
            payload (Any): Strategy-typed input. Validated against the per-type Zod schema at insert and dispatch.
            external_state (Any | None): Live state across waiting_external poll cycles. Null for sync strategies and before
                the first poll.
            output (Any | None): Terminal output payload set when status transitions to completed.
            error_message (None | str): Terminal error message set when status transitions to failed.
            attempts (int): Budget units consumed by this row. Bumped by claimPending on each run claim, and by
                scheduleRetryInTrx on each poll/aggregate retry (i.e. when the strategy returns { kind: "retry" } from poll or
                onChildrenComplete). Normal poll/aggregate reclaims that did not return retry are not counted.
            max_attempts (int): Retry budget. The row becomes terminally failed once attempts reaches this value. Default 1
                (single attempt, no retry); raised per-type via registerJobType or per-row via the spawn spec.
            scheduled_at (datetime.datetime): Earliest time this row is eligible to be claimed from status=pending.
            poll_after (datetime.datetime | None): While status=waiting_external, earliest time the poll loop will invoke
                PollStrategy.poll.
            started_at (datetime.datetime | None): Wall-clock timestamp the row first transitioned out of pending. Null
                until claimed.
            completed_at (datetime.datetime | None): Wall-clock timestamp the row entered a terminal status. Null until
                terminal.
            created_at (datetime.datetime): Row creation timestamp.
            updated_at (datetime.datetime): Row last-modified timestamp.
            environment_ids (list[UUID] | Unset): Environments this job is linked to (denormalized from environment_jobs).
            organization_ids (list[UUID] | Unset): Organizations this job is linked to (denormalized from
                organization_jobs).
            organization_names (TuningRunResponseDtoOrganizationNames | Unset): Display names for the ids in
                organizationIds, keyed by organization id. Present only on platform-admin cross-organization reads.
            problem_ids (list[UUID] | Unset): Problems this job is linked to (denormalized from problem_jobs).
     """

    id: UUID
    parent_job_id: None | UUID
    user_id: UUID
    type_: str
    name: None | str
    status: TuningRunResponseDtoStatus
    payload: Any
    external_state: Any | None
    output: Any | None
    error_message: None | str
    attempts: int
    max_attempts: int
    scheduled_at: datetime.datetime
    poll_after: datetime.datetime | None
    started_at: datetime.datetime | None
    completed_at: datetime.datetime | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    environment_ids: list[UUID] | Unset = UNSET
    organization_ids: list[UUID] | Unset = UNSET
    organization_names: TuningRunResponseDtoOrganizationNames | Unset = UNSET
    problem_ids: list[UUID] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.tuning_run_response_dto_organization_names import TuningRunResponseDtoOrganizationNames # noqa: PLC0415
        id = str(self.id)

        parent_job_id: None | str
        if isinstance(self.parent_job_id, UUID):
            parent_job_id = str(self.parent_job_id)
        else:
            parent_job_id = self.parent_job_id

        user_id = str(self.user_id)

        type_ = self.type_

        name: None | str
        name = self.name

        status = self.status.value

        payload = self.payload

        external_state: Any | None
        external_state = self.external_state

        output: Any | None
        output = self.output

        error_message: None | str
        error_message = self.error_message

        attempts = self.attempts

        max_attempts = self.max_attempts

        scheduled_at = self.scheduled_at.isoformat()

        poll_after: None | str
        if isinstance(self.poll_after, datetime.datetime):
            poll_after = self.poll_after.isoformat()
        else:
            poll_after = self.poll_after

        started_at: None | str
        if isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        completed_at: None | str
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        environment_ids: list[str] | Unset = UNSET
        if not isinstance(self.environment_ids, Unset):
            environment_ids = []
            for environment_ids_item_data in self.environment_ids:
                environment_ids_item = str(environment_ids_item_data)
                environment_ids.append(environment_ids_item)



        organization_ids: list[str] | Unset = UNSET
        if not isinstance(self.organization_ids, Unset):
            organization_ids = []
            for organization_ids_item_data in self.organization_ids:
                organization_ids_item = str(organization_ids_item_data)
                organization_ids.append(organization_ids_item)



        organization_names: dict[str, Any] | Unset = UNSET
        if not isinstance(self.organization_names, Unset):
            organization_names = self.organization_names.to_dict()

        problem_ids: list[str] | Unset = UNSET
        if not isinstance(self.problem_ids, Unset):
            problem_ids = []
            for problem_ids_item_data in self.problem_ids:
                problem_ids_item = str(problem_ids_item_data)
                problem_ids.append(problem_ids_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "parentJobId": parent_job_id,
            "userId": user_id,
            "type": type_,
            "name": name,
            "status": status,
            "payload": payload,
            "externalState": external_state,
            "output": output,
            "errorMessage": error_message,
            "attempts": attempts,
            "maxAttempts": max_attempts,
            "scheduledAt": scheduled_at,
            "pollAfter": poll_after,
            "startedAt": started_at,
            "completedAt": completed_at,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })
        if environment_ids is not UNSET:
            field_dict["environmentIds"] = environment_ids
        if organization_ids is not UNSET:
            field_dict["organizationIds"] = organization_ids
        if organization_names is not UNSET:
            field_dict["organizationNames"] = organization_names
        if problem_ids is not UNSET:
            field_dict["problemIds"] = problem_ids

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tuning_run_response_dto_organization_names import TuningRunResponseDtoOrganizationNames # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        def _parse_parent_job_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                parent_job_id_type_0 = UUID(data)



                return parent_job_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        parent_job_id = _parse_parent_job_id(d.pop("parentJobId"))


        user_id = UUID(d.pop("userId"))




        type_ = d.pop("type")

        def _parse_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        name = _parse_name(d.pop("name"))


        status = TuningRunResponseDtoStatus(d.pop("status"))




        payload = d.pop("payload")

        def _parse_external_state(data: object) -> Any | None:
            if data is None:
                return data
            return cast(Any | None, data)

        external_state = _parse_external_state(d.pop("externalState"))


        def _parse_output(data: object) -> Any | None:
            if data is None:
                return data
            return cast(Any | None, data)

        output = _parse_output(d.pop("output"))


        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("errorMessage"))


        attempts = d.pop("attempts")

        max_attempts = d.pop("maxAttempts")

        scheduled_at = datetime.datetime.fromisoformat(d.pop("scheduledAt"))




        def _parse_poll_after(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                poll_after_type_0 = datetime.datetime.fromisoformat(data)



                return poll_after_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        poll_after = _parse_poll_after(d.pop("pollAfter"))


        def _parse_started_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_at_type_0 = datetime.datetime.fromisoformat(data)



                return started_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        started_at = _parse_started_at(d.pop("startedAt"))


        def _parse_completed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = datetime.datetime.fromisoformat(data)



                return completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        completed_at = _parse_completed_at(d.pop("completedAt"))


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        _environment_ids = d.pop("environmentIds", UNSET)
        environment_ids: list[UUID] | Unset = UNSET
        if _environment_ids is not UNSET:
            environment_ids = []
            for environment_ids_item_data in _environment_ids:
                environment_ids_item = UUID(environment_ids_item_data)



                environment_ids.append(environment_ids_item)


        _organization_ids = d.pop("organizationIds", UNSET)
        organization_ids: list[UUID] | Unset = UNSET
        if _organization_ids is not UNSET:
            organization_ids = []
            for organization_ids_item_data in _organization_ids:
                organization_ids_item = UUID(organization_ids_item_data)



                organization_ids.append(organization_ids_item)


        _organization_names = d.pop("organizationNames", UNSET)
        organization_names: TuningRunResponseDtoOrganizationNames | Unset
        if isinstance(_organization_names,  Unset):
            organization_names = UNSET
        else:
            organization_names = TuningRunResponseDtoOrganizationNames.from_dict(_organization_names)




        _problem_ids = d.pop("problemIds", UNSET)
        problem_ids: list[UUID] | Unset = UNSET
        if _problem_ids is not UNSET:
            problem_ids = []
            for problem_ids_item_data in _problem_ids:
                problem_ids_item = UUID(problem_ids_item_data)



                problem_ids.append(problem_ids_item)


        tuning_run_response_dto = cls(
            id=id,
            parent_job_id=parent_job_id,
            user_id=user_id,
            type_=type_,
            name=name,
            status=status,
            payload=payload,
            external_state=external_state,
            output=output,
            error_message=error_message,
            attempts=attempts,
            max_attempts=max_attempts,
            scheduled_at=scheduled_at,
            poll_after=poll_after,
            started_at=started_at,
            completed_at=completed_at,
            created_at=created_at,
            updated_at=updated_at,
            environment_ids=environment_ids,
            organization_ids=organization_ids,
            organization_names=organization_names,
            problem_ids=problem_ids,
        )

        return tuning_run_response_dto

