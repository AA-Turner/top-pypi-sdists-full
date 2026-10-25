"""The Probe service installs a CLOSED desktop app's update (plan E1/E3, owner 2026-10-24).

Real files, real tar.gz archives, real Ed25519 keys made here and signed the
way Tauri's signer signs (`ED`: the archive's BLAKE2b-512; the trusted comment
with `version:`; the global signature over both), real processes and a real
flock for "the app is running". The service never moves the app's bundle: the
release's own helper does (prbe-ai/desktop `src-tauri/src/bin/probe-swap.rs`,
tested in that repo on macOS). Here a stand-in helper with the same arguments,
JSON line and exit codes plays it (FAKE_HELPER), and records every call, so the
tests see the service run it from the staged bundle and `--remove` from the
installed one. Only the network is also a stand-in (`Feed`), and `codesign`
(Linux has none; a script plays it where a test needs it). The real release's
signature is checked against the pinned key offline (its digest), and the
macOS workflow job (`agent-os-matrix.yml`, `run: app-install`) runs the install
against the real releases on a real Mac.
"""

from __future__ import annotations

import asyncio
import base64
import fcntl
import functools
import hashlib
import io
import json
import os
import plistlib
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import time
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from probe.service import appinstall, appupdate, paths, updater
from probe.service.appinstall import InstallError, Outcome
from probe.service.protocol import AppCheckReason, AppResult
from tests.service_fakes import enable_auto_update, fake_open, open_calls
from tests.service_harness import service_home  # noqa: F401 -- a fixture

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the service is POSIX-only (plan S8)")

ENDPOINT = "https://releases.example.test/latest.json"
ARCHIVE_URL = "https://releases.example.test/Probe_universal.app.tar.gz"
EXE = "desktop"


# -- keys and signatures, as Tauri's signer makes them ------------------------------


class Key:
    def __init__(self, key_id: bytes | None = None) -> None:
        self.private = Ed25519PrivateKey.generate()
        self.key_id = key_id or os.urandom(8)

    def public_b64(self) -> str:
        """tauri.conf.json's `pubkey`: base64 of the minisign key file."""
        raw = self.private.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
        line = base64.b64encode(b"Ed" + self.key_id + raw).decode()
        text = f"untrusted comment: minisign public key: {self.key_id[::-1].hex().upper()}\n{line}\n"
        return base64.b64encode(text.encode()).decode()

    def sign(self, data: bytes, version: str | None, *, prehashed: bool = True, trusted: str | None = None,
             tamper_trusted: str | None = None) -> str:
        """A manifest entry's `signature`: base64 of the `.sig` file."""
        algorithm = b"ED" if prehashed else b"Ed"
        message = hashlib.blake2b(data, digest_size=64).digest() if prehashed else data
        signature = self.private.sign(message)
        if trusted is None:
            trusted = "timestamp:1792810334\tfile:Probe.app.tar.gz" + (f"\tversion:{version}" if version else "")
        global_signature = self.private.sign(signature + trusted.encode())
        lines = [
            "untrusted comment: signature from tauri secret key",
            base64.b64encode(algorithm + self.key_id + signature).decode(),
            f"trusted comment: {tamper_trusted if tamper_trusted is not None else trusted}",
            base64.b64encode(global_signature).decode(),
        ]
        return base64.b64encode(("\n".join(lines) + "\n").encode()).decode()


# -- bundles and archives ------------------------------------------------------------


def info_plist(version: str, bundle_id: str = appinstall.BUNDLE_ID, helper: bool = True) -> bytes:
    info = {
        "CFBundleIdentifier": bundle_id,
        "CFBundleShortVersionString": version,
        "CFBundleVersion": version,
        "CFBundleExecutable": EXE,
    }
    if helper:
        info[appinstall.HELPER_KEY] = 1
    return plistlib.dumps(info)


#: A stand-in for the release's probe-swap: the same arguments, JSON line (`result`, `reason`,
#: `old`) and exit codes (0 swapped/removed, 3 app running, 4 refused, 5 not permitted, 1 error).
#: It swaps its own bundle with the target, finishes a journalled swap whose target is missing,
#: deletes with --remove, answers from `probe-swap.answer` beside it when there is one (after
#: swapping, when the answer says `"swap": true`, with `old` as the real helper gives it; nothing
#: at all with `"silent": true`, as when its answer is lost), and logs each call beside the app.
FAKE_HELPER = r"""#!{python} -I
import json, os, plistlib, shutil, sys
from pathlib import Path

exe = Path(os.path.realpath(sys.argv[0]))
own = exe.parents[2]
folder = own.parent
args = sys.argv[1:]
with open(folder / ".probe-swap-calls.jsonl", "a") as log:
    log.write(json.dumps({"bundle": own.name, "args": args}) + "\n")

def say(result, code, reason, **extra):
    print(json.dumps({"result": result, "reason": reason, **extra}))
    sys.exit(code)

def answer_with(data, **extra):
    if data.get("silent"):
        sys.exit(data["code"])
    say(data["result"], data["code"], data.get("reason"), detail=data.get("detail", ""),
        undo_failed=bool(data.get("undo_failed")), **extra)

answer = exe.parent / "probe-swap.answer"
data = json.loads(answer.read_text()) if answer.exists() else None
if data is not None and not data.get("swap"):
    answer_with(data)

def version(bundle):
    with open(bundle / "Contents" / "Info.plist", "rb") as handle:
        return plistlib.load(handle)["CFBundleShortVersionString"]

if args[:1] == ["--remove"]:
    deleting = args[1] if args[1].endswith(".deleting") else args[1] + ".deleting"
    if deleting != args[1]:
        os.rename(args[1], deleting)
    shutil.rmtree(deleting)
    say("removed", 0, "done")
target = Path(args[0])
journal = folder / ".Probe.app.probe-swap.json"
if not os.path.lexists(target) and journal.exists():
    os.rename(own, target)
    journal.unlink()
    say("swapped", 0, "finished", detail="finished an interrupted swap")
before, after = version(target), version(own)
tmp = folder / (own.name + ".tmp")
os.rename(target, tmp)
os.rename(own, target)
os.rename(tmp, own)
if data is not None:
    answer_with(data, old=str(own))
say("swapped", 0, "done", version_before=before, version_after=after, old=str(own), undo_failed=False)
""".replace("{python}", sys.executable)


def _dir(tar: tarfile.TarFile, name: str) -> None:
    info = tarfile.TarInfo(name)
    info.type = tarfile.DIRTYPE
    info.mode = 0o755
    tar.addfile(info)


def _file(tar: tarfile.TarFile, name: str, data: bytes, mode: int = 0o644) -> None:
    info = tarfile.TarInfo(name)
    info.size = len(data)
    info.mode = mode
    info.mtime = 1_792_000_000
    tar.addfile(info, io.BytesIO(data))


def archive(version: str, *, extra=None, bundle_id: str = appinstall.BUNDLE_ID, top: str = "Probe.app",
            exe: bytes = b"#!/bin/sh\necho new\n", helper: bool = True, answer: dict | None = None) -> bytes:
    """A Tauri updater archive: `Probe.app/...`, as tauri-bundler writes it,
    with the update helper (a release from E3 on) unless `helper` is False.
    `answer`: what that helper says instead of swapping (`{result, code, detail}`)."""
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        for name in (f"{top}/", f"{top}/Contents", f"{top}/Contents/MacOS", f"{top}/Contents/Resources"):
            _dir(tar, name)
        _file(tar, f"{top}/Contents/Info.plist", info_plist(version, bundle_id, helper))
        _file(tar, f"{top}/Contents/MacOS/{EXE}", exe, 0o755)
        if helper:
            _file(tar, f"{top}/Contents/MacOS/{appinstall.HELPER_NAME}", FAKE_HELPER.encode(), 0o755)
        if answer is not None:
            _file(tar, f"{top}/Contents/MacOS/probe-swap.answer", json.dumps(answer).encode())
        _file(tar, f"{top}/Contents/Resources/icon.icns", b"icon")
        if extra is not None:
            extra(tar)
    return buffer.getvalue()


def make_app(folder: Path, version: str, *, exe: Path | None = None, helper: bool = False,
             name: str = appupdate.APP_NAME) -> Path:
    """An installed `Probe.app` at `version` (its executable a copy of `exe`),
    with the update helper when `helper` (a release from E3 on)."""
    app = folder / name
    (app / "Contents" / "MacOS").mkdir(parents=True)
    (app / "Contents" / "Info.plist").write_bytes(info_plist(version, helper=helper))
    if helper:
        script = app / "Contents" / "MacOS" / appinstall.HELPER_NAME
        script.write_text(FAKE_HELPER)
        script.chmod(0o755)
    binary = app / "Contents" / "MacOS" / EXE
    if exe is not None:
        shutil.copy2(exe, binary)
    else:
        binary.write_text("#!/bin/sh\necho old\n")
    binary.chmod(0o755)
    return app


def version_of(app: Path) -> str:
    with open(app / "Contents" / "Info.plist", "rb") as handle:
        return plistlib.load(handle)["CFBundleShortVersionString"]


def manifest(version: str, signature: str, *, url: str = ARCHIVE_URL, keys=("darwin-aarch64-app", "darwin-aarch64",
             "darwin-x86_64-app", "darwin-x86_64", "darwin-universal")) -> dict:
    """latest.json as the release workflow publishes it."""
    return {
        "version": version,
        "notes": "notes",
        "pub_date": "2026-10-24T02:52:20.767Z",
        "platforms": {k: {"url": url, "signature": signature} for k in keys},
    }


class Feed:
    """The release server: the manifest at ENDPOINT, files by url. Records every
    request; `during_download` runs while the archive is being written."""

    def __init__(self, manifest_body: object, files: dict | None = None) -> None:
        self.manifest = manifest_body
        self.files = files or {}
        self.requests: list[tuple[str, str]] = []
        self.during_download = None

    def __call__(self, url, *, accept, limit, deadline, sink=None):
        self.requests.append((url, accept))
        deadline.left()
        if url == ENDPOINT:
            if self.manifest is None:
                return None  # 204 No Content
            body = json.dumps(self.manifest).encode()
            if len(body) > limit:
                raise InstallError("over the limit")
            return body
        data = self.files[url]
        if len(data) > limit:
            raise InstallError(f"{url} is over the {limit}-byte limit")
        if self.during_download is not None:
            self.during_download()
            deadline.left()  # the real fetch looks at it after every chunk
        sink.write(data)
        return len(data)

    def downloads(self) -> list[str]:
        return [url for url, _ in self.requests if url != ENDPOINT]


@pytest.fixture(autouse=True)
def no_codesign(monkeypatch):
    """Linux has no codesign; on a Mac these fake bundles are unsigned. The
    codesign tests put a script in its place."""
    monkeypatch.setattr(appinstall, "CODESIGN", "/nonexistent/codesign")


@pytest.fixture
def mac(tmp_path):
    """An Applications folder with Probe 0.1.51 installed, a home for the
    app's instance lock, the service's journal, and a release key."""
    apps = tmp_path / "Applications"
    apps.mkdir()
    home = tmp_path / "home"
    home.mkdir()
    (tmp_path / "state").mkdir()
    return {"apps": apps, "app": make_app(apps, "0.1.51"), "home": home, "key": Key()}


def release(mac, version: str = "0.1.52", **signing) -> Feed:
    data = archive(version)
    return Feed(manifest(version, mac["key"].sign(data, version, **signing)), {ARCHIVE_URL: data})


def install(mac, feed: Feed, **kwargs) -> dict:
    options = {"home": mac["home"], "endpoints": (ENDPOINT,),
               "pubkey": mac["key"].public_b64(), "fetcher": feed, "machine_arch": "aarch64", **kwargs}
    return appinstall.install_closed(mac["app"], **options)


