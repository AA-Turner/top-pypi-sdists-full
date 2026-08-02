"""GRAIL Phase 5 STEP 1 — live-wiring adapters + cli_loop orchestration.

Adapters are injectable so the orchestration is provable without live infra. Proves: live run fires only T1
(destructive never fired) + reports both channels + records; dry-run fires/sends/persists NOTHING even if a
sender is injected; the Telegram sender posts correctly / fails honestly; the runs log appends.
Run: python3 nx/cli/tests/test_nx_loop.py
"""
import os, sys, json, tempfile, types
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nx_loop import (
    cli_loop, send_telegram_message, persist_run, resolve_telegram_chat_id,
    parse_loop_args, resolve_worlds, DEFAULT_PILOT_WORLDS, parse_planned_reads,
    _filter_world_servers,
)


def _enum(world):
    return {
        "sales": [("hubspot", "list_deals"), ("gmail", "send_email")],     # T1 + T2
        "finance": [("stripe", "get_balance"), ("stripe", "send_wire")],   # T1 + T3
    }.get(world, [])


def test_cli_loop_live_fires_only_t1_reports_records():
    sent, brain, fires = [], [], []
    def fire(w, s, t, a=""):
        fires.append((w, s, t)); return (True, "{}.{}".format(s, t))
    loop_run, rr, rec = cli_loop(
        {"user_id": "u1"}, ["sales", "finance"], dry_run=False,
        enumerate_fn=_enum, fire_fn=fire,
        telegram_send=lambda t: sent.append(t), brain_write=lambda t, lr: brain.append(t),
        persist=False, now=lambda: 42,
    )
    assert loop_run.counts == {"worlds": 2, "fired": 2, "staged": 2, "capped": 0}
    assert {(w, s, t) for w, s, t in fires} == {("sales", "hubspot", "list_deals"), ("finance", "stripe", "get_balance")}
    # nothing destructive/fund-moving was ever fired
    assert all((s, t) not in {("gmail", "send_email"), ("stripe", "send_wire")} for _, s, t in fires)
    assert len(sent) == 1 and len(brain) == 1
    assert rr.delivered and rr.telegram_sent and rr.brain_teed
    assert rec["started_at"] == 42 and rec["ended_at"] == 42 and rec["run_id"]


def test_cli_loop_dry_run_fires_and_sends_nothing():
    sent = []
    loop_run, rr, rec = cli_loop(
        {}, ["sales"], dry_run=True,
        enumerate_fn=_enum, telegram_send=lambda t: sent.append(t), persist=False, now=lambda: 0,
    )
    # dry-run still CLASSIFIES (list_deals is T1) but fires only a marker, and sends nothing
    assert loop_run.counts["fired"] == 1
    assert [a.output for a in loop_run.all_fired] == ["[dry-run — not fired]"]
    assert sent == []              # injected sender NOT called in dry-run
    assert not rr.delivered


def _fake_requests(status=200, text="ok", get_json=None):
    calls = []
    m = types.ModuleType("requests")
    class R:
        def __init__(self, jd=None):
            self.status_code = status; self.text = text; self._jd = jd or {}
        def json(self):
            return self._jd
    m.post = lambda url, **kw: (calls.append((url, kw)), R())[1]
    m.get = lambda url, **kw: (calls.append((url, kw)), R(get_json))[1]
    return m, calls


def test_send_telegram_no_creds_raises():
    for k in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"):
        os.environ.pop(k, None)
    try:
        send_telegram_message("hi", {}); assert False, "should raise"
    except RuntimeError as e:
        assert "not configured" in str(e)


def test_send_telegram_posts_with_creds():
    fake, calls = _fake_requests(200)
    sys.modules["requests"] = fake
    os.environ["TELEGRAM_BOT_TOKEN"] = "T"; os.environ["TELEGRAM_CHAT_ID"] = "C"
    try:
        send_telegram_message("hello", {})
        assert len(calls) == 1 and calls[0][0].endswith("/botT/sendMessage")
        assert calls[0][1]["json"] == {"chat_id": "C", "text": "hello"}
    finally:
        del sys.modules["requests"]
        os.environ.pop("TELEGRAM_BOT_TOKEN"); os.environ.pop("TELEGRAM_CHAT_ID")


def test_send_telegram_non200_raises():
    fake, _ = _fake_requests(429, "rate limited")
    sys.modules["requests"] = fake
    os.environ["TELEGRAM_BOT_TOKEN"] = "T"; os.environ["TELEGRAM_CHAT_ID"] = "C"
    try:
        send_telegram_message("x", {}); assert False, "should raise"
    except RuntimeError as e:
        assert "429" in str(e)
    finally:
        del sys.modules["requests"]
        os.environ.pop("TELEGRAM_BOT_TOKEN"); os.environ.pop("TELEGRAM_CHAT_ID")


def test_resolve_telegram_chat_id_from_updates():
    fake, calls = _fake_requests(200, get_json={"result": [
        {"message": {"chat": {"id": 111}}},
        {"message": {"chat": {"id": 222}}},   # latest message wins
    ]})
    sys.modules["requests"] = fake
    os.environ.pop("TELEGRAM_CHAT_ID", None)
    try:
        assert resolve_telegram_chat_id({"telegram_bot_token": "T"}) == "222"
        assert calls[0][0].endswith("/botT/getUpdates")
    finally:
        del sys.modules["requests"]


