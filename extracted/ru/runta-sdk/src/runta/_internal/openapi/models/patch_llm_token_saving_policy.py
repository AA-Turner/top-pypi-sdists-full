from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchLlmTokenSavingPolicy")


@_attrs_define
class PatchLlmTokenSavingPolicy:
    """Per-method LLM tool-output compression patch. Omitted fields remain unchanged.

    Attributes:
        json_array_enabled (bool | Unset):
        log_enabled (bool | Unset):
        search_results_enabled (bool | Unset):
        git_diff_enabled (bool | Unset):
    """

    json_array_enabled: bool | Unset = UNSET
    log_enabled: bool | Unset = UNSET
    search_results_enabled: bool | Unset = UNSET
    git_diff_enabled: bool | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        json_array_enabled = self.json_array_enabled

        log_enabled = self.log_enabled

        search_results_enabled = self.search_results_enabled

        git_diff_enabled = self.git_diff_enabled

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if json_array_enabled is not UNSET:
            field_dict["json_array_enabled"] = json_array_enabled
        if log_enabled is not UNSET:
            field_dict["log_enabled"] = log_enabled
        if search_results_enabled is not UNSET:
            field_dict["search_results_enabled"] = search_results_enabled
        if git_diff_enabled is not UNSET:
            field_dict["git_diff_enabled"] = git_diff_enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        json_array_enabled = d.pop("json_array_enabled", UNSET)

        log_enabled = d.pop("log_enabled", UNSET)

        search_results_enabled = d.pop("search_results_enabled", UNSET)

        git_diff_enabled = d.pop("git_diff_enabled", UNSET)

        patch_llm_token_saving_policy = cls(
            json_array_enabled=json_array_enabled,
            log_enabled=log_enabled,
            search_results_enabled=search_results_enabled,
            git_diff_enabled=git_diff_enabled,
        )

        return patch_llm_token_saving_policy
