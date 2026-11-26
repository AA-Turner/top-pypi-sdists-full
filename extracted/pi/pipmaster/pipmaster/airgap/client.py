"""Offline side: dial the relay, show a plan, verify each wheel, install."""

from __future__ import annotations

import datetime
import hashlib
import hmac
import json
import re
import socket
import ssl
import subprocess
import sys
import tempfile
from collections.abc import Callable
from importlib import metadata
from pathlib import Path
from typing import Any

from packaging.requirements import InvalidRequirement, Requirement
from packaging.utils import canonicalize_name
from packaging.version import InvalidVersion, Version

from .common import (
    CHUNK,
    DEFAULT_PORT,
    AirgapError,
    AuthError,
    ProtocolError,
    client_auth,
    collect_profile,
    config_dir,
    parse_token,
    recv_frame,
    send_frame,
)

_WHEEL_RE = re.compile(r"^[A-Za-z0-9_.+!-]+\.whl$")
MAX_WHEEL = 8 << 30


# ------------------------------------------------------------------------ pairing
def _peer_file() -> Path:
    return config_dir() / "peer.json"


def save_peer(token: str) -> dict[str, Any]:
    from .common import b64e, write_private

    peer = parse_token(token)
    write_private(
        _peer_file(),
        json.dumps(
            {
                "fp": peer["fp"],
                "key": b64e(peer["key"]),
                "host": peer["host"],
                "port": peer["port"],
            }
        ).encode(),
    )
    return peer


def load_peer() -> dict[str, Any]:
    from .common import b64d

    try:
        data: dict[str, Any] = json.loads(_peer_file().read_text("utf-8"))
        data["key"] = b64d(data["key"])
        return data
    except (OSError, ValueError, KeyError) as exc:
        raise AirgapError(
            "not paired yet: run 'pipmaster-pair accept <token>'"
        ) from exc


# -------------------------------------------------------------------- requirements
def _add_spec(
    line: str, env: dict[str, str], out: list[str], warn: Callable[[str], None]
) -> None:
    try:
        req = Requirement(line)
    except InvalidRequirement:
        warn("skipped (not a plain requirement): " + line)
        return
    if req.url:
        warn("skipped (direct reference cannot cross the link): " + line)
        return
    if req.marker is not None:
        if not req.marker.evaluate({**env, "extra": ""}):
            return
        req.marker = None
    if str(req) not in out:
        out.append(str(req))


def _read_req_file(
    path: Path,
    env: dict[str, str],
    out: list[str],
    seen: set,
    warn: Callable[[str], None],
) -> None:
    path = path.resolve()
    if path in seen:
        return
    seen.add(path)
    lines, buf = [], ""
    for line in path.read_text("utf-8-sig").splitlines():
        if line.rstrip().endswith("\\"):
            buf += line.rstrip()[:-1] + " "
            continue
        lines.append(buf + line)
        buf = ""
    if buf:
        lines.append(buf)
    for line in lines:
        line = re.sub(r"(^|\s)#.*$", "", line).strip()
        if not line:
            continue
        include = re.match(r"^(?:-r|--requirement)[=\s]*(.+)$", line)
        if include:
            _read_req_file(path.parent / include.group(1).strip(), env, out, seen, warn)
        elif line.startswith("-"):
            warn("skipped option: " + line)
        else:
            _add_spec(re.split(r"\s+--", line)[0], env, out, warn)


def _pyproject_deps(path: Path) -> list[str]:
    try:
        import tomllib  # type: ignore[import-not-found]
    except ImportError:
        try:
            import tomli as tomllib  # type: ignore[no-redef]
        except ImportError as exc:
            raise AirgapError(
                "reading pyproject.toml needs Python 3.11+ or 'tomli'"
            ) from exc
    data = tomllib.loads(path.read_text("utf-8"))
    return [str(d) for d in data.get("project", {}).get("dependencies", [])]


def installed_versions() -> dict[str, str]:
    out: dict[str, str] = {}
    for dist in metadata.distributions():
        name = dist.metadata["Name"]
        if name:
            out[str(canonicalize_name(name))] = dist.version
    return out


