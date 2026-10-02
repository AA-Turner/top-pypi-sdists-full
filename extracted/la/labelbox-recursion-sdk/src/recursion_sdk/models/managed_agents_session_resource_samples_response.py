from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_session_resource_samples_response_resolution import ManagedAgentsSessionResourceSamplesResponseResolution
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_resource_sample_bucket import ManagedAgentsResourceSampleBucket
  from ..models.managed_agents_session_sandbox import ManagedAgentsSessionSandbox





T = TypeVar("T", bound="ManagedAgentsSessionResourceSamplesResponse")



@_attrs_define
class ManagedAgentsSessionResourceSamplesResponse:
    """ Sandbox CPU, memory, and accelerator usage for a session tree, as minute buckets per sandbox attachment. Samples are
    what the sandbox measured of itself, drained to the control plane on tool calls and on read.

        Example:
            {'as_of': '2026-02-18T09:30:00Z', 'buckets': [{'bucket_start': '2026-02-18T09:30:00Z', 'complete': True,
                'cpu_capacity_millicores': 1, 'cpu_limit_millicores': 1, 'cpu_millicores': [1], 'cpu_millicores_avg': 1,
                'cpu_millicores_peak': 1, 'disk_capacity_bytes': 1, 'disk_used_avg_bytes': 1, 'disk_used_bytes': [1],
                'disk_used_peak_bytes': 1, 'gpu_count': 1, 'gpu_devices': [{'index': 1, 'memory_total_bytes': 1,
                'memory_used_peak_bytes': 1, 'utilization_avg': 1.5, 'utilization_peak': 1.5}], 'gpu_memory_total_bytes': 1,
                'gpu_memory_used_bytes': [1], 'gpu_memory_used_peak_bytes': 1, 'gpu_utilization_avg': 1.5,
                'gpu_utilization_peak': 1.5, 'gpu_utilization_percent': [1.5], 'interval_ms': 1, 'memory_capacity_bytes': 1,
                'memory_limit_bytes': 1, 'memory_working_set_avg_bytes': 1, 'memory_working_set_bytes': [1],
                'memory_working_set_peak_bytes': 1, 'offsets_ms': [1], 'received_at': '2026-02-18T09:30:00Z', 'sample_count': 1,
                'sandbox_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'shared_slots': 1}], 'live': True, 'next_page_token':
                'example', 'resolution': 'minute', 'root_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sandboxes':
                [{'attached_at': '2026-02-18T09:30:00Z', 'detach_reason': 'example', 'detached_at': '2026-02-18T09:30:00Z',
                'last_drained_at': '2026-02-18T09:30:00Z', 'owner_session_path': 'example', 'revived_from_sandbox_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'role': 'user', 'sample_interval_ms': 1, 'sample_rows': 1,
                'sample_watermark_at': '2026-02-18T09:30:00Z', 'sampling_scope': 'example', 'sampling_source': 'example',
                'sandbox_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sandbox_instance_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sandbox_provider': 'example'}], 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            as_of (datetime.datetime): RFC 3339 server time at which the page was read.
            buckets (list[ManagedAgentsResourceSampleBucket] | None): One page of minute buckets ordered by (sandbox_id,
                bucket_start). Each bucket names its attachment; join on sandboxes to place it on a lane.
            live (bool): True while a sandbox that can be sampled is still attached to the tree. A client keeps polling
                while this is true and stops once it turns false; an attached sandbox that cannot measure itself does not keep
                it true.
            resolution (ManagedAgentsSessionResourceSamplesResponseResolution): Resolution the buckets were read at.
            root_session_id (str): Root of the tree the usage belongs to.
            sandboxes (list[ManagedAgentsSessionSandbox] | None): Every sandbox attachment the tree has had, oldest first,
                including ones that have since been released or closed. Empty when the tree never had a sandbox or sampling is
                disabled. Complete on every page.
            session_id (str): Session id named in the request.
            next_page_token (str | Unset): Present when more buckets remain. Pass as page_token with the same query to
                continue.
     """

    as_of: datetime.datetime
    buckets: list[ManagedAgentsResourceSampleBucket] | None
    live: bool
    resolution: ManagedAgentsSessionResourceSamplesResponseResolution
    root_session_id: str
    sandboxes: list[ManagedAgentsSessionSandbox] | None
    session_id: str
    next_page_token: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_resource_sample_bucket import ManagedAgentsResourceSampleBucket # noqa: PLC0415
        from ..models.managed_agents_session_sandbox import ManagedAgentsSessionSandbox # noqa: PLC0415
        as_of = self.as_of.isoformat()

        buckets: list[dict[str, Any]] | None
        if isinstance(self.buckets, list):
            buckets = []
            for buckets_type_0_item_data in self.buckets:
                buckets_type_0_item = buckets_type_0_item_data.to_dict()
                buckets.append(buckets_type_0_item)


        else:
            buckets = self.buckets

        live = self.live

        resolution = self.resolution.value

        root_session_id = self.root_session_id

        sandboxes: list[dict[str, Any]] | None
        if isinstance(self.sandboxes, list):
            sandboxes = []
            for sandboxes_type_0_item_data in self.sandboxes:
                sandboxes_type_0_item = sandboxes_type_0_item_data.to_dict()
                sandboxes.append(sandboxes_type_0_item)


        else:
            sandboxes = self.sandboxes

        session_id = self.session_id

        next_page_token = self.next_page_token


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "as_of": as_of,
            "buckets": buckets,
            "live": live,
            "resolution": resolution,
            "root_session_id": root_session_id,
            "sandboxes": sandboxes,
            "session_id": session_id,
        })
        if next_page_token is not UNSET:
            field_dict["next_page_token"] = next_page_token

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_resource_sample_bucket import ManagedAgentsResourceSampleBucket # noqa: PLC0415
        from ..models.managed_agents_session_sandbox import ManagedAgentsSessionSandbox # noqa: PLC0415
        d = dict(src_dict)
        as_of = datetime.datetime.fromisoformat(d.pop("as_of"))




        def _parse_buckets(data: object) -> list[ManagedAgentsResourceSampleBucket] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                buckets_type_0 = []
                _buckets_type_0 = data
                for buckets_type_0_item_data in (_buckets_type_0):
                    buckets_type_0_item = ManagedAgentsResourceSampleBucket.from_dict(buckets_type_0_item_data)



                    buckets_type_0.append(buckets_type_0_item)

                return buckets_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsResourceSampleBucket] | None, data)

        buckets = _parse_buckets(d.pop("buckets"))


        live = d.pop("live")

        resolution = ManagedAgentsSessionResourceSamplesResponseResolution(d.pop("resolution"))




        root_session_id = d.pop("root_session_id")

        def _parse_sandboxes(data: object) -> list[ManagedAgentsSessionSandbox] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                sandboxes_type_0 = []
                _sandboxes_type_0 = data
                for sandboxes_type_0_item_data in (_sandboxes_type_0):
                    sandboxes_type_0_item = ManagedAgentsSessionSandbox.from_dict(sandboxes_type_0_item_data)



                    sandboxes_type_0.append(sandboxes_type_0_item)

                return sandboxes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsSessionSandbox] | None, data)

        sandboxes = _parse_sandboxes(d.pop("sandboxes"))


        session_id = d.pop("session_id")

        next_page_token = d.pop("next_page_token", UNSET)

        managed_agents_session_resource_samples_response = cls(
            as_of=as_of,
            buckets=buckets,
            live=live,
            resolution=resolution,
            root_session_id=root_session_id,
            sandboxes=sandboxes,
            session_id=session_id,
            next_page_token=next_page_token,
        )


        managed_agents_session_resource_samples_response.additional_properties = d
        return managed_agents_session_resource_samples_response

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
