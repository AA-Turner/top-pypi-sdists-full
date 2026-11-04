"""`hugpy-core install | uninstall | status` — the whole hugpy orbit for one account, in one command.

pip only delivers the package; this performs the install, the same way `fitevict install` and
`hugpy-router install` do (and with the wrapper's helpers: plan -> numbered steps -> health).
Run it AS the account (e.g. `sudo -iu hugpy hugpy-core install --user`):

  1. code         this environment (sys.prefix); hugpy-wrapper, hugpy-router and
                  abstract_toolserver come with hugpy-core as dependencies
  2. database     the DATABASE SERVER, via the orbit toolserver's OWN db CLI
                  (`abstract-toolserver db install …`) — core provisions no Postgres itself
                  (the toolserver needs a database regardless and core uses the toolserver):
                    * own mode (DEFAULT, no root): the orbit's own private cluster on 7305,
                      socket-only, unit hugpy-postgres.service, data <data>/pg
                    * existing mode (--db-dsn): a database the account already owns; the orbit
                      toolserver gets its OWN db (--toolserver-db-dsn), core takes a SCHEMA
                    * --create-db: brand-new databases in the system cluster (needs CREATEDB)
  3. core-database the database/schema core + the call-log mirror use: own/create-db ->
                  `abstract-toolserver db ensure-database <db>` (its printed dsn); existing ->
                  CREATE SCHEMA <schema> in --db-dsn + a search_path conninfo
  4. toolserver   the orbit's OWN abstract-toolserver (not the account's per-user node):
                  ~/.config/hugpy/toolserver.env (0600, operator token made once and kept,
                  the db keys from step 2 preserved), its own config root <data>/toolserver,
                  unit hugpy-toolserver.service, health GET /healthz
  5. wrapper      `fitevict install --user --port <wrapper port>`      (its own installer)
  6. router       `hugpy-router install --user --port <router port>`   (its own installer)
  7. core         ~/.config/hugpy/core.env (0600; the resolved DSN for core and the call-log
                  mirror, the router and toolserver URLs + keys), serves the @hugpy/ui build
                  packaged in this wheel, unit hugpy-core.service, health GET /api/auth/config
  8. endpoint     ~/.config/hugpy/core.endpoint.json: the URLs + a db summary, no secret

Ports come from the account's block 7300-7399 (core 7301, wrapper 7302, router 7303,
toolserver 7304, the orbit cluster 7305), each overridable; a re-run keeps ports, tokens,
the schema and the DB. `auto` is not accepted: the orbit's ports are fixed so they can be
written down. Non-interactive by default (flags, so an apt postinst / scripted install runs
unattended); on a TTY with no DB flag, ONE question picks own-cluster (default) or an existing DSN.

core.env and hugpy-core.service are rendered whole on every run: a hand-made copy is taken over
(nothing of it is kept; the toolserver token is the orbit toolserver's own).
"""
from __future__ import annotations


import argparse
import json
import os
import secrets
import shutil
import subprocess
import sys
import time
import urllib.request
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from fitevict.cli import installer as W          # the wrapper's installer: shared helpers
from fitevict.cli.installer import InstallError, Plan, execute, port_free, probe_host, read_env, render_env, \
    write_file

from hugpy_core.imports import constants as _C
from hugpy_core.imports.constant.install import (
    SERVICE, TS_SERVICE, PG_SERVICE, PACKAGE,
    TS_EXE, DEFAULT_DB, DEFAULT_SCHEMA, DEFAULT_HOST,
    DEFAULT_PORTS, CLUSTER_PORT, PEER_HOST, TS_HOST,
    HEALTH_WAIT_S, TS_HEALTH_WAIT_S, MARK, ENV_CORE_URL,
    ENV_CORE_HOST, ENV_CORE_PORT, ENV_CORE_SCHEMA, ENV_CORE_TS_URL,
    ENV_CORE_TS_TOKEN, ENV_CENTRAL_MODELS_HOME, ROUTER_KEY_ENV, ROUTER_PORT_ENV,
    WRAPPER_PORT_ENV, TS_TOKEN_ENV, TS_DB_KEYS,
)


# ── layout ────────────────────────────────────────────────────────────────────
@dataclass
class Layout:
    conf_dir: str                 # ~/.config/hugpy (shared with wrapper.env, router.env)
    data_dir: str                 # the hugpy per-user data dir (app_dirs)
    unit_dir: str                 # ~/.config/systemd/user
    bin_dir: str                  # this environment's bin/

    @property
    def core_env(self) -> str:
        return os.path.join(self.conf_dir, "core.env")

    @property
    def ts_env(self) -> str:
        return os.path.join(self.conf_dir, "toolserver.env")

    @property
    def endpoint_file(self) -> str:
        return os.path.join(self.conf_dir, "core.endpoint.json")

    @property
    def wrapper_env(self) -> str:
        return os.path.join(self.conf_dir, "wrapper.env")

    @property
    def router_env(self) -> str:
        return os.path.join(self.conf_dir, "router.env")

    @property
    def router_endpoint(self) -> str:
        return os.path.join(self.conf_dir, "router.endpoint.json")

    @property
    def ts_home(self) -> str:
        return os.path.join(self.data_dir, "toolserver")

    @property
    def core_home(self) -> str:
        return os.path.join(self.data_dir, "core")

    @property
    def core_unit(self) -> str:
        return os.path.join(self.unit_dir, f"{SERVICE}.service")

    @property
    def ts_unit(self) -> str:
        return os.path.join(self.unit_dir, f"{TS_SERVICE}.service")

    def exe(self, name: str) -> str:
        return os.path.join(self.bin_dir, name)

    systemctl = ["systemctl", "--user"]


def layout() -> Layout:
    from hugpy_resources.imports.functions import application_paths as app_dirs
    cfg = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
    return Layout(app_dirs.resolve_paths()["config"], app_dirs.data_dir(), os.path.join(cfg, "systemd", "user"),
                  os.path.dirname(sys.executable))


