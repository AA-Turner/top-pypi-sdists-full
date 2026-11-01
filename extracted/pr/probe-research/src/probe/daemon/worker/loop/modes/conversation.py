"""conversation mode: the next user message of the session's one conversation, lean history, fresh starts after compactions."""

from __future__ import annotations
import asyncio
import dataclasses
import hashlib
import json
import os
from pathlib import Path
from probe.daemon.worker.bite import bite as bite_mod
from probe.daemon.agent import tools
from probe.daemon.agent.model import model as model_mod
from probe.daemon.store.logbook import CARRY_ON
#: The runs a writer message names are read in the daemon host before it is sent
#: (`_read_runs`, swarm friction T18), all at once, for at most this long; a read
#: still going then is left out of the message.
RUN_READ_TIMEOUT_S = 10.0
#: Lean history (daemon cost round 5): the last logbook write id a saved run's
#: "writes since" list showed (only ever moves forward), whether the writes after it
#: are still owed to a list (a lean save stripped their calls), and how many lines
#: one list shows at most.
LEAN_WRITES_MARK = "lean_writes_mark"
LEAN_WRITES_OWED = "lean_writes_owed"
LEAN_WRITES_SHOWN = 120
#: Lean history: {"conversation", "compactions"} the last lean run saw (a
#: compaction since, in that conversation, breaks the cached prefix once: D13).
LEAN_COMPACTIONS_SEEN = "lean_compactions_seen"
#: "<conversation id>:<compactions>" the agent memory index was last shown after.
INDEX_AFTER_COMPACTION = "index_after_compaction"
#: The summaries the writer keeps (ARTIFACT-PAGES P3, replacing the §3.5 pin
#: of one summary's whole text): before each run the worker checks out every
#: project and experiment the session wrote to or created (`tools.
#: autoload_summaries`, at most `tools.SUMMARY_DRAFTS_KEPT`), and the next
#: message starts with their OUTLINES (`tools.summary_outline`) -- where each
#: draft is, its headings, its opening, what happened since -- never their
#: text: the writer `read`s a part and `edit`s it in place. Shown once per
#: change (the header names the outline's digest), never a per-request tail.
#: Conversation mode: after this many compactions the next bite starts fresh from disk.
COMPACTIONS_BEFORE_FRESH = 8
#: Conversation mode (daemon cost round 7, F2): a conversation idle longer than
#: `model.writer_cold_fresh_s` resumes at the full price (the model's prompt cache
#: lives ~30 minutes: 5-7% of calls 10-30 min after the last were cold, 96% at
#: 30-60 min, strand-ai 20-23 Oct), so the next run starts fresh from disk instead
#: -- unless its saved history is under this many estimated tokens, which a fresh
#: start (median ~60K) would not undercut.
FRESH_FLOOR_TOKENS = 80_000


