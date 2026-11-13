"""System installation of the unified Flask Core and its intake worker.

PostgreSQL cluster and database creation belong to ``abstract-toolserver db``.
Core owns its schema and runs it before either installed process starts. The
old Basic database is retained on upgrades for historical records only; the
Flask console reads Core's unified projection.
"""
from __future__ import annotations


import argparse
import json
import os
from pathlib import Path
import pwd
import secrets
import shlex
import subprocess
import sys
import time
import urllib.error
import urllib.request

from hugpy_core import __version__
from hugpy_core.imports.constant.install import (
    DEFAULT_PORTS, ENV_CORE_TS_URL, ENV_CORE_TS_TOKEN, ENV_CORE_DB,
    ENV_CALLLOG_DSN, ENV_CORE_HOST, ENV_CORE_PORT, ENV_CORE_URL,
    TS_TOKEN_ENV, WRAPPER_TOKEN_ENV, TS_HOST, SERVICE,
    CORE_UNIT, DOWNLOAD_UNIT, CATALOG_UNIT,
    INTAKE_UNIT, PG_UNIT, TS_UNIT,
    DEFAULT_PORT, PG_PORT,
)

from . import system_layout


def read_env(path: Path) -> dict[str, str]:
    values = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.lstrip().startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            parts = shlex.split(value, comments=True)
            values[key.strip()] = parts[0] if parts else ""
    return values


def write_file(path: Path, data: str, *, mode: int, uid: int = 0, gid: int = 0) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".new")
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode)
    with os.fdopen(fd, "w", encoding="utf-8") as output:
        output.write(data)
        os.fchmod(output.fileno(), mode)
        os.fchown(output.fileno(), uid, gid)
    os.replace(temp, path)


def run(*args: str, input: str | None = None) -> subprocess.CompletedProcess:
    result = subprocess.run(args, input=input, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"{args[0]} {args[1] if len(args) > 1 else ''} failed: "
                           f"{(result.stderr or result.stdout).strip()[-600:]}")
    return result


def db_command(executable: str, *args: str) -> dict:
    result = run(executable, "db", *args, "--json")
    return json.loads(result.stdout.strip().splitlines()[-1])


def _quote(value):
    return json.dumps(str(value).replace('%', '%%'))


def _directory(value):
    # WorkingDirectory is one path, not a systemd word list: quotes are literal.
    return str(value).replace("%", "%%")


def _unit(lay, executable: str, host: str, port: int, *, intake: bool, paths: list[str]) -> str:
    description = "Hugpy Core telemetry intake" if intake else "Hugpy Core Flask API and console"
    launch = (f"{_quote(executable)} -m hugpy_core.intake.service" if intake else
              f"{_quote(executable)} -m hugpy_core.web.server --host {host} --port {port}")
    path_rule = "ReadWritePaths=" + " ".join(_quote(path) for path in paths)
    return "\n".join([
        "[Unit]", f"Description={description}", f"After=network-online.target {PG_UNIT}",
        "Wants=network-online.target",
        # A failed Requires job bypasses Restart and strands intake after DB recovery.
        *((f"Wants={PG_UNIT}", "StartLimitIntervalSec=0") if intake else (f"Requires={PG_UNIT}",)),
        "", "[Service]", "Type=simple",
        f"User={lay.account}", f"Group={lay.group}", f"WorkingDirectory={_directory(lay.state)}",
        f"EnvironmentFile={_directory(lay.config)}", "Environment=PYTHONDONTWRITEBYTECODE=1",
        f"ExecStartPre={_quote(executable)} -c 'from hugpy_core import schema; schema.ensure()'",
        f"ExecStart={launch}", "Restart=on-failure", "RestartSec=3", "TimeoutStopSec=15",
        "UMask=0077", "NoNewPrivileges=true", "PrivateTmp=true", "ProtectSystem=strict",
        "ProtectHome=read-only", path_rule, "", "[Install]", "WantedBy=multi-user.target", "",
    ])