def account() -> str:
    import pwd
    return pwd.getpwuid(os.getuid()).pw_name


def ours(path: str) -> bool:
    """Was this file rendered by this installer (vs. by hand)?"""
    try:
        with open(path, encoding="utf-8") as fh:
            return MARK in fh.readline()
    except OSError:
        return False


def render(values: Dict[str, str], title: str) -> str:
    """The wrapper's env rendering (quoting, refusals) under this installer's own header."""
    body = render_env(values).splitlines()[2:]
    return "\n".join([f"# {title} — {MARK}. Owner-only.",
                      "# Re-run `hugpy-core install --user` to apply changes; edits here are overwritten."]
                     + body) + "\n"


def url(host: str, port: int) -> str:
    h = probe_host(host)
    return f"http://[{h}]:{port}" if ":" in h else f"http://{h}:{port}"


def http_ok(u: str, timeout: float = 3) -> bool:
    try:
        with urllib.request.urlopen(u, timeout=timeout) as r:
            return r.status == 200
    except Exception:  # noqa: BLE001
        return False


def resolve_port(name: str, want, current: Optional[str]) -> int:
    raw = str(want or current or DEFAULT_PORTS[name]).strip()
    try:
        port = int(raw)
    except ValueError:
        raise InstallError(f"the {name} port must be a number, not {raw!r} (`auto` is not used for the orbit)") \
            from None
    if not 1024 <= port <= 65535:
        raise InstallError(f"the {name} port {port} is out of range (1024-65535)")
    return port


# ── database (the orbit toolserver's OWN db CLI does the provisioning) ──────────
# hugpy-core provisions NO Postgres itself (operator 2026-10-08): the orbit
# toolserver needs a database regardless and core uses the toolserver, so the
# cluster + databases belong to `abstract-toolserver db` (shipped by the toolserver,
# release 0.0.94). Core only SHELLS OUT to it, wires the DSNs, and — in existing-DSN
# mode — creates its own SCHEMA (the one bit of SQL it keeps; not provisioning).
#
#   db install --name <db> --port 7305 --data-dir <data>/pg --env-file <ts_env>
#              --mode own|existing [--dsn CONNINFO] --json
#       own (default): per-account cluster (box binaries, else pip pgserver), unit
#       hugpy-postgres.service, socket-only on 7305, creates the db, writes the
#       SOLCATCHER_POSTGRESQL_* keys into --env-file. existing: validates --dsn and
#       writes the keys from it. Prints {"mode","socket_dir","port","unit","database","ready"}.
#   db ensure-database <db> --env-file <ts_env> --json   -> {"dsn": "dbname=<db> host=<sock> port=7305"}
#   db status   --env-file <ts_env> --json
#   db uninstall --env-file <ts_env> [--keep-data]
def _db_cli(lay: "Layout", *args: str, want_json: bool = False, check: bool = True):
    """Run `abstract-toolserver db <args>` (the only way core touches Postgres
    provisioning). Returns parsed JSON (want_json) or the CompletedProcess; raises
    InstallError with the CLI's own stderr on failure. The tests fake this seam."""
    cmd = [lay.exe(TS_EXE), "db", *args]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if check and p.returncode:
        raise InstallError(f"`{' '.join(cmd)}` failed ({p.returncode}): "
                           f"{(p.stderr or p.stdout).strip()[-800:]}")
    if want_json:
        try:
            return json.loads(p.stdout or "{}")
        except ValueError:
            raise InstallError(f"`{' '.join(cmd)}` did not print JSON: "
                               f"{(p.stdout or p.stderr).strip()[:400]}") from None
    return p


def create_schema(dsn: str, schema: str, user: str) -> None:
    """CREATE SCHEMA IF NOT EXISTS <schema> AUTHORIZATION <user> on the account's own
    database (existing-DSN mode). The ONLY SQL core runs itself — the cluster and the
    databases belong to the toolserver's db CLI. The account owns the database (peer),
    so it may create a schema in it with no privilege question."""
    import psycopg
    from psycopg import sql
    with psycopg.connect(dsn, autocommit=True, connect_timeout=5) as c:
        c.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {} AUTHORIZATION {}").format(
            sql.Identifier(schema), sql.Identifier(user)))


def with_search_path(conninfo: str, schema: str) -> str:
    """Append ``options=-c search_path=<schema>,public`` to a libpq conninfo so core
    (and the call-log mirror) land in the orbit's schema. Left alone if the operator
    already set options= in their --db-dsn."""
    conninfo = (conninfo or "").strip()
    if "options=" in conninfo:
        return conninfo
    return f"{conninfo} options=-c search_path={schema},public"


def _dsn_dbname(conninfo: str) -> str:
    """The dbname= of a libpq conninfo (best-effort, for messages/summaries)."""
    for tok in (conninfo or "").split():
        if tok.startswith("dbname="):
            return tok[len("dbname="):]
    return ""


# ── env + units ───────────────────────────────────────────────────────────────


def toolserver_values(lay: Layout, port: int, current: Dict[str, str]) -> Dict[str, str]:
    """The toolserver env keys CORE owns — TOOLSERVER_* + its own config root (so its
    identity / advertisement never meet the per-user node's) + the operator token,
    made once and kept across re-runs. The DB keys (SOLCATCHER_POSTGRESQL_*) are
    written by `abstract-toolserver db install` and PRESERVED here, not set by core."""
    token = current.get(TS_TOKEN_ENV) or secrets.token_urlsafe(32)
    vals = {"TOOLSERVER_HOST": TS_HOST, "TOOLSERVER_PORT": str(port), "TOOLSERVER_URL": url(TS_HOST, port),
            TS_TOKEN_ENV: token, "TOOLSERVER_TOKEN": token,
            "ABSTRACT_TOOLSERVER_HOME": lay.ts_home,
            "ABSTRACT_TOOLSERVER_ENDPOINT_FILE": os.path.join(lay.ts_home, "endpoint.json")}
    # keep the DB keys db install wrote into the env, whatever they are
    for k in TS_DB_KEYS:
        if current.get(k) is not None:
            vals[k] = current[k]
    return vals


