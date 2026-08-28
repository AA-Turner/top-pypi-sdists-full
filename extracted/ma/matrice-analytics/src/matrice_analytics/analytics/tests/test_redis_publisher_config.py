"""Tests for AnalyticsRedisPublisher connection resolution.

Why this exists: `results-agg` sat at 0 entries because the publisher was
constructed with no config and fell through to
``os.environ.get("REDIS_HOST", "localhost")``. On a hostNetwork pod that
resolved to the node, where nothing was listening, so every publish timed out.

Two things had to change and both are pinned here: the caller can now pass the
resolved connection through, and on an HA cluster the publisher talks to
Sentinel rather than to a Service that fronts the master AND its replicas
(writes to a replica fail READONLY).
"""

from unittest.mock import MagicMock, patch

import pytest

from matrice_analytics.analytics.redis_publisher import (
    AnalyticsRedisPublisher,
    _parse_sentinel_hosts,
)

_SENTINEL_ENV = (
    "REDIS_HOST",
    "REDIS_PORT",
    "REDIS_PASSWORD",
    "REDIS_USERNAME",
    "REDIS_DB",
    "REDIS_SENTINEL_HOSTS",
    "REDIS_SENTINEL_PORT",
    "REDIS_MASTER_NAME",
)


@pytest.fixture(autouse=True)
def _clean_redis_env(monkeypatch):
    """Resolution must never depend on the developer's own environment."""
    for var in _SENTINEL_ENV:
        monkeypatch.delenv(var, raising=False)


class TestSentinelHostParsing:
    """The three shapes the value actually arrives in."""

    def test_comma_separated_string_from_env(self):
        assert _parse_sentinel_hosts("a.svc,b.svc", 26379) == [("a.svc", 26379), ("b.svc", 26379)]

    def test_explicit_ports_win_over_the_default(self):
        assert _parse_sentinel_hosts("a.svc:1234,b.svc", 26379) == [("a.svc", 1234), ("b.svc", 26379)]

    def test_list_of_pairs_passes_through(self):
        assert _parse_sentinel_hosts([("a.svc", 26379)], 26379) == [("a.svc", 26379)]

    def test_list_of_strings(self):
        assert _parse_sentinel_hosts(["a.svc", "b.svc:1"], 26379) == [("a.svc", 26379), ("b.svc", 1)]

    @pytest.mark.parametrize("empty", [None, "", [], "  "])
    def test_empty_yields_no_hosts(self, empty):
        assert _parse_sentinel_hosts(empty, 26379) == []

    def test_bad_entries_are_skipped_not_fatal(self):
        assert _parse_sentinel_hosts(["good.svc", "bad.svc:notaport", 42], 26379) == [("good.svc", 26379)]


class TestConnectionResolution:
    def test_defaults_to_localhost_when_nothing_is_configured(self):
        """The original bug's starting point, kept explicit so it stays visible."""
        pub = AnalyticsRedisPublisher()
        assert pub.host == "localhost"
        assert pub.sentinel_hosts == []

    def test_env_supplies_the_connection(self, monkeypatch):
        monkeypatch.setenv("REDIS_HOST", "redis-0.redis-hl.matrice.svc")
        monkeypatch.setenv("REDIS_PORT", "6379")
        monkeypatch.setenv("REDIS_PASSWORD", "secret")
        pub = AnalyticsRedisPublisher()
        assert pub.host == "redis-0.redis-hl.matrice.svc"
        assert pub.password == "secret"

    def test_explicit_config_beats_the_environment(self, monkeypatch):
        """A caller that already resolved the topology must not be overridden."""
        monkeypatch.setenv("REDIS_HOST", "from-env")
        pub = AnalyticsRedisPublisher({"host": "from-config"})
        assert pub.host == "from-config"

    def test_sentinel_from_env(self, monkeypatch):
        monkeypatch.setenv("REDIS_SENTINEL_HOSTS", "redis-sentinel.matrice.svc")
        monkeypatch.setenv("REDIS_SENTINEL_PORT", "26379")
        monkeypatch.setenv("REDIS_MASTER_NAME", "mymaster")
        pub = AnalyticsRedisPublisher()
        assert pub.sentinel_hosts == [("redis-sentinel.matrice.svc", 26379)]
        assert pub.master_name == "mymaster"

    def test_sentinel_from_config(self):
        pub = AnalyticsRedisPublisher(
            {"sentinel_hosts": [("s1", 26379)], "master_name": "mymaster"},
        )
        assert pub.sentinel_hosts == [("s1", 26379)]
        assert pub.master_name == "mymaster"


