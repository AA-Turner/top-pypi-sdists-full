from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID






T = TypeVar("T", bound="OwnedComputeListResponseDtoItemsItem")



@_attrs_define
class OwnedComputeListResponseDtoItemsItem:
    """ Compute payload enriched with the platform-side owner/run-config metadata.

        Example:
            {'id': 'b394e9de-3306-498a-b9a5-34749b57aaf1', 'name': 'vision-agent-dev', 'status': 'running', 'errorMessage':
                None, 'createdAt': '2026-01-15T09:30:00.000Z', 'startedAt': '2026-01-15T09:30:12.000Z', 'stoppedAt': None,
                'containerImage': 'us-docker.pkg.dev/example-project/recursion-agents/vision-agent:1.4.2', 'pvcSizeGi': 20,
                'httpPort': 8080, 'idleStopAfterSeconds': 2592000, 'stoppedDeleteAfterSeconds': 2592000, 'environmentId':
                '784e2386-e297-4f9d-a886-838422383b65', 'runConfigVersionId': '39088cb6-ca62-4544-a074-fc66e10807ad',
                'runConfigId': '5b1f0e2a-7c3d-4e8f-9a6b-2d4c8e1f3a57', 'runConfigVersionNumber': 3}

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
            environment_id (UUID): Environment that owns this compute.
            run_config_version_id (None | UUID): Run-config version that launched this compute, when one was associated;
                null otherwise.
            run_config_id (None | UUID): Run config that owns the launching run-config version; null when no version was
                associated.
            run_config_version_number (int | None): Version number of the launching run-config version within its run
                config; null when no version was associated.
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
    environment_id: UUID
    run_config_version_id: None | UUID
    run_config_id: None | UUID
    run_config_version_number: int | None





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

        environment_id = str(self.environment_id)

        run_config_version_id: None | str
        if isinstance(self.run_config_version_id, UUID):
            run_config_version_id = str(self.run_config_version_id)
        else:
            run_config_version_id = self.run_config_version_id

        run_config_id: None | str
        if isinstance(self.run_config_id, UUID):
            run_config_id = str(self.run_config_id)
        else:
            run_config_id = self.run_config_id

        run_config_version_number: int | None
        run_config_version_number = self.run_config_version_number


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
            "environmentId": environment_id,
            "runConfigVersionId": run_config_version_id,
            "runConfigId": run_config_id,
            "runConfigVersionNumber": run_config_version_number,
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

        environment_id = UUID(d.pop("environmentId"))




        def _parse_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                run_config_version_id_type_0 = UUID(data)



                return run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        run_config_version_id = _parse_run_config_version_id(d.pop("runConfigVersionId"))


        def _parse_run_config_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                run_config_id_type_0 = UUID(data)



                return run_config_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        run_config_id = _parse_run_config_id(d.pop("runConfigId"))


        def _parse_run_config_version_number(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        run_config_version_number = _parse_run_config_version_number(d.pop("runConfigVersionNumber"))


        owned_compute_list_response_dto_items_item = cls(
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
            environment_id=environment_id,
            run_config_version_id=run_config_version_id,
            run_config_id=run_config_id,
            run_config_version_number=run_config_version_number,
        )

        return owned_compute_list_response_dto_items_item

