"""Tests for the RateLimiter class."""

import time
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from connector.oai.errors import BudgetExhaustedError, RateLimitError, UpstreamError
from connector.utils.rate_limit_context import RATE_LIMIT_CONTEXT, RateLimitExecutionContext
from connector.utils.rate_limiting import RateLimiter
from connector_sdk_types.generated import (
    RateLimitMode,
    RateLimitStateSnapshot,
    StandardCapabilityName,
)
from connector_sdk_types.oai.modules.rate_limiting_types import (
    FIXED_DECAY_FLOOR,
    RateLimitConfig,
    RateLimitExtractorResponse,
    RateLimitStrategy,
)
from gql.transport.exceptions import TransportQueryError, TransportServerError


@pytest.fixture
def basic_config() -> RateLimitConfig:
    return RateLimitConfig(
        config_id="test",
        requests_per_window=5,
        window_seconds=10,
        strategy=RateLimitStrategy.FIXED,
        maximum_retries=2,
        max_delay=30.0,
        backoff_factor=1.5,
        initial_delay=0.0,
    )


def _http_status_error(status_code: int, text: str = "error") -> httpx.HTTPStatusError:
    resp = httpx.Response(status_code, text=text)
    resp._request = httpx.Request("GET", "https://example.com")
    return httpx.HTTPStatusError(str(status_code), request=resp._request, response=resp)


# is_transient_error


class TestIsTransientError:
    @pytest.mark.parametrize("status_code", [408, 502, 503, 504])
    def test_transient_http_status_codes(self, status_code: int) -> None:
        assert RateLimiter.is_transient_error(_http_status_error(status_code)) is True

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 429, 500, 501])
    def test_non_transient_http_status_codes(self, status_code: int) -> None:
        assert RateLimiter.is_transient_error(_http_status_error(status_code)) is False

    def test_connect_timeout(self) -> None:
        assert RateLimiter.is_transient_error(httpx.ConnectTimeout("timeout")) is True

    def test_read_timeout(self) -> None:
        assert RateLimiter.is_transient_error(httpx.ReadTimeout("timeout")) is True

    def test_remote_protocol_error(self) -> None:
        assert RateLimiter.is_transient_error(httpx.RemoteProtocolError("proto error")) is True

    def test_generic_exception_is_not_transient(self) -> None:
        assert RateLimiter.is_transient_error(Exception("boom")) is False

    def test_value_error_is_not_transient(self) -> None:
        assert RateLimiter.is_transient_error(ValueError("bad value")) is False

    @pytest.mark.parametrize("code", [408, 502, 503, 504])
    def test_transient_transport_server_error_codes(self, code: int) -> None:
        assert RateLimiter.is_transient_error(TransportServerError("error", code=code)) is True

    @pytest.mark.parametrize("code", [400, 401, 403, 404, 429, 500])
    def test_non_transient_transport_server_error_codes(self, code: int) -> None:
        assert RateLimiter.is_transient_error(TransportServerError("error", code=code)) is False

    def test_transport_server_error_without_code_is_not_transient(self) -> None:
        assert RateLimiter.is_transient_error(TransportServerError("error")) is False


# ── _effective_mode ────────────────────────────────────────────────────────────


class TestEffectiveMode:
    def test_none_mode_defaults_to_enforce(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config.model_copy(update={"mode": None}))
        assert limiter._effective_mode == RateLimitMode.ENFORCE

    @pytest.mark.parametrize("mode", list(RateLimitMode))
    def test_explicit_mode_is_returned(
        self, basic_config: RateLimitConfig, mode: RateLimitMode
    ) -> None:
        limiter = RateLimiter(basic_config.model_copy(update={"mode": mode}))
        assert limiter._effective_mode == mode


# ── _wait_time_needed with RETRY_ONLY ─────────────────────────────────────────


class TestWaitTimeNeeded:
    def test_retry_only_returns_zero_even_when_window_full(
        self, basic_config: RateLimitConfig
    ) -> None:
        config = basic_config.model_copy(
            update={"mode": RateLimitMode.RETRY_ONLY, "requests_per_window": 1}
        )
        limiter = RateLimiter(config)
        limiter.request_times = [time.time()]  # window exhausted
        assert limiter._wait_time_needed() == 0.0

    def test_enforce_returns_positive_when_window_exhausted(
        self, basic_config: RateLimitConfig
    ) -> None:
        config = basic_config.model_copy(
            update={"mode": RateLimitMode.ENFORCE, "requests_per_window": 1}
        )
        limiter = RateLimiter(config)
        limiter.request_times = [time.time()]
        assert limiter._wait_time_needed() > 0.0


# check_deadline / get_deadline


