"""The Probe service installs a CLOSED desktop app's update (plan E1/E3; owner 2026-10-24).

An open app is asked (`app.check`) and its own signed updater installs at a
quiet moment. A closed app used to wait for its next launch, and the person
waited for the update there. Now the update cycle installs it while nothing
of the app runs, starting no app process (a hidden `--background-update`
launch showed a Dock icon and "Stop Running in Background"; removed 10-23):

    manifest   the endpoint the app's updater reads (ENDPOINTS), parsed as
               tauri-plugin-updater 2.14.0 parses it, the entry its updater
               would pick (`darwin-<arch>-app`, then `darwin-<arch>`); never a
               version older than or equal to the installed bundle's
               CFBundleShortVersionString
    download   to a staging folder beside the bundle (same volume), bounded
               in time (each read too) and size, https only
    verify     the minisign signature exactly as the app's updater checks it
               (minisign-verify 0.3.0 with legacy allowed, then the signed
               version, `requireSignedVersion`): the key id, `Ed` (the file
               itself) or `ED` (its BLAKE2b-512, what Tauri's signer makes),
               the global signature over the trusted comment, and the trusted
               comment's `version:` equal to the announced version (build
               metadata compared literally, as the semver crate does). The
               key is PUBKEY, pinned here; anything that does not verify is
               refused
    extract    regular files, folders and links that stay inside the bundle
               (every link resolved, through chains of links); no `..`, no
               absolute paths, no hard links, devices or setuid bits, no entry
               twice (case- and normalization-folded, as APFS compares names),
               bounded in count and size; then the bundle id
               `ai.prbe.desktop`, the version the signature names, its
               executable, and `codesign --verify --deep --strict -R` against
               the Probe team's Developer ID (TEAM_REQUIREMENT)
    swap       NEVER by this Python: macOS App Management blocks a change to a
               notarized app by code not signed by the app's team and tells
               the person (WWDC22 10096). The staged release's own helper
               (`Contents/MacOS/probe-swap`, prbe-ai/desktop
               `src-tauri/src/bin/probe-swap.rs`, signed by the same team) runs
               as its OWN responsible process (posix_spawn with
               `responsibility_spawnattrs_setdisclaim`; a macOS without it
               fails the step before the download, and the app's own updater
               installs at its launch): it takes the app's instance lock,
               checks the app again under it, finds no process under the app,
               swaps with `renamex_np(RENAME_SWAP)` (two journalled renames
               where the volume cannot swap, finished by the next run:
               `recover`), verifies the new app and swaps back if it does not
               verify or an old copy started from the old bundle meanwhile.
               Its answer is read by its machine words (`result`, `reason`),
               never its `detail`. The old bundle is deleted by the NEW app's
               helper (`--remove`), now or on a later cycle (`sweep`); this
               Python deletes only a staged copy that still holds the NEW
               version with nothing running from it

Skipped, never prompted: a bundle or folder this user cannot write
(`not_writable`), a Probe app process or the instance lock held
(`app_running`), macOS refusing the helper's rename (the helper's
`not_permitted`: EPERM or EACCES, App Management or permissions), a
release without the helper (`no_helper`, every release before it; not
downloaded again): the app's own updater handles those at its next launch.

Someone opening the app mid-install: before the swap the old app opens as
always (its launch check is handed to it and its own updater runs; the helper
then finds the instance lock held and the staged copy is thrown away). During
the swap (milliseconds, under the instance lock) the launch resolves the
bundle path to the old or the new bundle, never a mix (one atomic rename). An
old copy that started from the old bundle in that window opens its window and
waits for the instance lock only at its update gate (the desktop app takes the
lock on a thread); the helper finds it under the old bundle's new name and
swaps back under it, so for those few milliseconds it may read resources from
the new bundle.

macOS only (`supported`): Linux and Windows have no desktop app; their app
step stays as it was. Stdlib at import (the service's start path, plan S1);
`cryptography` (Ed25519) is imported when a signature is checked, and
`preload` (the update cycle, before step 1 replaces the CLI's files, plan R2).
"""

from __future__ import annotations

import base64
import contextlib
import hashlib
import json
import os
import re
import secrets
import shutil
import stat
import subprocess
import sys
import time
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from . import appupdate

BUNDLE_ID = appupdate.BUNDLE_ID

#: prbe-ai/desktop `src-tauri/tauri.conf.json`, `plugins.updater.endpoints`:
#: the manifest the app's own updater reads. Keep the two the same.
ENDPOINTS = ("https://github.com/prbe-ai/desktop-releases/releases/latest/download/latest.json",)
#: prbe-ai/desktop `src-tauri/tauri.conf.json`, `plugins.updater.pubkey`,
#: verbatim: base64 of the minisign public key file ("untrusted comment:
#: minisign public key: AF847825AFE96A41" and the key). The app verifies every
#: update against it; so does this. A new key there is a new constant here.
PUBKEY = (
    "dW50cnVzdGVkIGNvbW1lbnQ6IG1pbmlzaWduIHB1YmxpYyBrZXk6IEFGODQ3ODI1QUZFOTZBNDEKUldSQmF1bXZKWGlFcno5ajlV"
    "SW1rWk1aUE83ejNxL3lubVY2MmQ0L1N2K0tiWTZZaFJPMnRDdUQK"
)
#: `plugins.updater.requireSignedVersion` there: a signature must name the
#: version it was made for (its trusted comment's `version:`).
REQUIRE_SIGNED_VERSION = True

#: The app's own bound (`background_update.rs` TIME_LIMIT): manifest and download.
TIME_LIMIT_S = 10 * 60
#: Each read from the network, at most.
READ_TIMEOUT_S = 30.0
MANIFEST_MAX_BYTES = 1024 * 1024
#: The archive (7 MB in 0.1.52) and what it unpacks to, at most.
ARCHIVE_MAX_BYTES = 256 * 1024 * 1024
UNPACKED_MAX_BYTES = 1024 * 1024 * 1024
MAX_ENTRIES = 20_000
CODESIGN = "/usr/bin/codesign"
CODESIGN_TIMEOUT_S = 120.0
#: The app's instance lock (prbe-ai/desktop `background_update.rs` INSTANCE_LOCK,
#: in Tauri's `app_data_dir()`: `~/Library/Application Support/<identifier>`).
#: Every app process holds it (flock) for its life.
INSTANCE_LOCK = Path("Library") / "Application Support" / BUNDLE_ID / "instance.lock"
#: Beside the bundle: the staged bundle (after the swap, the old one) and its
#: archive. A name without `.app`: Finder and LaunchServices see a folder.
#: prbe-ai/desktop `probe-swap.rs` `STAGING_PREFIX`: its `--remove` takes only these.
STAGING_PREFIX = f".{appupdate.APP_NAME}.probe-update-"
#: The Developer ID team that signs every Probe release: the certificate in
#: prbe-ai/desktop release.yml's `APPLE_CERTIFICATE` secret, "Developer ID
#: Application: Richard Wei (2HDWBQ9P3D)" (desktop CLAUDE.md, Releases; `spctl`
#: reports it as the origin of 0.1.53 and 0.1.54 on agent-os-matrix's macOS
#: job). Also pinned in desktop `probe-swap.rs` `TEAM_ID`: a new team is a new
#: constant in both, in the same release.
TEAM_ID = "2HDWBQ9P3D"
#: Developer ID only: Apple's Developer ID CA as the intermediate, a Developer
#: ID Application leaf, the team. The same text in desktop `probe-swap.rs`
#: `team_requirement` and release.yml's signature check.
TEAM_REQUIREMENT = (
    "=anchor apple generic and certificate 1[field.1.2.840.113635.100.6.2.6] exists"
    " and certificate leaf[field.1.2.840.113635.100.6.1.13] exists"
    f' and certificate leaf[subject.OU] = "{TEAM_ID}"'
)
#: The release's update helper (prbe-ai/desktop `src-tauri/src/bin/probe-swap.rs`)
#: and the Info.plist key that says a release has it (`ProbeSwapHelper` = 1).
HELPER_NAME = "probe-swap"
HELPER_KEY = "ProbeSwapHelper"
#: Beside the app while the helper's two renames are under way (`recover`);
#: desktop `probe-swap.rs` `JOURNAL_NAME`.
HELPER_JOURNAL_NAME = f".{appupdate.APP_NAME}.probe-swap.json"
#: A folder the helper's `--remove` renamed before deleting it (`DELETING_SUFFIX`):
#: what is left of it is the installed app's helper's to delete (`sweep`).
HELPER_DELETING_SUFFIX = ".deleting"
#: Its codesign checks of two bundles, the swap and `gktool scan` (60 s), at most.
HELPER_TIMEOUT_S = 5 * 60.0
#: <spawn.h> POSIX_SPAWN_CLOEXEC_DEFAULT (Apple): only the descriptors the file
#: actions name reach the helper.
_POSIX_SPAWN_CLOEXEC_DEFAULT = 0x4000
#: A refused swap (`not_permitted`) is not tried again for this long: each try
#: can raise a macOS notification about the refusal.
REFUSED_BACKOFF_S = 7 * 24 * 3600


