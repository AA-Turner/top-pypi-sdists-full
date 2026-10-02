from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_environment_setup_run import ManagedAgentsEnvironmentSetupRun





T = TypeVar("T", bound="ManagedAgentsEnvironmentSetupRunListResponse")



@_attrs_define
class ManagedAgentsEnvironmentSetupRunListResponse:
    """ Recent setup runs for one environment, newest first. The newest manual run is the one the environment's
    setup_verification describes.

        Example:
            {'setup_runs': [{'compute_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'compute_profile': {'key': 'example'},
                'created_at': '2026-02-18T09:30:00Z', 'duration_ms': 1, 'environment_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'exit_code': 1, 'failed_command': 'example', 'failed_line': 1,
                'failure_code': 'example', 'fingerprint': 'example', 'finished_at': '2026-02-18T09:30:00Z', 'gpu_readiness':
                {'key': 'example'}, 'hint': 'example', 'hint_code': 'example', 'image': 'example', 'imageCapture': {'at':
                '2026-02-18T09:30:00Z', 'message': 'example', 'reason': 'example', 'setupRunId': 'example', 'status': 'failed'},
                'imageId': 'example', 'kind': 'example', 'log_bytes': 1, 'log_lines': 1, 'log_truncated': True, 'message':
                'example', 'next_action': {'method': 'example', 'operation_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'path':
                'example'}, 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'phase': 'example',
                'providerEventCursor': 1, 'providerRunId': 'example', 'requested_by_user_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'setupImage':
                {'baseImageDigest': 'example', 'capturedAt': '2026-02-18T09:30:00Z', 'computeId': 'example', 'fingerprint':
                'example', 'generation': 1, 'image': 'example', 'imageId': 'example', 'runnerImage': 'example', 'setupRunId':
                'example', 'sizeBytes': 1, 'usable': True, 'warmup': 'example', 'warmupMessage': 'example'}, 'setup_run_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'started_at': '2026-02-18T09:30:00Z', 'status': 'example',
                'stderr_tail': 'example'}]}

        Attributes:
            setup_runs (list[ManagedAgentsEnvironmentSetupRun] | None): The environment's setup runs, newest first. Empty
                array when none has been requested.
     """

    setup_runs: list[ManagedAgentsEnvironmentSetupRun] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_environment_setup_run import ManagedAgentsEnvironmentSetupRun # noqa: PLC0415
        setup_runs: list[dict[str, Any]] | None
        if isinstance(self.setup_runs, list):
            setup_runs = []
            for setup_runs_type_0_item_data in self.setup_runs:
                setup_runs_type_0_item = setup_runs_type_0_item_data.to_dict()
                setup_runs.append(setup_runs_type_0_item)


        else:
            setup_runs = self.setup_runs


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "setup_runs": setup_runs,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_environment_setup_run import ManagedAgentsEnvironmentSetupRun # noqa: PLC0415
        d = dict(src_dict)
        def _parse_setup_runs(data: object) -> list[ManagedAgentsEnvironmentSetupRun] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                setup_runs_type_0 = []
                _setup_runs_type_0 = data
                for setup_runs_type_0_item_data in (_setup_runs_type_0):
                    setup_runs_type_0_item = ManagedAgentsEnvironmentSetupRun.from_dict(setup_runs_type_0_item_data)



                    setup_runs_type_0.append(setup_runs_type_0_item)

                return setup_runs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsEnvironmentSetupRun] | None, data)

        setup_runs = _parse_setup_runs(d.pop("setup_runs"))


        managed_agents_environment_setup_run_list_response = cls(
            setup_runs=setup_runs,
        )


        managed_agents_environment_setup_run_list_response.additional_properties = d
        return managed_agents_environment_setup_run_list_response

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
