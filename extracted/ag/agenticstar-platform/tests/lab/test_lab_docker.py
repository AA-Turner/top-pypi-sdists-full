"""Local integration lab の Docker end-to-end テスト（opt-in、molt#1610）。

Docker daemon と compose v2 が必要なため、既定では skip し
`LAB_DOCKER_TESTS=1` を設定したときだけ実行する（現行 GitLab CI runner は
Kaniko ベースで docker daemon を持たないため、CI では既定 skip となる）:

    LAB_DOCKER_TESTS=1 python -m pytest tests/lab/test_lab_docker.py -v

検証内容: happy path（`python -m agenticstar_platform.lab` 1 コマンド完走）、
再実行の冪等性、reset、reset 後の再現性。モックなし・実 container。
外部利用者と同じ形（パッケージ実行 + 任意 cwd）で起動し、artifact が
cwd 配下に置かれることも検証する。lab 専用 compose project のみを操作する。
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

SDK_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SDK_ROOT))

from agenticstar_platform.lab import lab_config  # noqa: E402

pytestmark = pytest.mark.skipif(
    os.environ.get("LAB_DOCKER_TESTS") != "1",
    reason="Docker end-to-end は LAB_DOCKER_TESTS=1 のときだけ実行する",
)

# 外部利用者相当の任意 cwd（artifact はここに置かれる）。repo コピーの
# agenticstar_platform を使うため PYTHONPATH で SDK_ROOT を先頭に載せる。
# WORKDIR は module fixture で作成する（skip 時に何も作らない・pytest が掃除する）
WORKDIR: Path | None = None
ENV = {**os.environ, "PYTHONPATH": str(SDK_ROOT)}


def _artifacts_dir() -> Path:
    assert WORKDIR is not None
    return WORKDIR / "agenticstar-lab-artifacts"


def _run_lab(*args: str) -> subprocess.CompletedProcess:
    assert WORKDIR is not None
    return subprocess.run(
        [sys.executable, "-m", "agenticstar_platform.lab", *args],
        capture_output=True, text=True, timeout=600, cwd=WORKDIR, env=ENV,
    )


@pytest.fixture(scope="module", autouse=True)
def clean_lab(tmp_path_factory):
    """テスト前後で lab を初期状態にする（lab 専用 project のみ操作）。"""
    global WORKDIR
    WORKDIR = tmp_path_factory.mktemp("agenticstar-lab-e2e")
    _run_lab("--reset", "--yes")
    yield
    _run_lab("--reset", "--yes")
    WORKDIR = None


def test_happy_path_one_command():
    proc = _run_lab()
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout
    assert "🎉 lab journey succeeded" in out
    assert "completion_success" in out
    assert out.count('"event_type": "completion_success"') == 1  # 正確に 1 回
    assert f"retrieved : {lab_config.EXPECTED_DOCUMENT_ID}" in out
    assert f"s3://{lab_config.S3_BUCKET}/" in out
    # artifact のローカルコピーは実行 cwd 配下
    assert _artifacts_dir().is_dir() and list(_artifacts_dir().glob("answer-lab-*.md"))
    # secret を stdout / stderr に出さない
    for secret in (lab_config.PG_PASSWORD, lab_config.S3_SECRET_KEY):
        assert secret not in out and secret not in proc.stderr


def test_rerun_is_idempotent_and_state_survives():
    proc = _run_lab()
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "🎉 lab journey succeeded" in proc.stdout
    assert f"retrieved : {lab_config.EXPECTED_DOCUMENT_ID}" in proc.stdout


def test_doctor_all_green_while_running():
    proc = _run_lab("doctor")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "all checks passed" in proc.stdout


def test_reset_preserves_foreign_files_then_rerun_reproduces_result():
    # 利用者のファイルが artifacts ディレクトリに同居していても reset で消えないこと
    sentinel = _artifacts_dir() / "user-notes.md"
    _artifacts_dir().mkdir(exist_ok=True)
    sentinel.write_text("do not delete", encoding="utf-8")

    reset = _run_lab("--reset", "--yes")
    assert reset.returncode == 0, reset.stdout + reset.stderr
    assert "reset は以下を削除します" in reset.stdout  # 対象の事前列挙
    # reset が no-op でないこと: container / volume / lab 生成 artifact が消えている
    ps = subprocess.run(
        ["docker", "ps", "-a", "--filter", "name=agenticstar-lab", "--format", "{{.Names}}"],
        capture_output=True, text=True, timeout=30,
    )
    assert ps.stdout.strip() == "", f"containers still present: {ps.stdout}"
    vols = subprocess.run(
        ["docker", "volume", "ls", "--filter",
         f"name={lab_config.COMPOSE_PROJECT}_", "--format", "{{.Name}}"],
        capture_output=True, text=True, timeout=30,
    )
    assert vols.stdout.strip() == "", f"volumes still present: {vols.stdout}"
    assert not list(_artifacts_dir().glob("answer-lab-*.md"))
    # sentinel（lab 由来でないファイル）は残り、ディレクトリも保持される
    assert sentinel.read_text(encoding="utf-8") == "do not delete"
    sentinel.unlink()

    rerun = _run_lab()
    assert rerun.returncode == 0, rerun.stdout + rerun.stderr
    assert f"retrieved : {lab_config.EXPECTED_DOCUMENT_ID}" in rerun.stdout
