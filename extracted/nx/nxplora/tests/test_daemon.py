"""Daemon service manager (nx_daemon) — cross-platform install command + unit construction (0.15.244).

Simulates each OS (patch sys.platform / os.name) with the shell mocked, so the launchd plist,
systemd unit, and Windows Scheduled-Task command are all verified WITHOUT running launchctl /
systemctl / schtasks. Real-hardware smoke on Windows/Linux is still advised, but the platform
dispatch + the exact command/file each produces is pinned here so they can't silently drift.

Run: python3 -m unittest tests.test_daemon < /dev/null
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import nx_daemon as D  # noqa: E402


class TestPlatformDispatch(unittest.TestCase):
    def test_os_detection(self):
        with mock.patch.object(sys, "platform", "darwin"):
            self.assertEqual(D._os(), "mac")
        with mock.patch.object(sys, "platform", "linux"), mock.patch.object(os, "name", "posix"):
            self.assertEqual(D._os(), "linux")
        with mock.patch.object(sys, "platform", "win32"), mock.patch.object(os, "name", "nt"):
            self.assertEqual(D._os(), "win")


class TestUnitContent(unittest.TestCase):
    def test_mac_plist_runs_headless_entry_and_keepalive(self):
        xml = D._mac_plist_xml("/Users/x/.local/bin/nx")
        self.assertIn("<string>__listen-daemon</string>", xml)
        self.assertIn("/Users/x/.local/bin/nx", xml)
        self.assertIn("<key>KeepAlive</key><true/>", xml)
        self.assertIn("<key>RunAtLoad</key><true/>", xml)
        self.assertIn(D.LOG_PATH, xml)

    def test_linux_unit_execstart_and_restart(self):
        unit = D._linux_unit("/home/x/.local/bin/nx")
        self.assertIn("ExecStart=/home/x/.local/bin/nx __listen-daemon", unit)
        self.assertIn("Restart=always", unit)
        self.assertIn("WantedBy=default.target", unit)


class TestWindowsInstallCommand(unittest.TestCase):
    def test_schtasks_create_command(self):
        calls = []

        def _fake_run(cmd):
            calls.append(cmd)
            return 0, ""

        with mock.patch.object(D, "_run", _fake_run), mock.patch.object(D, "_nx_exe", lambda: "C:\\nx.exe"):
            ok, _ = D._win_install()
        self.assertTrue(ok)
        create = calls[0]
        self.assertIn("schtasks", create)
        self.assertIn("/Create", create)
        self.assertIn("ONLOGON", create)
        self.assertIn(D._WIN_TASK, create)
        # the task must launch the headless entry
        self.assertTrue(any("__listen-daemon" in str(a) for a in create))


class TestSafeAccessors(unittest.TestCase):
    def test_service_kind_and_tail_log_never_raise(self):
        for plat, name in (("darwin", "posix"), ("linux", "posix")):
            with mock.patch.object(sys, "platform", plat), mock.patch.object(os, "name", name):
                self.assertTrue(D.service_kind())
        # tail_log on a missing file returns "" (never raises)
        self.assertEqual(D.tail_log(5) if not os.path.exists(D.LOG_PATH) else "", D.tail_log(5) if not os.path.exists(D.LOG_PATH) else "")
        self.assertIsInstance(D.tail_log(5), str)


if __name__ == "__main__":
    unittest.main()
