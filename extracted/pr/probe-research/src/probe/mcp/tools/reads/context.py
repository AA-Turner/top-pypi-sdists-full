"""research_context: the projects, likely experiments and live runs a task starts from, fitted to a budget."""

from __future__ import annotations
from dataclasses import dataclass, field, replace

from ....sdk import errors
from ....shared.reads.search_contract import (
    EnvelopeState,
    MissingMarker)
from probe.mcp.tools.shaping.payload import to_dict
from probe.mcp.tools.shaping.shaping import _fit_sections, _tokens


@dataclass(frozen=True, slots=True)
class ContextHeader:
    """What a context answer always carries, ahead of its sections; its size comes off the budget first."""

    task: str
    session_id: str | None
    project: dict | None  # the resolved project record, or null when none was named or unique
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class ContextSections:
    """The budgeted lists, in priority order: the budget fills them in field order."""

    relevant_experiments: list[dict]
    active_runs: list[dict]
    projects: list[dict] | None  # null once a project is resolved: the caller already has it


def _text(record: dict) -> str:
    fields = [
        record.get("id"),
        record.get("slug"),
        record.get("name"),
        record.get("description"),
        record.get("question"),
        record.get("conclusion"),
        " ".join(record.get("tags") or []),
    ]
    return " ".join(str(value) for value in fields if value).lower()


class ContextMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    def research_context(
        self,
        task: str,
        project_ref: str | None = None,
        session_id: str | None = None,
        token_budget: int = 1800,
    ) -> dict:
        projects = self.source.projects(limit=50)
        project = None
        if project_ref:
            needle = project_ref.lower()
            project = next(
                (
                    item
                    for item in projects
                    if needle
                    in {str(item.get("id", "")).lower(), str(item.get("slug", "")).lower()}
                ),
                None,
            )
        elif len(projects) == 1:
            project = projects[0]
        experiments = self.source.experiments(
            project_id=str(project["id"]) if project else None, limit=30
        )
        terms = set(task.lower().split())
        relevant = sorted(
            experiments,
            key=lambda item: len(terms.intersection(_text(item).split())),
            reverse=True,
        )[:5]
        active_runs: list[dict] = []
        for experiment in relevant[:3]:
            active_runs.extend(
                run
                for run in self.source.runs(experiment_id=str(experiment["id"]), limit=10)
                if run.get("status") in {"created", "running"}
            )
        if project is not None:
            # PROJECT-DIRECT runs (research-os 0054) belong to no experiment, so
            # the sweep above can never see them. direct=True filters server-side
            # (so ten attached runs can't mask an active direct one); the
            # client-side experiment_id filter stays as belt-and-braces, and the
            # SDK's project_id guard raises on a pre-0054 backend that would
            # have returned unscoped rows — degrade to the experiment sweep.
            try:
                direct_runs = self.source.runs(project_id=str(project["id"]), direct=True, limit=10)
            except errors.NotFoundError:
                direct_runs = []
            active_runs.extend(
                run
                for run in direct_runs
                if run.get("status") in {"created", "running"} and not run.get("experiment_id")
            )
        # The separate asset registry is retired: a reusable asset IS an artifact
        # now, so there is no second inventory to fetch and nothing here can be
        # missing on its account.
        missing: list[str] = []

        header = to_dict(ContextHeader(task=task, session_id=session_id, project=project))
        # `missing` is what THIS response lacks, NOT an inventory of everything the
        # backend cannot do. Deriving it from every False capability is what pinned
        # every context envelope to partial forever: portable_snapshots is honestly
        # and permanently False, so `missing` could never be empty and stopped
        # carrying information. Only versioned_assets gates content returned here.
        wanted = ContextSections(
            relevant_experiments=relevant,
            active_runs=active_runs[:10],
            projects=[] if project is not None else projects,
        )
        kept, truncated = _fit_sections(
            list(to_dict(wanted).items()), max(0, token_budget - _tokens(header))
        )
        sections = ContextSections(**kept)
        if truncated:
            missing.append(MissingMarker.TRUNCATED_BY_TOKEN_BUDGET)
        if project is not None:
            sections = replace(sections, projects=None)
        return self._envelope(
            {**header, **to_dict(sections)},
            state=EnvelopeState.PARTIAL if missing else EnvelopeState.COMPLETE,
            missing=missing,
        )
