from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.create_check_fix_cycle_dto_fix_step_type_0 import CreateCheckFixCycleDtoFixStepType0
  from ..models.create_check_fix_cycle_dto_target_type_0 import CreateCheckFixCycleDtoTargetType0





T = TypeVar("T", bound="CreateCheckFixCycleDto")



@_attrs_define
class CreateCheckFixCycleDto:
    """ Create-request body for a check_fix_cycle: the problem under repair, the fork/commit target, the check run-config
    versions run each wave, the fix step, the submit run-config version, and the fix-attempt cap (organizationId is
    stamped from the route).

        Example:
            {'problemId': '11111111-1111-4111-8111-111111111111', 'target': {'kind': 'git_fork', 'forkRepo': 'acme-org/fork-
                repo', 'baseSha': '0123456789abcdef0123456789abcdef01234567', 'headSha':
                'fedcba9876543210fedcba9876543210fedcba98', 'headRef': 'submission-branch', 'problemDir': 'problems/example-
                task'}, 'checkRunConfigVersionIds': ['11111111-1111-4111-8111-111111111111'], 'fixStep': {'kind': 'run_config',
                'runConfigVersionId': '22222222-2222-4222-8222-222222222222'}, 'submitRunConfigVersionId':
                '33333333-3333-4333-8333-333333333333', 'maxFixAttempts': 3}

        Attributes:
            problem_id (UUID): The problem this fix cycle repairs.
            target (CreateCheckFixCycleDtoTargetType0): The checkable artifact this cycle targets. git_fork is the only arm
                today.
            check_run_config_version_ids (list[UUID]): Locked, agent-harness run-config versions executed as check children
                every wave -- a fan-out ceiling of 16 parallel check containers per wave.
            fix_step (CreateCheckFixCycleDtoFixStepType0): The fix step spawned on red. run_config is the only arm today.
            max_fix_attempts (int): Maximum number of fix children that may be spawned before the cycle terminates
                attempts_exhausted. N permits N fix children and N+1 check waves, each up to the check fan-out ceiling of check
                containers -- at the ceiling (N=50) that is 50 fix children + 51 x 16 = 866 containers authorized by a single
                request, each able to run to run_config_run's own 36-hour wall-clock cap.
            submit_run_config_version_id (UUID | Unset): Locked, agent-harness run-config version executed as the submit
                child once a wave passes every check.
            early_abort_after_stall_waves (int | Unset): Opt-in early-abort for a cycle that stops making progress.
                Additive-optional and OFF by default: absent, the cycle always runs its full maxFixAttempts budget. When set,
                the cycle terminates stalled once this many consecutive decided red waves in a row report an identical outcome
                to the one before it -- i.e. the fixer made no measurable progress -- instead of burning the remaining fix-
                attempt budget on a cycle that has already shown it is not converging. Never triggers on a cycle's first red
                wave.
     """

    problem_id: UUID
    target: CreateCheckFixCycleDtoTargetType0
    check_run_config_version_ids: list[UUID]
    fix_step: CreateCheckFixCycleDtoFixStepType0
    max_fix_attempts: int
    submit_run_config_version_id: UUID | Unset = UNSET
    early_abort_after_stall_waves: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_check_fix_cycle_dto_fix_step_type_0 import CreateCheckFixCycleDtoFixStepType0 # noqa: PLC0415
        from ..models.create_check_fix_cycle_dto_target_type_0 import CreateCheckFixCycleDtoTargetType0 # noqa: PLC0415
        problem_id = str(self.problem_id)

        target: dict[str, Any]
        if isinstance(self.target, CreateCheckFixCycleDtoTargetType0):
            target = self.target.to_dict()


        check_run_config_version_ids = []
        for check_run_config_version_ids_item_data in self.check_run_config_version_ids:
            check_run_config_version_ids_item = str(check_run_config_version_ids_item_data)
            check_run_config_version_ids.append(check_run_config_version_ids_item)



        fix_step: dict[str, Any]
        if isinstance(self.fix_step, CreateCheckFixCycleDtoFixStepType0):
            fix_step = self.fix_step.to_dict()


        max_fix_attempts = self.max_fix_attempts

        submit_run_config_version_id: str | Unset = UNSET
        if not isinstance(self.submit_run_config_version_id, Unset):
            submit_run_config_version_id = str(self.submit_run_config_version_id)

        early_abort_after_stall_waves = self.early_abort_after_stall_waves


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "problemId": problem_id,
            "target": target,
            "checkRunConfigVersionIds": check_run_config_version_ids,
            "fixStep": fix_step,
            "maxFixAttempts": max_fix_attempts,
        })
        if submit_run_config_version_id is not UNSET:
            field_dict["submitRunConfigVersionId"] = submit_run_config_version_id
        if early_abort_after_stall_waves is not UNSET:
            field_dict["earlyAbortAfterStallWaves"] = early_abort_after_stall_waves

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_check_fix_cycle_dto_fix_step_type_0 import CreateCheckFixCycleDtoFixStepType0 # noqa: PLC0415
        from ..models.create_check_fix_cycle_dto_target_type_0 import CreateCheckFixCycleDtoTargetType0 # noqa: PLC0415
        d = dict(src_dict)
        problem_id = UUID(d.pop("problemId"))




        def _parse_target(data: object) -> CreateCheckFixCycleDtoTargetType0:
            if not isinstance(data, dict):
                raise TypeError()
            target_type_0 = CreateCheckFixCycleDtoTargetType0.from_dict(data)



            return target_type_0

        target = _parse_target(d.pop("target"))


        check_run_config_version_ids = []
        _check_run_config_version_ids = d.pop("checkRunConfigVersionIds")
        for check_run_config_version_ids_item_data in (_check_run_config_version_ids):
            check_run_config_version_ids_item = UUID(check_run_config_version_ids_item_data)



            check_run_config_version_ids.append(check_run_config_version_ids_item)


        def _parse_fix_step(data: object) -> CreateCheckFixCycleDtoFixStepType0:
            if not isinstance(data, dict):
                raise TypeError()
            fix_step_type_0 = CreateCheckFixCycleDtoFixStepType0.from_dict(data)



            return fix_step_type_0

        fix_step = _parse_fix_step(d.pop("fixStep"))


        max_fix_attempts = d.pop("maxFixAttempts")

        _submit_run_config_version_id = d.pop("submitRunConfigVersionId", UNSET)
        submit_run_config_version_id: UUID | Unset
        if isinstance(_submit_run_config_version_id,  Unset):
            submit_run_config_version_id = UNSET
        else:
            submit_run_config_version_id = UUID(_submit_run_config_version_id)




        early_abort_after_stall_waves = d.pop("earlyAbortAfterStallWaves", UNSET)

        create_check_fix_cycle_dto = cls(
            problem_id=problem_id,
            target=target,
            check_run_config_version_ids=check_run_config_version_ids,
            fix_step=fix_step,
            max_fix_attempts=max_fix_attempts,
            submit_run_config_version_id=submit_run_config_version_id,
            early_abort_after_stall_waves=early_abort_after_stall_waves,
        )

        return create_check_fix_cycle_dto

