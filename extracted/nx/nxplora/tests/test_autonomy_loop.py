"""GRAIL Phase 4 STEP 1 — the autonomy loop's single-action control-flow (guarded_loop_action).

Proves the born-safe invariant: the ONLY verdict that fires is FIRE_T1, reached only for a resolved-SAFE,
not-untouchable action. Every money-movement / signing op → STOP_T3 (never autonomous); every other
destructive op → STOP_T2 (staged for approval); is_untouchable() is checked FIRST so a fund-mover can never
leak as T1/T2. Run: python3 nx/cli/tests/test_autonomy_loop.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autonomy_loop import (
    guarded_loop_action, FIRE_T1, STOP_T2_APPROVAL, STOP_T3_UNTOUCHABLE,
    resolve_world_tiers, world_coarse_tier, WORLD_COARSE_TIER, T2_HEAVY, T3_HEAVY,
    Candidate, run_world, run_autonomy_loop, compose_plan,
    format_report, report,
    run_record, pending_approvals,
)
import json


def _sample_run():
    fire, _ = _recording_fire()
    world_actions = {
        "sales": [("hubspot", "list_deals"), ("gmail", "send_email")],    # T1 fired + T2 staged
        "finance": [("stripe", "get_balance"), ("stripe", "send_wire")],  # T1 fired + T3 staged
    }
    return run_autonomy_loop(["sales", "finance"], compose_plan(lambda w: world_actions.get(w, [])), fire)


def _recording_fire():
    calls = []
    def fire(world, server, tool, args):
        calls.append((world, server, tool, args))
        return (True, f"{server}.{tool}=ok")
    return fire, calls


def test_t3_money_movement_never_autonomous():
    for server, tool in [
        ("stripe", "create_charge"), ("stripe", "send_payout"), ("paypal", "transfer"),
        ("gusto", "run_payroll"), ("mercury", "send_wire"), ("quickbooks", "create_refund"),
        ("wise", "disburse"), ("column", "ach_debit"),
    ]:
        v = guarded_loop_action(server, tool)
        assert v.verdict == STOP_T3_UNTOUCHABLE and v.tier == "T3" and not v.fires, f"{server}.{tool} → {v.verdict}"


def test_t3_signing_never_autonomous():
    for server, tool in [
        ("docusign", "send_for_signature"), ("hellosign", "create_signature_request"),
        ("pandadoc", "countersign"), ("anyserver", "sign_document"), ("anyserver", "notarize"),
        ("docusign", "create_envelope"),  # non-read on a signing server
    ]:
        v = guarded_loop_action(server, tool)
        assert v.verdict == STOP_T3_UNTOUCHABLE and not v.fires, f"{server}.{tool} → {v.verdict}"


def test_t3_failsafe_on_unknown_money_op():
    # a brand-new / unrecognized op on a fund-mover server → fail-safe T3 (not T1/T2)
    v = guarded_loop_action("stripe", "frobnicate_ledger")
    assert v.verdict == STOP_T3_UNTOUCHABLE and not v.fires
    v2 = guarded_loop_action("gusto", "quux")
    assert v2.verdict == STOP_T3_UNTOUCHABLE and not v2.fires


def test_t1_safe_reads_fire():
    for server, tool in [
        ("clickup", "get_tasks"), ("notion", "search"), ("hubspot", "list_contacts"),
        ("ga", "get_report"), ("linear", "list_issues"), ("stripe", "get_balance"),  # clear read on a money server
        ("quickbooks", "get_invoice"),  # a lookup, not a movement
    ]:
        v = guarded_loop_action(server, tool)
        assert v.verdict == FIRE_T1 and v.tier == "T1" and v.fires, f"{server}.{tool} → {v.verdict}"


def test_t2_destructive_non_money_stops_for_approval():
    for server, tool in [
        ("clickup", "delete_task"), ("gmail", "send_email"), ("slack", "post_message"),
        ("github", "delete_repo"), ("hubspot", "delete_contact"),
    ]:
        v = guarded_loop_action(server, tool)
        assert v.verdict == STOP_T2_APPROVAL and v.tier == "T2" and not v.fires, f"{server}.{tool} → {v.verdict}"


def test_t2_failclosed_on_unknown_nonmoney_op():
    # unrecognized op on a non-fund/non-signing server → DESTRUCTIVE default → T2 (approvable), NOT a fire
    v = guarded_loop_action("some_new_server", "mystery_verb")
    assert v.verdict == STOP_T2_APPROVAL and not v.fires


def test_reads_only_fire_reversible_writes_stage():
    # the born-safe tightening (from the first real run): a CLEAR read fires; a reversible SAFE write
    # (create/update/duplicate) is STAGED, not fired — the loop only ever fires reads autonomously.
    for server, tool in [("notion", "get_teams"), ("notion", "search"), ("sentry", "find_projects"),
                         ("clickup", "list_tasks"), ("ga", "get_report")]:
        assert guarded_loop_action(server, tool).verdict == FIRE_T1, tool
    for server, tool in [("notion", "create_pages"), ("notion", "update_page"), ("notion", "duplicate_page"),
                         ("sentry", "update_issue"), ("clickup", "create_task"), ("linear", "create_comment")]:
        v = guarded_loop_action(server, tool)
        assert v.verdict == STOP_T2_APPROVAL and not v.fires, "{} → {}".format(tool, v.verdict)
        assert "reversible write" in v.reason, v.reason


def test_invariant_only_safe_ever_fires():
    # The core born-safe guarantee across a broad matrix: fires iff FIRE_T1 iff tier T1.
    matrix = [
        ("stripe", "create_charge"), ("docusign", "sign"), ("gusto", "run_payroll"),   # T3
        ("clickup", "delete_task"), ("gmail", "send_email"), ("xx", "unknown"),          # T2
        ("clickup", "get_tasks"), ("notion", "retrieve"), ("stripe", "list_charges"),    # T1 (reads)
    ]
    for server, tool in matrix:
        v = guarded_loop_action(server, tool)
        assert v.fires == (v.verdict == FIRE_T1) == (v.tier == "T1"), f"{server}.{tool} broke the invariant: {v}"
        if v.tier in ("T2", "T3"):
            assert not v.fires, f"{server}.{tool} is {v.tier} but fired!"


# ── STEP 2 — world → action tier resolver ────────────────────────────────────────────────────────────────

def test_resolve_world_tiers_groups_by_tier():
    # a finance world with a read (T1), a fund movement (T3), and a destructive non-money op (T2)
    m = resolve_world_tiers("finance", [
        ("stripe", "get_balance"),       # T1 read
        ("stripe", "create_charge"),     # T3 money movement
        ("clickup", "delete_task"),      # T2 destructive
        ("quickbooks", "list_invoices"), # T1 read
    ])
    assert m.world == "finance" and m.coarse_tier == T3_HEAVY
    assert m.counts == {"t1": 2, "t2": 1, "t3": 1}
    assert {(s, t) for s, t, _ in m.t1} == {("stripe", "get_balance"), ("quickbooks", "list_invoices")}
    assert {(s, t) for s, t, _ in m.t3} == {("stripe", "create_charge")}
    assert {(s, t) for s, t, _ in m.t2} == {("clickup", "delete_task")}


def test_world_tier_map_properties():
    m = resolve_world_tiers("sales", [
        ("hubspot", "list_deals"),   # T1
        ("gmail", "send_email"),     # T2
        ("stripe", "send_payout"),   # T3
    ])
    assert [(s, t) for s, t, _ in m.autonomous] == [("hubspot", "list_deals")]           # only T1 fires
    assert {(s, t) for s, t, _ in m.staged} == {("gmail", "send_email"), ("stripe", "send_payout")}
    assert m.counts == {"t1": 1, "t2": 1, "t3": 1}


def test_only_t1_fires_in_world_map():
    # invariant at the world level: every autonomous action fires, every staged action does not
    m = resolve_world_tiers("ops", [
        ("notion", "search"), ("clickup", "delete_task"), ("docusign", "sign"), ("ga", "get_report"),
    ])
    assert all(v.fires for _, _, v in m.autonomous)
    assert all(not v.fires for _, _, v in m.staged)
    assert all(v.tier == "T1" for _, _, v in m.t1)


def test_coarse_tier_hint_and_unknown_world():
    assert world_coarse_tier("finance") == T3_HEAVY
    assert world_coarse_tier("FINANCE ") == T3_HEAVY           # normalized
    assert world_coarse_tier("nonexistent") == T2_HEAVY        # unknown → cautious default
    assert world_coarse_tier("") == T2_HEAVY


def test_coarse_tier_covers_every_real_world_no_drift():
    # every world the CLI actually defines must have a coarse tier — and no extra/stale keys
    from nx_prompts import NX_WORLD_CONTEXT
    real = set(NX_WORLD_CONTEXT) - {"lead"}   # "lead" is an alias of "leads"
    assert real == set(WORLD_COARSE_TIER), f"world/coarse-tier drift: {real ^ set(WORLD_COARSE_TIER)}"


# ── STEP 3 — the a–z autonomy loop (gate downstream of the planner) ──────────────────────────────────────

def test_run_world_fires_only_t1_stages_rest():
    fire, calls = _recording_fire()
    cands = [
        Candidate("hubspot", "list_deals", "", "fixed"),   # T1
        Candidate("gmail", "send_email", "", "fixed"),     # T2
        Candidate("stripe", "send_wire", "", "planned"),   # T3 — proposed by the LLM (B)!
        Candidate("notion", "search", "", "planned"),      # T1
    ]
    r = run_world("sales", cands, fire)
    assert r.counts == {"fired": 2, "staged": 2, "capped": 0}
    assert {(a.server, a.tool) for a in r.fired} == {("hubspot", "list_deals"), ("notion", "search")}
    assert {(s.server, s.tool, s.tier) for s in r.staged} == {("gmail", "send_email", "T2"), ("stripe", "send_wire", "T3")}
    # fire_fn was called ONLY for the two T1 reads — never for send_email / send_wire
    assert len(calls) == 2
    assert ("sales", "stripe", "send_wire", "") not in calls and ("sales", "gmail", "send_email", "") not in calls


def test_malicious_llm_proposal_never_fires():
    # B proposes only fund-moving + binding ops; the downstream gate stages all, fire_fn is never called
    fire, calls = _recording_fire()
    cands = [Candidate(s, t, "", "planned") for s, t in
             [("stripe", "create_charge"), ("github", "delete_repo"), ("docusign", "sign"), ("gusto", "run_payroll")]]
    r = run_world("finance", cands, fire)
    assert r.counts["fired"] == 0 and r.counts["staged"] == 4
    assert calls == []   # the born-safe guarantee: nothing fired


def test_dedupe_same_action_from_a_and_b():
    fire, calls = _recording_fire()
    cands = [Candidate("notion", "search", "q", "fixed"), Candidate("notion", "search", "q", "planned")]
    r = run_world("research", cands, fire)
    assert r.counts["fired"] == 1 and len(calls) == 1


def test_compose_plan_unions_a_and_b():
    plan = compose_plan(lambda w: [("hubspot", "list_deals")], lambda w: [("notion", "search", "q")])
    cands = plan("sales")
    assert Candidate("hubspot", "list_deals", "", "fixed") in cands
    assert Candidate("notion", "search", "q", "planned") in cands
    plan_a = compose_plan(lambda w: [("ga", "get_report")])   # A only, no llm_fn
    assert [c.source for c in plan_a("x")] == ["fixed"]


def test_run_autonomy_loop_aggregates():
    fire, _ = _recording_fire()
    world_actions = {
        "sales": [("hubspot", "list_deals"), ("gmail", "send_email")],
        "finance": [("stripe", "get_balance"), ("stripe", "send_wire")],
    }
    plan = compose_plan(lambda w: world_actions.get(w, []))
    run = run_autonomy_loop(["sales", "finance"], plan, fire)
    assert run.counts == {"worlds": 2, "fired": 2, "staged": 2, "capped": 0}
    assert {(a.server, a.tool) for a in run.all_fired} == {("hubspot", "list_deals"), ("stripe", "get_balance")}
    assert {(s.server, s.tool, s.tier) for s in run.all_staged} == {("gmail", "send_email", "T2"), ("stripe", "send_wire", "T3")}


def test_invariant_fire_fn_only_for_t1():
    fire, calls = _recording_fire()
    cands = [
        Candidate("stripe", "create_charge", "", "planned"), Candidate("clickup", "delete_task", "", "fixed"),
        Candidate("docusign", "sign", "", "planned"), Candidate("notion", "search", "", "fixed"),
        Candidate("ga", "get_report", "", "planned"), Candidate("hubspot", "list_contacts", "", "fixed"),
    ]
    r = run_world("ops", cands, fire)
    t1_count = sum(1 for c in cands if guarded_loop_action(c.server, c.tool, c.args).fires)
    assert len(calls) == t1_count == len(r.fired)
    assert all(guarded_loop_action(a.server, a.tool, a.args).fires for a in r.fired)


# ── STEP 4 — report-back (Telegram + brain tee, honest framing) ──────────────────────────────────────────

def test_format_report_structure():
    text = format_report(_sample_run(), header="test run")
    assert text.startswith("test run — 2 world(s) · fired 2 · staged 2 (T2 1 / T3 1)")
    assert "hubspot.list_deals (ok)" in text
    assert "T2 gmail.send_email" in text        # staged for approval
    assert "T3 stripe.send_wire" in text        # founder-only surfaced


def test_report_fans_out_to_both_channels():
    run = _sample_run()
    sent, brain = [], []
    r = report(run, telegram_send=lambda t: sent.append(t), brain_write=lambda t, lr: brain.append((t, lr)))
    assert r.telegram_sent and r.brain_teed and r.delivered
    assert len(sent) == 1 and len(sent[0]) <= len(r.text)                      # telegram gets the BRIEF summary
    assert len(brain) == 1 and brain[0][0] == r.text and brain[0][1] is run    # brain gets the FULL digest


def test_report_honest_on_telegram_failure():
    run = _sample_run()
    brain = []
    def boom(_t):
        raise RuntimeError("telegram 429")
    r = report(run, telegram_send=boom, brain_write=lambda t, lr: brain.append(t))
    assert not r.telegram_sent and "429" in r.telegram_error   # failure surfaced, not swallowed
    assert r.brain_teed and r.delivered                        # brain still teed → run not lost
    assert len(brain) == 1


def test_report_no_senders_is_not_delivered():
    r = report(_sample_run())
    assert not r.telegram_sent and not r.brain_teed and not r.delivered   # surfaced, never silently dropped
    assert r.text and r.telegram_error is None and r.brain_error is None


def test_report_all_autonomous_note():
    fire, _ = _recording_fire()
    plan = compose_plan(lambda w: {"research": [("notion", "search"), ("ga", "get_report")]}.get(w, []))
    text = format_report(run_autonomy_loop(["research"], plan, fire))
    assert "nothing needs your approval" in text


# ── STEP 5 — resumable + observable audit ────────────────────────────────────────────────────────────────

def test_run_record_is_json_serializable_and_complete():
    run = _sample_run()
    rr = report(run, telegram_send=lambda t: None, brain_write=lambda t, lr: None)
    rec = run_record(run, rr, run_id="run-1", started_at=100, ended_at=200)
    # round-trips through JSON (persistable)
    back = json.loads(json.dumps(rec))
    assert back["run_id"] == "run-1" and back["started_at"] == 100 and back["ended_at"] == 200
    assert back["counts"] == {"worlds": 2, "fired": 2, "staged": 2, "capped": 0}
    fin = next(w for w in back["worlds"] if w["world"] == "finance")
    assert {a["tool"] for a in fin["fired"]} == {"get_balance"}
    assert {s["tool"] for s in fin["staged"]} == {"send_wire"} and fin["staged"][0]["tier"] == "T3"
    assert back["report"]["delivered"] is True and back["report"]["telegram_sent"] is True


def test_run_record_without_report():
    rec = run_record(_sample_run())
    assert rec["report"] is None and rec["run_id"] is None
    assert rec["counts"]["fired"] == 2


def test_pending_approvals_is_t2_only():
    q = pending_approvals(_sample_run())
    # only the T2 (gmail.send_email in sales) is an approvable hand-off; the T3 send_wire is NOT queued
    assert q == [{"world": "sales", "server": "gmail", "tool": "send_email", "args": "",
                  "reason": next(s.reason for w in _sample_run().worlds for s in w.staged if s.tier == "T2")}]
    assert all(item["server"] != "stripe" for item in q)   # the fund-mover is never in the approval queue


def test_run_world_caps_t1_fires():
    # 5 distinct T1 reads (search on 5 servers), cap at 2 → fire 2, cap 3 (surfaced), never over-fire
    fire, calls = _recording_fire()
    cands = [Candidate("srv{}".format(i), "search", "", "fixed") for i in range(5)]
    r = run_world("research", cands, fire, max_fires=2)
    assert r.counts == {"fired": 2, "staged": 0, "capped": 3}
    assert len(calls) == 2                                  # fire_fn called only up to the cap
    # cap never affects T2/T3 classification; it only bounds T1 fires
    cands2 = [Candidate("stripe", "send_wire", "", "planned")] + [Candidate("srv{}".format(i), "search", "", "fixed") for i in range(3)]
    r2 = run_world("finance", cands2, fire, max_fires=1)
    assert r2.counts == {"fired": 1, "staged": 1, "capped": 2}   # 1 T1 fired · T3 staged · 2 T1 capped
    assert all((c.server, c.tool) != ("stripe", "send_wire") for c in r2.capped)   # T3 is staged, not capped


if __name__ == "__main__":
    for n, f in sorted((n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)):
        f(); print(f"  ✓ {n}")
    print("ALL PHASE-4 STEP-1 GUARDED-LOOP-ACTION PROOFS PASS")