class Outcome:
    """What `install_closed` did: the cycle's `app` step outcome."""

    #: The newer app is in place (`version_before` -> `version_after`).
    INSTALLED = "installed"
    #: The installed app is the newest (nothing downloaded).
    CURRENT = "current"
    #: The manifest, download, signature, archive or swap failed (`error`).
    FAILED = "failed"
    #: Skipped: this user cannot write the bundle or its folder.
    NOT_WRITABLE = "not_writable"
    #: Skipped: a Probe app process runs, or holds the instance lock.
    APP_RUNNING = "app_running"
    #: Skipped: the system refused the helper's rename (macOS App Management).
    NOT_PERMITTED = "not_permitted"
    #: Skipped: the release has no update helper (`ProbeSwapHelper`); the app's
    #: own updater installs it at its next launch.
    NO_HELPER = "no_helper"
    #: Skipped: this release's helper refused it earlier for a reason that does
    #: not change for the same release (`PERMANENT_REFUSALS`); not downloaded
    #: again for REFUSED_BACKOFF_S or until another release is the latest.
    REFUSED_RELEASE = "refused_release"


SKIPS = frozenset({
    Outcome.NOT_WRITABLE, Outcome.APP_RUNNING, Outcome.NOT_PERMITTED, Outcome.NO_HELPER, Outcome.REFUSED_RELEASE,
})


class InstallError(Exception):
    """A step that failed: its message is the step's `error`."""


class Skip(Exception):
    """A step that cannot go ahead now, harmlessly (`Outcome` in SKIPS)."""

    def __init__(self, outcome: str, detail: str) -> None:
        super().__init__(detail)
        self.outcome = outcome


def supported() -> bool:
    """The desktop app exists on macOS only."""
    return sys.platform == "darwin"


def preload() -> None:
    """What an install imports later, now (`updater.preload`, plan R2)."""
    import ctypes  # noqa: F401
    import ctypes.util  # noqa: F401
    import fcntl  # noqa: F401
    import signal  # noqa: F401
    import tempfile  # noqa: F401
    import plistlib  # noqa: F401
    import ssl  # noqa: F401
    import tarfile  # noqa: F401
    import urllib.request  # noqa: F401
    import zlib  # noqa: F401

    with contextlib.suppress(Exception):
        from probe.sdk import tls  # noqa: F401
    with contextlib.suppress(ImportError):
        from cryptography.hazmat.primitives.asymmetric import ed25519  # noqa: F401


# -- versions (the semver crate's, as tauri-plugin-updater compares them) ------

_SEMVER = re.compile(
    r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
)


def parse_version(text: object) -> tuple | None:
    """`(major, minor, patch, pre)` of a semver string (a leading `v` dropped,
    as the updater's `parse_version` does), or None."""
    if not isinstance(text, str):
        return None
    found = _SEMVER.fullmatch(text[1:] if text.startswith("v") else text)
    if found is None:
        return None
    pre = tuple(int(p) if p.isdigit() else p for p in found.group(4).split(".")) if found.group(4) else ()
    return int(found.group(1)), int(found.group(2)), int(found.group(3)), pre


def _pre_key(pre: tuple) -> tuple:
    # Semver precedence: no pre-release ranks above any; numeric below alphanumeric.
    if not pre:
        return (1,)
    return (0, tuple((0, p, "") if isinstance(p, int) else (1, 0, p) for p in pre))


def newer(version: str, than: str) -> bool:
    """Is `version` strictly newer than `than`? False when either is not semver."""
    a, b = parse_version(version), parse_version(than)
    if a is None or b is None:
        return False
    return (a[:3], _pre_key(a[3])) > (b[:3], _pre_key(b[3]))


def _build(text: str) -> str | None:
    return text.split("+", 1)[1] if "+" in text else None


def same_version(a: str, b: str) -> bool:
    """The signed-version check's equality: the semver crate's, `v` dropped,
    build metadata compared literally (`0.1.54+x` is not `0.1.54`); else the
    literal text."""
    pa, pb = parse_version(a), parse_version(b)
    if pa is not None and pb is not None:
        return pa == pb and _build(a) == _build(b)
    return a == b


# -- minisign, as minisign-verify 0.3.0 and tauri-plugin-updater 2.14.0 check it --


@dataclass(frozen=True)
class PublicKey:
    key_id: bytes  # 8 bytes
    key: bytes  # 32 bytes, Ed25519


@dataclass(frozen=True)
class Signature:
    algorithm: bytes  # b"Ed" (the data itself) or b"ED" (its BLAKE2b-512)
    key_id: bytes
    signature: bytes  # 64 bytes, over the data or its hash
    trusted_comment: str  # after "trusted comment: "
    global_signature: bytes  # 64 bytes, over signature + trusted comment

    @property
    def prehashed(self) -> bool:
        return self.algorithm == b"ED"


def _b64(text: str) -> bytes:
    try:
        return base64.b64decode(text, validate=True)
    except (ValueError, TypeError) as exc:
        raise InstallError("not valid base64") from exc


def _lines(text: str) -> list[str]:
    # Rust's `str::lines`: split at "\n", one trailing "\r" dropped from each.
    out = text.split("\n")
    if out and out[-1] == "":
        out.pop()
    return [line[:-1] if line.endswith("\r") else line for line in out]


def _text(blob: bytes, what: str) -> str:
    try:
        return blob.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InstallError(f"the {what} is not UTF-8") from exc


def parse_public_key(encoded: str) -> PublicKey:
    """tauri.conf.json's `pubkey`: base64 of a minisign key file, whose second
    line is base64 of `Ed` + key id (8) + key (32)."""
    lines = _lines(_text(_b64(encoded), "public key"))
    if len(lines) < 2:
        raise InstallError("the public key has no key line")
    raw = _b64(lines[1])
    if len(raw) != 42 or raw[:2] not in (b"Ed", b"ED"):
        raise InstallError("the public key is not a minisign Ed25519 key")
    return PublicKey(key_id=raw[2:10], key=raw[10:42])


