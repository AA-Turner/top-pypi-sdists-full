"""Safety proof for the /browse gate — read=auto, buy/submit=gated, credentials=never; unknown=default-closed."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import nx_browse


class TestBrowseGate(unittest.TestCase):
    def test_read_actions_are_safe(self):
        for k in ["navigate", "goto", "read", "get_text", "extract", "screenshot", "scroll", "search", "back"]:
            self.assertEqual(nx_browse.classify_browse_action(k), "SAFE", k)

    def test_transactions_are_gated(self):
        for k in ["click_buy", "submit_form", "checkout", "place_order", "subscribe", "post", "publish", "send"]:
            self.assertEqual(nx_browse.classify_browse_action(k), "GATED", k)

    def test_credentials_and_captcha_prohibited(self):
        for k in ["enter_credential", "enter_password", "enter_payment", "solve_captcha", "create_account"]:
            self.assertEqual(nx_browse.classify_browse_action(k), "PROHIBITED", k)

    def test_typing_and_nav_click_are_safe(self):
        # typing is reversible + has no outward effect — SAFE; the SUBMIT/BUY is what gets gated.
        for k in ["fill", "type", "press", "select"]:
            self.assertEqual(nx_browse.classify_browse_action(k), "SAFE", k)
        self.assertEqual(nx_browse.classify_browse_action("click", "Next page"), "SAFE")

    def test_transactional_target_click_is_gated(self):
        # defense: a plain click whose TARGET reads transactional is GATED even if under-labelled.
        for tgt in ["Buy now", "Checkout", "Place order", "Add to cart", "Complete purchase", "Subscribe"]:
            self.assertEqual(nx_browse.classify_browse_action("click", tgt), "GATED", tgt)

    def test_unknown_action_is_default_closed(self):
        # posture holds: an action NX doesn't recognize as a read/type is NEVER auto-fired (never SAFE).
        for k in ["frobnicate", "xyzzy", "", None, "click_pay_now", "wire_funds"]:
            self.assertNotEqual(nx_browse.classify_browse_action(k), "SAFE", repr(k))

    def test_playwright_is_optional(self):
        # the module imports without playwright; availability is reported, install is guided.
        self.assertIn(nx_browse.playwright_available(), (True, False))
        self.assertTrue(nx_browse.install_hint())

    def test_browse_url_rejects_empty(self):
        r = nx_browse.browse_url("", watch=False)
        self.assertFalse(r["ok"])
        self.assertEqual(r["error"], "empty_url")

    def test_plan_next_action_parses_and_is_failsafe(self):
        # clean json → the action
        a = nx_browse.plan_next_action("t", {"url": "x", "title": "y", "text": "z"}, [],
                                       lambda p: '{"kind":"click","target":"Next","why":"go"}')
        self.assertEqual(a["kind"], "click")
        self.assertEqual(a["target"], "Next")
        # json embedded in prose → still extracted
        a = nx_browse.plan_next_action("t", {}, [], lambda p: 'Sure — {"kind":"navigate","target":"https://x.com"} ok')
        self.assertEqual(a["kind"], "navigate")
        # FAIL-SAFE: unparseable reply → done (never act blindly)
        self.assertEqual(nx_browse.plan_next_action("t", {}, [], lambda p: "no json here")["kind"], "done")

        # FAIL-SAFE: model error → done
        def _boom(_p):
            raise RuntimeError("model down")
        self.assertEqual(nx_browse.plan_next_action("t", {}, [], _boom)["kind"], "done")

    @unittest.skipUnless(nx_browse.playwright_available(), "needs playwright + a browser")
    def test_autonomous_loop_navigates_then_gates_a_buy(self):
        # END-TO-END: a deterministic "model" drives the FULL loop on a real browser — navigate A→B (SAFE, fires),
        # then attempt a purchase (GATED, denied → NOT fired), then done. The gate governs the autonomous run.
        import os
        import tempfile
        d = tempfile.mkdtemp()
        b_url = "file://" + os.path.join(d, "b.html")
        with open(os.path.join(d, "a.html"), "w") as fh:
            fh.write("<html><head><title>Page A</title></head><body><h1>Page A</h1></body></html>")
        with open(os.path.join(d, "b.html"), "w") as fh:
            fh.write("<html><head><title>Page B</title></head><body><h1>Page B</h1>"
                     "<button onclick=\"document.title='BOUGHT'\">Buy</button></body></html>")
        script = iter([
            '{"kind":"navigate","target":"%s","why":"go to B"}' % b_url,
            '{"kind":"click_buy","target":"Buy","why":"purchase it"}',
            '{"kind":"done","why":"blocked at checkout"}',
        ])
        planner = lambda t, o, h: nx_browse.plan_next_action(t, o, h, lambda prompt: next(script, '{"kind":"done"}'))
        r = nx_browse.browse_task("file://" + os.path.join(d, "a.html"), "buy the thing on page B",
                                  planner=planner, confirm=lambda a: False, watch=False, max_steps=6)
        self.assertTrue(r["ok"], r.get("error"))
        kinds = [(s["result"]["kind"], s["result"]["verdict"], s["result"]["executed"]) for s in r["steps"]]
        self.assertIn(("navigate", "SAFE", True), kinds)              # it navigated A→B on its own
        buy = [s for s in r["steps"] if s["result"]["kind"] == "click_buy"][0]
        self.assertEqual(buy["result"]["verdict"], "GATED")            # the purchase was gated
        self.assertFalse(buy["result"]["executed"])                    # denied → NOT bought
        self.assertIn("Page B", (r.get("final") or {}).get("text", ""))  # ended on B, never BOUGHT

    @unittest.skipUnless(nx_browse.playwright_available(), "needs playwright + a browser")
    def test_browse_task_loop_gates_a_transaction(self):
        # the agentic loop drives a real page: a SAFE fill executes; a GATED buy (denied) does NOT fire.
        import os
        import tempfile
        html = ('<html><body><input id="q" type="text">'
                '<button onclick="document.title=\'BOUGHT\'">Buy now</button></body></html>')
        f = os.path.join(tempfile.mkdtemp(), "t.html")
        with open(f, "w") as fh:
            fh.write(html)
        plan = iter([{"kind": "fill", "target": "#q", "value": "stand"},
                     {"kind": "click", "target": "Buy now"},
                     {"kind": "done"}])
        r = nx_browse.browse_task("file://" + f, "buy a stand",
                                  planner=lambda *a: next(plan, {"kind": "done"}),
                                  confirm=lambda a: False, watch=False, max_steps=5)
        self.assertTrue(r["ok"], r.get("error"))
        results = {s["result"]["kind"]: s["result"] for s in r["steps"]}
        self.assertTrue(results["fill"]["executed"])          # typing is SAFE → executed
        self.assertEqual(results["click"]["verdict"], "GATED")  # 'Buy now' caught by the target-defense
        self.assertFalse(results["click"]["executed"])         # denied → NOT bought


if __name__ == "__main__":
    unittest.main()


class TestGotoRetry(unittest.TestCase):
    """The transient-retry primitive on navigation (parity with the Nexplora code agent's tool retry)."""

    class _Page:
        def __init__(self, fail_times, exc_text):
            self.calls = 0
            self.fail_times = fail_times
            self.exc_text = exc_text

        def goto(self, url, **kw):
            self.calls += 1
            if self.calls <= self.fail_times:
                raise RuntimeError(self.exc_text)
            return {"ok": True, "url": url}

    def test_transient_failure_retries_then_succeeds(self):
        page = self._Page(fail_times=1, exc_text="Timeout 30000ms exceeded")
        r = nx_browse._goto_with_retry(page, "https://x.test", tool="browse_url")
        self.assertEqual(page.calls, 2)  # one retry
        self.assertTrue(r["ok"])

    def test_deterministic_failure_raises_immediately(self):
        page = self._Page(fail_times=99, exc_text="net::ERR_NAME_NOT_RESOLVED bad host")
        with self.assertRaises(RuntimeError):
            nx_browse._goto_with_retry(page, "https://nope.test", tool="browse_url")
        self.assertEqual(page.calls, 1)  # no retry on a non-transient error

    def test_persistent_transient_exhausts_retries_then_raises(self):
        page = self._Page(fail_times=99, exc_text="Connection reset by peer")
        with self.assertRaises(RuntimeError):
            nx_browse._goto_with_retry(page, "https://x.test", tool="browse_url")
        self.assertEqual(page.calls, 3)  # first + 2 backoff retries
