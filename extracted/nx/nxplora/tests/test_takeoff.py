"""/takeoff loop — end-to-end ROUTING proof (the wiring the unit tests didn't cover).

Drives one pass of _run_listen(once=True) with the network + creds mocked, and asserts the
three routes that matter:
  1. a real PERSON's email        → REPLY to that person (the sender);
  2. an automated NOTIFICATION     → ALERT the OPERATOR (their own address), never the bot;
  3. a Telegram message            → REPLY on Telegram via the agent's bot.
Also confirms the session PREFLIGHT refuses when the token is expired (no dispatch on a dead
session — the bug that made agents "read but never answer").

Run: python3 -m unittest tests.test_takeoff < /dev/null
"""
import base64
import json
import os
import sys
import time
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import nx_cli  # noqa: E402


def _tok(exp_delta):
    payload = base64.urlsafe_b64encode(json.dumps({"exp": int(time.time()) + exp_delta}).encode()).decode().rstrip("=")
    return f"h.{payload}.s"


class TakeoffRouting(unittest.TestCase):
    def _run_one(self, incoming_email, incoming_tg):
        sends = {"email": [], "telegram": []}
        bind = {"name": "vinny", "display": "Vinny", "channels": {
            "email": {"handle": "agent@nexplora.ai", "host": "smtp.gmail.com", "port": 587},
            "telegram": {"handle": "8948", "offset": None},
        }}
        cfg = {"token": _tok(3600), "account": "victor@nexplora.ai"}

        with mock.patch.object(nx_cli, "_load_user_items", lambda k: [dict(bind)] if k == "agent-channels" else []), \
             mock.patch.object(nx_cli, "load_config", lambda: dict(cfg)), \
             mock.patch.object(nx_cli, "refresh_token_if_needed", lambda c, **k: c), \
             mock.patch.object(nx_cli, "_save_user_item", lambda *a, **k: True), \
             mock.patch("nx_channels.kc_get", lambda name: "secret"), \
             mock.patch.object(nx_cli, "_agent_email_answer", lambda *a, **k: "Here is the answer."), \
             mock.patch("nx_inbox.fetch_new", lambda *a, **k: list(incoming_email)), \
             mock.patch("nx_inbox.fetch_telegram_new", lambda *a, **k: (list(incoming_tg), 999)), \
             mock.patch.object(nx_cli, "_send_as_agent_email",
                               lambda frm, host, port, pwd, to, subj, body, **k: sends["email"].append({"to": to, "subj": subj})), \
             mock.patch.object(nx_cli, "_send_as_agent_telegram",
                               lambda tok, chat_id, text: sends["telegram"].append({"chat_id": chat_id})):
            nx_cli._run_listen(cfg, once=True, poll_s=1, confirm=False)
        return sends

    def test_person_email_replies_to_sender(self):
        person = {"from_addr": "sarah@acme.com", "subject": "quick q", "body": "can you help?",
                  "message_id": "<1@x>", "references": "", "is_notification": False}
        sends = self._run_one([person], [])
        self.assertEqual([s["to"] for s in sends["email"]], ["sarah@acme.com"])
        self.assertTrue(sends["email"][0]["subj"].lower().startswith("re:"))

    def test_notification_alerts_operator_not_the_bot(self):
        note = {"from_addr": "notifications@github.com", "subject": "PR run failed", "body": "the proof suite failed",
                "message_id": "<2@gh>", "references": "", "is_notification": True}
        sends = self._run_one([note], [])
        # goes to the OPERATOR's own address, never back to notifications@github.com
        self.assertEqual([s["to"] for s in sends["email"]], ["victor@nexplora.ai"])
        self.assertNotIn("notifications@github.com", [s["to"] for s in sends["email"]])

    def test_telegram_message_replies_on_telegram(self):
        tg = {"text": "Sup Vinny", "who": "Victor", "chat_id": "8948", "message_id": 5}
        sends = self._run_one([], [tg])
        self.assertEqual([s["chat_id"] for s in sends["telegram"]], ["8948"])

    def test_expired_session_refuses_dispatch(self):
        """A token that EXISTS but is expired must not dispatch — else agents read and never answer."""
        bind = {"name": "vinny", "display": "Vinny",
                "channels": {"email": {"handle": "a@b.com", "host": "smtp.gmail.com", "port": 587}}}
        sent = []
        with mock.patch.object(nx_cli, "_load_user_items", lambda k: [bind] if k == "agent-channels" else []), \
             mock.patch.object(nx_cli, "refresh_token_if_needed", lambda c, **k: c), \
             mock.patch("nx_inbox.fetch_new", lambda *a, **k: [{"from_addr": "x@y.com", "subject": "s", "body": "b",
                                                                "message_id": "<1>", "references": "", "is_notification": False}]), \
             mock.patch.object(nx_cli, "_send_as_agent_email", lambda *a, **k: sent.append(1)):
            nx_cli._run_listen({"token": _tok(-99999), "account": "v@x.com"}, once=True, confirm=False)
        self.assertEqual(sent, [], "dispatched on an expired session")


if __name__ == "__main__":
    unittest.main()
