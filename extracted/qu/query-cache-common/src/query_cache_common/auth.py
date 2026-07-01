from __future__ import annotations

import typing as t
from functools import cached_property


RUNCACHE_ORG_SCOPE_PREFIX = "runcache:scope:org"
LEGACY_ORG_SCOPE_PREFIX = "conway:scope:org"
ORG_SCOPE_PREFIXES = (RUNCACHE_ORG_SCOPE_PREFIX, LEGACY_ORG_SCOPE_PREFIX)
RUNCACHE_APP_SCOPE_PREFIX = "runcache:scope:app"


def _extract_org_id_and_level(scope: str) -> t.Optional[t.Tuple[str, str]]:
    # scope looks something like 'runcache:scope:app:tues_test:developer'
    # that is, SCOPE_PREFIX:{org_id}:{level}
    scope_parts = scope.split(":")
    org_id = scope_parts[3]
    return (org_id, scope_parts[4]) if org_id else None


def _org_id_to_level(scopes: t.List[str]) -> t.Dict[str, str]:
    mapping = filter(None, [_extract_org_id_and_level(scope) for scope in scopes])
    return {org_id: level for org_id, level in mapping}


class Scope:
    def __init__(self, org_scopes: t.List[str], app_scopes: t.List[str]) -> None:
        self._org_scopes = org_scopes
        self._app_scopes = app_scopes

        for scope in org_scopes + app_scopes:
            if scope.count(":") < 4:
                raise ValueError(f"Invalid scope format: '{scope}'.")

    @classmethod
    def from_string(cls, scope: str) -> Scope:
        """Create a Scope instance from a scope string.

        Supports both the current ``runcache:`` prefix and the legacy ``conway:`` prefix.

        Args:
            scope: The scope string to parse.

        Returns:
            A Scope instance.
        """
        scopes = [s.strip() for s in scope.split(" ")]

        org_scopes = [s for s in scopes if any(s.startswith(p) for p in ORG_SCOPE_PREFIXES)]
        app_scopes = [s for s in scopes if s.startswith(RUNCACHE_APP_SCOPE_PREFIX)]

        return cls(org_scopes=org_scopes, app_scopes=app_scopes)

    @property
    def org_id(self) -> str:
        """Extract the organization ID from a given scope string.

        This method raises ValueError if the scope is not associated with exactly one organization ID.

        Returns:
            The extracted organization ID.
        """
        org_ids = self.org_ids
        if not org_ids:
            raise ValueError("No organization scope found.")
        if len(org_ids) > 1:
            raise ValueError(f"Only one organization scope is supported, got multiple: {org_ids}.")
        org_id = org_ids[0]
        if org_id == "*":
            raise ValueError(f"Wildcard organization ID is not allowed.")
        return org_id

    @cached_property
    def org_ids(self) -> t.List[str]:
        """Returns all organization IDs from the scope, including wildcards."""
        return list(_org_id_to_level(self._org_scopes))

    @cached_property
    def disabled_org_ids(self) -> t.List[str]:
        """Returns organization IDs present in :app: scopes but absent from :org: scopes.

        These are organizations the user is associated with but whose access has been disabled.
        """
        active_org_ids = set(self.org_ids)
        app_org_ids = _org_id_to_level(self._app_scopes)
        return [org_id for org_id in app_org_ids if org_id not in active_org_ids]

    def is_org_id_in_scope(self, org_id: str) -> bool:
        """Check if the given organization ID is included in the scope.

        Args:
            org_id: The organization ID to check.

        Returns:
            True if the org_id is in the scope or if a wildcard "*" is present; False otherwise.
        """
        return org_id in self.org_ids or "*" in self.org_ids

    def is_org_id_disabled(self, org_id: str) -> bool:
        """Check if the user's access has been disabled for the given organization.

        Args:
            org_id: The organization ID to check.

        Returns:
            True if the user's access to the organization has been disabled,
            False if the user is either not a member of the organization or is still an active member
        """

        # if we have an :app: scope containing the org id, but not an :org: scope, the organization has been disabled for the user
        org_ids_in_app_scopes = _org_id_to_level(self._app_scopes)

        if self.is_org_id_in_scope(org_id):
            return False

        return org_id in org_ids_in_app_scopes