def test_send_telegram_auto_resolves_chat_id():
    # token set, NO chat_id → send auto-resolves via getUpdates, then posts to the resolved chat
    fake, calls = _fake_requests(200, get_json={"result": [{"message": {"chat": {"id": 999}}}]})
    sys.modules["requests"] = fake
    os.environ["TELEGRAM_BOT_TOKEN"] = "T"; os.environ.pop("TELEGRAM_CHAT_ID", None)
    try:
        send_telegram_message("hi", {})
        urls = [u for u, _ in calls]
        assert any("getUpdates" in u for u in urls) and any("sendMessage" in u for u in urls)
        post_kw = [kw for u, kw in calls if "sendMessage" in u][0]
        assert post_kw["json"]["chat_id"] == "999"
    finally:
        del sys.modules["requests"]; os.environ.pop("TELEGRAM_BOT_TOKEN")


def test_persist_run_appends_jsonl():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "runs.jsonl")
        assert persist_run({"run_id": "a"}, p) and persist_run({"run_id": "b"}, p)
        got = [json.loads(l)["run_id"] for l in open(p).read().strip().split("\n")]
        assert got == ["a", "b"]


def test_parse_planned_reads():
    text = ('plan: [{"server":"Tavily","tool":"tavily_search","args":{"query":"AI agents"}}, '
            '{"server":"Notion","tool":"search","args":{"query":"roadmap"}}, {"bad":"entry"}] done')
    assert parse_planned_reads(text) == [
        ("Tavily", "tavily_search", '{"query": "AI agents"}'),
        ("Notion", "search", '{"query": "roadmap"}'),
    ]
    assert parse_planned_reads("no json") == []
    assert parse_planned_reads("[not valid") == []
    assert parse_planned_reads('[{"server":"x","tool":"y","args":"raw"}]') == [("x", "y", "raw")]


def test_cli_loop_llm_planner_gated():
    # B (llm_fn) proposes a read WITH args + a write; only the read fires (with its args), the write is staged.
    # The read tool must LEAD with a read verb (get/list/fetch/search/…) — is_read_only fail-closes on any
    # unrecognized leading token (e.g. a vendor-prefixed 'tavily_search'), staging it rather than auto-firing.
    fires = []
    def fire(w, s, t, a=""):
        fires.append((s, t, a)); return (True, "ok")
    llm = lambda world: [("Tavily", "search", '{"query":"x"}'), ("Notion", "create_page", '{"title":"z"}')]
    loop_run, rr, rec = cli_loop(
        {}, ["research"], use_llm=True, dry_run=False, send=False,
        enumerate_fn=lambda w: [], llm_fn=llm, fire_fn=fire, persist=False, now=lambda: 0,
    )
    assert [(s, t) for s, t, _ in fires] == [("Tavily", "search")]           # only the read fired
    assert fires[0][2] == '{"query":"x"}'                                    # WITH the planned args
    assert loop_run.counts["staged"] == 1                                    # the create_page was staged, not fired


def test_parse_loop_args():
    p = parse_loop_args(["--dry-run", "--world", "research", "--world", "finance", "--llm"])
    assert p == {"worlds": ["research", "finance"], "dry_run": True, "use_llm": True, "all_worlds": False, "rounds": 1}
    assert parse_loop_args([]) == {"worlds": [], "dry_run": False, "use_llm": False, "all_worlds": False, "rounds": 1}
    assert parse_loop_args(["--chain"])["rounds"] == 2
    assert parse_loop_args(["--all"])["all_worlds"] is True
    assert parse_loop_args(["--world"])["worlds"] == []   # dangling --world ignored


def test_resolve_worlds():
    allw = ["research", "knowledge", "finance", "sales"]
    assert resolve_worlds({"all_worlds": True}, allw) == allw
    assert resolve_worlds({"worlds": ["finance", "bogus"]}, allw) == ["finance"]   # invalid dropped
    assert resolve_worlds({"worlds": []}, allw) == DEFAULT_PILOT_WORLDS            # pilot default
    assert resolve_worlds({"worlds": ["bogus"]}, allw) == DEFAULT_PILOT_WORLDS     # all-invalid → default



def test_cli_loop_chaining_feeds_prior_to_round2():
    fires, calls = [], []
    def fire(w, s, t, a=""):
        fires.append((s, t))
        return (True, "found id=42" if t == "search" else "ok")
    def llm(world, prior=None):
        calls.append(prior)
        return [("Notion", "search", '{"q":"x"}')] if not prior else [("Notion", "fetch", '{"id":"42"}')]
    loop_run, rr, rec = cli_loop(
        {}, ["research"], use_llm=True, rounds=2, dry_run=False, send=False,
        enumerate_fn=lambda w: [], llm_fn=llm, fire_fn=fire, persist=False, now=lambda: 0,
    )
    assert fires == [("Notion", "search"), ("Notion", "fetch")]        # BOTH rounds fired
    assert len(calls) == 2 and calls[0] is None and calls[1] is not None  # round 2 received prior
    assert any(getattr(a, "ok", False) and a.tool == "search" for a in calls[1])  # prior carries round-1 result



def test_filter_world_servers():
    g = {"stripe": {"name": "Stripe"}, "hubspot": {"name": "HubSpot"}, "notion": {"name": "Notion"}}
    assert set(_filter_world_servers("finance", g)) == {"stripe"}      # money server → finance
    assert set(_filter_world_servers("sales", g)) == {"hubspot"}       # crm → sales
    assert set(_filter_world_servers("research", g)) == {"notion"}     # notion → research
    assert set(_filter_world_servers("nx-1", g)) == set(g)             # unmapped world → all (fallback)
    assert set(_filter_world_servers("brand", g)) == set(g)            # mapped but 0 match → all (never empty)
    assert _filter_world_servers("finance", {}) == {}                 # empty stays empty


if __name__ == "__main__":
    for n, f in sorted((n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)):
        f(); print("  ✓ {}".format(n))
    print("ALL PHASE-5 STEP-1 LIVE-WIRING PROOFS PASS")
