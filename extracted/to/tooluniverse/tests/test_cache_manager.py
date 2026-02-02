import os
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory

os.environ.setdefault("TOOLUNIVERSE_LIGHT_IMPORT", "1")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from tooluniverse.cache.result_cache_manager import ResultCacheManager


def test_memory_cache_roundtrip():
    manager = ResultCacheManager(
        memory_size=4,
        persistent_path=None,
        enabled=True,
        persistence_enabled=False,
        singleflight=False,
    )

    manager.set(
        namespace="tool",
        version="v1",
        cache_key="key",
        value={"data": 123},
    )

    result = manager.get(namespace="tool", version="v1", cache_key="key")
    assert result == {"data": 123}


def test_cache_ttl_expiration():
    manager = ResultCacheManager(
        memory_size=4,
        persistent_path=None,
        enabled=True,
        persistence_enabled=False,
        singleflight=False,
    )

    manager.set(
        namespace="tool",
        version="v1",
        cache_key="expire",
        value=42,
        ttl=1,
    )
    assert manager.get(namespace="tool", version="v1", cache_key="expire") == 42
    time.sleep(1.1)
    assert manager.get(namespace="tool", version="v1", cache_key="expire") is None


def test_persistent_cache_survives_restart():
    with TemporaryDirectory() as tmpdir:
        cache_path = os.path.join(tmpdir, "cache.sqlite")

        manager1 = ResultCacheManager(
            memory_size=2,
            persistent_path=cache_path,
            enabled=True,
            persistence_enabled=True,
            singleflight=False,
        )
        manager1.set(
            namespace="tool",
            version="v1",
            cache_key="persist",
            value={"foo": "bar"},
        )
        manager1.close()

        manager2 = ResultCacheManager(
            memory_size=1,
            persistent_path=cache_path,
            enabled=True,
            persistence_enabled=True,
            singleflight=False,
        )

        persisted = manager2.get(namespace="tool", version="v1", cache_key="persist")
        assert persisted == {"foo": "bar"}
        manager2.close()
