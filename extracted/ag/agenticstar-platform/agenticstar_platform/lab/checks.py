"""lab の前提・readiness 検査（run_lab と doctor の共通実装、molt#1610）。

すべて read-only。書き込み・container 起動・状態変更は一切行わない。
各 check は CheckResult(ok, name, reason, next_command) を返し、
doctor はそのまま表示し、run_lab は prerequisites / service wait に使う。
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import socket
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Dict, List, Optional

from . import lab_config


@dataclass
class CheckResult:
    ok: bool
    name: str
    reason: str
    next_command: Optional[str] = None

    def render(self) -> str:
        mark = "✅" if self.ok else "❌"
        line = f"{mark} {self.name} — {self.reason}"
        if not self.ok and self.next_command:
            line += f"\n     next: {self.next_command}"
        return line


# --- Docker / compose ---

def _run_command(cmd: List[str], timeout: int = 20):
    """subprocess 実行。hang / OS エラーも traceback にせず分類して返す。

    Returns:
        (CompletedProcess | None, error_reason | None)
    """
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout), None
    except subprocess.TimeoutExpired:
        return None, f"{timeout}s で応答なし（daemon hang の可能性）"
    except OSError as exc:
        return None, f"実行不能 ({type(exc).__name__}: {exc})"


def check_docker_cli() -> CheckResult:
    if shutil.which("docker") is None:
        return CheckResult(
            False, "docker CLI", "docker コマンドが見つかりません",
            "https://docs.docker.com/get-docker/ から Docker をインストール",
        )
    return CheckResult(True, "docker CLI", "found")


def check_docker_daemon() -> CheckResult:
    proc, err = _run_command(["docker", "info", "--format", "{{.ServerVersion}}"])
    if err:
        return CheckResult(
            False, "docker daemon", f"docker info が {err}",
            "Docker Desktop / dockerd を再起動してから再実行",
        )
    if proc.returncode != 0:
        return CheckResult(
            False, "docker daemon", "Docker daemon に接続できません",
            "Docker Desktop / dockerd を起動してから再実行",
        )
    return CheckResult(True, "docker daemon", f"server {proc.stdout.strip()}")


def check_compose() -> CheckResult:
    proc, err = _run_command(["docker", "compose", "version", "--short"])
    if err:
        return CheckResult(
            False, "docker compose", f"docker compose version が {err}",
            "Docker Desktop / dockerd を再起動してから再実行",
        )
    if proc.returncode != 0:
        return CheckResult(
            False, "docker compose", "docker compose (v2) が使えません",
            "Docker Compose v2 プラグインをインストール",
        )
    return CheckResult(True, "docker compose", f"v{proc.stdout.strip()}")


# --- Python extras ---

def check_extras() -> List[CheckResult]:
    results = []
    missing = []
    for module, extra in lab_config.REQUIRED_MODULES.items():
        try:
            spec = importlib.util.find_spec(module)
        except (ModuleNotFoundError, ImportError):
            # dotted name（azure.identity）は親 package 不在だと find_spec 自体が
            # 例外を投げる。これも「未インストール」として扱う
            spec = None
        if spec is None:
            missing.append((module, extra))
    if missing:
        names = ", ".join(f"{m} ([{e}])" for m, e in missing)
        results.append(CheckResult(
            False, "python extras", f"必要モジュール不足: {names}",
            lab_config.INSTALL_HINT,
        ))
    else:
        results.append(CheckResult(True, "python extras", "db / rag / storage-aws 揃っています"))
    return results


def check_artifacts_path() -> CheckResult:
    """artifact 出力先（cwd 配下）の使用可否を preflight する（read-only）。"""
    target = lab_config.ARTIFACTS_DIR
    if target.is_symlink() or (target.exists() and not target.is_dir()):
        return CheckResult(
            False, "artifacts path",
            f"{target} がディレクトリ以外（file/symlink）として存在します",
            f"別のディレクトリへ移動するか名前を変更: ls -la {target}",
        )
    parent = target if target.is_dir() else target.parent
    if not os.access(parent, os.W_OK | os.X_OK):
        return CheckResult(
            False, "artifacts path",
            f"{parent} に書き込みできません（artifact を保存できない）",
            "書き込み可能なディレクトリへ cd してから再実行",
        )
    return CheckResult(True, "artifacts path", f"{target} (writable)")


# --- compose 状態 / port ---

def compose_ps() -> Optional[Dict[str, dict]]:
    """service 名 -> {state, health} を返す。

    Returns:
        dict: 正常に取得できた場合（container が無ければ空 dict）
        None: compose ps 自体が失敗した場合（「container なし」と混同しない）
    """
    proc, err = _run_command(
        ["docker", "compose", "-p", lab_config.COMPOSE_PROJECT,
         "-f", str(lab_config.COMPOSE_FILE), "ps", "-a", "--format", "json"],
    )
    if err or proc.returncode != 0:
        return None
    services: Dict[str, dict] = {}
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        rows = row if isinstance(row, list) else [row]
        for r in rows:
            services[r.get("Service", r.get("Name", "?"))] = {
                "state": r.get("State", "unknown"),
                "health": r.get("Health", ""),
            }
    return services


def port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _http_ok(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=3) as resp:
            return 200 <= resp.status < 300
    except (urllib.error.URLError, OSError, TimeoutError):
        return False


# --- service readiness（read-only probe） ---

def probe_qdrant() -> bool:
    return _http_ok(f"{lab_config.QDRANT_URL}/readyz")


def probe_minio() -> bool:
    return _http_ok(f"{lab_config.S3_ENDPOINT}/minio/health/live")


async def probe_postgres() -> bool:
    try:
        import asyncpg
    except ImportError:
        return False
    try:
        conn = await asyncpg.connect(
            host=lab_config.PG_HOST, port=lab_config.PG_PORT,
            database=lab_config.PG_DATABASE, user=lab_config.PG_USER,
            password=lab_config.PG_PASSWORD, timeout=3,
        )
        try:
            await conn.fetchval("SELECT 1")
        finally:
            await conn.close()
        return True
    except Exception:
        return False


def service_checks(ps: Optional[Dict[str, dict]], pg_ready: bool) -> List[CheckResult]:
    """container 状態 + port + readiness を service ごとに分類する。"""
    if ps is None:
        return [CheckResult(
            False, "compose ps", "docker compose ps が失敗しました（compose 環境の異常）",
            f"docker compose -p {lab_config.COMPOSE_PROJECT} -f {lab_config.COMPOSE_FILE} ps -a を直接実行して原因を確認",
        )]
    plan = [
        ("lab-postgres", pg_ready),
        ("lab-qdrant", probe_qdrant()),
        ("lab-minio", probe_minio()),
    ]
    results = []
    for service, ready in plan:
        ports = lab_config.SERVICE_PORTS[service]
        info = ps.get(service)
        if info is None:
            conflicts = [p for p in ports if port_in_use(p)]
            if conflicts:
                plist = ", ".join(str(p) for p in conflicts)
                results.append(CheckResult(
                    False, service,
                    f"lab の container が無いのに port {plist} が使用中（port 競合）",
                    f"該当 port を使っているプロセスを止めるか確認: lsof -i :{conflicts[0]}",
                ))
            else:
                results.append(CheckResult(
                    False, service, "container が起動していません",
                    "python -m agenticstar_platform.lab",
                ))
        elif info["state"] != "running":
            results.append(CheckResult(
                False, service, f"container state={info['state']}",
                f"docker compose -p {lab_config.COMPOSE_PROJECT} -f {lab_config.COMPOSE_FILE} logs {service}",
            ))
        elif not ready:
            results.append(CheckResult(
                False, service, "container は running だが readiness 応答なし（起動中 or 異常）",
                f"数秒待って再実行。改善しなければ: docker compose -p {lab_config.COMPOSE_PROJECT} -f {lab_config.COMPOSE_FILE} logs {service}",
            ))
        else:
            results.append(CheckResult(True, service, "running / ready"))
    return results


# --- seed 状態 ---

async def seed_status() -> CheckResult:
    """lab_meta の seed/embedding version を検査する（read-only）。"""
    try:
        import asyncpg
    except ImportError:
        return CheckResult(False, "seed", "asyncpg 未インストールで検査不能", lab_config.INSTALL_HINT)
    try:
        conn = await asyncpg.connect(
            host=lab_config.PG_HOST, port=lab_config.PG_PORT,
            database=lab_config.PG_DATABASE, user=lab_config.PG_USER,
            password=lab_config.PG_PASSWORD, timeout=3,
        )
        try:
            exists = await conn.fetchval(
                "SELECT 1 FROM information_schema.tables WHERE table_name = $1",
                lab_config.META_TABLE,
            )
            if not exists:
                return CheckResult(
                    False, "seed", "seed 未適用（lab_meta がありません）",
                    "python -m agenticstar_platform.lab",
                )
            rows = await conn.fetch(
                f"SELECT key, value FROM {lab_config.META_TABLE}"
            )
            meta = {r["key"]: r["value"] for r in rows}
        finally:
            await conn.close()
    except Exception as exc:
        return CheckResult(
            False, "seed", f"PostgreSQL に接続できず検査不能 ({type(exc).__name__})",
            "python -m agenticstar_platform.lab doctor で service 状態を確認",
        )

    expected = {
        "seed_version": lab_config.SEED_VERSION,
        "embedding_version": lab_config.EMBEDDING_VERSION,
    }
    mismatches = {
        k: (meta.get(k), v) for k, v in expected.items() if meta.get(k) != v
    }
    if mismatches:
        detail = ", ".join(
            f"{k}: applied={a!r} expected={e!r}" for k, (a, e) in mismatches.items()
        )
        return CheckResult(
            False, "seed", f"version 不一致（{detail}）",
            "python -m agenticstar_platform.lab --reset で破棄してから再実行",
        )
    return CheckResult(True, "seed", f"seed_version={meta['seed_version']} / {meta['embedding_version']}")
