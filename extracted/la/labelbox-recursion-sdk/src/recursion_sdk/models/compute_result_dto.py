from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID






T = TypeVar("T", bound="ComputeResultDto")



@_attrs_define
class ComputeResultDto:
    """ Mirror of the agent-service ComputeResult payload — lifecycle metadata for a single compute.

        Example:
            {'id': 'b394e9de-3306-498a-b9a5-34749b57aaf1', 'name': 'vision-agent-dev', 'status': 'running', 'errorMessage':
                None, 'createdAt': '2026-01-15T09:30:00.000Z', 'startedAt': '2026-01-15T09:30:12.000Z', 'stoppedAt': None,
                'containerImage': 'us-docker.pkg.dev/example-project/recursion-agents/vision-agent:1.4.2', 'pvcSizeGi': 20,
                'httpPort': 8080, 'idleStopAfterSeconds': 2592000, 'stoppedDeleteAfterSeconds': 2592000}

        Attributes:
            id (UUID): Stable identifier of the compute (issued by agent-service).
            name (str): Human-readable compute name.
            status (str): Lifecycle status reported by agent-service (e.g. "pending", "running", "stopped").
            error_message (None | str): Error message emitted by the runtime if the compute failed; null otherwise.
            created_at (str): Timestamp when the compute was created (ISO-8601, UTC).
            started_at (None | str): Timestamp when the compute entered the running state (ISO-8601, UTC); null while
                pending.
            stopped_at (None | str): Timestamp when the compute terminated (ISO-8601, UTC); null while still running.
            container_image (None | str): Container image the compute was launched with; null when not yet resolved.
            pvc_size_gi (float): Size of the attached persistent volume claim in GiB.
            http_port (float | None): Container HTTP port exposed for redemption; null when no port was requested.
            idle_stop_after_seconds (int): Idle-stop timeout in seconds; maximum 30 days.
            stopped_delete_after_seconds (int): Stopped-to-deleted timeout in seconds; maximum 30 days.
     """

    id: UUID
    name: str
    status: str
    error_message: None | str
    created_at: str
    started_at: None | str
    stopped_at: None | str
    container_image: None | str
    pvc_size_gi: float
    http_port: float | None
    idle_stop_after_seconds: int
    stopped_delete_after_seconds: int





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        status = self.status

        error_message: None | str
        error_message = self.error_message

        created_at = self.created_at

        started_at: None | str
        started_at = self.started_at

        stopped_at: None | str
        stopped_at = self.stopped_at

        container_image: None | str
        container_image = self.container_image

        pvc_size_gi = self.pvc_size_gi

        http_port: float | None
        http_port = self.http_port

        idle_stop_after_seconds = self.idle_stop_after_seconds

        stopped_delete_after_seconds = self.stopped_delete_after_seconds


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "name": name,
            "status": status,
            "errorMessage": error_message,
            "createdAt": created_at,
            "startedAt": started_at,
            "stoppedAt": stopped_at,
            "containerImage": container_image,
            "pvcSizeGi": pvc_size_gi,
            "httpPort": http_port,
            "idleStopAfterSeconds": idle_stop_after_seconds,
            "stoppedDeleteAfterSeconds": stopped_delete_after_seconds,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        name = d.pop("name")

        status = d.pop("status")

        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("errorMessage"))


        created_at = d.pop("createdAt")

        def _parse_started_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        started_at = _parse_started_at(d.pop("startedAt"))


        def _parse_stopped_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        stopped_at = _parse_stopped_at(d.pop("stoppedAt"))


        def _parse_container_image(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        container_image = _parse_container_image(d.pop("containerImage"))


        pvc_size_gi = d.pop("pvcSizeGi")

        def _parse_http_port(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        http_port = _parse_http_port(d.pop("httpPort"))


        idle_stop_after_seconds = d.pop("idleStopAfterSeconds")

        stopped_delete_after_seconds = d.pop("stoppedDeleteAfterSeconds")

        compute_result_dto = cls(
            id=id,
            name=name,
            status=status,
            error_message=error_message,
            created_at=created_at,
            started_at=started_at,
            stopped_at=stopped_at,
            container_image=container_image,
            pvc_size_gi=pvc_size_gi,
            http_port=http_port,
            idle_stop_after_seconds=idle_stop_after_seconds,
            stopped_delete_after_seconds=stopped_delete_after_seconds,
        )

        return compute_result_dto