class TestCheckDeadline:
    def _ctx(self, seconds_until_deadline: float) -> RateLimitExecutionContext:
        return RateLimitExecutionContext(
            capability_name=StandardCapabilityName.LIST_ACCOUNTS,
            capability_level="read",
            caller_override_mode=None,
            deadline=time.time() + seconds_until_deadline,
        )

    def test_no_context_is_noop(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)
        token = RATE_LIMIT_CONTEXT.set(None)
        try:
            limiter._check_deadline(99999.0)  # huge sleep, no raise without context
        finally:
            RATE_LIMIT_CONTEXT.reset(token)

    def test_raises_when_sleep_exceeds_deadline(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)
        token = RATE_LIMIT_CONTEXT.set(self._ctx(seconds_until_deadline=5.0))
        try:
            with pytest.raises(BudgetExhaustedError):
                limiter._check_deadline(60.0)  # would overshoot 5s deadline
        finally:
            RATE_LIMIT_CONTEXT.reset(token)

    def test_no_raise_when_sleep_within_deadline(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)
        token = RATE_LIMIT_CONTEXT.set(self._ctx(seconds_until_deadline=120.0))
        try:
            limiter._check_deadline(1.0)  # fits easily
        finally:
            RATE_LIMIT_CONTEXT.reset(token)

    def test_budget_exhausted_error_contains_retry_after_seconds(
        self, basic_config: RateLimitConfig
    ) -> None:
        limiter = RateLimiter(basic_config)
        token = RATE_LIMIT_CONTEXT.set(self._ctx(seconds_until_deadline=5.0))
        try:
            with pytest.raises(BudgetExhaustedError) as exc_info:
                limiter._check_deadline(30.0)
            assert exc_info.value.retry_after_seconds is not None
            assert exc_info.value.retry_after_seconds == 30
        finally:
            RATE_LIMIT_CONTEXT.reset(token)


class TestCheckDeadlineExpired:
    def _ctx(self, seconds_until_deadline: float) -> RateLimitExecutionContext:
        return RateLimitExecutionContext(
            capability_name=StandardCapabilityName.LIST_ACCOUNTS,
            capability_level="read",
            caller_override_mode=None,
            deadline=time.time() + seconds_until_deadline,
        )

    def test_no_context_is_noop(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)
        token = RATE_LIMIT_CONTEXT.set(None)
        try:
            limiter._check_deadline_expired()  # no raise without context
        finally:
            RATE_LIMIT_CONTEXT.reset(token)

    def test_no_raise_when_deadline_in_future(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)
        token = RATE_LIMIT_CONTEXT.set(self._ctx(seconds_until_deadline=60.0))
        try:
            limiter._check_deadline_expired()
        finally:
            RATE_LIMIT_CONTEXT.reset(token)

    def test_raises_when_deadline_passed(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)
        token = RATE_LIMIT_CONTEXT.set(self._ctx(seconds_until_deadline=-1.0))
        try:
            with pytest.raises(BudgetExhaustedError) as exc_info:
                limiter._check_deadline_expired()
            assert exc_info.value.retry_after_seconds == 0
        finally:
            RATE_LIMIT_CONTEXT.reset(token)

    async def test_raised_without_rate_limiting_sleep(self, basic_config: RateLimitConfig) -> None:
        """BudgetExhaustedError raised even when no rate limiting wait is needed."""
        limiter = RateLimiter(basic_config)
        token = RATE_LIMIT_CONTEXT.set(self._ctx(seconds_until_deadline=-1.0))
        try:
            with pytest.raises(BudgetExhaustedError):
                await limiter.execute_requests([object()], AsyncMock())
        finally:
            RATE_LIMIT_CONTEXT.reset(token)


# seed_from_state


