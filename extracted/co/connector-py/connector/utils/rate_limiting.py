"""
Rate limiting utilities for connector SDK.

This module provides classes and functions to handle rate limiting when making
requests to third-party APIs. It supports batching requests, respecting rate limits,
and handling rate limit headers.
"""

import asyncio
import logging
import math
import time
from collections.abc import Callable
from typing import Any, Generic, TypeVar

import httpx
from connector_sdk_types.generated import RateLimitStateSnapshot, RateLimitStateSnapshotSource
from connector_sdk_types.oai.modules.rate_limiting_types import (
    FIXED_DECAY_FLOOR,
    LIMIT_CEILING,
    REQUESTS_PER_WINDOW_CEILING,
    STATIC_RATE_LIMIT_DICTIONARY,
    RateLimitConfig,
    RateLimitMode,
    RateLimitStrategy,
)
from gql.transport.exceptions import TransportQueryError, TransportServerError

from connector.oai.errors import BudgetExhaustedError, RateLimitError, UpstreamError
from connector.utils.rate_limit_context import RATE_LIMIT_CONTEXT

RequestType = TypeVar("RequestType")  # Input request type
ResponseType = TypeVar("ResponseType")  # Response type

logger = logging.getLogger(__name__)


class RateLimiter(Generic[RequestType, ResponseType]):
    """
    Rate limiter for API requests.

    This class helps manage the rate of requests to third-party APIs by batching
    requests, respecting rate limits, and handling rate limit headers.
    """

    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.request_times: list[float] = []
        self.current_delay = config.initial_delay
        self.semaphore = asyncio.Semaphore(config.max_concurrent)
        self.snapshot_source = RateLimitStateSnapshotSource.SDK_COUNTER
        self.last_reset: float | None = None

        # Set default max_batch_size if not provided
        if self.config.max_batch_size is None:
            self.config.max_batch_size = self.config.requests_per_window

    @staticmethod
    def is_transient_error(e: Exception) -> bool:
        """Check if the error is a transient error."""
        # GQL transport errors
        if isinstance(e, TransportServerError) and e.code in (408, 502, 503, 504):
            return True

        # HTTP status/transport errors
        return (
            isinstance(e, httpx.HTTPStatusError)
            and e.response.status_code in (408, 502, 503, 504)
            or isinstance(e, httpx.ConnectTimeout | httpx.ReadTimeout | httpx.RemoteProtocolError)
        )

    @staticmethod
    def is_rate_limit_error(e: Exception) -> bool:
        """Check if the error is a rate limit error."""
        # GQL Transport error
        if isinstance(e, TransportServerError) and e.code == httpx.codes.TOO_MANY_REQUESTS:
            return True

        # Keyword check for GQL (see below for httpx)
        if isinstance(e, TransportQueryError) and e.errors:
            errors_text = str(e.errors).lower()
            if any(kw in errors_text for kw in STATIC_RATE_LIMIT_DICTIONARY):
                return True

        # Simple check for basic HTTP 429 errors
        is_rate_limit_error = (
            isinstance(e, httpx.HTTPStatusError)
            and e.response.status_code == httpx.codes.TOO_MANY_REQUESTS
        )
        if is_rate_limit_error:
            return is_rate_limit_error

        # Check for response text for rate limit keywords if it's an HTTPStatusError
        # This is a fallback for cases where the response is not a 429 but contains rate limit keywords
        if isinstance(e, httpx.HTTPStatusError) and not is_rate_limit_error:
            try:
                response_text = e.response.text.lower()
                is_rate_limit_error = any(
                    keyword in response_text for keyword in STATIC_RATE_LIMIT_DICTIONARY
                )
            except Exception:
                pass

        return is_rate_limit_error

    def _update_request_times(self) -> None:
        """Update the list of request times, removing expired ones."""
        current_time = time.time()
        self.request_times = [
            t for t in self.request_times if current_time - t < self.config.window_seconds
        ]

    def _can_make_request(self) -> bool:
        """Check if a request can be made without exceeding the rate limit."""
        self._update_request_times()
        return len(self.request_times) < self.config.requests_per_window

    @property
    def _effective_mode(self) -> RateLimitMode:
        return self.config.mode or RateLimitMode.ENFORCE

    def _wait_time_needed(self) -> float:
        """Calculate the time to wait before making the next request."""
        if self._effective_mode == RateLimitMode.RETRY_ONLY:
            return 0.0

        if self._can_make_request():
            return 0.0

        self._update_request_times()
        if not self.request_times:
            return 0.0

        oldest_request = min(self.request_times)
        return oldest_request + self.config.window_seconds - time.time()

    def _update_rate_limits(self, response: Any) -> None:
        """
        Update rate limits based on response.
        """
        if (
            self.config.strategy == RateLimitStrategy.ADAPTIVE
            and self.config.rate_limit_extractor is not None
        ):
            rate_limit_info = self.config.rate_limit_extractor(response)

            # Set the proper snapshot source
            self.snapshot_source = RateLimitStateSnapshotSource.API_HEADERS

            # Update the configuration based on the rate limit information
            if rate_limit_info.requests_per_window is not None:
                self.config.requests_per_window = rate_limit_info.requests_per_window

            if rate_limit_info.window_seconds is not None:
                self.config.window_seconds = rate_limit_info.window_seconds

            # If reset time is available, check it
            if rate_limit_info.reset is not None:
                self.last_reset = float(rate_limit_info.reset)
                current_time = time.time()
                time_until_reset = rate_limit_info.reset - current_time

                # If reset is within the max delay, adjust the delay
                if (
                    time_until_reset > 0
                    and time_until_reset < self.config.max_delay
                    and rate_limit_info.remaining < rate_limit_info.limit * LIMIT_CEILING
                ):
                    self.current_delay = time_until_reset
                    return

            # If we're approaching the limit, increase the delay
            if (
                rate_limit_info.remaining
                < self.config.requests_per_window * REQUESTS_PER_WINDOW_CEILING
            ):
                self.current_delay = min(
                    self.current_delay * self.config.backoff_factor, self.config.max_delay
                )
            else:
                # If we're not close to the limit, reduce the delay
                self.current_delay = max(
                    self.current_delay / self.config.backoff_factor, self.config.initial_delay
                )

            self.debug_log(
                f"Updated rate limits: {self.config.requests_per_window} requests per {self.config.window_seconds} seconds, current delay: {self.current_delay}"
            )

    def _handle_rate_limit_exceeded(self) -> None:
        """Handle the case when rate limit is exceeded."""
        if (
            self._effective_mode == RateLimitMode.ENFORCE
            and self.config.strategy == RateLimitStrategy.FIXED
        ):
            # For ENFORCE+FIXED: jump to window_seconds so we respect the full window before retry.
            # RETRY_ONLY skips this to avoid blocking callers; it uses pure exponential backoff.
            self.debug_log(
                f"Rate limit exceeded; setting delay to {self.config.window_seconds} seconds"
            )
            self.current_delay = self.config.window_seconds

        self.current_delay = min(
            self.current_delay * self.config.backoff_factor, self.config.max_delay
        )

    def debug_log(self, message: str):
        """Log the current rate limit status."""
        logger.debug(f"[RateLimiter/{self.config.effective_config_id}] {message}")

    def _get_deadline(self) -> float | None:
        """Return the caller-supplied execution deadline (Unix timestamp), if any."""
        ctx = RATE_LIMIT_CONTEXT.get()
        return ctx.deadline if ctx is not None else None

    def _check_deadline(self, sleep_seconds: float) -> None:
        """
        Raise BudgetExhaustedError if sleeping sleep_seconds would exceed the deadline.

        Note:
        This is a possible entrypoint for partial responses support, if not implemented via caching.
        """
        deadline = self._get_deadline()
        if deadline is not None and time.time() + sleep_seconds >= deadline:
            raise BudgetExhaustedError(
                retry_after_seconds=math.ceil(sleep_seconds),
                message=(f"Rate limit sleep of {sleep_seconds:.0f}s would exceed caller deadline"),
            )

    def _check_deadline_expired(self) -> None:
        """Raise BudgetExhaustedError if the execution deadline has already passed."""
        deadline = self._get_deadline()
        if deadline is not None and time.time() >= deadline:
            raise BudgetExhaustedError(
                retry_after_seconds=0,
                message="Execution deadline exceeded",
            )

    def seed_from_state(self, state: RateLimitStateSnapshot) -> None:
        """Seed this rate limiter from a snapshot returned by a previous execution.

        Preserves ADAPTIVE rate limiting state across page calls and connector restarts.
        Only non-None fields are applied so partial snapshots are safe to pass.
        """
        if state.limit is not None:
            self.config.requests_per_window = state.limit
        if state.window_seconds is not None:
            self.config.window_seconds = state.window_seconds
        if state.current_delay is not None:
            if state.reset is not None and state.reset <= time.time():
                self.current_delay = self.config.initial_delay
            else:
                self.current_delay = float(state.current_delay)
        if state.reset is not None:
            self.last_reset = float(state.reset)
        if state.remaining is not None and state.limit is not None:
            used = state.limit - state.remaining
            if used > 0:
                if state.reset is not None:
                    if state.reset > time.time():
                        # Window still active: anchor entries at window start so they expire at reset
                        entry_time = state.reset - self.config.window_seconds
                        self.request_times = [entry_time] * used
                else:
                    # No reset info: conservative fallback, treat used slots as fresh
                    self.request_times = [time.time()] * used
        self.debug_log(
            f"Seeded from state: requests_per_window={self.config.requests_per_window}, "
            f"window_seconds={self.config.window_seconds}, current_delay={self.current_delay}, "
            f"remaining={state.remaining}"
        )

    def get_current_state(self) -> RateLimitStateSnapshot:
        """Return a snapshot of current rate limit state for passthrough to the caller."""
        self._update_request_times()
        remaining = max(0, self.config.requests_per_window - len(self.request_times))

        if self.config.strategy == RateLimitStrategy.ADAPTIVE:
            reset = int(self.last_reset) if self.last_reset is not None else None
        else:
            reset = (
                int(min(self.request_times) + self.config.window_seconds)
                if self.request_times
                else None
            )

        return RateLimitStateSnapshot(
            remaining=remaining,
            limit=self.config.requests_per_window,
            window_seconds=self.config.window_seconds,
            current_delay=round(self.current_delay),
            reset=reset,
            source=self.snapshot_source,
        )

    async def execute_requests(
        self,
        requests: list[RequestType],
        request_handler: Callable[[RequestType], ResponseType | asyncio.Future[ResponseType]],
    ) -> list[ResponseType]:
        """
        Execute requests with rate limiting.
        """
        responses: list[ResponseType | BaseException] = []

        # Handle empty requests list
        if not requests:
            return []

        # Sequential processing
        if self.config.max_concurrent == 1 or len(requests) == 1:
            return await self._execute_requests_sequential(requests, request_handler)

        # For concurrent execution, use semaphore + asyncio.gather
        self.debug_log(
            f"Executing {len(requests)} requests with max_concurrent={self.config.max_concurrent}"
        )

        async def execute_with_semaphore(request: RequestType) -> ResponseType:
            async with self.semaphore:
                return await self._execute_single_request(request, request_handler)

        # Create tasks for all requests - this is what makes them run concurrently
        tasks = [execute_with_semaphore(request) for request in requests]

        # Execute all tasks concurrently (limited by semaphore)
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Log and raise any exceptions that occurred
        # These are going to be non-rate-limit related and non-httpx related
        processed_responses: list[ResponseType] = []
        for i, response in enumerate(responses):
            if isinstance(response, BaseException):
                self.debug_log(f"Request {i + 1} failed: {response}")
                raise response
            else:
                processed_responses.append(response)

        return processed_responses

    async def _execute_single_request(
        self,
        request: RequestType,
        request_handler: Callable[[RequestType], ResponseType | asyncio.Future[ResponseType]],
    ) -> ResponseType:
        """Execute a single request with rate limiting and retry logic."""
        retry_count = 0
        transient_retry_count = 0

        while retry_count <= self.config.maximum_retries:
            self._check_deadline_expired()
            wait_time = self._wait_time_needed()
            if wait_time > 0:
                self.debug_log(f"Waiting {wait_time} seconds before making request")
                self._check_deadline(wait_time)
                await asyncio.sleep(wait_time)

            try:
                result = request_handler(request)

                # Handle both synchronous and asynchronous results
                if asyncio.iscoroutine(result) or isinstance(result, asyncio.Future):
                    response = await result
                else:
                    response = result

                # Record the time
                self.request_times.append(time.time())

                # Update rate limits
                self._update_rate_limits(response)

                # For FIXED strategy:
                # Decay current_delay once window pressure has cleared.
                # ADAPTIVE gets this via _update_rate_limits; FIXED has no external signals.
                if (
                    self.config.strategy == RateLimitStrategy.FIXED
                    and self.current_delay > self.config.initial_delay
                    and self._can_make_request()
                ):
                    decayed = max(
                        self.current_delay / self.config.backoff_factor,
                        self.config.initial_delay,
                    )
                    self.current_delay = (
                        self.config.initial_delay if decayed < FIXED_DECAY_FLOOR else decayed
                    )

                return response
            except Exception as e:
                # Handle rate limit errors
                error_check = self.config.rate_limit_error_check or RateLimiter.is_rate_limit_error
                is_rate_limit_error = error_check(e)

                # Check for transient issues
                # Like the end system being unavailable or network issues
                transient_check = (
                    self.config.transient_error_check or RateLimiter.is_transient_error
                )
                is_transient = transient_check(e)

                if is_rate_limit_error or is_transient:
                    self._handle_rate_limit_exceeded()

                    if is_transient:
                        self.debug_log(f"Transient error; current delay: {self.current_delay}")
                    else:
                        self.debug_log(f"Rate limit exceeded; current delay: {self.current_delay}")

                    # Attempt to extract rate limit information if there is a response
                    if isinstance(e, httpx.HTTPStatusError) and (
                        error_response := getattr(e, "response", None)
                    ):
                        self._update_rate_limits(error_response)

                    if is_transient:
                        # Transient errors get their own counter
                        transient_retry_count += 1
                        if transient_retry_count > self.config.maximum_retries:
                            raise UpstreamError(
                                retry_after_seconds=math.ceil(self.current_delay)
                                or self.config.window_seconds,
                                message="Unable to process requests due to transient issues, retries exhausted",
                            ) from e
                    else:
                        retry_count += 1
                        if retry_count > self.config.maximum_retries:
                            raise RateLimitError(
                                retry_after_seconds=math.ceil(self.current_delay)
                                or self.config.window_seconds,
                                message=f"Maximum retries ({self.config.maximum_retries}) reached",
                            ) from e

                    # Retry the request after a delay
                    self._check_deadline(self.current_delay)
                    await asyncio.sleep(self.current_delay)
                else:
                    # Re-raise other exceptions
                    raise

        # This should not be reachable
        raise Exception("Retry loop completed without success or exception raised.")

    async def _execute_requests_sequential(
        self,
        requests: list[RequestType],
        request_handler: Callable[[RequestType], ResponseType | asyncio.Future[ResponseType]],
    ) -> list[ResponseType]:
        """
        Execute requests sequentially (original implementation).
        """
        responses: list[ResponseType] = []

        # Calc batch size
        batch_size = max(
            1,
            min(
                self.config.max_batch_size or self.config.requests_per_window,
                self.config.requests_per_window,
            ),
        )

        # Process requests in batches
        self.debug_log(
            f"Executing {len(requests)} requests in {len(requests) // batch_size} batches with batch size {batch_size}"
        )

        for i in range(0, len(requests), batch_size):
            batch = requests[i : i + batch_size]
            batch_responses = []

            for request in batch:
                response = await self._execute_single_request(request, request_handler)
                batch_responses.append(response)
                self.debug_log(
                    f"Request {len(responses) + len(batch_responses)} of {len(requests)} completed"
                )

            responses.extend(batch_responses)

            # Wait between batches — skipped in RETRY_ONLY to avoid blocking callers
            if (
                i + batch_size < len(requests)
                and self.current_delay > 0
                and self._effective_mode == RateLimitMode.ENFORCE
            ):
                self._check_deadline(self.current_delay)
                await asyncio.sleep(self.current_delay)

        return responses
