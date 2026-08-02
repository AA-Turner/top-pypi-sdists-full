"""GRAIL Phase 5 follow-up #1 — per-operator report-back channels (nx_message).

Proves the channel model (configure → state → toggle), the fan-out to ACTIVE+configured channels only, honest
per-channel failure reporting, and the /message command (show/toggle/imessage). Isolated: temp config +
in-memory Keychain + fake senders (no network, no real Keychain). Run: python3 nx/cli/tests/test_nx_message.py
"""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_message as M


def _isolate(tmp):
    M._CONFIG = os.path.join(tmp, "config.json")
    kc = {}
    M.kc_get = lambda s: kc.get(s)
    M.kc_set = lambda s, v: (kc.__setitem__(s, v) or True)
    M.kc_delete = lambda s: (kc.pop(s, None) or True)
    return kc


def test_configure_and_state():
    with tempfile.TemporaryDirectory() as d:
        _isolate(d)
        st = M.channels_state()
        assert all(not st[c]["configured"] for c in M.CHANNELS)         # nothing set yet
        M.configure_imessage("+15551234")                               # no secret
        M.configure_telegram("tok", chat_id="99")                       # token → keychain
        st = M.channels_state()
        assert st["imessage"]["configured"] and st["imessage"]["active"] and st["imessage"]["to"] == "+15551234"
        assert st["telegram"]["configured"] and st["telegram"]["active"] and st["telegram"]["chat_id"] == "99"
        assert not st["email"]["configured"] and not st["whatsapp"]["configured"]


def test_set_active_toggle():
    with tempfile.TemporaryDirectory() as d:
        _isolate(d)
        M.configure_imessage("+1")
        assert M.channels_state()["imessage"]["active"]
        M.set_active("imessage", False)
        assert not M.channels_state()["imessage"]["active"]
        M.set_active("imessage", True)
        assert M.channels_state()["imessage"]["active"]


def test_send_report_fans_out_to_active_only():
    with tempfile.TemporaryDirectory() as d:
        _isolate(d)
        M.configure_imessage("+1")
        M.configure_telegram("tok", chat_id="9")
        # email + whatsapp are NOT configured → must be skipped
        sent = []
        M._SENDERS = {c: (lambda text, entry, _c=c: sent.append(_c)) for c in M.CHANNELS}
        res = M.send_report("hi")
        assert set(res) == {"telegram", "imessage"}
        assert set(sent) == {"telegram", "imessage"} and all(res[c]["sent"] for c in res)
        assert M.any_delivered(res)


def test_send_report_honest_on_failure():
    with tempfile.TemporaryDirectory() as d:
        _isolate(d)
        M.configure_imessage("+1")
        def boom(text, entry):
            raise RuntimeError("nope-429")
        M._SENDERS = dict(M._SENDERS, imessage=boom)
        res = M.send_report("hi")
        assert res["imessage"]["sent"] is False and "nope-429" in res["imessage"]["error"]
        assert not M.any_delivered(res)          # nothing delivered → surfaced, not hidden


def test_inactive_channel_not_sent():
    with tempfile.TemporaryDirectory() as d:
        _isolate(d)
        M.configure_imessage("+1")
        M.set_active("imessage", False)          # configured but OFF
        sent = []
        M._SENDERS = {c: (lambda text, entry, _c=c: sent.append(_c)) for c in M.CHANNELS}
        assert M.send_report("hi") == {} and sent == []


def test_handle_command_show_toggle_imessage():
    with tempfile.TemporaryDirectory() as d:
        _isolate(d)
        out = M.handle_message_command(["imessage", "+15550000"])
        assert "text" in out and M.channels_state()["imessage"]["to"] == "+15550000"
        assert "off" in M.handle_message_command(["off", "imessage"]).lower()
        assert not M.channels_state()["imessage"]["active"]
        show = M.handle_message_command([])
        assert "Report-back channels" in show and "imessage" in show
        assert "usage" in M.handle_message_command(["on"]).lower()   # missing channel arg


def test_safe_port_never_crashes():
    # regression: `/message email` with a non-numeric port ("?") used to raise
    # ValueError: invalid literal for int() with base 10: '?'
    assert M._safe_port("?") == 587
    assert M._safe_port("") == 587 and M._safe_port(None) == 587 and M._safe_port("abc") == 587
    assert M._safe_port("465") == 465 and M._safe_port(" 25 ") == 25