def nothing_left(mac) -> None:
    """No staging folder, archive or old bundle beside the app, no journal."""
    assert appinstall.leftovers(mac["app"]) == []
    assert not (mac["apps"] / appinstall.HELPER_JOURNAL_NAME).exists()


def helper_calls(folder: Path) -> list[dict]:
    """Every run of a stand-in helper beside the app: `{bundle, args}`."""
    log = folder / ".probe-swap-calls.jsonl"
    return [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []


def same_tree(path: Path) -> dict:
    return {str(p.relative_to(path)): (p.read_bytes() if p.is_file() else None) for p in sorted(path.rglob("*"))}


# -- the real release, offline --------------------------------------------------------

#: prbe-ai/desktop-releases v0.1.52 `latest.json` `platforms.darwin-aarch64.signature`, and
#: the BLAKE2b-512 of `Probe_0.1.52_universal.app.tar.gz` (7,325,222 bytes) it signs.
REAL_0152_SIGNATURE = (
    "dW50cnVzdGVkIGNvbW1lbnQ6IHNpZ25hdHVyZSBmcm9tIHRhdXJpIHNlY3JldCBrZXkKUlVSQmF1bXZKWGlFcisrb1RYbGIyU1RiS0RaNXp2d0lC"
    "ajhjeTAyTTFMejhDV1NYVG56REZrTmFsOG1aejgxVzBBSnlTZDhCSEcrdDRQcVdBdFcweGV6a3R6K2Z6b0hKTEFJPQp0cnVzdGVkIGNvbW1lbnQ6"
    "IHRpbWVzdGFtcDoxNzkyODEwMzM0CWZpbGU6UHJvYmUuYXBwLnRhci5negl2ZXJzaW9uOjAuMS41MgpKUzhjR1VZVkRXRXl0MnhJbDJjT241bDlK"
    "Z080UDM4QWRhblo3NC9NL0pTZE00TVBsNGU5R3pQMmlSYUtRcTN3aDBVZXBlUW1IbU05WGhiTnk1bGlBQT09Cg=="
)
REAL_0152_DIGEST = bytes.fromhex(
    "77b9d626492ceda2d445187566947aca75b44089301b34a1546c5b67c887397c"
    "14ccaa1a38e784b7c1a794b8ba348fede6c4077cb2a4e436b7f716ee39b4bef4"
)


def test_the_real_release_verifies_with_the_pinned_key_and_nothing_else_does():
    """Tauri's signer makes `ED` (prehashed) signatures whose trusted comment
    names the version; the pinned key is desktop's tauri.conf.json pubkey."""
    key = appinstall.parse_public_key(appinstall.PUBKEY)
    sig = appinstall.parse_signature(REAL_0152_SIGNATURE)
    assert sig.algorithm == b"ED" and sig.prehashed
    assert sig.key_id == key.key_id
    assert sig.trusted_comment == "timestamp:1792810334\tfile:Probe.app.tar.gz\tversion:0.1.52"
    appinstall.verify(b"", sig, key, "0.1.52", prehashed_digest=REAL_0152_DIGEST)
    appinstall.verify(b"", sig, key, "v0.1.52", prehashed_digest=REAL_0152_DIGEST)  # as semver
    with pytest.raises(InstallError, match="does not verify"):
        appinstall.verify(b"", sig, key, "0.1.52", prehashed_digest=bytes(64))
    with pytest.raises(InstallError, match="for 0.1.52, not the announced 0.1.53"):
        appinstall.verify(b"", sig, key, "0.1.53", prehashed_digest=REAL_0152_DIGEST)
    other = appinstall.parse_public_key(Key(key_id=key.key_id).public_b64())
    with pytest.raises(InstallError, match="does not verify"):
        appinstall.verify(b"", sig, other, "0.1.52", prehashed_digest=REAL_0152_DIGEST)


def test_the_pinned_key_and_endpoint_are_desktops():
    """The constants are desktop's tauri.conf.json `plugins.updater`, verbatim."""
    text = base64.b64decode(appinstall.PUBKEY).decode()
    assert text.startswith("untrusted comment: minisign public key: AF847825AFE96A41\n")
    assert appinstall.ENDPOINTS == (
        "https://github.com/prbe-ai/desktop-releases/releases/latest/download/latest.json",
    )
    assert appinstall.REQUIRE_SIGNED_VERSION is True
    desktop = Path.home() / "desktop" / "src-tauri" / "tauri.conf.json"
    if desktop.is_file():  # a checkout of prbe-ai/desktop beside this one
        conf = json.loads(desktop.read_text())["plugins"]["updater"]
        assert conf["pubkey"] == appinstall.PUBKEY
        assert tuple(conf["endpoints"]) == appinstall.ENDPOINTS
        assert conf.get("requireSignedVersion") is True


# -- a good signature, and every way it is not ----------------------------------------


def test_a_signed_newer_release_replaces_the_closed_app(mac):
    feed = release(mac)
    before = os.stat(mac["app"]).st_ino
    previous = os.umask(0o077)  # a strict umask must not keep other users out of the app
    try:
        result = install(mac, feed)
    finally:
        os.umask(previous)
    assert result["outcome"] == Outcome.INSTALLED, result
    assert (result["version_before"], result["version_after"]) == ("0.1.51", "0.1.52")
    assert result["codesign"] == "unavailable"
    assert version_of(mac["app"]) == "0.1.52"
    assert os.stat(mac["app"]).st_ino != before, "a new bundle, swapped in whole"
    binary = mac["app"] / "Contents" / "MacOS" / EXE
    assert binary.read_text() == "#!/bin/sh\necho new\n"
    assert stat.S_IMODE(binary.stat().st_mode) == 0o755
    assert stat.S_IMODE((mac["app"] / "Contents" / "Info.plist").stat().st_mode) == 0o644
    assert stat.S_IMODE(mac["app"].stat().st_mode) == 0o755, "the bundle root is not left 0700"
    # The swap was the staged release's own helper, the removal the installed (new) app's.
    calls = helper_calls(mac["apps"])
    assert [c["args"][:1] for c in calls] == [[str(mac["app"])], ["--remove"]], calls
    assert calls[0]["bundle"].startswith(appinstall.STAGING_PREFIX)
    assert calls[1]["bundle"] == "Probe.app"
    assert stat.S_IMODE((mac["app"] / "Contents" / "MacOS").stat().st_mode) == 0o755
    assert result["old_bundle"] == "removed"
    nothing_left(mac)
    assert feed.requests == [(ENDPOINT, "application/json"), (ARCHIVE_URL, "application/octet-stream")]


@pytest.mark.parametrize("prehashed", [True, False], ids=["ED-blake2b", "Ed-legacy"])
def test_both_minisign_algorithms_verify_as_the_apps_updater_allows(mac, prehashed):
    """tauri-plugin-updater calls minisign-verify with legacy allowed: `Ed`
    (the file itself) verifies too, though Tauri's signer makes `ED`."""
    assert install(mac, release(mac, prehashed=prehashed))["outcome"] == Outcome.INSTALLED


@pytest.mark.parametrize(
    ("case", "error"),
    [
        ("another key", "different key"),
        ("another key with the pinned key id", "does not verify"),
        ("a tampered archive", "does not verify"),
        ("a tampered trusted comment", "trusted comment does not verify"),
        ("signed for another version", "is for 0.1.53, not the announced 0.1.52"),
        ("no signed version", "names no version"),
        ("an unknown algorithm", "not supported"),
        ("not a signature", "not a minisign signature|not valid base64"),
    ],
)
def test_anything_that_does_not_verify_is_refused_and_the_app_is_untouched(mac, case, error):
    data = archive("0.1.52")
    key = mac["key"]
    if case == "another key":
        signature = Key().sign(data, "0.1.52")
    elif case == "another key with the pinned key id":
        signature = Key(key_id=key.key_id).sign(data, "0.1.52")
    elif case == "a tampered archive":
        signature = key.sign(data, "0.1.52")
        data = data[:-10] + bytes(10)
    elif case == "a tampered trusted comment":
        signature = key.sign(data, "0.1.52", tamper_trusted="timestamp:1\tfile:x\tversion:0.1.52")
    elif case == "signed for another version":
        signature = key.sign(data, "0.1.53")
    elif case == "no signed version":
        signature = key.sign(data, None)
    elif case == "an unknown algorithm":
        raw = base64.b64decode(key.sign(data, "0.1.52")).decode().split("\n")
        blob = base64.b64decode(raw[1])
        raw[1] = base64.b64encode(b"XX" + blob[2:]).decode()
        signature = base64.b64encode("\n".join(raw).encode()).decode()
    else:
        signature = base64.b64encode(b"untrusted comment: nope\nnope\n").decode()
    tree = same_tree(mac["app"])
    result = install(mac, Feed(manifest("0.1.52", signature), {ARCHIVE_URL: data}))
    assert result["outcome"] == Outcome.FAILED
    assert result["error"] and __import__("re").search(error, result["error"]), result
    assert same_tree(mac["app"]) == tree and version_of(mac["app"]) == "0.1.51"
    nothing_left(mac)


@pytest.mark.parametrize("latest", ["0.1.51", "0.1.50", "0.1.52-beta.1", "v0.1.51"])
def test_never_an_older_or_the_same_version_and_nothing_is_downloaded(mac, latest):
    data = archive(latest.lstrip("v"))
    mac["app"] = make_app(mac["apps"] / "other", "0.1.52-beta.2" if "beta" in latest else "0.1.51")
    feed = Feed(manifest(latest, mac["key"].sign(data, latest.lstrip("v"))), {ARCHIVE_URL: data})
    result = install(mac, feed)
    assert result["outcome"] == Outcome.CURRENT, result
    assert feed.downloads() == []
    assert result["version_after"] == result["version_before"]


def test_no_content_reads_as_current(mac):
    feed = Feed(None)
    assert install(mac, feed)["outcome"] == Outcome.CURRENT
    assert feed.downloads() == []


def test_the_bundle_in_the_archive_must_be_probe_at_the_signed_version(mac):
    for data, error in [
        (archive("0.1.52", bundle_id="com.example.other"), "bundle id"),
        (archive("0.1.53"), "version '0.1.53', not 0.1.52"),
    ]:
        feed = Feed(manifest("0.1.52", mac["key"].sign(data, "0.1.52")), {ARCHIVE_URL: data})
        result = install(mac, feed)
        assert result["outcome"] == Outcome.FAILED and error in result["error"], result
        assert version_of(mac["app"]) == "0.1.51"
        nothing_left(mac)


# -- the archive's entries --------------------------------------------------------------


def _entry(name: str, kind: bytes = tarfile.REGTYPE, *, link: str = "", mode: int = 0o644, data: bytes = b"x"):
    def add(tar: tarfile.TarFile) -> None:
        info = tarfile.TarInfo(name)
        info.type = kind
        info.mode = mode
        info.linkname = link
        if kind == tarfile.REGTYPE:
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
        else:
            tar.addfile(info)
    return add


def _both(*adds):
    def add(tar):
        for one in adds:
            one(tar)
    return add


UNSAFE = {
    "a parent folder": _entry("Probe.app/../escaped"),
    "a path above the bundle": _entry("Probe.app/Contents/../../../escaped"),
    "an absolute path": _entry("/tmp/escaped"),
    "a second top-level folder": _entry("Other.app/Contents/x"),
    "a link pointing outside": _entry("Probe.app/Contents/out", tarfile.SYMTYPE, link="../../../etc"),
    "an absolute link": _entry("Probe.app/Contents/out", tarfile.SYMTYPE, link="/etc"),
    "a hard link": _entry("Probe.app/Contents/hard", tarfile.LNKTYPE, link="Probe.app/Contents/Info.plist"),
    "a device": _entry("Probe.app/Contents/dev", tarfile.CHRTYPE),
    "a fifo": _entry("Probe.app/Contents/fifo", tarfile.FIFOTYPE),
    "a write through a link": _both(
        _entry("Probe.app/Contents/Frameworks", tarfile.SYMTYPE, link="Resources"),
        _entry("Probe.app/Contents/Frameworks/x"),
    ),
    "an entry twice": _entry("Probe.app/Contents/Resources/icon.icns"),
    "an entry twice, another case": _entry("Probe.app/Contents/resources/ICON.icns"),
    # Each link inside alone, the chain outside: b -> a/../../.. through a -> ..
    "a chain of links escaping": _both(
        _entry("Probe.app/Contents/MacOS/a", tarfile.SYMTYPE, link=".."),
        _entry("Probe.app/Contents/MacOS/b", tarfile.SYMTYPE, link="a/../../.."),
    ),
}


@pytest.mark.parametrize("case", sorted(UNSAFE))
def test_an_unsafe_archive_entry_is_refused_and_nothing_lands_outside(mac, case, tmp_path):
    data = archive("0.1.52", extra=UNSAFE[case])
    tree = same_tree(mac["app"])
    outside = sorted(p.name for p in tmp_path.iterdir())
    result = install(mac, Feed(manifest("0.1.52", mac["key"].sign(data, "0.1.52")), {ARCHIVE_URL: data}))
    assert result["outcome"] == Outcome.FAILED, result
    assert same_tree(mac["app"]) == tree
    assert sorted(p.name for p in tmp_path.iterdir()) == outside
    assert not (mac["apps"] / "escaped").exists() and not (tmp_path / "escaped").exists()
    nothing_left(mac)


def test_an_archive_whose_top_is_not_an_app_bundle_is_refused(mac):
    data = archive("0.1.52", top="Probe")
    result = install(mac, Feed(manifest("0.1.52", mac["key"].sign(data, "0.1.52")), {ARCHIVE_URL: data}))
    assert result["outcome"] == Outcome.FAILED and "not an app bundle" in result["error"]


def test_setuid_and_group_write_bits_never_survive_and_inner_links_do(mac):
    data = archive("0.1.52", extra=_both(
        _entry("Probe.app/Contents/MacOS/helper", mode=0o6777, data=b"#!/bin/sh\n"),
        _entry("Probe.app/Contents/Resources/current", tarfile.SYMTYPE, link="icon.icns"),
        _entry("Probe.app/Contents/Resources/up", tarfile.SYMTYPE, link="../Info.plist"),
    ))
    result = install(mac, Feed(manifest("0.1.52", mac["key"].sign(data, "0.1.52")), {ARCHIVE_URL: data}))
    assert result["outcome"] == Outcome.INSTALLED, result
    helper = mac["app"] / "Contents" / "MacOS" / "helper"
    assert stat.S_IMODE(helper.stat().st_mode) == 0o755
    assert os.readlink(mac["app"] / "Contents" / "Resources" / "current") == "icon.icns"
    assert (mac["app"] / "Contents" / "Resources" / "up").read_bytes() == info_plist("0.1.52")


# -- bounds ------------------------------------------------------------------------------


def test_an_archive_over_the_size_bound_is_refused(mac, monkeypatch):
    monkeypatch.setattr(appinstall, "ARCHIVE_MAX_BYTES", 100)
    result = install(mac, release(mac))
    assert result["outcome"] == Outcome.FAILED and "limit" in result["error"]
    nothing_left(mac)


def test_an_archive_that_unpacks_too_big_is_refused(mac, monkeypatch):
    monkeypatch.setattr(appinstall, "UNPACKED_MAX_BYTES", 100)
    data = archive("0.1.52", extra=_entry("Probe.app/Contents/Resources/big", data=b"0" * 4096))
    result = install(mac, Feed(manifest("0.1.52", mac["key"].sign(data, "0.1.52")), {ARCHIVE_URL: data}))
    assert result["outcome"] == Outcome.FAILED and "more than 100 bytes" in result["error"]
    assert version_of(mac["app"]) == "0.1.51"
    nothing_left(mac)


def test_past_the_time_limit_the_install_gives_up(mac):
    feed = release(mac)
    feed.during_download = lambda: time.sleep(0.3)
    result = install(mac, feed, time_limit_s=0.2)
    assert result["outcome"] == Outcome.FAILED and "gave up" in result["error"], result
    assert version_of(mac["app"]) == "0.1.51"
    nothing_left(mac)


class _Sock:
    def __init__(self) -> None:
        self.timeouts: list[float] = []

    def settimeout(self, value: float) -> None:
        self.timeouts.append(value)


class _Response:
    def __init__(self, body: bytes, *, status: int = 200, length: str | None = None, stall: float = 0.0) -> None:
        self.stream = io.BytesIO(body)
        self.status = status
        self.headers = {"Content-Length": length} if length is not None else {}
        self.sock = _Sock()
        self.fp = type("Fp", (), {"raw": type("Raw", (), {"_sock": self.sock})()})()
        self.stall = stall

    def read(self, n: int) -> bytes:
        return self.stream.read(n)

    def read1(self, n: int) -> bytes:
        if self.stall:
            time.sleep(self.sock.timeouts[-1])
            raise TimeoutError("timed out")
        return self.stream.read(n)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def test_the_network_fetch_is_https_only_bounded_and_sends_the_updaters_accept(monkeypatch):
    seen = []

    class Opener:
        def __init__(self, response):
            self.response = response

        def open(self, request, timeout):
            seen.append((request.full_url, request.get_header("Accept"), timeout))
            return self.response

    deadline = appinstall._Deadline(60)  # noqa: SLF001
    with pytest.raises(InstallError, match="not https"):
        appinstall.fetch("http://example.test/latest.json", accept="application/json", limit=10, deadline=deadline)
    monkeypatch.setattr(appinstall, "_opener", lambda: Opener(_Response(b"x" * 50, length="50")))
    with pytest.raises(InstallError, match="over the 10-byte limit"):
        appinstall.fetch("https://example.test/a", accept="application/octet-stream", limit=10, deadline=deadline)
    monkeypatch.setattr(appinstall, "_opener", lambda: Opener(_Response(b"x" * 50)))  # no length: counted
    with pytest.raises(InstallError, match="over the 10-byte limit"):
        appinstall.fetch("https://example.test/a", accept="application/octet-stream", limit=10, deadline=deadline)
    monkeypatch.setattr(appinstall, "_opener", lambda: Opener(_Response(b"", status=204)))
    assert appinstall.fetch("https://example.test/m", accept="application/json", limit=10, deadline=deadline) is None
    monkeypatch.setattr(appinstall, "_opener", lambda: Opener(_Response(b"abc")))
    sink = io.BytesIO()
    assert appinstall.fetch("https://example.test/a", accept="application/octet-stream", limit=10,
                            deadline=deadline, sink=sink) == 3
    assert sink.getvalue() == b"abc"
    assert seen[-1][1] == "application/octet-stream" and seen[-1][2] <= appinstall.READ_TIMEOUT_S


def test_each_read_waits_at_most_what_is_left_of_the_deadline(monkeypatch):
    """A server trickling a byte at a time cannot hold the step past its
    deadline: every read's socket timeout is the smaller of READ_TIMEOUT_S and
    the time left."""
    response = _Response(b"", stall=1.0)
    monkeypatch.setattr(appinstall, "_opener", lambda: type("O", (), {"open": lambda self, r, timeout: response})())
    deadline = appinstall._Deadline(0.3)  # noqa: SLF001
    started = time.monotonic()
    with pytest.raises(InstallError):
        appinstall.fetch("https://example.test/a", accept="application/octet-stream", limit=10,
                         deadline=deadline, sink=io.BytesIO())
    assert response.sock.timeouts and response.sock.timeouts[0] <= 0.3
    assert time.monotonic() - started < 2.0


def test_a_redirect_away_from_https_is_refused():
    handler = None
    opener = appinstall._opener()  # noqa: SLF001
    for one in opener.handlers:
        if type(one).__name__ == "HttpsOnly":
            handler = one
    assert handler is not None
    with pytest.raises(InstallError, match="not https"):
        handler.redirect_request(None, None, 302, "Found", {}, "http://evil.test/x")


# -- the manifest ---------------------------------------------------------------------------


def test_the_manifest_entry_is_the_one_the_apps_updater_picks():
    entry = {"url": "https://x/a", "signature": "s"}
    other = {"url": "https://x/b", "signature": "t"}
    data = {"version": "v0.1.52", "platforms": {"darwin-aarch64": other, "darwin-aarch64-app": entry}}
    assert appinstall.parse_manifest(data, "aarch64") == ("v0.1.52", {**entry, "target": "darwin-aarch64-app"})
    assert appinstall.parse_manifest({"version": "0.1.52", "platforms": {"darwin-x86_64": other}}, "x86_64")[1][
        "target"] == "darwin-x86_64"
    assert appinstall.parse_manifest({"version": "0.1.52", "platforms": {"darwin-x86_64": other}}, "aarch64")[1] is None
    # Dynamic (server) format: the answer is the entry.
    assert appinstall.parse_manifest({"name": "0.1.52", "url": "https://x/a", "signature": "s"}, "aarch64") == (
        "0.1.52", {"url": "https://x/a", "signature": "s", "target": ""})
    for bad in ({"version": "latest"}, {"version": "0.1.52", "pub_date": "yesterday", "platforms": {}},
                {"version": "0.1.52"}, [], {"version": "01.1.52", "platforms": {}}):
        with pytest.raises(InstallError):
            appinstall.parse_manifest(bad, "aarch64")


def test_the_first_endpoint_that_answers_wins(mac):
    good = release(mac)

    def two(url, **kw):
        if url == "https://down.example.test/latest.json":
            raise InstallError("down")
        return good(url, **kw)

    result = install(mac, good, endpoints=("https://down.example.test/latest.json", ENDPOINT), fetcher=two)
    assert result["outcome"] == Outcome.INSTALLED


def test_versions_compare_as_semver():
    assert appinstall.newer("0.1.10", "0.1.9")
    assert appinstall.newer("0.2.0", "0.1.99")
    assert appinstall.newer("0.1.52", "0.1.52-beta.1")
    assert appinstall.newer("0.1.52-beta.10", "0.1.52-beta.2")
    assert appinstall.newer("0.1.52-beta", "0.1.52-alpha")
    assert not appinstall.newer("0.1.52", "0.1.52")
    assert not appinstall.newer("0.1.52+build", "0.1.52")
    assert not appinstall.newer("garbage", "0.1.0") and not appinstall.newer("1.0.0", "garbage")
    assert appinstall.same_version("v0.1.52", "0.1.52")
    # The semver crate's equality keeps build metadata: the app's updater refuses a
    # `version:0.1.54+x` signature for an announced 0.1.54, and so does this.
    assert not appinstall.same_version("0.1.54+x", "0.1.54")
    assert appinstall.same_version("0.1.54+x", "v0.1.54+x")


# -- when not to install: not writable, running, starting ---------------------------------


@pytest.mark.skipif(os.geteuid() == 0, reason="root writes anywhere")
@pytest.mark.parametrize("which", ["folder", "bundle"])
def test_a_bundle_or_folder_this_user_cannot_write_is_skipped_without_a_download(mac, which):
    target = mac["apps"] if which == "folder" else mac["app"]
    target.chmod(0o555)
    try:
        feed = release(mac)
        result = install(mac, feed)
    finally:
        target.chmod(0o755)
    assert result["outcome"] == Outcome.NOT_WRITABLE, result
    assert str(target) in result["detail"]
    assert feed.requests == []
    assert version_of(mac["app"]) == "0.1.51"


def _sleeper(mac) -> Path:
    """The installed app with a real long-running executable (a copy of `sleep`)."""
    shutil.rmtree(mac["app"])
    return make_app(mac["apps"], "0.1.51", exe=Path(shutil.which("sleep")))


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="/proc tells exactly where an executable runs from")
def test_a_running_app_is_skipped_without_a_download(mac):
    app = _sleeper(mac)
    proc = subprocess.Popen([str(app / "Contents" / "MacOS" / EXE), "60"])
    try:
        time.sleep(0.2)
        assert appinstall.running_from(app) == [proc.pid]
        feed = release(mac)
        result = install(mac, feed)
    finally:
        proc.kill()
        proc.wait()
    assert result["outcome"] == Outcome.APP_RUNNING, result
    assert feed.requests == []
    assert version_of(app) == "0.1.51"


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="/proc tells exactly where an executable runs from")
def test_an_app_process_that_starts_during_the_download_stops_the_install_before_the_helper(mac):
    """The instance lock free, a process running from the app (an old build, or
    the lock not taken yet): the look right before the helper runs skips it."""
    app = _sleeper(mac)
    started = []
    feed = release(mac)
    feed.during_download = lambda: started.append(subprocess.Popen([str(app / "Contents" / "MacOS" / EXE), "60"]))
    try:
        result = install(mac, feed)
    finally:
        for proc in started:
            proc.kill()
            proc.wait()
    assert result["outcome"] == Outcome.APP_RUNNING and "during the download" in result["detail"], result
    assert helper_calls(mac["apps"]) == []
    assert version_of(app) == "0.1.51"
    nothing_left(mac)


