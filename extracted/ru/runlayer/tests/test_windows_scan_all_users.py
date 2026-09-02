"""Tests for the SYSTEM all-users scan orchestration (windows_users.py).

Covers the profile filter (the ported S-1-5-21 / S-1-12-1 SID gate), username
resolution, the SYSTEM env-pointed child env, the SYSTEM guard, and the
``run_all_users_scan`` orchestrator with mocked launchers (launcher selection,
per-profile resilience, aggregated exit). The ctypes/winreg Win32 seams
(``_token_user_sid``, ``active_session_sids``, ``launch_scan_as_user``, the live
launchers) are monkeypatched — they can't be exercised off-Windows.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from runlayer_cli.scan import windows_users
from runlayer_cli.scan.windows_users import (
    EXIT_MISCONFIG,
    RealUserProfile,
    _profile_env,
    _scan_argv,
    enumerate_real_user_profiles,
    is_real_user_profile_sid,
    resolve_profile_username,
    run_all_users_scan,
    run_scan_as_system,
)


def _profile(
    sid: str, path: str = r"C:\Users\u", username: str = "u"
) -> RealUserProfile:
    return RealUserProfile(sid=sid, profile_path=Path(path), username=username)


# Resource caps are required keyword args on every launcher / orchestrator entry;
# the cases that aren't specifically about caps just pass this fixed set.
_CAPS = {"cpu_cores": 2, "max_cpu_percent": 50, "memory_limit_mb": 1024}


class TestIsRealUserProfileSid:
    def test_accepts_local_account_sid(self):
        assert is_real_user_profile_sid("S-1-5-21-111-222-333-1001", r"C:\Users\alice")

    def test_accepts_entra_account_sid(self):
        # The whole point of the rework: Entra S-1-12-1 SIDs are real users.
        assert is_real_user_profile_sid("S-1-12-1-111-222-333-444", r"C:\Users\bob")

    @pytest.mark.parametrize("sid", ["S-1-5-18", "S-1-5-19", "S-1-5-20"])
    def test_rejects_service_sids(self, sid: str):
        assert not is_real_user_profile_sid(sid, r"C:\Windows\x")

    def test_rejects_empty_profile_image_path(self):
        assert not is_real_user_profile_sid("S-1-5-21-1-2-3-1001", "")

    @pytest.mark.parametrize(
        "sid",
        [
            "",
            "not-a-sid",
            "S-1-5-32-544",  # builtin admins group
            "S-1-5-21-1-2-3",  # too few sub-authorities (no RID)
        ],
    )
    def test_rejects_malformed_or_non_user_sids(self, sid: str):
        assert not is_real_user_profile_sid(sid, r"C:\Users\x")


class TestResolveProfileUsername:
    def test_strips_entra_domain_prefix(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(
            windows_users, "_lookup_account_name", lambda sid: "AzureAD\\alice"
        )
        assert (
            resolve_profile_username("S-1-12-1-1-2-3-4", r"C:\Users\alice") == "alice"
        )

    def test_strips_local_domain_prefix(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(
            windows_users, "_lookup_account_name", lambda sid: "CORP\\bob"
        )
        assert resolve_profile_username("S-1-5-21-1-2-3-1001", r"C:\Users\bob") == "bob"

    def test_falls_back_to_profile_folder_when_unresolvable(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        # Deleted/orphaned account: SID no longer maps to a name.
        monkeypatch.setattr(windows_users, "_lookup_account_name", lambda sid: None)
        assert (
            resolve_profile_username("S-1-5-21-1-2-3-1001", r"C:\Users\ghost")
            == "ghost"
        )


class TestEnumerateRealUserProfiles:
    def test_filters_to_real_users_and_resolves_names(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.setattr(
            windows_users,
            "_iter_profile_list",
            lambda: [
                ("S-1-5-18", r"C:\Windows\system32\config\systemprofile"),  # service
                ("S-1-5-21-1-2-3-1001", r"C:\Users\alice"),  # local
                ("S-1-12-1-1-2-3-4", r"C:\Users\bob"),  # entra
                ("S-1-5-21-1-2-3-1002", ""),  # missing image -> dropped
            ],
        )
        monkeypatch.setattr(
            windows_users, "_lookup_account_name", lambda sid: None
        )  # force folder-leaf fallback

        profiles = enumerate_real_user_profiles()

        assert [p.sid for p in profiles] == [
            "S-1-5-21-1-2-3-1001",
            "S-1-12-1-1-2-3-4",
        ]
        assert [p.username for p in profiles] == ["alice", "bob"]
        assert profiles[0].profile_path == Path(r"C:\Users\alice")


class TestScanArgv:
    def test_default_includes_username_and_project_flags(self):
        argv = _scan_argv(
            "alice",
            scan_projects=True,
            project_timeout=60,
            project_depth=7,
            cpu_cores=2,
            max_cpu_percent=50,
            memory_limit_mb=1024,
        )
        assert argv == [
            "scan",
            "--username",
            "alice",
            "--project-timeout",
            "60",
            "--project-depth",
            "7",
            "--cpu-cores",
            "2",
            "--max-cpu-percent",
            "50",
            "--memory-limit-mb",
            "1024",
        ]

    def test_no_projects_appends_flag(self):
        argv = _scan_argv(
            "alice", scan_projects=False, project_timeout=60, project_depth=7, **_CAPS
        )
        assert "--no-projects" in argv

    def test_forwards_resource_caps(self):
        """Each per-profile child must carry the caps so it self-governs."""
        argv = _scan_argv(
            "alice",
            scan_projects=True,
            project_timeout=60,
            project_depth=7,
            cpu_cores=1,
            max_cpu_percent=25,
            memory_limit_mb=512,
        )
        assert argv[argv.index("--cpu-cores") + 1] == "1"
        assert argv[argv.index("--max-cpu-percent") + 1] == "25"
        assert argv[argv.index("--memory-limit-mb") + 1] == "512"

    @pytest.mark.parametrize(
        ("enabled", "expected_flag"),
        [
            (True, "--artifact-lookup-cache"),
            (False, "--no-artifact-lookup-cache"),
        ],
    )
    def test_forwards_explicit_artifact_cache_setting(
        self,
        enabled: bool,
        expected_flag: str,
    ):
        argv = _scan_argv(
            "alice",
            scan_projects=True,
            project_timeout=60,
            project_depth=7,
            artifact_lookup_cache=enabled,
            **_CAPS,
        )

        assert expected_flag in argv


class TestProfileEnv:
    def test_points_paths_at_profile_home(self):
        env = _profile_env(_profile("S-1-5-21-1-2-3-1001", r"C:\Users\alice", "alice"))

        assert env["USERPROFILE"] == r"C:\Users\alice"
        assert env["APPDATA"] == r"C:\Users\alice\AppData\Roaming"
        assert env["LOCALAPPDATA"] == r"C:\Users\alice\AppData\Local"
        assert env["HOMEDRIVE"] == "C:"
        assert env["HOMEPATH"] == r"\Users\alice"


class TestRunScanAsSystem:
    def test_passes_profile_env_and_username(self, monkeypatch: pytest.MonkeyPatch):
        captured: dict = {}

        def fake_run(argv, **kwargs):
            captured["argv"] = argv
            captured["env"] = kwargs.get("env")
            return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")

        monkeypatch.setattr(windows_users.subprocess, "run", fake_run)

        code = run_scan_as_system(
            _profile("S-1-5-21-1-2-3-1001", r"C:\Users\alice", "alice"),
            scan_projects=True,
            project_timeout=60,
            project_depth=7,
            timeout=180,
            **_CAPS,
        )

        assert code == 0
        assert "--username" in captured["argv"]
        assert "alice" in captured["argv"]
        assert "--no-artifact-lookup-cache" in captured["argv"]
        assert captured["env"]["USERPROFILE"] == r"C:\Users\alice"

    def test_timeout_is_nonzero(self, monkeypatch: pytest.MonkeyPatch):
        def fake_run(argv, **kwargs):
            raise subprocess.TimeoutExpired(cmd=argv, timeout=kwargs.get("timeout"))

        monkeypatch.setattr(windows_users.subprocess, "run", fake_run)

        code = run_scan_as_system(
            _profile("S-1-5-21-1-2-3-1001"),
            scan_projects=True,
            project_timeout=60,
            project_depth=7,
            timeout=180,
            **_CAPS,
        )
        assert code != 0


class TestLaunchScanAsUser:
    """The logged-on token launcher must hand ``CreateProcessAsUserW`` a *mutable*
    command-line buffer.

    The Unicode ``CreateProcessW`` / ``CreateProcessAsUserW`` is documented to
    write into ``lpCommandLine`` while parsing it, so the argument "cannot be a
    pointer to read-only memory ... the function may cause an access violation".
    ``ctypes.c_wchar_p(cmdline)`` wraps the immutable Python ``str`` buffer;
    ``ctypes.create_unicode_buffer(cmdline)`` allocates a writable wchar array
    that satisfies the Win32 contract. The ctypes ``windll`` seam is faked so the
    launcher runs off-Windows and we can inspect the argument it builds.
    """

    @staticmethod
    def _fake_windll() -> MagicMock:
        windll = MagicMock()
        windll.wtsapi32.WTSQueryUserToken.return_value = 1  # token acquired
        windll.userenv.CreateEnvironmentBlock.return_value = 0  # have_env False
        windll.advapi32.CreateProcessAsUserW.return_value = 1  # spawn ok
        windll.kernel32.WaitForSingleObject.return_value = 0  # _WAIT_OBJECT_0
        return windll

    def test_lp_command_line_is_writable_buffer_not_const_pointer(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        import ctypes

        windll = self._fake_windll()
        monkeypatch.setattr(ctypes, "windll", windll, raising=False)

        code = windows_users.launch_scan_as_user(
            3,
            _profile("S-1-12-1-1-2-3-4", r"C:\Users\alice", "alice"),
            scan_projects=True,
            project_timeout=60,
            project_depth=7,
            timeout=180,
            **_CAPS,
        )
        assert code == 0

        call = windll.advapi32.CreateProcessAsUserW.call_args
        lp_command_line = call.args[2]  # 3rd positional arg == lpCommandLine

        # create_unicode_buffer() yields a writable c_wchar Array; c_wchar_p does not.
        assert isinstance(lp_command_line, ctypes.Array)
        assert lp_command_line._type_ is ctypes.c_wchar
        assert not isinstance(lp_command_line, ctypes.c_wchar_p)

        expected = subprocess.list2cmdline(
            [
                sys.executable,
                *_scan_argv(
                    "alice",
                    scan_projects=True,
                    project_timeout=60,
                    project_depth=7,
                    **_CAPS,
                ),
            ]
        )
        assert lp_command_line.value == expected

    def test_lp_application_name_may_stay_const_pointer(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        # Only lpCommandLine is modified by the API; lpApplicationName is const,
        # so it correctly stays a c_wchar_p wrapping sys.executable.
        import ctypes

        windll = self._fake_windll()
        monkeypatch.setattr(ctypes, "windll", windll, raising=False)

        windows_users.launch_scan_as_user(
            3,
            _profile("S-1-12-1-1-2-3-4", r"C:\Users\alice", "alice"),
            scan_projects=True,
            project_timeout=60,
            project_depth=7,
            timeout=180,
            **_CAPS,
        )

        call = windll.advapi32.CreateProcessAsUserW.call_args
        lp_application_name = call.args[1]
        assert isinstance(lp_application_name, ctypes.c_wchar_p)
        assert lp_application_name.value == sys.executable

    def test_logged_on_scan_forwards_enabled_artifact_cache(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ):
        captured: dict[str, list[str]] = {}

        def fake_launch(_session_id: int, argv: list[str], _timeout: int) -> int:
            captured["argv"] = argv
            return 0

        monkeypatch.setattr(windows_users, "launch_argv_as_user", fake_launch)

        code = windows_users.launch_scan_as_user(
            3,
            _profile("S-1-12-1-1-2-3-4", r"C:\Users\alice", "alice"),
            scan_projects=True,
            project_timeout=60,
            project_depth=7,
            timeout=180,
            artifact_lookup_cache=True,
            **_CAPS,
        )

        assert code == 0
        assert "--artifact-lookup-cache" in captured["argv"]

    def test_wait_failed_terminates_child_and_raises(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        # WAIT_FAILED must not fall through to GetExitCodeProcess: the child
        # may still be alive, so STILL_ACTIVE (259) would be reported as a
        # spurious exit code while the process leaks.
        import ctypes

        windll = self._fake_windll()
        windll.kernel32.WaitForSingleObject.return_value = 0xFFFFFFFF  # WAIT_FAILED
        monkeypatch.setattr(ctypes, "windll", windll, raising=False)

        with pytest.raises(OSError, match="WaitForSingleObject failed"):
            windows_users.launch_argv_as_user(3, [sys.executable, "-c", "pass"], 60)

        windll.kernel32.TerminateProcess.assert_called_once()
        windll.kernel32.GetExitCodeProcess.assert_not_called()

    def test_wait_timeout_terminates_child_and_raises_timeout(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        import ctypes

        windll = self._fake_windll()
        windll.kernel32.WaitForSingleObject.return_value = 0x00000102  # WAIT_TIMEOUT
        monkeypatch.setattr(ctypes, "windll", windll, raising=False)

        with pytest.raises(TimeoutError):
            windows_users.launch_argv_as_user(3, [sys.executable, "-c", "pass"], 60)

        windll.kernel32.TerminateProcess.assert_called_once()
        windll.kernel32.GetExitCodeProcess.assert_not_called()


class TestApplyWin32Signatures:
    """F2 regression: every Win32 call must declare ``restype``/``argtypes``.

    Without an explicit ``HANDLE`` restype, x64 ctypes treats
    ``kernel32.GetCurrentProcess()`` as returning ``c_int`` and truncates the
    64-bit pseudo-handle, so ``OpenProcessToken`` fails, the SID never resolves,
    and ``is_running_as_system()`` wrongly returns ``False`` — aborting ``scan
    --all-users`` with ``EXIT_MISCONFIG``. These run off-Windows by faking the
    DLL handles (the helper only assigns ``restype``/``argtypes``; it makes no
    calls).
    """

    @staticmethod
    def _apply_to_fakes() -> dict[str, MagicMock]:
        dlls = {
            "kernel32": MagicMock(),
            "advapi32": MagicMock(),
            "userenv": MagicMock(),
            "wtsapi32": MagicMock(),
        }
        windows_users._apply_win32_signatures(**dlls)
        return dlls

    def test_get_current_process_restype_is_handle_not_default_int(self):
        # THE bug: a default ``c_int`` restype truncates the x64 pseudo-handle.
        from ctypes import wintypes  # noqa: PLC0415

        dlls = self._apply_to_fakes()
        assert dlls["kernel32"].GetCurrentProcess.restype is wintypes.HANDLE
        assert dlls["kernel32"].GetCurrentProcess.argtypes == []

    def test_open_process_token_takes_pointer_sized_handle(self):
        import ctypes  # noqa: PLC0415
        from ctypes import wintypes  # noqa: PLC0415

        dlls = self._apply_to_fakes()
        fn = dlls["advapi32"].OpenProcessToken
        assert fn.restype is wintypes.BOOL
        assert fn.argtypes == [
            wintypes.HANDLE,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.HANDLE),
        ]

    def test_guard_chain_remainder_is_signed(self):
        from ctypes import wintypes  # noqa: PLC0415

        dlls = self._apply_to_fakes()
        assert dlls["advapi32"].GetTokenInformation.restype is wintypes.BOOL
        assert dlls["advapi32"].ConvertSidToStringSidW.restype is wintypes.BOOL

    def test_signs_every_required_win32_function(self):
        # Non-circular: assert each required function had *some* ctypes
        # restype + an argtypes list assigned (not a bare MagicMock attr).
        dlls = self._apply_to_fakes()
        required = {
            "kernel32": [
                "GetCurrentProcess",
                "CloseHandle",
                "LocalFree",
                "WaitForSingleObject",
                "GetExitCodeProcess",
                "TerminateProcess",
            ],
            "advapi32": [
                "OpenProcessToken",
                "GetTokenInformation",
                "ConvertSidToStringSidW",
                "ConvertStringSidToSidW",
                "LookupAccountSidW",
                "CreateProcessAsUserW",
            ],
            "userenv": ["CreateEnvironmentBlock", "DestroyEnvironmentBlock"],
            "wtsapi32": ["WTSQueryUserToken"],
        }
        for dll_name, funcs in required.items():
            for func_name in funcs:
                fn = getattr(dlls[dll_name], func_name)
                assert not isinstance(fn.restype, MagicMock), (
                    f"{dll_name}.{func_name}.restype not set"
                )
                assert isinstance(fn.argtypes, list), (
                    f"{dll_name}.{func_name}.argtypes not set"
                )

    def test_only_applies_supplied_dlls_and_is_idempotent(self):
        from ctypes import wintypes  # noqa: PLC0415

        kernel32 = MagicMock()
        windows_users._apply_win32_signatures(kernel32=kernel32)
        windows_users._apply_win32_signatures(kernel32=kernel32)  # idempotent
        assert kernel32.GetCurrentProcess.restype is wintypes.HANDLE
        assert kernel32.GetCurrentProcess.argtypes == []


class TestRunAllUsersScanGuard:
    def test_non_windows_returns_misconfig(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(windows_users.platform, "system", lambda: "Linux")

        code = run_all_users_scan(
            scan_projects=True, project_timeout=60, project_depth=7, **_CAPS
        )
        assert code == EXIT_MISCONFIG

    def test_not_system_returns_misconfig(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(windows_users.platform, "system", lambda: "Windows")
        monkeypatch.setattr(windows_users, "is_running_as_system", lambda: False)

        code = run_all_users_scan(
            scan_projects=True, project_timeout=60, project_depth=7, **_CAPS
        )
        assert code == EXIT_MISCONFIG


class TestRunAllUsersScanOrchestration:
    @pytest.fixture(autouse=True)
    def _as_system(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(windows_users.platform, "system", lambda: "Windows")
        monkeypatch.setattr(windows_users, "is_running_as_system", lambda: True)

    def test_no_profiles_is_clean(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(windows_users, "enumerate_real_user_profiles", lambda: [])
        monkeypatch.setattr(windows_users, "active_session_sids", lambda: {})

        code = run_all_users_scan(
            scan_projects=True, project_timeout=60, project_depth=7, **_CAPS
        )
        assert code == 0

    def test_selects_token_launcher_when_logged_on_else_system(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        alice = _profile("S-1-12-1-1-2-3-4", r"C:\Users\alice", "alice")  # logged on
        bob = _profile("S-1-5-21-1-2-3-1001", r"C:\Users\bob", "bob")  # logged off
        monkeypatch.setattr(
            windows_users, "enumerate_real_user_profiles", lambda: [alice, bob]
        )
        monkeypatch.setattr(
            windows_users, "active_session_sids", lambda: {alice.sid: 3}
        )

        launched: list[tuple[int, str]] = []
        system_scanned: list[str] = []

        def fake_launch(session_id, profile, **kwargs):
            launched.append((session_id, profile.username))
            return 0

        def fake_system(profile, **kwargs):
            system_scanned.append(profile.username)
            return 0

        monkeypatch.setattr(windows_users, "launch_scan_as_user", fake_launch)
        monkeypatch.setattr(windows_users, "run_scan_as_system", fake_system)

        code = run_all_users_scan(
            scan_projects=True, project_timeout=60, project_depth=7, **_CAPS
        )

        assert code == 0
        assert launched == [(3, "alice")]  # logged-on Entra user -> token drop
        assert system_scanned == ["bob"]  # logged-off -> SYSTEM env-pointed

    def test_forwards_cache_setting_only_to_non_elevated_child(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ):
        logged_on = _profile("S-1-12-1-1-2-3-4", r"C:\Users\alice", "alice")
        logged_off = _profile("S-1-5-21-1-2-3-1002", r"C:\Users\bob", "bob")
        monkeypatch.setattr(
            windows_users,
            "enumerate_real_user_profiles",
            lambda: [logged_on, logged_off],
        )
        monkeypatch.setattr(
            windows_users,
            "active_session_sids",
            lambda: {logged_on.sid: 3},
        )
        user_kwargs: dict = {}
        system_kwargs: dict = {}

        def fake_launch(_session_id, _profile, **kwargs):
            user_kwargs.update(kwargs)
            return 0

        def fake_system(_profile, **kwargs):
            system_kwargs.update(kwargs)
            return 0

        monkeypatch.setattr(windows_users, "launch_scan_as_user", fake_launch)
        monkeypatch.setattr(windows_users, "run_scan_as_system", fake_system)

        code = run_all_users_scan(
            scan_projects=True,
            project_timeout=60,
            project_depth=7,
            artifact_lookup_cache=True,
            **_CAPS,
        )

        assert code == 0
        assert user_kwargs["artifact_lookup_cache"] is True
        assert "artifact_lookup_cache" not in system_kwargs

    def test_forwards_resource_caps_to_both_launchers(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        """Operator caps flow through to the token-drop and SYSTEM launchers."""
        alice = _profile("S-1-12-1-1-2-3-4", r"C:\Users\alice", "alice")  # logged on
        bob = _profile("S-1-5-21-1-2-3-1001", r"C:\Users\bob", "bob")  # logged off
        monkeypatch.setattr(
            windows_users, "enumerate_real_user_profiles", lambda: [alice, bob]
        )
        monkeypatch.setattr(
            windows_users, "active_session_sids", lambda: {alice.sid: 3}
        )

        launch_caps: dict = {}
        system_caps: dict = {}

        def fake_launch(session_id, profile, **kwargs):
            launch_caps.update(kwargs)
            return 0

        def fake_system(profile, **kwargs):
            system_caps.update(kwargs)
            return 0

        monkeypatch.setattr(windows_users, "launch_scan_as_user", fake_launch)
        monkeypatch.setattr(windows_users, "run_scan_as_system", fake_system)

        code = run_all_users_scan(
            scan_projects=True,
            project_timeout=60,
            project_depth=7,
            cpu_cores=1,
            max_cpu_percent=25,
            memory_limit_mb=512,
        )

        assert code == 0
        for caps in (launch_caps, system_caps):
            assert caps["cpu_cores"] == 1
            assert caps["max_cpu_percent"] == 25
            assert caps["memory_limit_mb"] == 512

    def test_one_profile_failure_does_not_abort_and_aggregates_nonzero(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        p1 = _profile("S-1-5-21-1-2-3-1001", r"C:\Users\a", "a")
        p2 = _profile("S-1-5-21-1-2-3-1002", r"C:\Users\b", "b")
        p3 = _profile("S-1-5-21-1-2-3-1003", r"C:\Users\c", "c")
        monkeypatch.setattr(
            windows_users, "enumerate_real_user_profiles", lambda: [p1, p2, p3]
        )
        monkeypatch.setattr(windows_users, "active_session_sids", lambda: {})

        scanned: list[str] = []

        def fake_system(profile, **kwargs):
            scanned.append(profile.username)
            if profile.username == "b":
                raise OSError("boom")  # one profile blows up
            return 0

        monkeypatch.setattr(windows_users, "run_scan_as_system", fake_system)

        code = run_all_users_scan(
            scan_projects=True, project_timeout=60, project_depth=7, **_CAPS
        )

        # Every profile is still attempted, and the run reports failure.
        assert scanned == ["a", "b", "c"]
        assert code == 1

    def test_nonzero_child_exit_aggregates_to_failure(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        p1 = _profile("S-1-5-21-1-2-3-1001", r"C:\Users\a", "a")
        monkeypatch.setattr(windows_users, "enumerate_real_user_profiles", lambda: [p1])
        monkeypatch.setattr(windows_users, "active_session_sids", lambda: {})
        monkeypatch.setattr(
            windows_users, "run_scan_as_system", lambda profile, **kwargs: 2
        )

        code = run_all_users_scan(
            scan_projects=True, project_timeout=60, project_depth=7, **_CAPS
        )
        assert code == 1

    def test_logged_on_launch_raise_falls_back_to_system_scan(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        # F1: a logged-on token launch that *raises* (transient Win32 failure)
        # must fall back to a SYSTEM env-pointed scan before counting it failed.
        alice = _profile("S-1-12-1-1-2-3-4", r"C:\Users\alice", "alice")
        monkeypatch.setattr(
            windows_users, "enumerate_real_user_profiles", lambda: [alice]
        )
        monkeypatch.setattr(
            windows_users, "active_session_sids", lambda: {alice.sid: 3}
        )

        def boom_launch(session_id, profile, **kwargs):
            raise OSError("WTSQueryUserToken failed")

        system_scanned: list[str] = []

        def fake_system(profile, **kwargs):
            system_scanned.append(profile.username)
            return 0

        monkeypatch.setattr(windows_users, "launch_scan_as_user", boom_launch)
        monkeypatch.setattr(windows_users, "run_scan_as_system", fake_system)

        code = run_all_users_scan(
            scan_projects=True, project_timeout=60, project_depth=7, **_CAPS
        )

        assert code == 0  # fallback succeeded, profile counted as scanned
        assert system_scanned == ["alice"]

    def test_logged_on_nonzero_exit_does_not_fall_back(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        # F1 boundary: a nonzero child *exit* is not a raise — it is counted as
        # a failure directly, with NO SYSTEM fallback.
        alice = _profile("S-1-12-1-1-2-3-4", r"C:\Users\alice", "alice")
        monkeypatch.setattr(
            windows_users, "enumerate_real_user_profiles", lambda: [alice]
        )
        monkeypatch.setattr(
            windows_users, "active_session_sids", lambda: {alice.sid: 3}
        )
        monkeypatch.setattr(windows_users, "launch_scan_as_user", lambda *a, **k: 3)

        system_called: list[str] = []
        monkeypatch.setattr(
            windows_users,
            "run_scan_as_system",
            lambda profile, **k: system_called.append(profile.username) or 0,
        )

        code = run_all_users_scan(
            scan_projects=True, project_timeout=60, project_depth=7, **_CAPS
        )

        assert code == 1  # nonzero child exit aggregates to failure
        assert system_called == []  # no fallback on a nonzero child exit

    def test_logged_on_launch_raise_then_fallback_also_fails(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        # F1: when both the token launch and the SYSTEM fallback raise, the
        # profile is counted failed and the run still completes.
        alice = _profile("S-1-12-1-1-2-3-4", r"C:\Users\alice", "alice")
        monkeypatch.setattr(
            windows_users, "enumerate_real_user_profiles", lambda: [alice]
        )
        monkeypatch.setattr(
            windows_users, "active_session_sids", lambda: {alice.sid: 3}
        )

        def boom_launch(*a, **k):
            raise OSError("token launch failed")

        def boom_system(*a, **k):
            raise OSError("system scan failed")

        monkeypatch.setattr(windows_users, "launch_scan_as_user", boom_launch)
        monkeypatch.setattr(windows_users, "run_scan_as_system", boom_system)

        code = run_all_users_scan(
            scan_projects=True, project_timeout=60, project_depth=7, **_CAPS
        )

        assert code == 1

    def test_session_enum_failure_falls_back_to_system_scans(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        alice = _profile("S-1-12-1-1-2-3-4", r"C:\Users\alice", "alice")
        monkeypatch.setattr(
            windows_users, "enumerate_real_user_profiles", lambda: [alice]
        )

        def boom():
            raise OSError("WTS enum failed")

        monkeypatch.setattr(windows_users, "active_session_sids", boom)

        system_scanned: list[str] = []
        monkeypatch.setattr(
            windows_users,
            "run_scan_as_system",
            lambda profile, **kwargs: system_scanned.append(profile.username) or 0,
        )
        monkeypatch.setattr(
            windows_users,
            "launch_scan_as_user",
            lambda *a, **k: pytest.fail(
                "must not token-launch when session enum failed"
            ),
        )

        code = run_all_users_scan(
            scan_projects=True, project_timeout=60, project_depth=7, **_CAPS
        )

        assert code == 0
        assert system_scanned == ["alice"]
