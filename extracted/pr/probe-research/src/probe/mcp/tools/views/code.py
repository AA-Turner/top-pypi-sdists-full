"""code views: attached repositories and commits, what changed between runs, a run's owner/repo@sha, the README."""

from __future__ import annotations
from typing import Any
from ....shared.reads.search_contract import (
    ReadmeState,
    ReadmeUnavailableReason)
from probe.mcp.tools.view import _Req, _ViewData

#: ProjectReadmeOut, `markdown` last so a reader meets the provenance first.
_README_FIELDS = (
    "state",
    "reason",
    "repo",
    "path",
    "commit_sha",
    "html_url",
    "fetched_at",
    "markdown",
)

#: What a README read with no text MEANS, per state and unavailable reason.
#: The backend sends the state and reason codes only; the dashboard renders
#: its own copy for each, and an agent reading a bare `live` cannot tell it from
#: a failure.
_README_STATE_NOTES: dict[str, str] = {
    ReadmeState.LIVE: (
        "Probe holds no copy of this README: no installation of the Probe GitHub "
        "app covers the repository, so the dashboard reads it from GitHub in the "
        "browser. It is at html_url."
    ),
    ReadmeState.NONE: "No repository is attached to this project, so it has no README.",
}
_README_UNAVAILABLE_NOTES: dict[str, str] = {
    ReadmeUnavailableReason.NOT_FOUND_OR_NO_ACCESS: (
        "GitHub answered 404: the repository or its README does not exist, or the "
        "Probe GitHub app cannot see the repository."
    ),
    ReadmeUnavailableReason.RATE_LIMITED: "GitHub rate-limited the read; try again later.",
    ReadmeUnavailableReason.UPSTREAM_ERROR: "GitHub did not answer the read; try again later.",
    ReadmeUnavailableReason.APP_PERMISSION_REQUIRED: (
        "The Probe GitHub app is installed without the Contents permission; a GitHub "
        "admin has to approve that before the README can be read."
    ),
}


def _readme_note(state: Any, reason: Any) -> str | None:
    """The sentence a README read with no text carries, or None for a snapshot."""
    if state == ReadmeState.SNAPSHOT:
        return None
    if state == ReadmeState.UNAVAILABLE:
        return _README_UNAVAILABLE_NOTES.get(reason, "The README could not be read.")
    return _README_STATE_NOTES.get(state, "No README text came back.")


class CodeViewsMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    def _view_project_code(self, entity: dict, request: _Req) -> _ViewData:
        """The project's attached repositories + one page of commit timeline.

        The timeline is read THROUGH GitHub by the backend (ETag-cached), so
        `timeline.state` is part of the answer: `ok`, `stale` (real data,
        degraded freshness — GitHub could not refresh it just now) or
        `unavailable` (no data; the reason says why). A run's `sha` here means
        the run was BASED ON that commit (nearest pushed ancestor), never that
        it ran exactly that code — the uploaded archive stays the code's home.

        Filters: `commit=<sha>` drills to one commit (message body, files,
        stats, linked runs); `source=<id>` picks a repository when several are
        attached; `cursor`, `author`, `path`, `include_excluded` page and
        narrow the list. Attach is NOT here: `probe project code attach
        <project> <owner/repo>` is the write door.
        """
        sources = entity.get("code_sources") or []
        filters = dict(request.filters)
        sha = filters.pop("commit", None)
        source_id = filters.pop("source", None)
        source_rows = self._code_source_rows(sources)
        if sha:
            card = self.source.project_commit(
                str(entity["id"]), str(sha), str(source_id) if source_id else None
            )
            return _ViewData(payload={"commit": card, "sources": source_rows})
        if not sources:
            return _ViewData(
                payload={
                    "sources": [],
                    "note": (
                        "no code source attached. A person attaches from the "
                        "dashboard; an agent uses `probe project code attach "
                        "<project> <owner/repo> --reason ...` when the repo is "
                        "plainly this project's (e.g. a run's snapshot names it)."
                    ),
                }
            )
        selectable = [s for s in sources if s.get("status") in ("active", "missing")]
        if len(selectable) > 1 and not source_id:
            return _ViewData(
                payload={
                    "sources": source_rows,
                    "note": (
                        "several code sources are attached; pass "
                        'view_options={"source": "<id>"} to read one timeline'
                    ),
                }
            )
        if source_id:
            filters["source_id"] = str(source_id)
        page = self.source.project_code_commits(str(entity["id"]), **filters)
        timeline: dict = {"state": page.get("state")}
        if page.get("reason"):
            timeline["reason"] = page["reason"]
        if page.get("cursor"):
            timeline["next"] = 'view_options={"cursor": "%s"}' % page["cursor"]
        return _ViewData(
            payload={"sources": source_rows, "timeline": timeline},
            rows=page.get("items") or [],
            rows_key="commits",
            more_beyond=bool(page.get("cursor")),
        )

    #: The source-row keys every code view echoes — one trim, three views.
    _CODE_SOURCE_KEYS = (
        "id",
        "repo",
        "ref",
        "path_prefix",
        "status",
        "status_reason",
        "attached_via",
        "attach_reason",
        "head_sha",
        "start_sha",
        "html_url",
    )

    @classmethod
    def _code_source_rows(cls, sources: list[dict]) -> list[dict]:
        return [
            {key: s.get(key) for key in cls._CODE_SOURCE_KEYS if s.get(key) not in (None, "")}
            for s in sources
        ]

    def _view_experiment_code(self, entity: dict, request: _Req) -> _ViewData:
        """What changed in the repo between this experiment's runs (phase 6).

        STORED ROWS ONLY, unlike the project view's proxied timeline: the
        backend assembles this from run↔commit links and never asks GitHub, so
        a window here is the shas this experiment's runs actually resolved to
        — never the full git range between them. The project `view="code"`
        timeline is the complete, live history when that distinction matters.

        Sources are the PROJECT's (an experiment inherits them; attach stays a
        project-level write: `probe project code attach`). Runs are the rows —
        one per run, ordered by the run's own clock, each with its stored
        `owner/repo@sha`. Windows ride the fixed payload with commits
        compacted to short shas: the full rows (first_run_at, run_count) live
        on `GET /v1/projects/{ref}/code`, and re-printing them here would
        spend the row budget on the part that is already a summary.
        """
        out = self.source.experiment_code(str(entity["id"]))
        windows = []
        for window in out.get("windows") or []:
            row: dict = {
                key: window.get(key)
                for key in ("repo", "source_attached", "from_sha", "to_sha")
                if window.get(key) is not None
            }
            row["commits"] = [
                c.get("short_sha") or str(c.get("sha") or "")[:7]
                for c in window.get("commits") or []
            ]
            if window.get("commits_truncated"):
                row["commits_truncated"] = True
            windows.append(row)
        return _ViewData(
            payload={
                "sources": self._code_source_rows(out.get("sources") or []),
                "windows": windows,
            },
            rows=out.get("runs") or [],
            rows_key="runs",
        )

    def _view_run_code(self, entity: dict, request: _Req) -> _ViewData:
        """The run's resolved `owner/repo@sha` — and, with
        view_options={"compare_to": "run:<ref>"}, what changed in code between the
        two runs (base = the older run; `commits` reads oldest first).

        A compare FILTER on this view rather than a new view or a `reproduce`
        mode, deliberately: `code` is already the vocabulary's one word for
        "which commit is this code" (project timeline, experiment window), so
        the run grain completes that word instead of inventing a second one —
        and comparing IS the run-level code question asked about two runs, the
        way `commit=` drills the project timeline to one commit. Hanging it
        off `reproduce` was rejected: that view is an atomic passthrough of
        the backend manifest, and a second mode there would fork its contract.

        The plain read may verify resolvability against GitHub server-side
        (cached, bounded — it is the run panel's read); the compare is STORED
        ROWS ONLY, so its commit list is the shas runs resolved to between the
        two, never the full git range. Both are bounded server-side.
        """
        run_id = str(entity["id"])
        compare_to = request.filters.get("compare_to")
        if compare_to:
            ref = str(compare_to)
            if ref.startswith("run:"):
                ref = ref[len("run:") :]
            return _ViewData(payload={"compare": self.source.run_code_compare(run_id, ref)})
        return _ViewData(payload={"code": self.source.run_code(run_id)})

    def _view_project_readme(self, entity: dict, request: _Req) -> _ViewData:
        """The attached repository's README. Only a `snapshot` carries text; every
        other state says WHY there is none in `note`, because an absent
        `markdown` reads the same for "no repository attached", "Probe holds no
        copy, read it on GitHub" and "GitHub refused" -- and only the first is
        a fact about the project."""
        readme = self.source.project_readme(str(entity["id"]))
        shaped = {key: readme[key] for key in _README_FIELDS if readme.get(key) is not None}
        note = _readme_note(readme.get("state"), readme.get("reason"))
        if note:
            shaped["note"] = note
        return _ViewData(payload={"readme": shaped})