def test_smtp_host_derived_from_address():
    # the simplified email setup derives the SMTP host so the operator never types it
    assert M._smtp_host_for("victorsetton3@gmail.com") == "smtp.gmail.com"
    assert M._smtp_host_for("x@icloud.com") == "smtp.mail.me.com"
    assert M._smtp_host_for("x@outlook.com") == "smtp-mail.outlook.com"
    assert M._smtp_host_for("hello@nexplora.ai") == "smtp.nexplora.ai"   # fallback smtp.<domain>


def test_email_byok_smtp_is_simple_and_crash_free():
    # `/message email smtp` (advanced BYOK): 3 prompts (email, to, app-password) — no SMTP
    # host/port typing — and a "?" can't crash it.
    with tempfile.TemporaryDirectory() as d:
        _isolate(d)
        answers = iter(["me@gmail.com", ""])            # address, then Enter (to = same address)
        out = M.handle_message_command(["email", "smtp"], prompt=lambda _l: next(answers),
                                       prompt_secret=lambda _l: "app-pass-1234")
        assert "configured + active" in out and "smtp.gmail.com" in out
        st = M.channels_state()
        assert st["email"]["configured"] and st["email"]["active"] and st["email"]["hosted"] is False
        assert st["email"]["host"] == "smtp.gmail.com" and st["email"]["port"] == 587


def test_email_default_is_nexplora_hosted():
    # default `/message email` = hosted: just your address, no SMTP creds.
    with tempfile.TemporaryDirectory() as d:
        _isolate(d)
        out = M.handle_message_command(["email"], prompt=lambda _l: "op@x.com", prompt_secret=lambda _l: "")
        assert "via Nexplora" in out
        st = M.channels_state()
        assert st["email"]["hosted"] and st["email"]["configured"] and st["email"]["active"]
        assert st["email"]["to"] == "op@x.com"


def test_text_default_hosted_and_local_opt():
    with tempfile.TemporaryDirectory() as d:
        _isolate(d)
        M.handle_message_command(["text", "9177246262"])                 # default → hosted SMS
        assert M.channels_state()["imessage"]["hosted"] is True
        M.handle_message_command(["text", "local", "+15551234"])         # advanced → local iMessage
        st = M.channels_state()
        assert st["imessage"]["hosted"] is False and st["imessage"]["to"] == "+15551234"


def test_hosted_send_posts_to_relay():
    # a hosted channel routes through /api/nexplora/notify with the operator's bearer token — no creds.
    # Call the senders DIRECTLY (not send_report) so a sibling test's _SENDERS monkeypatch can't hide this.
    import types, json
    with tempfile.TemporaryDirectory() as d:
        _isolate(d)
        json.dump({"token": "TOK"}, open(M._CONFIG, "w"))     # the token the relay reads
        captured = {}

        class _R:
            status_code = 200
            def json(self):
                return {"ok": True, "messageId": "m1"}

        fake = types.ModuleType("requests")
        fake.post = lambda url, json=None, headers=None, timeout=None: (
            captured.update(url=url, json=json, auth=(headers or {}).get("Authorization")) or _R())
        old_req, sys.modules["requests"] = sys.modules.get("requests"), fake
        try:
            M._send_email("hello report", {"to": "op@x.com", "hosted": True})       # hosted email → relay
            assert captured["url"].endswith("/api/nexplora/notify")
            assert captured["json"] == {"channel": "email", "to": "op@x.com", "text": "hello report", "subject": "NX report"}
            assert captured["auth"] == "Bearer TOK"
            captured.clear()
            M._send_imessage("ping", {"to": "9177246262", "hosted": True})          # hosted text → relay SMS
            assert captured["json"] == {"channel": "sms", "to": "9177246262", "text": "ping"}
        finally:
            if old_req is not None:
                sys.modules["requests"] = old_req
            else:
                sys.modules.pop("requests", None)


if __name__ == "__main__":
    for n, f in sorted((n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)):
        f(); print("  ✓ {}".format(n))
    print("ALL PHASE-5 #1 REPORT-BACK-CHANNELS PROOFS PASS")
