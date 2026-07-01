"""
cvc.sdk.router — Hierarchical routing engine for hive mind (Phase 6).

Formalises the AstroSwarm routing model as a first-class CVC feature:

* **YAML routing config** (``.cvc/routing.yaml``) — declarative role-based
  access rules with glob-pattern branch matching.
* **Role-based ACL** — each role defines readable/writable branch patterns.
* **Context isolation** — agents see only commits from branches they can
  read, preventing context collapse across the hierarchy.
* **Automatic message routing** — ``route()`` determines which branches
  a commit should land on based on the agent's role/squad.
"""

from __future__ import annotations

import fnmatch
import logging
from pathlib import Path
from typing import Any

from cvc.core.database import IndexDB
from cvc.core.models import BranchPointer, CognitiveCommit
from cvc.sdk.registry import AgentRegistry

logger = logging.getLogger("cvc.sdk.router")

# Default branch naming conventions
GLOBAL_BRANCH = "main"
SQUAD_PREFIX = "squad/"
AGENT_PREFIX = "agent/"

# ---------------------------------------------------------------------------
# Routing configuration
# ---------------------------------------------------------------------------

# Default routing rules (used when no .cvc/routing.yaml exists)
_DEFAULT_ROUTING_RULES: dict[str, Any] = {
    "version": 1,
    "roles": {
        "specialist": {
            "readable": ["squad/{squad}"],
            "writable": ["squad/{squad}"],
            "context_priority": ["squad/{squad}"],
        },
        "captain": {
            "readable": ["squad/{squad}", "main"],
            "writable": ["squad/{squad}"],
            "context_priority": ["squad/{squad}", "main"],
        },
        "mission_controller": {
            "readable": ["main", "squad/*"],
            "writable": ["main"],
            "context_priority": ["main"],
        },
        "zeus": {
            "readable": ["main", "squad/*"],
            "writable": ["main"],
            "context_priority": ["main"],
        },
    },
    "defaults": {
        "unregistered": {
            "readable": ["main"],
            "writable": ["main"],
        },
        "unknown_role": {
            "readable": ["**"],
            "writable": ["**"],
        },
    },
}


class RoutingConfig:
    """
    Parsed routing configuration, loaded from YAML or defaults.

    The config maps roles to branch-pattern rules:

    .. code-block:: yaml

        version: 1
        roles:
          specialist:
            readable: ["squad/{squad}"]
            writable: ["squad/{squad}"]
            context_priority: ["squad/{squad}"]
          captain:
            readable: ["squad/{squad}", "main"]
            writable: ["squad/{squad}"]
            context_priority: ["squad/{squad}", "main"]
          zeus:
            readable: ["main", "squad/*"]
            writable: ["main"]
            context_priority: ["main"]
        defaults:
          unregistered:
            readable: ["main"]
            writable: ["main"]
          unknown_role:
            readable: ["**"]
            writable: ["**"]

    Patterns:
    - Literal: ``"main"`` matches only ``"main"``
    - Glob: ``"squad/*"`` matches ``"squad/aegis"``, ``"squad/cvc"``, etc.
    - Double-star: ``"**"`` matches everything (unrestricted)
    - Template: ``"{squad}"`` is expanded per-agent from the agent's profile
    """

    def __init__(self, raw: dict[str, Any] | None = None) -> None:
        self._raw = raw or _DEFAULT_ROUTING_RULES
        self.version: int = self._raw.get("version", 1)
        self.roles: dict[str, dict[str, Any]] = self._raw.get("roles", {})
        self.defaults: dict[str, dict[str, Any]] = self._raw.get("defaults", {})

    @classmethod
    def load(cls, cvc_root: Path) -> RoutingConfig:
        """Load routing config from ``.cvc/routing.yaml``, falling back to defaults."""
        yaml_path = cvc_root / "routing.yaml"
        if yaml_path.exists():
            try:
                import yaml  # type: ignore[import-untyped]
                raw = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
                if isinstance(raw, dict):
                    logger.info("Loaded routing config from %s", yaml_path)
                    return cls(raw)
            except ImportError:
                logger.warning("PyYAML not installed — using default routing rules")
            except Exception as exc:
                logger.warning("Failed to parse routing.yaml: %s — using defaults", exc)
        return cls()

    def save(self, cvc_root: Path) -> None:
        """Write the current routing config to ``.cvc/routing.yaml``."""
        yaml_path = cvc_root / "routing.yaml"
        try:
            import yaml  # type: ignore[import-untyped]
            yaml_path.write_text(
                yaml.dump(self._raw, default_flow_style=False, sort_keys=False),
                encoding="utf-8",
            )
        except ImportError:
            import json
            yaml_path.write_text(
                json.dumps(self._raw, indent=2),
                encoding="utf-8",
            )

    def rules_for_role(self, role: str) -> dict[str, Any]:
        """Return routing rules for a given role."""
        return self.roles.get(role, self.defaults.get("unknown_role", {}))

    def rules_for_unregistered(self) -> dict[str, Any]:
        """Return rules for agents not in the registry."""
        return self.defaults.get("unregistered", {"readable": ["main"], "writable": ["main"]})


