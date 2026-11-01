"""file views: artifacts at every level, inherited files, version chains (reuse check), stored text in line sections, papers, groups."""

from __future__ import annotations
import hashlib
from typing import Any
from ....sdk import errors
from probe.mcp.tools.view import _Req, _ViewData

# Rows fetched past the caller's offset — far more than any sane token_budget
# emits, so a page costs one backend call. The slice is client-side because the
# spans/artifacts/events routes take no offset (only `limit`).
_PAGE_FETCH = 200

# Transcript sectioning. GET /v1/sessions/{id}/transcript returns ONE complete
# document (no server-side windowing exists), so the view splits it into
# line-sections and lets the ordinary rows machinery bound and page them. 40
# lines is a screenful of dialogue -- big enough that a default budget reads
# meaningful context, small enough that the cursor lands with usable granularity.
_TRANSCRIPT_SECTION_LINES = 40
#: Artifact `content` view: text files up to this size; larger ones download.
_ARTIFACT_CONTENT_MAX_BYTES = 2 * 1024 * 1024
_TRANSCRIPT_CONTEXT_DEFAULT = 3
_TRANSCRIPT_CONTEXT_MAX = 20


def _satisfies(version: dict, requirement: str) -> bool:
    """Does this artifact version satisfy `requirement`?

    Artifact versions are MONOTONIC INTEGERS with optional labels, not semver --
    so this supports exactly what the data supports: an exact label/version
    match, or `>=N` / `>N` / `<=N` / `<N` against the integer. Pretending to
    understand semver ranges over integer versions would answer confidently and
    wrongly, which is the failure mode this whole view exists to prevent.
    """
    raw = str(version.get("version", ""))
    label = version.get("label")
    requirement = requirement.strip()
    # Order matters: ">=" must be tested before ">", and "==" before "=".
    for op in (">=", "<=", "==", ">", "<", "="):
        if requirement.startswith(op):
            operand = requirement[len(op) :].strip()
            try:
                have, want = int(raw), int(operand)
            except (TypeError, ValueError):
                # A malformed operand must NOT quietly answer "no version
                # satisfies this". That is a THIRD kind of nothing, and it is
                # indistinguishable from a real version ceiling: the caller sees
                # state="no_match" with completeness="complete", believes the
                # artifact is too old, and registers a duplicate -- the exact
                # outcome this view exists to prevent. ">=2.0" is the obvious
                # way to write this and it is not a version here.
                raise errors.ValidationError(
                    f"artifact versions are monotonic integers, not semver: "
                    f"{requirement!r} does not name one (try '>=2', '<3', "
                    f"'==1', or a bare label)",
                    status=422,
                ) from None
            return {
                ">=": have >= want,
                "<=": have <= want,
                "==": have == want,
                "=": have == want,
                ">": have > want,
                "<": have < want,
            }[op]
    # Bare value: exact match on version or label.
    return requirement == raw or requirement == label


class FileViewsMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    def _view_run_artifacts(self, entity: dict, request: _Req) -> _ViewData:
        rows = self.source.run_artifacts(str(entity["id"]), **request.filters)
        payload: dict = {"filters": request.filters or None}
        # Async-outbox visibility (eng review 2026-07-29, 1A): a row with
        # status "pending" is a REGISTERED INTENT whose bytes have not arrived
        # (a client outbox may still deliver it); "failed" means the grace
        # window expired undelivered. Surfacing the counts here keeps the
        # metadata-match-is-not-the-blob rule unmissable for agents.
        pending = sum(1 for r in rows if isinstance(r, dict) and r.get("status") == "pending")
        failed = sum(1 for r in rows if isinstance(r, dict) and r.get("status") == "failed")
        if pending or failed:
            payload["undelivered"] = {
                "pending": pending,
                "failed": failed,
                "note": (
                    "pending = upload intent registered, bytes not yet arrived "
                    "(an async client outbox may still deliver); failed = the "
                    "grace window expired undelivered. Only status='complete' "
                    "rows have retrievable bytes."
                ),
            }
        return _ViewData(payload=payload, rows=rows, rows_key="artifacts")

    def _view_experiment_artifacts(self, entity: dict, request: _Req) -> _ViewData:
        return _ViewData(
            rows=self.source.experiment_artifacts(str(entity["id"])), rows_key="artifacts"
        )

    def _view_experiment_inherited(self, entity: dict, request: _Req) -> _ViewData:
        """What a fork reads live from its source: the source's run files as
        they were at the fork, or with `view_options.runs` the runs themselves.

        ONE route page per call, resumed on the route's own `after` (the last
        row id sent, `resume_key`), so every row stays reachable without
        re-reading from the first. `sources` is the chain, nearest first; the
        route counts `total` on the first page only. A file the source changed
        or removed since the fork is the fork's own file now and is listed by
        `view="artifacts"`, not here. An experiment that is no fork answers
        empty, and says so."""
        runs = request.filters.get("runs", False)
        if not isinstance(runs, bool):
            raise errors.ValidationError(
                "view_options.runs must be true (the source runs) or false (their files)",
                status=422,
            )
        home = entity.get("project_id")
        page = self.source.experiment_inherited(
            str(entity["id"]),
            runs=runs,
            after=request.after,
            limit=_PAGE_FETCH,
            project_id=str(home) if home else None,
        )
        items = [i for i in page.get("items") or [] if isinstance(i, dict)]
        sources = [
            {key: src[key] for key in ("id", "slug", "name", "forked_at") if src.get(key)}
            for src in page.get("sources") or []
            if isinstance(src, dict)
        ]
        payload: dict[str, Any] = {"kind": "runs" if runs else "files", "sources": sources}
        if isinstance(page.get("total"), int):
            payload["total"] = page["total"]
        if not sources:
            payload["note"] = "Not a fork: this experiment reads nothing live from another."
        elif not runs:
            # The route leaves out the files of runs behind the plan's
            # retention window and still lists those runs, so a short list here
            # is not the whole story.
            payload["note"] = (
                "Files of runs older than the plan's retention window are not listed; "
                'the runs are (view_options={"runs": true}).'
            )
        return _ViewData(
            payload=payload,
            rows=[{k: v for k, v in i.items() if v is not None} for i in items],
            rows_key="runs" if runs else "files",
            more_beyond=bool(page.get("next_after")) and bool(items),
            resume_key="id",
            resume_fetched=str(items[-1]["id"]) if items and items[-1].get("id") else None,
        )

    def _view_project_artifacts(self, entity: dict, request: _Req) -> _ViewData:
        return _ViewData(
            rows=self.source.project_artifacts(str(entity["id"])), rows_key="artifacts"
        )

    def _view_project_papers(self, entity: dict, request: _Req) -> _ViewData:
        """The papers recorded against this project, newest first.

        EMPTY IS AN ANSWER, and which answer depends on the project: on a
        review-flavored one it is a capture failure surfacing itself (someone
        read papers and recorded none); on a design-flavored one it is simply
        sparse. Either way it means "zero rows read successfully" and never
        "this read did not look" — a failed read raises rather than returning
        an empty list.

        Write with `probe paper add` / the SDK's `add_paper`; there is no write
        door here.
        """
        rows, more = self.source.project_papers(str(entity["id"]))
        return _ViewData(rows=rows, rows_key="papers", more_beyond=more)

    def _view_groups(self, entity: dict, request: _Req) -> _ViewData:
        """Sweeps/ensembles under an experiment — reached by a view, not by a
        research_list_groups tool. One group is research_get(ref="group:<id>")."""
        return _ViewData(rows=self.source.experiment_groups(str(entity["id"])), rows_key="groups")

    def _view_artifact_versions(self, entity: dict, request: _Req) -> _ViewData:
        """The reuse check's answer: this artifact's version chain, optionally
        narrowed to the versions that satisfy `requirement`.

        The two empty answers are OPPOSITES and this view is the only thing that
        can tell them apart, so it never collapses them:

        - the artifact does not exist -> resolution already raised NotFoundError
          (`artifact_by_name` for a name, the by-id `/versions` probe in
          `artifact_by_id` for an id), and a new identity is genuinely licensed.
          Note the two differ in REACH: a name only ever ruled out SHARED, while
          an id is global and rules out every anchor at once.
        - the artifact EXISTS but no version satisfies `requirement` ->
          state="no_match", carrying the versions that DO exist so the caller sees
          the real ceiling. Pin a new version of the SAME artifact.

        A caller that reads the second as the first opens a duplicate identity,
        which is the single most expensive avoidable error in this system.
        """
        versions = self.source.artifact_versions(str(entity["id"]))
        requirement = request.filters.get("requirement")
        if requirement is None or requirement == "":
            return _ViewData(rows=versions, rows_key="versions")
        requirement = str(requirement)
        # Validated BEFORE the per-version scan, not inside it. Inside, an artifact
        # with zero versions never reaches _satisfies, so a malformed ">=2.0" would
        # skip validation entirely and answer an authoritative no_match -- the
        # THIRD kind of nothing _satisfies exists to refuse, and indistinguishable
        # from a real ceiling.
        # "0" and not "": the probe must PARSE, so that only a malformed operand
        # raises. An unparseable probe version would reject ">=2" as well.
        _satisfies({"version": "0"}, requirement)
        matching = [v for v in versions if _satisfies(v, requirement)]
        if matching:
            return _ViewData(
                payload={"requirement": requirement},
                rows=matching,
                rows_key="versions",
            )
        # No match: return every version that EXISTS, not an empty list. An empty
        # list here is indistinguishable from an empty artifact, and that is the
        # confusion that creates duplicates.
        #
        # `highest_version` rides the FIXED-size payload rather than the rows,
        # because rows are what token_budget truncates: a tight budget could
        # otherwise emit state="no_match" with every version cut, promising a
        # ceiling the response no longer carries. The ceiling is the whole answer,
        # so it must survive truncation.
        numeric = [int(v["version"]) for v in versions if str(v.get("version", "")).isdigit()]
        return _ViewData(
            payload={
                "requirement": requirement,
                "satisfied_by": None,
                "highest_version": max(numeric) if numeric else None,
                "version_count": len(versions),
            },
            rows=versions,
            rows_key="versions",
            no_match=True,
        )

    def _view_versions(self, entity: dict, request: _Req) -> _ViewData:
        """Real, against the live registry: this view used to unconditionally
        report missing:["versioned_assets"] and had never been implemented."""
        return _ViewData(
            rows=self.source.experiment_versions(str(entity["id"])), rows_key="versions"
        )

    def _line_sections(
        self, lines: list[str], request: _Req, payload: dict[str, Any], *, noun: str
    ) -> _ViewData:
        """One text document as bounded line sections: a plain read pages from
        `start_line`, `grep` returns one section per matching line with
        `context_lines` around it. Shared by session transcripts and artifact
        content, so both read and page the same way."""
        total = len(lines)
        window = request.offset + _PAGE_FETCH
        grep = request.filters.get("grep")
        if grep is None:
            if "context_lines" in request.filters:
                # Accepted-but-inert is the lie the filter table guards against,
                # one key at a time.
                raise errors.ValidationError(
                    "context_lines only applies together with grep", status=422
                )
            start = self._transcript_int(request.filters, "start_line", default=1, floor=1)
            starts = range(start, total + 1, _TRANSCRIPT_SECTION_LINES)
            rows = [
                {
                    "line_start": a,
                    "line_end": min(total, a + _TRANSCRIPT_SECTION_LINES - 1),
                    "text": "\n".join(lines[a - 1 : a + _TRANSCRIPT_SECTION_LINES - 1]),
                }
                for a in starts[:window]
            ]
            return _ViewData(
                payload=payload,
                rows=rows,
                rows_key="sections",
                more_beyond=len(starts) > window,
            )
        if not isinstance(grep, str) or not grep:
            # An empty needle matches EVERY line ("" in s is always True), i.e. a
            # request to read the whole transcript wearing a search's clothes,
            # and a list/dict would str()-coerce into a surprising literal. Both
            # are caller errors, refused rather than answered.
            raise errors.ValidationError(
                f"grep must be a non-empty string: to read the whole {noun} "
                "omit grep and page the sections instead",
                status=422,
            )
        if "start_line" in request.filters:
            # Symmetric with the context_lines-without-grep guard above:
            # start_line is a plain-read control the grep scan never consults, so
            # accepting it beside grep is the accepted-but-inert lie again.
            raise errors.ValidationError(
                "start_line applies to a plain read, not to grep (grep scans the "
                f"whole {noun}); pass one or the other",
                status=422,
            )
        context = self._transcript_int(
            request.filters, "context_lines", default=_TRANSCRIPT_CONTEXT_DEFAULT, floor=0
        )
        context = min(context, _TRANSCRIPT_CONTEXT_MAX)
        needle = grep.lower()
        rows = []
        more = False
        for n, line in enumerate(lines, start=1):
            if needle in line.lower():
                if len(rows) >= window:
                    # One match past the window is all it takes to know there is
                    # more; stop rather than scanning (and section-joining) the
                    # rest of a large transcript for rows this page cannot carry.
                    more = True
                    break
                a, b = max(1, n - context), min(total, n + context)
                rows.append(
                    {
                        "line": n,
                        "line_start": a,
                        "line_end": b,
                        "text": "\n".join(lines[a - 1 : b]),
                    }
                )
        # no_match: the whole document was scanned and no line contains the
        # needle -- an answer, with total_lines as its denominator, distinct from
        # a page that filled and left more behind (more_beyond).
        return _ViewData(
            payload=payload,
            rows=rows,
            rows_key="sections",
            more_beyond=more,
            no_match=not rows,
        )

    def _view_artifact_content(self, entity: dict, request: _Req) -> _ViewData:
        """The artifact's stored TEXT, in bounded line sections.

        Any anchor (run, experiment, project, shared): the id already resolved
        under the caller's tenant. Refused by name, never answered empty, when
        there is no text to give: a client-owned reference (no managed bytes), a
        file past `_ARTIFACT_CONTENT_MAX_BYTES`, or bytes that are not UTF-8 text.
        """
        artifact_id = str(entity["id"])
        download = f"`probe artifact download {artifact_id} -o <path>`"
        if entity.get("is_reference"):
            raise errors.ValidationError(
                f"artifact {artifact_id} is a reference ({entity.get('uri')}); Probe "
                "holds no bytes for it, so read it from where it lives",
                status=422,
            )
        size = entity.get("size_bytes")
        if isinstance(size, int) and size > _ARTIFACT_CONTENT_MAX_BYTES:
            raise errors.ValidationError(
                f"artifact {artifact_id} is {size} bytes, past this view's "
                f"{_ARTIFACT_CONTENT_MAX_BYTES}-byte text limit; fetch it with {download}",
                status=422,
            )
        blob = self.source.artifact_content(artifact_id)
        if len(blob) > _ARTIFACT_CONTENT_MAX_BYTES:
            raise errors.ValidationError(
                f"artifact {artifact_id} is {len(blob)} bytes, past this view's "
                f"{_ARTIFACT_CONTENT_MAX_BYTES}-byte text limit; fetch it with {download}",
                status=422,
            )
        try:
            if b"\x00" in blob:
                raise UnicodeDecodeError("utf-8", blob, 0, 1, "NUL byte")
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            raise errors.ValidationError(
                f"artifact {artifact_id} is binary (not UTF-8 text); fetch it with {download}",
                status=422,
            ) from None
        lines = text.split("\n")
        payload: dict[str, Any] = {
            "name": entity.get("name"),
            "content_type": entity.get("content_type"),
            "size_bytes": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest(),
            "total_lines": len(lines),
            "filters": request.filters or None,
        }
        return self._line_sections(lines, request, payload, noun="file")