def _hold_instance_lock(home: Path):
    path = appinstall.instance_lock_path(home)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = open(path, "a+")  # noqa: SIM115 -- the caller closes it
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    return handle


def test_an_app_that_starts_during_the_download_is_never_swapped_under(mac):
    """It takes its instance lock at once: the install stops before the helper
    runs, and the staged copy is thrown away (the app's own updater has its
    launch check)."""
    held = []
    feed = release(mac)
    feed.during_download = lambda: held.append(_hold_instance_lock(mac["home"]))
    tree = same_tree(mac["app"])
    try:
        result = install(mac, feed)
    finally:
        for handle in held:
            handle.close()
    assert result["outcome"] == Outcome.APP_RUNNING, result
    assert helper_calls(mac["apps"]) == []
    assert same_tree(mac["app"]) == tree
    nothing_left(mac)


# -- the helper does every change to the app's bundle -------------------------------------


def test_the_service_never_renames_or_deletes_the_app_bundle_itself(mac, monkeypatch):
    """Every rename, swap and delete of the app or its old bundle is the
    helper's (a process of its own): this Python's os.rename, os.replace,
    shutil.rmtree and unlink never touch the app or a bundle that was it."""
    touched = []
    for module, name in ((os, "rename"), (os, "replace"), (os, "unlink"), (shutil, "rmtree")):
        real = getattr(module, name)

        def spy(*args, _real=real, _name=name, **kwargs):
            touched.append((_name, [str(a) for a in args if isinstance(a, (str, Path))]))
            return _real(*args, **kwargs)

        monkeypatch.setattr(module, name, spy)
    result = install(mac, release(mac))
    assert result["outcome"] == Outcome.INSTALLED, result
    app = str(mac["app"])
    for name, args in touched:
        assert not any(a == app or a.startswith(app + os.sep) for a in args), (name, args)
        # Only its own download and staged copy, by name: never an old bundle.
        for a in args:
            if os.path.basename(a).startswith(appinstall.STAGING_PREFIX):
                assert a.endswith(".tar.gz") or name == "rmtree", (name, args)


