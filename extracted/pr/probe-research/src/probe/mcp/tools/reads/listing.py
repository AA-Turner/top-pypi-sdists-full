"""browse_list, every list mode, and its shared walk: resume after the last row sent, fill past hidden rows, page whole rows."""

from __future__ import annotations
import json
import uuid
from typing import Any
from ....sdk import errors
from ...delivery import accounting
from ..views import branch_projection as _branches
from ....shared.reads.search_contract import (
    BrowseMode,
    EntityType,
    EnvelopeState,
    MissingMarker,
    NoteCatalogKind)
from ...delivery.context import source_changed
from probe.mcp.tools.shaping.cursors import _pack_cursor, _unpack_cursor
from probe.mcp.tools.view import _supported_views
from probe.mcp.source import RunListQuery


class BrowseListMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    # -- browse: the flat listings ------------------------------------------------
    #
    # Every mode but `projects` lists ONE kind of row from ONE route, newest-first or
    # name-ordered as that route orders it. The service answers one backend page
    # (from the position its own cursor names) and says, per row, the cursor that
    # resumes AFTER that row (`_list_after`) -- the same contract the tree's
    # `_browse_handles` give browse delivery, so delivery can send the largest
    # prefix of WHOLE rows the budget holds and continue exactly where it cut,
    # never skipping a row it did not send. See `browse_list` for why a position
    # is always the last row sent and never a count.

    #: Rows one flat-listing page fetches at most. Kept small: a notes
    #: continuation re-reads its page to find the row it stopped after.
    _BROWSE_LIST_MAX = 50

    #: The Shared and workspace file routes' own ceiling for one read (`le=1000`).
    #: They take no cursor, so a folder past it is unreachable by paging.
    _FILES_BACKEND_MAX = 1_000

    #: How many backend pages one flat-listing call reads looking for a row the
    #: caller may see, when the caller's own session work is hidden. Past it the
    #: call answers with no rows, `next_cursor` and a marker rather than walk an
    #: unbounded run of the caller's own rows in one request.
    _HIDDEN_FILL_PAGES = 5
    #: A short runs page under `X-Probe-Hide-Session-Work` re-reads this many
    #: rows WITHOUT the server's exclusion, once, to count what it hid (the
    #: route's own `limit` ceiling).
    _HIDDEN_COUNT_READ = 200

    @staticmethod
    def _list_position(cursor: str | None, mode: str) -> tuple[str | None, str | None]:
        """`(backend cursor, the last row sent)` from this mode's continuation
        token -- WHERE TO RESUME, never how many rows to skip.

        A position is the row the previous page ENDED on, not an offset into a
        re-fetched page: an offset counts rows, and a row that disappears (a run
        no longer active, a note emptied, a file deleted) between two calls
        shifts every later row by one, so the row after the cut is skipped with
        nothing saying so. The mode rides in the token so a cursor can never be
        replayed against a different listing."""
        if not cursor:
            return None, None
        parsed = _unpack_cursor(cursor, hint="browse")
        backend, last = parsed.get("c"), parsed.get("a")
        if (
            parsed.get("browse") != str(mode)
            or (backend is not None and not isinstance(backend, str))
            or (last is not None and not isinstance(last, str))
        ):
            raise errors.ValidationError(
                f"this cursor does not continue browse(mode={str(mode)!r}): pass the "
                "next_cursor value from a previous call with the same arguments",
                status=422,
            )
        return backend, last

    @staticmethod
    def _list_cursor(mode: str, backend: str | None = None, last: str | None = None) -> str:
        return _pack_cursor({"browse": str(mode), "c": backend, "a": last})

    @staticmethod
    def _uuid_ref(value: str, kinds: tuple[str, ...], *, what: str) -> tuple[str, str]:
        """`kind:<uuid>` -> `(kind, uuid)` for one of `kinds`, or a refusal that
        names the accepted forms. A UUID because these filters are UUID-typed
        query parameters: a slug would 422 at the route in words about a field
        the caller never wrote."""
        kind, _, ident = str(value).partition(":")
        try:
            if kind not in kinds or not ident:
                raise ValueError
            uuid_value = str(uuid.UUID(ident))
        except ValueError:
            accepted = " or ".join(f"`{k}:<uuid>`" for k in kinds)
            raise errors.ValidationError(
                f"{what} takes {accepted}, not {value!r}: name the scope with `project` or "
                "`experiment` instead (a slug or a uuid)",
                status=422,
            ) from None
        return kind, uuid_value

    _TEAM_NOTE_IDENTITY = f"{NoteCatalogKind.TEAM_NOTE.value}:"

    #: Per catalog mode: the caller's argument name -> the route's query name.
    #: The ONLY filters each mode sends; `server._BROWSE_MODE_ARGS` refuses
    #: the rest before they reach here.
    _CATALOG_FILTERS: dict[BrowseMode, dict[str, str]] = {
        BrowseMode.DATASETS: {"query": "q", "project": "project", "registered": "registered"},
        BrowseMode.CHECKPOINTS: {
            "project": "project",
            "experiment": "experiment",
            "run": "run",
            "best": "best",
            "stored": "stored",
        },
        BrowseMode.SOURCES: {"query": "q", "provider": "provider", "kind": "kind"},
    }
    #: The catalog routes' own `limit` ceiling (`le=100`): what a continuation
    #: re-reads to find the row it stopped after.
    _CATALOG_REREAD_LIMIT = 100

    @staticmethod
    def _gone(what: str) -> errors.ValidationError:
        """The refusal for a continuation whose resume row has disappeared.
        Restarting is the only honest answer: guessing where the listing would
        have continued is how a row gets skipped."""
        return source_changed(f"the {what} this listing stopped after is gone since that page")

    def browse_list(
        self,
        mode: str,
        *,
        scope: str | None = None,
        status: str | None = None,
        tags: list[str] | None = None,
        active: bool | None = None,
        run_filter: dict | None = None,
        order: str | None = None,
        latest_metrics: list[str] | None = None,
        query: str | None = None,
        prefix: str | None = None,
        workspace_id: str | None = None,
        limit: int = 10,
        cursor: str | None = None,
        project: str | None = None,
        experiment: str | None = None,
        run: str | None = None,
        registered: str | None = None,
        best: bool | None = None,
        stored: str | None = None,
        provider: str | None = None,
        kind: str | None = None,
        branch: str | None = None,
        token_budget: int = 2000,
    ) -> dict:
        """One page of a flat listing: runs (newest first), workspaces, the
        notes catalog, the files in Shared / one workspace, or the data
        catalog's datasets, checkpoints or sources.

        `token_budget` sizes only a fixed part that scales: the workspace's
        pick history on the first branches page. Delivery fits the rows.

        Returns the compact envelope plus private keys browse delivery
        consumes and strips: `_list_after` (per row, the cursor resuming after
        it), `_list_end` (the cursor after the whole page, or None) and
        `_list_key` (where in `data` the rows are). An in-process caller reads
        `next_cursor`, which is `_list_end`.

        Every resume position names the LAST ROW SENT, in the form the route can
        act on: runs carry the list's own `(created_at, id)` keyset, notes the
        catalog page plus the row's identity (refused, never guessed, if it is
        gone), workspaces the row's id, files the row's name, the data catalog
        its page plus the row's ref (the notes fallback, for the same reason).
        None of them is a count of rows to skip.
        """
        mode = BrowseMode(mode)
        if mode is BrowseMode.PROJECTS:
            raise errors.ValidationError("mode=projects is browse_research", status=422)
        page_size = max(1, min(int(limit), self._BROWSE_LIST_MAX))
        backend_cursor, last_sent = self._list_position(cursor, mode)
        hide_session = accounting.session_work_to_hide()
        missing: list[str] = []
        data: dict[str, Any] = {"mode": str(mode)}
        # (projected row, the cursor resuming after it) for every row this call
        # sends; `end` resumes after the whole page.
        sent: list[tuple[dict, str | None]] = []
        # Where the rows go in `data`: the mode's name, but one branch in full
        # lists its experiments.
        list_key = str(mode)
        end: str | None = None
        hidden: frozenset[str] | None = None
        # Rows the caller's own session accounted for, in the positions this
        # call read: said when they left the page short (`hidden_own_session_work`).
        hidden_count = 0
        hidden_count_more = False

        if (
            mode in (BrowseMode.RUNS, BrowseMode.NOTES, BrowseMode.DATASETS, BrowseMode.CHECKPOINTS)
            and hide_session is not None
        ):
            created = self._session_created_ids(hide_session)
            if created is None:
                missing.append(MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED)
            else:
                hidden, truncated = created
                if truncated:
                    missing.append(MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED)

        if mode is BrowseMode.RUNS:
            (
                end, hidden_count, hidden_count_more, views_by_kind,
            ) = self._list_runs_page(
                active=active, backend_cursor=backend_cursor, data=data, end=end, hidden=hidden,
                hidden_count=hidden_count, hidden_count_more=hidden_count_more,
                hide_session=hide_session, kind=kind, missing=missing, mode=mode,
                page_size=page_size, scope=scope, sent=sent, status=status, tags=tags,
                query=RunListQuery(run_filter=run_filter or None, order=order or None,
                                   latest_metrics=latest_metrics or None),
            )
        elif mode in self._CATALOG_FILTERS:
            end, hidden_count, views_by_kind = self._list_catalog_page(
                backend_cursor=backend_cursor, best=best, data=data, end=end, experiment=experiment,
                hidden=hidden, hidden_count=hidden_count, kind=kind, last_sent=last_sent,
                missing=missing, mode=mode, page_size=page_size, project=project, provider=provider,
                query=query, registered=registered, run=run, sent=sent, stored=stored,
            )
        elif mode is BrowseMode.NOTES:
            if query is not None:
                data["query"] = query
            position, resume_after = backend_cursor, last_sent
            for _ in range(self._HIDDEN_FILL_PAGES):
                page = self.source.notes_catalog(query=query, cursor=position, limit=page_size)
                rows = [row for row in (page or {}).get("items") or [] if isinstance(row, dict)]
                backend_next = (page or {}).get("next_cursor")
                start = 0
                if resume_after is not None:
                    # Only for a row the catalog's keyset cannot name: the team
                    # note (the first page's singleton, with no keyset) or a
                    # kind this client has no rank for. Found again in the same
                    # page by identity.
                    found = next(
                        (
                            i
                            for i, row in enumerate(rows)
                            if self._note_identity(row) == resume_after
                        ),
                        None,
                    )
                    if found is not None:
                        start = found + 1
                    elif resume_after != self._TEAM_NOTE_IDENTITY:
                        raise self._gone("note")
                    # A team note emptied since: it only ever led page one, so
                    # every entity row of that page still follows it.
                    resume_after = None
                visible = [
                    row
                    for row in rows[start:]
                    if not (hidden and self._note_names_hidden(row, hidden))
                ]
                hidden_count += len(rows) - start - len(visible)
                end = self._list_cursor(mode, backend_next) if backend_next else None
                if visible or not backend_next:
                    break
                position = backend_next
            else:
                missing.append(MissingMarker.PAGE_HIDDEN_AS_OWN_SESSION_WORK)
            for index, row in enumerate(visible):
                if index + 1 == len(visible):
                    after = end
                elif keyset := self.source.note_cursor_after(row):
                    # The catalog's OWN cursor, built from the row: newer notes
                    # landing on the first page cannot push it off its page.
                    after = self._list_cursor(mode, keyset)
                else:
                    after = self._list_cursor(mode, position, self._note_identity(row))
                sent.append((self._note_row(row), after))
            views_by_kind = {row["entity_type"] for row, _ in sent if "entity_type" in row}
        elif mode is BrowseMode.WORKSPACES:
            # The whole list, every call (the route does not page; creation is
            # capped tenant-wide), resumed at the first workspace whose SORT
            # KEY is past the last one sent. The key, not the id: a workspace
            # renamed between pages moves in the order, and resuming after
            # wherever its id now sits ended the walk early or repeated rows.
            rows = [row for row in self.source.workspaces() or [] if isinstance(row, dict)]
            # In OUR key's order, not just the route's: they agree on prod
            # (datcollate=C), and on a database where they do not, resuming in
            # the route's order could hand back the same page forever.
            rows.sort(key=self._workspace_key)
            start = 0
            if last_sent is not None:
                try:
                    name, ident = json.loads(last_sent)
                    resume = (str(name), str(ident))
                except (ValueError, TypeError):
                    raise errors.ValidationError(
                        "malformed browse cursor: pass the next_cursor value from a "
                        "previous call with the same arguments",
                        status=422,
                    ) from None
                start = next(
                    (i for i, row in enumerate(rows) if self._workspace_key(row) > resume),
                    len(rows),
                )
            window = rows[start : start + page_size]
            for offset, row in enumerate(window, start=start):
                after = (
                    self._list_cursor(mode, last=json.dumps(list(self._workspace_key(row))))
                    if offset + 1 < len(rows)
                    else None
                )
                sent.append((self._workspace_row(row), after))
            end = sent[-1][1] if sent else None
            views_by_kind = set()
        elif mode is BrowseMode.BRANCHES:
            # The whole read every call (the route does not page), its rows
            # resumed after the last REF sent; delivery fits whole rows to the
            # budget. `branch` opens one branch in full FROM THIS READ, so a
            # branch that crosses projects keeps every member and number it
            # was listed with (a project read would cut it at the project).
            if workspace_id is None:
                raise errors.ValidationError(
                    "browse(mode='branches') needs workspace_id (browse(mode='workspaces') lists them)",
                    status=422,
                )
            try:
                workspace_id = str(uuid.UUID(str(workspace_id)))
            except ValueError:
                raise errors.ValidationError(
                    f"workspace_id must be a workspace UUID (browse(mode='workspaces') "
                    f"lists them), not {workspace_id!r}",
                    status=422,
                ) from None
            tier = _branches.project(
                self.source.workspace_branches(workspace_id),
                branch=branch,
                after=last_sent,
                workspace=True,
            )
            data.update(tier.payload)
            list_key = tier.rows_key
            if branch is None and last_sent is None:
                self._workspace_pick_history(
                    data, workspace_id, token_budget, missing, rows={list_key: tier.rows}
                )
            if hide_session is not None:
                missing.append(MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED)
            for offset, row in enumerate(tier.rows):
                after = (
                    self._list_cursor(mode, last=str(row["ref"]))
                    if offset + 1 < len(tier.rows)
                    else None
                )
                sent.append((row, after))
            end = None
            views_by_kind = set()
        else:
            end, views_by_kind = self._list_other_page(
                data=data, end=end, last_sent=last_sent, missing=missing, mode=mode,
                page_size=page_size, prefix=prefix, sent=sent, workspace_id=workspace_id,
            )

        data[list_key] = [row for row, _ in sent]
        if hidden_count and len(sent) < page_size:
            # A short page that the hiding made short: an agent must not read
            # "nothing here" off it (the audit's empty `browse(runs)`).
            data["hidden_own_session_work"] = hidden_count
            if hidden_count_more:
                data["hidden_own_session_work_more"] = True
        views = {kind: _supported_views(kind) for kind in sorted(views_by_kind)}
        if views:
            data["available_views"] = views
        envelope = self._envelope(
            data,
            state=EnvelopeState.PARTIAL if missing else EnvelopeState.COMPLETE,
            missing=missing,
            next_cursor=end,
        )
        envelope["_list_after"] = [after for _, after in sent]
        envelope["_list_end"] = end
        envelope["_list_key"] = list_key
        return envelope


    def _list_runs_page(
        self, *, active, backend_cursor, data, end, hidden, hidden_count, hidden_count_more,
        hide_session, kind, missing, mode, page_size, scope, sent, status, tags, query,
    ):
        """mode=runs: one page of runs, newest first, reading past the caller's own hidden work. An ordered read
        (`order` other than newest first) is ONE top-N page: the server sends no cursor for it, and no row here
        gets one either, since a `created_at` keyset would resume a different order."""
        project_id = experiment_id = None
        if scope is not None:
            kind, ident = self._uuid_ref(
                scope,
                (EntityType.PROJECT.value, EntityType.EXPERIMENT.value),
                what="browse(mode='runs') scope",
            )
            if kind == EntityType.PROJECT.value:
                project_id = ident
            else:
                experiment_id = ident
            data["scope"] = scope
        position = backend_cursor
        for _ in range(self._HIDDEN_FILL_PAGES):
            rows, backend_next = self.source.run_list(
                project_id=project_id,
                experiment_id=experiment_id,
                status=status,
                tags=tags,
                active=bool(active),
                cursor=position,
                limit=page_size,
                exclude_origin_session=hide_session,
                query=query,
            )
            visible = [
                row
                for row in rows
                if isinstance(row, dict)
                and row.get("id")
                and not (hidden and str(row["id"]).lower() in hidden)
            ]
            end = self._list_cursor(mode, backend_next) if backend_next else None
            if visible or not backend_next:
                break
            position = backend_next
        else:
            missing.append(MissingMarker.PAGE_HIDDEN_AS_OWN_SESSION_WORK)
        if hide_session is not None and hidden is not None and not end and len(visible) < page_size:
            # The listing ended short, and the server left the session's
            # runs out before the page was cut, so nothing here saw them:
            # read the same positions once without the exclusion and count
            # the ones the session created. Unknown, and left unsaid, when
            # that read fails -- never a failed browse.
            try:
                probe, probe_next = self.source.run_list(
                    project_id=project_id,
                    experiment_id=experiment_id,
                    status=status,
                    tags=tags,
                    active=bool(active),
                    cursor=backend_cursor,
                    limit=self._HIDDEN_COUNT_READ,
                    query=query,
                )
            except Exception:  # noqa: BLE001 -- the count is optional
                probe, probe_next = [], None
            hidden_count = sum(
                1
                for row in probe
                if isinstance(row, dict) and str(row.get("id") or "").lower() in hidden
            )
            hidden_count_more = bool(probe_next) and hidden_count > 0
        for index, row in enumerate(visible):
            if index + 1 == len(visible) or query.is_ordered:
                # An ordered page ends here: a budget cut says `truncated_by_token_budget`, never a cursor.
                after = end
            else:
                keyset = self.source.run_cursor_after(row)
                if keyset is None:
                    raise errors.ValidationError(
                        "a run row came back without `created_at`, so this "
                        "listing cannot resume after it; raise `limit` to read "
                        "the page whole",
                        status=422,
                    )
                after = self._list_cursor(mode, keyset)
            sent.append((self._run_row(row), after))
        if backend_cursor is None:
            # The whole listing's size, on its first page: a page is one page (Anthrogen 2026-11-05,
            # "ten runs failed" from a 10-row page of 26). Same filter, so the totals and the pages
            # count one set; never fails the browse.
            try:
                data["totals"] = self.source.run_counts(
                    project_id=project_id,
                    experiment_id=experiment_id,
                    status=status,
                    tags=tags,
                    is_active=bool(active),
                    exclude_origin_session=hide_session,
                    run_filter=query.run_filter,
                )
            except Exception:  # noqa: BLE001 -- an older API or a count past its bound
                missing.append(MissingMarker.TOTALS_UNAVAILABLE)
        views_by_kind = {EntityType.RUN.value}
        return end, hidden_count, hidden_count_more, views_by_kind


    def _list_catalog_page(
        self, *, backend_cursor, best, data, end, experiment, hidden, hidden_count, kind, last_sent,
        missing, mode, page_size, project, provider, query, registered, run, sent, stored,
    ):
        """A catalog mode (datasets, checkpoints, ...): one page of its filtered rows."""
        given = {
            "query": query,
            "project": project,
            "experiment": experiment,
            "run": run,
            "registered": registered,
            # A filter, not a toggle: `best=false` asks for nothing.
            "best": True if best else None,
            "stored": stored,
            "provider": provider,
            "kind": kind,
        }
        filters = {
            route_name: given[name]
            for name, route_name in self._CATALOG_FILTERS[mode].items()
            if given[name] is not None
        }
        data.update(
            {name: given[name] for name in self._CATALOG_FILTERS[mode] if given[name] is not None}
        )
        # The catalog lists' cursor is the server's own and opaque here, so
        # a cut INSIDE a page resumes by finding the last row sent again,
        # from the same position: refused, never guessed, if it is gone.
        # The re-read takes the route's ceiling, so rows registered since
        # cannot push that row off the page. A page's last row resumes on
        # the route's own cursor. Under `X-Probe-Hide-Session-Work` the
        # caller's own rows are left out and a page of nothing else reads
        # the next one, as for runs.
        position, resume_after = backend_cursor, last_sent
        for _ in range(self._HIDDEN_FILL_PAGES):
            page = self.source.catalog_list(
                str(mode),
                cursor=position,
                limit=page_size if resume_after is None else self._CATALOG_REREAD_LIMIT,
                **filters,
            )
            rows = [row for row in page.get("items") or [] if isinstance(row, dict)]
            for row in rows:
                if not (row.get("ref") or row.get("id")):
                    raise errors.ValidationError(
                        f"a {mode} row came back without `ref` or `id`, so this listing "
                        "cannot resume after it; raise `limit` to read the page whole",
                        status=422,
                    )
            start = 0
            if resume_after is not None:
                found = next(
                    (
                        i
                        for i, row in enumerate(rows)
                        if self._catalog_row_identity(row) == resume_after
                    ),
                    None,
                )
                if found is None:
                    raise self._gone(self._CATALOG_ROW_NAMES[mode])
                start = found + 1
            backend_next = page.get("next_cursor")
            fetched_end = self._list_cursor(mode, backend_next) if backend_next else None
            visible = [
                index
                for index in range(start, len(rows))
                if not (hidden and self._catalog_row_hidden(mode, rows[index], hidden))
            ]
            hidden_count += len(rows) - start - len(visible)
            for n, index in enumerate(visible[:page_size]):
                # Nothing this page still holds is sent after it: resume
                # on the route's own cursor, past the page's hidden tail.
                after = (
                    fetched_end
                    if n + 1 == len(visible)
                    else self._list_cursor(
                        mode, position, self._catalog_row_identity(rows[index])
                    )
                )
                sent.append((self._catalog_row(mode, rows[index]), after))
            end = sent[-1][1] if sent else fetched_end
            if sent or not backend_next:
                break
            position, resume_after = backend_next, None
        else:
            missing.append(MissingMarker.PAGE_HIDDEN_AS_OWN_SESSION_WORK)
        if (
            mode is BrowseMode.CHECKPOINTS
            and isinstance(page.get("totals"), dict)
            # Counted over the caller's own saves too, and named by project:
            # this view cannot take them out, so it does not send them.
            and not hidden
        ):
            # Bytes and counts for the WHOLE filtered listing, not this page.
            data["totals"] = page["totals"]
        views_by_kind = {row["entity_type"] for row, _ in sent}
        return end, hidden_count, views_by_kind


    def _list_other_page(
        self, *, data, end, last_sent, missing, mode, page_size, prefix, sent, workspace_id,
    ):
        """The remaining modes: one page of their rows, a workspace's when one is named."""
        if workspace_id is not None:
            try:
                workspace_id = str(uuid.UUID(str(workspace_id)))
            except ValueError:
                raise errors.ValidationError(
                    f"workspace_id must be a workspace UUID (browse(mode='workspaces') "
                    f"lists them), not {workspace_id!r}",
                    status=422,
                ) from None
            data["workspace_id"] = workspace_id
        if prefix is not None:
            data["prefix"] = prefix
        # Name-ordered and cursorless: the first page reads one row past
        # its window (so "there is more" is a fact), and a continuation reads
        # the route's whole ceiling and resumes after the last NAME sent.
        # Names are unique per folder, so the name IS the position.
        rows = [
            row
            for row in self.source.files(
                workspace_id=workspace_id,
                prefix=prefix,
                limit=(
                    min(page_size + 1, self._FILES_BACKEND_MAX)
                    if last_sent is None
                    else self._FILES_BACKEND_MAX
                ),
            )
            if isinstance(row, dict)
        ]
        start = 0
        if last_sent is not None:
            found = next(
                (i for i, row in enumerate(rows) if row.get("name") == last_sent), None
            )
            # A file deleted since the last page: continue at the first name
            # after it. Code-point order IS the route's `ORDER BY name` order
            # because the research databases are `datcollate=C` (UTF-8 bytes
            # sort as code points do).
            start = (
                found + 1
                if found is not None
                else next(
                    (i for i, row in enumerate(rows) if str(row.get("name")) > last_sent),
                    len(rows),
                )
            )
        window = rows[start : start + page_size]
        capped = len(rows) >= self._FILES_BACKEND_MAX
        if capped and start + page_size >= len(rows):
            # The window reached the end of what one read can return.
            missing.append(MissingMarker.FILES_BEYOND_BACKEND_LIMIT)
        for offset, row in enumerate(window, start=start):
            after = (
                self._list_cursor(mode, last=str(row.get("name")))
                if offset + 1 < len(rows)
                else None
            )
            sent.append((self._file_row(row), after))
        end = sent[-1][1] if sent else None
        views_by_kind = {EntityType.ARTIFACT.value}
        return end, views_by_kind
