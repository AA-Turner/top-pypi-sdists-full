from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ForgeCapabilities")



@_attrs_define
class ForgeCapabilities:
    """ What one forge can do, as facts a client reads instead of testing the forge's name. A forge this service learns to
    talk to is one more set of values here, so a client that reads these needs no change for it.

        Attributes:
            auto_merge_held_by_app (bool): True when this app holds an armed auto-merge and merges the pull request itself
                once its checks pass. False when the forge holds it and merges on its own.
            checks_via_webhook (bool): True when the forge reports check results by webhook, so a pending run is polled only
                when no event arrived. False when results are found by polling.
            serves_running_log (bool): True when a job's log can be read while the job runs.
            server_log_excerpts (bool): True when a failed job's excerpt is read from the log endpoint (`excerpt=true`).
                False when the check list already carries it.
            approval_gated_runs (bool): True when a run can be held until a person approves it.
            dependabot_commands (bool): True when a `@dependabot` comment does anything on this forge.
            advisory_source (str): Where the repository advisories come from. Open-ended, so a new source is not a breaking
                change; today `dependabot` and `osv`.
            advisory_unknown_needs_reason (bool): True when an `unknown` advisory answer is worth showing only if the row
                names a reason. Without one it usually means a repository with nothing to check. False when every `unknown`
                answer is a failure to read.
            status_page_url (str): The forge's public status page, or an empty string when it has none.
            rate_limit_model (str): How the forge budgets requests. Open-ended; today `graphql_and_rest` (two separate
                allowances) and `rest`.
            issue_ref_syntax (str): The forms the forge's text uses to reference an issue. Open-ended; today
                `hash_or_gh_prefix` (a hash sign or a `GH-` prefix before the number) and `hash` (the hash sign only).
            label (str): The forge's name as a person reads it, such as `GitHub`.
     """

    auto_merge_held_by_app: bool
    checks_via_webhook: bool
    serves_running_log: bool
    server_log_excerpts: bool
    approval_gated_runs: bool
    dependabot_commands: bool
    advisory_source: str
    advisory_unknown_needs_reason: bool
    status_page_url: str
    rate_limit_model: str
    issue_ref_syntax: str
    label: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        auto_merge_held_by_app = self.auto_merge_held_by_app

        checks_via_webhook = self.checks_via_webhook

        serves_running_log = self.serves_running_log

        server_log_excerpts = self.server_log_excerpts

        approval_gated_runs = self.approval_gated_runs

        dependabot_commands = self.dependabot_commands

        advisory_source = self.advisory_source

        advisory_unknown_needs_reason = self.advisory_unknown_needs_reason

        status_page_url = self.status_page_url

        rate_limit_model = self.rate_limit_model

        issue_ref_syntax = self.issue_ref_syntax

        label = self.label


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "autoMergeHeldByApp": auto_merge_held_by_app,
            "checksViaWebhook": checks_via_webhook,
            "servesRunningLog": serves_running_log,
            "serverLogExcerpts": server_log_excerpts,
            "approvalGatedRuns": approval_gated_runs,
            "dependabotCommands": dependabot_commands,
            "advisorySource": advisory_source,
            "advisoryUnknownNeedsReason": advisory_unknown_needs_reason,
            "statusPageUrl": status_page_url,
            "rateLimitModel": rate_limit_model,
            "issueRefSyntax": issue_ref_syntax,
            "label": label,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        auto_merge_held_by_app = d.pop("autoMergeHeldByApp")

        checks_via_webhook = d.pop("checksViaWebhook")

        serves_running_log = d.pop("servesRunningLog")

        server_log_excerpts = d.pop("serverLogExcerpts")

        approval_gated_runs = d.pop("approvalGatedRuns")

        dependabot_commands = d.pop("dependabotCommands")

        advisory_source = d.pop("advisorySource")

        advisory_unknown_needs_reason = d.pop("advisoryUnknownNeedsReason")

        status_page_url = d.pop("statusPageUrl")

        rate_limit_model = d.pop("rateLimitModel")

        issue_ref_syntax = d.pop("issueRefSyntax")

        label = d.pop("label")

        forge_capabilities = cls(
            auto_merge_held_by_app=auto_merge_held_by_app,
            checks_via_webhook=checks_via_webhook,
            serves_running_log=serves_running_log,
            server_log_excerpts=server_log_excerpts,
            approval_gated_runs=approval_gated_runs,
            dependabot_commands=dependabot_commands,
            advisory_source=advisory_source,
            advisory_unknown_needs_reason=advisory_unknown_needs_reason,
            status_page_url=status_page_url,
            rate_limit_model=rate_limit_model,
            issue_ref_syntax=issue_ref_syntax,
            label=label,
        )


        forge_capabilities.additional_properties = d
        return forge_capabilities

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