def test_a_release_without_the_helper_is_skipped_and_records_nothing(mac):
    """Every release before the helper (E3): skipped, the staged copy thrown
    away, the app untouched; the app's own updater installs it at its launch.
    The same release is not downloaded again."""
    data = archive("0.1.52", helper=False)
    feed = Feed(manifest("0.1.52", mac["key"].sign(data, "0.1.52")), {ARCHIVE_URL: data})
    tree = same_tree(mac["app"])
    result = install(mac, feed)
    assert result["outcome"] == Outcome.NO_HELPER, result
    assert result["latest"] == "0.1.52"
    assert same_tree(mac["app"]) == tree
    nothing_left(mac)
    assert len(feed.downloads()) == 1
    again = install(mac, feed, skip_version="0.1.52")
    assert again["outcome"] == Outcome.NO_HELPER
    assert len(feed.downloads()) == 1, "not downloaded again"
    # A newer release is looked at.
    newer_data = archive("0.1.53")
    newer_feed = Feed(manifest("0.1.53", mac["key"].sign(newer_data, "0.1.53")), {ARCHIVE_URL: newer_data})
    assert install(mac, newer_feed, skip_version="0.1.52")["outcome"] == Outcome.INSTALLED


@pytest.mark.parametrize(
    ("answer", "outcome"),
    [
        ({"result": "app_running", "code": 3, "reason": "lock_held", "detail": "the app holds its instance lock"},
         Outcome.APP_RUNNING),
        ({"result": "app_running", "code": 3, "reason": "app_started", "detail": "an old copy started; swapped back"},
         Outcome.APP_RUNNING),
        ({"result": "not_permitted", "code": 5, "reason": "not_permitted", "detail": "EPERM"}, Outcome.NOT_PERMITTED),
        # Only the machine words count: a refusal whose text reads like the system's is a refusal.
        ({"result": "refused", "code": 4, "reason": "changed",
          "detail": "the system refused to replace /Applications/Probe.app"}, Outcome.FAILED),
        ({"result": "refused", "code": 4, "reason": "not_newer", "detail": "this helper's bundle is not newer"},
         Outcome.FAILED),
        ({"result": "error", "code": 1, "reason": "lock_failed", "detail": "the instance lock: EIO"}, Outcome.FAILED),
    ],
)
def test_what_the_helper_answers_is_the_outcome_and_its_staged_copy_is_thrown_away(mac, answer, outcome):
    data = archive("0.1.52", answer=answer)
    feed = Feed(manifest("0.1.52", mac["key"].sign(data, "0.1.52")), {ARCHIVE_URL: data})
    tree = same_tree(mac["app"])
    result = install(mac, feed)
    assert result["outcome"] == outcome, result
    assert result["helper"] == {"result": answer["result"], "reason": answer["reason"], "undo_failed": False}
    if outcome == Outcome.FAILED:
        assert f"{answer['result']} ({answer['reason']}, exit {answer['code']})" in result["error"]
    assert same_tree(mac["app"]) == tree
    nothing_left(mac)
    assert [c["args"] for c in helper_calls(mac["apps"])] == [[str(mac["app"])]]


@pytest.mark.parametrize(
    "answer",
    [
        {"silent": True, "code": 1, "swap": True},  # swapped, then its answer was lost
        {"result": "error", "code": 1, "reason": "app_started", "undo_failed": True, "swap": True},
    ],
    ids=["answer lost", "old copy started, undo failed"],
)
def test_a_new_release_in_place_without_swapped_is_installed_and_the_old_app_waits_for_the_sweep(mac, answer):
    """The helper really swapped, then its answer was lost, or it could not swap back
    from under an old copy that started: the app reads the new version, so the
    install happened. The old app is not removed now (only after a `swapped` the
    helper verified) and never by this Python; the sweep has the new app's helper
    remove it once nothing runs from it."""
    data = archive("0.1.52", answer=answer)
    feed = Feed(manifest("0.1.52", mac["key"].sign(data, "0.1.52")), {ARCHIVE_URL: data})
    result = install(mac, feed)
    assert result["outcome"] == Outcome.INSTALLED and result["version_after"] == "0.1.52", result
    assert version_of(mac["app"]) == "0.1.52"
    assert [c["args"][:1] for c in helper_calls(mac["apps"])] == [[str(mac["app"])]], "no --remove yet"
    left = [p for p in appinstall.leftovers(mac["app"]) if p.is_dir()]
    assert len(left) == 1 and version_of(left[0]) == "0.1.51", "the old app is left for the sweep"
    assert appinstall.sweep(mac["app"], mac["home"]) == [left[0].name]
    assert helper_calls(mac["apps"])[-1] == {"bundle": "Probe.app", "args": ["--remove", str(left[0])]}
    nothing_left(mac)


@pytest.mark.parametrize("reason", ["verify_failed", "changed"])
def test_a_new_app_that_failed_its_checks_after_the_swap_is_never_installed_or_trusted(mac, reason):
    """The helper swapped, the new app failed its post-swap check (`verify_failed`, or
    what moved is not what was checked: `changed`), and the swap back failed: the app
    reads the new version, but it is FAILED, its helper never runs `--remove`, and
    the old app (the last verified copy) stays where the answer says."""
    data = archive("0.1.52", answer={"result": "error", "code": 1, "reason": reason, "undo_failed": True,
                                     "detail": "EIO", "swap": True})
    feed = Feed(manifest("0.1.52", mac["key"].sign(data, "0.1.52")), {ARCHIVE_URL: data})
    result = install(mac, feed)
    assert result["outcome"] == Outcome.FAILED, result
    assert result["helper"] == {"result": "error", "reason": reason, "undo_failed": True}
    assert f"error ({reason}, undo failed, exit 1)" in result["error"]
    left = [p for p in appinstall.leftovers(mac["app"]) if p.is_dir()]
    assert len(left) == 1 and version_of(left[0]) == "0.1.51"
    assert f"the old app is at {left[0]}" in result["error"]
    assert [c["args"] for c in helper_calls(mac["apps"])] == [[str(mac["app"])]], "no --remove"


def test_a_staged_copy_something_runs_from_is_never_deleted_here(mac):
    """A refused answer with a process under the staged copy: it is left for the
    sweep, which also leaves it while that process runs."""
    data = archive("0.1.52", answer={"result": "refused", "code": 4, "reason": "unsigned"})
    feed = Feed(manifest("0.1.52", mac["key"].sign(data, "0.1.52")), {ARCHIVE_URL: data})
    after_download = []
    feed.during_download = lambda: after_download.append(True)

    def lister():
        if not after_download:
            return []
        return [(4242, str(p / "Contents" / "MacOS" / EXE)) for p in appinstall.leftovers(mac["app"]) if p.is_dir()]

    result = install(mac, feed, lister=lister)
    assert result["outcome"] == Outcome.FAILED, result
    left = [p for p in appinstall.leftovers(mac["app"]) if p.is_dir()]
    assert len(left) == 1 and version_of(left[0]) == "0.1.52"
    assert appinstall.sweep(mac["app"], mac["home"], lister=lister) == []
    assert left[0].exists()


def test_a_helper_stopped_halfway_keeps_its_staged_copy_for_the_next_run(mac):
    """An error with the helper's journal beside the app: the staged copy is
    the helper's to finish the swap from (`recover`), never deleted here."""
    data = archive("0.1.52", answer={"result": "error", "code": 1, "detail": "stopped"})
    feed = Feed(manifest("0.1.52", mac["key"].sign(data, "0.1.52")), {ARCHIVE_URL: data})
    journal = mac["apps"] / appinstall.HELPER_JOURNAL_NAME
    journal.write_text("{}")
    result = install(mac, feed)
    assert result["outcome"] == Outcome.FAILED
    staged = [p for p in appinstall.leftovers(mac["app"]) if p.is_dir()]
    assert len(staged) == 1 and appinstall.helper_of(staged[0]) is not None


