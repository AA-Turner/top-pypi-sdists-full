"""NotesResource (client.notes, typed reads) and NotesMixin, Client's methods: notes, sub-notes, the
notes catalog, the project notes file and the team note (twins: app/notes, app/team_notes)."""

from __future__ import annotations
from ....generated.models import (
    NoteCatalogOut,
    SubNoteListOut,
    SubNoteOut,
    TeamNoteBriefOut,
    TeamNoteOut,
    TeamNoteVersionsOut,
)
from ..resource import Resource

from ... import errors


class NotesMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- the project's notes file ------------------------------------------
    # One markdown document per project that agents read and write. Deliberately NOT
    # a schema: an earlier attempt gave notes a kind vocabulary
    # (intent/decision/observation/...), supersession and an authority field, and
    # nothing server-side validated, aggregated or grouped by any of it -- eight
    # kinds bought one list filter. Prose is what people actually write.
    #
    # It is a COLUMN on the project (research-os 0094), not an artifact. The artifact
    # version was the first implementation and it was wrong twice over: artifact
    # identity is anchor+name+content_hash, so every edit appended a new row and a
    # project's artifact list filled with copies of one file; and reading a paragraph
    # cost three round trips (list -> presign -> R2 GET). The column rides along on
    # the project row, so an orienting caller gets the notes with NO extra request.

    def get_project_notes(self, project_id: str) -> str | None:
        """The project's notes, or None when nobody has written any.

        Note that `GET /v1/projects/{id}` already returns this, so a caller that
        holds the project row should read `row["notes"]` rather than call here --
        the point of the column is that the text costs no second request."""
        return self.get_project(project_id).get("notes")

    def _set_project_notes(self, project_id: str, text: str) -> str:
        """Replace the project's notes and return what the server actually stored.

        The read-back is not belt-and-braces. `ProjectPatch` does not forbid extra
        fields, so a backend PREDATING 0094 accepts `notes`, ignores it, and answers
        200 -- the write vanishes and the caller is told it succeeded. Returning the
        stored value makes that detectable instead of silent."""
        # sync=True: the read-back below is the only thing that catches a
        # backend which accepts the field, ignores it and answers 200. A
        # queued write skips that check entirely, so under async the guard
        # would never run. These are one-shot metadata writes, not loop
        # traffic, so paying the round trip costs nothing that matters.
        queued = self.write(
            "PATCH",
            f"/v1/projects/{project_id}",
            # force: this door replaces a whole document with no version in hand
            # (`probe notes write <file>`), and the server now REFUSES an
            # unguarded replace. Saying it explicitly is the honest spelling of
            # what this verb has always done; `probe notes checkout`/`push` is
            # the door that actually merges.
            {"notes": text, "force": True},
            sync=True,
            raise_permanent=True,
        )
        # scanning disabled: from .redaction import default_scrub

        # scanning disabled: expected = default_scrub(text)
        expected = text
        if queued is None:
            # Journaled (async mode) or fail-open-spooled: nothing reached the server,
            # so there is nothing to read back. Verifying here would report a failure
            # for a write that is simply still in the outbox.
            return expected
        stored = self.get_project(project_id).get("notes")
        if stored != expected:
            raise errors.RosError(
                "the server did not store the notes: this backend predates the "
                "projects.notes column (research-os 0094) and silently ignored the "
                "field. Upgrade the backend."
            )
        return stored

    def _write_notes(
        self, entity: str, entity_id: str, body: dict, *, strict: bool = False, sync: bool = False
    ) -> dict | None:
        """`strict=True` for an EDIT, and it is not a preference.

        The default write path is fail-open: a failed request is journaled and
        the drainer replays it. It is wrong for an edit, whose characteristic
        failure is a 409 saying `old_text` matched zero times or twice -- a
        permanent refusal the caller was told about. Journaling it would replay
        the refusal forever, or worse, land it later against a document where
        the text has since become unique, applying an edit the caller believes
        was rejected.

        An APPEND is fail-open but never queues a refusal, which is what
        `raise_permanent` means here. This used to say an append "fails only
        transiently" and that was false: a document at its cap refuses every
        further append with a 422 naming the cap, permanently. The
        SDK swallowed it, the CLI printed "appended to <kind> notes" and exited
        0, and the paragraph went to the outbox to be dead-lettered -- so an
        agent kept appending to a document that had stopped accepting anything,
        one silent success at a time, and read its own dead letters afterwards
        as a broken outbox. A network blip still queues, which is the case the
        fail-open path was built for.

        RETURNS the PATCH response so the caller can read the headroom the server
        published on it, or None when the write was journaled rather than sent --
        the same None ``Client.write`` already returns, meaning "no server has
        seen this yet", never "the document is fine".
        """
        # Every notes door, not just the append: `strict` already covers the
        # edit, and a PATCH the server refuses outright is never worth queueing
        # whichever field carried it.
        #
        # Spelled out per entity rather than through a {entity: segment} map, and
        # test_parity is why: it reads these call sites STATICALLY to prove every
        # path the client calls is one the backend declares. A computed path is
        # invisible to that check, which would take three real routes out of its
        # coverage and hand it one phantom `/v1/{route}` instead.
        # `sync` is SEPARATE from `strict` and not implied by it: strict decides
        # whether a refusal is journaled, sync decides whether the request is
        # made at all. A replace needs both -- under `async_writes` a journaled
        # replace drains later against a `base_version` that has since moved and
        # dead-letters, after the caller was told it shipped.
        kw = {"strict": strict, "raise_permanent": True, "sync": sync}
        if entity == "project":
            return self.write("PATCH", f"/v1/projects/{entity_id}", body, **kw)
        if entity == "experiment":
            # The experiment API's body is CLOSED and has no `op_key` (the leaf
            # door accepted and ignored it), so it is not sent there.
            experiment_body = {k: v for k, v in body.items() if k != "op_key"}
            return self._on_experiment(
                lambda p, e: self.write(
                    "PATCH", f"/v1/projects/{p}/experiments/{e}", experiment_body, **kw
                ),
                entity_id,
                journaled=self._journals(strict=strict, sync=sync),
            )
        if entity == "run":
            return self.write("PATCH", f"/v1/runs/{entity_id}", body, **kw)
        raise errors.RosError(
            f"{entity!r} carries no notes; expected one of {', '.join(self.NOTES_ENTITIES)}"
        )

    def _replace_notes(
        self,
        entity: str,
        entity_id: str,
        text: str,
        *,
        base_version: int | None,
        op_key: str,
    ) -> dict | None:
        """Replace an entity's whole note, pinned to the version it was read at.

        THE FILE-MODEL WRITE. `base_version` is the `notes_version` the document
        was checked out at; the server refuses with a 409 carrying the current
        version and NO body when the head has moved, and the caller re-reads
        through the READ door to merge. `None` is `--force`: replace whatever is
        there. `op_key` identifies a retry after a lost response as a replay --
        the server does not act on it yet (TODOS.md), so it is not yet a
        guarantee against a duplicate.

        strict=True, and not as a preference: a 409 here is a permanent refusal
        the caller was told about, and journaling it would replay that refusal
        forever -- or land it later against a document that has since moved
        again. See `_write_notes`.
        """
        body: dict = {"notes": text, "op_key": op_key}
        if base_version is None:
            # Say it out loud. An omitted `base_version` is exactly what the
            # server refuses, so a silent omission is not a force -- it is a 422.
            body["force"] = True
        else:
            body["base_version"] = base_version
        # sync=True, and NOT covered by strict: under `async_writes` the write
        # would be journaled without touching the network and return None, so
        # `push` would read version 0, commit a base at 0 and print "pushed",
        # while nothing had been sent. The queued replace would later drain
        # against a stale base_version and dead-letter -- the edit lost after
        # the caller was told it shipped.
        return self._write_notes(entity, entity_id, body, strict=True, sync=True)

    def list_sub_notes(self, entity: str, entity_id: str) -> dict:
        """Titles + fullness for an entity's sub-notes. NO bodies — the list
        is for choosing; `get_sub_note` is the document read."""
        if entity == "project":
            return self.transport.get(f"/v1/projects/{entity_id}/sub-notes")
        if entity == "experiment":
            return self._on_experiment(
                lambda p, e: self.transport.get(f"/v1/projects/{p}/experiments/{e}/sub-notes"),
                entity_id,
            )
        if entity == "run":
            return self.transport.get(f"/v1/runs/{entity_id}/sub-notes")
        raise errors.RosError(
            f"{entity!r} carries no sub-notes; expected one of {', '.join(self.NOTES_ENTITIES)}"
        )

    def get_sub_note(self, sub_note_id: str) -> dict:
        """One sub-note WITH its body and headroom (`tokens`, `limit_tokens`,
        `remaining_tokens`; `remaining_chars` / `limit_chars` are the character
        backstop's) — the write responses deliberately omit the body."""
        return self.transport.get(f"/v1/sub-notes/{sub_note_id}")

    def _create_sub_note(
        self, entity: str, entity_id: str, title: str, body: str = ""
    ) -> dict | None:
        """Create a titled sub-note. STRICT, never journaled — creation is not
        idempotent: titles are non-unique by design, so a create whose response
        was lost and then replayed is a second tab, not a retry, and the
        duplicate immediately makes every title-addressed write ambiguous.
        Refusals (blank title, the 20-per-entity cap) raise for the
        `_write_notes` reason: a refusal replayed later is the same no."""
        payload = {"title": title, "body": body}
        kw = {"strict": True, "raise_permanent": True}
        if entity == "project":
            return self.write("POST", f"/v1/projects/{entity_id}/sub-notes", payload, **kw)
        if entity == "experiment":
            return self._on_experiment(
                lambda p, e: self.write(
                    "POST", f"/v1/projects/{p}/experiments/{e}/sub-notes", payload, **kw
                ),
                entity_id,
            )
        if entity == "run":
            return self.write("POST", f"/v1/runs/{entity_id}/sub-notes", payload, **kw)
        raise errors.RosError(
            f"{entity!r} carries no sub-notes; expected one of {', '.join(self.NOTES_ENTITIES)}"
        )

    def _write_sub_note_by_title(
        self, entity: str, entity_id: str, body: dict, *, strict: bool = False
    ) -> dict | None:
        """The title-addressed write. `strict=True` for an edit — same contract,
        same reasoning, as `_write_notes`."""
        kw = {"strict": strict, "raise_permanent": True}
        if entity == "project":
            return self.write("PATCH", f"/v1/projects/{entity_id}/sub-notes", body, **kw)
        if entity == "experiment":
            return self._on_experiment(
                lambda p, e: self.write(
                    "PATCH", f"/v1/projects/{p}/experiments/{e}/sub-notes", body, **kw
                ),
                entity_id,
                journaled=self._journals(strict=strict),
            )
        if entity == "run":
            return self.write("PATCH", f"/v1/runs/{entity_id}/sub-notes", body, **kw)
        raise errors.RosError(
            f"{entity!r} carries no sub-notes; expected one of {', '.join(self.NOTES_ENTITIES)}"
        )

    def _replace_sub_note_by_title(
        self,
        entity: str,
        entity_id: str,
        title: str,
        text: str,
        *,
        base_version: int | None = None,
        op_key: str = "",
    ) -> dict | None:
        """Replace a sub-note's body addressed by TITLE, not id.

        The title travels IN the write and the server resolves it at apply time,
        exactly once or refused with the count. That resolution is the door's
        whole reason to exist: a client-side resolve-then-write cannot be replayed
        safely, and an ambiguous title must refuse rather than pick.

        Spelled out per entity for the same reason `_write_notes` is: test_parity
        reads these call sites statically, and a computed path is invisible to it.
        """
        body: dict = {"note_title": title, "body": text}
        if op_key:
            body["op_key"] = op_key
        if base_version is None:
            body["force"] = True
        else:
            body["base_version"] = base_version
        kw = {"strict": True, "sync": True, "raise_permanent": True}
        if entity == "project":
            return self.write("PATCH", f"/v1/projects/{entity_id}/sub-notes", body, **kw)
        if entity == "experiment":
            return self._on_experiment(
                lambda p, e: self.write(
                    "PATCH", f"/v1/projects/{p}/experiments/{e}/sub-notes", body, **kw
                ),
                entity_id,
            )
        if entity == "run":
            return self.write("PATCH", f"/v1/runs/{entity_id}/sub-notes", body, **kw)
        raise ValueError(f"unknown notes carrier: {entity}")

    def _replace_sub_note(
        self, sub_note_id: str, text: str, *, base_version: int | None, op_key: str
    ) -> dict | None:
        """Replace ONE sub-note's whole body, pinned to the version it was read at.

        Id-addressed, like rename and delete: the title-addressed door exists so
        a write can resolve at APPLY time and survive a queue, and this write
        never queues (strict=True -- a 409 is a permanent refusal the caller was
        told about). The CLI has already resolved the title through the list read.
        """
        body: dict = {"body": text, "op_key": op_key}
        if base_version is None:
            body["force"] = True
        else:
            body["base_version"] = base_version
        return self.write(
            "PATCH",
            f"/v1/sub-notes/{sub_note_id}",
            body,
            strict=True,
            sync=True,
            raise_permanent=True,
        )

    def _rename_sub_note(self, sub_note_id: str, title: str) -> dict | None:
        return self.write(
            "PATCH",
            f"/v1/sub-notes/{sub_note_id}",
            {"title": title},
            strict=True,
            raise_permanent=True,
        )

    def _delete_sub_note(self, sub_note_id: str) -> None:
        """Hard delete; the sub-note's history cascades with it. Direct, never
        journaled — a delete is confirmed interactively and must not land
        later against a tab someone kept using."""
        self.transport.delete(f"/v1/sub-notes/{sub_note_id}")

    def list_notes(
        self,
        *,
        query: str | None = None,
        cursor: str | None = None,
        limit: int = 100,
        include_sub_notes: bool = False,
    ) -> dict:
        """One page of the tenant-wide notes catalog: `{items, next_cursor}`.

        The DISCOVERY read, and the only one that answers a question no
        per-entity read can: which documents across the tenant are close to their
        cap. Every row carries `tokens` and `limit_tokens` (the cap, in o200k_base
        tokens; `tokens` is null for a document the server has not counted yet)
        beside `chars` / `limit_chars` (the character backstop), so a sweep is one
        page of this instead of one fetch per entity -- sizing 52 documents used to
        cost 52 API calls, which is why nobody did it and why
        `assignment-modeling` sat refused at 99,992 of its then 100,000-character
        cap for a day.

        Rows are bounded by construction: an `excerpt` capped at 280 characters,
        never a body. `query` searches note bodies, titles and project /
        experiment / run ancestor titles LITERALLY (not wildcards).

        `limit` IS LOAD-BEARING, not a tuning knob. A bare `GET /v1/notes` with
        no query, cursor or limit returns the dashboard's lazy tree -- ROOT
        branches only, with children fetched per expansion -- so a sweep made
        without one would silently see only top-level documents and report
        "nothing is near full" about everything nested beneath them. Passing a
        limit selects the flat, keyset-paged listing, which is the one that
        walks every carrier in the tenant.

        This route was on `test_parity`'s permanent NOT_CLIENT_SURFACE list, with
        the reason "agents read and edit a known note through its owning entity".
        That reason held while the row carried no length -- the catalog told a
        client nothing it could not get from the entity. The sizes made it
        false, so the entry is gone rather than reworded.
        """
        params: dict[str, object] = {"limit": limit}
        if query is not None:
            params["query"] = query
        if cursor is not None:
            params["cursor"] = cursor
        if include_sub_notes:
            # Opt-in (0146): sub-note rows join the flat listing and the search
            # results. A server that predates the flag drops the unknown param
            # and answers the pre-0146 shape — degraded to the old sweep, never
            # an error.
            params["include_sub_notes"] = "true"
        return self.transport.get("/v1/notes", params=params)

    # ---------------------------------------------------------------- team note

    def get_team_note(self) -> dict:
        """The team's shared document: `{body, version, updated_at, updated_by,
        tokens, limit_tokens, remaining_tokens, remaining_chars}` (the cap is in
        tokens; `remaining_chars` is the character backstop's room). Never 404s --
        a team that has written nothing has an empty document at version 0.

        THE SYNC CLIENT USUALLY DOES NOT CALL THIS. `get_team_note_brief` already
        carries `version` AND `truncated`, so a brief that is not truncated IS
        the whole document -- which is the case for any note under
        BRIEF_MAX_CHARS. The file seed costs one request in the common case and
        falls back here only for a document large enough to be sliced.
        """
        return self.transport.get("/v1/team-note")

    def get_team_note_brief(self) -> dict:
        """The bounded slice a session is briefed with: `{text, truncated,
        version}`. What the SessionStart hook injects, and cheap enough to ask
        for mid-session when you want the current briefing without the document."""
        return self.transport.get("/v1/team-note/brief")

    def sync_team_note(self, body: str, *, base_version: int) -> dict:
        """THE AGENT WRITE: the whole document, plus the version it was edited from.

        Agents do not compose operations against this document any more. A
        session-start hook seeds a local markdown file, the agent edits it like
        any other file, and the session-stop reconcile sends the result here with
        the version it started from. The server merges against that base, so a
        teammate writing while this session worked is an ordinary merge rather
        than a refusal -- and two sides that both only ADDED text both land,
        which is the property the old `append` guaranteed.

        Returns `{state, version, tokens, limit_tokens, remaining_tokens,
        remaining_chars, body?, merged}`. `state` is
        `applied` or `unchanged`; `unchanged` is what a retried reconcile gets
        and mints no version. When `merged` is true the server combined this
        document with someone else's and `body` is the result, which the caller
        must write back to its file so the next base comparison stays honest.

        A 409 carries the merged document WITH conflict markers under
        `merged_body`: write it to the file, resolve, sync again. A 422 names the
        marker lines when the document still has unresolved ones.
        """
        # strict: a 409 here is a REFUSAL carrying a document to act on, not a
        # transient failure to retry blindly.
        # sync=True: the reconcile needs the RESPONSE in hand (the new version,
        # and the merged body when the server combined two edits). Journaling
        # this write for later delivery would hand back None and leave the local
        # base copy pointing at a version that never existed.
        return self.write(
            "POST",
            "/v1/team-note/sync",
            {"body": body, "base_version": base_version},
            strict=True,
            sync=True,
        )

    def append_team_note(self, text: str) -> dict:
        """Add a paragraph at the end of the team note, merged by the SERVER.

        For a caller with no team-note file: the server reads, appends after a
        blank line and stores under its own row lock, so nothing a teammate
        wrote is lost and no version is needed. A caller that HAS the file
        edits it and syncs (`sync_team_note`) instead.

        Returns `{state, version, tokens, limit_tokens, remaining_tokens,
        remaining_chars}`. A 422 names the cap (in tokens) or the
        conflict-marker lines; a 409 carrying `retryable: true` means another
        write landed at the same moment and nothing was stored.
        """
        # strict + sync: never journaled. A refusal replayed later is the same
        # refusal, and a queued write would hand back None instead of the
        # version the caller reports.
        return self.write(
            "POST",
            "/v1/team-note/apply/paragraph",
            {"text": text},
            strict=True,
            sync=True,
            raise_permanent=True,
        )

    def edit_team_note(self, old_text: str, new_text: str) -> dict:
        """Replace one exact piece of the team note, matched by the SERVER.

        `old_text` must occur exactly once; otherwise nothing is written and the
        409's detail carries `match_count`. `new_text=""` deletes it. Same
        return shape and other refusals as `append_team_note`.
        """
        return self.write(
            "POST",
            "/v1/team-note/apply/span",
            {"old_text": old_text, "new_text": new_text},
            strict=True,
            sync=True,
            raise_permanent=True,
        )

    def list_team_note_versions(
        self, *, limit: int | None = None, before: int | None = None
    ) -> dict:
        """History, newest first, WITHOUT bodies (a page of full documents is a
        megabyte). Each row is `{version, created_at, created_by, size_chars}`.

        `before` walks backwards: pass the response's `next_before` to get the
        next page, and stop when it comes back None. History is retained to the
        server's last N versions, so the walk ends at the oldest kept version
        rather than at version 1.
        """
        params = {k: v for k, v in (("limit", limit), ("before", before)) if v is not None}
        return self.transport.get("/v1/team-note/versions", params=params or None)

    def get_team_note_version(self, version: int) -> dict:
        """One past body, so you can see what you are about to restore."""
        return self.transport.get(f"/v1/team-note/versions/{version}")

    def restore_team_note_version(self, version: int) -> dict:
        """Make a past version current again, as a NEW version.

        A restore is an ordinary write, not a rewind: it takes the next version
        number and is itself recorded, so undoing an undo is possible and the
        history never loses the versions being stepped over.
        """
        return self.write("POST", f"/v1/team-note/versions/{version}/restore", {}, strict=True)


