"""Pre-create idempotency lookup for GitHub issue creation."""

from __future__ import annotations

from agentic_devtools.adapters.github_provider_hierarchy import GitHubProviderCreationHierarchyMixin
from agentic_devtools.adapters.github_provider_idempotency import GitHubProviderIdempotencyMixin
from agentic_devtools.adapters.issue_provider import DefinitiveCreationFailure, PreCreateLookup, ProviderIssueResult


class GitHubProviderCreationLookupMixin(GitHubProviderCreationHierarchyMixin, GitHubProviderIdempotencyMixin):
    def _validate_precreate_lookup(self, precreate_lookup: PreCreateLookup | None, idempotency_key: str | None) -> None:
        if precreate_lookup is not None and (
            not idempotency_key or precreate_lookup.orchestration_key != idempotency_key
        ):
            raise DefinitiveCreationFailure("precreate_lookup must match the idempotency_key.")
        if precreate_lookup is not None and precreate_lookup.legacy_orchestration_key is not None:
            if (
                not isinstance(precreate_lookup.legacy_orchestration_key, str)
                or not precreate_lookup.legacy_orchestration_key.strip()
                or not isinstance(precreate_lookup.node_ref, str)
                or not precreate_lookup.node_ref.strip()
                or not isinstance(precreate_lookup.legacy_adoption_permitted, bool)
            ):
                raise DefinitiveCreationFailure("precreate_lookup legacy candidate is invalid.")

    def _lookup_existing_for_creation(
        self,
        orch_key: str,
        lookup_key: str,
        normalized_parent_id: str | None,
        precreate_lookup: PreCreateLookup | None,
    ) -> ProviderIssueResult | None:
        existing: ProviderIssueResult | None = None
        if precreate_lookup is None and orch_key in self._idempotency_cache:
            cached_issue = self._idempotency_cache[orch_key]
            return self._link_created_issue(cached_issue, normalized_parent_id, newly_created=False)
        if precreate_lookup is not None:
            cached = self._idempotency_cache.get(orch_key)
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
                if legacy_key is not None and legacy_key != orch_key
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
        else:
            existing = self._find_by_orchestration_key(lookup_key)
        if not existing:
            return None
        existing_result = self._link_created_issue(
            ProviderIssueResult(
                identifier=existing.identifier,
                url=existing.url,
                status="existing",
                metadata=existing.metadata,
            ),
            normalized_parent_id,
            newly_created=False,
            error_result=existing,
        )
        self._idempotency_cache[orch_key] = existing_result
        return existing_result
