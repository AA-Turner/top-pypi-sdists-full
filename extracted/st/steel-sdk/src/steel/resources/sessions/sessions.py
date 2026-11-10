# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

import warnings
from typing import Any, Dict, List, Union, Iterable, cast
from datetime import datetime
from typing_extensions import Literal, overload

import httpx

from .files import (
    FilesResource,
    AsyncFilesResource,
    FilesResourceWithRawResponse,
    AsyncFilesResourceWithRawResponse,
    FilesResourceWithStreamingResponse,
    AsyncFilesResourceWithStreamingResponse,
)
from ...types import (
    session_list_params,
    session_logs_params,
    session_create_params,
    session_events_params,
    session_commands_params,
    session_computer_params,
    session_release_all_params,
    session_agent_traces_params,
    session_update_metadata_params,
    session_replace_metadata_params,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import path_template, required_args, maybe_transform, strip_not_given, async_maybe_transform
from .captchas import (
    CaptchasResource,
    AsyncCaptchasResource,
    CaptchasResourceWithRawResponse,
    AsyncCaptchasResourceWithRawResponse,
    CaptchasResourceWithStreamingResponse,
    AsyncCaptchasResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ...pagination import SyncSessionsCursor, AsyncSessionsCursor
from ..._base_client import AsyncPaginator, make_request_options
from ...types.session import Session as TypesSession
from ...types.sessionslist import Session as SessionslistSession
from ...types.session_context import SessionContext
from ...types.session_cost_response import SessionCostResponse
from ...types.session_logs_response import SessionLogsResponse
from ...types.session_events_response import SessionEventsResponse
from ...types.session_release_response import SessionReleaseResponse
from ...types.session_commands_response import SessionCommandsResponse
from ...types.session_computer_response import SessionComputerResponse
from ...types.session_release_all_response import SessionReleaseAllResponse
from ...types.session_agent_traces_response import SessionAgentTracesResponse
from ...types.session_live_details_response import SessionLiveDetailsResponse
from ...types.session_signal_catalog_response import SessionSignalCatalogResponse
from ...types.session_update_metadata_response import SessionUpdateMetadataResponse
from ...types.session_replace_metadata_response import SessionReplaceMetadataResponse

__all__ = ["SessionsResource", "AsyncSessionsResource"]


class SessionsResource(SyncAPIResource):
    @cached_property
    def captchas(self) -> CaptchasResource:
        return CaptchasResource(self._client)

    @cached_property
    def files(self) -> FilesResource:
        return FilesResource(self._client)

    @cached_property
    def with_raw_response(self) -> SessionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#accessing-raw-response-data-eg-headers
        """
        return SessionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SessionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#with_streaming_response
        """
        return SessionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        block_ads: bool | Omit = omit,
        ca_certificates: SequenceNotStr[str] | Omit = omit,
        concurrency: int | Omit = omit,
        credentials: session_create_params.Credentials | Omit = omit,
        debug_config: session_create_params.DebugConfig | Omit = omit,
        device_config: session_create_params.DeviceConfig | Omit = omit,
        dimensions: session_create_params.Dimensions | Omit = omit,
        experimental_features: SequenceNotStr[str] | Omit = omit,
        extension_ids: SequenceNotStr[str] | Omit = omit,
        fullscreen: bool | Omit = omit,
        headless: bool | Omit = omit,
        inactivity_timeout: int | Omit = omit,
        is_selenium: bool | Omit = omit,
        metadata: Dict[str, Union[str, float, bool]] | Omit = omit,
        namespace: str | Omit = omit,
        optimize_bandwidth: session_create_params.OptimizeBandwidth | Omit = omit,
        persist_profile: bool | Omit = omit,
        profile_id: str | Omit = omit,
        project_id: str | Omit = omit,
        proxy_url: str | Omit = omit,
        recording: bool | Omit = omit,
        region: object | Omit = omit,
        session_context: session_create_params.SessionContext | Omit = omit,
        session_id: str | Omit = omit,
        solve_captcha: bool | Omit = omit,
        stealth_config: session_create_params.StealthConfig | Omit = omit,
        api_timeout: int | Omit = omit,
        use_proxy: session_create_params.UseProxy | Omit = omit,
        user_agent: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TypesSession:
        """
        Creates a new session with the provided configuration.

        Args:
          block_ads: Block ads in the browser session. Default is false.

          ca_certificates: PEM-encoded root CA certificates to trust in this session. THIS IS CURRENTLY AN
              EXPERIMENTAL FEATURE.

          concurrency: Number of sessions to create concurrently (check your plan limit)

          credentials: Configuration for session credentials

          debug_config: Configuration for the debug URL and session viewer. Controls interaction
              capabilities, cursor visibility, and other debug-related settings.

          device_config: Device configuration for the session. Specify 'mobile' for mobile device
              fingerprints and configurations.

          dimensions: Viewport and browser window dimensions for the session. Mobile sessions require
              dimensions of at least 508x1074; smaller mobile dimensions are rejected with a
              400 response.

          experimental_features: Enable experimental features for the session.

          extension_ids: Array of extension IDs to install in the session. Use ['all_ext'] to install all
              uploaded extensions.

          fullscreen: Launch the browser in fullscreen mode, covering the full screen with no Chrome
              UI. Default is false.

          headless: Enable headless browser mode (disable Headful mode)

          inactivity_timeout: Inactivity timeout in milliseconds. When set, the session is released if no CDP
              command or remote input is received for this duration, even if `timeout` has not
              yet elapsed. Note that `timeout` remains the hard cap on session lifetime: if
              `inactivityTimeout` is greater than or equal to the effective `timeout`, it has
              no effect since `timeout` always elapses first. Omit to disable.

          is_selenium: Deprecated. Selenium sessions are no longer supported, and a request that sets
              this to true is rejected with 400. Connect over CDP with Playwright or Puppeteer
              instead.

          metadata: Customer-defined flat metadata: up to 50 keys and 8192 UTF-8 JSON bytes. Keys
              must start with a letter, use only letters, digits, underscores, dots or
              hyphens, and be at most 64 characters; steel\\__ is reserved. Values are strings
              (up to 1024 characters, valid Unicode without NUL), finite numbers or booleans.
              Numbers and booleans are stored as strings, so 3 and "3" are the same value.

          namespace: The namespace the session should be created against. Defaults to "default".

          optimize_bandwidth: Enable bandwidth optimizations. Passing true enables all flags (except
              hosts/patterns). Object allows granular control.

          persist_profile: This flag will persist the user profile for the session.

          profile_id: This flag will set the profile for the session.

          project_id: The project to create the session in. When provided, the session namespace is
              resolved from the project.

          proxy_url: Custom proxy URL for the browser session. Overrides useProxy, disabling
              Steel-provided proxies in favor of your specified proxy. Format:
              http(s)://username:password@hostname:port

          recording: Record the headful session for playback after it ends. Default is true.
              Disabling recording does not affect live WHEP viewing.

          region: The desired region for the session. Available: us-east, us-west, us-central,
              eu-west, eu-central, ap-northeast, ap-southeast, sa-east. Legacy codes (iad,
              lax, ord) are also accepted.

          session_context: Session context data to be used in the created session. Sessions will start with
              an empty context by default.

          session_id: Optional custom UUID for the session

          solve_captcha: Enable automatic captcha solving. Default is false.

          stealth_config: Stealth configuration for the session

          api_timeout: Session timeout duration in milliseconds. Default is 300000 (5 minutes).

          use_proxy: Simple boolean to enable/disable Steel proxies

          user_agent: Custom user agent string for the browser session

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_timeout and isinstance(timeout, (int, float)) and timeout:
            warnings.warn(
                "Setting the session timeout with `timeout` is deprecated and stops working in a future release. "
                "Use `api_timeout` for the session timeout. `timeout` sets the HTTP request timeout.",
                DeprecationWarning,
                stacklevel=2,
            )
            api_timeout = int(timeout)
        return self._post(
            "/v1/sessions",
            body=maybe_transform(
                {
                    "block_ads": block_ads,
                    "ca_certificates": ca_certificates,
                    "concurrency": concurrency,
                    "credentials": credentials,
                    "debug_config": debug_config,
                    "device_config": device_config,
                    "dimensions": dimensions,
                    "experimental_features": experimental_features,
                    "extension_ids": extension_ids,
                    "fullscreen": fullscreen,
                    "headless": headless,
                    "inactivity_timeout": inactivity_timeout,
                    "is_selenium": is_selenium,
                    "metadata": metadata,
                    "namespace": namespace,
                    "optimize_bandwidth": optimize_bandwidth,
                    "persist_profile": persist_profile,
                    "profile_id": profile_id,
                    "project_id": project_id,
                    "proxy_url": proxy_url,
                    "recording": recording,
                    "region": region,
                    "session_context": session_context,
                    "session_id": session_id,
                    "solve_captcha": solve_captcha,
                    "stealth_config": stealth_config,
                    "api_timeout": api_timeout,
                    "use_proxy": use_proxy,
                    "user_agent": user_agent,
                },
                session_create_params.SessionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TypesSession,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TypesSession:
        """
        Retrieves details of a specific session by ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/v1/sessions/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TypesSession,
        )

    def list(
        self,
        *,
        created_after: Union[str, datetime] | Omit = omit,
        created_before: Union[str, datetime] | Omit = omit,
        cursor_id: str | Omit = omit,
        limit: int | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        project_id: str | Omit = omit,
        release_reason: Literal[
            "user_requested",
            "timeout",
            "inactivity_timeout",
            "creation_timeout",
            "startup_failed",
            "browser_closed",
            "browser_crashed",
        ]
        | Omit = omit,
        signal: List[
            Literal[
                "captcha_encountered",
                "proxy_connection_failed",
                "session_timeout_exceeded",
                "bot_detection_triggered",
                "context_restored",
            ]
        ]
        | Omit = omit,
        status: Literal["live", "released", "failed"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncSessionsCursor[SessionslistSession]:
        """
        Fetches all active sessions for the current organization.

        Args:
          created_after: Only sessions created at or after this ISO 8601 timestamp, e.g.
              2026-10-01T00:00:00Z.

          created_before: Only sessions created before this ISO 8601 timestamp.

          cursor_id: Cursor ID for pagination

          limit: Number of sessions to return. Default is 50, max is 100.

          metadata: Exact-match metadata filters, e.g. metadata[environment]=production. All entries
              must match. Values match the stored string exactly; numbers and booleans are
              stored as strings, so metadata[attempt]=3 matches attempt sent as 3 or "3".

          project_id: Filter sessions by project

          release_reason: Filter released sessions by why they ended. Live sessions have no release reason
              and are excluded whenever this is set. Without an explicit status, matching
              failed sessions are included.

          signal: Signals the session must carry; repeat the parameter to require several. All
              must match. Derived signals are finalized at release.

          status: Filter sessions by current status

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/sessions",
            page=SyncSessionsCursor[SessionslistSession],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "created_after": created_after,
                        "created_before": created_before,
                        "cursor_id": cursor_id,
                        "limit": limit,
                        "metadata": metadata,
                        "project_id": project_id,
                        "release_reason": release_reason,
                        "signal": signal,
                        "status": status,
                    },
                    session_list_params.SessionListParams,
                ),
            ),
            model=SessionslistSession,
        )

    def agent_traces(
        self,
        id: str,
        *,
        end_time: Union[str, datetime] | Omit = omit,
        event_types: SequenceNotStr[str] | Omit = omit,
        limit: int | Omit = omit,
        namespace: str | Omit = omit,
        offset: int | Omit = omit,
        start_time: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionAgentTracesResponse:
        """
        Query the semantic agent trace timeline for a session: a coalesced,
        replay-oriented record of user/agent interactions (clicks, typing, scrolls,
        drags, navigations) with target metadata (role, accessible name, selectors).
        Returns an empty list for sessions that predate browser-interaction capture.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/v1/sessions/{id}/agent-traces", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "end_time": end_time,
                        "event_types": event_types,
                        "limit": limit,
                        "namespace": namespace,
                        "offset": offset,
                        "start_time": start_time,
                    },
                    session_agent_traces_params.SessionAgentTracesParams,
                ),
            ),
            cast_to=SessionAgentTracesResponse,
        )

    def commands(
        self,
        session_id: str,
        *,
        commands: session_commands_params.Commands,
        after: str | Omit = omit,
        events_after: str | Omit = omit,
        observe: session_commands_params.Observe | Omit = omit,
        idempotency_key: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCommandsResponse:
        """
        Drives the session's browser with high-level commands such as snapshot, click,
        and fill. Commands run in order and stop at the first failure. Send a random
        Idempotency-Key header to make retries safe.

        Args:
          commands: One command, or an array of up to 50. They run in order and stop at the first
              failure. Commands that already ran are not undone.

          after: The next value from your last response. A retry with the same after and commands
              runs only once.

          events_after: c-0 the first time, then the last events.cursor.

          observe: Returns a snapshot, or a diff against the last one, after the commands.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        extra_headers = {**strip_not_given({"idempotency-key": idempotency_key}), **(extra_headers or {})}
        return cast(
            SessionCommandsResponse,
            self._post(
                path_template("/v1/sessions/{session_id}/commands", session_id=session_id),
                body=maybe_transform(
                    {
                        "commands": commands,
                        "after": after,
                        "events_after": events_after,
                        "observe": observe,
                    },
                    session_commands_params.SessionCommandsParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, SessionCommandsResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    @overload
    def computer(
        self,
        session_id: str,
        *,
        action: Literal["move_mouse"],
        coordinates: Iterable[float],
        hold_keys: SequenceNotStr[str] | Omit = omit,
        screenshot: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          coordinates: X and Y coordinates [x, y]

          hold_keys: Keys to hold while moving

          screenshot: Whether to take a screenshot after the action

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def computer(
        self,
        session_id: str,
        *,
        action: Literal["click_mouse"],
        button: Literal["left", "right", "middle", "back", "forward"] | Omit = omit,
        click_type: Literal["down", "up", "click"] | Omit = omit,
        coordinates: Iterable[float] | Omit = omit,
        hold_keys: SequenceNotStr[str] | Omit = omit,
        num_clicks: float | Omit = omit,
        screenshot: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          button: Mouse button to click. Defaults to 'left'

          click_type: Type of click (down, up, or click). Defaults to 'click'

          coordinates: X and Y coordinates [x, y]

          hold_keys: Keys to hold while clicking

          num_clicks: Number of clicks. Defaults to 1

          screenshot: Whether to take a screenshot after the action

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def computer(
        self,
        session_id: str,
        *,
        action: Literal["drag_mouse"],
        path: Iterable[Iterable[float]],
        hold_keys: SequenceNotStr[str] | Omit = omit,
        screenshot: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          path: Array of [x, y] coordinate pairs

          hold_keys: Keys to hold while dragging

          screenshot: Whether to take a screenshot after the action

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def computer(
        self,
        session_id: str,
        *,
        action: Literal["scroll"],
        coordinates: Iterable[float] | Omit = omit,
        delta_x: float | Omit = omit,
        delta_y: float | Omit = omit,
        hold_keys: SequenceNotStr[str] | Omit = omit,
        screenshot: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          coordinates: X and Y coordinates [x, y]

          delta_x: Horizontal scroll amount. Defaults to 0

          delta_y: Vertical scroll amount. Defaults to 0

          hold_keys: Keys to hold while scrolling

          screenshot: Whether to take a screenshot after the action

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def computer(
        self,
        session_id: str,
        *,
        action: Literal["press_key"],
        keys: SequenceNotStr[str],
        duration: float | Omit = omit,
        screenshot: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          keys: Keys to press

          duration: Duration to hold keys in seconds

          screenshot: Whether to take a screenshot after the action

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def computer(
        self,
        session_id: str,
        *,
        action: Literal["type_text"],
        text: str,
        hold_keys: SequenceNotStr[str] | Omit = omit,
        screenshot: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          text: Text to type

          hold_keys: Keys to hold while typing

          screenshot: Whether to take a screenshot after the action

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def computer(
        self,
        session_id: str,
        *,
        action: Literal["wait"],
        duration: float,
        screenshot: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          duration: Duration to wait in seconds

          screenshot: Whether to take a screenshot after the action

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def computer(
        self,
        session_id: str,
        *,
        action: Literal["take_screenshot"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def computer(
        self,
        session_id: str,
        *,
        action: Literal["get_cursor_position"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["action", "coordinates"],
        ["action"],
        ["action", "path"],
        ["action", "keys"],
        ["action", "text"],
        ["action", "duration"],
    )
    def computer(
        self,
        session_id: str,
        *,
        action: Literal["move_mouse"]
        | Literal["click_mouse"]
        | Literal["drag_mouse"]
        | Literal["scroll"]
        | Literal["press_key"]
        | Literal["type_text"]
        | Literal["wait"]
        | Literal["take_screenshot"]
        | Literal["get_cursor_position"],
        coordinates: Iterable[float] | Omit = omit,
        hold_keys: SequenceNotStr[str] | Omit = omit,
        screenshot: bool | Omit = omit,
        button: Literal["left", "right", "middle", "back", "forward"] | Omit = omit,
        click_type: Literal["down", "up", "click"] | Omit = omit,
        num_clicks: float | Omit = omit,
        path: Iterable[Iterable[float]] | Omit = omit,
        delta_x: float | Omit = omit,
        delta_y: float | Omit = omit,
        keys: SequenceNotStr[str] | Omit = omit,
        duration: float | Omit = omit,
        text: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._post(
            path_template("/v1/sessions/{session_id}/computer", session_id=session_id),
            body=maybe_transform(
                {
                    "action": action,
                    "coordinates": coordinates,
                    "hold_keys": hold_keys,
                    "screenshot": screenshot,
                    "button": button,
                    "click_type": click_type,
                    "num_clicks": num_clicks,
                    "path": path,
                    "delta_x": delta_x,
                    "delta_y": delta_y,
                    "keys": keys,
                    "duration": duration,
                    "text": text,
                },
                session_computer_params.SessionComputerParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionComputerResponse,
        )

    def context(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionContext:
        """
        Fetches the context data of a specific session.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/v1/sessions/{id}/context", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionContext,
        )

    def cost(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCostResponse:
        """
        Returns the finalized cost of a released session as an exact amount in US
        dollars (e.g. 0.031905), suitable for precise billing passthrough.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/v1/sessions/{id}/cost", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionCostResponse,
        )

    def events(
        self,
        id: str,
        *,
        compressed: bool | Omit = omit,
        limit: int | Omit = omit,
        pointer: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionEventsResponse:
        """
        This endpoint allows you to get the recorded session events in the RRWeb format

        Args:
          compressed: Compress the events

          limit: Optional pagination limit

          pointer: Opaque pagination token. Pass the Next-Cursor header value to get the next page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/v1/sessions/{id}/events", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "compressed": compressed,
                        "limit": limit,
                        "pointer": pointer,
                    },
                    session_events_params.SessionEventsParams,
                ),
            ),
            cast_to=SessionEventsResponse,
        )

    def hls(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BinaryAPIResponse:
        """
        Get HLS playlist for a session recording using app auth or an RTC token

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/vnd.apple.mpegurl", **(extra_headers or {})}
        return self._get(
            path_template("/v1/sessions/{id}/hls", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def live_details(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionLiveDetailsResponse:
        """
        Returns the live state of the session, including pages, tabs, and browser state

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/v1/sessions/{id}/live-details", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionLiveDetailsResponse,
        )

    def logs(
        self,
        id: str,
        *,
        end_time: Union[str, datetime] | Omit = omit,
        event_types: SequenceNotStr[str] | Omit = omit,
        limit: int | Omit = omit,
        namespace: str | Omit = omit,
        offset: int | Omit = omit,
        start_time: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionLogsResponse:
        """
        Query browser event logs for a session

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/v1/sessions/{id}/logs", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "end_time": end_time,
                        "event_types": event_types,
                        "limit": limit,
                        "namespace": namespace,
                        "offset": offset,
                        "start_time": start_time,
                    },
                    session_logs_params.SessionLogsParams,
                ),
            ),
            cast_to=SessionLogsResponse,
        )

    def release(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionReleaseResponse:
        """
        Releases a specific session by ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/v1/sessions/{id}/release", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionReleaseResponse,
        )

    def release_all(
        self,
        *,
        project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionReleaseAllResponse:
        """
        Releases all active sessions for the current organization.

        Args:
          project_id: Release sessions only within this project

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/sessions/release",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"project_id": project_id}, session_release_all_params.SessionReleaseAllParams),
            ),
            cast_to=SessionReleaseAllResponse,
        )

    def replace_metadata(
        self,
        id: str,
        *,
        metadata: Dict[str, Union[str, float, bool]],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionReplaceMetadataResponse:
        """Atomically replace customer metadata.

        Send an empty object to clear it. Last
        accepted write wins; use PATCH to change individual keys. Subject to session
        organization and project access.

        Args:
          metadata: Customer-defined flat metadata: up to 50 keys and 8192 UTF-8 JSON bytes. Keys
              must start with a letter, use only letters, digits, underscores, dots or
              hyphens, and be at most 64 characters; steel\\__ is reserved. Values are strings
              (up to 1024 characters, valid Unicode without NUL), finite numbers or booleans.
              Numbers and booleans are stored as strings, so 3 and "3" are the same value.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._put(
            path_template("/v1/sessions/{id}/metadata", id=id),
            body=maybe_transform({"metadata": metadata}, session_replace_metadata_params.SessionReplaceMetadataParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionReplaceMetadataResponse,
        )

    def signal_catalog(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionSignalCatalogResponse:
        """Returns current signal labels and meanings for customer integrations.

        Uses
        normal Steel API-key authentication. Includes no session data or administrative
        signals. Definitions do not establish that detection ran for a particular
        session.
        """
        return self._get(
            "/v1/sessions/signals/catalog",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionSignalCatalogResponse,
        )

    def update_metadata(
        self,
        id: str,
        *,
        metadata: Dict[str, Union[str, float, bool, None]],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionUpdateMetadataResponse:
        """Atomically merge keys into customer metadata.

        Set a key to null to remove it;
        keys you leave out are kept, so concurrent updates to different keys are all
        kept. Returns the merged metadata, which must stay within the metadata limits.
        Subject to session organization and project access.

        Args:
          metadata: Metadata keys to change, up to 100 per update. Keys follow the same rules as
              metadata keys. Send a string, finite number or boolean to set a key, or null to
              remove it; keys you leave out are kept. The merged metadata must stay within 50
              keys and 8192 UTF-8 JSON bytes.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._patch(
            path_template("/v1/sessions/{id}/metadata", id=id),
            body=maybe_transform({"metadata": metadata}, session_update_metadata_params.SessionUpdateMetadataParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionUpdateMetadataResponse,
        )


class AsyncSessionsResource(AsyncAPIResource):
    @cached_property
    def captchas(self) -> AsyncCaptchasResource:
        return AsyncCaptchasResource(self._client)

    @cached_property
    def files(self) -> AsyncFilesResource:
        return AsyncFilesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSessionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#accessing-raw-response-data-eg-headers
        """
        return AsyncSessionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSessionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://github.com/steel-dev/sdk/tree/main/python#with_streaming_response
        """
        return AsyncSessionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        block_ads: bool | Omit = omit,
        ca_certificates: SequenceNotStr[str] | Omit = omit,
        concurrency: int | Omit = omit,
        credentials: session_create_params.Credentials | Omit = omit,
        debug_config: session_create_params.DebugConfig | Omit = omit,
        device_config: session_create_params.DeviceConfig | Omit = omit,
        dimensions: session_create_params.Dimensions | Omit = omit,
        experimental_features: SequenceNotStr[str] | Omit = omit,
        extension_ids: SequenceNotStr[str] | Omit = omit,
        fullscreen: bool | Omit = omit,
        headless: bool | Omit = omit,
        inactivity_timeout: int | Omit = omit,
        is_selenium: bool | Omit = omit,
        metadata: Dict[str, Union[str, float, bool]] | Omit = omit,
        namespace: str | Omit = omit,
        optimize_bandwidth: session_create_params.OptimizeBandwidth | Omit = omit,
        persist_profile: bool | Omit = omit,
        profile_id: str | Omit = omit,
        project_id: str | Omit = omit,
        proxy_url: str | Omit = omit,
        recording: bool | Omit = omit,
        region: object | Omit = omit,
        session_context: session_create_params.SessionContext | Omit = omit,
        session_id: str | Omit = omit,
        solve_captcha: bool | Omit = omit,
        stealth_config: session_create_params.StealthConfig | Omit = omit,
        api_timeout: int | Omit = omit,
        use_proxy: session_create_params.UseProxy | Omit = omit,
        user_agent: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TypesSession:
        """
        Creates a new session with the provided configuration.

        Args:
          block_ads: Block ads in the browser session. Default is false.

          ca_certificates: PEM-encoded root CA certificates to trust in this session. THIS IS CURRENTLY AN
              EXPERIMENTAL FEATURE.

          concurrency: Number of sessions to create concurrently (check your plan limit)

          credentials: Configuration for session credentials

          debug_config: Configuration for the debug URL and session viewer. Controls interaction
              capabilities, cursor visibility, and other debug-related settings.

          device_config: Device configuration for the session. Specify 'mobile' for mobile device
              fingerprints and configurations.

          dimensions: Viewport and browser window dimensions for the session. Mobile sessions require
              dimensions of at least 508x1074; smaller mobile dimensions are rejected with a
              400 response.

          experimental_features: Enable experimental features for the session.

          extension_ids: Array of extension IDs to install in the session. Use ['all_ext'] to install all
              uploaded extensions.

          fullscreen: Launch the browser in fullscreen mode, covering the full screen with no Chrome
              UI. Default is false.

          headless: Enable headless browser mode (disable Headful mode)

          inactivity_timeout: Inactivity timeout in milliseconds. When set, the session is released if no CDP
              command or remote input is received for this duration, even if `timeout` has not
              yet elapsed. Note that `timeout` remains the hard cap on session lifetime: if
              `inactivityTimeout` is greater than or equal to the effective `timeout`, it has
              no effect since `timeout` always elapses first. Omit to disable.

          is_selenium: Deprecated. Selenium sessions are no longer supported, and a request that sets
              this to true is rejected with 400. Connect over CDP with Playwright or Puppeteer
              instead.

          metadata: Customer-defined flat metadata: up to 50 keys and 8192 UTF-8 JSON bytes. Keys
              must start with a letter, use only letters, digits, underscores, dots or
              hyphens, and be at most 64 characters; steel\\__ is reserved. Values are strings
              (up to 1024 characters, valid Unicode without NUL), finite numbers or booleans.
              Numbers and booleans are stored as strings, so 3 and "3" are the same value.

          namespace: The namespace the session should be created against. Defaults to "default".

          optimize_bandwidth: Enable bandwidth optimizations. Passing true enables all flags (except
              hosts/patterns). Object allows granular control.

          persist_profile: This flag will persist the user profile for the session.

          profile_id: This flag will set the profile for the session.

          project_id: The project to create the session in. When provided, the session namespace is
              resolved from the project.

          proxy_url: Custom proxy URL for the browser session. Overrides useProxy, disabling
              Steel-provided proxies in favor of your specified proxy. Format:
              http(s)://username:password@hostname:port

          recording: Record the headful session for playback after it ends. Default is true.
              Disabling recording does not affect live WHEP viewing.

          region: The desired region for the session. Available: us-east, us-west, us-central,
              eu-west, eu-central, ap-northeast, ap-southeast, sa-east. Legacy codes (iad,
              lax, ord) are also accepted.

          session_context: Session context data to be used in the created session. Sessions will start with
              an empty context by default.

          session_id: Optional custom UUID for the session

          solve_captcha: Enable automatic captcha solving. Default is false.

          stealth_config: Stealth configuration for the session

          api_timeout: Session timeout duration in milliseconds. Default is 300000 (5 minutes).

          use_proxy: Simple boolean to enable/disable Steel proxies

          user_agent: Custom user agent string for the browser session

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_timeout and isinstance(timeout, (int, float)) and timeout:
            warnings.warn(
                "Setting the session timeout with `timeout` is deprecated and stops working in a future release. "
                "Use `api_timeout` for the session timeout. `timeout` sets the HTTP request timeout.",
                DeprecationWarning,
                stacklevel=2,
            )
            api_timeout = int(timeout)
        return await self._post(
            "/v1/sessions",
            body=await async_maybe_transform(
                {
                    "block_ads": block_ads,
                    "ca_certificates": ca_certificates,
                    "concurrency": concurrency,
                    "credentials": credentials,
                    "debug_config": debug_config,
                    "device_config": device_config,
                    "dimensions": dimensions,
                    "experimental_features": experimental_features,
                    "extension_ids": extension_ids,
                    "fullscreen": fullscreen,
                    "headless": headless,
                    "inactivity_timeout": inactivity_timeout,
                    "is_selenium": is_selenium,
                    "metadata": metadata,
                    "namespace": namespace,
                    "optimize_bandwidth": optimize_bandwidth,
                    "persist_profile": persist_profile,
                    "profile_id": profile_id,
                    "project_id": project_id,
                    "proxy_url": proxy_url,
                    "recording": recording,
                    "region": region,
                    "session_context": session_context,
                    "session_id": session_id,
                    "solve_captcha": solve_captcha,
                    "stealth_config": stealth_config,
                    "api_timeout": api_timeout,
                    "use_proxy": use_proxy,
                    "user_agent": user_agent,
                },
                session_create_params.SessionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TypesSession,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TypesSession:
        """
        Retrieves details of a specific session by ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/v1/sessions/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TypesSession,
        )

    def list(
        self,
        *,
        created_after: Union[str, datetime] | Omit = omit,
        created_before: Union[str, datetime] | Omit = omit,
        cursor_id: str | Omit = omit,
        limit: int | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        project_id: str | Omit = omit,
        release_reason: Literal[
            "user_requested",
            "timeout",
            "inactivity_timeout",
            "creation_timeout",
            "startup_failed",
            "browser_closed",
            "browser_crashed",
        ]
        | Omit = omit,
        signal: List[
            Literal[
                "captcha_encountered",
                "proxy_connection_failed",
                "session_timeout_exceeded",
                "bot_detection_triggered",
                "context_restored",
            ]
        ]
        | Omit = omit,
        status: Literal["live", "released", "failed"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[SessionslistSession, AsyncSessionsCursor[SessionslistSession]]:
        """
        Fetches all active sessions for the current organization.

        Args:
          created_after: Only sessions created at or after this ISO 8601 timestamp, e.g.
              2026-10-01T00:00:00Z.

          created_before: Only sessions created before this ISO 8601 timestamp.

          cursor_id: Cursor ID for pagination

          limit: Number of sessions to return. Default is 50, max is 100.

          metadata: Exact-match metadata filters, e.g. metadata[environment]=production. All entries
              must match. Values match the stored string exactly; numbers and booleans are
              stored as strings, so metadata[attempt]=3 matches attempt sent as 3 or "3".

          project_id: Filter sessions by project

          release_reason: Filter released sessions by why they ended. Live sessions have no release reason
              and are excluded whenever this is set. Without an explicit status, matching
              failed sessions are included.

          signal: Signals the session must carry; repeat the parameter to require several. All
              must match. Derived signals are finalized at release.

          status: Filter sessions by current status

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/sessions",
            page=AsyncSessionsCursor[SessionslistSession],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "created_after": created_after,
                        "created_before": created_before,
                        "cursor_id": cursor_id,
                        "limit": limit,
                        "metadata": metadata,
                        "project_id": project_id,
                        "release_reason": release_reason,
                        "signal": signal,
                        "status": status,
                    },
                    session_list_params.SessionListParams,
                ),
            ),
            model=SessionslistSession,
        )

    async def agent_traces(
        self,
        id: str,
        *,
        end_time: Union[str, datetime] | Omit = omit,
        event_types: SequenceNotStr[str] | Omit = omit,
        limit: int | Omit = omit,
        namespace: str | Omit = omit,
        offset: int | Omit = omit,
        start_time: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionAgentTracesResponse:
        """
        Query the semantic agent trace timeline for a session: a coalesced,
        replay-oriented record of user/agent interactions (clicks, typing, scrolls,
        drags, navigations) with target metadata (role, accessible name, selectors).
        Returns an empty list for sessions that predate browser-interaction capture.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/v1/sessions/{id}/agent-traces", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "end_time": end_time,
                        "event_types": event_types,
                        "limit": limit,
                        "namespace": namespace,
                        "offset": offset,
                        "start_time": start_time,
                    },
                    session_agent_traces_params.SessionAgentTracesParams,
                ),
            ),
            cast_to=SessionAgentTracesResponse,
        )

    async def commands(
        self,
        session_id: str,
        *,
        commands: session_commands_params.Commands,
        after: str | Omit = omit,
        events_after: str | Omit = omit,
        observe: session_commands_params.Observe | Omit = omit,
        idempotency_key: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCommandsResponse:
        """
        Drives the session's browser with high-level commands such as snapshot, click,
        and fill. Commands run in order and stop at the first failure. Send a random
        Idempotency-Key header to make retries safe.

        Args:
          commands: One command, or an array of up to 50. They run in order and stop at the first
              failure. Commands that already ran are not undone.

          after: The next value from your last response. A retry with the same after and commands
              runs only once.

          events_after: c-0 the first time, then the last events.cursor.

          observe: Returns a snapshot, or a diff against the last one, after the commands.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        extra_headers = {**strip_not_given({"idempotency-key": idempotency_key}), **(extra_headers or {})}
        return cast(
            SessionCommandsResponse,
            await self._post(
                path_template("/v1/sessions/{session_id}/commands", session_id=session_id),
                body=await async_maybe_transform(
                    {
                        "commands": commands,
                        "after": after,
                        "events_after": events_after,
                        "observe": observe,
                    },
                    session_commands_params.SessionCommandsParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, SessionCommandsResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    @overload
    async def computer(
        self,
        session_id: str,
        *,
        action: Literal["move_mouse"],
        coordinates: Iterable[float],
        hold_keys: SequenceNotStr[str] | Omit = omit,
        screenshot: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          coordinates: X and Y coordinates [x, y]

          hold_keys: Keys to hold while moving

          screenshot: Whether to take a screenshot after the action

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def computer(
        self,
        session_id: str,
        *,
        action: Literal["click_mouse"],
        button: Literal["left", "right", "middle", "back", "forward"] | Omit = omit,
        click_type: Literal["down", "up", "click"] | Omit = omit,
        coordinates: Iterable[float] | Omit = omit,
        hold_keys: SequenceNotStr[str] | Omit = omit,
        num_clicks: float | Omit = omit,
        screenshot: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          button: Mouse button to click. Defaults to 'left'

          click_type: Type of click (down, up, or click). Defaults to 'click'

          coordinates: X and Y coordinates [x, y]

          hold_keys: Keys to hold while clicking

          num_clicks: Number of clicks. Defaults to 1

          screenshot: Whether to take a screenshot after the action

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def computer(
        self,
        session_id: str,
        *,
        action: Literal["drag_mouse"],
        path: Iterable[Iterable[float]],
        hold_keys: SequenceNotStr[str] | Omit = omit,
        screenshot: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          path: Array of [x, y] coordinate pairs

          hold_keys: Keys to hold while dragging

          screenshot: Whether to take a screenshot after the action

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def computer(
        self,
        session_id: str,
        *,
        action: Literal["scroll"],
        coordinates: Iterable[float] | Omit = omit,
        delta_x: float | Omit = omit,
        delta_y: float | Omit = omit,
        hold_keys: SequenceNotStr[str] | Omit = omit,
        screenshot: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          coordinates: X and Y coordinates [x, y]

          delta_x: Horizontal scroll amount. Defaults to 0

          delta_y: Vertical scroll amount. Defaults to 0

          hold_keys: Keys to hold while scrolling

          screenshot: Whether to take a screenshot after the action

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def computer(
        self,
        session_id: str,
        *,
        action: Literal["press_key"],
        keys: SequenceNotStr[str],
        duration: float | Omit = omit,
        screenshot: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          keys: Keys to press

          duration: Duration to hold keys in seconds

          screenshot: Whether to take a screenshot after the action

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def computer(
        self,
        session_id: str,
        *,
        action: Literal["type_text"],
        text: str,
        hold_keys: SequenceNotStr[str] | Omit = omit,
        screenshot: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          text: Text to type

          hold_keys: Keys to hold while typing

          screenshot: Whether to take a screenshot after the action

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def computer(
        self,
        session_id: str,
        *,
        action: Literal["wait"],
        duration: float,
        screenshot: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          duration: Duration to wait in seconds

          screenshot: Whether to take a screenshot after the action

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def computer(
        self,
        session_id: str,
        *,
        action: Literal["take_screenshot"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def computer(
        self,
        session_id: str,
        *,
        action: Literal["get_cursor_position"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        """
        Execute computer actions like mouse movements, clicks, keyboard input, and more

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["action", "coordinates"],
        ["action"],
        ["action", "path"],
        ["action", "keys"],
        ["action", "text"],
        ["action", "duration"],
    )
    async def computer(
        self,
        session_id: str,
        *,
        action: Literal["move_mouse"]
        | Literal["click_mouse"]
        | Literal["drag_mouse"]
        | Literal["scroll"]
        | Literal["press_key"]
        | Literal["type_text"]
        | Literal["wait"]
        | Literal["take_screenshot"]
        | Literal["get_cursor_position"],
        coordinates: Iterable[float] | Omit = omit,
        hold_keys: SequenceNotStr[str] | Omit = omit,
        screenshot: bool | Omit = omit,
        button: Literal["left", "right", "middle", "back", "forward"] | Omit = omit,
        click_type: Literal["down", "up", "click"] | Omit = omit,
        num_clicks: float | Omit = omit,
        path: Iterable[Iterable[float]] | Omit = omit,
        delta_x: float | Omit = omit,
        delta_y: float | Omit = omit,
        keys: SequenceNotStr[str] | Omit = omit,
        duration: float | Omit = omit,
        text: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionComputerResponse:
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._post(
            path_template("/v1/sessions/{session_id}/computer", session_id=session_id),
            body=await async_maybe_transform(
                {
                    "action": action,
                    "coordinates": coordinates,
                    "hold_keys": hold_keys,
                    "screenshot": screenshot,
                    "button": button,
                    "click_type": click_type,
                    "num_clicks": num_clicks,
                    "path": path,
                    "delta_x": delta_x,
                    "delta_y": delta_y,
                    "keys": keys,
                    "duration": duration,
                    "text": text,
                },
                session_computer_params.SessionComputerParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionComputerResponse,
        )

    async def context(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionContext:
        """
        Fetches the context data of a specific session.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/v1/sessions/{id}/context", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionContext,
        )

    async def cost(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCostResponse:
        """
        Returns the finalized cost of a released session as an exact amount in US
        dollars (e.g. 0.031905), suitable for precise billing passthrough.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/v1/sessions/{id}/cost", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionCostResponse,
        )

    async def events(
        self,
        id: str,
        *,
        compressed: bool | Omit = omit,
        limit: int | Omit = omit,
        pointer: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionEventsResponse:
        """
        This endpoint allows you to get the recorded session events in the RRWeb format

        Args:
          compressed: Compress the events

          limit: Optional pagination limit

          pointer: Opaque pagination token. Pass the Next-Cursor header value to get the next page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/v1/sessions/{id}/events", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "compressed": compressed,
                        "limit": limit,
                        "pointer": pointer,
                    },
                    session_events_params.SessionEventsParams,
                ),
            ),
            cast_to=SessionEventsResponse,
        )

    async def hls(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncBinaryAPIResponse:
        """
        Get HLS playlist for a session recording using app auth or an RTC token

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/vnd.apple.mpegurl", **(extra_headers or {})}
        return await self._get(
            path_template("/v1/sessions/{id}/hls", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def live_details(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionLiveDetailsResponse:
        """
        Returns the live state of the session, including pages, tabs, and browser state

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/v1/sessions/{id}/live-details", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionLiveDetailsResponse,
        )

    async def logs(
        self,
        id: str,
        *,
        end_time: Union[str, datetime] | Omit = omit,
        event_types: SequenceNotStr[str] | Omit = omit,
        limit: int | Omit = omit,
        namespace: str | Omit = omit,
        offset: int | Omit = omit,
        start_time: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionLogsResponse:
        """
        Query browser event logs for a session

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/v1/sessions/{id}/logs", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "end_time": end_time,
                        "event_types": event_types,
                        "limit": limit,
                        "namespace": namespace,
                        "offset": offset,
                        "start_time": start_time,
                    },
                    session_logs_params.SessionLogsParams,
                ),
            ),
            cast_to=SessionLogsResponse,
        )

    async def release(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionReleaseResponse:
        """
        Releases a specific session by ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/v1/sessions/{id}/release", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionReleaseResponse,
        )

    async def release_all(
        self,
        *,
        project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionReleaseAllResponse:
        """
        Releases all active sessions for the current organization.

        Args:
          project_id: Release sessions only within this project

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/sessions/release",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"project_id": project_id}, session_release_all_params.SessionReleaseAllParams
                ),
            ),
            cast_to=SessionReleaseAllResponse,
        )

    async def replace_metadata(
        self,
        id: str,
        *,
        metadata: Dict[str, Union[str, float, bool]],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionReplaceMetadataResponse:
        """Atomically replace customer metadata.

        Send an empty object to clear it. Last
        accepted write wins; use PATCH to change individual keys. Subject to session
        organization and project access.

        Args:
          metadata: Customer-defined flat metadata: up to 50 keys and 8192 UTF-8 JSON bytes. Keys
              must start with a letter, use only letters, digits, underscores, dots or
              hyphens, and be at most 64 characters; steel\\__ is reserved. Values are strings
              (up to 1024 characters, valid Unicode without NUL), finite numbers or booleans.
              Numbers and booleans are stored as strings, so 3 and "3" are the same value.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._put(
            path_template("/v1/sessions/{id}/metadata", id=id),
            body=await async_maybe_transform(
                {"metadata": metadata}, session_replace_metadata_params.SessionReplaceMetadataParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionReplaceMetadataResponse,
        )

    async def signal_catalog(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionSignalCatalogResponse:
        """Returns current signal labels and meanings for customer integrations.

        Uses
        normal Steel API-key authentication. Includes no session data or administrative
        signals. Definitions do not establish that detection ran for a particular
        session.
        """
        return await self._get(
            "/v1/sessions/signals/catalog",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionSignalCatalogResponse,
        )

    async def update_metadata(
        self,
        id: str,
        *,
        metadata: Dict[str, Union[str, float, bool, None]],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionUpdateMetadataResponse:
        """Atomically merge keys into customer metadata.

        Set a key to null to remove it;
        keys you leave out are kept, so concurrent updates to different keys are all
        kept. Returns the merged metadata, which must stay within the metadata limits.
        Subject to session organization and project access.

        Args:
          metadata: Metadata keys to change, up to 100 per update. Keys follow the same rules as
              metadata keys. Send a string, finite number or boolean to set a key, or null to
              remove it; keys you leave out are kept. The merged metadata must stay within 50
              keys and 8192 UTF-8 JSON bytes.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._patch(
            path_template("/v1/sessions/{id}/metadata", id=id),
            body=await async_maybe_transform(
                {"metadata": metadata}, session_update_metadata_params.SessionUpdateMetadataParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionUpdateMetadataResponse,
        )


class SessionsResourceWithRawResponse:
    def __init__(self, sessions: SessionsResource) -> None:
        self._sessions = sessions

        self.create = to_raw_response_wrapper(
            sessions.create,
        )
        self.retrieve = to_raw_response_wrapper(
            sessions.retrieve,
        )
        self.list = to_raw_response_wrapper(
            sessions.list,
        )
        self.agent_traces = to_raw_response_wrapper(
            sessions.agent_traces,
        )
        self.commands = to_raw_response_wrapper(
            sessions.commands,
        )
        self.computer = to_raw_response_wrapper(
            sessions.computer,
        )
        self.context = to_raw_response_wrapper(
            sessions.context,
        )
        self.cost = to_raw_response_wrapper(
            sessions.cost,
        )
        self.events = to_raw_response_wrapper(
            sessions.events,
        )
        self.hls = to_custom_raw_response_wrapper(
            sessions.hls,
            BinaryAPIResponse,
        )
        self.live_details = to_raw_response_wrapper(
            sessions.live_details,
        )
        self.logs = to_raw_response_wrapper(
            sessions.logs,
        )
        self.release = to_raw_response_wrapper(
            sessions.release,
        )
        self.release_all = to_raw_response_wrapper(
            sessions.release_all,
        )
        self.replace_metadata = to_raw_response_wrapper(
            sessions.replace_metadata,
        )
        self.signal_catalog = to_raw_response_wrapper(
            sessions.signal_catalog,
        )
        self.update_metadata = to_raw_response_wrapper(
            sessions.update_metadata,
        )

    @cached_property
    def captchas(self) -> CaptchasResourceWithRawResponse:
        return CaptchasResourceWithRawResponse(self._sessions.captchas)

    @cached_property
    def files(self) -> FilesResourceWithRawResponse:
        return FilesResourceWithRawResponse(self._sessions.files)


class AsyncSessionsResourceWithRawResponse:
    def __init__(self, sessions: AsyncSessionsResource) -> None:
        self._sessions = sessions

        self.create = async_to_raw_response_wrapper(
            sessions.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            sessions.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            sessions.list,
        )
        self.agent_traces = async_to_raw_response_wrapper(
            sessions.agent_traces,
        )
        self.commands = async_to_raw_response_wrapper(
            sessions.commands,
        )
        self.computer = async_to_raw_response_wrapper(
            sessions.computer,
        )
        self.context = async_to_raw_response_wrapper(
            sessions.context,
        )
        self.cost = async_to_raw_response_wrapper(
            sessions.cost,
        )
        self.events = async_to_raw_response_wrapper(
            sessions.events,
        )
        self.hls = async_to_custom_raw_response_wrapper(
            sessions.hls,
            AsyncBinaryAPIResponse,
        )
        self.live_details = async_to_raw_response_wrapper(
            sessions.live_details,
        )
        self.logs = async_to_raw_response_wrapper(
            sessions.logs,
        )
        self.release = async_to_raw_response_wrapper(
            sessions.release,
        )
        self.release_all = async_to_raw_response_wrapper(
            sessions.release_all,
        )
        self.replace_metadata = async_to_raw_response_wrapper(
            sessions.replace_metadata,
        )
        self.signal_catalog = async_to_raw_response_wrapper(
            sessions.signal_catalog,
        )
        self.update_metadata = async_to_raw_response_wrapper(
            sessions.update_metadata,
        )

    @cached_property
    def captchas(self) -> AsyncCaptchasResourceWithRawResponse:
        return AsyncCaptchasResourceWithRawResponse(self._sessions.captchas)

    @cached_property
    def files(self) -> AsyncFilesResourceWithRawResponse:
        return AsyncFilesResourceWithRawResponse(self._sessions.files)


class SessionsResourceWithStreamingResponse:
    def __init__(self, sessions: SessionsResource) -> None:
        self._sessions = sessions

        self.create = to_streamed_response_wrapper(
            sessions.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            sessions.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            sessions.list,
        )
        self.agent_traces = to_streamed_response_wrapper(
            sessions.agent_traces,
        )
        self.commands = to_streamed_response_wrapper(
            sessions.commands,
        )
        self.computer = to_streamed_response_wrapper(
            sessions.computer,
        )
        self.context = to_streamed_response_wrapper(
            sessions.context,
        )
        self.cost = to_streamed_response_wrapper(
            sessions.cost,
        )
        self.events = to_streamed_response_wrapper(
            sessions.events,
        )
        self.hls = to_custom_streamed_response_wrapper(
            sessions.hls,
            StreamedBinaryAPIResponse,
        )
        self.live_details = to_streamed_response_wrapper(
            sessions.live_details,
        )
        self.logs = to_streamed_response_wrapper(
            sessions.logs,
        )
        self.release = to_streamed_response_wrapper(
            sessions.release,
        )
        self.release_all = to_streamed_response_wrapper(
            sessions.release_all,
        )
        self.replace_metadata = to_streamed_response_wrapper(
            sessions.replace_metadata,
        )
        self.signal_catalog = to_streamed_response_wrapper(
            sessions.signal_catalog,
        )
        self.update_metadata = to_streamed_response_wrapper(
            sessions.update_metadata,
        )

    @cached_property
    def captchas(self) -> CaptchasResourceWithStreamingResponse:
        return CaptchasResourceWithStreamingResponse(self._sessions.captchas)

    @cached_property
    def files(self) -> FilesResourceWithStreamingResponse:
        return FilesResourceWithStreamingResponse(self._sessions.files)


class AsyncSessionsResourceWithStreamingResponse:
    def __init__(self, sessions: AsyncSessionsResource) -> None:
        self._sessions = sessions

        self.create = async_to_streamed_response_wrapper(
            sessions.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            sessions.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            sessions.list,
        )
        self.agent_traces = async_to_streamed_response_wrapper(
            sessions.agent_traces,
        )
        self.commands = async_to_streamed_response_wrapper(
            sessions.commands,
        )
        self.computer = async_to_streamed_response_wrapper(
            sessions.computer,
        )
        self.context = async_to_streamed_response_wrapper(
            sessions.context,
        )
        self.cost = async_to_streamed_response_wrapper(
            sessions.cost,
        )
        self.events = async_to_streamed_response_wrapper(
            sessions.events,
        )
        self.hls = async_to_custom_streamed_response_wrapper(
            sessions.hls,
            AsyncStreamedBinaryAPIResponse,
        )
        self.live_details = async_to_streamed_response_wrapper(
            sessions.live_details,
        )
        self.logs = async_to_streamed_response_wrapper(
            sessions.logs,
        )
        self.release = async_to_streamed_response_wrapper(
            sessions.release,
        )
        self.release_all = async_to_streamed_response_wrapper(
            sessions.release_all,
        )
        self.replace_metadata = async_to_streamed_response_wrapper(
            sessions.replace_metadata,
        )
        self.signal_catalog = async_to_streamed_response_wrapper(
            sessions.signal_catalog,
        )
        self.update_metadata = async_to_streamed_response_wrapper(
            sessions.update_metadata,
        )

    @cached_property
    def captchas(self) -> AsyncCaptchasResourceWithStreamingResponse:
        return AsyncCaptchasResourceWithStreamingResponse(self._sessions.captchas)

    @cached_property
    def files(self) -> AsyncFilesResourceWithStreamingResponse:
        return AsyncFilesResourceWithStreamingResponse(self._sessions.files)
