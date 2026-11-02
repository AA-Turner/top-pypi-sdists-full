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
    WRAPPER_ENDPOINT, WRAPPER_CONFIG, ACCOUNT, STATE,
    CONFIG, FLASK_CONFIG, TOOLSERVER_CONFIG, ENDPOINT,
    UNIT_DIR, CORE_UNIT, DOWNLOAD_UNIT, CATALOG_UNIT,
    INTAKE_UNIT, PG_UNIT, TS_UNIT, TS_HOME,
    DEFAULT_PORT, PG_PORT,
)


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


def _unit(executable: str, host: str, port: int, *, intake: bool, paths: list[str]) -> str:
    description = "Hugpy Core telemetry intake" if intake else "Hugpy Core Flask API and console"
    launch = (f"{executable} -m hugpy_core.intake.service" if intake else
              f"{executable} -m hugpy_core.web.server --host {host} --port {port}")
    path_rule = "ReadWritePaths=" + " ".join(paths)
    return "\n".join([
        "[Unit]", f"Description={description}", f"After=network-online.target {PG_UNIT}",
        "Wants=network-online.target",
        # A failed Requires job bypasses Restart and strands intake after DB recovery.
        *((f"Wants={PG_UNIT}", "StartLimitIntervalSec=0") if intake else (f"Requires={PG_UNIT}",)),
        "", "[Service]", "Type=simple",
        f"User={ACCOUNT}", f"Group={ACCOUNT}", f"WorkingDirectory={STATE}",
        f"EnvironmentFile={CONFIG}", "Environment=PYTHONDONTWRITEBYTECODE=1",
        f"ExecStartPre={executable} -c 'from hugpy_core import schema; schema.ensure()'",
        f"ExecStart={launch}", "Restart=on-failure", "RestartSec=3", "TimeoutStopSec=15",
        "UMask=0077", "NoNewPrivileges=true", "PrivateTmp=true", "ProtectSystem=strict",
        "ProtectHome=true", path_rule, "", "[Install]", "WantedBy=multi-user.target", "",
    ])


def _local_wrapper(executable: str, dsn: str) -> None:
    endpoint_file = WRAPPER_ENDPOINT
    if not endpoint_file.exists():
        return
    endpoint = json.loads(endpoint_file.read_text(encoding="utf-8"))
    url = str(endpoint.get("url") or "").rstrip("/")
    if not url:
        return
    token_path = Path(endpoint.get("token_file") or str(WRAPPER_CONFIG))
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
    subprocess.run(["runuser", "-u", ACCOUNT, "--", executable, "-c", script],
                   input=json.dumps(registration), text=True,
                   env={**os.environ, ENV_CORE_DB: dsn}, check=True,
                   stdout=subprocess.DEVNULL)


def _toolserver(executable: str, current: dict, account) -> None:
    """Provision the Orbit's backend independently of per-user toolserver nodes."""
    existing_url = current.get(ENV_CORE_TS_URL)
    ts = read_env(TOOLSERVER_CONFIG)
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
    TS_HOME.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chown(TS_HOME, account.pw_uid, account.pw_gid)
    ts.update({"TOOLSERVER_HOST": TS_HOST, "TOOLSERVER_PORT": str(port),
               "TOOLSERVER_URL": url, "TOOLSERVER_STORE": "local",
               TS_TOKEN_ENV: token, "TOOLSERVER_TOKEN": token,
               "ABSTRACT_TOOLSERVER_HOME": str(TS_HOME),
               "ABSTRACT_TOOLSERVER_ENDPOINT_FILE": str(TS_HOME / "endpoint.json")})
    write_file(TOOLSERVER_CONFIG, "".join(f"{key}={json.dumps(value)}\n"
                                        for key, value in sorted(ts.items())),
               mode=0o640, gid=account.pw_gid)
    launch = str(Path(executable).with_name("abstract-toolserver"))
    write_file(UNIT_DIR / TS_UNIT, "\n".join([
        "[Unit]", "Description=Hugpy Orbit toolserver backend",
        f"After=network-online.target {PG_UNIT}", f"Requires={PG_UNIT}",
        "Wants=network-online.target", "", "[Service]", "Type=simple",
        f"User={ACCOUNT}", f"Group={ACCOUNT}", f"WorkingDirectory={TS_HOME}",
        f"EnvironmentFile={TOOLSERVER_CONFIG}",
        f"Environment=ABSTRACT_TOOLSERVER_HOME={TS_HOME}",
        f"Environment=TOOLSERVER_ENV_FILE={TOOLSERVER_CONFIG}",
        f"Environment=TOOLSERVER_TOKEN_FILE={TOOLSERVER_CONFIG}",
        "Environment=PYTHONDONTWRITEBYTECODE=1", "Environment=PYTHONUNBUFFERED=1",
        "UnsetEnvironment=XDG_RUNTIME_DIR", f"ExecStart={launch} serve --host {TS_HOST} --port {port}",
        "Restart=on-failure", "RestartSec=3", "UMask=0077", "NoNewPrivileges=true",
        "", "[Install]", "WantedBy=multi-user.target", "",
    ]), mode=0o644)
    run("systemctl", "daemon-reload")
    run("systemctl", "enable", TS_UNIT)
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