class TestClientConstruction:
    def test_uses_sentinel_when_configured(self):
        """Sentinel resolves the CURRENT master and follows failover; a fixed
        host cannot, and on an HA Service it is a replica half the time."""
        pub = AnalyticsRedisPublisher(
            {
                "sentinel_hosts": [("s1", 26379)],
                "master_name": "mymaster",
                "password": "pw",
            }
        )
        fake_sentinel_mod = MagicMock()
        master = MagicMock()
        fake_sentinel_mod.Sentinel.return_value.master_for.return_value = master

        with patch.dict("sys.modules", {"redis": MagicMock(), "redis.sentinel": fake_sentinel_mod}):
            assert pub._get_client() is master

        fake_sentinel_mod.Sentinel.assert_called_once()
        assert fake_sentinel_mod.Sentinel.call_args[0][0] == [("s1", 26379)]
        assert fake_sentinel_mod.Sentinel.call_args[1]["password"] == "pw"
        assert fake_sentinel_mod.Sentinel.return_value.master_for.call_args[0][0] == "mymaster"

    def test_falls_back_to_a_direct_client_without_sentinel(self):
        pub = AnalyticsRedisPublisher({"host": "redis.matrice.svc", "port": 6379})
        fake_redis = MagicMock()

        with patch.dict("sys.modules", {"redis": fake_redis}):
            pub._get_client()

        assert fake_redis.Redis.call_args[1]["host"] == "redis.matrice.svc"

    def test_connect_failure_degrades_to_a_no_op(self):
        """Publishing must never take the pipeline down with it."""
        pub = AnalyticsRedisPublisher({"host": "nope"})
        fake_redis = MagicMock()
        fake_redis.Redis.side_effect = OSError("unreachable")

        with patch.dict("sys.modules", {"redis": fake_redis}):
            assert pub._get_client() is None
        assert pub.publish_aggregation("cam1", {"a": 1}) is False
        assert pub.stats["errors"] >= 1

    def test_target_description_names_sentinel(self):
        pub = AnalyticsRedisPublisher({"sentinel_hosts": [("s1", 26379)], "master_name": "mymaster"})
        assert "sentinel" in pub._target_description()
        assert "mymaster" in pub._target_description()


class TestConfigSeam:
    """PostProcRunner -> PostProcessor -> publisher. This chain was severed:
    the correctly-resolved config existed upstream but was never forwarded."""

    def test_post_processor_forwards_redis_config(self):
        from matrice_analytics.post_processing.post_processor import PostProcessor

        cfg = {"host": "redis-0.redis-hl.matrice.svc", "master_name": "mymaster"}
        proc = PostProcessor(redis_config=cfg)
        assert proc._redis_config == cfg

        publisher = proc._get_analytics_publisher()
        assert publisher.host == "redis-0.redis-hl.matrice.svc"
        assert publisher.master_name == "mymaster"

    def test_post_processor_without_config_still_works(self):
        from matrice_analytics.post_processing.post_processor import PostProcessor

        assert PostProcessor()._redis_config == {}


class TestPy38Compatibility:
    """The Orin image runs Python 3.8. A PEP 604 union in a module WITHOUT
    `from __future__ import annotations` is evaluated at import and raises
    TypeError there — that is exactly what crashed matrice_common on Orin.
    ruff's target-version is py311 while requires-python is >=3.8, so it will
    keep suggesting the unsafe form; this test is the guard.
    """

    @pytest.mark.parametrize(
        "module_path",
        [
            "matrice_analytics/analytics/redis_publisher.py",
            "matrice_analytics/post_processing/post_processor.py",
        ],
    )
    def test_no_pep604_unions_without_future_import(self, module_path):
        import ast
        import pathlib

        import matrice_analytics

        root = pathlib.Path(matrice_analytics.__file__).parent.parent
        source = (root / module_path).read_text(encoding="utf-8")
        if "from __future__ import annotations" in source:
            pytest.skip("annotations are deferred in this module; PEP 604 is safe here")

        tree = ast.parse(source)
        offenders = [
            node.lineno
            for node in ast.walk(tree)
            if isinstance(node, ast.arg)
            and isinstance(node.annotation, ast.BinOp)
            and isinstance(node.annotation.op, ast.BitOr)
        ]
        assert not offenders, f"PEP 604 unions at lines {offenders} break the py3.8 Orin image"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
