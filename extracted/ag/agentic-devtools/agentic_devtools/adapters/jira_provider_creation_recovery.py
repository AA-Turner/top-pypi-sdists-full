"""Jira issue-creation lookup and recovery helpers."""

from __future__ import annotations

import copy

import requests as requests_lib

from agentic_devtools.adapters.exceptions import HierarchyLinkError
from agentic_devtools.adapters.issue_provider import (
    DefinitiveCreationFailure,
    PreCreateLookup,
    ProviderIssueResult,
)
from agentic_devtools.adapters.jira_provider_config import _JiraProviderMixinProtocol
from agentic_devtools.adapters.retry import TransientError, retry_on_transient


class _JiraProviderCreationRecoveryMixin(_JiraProviderMixinProtocol):
    """Lookup and recovery behavior used by issue creation."""

    def _validate_precreate_lookup(
        self,
        idempotency_key: str | None,
        precreate_lookup: PreCreateLookup | None,
    ) -> None:
        if precreate_lookup is None:
            return
        if not idempotency_key or precreate_lookup.orchestration_key != idempotency_key:
            raise DefinitiveCreationFailure("precreate_lookup must match the idempotency_key.")
        if precreate_lookup.legacy_orchestration_key is None:
            return
        if (
            not isinstance(precreate_lookup.legacy_orchestration_key, str)
            or not precreate_lookup.legacy_orchestration_key.strip()
            or not isinstance(precreate_lookup.node_ref, str)
            or not precreate_lookup.node_ref.strip()
            or not isinstance(precreate_lookup.legacy_adoption_permitted, bool)
        ):
            raise DefinitiveCreationFailure("precreate_lookup legacy candidate is invalid.")

    def _resolve_precreate_lookup(
        self,
        precreate_lookup: PreCreateLookup,
        idempotency_key: str,
        orchestration_key: str,
    ) -> ProviderIssueResult | None:
        cached = self._idempotency_keys.get(idempotency_key)
        existing = precreate_lookup.issue or cached
        if precreate_lookup.issue is not None and cached is not None:
            if self.normalize_identifier(precreate_lookup.issue.identifier) != self.normalize_identifier(
                cached.identifier
            ):
                raise DefinitiveCreationFailure(
                    f"Ambiguous tree-scoped lookup results for node {precreate_lookup.node_ref!r}."
                )

        legacy_key = precreate_lookup.legacy_orchestration_key
        legacy_match = (
            self._find_by_orchestration_key(legacy_key)
            if legacy_key is not None and legacy_key != orchestration_key
            else None
        )
        if existing is not None and legacy_match is not None:
            if self.normalize_identifier(existing.identifier) != self.normalize_identifier(legacy_match.identifier):
                raise DefinitiveCreationFailure(
                    f"Ambiguous tree-scoped and legacy orchestration-key matches for node "
                    f"{precreate_lookup.node_ref!r} identify different issues."
                )
        elif existing is None and legacy_match is not None:
            if not precreate_lookup.legacy_adoption_permitted:
                raise DefinitiveCreationFailure(
                    f"Unverified legacy orchestration-key match for node "
                    f"{precreate_lookup.node_ref!r}; import a verified legacy mapping before adoption."
                )
            existing = legacy_match
        return existing

    def _link_existing_issue(
        self,
        existing: ProviderIssueResult,
        parent_id: str | None,
    ) -> ProviderIssueResult:
        try:
            hierarchy_link_result = (
                self.link_subissue(parent_id, existing.identifier, dry_run=False) if parent_id is not None else None
            )
        except Exception as link_exc:
            raise HierarchyLinkError(
                f"Issue {existing.identifier} already exists at {existing.url} but linking to "
                f"parent {parent_id} failed (see chained exception for details)",
                created_result=existing,
                stage="link_subissue",
                cause=link_exc,
            ) from link_exc
        return ProviderIssueResult(
            identifier=existing.identifier,
            url=existing.url,
            status="existing",
            metadata=copy.deepcopy(existing.metadata),
            hierarchy_link_result=hierarchy_link_result,
        )

    def _find_existing_issue(
        self,
        idempotency_key: str | None,
        precreate_lookup: PreCreateLookup | None,
        orchestration_key: str | None,
        lookup_key: str,
        parent_id: str | None,
    ) -> ProviderIssueResult | None:
        if precreate_lookup is None and idempotency_key is not None and idempotency_key in self._idempotency_keys:
            return self._link_existing_issue(self._idempotency_keys[idempotency_key], parent_id)
        if not orchestration_key:
            return None
        if precreate_lookup is not None:
            assert idempotency_key is not None
            existing = self._resolve_precreate_lookup(precreate_lookup, idempotency_key, orchestration_key)
        else:
            existing = self._find_by_orchestration_key(lookup_key)
        if existing is None:
            return None
        result = self._link_existing_issue(existing, parent_id)
        if idempotency_key is not None:
            self._idempotency_keys[idempotency_key] = result
        return result

    def _request_issue_creation(
        self,
        lookup_key: str,
        url: str,
        fields: dict[str, object],
    ) -> tuple[requests_lib.Response | None, ProviderIssueResult | None]:
        recovered: ProviderIssueResult | None = None
        recovery_attempted = False

        def create_issue_request() -> requests_lib.Response | None:
            nonlocal recovered, recovery_attempted
            if recovery_attempted and lookup_key:
                recovered = self._find_after_transient(lookup_key)
                if recovered is not None:
                    return None
                raise RuntimeError(
                    "Issue creation outcome is uncertain after a transient response; the mapping entry remains pending."
                )
            try:
                return self._request("POST", url, json={"fields": fields})
            except TransientError:
                if lookup_key:
                    recovery_attempted = True
                    recovered = self._find_after_transient(lookup_key)
                    if recovered is not None:
                        return None
                raise

        try:
            response = retry_on_transient(create_issue_request)() if lookup_key else create_issue_request()
        except TransientError as exc:
            if not lookup_key:
                raise
            raise RuntimeError(
                "Issue creation outcome is uncertain after a transient response; the mapping entry remains pending."
            ) from exc
        return response, recovered

    def _find_after_transient(self, lookup_key: str) -> ProviderIssueResult | None:
        try:
            return self._find_by_orchestration_key(lookup_key)
        except TransientError:
            raise
        except Exception as lookup_exc:
            raise RuntimeError(
                "Issue creation outcome is uncertain after a transient response; the mapping entry remains pending."
            ) from lookup_exc