def parse_signature(encoded: str) -> Signature:
    """A manifest entry's `signature`: base64 of a minisign `.sig` file (an
    untrusted comment, the signature line, the trusted comment, the global
    signature line)."""
    lines = _lines(_text(_b64(encoded), "signature"))
    if len(lines) < 4:
        raise InstallError("the signature is not a minisign signature")
    raw = _b64(lines[1])
    if len(raw) != 74:
        raise InstallError("the signature line has the wrong length")
    trusted = lines[2]
    if not trusted.startswith("trusted comment: "):
        raise InstallError("the signature has no trusted comment")
    global_signature = _b64(lines[3])
    if len(global_signature) != 64:
        raise InstallError("the global signature has the wrong length")
    if raw[:2] not in (b"Ed", b"ED"):
        raise InstallError("the signature algorithm is not supported")
    return Signature(
        algorithm=raw[:2],
        key_id=raw[2:10],
        signature=raw[10:74],
        trusted_comment=trusted[len("trusted comment: "):],
        global_signature=global_signature,
    )


def _ed25519_verify(key: bytes, signature: bytes, message: bytes) -> bool:
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError as exc:  # pinned in pyproject.toml; a broken env fails closed
        raise InstallError("this Probe install cannot check signatures (no `cryptography`)") from exc
    try:
        Ed25519PublicKey.from_public_bytes(key).verify(signature, message)
    except (InvalidSignature, ValueError):
        return False
    return True


def signed_version(trusted_comment: str) -> str | None:
    """The `version:` field of Tauri's trusted comment (tab-separated `key:value`)."""
    for field in trusted_comment.split("\t"):
        if field.startswith("version:"):
            return field[len("version:"):]
    return None


def verify(
    message: bytes,
    sig: Signature,
    key: PublicKey,
    announced_version: str,
    *,
    prehashed_digest: bytes | None = None,
    require_signed_version: bool = REQUIRE_SIGNED_VERSION,
) -> None:
    """Raise InstallError unless `sig` is `key`'s signature of `message` (or,
    for `ED`, of its BLAKE2b-512 `prehashed_digest`) and names
    `announced_version`. minisign-verify's `verify(.., allow_legacy=true)`,
    then the updater's `verify_signed_version`: the trusted comment is read
    only after the global signature proves it."""
    if sig.key_id != key.key_id:
        raise InstallError("the signature was made with a different key than the app's")
    if sig.prehashed:
        signed = prehashed_digest if prehashed_digest is not None else hashlib.blake2b(message, digest_size=64).digest()
    else:
        signed = message
    if not _ed25519_verify(key.key, sig.signature, signed):
        raise InstallError("the signature does not verify")
    if not _ed25519_verify(key.key, sig.global_signature, sig.signature + sig.trusted_comment.encode("utf-8")):
        raise InstallError("the signature's trusted comment does not verify")
    version = signed_version(sig.trusted_comment)
    if version is None:
        if require_signed_version:
            raise InstallError("the signature names no version")
        return
    if not same_version(version, announced_version):
        raise InstallError(f"the signature is for {version}, not the announced {announced_version}")


def verify_file(path: Path, sig: Signature, key: PublicKey, announced_version: str) -> None:
    """`verify` of a file: hashed in chunks for `ED`, read whole for `Ed`."""
    if sig.prehashed:
        digest = hashlib.blake2b(digest_size=64)
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        verify(b"", sig, key, announced_version, prehashed_digest=digest.digest())
    else:
        verify(path.read_bytes(), sig, key, announced_version)


# -- the manifest ------------------------------------------------------------------


@dataclass(frozen=True)
class Release:
    version: str
    url: str
    signature: str
    target: str  # the manifest key it came from ("" for a dynamic answer)


_RFC3339 = re.compile(r"\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}:\d{2}(\.\d+)?([Zz]|[+-]\d{2}:\d{2})")


def arch() -> str:
    """The architecture the app's updater names (`updater_arch`, its own build's
    `target_arch`): the universal app runs native, so the machine's, even when
    this Python runs under Rosetta."""
    machine = os.uname().machine
    if machine in ("arm64", "aarch64"):
        return "aarch64"
    if supported():
        with contextlib.suppress(OSError, subprocess.SubprocessError):
            done = subprocess.run(
                ["/usr/sbin/sysctl", "-n", "hw.optional.arm64"], capture_output=True, text=True, timeout=5
            )
            if done.stdout.strip() == "1":
                return "aarch64"
    return "x86_64" if machine in ("x86_64", "amd64") else machine


def targets(machine_arch: str | None = None) -> list[str]:
    """`get_urls`'s lookup order for a macOS `.app`: `{os}-{arch}-{installer}`, `{os}-{arch}`."""
    a = machine_arch or arch()
    return [f"darwin-{a}-app", f"darwin-{a}"]


def parse_manifest(data: object, machine_arch: str | None = None) -> tuple[str, dict | None]:
    """`(version, entry)` of a manifest as the updater deserializes it: a
    static one's `platforms[...]` for the first target it has, or a dynamic
    one's own `url`/`signature`. `entry` is None when no target matches."""
    if not isinstance(data, dict):
        raise InstallError("the manifest is not a JSON object")
    version = data.get("version", data.get("name"))
    if parse_version(version) is None:
        raise InstallError(f"the manifest's version {version!r} is not a version")
    pub_date = data.get("pub_date")
    if pub_date is not None and (not isinstance(pub_date, str) or not _RFC3339.fullmatch(pub_date)):
        raise InstallError("the manifest's pub_date is not an RFC 3339 date")
    platforms = data.get("platforms")
    if platforms is not None:
        if not isinstance(platforms, dict):
            raise InstallError("the manifest's platforms is not an object")
        for target in targets(machine_arch):
            entry = platforms.get(target)
            if isinstance(entry, dict) and isinstance(entry.get("url"), str) and isinstance(entry.get("signature"), str):
                return version, {**entry, "target": target}
        return version, None
    if not isinstance(data.get("url"), str) or not isinstance(data.get("signature"), str):
        raise InstallError("the manifest has neither platforms nor a url and signature")
    return version, {"url": data["url"], "signature": data["signature"], "target": ""}


# -- the network -------------------------------------------------------------------

USER_AGENT = "probe-service (desktop app update)"


class _Deadline:
    def __init__(self, seconds: float) -> None:
        self.seconds = seconds
        self.end = time.monotonic() + seconds

    def left(self) -> float:
        left = self.end - time.monotonic()
        if left <= 0:
            raise InstallError(f"no result within {self.seconds:g} s; gave up on the update")
        return left