def core_values(*, core_dsn: str, schema: Optional[str], host: str, port: int, core_url: str,
                router_url: str, router_key: str, ts_url: str, ts_token: str,
                central_models_home: Optional[str] = None) -> Dict[str, str]:
    """core.env: the resolved core DSN (own mode: the cluster's db, from
    `db ensure-database`; existing mode: --db-dsn + search_path) for BOTH core and
    the call-log mirror, the router + toolserver URLs/keys, and — existing mode only —
    the schema (so schema.ensure pins the session to it)."""
    vals = {_C.ENV_CORE_DB: core_dsn, _C.ENV_CALLLOG_DSN: core_dsn,   # intake mirrors the wrapper into the SAME db
            ENV_CORE_HOST: host, ENV_CORE_PORT: str(port), ENV_CORE_URL: core_url,
            _C.ENV_SELF_BASE: router_url,
            ENV_CORE_TS_URL: ts_url, ENV_CORE_TS_TOKEN: ts_token,
            _C.ENV_ROUTER_URL: router_url, _C.ENV_ROUTER_KEY: router_key}
    if schema:
        vals[ENV_CORE_SCHEMA] = schema
    if central_models_home:
        vals[ENV_CENTRAL_MODELS_HOME] = central_models_home
    return vals


def wrapper_args(args) -> list:
    """The `fitevict install` options core passes through: the box's worker name, its own
    model store, its engine, its transformers engine (--wrapper-tf), extra settings. Always
    --yes: core already asked its own questions, and the wrapper's guided prompts must not
    fire inside core's run."""
    out = ["--yes"]
    for flag, val in (("--worker", getattr(args, "worker", None)),
                      ("--models", getattr(args, "models", None)),
                      ("--engine", getattr(args, "engine", None))):
        if val:
            out += [flag, str(val)]
    if getattr(args, "wrapper_tf", False) and not getattr(args, "minimal", False):
        out.append("--tf")
    if getattr(args, "wrapper_tf", False) and not getattr(args, "minimal", False) and getattr(args, "wrapper_tf_find_links", None):
        out += ["--tf-find-links", str(args.wrapper_tf_find_links)]
    if getattr(args, "minimal", False):
        out.append("--minimal")
    for kv in getattr(args, "wrapper_env", None) or []:
        out += ["--env", kv]
    return out


def render_toolserver_unit(lay: Layout, port: int) -> str:
    return "\n".join([
        "[Unit]",
        "Description=hugpy orbit toolserver (abstract-toolserver for hugpy-core; not the per-user node)",
        "After=network-online.target postgresql.service", "Wants=network-online.target", "",
        "[Service]", "Type=simple",
        f"EnvironmentFile={lay.ts_env}",
        # its own config root: node.json / endpoint.json / ~/.env lookups resolve under it.
        # ABSTRACT_TOOLSERVER_HOME is the new knob; HOME is what the current release reads.
        f"Environment=HOME={lay.ts_home}",
        f"Environment=ABSTRACT_TOOLSERVER_HOME={lay.ts_home}",
        f"Environment=TOOLSERVER_ENV_FILE={lay.ts_env}",
        f"Environment=TOOLSERVER_TOKEN_FILE={lay.ts_env}",
        # the per-user runtime advertisement belongs to the account's own node
        "UnsetEnvironment=XDG_RUNTIME_DIR",
        f"Environment=PATH={lay.bin_dir}:/usr/local/bin:/usr/bin:/bin",
        "Environment=PYTHONUNBUFFERED=1",
        f"WorkingDirectory={lay.ts_home}",
        f"ExecStart={lay.exe('abstract-toolserver')} serve --host {TS_HOST} --port {port}",
        "Restart=on-failure", "RestartSec=3", "",
        "[Install]", "WantedBy=default.target", ""])


def render_core_unit(lay: Layout, host: str, port: int) -> str:
    return "\n".join([
        "[Unit]", "Description=hugpy core (console UI + API)",
        f"After=network-online.target hugpy-router.service {TS_SERVICE}.service",
        "Wants=network-online.target", "",
        "[Service]", "Type=simple",
        f"EnvironmentFile={lay.core_env}",
        f"Environment=PATH={lay.bin_dir}:/usr/local/bin:/usr/bin:/bin",
        "Environment=PYTHONUNBUFFERED=1",
        f"WorkingDirectory={lay.core_home}",
        f"ExecStart={lay.exe('hugpy-core')} --host {host} --port {port}",
        "Restart=on-failure", "RestartSec=3", "",
        "[Install]", "WantedBy=default.target", ""])


def render_downloader_unit(lay: Layout) -> str:
    return "\n".join([
        "[Unit]", "Description=Hugpy model download daemon", "After=network-online.target",
        "Wants=network-online.target", "", "[Service]", "Type=simple",
        f"EnvironmentFile={lay.core_env}", f"WorkingDirectory={lay.core_home}",
        f"ExecStart={lay.exe('python')} -m hugpy_storage.downloader.daemon",
        "Restart=on-failure", "RestartSec=3", "KillMode=control-group", "",
        "[Install]", "WantedBy=default.target", ""])


def render_catalog_unit(lay: Layout) -> str:
    return render_downloader_unit(lay).replace("Description=Hugpy model download daemon", "Description=Hugpy background model catalog").replace(
        "-m hugpy_storage.downloader.daemon", "-m hugpy_storage.hub.discovery")


# ── steps' helpers ────────────────────────────────────────────────────────────
def _run(cmd: List[str]) -> None:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        raise InstallError(f"`{' '.join(cmd)}` failed ({p.returncode}): {(p.stderr or p.stdout).strip()[-600:]}")


