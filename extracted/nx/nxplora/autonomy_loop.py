"""GRAIL Phase 4 — the autonomy loop, born safe. STEP 1: the canonical single-action control-flow.

Every action the autonomy loop considers passes `guarded_loop_action()` BEFORE anything fires. The order is
the ratified fail-safe: **is_untouchable() is checked FIRST** (the T3 structural wall — money movement /
signing / legal execution → founder-only, NEVER autonomous), and only then the SAFE/DESTRUCTIVE tier. Because
is_untouchable() is the first wall, a mislabelled or brand-new money/signing tool cannot leak through as a
lower tier — the runtime money-mover/signing guard catches it before anything else.

The loop, by construction, can only ever **fire T1** (a SAFE read/analysis/draft, then report back). Every
T2 (DESTRUCTIVE — approvable, but not autonomously) and T3 (untouchable) returns a STOP verdict: the loop
stages the action, reports it, and hands off to the operator. There is no code path here that fires a
DESTRUCTIVE or fund-moving action autonomously — the only verdict that fires is FIRE_T1, reached only for a
resolved-SAFE action that is not untouchable.

This composes the three proven foundations at the single per-action chokepoint: Phase 1 (is_untouchable /
resolve_tier) decides the tier; a STOP_T2 hand-off is where Phase 3 (GATE-1) takes over on the web (the
operator approves, the fire is content-bound-verified); the caller tees the outcome to Phase 2 (the brain).
"""
from __future__ import annotations

from typing import NamedTuple

try:  # importable both as a bare module (nx/cli on sys.path, like nx_cli) and as a package submodule
    from risk_tiers import is_untouchable, is_read_only, resolve_tier, SAFE
except ImportError:  # pragma: no cover
    from .risk_tiers import is_untouchable, is_read_only, resolve_tier, SAFE

# ── Loop verdicts ────────────────────────────────────────────────────────────────────────────────────────
FIRE_T1 = "FIRE_T1"                          # T1 — SAFE: fire autonomously, then report back
STOP_T2_APPROVAL = "STOP_T2_APPROVAL"        # T2 — DESTRUCTIVE: stop, stage, hand off (GATE-1 approval on the web)
STOP_T3_UNTOUCHABLE = "STOP_T3_UNTOUCHABLE"  # T3 — money/signing: founder-only, NEVER autonomous


class LoopVerdict(NamedTuple):
    """The typed decision for one action at the loop's chokepoint."""
    verdict: str   # FIRE_T1 | STOP_T2_APPROVAL | STOP_T3_UNTOUCHABLE
    tier: str      # "T1" | "T2" | "T3"
    reason: str

    @property
    def fires(self) -> bool:
        """True ONLY for FIRE_T1 — the single autonomous-fire path."""
        return self.verdict == FIRE_T1


def guarded_loop_action(server: str, tool: str, args: str = "") -> LoopVerdict:
    """The autonomy loop's single-action chokepoint. is_untouchable() FIRST, then the SAFE/DESTRUCTIVE tier.

    Returns a LoopVerdict; only FIRE_T1 authorizes an autonomous fire. A DESTRUCTIVE (T2) or untouchable (T3)
    action never fires here — it is staged for operator hand-off. Fail-closed by inheritance: resolve_tier
    defaults unknown/typo'd ops to DESTRUCTIVE, and is_untouchable fail-safes ambiguous money/signing to T3.
    """
    # 1) T3 structural wall FIRST — moves real funds or legally binds → founder-only, never autonomous.
    if is_untouchable(server, tool, args):
        return LoopVerdict(
            STOP_T3_UNTOUCHABLE, "T3",
            f"{server}.{tool} moves funds or legally binds — founder-only, never fires autonomously",
        )
    # 2) A CLEAR READ → T1: the ONLY autonomous-fire path. (Stricter than SAFE — a reversible write is NOT a read.)
    if is_read_only(server, tool, args):
        return LoopVerdict(
            FIRE_T1, "T1",
            f"{server}.{tool} is a clear read — fires autonomously, then reports back",
        )
    # 3) Not a read → STAGE for operator approval. Distinguish a reversible write (SAFE) from a destructive op;
    #    both are held — the loop only ever FIRES reads. (A destructive/write cloud action verifies via GATE-1.)
    if resolve_tier(server, tool, args) == SAFE:
        why = "is a reversible write — staged; the loop fires only reads autonomously"
    else:
        why = "is destructive — staged; needs operator approval before it can fire"
    return LoopVerdict(STOP_T2_APPROVAL, "T2", f"{server}.{tool} {why}")


