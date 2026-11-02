from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="LlmTokenSavingPolicy")


@_attrs_define
class LlmTokenSavingPolicy:
    """Canonical per-runtime LLM tool-output compression settings.

    Attributes:
        json_array_enabled (bool):
        log_enabled (bool):
        search_results_enabled (bool):
        git_diff_enabled (bool):
    """

    json_array_enabled: bool
    log_enabled: bool
    search_results_enabled: bool
    git_diff_enabled: bool

    def to_dict(self) -> dict[str, Any]:
        json_array_enabled = self.json_array_enabled

        log_enabled = self.log_enabled

        search_results_enabled = self.search_results_enabled

        git_diff_enabled = self.git_diff_enabled

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "json_array_enabled": json_array_enabled,
                "log_enabled": log_enabled,
                "search_results_enabled": search_results_enabled,
                "git_diff_enabled": git_diff_enabled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        json_array_enabled = d.pop("json_array_enabled")

        log_enabled = d.pop("log_enabled")

        search_results_enabled = d.pop("search_results_enabled")

        git_diff_enabled = d.pop("git_diff_enabled")

        llm_token_saving_policy = cls(
            json_array_enabled=json_array_enabled,
            log_enabled=log_enabled,
            search_results_enabled=search_results_enabled,
            git_diff_enabled=git_diff_enabled,
        )

        return llm_token_saving_policy
