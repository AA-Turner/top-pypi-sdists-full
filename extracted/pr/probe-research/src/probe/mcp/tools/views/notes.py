"""notes views: the project card with its notes, full notes with titled sub-notes, the team note."""

from __future__ import annotations
from ....sdk import errors
from ....sdk.reads.notes_cap import read_advisory
from ....shared.reads.search_contract import EntityType
from ...delivery.context import current_delivery, pin_document
from probe.mcp.tools.shaping.cards import _notes_excerpt
from probe.mcp.tools.view import _Req, _ViewData

#: Card cap: the card is the cheap glance, and `token_budget` bounds ROWS,
#: not payload -- so each block caps itself.
_MAX_CARD_CONTRIBUTORS = 8

#: Per-sub-note excerpt inside `view="notes"` (0146). Twenty of these is a
#: bounded ~14k characters — a section, never a context bomb.
_SUB_NOTE_VIEW_EXCERPT = 700


#: How many peer slugs the project CARD lists per direction. The card is an
#: orientation read, so it names a few and states the count; `view="card"` is
#: not where a 200-edge graph gets enumerated.
_CARD_REFERENCE_SLUGS = 10


def _card_part_of(payload: dict, entity: dict) -> None:
    """`part_of` (what this project is a part of: its outgoing `part_of_links`)
    and `parts` (the projects that are a part of it: incoming), each only when
    it has any. Capped like the references; the count stays exact."""
    links = entity.get("part_of_links") or []
    for key, direction in (("part_of", "outgoing"), ("parts", "incoming")):
        rows = [
            {"id": link.get("project_id"), "name": link.get("project_name") or link.get("project_slug")}
            for link in links
            if link.get("direction") == direction
        ]
        if not rows:
            continue
        block: dict = {"projects": rows[:_CARD_REFERENCE_SLUGS]}
        if len(rows) > _CARD_REFERENCE_SLUGS:
            block["count"] = len(rows)
        payload[key] = block
    if entity.get("part_of_links_truncated"):
        payload["part_of_links_truncated"] = True


class NotesViewsMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    def _view_project_card(self, entity: dict, request: _Req) -> _ViewData:
        """The project card, carrying the project's notes.

        Read straight off the entity, which `source.get` already fetched: since
        research-os 0094 the notes are a COLUMN on the project row, so this costs no
        request at all. That is what makes putting them on the card affordable --
        orientation is `browse_research` then a card, and a briefing an agent has to
        KNOW to ask for is one it does not read. Bounded to an excerpt so a long
        document cannot blow the token budget of what is supposed to be the cheap
        glance; `view="notes"` has the rest.
        """
        payload: dict = {}
        excerpt = _notes_excerpt(entity.get("notes"))
        if excerpt is not None:
            payload["notes"] = excerpt
        # 0134: the connection fact, off the already-fetched detail row (the
        # backend puts code_sources on the project read), so it costs nothing.
        sources = entity.get("code_sources") or []
        if sources:
            active = [s for s in sources if s.get("status") == "active"]
            suggested = sum(1 for s in sources if s.get("status") == "suggested")
            code: dict = {
                "repos": [f"{s['repo']}@{s['ref']}" for s in active[:5]],
                # Non-revoked, matching every backend code_source_count surface
                # (a revoked source is history, not a live connection).
                "count": sum(1 for s in sources if s.get("status") != "revoked"),
                "read_history": 'view="code"',
            }
            if suggested:
                code["suggested"] = suggested
            payload["code"] = code
        # 0159: who worked on this, off the already-fetched detail row, so it
        # costs no request. NAMES, because a uuid answers nobody's question.
        # `via` names the project the work was done in when it was not this
        # one; its absence means they worked here.
        contributors = entity.get("contributors") or []
        if contributors:
            payload["contributors"] = [
                {
                    "name": c.get("name") or c.get("email") or c.get("user_id"),
                    **({} if c.get("direct", True) else {"via": c.get("via_project_id")}),
                }
                for c in contributors[:_MAX_CARD_CONTRIBUTORS]
            ]
            if len(contributors) > _MAX_CARD_CONTRIBUTORS:
                payload["contributors_truncated"] = len(contributors)
        # 0153: lateral peer edges, both directions, off the already-fetched
        # detail row. On the CARD rather than behind a view for the same reason
        # `code` is: a relationship an agent has to know to ask about is one it
        # never sees, and a lit review's whole point is being reachable from
        # the work it informed.
        references = entity.get("references") or []
        if references:
            # FLAT keys, matching what the tool description advertises. Nesting
            # them under `references` made an agent looking for
            # `referenced_by` find nothing and read that as "no incoming
            # links" — a confident wrong answer about the exact relation this
            # exists to surface.
            #
            # CAPPED per direction, like the `code` block above. The card is
            # the cheap glance, and `token_budget` bounds ROWS, not payload —
            # so an uncapped list here (up to MAX_PROJECT_REFERENCES per
            # direction) would blow the default budget on a heavily-referenced
            # project and degrade the one read meant to be cheapest. The
            # counts stay exact so the excerpt never reads as the whole set.
            for key, direction in (
                ("references", "outgoing"),
                ("referenced_by", "incoming"),
            ):
                slugs = [r["project_slug"] for r in references if r.get("direction") == direction]
                if not slugs:
                    continue
                block: dict = {"projects": slugs[:_CARD_REFERENCE_SLUGS]}
                if len(slugs) > _CARD_REFERENCE_SLUGS:
                    block["count"] = len(slugs)
                payload[key] = block
            if entity.get("references_truncated"):
                payload["references_truncated"] = True
        # 0401: projects are flat, and a phase of a bigger effort is its own
        # project linked `part_of` it. The detail read serves those links
        # apart from `references` (`part_of_links`). One hop each way, NAMES
        # AND IDS: a recorder writing the page of a bigger effort reads its
        # parts from here (`entity` on each id), and a part's page names the
        # effort it belongs to.
        _card_part_of(payload, entity)
        return _ViewData(payload=payload) if payload else _ViewData()

    def _view_project_notes(self, entity: dict, request: _Req) -> _ViewData:
        """The project's notes in full. No schema: free-text markdown that agents
        read and write, not a record type. The MAIN note is off the
        already-fetched row; the sub-notes section (0146) is fetched here."""
        return self._notes_with_sub_notes(entity, "project")

    def _view_run_notes(self, entity: dict, request: _Req) -> _ViewData:
        """A run's notes in full (0124) + its titled sub-notes (0146)."""
        return self._notes_with_sub_notes(entity, "run")

    def _view_experiment_notes(self, entity: dict, request: _Req) -> _ViewData:
        """An experiment's notes in full (0124) + its titled sub-notes (0146)."""
        return self._notes_with_sub_notes(entity, "experiment")

    def _notes_with_sub_notes(self, entity: dict, kind: str) -> _ViewData:
        """The full-notes view: the MAIN document off the already-fetched row,
        plus each titled SUB-NOTE (0146) as a bounded excerpt.

        Excerpts, not full bodies, and the bound is deliberate: twenty 100k
        documents inside one tool result is a context bomb, and the view's job
        is surfacing that a caveat EXISTS and what it starts with. `read_all`
        names the doors that hold the whole document. Cards stay untouched —
        a titles line there would be an N+1 on the cheapest read.

        ABSENT on any failure, never invented: a backend without 0146 (or a
        transient error) yields no `sub_notes` key at all, exactly like an
        entity that has none — the headroom rule's "absent means the response
        did not carry it" applied one level up.
        """
        body, version = entity.get("notes"), entity.get("notes_version")
        if current_delivery() is not None:
            if hasattr(self.source, "notes_document") and entity.get("id"):
                body, version = self.source.notes_document(kind, entity)
            else:
                pinned = pin_document(
                    body or "", f"notes:{kind}:{entity.get('id')}", version=version
                )
                body = None if body is None and not pinned else pinned
        payload: dict = {"notes": body}
        if version is not None:
            payload["notes_version"] = version
        # THE REMINDER TRAVELS WITH THE DOCUMENT. A skill file read once at load
        # does not reach the model forty minutes later holding the note that
        # contradicts it -- measured 2026-09-08, when an agent found six claims
        # this repository disproved and corrected none of them. Derived from the
        # headroom the server already publishes, so it is silent rather than
        # invented when the response did not carry the document.
        # Only where there IS a document. `notes_headroom` publishes the full cap
        # for a NULL `notes`, and the notes view is offered on every entity, so
        # without this a run that never had a note answers "0% full — correct
        # what your evidence contradicts", which is advice about nothing.
        advisory = read_advisory(entity, version=version) if body else None
        if advisory is not None:
            payload["notes_advisory"] = advisory
        entity_id = entity.get("id") if isinstance(entity, dict) else None
        if entity_id:
            try:
                page = self.source.client.list_sub_notes(kind, str(entity_id))
            except errors.RosError:
                page = None
            rows = (page or {}).get("sub_notes") or []
            section = []
            for row in rows:
                item: dict = {"title": row.get("title")}
                # Fullness in tokens, the unit the cap refuses in; an uncounted
                # sub-note (null) says nothing rather than a guess.
                for key in ("tokens", "limit_tokens"):
                    if row.get(key) is not None:
                        item[key] = row[key]
                if row.get("id"):
                    # The address of the WHOLE sub-note: the excerpt below is
                    # bounded, and `entity` on this reads the rest.
                    item["uuid"] = f"{EntityType.SUB_NOTE.value}:{row['id']}"
                try:
                    body = self.source.client.get_sub_note(str(row["id"])).get("body") or ""
                except errors.RosError:
                    # A failed body read must not render as an EMPTY sub-note —
                    # "this caveat tab is blank" is a conclusion, and an outage
                    # must not draw it. Say unavailable instead.
                    item["unavailable"] = True
                    body = ""
                if body:
                    item["excerpt"] = body[:_SUB_NOTE_VIEW_EXCERPT]
                    if len(body) > _SUB_NOTE_VIEW_EXCERPT:
                        item["truncated"] = True
                        item["read_all"] = (
                            "entity(refs=[uuid])"
                            if "uuid" in item
                            else "the entity page's Notes tab, or `probe notes show --note <title>`"
                        )
                section.append(item)
            if section:
                payload["sub_notes"] = section
        return _ViewData(payload=payload)

    def _view_card_with_notes(self, entity: dict, request: _Req) -> _ViewData:
        """The generic card, plus a bounded notes excerpt (0124).

        Runs and experiments carry notes now, and the argument that put
        them on the PROJECT card applies unchanged: orientation is
        `browse_research` then a card, and a caveat an agent has to know to ask
        for is one it does not read. A run whose note says "the scorer was stale,
        distrust these numbers" must reach a reader who only glanced at it.
        """
        excerpt = _notes_excerpt(entity.get("notes"))
        return _ViewData() if excerpt is None else _ViewData(payload={"notes": excerpt})

    def _view_sub_note_card(self, entity: dict, request: _Req) -> _ViewData:
        """One sub-note, WHOLE -- its card is the document, as the team note's
        is. Pinned so a paged read cannot splice two versions together."""
        if current_delivery() is not None:
            entity["body"] = pin_document(
                entity.get("body") or "", f"{EntityType.SUB_NOTE.value}:{entity.get('id')}"
            )
        if entity.get("body"):
            return _ViewData()
        return _ViewData(payload={"state": "empty"})

    def _view_team_note_card(self, entity: dict, request: _Req) -> _ViewData:
        """The team note, WHOLE -- see its `_VIEWS` entry for why a card is the
        document here rather than a glance.

        The empty case gets words, deliberately: an
        agent reading a blank `body` cannot tell "this team has written nothing
        down" from "the read gave me nothing", and version 0 says which only to a
        reader who knows 0 is the sentinel. The explicit empty state conveys
        that distinction without repeating write instructions in read data.
        """
        if current_delivery() is not None:
            entity["body"] = pin_document(
                entity.get("body") or "", "team-note", version=entity.get("version")
            )
        if entity.get("body"):
            return _ViewData()
        return _ViewData(payload={"state": "empty"})