# ── STEP 2 — world → action tier resolver ────────────────────────────────────────────────────────────────
# The per-action verdict (guarded_loop_action, is_untouchable-FIRST) is ALWAYS authoritative and resolves the
# dual-gating conflict toward safety: a money-mover is T3 here regardless of any pack-catalog label. The coarse
# world-tier below is only a routing/reporting HINT (grounding STEP 0) — it never overrides a per-action verdict.
T3_HEAVY, T2_HEAVY, T1_HEAVY = "T3_HEAVY", "T2_HEAVY", "T1_HEAVY"

# Keys mirror nx_prompts.NX_WORLD_CONTEXT (25 worlds). Bias only — "expect most of this world's actions to stop".
WORLD_COARSE_TIER = {
    # money moved / legally binding / people records dominate → most actions stop for founder or approval
    "finance": T3_HEAVY, "legal": T3_HEAVY, "capital": T3_HEAVY, "hr": T3_HEAVY, "compliance": T3_HEAVY,
    # outward / customer-facing action → mostly approval-gated
    "sales": T2_HEAVY, "leads": T2_HEAVY, "crm": T2_HEAVY, "customers": T2_HEAVY, "marketing": T2_HEAVY,
    "growth": T2_HEAVY, "product": T2_HEAVY, "brand": T2_HEAVY, "support": T2_HEAVY, "ops": T2_HEAVY,
    "onboarding": T2_HEAVY, "recruiting": T2_HEAVY, "code": T2_HEAVY, "devops": T2_HEAVY,
    # read / analysis / internal-coordination → mostly autonomous
    "research": T1_HEAVY, "knowledge": T1_HEAVY, "strategy": T1_HEAVY, "cowork": T1_HEAVY,
    "agents": T1_HEAVY, "nx-1": T1_HEAVY,
}


def world_coarse_tier(world: str) -> str:
    """Routing/reporting hint only. Unknown world → T2_HEAVY (fail toward caution). Never overrides a verdict."""
    return WORLD_COARSE_TIER.get((world or "").strip().lower(), T2_HEAVY)


class WorldTierMap(NamedTuple):
    """A world's candidate actions, each classified by the per-action chokepoint."""
    world: str
    coarse_tier: str
    t1: list  # [(server, tool, LoopVerdict), ...] — autonomous, WILL fire this run
    t2: list  # staged: destructive, needs operator approval (GATE-1)
    t3: list  # staged: founder-only, never autonomous

    @property
    def autonomous(self):
        """The T1 actions the loop fires autonomously."""
        return self.t1

    @property
    def staged(self):
        """Everything handed off to the operator (T2 approvals + T3 founder-only)."""
        return self.t2 + self.t3

    @property
    def counts(self):
        return {"t1": len(self.t1), "t2": len(self.t2), "t3": len(self.t3)}


