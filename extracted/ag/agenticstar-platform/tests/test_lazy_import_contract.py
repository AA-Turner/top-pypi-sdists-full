"""遅延 import (PEP 562) の契約テスト。

0.5.25 で `__init__.py` の無条件 import を `__getattr__` による遅延 import へ変えた。
公開 API の後方互換と、「extra 不足の案内が誤診にならないこと」を固定する。

実行: python -m pytest tests/test_lazy_import_contract.py -v
"""

from __future__ import annotations

import builtins
import importlib
import sys

import pytest

import agenticstar_platform as sdk


def test_symbol_module_map_matches_public_api() -> None:
    """__all__ と _SYMBOL_MODULES に欠落・余剰がないこと。"""
    assert set(sdk.__all__) == set(sdk._SYMBOL_MODULES)
    assert len(sdk.__all__) == len(set(sdk.__all__)), "__all__ に重複がある"


def test_every_symbol_resolves_from_its_module() -> None:
    """全公開シンボルが割当先モジュールに実在すること（この環境で解決できる範囲）。"""
    missing = []
    for name, module_path in sdk._SYMBOL_MODULES.items():
        try:
            module = importlib.import_module(module_path, sdk.__name__)
        except ImportError:
            continue  # extra 未導入の環境ではスキップ
        if not hasattr(module, name):
            missing.append(f"{module_path}:{name}")
    assert not missing, f"割当先モジュールに存在しないシンボル: {missing}"


def test_symbol_extras_reference_known_extras() -> None:
    """_SYMBOL_EXTRAS / _MODULE_EXTRAS が _EXTRA_DEPENDENCIES に載った extra を指すこと。"""
    known = set(sdk._EXTRA_DEPENDENCIES)
    assert set(sdk._MODULE_EXTRAS.values()) <= known
    for name, (extra, required) in sdk._SYMBOL_EXTRAS.items():
        assert extra in known, f"{name} が未知の extra を指している: {extra}"
        assert required, f"{name} の必要依存が空"


def test_submodule_attribute_access_is_backward_compatible() -> None:
    """`agenticstar_platform.events` のようなサブモジュール属性が従来どおり参照できること。

    0.5.24 以前は全 import の副作用で成立していた。遅延化で失われないよう固定する。
    """
    assert sdk.events.EventEmitter is sdk.EventEmitter
    assert "events" in dir(sdk)


def test_unknown_attribute_raises_attribute_error() -> None:
    with pytest.raises(AttributeError):
        getattr(sdk, "ThisSymbolDoesNotExist")  # noqa: B009 - 属性エラーの検証が目的


def test_repeated_access_returns_identical_object() -> None:
    """キャッシュ後も同一オブジェクトを返すこと。"""
    first = sdk.EventEmitter
    second = sdk.EventEmitter
    assert first is second
    from agenticstar_platform import EventEmitter  # noqa: PLC0415

    assert EventEmitter is first


def test_missing_extra_gives_actionable_hint(monkeypatch: pytest.MonkeyPatch) -> None:
    """extra 不足は「どの extra を入れればよいか」を示す ImportError になること。"""
    for name in ("agenticstar_platform.db", "agenticstar_platform.db.manager"):
        monkeypatch.delitem(sys.modules, name, raising=False)
    monkeypatch.delitem(sdk.__dict__, "PostgreSQLManager", raising=False)

    real_import = builtins.__import__

    def _fake_import(name, *args, **kwargs):
        if name == "asyncpg" or name.startswith("asyncpg."):
            raise ModuleNotFoundError("No module named 'asyncpg'", name="asyncpg")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", _fake_import)

    with pytest.raises(ImportError) as excinfo:
        sdk.__getattr__("PostgreSQLManager")

    message = str(excinfo.value)
    assert "'db' extra" in message
    assert "pip install 'agenticstar-platform[db]'" in message
    assert "asyncpg" in message


def test_unrelated_import_error_is_not_reported_as_missing_extra(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """実装内部の import ミスを「extra 不足」と誤診しないこと（Codex 指摘 #2）。"""
    for name in ("agenticstar_platform.db", "agenticstar_platform.db.manager"):
        monkeypatch.delitem(sys.modules, name, raising=False)
    monkeypatch.delitem(sdk.__dict__, "PostgreSQLManager", raising=False)

    real_import = builtins.__import__

    def _fake_import(name, *args, **kwargs):
        if name == "some_internal_typo_module":
            raise ModuleNotFoundError(
                "No module named 'some_internal_typo_module'",
                name="some_internal_typo_module",
            )
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", _fake_import)
    monkeypatch.setattr(
        sdk, "_SYMBOL_MODULES", {**sdk._SYMBOL_MODULES, "PostgreSQLManager": ".db"}
    )

    # db モジュール本体の import 内で無関係な依存が欠けた状況を作る
    def _raise_unrelated(*_args, **_kwargs):
        raise ModuleNotFoundError(
            "No module named 'some_internal_typo_module'",
            name="some_internal_typo_module",
        )

    monkeypatch.setattr(importlib, "import_module", _raise_unrelated)

    with pytest.raises(ModuleNotFoundError) as excinfo:
        sdk.__getattr__("PostgreSQLManager")

    assert "some_internal_typo_module" in str(excinfo.value)
    assert "extra" not in str(excinfo.value), "無関係な import 失敗を extra 不足と誤診している"


def test_symbol_level_extra_is_detected_before_silent_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """aiohttp 不在の WebhookEventHandler をシンボル取得時に弾くこと（Codex 指摘 #3）。

    実装は aiohttp が無いとログを出して None を返すだけで、webhook が送られない
    ことに気づけない。取得時点で actionable なエラーにする。
    """
    monkeypatch.delitem(sdk.__dict__, "WebhookEventHandler", raising=False)

    real_find_spec = importlib.util.find_spec

    def _fake_find_spec(name, *args, **kwargs):
        if name == "aiohttp":
            return None
        return real_find_spec(name, *args, **kwargs)

    monkeypatch.setattr(importlib.util, "find_spec", _fake_find_spec)

    with pytest.raises(ImportError) as excinfo:
        sdk.__getattr__("WebhookEventHandler")

    assert "'webhook' extra" in str(excinfo.value)
    assert "aiohttp" in str(excinfo.value)


def test_all_extra_covers_every_other_extra() -> None:
    """[all] が他の全 extra を包含すること（Codex 指摘 #4）。"""
    tomllib = pytest.importorskip("tomllib")
    from pathlib import Path

    pyproject = tomllib.loads(
        (Path(__file__).resolve().parents[1] / "pyproject.toml").read_text("utf-8")
    )
    extras = pyproject["project"]["optional-dependencies"]

    def _names(specs):
        return {
            spec.split(">=")[0].split("==")[0].split("[")[0].strip() for spec in specs
        }

    all_names = _names(extras["all"])
    for extra, specs in extras.items():
        if extra in ("all", "dev"):
            continue
        missing = _names(specs) - all_names - {"httpx"}  # httpx は core 依存
        assert not missing, f"[all] が [{extra}] の依存を含んでいない: {missing}"


def test_version_is_consistent_between_module_and_pyproject() -> None:
    """__version__ と pyproject の version がズレていないこと（publish 漏れの温床）。"""
    tomllib = pytest.importorskip("tomllib")
    from pathlib import Path

    pyproject = tomllib.loads(
        (Path(__file__).resolve().parents[1] / "pyproject.toml").read_text("utf-8")
    )
    assert sdk.__version__ == pyproject["project"]["version"]