class TestSeedFromState:
    def test_applies_non_none_fields(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)
        limiter.seed_from_state(
            RateLimitStateSnapshot(limit=20, window_seconds=30, current_delay=5)
        )
        assert limiter.config.requests_per_window == 20
        assert limiter.config.window_seconds == 30
        assert limiter.current_delay == 5.0

    def test_all_none_state_leaves_config_unchanged(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)
        original_rpw = limiter.config.requests_per_window
        original_ws = limiter.config.window_seconds
        original_delay = limiter.current_delay

        limiter.seed_from_state(RateLimitStateSnapshot())

        assert limiter.config.requests_per_window == original_rpw
        assert limiter.config.window_seconds == original_ws
        assert limiter.current_delay == original_delay

    def test_partial_state_only_applies_set_fields(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)
        original_ws = limiter.config.window_seconds
        limiter.seed_from_state(RateLimitStateSnapshot(limit=99))
        assert limiter.config.requests_per_window == 99
        assert limiter.config.window_seconds == original_ws  # unchanged

    def test_remaining_prefills_request_times_no_reset(self, basic_config: RateLimitConfig) -> None:
        # No reset info: falls back to time.time() entries
        limiter = RateLimiter(basic_config)
        limiter.seed_from_state(RateLimitStateSnapshot(limit=10, remaining=3))
        assert len(limiter.request_times) == 7

    def test_remaining_with_future_reset_anchors_entries_at_window_start(
        self, basic_config: RateLimitConfig
    ) -> None:
        limiter = RateLimiter(basic_config)
        future_reset = int(time.time()) + 20
        limiter.seed_from_state(
            RateLimitStateSnapshot(limit=10, remaining=3, reset=future_reset, window_seconds=60)
        )
        assert len(limiter.request_times) == 7
        expected_entry_time = future_reset - 60
        assert all(t == expected_entry_time for t in limiter.request_times)

    def test_remaining_with_past_reset_leaves_request_times_empty(
        self, basic_config: RateLimitConfig
    ) -> None:
        # Window has already turned over — stale remaining should be ignored
        limiter = RateLimiter(basic_config)
        past_reset = int(time.time()) - 5
        limiter.seed_from_state(
            RateLimitStateSnapshot(limit=10, remaining=0, reset=past_reset, window_seconds=60)
        )
        assert len(limiter.request_times) == 0

    def test_remaining_equal_to_limit_leaves_request_times_empty(
        self, basic_config: RateLimitConfig
    ) -> None:
        limiter = RateLimiter(basic_config)
        limiter.seed_from_state(RateLimitStateSnapshot(limit=10, remaining=10))
        assert len(limiter.request_times) == 0

    def test_remaining_without_limit_leaves_request_times_empty(
        self, basic_config: RateLimitConfig
    ) -> None:
        limiter = RateLimiter(basic_config)
        limiter.seed_from_state(RateLimitStateSnapshot(remaining=3))
        assert len(limiter.request_times) == 0

    @pytest.fixture(autouse=True)
    def suppress_rate_limit_state_passthrough(self):
        """Override the SDK plugin fixture so get_current_state runs for real."""
        yield

    def test_seeded_remaining_reflected_in_get_current_state(
        self, basic_config: RateLimitConfig
    ) -> None:
        limiter = RateLimiter(basic_config)
        limiter.seed_from_state(RateLimitStateSnapshot(limit=10, window_seconds=60, remaining=3))
        state = limiter.get_current_state()
        assert state.remaining == 3

    def test_seeded_reset_stored_on_instance(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)
        limiter.seed_from_state(RateLimitStateSnapshot(reset=1234567890))
        assert limiter.last_reset == 1234567890.0

    def test_seeded_reset_reflected_in_get_current_state(
        self, basic_config: RateLimitConfig
    ) -> None:
        basic_config.strategy = RateLimitStrategy.ADAPTIVE
        limiter = RateLimiter(basic_config)
        limiter.seed_from_state(RateLimitStateSnapshot(reset=1234567890))
        state = limiter.get_current_state()
        assert state.reset == 1234567890


# get_current_state


class TestGetCurrentState:
    """Tests that call get_current_state directly, must un-suppress the autouse plugin patch."""

    @pytest.fixture(autouse=True)
    def suppress_rate_limit_state_passthrough(self):
        """Override the SDK plugin fixture so the real get_current_state runs."""
        yield  # no patch

    def test_returns_snapshot_with_correct_limit_and_window(
        self, basic_config: RateLimitConfig
    ) -> None:
        limiter = RateLimiter(basic_config)
        state = limiter.get_current_state()
        assert state.limit == basic_config.requests_per_window
        assert state.window_seconds == basic_config.window_seconds

    def test_remaining_equals_limit_when_no_requests_made(
        self, basic_config: RateLimitConfig
    ) -> None:
        limiter = RateLimiter(basic_config)
        state = limiter.get_current_state()
        assert state.remaining == basic_config.requests_per_window

    def test_remaining_decrements_with_recorded_requests(
        self, basic_config: RateLimitConfig
    ) -> None:
        limiter = RateLimiter(basic_config)
        now = time.time()
        limiter.request_times = [now - 1, now - 2, now - 3]
        state = limiter.get_current_state()
        assert state.remaining == basic_config.requests_per_window - 3

    def test_remaining_clamped_to_zero(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)
        now = time.time()
        limiter.request_times = [now - i * 0.1 for i in range(basic_config.requests_per_window + 5)]
        state = limiter.get_current_state()
        assert state.remaining == 0

    def test_current_delay_rounded(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)
        limiter.current_delay = 7.8
        state = limiter.get_current_state()
        assert state.current_delay == 8  # round(7.8) == 8

    def test_reset_is_none_when_no_requests_made_fixed(self, basic_config: RateLimitConfig) -> None:
        state = RateLimiter(basic_config).get_current_state()
        assert state.reset is None

    def test_reset_is_oldest_request_plus_window_for_fixed(
        self, basic_config: RateLimitConfig
    ) -> None:
        limiter = RateLimiter(basic_config)
        oldest = time.time() - 3
        limiter.request_times = [oldest, oldest + 1, oldest + 2]
        state = limiter.get_current_state()
        assert state.reset == int(oldest + basic_config.window_seconds)

    def test_reset_comes_from_last_reset_for_adaptive(self, basic_config: RateLimitConfig) -> None:
        basic_config.strategy = RateLimitStrategy.ADAPTIVE
        limiter = RateLimiter(basic_config)
        limiter.last_reset = 9999999.0
        state = limiter.get_current_state()
        assert state.reset == 9999999

    def test_reset_is_none_for_adaptive_without_extractor_data(
        self, basic_config: RateLimitConfig
    ) -> None:
        basic_config.strategy = RateLimitStrategy.ADAPTIVE
        state = RateLimiter(basic_config).get_current_state()
        assert state.reset is None