def collect_requirements(
    paths: list[str],
    packages: list[str],
    env: dict[str, str],
    upgrade_installed: bool,
    warn: Callable[[str], None],
) -> list[str]:
    out: list[str] = []
    seen: set = set()
    for raw in paths:
        path = Path(raw).expanduser()
        if path.is_dir():
            found = False
            if (path / "requirements.txt").exists():
                _read_req_file(path / "requirements.txt", env, out, seen, warn)
                found = True
            if (path / "pyproject.toml").exists():
                for dep in _pyproject_deps(path / "pyproject.toml"):
                    _add_spec(dep, env, out, warn)
                found = True
            if not found:
                warn("no requirements.txt or pyproject.toml in " + str(path))
        elif path.suffix == ".toml":
            for dep in _pyproject_deps(path):
                _add_spec(dep, env, out, warn)
        elif path.is_file():
            _read_req_file(path, env, out, seen, warn)
        else:
            raise AirgapError("no such path: " + raw)
    for spec in packages:
        _add_spec(spec, env, out, warn)
    if upgrade_installed:
        for name in installed_versions():
            _add_spec(name, env, out, warn)
    return out


# --------------------------------------------------------------------------- link
class RelayClient:
    def __init__(self, peer: dict[str, Any], address: str | None = None) -> None:
        host, port = peer.get("host"), peer.get("port")
        if address:
            host, _, text = address.rpartition(":")
            if not host:
                host, text = address, str(port)
            port = int(text)
        if not host:
            raise AirgapError("no relay address: pass --relay HOST[:PORT]")
        self.peer, self.host, self.port = peer, host, int(port or DEFAULT_PORT)
        self.sock: Any = None

    def __enter__(self) -> RelayClient:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        ctx.check_hostname = False
        # identity is enforced by the pinned fingerprint checked below
        ctx.verify_mode = ssl.CERT_NONE
        raw = socket.create_connection((self.host, self.port), timeout=30)
        self.sock = ctx.wrap_socket(raw)
        der = self.sock.getpeercert(binary_form=True) or b""
        if not hmac.compare_digest(hashlib.sha256(der).hexdigest(), self.peer["fp"]):
            self.sock.close()
            raise AuthError("relay certificate does not match the paired fingerprint")
        self.sock.settimeout(3600)  # resolving can take a while on the relay
        client_auth(self.sock, self.peer["key"])
        return self

    def __exit__(self, *exc: Any) -> None:
        try:
            send_frame(self.sock, {"op": "bye"})
        except (OSError, AirgapError):
            pass
        self.sock.close()

    def resolve(
        self, requirements: list[str], profile: dict[str, Any]
    ) -> dict[str, Any]:
        send_frame(
            self.sock,
            {"op": "resolve", "requirements": requirements, "profile": profile},
        )
        reply = recv_frame(self.sock)
        if not reply.get("ok"):
            raise AirgapError("relay could not resolve: " + str(reply.get("error")))
        for entry in reply["files"]:
            if not _WHEEL_RE.match(entry["filename"]) or not re.fullmatch(
                r"[0-9a-f]{64}", entry["sha256"]
            ):
                raise ProtocolError("relay sent an unsafe manifest entry")
        return reply

    def fetch(self, entry: dict[str, Any], dest: Path) -> Path:
        send_frame(self.sock, {"op": "fetch", "filename": entry["filename"]})
        head = recv_frame(self.sock)
        size = int(head.get("size", -1))
        if not head.get("ok") or size != entry["size"] or not 0 < size <= MAX_WHEEL:
            raise ProtocolError("relay refused or mis-sized " + entry["filename"])
        target, digest, left = Path(dest / entry["filename"]), hashlib.sha256(), size
        with open(target, "wb") as fh:
            while left:
                chunk = self.sock.recv(min(CHUNK, left))
                if not chunk:
                    raise ProtocolError("connection closed mid-file")
                digest.update(chunk)
                fh.write(chunk)
                left -= len(chunk)
        if digest.hexdigest() != entry["sha256"]:
            target.unlink()
            raise AuthError("hash mismatch on " + entry["filename"])
        return target


# ---------------------------------------------------------------------------- plan
def _classify(entry: dict[str, Any], installed: dict[str, str]) -> str:
    current = installed.get(entry["name"])
    if current is None:
        return "new"
    try:
        a, b = Version(current), Version(entry["version"])
    except InvalidVersion:
        return "same" if current == entry["version"] else "upgrade"
    return "same" if a == b else ("upgrade" if b > a else "downgrade")


def build_plan(
    manifest: dict[str, Any], installed: dict[str, str]
) -> list[dict[str, Any]]:
    return [
        {**e, "kind": _classify(e, installed), "current": installed.get(e["name"])}
        for e in manifest["files"]
    ]


def load_policy() -> dict[str, Any]:
    path = config_dir() / "policy.json"
    try:
        policy: dict[str, Any] = json.loads(path.read_text("utf-8"))
        return policy
    except (OSError, ValueError):
        return {}


