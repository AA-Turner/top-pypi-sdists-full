"""Tests for connector_sdk_types.oai.modules.rate_limiting_types."""

import pytest
from connector_sdk_types.generated import RateLimitStateSnapshotSource
from connector_sdk_types.oai.modules.rate_limiting_types import (
    LIMIT_CEILING,
    MAXIMUM_RETRIES,
    REQUESTS_PER_WINDOW_CEILING,
    STATIC_RATE_LIMIT_DICTIONARY,
    RateLimitConfig,
    RateLimitConfigBase,
    RateLimitExtractor,
    RateLimitExtractorResponse,
    RateLimitPolicySource,
    RateLimitStrategy,
)


class TestConstants:
    def test_requests_per_window_ceiling(self):
        assert REQUESTS_PER_WINDOW_CEILING == 0.2

    def test_limit_ceiling(self):
        assert LIMIT_CEILING == 0.2

    def test_maximum_retries(self):
        assert MAXIMUM_RETRIES == 5

    def test_static_rate_limit_dictionary_contains_keywords(self):
        assert "rate limit exceeded" in STATIC_RATE_LIMIT_DICTIONARY
        assert "too many requests" in STATIC_RATE_LIMIT_DICTIONARY
        assert len(STATIC_RATE_LIMIT_DICTIONARY) > 0


class TestRateLimitStateSnapshotSource:
    def test_constants(self):
        assert RateLimitStateSnapshotSource.API_HEADERS == "api_headers"
        assert RateLimitStateSnapshotSource.SDK_COUNTER == "sdk_counter"


class TestRateLimitPolicySource:
    def test_all_values_present(self):
        assert RateLimitPolicySource.CALLER == "caller"
        assert RateLimitPolicySource.CAPABILITY == "capability"
        assert RateLimitPolicySource.CONNECTOR == "connector"
        assert RateLimitPolicySource.SDK == "sdk"

    def test_is_str_enum(self):
        assert isinstance(RateLimitPolicySource.CALLER, str)


class TestRateLimitStrategy:
    def test_fixed(self):
        assert RateLimitStrategy.FIXED == "fixed"

    def test_adaptive(self):
        assert RateLimitStrategy.ADAPTIVE == "adaptive"

    def test_is_str_enum(self):
        assert isinstance(RateLimitStrategy.FIXED, str)


class TestRateLimitExtractorResponse:
    def test_required_fields(self):
        r = RateLimitExtractorResponse(remaining=10, limit=100)
        assert r.remaining == 10
        assert r.limit == 100

    def test_optional_fields_default_to_none(self):
        r = RateLimitExtractorResponse(remaining=5, limit=50)
        assert r.reset is None
        assert r.window_seconds is None
        assert r.observed is None
        assert r.requests_per_window is None

    def test_all_optional_fields_can_be_set(self):
        r = RateLimitExtractorResponse(
            remaining=5,
            limit=50,
            reset=1234567890,
            window_seconds=60,
            observed="10",
            requests_per_window=40,
        )
        assert r.reset == 1234567890
        assert r.window_seconds == 60
        assert r.observed == "10"
        assert r.requests_per_window == 40


class TestRateLimitExtractor:
    def test_is_abstract(self):
        with pytest.raises(TypeError):
            RateLimitExtractor()  # type: ignore[abstract]

    def test_concrete_subclass_works(self):
        import httpx

        class ConcreteExtractor(RateLimitExtractor):
            def extract(self, response: httpx.Response) -> RateLimitExtractorResponse:
                return RateLimitExtractorResponse(remaining=5, limit=10)

        extractor = ConcreteExtractor()
        resp = httpx.Response(200)
        result = extractor.extract(resp)
        assert result.remaining == 5
        assert result.limit == 10


class TestRateLimitConfigBase:
    def test_required_fields(self):
        config = RateLimitConfigBase(requests_per_window=30, window_seconds=60)
        assert config.requests_per_window == 30
        assert config.window_seconds == 60

    def test_default_values(self):
        config = RateLimitConfigBase(requests_per_window=30, window_seconds=60)
        assert config.maximum_retries == MAXIMUM_RETRIES
        assert config.strategy == RateLimitStrategy.FIXED
        assert config.max_batch_size is None
        assert config.initial_delay == 0.0
        assert config.max_delay == 60.0
        assert config.backoff_factor == 1.5
        assert config.max_concurrent == 1
        assert config.mode is None

    def test_strategy_override(self):
        config = RateLimitConfigBase(
            requests_per_window=10, window_seconds=30, strategy=RateLimitStrategy.ADAPTIVE
        )
        assert config.strategy == RateLimitStrategy.ADAPTIVE


class TestRateLimitConfig:
    def test_default_factory(self):
        config = RateLimitConfig.default("myapp")
        assert config.config_id == "myapp"
        assert config.requests_per_window == 30
        assert config.window_seconds == 60
        assert config.strategy == RateLimitStrategy.FIXED
        assert config.max_batch_size == 15
        assert config.max_concurrent == 1

    def test_explicit_construction(self):
        config = RateLimitConfig(config_id="test", requests_per_window=10, window_seconds=60)
        assert config.config_id == "test"
        assert config.rate_limit_extractor is None
        assert config.rate_limit_error_check is None

    def test_overwrite_updates_existing_field(self):
        config = RateLimitConfig.default("app")
        config.overwrite(requests_per_window=50)
        assert config.requests_per_window == 50

    def test_overwrite_multiple_fields(self):
        config = RateLimitConfig.default("app")
        config.overwrite(window_seconds=120, max_concurrent=5)
        assert config.window_seconds == 120
        assert config.max_concurrent == 5

    def test_overwrite_ignores_unknown_fields(self):
        config = RateLimitConfig.default("app")
        original_rps = config.requests_per_window
        config.overwrite(nonexistent_field="value")
        assert config.requests_per_window == original_rps

    def test_rate_limit_extractor_callable(self):
        import httpx

        def extractor(resp: httpx.Response) -> RateLimitExtractorResponse:
            return RateLimitExtractorResponse(remaining=1, limit=10)

        config = RateLimitConfig(
            config_id="test",
            requests_per_window=10,
            window_seconds=60,
            rate_limit_extractor=extractor,
        )
        assert config.rate_limit_extractor is extractor

    def test_rate_limit_error_check_callable(self):
        def checker(e: Exception) -> bool:
            return "rate" in str(e).lower()

        config = RateLimitConfig(
            config_id="test",
            requests_per_window=10,
            window_seconds=60,
            rate_limit_error_check=checker,
        )
        assert config.rate_limit_error_check is checker

    def test_config_id_is_required(self):
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            RateLimitConfig(requests_per_window=10, window_seconds=60)  # type: ignore[call-arg]