def resolve_world_tiers(world, actions) -> WorldTierMap:
    """Classify one world's candidate actions into T1/T2/T3 via guarded_loop_action (is_untouchable-FIRST).

    actions: iterable of (server, tool) or (server, tool, args). Only .t1 will fire autonomously; .t2 and .t3
    are staged for operator hand-off. The per-action verdict is authoritative — a money/signing op lands in
    .t3 even if a catalog would call it T2.
    """
    t1, t2, t3 = [], [], []
    for a in actions:
        server, tool = a[0], a[1]
        args = a[2] if len(a) > 2 else ""
        v = guarded_loop_action(server, tool, args)
        if v.verdict == FIRE_T1:
            t1.append((server, tool, v))
        elif v.verdict == STOP_T2_APPROVAL:
            t2.append((server, tool, v))
        else:
            t3.append((server, tool, v))
    return WorldTierMap(world, world_coarse_tier(world), t1, t2, t3)


# ── STEP 3 — the a–z autonomy loop (born safe: the gate sits DOWNSTREAM of the planner) ───────────────────
# The loop plans candidate reads two ways — (A) a fixed "pull the state" set from the world's connected tools,
# and (B) an LLM-planned set — then UNIONS them and runs EVERY candidate through guarded_loop_action before
# anything fires. Only FIRE_T1 candidates are executed; every T2/T3 (including a hallucinated B proposal like
# send_wire or delete_repo) is STAGED, never fired. fire_fn is called ONLY for a T1 candidate — that is the
# structural born-safe guarantee. enumerate_fn / llm_fn / fire_fn are injected so the loop is unit-provable
# without live infra; the live CLI wiring (agent_slugs→tools_schema, guarded MCP read, the LLM planner) is a
# thin adapter over these seams.

class Candidate(NamedTuple):
    server: str
    tool: str
    args: str
    source: str   # "fixed" (A: connected read-set) | "planned" (B: LLM-proposed)


class ActionResult(NamedTuple):
    server: str
    tool: str
    args: str
    ok: bool
    output: object
    source: str


class StagedAction(NamedTuple):
    server: str
    tool: str
    args: str
    tier: str      # "T2" | "T3"
    reason: str
    source: str


class WorldRunResult(NamedTuple):
    world: str
    coarse_tier: str
    fired: list          # [ActionResult]   — T1 reads that ran autonomously
    staged: list         # [StagedAction]   — T2/T3 handed off to the operator
    capped: list = ()    # [Candidate]      — T1 reads NOT fired (per-world cap hit) — surfaced, never dropped

    @property
    def counts(self):
        return {"fired": len(self.fired), "staged": len(self.staged), "capped": len(self.capped)}


class LoopRun(NamedTuple):
    worlds: list   # [WorldRunResult]

    @property
    def all_fired(self):
        return [a for w in self.worlds for a in w.fired]

    @property
    def all_staged(self):
        return [s for w in self.worlds for s in w.staged]

    @property
    def all_capped(self):
        return [c for w in self.worlds for c in w.capped]

    @property
    def counts(self):
        return {"worlds": len(self.worlds), "fired": len(self.all_fired),
                "staged": len(self.all_staged), "capped": len(self.all_capped)}


def compose_plan(enumerate_fn, llm_fn=None):
    """Build a plan(world) -> [Candidate] that unions (A) connected reads + (B) LLM-planned reads.

    enumerate_fn(world) -> iterable of (server, tool[, args])  — the world's connected tools (A).
    llm_fn(world)       -> iterable of (server, tool[, args])  — the LLM's proposed reads (B), optional.
    Every candidate is gated later in run_world; the planner is untrusted by construction.
    """
    def plan(world):
        out = [Candidate(a[0], a[1], a[2] if len(a) > 2 else "", "fixed") for a in enumerate_fn(world)]
        if llm_fn:
            out += [Candidate(a[0], a[1], a[2] if len(a) > 2 else "", "planned") for a in (llm_fn(world) or [])]
        return out
    return plan


