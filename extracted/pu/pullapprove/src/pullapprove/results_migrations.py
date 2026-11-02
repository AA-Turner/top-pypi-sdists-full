"""
Versioned migrations for PullRequestResults data.

When the schema changes, add a new migration function and append it to ResultsMigrator.migrations.
Old stored data will be migrated on-the-fly when loaded via from_dict().

A migration must also work on a partial result: a list page reads only the
`version` and `scope_results` keys of a stored result and migrates just those
(PullRequestResults.scope_results_from_keys), so reach every other key
with `.get()` and never derive one key from another.
"""

from __future__ import annotations

from typing import Any


def migrate_resview_results_scopes(data: dict[str, Any]) -> dict[str, Any]:
    """
    Migrate v1 -> v2:
    - Rename ReviewResult.scopes -> matched_scopes
    """
    if "review_results" in data:
        for review_result in data["review_results"].values():
            # Rename scopes -> matched_scopes
            if "scopes" in review_result:
                review_result["matched_scopes"] = review_result.pop("scopes")

    return data


def migrate_drop_config_branches(data: dict[str, Any]) -> dict[str, Any]:
    """
    Migrate v2 -> v3:
    - Config-level `branches` was removed. Drop it from stored configs so old
      results re-parse cleanly. Scope-level `branches` is unaffected.
    """
    for config_result in data.get("config_results", {}).values():
        config = config_result.get("config")
        if isinstance(config, dict):
            config.pop("branches", None)

    return data


def migrate_drop_branch_fields(data: dict[str, Any]) -> dict[str, Any]:
    """
    Migrate v3 -> v4:
    - Scope-level `branches` was removed.
    - The PullRequest `base_branch`/`head_branch` fields were removed along with
      the `Branch` domain object.

    Both models forbid extra keys, so any leftover value in an old stored result
    would break re-parsing. `base_branch`/`head_branch` were required (no
    default), so every pre-v4 result carries them. Drop them from the pullrequest
    and `branches` from every stored scope (configs and scope results).
    """
    pullrequest = data.get("pullrequest")
    if isinstance(pullrequest, dict):
        pullrequest.pop("base_branch", None)
        pullrequest.pop("head_branch", None)

    scopes: list[Any] = []
    for config_result in data.get("config_results", {}).values():
        if isinstance(config_result, dict) and isinstance(
            config_result.get("config"), dict
        ):
            scopes.extend(config_result["config"].get("scopes") or [])
    for scope_result in data.get("scope_results", {}).values():
        if isinstance(scope_result, dict):
            scopes.append(scope_result.get("scope"))

    for scope in scopes:
        if isinstance(scope, dict):
            scope.pop("branches", None)

    return data


def migrate_drop_reviewed_for(data: dict[str, Any]) -> dict[str, Any]:
    """
    Migrate v4 -> v5:
    - The scope-level `reviewed_for` setting was removed. ScopeModel forbids
      extra keys, so any stored scope that set `reviewed_for` to a non-default
      value (`required`/`ignored`) would break re-parsing. Drop it from every
      stored scope (configs and scope results).
    """
    scopes: list[Any] = []
    for config_result in data.get("config_results", {}).values():
        if isinstance(config_result, dict) and isinstance(
            config_result.get("config"), dict
        ):
            scopes.extend(config_result["config"].get("scopes") or [])
    for scope_result in data.get("scope_results", {}).values():
        if isinstance(scope_result, dict):
            scopes.append(scope_result.get("scope"))

    for scope in scopes:
        if isinstance(scope, dict):
            scope.pop("reviewed_for", None)

    return data


def migrate_unwrap_review_results(data: dict[str, Any]) -> dict[str, Any]:
    """
    Migrate v5 -> v6:
    - The ReviewResult wrapper was removed; review_results now maps host_id ->
      Review directly. Unwrap each stored {"review": {...}, ...} into the bare
      review dict (which also drops the removed matched_scopes field).
    """
    review_results = data.get("review_results")
    if isinstance(review_results, dict):
        for host_id, review_result in review_results.items():
            if isinstance(review_result, dict) and isinstance(
                review_result.get("review"), dict
            ):
                review_results[host_id] = review_result["review"]

    return data