def _run_through(cmd: List[str]) -> None:
    """A sub-installer, its numbered steps shown as they happen."""
    print(f"    $ {' '.join(cmd)}", flush=True)
    p = subprocess.run(cmd, capture_output=True, text=True)
    for line in (p.stdout + p.stderr).splitlines():
        print(f"    | {line}", flush=True)
    if p.returncode:
        raise InstallError(f"`{' '.join(cmd)}` failed ({p.returncode})")


def _active(lay: Layout, service: str) -> str:
    return subprocess.run(lay.systemctl + ["is-active", f"{service}.service"],
                          capture_output=True, text=True).stdout.strip() or "unknown"


def _start_unit(lay: Layout, service: str, unit_path: str, text: str) -> None:
    write_file(unit_path, text, 0o644)
    _run(lay.systemctl + ["daemon-reload"])
    _run(lay.systemctl + ["enable", f"{service}.service"])
    _run(lay.systemctl + ["restart", f"{service}.service"])


def _wait(u: str, seconds: int, service: str) -> None:
    deadline = time.time() + seconds
    while time.time() < deadline:
        if http_ok(u):
            return
        time.sleep(1)
    raise InstallError(f"no 200 from {u} within {seconds}s (see `journalctl --user -u {service}`)")


def _check_port(lay: Layout, name: str, service: str, port: int, host: str, ports: Dict[str, int]) -> None:
    others = [k for k, v in ports.items() if v == port and k != name]
    if others:
        raise InstallError(f"the {name} and {others[0]} ports are both {port}")
    if not port_free(host, port) and _active(lay, service) != "active":
        raise InstallError(f"{host}:{port} ({name}) is taken by something that is not {service}; "
                           f"choose another --{'' if name == 'core' else name + '-'}port")


def preflight(lay: Layout) -> Tuple[List[str], List[str]]:
    """(notes, problems): problems stop a real install before any step runs; a dry run lists them."""
    notes, problems = [], []
    if not sys.platform.startswith("linux") or not os.path.isdir("/run/systemd/system"):
        raise InstallError("the systemd backend is the only one so far (Linux with systemd)")
    if os.geteuid() == 0:
        raise InstallError("--user as root makes no sense: run it as the account (sudo -iu <account> ...)")
    linger = subprocess.run(["loginctl", "show-user", account(), "-p", "Linger"],
                            capture_output=True, text=True).stdout.strip()
    if linger != "Linger=yes":
        notes.append("lingering is off for this user: the services stop when you log out "
                     "(`loginctl enable-linger` keeps them running)")
    for exe in ("hugpy-core", "fitevict", "hugpy-router", "abstract-toolserver"):
        if not os.access(lay.exe(exe), os.X_OK):
            problems.append(f"{lay.exe(exe)} is missing: install hugpy-core with its dependencies "
                            f"into {sys.prefix} first")
    return notes, problems


def package_version() -> str:
    try:
        from importlib.metadata import version
        return version(PACKAGE)
    except Exception:  # noqa: BLE001
        return ""


def console_dir() -> Optional[str]:
    from hugpy_core.web import ui
    return ui.PACKAGED_DIST if os.path.isfile(os.path.join(ui.PACKAGED_DIST, "index.html")) else None


