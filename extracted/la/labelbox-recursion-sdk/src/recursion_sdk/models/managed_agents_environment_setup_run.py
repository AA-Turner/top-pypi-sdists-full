from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_environment_setup_image import ManagedAgentsEnvironmentSetupImage
  from ..models.managed_agents_environment_setup_image_capture import ManagedAgentsEnvironmentSetupImageCapture
  from ..models.managed_agents_environment_setup_run_compute_profile import ManagedAgentsEnvironmentSetupRunComputeProfile
  from ..models.managed_agents_environment_setup_run_gpu_readiness import ManagedAgentsEnvironmentSetupRunGpuReadiness
  from ..models.managed_agents_next_action import ManagedAgentsNextAction





T = TypeVar("T", bound="ManagedAgentsEnvironmentSetupRun")



@_attrs_define
class ManagedAgentsEnvironmentSetupRun:
    """ One execution of an environment's setup script on fresh compute: provision, GPU check, script, profile, image
    capture, cleanup. Read status until terminal, then hint, failed_line, and stderr_tail; the full log is a separate
    call.

        Example:
            {'compute_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'compute_profile': {'key': 'example'}, 'created_at':
                '2026-02-18T09:30:00Z', 'duration_ms': 1, 'environment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'exit_code':
                1, 'failed_command': 'example', 'failed_line': 1, 'failure_code': 'example', 'fingerprint': 'example',
                'finished_at': '2026-02-18T09:30:00Z', 'gpu_readiness': {'key': 'example'}, 'hint': 'example', 'hint_code':
                'example', 'image': 'example', 'imageCapture': {'at': '2026-02-18T09:30:00Z', 'message': 'example', 'reason':
                'example', 'setupRunId': 'example', 'status': 'failed'}, 'imageId': 'example', 'kind': 'example', 'log_bytes':
                1, 'log_lines': 1, 'log_truncated': True, 'message': 'example', 'next_action': {'method': 'example',
                'operation_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'path': 'example'}, 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'phase': 'example', 'providerEventCursor': 1, 'providerRunId':
                'example', 'requested_by_user_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'setupImage': {'baseImageDigest': 'example', 'capturedAt':
                '2026-02-18T09:30:00Z', 'computeId': 'example', 'fingerprint': 'example', 'generation': 1, 'image': 'example',
                'imageId': 'example', 'runnerImage': 'example', 'setupRunId': 'example', 'sizeBytes': 1, 'usable': True,
                'warmup': 'example', 'warmupMessage': 'example'}, 'setup_run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'started_at': '2026-02-18T09:30:00Z', 'status': 'example', 'stderr_tail': 'example'}

        Attributes:
            created_at (datetime.datetime): When the run was requested.
            environment_id (str): Environment whose setup ran.
            kind (str): manual (requested through the API to verify the environment) or session (performed while
                provisioning a session).
            organization_id (str): Organization that owns the environment.
            setup_run_id (str): Server-assigned id of the run.
            status (str): queued, provisioning, running, succeeded, failed, or cancelled. Poll until one of the last three;
                getEnvironmentSetupRun accepts wait_seconds to do that server-side.
            compute_id (str | Unset): Provider id of the compute the run used. Released when the run ends.
            compute_profile (ManagedAgentsEnvironmentSetupRunComputeProfile | Unset): What the compute turned out to be:
                vCPUs, memory, GPUs, Docker state, image tools. Recorded after setup passed.
            duration_ms (int | Unset): Wall-clock duration in milliseconds, provisioning included.
            exit_code (int | Unset): Exit code of the setup script when it ran. 124 means the timeout elapsed.
            failed_command (str | Unset): The failing line's command as written, unexpanded.
            failed_line (int | Unset): 1-based line in the setup script whose command exited non-zero. 0 when unknown.
            failure_code (str | Unset): Machine-readable failure class when the run did not succeed:
                environment_setup_failed, sandbox_capacity_unavailable, sandbox_gpu_not_ready, sandbox_provision_timeout, and so
                on. Same vocabulary as session failures.
            fingerprint (str | Unset): Hash of the environment configuration the run executed.
            finished_at (datetime.datetime | Unset): When the run reached a terminal status.
            gpu_readiness (ManagedAgentsEnvironmentSetupRunGpuReadiness | Unset): GPU readiness report for accelerator
                environments.
            hint (str | Unset): Likely fix when the failure cause is recognised.
            hint_code (str | Unset): Stable identifier of the recognised failure cause.
            image (str | Unset): Runner image the compute booted.
            image_capture (ManagedAgentsEnvironmentSetupImageCapture | Unset): Why a verified setup run published no new
                reusable image. Example: {'at': '2026-02-18T09:30:00Z', 'message': 'example', 'reason': 'example', 'setupRunId':
                'example', 'status': 'failed'}.
            image_id (str | Unset): Agent Service image id being captured.
            log_bytes (int | Unset): Bytes of log persisted for the run.
            log_lines (int | Unset): Lines of log persisted for the run. The last line's seq equals this; pass it as after
                to tail.
            log_truncated (bool | Unset): True when the script produced more output than the run keeps (4 MiB); the head and
                the stderr tail are retained.
            message (str | Unset): One-sentence description of the outcome.
            next_action (ManagedAgentsNextAction | Unset): The literal next API call to make. Included on errors and results
                whose resolution is one known call, so a caller need not infer it. Example: {'method': 'example',
                'operation_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'path': 'example'}.
            phase (str | Unset): Current or final phase: provision, gpu_check, setup, profile, commit, cleanup.
            provider_event_cursor (int | Unset): Last Agent Service setup event sequence persisted into this run's log.
            provider_run_id (str | Unset): Durable Agent Service run id executing the setup script.
            requested_by_user_id (str | Unset): User who requested a manual run.
            session_id (str | Unset): Session the run provisioned, for kind session.
            setup_image (ManagedAgentsEnvironmentSetupImage | Unset): An immutable setup image published after a manual
                setup run passes. Identity includes the environment fingerprint, configured runner, observed base digest, and
                capture generation. Example: {'baseImageDigest': 'example', 'capturedAt': '2026-02-18T09:30:00Z', 'computeId':
                'example', 'fingerprint': 'example', 'generation': 1, 'image': 'example', 'imageId': 'example', 'runnerImage':
                'example', 'setupRunId': 'example', 'sizeBytes': 1, 'usable': True, 'warmup': 'example', 'warmupMessage':
                'example'}.
            started_at (datetime.datetime | Unset): When provisioning began.
            stderr_tail (str | Unset): Last lines of stderr, redacted and bounded to 2 KiB.
     """

    created_at: datetime.datetime
    environment_id: str
    kind: str
    organization_id: str
    setup_run_id: str
    status: str
    compute_id: str | Unset = UNSET
    compute_profile: ManagedAgentsEnvironmentSetupRunComputeProfile | Unset = UNSET
    duration_ms: int | Unset = UNSET
    exit_code: int | Unset = UNSET
    failed_command: str | Unset = UNSET
    failed_line: int | Unset = UNSET
    failure_code: str | Unset = UNSET
    fingerprint: str | Unset = UNSET
    finished_at: datetime.datetime | Unset = UNSET
    gpu_readiness: ManagedAgentsEnvironmentSetupRunGpuReadiness | Unset = UNSET
    hint: str | Unset = UNSET
    hint_code: str | Unset = UNSET
    image: str | Unset = UNSET
    image_capture: ManagedAgentsEnvironmentSetupImageCapture | Unset = UNSET
    image_id: str | Unset = UNSET
    log_bytes: int | Unset = UNSET
    log_lines: int | Unset = UNSET
    log_truncated: bool | Unset = UNSET
    message: str | Unset = UNSET
    next_action: ManagedAgentsNextAction | Unset = UNSET
    phase: str | Unset = UNSET
    provider_event_cursor: int | Unset = UNSET
    provider_run_id: str | Unset = UNSET
    requested_by_user_id: str | Unset = UNSET
    session_id: str | Unset = UNSET
    setup_image: ManagedAgentsEnvironmentSetupImage | Unset = UNSET
    started_at: datetime.datetime | Unset = UNSET
    stderr_tail: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_environment_setup_image import ManagedAgentsEnvironmentSetupImage # noqa: PLC0415
        from ..models.managed_agents_environment_setup_image_capture import ManagedAgentsEnvironmentSetupImageCapture # noqa: PLC0415
        from ..models.managed_agents_environment_setup_run_compute_profile import ManagedAgentsEnvironmentSetupRunComputeProfile # noqa: PLC0415
        from ..models.managed_agents_environment_setup_run_gpu_readiness import ManagedAgentsEnvironmentSetupRunGpuReadiness # noqa: PLC0415
        from ..models.managed_agents_next_action import ManagedAgentsNextAction # noqa: PLC0415
        created_at = self.created_at.isoformat()

        environment_id = self.environment_id

        kind = self.kind

        organization_id = self.organization_id

        setup_run_id = self.setup_run_id

        status = self.status

        compute_id = self.compute_id

        compute_profile: dict[str, Any] | Unset = UNSET
        if not isinstance(self.compute_profile, Unset):
            compute_profile = self.compute_profile.to_dict()

        duration_ms = self.duration_ms

        exit_code = self.exit_code

        failed_command = self.failed_command

        failed_line = self.failed_line

        failure_code = self.failure_code

        fingerprint = self.fingerprint

        finished_at: str | Unset = UNSET
        if not isinstance(self.finished_at, Unset):
            finished_at = self.finished_at.isoformat()

        gpu_readiness: dict[str, Any] | Unset = UNSET
        if not isinstance(self.gpu_readiness, Unset):
            gpu_readiness = self.gpu_readiness.to_dict()

        hint = self.hint

        hint_code = self.hint_code

        image = self.image

        image_capture: dict[str, Any] | Unset = UNSET
        if not isinstance(self.image_capture, Unset):
            image_capture = self.image_capture.to_dict()

        image_id = self.image_id

        log_bytes = self.log_bytes

        log_lines = self.log_lines

        log_truncated = self.log_truncated

        message = self.message

        next_action: dict[str, Any] | Unset = UNSET
        if not isinstance(self.next_action, Unset):
            next_action = self.next_action.to_dict()

        phase = self.phase

        provider_event_cursor = self.provider_event_cursor

        provider_run_id = self.provider_run_id

        requested_by_user_id = self.requested_by_user_id

        session_id = self.session_id

        setup_image: dict[str, Any] | Unset = UNSET
        if not isinstance(self.setup_image, Unset):
            setup_image = self.setup_image.to_dict()

        started_at: str | Unset = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        stderr_tail = self.stderr_tail


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "created_at": created_at,
            "environment_id": environment_id,
            "kind": kind,
            "organization_id": organization_id,
            "setup_run_id": setup_run_id,
            "status": status,
        })
        if compute_id is not UNSET:
            field_dict["compute_id"] = compute_id
        if compute_profile is not UNSET:
            field_dict["compute_profile"] = compute_profile
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms
        if exit_code is not UNSET:
            field_dict["exit_code"] = exit_code
        if failed_command is not UNSET:
            field_dict["failed_command"] = failed_command
        if failed_line is not UNSET:
            field_dict["failed_line"] = failed_line
        if failure_code is not UNSET:
            field_dict["failure_code"] = failure_code
        if fingerprint is not UNSET:
            field_dict["fingerprint"] = fingerprint
        if finished_at is not UNSET:
            field_dict["finished_at"] = finished_at
        if gpu_readiness is not UNSET:
            field_dict["gpu_readiness"] = gpu_readiness
        if hint is not UNSET:
            field_dict["hint"] = hint
        if hint_code is not UNSET:
            field_dict["hint_code"] = hint_code
        if image is not UNSET:
            field_dict["image"] = image
        if image_capture is not UNSET:
            field_dict["imageCapture"] = image_capture
        if image_id is not UNSET:
            field_dict["imageId"] = image_id
        if log_bytes is not UNSET:
            field_dict["log_bytes"] = log_bytes
        if log_lines is not UNSET:
            field_dict["log_lines"] = log_lines
        if log_truncated is not UNSET:
            field_dict["log_truncated"] = log_truncated
        if message is not UNSET:
            field_dict["message"] = message
        if next_action is not UNSET:
            field_dict["next_action"] = next_action
        if phase is not UNSET:
            field_dict["phase"] = phase
        if provider_event_cursor is not UNSET:
            field_dict["providerEventCursor"] = provider_event_cursor
        if provider_run_id is not UNSET:
            field_dict["providerRunId"] = provider_run_id
        if requested_by_user_id is not UNSET:
            field_dict["requested_by_user_id"] = requested_by_user_id
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if setup_image is not UNSET:
            field_dict["setupImage"] = setup_image
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if stderr_tail is not UNSET:
            field_dict["stderr_tail"] = stderr_tail

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_environment_setup_image import ManagedAgentsEnvironmentSetupImage # noqa: PLC0415
        from ..models.managed_agents_environment_setup_image_capture import ManagedAgentsEnvironmentSetupImageCapture # noqa: PLC0415
        from ..models.managed_agents_environment_setup_run_compute_profile import ManagedAgentsEnvironmentSetupRunComputeProfile # noqa: PLC0415
        from ..models.managed_agents_environment_setup_run_gpu_readiness import ManagedAgentsEnvironmentSetupRunGpuReadiness # noqa: PLC0415
        from ..models.managed_agents_next_action import ManagedAgentsNextAction # noqa: PLC0415
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        environment_id = d.pop("environment_id")

        kind = d.pop("kind")

        organization_id = d.pop("organization_id")

        setup_run_id = d.pop("setup_run_id")

        status = d.pop("status")

        compute_id = d.pop("compute_id", UNSET)

        _compute_profile = d.pop("compute_profile", UNSET)
        compute_profile: ManagedAgentsEnvironmentSetupRunComputeProfile | Unset
        if isinstance(_compute_profile,  Unset):
            compute_profile = UNSET
        else:
            compute_profile = ManagedAgentsEnvironmentSetupRunComputeProfile.from_dict(_compute_profile)




        duration_ms = d.pop("duration_ms", UNSET)

        exit_code = d.pop("exit_code", UNSET)

        failed_command = d.pop("failed_command", UNSET)

        failed_line = d.pop("failed_line", UNSET)

        failure_code = d.pop("failure_code", UNSET)

        fingerprint = d.pop("fingerprint", UNSET)

        _finished_at = d.pop("finished_at", UNSET)
        finished_at: datetime.datetime | Unset
        if isinstance(_finished_at,  Unset):
            finished_at = UNSET
        else:
            finished_at = datetime.datetime.fromisoformat(_finished_at)




        _gpu_readiness = d.pop("gpu_readiness", UNSET)
        gpu_readiness: ManagedAgentsEnvironmentSetupRunGpuReadiness | Unset
        if isinstance(_gpu_readiness,  Unset):
            gpu_readiness = UNSET
        else:
            gpu_readiness = ManagedAgentsEnvironmentSetupRunGpuReadiness.from_dict(_gpu_readiness)




        hint = d.pop("hint", UNSET)

        hint_code = d.pop("hint_code", UNSET)

        image = d.pop("image", UNSET)

        _image_capture = d.pop("imageCapture", UNSET)
        image_capture: ManagedAgentsEnvironmentSetupImageCapture | Unset
        if isinstance(_image_capture,  Unset):
            image_capture = UNSET
        else:
            image_capture = ManagedAgentsEnvironmentSetupImageCapture.from_dict(_image_capture)




        image_id = d.pop("imageId", UNSET)

        log_bytes = d.pop("log_bytes", UNSET)

        log_lines = d.pop("log_lines", UNSET)

        log_truncated = d.pop("log_truncated", UNSET)

        message = d.pop("message", UNSET)

        _next_action = d.pop("next_action", UNSET)
        next_action: ManagedAgentsNextAction | Unset
        if isinstance(_next_action,  Unset):
            next_action = UNSET
        else:
            next_action = ManagedAgentsNextAction.from_dict(_next_action)




        phase = d.pop("phase", UNSET)

        provider_event_cursor = d.pop("providerEventCursor", UNSET)

        provider_run_id = d.pop("providerRunId", UNSET)

        requested_by_user_id = d.pop("requested_by_user_id", UNSET)

        session_id = d.pop("session_id", UNSET)

        _setup_image = d.pop("setupImage", UNSET)
        setup_image: ManagedAgentsEnvironmentSetupImage | Unset
        if isinstance(_setup_image,  Unset):
            setup_image = UNSET
        else:
            setup_image = ManagedAgentsEnvironmentSetupImage.from_dict(_setup_image)




        _started_at = d.pop("started_at", UNSET)
        started_at: datetime.datetime | Unset
        if isinstance(_started_at,  Unset):
            started_at = UNSET
        else:
            started_at = datetime.datetime.fromisoformat(_started_at)




        stderr_tail = d.pop("stderr_tail", UNSET)

        managed_agents_environment_setup_run = cls(
            created_at=created_at,
            environment_id=environment_id,
            kind=kind,
            organization_id=organization_id,
            setup_run_id=setup_run_id,
            status=status,
            compute_id=compute_id,
            compute_profile=compute_profile,
            duration_ms=duration_ms,
            exit_code=exit_code,
            failed_command=failed_command,
            failed_line=failed_line,
            failure_code=failure_code,
            fingerprint=fingerprint,
            finished_at=finished_at,
            gpu_readiness=gpu_readiness,
            hint=hint,
            hint_code=hint_code,
            image=image,
            image_capture=image_capture,
            image_id=image_id,
            log_bytes=log_bytes,
            log_lines=log_lines,
            log_truncated=log_truncated,
            message=message,
            next_action=next_action,
            phase=phase,
            provider_event_cursor=provider_event_cursor,
            provider_run_id=provider_run_id,
            requested_by_user_id=requested_by_user_id,
            session_id=session_id,
            setup_image=setup_image,
            started_at=started_at,
            stderr_tail=stderr_tail,
        )


        managed_agents_environment_setup_run.additional_properties = d
        return managed_agents_environment_setup_run

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
