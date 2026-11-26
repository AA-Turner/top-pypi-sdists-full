"""Online side: resolves and serves wheels for a paired, offline client."""

from __future__ import annotations

import datetime
import hashlib
import ipaddress
import json
import secrets
import shutil
import socket
import ssl
import subprocess
import sys
import tempfile
import time
import zipfile
from collections.abc import Callable
from email.parser import Parser
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

from packaging.requirements import InvalidRequirement, Requirement
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.utils import canonicalize_name, parse_wheel_filename
from packaging.version import InvalidVersion, Version

from .common import (
    CHUNK,
    DEFAULT_PORT,
    AirgapError,
    ProtocolError,
    b64d,
    b64e,
    config_dir,
    make_token,
    recv_frame,
    send_frame,
    server_auth,
    validate_profile,
    write_private,
)

MAX_SPECS = 500
MAX_OPS = 200
MAX_AGE_ROUNDS = 6
MAX_CLOSURE_PASSES = 6


class ResolveError(AirgapError):
    """The requested set could not be resolved for the target."""


# ------------------------------------------------------------------------ identity
def _relay_dir() -> Path:
    path = config_dir() / "relay"
    path.mkdir(exist_ok=True)
    return path


def create_identity(
    host: str | None = None, port: int = DEFAULT_PORT, force: bool = False
) -> str:
    """Create the relay's pinned certificate and secret; return the pairing token."""
    try:
        from cryptography import x509
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.x509.oid import NameOID
    except ImportError as exc:
        raise AirgapError(
            "the relay needs 'cryptography': pip install pipmaster[airgap]"
        ) from exc
    folder = _relay_dir()
    meta = folder / "relay.json"
    if meta.exists() and not force:
        raise AirgapError("a relay identity already exists (use --force to rotate it)")
    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "pipmaster-relay")])
    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(days=1))
        .not_valid_after(now + datetime.timedelta(days=3650))
        .sign(key, hashes.SHA256())
    )
    fingerprint = hashlib.sha256(
        cert.public_bytes(serialization.Encoding.DER)
    ).hexdigest()
    secret = secrets.token_bytes(32)
    write_private(
        folder / "key.pem",
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        ),
    )
    (folder / "cert.pem").write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    write_private(
        meta,
        json.dumps(
            {"fp": fingerprint, "key": b64e(secret), "host": host, "port": port}
        ).encode("utf-8"),
    )
    return make_token(fingerprint, secret, host, port)


def load_identity() -> dict[str, Any]:
    folder = _relay_dir()
    try:
        data = json.loads((folder / "relay.json").read_text("utf-8"))
        return {
            "cert": folder / "cert.pem",
            "key_file": folder / "key.pem",
            "fp": data["fp"],
            "secret": b64d(data["key"]),
            "host": data.get("host"),
            "port": data.get("port") or DEFAULT_PORT,
        }
    except (OSError, ValueError, KeyError) as exc:
        raise AirgapError("no relay identity yet: run 'pipmaster-pair create'") from exc


def current_token() -> str:
    ident = load_identity()
    return make_token(ident["fp"], ident["secret"], ident["host"], ident["port"])


# ------------------------------------------------------------------------- resolver
def _tail(text: str, size: int = 2500) -> str:
    return text if len(text) <= size else "..." + text[-size:]