def test_recover_has_the_staged_releases_own_helper_finish_an_interrupted_swap(tmp_path):
    """The helper stopped between its two renames: the app is missing, the old
    one aside, the journal names the staged copy. The service only runs that
    copy's helper again, which finishes it."""
    home = tmp_path / "home"
    folder = home / "Applications"
    folder.mkdir(parents=True)
    staged = make_app(folder, "0.1.52", helper=True, name=f"{appinstall.STAGING_PREFIX}abc")
    aside = make_app(folder, "0.1.51", name=f"{appinstall.STAGING_PREFIX}abc.previous")
    app = folder / appupdate.APP_NAME
    journal = folder / appinstall.HELPER_JOURNAL_NAME
    journal.write_text(json.dumps({"target": str(app), "own": str(staged), "aside": str(aside)}))
    done = appinstall.recover(home)
    assert done and "swapped" in done[0], done
    assert version_of(app) == "0.1.52" and not journal.exists()
    assert helper_calls(folder) == [{"bundle": staged.name, "args": [str(app)]}]
    assert appinstall.recover(home) == [], "nothing left to finish"
    # A journal naming something else, or an app that is there: never acted on.
    journal.write_text(json.dumps({"target": str(app), "own": str(aside), "aside": "/elsewhere"}))
    assert appinstall.recover(home) == []
    journal.write_text(json.dumps({"target": "/etc/x", "own": str(staged), "aside": str(aside)}))
    assert appinstall.recover(home) == []


def test_the_sweep_has_the_installed_apps_helper_remove_an_old_bundle(mac):
    """An old bundle a swap left (older than the app) is removed only by the
    installed app's own helper (--remove); a staged copy never swapped in (as
    new as the app or newer) and a download are ours and deleted here; one a
    process runs from is left."""
    shutil.rmtree(mac["app"])
    app = make_app(mac["apps"], "0.1.52", helper=True)
    old = make_app(mac["apps"], "0.1.51", name=f"{appinstall.STAGING_PREFIX}old")
    never = make_app(mac["apps"], "0.1.53", name=f"{appinstall.STAGING_PREFIX}never")
    download = mac["apps"] / f"{appinstall.STAGING_PREFIX}dl.tar.gz"
    download.write_bytes(b"x")
    busy = make_app(mac["apps"], "0.1.50", name=f"{appinstall.STAGING_PREFIX}busy")
    busy_exe = str(busy / "Contents" / "MacOS" / EXE)
    removed = appinstall.sweep(app, mac["home"], lister=lambda: [(4242, busy_exe)])
    assert sorted(removed) == sorted([old.name, never.name, download.name])
    assert not old.exists() and not never.exists() and not download.exists() and busy.exists()
    assert helper_calls(mac["apps"]) == [{"bundle": "Probe.app", "args": ["--remove", str(old)]}]
    # An installed app without the helper (an older release) leaves old bundles for later.
    shutil.rmtree(app)
    plain = make_app(mac["apps"], "0.1.52")
    assert appinstall.sweep(plain, mac["home"]) == []
    assert busy.exists()


def test_what_a_stopped_removal_left_is_finished_by_the_installed_apps_helper(mac):
    """`--remove` renames the old bundle to `<name>.deleting` first; stopped
    halfway, what is left (no Info.plist any more) is the installed app's
    helper's to delete, never this Python's, and never while something runs
    from it."""
    shutil.rmtree(mac["app"])
    app = make_app(mac["apps"], "0.1.52", helper=True)
    half = mac["apps"] / f"{appinstall.STAGING_PREFIX}old.deleting"
    (half / "Contents" / "MacOS").mkdir(parents=True)
    (half / "Contents" / "MacOS" / EXE).write_text("x")
    busy = [(4242, str(half / "Contents" / "MacOS" / EXE))]
    assert appinstall.sweep(app, mac["home"], lister=lambda: busy) == [] and half.exists()
    assert appinstall.sweep(app, mac["home"]) == [half.name]
    assert not half.exists()
    assert helper_calls(mac["apps"]) == [{"bundle": "Probe.app", "args": ["--remove", str(half)]}]


def test_recover_compares_the_journals_real_paths_with_the_folders(tmp_path):
    """The helper writes its journal with real paths; ~/Applications reached
    through a link is the same folder."""
    real = tmp_path / "real" / "Applications"
    real.mkdir(parents=True)
    home = tmp_path / "home"
    home.mkdir()
    (home / "Applications").symlink_to(real)
    staged = make_app(real, "0.1.52", helper=True, name=f"{appinstall.STAGING_PREFIX}abc")
    aside = make_app(real, "0.1.51", name=f"{appinstall.STAGING_PREFIX}abc.previous")
    journal = real / appinstall.HELPER_JOURNAL_NAME
    journal.write_text(json.dumps({"target": os.path.realpath(real / appupdate.APP_NAME),
                                   "own": os.path.realpath(staged), "aside": os.path.realpath(aside)}))
    done = appinstall.recover(home)
    assert done and "swapped (finished)" in done[0], done
    assert version_of(real / appupdate.APP_NAME) == "0.1.52" and not journal.exists()


def _journal_halfway(folder: Path, *, staged_answer: dict | None, staged_helper: bool = True,
                     aside_helper: bool = True) -> tuple[Path, Path, Path, Path]:
    """A two-rename swap stopped mid-undo: the app missing, the new bundle at its
    staged path (its helper answering `staged_answer`, or none), the old app aside."""
    staged = make_app(folder, "0.1.52", helper=staged_helper, name=f"{appinstall.STAGING_PREFIX}abc")
    if staged_answer is not None:
        (staged / "Contents" / "MacOS" / "probe-swap.answer").write_text(json.dumps(staged_answer))
    aside = make_app(folder, "0.1.51", helper=aside_helper, name=f"{appinstall.STAGING_PREFIX}abc.previous")
    app = folder / appupdate.APP_NAME
    journal = folder / appinstall.HELPER_JOURNAL_NAME
    journal.write_text(json.dumps({"target": str(app), "own": str(staged), "aside": str(aside)}))
    return app, staged, aside, journal


@pytest.mark.parametrize("staged", ["refuses", "has no helper"])
def test_recover_has_the_old_app_put_itself_back_when_the_new_bundle_cannot_finish(tmp_path, staged):
    """The new bundle failed its check and the helper stopped mid-undo: the new
    bundle's helper refuses (its signature fails) or is gone. The old app moved
    aside puts itself back with its own helper; the journal goes."""
    home = tmp_path / "home"
    folder = home / "Applications"
    folder.mkdir(parents=True)
    app, new, aside, journal = _journal_halfway(
        folder, staged_answer={"result": "refused", "code": 4, "reason": "unsigned"} if staged == "refuses" else None,
        staged_helper=staged == "refuses")
    done = appinstall.recover(home)
    assert done and done[0].startswith(f"put the old app back at {app}"), done
    assert version_of(app) == "0.1.51" and not aside.exists() and not journal.exists()
    calls = [c["bundle"] for c in helper_calls(folder)]
    assert calls == ([new.name] if staged == "refuses" else []) + [aside.name]
    # The new bundle, never the app, is a staged copy the next sweep deletes.
    assert new.exists()


def test_recover_says_reinstall_when_no_helper_can_put_an_app_back(tmp_path):
    home = tmp_path / "home"
    folder = home / "Applications"
    folder.mkdir(parents=True)
    app, _new, aside, journal = _journal_halfway(
        folder, staged_answer={"result": "refused", "code": 4, "reason": "unsigned"}, aside_helper=False)
    done = appinstall.recover(home)
    assert len(done) == 1 and "refused (unsigned)" in done[0] and done[0].endswith("reinstall Probe"), done
    assert not app.exists() and aside.exists() and journal.exists()


@pytest.mark.parametrize("helper_answer", [None, {"result": "refused", "code": 4, "reason": "not_newer"}])
def test_the_sweep_has_the_installed_helper_judge_a_same_version_copy(mac, helper_answer):
    """The same version beside the app: the installed app's helper removes it when it is
    the app a repair replaced (it fails its signature check); a copy that helper refuses
    (one that verifies: a staged copy never swapped in) is ours and deleted here."""
    shutil.rmtree(mac["app"])
    app = make_app(mac["apps"], "0.1.52", helper=True)
    if helper_answer is not None:
        (app / "Contents" / "MacOS" / "probe-swap.answer").write_text(json.dumps(helper_answer))
    same = make_app(mac["apps"], "0.1.52", name=f"{appinstall.STAGING_PREFIX}same")
    assert appinstall.sweep(app, mac["home"]) == [same.name]
    assert not same.exists()
    assert helper_calls(mac["apps"]) == [{"bundle": "Probe.app", "args": ["--remove", str(same)]}]


# -- codesign: integrity AND the Probe team -------------------------------------------------


def _codesign(tmp_path: Path, code: int) -> Path:
    script = tmp_path / "codesign"
    script.write_text(f"#!/bin/sh\nprintf '%s\\n' \"$@\" > {tmp_path}/codesign-args\n"
                      + ("echo 'invalid signature' >&2\n" if code else "") + f"exit {code}\n")
    script.chmod(0o755)
    return script


def test_codesign_verifies_the_staged_bundle_deep_strict_and_signed_by_the_probe_team(mac, tmp_path, monkeypatch):
    monkeypatch.setattr(appinstall, "CODESIGN", str(_codesign(tmp_path, 0)))
    result = install(mac, release(mac))
    assert result["outcome"] == Outcome.INSTALLED and result["codesign"] == "verified"
    args = (tmp_path / "codesign-args").read_text().splitlines()
    assert args[:3] == ["--verify", "--deep", "--strict"]
    assert args[3:5] == ["-R", (
        "=anchor apple generic and certificate 1[field.1.2.840.113635.100.6.2.6] exists"
        " and certificate leaf[field.1.2.840.113635.100.6.1.13] exists"
        ' and certificate leaf[subject.OU] = "2HDWBQ9P3D"'
    )], "Developer ID only: the CA intermediate, a Developer ID Application leaf, the team"
    assert Path(args[5]).name.startswith(appinstall.STAGING_PREFIX), "the staged bundle, before its helper runs"


def test_a_bundle_codesign_refuses_is_never_installed(mac, tmp_path, monkeypatch):
    monkeypatch.setattr(appinstall, "CODESIGN", str(_codesign(tmp_path, 1)))
    result = install(mac, release(mac))
    assert result["outcome"] == Outcome.FAILED and "codesign refused" in result["error"]
    assert version_of(mac["app"]) == "0.1.51"
    assert helper_calls(mac["apps"]) == [], "its helper never runs"
    nothing_left(mac)


#: A checkout of prbe-ai/desktop beside this one (`PROBE_DESKTOP_CHECKOUT` names another).
DESKTOP = Path(os.environ.get("PROBE_DESKTOP_CHECKOUT") or Path.home() / "desktop")


def test_the_helpers_names_and_words_are_desktops():
    """What this side reads from the helper is what desktop's probe-swap.rs writes:
    the team, the staging prefix, the journal and `.deleting` names, the Info.plist
    key and every `result` word (each with its `Outcome::word` arm)."""
    assert appinstall.TEAM_ID == "2HDWBQ9P3D"
    helper = DESKTOP / "src-tauri" / "src" / "bin" / "probe-swap.rs"
    if not helper.is_file():  # a checkout of prbe-ai/desktop with the helper
        pytest.skip(f"no {helper}")
    text = helper.read_text()
    assert f'const TEAM_ID: &str = "{appinstall.TEAM_ID}";' in text
    assert f'const STAGING_PREFIX: &str = "{appinstall.STAGING_PREFIX}";' in text
    assert f'const JOURNAL_NAME: &str = "{appinstall.HELPER_JOURNAL_NAME}";' in text
    assert f'const DELETING_SUFFIX: &str = "{appinstall.HELPER_DELETING_SUFFIX}";' in text
    requirement = appinstall.TEAM_REQUIREMENT.removeprefix("=").replace(appinstall.TEAM_ID, "{TEAM_ID}")
    joined = re.sub(r"\\\n\s*", "", text)  # Rust's string continuations
    assert requirement.replace('"', '\\"') in joined, "the same Developer ID requirement"
    words = dict(re.findall(r'Outcome::(\w+) => "(\w+)"', text))
    assert sorted(words.values()) == sorted(appinstall.HELPER_RESULTS)
    assert f"<key>{appinstall.HELPER_KEY}</key>" in (DESKTOP / "src-tauri" / "Info.plist").read_text()


