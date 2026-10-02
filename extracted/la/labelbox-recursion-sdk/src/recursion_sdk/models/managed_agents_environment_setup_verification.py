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
  from ..models.managed_agents_environment_setup_run_summary import ManagedAgentsEnvironmentSetupRunSummary





T = TypeVar("T", bound="ManagedAgentsEnvironmentSetupVerification")



@_attrs_define
class ManagedAgentsEnvironmentSetupVerification:
    """ Whether an environment's setup script has been proven to run on real compute. Server-owned: it is written by manual
    setup runs and never accepted from a request body.

        Example:
            {'active_setup_run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'at': '2026-02-18T09:30:00Z', 'fingerprint':
                'example', 'image': {'baseImageDigest': 'example', 'capturedAt': '2026-02-18T09:30:00Z', 'computeId': 'example',
                'fingerprint': 'example', 'generation': 1, 'image': 'example', 'imageId': 'example', 'runnerImage': 'example',
                'setupRunId': 'example', 'sizeBytes': 1, 'usable': True, 'warmup': 'example', 'warmupMessage': 'example'},
                'imageCapture': {'at': '2026-02-18T09:30:00Z', 'message': 'example', 'reason': 'example', 'setupRunId':
                'example', 'status': 'failed'}, 'last_run': {'duration_ms': 1, 'exit_code': 1, 'failed_command': 'example',
                'failed_line': 1, 'hint': 'example', 'hint_code': 'example', 'message': 'example', 'phase': 'example',
                'setup_run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'example', 'stderr_tail': 'example'},
                'setup_run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'stale': True, 'status': 'example',
                'verified_by_user_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            stale (bool): True when the environment's provider, image, compute (resources, workspace disk size, provider
                config), setup script or timeout, variables, secret references, mounts, network policy, or privileged access
                changed after the recorded run, so the verdict no longer describes this configuration. Name, description,
                metadata, and the HTTP port do not count. Re-run setup to clear it. Always false for not_applicable and never.
            status (str): not_applicable (no setup script), never (a script exists but no run has recorded a verdict),
                running (a manual setup run is in flight and there is no earlier passing verdict to stand on), verified (the
                latest recorded manual run passed), or failed (the latest recorded manual run failed). Sessions on managed
                providers require verified and not stale when a script is configured; Runs additionally requires a valid
                captured image. When the captured base differs from the runner resolved at session start, setup runs on the
                session's compute instead of booting the captured image. The verdict is monotone: re-verifying a verified
                environment keeps it verified, with the new run in active_setup_run_id, until that run records its own verdict.
            active_setup_run_id (str | Unset): Manual setup run in flight for this environment, when there is one. Present
                alongside any status: a verified environment being re-verified stays verified, and sessions keep starting, until
                this run finishes. Follow it with getEnvironmentSetupRun or getEnvironmentSetupRunLog. Cleared when the run
                records a verdict or is cancelled.
            at (datetime.datetime | Unset): RFC 3339 timestamp of when the recorded run finished.
            fingerprint (str | Unset): Hash of the environment configuration the run executed. Compared against the current
                configuration to derive stale; opaque to callers.
            image (ManagedAgentsEnvironmentSetupImage | Unset): An immutable setup image published after a manual setup run
                passes. Identity includes the environment fingerprint, configured runner, observed base digest, and capture
                generation. Example: {'baseImageDigest': 'example', 'capturedAt': '2026-02-18T09:30:00Z', 'computeId':
                'example', 'fingerprint': 'example', 'generation': 1, 'image': 'example', 'imageId': 'example', 'runnerImage':
                'example', 'setupRunId': 'example', 'sizeBytes': 1, 'usable': True, 'warmup': 'example', 'warmupMessage':
                'example'}.
            image_capture (ManagedAgentsEnvironmentSetupImageCapture | Unset): Why a verified setup run published no new
                reusable image. Example: {'at': '2026-02-18T09:30:00Z', 'message': 'example', 'reason': 'example', 'setupRunId':
                'example', 'status': 'failed'}.
            last_run (ManagedAgentsEnvironmentSetupRunSummary | Unset): The outcome of one setup run, reduced to what a
                caller needs to fix it: exit code, failing line, stderr tail, and a hint when the cause is recognised. Example:
                {'duration_ms': 1, 'exit_code': 1, 'failed_command': 'example', 'failed_line': 1, 'hint': 'example',
                'hint_code': 'example', 'message': 'example', 'phase': 'example', 'setup_run_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'example', 'stderr_tail': 'example'}.
            setup_run_id (str | Unset): Setup run the status was written from. Read its log with getEnvironmentSetupRunLog
                when the status is failed.
            verified_by_user_id (str | Unset): User who requested the recorded run.
     """

    stale: bool
    status: str
    active_setup_run_id: str | Unset = UNSET
    at: datetime.datetime | Unset = UNSET
    fingerprint: str | Unset = UNSET
    image: ManagedAgentsEnvironmentSetupImage | Unset = UNSET
    image_capture: ManagedAgentsEnvironmentSetupImageCapture | Unset = UNSET
    last_run: ManagedAgentsEnvironmentSetupRunSummary | Unset = UNSET
    setup_run_id: str | Unset = UNSET
    verified_by_user_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_environment_setup_image import ManagedAgentsEnvironmentSetupImage # noqa: PLC0415
        from ..models.managed_agents_environment_setup_image_capture import ManagedAgentsEnvironmentSetupImageCapture # noqa: PLC0415
        from ..models.managed_agents_environment_setup_run_summary import ManagedAgentsEnvironmentSetupRunSummary # noqa: PLC0415
        stale = self.stale

        status = self.status

        active_setup_run_id = self.active_setup_run_id

        at: str | Unset = UNSET
        if not isinstance(self.at, Unset):
            at = self.at.isoformat()

        fingerprint = self.fingerprint

        image: dict[str, Any] | Unset = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_dict()

        image_capture: dict[str, Any] | Unset = UNSET
        if not isinstance(self.image_capture, Unset):
            image_capture = self.image_capture.to_dict()

        last_run: dict[str, Any] | Unset = UNSET
        if not isinstance(self.last_run, Unset):
            last_run = self.last_run.to_dict()

        setup_run_id = self.setup_run_id

        verified_by_user_id = self.verified_by_user_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "stale": stale,
            "status": status,
        })
        if active_setup_run_id is not UNSET:
            field_dict["active_setup_run_id"] = active_setup_run_id
        if at is not UNSET:
            field_dict["at"] = at
        if fingerprint is not UNSET:
            field_dict["fingerprint"] = fingerprint
        if image is not UNSET:
            field_dict["image"] = image
        if image_capture is not UNSET:
            field_dict["imageCapture"] = image_capture
        if last_run is not UNSET:
            field_dict["last_run"] = last_run
        if setup_run_id is not UNSET:
            field_dict["setup_run_id"] = setup_run_id
        if verified_by_user_id is not UNSET:
            field_dict["verified_by_user_id"] = verified_by_user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_environment_setup_image import ManagedAgentsEnvironmentSetupImage # noqa: PLC0415
        from ..models.managed_agents_environment_setup_image_capture import ManagedAgentsEnvironmentSetupImageCapture # noqa: PLC0415
        from ..models.managed_agents_environment_setup_run_summary import ManagedAgentsEnvironmentSetupRunSummary # noqa: PLC0415
        d = dict(src_dict)
        stale = d.pop("stale")

        status = d.pop("status")

        active_setup_run_id = d.pop("active_setup_run_id", UNSET)

        _at = d.pop("at", UNSET)
        at: datetime.datetime | Unset
        if isinstance(_at,  Unset):
            at = UNSET
        else:
            at = datetime.datetime.fromisoformat(_at)




        fingerprint = d.pop("fingerprint", UNSET)

        _image = d.pop("image", UNSET)
        image: ManagedAgentsEnvironmentSetupImage | Unset
        if isinstance(_image,  Unset):
            image = UNSET
        else:
            image = ManagedAgentsEnvironmentSetupImage.from_dict(_image)




        _image_capture = d.pop("imageCapture", UNSET)
        image_capture: ManagedAgentsEnvironmentSetupImageCapture | Unset
        if isinstance(_image_capture,  Unset):
            image_capture = UNSET
        else:
            image_capture = ManagedAgentsEnvironmentSetupImageCapture.from_dict(_image_capture)




        _last_run = d.pop("last_run", UNSET)
        last_run: ManagedAgentsEnvironmentSetupRunSummary | Unset
        if isinstance(_last_run,  Unset):
            last_run = UNSET
        else:
            last_run = ManagedAgentsEnvironmentSetupRunSummary.from_dict(_last_run)




        setup_run_id = d.pop("setup_run_id", UNSET)

        verified_by_user_id = d.pop("verified_by_user_id", UNSET)

        managed_agents_environment_setup_verification = cls(
            stale=stale,
            status=status,
            active_setup_run_id=active_setup_run_id,
            at=at,
            fingerprint=fingerprint,
            image=image,
            image_capture=image_capture,
            last_run=last_run,
            setup_run_id=setup_run_id,
            verified_by_user_id=verified_by_user_id,
        )


        managed_agents_environment_setup_verification.additional_properties = d
        return managed_agents_environment_setup_verification

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