class Resolver:
    """Turns requirement strings plus a target profile into a vetted wheelhouse."""

    def __init__(
        self,
        index_url: str | None = None,
        min_age_days: float = 7,
        audit: bool = False,
        log: Callable[[str], None] = print,
    ) -> None:
        if index_url and min_age_days > 0:
            raise AirgapError(
                "--min-age-days needs pypi.org metadata; use 0 with --index-url"
            )
        self.index_url = index_url
        self.min_age_days = min_age_days
        self.audit = audit
        self.log = log
        self._ages: dict[str, float | None] = {}

    # -- public ---------------------------------------------------------------
    def resolve(
        self, request: dict[str, Any], workdir: Path
    ) -> tuple[dict[str, Any], dict[str, Path]]:
        profile = validate_profile(request.get("profile"))
        specs = self._validate_specs(request.get("requirements"))
        limits: dict[str, str] = {}
        held: list[dict[str, Any]] = []
        wheels: dict[str, tuple[str, Path]] = {}
        for attempt in range(MAX_AGE_ROUNDS):
            dest = workdir / f"wheels{attempt}"
            shutil.rmtree(dest, ignore_errors=True)
            dest.mkdir(parents=True)
            constraints = [f"{n}{c}" for n, c in sorted(limits.items())]
            wheels = self._download_closure(specs, dest, profile, constraints, workdir)
            young = self._too_young(wheels)
            if not young:
                break
            for name, version, age in young:
                newest_old = self._newest_old_version(name)
                limits[name] = f"<={newest_old}" if newest_old else f"<{version}"
                held.append({"name": name, "version": version, "age_days": age})
        else:
            names = ", ".join(f"{h['name']}=={h['version']}" for h in held[-5:])
            raise ResolveError(
                "quarantine could not be satisfied (age unknown or too new): " + names
            )
        files, staged = [], {}
        for name, (version, path) in sorted(wheels.items()):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            files.append(
                {
                    "filename": path.name,
                    "name": name,
                    "version": version,
                    "size": path.stat().st_size,
                    "sha256": digest,
                    "age_days": self._ages.get(path.name),
                }
            )
            staged[path.name] = path
        manifest = {
            "ok": True,
            "files": files,
            "held_back": held,
            "audit": self._run_audit(files, workdir) if self.audit else None,
        }
        return manifest, staged

    # -- request hygiene --------------------------------------------------------
    @staticmethod
    def _validate_specs(raw: Any) -> list[Requirement]:
        if not isinstance(raw, list) or not 1 <= len(raw) <= MAX_SPECS:
            raise ProtocolError(
                f"requirements must be a list of 1..{MAX_SPECS} strings"
            )
        specs = []
        for item in raw:
            try:
                req = Requirement(str(item))
            except InvalidRequirement as exc:
                raise ProtocolError(f"invalid requirement: {str(item)[:80]!r}") from exc
            if req.url:
                raise ProtocolError(f"direct references are not served: {req.name}")
            # the client already evaluated markers for ITS environment
            req.marker = None
            specs.append(req)
        return specs

    # -- download + marker closure --------------------------------------------
    def _pip_download(
        self,
        lines: list[str],
        dest: Path,
        profile: dict[str, Any],
        constraints: list[str],
        workdir: Path,
    ) -> None:
        req_file = workdir / "req.txt"
        req_file.write_text("\n".join(lines) + "\n", "utf-8")
        major, minor = profile["python"]
        cmd = [
            sys.executable,
            "-m",
            "pip",
            "download",
            "--disable-pip-version-check",
            "--no-input",
            "--only-binary=:all:",
            "--dest",
            str(dest),
            "-r",
            str(req_file),
            "--python-version",
            f"{major}{minor}",
            "--implementation",
            profile["implementation"],
        ]
        for plat in profile["platforms"]:
            cmd += ["--platform", plat]
        for abi in profile["abis"]:
            cmd += ["--abi", abi]
        if constraints:
            cfile = workdir / "constraints.txt"
            cfile.write_text("\n".join(constraints) + "\n", "utf-8")
            cmd += ["-c", str(cfile)]
        if self.index_url:
            cmd += ["--index-url", self.index_url]
        self.log(f"pip download: {len(lines)} requirement(s)")
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        if proc.returncode != 0:
            raise ResolveError(_tail((proc.stderr or proc.stdout).strip()))

    @staticmethod
    def _scan(dest: Path) -> dict[str, tuple[str, Path]]:
        found: dict[str, tuple[str, Path]] = {}
        for path in sorted(dest.glob("*.whl")):
            name, version, _build, _tags = parse_wheel_filename(path.name)
            key = canonicalize_name(name)
            if key in found:
                raise ResolveError(f"two versions of {key} were resolved")
            found[key] = (str(version), path)
        return found

    @staticmethod
    def _wheel_requires(path: Path) -> list[Requirement]:
        with zipfile.ZipFile(path) as zf:
            member = next(
                (
                    n
                    for n in zf.namelist()
                    if n.endswith(".dist-info/METADATA") and n.count("/") == 1
                ),
                None,
            )
            if member is None:
                return []
            with zf.open(member) as fh:
                text = fh.read(1 << 20).decode("utf-8", "replace")
        out = []
        for line in Parser().parsestr(text).get_all("Requires-Dist") or []:
            try:
                out.append(Requirement(line))
            except InvalidRequirement:
                continue
        return out

    def _missing(
        self,
        specs: list[Requirement],
        wheels: dict[str, tuple[str, Path]],
        env: dict[str, str],
    ) -> list[str]:
        """pip evaluates markers for the HOST; redo the walk for the TARGET."""
        extras: dict[str, set[str]] = {}
        wanted: dict[str, list[str]] = {}
        for spec in specs:
            key = str(canonicalize_name(spec.name))
            extras.setdefault(key, set()).update(
                canonicalize_name(e) for e in spec.extras
            )
            wanted.setdefault(key, []).append(str(spec.specifier))
        done: dict[str, frozenset] = {}
        changed = True
        while changed:
            changed = False
            for key in list(extras):
                state = frozenset(extras[key])
                if key not in wheels or done.get(key) == state:
                    continue
                done[key] = state
                changed = True
                for dep in self._wheel_requires(wheels[key][1]):
                    if dep.marker is not None and not any(
                        dep.marker.evaluate({**env, "extra": e})
                        for e in (state or {""})
                    ):
                        continue
                    dkey = canonicalize_name(dep.name)
                    extras.setdefault(dkey, set()).update(
                        canonicalize_name(e) for e in dep.extras
                    )
                    wanted.setdefault(dkey, []).append(str(dep.specifier))
        missing = []
        for name, found in extras.items():
            joined = ",".join(s for s in wanted[name] if s)
            have = wheels.get(name)
            ok = have is not None
            if have is not None and joined:
                try:
                    ok = SpecifierSet(joined).contains(
                        Version(have[0]), prereleases=True
                    )
                except (InvalidSpecifier, InvalidVersion):
                    ok = True
            if not ok:
                tag = "[{}]".format(",".join(sorted(found))) if found else ""
                missing.append(f"{name}{tag}{joined}")
        return missing

    def _download_closure(
        self,
        specs: list[Requirement],
        dest: Path,
        profile: dict[str, Any],
        constraints: list[str],
        workdir: Path,
    ) -> dict[str, tuple[str, Path]]:
        self._pip_download([str(s) for s in specs], dest, profile, constraints, workdir)
        for _ in range(MAX_CLOSURE_PASSES):
            wheels = self._scan(dest)
            missing = self._missing(specs, wheels, profile["env"])
            if not missing:
                return wheels
            names = {canonicalize_name(Requirement(m).name) for m in missing}
            for name in names & set(wheels):
                wheels[name][1].unlink()  # stale version, replaced below
            pins = [f"{k}=={v[0]}" for k, v in wheels.items() if k not in names]
            self._pip_download(missing, dest, profile, constraints + pins, workdir)
        raise ResolveError("dependency closure for the target did not converge")

    # -- quarantine -------------------------------------------------------------
    def _age_days(self, name: str, version: str, filename: str) -> float | None:
        if filename in self._ages:
            return self._ages[filename]
        age: float | None = None
        try:
            req = Request(
                f"https://pypi.org/pypi/{name}/{version}/json",
                headers={"User-Agent": "pipmaster-airgap-relay"},
            )
            with urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            for entry in data.get("urls", []):
                if entry.get("filename") == filename:
                    stamp = entry["upload_time_iso_8601"].replace("Z", "+00:00")
                    uploaded = datetime.datetime.fromisoformat(stamp)
                    age = (
                        datetime.datetime.now(datetime.timezone.utc) - uploaded
                    ).total_seconds() / 86400
        except (OSError, ValueError, KeyError):
            age = None
        self._ages[filename] = age
        return age

    def _newest_old_version(self, name: str) -> str | None:
        """Newest stable release old enough to leave the quarantine window."""
        try:
            req = Request(
                f"https://pypi.org/pypi/{name}/json",
                headers={"User-Agent": "pipmaster-airgap-relay"},
            )
            with urlopen(req, timeout=30) as resp:
                releases = json.loads(resp.read().decode("utf-8")).get("releases") or {}
        except (OSError, ValueError):
            return None
        now = datetime.datetime.now(datetime.timezone.utc)
        best: Version | None = None
        for text, files in releases.items():
            try:
                version = Version(text)
                stamps = [
                    datetime.datetime.fromisoformat(
                        f["upload_time_iso_8601"].replace("Z", "+00:00")
                    )
                    for f in files
                    if not f.get("yanked")
                ]
            except (InvalidVersion, KeyError, ValueError):
                continue
            if version.is_prerelease or not stamps:
                continue
            if (now - min(stamps)).total_seconds() / 86400 >= self.min_age_days and (
                best is None or version > best
            ):
                best = version
        return str(best) if best else None

    def _too_young(
        self, wheels: dict[str, tuple[str, Path]]
    ) -> list[tuple[str, str, float | None]]:
        if self.min_age_days <= 0:
            return []
        young = []
        for name, (version, path) in wheels.items():
            age = self._age_days(name, version, path.name)
            if age is None or age < self.min_age_days:
                young.append((name, version, None if age is None else round(age, 1)))
        return young

    # -- audit --------------------------------------------------------------------
    def _run_audit(self, files: list[dict[str, Any]], workdir: Path) -> dict[str, Any]:
        exe = shutil.which("pip-audit")
        if not exe:
            return {"ran": False, "output": "pip-audit not installed on the relay"}
        lock = workdir / "audit.txt"
        lock.write_text(
            "".join(
                f"{f['name']}=={f['version']} --hash=sha256:{f['sha256']}\n"
                for f in files
            ),
            "utf-8",
        )
        proc = subprocess.run(
            [
                exe,
                "-r",
                str(lock),
                "--no-deps",
                "--disable-pip",
                "--progress-spinner",
                "off",
            ],
            capture_output=True,
            text=True,
            timeout=900,
        )
        return {
            "ran": True,
            "vulnerable": proc.returncode == 1,
            "output": _tail(
                "\n".join(
                    ln
                    for ln in (proc.stdout + proc.stderr).splitlines()
                    if not ln.startswith("WARNING:")
                ),
                3000,
            ),
        }


