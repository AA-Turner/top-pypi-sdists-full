"""Apollo-backed RBAC: which cubes (environments) can a profile's creds see.

Apollo is the source of truth for cube visibility — every cube is an Apollo
environment, with or without Teleport/Groundcover enrollment. The profile's
Apollo OAuth2 credentials (selected by the API-key middleware from the Cognito
group) determine team membership; team membership determines environment access.

This module is shared by the environment tools and the Groundcover tools so the
RBAC logic lives in exactly one place.
"""

from __future__ import annotations

import logging

from cube_common.apollo_client import ApolloClient
from cube_common.apollo_pagination import fetch_all_environments
from cube_common import apollo_queries as Q

logger = logging.getLogger(__name__)


async def get_user_team_names(client: ApolloClient) -> set[str]:
    """Return the set of Apollo team names the current credentials belong to."""
    data = await client.graphql(Q.MY_TEAMS)
    teams = data.get("me", {}).get("apolloTeams", [])
    return {t["name"] for t in teams}


def has_environment_access(env: dict, user_teams: set[str]) -> bool:
    """True if any of the user's teams has a role on this environment."""
    role_policy = env.get("rolePolicy") or {}
    for stmt in role_policy.get("teamRoleStatements", []) or []:
        team_name = (stmt.get("team") or {}).get("name") or ""
        # `team_name and ...` is the fail-CLOSED guard. Without it a malformed
        # Apollo payload fails OPEN: a statement of `{"team": {}}` yields "" and
        # matches a caller whose team set contains "" (which `get_user_team_names`
        # would build from an `apolloTeams` entry with an empty/null name). The
        # console caches the team set for its TTL, so a transient blip would
        # persist rather than affect one request — cheap to make impossible.
        if team_name and team_name in user_teams:
            return True
    return False


def cluster_name(env_name: str) -> str:
    """Map an Apollo environment name to its Groundcover/Teleport cluster name.

    Verified against the live ri.apollo.main backend: cube environment names are
    ALREADY the cluster name (e.g. ``cube-o2e87m9a``); the deploy suffix only
    appears in ``namespaceId``, never the env name. So this is the identity
    function. Kept as a one-line seam in case a future backend reintroduces a
    suffix — change it here and both the authz set and label injection follow.
    """
    return env_name


async def allowed_cubes(client: ApolloClient) -> set[str]:
    """Return the set of cluster names the current credentials may read.

    This is the authorization boundary for Groundcover: only cubes whose Apollo
    environment the caller's team has a role on. Admin service accounts (in
    ``Edgescale-AI-admins``) have a role on every environment, so they get the
    full set; a tenant gets only their cube(s).

    **The read is drained across every page, and that used to be the most
    consequential instance of issue 252.** A single-page read here is not a display
    problem, it is a silent authorization NARROWING: the cube is dropped from the
    set, and its owner is then told *"Access denied: cube 'x' is not in your
    authorized set"* for a cube they own. Fail-closed, so never a security hole —
    but indistinguishable from a real permission problem, which is what made it
    expensive to diagnose.

    **A truncated drain is logged, not raised.** This function is on the hot path
    for every Groundcover tool call and three console read paths; raising would
    convert "some caller is past the page cap" into "Groundcover is down for
    everyone". The drain's own guards make truncation a `MAX_PAGES`-or-stalled-token
    condition rather than an ordinary one, so the log is the alarm.
    """
    teams = await get_user_team_names(client)
    result = await fetch_all_environments(client, Q.LIST_ENVIRONMENTS)
    if result.truncated:
        logger.error(
            "allowed_cubes: the environment drain did not complete (%d environments "
            "read) — the AUTHORIZATION set is incomplete and cubes the caller owns "
            "may read as access-denied. See issue 252 / OI-6.",
            len(result.items),
        )
    return {
        cluster_name(e["name"])
        for e in result.items
        if has_environment_access(e, teams)
    }