def _codesign_broken_marker(tmp_path: Path) -> Path:
    """A codesign that refuses any bundle holding `Contents/BROKEN` (an app whose seal
    broke) and verifies every other one."""
    script = tmp_path / "codesign"
    script.write_text('#!/bin/sh\nfor last; do :; done\n'
                      'if [ -e "$last/Contents/BROKEN" ]; then echo "a sealed resource is missing or invalid" >&2; exit 1; fi\n'
                      "exit 0\n")
    script.chmod(0o755)
    return script


def test_a_repair_is_never_current_while_the_app_fails_codesign(mac, tmp_path, monkeypatch):
    """`repair`: the installed app (0.1.52) fails codesign. The same version is the
    latest: it is installed over it (the helper takes the same version over a broken
    app), never `current`; the repaired app's helper removes the broken copy. With
    no release of that version: failed, `reinstall Probe`. A verifying app: current."""
    monkeypatch.setattr(appinstall, "CODESIGN", str(_codesign_broken_marker(tmp_path)))
    shutil.rmtree(mac["app"])
    app = mac["app"] = make_app(mac["apps"], "0.1.52", helper=True)
    (app / "Contents" / "BROKEN").write_text("x")
    data = archive("0.1.52")
    feed = Feed(manifest("0.1.52", mac["key"].sign(data, "0.1.52")), {ARCHIVE_URL: data})
    assert install(mac, feed)["outcome"] == Outcome.CURRENT, "without `repair` nothing looks"
    result = install(mac, feed, repair=True)
    assert result["outcome"] == Outcome.INSTALLED and result.get("repair") is True, result
    assert (result["version_before"], result["version_after"]) == ("0.1.52", "0.1.52")
    assert not (app / "Contents" / "BROKEN").exists(), "the repaired app is in"
    assert result["old_bundle"] == "removed"
    nothing_left(mac)
    assert install(mac, feed, repair=True)["outcome"] == Outcome.CURRENT, "it verifies now"
    (app / "Contents" / "BROKEN").write_text("x")
    older = Feed(None)
    result = install(mac, older, repair=True)
    assert result["outcome"] == Outcome.FAILED and result["error"].endswith("reinstall Probe"), result


def test_a_repair_counts_as_installed_only_on_swapped(mac, tmp_path, monkeypatch):
    """A repair keeps the version: an answer lost before the helper swapped reads the
    same version as before, which says nothing. It is failed, never installed."""
    monkeypatch.setattr(appinstall, "CODESIGN", str(_codesign_broken_marker(tmp_path)))
    shutil.rmtree(mac["app"])
    app = mac["app"] = make_app(mac["apps"], "0.1.52", helper=True)
    (app / "Contents" / "BROKEN").write_text("x")
    data = archive("0.1.52", answer={"silent": True, "code": 1})
    feed = Feed(manifest("0.1.52", mac["key"].sign(data, "0.1.52")), {ARCHIVE_URL: data})
    result = install(mac, feed, repair=True)
    assert result["outcome"] == Outcome.FAILED and result["helper"]["reason"] == "no_answer", result
    assert (app / "Contents" / "BROKEN").exists()


def test_a_repair_whose_undo_failed_never_deletes_the_old_app_of_the_same_version(mac, tmp_path, monkeypatch):
    """A repair swapped, the new app failed its check and the swap back failed: the
    staged path holds the old (broken) app at the same version as the new one. The
    helper's `old` names it, so this Python never deletes it."""
    monkeypatch.setattr(appinstall, "CODESIGN", str(_codesign_broken_marker(tmp_path)))
    shutil.rmtree(mac["app"])
    app = mac["app"] = make_app(mac["apps"], "0.1.52", helper=True)
    (app / "Contents" / "BROKEN").write_text("x")
    data = archive("0.1.52", answer={"result": "error", "code": 1, "reason": "verify_failed", "undo_failed": True,
                                     "swap": True})
    feed = Feed(manifest("0.1.52", mac["key"].sign(data, "0.1.52")), {ARCHIVE_URL: data})
    result = install(mac, feed, repair=True)
    assert result["outcome"] == Outcome.FAILED, result
    left = [p for p in appinstall.leftovers(mac["app"]) if p.is_dir()]
    assert len(left) == 1 and (left[0] / "Contents" / "BROKEN").exists(), "the old app stays"
    assert result["old_app"] == str(left[0])


# -- running the helper ----------------------------------------------------------------------