class NotesResource(Resource):
    """`client.notes`: typed reads of the notes catalog, sub-notes and the team note."""

    __slots__ = ()

    def list(
        self, *, query: str | None = None, cursor: str | None = None, limit: int = 100,
        include_sub_notes: bool = False,
    ) -> NoteCatalogOut:
        """`Client.list_notes` as a `NoteCatalogOut`."""
        return self._to_model(
            NoteCatalogOut,
            self._client.list_notes(
                query=query, cursor=cursor, limit=limit, include_sub_notes=include_sub_notes,
            ),
        )

    def list_sub_notes(self, entity: str, entity_id: str) -> SubNoteListOut:
        """`Client.list_sub_notes` as a `SubNoteListOut`."""
        return self._to_model(SubNoteListOut, self._client.list_sub_notes(entity, entity_id))

    def get_sub_note(self, sub_note_id: str) -> SubNoteOut:
        """`Client.get_sub_note` as a `SubNoteOut`."""
        return self._to_model(SubNoteOut, self._client.get_sub_note(sub_note_id))

    def get_team_note(self) -> TeamNoteOut:
        """`Client.get_team_note` as a `TeamNoteOut`."""
        return self._to_model(TeamNoteOut, self._client.get_team_note())

    def get_team_note_brief(self) -> TeamNoteBriefOut:
        """`Client.get_team_note_brief` as a `TeamNoteBriefOut`."""
        return self._to_model(TeamNoteBriefOut, self._client.get_team_note_brief())

    def list_team_note_versions(
        self, *, limit: int | None = None, before: int | None = None,
    ) -> TeamNoteVersionsOut:
        """`Client.list_team_note_versions` as a `TeamNoteVersionsOut`."""
        return self._to_model(
            TeamNoteVersionsOut,
            self._client.list_team_note_versions(limit=limit, before=before),
        )

    def get_team_note_version(self, version: int) -> TeamNoteOut:
        """`Client.get_team_note_version` as a `TeamNoteOut`."""
        return self._to_model(TeamNoteOut, self._client.get_team_note_version(version))