# ---------------------------------------------------------------------------
# Branch pattern matching
# ---------------------------------------------------------------------------

def _expand_pattern(pattern: str, profile: dict[str, Any] | None) -> str:
    """Expand ``{squad}`` and ``{agent_id}`` placeholders in a branch pattern."""
    if profile is None:
        return pattern
    return pattern.format_map({
        "squad": profile.get("squad", "*"),
        "agent_id": profile.get("agent_id", "*"),
        "rank": profile.get("rank", "*"),
    })


def _branch_matches(branch: str, pattern: str) -> bool:
    """Check if a branch name matches a (possibly glob) pattern."""
    if pattern == "**":
        return True
    return fnmatch.fnmatch(branch, pattern)


def resolve_branch_patterns(
    patterns: list[str],
    profile: dict[str, Any] | None,
    all_branches: list[str] | None = None,
) -> list[str]:
    """Expand patterns and resolve globs against actual branches.

    Returns concrete branch names when *all_branches* is given,
    otherwise returns the expanded (but possibly still globbed) patterns.
    """
    expanded = [_expand_pattern(p, profile) for p in patterns]
    if all_branches is None:
        return expanded
    result: list[str] = []
    for pattern in expanded:
        if pattern == "**":
            return list(all_branches)
        for b in all_branches:
            if _branch_matches(b, pattern) and b not in result:
                result.append(b)
    return result


def default_branches_for_rank(
    rank: str | None,
    squad: str | None,
) -> tuple[list[str], list[str]]:
    """Return (readable_branches, writable_branches) defaults based on rank.

    - **specialist**: read/write ``squad/{squad}`` only
    - **captain**: read/write ``squad/{squad}`` + read ``main``
    - **mission_controller** / **zeus**: read/write ``main``
    - Anything else / None: unrestricted (empty lists)
    """
    rank_lower = (rank or "").lower()
    squad_branch = f"{SQUAD_PREFIX}{squad}" if squad else None

    if rank_lower == "specialist" and squad_branch:
        return ([squad_branch], [squad_branch])
    if rank_lower == "captain" and squad_branch:
        return ([squad_branch, GLOBAL_BRANCH], [squad_branch])
    if rank_lower in ("mission_controller", "zeus"):
        return ([GLOBAL_BRANCH], [GLOBAL_BRANCH])
    # Unknown rank / no rank → unrestricted
    return ([], [])


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

