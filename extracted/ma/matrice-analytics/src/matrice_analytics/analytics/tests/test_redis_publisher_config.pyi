"""Auto-generated stub for module: test_redis_publisher_config."""
from typing import Any

# Classes
class TestClientConstruction:
    def test_connect_failure_degrades_to_a_no_op(self: Any) -> Any:
        """
        Publishing must never take the pipeline down with it.
        """
        ...

    def test_falls_back_to_a_direct_client_without_sentinel(self: Any) -> Any: ...

    def test_target_description_names_sentinel(self: Any) -> Any: ...

    def test_uses_sentinel_when_configured(self: Any) -> Any:
        """
        Sentinel resolves the CURRENT master and follows failover; a fixed
                host cannot, and on an HA Service it is a replica half the time.
        """
        ...

class TestConfigSeam:
    # PostProcRunner -> PostProcessor -> publisher. This chain was severed:
    #     the correctly-resolved config existed upstream but was never forwarded.

    def test_post_processor_forwards_redis_config(self: Any) -> Any: ...

    def test_post_processor_without_config_still_works(self: Any) -> Any: ...

class TestConnectionResolution:
    def test_defaults_to_localhost_when_nothing_is_configured(self: Any) -> Any:
        """
        The original bug's starting point, kept explicit so it stays visible.
        """
        ...

    def test_env_supplies_the_connection(self: Any, monkeypatch: Any) -> Any: ...

    def test_explicit_config_beats_the_environment(self: Any, monkeypatch: Any) -> Any:
        """
        A caller that already resolved the topology must not be overridden.
        """
        ...

    def test_sentinel_from_config(self: Any) -> Any: ...

    def test_sentinel_from_env(self: Any, monkeypatch: Any) -> Any: ...

class TestPy38Compatibility:
    # The Orin image runs Python 3.8. A PEP 604 union in a module WITHOUT
    #     `from __future__ import annotations` is evaluated at import and raises
    #     TypeError there — that is exactly what crashed matrice_common on Orin.
    #     ruff's target-version is py311 while requires-python is >=3.8, so it will
    #     keep suggesting the unsafe form; this test is the guard.

    def test_no_pep604_unions_without_future_import(self: Any, module_path: Any) -> Any: ...

class TestSentinelHostParsing:
    # The three shapes the value actually arrives in.

    def test_bad_entries_are_skipped_not_fatal(self: Any) -> Any: ...

    def test_comma_separated_string_from_env(self: Any) -> Any: ...

    def test_empty_yields_no_hosts(self: Any, empty: Any) -> Any: ...

    def test_explicit_ports_win_over_the_default(self: Any) -> Any: ...

    def test_list_of_pairs_passes_through(self: Any) -> Any: ...

    def test_list_of_strings(self: Any) -> Any: ...