def install(args) -> int:
    if os.geteuid() != 0:
        raise RuntimeError("--system requires root")
    try:
        account = pwd.getpwnam(ACCOUNT)
    except KeyError:
        run("useradd", "--system", "--user-group", "--home-dir", str(STATE),
            "--shell", "/usr/sbin/nologin", ACCOUNT)
        account = pwd.getpwnam(ACCOUNT)
    STATE.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chown(STATE, account.pw_uid, account.pw_gid)
    os.chmod(STATE, 0o700)
    current = read_env(CONFIG)
    old_flask = read_env(FLASK_CONFIG)
    previous = json.loads(ENDPOINT.read_text()) if ENDPOINT.exists() else {}
    host = args.host or str(previous.get("host") or current.get(ENV_CORE_HOST) or TS_HOST).split(",")[0]
    port = int(args.port or previous.get("port") or current.get(ENV_CORE_PORT) or DEFAULT_PORT)
    if not 1 <= port <= 65535:
        raise RuntimeError("Core port is out of range")
    pg_port = str(current.get("SOLCATCHER_POSTGRESQL_PORT") or PG_PORT)
    executable = str(Path(sys.executable).absolute())
    toolserver = str(Path(executable).with_name("abstract-toolserver"))

    # The toolserver's records have their own database. The existing cluster
    # and Basic database remain untouched during an upgrade.
    cluster = db_command(toolserver, "install", "--system", "--account", ACCOUNT,
                         "--name", ACCOUNT, "--port", pg_port,
                         "--data-dir", str(STATE / "pg"), "--env-file", str(TOOLSERVER_CONFIG),
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
                              "--env-file", str(TOOLSERVER_CONFIG))["dsn"]

    current.update({
        ENV_CORE_DB: core_dsn, ENV_CALLLOG_DSN: core_dsn,
        ENV_CORE_HOST: host, ENV_CORE_PORT: str(port),
        ENV_CORE_URL: f"http://{host}:{port}",
        "HUGPY_SELF_BASE": f"http://{host}:{port}",
        "HUGPY_CORE_HOME": str(STATE), "HUGPY_CORE_SHARED_PRESENCE": "1",
        "HUGPY_ROUTER_KEY": current.get("HUGPY_ROUTER_KEY") or "hpk_box_" + secrets.token_urlsafe(32),
    })
    if args.central_models_home:
        current["HUGPY_CENTRAL_MODELS_HOME"] = str(Path(args.central_models_home).absolute())
        current.setdefault("HUGPY_CENTRAL_DRIVES", current["HUGPY_CENTRAL_MODELS_HOME"])
    # Carry current Flask settings over from the old drop-in on upgrades.
    for key, value in old_flask.items():
        if key.startswith("HUGPY_") and key not in (ENV_CORE_DB, ENV_CALLLOG_DSN):
            current.setdefault(key, value)
    _toolserver(executable, current, account)
    current.pop("HUGPY_BASIC_COMPAT_DB", None)
    current.setdefault("HUGPY_COMMS_DB", str(STATE / "downloads.sqlite3"))
    write_file(CONFIG, "".join(f"{key}={json.dumps(value)}\n" for key, value in sorted(current.items())),
               mode=0o640, gid=account.pw_gid)
    # runuser needs the new env; systemctl loads it for all Core service units.
    migrate = subprocess.run(["runuser", "-u", ACCOUNT, "--", executable, "-c",
                              "from hugpy_core import schema; schema.ensure()"],
                             env={**os.environ, **current}, text=True, capture_output=True)
    if migrate.returncode:
        raise RuntimeError("Core schema migration failed: " + migrate.stderr.strip()[-600:])
    _local_wrapper(executable, core_dsn)

    paths = [str(STATE)]
    for value in [current.get("HUGPY_CENTRAL_MODELS_HOME", ""),
                  *[part.split(":", 1)[0] for part in current.get("HUGPY_CENTRAL_DRIVES", "").split(",")]]:
        if value and value.startswith("/"):
            paths.extend(["-" + value, "-" + os.path.realpath(value)])
    # The console's Station tab runs the harness TUI in-process on the sessions
    # service's workspace (hugpy-agent on this box), so the TUI, the brain and the
    # registry share one journal. Optional path: absent when the agent isn't here.
    paths.append("-/var/lib/hugpy-agent/sessions")
    paths = list(dict.fromkeys(paths))
    write_file(UNIT_DIR / CORE_UNIT, _unit(executable, host, port, intake=False, paths=paths), mode=0o644)
    write_file(UNIT_DIR / INTAKE_UNIT, _unit(executable, host, port, intake=True, paths=[str(STATE)]), mode=0o644)
    download_unit = _unit(executable, host, port, intake=False, paths=paths)
    download_unit = download_unit.replace("Description=Hugpy Core Flask API and console", "Description=Hugpy model download daemon")
    download_unit = download_unit.replace(
        f"-m hugpy_core.web.server --host {host} --port {port}", "-m hugpy_storage.downloader.daemon")
    download_unit = download_unit.replace("TimeoutStopSec=15", "TimeoutStopSec=20\nKillMode=control-group\nLimitNOFILE=65536")
    write_file(UNIT_DIR / DOWNLOAD_UNIT, download_unit, mode=0o644)
    catalog_unit = download_unit.replace("Description=Hugpy model download daemon", "Description=Hugpy background model catalog")
    catalog_unit = catalog_unit.replace("-m hugpy_storage.downloader.daemon", "-m hugpy_storage.hub.discovery")
    write_file(UNIT_DIR / CATALOG_UNIT, catalog_unit, mode=0o644)
    endpoint = {"service": SERVICE, "profile": "flask", "version": __version__,
                "host": host, "port": port, "url": f"http://{host}:{port}",
                "token_file": str(CONFIG), "token_env": "HUGPY_ROUTER_KEY", "store": str(STATE)}
    write_file(ENDPOINT, json.dumps(endpoint, indent=2) + "\n", mode=0o644)
    run("systemctl", "daemon-reload")
    run("systemctl", "enable", CORE_UNIT, INTAKE_UNIT, DOWNLOAD_UNIT, CATALOG_UNIT)
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


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog=SERVICE)
    sub = parser.add_subparsers(dest="verb", required=True)
    installer = sub.add_parser("install")
    installer.add_argument("--system", action="store_true", required=True)
    installer.add_argument("--host")
    installer.add_argument("--port", type=int)
    installer.add_argument("--database")
    installer.add_argument("--central-models-home")
    for verb in ("status", "uninstall"):
        p = sub.add_parser(verb)
        p.add_argument("--system", action="store_true", required=True)
    args = parser.parse_args(argv)
    try:
        if args.verb == "install":
            return install(args)
        if args.verb == "status":
            print(json.dumps({"core": subprocess.run(["systemctl", "is-active", CORE_UNIT],
                                                     capture_output=True, text=True).stdout.strip(),
                              "intake": subprocess.run(["systemctl", "is-active", INTAKE_UNIT],
                                                       capture_output=True, text=True).stdout.strip(),
                              "toolserver": subprocess.run(["systemctl", "is-active", TS_UNIT],
                                                           capture_output=True, text=True).stdout.strip(),
                              "endpoint": json.loads(ENDPOINT.read_text()) if ENDPOINT.exists() else None}))
            return 0
        if os.geteuid() != 0:
            raise RuntimeError("--system requires root")
        run("systemctl", "disable", "--now", CORE_UNIT, INTAKE_UNIT, DOWNLOAD_UNIT, CATALOG_UNIT)
        if (UNIT_DIR / TS_UNIT).exists():
            run("systemctl", "disable", "--now", TS_UNIT)
        return 0
    except (RuntimeError, ValueError, OSError, KeyError) as exc:
        print(f"hugpy-core {args.verb}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
