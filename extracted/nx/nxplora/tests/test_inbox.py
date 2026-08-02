"""Inbound email (nx_inbox) — the receive half of /supply email (0.15.242).

The load-bearing invariant is LOOP-SAFETY when the operator's address == the agent's address
(victor@nexplora.ai sends AS the agent AND replies FROM it): the agent must answer the human's
reply but NEVER its own sends. That's the X-NX-Agent header check — pinned here so it can't
regress into an email loop.

Run: python3 -m unittest tests.test_inbox < /dev/null
"""
import os
import sys
import unittest
from email.mime.text import MIMEText

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import nx_inbox  # noqa: E402


class TestImapHostMapping(unittest.TestCase):
    def test_known_and_generic(self):
        self.assertEqual(nx_inbox.imap_host_for("smtp.gmail.com"), "imap.gmail.com")
        self.assertEqual(nx_inbox.imap_host_for("smtp-mail.outlook.com"), "outlook.office365.com")
        self.assertEqual(nx_inbox.imap_host_for("smtp.mail.yahoo.com"), "imap.mail.yahoo.com")
        # custom domain / unknown provider → generic smtp.X -> imap.X
        self.assertEqual(nx_inbox.imap_host_for("smtp.myco.io"), "imap.myco.io")


class TestLoopSafety(unittest.TestCase):
    def _msg(self, frm, to, headers=None, body="hi"):
        m = MIMEText(body)
        m["From"] = frm
        m["To"] = to
        for k, v in (headers or {}).items():
            m[k] = v
        return m

    def test_agent_own_send_is_skipped_even_when_from_equals_to(self):
        # The exact same-address case from the operator's setup.
        own = self._msg("victor@nexplora.ai", "victor@nexplora.ai", {"X-NX-Agent": "vinny"})
        self.assertTrue(nx_inbox.is_own_or_auto(own))

    def test_human_reply_from_same_address_is_answered(self):
        human = self._msg("victor@nexplora.ai", "victor@nexplora.ai", body="Hey nx you hear this? Reply!")
        self.assertFalse(nx_inbox.is_own_or_auto(human))

    def test_bounce_and_autoreply_skipped(self):
        self.assertTrue(nx_inbox.is_own_or_auto(self._msg("mailer-daemon@google.com", "x@y.com")))
        self.assertTrue(nx_inbox.is_own_or_auto(self._msg("noreply@service.com", "x@y.com")))
        self.assertTrue(nx_inbox.is_own_or_auto(self._msg("bot@x.com", "y@y.com", {"Auto-Submitted": "auto-replied"})))


class TestNotificationDetection(unittest.TestCase):
    """A GitHub/CI alert must be flagged so the agent briefs the OPERATOR instead of replying to a bot."""

    def _msg(self, frm, headers=None, subj="x"):
        m = MIMEText("body")
        m["From"] = frm
        m["To"] = "victor@nexplora.ai"
        m["Subject"] = subj
        for k, v in (headers or {}).items():
            m[k] = v
        return m

    def test_github_notification_flagged(self):
        # the real shape that hit the operator: notifications@github.com with List-Id
        gh = self._msg("notifications@github.com",
                       {"List-Id": "Nexploraai/nexplora-v2 <nexplora-v2.Nexploraai.github.com>",
                        "X-GitHub-Reason": "subscribed"},
                       subj="[Nexploraai/nexplora-v2] PR run failed: proof-suite")
        self.assertTrue(nx_inbox.looks_like_notification(gh))

    def test_ci_and_bulk_and_machine_locals_flagged(self):
        self.assertTrue(nx_inbox.looks_like_notification(self._msg("ci@buildbot.example")))
        self.assertTrue(nx_inbox.looks_like_notification(self._msg("alerts@monitoring.io")))
        self.assertTrue(nx_inbox.looks_like_notification(self._msg("x@y.com", {"Precedence": "bulk"})))
        self.assertTrue(nx_inbox.looks_like_notification(self._msg("x@y.com", {"List-Unsubscribe": "<mailto:u@y.com>"})))

    def test_real_person_not_flagged(self):
        # a colleague writing a normal email must still get a REPLY
        self.assertFalse(nx_inbox.looks_like_notification(self._msg("sarah@acme.com", subj="quick question")))
        self.assertFalse(nx_inbox.looks_like_notification(self._msg("victor@nexplora.ai", subj="can you check this")))

    def test_vendor_agnostic_any_system_not_just_github(self):
        """GitHub is only an EXAMPLE — CI, monitoring, ticketing, billing, SaaS alerts from any
        company must route to the operator too."""
        for addr in ("builds@circleci.com", "jenkins@build.corp", "alerts@datadoghq.com",
                     "no-reply@sentry.io", "team.notifications@atlassian.net", "billing@stripe.com",
                     "alerts+prod@pagerduty.com", "noreply@linear.app", "uptime@statuspage.io",
                     "ticket-123@jira.corp"):
            self.assertTrue(nx_inbox.looks_like_notification(self._msg(addr)), f"missed: {addr}")

    def test_generic_bulk_headers_flagged_regardless_of_sender(self):
        for hdr in ({"List-Unsubscribe": "<mailto:u@v.io>"}, {"Precedence": "bulk"},
                    {"Feedback-ID": "1:2:3"}, {"Auto-Submitted": "auto-generated"},
                    {"X-Campaign-Id": "abc"}):
            self.assertTrue(nx_inbox.looks_like_notification(self._msg("hello@vendor.io", hdr)), f"missed: {hdr}")

    def test_no_reply_reply_to_flagged(self):
        m = self._msg("person@vendor.com")
        m["Reply-To"] = "no-reply@vendor.com"
        self.assertTrue(nx_inbox.looks_like_notification(m))

    def test_people_with_ordinary_addresses_never_flagged(self):
        """FALSE POSITIVES are the dangerous failure — a person flagged as a bot gets NO reply."""
        for addr in ("j.smith@bigco.co.uk", "dev-lead@startup.io", "maria.garcia@client.com",
                     "ceo@partner.org", "sarah@acme.com"):
            self.assertFalse(nx_inbox.looks_like_notification(self._msg(addr)), f"false positive: {addr}")


class TestStripQuotes(unittest.TestCase):
    def test_trims_quoted_history(self):
        q = "Yes I hear you.\n\nOn Sat, Jul 25 2026 <victor@nexplora.ai> wrote:\n> This is Vinny."
        self.assertEqual(nx_inbox.strip_quotes(q), "Yes I hear you.")

    def test_no_quotes_passthrough(self):
        self.assertEqual(nx_inbox.strip_quotes("just a line"), "just a line")


if __name__ == "__main__":
    unittest.main()
