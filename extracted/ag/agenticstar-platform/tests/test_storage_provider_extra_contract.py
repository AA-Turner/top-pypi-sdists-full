"""molt#1367: storage provider extra → 公開シンボル契約のテスト。

固定する契約:
  1. `AzureBlobStorageClient`→`storage-azure` / `S3StorageClient`→`storage-aws` /
     `GCSStorageClient`→`storage-gcp` の対応が公開 API contract である
  2. provider 依存が無い場合、シンボル取得の時点で (constructor まで遅延せず)
     正しい SDK extra と `pip install 'agenticstar-platform[<extra>]'` 形式の
     案内で失敗する。top-level / storage submodule の両 import 経路で同一挙動
  3. core 型 (StorageConfig 等) は provider 実装 module を一切 import せずに
     両経路から import できる
  4. 依存欠落だけを extra 不足へ変換し、provider module 内部の import 不具合は
     そのまま raise する (誤診しない)
  5. `__all__` / `dir()` の discoverability と、依存が揃った環境での
     両経路同一オブジェクト解決 (後方互換)
  6. _PROVIDER_CLIENTS (単一正本) と pyproject extras / _EXTRA_DEPENDENCIES の
     一致 (drift 検知)

実行: python -m pytest tests/test_storage_provider_extra_contract.py -v
"""

from __future__ import annotations

import importlib
import importlib.util
import sys

import pytest

import agenticstar_platform as sdk
import agenticstar_platform.storage as storage_pkg

# (公開シンボル, extra, ブロックする依存 root)
PROVIDER_CASES = [
    ("AzureBlobStorageClient", "storage-azure", "azure.storage.blob"),
    ("S3StorageClient", "storage-aws", "boto3"),
    ("GCSStorageClient", "storage-gcp", "google.cloud.storage"),
]

CORE_TYPES = ["StorageConfig", "UploadResult", "DownloadResult", "StoragePaths"]


def _purge_storage_modules(monkeypatch: pytest.MonkeyPatch) -> None:
    """storage 系 module と遅延解決キャッシュを剥がし、初回アクセス状態へ戻す。"""
    for mod in ("agenticstar_platform.storage.azure",
                "agenticstar_platform.storage.s3",
                "agenticstar_platform.storage.gcs"):
        monkeypatch.delitem(sys.modules, mod, raising=False)
    for name, _extra, _dep in PROVIDER_CASES:
        monkeypatch.delitem(storage_pkg.__dict__, name, raising=False)
        monkeypatch.delitem(sdk.__dict__, name, raising=False)


def _block_dependency(monkeypatch: pytest.MonkeyPatch, *roots: str) -> None:
    """find_spec を偽装して依存 root が「未インストール」に見える状態を作る。"""
    real_find_spec = importlib.util.find_spec

    def _fake_find_spec(name, *args, **kwargs):
        if any(name == r or name.startswith(r + ".") or r.startswith(name + ".")
               for r in roots):
            return None
        return real_find_spec(name, *args, **kwargs)

    monkeypatch.setattr(importlib.util, "find_spec", _fake_find_spec)


class TestSymbolExtraMapping:
    """契約 1+2: 依存欠落はシンボル取得時に正しい extra 案内で失敗する。"""

    @pytest.mark.parametrize("name,extra,dep_root", PROVIDER_CASES)
    def test_top_level_access_gives_provider_extra_hint(
        self, monkeypatch: pytest.MonkeyPatch, name, extra, dep_root
    ) -> None:
        _purge_storage_modules(monkeypatch)
        _block_dependency(monkeypatch, dep_root)

        with pytest.raises(ImportError) as excinfo:
            sdk.__getattr__(name)

        message = str(excinfo.value)
        assert f"'{extra}' extra" in message
        assert f"pip install 'agenticstar-platform[{extra}]'" in message
        # 生 package 名の直接 install を主案内にしない
        assert "pip install boto3" not in message
        assert "pip install azure-storage-blob" not in message
        assert "pip install google-cloud-storage" not in message

    @pytest.mark.parametrize("name,extra,dep_root", PROVIDER_CASES)
    def test_submodule_access_gives_same_extra_hint(
        self, monkeypatch: pytest.MonkeyPatch, name, extra, dep_root
    ) -> None:
        """`agenticstar_platform.storage.<Client>` 経路も同一契約 (両経路一致)。"""
        _purge_storage_modules(monkeypatch)
        _block_dependency(monkeypatch, dep_root)

        with pytest.raises(ImportError) as excinfo:
            storage_pkg.__getattr__(name)

        message = str(excinfo.value)
        assert f"'{extra}' extra" in message
        assert f"pip install 'agenticstar-platform[{extra}]'" in message

    @pytest.mark.parametrize("name,extra,dep_root", PROVIDER_CASES)
    def test_other_providers_unaffected_by_one_missing_dependency(
        self, monkeypatch: pytest.MonkeyPatch, name, extra, dep_root
    ) -> None:
        """1 provider の依存欠落が他 provider の解決を壊さない (単独 extra install)。"""
        _purge_storage_modules(monkeypatch)
        _block_dependency(monkeypatch, dep_root)

        for other_name, _other_extra, other_dep in PROVIDER_CASES:
            if other_name == name:
                continue
            resolved = storage_pkg.__getattr__(other_name)
            assert resolved.__name__ == other_name


