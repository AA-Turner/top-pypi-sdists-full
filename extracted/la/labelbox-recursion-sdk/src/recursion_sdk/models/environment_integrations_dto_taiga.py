from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="EnvironmentIntegrationsDtoTaiga")



@_attrs_define
class EnvironmentIntegrationsDtoTaiga:
    """ Taiga integration settings for one environment.

        Attributes:
            enabled (bool): When true, the Send-to-Taiga button is visible in the env-overview toolbar.
            default_env_id (None | str): Default Taiga env id pre-filled in the Send-to-Taiga dialog. Null leaves the field
                empty.
            default_api_model_name (None | str): Default solver model forwarded to Taiga at submission time. Null falls back
                to the platform default at dialog render time.
            default_n_attempts_per_problem (int | None): Default attempts-per-problem forwarded to Taiga at submission time.
                Null falls back to the platform default.
            strict_compatibility (bool): When true, the problem editor disables grading shapes that Send-to-Taiga can't
                honor (max composition) and the backend rejects locking a draft whose grading_config contains any of them. A
                per-leaf programmatic graderImage is not gated — it is ignored on Taiga (the grade runs in the env image).
            sync_on_lock (bool): When true, locking a problem version eagerly pushes it to Taiga (creates/updates the
                corresponding Taiga problem + problem-version). When false, the push happens lazily on the next Send-to-Taiga.
            taiga_image_url (None | str): Per-env image URL used as the Taiga problem container. Required when sync-on-lock
                is enabled (lock validation rejects an empty value in that case) and on every Send-to-Taiga submission (the per-
                submission dialog can pick a different image, but one or the other must resolve). The gate does NOT fire merely
                because the integration is enabled. Picked from the org's Taiga image catalog via the integration UI — selection
                copies the built image URI here, snapshot-style. Stored as plain text with no FK to the catalog, so catalog
                deletions do not invalidate existing integrations.
            import_problem_run_results (bool): When true (default), Send-to-Taiga imports each Taiga problem-run back into
                Recursion as a problem_run row. When false, the export runs on Taiga but no Recursion problem_runs are created.
     """

    enabled: bool
    default_env_id: None | str
    default_api_model_name: None | str
    default_n_attempts_per_problem: int | None
    strict_compatibility: bool
    sync_on_lock: bool
    taiga_image_url: None | str
    import_problem_run_results: bool





    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        default_env_id: None | str
        default_env_id = self.default_env_id

        default_api_model_name: None | str
        default_api_model_name = self.default_api_model_name

        default_n_attempts_per_problem: int | None
        default_n_attempts_per_problem = self.default_n_attempts_per_problem

        strict_compatibility = self.strict_compatibility

        sync_on_lock = self.sync_on_lock

        taiga_image_url: None | str
        taiga_image_url = self.taiga_image_url

        import_problem_run_results = self.import_problem_run_results


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "enabled": enabled,
            "defaultEnvId": default_env_id,
            "defaultApiModelName": default_api_model_name,
            "defaultNAttemptsPerProblem": default_n_attempts_per_problem,
            "strictCompatibility": strict_compatibility,
            "syncOnLock": sync_on_lock,
            "taigaImageUrl": taiga_image_url,
            "importProblemRunResults": import_problem_run_results,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        def _parse_default_env_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        default_env_id = _parse_default_env_id(d.pop("defaultEnvId"))


        def _parse_default_api_model_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        default_api_model_name = _parse_default_api_model_name(d.pop("defaultApiModelName"))


        def _parse_default_n_attempts_per_problem(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        default_n_attempts_per_problem = _parse_default_n_attempts_per_problem(d.pop("defaultNAttemptsPerProblem"))


        strict_compatibility = d.pop("strictCompatibility")

        sync_on_lock = d.pop("syncOnLock")

        def _parse_taiga_image_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        taiga_image_url = _parse_taiga_image_url(d.pop("taigaImageUrl"))


        import_problem_run_results = d.pop("importProblemRunResults")

        environment_integrations_dto_taiga = cls(
            enabled=enabled,
            default_env_id=default_env_id,
            default_api_model_name=default_api_model_name,
            default_n_attempts_per_problem=default_n_attempts_per_problem,
            strict_compatibility=strict_compatibility,
            sync_on_lock=sync_on_lock,
            taiga_image_url=taiga_image_url,
            import_problem_run_results=import_problem_run_results,
        )

        return environment_integrations_dto_taiga

