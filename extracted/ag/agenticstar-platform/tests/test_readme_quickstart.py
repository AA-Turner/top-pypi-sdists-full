"""README の Quick Start が実際に動くことを保証する drift テスト。

背景: README の Quick Start は長らく「`async def main()` を定義するだけで呼び出さない」
断片で、コピーして実行しても何も起きなかった。さらに `__init__.py` が全モジュールを
無条件 import していたため、README が案内する軽量インストール
(`pip install agenticstar-platform` / `[db]` など) では `import agenticstar_platform`
自体が ModuleNotFoundError で失敗していた。

ここでは README **本文から実際にコードを抜き出して実行**することで、
README とサンプルの drift（README だけ直る / コードだけ直る）を検出する。

実行: python -m pytest tests/test_readme_quickstart.py -v
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
README = REPO_ROOT / "README.md"


def _first_python_block(section_heading: str) -> str:
    """指定見出し直後の最初の python コードブロックを返す。"""
    text = README.read_text(encoding="utf-8")
    assert section_heading in text, f"README に見出しがない: {section_heading}"
    after = text.split(section_heading, 1)[1]
    match = re.search(r"```python\n(.*?)```", after, re.S)
    assert match, f"{section_heading} 直後に python コードブロックがない"
    return match.group(1)


@pytest.fixture(scope="module")
def quickstart_code() -> str:
    return _first_python_block("### 1. A minimal agent")


def _run(code: str, tmp_path: Path) -> subprocess.CompletedProcess:
    script = tmp_path / "quickstart.py"
    script.write_text(code, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=tmp_path,
        env={"PYTHONPATH": str(REPO_ROOT), "PATH": "/usr/bin:/bin"},
    )


def test_quickstart_is_executable(quickstart_code: str) -> None:
    """定義しただけで終わる断片ではなく、実行可能な形になっていること。"""
    assert "asyncio.run(" in quickstart_code, (
        "Quick Start が main() を呼んでいない（コピーしても何も起きない状態）"
    )


def test_quickstart_emits_progress_then_terminal_success(
    quickstart_code: str, tmp_path: Path
) -> None:
    """外部サービスなしで progress → terminal success が順に出ること。"""
    result = _run(quickstart_code, tmp_path)

    assert result.returncode == 0, f"stderr:\n{result.stderr}"
    events = _parse_json_lines(result.stdout)
    types = [e["event_type"] for e in events]

    assert types == ["phase_start", "completion_success"], types
    assert events[-1]["message"] == "HELLO AGENTICSTAR"
    assert all(e["execution_id"] == "demo-001" for e in events)


def test_quickstart_failure_path_emits_terminal_failure(
    quickstart_code: str, tmp_path: Path
) -> None:
    """README が案内するとおり、例外時は completion_failure が終端イベントになること。"""
    code = quickstart_code.replace(
        'answer = request.upper()  # replace this with your actual logic',
        'raise RuntimeError("upstream timeout")',
    )
    assert code != quickstart_code, "README の置き換え対象行が変わっている"

    result = _run(code, tmp_path)

    assert result.returncode == 0, f"stderr:\n{result.stderr}"
    events = _parse_json_lines(result.stdout)
    assert [e["event_type"] for e in events] == ["phase_start", "completion_failure"]
    assert events[-1]["message"] == "upstream timeout"


def test_quickstart_uses_only_core_dependencies(quickstart_code: str) -> None:
    """Quick Start が extra 必須のシンボルを使っていないこと。

    README は core install (`pip install agenticstar-platform`) だけで動くと書いている。
    """
    import agenticstar_platform as sdk

    used = re.findall(r"from agenticstar_platform import \(?([^)\n]+)", quickstart_code)
    symbols = {s.strip() for chunk in used for s in chunk.split(",") if s.strip()}
    assert symbols, "Quick Start が SDK を import していない"

    # マッピング表ではなく実際の解決可否で判定する（表の誤りを独立に検出するため）
    failed = {}
    for name in symbols:
        try:
            getattr(sdk, name)
        except ImportError as exc:  # extra 不足
            failed[name] = str(exc)
    assert not failed, (
        f"この環境で解決できないシンボルが Quick Start にある: {failed}"
    )


def _parse_json_lines(stdout: str) -> list[dict]:
    """1 行 1 JSON であることまで含めて検証する。

    README は出力例を 2 行で示している。サンプルが `print(chunk, end="")` に戻ると
    区切りなしで連結され README と食い違うため、寛容なパーサーで吸収しない。
    """
    lines = [line for line in stdout.splitlines() if line.strip()]
    return [json.loads(line) for line in lines]


# ---------------------------------------------------------------------------
# Marketplace runner サンプル（### 2.）の drift 検出
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def marketplace_code() -> str:
    return _first_python_block("### 2. Run the same function Marketplace-compatible")


def test_marketplace_sample_uses_public_runner_api(marketplace_code: str) -> None:
    """README の Marketplace サンプルが公開 runner API と一致していること。

    実行には DB / webhook が要るため、ここでは compile と公開シンボルの解決
    （= rename や export 漏れの drift）を固定する。実行時の契約は
    tests/runner/test_marketplace_runner_contract.py が担う。
    """
    compile(marketplace_code, "marketplace_agent.py", "exec")
    assert "run_marketplace_agent(" in marketplace_code

    import agenticstar_platform as sdk

    assert callable(sdk.run_marketplace_agent)


def test_marketplace_env_contract_documented(marketplace_code: str) -> None:
    """README の env 契約表が runner の実装契約と一致していること。"""
    from agenticstar_platform.runner import REQUIRED_IDENTITY_ENV, WEBHOOK_URL_ENV

    text = README.read_text(encoding="utf-8")
    section = text.split("### 2. Run the same function Marketplace-compatible", 1)[1]
    section = section.split("### 3.", 1)[0]
    for name in (*REQUIRED_IDENTITY_ENV, WEBHOOK_URL_ENV):
        assert name in section, f"README の env 契約表に {name} がない"