# ── install ───────────────────────────────────────────────────────────────────
def plan_install(args) -> Plan:
    if args.mode == "system":
        raise InstallError("--system is not done yet for hugpy-core; run it as the account instead: "
                           "sudo -iu <account> hugpy-core install --user")
    lay = layout()
    plan = Plan()
    notes, problems = preflight(lay)
    plan.notes += notes
    user = account()

    core_cur = read_env(lay.core_env) if ours(lay.core_env) else {}     # a hand-made core.env is taken over
    central_models_home = args.central_models_home or core_cur.get(ENV_CENTRAL_MODELS_HOME)
    if central_models_home and not os.path.isdir(central_models_home):
        raise InstallError(f"central model store is not mounted: {central_models_home}")
    ts_cur = read_env(lay.ts_env)
    ports = {"core": resolve_port("core", args.port, core_cur.get(ENV_CORE_PORT)),
             "wrapper": resolve_port("wrapper", args.wrapper_port, read_env(lay.wrapper_env).get(WRAPPER_PORT_ENV)),
             "router": resolve_port("router", args.router_port, read_env(lay.router_env).get(ROUTER_PORT_ENV)),
             "toolserver": resolve_port("toolserver", args.toolserver_port, ts_cur.get("TOOLSERVER_PORT"))}
    _check_port(lay, "toolserver", TS_SERVICE, ports["toolserver"], TS_HOST, ports)
    _check_port(lay, "core", SERVICE, ports["core"], args.host, ports)
    if len(set(ports.values())) != 4:
        raise InstallError(f"the four ports must differ: {ports}")

    core_url = args.url or (core_cur.get(ENV_CORE_URL) if core_cur.get(ENV_CORE_PORT) == str(ports["core"])
                            else None) or url(args.host, ports["core"])
    router_url = url("127.0.0.1", ports["router"])
    wrapper_url = url("127.0.0.1", ports["wrapper"])
    ts_url = url(TS_HOST, ports["toolserver"])
    db = args.db or DEFAULT_DB

    # ── DATABASE MODE (flag-driven; the one TTY question in main() may set args.db_dsn) ──
    db_dsn = (args.db_dsn or "").strip() or None
    schema = (args.schema or core_cur.get(ENV_CORE_SCHEMA) or DEFAULT_SCHEMA)
    if db_dsn:
        mode = "existing"
    elif getattr(args, "create_db", False):
        mode = "create-db"
    elif core_cur.get(ENV_CORE_SCHEMA):                 # a prior existing-DSN install, re-run with no flag
        mode, db_dsn = "existing", _strip_search_path(core_cur.get(_C.ENV_CORE_DB, ""))
    else:
        mode = "own"
    ts_db_dsn = (args.toolserver_db_dsn or "").strip() or None
    if mode == "existing" and not ts_db_dsn:
        ts_db_dsn = _ts_dsn_from_env(ts_cur) or None    # re-run: reuse what db install wrote before
    if mode == "existing" and not ts_db_dsn and not getattr(args, "create_db", False):
        problems.append(
            "existing-database mode (--db-dsn) needs a database for the orbit toolserver, which has no "
            "schema setting. Choose one:\n"
            "    * pass --toolserver-db-dsn <conninfo> for a database the account already owns; or\n"
            f"    * once as root: sudo -u postgres psql -c 'ALTER ROLE {user} CREATEDB'  then add --create-db; or\n"
            "    * drop --db-dsn to use the orbit's own private cluster (the no-root default)")

    if problems:
        if not args.dry_run:
            raise InstallError("\n  ".join(["cannot install:"] + problems))
        plan.notes += [f"a real run would stop here: {p}" for p in problems]

    st: Dict[str, object] = {"core_dsn": None, "db": None, "db_install": {}}

    # 1. code
    plan.add("code", f"use this environment ({sys.prefix}; hugpy-core {package_version() or '?'} with "
                     "hugpy-wrapper, hugpy-router, abstract_toolserver)", lambda: None)

    # 2. database SERVER — the orbit toolserver's own db CLI (core provisions nothing)
    os.makedirs(lay.ts_home, mode=0o700, exist_ok=True)
    pg_data = os.path.join(lay.data_dir, "pg")
    if mode == "own":
        # the orbit toolserver gets its OWN database in the private cluster (never core's):
        # its tables and core's share no namespace, and either can be dropped alone
        inst_args = ["install", "--name", db, "--port", str(CLUSTER_PORT), "--data-dir", pg_data,
                     "--env-file", lay.ts_env, "--mode", "own", "--database", f"{db}_toolserver", "--json"]
        server_detail = (f"abstract-toolserver db install --mode own (the orbit's own cluster on {CLUSTER_PORT}, "
                         f"socket-only, {PG_SERVICE}, data {pg_data}); writes the toolserver's db keys into {lay.ts_env}")
    elif mode == "existing":
        inst_args = ["install", "--name", _dsn_dbname(ts_db_dsn) or f"{db}_toolserver", "--port", str(CLUSTER_PORT),
                     "--data-dir", pg_data, "--env-file", lay.ts_env, "--mode", "existing", "--dsn", ts_db_dsn, "--json"]
        server_detail = (f"abstract-toolserver db install --mode existing --dsn {_redact(ts_db_dsn)} "
                         f"(the orbit toolserver's own account-owned database)")
    else:  # create-db
        ts_db_dsn = ts_db_dsn or f"dbname={db}_toolserver host={PEER_HOST}"
        inst_args = ["install", "--name", _dsn_dbname(ts_db_dsn), "--port", str(CLUSTER_PORT),
                     "--data-dir", pg_data, "--env-file", lay.ts_env, "--mode", "existing", "--dsn", ts_db_dsn, "--json"]
        server_detail = (f"abstract-toolserver db install --mode existing on the system cluster ({PEER_HOST}); "
                         f"brand-new databases (needs CREATEDB)")

    def _db_server():
        st["db_install"] = _db_cli(lay, *inst_args, want_json=True) or {}
    plan.add("database", server_detail, _db_server)

    # 3. core DATABASE — own/create-db: a db in that cluster (db ensure-database); existing: our schema
    def _core_db():
        if mode == "existing":
            dsn = with_search_path(db_dsn, schema)
            create_schema(dsn, schema, user)            # the only SQL core runs itself
            st["core_dsn"], st["db"] = dsn, f"{_dsn_dbname(db_dsn) or '?'} schema {schema}"
        else:
            out = _db_cli(lay, "ensure-database", db, "--env-file", lay.ts_env, "--json", want_json=True) or {}
            dsn = out.get("dsn")
            if not dsn:
                raise InstallError(f"`abstract-toolserver db ensure-database {db}` printed no dsn")
            st["core_dsn"], st["db"] = dsn, db
    core_db_detail = (f"schema {schema} in {_dsn_dbname(db_dsn) or 'the --db-dsn database'} "
                      "(CREATE SCHEMA AUTHORIZATION the account; search_path in the DSN)"
                      if mode == "existing" else
                      f"abstract-toolserver db ensure-database {db} -> HUGPY_CORE_DB / HUGPY_CALLLOG_DSN")
    plan.add("core-database", core_db_detail, _core_db)

    # 4. orbit toolserver — its env now holds the db keys (step 2); core merges its own keys + unit + health
    def _toolserver():
        cur = read_env(lay.ts_env)                      # the SOLCATCHER_POSTGRESQL_* db install just wrote
        merged = {**{k: cur[k] for k in TS_DB_KEYS if cur.get(k) is not None},
                  **toolserver_values(lay, ports["toolserver"], {**ts_cur, **cur})}
        write_file(lay.ts_env, render(merged, f"{TS_SERVICE}: the hugpy orbit's own toolserver"), 0o600)
        _start_unit(lay, TS_SERVICE, lay.ts_unit, render_toolserver_unit(lay, ports["toolserver"]))
        _wait(ts_url + "/healthz", TS_HEALTH_WAIT_S, TS_SERVICE)
    plan.add("toolserver", f"{lay.ts_env} (0600, operator token "
                           f"{'kept' if ts_cur.get(TS_TOKEN_ENV) else 'new'}, db keys from the db step, "
                           f"home {lay.ts_home}); {lay.ts_unit} -> {ts_url}/healthz", _toolserver)

    # 5. wrapper, 6. router: their own installers (idempotent)
    wcmd = [lay.exe("fitevict"), "install", "--user", "--port", str(ports["wrapper"])] + wrapper_args(args)
    plan.add("wrapper", " ".join(wcmd), lambda: _run_through(wcmd))
    if not args.minimal and not getattr(args, "no_assistant_model", False):
        def _assistant_model():
            home = read_env(lay.wrapper_env).get("MODELS_HOME")
            if not home:
                raise InstallError(f"wrapper install did not establish MODELS_HOME in {lay.wrapper_env}")
            _run_through([lay.exe("fitevict-assist"), "--models-home", home, "bootstrap"])
        plan.add("assistant-model", "verified 0.5B GGUF in the wrapper model store (download once)",
                 _assistant_model)
    rcmd = [lay.exe("hugpy-router"), "install", "--user", "--port", str(ports["router"])]
    plan.add("router", " ".join(rcmd), lambda: _run_through(rcmd))

    # 7. core env + unit (serves the @hugpy/ui build packaged in the wheel)
    def _core():
        if not console_dir():
            raise InstallError("this hugpy-core has no packaged console (hugpy_core/web/console/index.html)")
        renv = read_env(lay.router_env)
        if not renv.get(ROUTER_KEY_ENV):
            raise InstallError(f"no {ROUTER_KEY_ENV} in {lay.router_env} after the router step")
        try:
            with open(lay.router_endpoint, encoding="utf-8") as fh:
                r_url = (json.load(fh).get("url") or router_url).rstrip("/")
        except (OSError, ValueError):
            r_url = router_url
        ts_token = read_env(lay.ts_env).get(TS_TOKEN_ENV, "")
        vals = core_values(core_dsn=st["core_dsn"], schema=schema if mode == "existing" else None,
                           host=args.host, port=ports["core"], core_url=core_url, router_url=r_url,
                           router_key=renv[ROUTER_KEY_ENV], ts_url=ts_url, ts_token=ts_token,
                           central_models_home=central_models_home)
        os.makedirs(lay.core_home, mode=0o700, exist_ok=True)
        vals["HUGPY_COMMS_DB"] = core_cur.get("HUGPY_COMMS_DB") or os.path.join(lay.core_home, "downloads.sqlite3")
        write_file(lay.core_env, render(vals, f"{SERVICE}"), 0o600)
        # a hand-started or hand-written unit of the same name goes first
        subprocess.run(lay.systemctl + ["stop", f"{SERVICE}.service"], capture_output=True)
        _start_unit(lay, SERVICE, lay.core_unit, render_core_unit(lay, args.host, ports["core"]))
        _start_unit(lay, "hugpy-core-downloader", os.path.join(lay.unit_dir, "hugpy-core-downloader.service"), render_downloader_unit(lay))
        _start_unit(lay, "hugpy-core-catalog", os.path.join(lay.unit_dir, "hugpy-core-catalog.service"), render_catalog_unit(lay))
        _wait(url(args.host, ports["core"]) + "/api/auth/config", HEALTH_WAIT_S, SERVICE)
    took_over = os.path.exists(lay.core_env) and not core_cur
    core_db_str = (f"schema {schema} in the --db-dsn database" if mode == "existing"
                   else f"db {db} in the orbit cluster")
    plan.add("core", f"{lay.core_env} (0600{', replaces the hand-made one' if took_over else ''}: {core_db_str} for "
                     f"core + call log, router {router_url} + its key, toolserver {ts_url} + its token); "
                     f"packaged console {console_dir() or '<missing>'} at {core_url}/; "
                     f"{lay.core_unit} on {args.host}:{ports['core']} -> /api/auth/config", _core)

    # 8. endpoint
    def _endpoint():
        write_file(lay.endpoint_file, json.dumps({
            "service": SERVICE, "mode": "user", "version": package_version() or None,
            "core": core_url, "console": core_url + "/", "wrapper": wrapper_url, "router": router_url,
            "toolserver": ts_url, "db_mode": mode, "db": st.get("db"),
            "db_server": {k: st.get("db_install", {}).get(k)
                          for k in ("mode", "socket_dir", "host", "port", "unit", "database", "ready")},
            "core_schema": schema if mode == "existing" else None,
            "env_file": lay.core_env, "toolserver_env_file": lay.ts_env}, indent=1) + "\n", 0o644)
    plan.add("endpoint", f"{lay.endpoint_file} (core, wrapper, router, toolserver urls + db summary; no secret)",
             _endpoint)
    return plan


