from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.container_v2_failure import ContainerV2Failure
    from ..models.container_v2_migration import ContainerV2Migration
    from ..models.container_v2_resources import ContainerV2Resources
    from ..models.container_v2_usage import ContainerV2Usage
    from ..models.timeout_policy import TimeoutPolicy


T = TypeVar("T", bound="ContainerV2")


@_attrs_define
class ContainerV2:
    """
    Attributes:
        id (str):
        architecture (str):
        revision (int):
        pending_change (bool):
        phase (str):
        auto_shutdown_policy (TimeoutPolicy | Unset):
        auto_delete_policy (TimeoutPolicy | Unset):
        auto_shutdown_at (datetime.datetime | Unset):
        auto_delete_at (datetime.datetime | Unset):
        image (str | Unset):
        name (str | Unset):
        worker_id (str | Unset):
        desired_state (str | Unset):
        actual_state (str | Unset):
        migration (ContainerV2Migration | Unset):
        observed_at_unix_millis (int | Unset):
        resources (ContainerV2Resources | Unset):
        applied_resources (ContainerV2Resources | Unset):
        usage (ContainerV2Usage | Unset):
        failure (ContainerV2Failure | Unset):
        main_process_id (str | Unset):
    """

    id: str
    architecture: str
    revision: int
    pending_change: bool
    phase: str
    auto_shutdown_policy: TimeoutPolicy | Unset = UNSET
    auto_delete_policy: TimeoutPolicy | Unset = UNSET
    auto_shutdown_at: datetime.datetime | Unset = UNSET
    auto_delete_at: datetime.datetime | Unset = UNSET
    image: str | Unset = UNSET
    name: str | Unset = UNSET
    worker_id: str | Unset = UNSET
    desired_state: str | Unset = UNSET
    actual_state: str | Unset = UNSET
    migration: ContainerV2Migration | Unset = UNSET
    observed_at_unix_millis: int | Unset = UNSET
    resources: ContainerV2Resources | Unset = UNSET
    applied_resources: ContainerV2Resources | Unset = UNSET
    usage: ContainerV2Usage | Unset = UNSET
    failure: ContainerV2Failure | Unset = UNSET
    main_process_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        architecture = self.architecture

        revision = self.revision

        pending_change = self.pending_change

        phase = self.phase

        auto_shutdown_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.auto_shutdown_policy, Unset):
            auto_shutdown_policy = self.auto_shutdown_policy.to_dict()

        auto_delete_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.auto_delete_policy, Unset):
            auto_delete_policy = self.auto_delete_policy.to_dict()

        auto_shutdown_at: str | Unset = UNSET
        if not isinstance(self.auto_shutdown_at, Unset):
            auto_shutdown_at = self.auto_shutdown_at.isoformat()

        auto_delete_at: str | Unset = UNSET
        if not isinstance(self.auto_delete_at, Unset):
            auto_delete_at = self.auto_delete_at.isoformat()

        image = self.image

        name = self.name

        worker_id = self.worker_id

        desired_state = self.desired_state

        actual_state = self.actual_state

        migration: dict[str, Any] | Unset = UNSET
        if not isinstance(self.migration, Unset):
            migration = self.migration.to_dict()

        observed_at_unix_millis = self.observed_at_unix_millis

        resources: dict[str, Any] | Unset = UNSET
        if not isinstance(self.resources, Unset):
            resources = self.resources.to_dict()

        applied_resources: dict[str, Any] | Unset = UNSET
        if not isinstance(self.applied_resources, Unset):
            applied_resources = self.applied_resources.to_dict()

        usage: dict[str, Any] | Unset = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()

        failure: dict[str, Any] | Unset = UNSET
        if not isinstance(self.failure, Unset):
            failure = self.failure.to_dict()

        main_process_id = self.main_process_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "architecture": architecture,
                "revision": revision,
                "pending_change": pending_change,
                "phase": phase,
            }
        )
        if auto_shutdown_policy is not UNSET:
            field_dict["auto_shutdown_policy"] = auto_shutdown_policy
        if auto_delete_policy is not UNSET:
            field_dict["auto_delete_policy"] = auto_delete_policy
        if auto_shutdown_at is not UNSET:
            field_dict["auto_shutdown_at"] = auto_shutdown_at
        if auto_delete_at is not UNSET:
            field_dict["auto_delete_at"] = auto_delete_at
        if image is not UNSET:
            field_dict["image"] = image
        if name is not UNSET:
            field_dict["name"] = name
        if worker_id is not UNSET:
            field_dict["worker_id"] = worker_id
        if desired_state is not UNSET:
            field_dict["desired_state"] = desired_state
        if actual_state is not UNSET:
            field_dict["actual_state"] = actual_state
        if migration is not UNSET:
            field_dict["migration"] = migration
        if observed_at_unix_millis is not UNSET:
            field_dict["observed_at_unix_millis"] = observed_at_unix_millis
        if resources is not UNSET:
            field_dict["resources"] = resources
        if applied_resources is not UNSET:
            field_dict["applied_resources"] = applied_resources
        if usage is not UNSET:
            field_dict["usage"] = usage
        if failure is not UNSET:
            field_dict["failure"] = failure
        if main_process_id is not UNSET:
            field_dict["main_process_id"] = main_process_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.container_v2_failure import ContainerV2Failure
        from ..models.container_v2_migration import ContainerV2Migration
        from ..models.container_v2_resources import ContainerV2Resources
        from ..models.container_v2_usage import ContainerV2Usage
        from ..models.timeout_policy import TimeoutPolicy

        d = dict(src_dict)
        id = d.pop("id")

        architecture = d.pop("architecture")

        revision = d.pop("revision")

        pending_change = d.pop("pending_change")

        phase = d.pop("phase")

        _auto_shutdown_policy = d.pop("auto_shutdown_policy", UNSET)
        auto_shutdown_policy: TimeoutPolicy | Unset
        if isinstance(_auto_shutdown_policy, Unset):
            auto_shutdown_policy = UNSET
        else:
            auto_shutdown_policy = TimeoutPolicy.from_dict(_auto_shutdown_policy)

        _auto_delete_policy = d.pop("auto_delete_policy", UNSET)
        auto_delete_policy: TimeoutPolicy | Unset
        if isinstance(_auto_delete_policy, Unset):
            auto_delete_policy = UNSET
        else:
            auto_delete_policy = TimeoutPolicy.from_dict(_auto_delete_policy)

        _auto_shutdown_at = d.pop("auto_shutdown_at", UNSET)
        auto_shutdown_at: datetime.datetime | Unset
        if isinstance(_auto_shutdown_at, Unset):
            auto_shutdown_at = UNSET
        else:
            auto_shutdown_at = datetime.datetime.fromisoformat(
                _auto_shutdown_at.replace("Z", "+00:00")
            )

        _auto_delete_at = d.pop("auto_delete_at", UNSET)
        auto_delete_at: datetime.datetime | Unset
        if isinstance(_auto_delete_at, Unset):
            auto_delete_at = UNSET
        else:
            auto_delete_at = datetime.datetime.fromisoformat(
                _auto_delete_at.replace("Z", "+00:00")
            )

        image = d.pop("image", UNSET)

        name = d.pop("name", UNSET)

        worker_id = d.pop("worker_id", UNSET)

        desired_state = d.pop("desired_state", UNSET)

        actual_state = d.pop("actual_state", UNSET)

        _migration = d.pop("migration", UNSET)
        migration: ContainerV2Migration | Unset
        if isinstance(_migration, Unset):
            migration = UNSET
        else:
            migration = ContainerV2Migration.from_dict(_migration)

        observed_at_unix_millis = d.pop("observed_at_unix_millis", UNSET)

        _resources = d.pop("resources", UNSET)
        resources: ContainerV2Resources | Unset
        if isinstance(_resources, Unset):
            resources = UNSET
        else:
            resources = ContainerV2Resources.from_dict(_resources)

        _applied_resources = d.pop("applied_resources", UNSET)
        applied_resources: ContainerV2Resources | Unset
        if isinstance(_applied_resources, Unset):
            applied_resources = UNSET
        else:
            applied_resources = ContainerV2Resources.from_dict(_applied_resources)

        _usage = d.pop("usage", UNSET)
        usage: ContainerV2Usage | Unset
        if isinstance(_usage, Unset):
            usage = UNSET
        else:
            usage = ContainerV2Usage.from_dict(_usage)

        _failure = d.pop("failure", UNSET)
        failure: ContainerV2Failure | Unset
        if isinstance(_failure, Unset):
            failure = UNSET
        else:
            failure = ContainerV2Failure.from_dict(_failure)

        main_process_id = d.pop("main_process_id", UNSET)

        container_v2 = cls(
            id=id,
            architecture=architecture,
            revision=revision,
            pending_change=pending_change,
            phase=phase,
            auto_shutdown_policy=auto_shutdown_policy,
            auto_delete_policy=auto_delete_policy,
            auto_shutdown_at=auto_shutdown_at,
            auto_delete_at=auto_delete_at,
            image=image,
            name=name,
            worker_id=worker_id,
            desired_state=desired_state,
            actual_state=actual_state,
            migration=migration,
            observed_at_unix_millis=observed_at_unix_millis,
            resources=resources,
            applied_resources=applied_resources,
            usage=usage,
            failure=failure,
            main_process_id=main_process_id,
        )

        container_v2.additional_properties = d
        return container_v2

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