# _handle_rate_limit_exceeded mode behaviour


class TestHandleRateLimitExceededMode:
    def test_enforce_fixed_jumps_delay_to_window_seconds_then_applies_backoff(
        self, basic_config: RateLimitConfig
    ) -> None:
        config = basic_config.model_copy(
            update={
                "mode": RateLimitMode.ENFORCE,
                "strategy": RateLimitStrategy.FIXED,
                "window_seconds": 10,
                "backoff_factor": 2.0,
                "max_delay": 100.0,
            }
        )
        limiter = RateLimiter(config)
        limiter.current_delay = 0.0
        limiter._handle_rate_limit_exceeded()
        # jump to 10 → apply *2 → 20
        assert abs(limiter.current_delay - 20.0) < 0.01

    def test_retry_only_does_not_jump_to_window_seconds(
        self, basic_config: RateLimitConfig
    ) -> None:
        config = basic_config.model_copy(
            update={
                "mode": RateLimitMode.RETRY_ONLY,
                "strategy": RateLimitStrategy.FIXED,
                "window_seconds": 10,
                "backoff_factor": 2.0,
                "max_delay": 100.0,
            }
        )
        limiter = RateLimiter(config)
        limiter.current_delay = 1.0
        limiter._handle_rate_limit_exceeded()
        # Should NOT jump to 10s, just apply backoff: 1.0 * 2.0 = 2.0
        assert abs(limiter.current_delay - 2.0) < 0.01
        assert limiter.current_delay < 10.0  # never jumped to window_seconds


# transient error retry logic


