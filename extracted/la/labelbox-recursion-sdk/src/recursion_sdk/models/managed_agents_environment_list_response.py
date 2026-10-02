from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_environment import ManagedAgentsEnvironment





T = TypeVar("T", bound="ManagedAgentsEnvironmentListResponse")



@_attrs_define
class ManagedAgentsEnvironmentListResponse:
    """ Response body of GET /v1/environments. An environment is the sandbox recipe a session runs inside; pick an
    environment_id from here when starting a session with POST /v1/sessions.

        Example:
            {'environments': [{'computer_use': True, 'config': {'key': 'example'}, 'created_at': '2026-02-18T09:30:00Z',
                'description': 'example', 'env_vars': {'key': 'example'}, 'environment_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'http_port': 1, 'idle_stop_after_seconds': 1, 'image': 'example',
                'metadata': {'key': 'example'}, 'mounts': [{'mount_path': 'example', 'source': 'example'}], 'name': 'example-
                name', 'network_policy': {'key': 'example'}, 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'privileged': True, 'provider': 'example', 'pvc_size_gi': 1, 'resources': {'accelerator': {'count': 1, 'name':
                'example-name', 'type': 'example'}, 'cpu_milli': 1, 'memory_mib': 1, 'placement': {'allow_spot': True,
                'max_price_per_hour_usd': 1.5, 'min_accelerator_vram_gb': 1, 'providers': ['example'], 'regions': ['example']},
                'timeout_seconds': 1}, 'scope': 'example', 'secrets': {'key': 'example'}, 'setup': {'script': 'example',
                'timeout_seconds': 1}, 'setup_updated_at': '2026-02-18T09:30:00Z', 'setup_updated_by_user_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'setup_verification': {'active_setup_run_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'at': '2026-02-18T09:30:00Z', 'fingerprint': 'example', 'image':
                {'baseImageDigest': 'example', 'capturedAt': '2026-02-18T09:30:00Z', 'computeId': 'example', 'fingerprint':
                'example', 'generation': 1, 'image': 'example', 'imageId': 'example', 'runnerImage': 'example', 'setupRunId':
                'example', 'sizeBytes': 1, 'usable': True, 'warmup': 'example', 'warmupMessage': 'example'}, 'imageCapture':
                {'at': '2026-02-18T09:30:00Z', 'message': 'example', 'reason': 'example', 'setupRunId': 'example', 'status':
                'failed'}, 'last_run': {'duration_ms': 1, 'exit_code': 1, 'failed_command': 'example', 'failed_line': 1, 'hint':
                'example', 'hint_code': 'example', 'message': 'example', 'phase': 'example', 'setup_run_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'example', 'stderr_tail': 'example'}, 'setup_run_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'stale': True, 'status': 'example', 'verified_by_user_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'setup_warnings': [{'code': 'example', 'line': 1, 'message':
                'example'}], 'stopped_delete_after_seconds': 1, 'updated_at': '2026-02-18T09:30:00Z'}]}

        Attributes:
            environments (list[ManagedAgentsEnvironment] | None): Every environment in the caller's organization, newest
                first. Null rather than an empty array when the organization has no environments. Soft-deleted environments are
                omitted.
     """

    environments: list[ManagedAgentsEnvironment] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_environment import ManagedAgentsEnvironment # noqa: PLC0415
        environments: list[dict[str, Any]] | None
        if isinstance(self.environments, list):
            environments = []
            for environments_type_0_item_data in self.environments:
                environments_type_0_item = environments_type_0_item_data.to_dict()
                environments.append(environments_type_0_item)


        else:
            environments = self.environments


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "environments": environments,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_environment import ManagedAgentsEnvironment # noqa: PLC0415
        d = dict(src_dict)
        def _parse_environments(data: object) -> list[ManagedAgentsEnvironment] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                environments_type_0 = []
                _environments_type_0 = data
                for environments_type_0_item_data in (_environments_type_0):
                    environments_type_0_item = ManagedAgentsEnvironment.from_dict(environments_type_0_item_data)



                    environments_type_0.append(environments_type_0_item)

                return environments_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsEnvironment] | None, data)

        environments = _parse_environments(d.pop("environments"))


        managed_agents_environment_list_response = cls(
            environments=environments,
        )


        managed_agents_environment_list_response.additional_properties = d
        return managed_agents_environment_list_response

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