# --------------------------------------------------------------------------- server
class Relay:
    """Listens for a limited time, serves one paired client, then closes."""

    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = DEFAULT_PORT,
        duration: float = 900,
        allow_from: list[str] | None = None,
        resolver: Resolver | None = None,
        keep_open: bool = False,
        log: Callable[[str], None] = print,
    ) -> None:
        self.host, self.port, self.duration = host, port, duration
        self.networks = [
            ipaddress.ip_network(a, strict=False) for a in (allow_from or [])
        ]
        self.resolver = resolver or Resolver(log=log)
        self.keep_open = keep_open
        self.log = log
        self.identity = load_identity()

    def _peer_allowed(self, address: str) -> bool:
        if not self.networks:
            return True
        ip = ipaddress.ip_address(address)
        return any(ip in net for net in self.networks)

    def serve(self) -> None:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        ctx.load_cert_chain(str(self.identity["cert"]), str(self.identity["key_file"]))
        deadline = time.monotonic() + self.duration
        failures = 0
        with socket.create_server((self.host, self.port)) as srv:
            srv.settimeout(1.0)
            self.log(
                f"relay open on {self.host}:{self.port} for {self.duration:.0f} s "
                f"(fingerprint {self.identity['fp'][:16]}...)"
            )
            while time.monotonic() < deadline and failures < 5:
                try:
                    conn, addr = srv.accept()
                except socket.timeout:
                    continue
                if not self._peer_allowed(addr[0]):
                    self.log(f"refused {addr[0]} (not in --allow-from)")
                    conn.close()
                    continue
                conn.settimeout(120)
                try:
                    tls = ctx.wrap_socket(conn, server_side=True)
                except (ssl.SSLError, OSError):
                    conn.close()
                    continue
                with tls:
                    try:
                        finished = self._session(tls, addr[0])
                    except (AirgapError, OSError, ssl.SSLError) as exc:
                        self.log(f"session error: {exc}")
                        finished = False
                if finished and not self.keep_open:
                    break
                if not finished:
                    failures += 1
        self.log("relay closed")

    def _session(self, tls: Any, peer: str) -> bool:
        if not server_auth(tls, self.identity["secret"]):
            self.log(f"authentication failed from {peer}")
            return False
        self.log(f"client {peer} authenticated")
        staged: dict[str, Path] = {}
        with tempfile.TemporaryDirectory(prefix="pipmaster-relay-") as tmp:
            for _ in range(MAX_OPS):
                msg = recv_frame(tls)
                op = msg.get("op")
                if op == "resolve":
                    try:
                        manifest, staged = self.resolver.resolve(msg, Path(tmp))
                        send_frame(tls, manifest)
                        self.log(f"served manifest: {len(manifest['files'])} file(s)")
                    except ResolveError as exc:
                        send_frame(tls, {"ok": False, "error": str(exc)})
                elif op == "fetch":
                    path = staged.get(str(msg.get("filename")))
                    if path is None:
                        send_frame(tls, {"ok": False, "error": "unknown file"})
                        continue
                    send_frame(tls, {"ok": True, "size": path.stat().st_size})
                    with open(path, "rb") as fh:
                        while True:
                            chunk = fh.read(CHUNK)
                            if not chunk:
                                break
                            tls.sendall(chunk)
                elif op == "bye":
                    send_frame(tls, {"ok": True})
                    return True
                else:
                    send_frame(tls, {"ok": False, "error": "unknown op"})
        return False