def _strip_search_path(conninfo: str) -> str:
    """Drop a trailing ``options=-c search_path=…`` core itself appended, to recover
    the operator's bare --db-dsn for an existing-mode re-run."""
    i = (conninfo or "").find("options=-c search_path=")
    return conninfo[:i].strip() if i >= 0 else (conninfo or "").strip()


def _ts_dsn_from_env(env: Dict[str, str]) -> str:
    """Rebuild a libpq conninfo from the toolserver env's SOLCATCHER_POSTGRESQL_* keys
    (existing-mode re-run: reuse the toolserver database db install wrote last time)."""
    m = [("dbname", "SOLCATCHER_POSTGRESQL_NAME"), ("host", "SOLCATCHER_POSTGRESQL_HOST"),
         ("port", "SOLCATCHER_POSTGRESQL_PORT"), ("user", "SOLCATCHER_POSTGRESQL_USER")]
    return " ".join(f"{kw}={env[k]}" for kw, k in m if env.get(k))


def _redact(conninfo: str) -> str:
    """A conninfo with any password= removed, for plan details / logs."""
    return " ".join(t for t in (conninfo or "").split() if not t.startswith("password="))


# ── uninstall / status ───────────────────────────────────────────────────────
def plan_uninstall(args) -> Plan:
    if args.mode == "system":
        raise InstallError("--system is not done yet for hugpy-core")
    lay = layout()
    plan = Plan()
    purge = getattr(args, "purge", False)
    if purge and not getattr(args, "dry_run", False) and not getattr(args, "yes", False):
        # --purge drops the orbit's cluster and EVERY database in it: confirm here, once,
        # then hand the db CLI --yes (its own prompt would be swallowed by _db_cli's capture,
        # and without a TTY it silently KEPT the data — 2026-10-08 fresh-db runs reused it)
        if not sys.stdin.isatty():
            raise InstallError("--purge removes the orbit's database cluster and all its databases: "
                               "pass --yes to confirm (no terminal to ask on)")
        ans = input(f"remove the orbit's database cluster ({os.path.join(lay.data_dir, 'pg')}) "
                    "and ALL its databases? [y/N] ").strip().lower()
        if ans not in ("y", "yes"):
            raise InstallError("not purged: nothing was changed")

    def _stop_core():
        subprocess.run(lay.systemctl + ["disable", "--now", f"{SERVICE}.service"], capture_output=True)
        subprocess.run(lay.systemctl + ["disable", "--now", "hugpy-core-downloader.service"], capture_output=True)
        subprocess.run(lay.systemctl + ["disable", "--now", "hugpy-core-catalog.service"], capture_output=True)
        for p in (lay.core_unit, lay.core_env, os.path.join(lay.unit_dir, "hugpy-core-downloader.service"), os.path.join(lay.unit_dir, "hugpy-core-catalog.service")):
            if os.path.exists(p):
                os.remove(p)
        subprocess.run(lay.systemctl + ["daemon-reload"], capture_output=True)
    plan.add(SERVICE, f"stop, disable, remove {lay.core_unit} and {lay.core_env}", _stop_core)

    def _stop_ts():                                     # the toolserver env stays until the db step reads it
        subprocess.run(lay.systemctl + ["disable", "--now", f"{TS_SERVICE}.service"], capture_output=True)
        if os.path.exists(lay.ts_unit):
            os.remove(lay.ts_unit)
        subprocess.run(lay.systemctl + ["daemon-reload"], capture_output=True)
    plan.add(TS_SERVICE, f"stop, disable, remove {lay.ts_unit}", _stop_ts)

    def _db():
        # the toolserver's db CLI owns the cluster/unit (hugpy-postgres); it keeps the
        # data unless told otherwise. Never fatal — an orbit with no cluster still cleans up.
        _db_cli(lay, "uninstall", "--env-file", lay.ts_env, *(["--yes"] if purge else ["--keep-data"]), check=False)
        if purge:
            if os.path.exists(lay.ts_env):
                os.remove(lay.ts_env)
            shutil.rmtree(lay.ts_home, ignore_errors=True)
    plan.add("database", f"abstract-toolserver db uninstall{'' if purge else ' --keep-data'}"
                         + ("; remove the toolserver env + home" if purge else ""), _db)

    plan.add("endpoint", f"remove {lay.endpoint_file}",
             lambda: os.path.exists(lay.endpoint_file) and os.remove(lay.endpoint_file))
    if not purge:
        plan.notes.append(f"kept the database/cluster and the toolserver home ({lay.ts_home}) and its env "
                          f"({lay.ts_env}); re-run `hugpy-core uninstall --user --purge` to drop them too")
    plan.notes.append("kept the wrapper and the router: they have their own "
                      "`fitevict uninstall --user` / `hugpy-router uninstall --user`")
    return plan


