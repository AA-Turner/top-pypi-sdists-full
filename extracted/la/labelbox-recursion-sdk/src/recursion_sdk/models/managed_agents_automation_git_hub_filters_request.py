from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_automation_git_hub_filters_request_comment_on import ManagedAgentsAutomationGitHubFiltersRequestCommentOn
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsAutomationGitHubFiltersRequest")



@_attrs_define
class ManagedAgentsAutomationGitHubFiltersRequest:
    """ Optional conditions on the verified GitHub delivery body. Every present condition must match; empty lists accept any
    value.

        Example:
            {'actions': ['example'], 'addedLabels': ['example'], 'baseBranches': ['example'], 'branches': ['example'],
                'commentOn': 'pull_request', 'conclusions': ['example'], 'excludeDrafts': True, 'ignoreBots': True, 'labelsAny':
                ['example'], 'labelsNone': ['example'], 'merged': True, 'repositories': ['example'], 'reviewStates':
                ['example'], 'senders': ['example'], 'textContains': ['example'], 'textExcludes': ['example'], 'textMatches':
                'example'}

        Attributes:
            actions (list[str] | Unset): GitHub delivery action values that may match, such as opened, labeled, submitted,
                or completed. Empty accepts every action.
            added_labels (list[str] | Unset): For labeled deliveries: the added label must be one of these.
            base_branches (list[str] | Unset): Pull request base branch globs. An asterisk matches any characters, including
                slashes; a question mark matches one character.
            branches (list[str] | Unset): Branch globs for push and workflow run deliveries, with the same syntax as
                baseBranches.
            comment_on (ManagedAgentsAutomationGitHubFiltersRequestCommentOn | Unset): For issue_comment deliveries: whether
                the comment is on a pull request or on an issue.
            conclusions (list[str] | Unset): For completed workflow runs: conclusions such as failure, success, or
                cancelled. Empty accepts any conclusion.
            exclude_drafts (bool | Unset): Reject draft pull requests.
            ignore_bots (bool | Unset): Reject deliveries whose sender is a GitHub bot account.
            labels_any (list[str] | Unset): Match only when the pull request or issue carries at least one of these labels.
            labels_none (list[str] | Unset): Reject when the pull request or issue carries any of these labels.
            merged (bool | Unset): For closed pull requests: true matches merged, false matches closed without merging.
            repositories (list[str] | Unset): Repository full names (owner/name), compared case-insensitively. Empty accepts
                every repository.
            review_states (list[str] | Unset): For submitted reviews: approved, changes_requested, or commented. Empty
                accepts any review.
            senders (list[str] | Unset): GitHub logins of the account that caused the delivery. Empty accepts anyone.
            text_contains (list[str] | Unset): For comment deliveries: the comment must contain at least one of these
                phrases, ignoring case.
            text_excludes (list[str] | Unset): For comment deliveries: the comment must contain none of these phrases,
                ignoring case.
            text_matches (str | Unset): For comment deliveries: an RE2 regular expression the comment must match, ignoring
                case.
     """

    actions: list[str] | Unset = UNSET
    added_labels: list[str] | Unset = UNSET
    base_branches: list[str] | Unset = UNSET
    branches: list[str] | Unset = UNSET
    comment_on: ManagedAgentsAutomationGitHubFiltersRequestCommentOn | Unset = UNSET
    conclusions: list[str] | Unset = UNSET
    exclude_drafts: bool | Unset = UNSET
    ignore_bots: bool | Unset = UNSET
    labels_any: list[str] | Unset = UNSET
    labels_none: list[str] | Unset = UNSET
    merged: bool | Unset = UNSET
    repositories: list[str] | Unset = UNSET
    review_states: list[str] | Unset = UNSET
    senders: list[str] | Unset = UNSET
    text_contains: list[str] | Unset = UNSET
    text_excludes: list[str] | Unset = UNSET
    text_matches: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        actions: list[str] | Unset = UNSET
        if not isinstance(self.actions, Unset):
            actions = self.actions



        added_labels: list[str] | Unset = UNSET
        if not isinstance(self.added_labels, Unset):
            added_labels = self.added_labels



        base_branches: list[str] | Unset = UNSET
        if not isinstance(self.base_branches, Unset):
            base_branches = self.base_branches



        branches: list[str] | Unset = UNSET
        if not isinstance(self.branches, Unset):
            branches = self.branches



        comment_on: str | Unset = UNSET
        if not isinstance(self.comment_on, Unset):
            comment_on = self.comment_on.value


        conclusions: list[str] | Unset = UNSET
        if not isinstance(self.conclusions, Unset):
            conclusions = self.conclusions



        exclude_drafts = self.exclude_drafts

        ignore_bots = self.ignore_bots

        labels_any: list[str] | Unset = UNSET
        if not isinstance(self.labels_any, Unset):
            labels_any = self.labels_any



        labels_none: list[str] | Unset = UNSET
        if not isinstance(self.labels_none, Unset):
            labels_none = self.labels_none



        merged = self.merged

        repositories: list[str] | Unset = UNSET
        if not isinstance(self.repositories, Unset):
            repositories = self.repositories



        review_states: list[str] | Unset = UNSET
        if not isinstance(self.review_states, Unset):
            review_states = self.review_states



        senders: list[str] | Unset = UNSET
        if not isinstance(self.senders, Unset):
            senders = self.senders



        text_contains: list[str] | Unset = UNSET
        if not isinstance(self.text_contains, Unset):
            text_contains = self.text_contains



        text_excludes: list[str] | Unset = UNSET
        if not isinstance(self.text_excludes, Unset):
            text_excludes = self.text_excludes



        text_matches = self.text_matches


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if actions is not UNSET:
            field_dict["actions"] = actions
        if added_labels is not UNSET:
            field_dict["addedLabels"] = added_labels
        if base_branches is not UNSET:
            field_dict["baseBranches"] = base_branches
        if branches is not UNSET:
            field_dict["branches"] = branches
        if comment_on is not UNSET:
            field_dict["commentOn"] = comment_on
        if conclusions is not UNSET:
            field_dict["conclusions"] = conclusions
        if exclude_drafts is not UNSET:
            field_dict["excludeDrafts"] = exclude_drafts
        if ignore_bots is not UNSET:
            field_dict["ignoreBots"] = ignore_bots
        if labels_any is not UNSET:
            field_dict["labelsAny"] = labels_any
        if labels_none is not UNSET:
            field_dict["labelsNone"] = labels_none
        if merged is not UNSET:
            field_dict["merged"] = merged
        if repositories is not UNSET:
            field_dict["repositories"] = repositories
        if review_states is not UNSET:
            field_dict["reviewStates"] = review_states
        if senders is not UNSET:
            field_dict["senders"] = senders
        if text_contains is not UNSET:
            field_dict["textContains"] = text_contains
        if text_excludes is not UNSET:
            field_dict["textExcludes"] = text_excludes
        if text_matches is not UNSET:
            field_dict["textMatches"] = text_matches

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        actions = cast(list[str], d.pop("actions", UNSET))


        added_labels = cast(list[str], d.pop("addedLabels", UNSET))


        base_branches = cast(list[str], d.pop("baseBranches", UNSET))


        branches = cast(list[str], d.pop("branches", UNSET))


        _comment_on = d.pop("commentOn", UNSET)
        comment_on: ManagedAgentsAutomationGitHubFiltersRequestCommentOn | Unset
        if isinstance(_comment_on,  Unset):
            comment_on = UNSET
        else:
            comment_on = ManagedAgentsAutomationGitHubFiltersRequestCommentOn(_comment_on)




        conclusions = cast(list[str], d.pop("conclusions", UNSET))


        exclude_drafts = d.pop("excludeDrafts", UNSET)

        ignore_bots = d.pop("ignoreBots", UNSET)

        labels_any = cast(list[str], d.pop("labelsAny", UNSET))


        labels_none = cast(list[str], d.pop("labelsNone", UNSET))


        merged = d.pop("merged", UNSET)

        repositories = cast(list[str], d.pop("repositories", UNSET))


        review_states = cast(list[str], d.pop("reviewStates", UNSET))


        senders = cast(list[str], d.pop("senders", UNSET))


        text_contains = cast(list[str], d.pop("textContains", UNSET))


        text_excludes = cast(list[str], d.pop("textExcludes", UNSET))


        text_matches = d.pop("textMatches", UNSET)

        managed_agents_automation_git_hub_filters_request = cls(
            actions=actions,
            added_labels=added_labels,
            base_branches=base_branches,
            branches=branches,
            comment_on=comment_on,
            conclusions=conclusions,
            exclude_drafts=exclude_drafts,
            ignore_bots=ignore_bots,
            labels_any=labels_any,
            labels_none=labels_none,
            merged=merged,
            repositories=repositories,
            review_states=review_states,
            senders=senders,
            text_contains=text_contains,
            text_excludes=text_excludes,
            text_matches=text_matches,
        )

        return managed_agents_automation_git_hub_filters_request