class TestTransientErrorRetry:
    async def test_transient_error_retried_and_raises_upstream_error(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """After exhausting transient retries, UpstreamError is raised."""
        config = basic_config.model_copy(update={"maximum_retries": 1})
        limiter = RateLimiter(config)
        call_count = {"n": 0}

        async def always_502(_: str) -> str:
            call_count["n"] += 1
            raise _http_status_error(502)

        monkeypatch.setattr("asyncio.sleep", AsyncMock())

        with pytest.raises(UpstreamError) as exc_info:
            await limiter._execute_single_request("req", always_502)

        # 1 initial attempt + 1 retry = 2 total
        assert call_count["n"] == 2
        assert exc_info.value.retry_after_seconds is not None
        assert exc_info.value.retry_after_seconds == 15

    async def test_transient_retries_independent_of_rate_limit_retries(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Transient errors consume a separate counter from rate-limit errors."""
        config = basic_config.model_copy(update={"maximum_retries": 2})
        limiter = RateLimiter(config)
        call_count = {"n": 0}

        async def two_503s_then_success(_: str) -> str:
            call_count["n"] += 1
            if call_count["n"] <= 2:
                raise _http_status_error(503)
            return "ok"

        monkeypatch.setattr("asyncio.sleep", AsyncMock())
        result = await limiter._execute_single_request("req", two_503s_then_success)
        assert result == "ok"
        assert call_count["n"] == 3

    async def test_connect_timeout_is_retried(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """httpx.ConnectTimeout triggers transient retry, not immediate raise."""
        config = basic_config.model_copy(update={"maximum_retries": 1})
        limiter = RateLimiter(config)
        call_count = {"n": 0}

        async def timeout_then_success(_: str) -> str:
            call_count["n"] += 1
            if call_count["n"] == 1:
                raise httpx.ConnectTimeout("timeout")
            return "ok"

        monkeypatch.setattr("asyncio.sleep", AsyncMock())
        result = await limiter._execute_single_request("req", timeout_then_success)
        assert result == "ok"

    async def test_check_deadline_called_before_transient_retry_sleep(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """BudgetExhaustedError raised before sleeping past deadline on transient retry."""
        config = basic_config.model_copy(update={"maximum_retries": 2})
        limiter = RateLimiter(config)
        # Set current_delay high enough to exceed a short deadline
        limiter.current_delay = 60.0

        ctx = RateLimitExecutionContext(
            capability_name=StandardCapabilityName.LIST_ACCOUNTS,
            capability_level="write",
            caller_override_mode=None,
            deadline=time.time() + 5.0,
        )
        token = RATE_LIMIT_CONTEXT.set(ctx)
        try:

            async def always_502(_: str) -> str:
                raise _http_status_error(502)

            monkeypatch.setattr("asyncio.sleep", AsyncMock())
            with pytest.raises(BudgetExhaustedError):
                await limiter._execute_single_request("req", always_502)
        finally:
            RATE_LIMIT_CONTEXT.reset(token)


# RETRY_ONLY skips inter-batch sleep


class TestRetryOnlyInterBatchDelay:
    async def test_retry_only_skips_inter_batch_delay(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        config = RateLimitConfig(
            config_id="test",
            requests_per_window=2,
            window_seconds=10,
            strategy=RateLimitStrategy.FIXED,
            max_batch_size=2,
            mode=RateLimitMode.RETRY_ONLY,
        )
        limiter = RateLimiter(config)
        limiter.current_delay = 5.0

        sleep_calls: list[float] = []
        monkeypatch.setattr("asyncio.sleep", AsyncMock(side_effect=lambda s: sleep_calls.append(s)))

        async def handler(req: str) -> str:
            return req

        await limiter._execute_requests_sequential(["a", "b", "c", "d"], handler)

        inter_batch_sleeps = [s for s in sleep_calls if abs(s - 5.0) < 0.1]
        assert len(inter_batch_sleeps) == 0, f"Expected no inter-batch sleeps, got {sleep_calls}"

    async def test_enforce_mode_applies_inter_batch_delay(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        config = RateLimitConfig(
            config_id="test",
            requests_per_window=2,
            window_seconds=10,
            strategy=RateLimitStrategy.FIXED,
            max_batch_size=2,
            mode=RateLimitMode.ENFORCE,
        )
        limiter = RateLimiter(config)
        limiter.current_delay = 5.0

        sleep_calls: list[float] = []
        monkeypatch.setattr("asyncio.sleep", AsyncMock(side_effect=lambda s: sleep_calls.append(s)))

        async def handler(req: str) -> str:
            return req

        with patch.object(limiter, "_wait_time_needed", return_value=0.0):
            await limiter._execute_requests_sequential(["a", "b", "c", "d"], handler)

        expected_sleep = 5.0 / config.backoff_factor
        inter_batch_sleeps = [s for s in sleep_calls if abs(s - expected_sleep) < 0.1]
        assert (
            inter_batch_sleeps[0] == expected_sleep
        ), f"Expected inter-batch sleep of ~{expected_sleep:.2f}s, got {sleep_calls}"


# is_rate_limit_error (direct unit tests)


class TestIsRateLimitError:
    def test_429_returns_true(self) -> None:
        assert RateLimiter.is_rate_limit_error(_http_status_error(429)) is True

    def test_429_takes_early_return_path(self) -> None:
        """429 short-circuits before checking response text."""
        # Give it a body that does NOT contain any keyword, still True because of status code only
        resp = httpx.Response(429, text="some unrelated error body")
        resp._request = httpx.Request("GET", "https://example.com")
        err = httpx.HTTPStatusError("429", request=resp._request, response=resp)
        assert RateLimiter.is_rate_limit_error(err) is True

    @pytest.mark.parametrize(
        "keyword",
        [
            "rate limit exceeded",
            "too many requests",
            "quota exceeded",
            "exceeded your rate limit",
            "request limit reached",
        ],
    )
    def test_rate_limit_keyword_in_non_429_body_returns_true(self, keyword: str) -> None:
        resp = httpx.Response(400, text=f"Error: {keyword}")
        resp._request = httpx.Request("GET", "https://example.com")
        err = httpx.HTTPStatusError("400", request=resp._request, response=resp)
        assert RateLimiter.is_rate_limit_error(err) is True

    def test_non_rate_limit_400_returns_false(self) -> None:
        assert RateLimiter.is_rate_limit_error(_http_status_error(400, "bad request")) is False

    def test_non_httpstatus_error_returns_false(self) -> None:
        assert RateLimiter.is_rate_limit_error(ValueError("oops")) is False

    def test_response_text_read_failure_returns_false(self) -> None:
        """When response.text raises, the except branch catches it and returns False."""

        class UnreadableResponse:
            status_code = 400
            _request = httpx.Request("GET", "https://example.com")

            @property
            def text(self):
                raise RuntimeError("can't read")

        err = httpx.HTTPStatusError(
            "400", request=UnreadableResponse._request, response=UnreadableResponse()
        )
        assert RateLimiter.is_rate_limit_error(err) is False

    def test_transport_server_error_429_returns_true(self) -> None:
        assert (
            RateLimiter.is_rate_limit_error(TransportServerError("Too Many Requests", code=429))
            is True
        )

    def test_transport_server_error_non_429_returns_false(self) -> None:
        assert (
            RateLimiter.is_rate_limit_error(TransportServerError("Bad Request", code=400)) is False
        )

    def test_transport_server_error_without_code_returns_false(self) -> None:
        assert RateLimiter.is_rate_limit_error(TransportServerError("error")) is False

    @pytest.mark.parametrize(
        "keyword",
        [
            "rate limit exceeded",
            "too many requests",
            "quota exceeded",
            "exceeded your rate limit",
            "request limit reached",
        ],
    )
    def test_transport_query_error_with_rate_limit_keyword_returns_true(self, keyword: str) -> None:
        err = TransportQueryError("GraphQL error", errors=[{"message": keyword}])
        assert RateLimiter.is_rate_limit_error(err) is True

    def test_transport_query_error_without_keywords_returns_false(self) -> None:
        err = TransportQueryError("GraphQL error", errors=[{"message": "some unrelated error"}])
        assert RateLimiter.is_rate_limit_error(err) is False

    def test_transport_query_error_without_errors_returns_false(self) -> None:
        err = TransportQueryError("GraphQL error")
        assert RateLimiter.is_rate_limit_error(err) is False


# _update_request_times


class TestUpdateRequestTimes:
    def test_removes_expired_entries(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)
        now = time.time()
        # One recent, one expired (11s ago, window is 10s)
        limiter.request_times = [now - 11.0, now - 1.0]
        limiter._update_request_times()
        assert len(limiter.request_times) == 1

    def test_keeps_all_fresh_entries(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)
        now = time.time()
        limiter.request_times = [now - 1.0, now - 5.0, now - 9.0]
        limiter._update_request_times()
        assert len(limiter.request_times) == 3

    def test_clears_all_when_all_expired(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)
        now = time.time()
        limiter.request_times = [now - 20.0, now - 30.0]
        limiter._update_request_times()
        assert limiter.request_times == []


# _can_make_request


class TestCanMakeRequest:
    def test_returns_true_when_under_limit(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)  # requests_per_window=5
        now = time.time()
        limiter.request_times = [now - 1.0, now - 2.0]  # 2 of 5 used
        assert limiter._can_make_request() is True

    def test_returns_false_when_at_limit(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)  # requests_per_window=5
        now = time.time()
        limiter.request_times = [now - i * 0.5 for i in range(5)]  # exactly 5 in window
        assert limiter._can_make_request() is False

    def test_returns_true_after_old_requests_expire(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """After advancing time past window, old requests prune out and the slot opens."""
        current_time = 1000.0
        monkeypatch.setattr("time.time", lambda: current_time)
        limiter = RateLimiter(basic_config)
        limiter.request_times = [995.0] * 5  # 5 requests 5s ago, window=10s → still in window

        assert limiter._can_make_request() is False

        current_time = 1006.0  # advance past window
        assert limiter._can_make_request() is True


# _wait_time_needed edge case


class TestWaitTimeNeededEdgeCases:
    def test_returns_zero_when_all_requests_expired_mid_call(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Covers line 114: after second _update_request_times call, list is empty."""
        # Fill the window with near-expired entries
        call_count = {"n": 0}

        def mock_time() -> float:
            call_count["n"] += 1
            # First call (in _can_make_request): entries still in window
            # Second call (in _wait_time_needed body): entries have just expired
            if call_count["n"] <= 2:
                return 1000.0
            return 1011.0  # > window_seconds away from the recorded times

        monkeypatch.setattr("time.time", mock_time)
        limiter = RateLimiter(basic_config)
        # Records from 1s ago, in window at t=1000 but expired at t=1011
        limiter.request_times = [990.0] * 5  # 10s ago at t=1000, expired at t=1001+

        # After advancing time past window, _update_request_times returns []
        result = limiter._wait_time_needed()
        assert result == 0.0


# _update_rate_limits ADAPTIVE strategy


class TestUpdateRateLimitsAdaptive:
    def _adaptive_config(self, basic_config: RateLimitConfig, extractor) -> RateLimitConfig:
        return basic_config.model_copy(
            update={
                "strategy": RateLimitStrategy.ADAPTIVE,
                "rate_limit_extractor": extractor,
                "initial_delay": 1.0,
                "backoff_factor": 2.0,
            }
        )

    def test_fixed_strategy_is_noop(self, basic_config: RateLimitConfig) -> None:
        """_update_rate_limits does nothing when strategy is FIXED."""
        limiter = RateLimiter(basic_config)
        original_delay = limiter.current_delay
        limiter._update_rate_limits(httpx.Response(200))
        assert limiter.current_delay == original_delay

    def test_adaptive_no_extractor_is_noop(self, basic_config: RateLimitConfig) -> None:
        config = basic_config.model_copy(update={"strategy": RateLimitStrategy.ADAPTIVE})
        limiter = RateLimiter(config)
        original_delay = limiter.current_delay
        limiter._update_rate_limits(httpx.Response(200))
        assert limiter.current_delay == original_delay

    def test_adaptive_updates_requests_per_window(self, basic_config: RateLimitConfig) -> None:
        def extractor(_) -> RateLimitExtractorResponse:
            return RateLimitExtractorResponse(remaining=50, limit=50, requests_per_window=50)

        config = self._adaptive_config(basic_config, extractor)
        limiter = RateLimiter(config)
        limiter._update_rate_limits(httpx.Response(200))
        assert limiter.config.requests_per_window == 50

    def test_adaptive_updates_window_seconds(self, basic_config: RateLimitConfig) -> None:
        def extractor(_) -> RateLimitExtractorResponse:
            return RateLimitExtractorResponse(remaining=5, limit=10, window_seconds=30)

        config = self._adaptive_config(basic_config, extractor)
        limiter = RateLimiter(config)
        limiter._update_rate_limits(httpx.Response(200))
        assert limiter.config.window_seconds == 30

    def test_adaptive_uses_reset_time_when_near_limit(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """When remaining < LIMIT_CEILING fraction and reset is soon, delay is set to time_until_reset."""
        now = 1000.0
        monkeypatch.setattr("time.time", lambda: now)
        reset_time = int(now + 5)  # 5 seconds from now

        def extractor(_) -> RateLimitExtractorResponse:
            # remaining=0 < limit*0.2=2, triggers the reset branch
            return RateLimitExtractorResponse(remaining=0, limit=10, reset=reset_time)

        config = self._adaptive_config(basic_config, extractor)
        config = config.model_copy(update={"max_delay": 60.0})
        limiter = RateLimiter(config)
        limiter._update_rate_limits(httpx.Response(200))
        assert abs(limiter.current_delay - 5.0) < 0.5

    def test_adaptive_increases_delay_when_approaching_limit(
        self, basic_config: RateLimitConfig
    ) -> None:
        """remaining below REQUESTS_PER_WINDOW_CEILING → delay increases."""

        def extractor(_) -> RateLimitExtractorResponse:
            # remaining=0 < requests_per_window*0.2 → backoff
            return RateLimitExtractorResponse(remaining=0, limit=10)

        config = self._adaptive_config(basic_config, extractor)
        limiter = RateLimiter(config)
        limiter.current_delay = 2.0
        limiter._update_rate_limits(httpx.Response(200))
        assert limiter.current_delay > 2.0  # increased by backoff

    def test_adaptive_decreases_delay_when_plenty_remaining(
        self, basic_config: RateLimitConfig
    ) -> None:
        """remaining above threshold → delay decreases."""

        def extractor(_) -> RateLimitExtractorResponse:
            # remaining=5 > requests_per_window*0.2=1 → reduce backoff
            return RateLimitExtractorResponse(remaining=5, limit=10)

        config = self._adaptive_config(basic_config, extractor)
        limiter = RateLimiter(config)
        limiter.current_delay = 4.0
        limiter._update_rate_limits(httpx.Response(200))
        assert limiter.current_delay < 4.0  # decreased


# execute_requests


class TestExecuteRequests:
    async def test_empty_list_returns_empty(self, basic_config: RateLimitConfig) -> None:
        limiter = RateLimiter(basic_config)
        result = await limiter.execute_requests([], AsyncMock())
        assert result == []

    async def test_single_request_uses_sequential_path(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """len(requests)==1 → sequential even when max_concurrent>1."""
        config = basic_config.model_copy(update={"max_concurrent": 4})
        limiter = RateLimiter(config)
        monkeypatch.setattr("asyncio.sleep", AsyncMock())

        async def handler(req: str) -> str:
            return req + "_done"

        result = await limiter.execute_requests(["only"], handler)
        assert result == ["only_done"]

    async def test_concurrent_execution_path(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """max_concurrent>1 with multiple requests → gather-based path."""
        config = basic_config.model_copy(update={"max_concurrent": 3})
        limiter = RateLimiter(config)
        monkeypatch.setattr("asyncio.sleep", AsyncMock())

        order: list[str] = []

        async def handler(req: str) -> str:
            order.append(req)
            return req

        result = await limiter.execute_requests(["a", "b", "c"], handler)
        assert sorted(result) == ["a", "b", "c"]

    async def test_concurrent_raises_on_exception(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Non-rate-limit, non-transient exception from concurrent path is re-raised."""
        config = basic_config.model_copy(update={"max_concurrent": 2})
        limiter = RateLimiter(config)
        monkeypatch.setattr("asyncio.sleep", AsyncMock())

        async def handler(req: str) -> str:
            if req == "bad":
                raise ValueError("boom")
            return req

        with pytest.raises(ValueError, match="boom"):
            await limiter.execute_requests(["ok", "bad"], handler)


# _execute_single_request: sync handler and adaptive update from errors


class TestExecuteSingleRequestAdditional:
    async def test_synchronous_handler_supported(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Handler that returns a plain value (not a coroutine) is handled correctly."""
        limiter = RateLimiter(basic_config)
        monkeypatch.setattr("asyncio.sleep", AsyncMock())

        def sync_handler(req: str) -> str:
            return req + "_sync"

        result = await limiter._execute_single_request("hello", sync_handler)
        assert result == "hello_sync"

    async def test_rate_limit_error_triggers_adaptive_update_from_response(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """When a rate limit HTTP error occurs, _update_rate_limits is called with the response."""

        def extractor(resp) -> RateLimitExtractorResponse:
            return RateLimitExtractorResponse(remaining=0, limit=10, requests_per_window=10)

        config = basic_config.model_copy(
            update={
                "strategy": RateLimitStrategy.ADAPTIVE,
                "rate_limit_extractor": extractor,
                "maximum_retries": 1,
            }
        )
        limiter = RateLimiter(config)
        monkeypatch.setattr("asyncio.sleep", AsyncMock())
        call_count = {"n": 0}

        async def handler(req: str) -> str:
            call_count["n"] += 1
            if call_count["n"] == 1:
                raise _http_status_error(429)
            return "ok"

        result = await limiter._execute_single_request("req", handler)
        assert result == "ok"
        # The extractor updated requests_per_window from the 429 response
        assert limiter.config.requests_per_window == 10

    async def test_non_rate_limit_non_transient_error_raises_immediately(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Errors that are neither rate-limit nor transient are re-raised without retry."""
        limiter = RateLimiter(basic_config)
        monkeypatch.setattr("asyncio.sleep", AsyncMock())
        call_count = {"n": 0}

        async def handler(req: str) -> str:
            call_count["n"] += 1
            raise ValueError("unexpected")

        with pytest.raises(ValueError, match="unexpected"):
            await limiter._execute_single_request("req", handler)

        assert call_count["n"] == 1  # no retry

    async def test_rate_limit_exhaustion_raises_rate_limit_error(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """After exhausting rate-limit retries, RateLimitError is raised."""
        config = basic_config.model_copy(update={"maximum_retries": 1})
        limiter = RateLimiter(config)
        monkeypatch.setattr("asyncio.sleep", AsyncMock())

        async def always_429(req: str) -> str:
            raise _http_status_error(429)

        with pytest.raises(RateLimitError):
            await limiter._execute_single_request("req", always_429)


# FIXED strategy current_delay decay


class TestFixedStrategyDelayDecay:
    """current_delay for FIXED strategy should decay after a 429 once window pressure clears."""

    async def test_delay_decays_on_success_when_window_has_capacity(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """After a 429 elevates current_delay, a successful request with window capacity decays it."""
        monkeypatch.setattr("asyncio.sleep", AsyncMock())
        limiter = RateLimiter(basic_config)
        limiter.current_delay = 30.0

        async def success_handler(req: str) -> str:
            return "ok"

        await limiter._execute_single_request("req", success_handler)

        assert limiter.current_delay < 30.0
        assert limiter.current_delay == pytest.approx(30.0 / basic_config.backoff_factor)

    async def test_delay_does_not_decay_when_window_is_full(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Decay is suppressed while the window is at capacity."""
        monkeypatch.setattr("asyncio.sleep", AsyncMock())
        config = basic_config.model_copy(update={"requests_per_window": 2})
        limiter = RateLimiter(config)
        limiter.current_delay = 30.0

        now = time.time()
        limiter.request_times = [now, now]

        async def success_handler(req: str) -> str:
            return "ok"

        await limiter._execute_single_request("req", success_handler)

        assert limiter.current_delay == 30.0

    async def test_delay_decays_to_initial_delay_floor(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Decay never goes below initial_delay."""
        monkeypatch.setattr("asyncio.sleep", AsyncMock())
        config = basic_config.model_copy(update={"initial_delay": 2.0})
        limiter = RateLimiter(config)
        limiter.current_delay = 2.5

        async def success_handler(req: str) -> str:
            return "ok"

        await limiter._execute_single_request("req", success_handler)

        assert limiter.current_delay == pytest.approx(2.0)

    async def test_delay_at_initial_is_not_touched(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """No decay runs when current_delay is already at initial_delay."""
        monkeypatch.setattr("asyncio.sleep", AsyncMock())
        limiter = RateLimiter(basic_config)
        assert limiter.current_delay == basic_config.initial_delay  # 0.0

        async def success_handler(req: str) -> str:
            return "ok"

        await limiter._execute_single_request("req", success_handler)

        assert limiter.current_delay == basic_config.initial_delay

    async def test_delay_snaps_to_initial_delay_below_floor(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """current_delay snaps to initial_delay once decay drops it below FIXED_DECAY_FLOOR."""
        monkeypatch.setattr("asyncio.sleep", AsyncMock())
        limiter = RateLimiter(basic_config)
        limiter.current_delay = FIXED_DECAY_FLOOR * 1.1

        async def success_handler(req: str) -> str:
            return "ok"

        await limiter._execute_single_request("req", success_handler)

        assert limiter.current_delay == basic_config.initial_delay

    async def test_adaptive_strategy_not_affected(
        self, basic_config: RateLimitConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """ADAPTIVE strategy is handled by _update_rate_limits, not the FIXED decay path."""
        monkeypatch.setattr("asyncio.sleep", AsyncMock())

        def extractor(resp) -> RateLimitExtractorResponse:
            return RateLimitExtractorResponse(remaining=10, limit=10)

        config = basic_config.model_copy(
            update={"strategy": RateLimitStrategy.ADAPTIVE, "rate_limit_extractor": extractor}
        )
        limiter = RateLimiter(config)
        limiter.current_delay = 30.0

        async def success_handler(req: str) -> str:
            return "ok"

        await limiter._execute_single_request("req", success_handler)

        # ADAPTIVE decay comes from _update_rate_limits (divided by backoff_factor)
        assert limiter.current_delay == 20.0
