"""``pysae-ai-tools ci verify-deploy-contract`` — assert every prod deploy job still
carries what the shared template promises.

For each project of the group that pulls ``gitlab-templates``' ``deploy.yml``: read its
raw ``.gitlab-ci.yml`` to find the jobs declaring ``extends: .deploy_prod``, resolve the
pipeline through GitLab's own CI-lint API, then check the resolved job kept every
guarantee in :data:`core.CONTRACT`.

Resolution is delegated to GitLab rather than reimplemented: ``extends``, ``!reference``,
anchors and cross-project ``include`` all behave exactly as they will at pipeline time.

Exit codes: ``0`` clean, ``2`` at least one violation (see the CLI conventions), ``1`` on
an operational failure.
"""

import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from typing import Annotated, Any

import typer
import yaml

from ...common.glab.runner import run_glab
from ...common.group import resolve_group
from ...common.project_config import discover_project_paths
from .core import Violation, includes_deploy_template, jobs_extending, violations_for_job

CI_FILE = ".gitlab-ci.yml"


class _TolerantLoader(yaml.SafeLoader):
    """SafeLoader that tolerates GitLab's custom tags (``!reference``) instead of raising."""


# yaml stubs type this as untyped; the callback shape is fixed by PyYAML.
_TolerantLoader.add_multi_constructor("!", lambda loader, suffix, node: None)  # type: ignore[no-untyped-call]


def _encode(project: str) -> str:
    return project.replace("/", "%2F")


def _raw_ci_file(project: str) -> str | None:
    res = run_glab("api", f"projects/{_encode(project)}/repository/files/{CI_FILE.replace('.', '%2E')}/raw?ref=HEAD")
    return res.stdout if res.ok and res.stdout.strip() else None


def _lint(project: str, content: str) -> dict[str, Any] | None:
    """Resolve a pipeline through GitLab CI-lint; ``None`` when the call itself failed."""
    payload = json.dumps({"content": content, "include_jobs": True})
    res = run_glab(
        "api",
        "-X",
        "POST",
        "-H",
        "Content-Type: application/json",
        f"projects/{_encode(project)}/ci/lint",
        "--input",
        "-",
        stdin_data=payload,
    )
    if not res.ok:
        return None
    try:
        parsed = json.loads(res.stdout)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def _audit_project(project: str) -> dict[str, Any]:
    """Audit one project; ``violations`` empty means it honours the contract."""
    raw = _raw_ci_file(project)
    if raw is None:
        return {"project": project, "skipped": "no .gitlab-ci.yml"}
    try:
        document = yaml.load(raw, Loader=_TolerantLoader)
    except yaml.YAMLError as exc:
        return {"project": project, "error": f"unparseable {CI_FILE}: {exc}"}
    # `extends: .deploy_prod` is the authoritative signal, so it decides on its own.
    # Gating on the include text first would silently skip a repo reaching the template
    # through an intermediate local file — measured as nobody today, which is exactly
    # when such a hole is cheapest to close.
    jobs = jobs_extending(document)
    if not jobs:
        return {"project": project, "skipped": "no job extends .deploy_prod"}
    if not includes_deploy_template(raw):
        # Its own `.deploy_prod`, not the shared one: nothing here promises those steps.
        return {"project": project, "skipped": "extends a local .deploy_prod, not the shared template"}
    linted = _lint(project, raw)
    if linted is None:
        return {"project": project, "error": "ci/lint call failed"}
    if not linted.get("valid"):
        # A pipeline that does not even lint is the consumer's own problem, not a
        # contract breach — report it without claiming the guarantees were dropped.
        return {"project": project, "error": f"pipeline invalid: {linted.get('errors')}"}
    try:
        merged = yaml.load(str(linted.get("merged_yaml") or ""), Loader=_TolerantLoader)
    except yaml.YAMLError as exc:
        return {"project": project, "error": f"unparseable merged_yaml: {exc}"}
    found: list[Violation] = []
    for job in jobs:
        resolved = merged.get(job) if isinstance(merged, dict) else None
        found.extend(violations_for_job(project, job, resolved))
    return {"project": project, "jobs": jobs, "violations": [v.to_dict() for v in found]}


def main(
    project: Annotated[
        list[str] | None,
        typer.Option("--project", help="Audit only these project(s) (repeatable). Default: every project in --group."),
    ] = None,
    group: Annotated[
        str | None, typer.Option("--group", help="Group whose projects are audited. Default: the resolved group.")
    ] = None,
    workers: Annotated[int, typer.Option("--workers", help="Concurrent project audits.")] = 8,
) -> None:
    """Check that every job extending ``.deploy_prod`` kept the template's guarantees.

    Overriding ``script:`` on such a job replaces the key wholesale and silently drops
    the steps the template appends after it. This command is the regression guard for
    that class of loss: it resolves each consumer's pipeline through GitLab CI-lint and
    fails when a guarantee is gone.
    """
    resolved_group = group or resolve_group()
    if project:
        projects = sorted(project)
    else:
        try:
            projects = discover_project_paths(resolved_group)
        except RuntimeError as exc:
            print(json.dumps({"error": str(exc)}))
            raise typer.Exit(1) from exc
    if not projects:
        print(json.dumps({"error": f"no projects found in group '{resolved_group}'"}))
        raise typer.Exit(1)

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        reports = list(pool.map(_audit_project, projects))

    audited = [r for r in reports if "violations" in r]
    breached = [r for r in audited if r["violations"]]
    errored = [r for r in reports if "error" in r]
    # Report why a project was left out: a silent skip reads as "covered", and this
    # command exists precisely because a silent loss went unnoticed for two months.
    skipped = Counter(str(r["skipped"]) for r in reports if "skipped" in r)
    print(
        json.dumps(
            {
                "group": resolved_group,
                "projects_scanned": len(projects),
                "projects_with_prod_deploy": len(audited),
                "projects_in_breach": len(breached),
                "skipped": dict(skipped),
                "results": breached,
                "errors": errored,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    if breached:
        raise typer.Exit(2)


if __name__ == "__main__":
    typer.run(main)
