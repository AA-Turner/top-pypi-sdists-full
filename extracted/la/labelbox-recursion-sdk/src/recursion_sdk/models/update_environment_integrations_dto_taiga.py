from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="UpdateEnvironmentIntegrationsDtoTaiga")



@_attrs_define
class UpdateEnvironmentIntegrationsDtoTaiga:
    """ Patch-style update for the Taiga integration. Omitting a field leaves the existing value untouched.

        Attributes:
            enabled (bool | Unset): When true, the Send-to-Taiga button is visible in the env-overview toolbar.
            default_env_id (None | str | Unset): Default Taiga env id pre-filled in the Send-to-Taiga dialog. Null leaves
                the field empty.
            default_api_model_name (None | str | Unset): Default solver model forwarded to Taiga at submission time. Null
                falls back to the platform default at dialog render time.
            default_n_attempts_per_problem (int | None | Unset): Default attempts-per-problem forwarded to Taiga at
                submission time. Null falls back to the platform default.
            strict_compatibility (bool | Unset): When true, the problem editor disables grading shapes that Send-to-Taiga
                can't honor (max composition) and the backend rejects locking a draft whose grading_config contains any of them.
                A per-leaf programmatic graderImage is not gated — it is ignored on Taiga (the grade runs in the env image).
            sync_on_lock (bool | Unset): When true, locking a problem version eagerly pushes it to Taiga (creates/updates
                the corresponding Taiga problem + problem-version). When false, the push happens lazily on the next Send-to-
                Taiga.
            taiga_image_url (None | str | Unset): Per-env image URL used as the Taiga problem container. Required when sync-
                on-lock is enabled (lock validation rejects an empty value in that case) and on every Send-to-Taiga submission
                (the per-submission dialog can pick a different image, but one or the other must resolve). The gate does NOT
                fire merely because the integration is enabled. Picked from the org's Taiga image catalog via the integration UI
                — selection copies the built image URI here, snapshot-style. Stored as plain text with no FK to the catalog, so
                catalog deletions do not invalidate existing integrations.
            import_problem_run_results (bool | Unset): When true (default), Send-to-Taiga imports each Taiga problem-run
                back into Recursion as a problem_run row. When false, the export runs on Taiga but no Recursion problem_runs are
                created.
     """

    enabled: bool | Unset = UNSET
    default_env_id: None | str | Unset = UNSET
    default_api_model_name: None | str | Unset = UNSET
    default_n_attempts_per_problem: int | None | Unset = UNSET
    strict_compatibility: bool | Unset = UNSET
    sync_on_lock: bool | Unset = UNSET
    taiga_image_url: None | str | Unset = UNSET
    import_problem_run_results: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        default_env_id: None | str | Unset
        if isinstance(self.default_env_id, Unset):
            default_env_id = UNSET
        else:
            default_env_id = self.default_env_id

        default_api_model_name: None | str | Unset
        if isinstance(self.default_api_model_name, Unset):
            default_api_model_name = UNSET
        else:
            default_api_model_name = self.default_api_model_name

        default_n_attempts_per_problem: int | None | Unset
        if isinstance(self.default_n_attempts_per_problem, Unset):
            default_n_attempts_per_problem = UNSET
        else:
            default_n_attempts_per_problem = self.default_n_attempts_per_problem

        strict_compatibility = self.strict_compatibility

        sync_on_lock = self.sync_on_lock

        taiga_image_url: None | str | Unset
        if isinstance(self.taiga_image_url, Unset):
            taiga_image_url = UNSET
        else:
            taiga_image_url = self.taiga_image_url

        import_problem_run_results = self.import_problem_run_results


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if default_env_id is not UNSET:
            field_dict["defaultEnvId"] = default_env_id
        if default_api_model_name is not UNSET:
            field_dict["defaultApiModelName"] = default_api_model_name
        if default_n_attempts_per_problem is not UNSET:
            field_dict["defaultNAttemptsPerProblem"] = default_n_attempts_per_problem
        if strict_compatibility is not UNSET:
            field_dict["strictCompatibility"] = strict_compatibility
        if sync_on_lock is not UNSET:
            field_dict["syncOnLock"] = sync_on_lock
        if taiga_image_url is not UNSET:
            field_dict["taigaImageUrl"] = taiga_image_url
        if import_problem_run_results is not UNSET:
            field_dict["importProblemRunResults"] = import_problem_run_results

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        def _parse_default_env_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        default_env_id = _parse_default_env_id(d.pop("defaultEnvId", UNSET))


        def _parse_default_api_model_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        default_api_model_name = _parse_default_api_model_name(d.pop("defaultApiModelName", UNSET))


        def _parse_default_n_attempts_per_problem(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        default_n_attempts_per_problem = _parse_default_n_attempts_per_problem(d.pop("defaultNAttemptsPerProblem", UNSET))


        strict_compatibility = d.pop("strictCompatibility", UNSET)

        sync_on_lock = d.pop("syncOnLock", UNSET)

        def _parse_taiga_image_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        taiga_image_url = _parse_taiga_image_url(d.pop("taigaImageUrl", UNSET))


        import_problem_run_results = d.pop("importProblemRunResults", UNSET)

        update_environment_integrations_dto_taiga = cls(
            enabled=enabled,
            default_env_id=default_env_id,
            default_api_model_name=default_api_model_name,
            default_n_attempts_per_problem=default_n_attempts_per_problem,
            strict_compatibility=strict_compatibility,
            sync_on_lock=sync_on_lock,
            taiga_image_url=taiga_image_url,
            import_problem_run_results=import_problem_run_results,
        )


        update_environment_integrations_dto_taiga.additional_properties = d
        return update_environment_integrations_dto_taiga

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