def _local_wrapper(lay, executable: str, dsn: str) -> None:
    endpoint_file = lay.wrapper_endpoint
    if not endpoint_file.exists():
        return
    endpoint = json.loads(endpoint_file.read_text(encoding="utf-8"))
    url = str(endpoint.get("url") or "").rstrip("/")
    if not url:
        return
    token_path = Path(endpoint.get("token_file") or str(lay.wrapper_config))
    key = read_env(token_path).get(endpoint.get("token_env") or WRAPPER_TOKEN_ENV, "")
    try:
        with urllib.request.urlopen(url + "/health", timeout=3) as response:
            name = str(json.load(response).get("worker") or "")
    except (OSError, ValueError):
        name = ""
    if not name:
        import socket
        name = socket.gethostname().split(".", 1)[0]
    script = ("import json,sys; from hugpy_core.registry.registrations import upsert; "
              "upsert(json.load(sys.stdin))")
    registration = {"name": name, "url": url}
    if key:
        registration["key"] = key
    subprocess.run(["runuser", "-u", lay.account, "--", executable, "-c", script],
                   input=json.dumps(registration), text=True,
                   env={**os.environ, **lay.environment(), ENV_CORE_DB: dsn}, check=True,
                   stdout=subprocess.DEVNULL)


def _toolserver(lay, executable: str, current: dict, account) -> None:
    """Provision the Orbit's backend independently of per-user toolserver nodes."""
    existing_url = current.get(ENV_CORE_TS_URL)
    ts = read_env(lay.toolserver_config)
    port = int(ts.get("TOOLSERVER_PORT") or DEFAULT_PORTS["toolserver"])
    if not 1 <= port <= 65535:
        raise RuntimeError("Toolserver port is out of range")
    url = f"http://{TS_HOST}:{port}"
    # An explicitly configured remote backend remains owned by its installer.
    if existing_url and existing_url.rstrip("/") != url:
        if not current.get(ENV_CORE_TS_TOKEN):
            raise RuntimeError("Configured external toolserver needs HUGPY_CORE_TOOLSERVER_TOKEN")
        return
    token = (current.get(ENV_CORE_TS_TOKEN)
             or ts.get(TS_TOKEN_ENV) or secrets.token_urlsafe(32))
    lay.ts_home.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chown(lay.ts_home, account.pw_uid, account.pw_gid)
    ts.update(lay.environment())
    ts.update({"TOOLSERVER_HOST": TS_HOST, "TOOLSERVER_PORT": str(port),
               "TOOLSERVER_URL": url, "TOOLSERVER_STORE": "local",
               TS_TOKEN_ENV: token, "TOOLSERVER_TOKEN": token,
               "ABSTRACT_TOOLSERVER_HOME": str(lay.ts_home),
               "ABSTRACT_TOOLSERVER_ENDPOINT_FILE": str(lay.ts_home / "endpoint.json")})
    write_file(lay.toolserver_config, "".join(f"{key}={json.dumps(value)}\n"
                                        for key, value in sorted(ts.items())),
               mode=0o640, gid=account.pw_gid)
    launch = str(Path(executable).with_name("abstract-toolserver"))
    write_file(lay.unit_dir / TS_UNIT, "\n".join([
        "[Unit]", "Description=Hugpy Orbit toolserver backend",
        f"After=network-online.target {PG_UNIT}", f"Requires={PG_UNIT}",
        "Wants=network-online.target", "", "[Service]", "Type=simple",
        f"User={lay.account}", f"Group={lay.group}", f"WorkingDirectory={_directory(lay.ts_home)}",
        f"EnvironmentFile={_directory(lay.toolserver_config)}",
        f"Environment={_quote('ABSTRACT_TOOLSERVER_HOME=' + str(lay.ts_home))}",
        f"Environment={_quote('TOOLSERVER_ENV_FILE=' + str(lay.toolserver_config))}",
        f"Environment={_quote('TOOLSERVER_TOKEN_FILE=' + str(lay.toolserver_config))}",
        "Environment=PYTHONDONTWRITEBYTECODE=1", "Environment=PYTHONUNBUFFERED=1",
        "UnsetEnvironment=XDG_RUNTIME_DIR", f"ExecStart={_quote(launch)} serve --host {TS_HOST} --port {port}",
        "Restart=on-failure", "RestartSec=3", "UMask=0077", "NoNewPrivileges=true",
        "", "[Install]", "WantedBy=multi-user.target", "",
    ]), mode=0o644)
    run("systemctl", "daemon-reload")
    run("systemctl", "enable", str(lay.unit_dir / TS_UNIT))
    run("systemctl", "restart", TS_UNIT)
    request = urllib.request.Request(url + "/ts/categories", data=b"{}",
                                     headers={"Content-Type": "application/json", "X-Operator-Token": token})
    for _ in range(30):
        try:
            with urllib.request.urlopen(request, timeout=2) as response:
                result = json.load(response)
                if response.status == 200 and isinstance(result, (dict, list)):
                    current.update({ENV_CORE_TS_URL: url,
                                    ENV_CORE_TS_TOKEN: token})
                    return
        except (OSError, ValueError):
            pass
        time.sleep(1)
    raise RuntimeError(f"Orbit toolserver did not become ready; check journalctl -u {TS_UNIT}")


