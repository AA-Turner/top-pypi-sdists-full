"""Native, opt-in proof that managed-policy publication reaches a running reader.

Run as root on macOS with RUNLAYER_TEST_MANAGED_POLICY=1. Changed preferences
belong to random synthetic domains, removed in finally. Readers run as the
sudo caller. The production publisher runs in a bounded child; browser policies,
MDM profiles, and preference daemons are untouched.
"""

from __future__ import annotations

import json
import os
import plistlib
import selectors
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

import pytest

from runlayer_cli.managed_policy_publication import publish_managed_policy

pytestmark = pytest.mark.skipif(
    sys.platform != "darwin"
    or getattr(os, "geteuid", lambda: -1)() != 0
    or os.environ.get("RUNLAYER_TEST_MANAGED_POLICY") != "1",
    reason="requires opt-in macOS root managed-preference integration test",
)

_PREFERENCE_ROOT = Path("/Library/Managed Preferences")
_DOMAIN_PREFIX = "com.runlayer.test.policy-publication."
_KEY = "RunlayerSyntheticPolicyProbe"
_NATIVE_READER_SOURCE = Path(__file__).parent / "fixtures/macos_policy_reader.c"


@pytest.fixture
def native_reader_directory():
    with tempfile.TemporaryDirectory(
        prefix="runlayer-native-reader-", dir="/private/tmp"
    ) as directory:
        path = Path(directory)
        path.chmod(0o755)
        yield path


def _build_native_reader(directory: Path, domain: str, unrelated: str) -> list[str]:
    contents = directory / "PolicyProbe.app/Contents"
    executable = contents / "MacOS/PolicyProbe"
    executable.parent.mkdir(parents=True)
    for folder in (contents.parent, contents, executable.parent):
        folder.chmod(0o755)
    (contents / "Info.plist").write_bytes(
        plistlib.dumps(
            {
                "CFBundleIdentifier": domain,
                "CFBundleExecutable": "PolicyProbe",
                "CFBundlePackageType": "APPL",
                "CFBundleVersion": "1",
            }
        )
    )
    (contents / "Info.plist").chmod(0o644)
    subprocess.run(
        [
            "/usr/bin/xcrun",
            "clang",
            "-std=c11",
            "-framework",
            "CoreFoundation",
            str(_NATIVE_READER_SOURCE),
            "-o",
            str(executable),
        ],
        check=True,
        capture_output=True,
        timeout=60,
    )
    executable.chmod(0o755)
    return [str(executable), domain, unrelated]


def _read_running(
    process: subprocess.Popen[str], command: str = "sync"
) -> dict[str, object]:
    assert process.stdin is not None and process.stdout is not None
    process.stdin.write(command + "\n")
    process.stdin.flush()
    with selectors.DefaultSelector() as selector:
        selector.register(process.stdout, selectors.EVENT_READ)
        assert selector.select(timeout=10), "native preference reader timed out"
    return json.loads(process.stdout.readline())


def _read_fresh(
    reader_args: list[str],
    uid: int,
    gid: int,
    env: dict[str, str],
    command: str = "sync",
) -> dict[str, object]:
    result = subprocess.run(
        reader_args,
        input=command + "\nquit\n",
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
        user=uid,
        group=gid,
        extra_groups=[],
        env=env,
    )
    return json.loads(result.stdout)


def _raw_write(path: Path, value: str) -> bytes:
    content = plistlib.dumps({_KEY: value, "UnrelatedSyntheticPolicy": "preserved"})
    temporary = path.with_suffix(".test-tmp")
    try:
        with temporary.open("xb") as stream:
            stream.write(content)
            stream.flush()
            os.fchmod(stream.fileno(), 0o644)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
    return content


def _assert_published(process: subprocess.Popen[str], value: str | None) -> None:
    expected = {"value": value, "forced": value is not None}
    deadline = time.monotonic() + 5
    observed = _read_running(process)
    while observed != expected and time.monotonic() < deadline:
        time.sleep(0.1)
        observed = _read_running(process)
    print(f"running reader after publication: {json.dumps(observed)}")
    assert observed == expected


def test_managed_policy_publication_reaches_running_reader(
    native_reader_directory: Path,
) -> None:
    import pwd

    uid = int(os.environ.get("SUDO_UID", "0"))
    assert uid >= 500, "run sudo from a non-root macOS test account"
    user = pwd.getpwuid(uid)
    domain = _DOMAIN_PREFIX + str(uuid.uuid4())
    unrelated_domain = _DOMAIN_PREFIX + str(uuid.uuid4())
    path = _PREFERENCE_ROOT / f"{domain}.plist"
    unrelated_path = _PREFERENCE_ROOT / f"{unrelated_domain}.plist"
    assert not path.exists() and not path.is_symlink()
    assert not unrelated_path.exists() and not unrelated_path.is_symlink()
    assert not _PREFERENCE_ROOT.is_symlink()
    created_directory = not _PREFERENCE_ROOT.exists()
    reader_args = _build_native_reader(
        native_reader_directory, domain, unrelated_domain
    )
    reader_env = {**os.environ, "HOME": user.pw_dir, "USER": user.pw_name}
    process = None
    try:
        _PREFERENCE_ROOT.mkdir(mode=0o755, exist_ok=True)
        unrelated_content = _raw_write(unrelated_path, "created")
        process = subprocess.Popen(
            reader_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            user=uid,
            group=user.pw_gid,
            extra_groups=[],
            env=reader_env,
        )
        assert _read_running(process) == {"value": None, "forced": False}
        unrelated_expected = {"value": "created", "forced": True}
        assert _read_running(process, "unrelated") == unrelated_expected
        raw_visibility: dict[str, dict[str, object]] = {}
        for value in ("created", "updated", None):
            phase = value or "removed"
            if value is None:
                path.unlink()
                content = plistlib.dumps({})
            else:
                content = _raw_write(path, value)
            raw_visibility[phase] = _read_running(process)
            raw_visibility[f"{phase}_fresh"] = _read_fresh(
                reader_args, uid, user.pw_gid, reader_env
            )
            print(
                json.dumps(
                    {
                        "publisher": "bounded-native-child",
                        "reader": "native-bundle-current-application",
                        "raw_visibility": raw_visibility,
                    }
                )
            )
            if value == "created":
                assert raw_visibility[f"{phase}_fresh"] == {
                    "value": value,
                    "forced": True,
                }
                assert raw_visibility[phase] == {"value": None, "forced": False}
            publish_managed_policy([path])
            _assert_published(process, value)
            expected = {"value": value, "forced": value is not None}
            assert _read_fresh(reader_args, uid, user.pw_gid, reader_env) == expected
            if value is None:
                assert not path.exists()
            else:
                assert plistlib.loads(path.read_bytes()) == plistlib.loads(content)
            publish_managed_policy([path])
            _assert_published(process, value)
            assert _read_fresh(reader_args, uid, user.pw_gid, reader_env) == expected
            assert unrelated_path.read_bytes() == unrelated_content
            assert _read_running(process, "unrelated") == unrelated_expected
            assert (
                _read_fresh(reader_args, uid, user.pw_gid, reader_env, "unrelated")
                == unrelated_expected
            )
    finally:
        try:
            if process is not None and process.poll() is None:
                try:
                    process.communicate("quit\n", timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.communicate(timeout=10)
        finally:
            try:
                path.unlink(missing_ok=True)
            finally:
                unrelated_path.unlink(missing_ok=True)
                if created_directory:
                    _PREFERENCE_ROOT.rmdir()
