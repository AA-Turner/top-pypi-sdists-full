"""Source→deploy branch topology of a project: is merged work already shipped?

Single source of truth for the question "does a merged ticket still have a deployment
step ahead of it?", shared by the two paths that settle a ticket's board status:
``workflow_transition.settle_issue_after_merge`` (live, on merge) and
``issue_workflow_update`` (reconciliation). They used to answer it differently — the
former on the ``board.to_deploy`` flag alone, the latter on the flag *and* the branch
topology — which parked merged tickets forever on repos that deploy from the MR
pipeline (Terraform apply, ArgoCD) and never grow a ``deploy/*`` branch.
"""

from typing import Any

from ..common.glab.runner import glab_api, glab_api_paginated
from ..common.project_config import ProjectConfig, ProjectConfigError, load_project_config_for

# source branch (pattern) → deploy branch (pattern); a ``*`` on both sides corresponds.
DEFAULT_DEPLOY_BRANCHES: dict[str, str] = {"main": "deploy/prod", "support/*": "deploy/support/*"}


def deploy_branches_for(project_path: str, override: dict[str, str] | None = None) -> dict[str, str]:
    """Source→deploy branch mapping for a project: CLI override, else its config, else defaults."""
    if override:
        return override
    cfg = _config_for(project_path)
    if cfg is not None and cfg.board.deploy_branches:
        return cfg.board.deploy_branches
    return dict(DEFAULT_DEPLOY_BRANCHES)


def shipped_when_job_for(project_path: str) -> str | None:
    """The CI job that stands in for a branch movement on this project (``board.shipped_when_job``).

    When set, a merged ticket has shipped once that job succeeded on its MR's pipeline.
    ``None`` (the default, and the fallback on a missing/broken config) keeps the branch oracle.
    """
    cfg = _config_for(project_path)
    return cfg.board.shipped_when_job if cfg is not None else ProjectConfig().board.shipped_when_job


def uses_to_deploy_column(project_path: str) -> bool:
    """Whether the project opts into the ``workflow::To deploy`` column (``board.to_deploy``).

    ``False`` marks a repo that ships at merge, so To deploy is skipped and a merged ticket
    is closed at once rather than parked. Missing/broken config falls back to the default (on).
    """
    cfg = _config_for(project_path)
    return cfg.board.to_deploy if cfg is not None else ProjectConfig().board.to_deploy


def branch_exists(project_id: str, branch: str) -> bool:
    enc = branch.replace("/", "%2F")
    return glab_api(f"projects/{project_id}/repository/branches/{enc}") is not None


def list_branch_names(project_id: str, search: str) -> list[str]:
    """Branch names of the project whose name contains ``search`` (paginated)."""
    enc = search.replace("/", "%2F")
    data = glab_api_paginated(f"projects/{project_id}/repository/branches?search={enc}")
    return [str(b["name"]) for b in data if b.get("name")]


def wildcard_capture(name: str, pattern: str) -> str | None:
    """Match ``name`` against a one-``*`` ``pattern``; return the ``*`` capture, or None.

    A pattern with no ``*`` matches only its exact self (capture ``""``).
    """
    if "*" not in pattern:
        return "" if name == pattern else None
    head, tail = pattern.split("*", 1)
    if name.startswith(head) and name.endswith(tail) and len(name) >= len(head) + len(tail):
        return name[len(head) :] if not tail else name[len(head) : len(name) - len(tail)]
    return None


def resolve_deploy_pairs(project_id: str, mapping: dict[str, str]) -> list[tuple[str, str]]:
    """Expand a source→deploy pattern mapping to concrete ``(source, deploy)`` branch pairs.

    A wildcard source (``support/*``) is globbed against the repo branches; the capture
    fills the deploy pattern (``deploy/support/*`` → ``deploy/support/<capture>``). A pair
    is kept only when its **deploy** branch exists (that is what makes the line deployable).
    """
    pairs: list[tuple[str, str]] = []
    for src_pattern, dep_pattern in mapping.items():
        if "*" in src_pattern:
            prefix = src_pattern[: src_pattern.index("*")]
            for src in list_branch_names(project_id, prefix):
                cap = wildcard_capture(src, src_pattern)
                if cap is None:
                    continue
                dep = dep_pattern.replace("*", cap) if "*" in dep_pattern else dep_pattern
                if (src, dep) not in pairs and branch_exists(project_id, dep):
                    pairs.append((src, dep))
        else:
            dep = dep_pattern
            if (src_pattern, dep) not in pairs and branch_exists(project_id, dep):
                pairs.append((src_pattern, dep))
    return pairs


def has_deploy_step(project_id: str, project_path: str = "") -> bool:
    """Whether a merged ticket must still wait in ``workflow::To deploy`` on this project.

    An explicit opt-out (``board.to_deploy: false``) always wins. Otherwise a step remains
    when the project names a deployment job (``board.shipped_when_job`` — the shipment is
    that job succeeding, not a branch moving), or when at least one source→deploy branch
    pair resolves. A repo with neither has no deployment step after the merge — its CI
    applies from the MR pipeline — so merging *is* shipping and the ticket closes.

    Fail-safe: when no pair resolves and the repo's branches cannot be listed at all, To
    deploy is kept — a transient API failure must never close a ticket early.
    """
    if not uses_to_deploy_column(project_path):
        return False
    if shipped_when_job_for(project_path):
        return True
    if resolve_deploy_pairs(project_id, deploy_branches_for(project_path)):
        return True
    return not _branches_reachable(project_id)


def _branches_reachable(project_id: str) -> bool:
    """Whether the project's branch list answers at all (proof the API call worked)."""
    data: Any = glab_api(f"projects/{project_id}/repository/branches?per_page=1")
    return isinstance(data, list) and bool(data)


def _config_for(project_path: str) -> ProjectConfig | None:
    if not project_path:
        return None
    try:
        return load_project_config_for(project_path)
    except ProjectConfigError:
        return None