class Router:
    """
    Hierarchical routing engine with YAML-configurable rules.

    Combines per-agent profile ACLs (set during registration) with
    role-based routing config (loaded from ``.cvc/routing.yaml``).

    Profile ACLs take precedence — if an agent has explicit ``readable_branches``
    or ``writable_branches`` in its profile, those are used.  Otherwise the
    routing config's role-based rules apply.
    """

    def __init__(
        self,
        index: IndexDB,
        registry: AgentRegistry,
        config: RoutingConfig | None = None,
    ) -> None:
        self._index = index
        self._registry = registry
        self._config = config or RoutingConfig()

    @property
    def config(self) -> RoutingConfig:
        return self._config

    # -- Routing -----------------------------------------------------------

    def target_branch(self, agent_id: str) -> str:
        """Determine the default write branch for an agent based on its squad."""
        profile = self._registry.get(agent_id)
        if profile is None:
            return GLOBAL_BRANCH
        squad = profile.get("squad")
        if squad:
            return f"{SQUAD_PREFIX}{squad}"
        return GLOBAL_BRANCH

    def route(self, agent_id: str) -> list[str]:
        """Determine all branches a commit from this agent should be routed to.

        For most agents this returns a single branch (their squad branch or
        main).  For agents with custom routing config, multiple branches may
        be returned (e.g., a captain writing to both squad and main).
        """
        profile = self._registry.get(agent_id)
        if profile is None:
            rules = self._config.rules_for_unregistered()
            return resolve_branch_patterns(
                rules.get("writable", ["main"]),
                None,
                self._all_branch_names(),
            ) or [GLOBAL_BRANCH]

        # Profile-level override
        writable = profile.get("writable_branches", [])
        if writable:
            return writable

        # Config-based routing
        role = (profile.get("role") or profile.get("rank") or "").lower()
        rules = self._config.rules_for_role(role)
        patterns = rules.get("writable", ["**"])
        return resolve_branch_patterns(
            patterns, profile, self._all_branch_names(),
        ) or [GLOBAL_BRANCH]

    # -- Validation --------------------------------------------------------

    def validate_write(self, agent_id: str, branch: str) -> bool:
        """Check if agent is allowed to write to the target branch."""
        profile = self._registry.get(agent_id)
        if profile is None:
            rules = self._config.rules_for_unregistered()
            patterns = rules.get("writable", ["main"])
            return any(_branch_matches(branch, p) for p in patterns)

        # Profile-level ACL (takes priority)
        writable = profile.get("writable_branches", [])
        if writable:
            return branch in writable or "**" in writable

        # Config-based ACL
        role = (profile.get("role") or profile.get("rank") or "").lower()
        rules = self._config.rules_for_role(role)
        patterns = rules.get("writable", ["**"])
        expanded = [_expand_pattern(p, profile) for p in patterns]
        return any(_branch_matches(branch, p) for p in expanded)

    def validate_read(self, agent_id: str, branch: str) -> bool:
        """Check if agent is allowed to read from the target branch."""
        profile = self._registry.get(agent_id)
        if profile is None:
            rules = self._config.rules_for_unregistered()
            patterns = rules.get("readable", ["main"])
            return any(_branch_matches(branch, p) for p in patterns)

        # Profile-level ACL
        readable = profile.get("readable_branches", [])
        if readable:
            return branch in readable or "**" in readable

        # Config-based ACL
        role = (profile.get("role") or profile.get("rank") or "").lower()
        rules = self._config.rules_for_role(role)
        patterns = rules.get("readable", ["**"])
        expanded = [_expand_pattern(p, profile) for p in patterns]
        return any(_branch_matches(branch, p) for p in expanded)

    # -- Branch enumeration ------------------------------------------------

    def readable_branches(self, agent_id: str) -> list[str]:
        """Return list of concrete branches this agent can read from."""
        profile = self._registry.get(agent_id)
        if profile is None:
            rules = self._config.rules_for_unregistered()
            return resolve_branch_patterns(
                rules.get("readable", ["main"]),
                None,
                self._all_branch_names(),
            ) or [GLOBAL_BRANCH]

        # Profile-level
        readable = profile.get("readable_branches", [])
        if readable:
            if "**" in readable:
                return self._all_branch_names()
            return readable

        # Config-based
        role = (profile.get("role") or profile.get("rank") or "").lower()
        rules = self._config.rules_for_role(role)
        patterns = rules.get("readable", ["**"])
        return resolve_branch_patterns(
            patterns, profile, self._all_branch_names(),
        ) or self._all_branch_names()

    def writable_branches(self, agent_id: str) -> list[str]:
        """Return list of concrete branches this agent can write to."""
        profile = self._registry.get(agent_id)
        if profile is None:
            rules = self._config.rules_for_unregistered()
            return resolve_branch_patterns(
                rules.get("writable", ["main"]),
                None,
                self._all_branch_names(),
            ) or [GLOBAL_BRANCH]

        writable = profile.get("writable_branches", [])
        if writable:
            if "**" in writable:
                return self._all_branch_names()
            return writable

        role = (profile.get("role") or profile.get("rank") or "").lower()
        rules = self._config.rules_for_role(role)
        patterns = rules.get("writable", ["**"])
        return resolve_branch_patterns(
            patterns, profile, self._all_branch_names(),
        ) or self._all_branch_names()

    # -- Context isolation -------------------------------------------------

    def context_for(
        self, agent_id: str, limit: int = 20
    ) -> list[CognitiveCommit]:
        """Return recent commits visible to this agent (from accessible branches only).

        Branch ordering follows the ``context_priority`` config: branches
        listed earlier in the priority list are queried first and their
        commits appear higher in the result.  This implements the key hive
        mind feature: specialists see squad context first, captains see
        squad then global, zeus sees global only.
        """
        priority_branches = self._context_priority_branches(agent_id)
        readable = set(self.readable_branches(agent_id))

        commits: list[CognitiveCommit] = []
        seen: set[str] = set()

        # Query priority branches first (in order)
        for branch_name in priority_branches:
            if branch_name not in readable:
                continue
            for c in self._index.list_commits(branch=branch_name, limit=limit):
                if c.commit_hash not in seen:
                    seen.add(c.commit_hash)
                    commits.append(c)

        # Then remaining readable branches
        for branch_name in readable:
            if branch_name in {b for b in priority_branches}:
                continue
            for c in self._index.list_commits(branch=branch_name, limit=limit):
                if c.commit_hash not in seen:
                    seen.add(c.commit_hash)
                    commits.append(c)

        return commits[:limit]

    def context_by_branch(
        self, agent_id: str, *, limit_per_branch: int = 10,
    ) -> dict[str, list[CognitiveCommit]]:
        """Return commits grouped by branch for this agent's readable scope.

        Useful for UIs that want to display per-branch context.
        """
        result: dict[str, list[CognitiveCommit]] = {}
        for branch_name in self.readable_branches(agent_id):
            branch_commits = self._index.list_commits(
                branch=branch_name, limit=limit_per_branch,
            )
            if branch_commits:
                result[branch_name] = branch_commits
        return result

    # -- Branch auto-creation ----------------------------------------------

    def ensure_squad_branch(self, squad: str) -> None:
        """Create the squad branch if it doesn't exist yet."""
        branch_name = f"{SQUAD_PREFIX}{squad}"
        existing = self._index.get_branch(branch_name)
        if existing is not None:
            return
        main = self._index.get_branch(GLOBAL_BRANCH)
        if main is None:
            return
        self._index.upsert_branch(BranchPointer(
            name=branch_name,
            head_hash=main.head_hash,
            parent_branch=GLOBAL_BRANCH,
            description=f"Squad branch for {squad}",
        ))
        logger.info("Created squad branch %s", branch_name)

    def ensure_agent_branch(self, agent_id: str) -> None:
        """Create a per-agent branch (``agent/{id}``) if it doesn't exist."""
        branch_name = f"{AGENT_PREFIX}{agent_id}"
        existing = self._index.get_branch(branch_name)
        if existing is not None:
            return
        # Derive from the agent's squad branch if it exists, otherwise main
        profile = self._registry.get(agent_id)
        squad = profile.get("squad") if profile else None
        parent = GLOBAL_BRANCH
        if squad:
            squad_branch = f"{SQUAD_PREFIX}{squad}"
            if self._index.get_branch(squad_branch) is not None:
                parent = squad_branch
        base = self._index.get_branch(parent)
        if base is None:
            return
        self._index.upsert_branch(BranchPointer(
            name=branch_name,
            head_hash=base.head_hash,
            parent_branch=parent,
            description=f"Per-agent branch for {agent_id}",
        ))
        logger.info("Created agent branch %s (parent=%s)", branch_name, parent)

    # -- Internals ---------------------------------------------------------

    def _all_branch_names(self) -> list[str]:
        """Return all branch names in the index."""
        return [b.name for b in self._index.list_branches()]

    def _context_priority_branches(self, agent_id: str) -> list[str]:
        """Return ordered list of branches for context priority."""
        profile = self._registry.get(agent_id)
        if profile is None:
            return [GLOBAL_BRANCH]

        # Check routing config for context_priority
        role = (profile.get("role") or profile.get("rank") or "").lower()
        rules = self._config.rules_for_role(role)
        patterns = rules.get("context_priority")

        if patterns:
            return resolve_branch_patterns(
                patterns, profile, self._all_branch_names(),
            )

        # Fallback: squad branch first (if any), then main
        squad = profile.get("squad")
        if squad:
            squad_branch = f"{SQUAD_PREFIX}{squad}"
            return [squad_branch, GLOBAL_BRANCH]
        return [GLOBAL_BRANCH]