def _script(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "probe-swap"
    path.write_text(f"#!/bin/sh\n{body}\n")
    path.chmod(0o755)
    return path


def test_the_helper_runs_with_a_clean_environment_and_its_last_json_line_is_the_answer(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_TOKEN", "secret")
    helper = _script(tmp_path, 'echo noise; echo "{\\"result\\":\\"swapped\\",\\"env\\":\\"$PROBE_TOKEN\\"}"; exit 0')
    assert appinstall.run_helper([str(helper), "/x"]) == (0, {"result": "swapped", "env": ""})
    silent = _script(tmp_path, "echo boom >&2; exit 1")
    assert appinstall.run_helper([str(silent)]) == (1, {"result": "error", "reason": "no_answer", "detail": "boom"})
    slow = _script(tmp_path, "sleep 30")
    code, answer = appinstall.run_helper([str(slow)], timeout=0.5)
    assert code != 0 and answer["result"] == "error"
    assert appinstall.run_helper([str(tmp_path / "missing")])[1]["result"] == "error"


@pytest.mark.skipif(sys.platform != "darwin", reason="macOS: posix_spawn with the responsibility disclaim")
def test_on_macos_the_helper_is_spawned_as_its_own_responsible_process(tmp_path):
    """The disclaim call exists (macOS 10.14+), the helper runs through it and
    only its stdio reaches it."""
    assert appinstall._disclaim_available()  # noqa: SLF001
    inherited = os.open(tmp_path / "held", os.O_WRONLY | os.O_CREAT)
    os.set_inheritable(inherited, True)
    helper = _script(tmp_path, f'[ -e /dev/fd/{inherited} ] && echo leaked >&2; echo "{{\\"result\\":\\"removed\\"}}"; exit 0')
    try:
        code, out, err = appinstall._spawn_disclaimed([str(helper), "--remove", "/x"], 30)  # noqa: SLF001
    finally:
        os.close(inherited)
    assert (code, out.strip(), err) == (0, '{"result":"removed"}', "")


def test_without_the_disclaim_the_helper_is_never_run_and_nothing_is_downloaded(mac, tmp_path, monkeypatch):
    """A macOS without `responsibility_spawnattrs_setdisclaim`: run any other way
    the helper's change would be judged by this Python. The install fails before
    the download (the app's own updater installs at its launch), and run_helper
    starts nothing."""
    monkeypatch.setattr(appinstall, "supported", lambda: True)
    monkeypatch.setattr(appinstall, "_disclaim_available", lambda: False)
    marker = tmp_path / "ran"
    helper = _script(tmp_path, f"touch {marker}; echo '{{\"result\":\"swapped\"}}'")
    assert appinstall.run_helper([str(helper), "/x"]) == (-1, {
        "result": "error", "reason": "no_disclaim", "detail": "this macOS cannot start the update helper as its own process"})
    assert not marker.exists()
    feed = release(mac)
    result = install(mac, feed, lister=lambda: [])
    assert result["outcome"] == Outcome.FAILED and "cannot start the update helper" in result["error"], result
    assert feed.downloads() == [] and helper_calls(mac["apps"]) == []
    assert version_of(mac["app"]) == "0.1.51"
    nothing_left(mac)


# -- the update cycle's app step --------------------------------------------------------------


def _updater(**kwargs) -> updater.Updater:
    return updater.Updater(
        version="0.304.0", emit=lambda *a: None, changed=lambda: None, stop=lambda r: None,
        action_running=lambda: False, discovering=lambda: False, **kwargs,
    )


@pytest.fixture
def closed_mac(service_home, monkeypatch):  # noqa: F811 -- the fixture
    """The service's home with Probe 0.1.51 in ~/Applications, closed, on a
    machine where the service installs a closed app (macOS), and a release."""
    home = service_home.home
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)  # autoupdate.json under this HOME
    enable_auto_update(home)
    app = make_app(home / "Applications", "0.1.51")
    key = Key()
    data = archive("0.1.52")
    feed = Feed(manifest("0.1.52", key.sign(data, "0.1.52")), {ARCHIVE_URL: data})
    monkeypatch.setattr(updater, "_installs_closed_app", lambda: True)
    monkeypatch.setattr(appinstall, "install_closed", functools.partial(
        appinstall.install_closed, endpoints=(ENDPOINT,), pubkey=key.public_b64(), fetcher=feed,
        machine_arch="aarch64"))
    if (Path("/Applications") / appupdate.APP_NAME).exists():
        pytest.skip("a real /Applications/Probe.app is found first")
    return {"home": home, "app": app, "feed": feed, "key": key}


def _steps(seen: list) -> list:
    return [(e["step"], e["state"]) for t, e in seen if t == "update.step"]


def test_the_cycle_installs_a_closed_apps_update_and_its_next_launch_is_not_due(closed_mac):
    seen = []
    up = _updater()
    up.emit = lambda topic, payload: seen.append((topic, payload))
    step = asyncio.run(up._app("cyc1", "schedule"))  # noqa: SLF001
    swapped = {"result": "swapped", "reason": "done", "undo_failed": False}
    assert step == {"state": "done", "outcome": "installed", "version_before": "0.1.51", "version_after": "0.1.52",
                    "helper": swapped}
    assert _steps(seen) == [("app", "started"), ("app", "done")]
    done_event = [e for t, e in seen if t == "update.step" and e["state"] == "done"][0]
    assert done_event["helper"] == swapped, "the step event carries the helper's answer"
    assert up.state["app"]["helper"] == swapped
    assert version_of(closed_mac["app"]) == "0.1.52"
    status = up.app_public()
    assert status["due"] is False and status["reason"] == AppCheckReason.CHECKED_RECENTLY
    assert status["last"]["via"] == updater.VIA_SERVICE_INSTALL
    assert status["last"]["result"] == AppResult.UPDATED
    assert (status["last"]["version_before"], status["last"]["version_after"]) == ("0.1.51", "0.1.52")
    record = json.loads(paths.update_state_path().read_text())
    assert record["app"]["result"] == "updated" and record["last_app_check"] == status["last_check"]
    launch = up._launch_check({"version": "0.1.52", "force": False}, {"outcome": "recent"})  # noqa: SLF001
    assert launch == {"due": False, "reason": AppCheckReason.CHECKED_RECENTLY, "cycle_id": None}
    assert asyncio.run(up._app("cyc2", "schedule")) == {"state": "skipped", "outcome": "checked_recently"}  # noqa: SLF001
    assert len(closed_mac["feed"].downloads()) == 1


def test_a_release_without_the_helper_leaves_the_apps_launch_check_due_and_is_not_fetched_again(closed_mac):
    data = archive("0.1.52", helper=False)
    feed = closed_mac["feed"]
    feed.manifest = manifest("0.1.52", closed_mac["key"].sign(data, "0.1.52"))
    feed.files[ARCHIVE_URL] = data
    up = _updater()
    step = asyncio.run(up._app("cyc1", "schedule"))  # noqa: SLF001
    assert step["state"] == "skipped" and step["outcome"] == Outcome.NO_HELPER, step
    status = up.app_public()
    assert status["due"] is True and status["last_check"] is None and status["last"] is None
    assert up.state["app_install_no_helper"]["version"] == "0.1.52"
    step = asyncio.run(_updater()._app("cyc2", "schedule"))  # noqa: SLF001 -- the next service
    assert step["outcome"] == Outcome.NO_HELPER
    assert len(feed.downloads()) == 1, "the same release is not downloaded again"


def test_a_skip_records_no_check_so_the_apps_own_updater_runs_at_its_launch(closed_mac):
    lock = _hold_instance_lock(closed_mac["home"])
    try:
        up = _updater()
        step = asyncio.run(up._app("cyc1", "schedule"))  # noqa: SLF001
    finally:
        lock.close()
    assert step["state"] == "skipped" and step["outcome"] == Outcome.APP_RUNNING, step
    status = up.app_public()
    assert status["due"] is True and status["last_check"] is None and status["last"] is None
    assert version_of(closed_mac["app"]) == "0.1.51"


def test_a_failed_install_is_the_app_step_and_due_again(closed_mac):
    closed_mac["feed"].files[ARCHIVE_URL] = b"not the signed archive"
    up = _updater()
    step = asyncio.run(up._app("cyc1", "schedule"))  # noqa: SLF001
    assert step["state"] == "failed" and step["outcome"] == "failed" and "does not verify" in step["error"]
    assert up.app_public()["due"] is True and up.app_public()["reason"] == AppCheckReason.LAST_FAILED


def test_a_launch_check_that_takes_the_app_during_the_install_keeps_its_record(closed_mac):
    """The person opened the app while the service downloaded: its launch
    check was handed the app's check, and the service's result never replaces
    that record, whether the install then stops (the lock) or completes."""
    for round_, holds_lock in enumerate((True, False)):
        paths.update_state_path().unlink(missing_ok=True)
        up = _updater()
        held = []

        def launch(up=up, held=held, holds_lock=holds_lock):
            up._launch_check({"version": "0.1.51", "force": False}, {"outcome": "running", "cycle_id": "cyc1"})  # noqa: SLF001
            if holds_lock:
                held.append(_hold_instance_lock(closed_mac["home"]))

        closed_mac["feed"].during_download = launch
        try:
            step = asyncio.run(up._app(f"cyc{round_}", "schedule"))  # noqa: SLF001
        finally:
            for handle in held:
                handle.close()
        assert step["outcome"] == (Outcome.APP_RUNNING if holds_lock else Outcome.INSTALLED), step
        assert up.state["app"]["state"] == "delegated" and up.state["app"]["via"] == "update.check_now", holds_lock


def test_an_update_the_app_downloaded_but_never_installed_is_installed_once_the_app_is_gone(closed_mac):
    """An open app downloaded an update (`ready`: it installs at the quit) and was
    killed before it installed it. Closed now, the service installs it; while the
    app still runs (its lock held), the `ready` record stays the app's."""
    up = _updater()
    ready = {"state": "ready", "delegated_at": time.time() - 60, "cycle_id": "c0", "trigger": "schedule",
             "via": "app.check", "version": "0.1.51", "owner": 3, "owner_pid": os.getpid() + 1,
             "at": time.time() - 30, "ready_at": time.time() - 30, "result": "ready",
             "version_before": "0.1.51", "version_after": "0.1.52", "error": None}
    up.state["app"] = dict(ready)
    lock = _hold_instance_lock(closed_mac["home"])
    try:
        step = asyncio.run(up._app("cyc1", "schedule"))  # noqa: SLF001
    finally:
        lock.close()
    assert step["outcome"] == Outcome.APP_RUNNING
    assert up.state["app"] == ready, "the app may still install it at its quit"
    step = asyncio.run(up._app("cyc2", "schedule"))  # noqa: SLF001
    assert step == {"state": "done", "outcome": "installed", "version_before": "0.1.51", "version_after": "0.1.52",
                    "helper": {"result": "swapped", "reason": "done", "undo_failed": False}}
    assert up.state["app"]["via"] == updater.VIA_SERVICE_INSTALL and up.state["app"]["result"] == "updated"
    assert version_of(closed_mac["app"]) == "0.1.52"


def test_a_ready_update_of_a_connected_app_waits_for_its_quit(closed_mac):
    """The app that downloaded it is still connected: it installs it itself at
    its quit or at a quiet moment; the service touches nothing."""
    ready = {"state": "ready", "delegated_at": time.time() - 60, "cycle_id": "c0", "trigger": "schedule",
             "via": "app.check", "version": "0.1.51", "owner": 3, "owner_pid": os.getpid(),
             "at": time.time() - 30, "ready_at": time.time() - 30, "result": "ready",
             "version_before": "0.1.51", "version_after": "0.1.52", "error": None}
    up = _updater(app_connected=lambda: 1, app_alive=lambda serial: serial == 3)
    up.state["app"] = dict(ready)
    step = asyncio.run(up._app("cyc1", "schedule"))  # noqa: SLF001
    assert step == {"state": "skipped", "outcome": "ready_waiting", "version_after": "0.1.52"}
    assert closed_mac["feed"].requests == []
    assert up.state["app"] == ready


def _ready_record(owner_pid: int) -> dict:
    return {"state": "ready", "delegated_at": time.time() - 60, "cycle_id": "c0", "trigger": "schedule",
            "via": "app.check", "version": "0.1.51", "owner": 3, "owner_pid": owner_pid,
            "at": time.time() - 30, "ready_at": time.time() - 30, "result": "ready",
            "version_before": "0.1.51", "version_after": "0.1.52", "error": None}


@pytest.mark.parametrize(
    ("connected", "owner_alive"),
    [(1, False), (0, True)],
    ids=["owner gone, another app connected", "owner alive, no app connected"],
)
def test_a_ready_update_is_installed_only_with_its_owner_gone_and_no_app_connected(closed_mac, connected, owner_alive):
    """The service installs a `ready` update only when the app that downloaded
    it is gone AND no app is connected at all: another open copy, or an owner
    still alive whose connection the service does not count, keeps it the
    app's."""
    ready = _ready_record(os.getpid())
    up = _updater(app_connected=lambda: connected, app_alive=lambda serial: owner_alive and serial == 3)
    up.state["app"] = dict(ready)
    step = asyncio.run(up._app("cyc1", "schedule"))  # noqa: SLF001
    assert step == {"state": "skipped", "outcome": "ready_waiting", "version_after": "0.1.52"}
    assert closed_mac["feed"].requests == [] and version_of(closed_mac["app"]) == "0.1.51"
    assert up.state["app"] == ready


def _halfway_swap(closed_mac) -> Path:
    folder = closed_mac["app"].parent
    staged = make_app(folder, "0.1.52", helper=True, name=f"{appinstall.STAGING_PREFIX}abc")
    aside = folder / f"{appinstall.STAGING_PREFIX}abc.previous"
    closed_mac["app"].rename(aside)
    journal = folder / appinstall.HELPER_JOURNAL_NAME
    journal.write_text(json.dumps({"target": str(closed_mac["app"]), "own": str(staged), "aside": str(aside)}))
    return journal


def test_the_service_start_finishes_a_halfway_swap_with_no_cycle_due(closed_mac, monkeypatch):
    """After discovery, before (and without) any cycle: the staged release's helper
    finishes the swap, so the app is there for whoever looks."""
    journal = _halfway_swap(closed_mac)
    monkeypatch.setattr(updater, "auto_update_enabled", lambda: False)
    started = []

    async def start():
        up = _updater()
        up.start = lambda trigger: started.append(trigger)
        up.attach(asyncio.get_running_loop())
        up.after_discovery()
        assert up._recovering is not None  # noqa: SLF001
        await up._recovering  # noqa: SLF001

    asyncio.run(start())
    assert started == []
    assert closed_mac["app"].exists() and version_of(closed_mac["app"]) == "0.1.52" and not journal.exists()


def test_a_cycle_looks_for_the_app_only_after_the_start_time_recover(closed_mac, monkeypatch):
    """The start-time recover is still running (a slow helper) when a cycle's app
    step begins: the step waits for it before anything looks for the app."""
    import threading

    events, lock = [], threading.Lock()
    calls = []

    def recover(home, **kw):
        with lock:
            calls.append(None)
            n = len(calls)
        if n == 1:
            time.sleep(0.4)
        events.append(("recovered", n))
        return []

    real_installed = appupdate.installed

    def installed():
        events.append(("looked",))
        return real_installed()

    monkeypatch.setattr(appinstall, "recover", recover)
    monkeypatch.setattr(appupdate, "installed", installed)
    monkeypatch.setattr(appinstall, "install_closed", lambda path, **kw: {
        "outcome": "current", "version_before": "0.1.51", "version_after": "0.1.51"})

    async def run():
        up = _updater()
        up.start = lambda trigger: None  # this test runs the app step itself
        up.attach(asyncio.get_running_loop())
        up.after_discovery()
        await asyncio.sleep(0)
        return await up._app("c1", "schedule")  # noqa: SLF001

    step = asyncio.run(run())
    assert step["outcome"] == "current", step
    assert events.index(("recovered", 1)) < events.index(("looked",)), events


def test_the_no_helper_release_is_forgotten_only_once_it_is_not_the_question(closed_mac):
    """`app_install_no_helper` stays through a failure that says nothing about the
    latest release; it goes once the app is current or installed, or once a
    different latest version is seen."""
    feed, key = closed_mac["feed"], closed_mac["key"]
    remembered = {"version": "0.1.52", "at": time.time()}
    up = _updater()
    up.state["app_install_no_helper"] = dict(remembered)
    feed.manifest = {"not": "a manifest"}
    step = asyncio.run(up._app("c1", "schedule"))  # noqa: SLF001
    assert step["outcome"] == Outcome.FAILED, step
    assert up.state["app_install_no_helper"] == remembered, "a failure keeps it"
    # A different latest release (whose download then fails): forgotten.
    feed.manifest = manifest("0.1.53", key.sign(b"another archive", "0.1.53"))
    feed.files[ARCHIVE_URL] = b"not it"
    up = _updater()
    up.state["app_install_no_helper"] = dict(remembered)
    step = asyncio.run(up._app("c2", "schedule"))  # noqa: SLF001
    assert step["outcome"] == Outcome.FAILED and "app_install_no_helper" not in up.state, step
    # The app is current (it installed 0.1.52 itself at a launch): forgotten.
    feed.manifest = manifest("0.1.51", key.sign(b"x", "0.1.51"))
    up = _updater()
    up.state["app_install_no_helper"] = dict(remembered)
    step = asyncio.run(up._app("c3", "schedule"))  # noqa: SLF001
    assert step["outcome"] == Outcome.CURRENT and "app_install_no_helper" not in up.state, step


def test_a_swap_left_halfway_is_finished_before_the_app_is_looked_for(closed_mac):
    """The helper stopped between its two renames: no Probe.app to find. The
    cycle has the staged release's own helper finish it first, then goes on."""
    folder = closed_mac["app"].parent
    staged = make_app(folder, "0.1.52", helper=True, name=f"{appinstall.STAGING_PREFIX}abc")
    aside = folder / f"{appinstall.STAGING_PREFIX}abc.previous"
    closed_mac["app"].rename(aside)
    journal = folder / appinstall.HELPER_JOURNAL_NAME
    journal.write_text(json.dumps({"target": str(closed_mac["app"]), "own": str(staged), "aside": str(aside)}))
    step = asyncio.run(_updater()._app("c1", "schedule"))  # noqa: SLF001
    assert closed_mac["app"].exists() and not journal.exists()
    assert version_of(closed_mac["app"]) == "0.1.52"
    assert step["outcome"] == "current", step


def test_a_refused_swap_is_not_tried_again_for_a_week(closed_mac):
    data = archive("0.1.52", answer={"result": "not_permitted", "code": 5, "reason": "not_permitted",
                                     "detail": "Operation not permitted"})
    feed = closed_mac["feed"]
    feed.manifest = manifest("0.1.52", closed_mac["key"].sign(data, "0.1.52"))
    feed.files[ARCHIVE_URL] = data
    up = _updater()
    assert asyncio.run(up._app("cyc1", "schedule"))["outcome"] == Outcome.NOT_PERMITTED  # noqa: SLF001
    downloads = len(feed.downloads())
    assert downloads == 1
    step = asyncio.run(_updater()._app("cyc2", "schedule"))  # noqa: SLF001 -- the next service
    assert step["outcome"] == Outcome.NOT_PERMITTED
    assert len(feed.downloads()) == downloads, "not tried again"


@pytest.mark.parametrize(("reason", "backs_off"), [("unsigned", True), ("not_newer", True), ("not_probe", True),
                                                   ("quarantined", True), ("changed", False)])
def test_a_release_its_helper_refused_for_good_is_not_downloaded_every_cycle(closed_mac, reason, backs_off):
    """A refusal that stays the same for the same release (unsigned, not_newer, not_probe,
    quarantined) is recorded with the helper's answer, and that release is skipped
    (`refused_release`, no download) until another release is the latest or a week
    passes. Any other refusal is tried again next cycle."""
    feed, key = closed_mac["feed"], closed_mac["key"]
    data = archive("0.1.52", answer={"result": "refused", "code": 4, "reason": reason})
    feed.manifest = manifest("0.1.52", key.sign(data, "0.1.52"))
    feed.files[ARCHIVE_URL] = data
    seen = []
    up = _updater()
    up.emit = lambda topic, payload: seen.append((topic, payload))
    step = asyncio.run(up._app("cyc1", "schedule"))  # noqa: SLF001
    answer = {"result": "refused", "reason": reason, "undo_failed": False}
    assert step["outcome"] == Outcome.FAILED and step["helper"] == answer, step
    assert [e for t, e in seen if t == "update.step" and e["state"] == "failed"][0]["helper"] == answer
    assert up.state["app"]["helper"] == answer
    assert len(feed.downloads()) == 1
    up.state.pop("last_app_check")  # due again at once
    step = asyncio.run(up._app("cyc2", "schedule"))  # noqa: SLF001
    if not backs_off:
        assert "app_install_refused_release" not in up.state
        assert step["outcome"] == Outcome.FAILED and len(feed.downloads()) == 2
        return
    assert up.state["app_install_refused_release"]["version"] == "0.1.52"
    assert step["state"] == "skipped" and step["outcome"] == Outcome.REFUSED_RELEASE, step
    assert len(feed.downloads()) == 1, "the same release is not downloaded again"
    # A week later it is tried again.
    up.state["app_install_refused_release"]["at"] -= appinstall.REFUSED_BACKOFF_S + 1
    assert asyncio.run(up._app("cyc3", "schedule"))["outcome"] == Outcome.FAILED  # noqa: SLF001
    assert len(feed.downloads()) == 2
    # Another release is looked at at once, and the refusal forgotten once it installs.
    newer_data = archive("0.1.53")
    feed.manifest = manifest("0.1.53", key.sign(newer_data, "0.1.53"))
    feed.files[ARCHIVE_URL] = newer_data
    step = asyncio.run(up._app("cyc4", "schedule"))  # noqa: SLF001
    assert step["outcome"] == Outcome.INSTALLED and "app_install_refused_release" not in up.state, step


def test_an_install_whose_undo_failed_is_sticky_until_the_app_verifies(closed_mac, tmp_path, monkeypatch):
    """The new app failed its check after the swap and could not be swapped back: the
    service keeps a record, every step says `reinstall`, and `probe doctor` says to
    reinstall Probe. The next cycles are never `current` while the app fails codesign:
    the same release is installed over it, and the record goes once the app verifies."""
    from probe.cli import service_calls

    monkeypatch.setattr(appinstall, "CODESIGN", str(_codesign_broken_marker(tmp_path)))
    feed, key = closed_mac["feed"], closed_mac["key"]
    data = archive("0.1.52", answer={"result": "error", "code": 1, "reason": "verify_failed", "undo_failed": True,
                                     "swap": True})
    feed.manifest = manifest("0.1.52", key.sign(data, "0.1.52"))
    feed.files[ARCHIVE_URL] = data
    up = _updater()
    step = asyncio.run(up._app("cyc1", "schedule"))  # noqa: SLF001
    assert step["outcome"] == Outcome.FAILED and step["reinstall"] is True, step
    assert up.state["app_install_broken"]["reason"] == "verify_failed"
    assert up.state["app"]["reinstall"] is True
    assert version_of(closed_mac["app"]) == "0.1.52"
    status = {"update": {"app": {"last": up.state["app"]}, "last_result": {"ok": True, "steps": {"app": step}}}}
    text = service_calls.app_update_text(service_calls._filled(status, {"sessions": []})["update"]["app"])  # noqa: SLF001
    assert "reinstall Probe" in text
    # The next cycle: the same release, 0.1.52, is the app's version, but the app fails codesign.
    (closed_mac["app"] / "Contents" / "BROKEN").write_text("x")
    good = archive("0.1.52")
    feed.manifest = manifest("0.1.52", key.sign(good, "0.1.52"))
    feed.files[ARCHIVE_URL] = good
    up.state.pop("last_app_check")
    step = asyncio.run(up._app("cyc2", "schedule"))  # noqa: SLF001
    assert step["outcome"] == Outcome.INSTALLED, step
    assert "app_install_broken" not in up.state and "reinstall" not in step
    assert not (closed_mac["app"] / "Contents" / "BROKEN").exists()
    old = [p for p in appinstall.leftovers(closed_mac["app"]) if p.is_dir()]
    assert [version_of(p) for p in old] == ["0.1.51"], "the last verified copy stayed while the app was broken"
    up.state.pop("last_app_check")
    assert asyncio.run(up._app("cyc3", "schedule"))["outcome"] == Outcome.CURRENT  # noqa: SLF001
    assert appinstall.leftovers(closed_mac["app"]) == [], "removed once the app verifies"


@pytest.mark.parametrize("connected", [False, True])
def test_no_cycle_ever_launches_the_app_where_it_installs_closed_apps(service_home, monkeypatch, tmp_path, connected):  # noqa: F811
    """macOS's variant of test_service_updater.py's "no cycle ever launches the
    app" (those assert Linux's `app_closed`): with the install stubbed, a closed
    or an open app, no `open` runs and the app's executable never starts."""
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    enable_auto_update(service_home.home)
    bin_dir = service_home.home / "bin"
    fake_open(bin_dir)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    marker = tmp_path / "app-ran"
    app = make_app(service_home.home / "Applications", "0.1.51")
    (app / "Contents" / "MacOS" / EXE).write_text(f"#!/bin/sh\ntouch {marker}\n")
    monkeypatch.setattr(updater, "_installs_closed_app", lambda: True)
    installs = []
    monkeypatch.setattr(appinstall, "install_closed", lambda path, **kw: installs.append(path) or {
        "outcome": "current", "version_before": "0.1.51", "version_after": "0.1.51"})
    if (Path("/Applications") / appupdate.APP_NAME).exists():
        pytest.skip("a real /Applications/Probe.app is found first")
    sent = []
    up = _updater(app_connected=lambda: int(connected), app_listeners=lambda: int(connected),
                  app_target=lambda: 7 if connected else None,
                  send_app_check=lambda serial, payload: sent.append(serial) or True)
    step = asyncio.run(up._app("cyc1", "schedule"))  # noqa: SLF001
    assert open_calls(service_home.home) == []
    assert not marker.exists()
    if connected:
        assert step["outcome"] == "app_check_sent" and sent == [7] and installs == []
    else:
        assert step["outcome"] == "current" and installs == [app]


def test_off_macos_a_closed_app_is_still_only_skipped(service_home, monkeypatch):  # noqa: F811
    """Linux and Windows have no desktop app: the step stays as it was."""
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    enable_auto_update(service_home.home)
    make_app(service_home.home / "Applications", "0.1.51")
    monkeypatch.setattr(updater, "_installs_closed_app", lambda: False)
    if (Path("/Applications") / appupdate.APP_NAME).exists():
        pytest.skip("a real /Applications/Probe.app is found first")
    step = asyncio.run(_updater()._app("cyc1", "schedule"))  # noqa: SLF001
    assert step == {"state": "skipped", "outcome": "app_closed", "version": "0.1.51"}


@pytest.mark.parametrize("mac_os", [True, False])
def test_the_install_is_imported_before_step_one_replaces_the_files(mac_os):
    """Plan R2: the cycle's preload imports the install (and cryptography) on
    macOS, before the update child replaces the files it would import from."""
    names = ["probe.service.appinstall", "cryptography.hazmat.primitives.asymmetric.ed25519", "tarfile",
             "urllib.request"]
    code = (
        "import sys; from probe.service import updater; "
        f"updater._installs_closed_app = lambda: {mac_os}; updater.preload(); "
        f"print(*[n in sys.modules for n in {names!r}])"
    )
    done = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, timeout=60, cwd="/")
    loaded = done.stdout.split()
    assert loaded[:2] == [str(mac_os)] * 2, done.stderr
    if mac_os:
        assert loaded[2:] == ["True", "True"], done.stderr