def migrate_drop_path_code_reviews(data: dict[str, Any]) -> dict[str, Any]:
    """
    Migrate v6 -> v7:
    - PathResult.reviews / CodeResult.reviews were removed (write-only dead
      state). Both models forbid extra keys, so strip `reviews` from every
      stored path result and code result.
    """
    for key in ("path_results", "code_results"):
        for result in data.get(key, {}).values():
            if isinstance(result, dict):
                result.pop("reviews", None)

    return data


def migrate_requested_reviews_to_flag(data: dict[str, Any]) -> dict[str, Any]:
    """
    Migrate v7 -> v8:
    - Review requests used to be represented as synthetic PENDING reviews with
      host_id "requested:<user id>". They are now a `requested` flag on the
      Reviewer instead. Strip the synthetic reviews everywhere they were
      stored (reviewer reviews, review_results, scope review id lists) and
      set `requested` on the reviewers that carried one. The large-scale
      change's review id list had them too; v13 drops that whole block.
    """

    def is_placeholder(host_id: Any) -> bool:
        return isinstance(host_id, str) and host_id.startswith("requested:")

    pullrequest = data.get("pullrequest")
    if isinstance(pullrequest, dict):
        for reviewer in pullrequest.get("reviewers") or []:
            if not isinstance(reviewer, dict):
                continue
            reviews = reviewer.get("reviews")
            if not isinstance(reviews, list):
                continue
            kept = [
                r
                for r in reviews
                if not (isinstance(r, dict) and is_placeholder(r.get("host_id")))
            ]
            if len(kept) != len(reviews):
                reviewer["reviews"] = kept
                reviewer["requested"] = True

    review_results = data.get("review_results")
    if isinstance(review_results, dict):
        for host_id in [k for k in review_results if is_placeholder(k)]:
            del review_results[host_id]

    for scope_result in data.get("scope_results", {}).values():
        if isinstance(scope_result, dict) and isinstance(
            scope_result.get("reviews"), list
        ):
            scope_result["reviews"] = [
                r for r in scope_result["reviews"] if not is_placeholder(r)
            ]

    return data


def migrate_drop_agents(data: dict[str, Any]) -> dict[str, Any]:
    """
    Migrate v8 -> v9:
    - `[[agents]]` was removed (replaced by scope-level `unless`). Results
      stored while a config declared agents carry an `agents` list at the top
      level and an `agents` key inside stored config dumps; the results model
      forbids extra keys and ConfigModel now rejects any `agents` key
      outright, so both must be stripped for old results to re-parse. Open
      pull requests would self-heal on their next processing run, but
      merged/closed ones never reprocess -- without this their stored history
      is unrenderable forever.
    """
    data.pop("agents", None)

    for config_result in data.get("config_results", {}).values():
        if isinstance(config_result, dict) and isinstance(
            config_result.get("config"), dict
        ):
            config_result["config"].pop("agents", None)

    return data


def migrate_agent_result_states(data: dict[str, Any]) -> dict[str, Any]:
    """
    Migrate v9 -> v10:
    - The single "pending" agent state split into "queued", "running" and
      "disputed", and the `in_flight`/`unstarted` booleans that used to carry
      that distinction moved onto the state itself. AgentResult forbids extra
      keys, so the old flags have to go or old results stop re-parsing.

      The flags are also the only record of WHICH of the three a stored
      "pending" was, so they are read before they are dropped: `unstarted`
      marked a review nothing had started, `in_flight` one that was on its
      way, and a dispute carried neither (both defaulted False, and results
      are dumped with exclude_defaults, so a dispute stored no flag at all).

      Merged and closed pull requests never reprocess, so what this writes is
      what their history keeps. Collapsing the three into one would relabel
      every settled dispute as a review still running — the exact sentence
      the split exists to stop showing.
    """
    for agent_result in data.get("agent_results", {}).values():
        if not isinstance(agent_result, dict):
            continue
        unstarted = agent_result.pop("unstarted", False)
        in_flight = agent_result.pop("in_flight", False)
        if agent_result.get("state") != "pending":
            continue
        if unstarted:
            agent_result["state"] = "queued"
        elif in_flight:
            agent_result["state"] = "running"
        else:
            agent_result["state"] = "disputed"

    return data