def status(args) -> dict:
    lay = layout()
    core = read_env(lay.core_env)
    ts = read_env(lay.ts_env)
    wr = read_env(lay.wrapper_env)
    ro = read_env(lay.router_env)
    out = {"mode": "user", "env": lay.core_env if core else None}

    def one(service, unit, u, probe):
        d = {"service": _active(lay, service), "unit": unit if os.path.exists(unit) else None, "url": u}
        if u:
            d["health"] = "ok" if http_ok(u + probe) else "down"
        return d
    core_u = url(core.get(ENV_CORE_HOST, "127.0.0.1"), int(core[ENV_CORE_PORT])) if core.get(ENV_CORE_PORT) else None
    out["core"] = one(SERVICE, lay.core_unit, core_u, "/api/auth/config")
    out["core"]["db"] = core.get(_C.ENV_CORE_DB)
    out["core"]["schema"] = core.get(ENV_CORE_SCHEMA)
    out["core"]["console"] = console_dir()
    out["toolserver"] = one(TS_SERVICE, lay.ts_unit, ts.get("TOOLSERVER_URL"), "/healthz")
    # the database server (owned by the toolserver's db CLI): kind/mode, socket/port, ready
    try:
        dbs = _db_cli(lay, "status", "--env-file", lay.ts_env, "--json", want_json=True, check=False) or {}
    except Exception:  # noqa: BLE001 — the db CLI absent/erroring never breaks status
        dbs = {}
    out["database"] = {"server": dbs.get("server"), "mode": dbs.get("mode"),
                       "socket_dir": dbs.get("socket_dir"), "host": dbs.get("host"),
                       "port": dbs.get("port"), "ready": dbs.get("ready"), "unit": dbs.get("unit"),
                       "core_db": core.get(_C.ENV_CORE_DB), "core_schema": core.get(ENV_CORE_SCHEMA),
                       "toolserver_db": ts.get("SOLCATCHER_POSTGRESQL_NAME")}
    wl = W.layout("user")
    out["wrapper"] = one("hugpy-wrapper", wl.unit_path,
                         url(wr.get("FITEVICT_HOST", "127.0.0.1"), int(wr[WRAPPER_PORT_ENV]))
                         if wr.get(WRAPPER_PORT_ENV) else None, "/health")
    out["router"] = one("hugpy-router", os.path.join(lay.unit_dir, "hugpy-router.service"),
                        url(ro.get("HUGPY_ROUTER_HOST", "127.0.0.1"), int(ro[ROUTER_PORT_ENV]))
                        if ro.get(ROUTER_PORT_ENV) else None, "/health")
    return out