def run_world(world, candidates, fire_fn, max_fires=None):
    """Gate every candidate; FIRE only T1 (via fire_fn); STAGE every T2/T3. Dedupe by (server, tool, args).

    fire_fn(world, server, tool, args) -> (ok: bool, output)  — the real guarded read (injected). It is called
    ONLY for a FIRE_T1 candidate, so no destructive/fund-moving action can execute here regardless of its source.
    max_fires: bound the number of T1 reads actually fired per world; T1 candidates beyond the cap are recorded
    in `capped` (surfaced in the report, never silently dropped) rather than fired. T2/T3 are always classified.
    """
    fired, staged, capped, seen = [], [], [], set()
    for c in candidates:
        key = (c.server, c.tool, c.args)
        if key in seen:
            continue
        seen.add(key)
        v = guarded_loop_action(c.server, c.tool, c.args)
        if v.fires:
            if max_fires is not None and len(fired) >= max_fires:
                capped.append(c)                     # T1, but over the per-world cap → not fired, surfaced
                continue
            ok, output = fire_fn(world, c.server, c.tool, c.args)
            fired.append(ActionResult(c.server, c.tool, c.args, bool(ok), output, c.source))
        else:
            staged.append(StagedAction(c.server, c.tool, c.args, v.tier, v.reason, c.source))
    return WorldRunResult(world, world_coarse_tier(world), fired, staged, capped)


def run_autonomy_loop(worlds, plan_fn, fire_fn, max_fires=None):
    """The a–z loop: for each world, plan (A+B) → gate → fire T1 (up to max_fires) / stage the rest. LoopRun."""
    return LoopRun([run_world(w, plan_fn(w), fire_fn, max_fires=max_fires) for w in worlds])


# ── STEP 4 — report-back (the transient half + the durable brain tee) ────────────────────────────────────
# Every run tees to TWO places: a transient report to the operator (Telegram first — the only live channel),
# and the permanent shared brain. Honest framing: report() never hides a delivery failure — it returns a
# per-channel status, and .delivered is False if nothing landed (the caller must not treat a run as reported
# unless it was). The senders are injected: telegram_send(text) and brain_write(text, loop_run) — the live
# wiring is a thin adapter (SkillsTelegramClient.sendTelegramMessage / _brain_route_push).

class ReportResult(NamedTuple):
    text: str
    telegram_sent: bool
    telegram_error: object   # None if sent or not configured
    brain_teed: bool
    brain_error: object

    @property
    def delivered(self) -> bool:
        """True if the run landed on at least one channel (transient OR durable). False → surface it."""
        return self.telegram_sent or self.brain_teed


def format_report(loop_run, header: str = "NX autonomy run", brief: bool = False) -> str:
    """Operator-facing digest: per-world, what fired autonomously (T1) and what is staged (T2 approval / T3
    founder-only). Action metadata only (server.tool + reason) — not raw outputs — so it is safe to broadcast.
    brief=True → a compact summary (per-world counts + the T3 items held) that fits a chat message (Telegram's
    4096-char limit); the full form is teed to the brain."""
    fired_n = len(loop_run.all_fired)
    t2_n = sum(1 for s in loop_run.all_staged if s.tier == "T2")
    t3_n = sum(1 for s in loop_run.all_staged if s.tier == "T3")
    capped_n = len(loop_run.all_capped)
    head = (
        f"{header} — {len(loop_run.worlds)} world(s) · fired {fired_n} · "
        f"staged {t2_n + t3_n} (T2 {t2_n} / T3 {t3_n})"
    )
    if capped_n:
        head += f" · {capped_n} T1 capped"
    lines = [head]
    for w in loop_run.worlds:
        if not (w.fired or w.staged or w.capped):
            continue
        if brief:
            extra = f" · +{len(w.capped)} capped" if w.capped else ""
            lines.append(f"[{w.world}] fired {len(w.fired)} read(s) · staged {len(w.staged)}{extra}")
            for s in w.staged:                                # list only the T3 (founder-only) items in brief
                if s.tier == "T3":
                    lines.append(f"  \U0001F512 T3 held: {s.server}.{s.tool}")
            continue
        lines.append(f"[{w.world}] ({w.coarse_tier})")
        for a in w.fired:
            lines.append(f"  ✅ {a.server}.{a.tool} ({'ok' if a.ok else 'FAILED'})")
        for s in w.staged:
            icon = "\U0001F512" if s.tier == "T3" else "⏸️"   # 🔒 T3 / ⏸️ T2
            lines.append(f"  {icon} {s.tier} {s.server}.{s.tool} — {s.reason}")
        if w.capped:
            lines.append(f"  … +{len(w.capped)} more safe reads available (capped this run)")
    if t2_n + t3_n == 0:
        lines.append("nothing needs your approval — all autonomous.")
    return "\n".join(lines)