def _opener():
    """urllib with the one TLS decision of this package (`probe.sdk.tls`: the OS
    store plus certifi, and the CA variables), the system's proxies (as the
    app's updater finds them), and redirects to https only."""
    import ssl
    import urllib.request

    try:
        from probe.sdk.tls import ssl_context

        context = ssl_context()
    except Exception:  # noqa: BLE001 -- the stdlib's default trust, never none
        context = ssl.create_default_context()

    class HttpsOnly(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
            if not str(newurl).startswith("https://"):
                raise InstallError(f"a redirect to {newurl.split('?')[0]} is not https")
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    return urllib.request.build_opener(urllib.request.HTTPSHandler(context=context), HttpsOnly())


def fetch(url: str, *, accept: str, limit: int, deadline: _Deadline, sink=None) -> bytes | int | None:
    """GET `url` (https only): its body (at most `limit` bytes), or with `sink`
    (a binary file) the number of bytes written to it. None: 204 No Content."""
    import urllib.error
    import urllib.request

    if not url.startswith("https://"):
        raise InstallError(f"{url.split('?')[0]} is not https")
    request = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": USER_AGENT})
    try:
        response = _opener().open(request, timeout=min(READ_TIMEOUT_S, deadline.left()))
    except urllib.error.HTTPError as exc:
        raise InstallError(f"{url.split('?')[0]} answered {exc.code}") from exc
    except (urllib.error.URLError, OSError) as exc:
        reason = getattr(exc, "reason", exc)
        raise InstallError(f"{url.split('?')[0]}: {reason}") from exc
    with response:
        if response.status == 204:
            return None
        length = response.headers.get("Content-Length")
        if length and length.isdigit() and int(length) > limit:
            raise InstallError(f"{url.split('?')[0]} is {length} bytes, over the {limit}-byte limit")
        body = bytearray()
        written = 0
        sock = getattr(getattr(getattr(response, "fp", None), "raw", None), "_sock", None)
        read = getattr(response, "read1", response.read)
        while True:
            # Each read waits at most what is left of the deadline: a server that
            # trickles a byte at a time cannot hold the step past it.
            left = deadline.left()
            if sock is not None:
                with contextlib.suppress(OSError):
                    sock.settimeout(min(READ_TIMEOUT_S, left))
            try:
                chunk = read(256 * 1024)
            except TimeoutError as exc:
                deadline.left()
                raise InstallError(f"{url.split('?')[0]}: no data for {min(READ_TIMEOUT_S, left):g} s") from exc
            except OSError as exc:
                raise InstallError(f"{url.split('?')[0]}: {exc}") from exc
            if not chunk:
                break
            written += len(chunk)
            if written > limit:
                raise InstallError(f"{url.split('?')[0]} is over the {limit}-byte limit")
            if sink is None:
                body += chunk
            else:
                sink.write(chunk)
    return bytes(body) if sink is None else written


def check(endpoints=ENDPOINTS, *, deadline: _Deadline, fetcher=fetch, machine_arch: str | None = None) -> tuple:
    """The updater's `check`: each endpoint in order, the first one that answers
    a manifest wins. `(version, entry)`; `(None, None)` for 204 No Content."""
    last: Exception | None = None
    for url in endpoints:
        try:
            body = fetcher(url, accept="application/json", limit=MANIFEST_MAX_BYTES, deadline=deadline)
        except InstallError as exc:
            last = exc
            continue
        if body is None:
            return None, None
        try:
            return parse_manifest(json.loads(body), machine_arch)
        except (InstallError, ValueError) as exc:
            last = exc
    raise InstallError(f"no update manifest: {last}" if last else "no update manifest")


# -- the archive -------------------------------------------------------------------


def _parts(name: str) -> tuple[str, ...]:
    if "\0" in name or "\\" in name:
        raise InstallError(f"the archive has an unsafe name {name!r}")
    if name.startswith("/"):
        raise InstallError(f"the archive has an absolute path {name!r}")
    parts = tuple(p for p in name.split("/") if p not in ("", "."))
    if ".." in parts:
        raise InstallError(f"the archive has a path outside it {name!r}")
    return parts


def _fold(parts: tuple[str, ...]) -> tuple[str, ...]:
    # APFS and HFS+ compare names case- and normalization-insensitively by default.
    return tuple(unicodedata.normalize("NFD", p).casefold() for p in parts)


def _real_dir(path: Path) -> bool:
    try:
        return stat.S_ISDIR(os.lstat(path).st_mode)
    except OSError:
        return False


def _mkdir(path: Path) -> None:
    # 0755 whatever the umask: every user of the Mac launches the app.
    os.mkdir(path, 0o700)
    os.chmod(path, 0o755)


def extract(archive: Path, root: Path) -> None:
    """Unpack a Tauri updater archive (`Probe.app/...`) into `root`, the
    bundle's own folder (its first path component dropped, as the updater's
    macOS install does), refusing anything unsafe. `root` exists and is empty."""
    import tarfile
    import zlib

    seen: set = set()
    links: set = set()
    top: str | None = None
    count = total = 0
    try:
        with tarfile.open(archive, mode="r:gz") as tar:
            for member in tar:
                count += 1
                if count > MAX_ENTRIES:
                    raise InstallError(f"the archive has more than {MAX_ENTRIES} entries")
                parts = _parts(member.name)
                if not parts:
                    continue
                if top is None:
                    if not parts[0].endswith(".app"):
                        raise InstallError(f"the archive holds {parts[0]!r}, not an app bundle")
                    top = parts[0]
                elif parts[0] != top:
                    raise InstallError("the archive holds more than one top-level folder")
                rel = parts[1:]
                if not rel:
                    if not member.isdir():
                        raise InstallError("the archive's bundle is not a folder")
                    continue
                key = _fold(rel)
                if key in seen:
                    raise InstallError(f"the archive has {'/'.join(rel)!r} twice")
                for i in range(1, len(rel)):
                    if _fold(rel[:i]) in links:
                        raise InstallError(f"the archive writes through the link {'/'.join(rel[:i])!r}")
                seen.add(key)
                target = root.joinpath(*rel)
                parent = target.parent
                # Parents the archive did not list: made here, each a real folder.
                for i in range(1, len(rel)):
                    step = root.joinpath(*rel[:i])
                    if not _real_dir(step):
                        if os.path.lexists(step):
                            raise InstallError(f"{'/'.join(rel[:i])!r} is not a folder")
                        _mkdir(step)
                if not _real_dir(parent):
                    raise InstallError(f"{'/'.join(rel[:-1])!r} is not a folder")
                if member.isdir():
                    if os.path.lexists(target):
                        if not _real_dir(target):
                            raise InstallError(f"{'/'.join(rel)!r} is not a folder")
                    else:
                        _mkdir(target)
                elif member.isreg():
                    total += member.size
                    if total > UNPACKED_MAX_BYTES:
                        raise InstallError(f"the archive unpacks to more than {UNPACKED_MAX_BYTES} bytes")
                    source = tar.extractfile(member)
                    if source is None:
                        raise InstallError(f"{'/'.join(rel)!r} cannot be read")
                    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
                    fd = os.open(target, flags, 0o600)
                    with os.fdopen(fd, "wb") as out:
                        copied = 0
                        for chunk in iter(lambda: source.read(1024 * 1024), b""):
                            copied += len(chunk)
                            out.write(chunk)
                        if copied != member.size:
                            raise InstallError(f"{'/'.join(rel)!r} is cut short")
                        # Never setuid, setgid, sticky or writable by others.
                        os.fchmod(out.fileno(), 0o755 if member.mode & 0o111 else 0o644)
                    with contextlib.suppress(OSError):
                        os.utime(target, (member.mtime, member.mtime))
                elif member.issym():
                    link = member.linkname
                    if not link or "\0" in link or link.startswith("/"):
                        raise InstallError(f"the link {'/'.join(rel)!r} points outside the bundle")
                    resolved = os.path.normpath(os.path.join(*rel[:-1], link) if len(rel) > 1 else link)
                    if resolved == ".." or resolved.startswith("../") or resolved.startswith("/"):
                        raise InstallError(f"the link {'/'.join(rel)!r} points outside the bundle")
                    os.symlink(link, target)
                    links.add(key)
                else:
                    raise InstallError(f"the archive has {'/'.join(rel)!r}, which is not a file, folder or link")
    except InstallError:
        raise
    except (tarfile.TarError, OSError, EOFError, zlib.error) as exc:
        raise InstallError(f"the archive could not be unpacked: {exc}") from exc
    if top is None:
        raise InstallError("the archive is empty")


def bundle_info(bundle: Path) -> dict:
    """The bundle's Info.plist (at most 1 MB), or InstallError."""
    import plistlib

    path = bundle / "Contents" / "Info.plist"
    try:
        if not stat.S_ISREG(os.lstat(path).st_mode) or os.lstat(path).st_size > 1024 * 1024:
            raise InstallError("the bundle's Info.plist is not a file")
        with open(path, "rb") as handle:
            data = plistlib.load(handle)
    except (OSError, ValueError, plistlib.InvalidFileException) as exc:
        raise InstallError(f"the bundle's Info.plist cannot be read: {exc}") from exc
    if not isinstance(data, dict):
        raise InstallError("the bundle's Info.plist is not a dictionary")
    return data


def check_bundle(bundle: Path, version: str) -> None:
    """The staged bundle is Probe at `version`, with its executable."""
    info = bundle_info(bundle)
    if info.get("CFBundleIdentifier") != BUNDLE_ID:
        raise InstallError(f"the update's bundle id is {info.get('CFBundleIdentifier')!r}, not {BUNDLE_ID}")
    found = info.get("CFBundleShortVersionString")
    if not isinstance(found, str) or not same_version(found, version):
        raise InstallError(f"the update's bundle is version {found!r}, not {version}")
    executable = info.get("CFBundleExecutable")
    if not isinstance(executable, str) or not executable or "/" in executable or executable in (".", ".."):
        raise InstallError("the update's bundle names no executable")
    path = bundle / "Contents" / "MacOS" / executable
    try:
        mode = os.lstat(path).st_mode
    except OSError as exc:
        raise InstallError(f"the update's executable {executable} is missing") from exc
    if not stat.S_ISREG(mode) or not mode & 0o100:
        raise InstallError(f"the update's executable {executable} is not an executable file")


def codesign_verify(bundle: Path, what: str = "the update") -> str:
    """`codesign --verify --deep --strict -R=<the Probe team>` on the staged
    bundle: integrity AND who signed it (an ad-hoc or another team's signature
    is refused; the service runs this bundle's helper next). "verified", or
    "unavailable" where there is no codesign (not macOS). InstallError otherwise
    (`what` names the bundle in its message)."""
    if not os.path.exists(CODESIGN):
        return "unavailable"
    try:
        done = subprocess.run(
            # `-R` and the requirement as two arguments: "=" then the text (attached,
            # `-R==…`, codesign reads an invalid requirement).
            [CODESIGN, "--verify", "--deep", "--strict", "-R", TEAM_REQUIREMENT, str(bundle)],
            capture_output=True,
            text=True,
            timeout=CODESIGN_TIMEOUT_S,
            stdin=subprocess.DEVNULL,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise InstallError(f"codesign could not run: {exc}") from exc
    if done.returncode != 0:
        raise InstallError(f"codesign refused {what}: {(done.stderr or done.stdout).strip()[:300]}")
    return "verified"


def app_broken(app: Path) -> str | None:
    """Why the installed app fails `codesign_verify`, or None when it passes
    (or there is no codesign to ask)."""
    try:
        codesign_verify(app, what="the installed app")
    except InstallError as exc:
        return str(exc)
    return None


# -- is the app running? -----------------------------------------------------------


_LIBSYSTEM: list = []


def _libsystem():
    """macOS libSystem (proc_pidpath, renamex_np), loaded once."""
    if not _LIBSYSTEM:
        import ctypes

        _LIBSYSTEM.append(ctypes.CDLL("/usr/lib/libSystem.B.dylib", use_errno=True))
    return _LIBSYSTEM[0]


def _darwin_exe_path(pid: int) -> str | None:
    """`proc_pidpath`: where pid's executable is NOW (it follows a rename)."""
    try:
        import ctypes

        buffer = ctypes.create_string_buffer(4096)
        size = _libsystem().proc_pidpath(ctypes.c_int(pid), buffer, ctypes.c_uint32(4096))
    except (OSError, AttributeError):
        return None
    if size <= 0:
        return None
    return buffer.raw[:size].decode("utf-8", "surrogateescape")


def processes() -> list[tuple[int, str]]:
    """`(pid, executable path)` of every process this user can see, as exact as
    the system says: Linux `/proc/<pid>/exe` (follows renames), macOS `ps`'s
    `comm` (every user's; the path it started from) and `proc_pidpath` where it
    answers (the path it runs from now). One process may be listed twice."""
    found: list[tuple[int, str]] = []
    if sys.platform.startswith("linux"):
        with contextlib.suppress(OSError):
            for entry in os.scandir("/proc"):
                if entry.name.isdigit():
                    with contextlib.suppress(OSError):
                        found.append((int(entry.name), os.readlink(f"/proc/{entry.name}/exe")))
        return found
    try:
        done = subprocess.run(
            ["/bin/ps", "-axww", "-o", "pid=,comm="], capture_output=True, text=True, timeout=15,
            stdin=subprocess.DEVNULL,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise InstallError(f"ps could not run: {exc}") from exc
    for line in done.stdout.splitlines():
        pid, _, path = line.strip().partition(" ")
        if pid.isdigit():
            found.append((int(pid), path.strip()))
            if supported():
                exact = _darwin_exe_path(int(pid))
                if exact:
                    found.append((int(pid), exact))
    return found


def _under(path: str, roots: list[str]) -> bool:
    return any(path == r or path.startswith(r.rstrip("/") + "/") for r in roots)


def _roots(*paths: Path) -> list[str]:
    out = []
    for path in paths:
        out.append(str(path))
        with contextlib.suppress(OSError):
            out.append(os.path.realpath(path))
    return sorted(set(out))


def running_from(*bundles: Path, lister=processes) -> list[int]:
    """The pids whose executable is under any of `bundles`."""
    roots = _roots(*bundles)
    return sorted({pid for pid, path in lister() if pid != os.getpid() and _under(path, roots)})


def instance_lock_path(home: Path) -> Path:
    return home / INSTANCE_LOCK


# -- the same-team helper (prbe-ai/desktop `src-tauri/src/bin/probe-swap.rs`) -------

#: The helper's `result` words (desktop `probe-swap.rs` `Outcome::word`); its
#: exit codes 0, 0, 3, 4, 5, 1. Each answer also carries a machine `reason`
#: (`Reason::word`) and, after an exchange, `old`: where the old bundle is.
HELPER_SWAPPED = "swapped"
HELPER_REMOVED = "removed"
HELPER_APP_RUNNING = "app_running"
HELPER_REFUSED = "refused"
HELPER_NOT_PERMITTED = "not_permitted"
HELPER_ERROR = "error"
HELPER_RESULTS = (HELPER_SWAPPED, HELPER_REMOVED, HELPER_APP_RUNNING, HELPER_REFUSED, HELPER_NOT_PERMITTED, HELPER_ERROR)
#: This side's own reasons for an `error` answer: the helper did not start or answer.
REASON_NO_DISCLAIM = "no_disclaim"
REASON_NOT_STARTED = "not_started"
REASON_NO_ANSWER = "no_answer"
#: The helper's reason when an old copy started from the old bundle during the swap.
REASON_APP_STARTED = "app_started"
#: An answer that is not `swapped`, with the new release already the app, counts
#: as installed only for these: the answer was lost (or the helper never ran and
#: something else put it there), or the helper could not swap back from under an
#: old copy that started (the new app was verified before the swap). Never for
#: `verify_failed` or `changed`: that new app is not the one checked.
INSTALLED_ANYWAY = frozenset({REASON_NO_ANSWER, REASON_NOT_STARTED, REASON_APP_STARTED})
#: The helper's reasons for an app that failed its checks after the swap; with
#: `undo_failed` that app may be the app now (`Updater`'s `app_install_broken`).
UNTRUSTED_AFTER_SWAP = frozenset({"verify_failed", "changed"})
#: The helper's `refused` reasons that stay the same for the same release: the
#: release is not tried again for REFUSED_BACKOFF_S unless another release is
#: the latest (`Outcome.REFUSED_RELEASE`).
PERMANENT_REFUSALS = frozenset({"unsigned", "not_newer", "not_probe", "quarantined"})


def helper_of(bundle: Path) -> Path | None:
    """The bundle's `Contents/MacOS/probe-swap`, when its Info.plist says it
    has one (`ProbeSwapHelper` = 1) and it is an executable file; else None."""
    try:
        info = bundle_info(bundle)
    except InstallError:
        return None
    flag = info.get(HELPER_KEY)
    if isinstance(flag, bool) or flag != 1:
        return None
    path = bundle / "Contents" / "MacOS" / HELPER_NAME
    try:
        mode = os.lstat(path).st_mode
    except OSError:
        return None
    return path if stat.S_ISREG(mode) and mode & 0o100 else None


def _helper_env() -> dict:
    # The helper reads nothing from its environment (its home comes from the
    # user database); a fixed PATH for the system tools it runs.
    return {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LANG": "C"}


def _answer(code: int, out: str, err: str) -> dict:
    for line in reversed(out.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            with contextlib.suppress(ValueError):
                data = json.loads(line)
                if isinstance(data, dict):
                    return data
    detail = err.strip()[-300:] or f"the update helper exited {code} and said nothing"
    return {"result": HELPER_ERROR, "reason": REASON_NO_ANSWER, "detail": detail}


def _wait(pid: int, timeout: float) -> int:
    import signal

    deadline = time.monotonic() + timeout
    while True:
        done, status = os.waitpid(pid, os.WNOHANG)
        if done == pid:
            return os.waitstatus_to_exitcode(status)
        if time.monotonic() >= deadline:
            with contextlib.suppress(OSError):
                os.kill(pid, signal.SIGKILL)
            _, status = os.waitpid(pid, 0)
            return os.waitstatus_to_exitcode(status)
        time.sleep(0.05)


def _disclaim_available() -> bool:
    try:
        return hasattr(_libsystem(), "responsibility_spawnattrs_setdisclaim")
    except OSError:
        return False


def _spawn_disclaimed(argv: list[str], timeout: float) -> tuple[int, str, str]:
    """posix_spawn the helper as its OWN responsible process
    (`responsibility_spawnattrs_setdisclaim`, looked up at run time as LLDB
    does): macOS then judges the change to the app by the helper's signature
    (the Probe team), not by this Python's. Only stdin/stdout/stderr reach it
    (POSIX_SPAWN_CLOEXEC_DEFAULT)."""
    import ctypes
    import tempfile

    libc = _libsystem()
    work = tempfile.mkdtemp(prefix="probe-swap-")
    out_path, err_path = os.path.join(work, "out"), os.path.join(work, "err")
    attr, actions = ctypes.c_void_p(), ctypes.c_void_p()
    pid = ctypes.c_int()
    try:
        if libc.posix_spawnattr_init(ctypes.byref(attr)) != 0:
            raise OSError("posix_spawnattr_init failed")
        try:
            if libc.posix_spawn_file_actions_init(ctypes.byref(actions)) != 0:
                raise OSError("posix_spawn_file_actions_init failed")
            try:
                if libc.responsibility_spawnattrs_setdisclaim(ctypes.byref(attr), ctypes.c_int(1)) != 0:
                    raise OSError("responsibility_spawnattrs_setdisclaim failed")
                if libc.posix_spawnattr_setflags(ctypes.byref(attr), ctypes.c_short(_POSIX_SPAWN_CLOEXEC_DEFAULT)) != 0:
                    raise OSError("posix_spawnattr_setflags failed")
                for fd, path, flags in (
                    (0, b"/dev/null", os.O_RDONLY),
                    (1, os.fsencode(out_path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC),
                    (2, os.fsencode(err_path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC),
                ):
                    if libc.posix_spawn_file_actions_addopen(
                        ctypes.byref(actions), ctypes.c_int(fd), path, ctypes.c_int(flags), ctypes.c_int(0o600)
                    ) != 0:
                        raise OSError("posix_spawn_file_actions_addopen failed")
                args = [os.fsencode(a) for a in argv]
                argv_c = (ctypes.c_char_p * (len(args) + 1))(*args, None)
                env = [f"{k}={v}".encode() for k, v in _helper_env().items()]
                envp = (ctypes.c_char_p * (len(env) + 1))(*env, None)
                rc = libc.posix_spawn(
                    ctypes.byref(pid), argv_c[0], ctypes.byref(actions), ctypes.byref(attr), argv_c, envp
                )
                if rc != 0:
                    raise OSError(rc, f"posix_spawn: {os.strerror(rc)}")
            finally:
                libc.posix_spawn_file_actions_destroy(ctypes.byref(actions))
        finally:
            libc.posix_spawnattr_destroy(ctypes.byref(attr))
        code = _wait(pid.value, timeout)
        out = Path(out_path).read_text(encoding="utf-8", errors="replace")
        err = Path(err_path).read_text(encoding="utf-8", errors="replace")
        return code, out, err
    finally:
        shutil.rmtree(work, ignore_errors=True)


def _spawn_plain(argv: list[str], timeout: float) -> tuple[int, str, str]:
    """Elsewhere (no desktop app; the tests): a plain child."""
    try:
        done = subprocess.run(
            argv, capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL, env=_helper_env()
        )
    except subprocess.TimeoutExpired:
        return -9, "", f"the update helper did not finish within {timeout:g} s"
    return done.returncode, done.stdout, done.stderr


def run_helper(argv: list[str], *, timeout: float = HELPER_TIMEOUT_S) -> tuple[int, dict]:
    """Run a bundle's update helper; `(exit code, its JSON answer)`. On macOS
    only as its own responsible process (posix_spawn with the disclaim
    attribute): without it the helper is not run at all, since macOS would
    judge its change by this Python and refuse it with a notification."""
    try:
        if supported():
            if not _disclaim_available():
                return -1, {"result": HELPER_ERROR, "reason": REASON_NO_DISCLAIM,
                            "detail": "this macOS cannot start the update helper as its own process"}
            code, out, err = _spawn_disclaimed(argv, timeout)
        else:
            code, out, err = _spawn_plain(argv, timeout)
    except (OSError, subprocess.SubprocessError) as exc:
        return -1, {"result": HELPER_ERROR, "reason": REASON_NOT_STARTED,
                    "detail": f"the update helper could not start: {exc}"}
    return code, _answer(code, out, err)


def lock_held(home: Path) -> bool:
    """Does an app process hold its instance lock now? Never creates it."""
    import fcntl

    try:
        fd = os.open(instance_lock_path(home), os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
    except OSError:
        return False
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return True
    except OSError:
        return False
    finally:
        os.close(fd)
    return False


def _remove(path: Path) -> bool:
    """Delete a download or staged copy of ours that was never the app (a real
    folder or file of this user, never through a link)."""
    try:
        info = os.lstat(path)
    except FileNotFoundError:
        return True
    except OSError:
        return False
    if info.st_uid != os.getuid():
        return False
    try:
        if stat.S_ISDIR(info.st_mode):
            shutil.rmtree(path)
        else:
            os.unlink(path)
    except OSError:
        return False
    return True


def leftovers(app: Path) -> list[Path]:
    """Downloads, staged copies and old bundles of ours beside `app`."""
    try:
        return sorted(p for p in app.parent.iterdir() if p.name.startswith(STAGING_PREFIX))
    except OSError:
        return []


def recover(home: Path, *, runner=run_helper, log=lambda message: None) -> list[str]:
    """A swap the helper left halfway (two renames, stopped between them: the
    app missing, the journal beside it): the staged bundle's own helper runs
    again and finishes it. The service never moves a bundle itself. Run before
    the app is looked for: until then there is no app to find. The helper
    writes its journal with real paths (`/private/var/...` for `/var/...`):
    both sides are compared resolved."""
    done = []
    for folder in (Path("/Applications"), home / "Applications"):
        journal = folder / HELPER_JOURNAL_NAME
        try:
            data = json.loads(journal.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(data, dict) or not isinstance(data.get("target"), str) or not isinstance(data.get("own"), str):
            continue
        real = os.path.realpath(folder)
        target, own = Path(os.path.realpath(data["target"])), Path(os.path.realpath(data["own"]))
        if (
            str(target.parent) != real
            or target.name != appupdate.APP_NAME
            or str(own.parent) != real
            or not own.name.startswith(STAGING_PREFIX)
        ):
            continue
        if os.path.lexists(target):
            continue  # the app is there: nothing to finish
        helper = helper_of(own)
        answer = runner([str(helper), str(target)])[1] if helper is not None else None
        if answer is not None and answer.get("result") != HELPER_REFUSED:
            done.append(f"finished an interrupted swap of {target}: {answer.get('result')} ({answer.get('reason')})")
            continue
        # The new bundle's helper cannot finish (it refuses: its signature fails, say, after
        # its swap was stopped mid-undo) or is gone: the old app moved aside puts itself back
        # with its own helper (`restored`), when the journal names it and it has one.
        aside = Path(os.path.realpath(data["aside"])) if isinstance(data.get("aside"), str) else None
        old_helper = (
            helper_of(aside)
            if aside is not None and str(aside.parent) == real and aside.name == own.name + ".previous"
            else None
        )
        if old_helper is None:
            why = f"refused ({answer.get('reason')})" if answer is not None else "has no update helper"
            done.append(f"{target} is missing, the new release's helper {why}, and the old app cannot put itself "
                        "back; reinstall Probe")
            continue
        _, restored = runner([str(old_helper), str(target)])
        done.append(f"put the old app back at {target}: {restored.get('result')} ({restored.get('reason')})")
    for line in done:
        log(line)
    return done


def sweep(app: Path, home: Path, *, runner=run_helper, lister=processes, keep_old: bool = False) -> list[str]:
    """What earlier installs left beside `app`: an OLD bundle (older than the
    app, left by a swap), the same version failing its signature check (the
    app a repair replaced) and what a stopped `--remove` left (`<name>.deleting`)
    are deleted by the installed app's own helper (`--remove`), never by this
    Python; a download or a staged copy that was never swapped in (newer than
    the app, or the same version that the helper refuses) is ours and deleted
    here. Anything a process runs from, or that cannot be read, is left.
    `keep_old`: the installed app may not verify (an install's undo failed):
    older bundles stay, the last verified copy among them, until it is repaired."""
    found = leftovers(app)
    if not found:
        return []
    try:
        installed = bundle_info(app).get("CFBundleShortVersionString")
    except InstallError:
        return []
    removed = []
    helper = None
    for path in found:
        if not _real_dir(path):
            if path.name.endswith(".tar.gz") and _remove(path):
                removed.append(path.name)
            continue
        if path.name.endswith(HELPER_DELETING_SUFFIX):
            helper = helper or helper_of(app)
            if helper is not None and not running_from(path, lister=lister):
                _, answer = runner([str(helper), "--remove", str(path)])
                if answer.get("result") == HELPER_REMOVED:
                    removed.append(path.name)
            continue
        try:
            version = bundle_info(path).get("CFBundleShortVersionString")
        except InstallError:
            continue
        if not isinstance(version, str) or not isinstance(installed, str) or running_from(path, lister=lister):
            continue
        if newer(installed, version):
            helper = helper or helper_of(app)
            if helper is None or keep_old:
                continue
            _, answer = runner([str(helper), "--remove", str(path)])
            if answer.get("result") == HELPER_REMOVED:
                removed.append(path.name)
            continue
        if same_version(version, installed):
            # The same version: the app a repair replaced (failing its signature check: the
            # installed app's helper removes it), or a staged copy that was never the app
            # (which that helper refuses: ours, deleted here).
            helper = helper or helper_of(app)
            if helper is not None:
                _, answer = runner([str(helper), "--remove", str(path)])
                if answer.get("result") == HELPER_REMOVED:
                    removed.append(path.name)
                    continue
                if answer.get("result") != HELPER_REFUSED:
                    continue
        if _remove(path):
            removed.append(path.name)
    return removed


# -- the install -------------------------------------------------------------------


def _writable(path: Path) -> bool:
    return os.access(path, os.W_OK, effective_ids=os.access in os.supports_effective_ids)


def check_links(root: Path) -> None:
    """Every link in the unpacked bundle resolves inside it, through any chain
    of links (each was checked on its own while unpacking)."""
    top = os.path.realpath(root)
    for folder, dirs, files in os.walk(root):
        for name in dirs + files:
            path = os.path.join(folder, name)
            if os.path.islink(path):
                real = os.path.realpath(path)
                if real != top and not real.startswith(top + os.sep):
                    raise InstallError(f"the link {os.path.relpath(path, root)!r} resolves outside the bundle")


def _holds_version(bundle: Path, version: str) -> bool:
    """Is `bundle` a real folder whose Info.plist names `version`?"""
    if not _real_dir(bundle):
        return False
    try:
        found = bundle_info(bundle).get("CFBundleShortVersionString")
    except InstallError:
        return False
    return isinstance(found, str) and same_version(found, version)


def install_closed(
    app: Path,
    *,
    home: Path,
    endpoints=ENDPOINTS,
    pubkey: str = PUBKEY,
    fetcher=fetch,
    lister=processes,
    runner=run_helper,
    machine_arch: str | None = None,
    time_limit_s: float = TIME_LIMIT_S,
    skip_version: str | None = None,
    refused_version: str | None = None,
    repair: bool = False,
    log=lambda message: None,
) -> dict:
    """Install the newest release over the closed app at `app`.

    `{outcome, version_before, version_after, latest, error, detail, helper}`
    (`Outcome`; `helper`: the helper's `result`, `reason` and `undo_failed`).
    `skip_version`: a release found earlier to have no update helper;
    `refused_version`: one whose helper refused it for a reason that does not
    change (PERMANENT_REFUSALS). Neither is downloaded again. `repair`: an
    earlier install's undo failed and left an app that may not verify; the app
    is never `current` while it fails `codesign_verify`, and the latest release
    of the same version is installed over it (the helper takes the same version
    over an app that fails its signature check). Never raises;
    never prompts; never starts the app; never renames, swaps or deletes the
    app's bundle (the release's own helper does)."""
    out: dict = {"outcome": Outcome.FAILED, "version_before": None, "version_after": None, "error": None}
    staged: Path | None = None
    archive: Path | None = None
    try:
        info = bundle_info(app)
        if info.get("CFBundleIdentifier") != BUNDLE_ID:
            raise InstallError(f"{app} is not the Probe app")
        before = info.get("CFBundleShortVersionString")
        if parse_version(before) is None:
            raise InstallError(f"the installed app's version {before!r} is not a version")
        out["version_before"] = out["version_after"] = before
        if os.path.islink(app):
            raise Skip(Outcome.NOT_WRITABLE, f"{app} is a link; the app's own updater installs it")
        for path in (app, app.parent):
            if not _writable(path):
                raise Skip(Outcome.NOT_WRITABLE, f"{path} is not writable by this user")
        removed = sweep(app, home, runner=runner, lister=lister, keep_old=repair)
        if removed:
            log(f"removed {', '.join(removed)} left by an earlier install")
        if running_from(app, lister=lister) or lock_held(home):
            raise Skip(Outcome.APP_RUNNING, "the app is running; it installs its own update")
        deadline = _Deadline(time_limit_s)
        version, entry = check(endpoints, deadline=deadline, fetcher=fetcher, machine_arch=machine_arch)
        if version is None or not newer(version, before):
            broken = app_broken(app) if repair else None
            if broken is None:
                out["outcome"] = Outcome.CURRENT
                out["latest"] = version
                log(f"the installed app ({before}) is the newest" + (f" (latest {version})" if version else ""))
                return out
            out["latest"] = version
            if version is None or not same_version(version, before):
                raise InstallError(f"{broken}; no release can repair it: reinstall Probe")
            out["repair"] = True
            log(f"{broken}: installing {version} over it")
        out["latest"] = version
        if skip_version is not None and same_version(version, skip_version):
            raise Skip(Outcome.NO_HELPER, f"{version} has no update helper; the app updates itself at its launch")
        if refused_version is not None and same_version(version, refused_version):
            raise Skip(Outcome.REFUSED_RELEASE,
                       f"{version}'s update helper refused it earlier; the app updates itself at its launch")
        if entry is None:
            raise InstallError(f"the {version} manifest has no entry for {', '.join(targets(machine_arch))}")
        if supported() and not _disclaim_available():
            # Run any other way, the helper's change would be judged by this Python
            # (App Management: refused, with a notification). Nothing is downloaded.
            raise InstallError(
                "this macOS cannot start the update helper as its own process; the app updates itself at its launch"
            )
        key = parse_public_key(pubkey)
        signature = parse_signature(entry["signature"])
        token = secrets.token_hex(6)
        staged = app.parent / f"{STAGING_PREFIX}{token}"
        archive = app.parent / f"{STAGING_PREFIX}{token}.tar.gz"
        log(f"downloading {version} for the closed app ({before})")
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        with os.fdopen(os.open(archive, flags, 0o600), "wb") as sink:
            fetcher(entry["url"], accept="application/octet-stream", limit=ARCHIVE_MAX_BYTES, deadline=deadline, sink=sink)
        verify_file(archive, signature, key, version)
        os.mkdir(staged, 0o700)
        if os.stat(staged).st_dev != os.stat(app).st_dev:
            raise InstallError("the staging folder is not on the app's volume")
        extract(archive, staged)
        archive.unlink()
        archive = None
        check_links(staged)
        check_bundle(staged, version)
        signed = codesign_verify(staged)
        helper = helper_of(staged)
        if helper is None:
            raise Skip(Outcome.NO_HELPER, f"{version} has no update helper; the app updates itself at its launch")
        # The installed bundle's root keeps the folder's usual mode.
        os.chmod(staged, 0o755)
        if running_from(app, lister=lister) or lock_held(home):
            raise Skip(Outcome.APP_RUNNING, "the app started during the download; it installs its own update")
        code, answer = runner([str(helper), str(app)])
        result, reason = answer.get("result"), answer.get("reason")
        undo_failed = answer.get("undo_failed") is True
        detail = str(answer.get("detail") or "")
        out["helper"] = {"result": result, "reason": reason, "undo_failed": undo_failed}
        # The staged path is this Python's to delete only while it still holds the NEW
        # release with nothing running from it, and no swap is halfway. After a swap
        # it holds the OLD app (the new app's helper removes it); after a swap the
        # helper could not undo, either one: the sweep looks again later. The helper's
        # `old` names it when it holds the old app (a repair's old app has the same
        # version as the new one).
        old_at = answer.get("old") if isinstance(answer.get("old"), str) else None
        if old_at is not None:
            out["old_app"] = old_at
        if staged is not None and (
            (app.parent / HELPER_JOURNAL_NAME).exists()
            or result == HELPER_SWAPPED
            or (old_at is not None and os.path.realpath(old_at) == os.path.realpath(staged))
            or not _holds_version(staged, version)
            or running_from(staged, lister=lister)
        ):
            staged = None
        try:
            after = bundle_info(app).get("CFBundleShortVersionString")
        except InstallError:
            after = None
        reads_new = isinstance(after, str) and same_version(after, version)
        # Without `swapped`, the version alone says the new release went in only when it
        # differs from the one before (a repair keeps the version).
        moved = reads_new and not same_version(str(before), version)
        if result == HELPER_SWAPPED and not reads_new:
            raise InstallError(f"after the swap {app} reads version {after!r}, not {version}")
        if result != HELPER_SWAPPED and not (moved and reason in INSTALLED_ANYWAY):
            if result == HELPER_APP_RUNNING:
                # Nothing moved, or the helper undid its swap under an old copy that started.
                raise Skip(Outcome.APP_RUNNING, detail or "the app started during the install")
            if result == HELPER_NOT_PERMITTED:
                raise Skip(Outcome.NOT_PERMITTED, detail or "the system refused the update helper's rename")
            message = f"the update helper answered {result} ({reason}{', undo failed' if undo_failed else ''}, " \
                      f"exit {code}): {detail}"
            if isinstance(answer.get("old"), str):
                message += f"; the old app is at {answer['old']}"
            raise InstallError(message)
        # In place: swapped, or an answer that is not `swapped` with the new release
        # already the app (INSTALLED_ANYWAY: the answer lost, or an old copy started).
        out.update(outcome=Outcome.INSTALLED, version_after=after, codesign=signed)
        out["old_bundle"] = "kept until no Probe process runs from it"
        old, new_helper = answer.get("old"), helper_of(app)
        if result == HELPER_SWAPPED and isinstance(old, str) and new_helper is not None:
            # Only after a swap the helper verified: otherwise the old app may be the last
            # verified copy, and the sweep looks at it later.
            _, removal = runner([str(new_helper), "--remove", old])
            if removal.get("result") == HELPER_REMOVED:
                out["old_bundle"] = "removed"
        if result == HELPER_SWAPPED:
            log(f"installed {after} over the closed app ({before}) with its update helper")
        else:
            log(f"the update helper answered {result} ({reason}), and {after} is the app now: installed")
        return out
    except Skip as skip:
        out.update(outcome=skip.outcome, detail=str(skip))
        log(f"app install skipped ({skip.outcome}): {skip}")
        return out
    except InstallError as exc:
        out.update(outcome=Outcome.FAILED, error=str(exc)[:500])
        log(f"app install failed: {exc}")
        return out
    except Exception as exc:  # noqa: BLE001 -- a bug costs this install, never the cycle
        out.update(outcome=Outcome.FAILED, error=f"{type(exc).__name__}: {exc}"[:500])
        log(f"app install failed: {exc!r}")
        return out
    finally:
        for leftover in (archive, staged):
            if leftover is not None:
                _remove(leftover)