def migrate_drop_agent_results(data: dict[str, Any]) -> dict[str, Any]:
    """
    Migrate v10 -> v11:
    - The agent gate was removed with the hosted agent reviews. Results stored
      while it existed carry an `agent_results` receipt at the top level, and
      config dumps carry an `agents` list; both models forbid extra keys, so
      both are stripped for old results to re-parse.
    """
    data.pop("agent_results", None)

    for config_result in data.get("config_results", {}).values():
        if isinstance(config_result, dict) and isinstance(
            config_result.get("config"), dict
        ):
            config_result["config"].pop("agents", None)

    return data


def migrate_drop_removal_kind_flags(data: dict[str, Any]) -> dict[str, Any]:
    """
    Migrate v11 -> v12:
    - A withdrawn review request used to be read three ways (self, someone
      else, bot), carried as `removed_by_self` / `removed_by_bot` on each
      reviewer. There is one rule now and the flags are gone. Reviewer forbids
      extra keys, so results stored in the window that wrote them must have
      them stripped or they stop re-parsing. `removed` itself stays.
    """
    pullrequest = data.get("pullrequest")
    if isinstance(pullrequest, dict):
        for reviewer in pullrequest.get("reviewers") or []:
            if isinstance(reviewer, dict):
                reviewer.pop("removed_by_self", None)
                reviewer.pop("removed_by_bot", None)

    return data


def migrate_drop_large_scale_change_results(data: dict[str, Any]) -> dict[str, Any]:
    """
    Migrate v12 -> v13:
    - A large-scale change is now reviewed as a scope in `scope_results`,
      instead of in its own `large_scale_change_results` block. The results
      model forbids extra keys, so the block is stripped. A migration can't
      turn it into a scope (see the module docstring), so an old large-scale
      change reads as having no scopes until it is processed again.
    """
    data.pop("large_scale_change_results", None)

    return data


def migrate_person_requested_to_requested_by(data: dict[str, Any]) -> dict[str, Any]:
    """
    Migrate v13 -> v14:
    - A scope's people recorded a request as `requested: true`. They now
      record who sent it, in `requested_by` ("pullapprove" or "host"), and
      `requested` is derived from that. Results stored before this can't say
      who asked, so every standing request reads as a person's: "host".
    """
    for scope_result in data.get("scope_results", {}).values():
        if not isinstance(scope_result, dict):
            continue
        for person in scope_result.get("people") or []:
            if isinstance(person, dict) and person.pop("requested", False):
                person["requested_by"] = "host"

    return data


class ResultsMigrator:
    """
    Handles versioned migrations for PullRequestResults data.
    """

    # Ordered list of migration functions.
    # Index 0 = v1->v2, index 1 = v2->v3, etc.
    migrations = (
        migrate_resview_results_scopes,
        migrate_drop_config_branches,
        migrate_drop_branch_fields,
        migrate_drop_reviewed_for,
        migrate_unwrap_review_results,
        migrate_drop_path_code_reviews,
        migrate_requested_reviews_to_flag,
        migrate_drop_agents,
        migrate_agent_result_states,
        migrate_drop_agent_results,
        migrate_drop_removal_kind_flags,
        migrate_drop_large_scale_change_results,
        migrate_person_requested_to_requested_by,
    )

    @classmethod
    def current_version(cls) -> int:
        """Current version is always 1 more than the number of migrations."""
        return len(cls.migrations) + 1

    @classmethod
    def migrate(cls, data: dict[str, Any]) -> dict[str, Any]:
        """
        Apply all necessary migrations to bring data to current version.

        Data without a version field is assumed to be v1.
        """
        version = data.get("version", 1)

        # Apply migrations from current version to latest
        for migration in cls.migrations[version - 1 :]:
            data = migration(data)

        data["version"] = cls.current_version()
        return data