class TestCoreTypesIndependence:
    """契約 3: core 型は provider 実装 module を import せず両経路から使える。"""

    def test_core_types_importable_with_all_provider_deps_missing(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _purge_storage_modules(monkeypatch)
        monkeypatch.delitem(sys.modules, "agenticstar_platform.storage", raising=False)
        _block_dependency(
            monkeypatch, "azure.storage.blob", "boto3", "google.cloud.storage"
        )

        storage = importlib.import_module("agenticstar_platform.storage")
        for type_name in CORE_TYPES:
            assert getattr(storage, type_name) is not None
        # provider 実装 module が import されていないこと (分離の実証)
        for mod in ("agenticstar_platform.storage.azure",
                    "agenticstar_platform.storage.s3",
                    "agenticstar_platform.storage.gcs"):
            assert mod not in sys.modules, (
                f"core 利用だけで {mod} が import されている (provider 分離が壊れている)"
            )

    def test_storage_package_import_does_not_load_provider_modules(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """依存が揃った環境でも、storage package import 自体は provider を読まない。"""
        _purge_storage_modules(monkeypatch)
        monkeypatch.delitem(sys.modules, "agenticstar_platform.storage", raising=False)

        importlib.import_module("agenticstar_platform.storage")
        for mod in ("agenticstar_platform.storage.azure",
                    "agenticstar_platform.storage.s3",
                    "agenticstar_platform.storage.gcs"):
            assert mod not in sys.modules


class TestMisdiagnosisPrevention:
    """契約 4: 内部 import 不具合を「extra 不足」と誤診しない。"""

    def test_internal_module_error_propagates_raw(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _purge_storage_modules(monkeypatch)  # 依存は揃っている (pre-check は通る)

        def _raise_unrelated(*_args, **_kwargs):
            raise ModuleNotFoundError(
                "No module named 'some_internal_typo_module'",
                name="some_internal_typo_module",
            )

        monkeypatch.setattr(importlib, "import_module", _raise_unrelated)

        with pytest.raises(ModuleNotFoundError) as excinfo:
            storage_pkg.__getattr__("S3StorageClient")

        assert "some_internal_typo_module" in str(excinfo.value)
        assert "extra" not in str(excinfo.value)


class TestDiscoverabilityAndCompatibility:
    """契約 5: __all__ / dir() / 両経路同一オブジェクト (後方互換)。"""

    def test_provider_clients_remain_in_public_api(self) -> None:
        for name, _extra, _dep in PROVIDER_CASES:
            assert name in storage_pkg.__all__
            assert name in dir(storage_pkg)
            assert name in sdk.__all__
            assert name in dir(sdk)

    def test_both_import_paths_resolve_same_object(self) -> None:
        """依存が揃った環境では従来どおり両経路で同じ class が返る。"""
        for name, _extra, _dep in PROVIDER_CASES:
            via_top = getattr(sdk, name)
            via_submodule = getattr(storage_pkg, name)
            assert via_top is via_submodule
            assert via_top.__name__ == name

    def test_repeated_access_is_cached(self) -> None:
        first = storage_pkg.S3StorageClient
        second = storage_pkg.S3StorageClient
        assert first is second


class TestMetadataDrift:
    """契約 6: _PROVIDER_CLIENTS と pyproject / _EXTRA_DEPENDENCIES の一致。"""

    def test_provider_extras_exist_in_pyproject_with_matching_deps(self) -> None:
        tomllib = pytest.importorskip("tomllib")
        from pathlib import Path

        pyproject = tomllib.loads(
            (Path(__file__).resolve().parents[1] / "pyproject.toml").read_text("utf-8")
        )
        extras = pyproject["project"]["optional-dependencies"]

        for name, (extra, module_path, required) in (
            storage_pkg._PROVIDER_CLIENTS.items()
        ):
            assert extra in extras, f"{name} の extra '{extra}' が pyproject に無い"
            assert required, f"{name} の必要依存が空"
            assert module_path.startswith("."), f"{name} の module path が相対でない"

    def test_provider_clients_match_top_level_extra_dependencies(self) -> None:
        """top-level _EXTRA_DEPENDENCIES との明示的一致 (drift 検知)。"""
        for name, (extra, _module, required) in (
            storage_pkg._PROVIDER_CLIENTS.items()
        ):
            assert extra in sdk._EXTRA_DEPENDENCIES, (
                f"{name} の extra '{extra}' が _EXTRA_DEPENDENCIES に無い"
            )
            assert tuple(required) == tuple(sdk._EXTRA_DEPENDENCIES[extra]), (
                f"'{extra}' の依存が storage._PROVIDER_CLIENTS と "
                f"_EXTRA_DEPENDENCIES で食い違っている"
            )

    def test_symbol_map_still_routes_provider_clients_via_storage(self) -> None:
        """top-level の解決が storage package (単一正本) へ委譲されていること。"""
        for name, _extra, _dep in PROVIDER_CASES:
            assert sdk._SYMBOL_MODULES.get(name) == ".storage"