def check_policy(plan: list[dict[str, Any]], policy: dict[str, Any]) -> list[str]:
    problems = []
    deny = {canonicalize_name(n) for n in policy.get("deny", [])}
    for item in plan:
        if item["kind"] != "same" and item["name"] in deny:
            problems.append("denied by policy: " + item["name"])
    limit = policy.get("max_new_packages")
    new = sum(1 for i in plan if i["kind"] == "new")
    if isinstance(limit, int) and new > limit:
        problems.append(f"{new} new packages exceed policy limit {limit}")
    return problems


def render_plan(plan: list[dict[str, Any]], manifest: dict[str, Any]) -> str:
    marks = {"new": "+", "upgrade": "^", "downgrade": "v", "same": "="}
    rows = []
    for i in sorted(plan, key=lambda x: (x["kind"] == "same", x["name"])):
        if i["current"] is None or i["kind"] == "same":
            change = i["version"]
        else:
            change = f"{i['current']} -> {i['version']}"
        rows.append(f"  {marks[i['kind']]} {i['name']:<32} {change}")
    for held in manifest.get("held_back", []):
        rows.append(
            "  ! {} {} held back (released {} days ago)".format(
                held["name"], held["version"], held["age_days"]
            )
        )
    audit = manifest.get("audit")
    if audit and audit.get("ran"):
        rows.append(
            "  audit: "
            + (
                "VULNERABILITIES FOUND\n" + audit["output"]
                if audit["vulnerable"]
                else "no known vulnerabilities"
            )
        )
    return "\n".join(rows)


# -------------------------------------------------------------------------- install
def snapshot() -> Path:
    folder = config_dir() / "snapshots"
    folder.mkdir(exist_ok=True)
    path = folder / (
        "freeze-{}.txt".format(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    )
    out = subprocess.run(
        [sys.executable, "-m", "pip", "freeze", "--disable-pip-version-check"],
        capture_output=True,
        text=True,
    )
    path.write_text(out.stdout, "utf-8")
    return path


def install_wheels(
    plan: list[dict[str, Any]], client: RelayClient, log: Callable[[str], None]
) -> int:
    todo = [i for i in plan if i["kind"] != "same"]
    if not todo:
        log("nothing to install: everything is already at the resolved versions")
        return 0
    with tempfile.TemporaryDirectory(prefix="pipmaster-stage-") as tmp:
        stage = Path(tmp)
        for n, item in enumerate(todo, 1):
            log(f"[{n}/{len(todo)}] fetching {item['filename']}")
            client.fetch(item, stage)
        lock = stage / "lock.txt"
        lock.write_text(
            "".join(
                "{}=={} --hash=sha256:{}\n".format(i["name"], i["version"], i["sha256"])
                for i in todo
            ),
            "utf-8",
        )
        cmd = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "--no-input",
            "--no-index",
            "--find-links",
            str(stage),
            "--require-hashes",
            "--no-deps",
            "-r",
            str(lock),
        ]
        code = subprocess.run(cmd).returncode
    if code == 0:
        subprocess.run(
            [sys.executable, "-m", "pip", "check", "--disable-pip-version-check"]
        )
    return code


def run_install(
    paths: list[str],
    packages: list[str],
    relay: str | None,
    upgrade_installed: bool,
    dry_run: bool,
    assume_yes: bool,
    log: Callable[[str], None] = print,
) -> int:
    profile = collect_profile()
    specs = collect_requirements(
        paths,
        packages,
        profile["env"],
        upgrade_installed,
        lambda m: log("warning: " + m),
    )
    if not specs:
        raise AirgapError("no requirements to resolve")
    log(
        f"{len(specs)} requirement(s) for {profile['os']} {profile['machine']}, "
        f"Python {profile['python'][0]}.{profile['python'][1]}"
    )
    with RelayClient(load_peer(), relay) as client:
        manifest = client.resolve(specs, profile)
        plan = build_plan(manifest, installed_versions())
        log("plan:\n" + render_plan(plan, manifest))
        problems = check_policy(plan, load_policy())
        if problems:
            raise AirgapError("; ".join(problems))
        if dry_run:
            return 0
        if not any(i["kind"] != "same" for i in plan):
            log("already up to date")
            return 0
        if not assume_yes and input("apply this plan? [y/N] ").strip().lower() != "y":
            log("aborted")
            return 1
        log("rollback snapshot: " + str(snapshot()))
        return install_wheels(plan, client, log)