# ── command line ──────────────────────────────────────────────────────────────
def _mode(p: argparse.ArgumentParser) -> None:
    m = p.add_mutually_exclusive_group()
    m.add_argument("--user", dest="mode", action="store_const", const="user",
                   help="this account's own services (default)")
    m.add_argument("--system", dest="mode", action="store_const", const="system", help="not done yet")
    p.set_defaults(mode="user")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="hugpy-core",
                                 description="Install, remove or inspect the hugpy orbit (core, its toolserver, "
                                             "the wrapper, the router) for this account.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pi = sub.add_parser("install", help="install or repair the whole orbit")
    _mode(pi)
    pi.add_argument("--host", default=DEFAULT_HOST, help=f"core's listen address (default {DEFAULT_HOST})")
    pi.add_argument("--port", help=f"core's port (default {DEFAULT_PORTS['core']}, or as installed)")
    pi.add_argument("--wrapper-port", help=f"default {DEFAULT_PORTS['wrapper']}, or as installed")
    pi.add_argument("--router-port", help=f"default {DEFAULT_PORTS['router']}, or as installed")
    pi.add_argument("--toolserver-port", help=f"default {DEFAULT_PORTS['toolserver']}, or as installed")
    pi.add_argument("--db", help=f"database name in the orbit's own cluster (own mode; default {DEFAULT_DB})")
    pi.add_argument("--db-dsn", help="EXISTING-database mode: a libpq conninfo for a database the account "
                                     "owns (peer auth). Core takes its own SCHEMA inside it (--schema).")
    pi.add_argument("--schema", help=f"existing-database mode: core's schema (default {DEFAULT_SCHEMA}, or as "
                                     "installed)")
    pi.add_argument("--toolserver-db-dsn", help="existing-database mode: a conninfo for the orbit toolserver's "
                                                "OWN database (it has no schema setting of its own)")
    pi.add_argument("--create-db", action="store_true",
                    help="create brand-new databases in the system cluster (needs the role's CREATEDB)")
    pi.add_argument("--url", help="core's URL as others reach it (HUGPY_CORE_URL; default from --host/--port)")
    pi.add_argument("--central-models-home", metavar="DIR",
                    help="central model store for worker transfers (kept on later installs)")
    # passed through to `fitevict install` (the box this orbit runs: its worker name, its own
    # model store on its drive, its engine); core asks its own questions, so the wrapper runs --yes
    pi.add_argument("--worker", help="the wrapper's worker name (default: the host name)")
    pi.add_argument("--models", help="the wrapper's model store (the box's own models on its drive)")
    pi.add_argument("--engine", help="pip spec of an engine for the wrapper to install")
    tf_choice = pi.add_mutually_exclusive_group()
    tf_choice.add_argument("--wrapper-tf", dest="wrapper_tf", action="store_true", default=True,
                           help="build the wrapper's transformers engine (default; serves non-GGUF models)")
    tf_choice.add_argument("--no-wrapper-tf", dest="wrapper_tf", action="store_false",
                           help="skip the transformers engine on a GGUF-only box")
    pi.add_argument("--wrapper-tf-find-links", metavar="DIR",
                    help="pass `--find-links DIR` to the wrapper's tf step (local wheels) — "
                         "`fitevict install --tf-find-links DIR`")
    pi.add_argument("--minimal", action="store_true", help="wrapper without an engine (pip-minimal form)")
    pi.add_argument("--no-assistant-model", action="store_true",
                    help="skip the default 0.5B model download (for offline installs)")
    pi.add_argument("--wrapper-env", action="append", metavar="KEY=VALUE", default=[],
                    help="extra wrapper setting, e.g. LLAMA_SERVER_BIN=/path (repeatable)")
    pi.add_argument("--dry-run", action="store_true", help="print the plan, change nothing")
    pu = sub.add_parser("uninstall", help="stop and remove core and its toolserver (DB, wrapper, router stay)")
    _mode(pu)
    pu.add_argument("--purge", action="store_true",
                    help="also drop the orbit's database/cluster and the toolserver home (default: keep data)")
    pu.add_argument("--yes", "-y", action="store_true", help="confirm --purge without asking (scripts)")
    pu.add_argument("--dry-run", action="store_true")
    ps = sub.add_parser("status", help="each service: active?, health, url; plus the database server")
    _mode(ps)
    return ap


def _ask_db_mode(args) -> None:
    """The ONE interactive question: only on a real TTY, only when no DB flag was
    given. The default (empty answer) is the orbit's own private cluster — no root.
    Scripted / unattended installs pass flags and never reach this. A seam so tests
    can fake sys.stdin.isatty() + input()."""
    if getattr(args, "db_dsn", None) or getattr(args, "create_db", False):
        return
    try:
        if not sys.stdin.isatty():
            return
    except (ValueError, OSError):
        return
    ans = input("database — [1] the orbit's own private cluster (default, no root)  "
                "[2] an existing database you own  > ").strip().lower()
    if ans in ("2", "e", "existing"):
        dsn = input("  libpq conninfo (e.g. dbname=toolserver_hugpy): ").strip()
        if dsn:
            args.db_dsn = dsn


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if not os.environ.get("XDG_RUNTIME_DIR"):
        run_dir = f"/run/user/{os.getuid()}"          # `systemctl --user` needs it (sudo -iu, ssh, cron)
        if os.path.isdir(run_dir):
            os.environ["XDG_RUNTIME_DIR"] = run_dir
    try:
        if args.cmd == "install":
            _ask_db_mode(args)
            execute(plan_install(args), args.dry_run)
        elif args.cmd == "uninstall":
            execute(plan_uninstall(args), args.dry_run)
        else:
            if args.mode == "system":
                raise InstallError("--system is not done yet for hugpy-core")
            print(json.dumps(status(args), indent=1))
    except InstallError as exc:
        print(f"hugpy-core {args.cmd}: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
