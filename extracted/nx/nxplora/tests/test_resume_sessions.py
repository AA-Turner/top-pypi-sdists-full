"""/resume shows the real sessions, and the menu stops offering sign-in to signed-in people.

/resume used to load the newest transcript silently and print "Resumed — N messages from your last
session are back in context." With several sessions on disk, "your last session" was a guess the CLI
made and then reported as fact — unseeable, uncheckable, unsteerable. These pin the listing that
replaces it.
"""
import json
import os
import sys
import tempfile
import time
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_cli  # noqa: E402
import nx_slash_menu  # noqa: E402


def _write_log(dirpath, name, msgs, age_s=0):
    p = os.path.join(dirpath, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        json.dump({"messages": msgs}, f)
    if age_s:
        t = time.time() - age_s
        os.utime(p, (t, t))
    return p


TURNS_A = [{"role": "user", "content": "wire the X publish path"},
           {"role": "assistant", "content": "done"}]
TURNS_B = [{"role": "user", "content": "fix the twilio webhook"},
           {"role": "assistant", "content": "ok"},
           {"role": "user", "content": "and the A2P status"}]


class SessionListing(unittest.TestCase):
    def test_sessions_are_listed_newest_first_with_a_real_title(self):
        with tempfile.TemporaryDirectory() as d:
            logs = os.path.join(d, "session-logs")
            _write_log(logs, "old/a.json", TURNS_A, age_s=7200)
            _write_log(logs, "new/b.json", TURNS_B, age_s=10)
            with mock.patch.object(nx_cli, "NX_DIR", d), \
                 mock.patch.object(nx_cli, "_AUTOSAVE_PATH", os.path.join(d, "none.json")):
                out = nx_cli._list_saved_sessions()

        self.assertEqual(len(out), 2)
        # The title is the operator's OWN first line — that is what they remember a session by,
        # not a filename or an id.
        self.assertEqual(out[0]["title"], "fix the twilio webhook")
        self.assertEqual(out[1]["title"], "wire the X publish path")
        self.assertEqual(out[0]["turns"], 3)
        # A blank date would mean the timestamp path silently failed into its except.
        self.assertTrue(out[0]["when"], "each session must carry a readable date")

    def test_the_live_autosave_is_offered_first(self):
        with tempfile.TemporaryDirectory() as d:
            logs = os.path.join(d, "session-logs")
            _write_log(logs, "x/a.json", TURNS_A, age_s=5)
            auto = os.path.join(d, "last.json")
            with open(auto, "w") as f:
                json.dump(TURNS_B, f)   # autosave is a bare array, not a dict payload
            with mock.patch.object(nx_cli, "NX_DIR", d), \
                 mock.patch.object(nx_cli, "_AUTOSAVE_PATH", auto):
                out = nx_cli._list_saved_sessions()

        # "Continue where I left off" is the autosave, so it leads regardless of mtime ordering.
        self.assertEqual(out[0]["path"], auto)
        self.assertEqual(out[0]["title"], "fix the twilio webhook")

    def test_empty_and_unreadable_sessions_are_not_offered(self):
        with tempfile.TemporaryDirectory() as d:
            logs = os.path.join(d, "session-logs")
            _write_log(logs, "e/empty.json", [])
            _write_log(logs, "e/sys-only.json", [{"role": "system", "content": "x"}])
            with open(os.path.join(logs, "e", "broken.json"), "w") as f:
                f.write("{not json")
            with mock.patch.object(nx_cli, "NX_DIR", d), \
                 mock.patch.object(nx_cli, "_AUTOSAVE_PATH", os.path.join(d, "none.json")):
                out = nx_cli._list_saved_sessions()
        # Offering a session that would resume nothing is the original bug in a new place.
        self.assertEqual(out, [])

    def test_no_sessions_at_all_is_an_empty_list_not_an_error(self):
        with tempfile.TemporaryDirectory() as d:
            with mock.patch.object(nx_cli, "NX_DIR", d), \
                 mock.patch.object(nx_cli, "_AUTOSAVE_PATH", os.path.join(d, "none.json")):
                self.assertEqual(nx_cli._list_saved_sessions(), [])


class SessionRead(unittest.TestCase):
    def test_reads_both_the_dict_payload_and_the_bare_array(self):
        with tempfile.TemporaryDirectory() as d:
            p1 = _write_log(d, "logs/a.json", TURNS_A)
            p2 = os.path.join(d, "auto.json")
            with open(p2, "w") as f:
                json.dump(TURNS_B, f)
            self.assertEqual(len(nx_cli._session_messages_at(p1)), 2)
            self.assertEqual(len(nx_cli._session_messages_at(p2)), 3)

    def test_a_missing_file_reads_as_empty_rather_than_raising(self):
        # /resume checks for this and says so — resuming nothing while reporting success is what
        # the old behaviour did.
        self.assertEqual(nx_cli._session_messages_at("/nope/does/not/exist.json"), [])


class MenuHygiene(unittest.TestCase):
    def _cmds(self):
        # SECTIONS[*]["commands"][*]["cmd"] — read from the real structure, and asserted non-empty
        # below so a rename turns these into failures rather than silent skips. A menu test that
        # skips proves nothing, which is the shape of vacuous test this session keeps finding.
        out = []
        for group in getattr(nx_slash_menu, "SECTIONS", []):
            for item in group.get("commands", []):
                out.append(item.get("cmd"))
        return out

    def test_login_is_not_offered_to_an_already_signed_in_operator(self):
        cmds = self._cmds()
        self.assertTrue(cmds, "the menu must expose commands — a skip here would prove nothing")
        self.assertNotIn("/login", cmds)
        # …but the repair path itself must survive: /login stays a typed command for a session that
        # expired mid-REPL, which is the one case it exists for.
        self.assertIn('cmd=="/login"', open(
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "nx_cli.py"),
            encoding="utf-8").read().replace(" ", ""))

    def test_logout_and_resume_are_still_offered(self):
        cmds = self._cmds()
        self.assertTrue(cmds, "the menu must expose commands")
        self.assertIn("/logout", cmds)
        self.assertIn("/resume", cmds)


if __name__ == "__main__":
    unittest.main()