def _service_directories(lay, executable: str, env: dict) -> list[str]:
    """Directories the service writes outside its own state, as its account resolves them, created
    by that account: the platform storage root (hugpy_platform's DEFAULT_ROOT; arms served
    in-process keep uploads and job state there) and the key store's home (API keys and the key
    requirement). On a host whose Core state is not the account's whole home, the unit's sandbox
    would otherwise refuse both."""
    found = []
    for probe in ("from hugpy_platform.constants import DEFAULT_ROOT as path",
                  "from hugpy_core.router.observability.store import home; path = home()"):
        result = subprocess.run(
            ["runuser", "-u", lay.account, "--", executable, "-c",
             probe + "; import os; os.makedirs(path, exist_ok=True); print(path)"],
            env={"PATH": os.environ.get("PATH", "/usr/sbin:/usr/bin:/sbin:/bin"), **env,
                 "HOME": str(lay.account_home)},
            text=True, capture_output=True, cwd="/")
        lines = (result.stdout or "").strip().splitlines() if result.returncode == 0 else []
        if lines and lines[-1].startswith("/") and Path(lines[-1]).is_dir():
            found.append(lines[-1])
    return found


def install(args) -> int:
    if os.geteuid() != 0:
        raise RuntimeError("--system requires root")
    name, units, existing = system_layout.select_identity()
    try:
        account = pwd.getpwnam(name)
    except KeyError:
        # Let the operating system choose its normal account home.
        run("useradd", "--system", "--user-group", "--create-home", name)
        account = pwd.getpwnam(name)
    lay = system_layout.resolve(account, units, existing)
    current = read_env(lay.config)
    lay = system_layout.resolve(account, units, existing, current)
    for root in (lay.config_dir, Path(lay.roots['data']), Path(lay.roots['cache'])):
        if not root.exists():
            root.mkdir(mode=0o750, parents=True, exist_ok=True)
            os.chown(root, account.pw_uid, account.pw_gid)
    lay.unit_dir.mkdir(parents=True, exist_ok=True)
    lay.state.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chown(lay.state, account.pw_uid, account.pw_gid)
    os.chmod(lay.state, 0o700)
    current = read_env(lay.config)
    current.update(lay.environment())
    for key in ('HUGPY_DISCOVERY_DATABASE', 'HUGPY_CATALOG_DISCOVERY_DB',
                'HUGPY_CATALOG_DISCOVERY_DIR', 'HUGPY_CATALOG_WRAPPER_DB'):
        if key in os.environ:
            current[key] = os.environ[key]
    old_flask = read_env(lay.flask_config)
    previous = json.loads(lay.endpoint.read_text()) if lay.endpoint.exists() else {}
    host = args.host or str(previous.get("host") or current.get(ENV_CORE_HOST) or TS_HOST).split(",")[0]
    port = int(args.port or previous.get("port") or current.get(ENV_CORE_PORT) or DEFAULT_PORT)
    if not 1 <= port <= 65535:
        raise RuntimeError("Core port is out of range")
    pg_port = str(current.get("SOLCATCHER_POSTGRESQL_PORT") or PG_PORT)
    executable = str(Path(sys.executable).absolute())
    toolserver = str(Path(executable).with_name("abstract-toolserver"))

    # The toolserver's records have their own database. The existing cluster
    # and Basic database remain untouched during an upgrade.
    cluster = db_command(toolserver, "install", "--system", "--account", lay.account,
                         "--name", SERVICE, "--port", pg_port,
                         "--data-dir", str(lay.state / "pg"), "--env-file", str(lay.toolserver_config),
                         "--database", "hugpy_toolserver", "--yes")
    if not cluster.get("ready"):
        raise RuntimeError("PostgreSQL cluster did not become ready")
    selected_dsn = old_flask.get(ENV_CORE_DB) or current.get(ENV_CORE_DB)
    if selected_dsn:
        core_dsn = selected_dsn
    else:
        target = args.database or ("hugpy_core_flask" if current.get("SOLCATCHER_POSTGRESQL_NAME")
                                   else "hugpy_core")
        core_dsn = db_command(toolserver, "ensure-database", target,
                              "--env-file", str(lay.toolserver_config))["dsn"]

    current.update({
        ENV_CORE_DB: core_dsn, ENV_CALLLOG_DSN: core_dsn,
        ENV_CORE_HOST: host, ENV_CORE_PORT: str(port),
        ENV_CORE_URL: f"http://{host}:{port}",
        "HUGPY_SELF_BASE": f"http://{host}:{port}",
        "HUGPY_CORE_HOME": str(lay.state), "HUGPY_CORE_SHARED_PRESENCE": "1",
        "HUGPY_ROUTER_KEY": current.get("HUGPY_ROUTER_KEY") or "hpk_box_" + secrets.token_urlsafe(32),
    })
    if args.central_models_home:
        current["HUGPY_CENTRAL_MODELS_HOME"] = str(Path(args.central_models_home).absolute())
        current.setdefault("HUGPY_CENTRAL_DRIVES", current["HUGPY_CENTRAL_MODELS_HOME"])
    # Carry current Flask settings over from the old drop-in on upgrades.
    for key, value in old_flask.items():
        if key.startswith("HUGPY_") and key not in (ENV_CORE_DB, ENV_CALLLOG_DSN):
            current.setdefault(key, value)
    _toolserver(lay, executable, current, account)
    current.pop("HUGPY_BASIC_COMPAT_DB", None)
    current.setdefault("HUGPY_LOG_DIR", str(lay.state / "logs"))
    current.setdefault("HUGPY_COMMS_DB", str(lay.state / "downloads.sqlite3"))
    write_file(lay.config, "".join(f"{key}={json.dumps(value)}\n" for key, value in sorted(current.items())),
               mode=0o640, gid=account.pw_gid)
    # runuser needs the new env; systemctl loads it for all Core service units.
    migrate = subprocess.run(["runuser", "-u", lay.account, "--", executable, "-c",
                              "from hugpy_core import schema; schema.ensure()"],
                             env={**os.environ, **current}, text=True, capture_output=True)
    if migrate.returncode:
        raise RuntimeError("Core schema migration failed: " + migrate.stderr.strip()[-600:])
    _local_wrapper(lay, executable, core_dsn)

    paths = [str(lay.state)]
    for value in [current.get("HUGPY_CENTRAL_MODELS_HOME", ""),
                  *[part.split(":", 1)[0] for part in current.get("HUGPY_CENTRAL_DRIVES", "").split(",")]]:
        if value and value.startswith("/"):
            paths.extend(["-" + value, "-" + os.path.realpath(value)])
    # The console's Station tab runs the harness TUI in-process on the sessions
    # service's workspace (hugpy-agent on this box), so the TUI, the brain and the
    # registry share one journal. Optional path: absent when the agent isn't here.
    paths.append("-" + str(Path(lay.roots["data"]) / "agent" / "sessions"))
    paths.extend(_service_directories(lay, executable, current))
    paths = list(dict.fromkeys(paths))
    write_file(lay.unit_dir / CORE_UNIT, _unit(lay, executable, host, port, intake=False, paths=paths), mode=0o644)
    write_file(lay.unit_dir / INTAKE_UNIT, _unit(lay, executable, host, port, intake=True, paths=[str(lay.state)]), mode=0o644)
    download_unit = _unit(lay, executable, host, port, intake=False, paths=paths)
    download_unit = download_unit.replace("Description=Hugpy Core Flask API and console", "Description=Hugpy model download daemon")
    download_unit = download_unit.replace(
        f"-m hugpy_core.web.server --host {host} --port {port}", "-m hugpy_storage.downloader.daemon")
    download_unit = download_unit.replace("TimeoutStopSec=15", "TimeoutStopSec=20\nKillMode=control-group\nLimitNOFILE=65536")
    write_file(lay.unit_dir / DOWNLOAD_UNIT, download_unit, mode=0o644)
    catalog_unit = download_unit.replace("Description=Hugpy model download daemon", "Description=Hugpy background model catalog")
    catalog_unit = catalog_unit.replace("-m hugpy_storage.downloader.daemon", "-m hugpy_storage.hub.discovery")
    write_file(lay.unit_dir / CATALOG_UNIT, catalog_unit, mode=0o644)
    endpoint = {"service": SERVICE, "profile": "flask", "version": __version__,
                "host": host, "port": port, "url": f"http://{host}:{port}",
                "token_file": str(lay.config), "token_env": "HUGPY_ROUTER_KEY", "store": str(lay.state)}
    write_file(lay.endpoint, json.dumps(endpoint, indent=2) + "\n", mode=0o644)
    run("systemctl", "daemon-reload")
    run("systemctl", "enable", *(str(lay.unit_dir / name) for name in
                                  (CORE_UNIT, INTAKE_UNIT, DOWNLOAD_UNIT, CATALOG_UNIT)))
    run("systemctl", "restart", CORE_UNIT, INTAKE_UNIT, DOWNLOAD_UNIT, CATALOG_UNIT)
    for _ in range(60):
        try:
            with urllib.request.urlopen(endpoint["url"] + "/api/auth/config", timeout=2) as response:
                if response.status == 200:
                    print(f"Hugpy Core Flask is ready: {endpoint['url']}")
                    return 0
        except (OSError, urllib.error.HTTPError):
            pass
        time.sleep(1)
    raise RuntimeError("Core did not become healthy. Check journalctl -u hugpy-core.service")


