from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.public_checkpoint_state import PublicCheckpointState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.checkpoint_source_runtime import CheckpointSourceRuntime
    from ..models.runtime_resources import RuntimeResources


T = TypeVar("T", bound="Checkpoint")


@_attrs_define
class Checkpoint:
    """Checkpoint response object.

    Attributes:
        display_name (str): User-chosen display name.
        id (str): Stable checkpoint UUID.
        created_at (str): RFC3339 timestamp when the control-plane checkpoint row was created.
        resources (RuntimeResources): Runtime resource requests and limits.
        state (PublicCheckpointState): Checkpoint lifecycle state.
        kind (str | Unset): Canonical checkpoint kind, full or cold. Absent on older servers.
        safe_error_code (None | str | Unset): Bounded non-sensitive reason when checkpoint creation failed.
        source_runtime (CheckpointSourceRuntime | Unset): Source runtime lineage for a checkpoint.
    """

    display_name: str
    id: str
    created_at: str
    resources: RuntimeResources
    state: PublicCheckpointState
    kind: str | Unset = UNSET
    safe_error_code: None | str | Unset = UNSET
    source_runtime: CheckpointSourceRuntime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        id = self.id

        created_at = self.created_at

        resources = self.resources.to_dict()

        state = self.state.value

        kind = self.kind

        safe_error_code: None | str | Unset
        if isinstance(self.safe_error_code, Unset):
            safe_error_code = UNSET
        else:
            safe_error_code = self.safe_error_code

        source_runtime: dict[str, Any] | Unset = UNSET
        if not isinstance(self.source_runtime, Unset):
            source_runtime = self.source_runtime.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "display_name": display_name,
                "id": id,
                "created_at": created_at,
                "resources": resources,
                "state": state,
            }
        )
        if kind is not UNSET:
            field_dict["kind"] = kind
        if safe_error_code is not UNSET:
            field_dict["safe_error_code"] = safe_error_code
        if source_runtime is not UNSET:
            field_dict["source_runtime"] = source_runtime

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.checkpoint_source_runtime import CheckpointSourceRuntime
        from ..models.runtime_resources import RuntimeResources

        d = dict(src_dict)
        display_name = d.pop("display_name")

        id = d.pop("id")

        created_at = d.pop("created_at")

        resources = RuntimeResources.from_dict(d.pop("resources"))

        state = PublicCheckpointState(d.pop("state"))

        kind = d.pop("kind", UNSET)

        def _parse_safe_error_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        safe_error_code = _parse_safe_error_code(d.pop("safe_error_code", UNSET))

        _source_runtime = d.pop("source_runtime", UNSET)
        source_runtime: CheckpointSourceRuntime | Unset
        if isinstance(_source_runtime, Unset):
            source_runtime = UNSET
        else:
            source_runtime = CheckpointSourceRuntime.from_dict(_source_runtime)

        checkpoint = cls(
            display_name=display_name,
            id=id,
            created_at=created_at,
            resources=resources,
            state=state,
            kind=kind,
            safe_error_code=safe_error_code,
            source_runtime=source_runtime,
        )

        checkpoint.additional_properties = d
        return checkpoint

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