def report(loop_run, telegram_send=None, brain_write=None, header: str = "NX autonomy run") -> ReportResult:
    """Format the run and tee it to the transient channel (Telegram, a BRIEF summary) + the durable brain (the
    FULL digest). Fail-open per channel, but honestly reported: a raising sender is caught; .delivered reflects
    reality. .text is the full form."""
    text = format_report(loop_run, header)
    brief = format_report(loop_run, header, brief=True)
    tg_sent, tg_err = False, None
    if telegram_send is not None:
        try:
            telegram_send(brief)          # transient channel gets the compact summary (fits the 4096 limit)
            tg_sent = True
        except Exception as e:  # never let a channel failure lose the run silently
            tg_err = str(e) or repr(e)
    br_teed, br_err = False, None
    if brain_write is not None:
        try:
            brain_write(text, loop_run)
            br_teed = True
        except Exception as e:
            br_err = str(e) or repr(e)
    return ReportResult(text, tg_sent, tg_err, br_teed, br_err)


# ── STEP 5 — resumable + observable audit ────────────────────────────────────────────────────────────────
# One JSON-serializable record per run: exactly what the loop perceived, fired (T1), and staged (T2/T3), plus
# the report delivery status. It makes a run OBSERVABLE (the operator can replay precisely what happened) and
# RESUMABLE — pending_approvals() is the T2 hand-off queue the operator returns to later (approve → the action
# fires on the web through GATE-1). run_id / timestamps are injected so the record is deterministic + testable;
# the live wiring stamps them and persists the record to a run table.

def run_record(loop_run, report_result=None, run_id=None, started_at=None, ended_at=None) -> dict:
    """A serializable, replayable audit record of one autonomy run (pure — no clock/uuid side effects here)."""
    return {
        "run_id": run_id,
        "started_at": started_at,
        "ended_at": ended_at,
        "counts": loop_run.counts,
        "worlds": [
            {
                "world": w.world,
                "coarse_tier": w.coarse_tier,
                "fired": [
                    {"server": a.server, "tool": a.tool, "args": a.args, "ok": a.ok, "source": a.source}
                    for a in w.fired
                ],
                "staged": [
                    {"server": s.server, "tool": s.tool, "args": s.args, "tier": s.tier,
                     "reason": s.reason, "source": s.source}
                    for s in w.staged
                ],
                "capped": [
                    {"server": c.server, "tool": c.tool, "args": c.args, "source": c.source}
                    for c in w.capped
                ],
            }
            for w in loop_run.worlds
        ],
        "report": None if report_result is None else {
            "text": report_result.text,
            "delivered": report_result.delivered,
            "telegram_sent": report_result.telegram_sent,
            "telegram_error": report_result.telegram_error,
            "brain_teed": report_result.brain_teed,
            "brain_error": report_result.brain_error,
        },
    }


def pending_approvals(loop_run) -> list:
    """The T2 hand-off queue — the actions staged for operator approval, keyed for resume (world+server+tool+args).
    T3 (untouchable) is deliberately excluded: it is founder-only and has NO approval path, so it is never queued."""
    out = []
    for w in loop_run.worlds:
        for s in w.staged:
            if s.tier == "T2":
                out.append({"world": w.world, "server": s.server, "tool": s.tool,
                            "args": s.args, "reason": s.reason})
    return out
