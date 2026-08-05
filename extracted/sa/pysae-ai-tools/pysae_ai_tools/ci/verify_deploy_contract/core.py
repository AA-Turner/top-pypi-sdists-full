"""Pure logic for ``ci verify-deploy-contract`` (no I/O — unit-testable).

A consuming project composes its own prod deploy job with ``extends: .deploy_prod``,
then routinely overrides ``script:`` to slip one command in. GitLab replaces the whole
key, so the steps the template appends after ``deploy-children`` are dropped silently:
the ``deploy/prod`` push, the ``:deploy-prod`` ECR retag, and the post-deploy board
settling. Nothing fails, nothing warns — the loss only surfaces months later as tickets
piling up in a board column, or as an ArgoCD baseline pointing at a dead branch.

This module answers two questions from already-fetched data: which jobs claim to extend
the template, and which of the guarantees their *resolved* definition lost.
"""

import re
from dataclasses import dataclass

DEPLOY_PROD_BASE = ".deploy_prod"

# What `.deploy_prod` guarantees on top of `.deploy_env`, as a marker that must survive
# resolution → the human-readable guarantee it stands for. Matched against the resolved
# `script` + `after_script`, so a consumer re-implementing a step by hand still passes:
# the contract is the behaviour, not the provenance.
CONTRACT: dict[str, str] = {
    "refs/heads/deploy/prod": "push the deploy/prod bookkeeping branch",
    'CHANNEL_TAG="deploy-': "retag the deployed image as :deploy-<env> in ECR",
    "issue-close-release": "settle the board after a prod deploy",
}

_INCLUDES_DEPLOY_TEMPLATE = re.compile(r"gitlab-templates", re.I)


@dataclass(frozen=True)
class Violation:
    """One guarantee a consumer's resolved job lost."""

    project: str
    job: str
    marker: str
    guarantee: str

    def to_dict(self) -> dict[str, str]:
        return {"project": self.project, "job": self.job, "marker": self.marker, "guarantee": self.guarantee}


def includes_deploy_template(raw_text: str) -> bool:
    """Whether a raw ``.gitlab-ci.yml`` pulls the shared ``deploy.yml`` template.

    Text-level on purpose: the include may sit behind ``deploy.auto.yml`` or a local
    file that re-includes it, and a false positive is harmless (the job lookup below
    simply finds nothing).
    """
    return bool(_INCLUDES_DEPLOY_TEMPLATE.search(raw_text)) and "deploy.yml" in raw_text


def jobs_extending(document: object, base: str = DEPLOY_PROD_BASE) -> list[str]:
    """Names of the top-level jobs whose ``extends`` mentions ``base``.

    Reads the *raw* document: after CI-lint resolution ``extends`` is gone, so the
    intent to build on the template can only be read before merging.
    """
    if not isinstance(document, dict):
        return []
    found: list[str] = []
    for name, body in document.items():
        if not isinstance(name, str) or name.startswith(".") or not isinstance(body, dict):
            continue
        extends = body.get("extends")
        targets = [extends] if isinstance(extends, str) else extends if isinstance(extends, list) else []
        if any(isinstance(t, str) and t == base for t in targets):
            found.append(name)
    return found


def _flatten(value: object) -> str:
    """Flatten a `script:`-shaped value (str, or nested lists from `!reference`) to text."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(_flatten(v) for v in value)
    return ""


def violations_for_job(project: str, job: str, resolved: object) -> list[Violation]:
    """Contract markers missing from a resolved job's ``script`` + ``after_script``."""
    if not isinstance(resolved, dict):
        return [Violation(project, job, marker, guarantee) for marker, guarantee in CONTRACT.items()]
    body = _flatten(resolved.get("script")) + "\n" + _flatten(resolved.get("after_script"))
    return [Violation(project, job, m, g) for m, g in CONTRACT.items() if m not in body]