def test_the_service_start_path_never_imports_the_install():
    done = subprocess.run(
        [sys.executable, "-I", "-c", "import probe.service.server, sys; "
         "print('probe.service.appinstall' in sys.modules, any(m.startswith('cryptography') for m in sys.modules))"],
        capture_output=True, text=True, timeout=60, cwd="/",
    )
    assert done.stdout.split() == ["False", "False"], done.stderr


# -- what probe doctor says ------------------------------------------------------------------


def test_doctor_names_who_installed_the_app_and_why_a_cycle_skipped():
    from probe.cli import service_calls

    record = {"state": "done", "result": "updated", "via": updater.VIA_SERVICE_INSTALL, "version_before": "0.1.51",
              "version_after": "0.1.52", "at": time.time()}
    status = {"update": {"app": {"last": record},
                         "last_result": {"ok": True, "steps": {"app": {"state": "done", "outcome": "installed"}}}}}
    view = service_calls._filled(status, {"sessions": []})  # noqa: SLF001
    text = service_calls.app_update_text(view["update"]["app"])
    assert text.startswith("0.1.51 -> 0.1.52, installed by the Probe service while the app was closed")
    for outcome in ("not_writable", "no_helper", "refused_release"):
        skipped = {"update": {"app": {"last": None}, "last_result": {"ok": True, "steps": {"app": {
            "state": "skipped", "outcome": outcome, "detail": "the reason"}}}}}
        text = service_calls.app_update_text(service_calls._filled(skipped, {"sessions": []})["update"]["app"])  # noqa: SLF001
        assert f"skipped ({outcome}: the reason" in text and "next launch" in text
    assert service_calls._filled({"update": {}}, {"sessions": []})["update"]["app"] is None  # noqa: SLF001