def uninstall(lay) -> int:
    """Remove what `install --system` laid down: stop and disable Core's units and delete their unit files,
    have the database's own installer take its unit away (its data stays), delete the endpoint file. Never
    removed: the configuration (core.env, toolserver.env), the state directory with the PostgreSQL cluster,
    the account, and any drop-ins an operator added beside the units. A later `install --system` finds the
    same account, configuration and state again (system_layout.recorded_install)."""
    if os.geteuid() != 0:
        raise RuntimeError("--system requires root")

    def say(action, what, detail=""):
        print(f"  {action:<10} {what}" + (f"  ({detail})" if detail else ""), flush=True)

    print(f"hugpy-core system uninstall ({__version__})", flush=True)
    for name in (CORE_UNIT, INTAKE_UNIT, DOWNLOAD_UNIT, CATALOG_UNIT, TS_UNIT):
        path = lay.unit_dir / name
        if not path.exists():
            continue
        subprocess.run(["systemctl", "disable", "--now", name], capture_output=True, text=True)
        path.unlink()
        say("remove", str(path), "stopped, disabled")
        if (lay.unit_dir / (name + ".d")).is_dir():
            say("keep", str(lay.unit_dir / (name + ".d")), "operator drop-ins")
    # The cluster belongs to `abstract-toolserver db`: its uninstall stops and removes the unit and keeps the data.
    toolserver = Path(sys.executable).absolute().with_name("abstract-toolserver")
    pg_unit = lay.unit_dir / PG_UNIT
    done = None
    if toolserver.exists() and lay.toolserver_config.exists():
        done = subprocess.run([str(toolserver), "db", "uninstall", "--env-file", str(lay.toolserver_config),
                               "--keep-data", "--json"], capture_output=True, text=True)
    if done is not None and done.returncode == 0 and not pg_unit.exists():
        say("remove", str(pg_unit), "abstract-toolserver db uninstall --keep-data")
    elif pg_unit.exists():      # no database installer to ask (or it left the unit): the same by hand
        subprocess.run(["systemctl", "disable", "--now", PG_UNIT], capture_output=True, text=True)
        pg_unit.unlink()
        say("remove", str(pg_unit), "stopped, disabled" + (f"; db uninstall said: {(done.stderr or done.stdout).strip()[-200:]}"
                                                           if done is not None and done.returncode else ""))
    if lay.endpoint.exists():
        lay.endpoint.unlink()
        say("remove", str(lay.endpoint))
    subprocess.run(["systemctl", "daemon-reload"], capture_output=True, text=True)
    subprocess.run(["systemctl", "reset-failed", CORE_UNIT, INTAKE_UNIT, DOWNLOAD_UNIT, CATALOG_UNIT, TS_UNIT, PG_UNIT],
                   capture_output=True, text=True)
    say("keep", f"{lay.config}, {lay.toolserver_config}", "configuration")
    say("keep", str(lay.state), "state, with the PostgreSQL cluster and its databases")
    say("keep", f"account {lay.account}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog=SERVICE)
    sub = parser.add_subparsers(dest="verb", required=True)
    installer = sub.add_parser("install")
    installer.add_argument("--system", action="store_true", required=True)
    installer.add_argument("--host")
    installer.add_argument("--port", type=int)
    installer.add_argument("--database")
    installer.add_argument("--central-models-home")
    commands = [installer]
    for verb in ("status", "uninstall"):
        p = sub.add_parser(verb)
        p.add_argument("--system", action="store_true", required=True)
        commands.append(p)
    for command in commands:
        command.add_argument('--account', help='service account override')
        command.add_argument('--config-dir', help='shared Hugpy configuration directory')
        command.add_argument('--data-dir', help='shared Hugpy data directory')
        command.add_argument('--home', help='shared HUGPY_HOME runtime root')
        command.add_argument('--unit-dir', help='systemd unit directory override')
    args = parser.parse_args(argv)
    for field, key in (('account', 'HUGPY_SERVICE_USER'), ('config_dir', 'HUGPY_CONFIG_DIR'),
                       ('data_dir', 'HUGPY_DATA_DIR'), ('home', 'HUGPY_HOME'),
                       ('unit_dir', 'HUGPY_SYSTEMD_UNIT_DIR')):
        if getattr(args, field, None):
            os.environ[key] = getattr(args, field)
    try:
        if args.verb == "install":
            return install(args)
        name, units, existing = system_layout.select_identity()
        try:
            account = pwd.getpwnam(name)
        except KeyError:
            if not existing:      # no unit, no recorded install, no such account: nothing to report on or remove
                print(f"hugpy-core {args.verb}: no system install found")
                return 0
            raise
        lay = system_layout.resolve(account, units, existing)
        try:
            lay = system_layout.resolve(account, units, existing, read_env(lay.config))
        except PermissionError:
            if args.verb != "status":
                raise
        if args.verb == "status":
            print(json.dumps({"core": subprocess.run(["systemctl", "is-active", CORE_UNIT],
                                                     capture_output=True, text=True).stdout.strip(),
                              "intake": subprocess.run(["systemctl", "is-active", INTAKE_UNIT],
                                                       capture_output=True, text=True).stdout.strip(),
                              "toolserver": subprocess.run(["systemctl", "is-active", TS_UNIT],
                                                           capture_output=True, text=True).stdout.strip(),
                              "endpoint": json.loads(lay.endpoint.read_text()) if lay.endpoint.exists() else None}))
            return 0
        return uninstall(lay)
    except (RuntimeError, ValueError, OSError, KeyError) as exc:
        print(f"hugpy-core {args.verb}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