class ConversationMixin:
    """Part of Worker: its methods run with `self` the Worker; compose() folds them into Worker."""

    # -- conversation mode (T15) ----------------------------------------------
    def _next_in_conversation(self, trigger: str, shrink: tuple[int, int] | None, *,
                              events_text: str | None = None, span: tuple[int, int] | None = None):
        """`(conversation id, saved history, the bite)`: the next user message of
        the live conversation, or -- no usable saved history -- a fresh start
        from disk (today's bite) that opens one. `(None, None, None)` when nothing
        is pending. `events_text`: the new events of `span` as the writer reads them,
        when indexed (`WriterEvents.INDEX`); a fresh start shows them raw."""
        from pydantic_ai.messages import ModelMessagesTypeAdapter

        live = self.store.live_conversation()
        fingerprint = self._fingerprint()
        if live is not None and live["messages"] and live["fingerprint"] != fingerprint:
            log.info("conversation %s was made by another session, job description, model or Pydantic AI version: "
                     "a fresh start from disk", live["id"])
            with self.store.tx():
                self._end_resumed(live["id"], "its fingerprint no longer matches (the session, the job "
                                              "description, the model or the Pydantic AI version changed)")
            live = None
        if live is not None and live["messages"]:
            idle = self._cold_idle_s(live)
            if idle is not None:
                log.info("conversation %s: idle %d min, its cached prompt is gone: a fresh start from disk",
                         live["id"], idle // 60)
                with self.store.tx():
                    self._end_resumed(live["id"], f"idle {idle // 60} min: the model's prompt cache is gone, so a "
                                                  "fresh start from disk costs less than re-reading it")
                self._fresh_why = "cold"
                live = None
        if live is not None and live["messages"]:
            try:
                history = ModelMessagesTypeAdapter.validate_json(live["messages"])
            except Exception as exc:  # noqa: BLE001 -- a history that cannot be read is replaced, never fatal
                log.warning("conversation %s: its saved history could not be read (%s): a fresh start from disk",
                            live["id"], type(exc).__name__)
                with self.store.tx():
                    self._end_resumed(live["id"], f"its saved history could not be read ({type(exc).__name__})")
                live, history = None, None
            if history:
                built = bite_mod.build_next(self.store, trigger=trigger, instructions=live["instructions"],
                                            shrink=shrink, carry_on=bool(self.store.fact(CARRY_ON)),
                                            events_text=events_text, span=span)
                if built is None:
                    return None, None, None
                if (model_mod.writer_history() == model_mod.WriterHistory.LEAN
                        or self.store.fact(LEAN_WRITES_OWED)):
                    # Lean history keeps no tool traffic: the writes it made are listed instead,
                    # in this message, once -- never rebuilt, so later requests extend it. Also
                    # the first run after a switch back to full: the stripped history still
                    # holds none of the lean runs' writes (review, Codex High).
                    block, built.writes_mark = self._writes_since()
                    built.prompt = f"{block}\n\n{built.prompt}"
                outline = self._summary_outline(history)
                skills = self._page_skills(history)
                if skills:
                    built.prompt = f"{skills}\n\n{built.prompt}"
                if outline:
                    built.prompt = f"{outline}\n\n{built.prompt}"
                mark = f"{live['id']}:{live['compactions']}"
                if live["compactions"] and self.store.fact(INDEX_AFTER_COMPACTION) != mark:
                    # A compaction summarised the first message away, and the agent memory
                    # index with it: the first message after one carries it again (the
                    # history was rewritten, so this costs no cached prefix).
                    index = self.memory_block()
                    if index:
                        built.prompt = f"{index}\n\n{built.prompt}"
                    self.store.set_fact(INDEX_AFTER_COMPACTION, mark)
                return live["id"], history, built
        # No history to carry on: a paused run's remaining work is the fresh start's.
        self.store.set_fact(CARRY_ON, None)
        built = bite_mod.build(self.store, trigger=trigger, context_line=self.context_line(),
                               pending_lines=self.pending_lines(), recent_writes=self.recent_writes(), shrink=shrink,
                               memory=self.memory_block())
        if built is None:
            return None, None, None
        outline = self._summary_outline(None)
        skills = self._page_skills(None)
        if skills:
            built.prompt = f"{skills}\n\n{built.prompt}"
        if outline:  # a fresh start from disk shows no earlier outline: it rides its first message
            built.prompt = f"{outline}\n\n{built.prompt}"
        if live is not None:  # opened, but its first run never finished: open it again with today's facts
            self.store.set_conversation_instructions(live["id"], built.instructions, fingerprint)
            return live["id"], None, built
        return self.store.start_conversation(built.instructions, fingerprint), None, built

    def _summary_outline(self, history) -> str:
        """The outlines of the summaries the writer keeps (`tools.summary_outline`)
        under their header, when the conversation does not show this exact
        outline already (its header names its digest): once per change, never a
        per-request tail (append-only). "" with nothing kept."""
        block = tools.summary_outline(self.store)
        if not block:
            return ""
        header = tools.outline_header(block)
        if history and _shows_text(history, header):
            return ""
        return f"{header}\n\n{block}"

    def _page_skills(self, history) -> str:
        """The page skills whole (`bite.PAGE_SKILLS`), once per conversation
        (again after a compaction summarised them away, or when a CLI update
        changed them): its header names their digest. Not gated on a kept
        page: a run that creates an experiment writes its first page in that
        same run, before any draft exists to key on. "" with no skills found."""
        text = bite_mod.skills_text(bite_mod.PAGE_SKILLS)
        if not text:
            return ""
        header = bite_mod.PAGE_SKILLS_HEADER.format(digest=hashlib.sha256(text.encode("utf-8")).hexdigest()[:8])
        if history and _shows_text(history, header):
            return ""
        return f"{header}\n\n{text}"

    async def _autoload_summaries(self, workdirs: list[Path] | None) -> None:
        """Before a writer run: check out what the session touched
        (`tools.autoload_summaries`). Never while Probe refuses the key."""
        if self.probe_refused_key:
            return
        await tools.autoload_summaries(self.deps(None, workdirs))

    async def _read_runs(self, built: bite_mod.Bite, deps: tools.Deps) -> int:
        """The runs the message names (`Bite.runs`), read in the daemon host at
        once and appended to it as one block (`bite.runs_block`, swarm friction
        T18): what the writer spent a model round on `probe run get` for. Only
        appended, so whatever came before it (the conversation, its cached
        prefix) is unchanged. A read that fails, is still going after
        RUN_READ_TIMEOUT_S (or the session-end deadline) or answers another run
        is left out, unsaid. How many it shows."""
        if not built.runs:
            return 0
        timeout = RUN_READ_TIMEOUT_S
        if self.finish_by is not None:
            timeout = min(timeout, self.finish_by - self.clock())
        if timeout <= 0:
            return 0
        seed = f"{self.session.session_id}:{built.first_seq}:run get"

        async def read(run: str) -> dict | None:
            try:
                answer = await asyncio.wait_for(tools.read_in_host(deps, ["run", "get", run], f"{seed}:{run}", timeout),
                                                timeout + 1)
                return _run_record(run, answer)
            except Exception as exc:  # noqa: BLE001 -- a read the message goes without
                log.warning("run %s not read for the writer: %s", run, type(exc).__name__)
                return None

        runs = [record for record in await asyncio.gather(*(read(run) for run in built.runs)) if record is not None]
        block = bite_mod.runs_block(runs)
        if block:
            built.prompt = f"{built.prompt}\n\n{block}"
        return len(runs)

    def _fingerprint(self) -> str:
        """What a saved conversation is bound to: this session's id (a store reached
        under another id is not this session's), the job description this CLI ships
        with the researcher's skills in it, the model's name and the Pydantic AI version (the history's format). A
        resume that finds another fingerprint starts fresh from disk."""
        import pydantic_ai

        from probe.daemon.agent.model import model as model_mod

        name = (getattr(self._model, "model_name", type(self._model).__name__) if self._model is not None
                else os.environ.get(model_mod.ENV_MODEL) or "default")
        job = hashlib.sha256(bite_mod.instructions_for("").encode("utf-8")).hexdigest()
        return hashlib.sha256("\n".join([self.session.session_id, job, str(name),
                                         pydantic_ai.__version__]).encode("utf-8")).hexdigest()

    async def _index_new_events(self, shrink: tuple[int, int] | None):
        """`WriterEvents.INDEX`: the next message's new events, indexed
        (`index.index_events`) -- only for a live conversation's next message; a
        fresh start from disk shows its window raw. None otherwise."""
        if model_mod.writer_events() != model_mod.WriterEvents.INDEX or self.probe_refused_key:
            return None  # refused: the run would stop before the model; never pay to index for it
        live = self.store.live_conversation()
        if live is None or not live["messages"]:
            return None
        span = bite_mod.cover(self.store, shrink)
        if span is None:
            return None
        from probe.daemon.lanes import index as index_mod

        if self._index_model is None:
            self._index_model = model_mod.build(model_mod.endpoint(), model_mod.LANE_INDEX, retries=0)
        events = self.store.events_between(span[0], span[1], recorded=True, new=True, uncovered=True)
        # Bounded (`index.INDEX_TIMEOUT_S` per call, `index.CONCURRENT_CALLS` at once): well
        # inside the writer's lease, so no renewal is needed while it runs.
        indexed = await index_mod.index_events(self._index_model, events)
        indexed.span = span  # the message covers exactly these: never events it did not show
        return indexed

    def _settle_writes_list(self, built: bite_mod.Bite, *, lean: bool, paused: bool = False) -> None:
        """A run with a "writes since" list was saved: the mark moves to what it
        listed. A COMPLETED lean run owes its writes to the next list (their calls
        are stripped); a completed full run owes nothing (its calls stay in its
        history); a paused run leaves what is owed as it was."""
        if built.writes_mark is None:
            return
        self.store.set_fact(LEAN_WRITES_MARK, built.writes_mark)
        if not paused:
            self.store.set_fact(LEAN_WRITES_OWED, bool(lean))

    def _writes_since(self) -> tuple[str, int]:
        """Lean history: the writes logged since the last completed run's list (all
        of the session's, on the first lean run), oldest first; and the last id."""
        mark = int(self.store.fact(LEAN_WRITES_MARK) or 0)
        rows = [r for r in reversed(self.store.recent_writes(10_000)) if int(r["id"]) > mark]
        last = max([mark] + [int(r["id"]) for r in rows])
        older = max(0, len(rows) - LEAN_WRITES_SHOWN)
        lines = [f"- {r['status']}: {' '.join(json.loads(r['argv']))[:240]}" for r in rows[older:]]
        head = f"({older} older: `session` op=logbook)\n" if older else ""
        return (f"# Your writes since your last run\n{head}" + ("\n".join(lines) or "- none")), last

    def _cold_idle_s(self, live) -> int | None:
        """How long, in whole seconds, the live conversation `live` has sat idle when
        that is past `model.writer_cold_fresh_s` and its saved history is at least
        FRESH_FLOOR_TOKENS (estimated from its stored JSON, which overstates it a
        little); else None (resume it)."""
        from probe.daemon.agent.model import model as model_mod

        limit = model_mod.writer_cold_fresh_s()
        if limit <= 0:
            return None
        last = live["updated"] if live["updated"] is not None else live["started"]
        if last is None:
            return None
        idle = self.clock() - float(last)
        size = (len(live["messages"] or "") + len(live["instructions"] or "")) // bite_mod.CHARS_PER_TOKEN
        if idle <= limit or size < FRESH_FLOOR_TOKENS:
            return None
        return int(idle)

    def _maybe_start_fresh(self, conversation: int) -> None:
        """After COMPACTIONS_BEFORE_FRESH compactions a summary of summaries has
        drifted far enough: the next bite starts fresh from disk."""
        row = self.store.db.execute("SELECT compactions FROM conversations WHERE id = ?", (conversation,)).fetchone()
        if row is not None and int(row["compactions"]) >= COMPACTIONS_BEFORE_FRESH:
            log.info("conversation %s: %s compactions, the next bite starts fresh from disk", conversation,
                     row["compactions"])
            self.store.end_conversation(conversation, f"{row['compactions']} compactions: a fresh start from disk")


def _lean(messages) -> list:
    """`WriterHistory.LEAN` (daemon cost round 5): the messages the writer was sent
    -- its user prompts, and a compaction's summary (a system part) -- with its own
    answers and tool traffic dropped. Each kept message is byte-identical to the
    one sent, so the next run's request extends this run's first one: the only
    prefix the model's prompt cache serves (measured 10-13, D3)."""
    from pydantic_ai.messages import ModelRequest, SystemPromptPart, UserPromptPart

    out = []
    for message in messages:
        if not isinstance(message, ModelRequest):
            continue
        parts = [p for p in message.parts if isinstance(p, (SystemPromptPart, UserPromptPart))]
        if parts:
            out.append(dataclasses.replace(message, parts=parts))
    return out


def _shows_text(history, text: str) -> bool:
    """Does any message part of the conversation carry `text`?"""
    for message in history:
        for part in getattr(message, "parts", ()):
            content = getattr(part, "content", None)
            shown = content if isinstance(content, str) else (
                json.dumps(content, default=str) if content is not None else "")
            if text in shown:
                return True
    return False


def _lean_reset(history, *, carry_on: bool) -> str | None:
    """Why a lean run's request cannot extend the last run's first one (counted on
    the trace, D13): its history still holds tool traffic -- a paused run being
    finished (`resume`), or the first run after the switch to lean (`switch`)."""
    from pydantic_ai.messages import ModelResponse

    if any(isinstance(m, ModelResponse) for m in history):
        return "resume" if carry_on else "switch"
    return None


def _dump_messages(messages) -> str:
    """A run's whole history as the store keeps it (Pydantic AI's own JSON)."""
    from pydantic_ai.messages import ModelMessagesTypeAdapter

    return ModelMessagesTypeAdapter.dump_json(messages).decode("utf-8")


def _compaction_available() -> bool:
    """Conversation mode needs compaction to bound its context: without it the
    worker runs as bites (logged once, at start), never an unbounded conversation."""
    try:
        from probe.daemon.agent.state import RunState
        from probe.daemon.agent.context import counted_compaction

        counted_compaction(RunState(conversation=True))
    except Exception as exc:  # noqa: BLE001
        log.warning("conversation mode needs compaction, which cannot be built (%s: %s): running as %s",
                    type(exc).__name__, exc, Mode.BITES)
        return False
    return True


def _run_record(run: str, answer: tools.ProbeResult | None) -> dict | None:
    """`answer` to `probe run get <run>` as that run's JSON; None when it was not
    answered, failed, is not a JSON object, or is another run's."""
    if answer is None or answer.code != 0:
        return None
    try:
        record = json.loads(answer.stdout)
    except ValueError:
        return None
    if not isinstance(record, dict) or str(record.get("id") or "").lower() != run:
        return None
    return record
from probe.daemon.worker.loop.mode import Mode  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.reading import log  # noqa: E402 -- pieces need each other; the front door loads this one first
