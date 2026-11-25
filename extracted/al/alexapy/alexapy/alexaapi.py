"""Python Package for controlling Alexa devices (echo dot, etc) programmatically.

SPDX-License-Identifier: Apache-2.0

API access.

For more details about this api, please refer to the documentation at
https://gitlab.com/keatontaylor/alexapy
"""

import asyncio
import contextlib
import json
import logging
import math
import random
import time
import urllib.parse
from dataclasses import dataclass, field
from json.decoder import JSONDecodeError
from types import NoneType
from typing import Any, ClassVar, Literal

import backoff
from aiohttp import ClientConnectionError, ClientResponse
from yarl import URL

from .alexalogin import AlexaLogin
from .const import (
    ALEXA_API_BASE,
    DEFAULT_LOCALE,
    GQL_FORGET_ENDPOINT,
    GQL_SET_ENDPOINT_ENABLEMENT,
    GQL_SET_ENDPOINT_FRIENDLY_NAME,
    GQL_SMARTHOME_QUERY,
    GQL_SMARTHOME_QUERY_LEGACY,
    LOGIN_APP_VERSION,
    SKILLS_STORE_ACCEPT,
)
from .errors import (
    AlexapyConnectionError,
    AlexapyLoginCloseRequested,
    AlexapyLoginError,
    AlexapyTooManyRequestsError,
)
from .helpers import _catch_all_exceptions, get_json_value, hide_email, hide_serial
from .request import RequestProfile, send_request

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class HistoryContinuation:
    """Opaque, in-memory RVH cursor bound to one login/session and query."""

    start_time: int
    end_time: int
    max_record_size: int
    _login: object = field(repr=False)
    _session: object = field(repr=False)
    _domain: str = field(repr=False)
    _account: str = field(repr=False)
    _token: str = field(repr=False)
    _seen: frozenset[str] = field(repr=False)


@dataclass(frozen=True)
class HistoryPage:
    """Normalized page: success has a cursor, exhausted is final, error is incomplete.

    Transport authentication/rate-limit exceptions and cancellation propagate.
    Cursors must not be persisted or logged and must be discarded on reload.
    """

    records: list[dict[str, Any]]
    status: Literal["success", "exhausted", "error"]
    continuation: HistoryContinuation | None = None
    error: str | None = None


def _min_expo_wait(min_wait: float):
    """Exponential backoff with a specified minimum wait time."""

    def f(*args, **kwargs):
        gen = backoff.expo(*args, **kwargs)
        while True:
            v = next(gen, None)
            # _LOGGER.debug("_min_expo_wait: next(gen) was %s", v)
            v = min_wait if v is None else max(min_wait, v)
            # _LOGGER.debug("_min_expo_wait: returning %s",v)
            yield v

    return f


class AlexaAPI:
    """Class for accessing a specific Alexa device using rest API.

    Args:
    device (AlexaClient): Instance of an AlexaClient to access
    login (AlexaLogin): Successfully logged in AlexaLogin

    """

    devices: ClassVar[dict[str, Any]] = {}
    wake_words: ClassVar[dict[str, Any]] = {}
    _gql_legacy_accounts: ClassVar[set[str]] = set()
    _sequence_queue: ClassVar[dict[Any, list[dict[Any, Any]]]] = {}
    _sequence_lock: ClassVar[dict[Any, asyncio.Lock]] = {}

    def __init__(self, device, login: AlexaLogin):
        """Initialize Alexa device."""
        self._device = device
        self._login = login
        self._session = login.session
        self._url: str = "https://alexa." + login.url
        self._login._headers["Referer"] = f"{self._url}/spa/index.html"
        AlexaAPI._sequence_queue[self._login.email] = []
        AlexaAPI._sequence_lock[self._login.email] = asyncio.Lock()
        try:
            csrf = self._login._get_cookies_from_session()["csrf"]
            self._login._headers["csrf"] = csrf.value
        except KeyError as ex:
            _LOGGER.warning(
                (
                    "AlexaLogin session is missing required token: %s "
                    "This may result in authorization errors, please report if unable to login"  # noqa: E501
                ),
                ex,
            )

    def update_login(self, login: AlexaLogin) -> bool:
        """Update Login if it has changed.

        Args
            login (AlexaLogin): AlexaLogin to check

        Returns
            bool: True if change detected

        """
        if login != self._login or login.session != self._session:
            _LOGGER.debug(
                "%s: New Login %s detected; replacing %s",
                hide_email(login.email),
                login,
                self._login,
            )
            self._login = login
            self._session = login.session
            self._url: str = "https://alexa." + login.url
            self._login._headers["Referer"] = f"{self._url}/spa/index.html"
            try:
                csrf = self._login._get_cookies_from_session()["csrf"]
                self._login._headers["csrf"] = csrf.value
            except KeyError as ex:
                if login.status and login.status.get("login_successful"):
                    _LOGGER.warning(
                        (
                            "AlexaLogin session is missing required token: %s "
                            "This may result in authorization errors, please report"
                        ),
                        ex,
                    )
            return True
        return False

    @staticmethod
    async def _get_alexa_api_base(login: AlexaLogin) -> str:
        """Return the base URL for the Alexa REST API (e.g. https://na-api-alexa.amazon.com)."""
        # Cached?
        cached = getattr(login, "_alexa_api_url", None)
        if cached:
            _LOGGER.debug(
                "%s: Returning cached url: %s", hide_email(login.email), cached
            )
            return cached

        session = login.session
        if session.closed:
            raise AlexapyLoginError("Session is closed")

        # Try /api/endpoints on the web host, e.g. https://alexa.amazon.ca/api/endpoints
        # login.url is usually 'amazon.ca' or 'amazon.com'
        endpoints_url = URL(f"https://alexa.{login.url}/api/endpoints")

        try:
            resp = await send_request(
                session, "get", endpoints_url, login, RequestProfile.DISCOVERY
            )
            text = await resp.text()
            _LOGGER.debug(
                "%s: /api/endpoints GET %s returned %s:%s:%s",
                hide_email(login.email),
                endpoints_url,
                resp.status,
                resp.reason,
                resp.content_type,
            )
            if resp.status == 200:
                try:
                    data = json.loads(text)
                    api_url = (
                        data.get("websiteApiUrl") if isinstance(data, dict) else None
                    )
                    if isinstance(api_url, str) and api_url.rstrip("/"):
                        login._alexa_api_url = api_url.rstrip("/")
                        _LOGGER.debug(
                            "%s: Using websiteApiUrl from /api/endpoints: %s",
                            hide_email(login.email),
                            api_url,
                        )
                        return login._alexa_api_url
                    else:
                        _LOGGER.debug(
                            "%s: Unable to extract websiteApiUrl from /api/endpoints",
                            hide_email(login.email),
                        )
                except ValueError:
                    _LOGGER.debug(
                        "%s: /api/endpoints returned invalid JSON",
                        hide_email(login.email),
                    )
        except ClientConnectionError as exc:
            _LOGGER.debug(
                "%s: /api/endpoints connection error: %s",
                hide_email(login.email),
                exc,
            )

        # Fallback: use region-based default, then web host as last resort
        domain = getattr(login, "url", "")  # e.g. 'amazon.ca'
        suffix = domain.lower().removeprefix("amazon")
        api_base = ALEXA_API_BASE.get(suffix)
        if not api_base:
            api_base = f"https://alexa.{domain}"

        login._alexa_api_url = api_base.rstrip("/")
        _LOGGER.debug(
            "%s: Falling back to default alexa API base: %s",
            hide_email(login.email),
            login._alexa_api_url,
        )
        return login._alexa_api_url

    @classmethod
    async def _process_response(
        cls, response: ClientResponse, login: AlexaLogin
    ) -> ClientResponse | None:
        """Process a response from _request or static_request.

        Args:
            ClientResponse (response): Response from _request

        Returns:
            None | ClientResponse: Response from server
        """
        if login.stats:
            login.stats["api_calls"] += 1
            _LOGGER.debug("api_calls: %s", login.stats["api_calls"])
        if response.status == 401:
            if login.status:
                login.status["login_successful"] = False
            raise AlexapyLoginError(response.reason)
        if response.status == 429:
            raise AlexapyTooManyRequestsError(response.reason)
        if response.status >= 400:
            _LOGGER.debug("Returning None due to status: %s", response.status)
            return None
        return response

    @staticmethod
    async def _refresh_csrf_overrides(
        login: AlexaLogin, url: URL, headers: dict[str, str] | None
    ) -> dict[str, str] | None:
        """Rebuild endpoint-specific CSRF overrides after reauthentication."""
        if not headers:
            return headers

        refreshed = headers.copy()
        for name in headers:
            if name.lower() == "anti-csrftoken-a2z":
                token = await login.get_csrf_token()
            elif name.lower() == "x-amzn-csrf":
                cookies = login._get_cookies_from_session(url.host or "")
                cookie = cookies.get("ft-panda-csrf-token")
                token = cookie.value if cookie else None
            else:
                continue

            if token:
                refreshed[name] = token
            else:
                # Let the rebuilt session supply any current header value.
                refreshed.pop(name)

        return refreshed

    @backoff.on_exception(
        _min_expo_wait(random.uniform(0.5, 1.5)),
        (AlexapyTooManyRequestsError, AlexapyConnectionError, ClientConnectionError),
        max_time=90,
        max_tries=10,
        jitter=None,
        # factor = 2,
        logger=__name__,
    )
    async def _request(
        self,
        method: str,
        uri: str,
        data: dict[str, str] | None = None,
        query: dict[str, str | int] | None = None,
    ) -> ClientResponse | None:
        await self._login._refresh_session_if_expired()
        if method == "get":
            if query and not query.get("_"):
                query["_"] = math.floor(time.time() * 1000)
            elif query is None:
                query = {"_": math.floor(time.time() * 1000)}
        url: URL = URL(self._url + uri).update_query(query)
        _LOGGER.debug(
            "%s: Trying %s: %s : with uri: %s data %s query %s",
            hide_email(self._login.email),
            method,
            url,
            uri,
            data,
            query,
        )
        if self._login.close_requested:
            _LOGGER.debug(
                "%s: Login object has been asked to close; ignoring %s request to %s with %s %s",  # noqa: E501
                hide_email(self._login.email),
                method,
                uri,
                data,
                query,
            )
            raise AlexapyLoginCloseRequested()
        if self._login.status and not self._login.status.get("login_successful"):
            _LOGGER.debug(
                "%s:Login error detected; ignoring %s request to %s with %s %s",
                hide_email(self._login.email),
                method,
                uri,
                data,
                query,
            )
            raise AlexapyLoginError("Login error detected; not contacting API")
        if self._session and self._session.closed:
            raise AlexapyLoginError("Session is closed")
        response = await send_request(
            self._session, method, url, self._login, RequestProfile.WEB_API, data=data
        )
        _LOGGER.debug(
            "%s: %s: %s returned %s:%s:%s",
            hide_email(self._login.email),
            response.request_info.method,
            response.request_info.url,
            response.status,
            response.reason,
            response.content_type,
        )
        return await self._process_response(response, self._login)

    async def _post_request(
        self,
        uri: str,
        data: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
    ) -> ClientResponse | None:
        return await self._request("post", uri, data, query)

    async def _put_request(
        self,
        uri: str,
        data: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
    ) -> ClientResponse | None:
        return await self._request("put", uri, data, query)

    async def _get_request(
        self,
        uri: str,
        data: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
    ) -> ClientResponse | None:
        return await self._request("get", uri, data, query)

    async def _del_request(
        self,
        uri: str,
        data: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
    ) -> ClientResponse | None:
        return await self._request("delete", uri, data, query)

    @staticmethod
    @backoff.on_exception(
        _min_expo_wait(random.uniform(0.8, 1.8)),
        (AlexapyTooManyRequestsError, AlexapyConnectionError, ClientConnectionError),
        max_time=120,
        max_tries=10,
        jitter=None,
        # factor = 2,
        logger=__name__,
    )
    async def _static_request(
        method: str,
        login: AlexaLogin,
        uri: str,
        data: dict[str, str | dict] | None = None,
        additional_headers: dict[str, str] | None = None,
        query: dict[str, str | int] | None = None,
        sub_domain: str = "alexa",
        with_status: bool = False,
    ) -> tuple[int, ClientResponse] | ClientResponse | None:
        await login._refresh_session_if_expired()
        session = login.session
        url: URL = URL("https://" + sub_domain + "." + login.url + uri).update_query(
            query
        )
        # _LOGGER.debug("%s: %s: Trying static %s: %s : with uri: %s data %s query %s",
        #                hide_email(login.email)
        #                method,
        #                url,
        #                uri,
        #                data,
        #                query,
        #            )
        if login.close_requested:
            _LOGGER.debug(
                "%s: Login object has been asked to close; ignoring %s request to %s with %s %s",  # noqa: E501
                hide_email(login.email),
                method,
                uri,
                data,
                query,
            )
            raise AlexapyLoginCloseRequested()
        if login.status and not login.status.get("login_successful"):
            _LOGGER.debug(
                "%s: Login error detected; ignoring %s request to %s with %s %s",
                hide_email(login.email),
                method,
                uri,
                data,
                query,
            )
            raise AlexapyLoginError("Login error detected; not contacting API")
        if session and session.closed:
            raise AlexapyLoginError("Session is closed")
        profile = (
            RequestProfile.WEB_API
            if sub_domain == "alexa"
            else RequestProfile.AUXILIARY_API
        )
        response = await send_request(
            session,
            method,
            url,
            login,
            profile,
            data=data,
            overrides=additional_headers,
        )
        _LOGGER.debug(
            "%s: static %s %s returned %s:%s:%s",
            hide_email(login.email),
            response.request_info.method,
            response.request_info.url,
            response.status,
            response.reason,
            response.content_type,
        )

        if response.status == 401 and await login.test_loggedin():
            additional_headers = await AlexaAPI._refresh_csrf_overrides(
                login, url, additional_headers
            )
            response = await send_request(
                login.session,
                method,
                url,
                login,
                profile,
                data=data,
                overrides=additional_headers,
            )
            _LOGGER.debug(
                "Error 401, retried once request: %s: static %s: %s returned %s:%s:%s",
                hide_email(login.email),
                response.request_info.method,
                response.request_info.url,
                response.status,
                response.reason,
                response.content_type,
            )

        # ★★★ Error body logger + basic throttling retry ★★★
        if response.status >= 400:
            try:
                body = await response.text()
            except Exception:
                body = "<unable to read body>"

            _LOGGER.debug(
                "HTTP static %s %s returned %s:%s; content_type=%s, body: %s",
                hide_email(login.email),
                response.request_info.url,
                response.status,
                response.reason,
                response.content_type,
                hide_serial(body),
            )

            # Simple, alexa-remote-style throttle handling
            if (
                response.status in (400, 429)
                and isinstance(body, str)
                and any(
                    marker in body
                    for marker in (
                        "Rate exceeded",
                        "ThrottlingException",
                        "Too many requests",
                    )
                )
                and not getattr(login, "_rate_retry_inflight", False)
            ):
                # Choose a delay similar to alexa-remote.js
                delay = random.uniform(10.0, 13.0)
                if "Too many requests" in body:
                    delay += 20.0 + random.uniform(0.0, 30.0)

                _LOGGER.debug(
                    "%s: Throttled (%s); retrying static %s %s once in %.1fs",
                    hide_email(login.email),
                    body,
                    method,
                    url,
                    delay,
                )

                # Prevent concurrent mass retries on the same login
                login._rate_retry_inflight = True
                try:
                    await asyncio.sleep(delay)
                    return await AlexaAPI._static_request(
                        method,
                        login,
                        uri,
                        data=data,
                        additional_headers=additional_headers,
                        query=query,
                        sub_domain=sub_domain,
                        with_status=with_status,
                    )
                finally:
                    login._rate_retry_inflight = False

        if with_status:
            if response.status == 401:
                # A 401 that survives the retry is a login failure, not a status.
                return await AlexaAPI._process_response(response, login)
            if login.stats:
                login.stats["api_calls"] += 1
            return response.status, response
        return await AlexaAPI._process_response(response, login)

    @_catch_all_exceptions
    async def run_behavior(
        self,
        node_data,
        queue_delay: float = 1.5,
    ) -> None:
        """Queue node_data for running a behavior in sequence.

        Amazon sequences and routines are based on node_data.

        Args:
            node_data (dict, list of dicts): The node_data to run.
            queue_delay (float, optional): The number of seconds to wait
                                          for commands to queue together.
                                          Defaults to 1.5.
                                          Must be positive.

        """
        sequence_json: dict[Any, Any] = {
            "@type": "com.amazon.alexa.behaviors.model.Sequence",
            "startNode": node_data,
        }
        if queue_delay is None:
            queue_delay = 1.5
        if queue_delay > 0:
            sequence_json["startNode"] = {
                "@type": "com.amazon.alexa.behaviors.model.SerialNode",
                "nodesToExecute": [],
            }
            async with AlexaAPI._sequence_lock[self._login.email]:
                if AlexaAPI._sequence_queue[self._login.email]:
                    last_node = AlexaAPI._sequence_queue[self._login.email][-1]
                    new_node = node_data
                    if node_data and isinstance(node_data, list):
                        new_node = node_data[0]
                    if (
                        last_node.get("operationPayload", {}).get("deviceSerialNumber")
                        and new_node.get("operationPayload", {}).get(
                            "deviceSerialNumber"
                        )
                    ) and last_node.get("operationPayload", {}).get(
                        "deviceSerialNumber"
                    ) != new_node.get("operationPayload", {}).get("deviceSerialNumber"):
                        _LOGGER.debug(
                            "%s: Creating Parallel node",
                            hide_email(self._login.email),
                        )
                        sequence_json["startNode"]["@type"] = (
                            "com.amazon.alexa.behaviors.model.ParallelNode"
                        )
                if isinstance(node_data, list):
                    AlexaAPI._sequence_queue[self._login.email].extend(node_data)
                else:
                    AlexaAPI._sequence_queue[self._login.email].append(node_data)
                items = len(AlexaAPI._sequence_queue[self._login.email])
                old_sequence: list[dict[Any, Any]] = AlexaAPI._sequence_queue[
                    self._login.email
                ]
            await asyncio.sleep(queue_delay)
            async with AlexaAPI._sequence_lock[self._login.email]:
                if (
                    items == len(AlexaAPI._sequence_queue[self._login.email])
                    and old_sequence == AlexaAPI._sequence_queue[self._login.email]
                ):
                    sequence_json["startNode"]["nodesToExecute"].extend(
                        AlexaAPI._sequence_queue[self._login.email]
                    )
                    AlexaAPI._sequence_queue[self._login.email] = []
                    _LOGGER.debug(
                        "%s: Creating sequence for %s items",
                        hide_email(self._login.email),
                        items,
                    )
                else:
                    _LOGGER.debug(
                        "%s: Queue changed while waiting %s seconds",
                        hide_email(self._login.email),
                        queue_delay,
                    )
                    return
        data = {
            "behaviorId": "PREVIEW",
            "sequenceJson": json.dumps(sequence_json),
            "status": "ENABLED",
        }
        _LOGGER.debug(
            "%s: Running behavior with data: %s",
            hide_email(self._login.email),
            json.dumps(data),
        )
        await self._post_request("/api/behaviors/preview", data=data)

    @_catch_all_exceptions
    async def send_sequence(
        self,
        sequence: str,
        customer_id: str | None = None,
        queue_delay: float = 1.5,
        extra: dict[Any, Any] | None = None,
        **kwargs,
    ) -> None:
        """Send sequence command.

        This allows some programmatic control of Echo device using the behaviors
        API and is the basis of play_music, send_announcement, and send_tts.

        Args:
        sequence (string): The Alexa sequence.  Supported list below.
        customer_id (string): CustomerId to use for authorization. When none
                             specified this defaults to the logged in user. Used
                             with households where others may have their own
                             music.
        queue_delay (float, optional): The number of seconds to wait
                                    for commands to queue together.
                                    Defaults to 1.5.
                                    Must be positive.
        extra (Dict): Extra dictionary array; functionality undetermined
        **kwargs : Each named variable must match a recognized Amazon variable
                   within the operationPayload. Please see examples in
                   play_music, send_announcement, and send_tts.
                   Variables with value None are removed from the operationPayload.
                   Variables prefixed with "root_" will be added to the root node instead.

        Supported sequences:
        Alexa.Weather.Play
        Alexa.Traffic.Play
        Alexa.FlashBriefing.Play
        Alexa.GoodMorning.Play
        Alexa.GoodNight.Play
        Alexa.SingASong.Play
        Alexa.TellStory.Play
        Alexa.FunFact.Play
        Alexa.Joke.Play
        Alexa.CleanUp.Play
        Alexa.Music.PlaySearchPhrase
        Alexa.Calendar.PlayTomorrow
        Alexa.Calendar.PlayToday
        Alexa.Calendar.PlayNext
        https://github.com/custom-components/alexa_media_player/wiki#sequence-commands-versions--100

        """  # noqa: E501
        extra = extra or {}
        operation_payload = {
            "deviceType": self._device._device_type,
            "deviceSerialNumber": self._device.device_serial_number,
            "locale": (
                self._device._locale if self._device._locale else DEFAULT_LOCALE
            ),
            "customerId": (
                self._login.customer_id if customer_id is None else customer_id
            ),
        }
        root_node = {}
        if kwargs is not None:
            operation_payload.update(kwargs)
            for key, value in kwargs.items():
                if value is None:  # remove null keys
                    operation_payload.pop(key)
                elif isinstance(value, str) and value.startswith("root_"):
                    operation_payload.pop(key)
                    root_node[key] = value[5:]
            if kwargs.get("devices"):
                operation_payload.pop("deviceType")
                operation_payload.pop("deviceSerialNumber")
        node_data = {
            "@type": "com.amazon.alexa.behaviors.model.OpaquePayloadOperationNode",
            "type": sequence,
            "operationPayload": operation_payload,
        }
        node_data.update(root_node)
        await self.run_behavior(node_data, queue_delay=queue_delay)

    @_catch_all_exceptions
    async def run_skill(
        self,
        skill_id: str,
        customer_id: str | None = None,
        queue_delay: float = 0,
    ) -> None:
        """Run Alexa skill.

        This allows running of defined Alexa skill.

        Args:
            skill_id (string): The full skill id.
            customer_id (string): CustomerId to use for authorization. When none
                             specified this defaults to the logged in user. Used
                             with households where others may have their own
                             music.
            queue_delay (float, optional): The number of seconds to wait
                                        for commands to queue together.
                                        Defaults to 1.5.
                                        Must be positive.

        """
        operation_payload = {
            "targetDevice": {
                "deviceType": self._device._device_type,
                "deviceSerialNumber": self._device.device_serial_number,
            },
            "locale": (
                self._device._locale if self._device._locale else DEFAULT_LOCALE
            ),
            "customerId": (
                self._login.customer_id if customer_id is None else customer_id
            ),
            "connectionRequest": {
                "uri": "connection://AMAZON.Launch/" + skill_id,
                "input": {},
            },
        }
        node_data = {
            "@type": "com.amazon.alexa.behaviors.model.OpaquePayloadOperationNode",
            "type": "Alexa.Operation.SkillConnections.Launch",
            "operationPayload": operation_payload,
        }
        await self.run_behavior(node_data, queue_delay=queue_delay)

    @_catch_all_exceptions
    async def run_custom(
        self,
        text: str,
        customer_id: str | None = None,
        queue_delay: float = 0,
        extra: dict[Any, Any] | None = None,
    ) -> None:
        """Run Alexa skill.

        This allows running exactly what you can say to alexa.

        Args:
            text (string): The full text you want alexa to execute.
            customer_id (string): CustomerId to use for authorization. When none
                             specified this defaults to the logged in user. Used
                             with households where others may have their own
                             music.
            queue_delay (float, optional): The number of seconds to wait
                                        for commands to queue together.
                                        Defaults to 1.5.
                                        Must be positive.
            extra (Dict): Extra dictionary array; functionality undetermined

        """
        extra = extra or {}
        await self.send_sequence(
            "Alexa.TextCommand",
            skillId="amzn1.ask.1p.tellalexa",
            text=text,
            queue_delay=queue_delay,
        )

    @_catch_all_exceptions
    async def run_routine(
        self,
        utterance: str,
        customer_id: str | None = None,
        queue_delay: float = 1.5,
    ) -> None:
        """Run Alexa automation routine.

        This allows running of defined Alexa automation routines.

        Args:
            utterance (string):
                The Alexa routine name or its voice utterance to run the routine.
            customer_id (string):
                CustomerId to use for authorization.
                When none specified this defaults to the logged in user.
                Used with households where others may have their own music.
            queue_delay (float, optional):
                The number of seconds to wait for commands to queue together.
                Defaults to 1.5.
                Must be positive.

        """

        def _populate_device_info(node) -> None:
            """Walk node structure and replace ALEXA_CURRENT_* placeholders."""
            if node is None:
                return

            if isinstance(node, list):
                for item in node:
                    _populate_device_info(item)
                return

            if not isinstance(node, dict):
                return

            if node.get("deviceType") == "ALEXA_CURRENT_DEVICE_TYPE":
                node["deviceType"] = self._device._device_type
            if node.get("deviceSerialNumber") == "ALEXA_CURRENT_DSN":
                node["deviceSerialNumber"] = self._device.device_serial_number
            if node.get("locale") == "ALEXA_CURRENT_LOCALE":
                node["locale"] = self._device._locale or DEFAULT_LOCALE

            for v in node.values():
                if isinstance(v, (dict, list)):
                    _populate_device_info(v)

        # Fetch automations (routines)
        if not (automations := await AlexaAPI.get_automations(self._login)):
            return

        utterance_cf = utterance.casefold()
        automation_id = None
        sequence = None

        for automation in automations:
            if not isinstance(automation, dict):
                continue

            # 1) Name match first (covers device-trigger routines)
            if (
                isinstance(name := automation.get("name"), str)
                and name.casefold() == utterance_cf
            ):
                automation_id = automation.get("automationId")
                seq = automation.get("sequence")
                sequence = seq if isinstance(seq, dict) else None
                break

            # 2) Fallback: spoken utterance match (CustomUtterance only)
            if not (
                isinstance(triggers := automation.get("triggers"), list)
                and triggers
                and isinstance(triggers[0], dict)
                and triggers[0].get("type") == "CustomUtterance"
                and isinstance(payload := triggers[0].get("payload"), dict)
            ):
                continue

            if (
                isinstance(u := payload.get("utterance"), str)
                and u.casefold() == utterance_cf
            ) or (
                isinstance(utterances := payload.get("utterances"), list)
                and any(
                    isinstance(x, str) and x.casefold() == utterance_cf
                    for x in utterances
                )
            ):
                automation_id = automation.get("automationId")
                seq = automation.get("sequence")
                sequence = seq if isinstance(seq, dict) else None
                break

        if automation_id is None or sequence is None:
            _LOGGER.debug(
                "%s: No routine found for %s",
                hide_email(self._login.email),
                utterance,
            )
            return

        if not isinstance(start_node := sequence.get("startNode"), dict):
            _LOGGER.debug(
                "%s: Routine %s found for %s, but sequence.startNode is "
                "missing/invalid",
                hide_email(self._login.email),
                automation_id,
                utterance,
            )
            return

        _populate_device_info(start_node)

        nodes = start_node.get("nodesToExecute")
        await self.run_behavior(
            nodes if isinstance(nodes, list) else start_node,
            queue_delay=queue_delay,
        )

    @_catch_all_exceptions
    async def play_music(
        self,
        provider_id: str,
        search_phrase: str,
        customer_id: str | None = None,
        timer: int | None = None,
        queue_delay: float = 1.5,
        extra: dict[Any, Any] | None = None,
    ) -> None:
        """Play music based on search.

        Args:
            provider_id (str): Amazon music provider.
            search_phrase (str): Phrase to be searched for
            customer_id (Optional[str], optional): CustomerId to use for authorization. When none
                             specified this defaults to the logged in user. Used
                             with households where others may have their own
                             music.
            timer (Optional[int]): Number of seconds to play before stopping.
            queue_delay (float, optional): The number of seconds to wait
                                   for commands to queue together.
                                   Must be positive. Defaults to 1.5.
            extra (Dict): Extra dictionary array; functionality undetermined

        """  # noqa: E501
        extra = extra or {}
        customer_id = self._login.customer_id if customer_id is None else customer_id
        if timer:
            await self.send_sequence(
                "Alexa.Music.PlaySearchPhrase",
                customer_id=customer_id,
                searchPhrase=search_phrase,
                sanitizedSearchPhrase=search_phrase,
                musicProviderId=provider_id,
                waitTimeInSeconds=timer,
                queue_delay=queue_delay,
            )
        else:
            await self.send_sequence(
                "Alexa.Music.PlaySearchPhrase",
                customer_id=customer_id,
                searchPhrase=search_phrase,
                sanitizedSearchPhrase=search_phrase,
                musicProviderId=provider_id,
                queue_delay=queue_delay,
            )

    @_catch_all_exceptions
    async def play_sound(
        self,
        sound_string_id: str,
        customer_id: str | None = None,
        queue_delay: float = 1.5,
        extra: dict[Any, Any] | None = None,
    ) -> None:
        """Play Alexa sound."""
        extra = extra or {}
        await self.send_sequence(
            "Alexa.Sound",
            customer_id=self._login.customer_id if customer_id is None else customer_id,
            soundStringId=sound_string_id,
            skillId="amzn1.ask.1p.sound",
            queue_delay=queue_delay,
        )

    @_catch_all_exceptions
    async def stop(
        self,
        customer_id: str | None = None,
        queue_delay: float = 1.5,
        all_devices: bool = False,
    ) -> None:
        """Stop device playback.

        Keyword Arguments:
            customer_id {str} -- CustomerId issuing command (default: {None})
            queue_delay {float} -- The number of seconds to wait
                                   for commands to queue together.
                                   Must be positive.
                                   (default: {1.5})
            all_devices {bool} -- Whether all devices should be stopped (default: {False})

        """  # noqa: E501
        kwargs = {}

        if all_devices:
            kwargs["devices"] = (
                {
                    "deviceType": "ALEXA_ALL_DEVICE_TYPE",
                    "deviceSerialNumber": "ALEXA_ALL_DSN",
                },
            )
        else:
            kwargs["devices"] = [
                {
                    "deviceSerialNumber": self._device.device_serial_number,
                    "deviceType": self._device._device_type,
                },
            ]

        await self.send_sequence(
            "Alexa.DeviceControls.Stop",
            skillId="amzn1.ask.1p.alexadevicecontrols",
            customer_id=self._login.customer_id if customer_id is None else customer_id,
            queue_delay=queue_delay,
            **kwargs,
        )

    def process_targets(self, targets: list[str] | None = None) -> list[dict[str, str]]:
        """Process targets list to generate list of devices.

        Keyword Arguments
            targets {Optional[List[str]]} -- List of serial numbers
                (default: {[]})

        Returns
            List[Dict[str, str] -- List of device dicts

        """
        targets = targets or []
        devices = []
        if self._device._device_family == "WHA":
            # Build group of devices based off _cluster_members
            for dev in AlexaAPI.devices[self._login.email]:
                if dev["serialNumber"] in self._device._cluster_members:
                    devices.append(
                        {
                            "deviceSerialNumber": dev["serialNumber"],
                            "deviceTypeId": dev["deviceType"],
                        }
                    )
        elif targets and isinstance(targets, list):
            for dev in AlexaAPI.devices[self._login.email]:
                if dev["serialNumber"] in targets or dev["accountName"] in targets:
                    devices.append(
                        {
                            "deviceSerialNumber": dev["serialNumber"],
                            "deviceTypeId": dev["deviceType"],
                        }
                    )
        else:
            devices.append(
                {
                    "deviceSerialNumber": self._device.device_serial_number,
                    "deviceTypeId": self._device._device_type,
                }
            )
        return devices

    @_catch_all_exceptions
    async def send_tts(
        self,
        message: str,
        customer_id: str | None = None,
        targets: list[str] | None = None,
        queue_delay: float = 1.5,
    ) -> None:
        """Send message for TTS at speaker.

        This is the old method which used Alexa Simon Says which did not work
        for WHA. This will not beep prior to sending. send_announcement
        should be used instead.

        Args:
        message (string): The message to speak. For canned messages, the message
                            must start with `alexa.cannedtts.speak` as discovered
                            in the routines.
        customer_id (string): CustomerId to use for authorization. When none
                             specified this defaults to the logged in user. Used
                             with households where others may have their own
                             music.
        targets (list(string)): WARNING: This is currently non functional due
                                to Alexa's API and is only included for future
                                proofing.
                                List of serialNumber or accountName to send the
                                tts to. Only those in this AlexaAPI
                                account will be searched. If None, announce
                                will be self.
        queue_delay (float, optional): The number of seconds to wait
                                          for commands to queue together.
                                          Defaults to 1.5.
                                          Must be positive.

        """
        if message.startswith("alexa.cannedtts.speak"):
            await self.send_sequence(
                "Alexa.CannedTts.Speak",
                customer_id=(
                    self._login.customer_id if customer_id is None else customer_id
                ),
                cannedTtsStringId=message,
                skillId="amzn1.ask.1p.saysomething",
                queue_delay=queue_delay,
            )
        else:
            target = {
                "customerId": (
                    self._login.customer_id if customer_id is None else customer_id
                ),
                "devices": self.process_targets(targets),
            }
            await self.send_sequence(
                "Alexa.Speak",
                customer_id=(
                    self._login.customer_id if customer_id is None else customer_id
                ),
                textToSpeak=message,
                target=target,
                skillId="amzn1.ask.1p.saysomething",
                queue_delay=queue_delay,
            )

    @_catch_all_exceptions
    async def send_announcement(
        self,
        message: str,
        method: str = "all",
        title: str = "Announcement",
        customer_id: str | None = None,
        targets: list[str] | None = None,
        queue_delay: float = 1.5,
        extra: dict[Any, Any] | None = None,
    ) -> None:
        """Send announcement to Alexa devices.

        This uses the AlexaAnnouncement and allows visual display on the Show.
        It will beep prior to speaking.

        Args:
        message (string): The message to speak or display.
        method (string): speak, show, or all
        title (string): title to display on Echo show
        customer_id (string): CustomerId to use for authorization. When none
                             specified this defaults to the logged in user. Used
                             with households where others may have their own
                             music.
        targets (list(string)): List of serialNumber or accountName to send the
                                announcement to. Only those in this AlexaAPI
                                account will be searched. If None, announce
                                will be self.
        queue_delay (float, optional): The number of seconds to wait
                                        for commands to queue together.
                                        Defaults to 1.5.
                                        Must be positive.
        extra (Dict): Extra dictionary array; functionality undetermined

        """
        extra = extra or {}
        display = (
            {"title": "", "body": ""}
            if method.lower() == "speak"
            else {"title": title, "body": message}
        )
        speak = (
            {"type": "text", "value": ""}
            if method.lower() == "show"
            else {"type": "text", "value": message}
        )
        content = [
            {
                "locale": (
                    self._device._locale if self._device._locale else DEFAULT_LOCALE
                ),
                "display": display,
                "speak": speak,
            }
        ]
        target = {
            "customerId": (
                self._login.customer_id if customer_id is None else customer_id
            ),
            "devices": self.process_targets(targets),
        }
        await self.send_sequence(
            "AlexaAnnouncement",
            customer_id=self._login.customer_id if customer_id is None else customer_id,
            expireAfter="PT5S",
            content=content,
            target=target,
            skillId="amzn1.ask.1p.routines.messaging",
            queue_delay=queue_delay,
        )

    @_catch_all_exceptions
    async def send_mobilepush(
        self,
        message: str,
        title: str = "AlexaAPI Message",
        customer_id: str | None = None,
        queue_delay: float = 1.5,
        extra: dict[Any, Any] | None = None,
    ) -> None:
        """Send mobile push to Alexa app.

        Push a message to mobile devices with the Alexa App. This probably
        should be a static method.

        Args:
        message (string): The message to push to the mobile device.
        title (string): Title for push notification
        customer_id (string): CustomerId to use for sending. When none
                              specified this defaults to the logged in user.
        queue_delay (float, optional): The number of seconds to wait
                                        for commands to queue together.
                                        Defaults to 1.5.
                                        Must be positive.
        extra (Dict): Extra dictionary array; functionality undetermined

        """
        extra = extra or {}
        await self.send_sequence(
            "Alexa.Notifications.SendMobilePush",
            customer_id=(
                self._login.customer_id if customer_id is None else customer_id
            ),
            notificationMessage=message,
            alexaUrl="#v2/behaviors",
            title=title,
            skillId="amzn1.ask.1p.routines.messaging",
            queue_delay=queue_delay,
        )

    @_catch_all_exceptions
    async def send_dropin_notification(
        self,
        message: str,
        title: str = "AlexaAPI Dropin Notification",
        customer_id: str | None = None,
        queue_delay: float = 1.5,
        extra: dict[Any, Any] | None = None,
    ) -> None:
        """Send dropin notification to Alexa app for Alexa device.

        Push a message to mobile devices with the Alexa App. This can spawn a
        notification to drop in on a specific device.

        Args:
        message (string): The message to push to the mobile device.
        title (string): Title for push notification
        customer_id (string): CustomerId to use for sending. When none
                              specified this defaults to the logged in user.
        queue_delay (float, optional): The number of seconds to wait
                                        for commands to queue together.
                                        Defaults to 1.5.
                                        Must be positive.
        extra (Dict): Extra dictionary array; functionality undetermined

        """
        extra = extra or {}
        await self.send_sequence(
            "Alexa.Notifications.DropIn",
            customer_id=(
                self._login.customer_id if customer_id is None else customer_id
            ),
            notificationMessage=message,
            alexaUrl="#v2/comms/conversation-list?showDropInDialog=true",
            title=title,
            skillId="root_amzn1.ask.1p.action.dropin",
            queue_delay=queue_delay,
            deviceType=None,
            deviceSerialNumber=None,
            locale=None,
        )

    async def set_media(self, data: dict[str, Any]) -> None:
        """Select the media player."""
        await self._post_request(
            "/api/np/command",
            data=data,
            query={
                "deviceSerialNumber": self._device.device_serial_number,
                "deviceType": self._device._device_type,
            },
        )

    @_catch_all_exceptions
    async def previous(self) -> None:
        """Play previous."""
        await self.set_media({"type": "PreviousCommand"})

    @_catch_all_exceptions
    async def next(self) -> None:
        """Play next."""
        await self.set_media({"type": "NextCommand"})

    @_catch_all_exceptions
    async def pause(self) -> None:
        """Pause."""
        await self.set_media({"type": "PauseCommand"})

    @_catch_all_exceptions
    async def play(self) -> None:
        """Play."""
        await self.set_media({"type": "PlayCommand"})

    @_catch_all_exceptions
    async def forward(self) -> None:
        """Fastforward."""
        await self.set_media({"type": "ForwardCommand"})

    @_catch_all_exceptions
    async def rewind(self) -> None:
        """Rewind."""
        await self.set_media({"type": "RewindCommand"})

    @_catch_all_exceptions
    async def set_volume(
        self,
        volume: float,
        customer_id: str | None = None,
        queue_delay: float = 1.5,
    ) -> None:
        """Set volume.

        Args:
        volume (float): The volume between 0 and 1.
        customer_id (string): CustomerId to use for sending. When none
                              specified this defaults to the logged in user.
        queue_delay (float, optional): The number of seconds to wait
                                        for commands to queue together.
                                        Defaults to 1.5.
                                        Must be positive.

        """
        await self.send_sequence(
            "Alexa.DeviceControls.Volume",
            customer_id=(
                self._login.customer_id if customer_id is None else customer_id
            ),
            value=volume * 100,
            queue_delay=queue_delay,
        )

    @_catch_all_exceptions
    async def shuffle(self, setting: bool) -> None:
        """Shuffle.

        setting (string) : true or false
        """
        await self.set_media({"type": "ShuffleCommand", "shuffle": setting})

    @_catch_all_exceptions
    async def repeat(self, setting: bool) -> None:
        """Repeat.

        setting (string) : true or false
        """
        await self.set_media({"type": "RepeatCommand", "repeat": setting})

    @_catch_all_exceptions
    async def get_state(self) -> dict[str, Any] | None:
        """Get playing state."""
        response = await self._get_request(
            "/api/np/player",
            query={
                "deviceSerialNumber": self._device.device_serial_number,
                "deviceType": self._device._device_type,
                "screenWidth": 2560,
            },
        )
        response_json, *_ = await get_json_value(response, None, dict)
        return response_json

    @_catch_all_exceptions
    async def get_wifi_details(self) -> dict[str, Any] | None:
        """Get wifi details."""
        response = await self._get_request(
            "/api/device-wifi-details",
            query={
                "deviceSerialNumber": self._device.device_serial_number,
                "deviceType": self._device._device_type,
            },
        )
        response_json, *_ = await get_json_value(response, None, dict)
        return response_json

    @_catch_all_exceptions
    async def set_dnd_state(self, state: bool) -> None:
        """Set Do Not Disturb state.

        Args:
        state (boolean): true or false

        Returns json

        """
        data = {
            "deviceSerialNumber": self._device.device_serial_number,
            "deviceType": self._device._device_type,
            "enabled": state,
        }
        _LOGGER.debug(
            "%s: Setting DND state: %s data: %s",
            hide_email(self._login.email),
            state,
            json.dumps(data),
        )
        response = await self._put_request("/api/dnd/status", data=data)
        response_json, *_ = await get_json_value(response, None, dict)
        success = data == response_json
        _LOGGER.debug(
            "%s: Success: %s Response: %s",
            hide_email(self._login.email),
            success,
            response_json,
        )
        return success

    @staticmethod
    @_catch_all_exceptions
    async def get_bluetooth(login) -> dict[str, Any] | None:
        """Get paired bluetooth devices."""
        response = await AlexaAPI._static_request(
            "get", login, "/api/bluetooth", query={"cached": "false"}
        )
        response_json, *_ = await get_json_value(response, None, dict)
        return response_json

    @_catch_all_exceptions
    async def set_bluetooth(self, mac: str) -> None:
        """Pair with bluetooth device with mac address."""
        await self._post_request(
            "/api/bluetooth/pair-sink/"
            + self._device._device_type
            + "/"
            + self._device.device_serial_number,
            data={"bluetoothDeviceAddress": mac},
        )

    @_catch_all_exceptions
    async def disconnect_bluetooth(self) -> None:
        """Disconnect all bluetooth devices."""
        await self._post_request(
            "/api/bluetooth/disconnect-sink/"
            + self._device._device_type
            + "/"
            + self._device.device_serial_number,
            data=None,
        )

    @staticmethod
    @_catch_all_exceptions
    async def get_devices(login: AlexaLogin) -> list[dict[str, Any]] | None:
        """Identify all Alexa devices."""
        response = await AlexaAPI._static_request(
            "get", login, "/api/devices-v2/device", query=None
        )
        devices, *_ = await get_json_value(response, "devices", list)

        if devices is not None:
            AlexaAPI.devices[login.email] = devices
            return devices

        if login.email in AlexaAPI.devices:
            _LOGGER.debug(
                "%s: Using cached device list because device API returned no data",
                hide_email(login.email),
            )
            return AlexaAPI.devices[login.email]

        _LOGGER.warning(
            "%s: Device API returned no data and no cached device list is available",
            hide_email(login.email),
        )
        AlexaAPI.devices[login.email] = []
        return AlexaAPI.devices[login.email]

    @staticmethod
    @_catch_all_exceptions
    async def rename_device(
        login: AlexaLogin,
        serial: str,
        device_type: str,
        device_account_id: str,
        name: str,
    ) -> bool:
        """Rename an Alexa device such as an Echo.

        Args:
            login (AlexaLogin): Successfully logged in AlexaLogin
            serial (str): ``serialNumber`` from ``get_devices``
            device_type (str): ``deviceType`` from ``get_devices``
            device_account_id (str): ``deviceAccountId`` from ``get_devices``
            name (str): New name

        Returns:
            True if Amazon accepted the new name.

        """
        if not serial or not name:
            return False
        response = await AlexaAPI._static_request(
            "put",
            login,
            f"/api/devices-v2/device/{urllib.parse.quote(serial, safe='')}",
            data={
                "accountName": name,
                "serialNumber": serial,
                "deviceAccountId": device_account_id,
                "deviceType": device_type,
            },
        )
        return response is not None

    @staticmethod
    @_catch_all_exceptions
    async def get_skills(login: AlexaLogin) -> list[dict[str, Any]] | None:
        """Get the skills enabled for the account.

        Args:
            login (AlexaLogin): Successfully logged in AlexaLogin

        Returns:
            The skill records of the skills store, or None if the page has no
            skill list. Each record has ``title``, ``asin``,
            ``productMetadata.skillId`` and ``productDetails.skillTypes``.

        """
        response = await AlexaAPI._static_request(
            "get",
            login,
            "/app/secure/your-skills-page",
            additional_headers={"Accept": SKILLS_STORE_ACCEPT},
            query={"deviceType": "app"},
            sub_domain="skills-store",
        )
        blocks, valid = await get_json_value(response, None, list)
        if not valid:
            return None
        for block in blocks:
            contents = block.get("contents") if isinstance(block, dict) else None
            if not isinstance(contents, list) or block.get("block") != "data":
                continue
            for content in contents:
                if (
                    isinstance(content, dict)
                    and content.get("id") == "skillsPageData"
                    and isinstance(content.get("contents"), dict)
                    and isinstance(content["contents"].get("products"), list)
                ):
                    return content["contents"]["products"]
        return None

    @staticmethod
    @_catch_all_exceptions
    async def get_child_mode(
        login: AlexaLogin, serial: str, device_type: str
    ) -> bool | None:
        """Return whether Amazon Kids (child mode) is active for a device.

        Amazon models the Amazon Kids/child state per device as the boolean
        ``isChildDirectedDevice``.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        serial (str): The device serial number
        device_type (str): The device type

        Returns:
        Optional[bool]: True if Amazon Kids is active, False if not,
            None if the state could not be determined.

        """
        response = await AlexaAPI._static_request(
            "get",
            login,
            "/api/device/op-mode",
            query={"deviceType": device_type, "deviceSerialNumber": serial},
        )
        value, _valid = await get_json_value(response, "isChildDirectedDevice", bool)
        return value

    @staticmethod
    @_catch_all_exceptions
    async def disable_child_mode(
        login: AlexaLogin, serial: str, device_type: str
    ) -> None:
        """Disable Amazon Kids (child mode) for a device.

        Unassigns the device from any child profile, which turns Amazon Kids
        off (``isChildDirectedDevice`` becomes False).

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        serial (str): The device serial number
        device_type (str): The device type

        """
        await AlexaAPI._static_request(
            "post",
            login,
            f"/api/unassign-device-from-child/{serial}/{device_type}",
        )

    @staticmethod
    async def _parent_dashboard_subdomain(login: AlexaLogin) -> str | None:
        """Return the discovered dashboard subdomain, or None if unavailable."""
        host = await login.resolve_parent_dashboard_host()
        return host.split(".", 1)[0] if host is not None else None

    @staticmethod
    async def supports_child_profiles(login: AlexaLogin) -> bool:
        """Return whether the child-profile dashboard hostname resolves in DNS.

        This checks DNS only, not HTTP availability, account eligibility or support
        for every Amazon Kids operation. Like AlexaLogin, the marketplace is a
        bare Amazon domain; domain comparisons are case-insensitive.
        """
        return await AlexaAPI._parent_dashboard_subdomain(login) is not None

    @staticmethod
    @_catch_all_exceptions
    async def get_child_profiles(login: AlexaLogin) -> list[dict[str, Any]] | None:
        """Return the child profiles of the Amazon household.

        Each entry contains at least ``firstName``, ``age`` and ``directedId``;
        the ``directedId`` is required to enable Amazon Kids on a device.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin

        Returns:
        Optional[list[dict]]: The CHILD household members, [] if the dashboard
        hostname is unavailable or there are no children, or None on error.

        """
        sub_domain = await AlexaAPI._parent_dashboard_subdomain(login)
        if sub_domain is None:
            return []

        response = await AlexaAPI._static_request(
            "get",
            login,
            "/ajax/get-household-with-age",
            sub_domain=sub_domain,
        )
        members, valid = await get_json_value(response, "members", list)
        if not valid or not members:
            return []
        return [member for member in members if member.get("role") == "CHILD"]

    @staticmethod
    @_catch_all_exceptions
    async def get_device_child(
        login: AlexaLogin, serial: str, device_type: str
    ) -> str | None:
        """Return the directedId of the child a device is assigned to.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        serial (str): The device serial number
        device_type (str): The device type

        Returns:
        Optional[str]: The child directedId, or None if unassigned, unknown,
        or the dashboard hostname is unavailable.

        """
        sub_domain = await AlexaAPI._parent_dashboard_subdomain(login)
        if sub_domain is None:
            return None

        response = await AlexaAPI._static_request(
            "get",
            login,
            "/ajax/get-oobe-device-data",
            query={"deviceId": serial, "deviceTypeId": device_type},
            sub_domain=sub_domain,
        )
        value, _valid = await get_json_value(response, "childDirectedId", str)
        return value or None

    @staticmethod
    @_catch_all_exceptions
    async def enable_child_mode(
        login: AlexaLogin, serial: str, device_type: str, child_directed_id: str
    ) -> None:
        """Enable Amazon Kids by assigning a device to a child profile.

        The parent dashboard uses its own CSRF token (``ft-panda-csrf-token``),
        which is seeded by loading the device onboarding page first; the token
        is then echoed back in the ``x-amzn-csrf`` header. Unavailable
        dashboard hostnames return None without making any requests.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        serial (str): The device serial number
        device_type (str): The device type
        child_directed_id (str): directedId of the child (see get_child_profiles)

        """
        sub_domain = await AlexaAPI._parent_dashboard_subdomain(login)
        if sub_domain is None:
            return None
        host = f"{sub_domain}.{login.url.lower()}"
        # Seed the parent-dashboard CSRF cookie (ft-panda-csrf-token).
        await AlexaAPI._static_request(
            "get",
            login,
            f"/oobe/brownie/start/{device_type}/{serial}",
            sub_domain=sub_domain,
        )
        additional_headers = {
            "Referer": (f"https://{host}/oobe/brownie/start/{device_type}/{serial}"),
            "Origin": f"https://{host}",
        }
        try:
            # The ft-panda-csrf-token cookie is scoped to the parent-dashboard
            # host, so it must be read for that host (not the default one).
            additional_headers["x-amzn-csrf"] = login._get_cookies_from_session(host)[
                "ft-panda-csrf-token"
            ].value
        except (KeyError, AttributeError):
            _LOGGER.debug(
                "%s: ft-panda-csrf-token not found after bootstrap; "
                "assign may be rejected",
                hide_email(login.email),
            )
        await AlexaAPI._static_request(
            "post",
            login,
            "/ajax/assign-device-to-child",
            data={
                "deviceId": serial,
                "deviceTypeId": device_type,
                "childDirectedId": child_directed_id,
            },
            additional_headers=additional_headers,
            sub_domain=sub_domain,
        )

    @staticmethod
    @_catch_all_exceptions
    async def get_wake_words(
        login: AlexaLogin, *, cached: bool = True
    ) -> list[dict[str, Any]] | None:
        """Get the wake words for the devices."""
        response = await AlexaAPI._static_request(
            "get",
            login,
            "/api/wake-word",
            query={"cached": "true" if cached else "false"},
        )

        wake_words, valid = await get_json_value(response, "wakeWords", list)

        if not valid or not wake_words:
            if not cached:
                return [] if valid else None
            # Lightweight diagnostics without leaking payload contents
            try:
                body = await response.json(content_type=None)
                if isinstance(body, dict):
                    _LOGGER.debug(
                        "Wake-word API returned no usable wakeWords. "
                        "Top-level keys: %s",
                        list(body.keys()),
                    )
                else:
                    _LOGGER.debug(
                        "Wake-word API returned unexpected JSON type: %s",
                        type(body).__name__,
                    )
            except Exception as exc:
                _LOGGER.debug(
                    "Wake-word API JSON inspection failed: %s",
                    exc,
                )

            # Safe fallback: return cached value or empty list
            return AlexaAPI.wake_words.get(login.email, [])

        AlexaAPI.wake_words[login.email] = wake_words
        return wake_words

    @staticmethod
    @_catch_all_exceptions
    async def get_available_wake_words(
        login: AlexaLogin, serial: str, device_type: str, software_version: str
    ) -> list[str] | None:
        """Get wake words supported by the device and its current locale."""
        response = await AlexaAPI._static_request(
            "get",
            login,
            "/api/wake-words-locale",
            query={
                "deviceSerialNumber": serial,
                "deviceType": device_type,
                "softwareVersion": software_version,
            },
        )
        words, valid = await get_json_value(response, "wakeWords", list)
        if not valid or not all(isinstance(word, str) for word in words):
            return None
        return words

    @staticmethod
    @_catch_all_exceptions
    async def set_wake_word(login: AlexaLogin, serial: str, wake_word: str) -> bool:
        """Change a device's wake word and verify that it has been applied.

        Wake words are sent in the upper case form Amazon uses, so the lower case
        value returned by ``find_wake_word()`` is accepted. Returns False if the
        device is unknown, the update is rejected, or the new wake word is not
        read back within about 80 seconds; in the last case the change may still
        be applied later.
        """
        if not isinstance(wake_word, str) or not wake_word.strip():
            return False
        wake_word = wake_word.strip().upper()
        models = await AlexaAPI.get_wake_words(login, cached=False)
        model = next(
            (
                item
                for item in models or []
                if isinstance(item, dict) and item.get("deviceSerialNumber") == serial
            ),
            None,
        )
        if model is None or not isinstance(model.get("wakeWord"), str):
            return False
        if model["wakeWord"] == wake_word:
            return True
        response = await AlexaAPI._static_request(
            "put",
            login,
            f"/api/wake-word/{serial}",
            data={**model, "wakeWord": wake_word},
        )
        if response is None or not 200 <= response.status < 300:
            return False
        # The official app re-reads uncached device state after these delays.
        for delay in (0.5, 5, 15, 30, 30):
            await asyncio.sleep(delay)
            models = await AlexaAPI.get_wake_words(login, cached=False)
            if any(
                isinstance(item, dict)
                and item.get("deviceSerialNumber") == serial
                and item.get("wakeWord") == wake_word
                for item in models or []
            ):
                return True
        return False

    @staticmethod
    @_catch_all_exceptions
    async def get_personality_styles(
        login: AlexaLogin, device_account_id: str, locale: str
    ) -> dict[str, Any] | None:
        """Return the current and available personality styles for a device.

        Returns the response containing ``curatedStyle`` and
        ``allCuratedStyles``, or None if the response is invalid.
        """
        response = await AlexaAPI._static_request(
            "get",
            login,
            "/api/personality/v1/getstyle/"
            + urllib.parse.quote(device_account_id, safe=""),
            additional_headers={"Accept-Language": locale},
        )
        result, valid = await get_json_value(response, None, dict)
        if not valid or not isinstance(result.get("allCuratedStyles"), list):
            return None
        if not isinstance(result.get("curatedStyle"), str):
            return None
        return result

    @staticmethod
    @_catch_all_exceptions
    async def set_personality_style(
        login: AlexaLogin, device_account_id: str, style_id: str, locale: str
    ) -> bool:
        """Set an unrestricted supported style and confirm it by reading back.

        Surrounding whitespace is ignored, but style IDs are case-sensitive.
        Returns False for invalid or unsupported styles, styles requiring
        consent, rejected updates, or changes not confirmed by a fresh read.
        An unconfirmed change may still be applied later.
        """
        if not isinstance(style_id, str) or not style_id.strip():
            return False
        style_id = style_id.strip()
        current = await AlexaAPI.get_personality_styles(
            login, device_account_id, locale
        )
        if current is None:
            return False
        if not any(
            isinstance(style, dict)
            and style.get("id") == style_id
            and not style.get("restrictedAccess")
            for style in current["allCuratedStyles"]
        ):
            return False
        if current["curatedStyle"] == style_id:
            return True
        response = await AlexaAPI._static_request(
            "post",
            login,
            "/api/personality/v1/setstyle",
            data={"deviceAccountId": device_account_id, "curatedStyle": style_id},
            additional_headers={"Accept-Language": locale},
        )
        if response is None or not 200 <= response.status < 300:
            return False
        updated = await AlexaAPI.get_personality_styles(
            login, device_account_id, locale
        )
        return updated is not None and updated["curatedStyle"] == style_id

    @staticmethod
    @_catch_all_exceptions
    async def find_wake_word(login: AlexaLogin, serial: str) -> str | None:
        """Find the wake word associated to a device."""
        wake_words = (
            AlexaAPI.wake_words[login.email]
            if login.email in AlexaAPI.wake_words
            else await AlexaAPI.get_wake_words(login)
        )
        if wake_words:
            found = next(
                filter(
                    lambda wake_word: serial == wake_word["deviceSerialNumber"],
                    wake_words,
                ),
                None,
            )
            if found is not None:
                return found["wakeWord"].lower()
        return None

    @staticmethod
    @_catch_all_exceptions
    async def get_authentication(login: AlexaLogin) -> dict[str, Any] | None:
        """Get authentication json."""
        response = await AlexaAPI._static_request(
            "get",
            login,
            f"/api/users/me?platform=ios&version={LOGIN_APP_VERSION}",
            query=None,
        )
        json_resp, *_ = await get_json_value(response, None, dict)
        if json_resp:
            return {
                "authenticated": True,
                "canAccessPrimeMusicContent": json_resp.get(
                    "canAccessPrimeMusicContent", True
                ),
                "customerEmail": json_resp.get("email"),
                "customerId": json_resp.get("id"),
                "customerName": json_resp.get("fullName"),
            }
        return None

    @staticmethod
    async def _customer_history_headers(login: AlexaLogin) -> dict:
        """Build RVH headers and refresh the CSRF token when needed."""
        headers = {
            "referer": f"https://www.{login.url}",
            "anti-csrftoken-a2z": login.csrf_token,
        }
        if login.csrf_token is None or (
            int(time.time()) - login.csrf_token_created_at > 24 * 3600
        ):
            headers["anti-csrftoken-a2z"] = await login.get_csrf_token()
        return headers

    @staticmethod
    async def _request_customer_history_page(
        login, start_time, end_time, max_record_size, token, headers
    ) -> dict | None:
        """Fetch one RVH payload through the shared authenticated transport."""
        response = await AlexaAPI._static_request(
            "post",
            login,
            "/alexa-privacy/apd/rvh/customer-history-records-v2",
            data={"previousRequestToken": token},
            additional_headers=headers,
            query={
                "startTime": start_time,
                "endTime": end_time,
                "recordType": "VOICE_HISTORY",
                "maxRecordSize": max_record_size,
            },
            sub_domain="www",
        )
        payload, valid = await get_json_value(response, None, dict)
        return payload if valid else None

    @staticmethod
    def _history_next_token(token, seen) -> tuple[str | None, str]:
        """Validate tokens consistently for legacy and page callers."""
        if token is None or token == "":
            return None, "no continuation token"
        if not isinstance(token, str):
            return None, "invalid continuation token type"
        if token in seen:
            return None, "repeated continuation token"
        return token, "continue"

    @staticmethod
    @_catch_all_exceptions
    async def get_customer_history_page(  # noqa: PLR0911
        login: AlexaLogin,
        start_time: int | None = None,
        end_time: int | None = None,
        max_record_size: int | None = None,
        *,
        continuation: HistoryContinuation | None = None,
    ) -> HistoryPage:
        """Return a normalized page and an in-memory, session-scoped cursor.

        Resumption freezes the initial query. Empty pages can continue.
        Invalid/cyclic tokens are errors, never genuine exhaustion. Transport
        authentication/rate-limit exceptions and cancellation propagate.
        An error may retain the input cursor for retry. Callers must bound
        retries: the transport can hide HTTP rejection/expiry as no response.
        Connection failures raise AlexapyConnectionError, as for other requests.
        """
        session, domain, account = login.session, login.url, login.email
        if continuation is not None:
            if not isinstance(continuation, HistoryContinuation):
                return HistoryPage([], "error", error="invalid continuation")
            if (
                continuation._login is not login
                or continuation._session is not login.session
                or continuation._domain != login.url
                or continuation._account != login.email
            ):
                return HistoryPage([], "error", error="continuation scope mismatch")
            if any(
                (
                    start_time is not None and start_time != continuation.start_time,
                    end_time is not None and end_time != continuation.end_time,
                    max_record_size is not None
                    and max_record_size != continuation.max_record_size,
                )
            ):
                return HistoryPage([], "error", error="continuation query mismatch")
            start_time, end_time = continuation.start_time, continuation.end_time
            max_record_size = continuation.max_record_size
            token, seen = continuation._token, continuation._seen
        else:
            now = time.time()
            start_time = (
                int((now - 7 * 24 * 3600) * 1000) if start_time is None else start_time
            )
            end_time = int((now + 24 * 3600) * 1000) if end_time is None else end_time
            max_record_size = 1 if max_record_size is None else max_record_size
            token, seen = None, frozenset()
        headers = await AlexaAPI._customer_history_headers(login)
        if (
            login.session is not session
            or login.url != domain
            or login.email != account
        ):
            return HistoryPage(
                [], "error", error="session changed during header refresh"
            )
        payload = await AlexaAPI._request_customer_history_page(
            login, start_time, end_time, max_record_size, token, headers
        )
        if (
            login.session is not session
            or login.url != domain
            or login.email != account
        ):
            return HistoryPage([], "error", error="session changed during request")
        if payload is None:
            return HistoryPage([], "error", continuation, "invalid or missing response")
        raw = payload.get("customerHistoryRecords")
        if raw is None and "customerHistoryRecords" in payload:
            if payload.get("encodedRequestToken") not in (None, ""):
                return HistoryPage([], "error", error="null records with continuation")
            return HistoryPage([], "exhausted")
        if not isinstance(raw, list):
            return HistoryPage([], "error", error="invalid customerHistoryRecords")
        next_token, reason = AlexaAPI._history_next_token(
            payload.get("encodedRequestToken"), seen
        )
        if reason not in ("continue", "no continuation token"):
            return HistoryPage([], "error", error=reason)
        records = []
        try:
            for record in raw:
                if not isinstance(record, dict):
                    return HistoryPage([], "error", error="invalid history record")
                records.append(await AlexaAPI._normalize_history_record(login, record))
        except (TypeError, ValueError, AttributeError, KeyError):
            return HistoryPage([], "error", error="invalid history record")
        # Normalization can await wake-word lookup and yield to reauthentication.
        if (
            login.session is not session
            or login.url != domain
            or login.email != account
        ):
            return HistoryPage(
                [], "error", error="session changed during normalization"
            )
        if next_token is None:
            return HistoryPage(records, "exhausted")
        cursor = HistoryContinuation(
            start_time,
            end_time,
            max_record_size,
            login,
            session,
            domain,
            account,
            next_token,
            seen | {next_token},
        )
        return HistoryPage(records, "success", cursor)

    @staticmethod
    @_catch_all_exceptions
    async def get_customer_history_records(
        login: AlexaLogin,
        start_time: int | None = None,
        end_time: int | None = None,
        max_record_size: int | None = 1,
        *,
        max_pages: int = 1,
        stop_on_usable_activity: bool = False,
    ) -> list[dict[str, Any]] | None:
        """Get normalized customer history records, optionally across RVH pages.

        Existing callers fetch one page. ``max_record_size`` remains the page
        size; ``max_pages`` bounds the total requests (between one and ten).
        Stop early on an activity usable for last_called when requested.
        A failed page returns None, rather than presenting partial history as
        complete. Missing or repeated continuation tokens end the search.
        The default start time is seven days ago.
        """
        max_pages = max(1, min(max_pages, 10))
        start_time = (
            int((time.time() - 7 * 24 * 3600) * 1000)
            if start_time is None
            else start_time
        )
        end_time = (
            int((time.time() + 24 * 3600) * 1000) if end_time is None else end_time
        )
        extra_headers = await AlexaAPI._customer_history_headers(login)

        ret: list[dict[str, Any]] = []
        previous_token: str | None = None
        seen_tokens: set[str] = set()

        def log_stop(page_number: int, reason: str) -> None:
            _LOGGER.debug(
                "RVH pagination stopped: pages=%s, activities=%s, reason=%s",
                page_number,
                len(ret),
                reason,
            )

        for page_number in range(1, max_pages + 1):
            payload = await AlexaAPI._request_customer_history_page(
                login,
                start_time,
                end_time,
                max_record_size,
                previous_token,
                extra_headers,
            )
            if payload is None:
                log_stop(page_number, "invalid or missing response")
                return None
            customerHistoryRecords = payload.get("customerHistoryRecords")
            if customerHistoryRecords is None:
                log_stop(page_number, "null or missing customerHistoryRecords")
                return ret if "customerHistoryRecords" in payload else None
            if not isinstance(customerHistoryRecords, list):
                log_stop(page_number, "invalid customerHistoryRecords type")
                return None

            _LOGGER.debug(
                "RVH page %s/%s: records=%s, continuation_token_present=%s",
                page_number,
                max_pages,
                len(customerHistoryRecords),
                bool(payload.get("encodedRequestToken")),
            )
            for record in customerHistoryRecords:
                o = await AlexaAPI._normalize_history_record(login, record)
                ret.append(o)

                if stop_on_usable_activity and AlexaAPI._is_usable_history_activity(o):
                    log_stop(page_number, "usable activity found")
                    return ret

            token, reason = AlexaAPI._history_next_token(
                payload.get("encodedRequestToken"), seen_tokens
            )
            if reason != "continue":
                log_stop(page_number, reason)
                break
            seen_tokens.add(token)
            previous_token = token
        else:
            log_stop(max_pages, "page limit reached")

        return ret

    @staticmethod
    async def _normalize_history_record(
        login: AlexaLogin, record: dict[str, Any]
    ) -> dict[str, Any]:
        """Normalize one RVH record to the existing activity format."""
        o: dict[str, Any] = {}
        conv_parts: dict[str, list[dict[str, Any]]] = {}

        for item in record.get("voiceHistoryRecordItems") or []:
            conv_parts.setdefault(item.get("recordItemType", ""), []).append(item)

        if conv_parts:
            o["conversionDetails"] = conv_parts

        if "recordKey" in record:
            o["recordKey"] = record["recordKey"]
        record_key = (record.get("recordKey") or "").split("#")
        o["deviceType"] = (
            record_key[2] if len(record_key) > 2 and record_key[2] else None
        )
        o["creationTimestamp"] = record.get("timestamp")
        o["deviceSerialNumber"] = record_key[3] if len(record_key) > 3 else None
        o["utteranceType"] = record.get("utteranceType")
        for key in ("domain", "intent", "skillName"):
            if key in record:
                o[key] = record[key]

        wake_word = (
            await AlexaAPI.find_wake_word(login, o["deviceSerialNumber"])
            if o.get("deviceSerialNumber")
            else None
        )
        lw = wake_word.lower() if wake_word else None

        # -------- Summary (what the user said) --------
        summary_parts: list[str] = []
        for key in ("CUSTOMER_TRANSCRIPT", "ASR_REPLACEMENT_TEXT"):
            for trans in conv_parts.get(key, []):
                text = (trans.get("transcriptText") or "").strip()
                if not text:
                    continue

                text_l = text.lower()
                if lw and text_l.startswith(lw):
                    # strip original-length wake_word, then punctuation/space
                    text = text[len(wake_word) :].lstrip(" ,:").strip()
                elif text_l.startswith("alexa"):
                    text = text[5:].lstrip(" ,:").strip()

                if text:
                    summary_parts.append(text)

        o["description"] = {"summary": ", ".join(summary_parts)}

        # -------- Alexa response (what Alexa said / TTS) --------
        response_parts: list[str] = []
        for key in ("ALEXA_RESPONSE", "TTS_REPLACEMENT_TEXT"):
            for trans in conv_parts.get(key, []):
                text = (trans.get("transcriptText") or "").strip()
                if text:
                    response_parts.append(text)

        o["alexaResponse"] = ", ".join(response_parts)

        return o

    @staticmethod
    @_catch_all_exceptions
    async def get_activities(
        login: AlexaLogin, items: int = 10
    ) -> dict[str, Any] | None:
        """Get activities json."""
        response = await AlexaAPI._static_request(
            "get",
            login,
            "/api/activities",
            query={"startTime": "", "size": items, "offset": 1},
        )
        result, *_ = await get_json_value(response, "activities", dict)
        return result

    @staticmethod
    @_catch_all_exceptions
    async def get_device_preferences(login: AlexaLogin) -> dict[str, Any] | None:
        """Identify all Alexa device preferences."""
        response = await AlexaAPI._static_request(
            "get", login, "/api/device-preferences", query={}
        )
        response_json, *_ = await get_json_value(response, None, dict)
        return response_json

    @staticmethod
    async def get_device_setting(
        login: AlexaLogin, device_account_id: str, setting: str
    ) -> tuple[int, Any]:
        """Return (HTTP status, decoded value) for one device setting.

        A 400 status means Amazon does not support the setting on the device.
        Other non-200 statuses are temporary and can be retried. A 401 that
        persists after the retry raises AlexapyLoginError and marks the login
        as failed, as for every other request. The response is released before
        returning.
        """
        if not device_account_id:
            return 0, None
        result = await AlexaAPI._static_request(
            "get",
            login,
            f"/api/v1/devices/{urllib.parse.quote(device_account_id, safe='')}"
            f"/settings/{urllib.parse.quote(setting, safe='')}",
            with_status=True,
        )
        if result is None:  # pragma: no cover - defensive
            return 0, None
        status, response = result
        try:
            if status != 200:
                return status, None
            try:
                data = await response.json(content_type=None)
            except (TypeError, ValueError):
                return status, None
            value = data.get("value") if isinstance(data, dict) else None
            if isinstance(value, str):
                with contextlib.suppress(TypeError, ValueError):
                    value = json.loads(value)
            if value is None or isinstance(value, (dict, list)):
                return status, None
            return status, value
        finally:
            response.release()

    @staticmethod
    async def set_device_setting(
        login: AlexaLogin, device_account_id: str, setting: str, value: Any
    ) -> bool:
        """Write one device setting and return whether Amazon accepted it."""
        if not device_account_id:
            return False
        response = await AlexaAPI._static_request(
            "put",
            login,
            f"/api/v1/devices/{urllib.parse.quote(device_account_id, safe='')}"
            f"/settings/{urllib.parse.quote(setting, safe='')}",
            data={"value": json.dumps(value)},
        )
        return response is not None

    @staticmethod
    @_catch_all_exceptions
    async def get_automations(
        login: AlexaLogin, items: int = 1000
    ) -> list[dict[str, Any]] | None:
        """Identify all Alexa automations."""
        response = await AlexaAPI._static_request(
            "get", login, "/api/behaviors/v2/automations", query={"limit": items}
        )
        response_json, *_ = await get_json_value(response, None, list)
        return response_json

    @staticmethod
    def _is_usable_history_activity(activity: dict[str, Any]) -> bool:
        """Identify voice history suitable for last_called."""
        return bool(
            activity.get("deviceSerialNumber")
            and (activity.get("description") or {}).get("summary")
            and activity.get("utteranceType") != "DEVICE_ARBITRATION"
        )

    @staticmethod
    @_catch_all_exceptions
    async def get_last_device_serial(
        login: AlexaLogin, items: int = 10
    ) -> dict[str, Any] | None:
        """Identify the last device's serial number and last summary.

        Search up to ten RVH pages of ``items`` records for the latest
        non-arbitration transcript with a device serial number. The existing
        default history time window applies to every page.
        """
        try:
            response = await AlexaAPI.get_customer_history_records(
                login,
                max_record_size=items,
                max_pages=10,
                stop_on_usable_activity=True,
            )
        except TypeError as e:
            _LOGGER.debug("Customer history request failed: %s", e)
            return None
        if response is not None:
            for last_activity in response:
                summary = ""
                # Ignore empty description and summary
                # Ignore utterance type DEVICE_ARBITRATION
                if AlexaAPI._is_usable_history_activity(last_activity):
                    with contextlib.suppress(AttributeError, JSONDecodeError):
                        summary = last_activity["description"]["summary"]
                    return {
                        "serialNumber": (last_activity["deviceSerialNumber"]),
                        "timestamp": last_activity["creationTimestamp"],
                        "summary": summary,
                        "response": last_activity.get("alexaResponse", ""),
                    }

        return None

    @_catch_all_exceptions
    async def set_guard_state(
        self, entity_id: str, state: str, queue_delay: float = 1.5
    ) -> None:
        """Set Guard state.

        Args:
        entity_id (str): numeric ending of applianceId of RedRock Panel
        state (str): AWAY, HOME
        queue_delay (float, optional): The number of seconds to wait
                                        for commands to queue together.
                                        Defaults to 1.5.
                                        Must be positive.
        Returns json

        """
        _LOGGER.debug(
            "%s: Setting Guard state: %s ", hide_email(self._login.email), state
        )

        await self.send_sequence(
            "controlGuardState",
            target=entity_id,
            operationId="controlGuardState",
            state=state,
            skillId="amzn1.ask.skill.f71a9b50-e99a-4669-a226-d50ebb5e0830",
            queue_delay=queue_delay,
        )

    @staticmethod
    @_catch_all_exceptions
    async def get_guard_state(
        login: AlexaLogin, entity_id: str
    ) -> dict[str, Any] | None:
        """Get state of Alexa guard.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        entity_id (str): applianceId of RedRock Panel

        Returns json

        """
        return await AlexaAPI.get_entity_state(login, appliance_ids=[entity_id])

    @staticmethod
    @_catch_all_exceptions
    async def get_entity_state(
        login: AlexaLogin,
        entity_ids: list[str] | None = None,
        appliance_ids: list[str] | None = None,
    ) -> dict[str, Any] | None:
        """Get the current state of multiple appliances.

        Note that this can take both entity_ids and appliance_ids.
        If you have both pieces of data available, prefer the entity id. A single entity might have multiple
        appliance ids. Its easier to ensure you don't miss data by just providing entity id instead.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        entity_ids (List[str]): The list of entities you want information about.
        appliance_ids: (List[str]): The list of appliances you want information about.

        Returns json

        """  # noqa: E501
        state_requests = []
        if entity_ids is not None:
            for entity_id in entity_ids:
                state_requests.append({"entityId": entity_id, "entityType": "ENTITY"})
        if appliance_ids is not None:
            for appliance_id in appliance_ids:
                state_requests.append(
                    {"entityId": appliance_id, "entityType": "APPLIANCE"}
                )
        data = {"stateRequests": state_requests}
        response = await AlexaAPI._static_request(
            "post", login, "/api/phoenix/state", data=data
        )
        response_json, *_ = await get_json_value(response, None, dict)
        _LOGGER.debug(
            "%s: get_entity_state response: %s", hide_email(login.email), response_json
        )
        return response_json

    @staticmethod
    @_catch_all_exceptions
    async def static_set_guard_state(
        login: AlexaLogin, entity_id: str, state: str
    ) -> dict[str, Any] | None:
        """Set state of Alexa guard.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        entity_id (str): entityId of RedRock Panel
        state (str): ARMED_AWAY, ARMED_STAY

        Returns json

        """
        parameters = {"action": "controlSecurityPanel", "armState": state}
        data = {
            "controlRequests": [
                {
                    "entityId": entity_id,
                    "entityType": "APPLIANCE",
                    "parameters": parameters,
                }
            ]
        }
        response = await AlexaAPI._static_request(
            "put", login, "/api/phoenix/state", data=data
        )
        response_json, *_ = await get_json_value(response, None, dict)
        _LOGGER.debug(
            "%s: set_guard_state response: %s for data: %s ",
            hide_email(login.email),
            response_json,
            json.dumps(data),
        )
        return response_json

    @staticmethod
    @_catch_all_exceptions
    async def set_light_state(
        login: AlexaLogin,
        entity_id: str,
        power_on: bool = True,
        brightness: int | None = None,
        color_name: str | None = None,
        color_temperature_name: str | None = None,
    ) -> dict[str, Any] | None:
        """Set state of a light.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        entity_id (str): Entity ID of The light. Not the Application ID.
        power_on (bool): Should the light be on or off.
        brightness (Optional[int]): 0-100 or None to leave as is
        color_name (Optional[str]): The name of a color that Alexa supports in snake case.
        color_temperature_name (Optional[str]): The name of a color temperature name that Alexa supports in snake case.

        Returns json

        """  # noqa: E501
        control_requests = [
            {
                "entityId": entity_id,
                "entityType": "ENTITY",
                "parameters": {"action": "turnOn" if power_on else "turnOff"},
            }
        ]

        if brightness is not None and 0 <= brightness <= 100:
            control_requests.append(
                {
                    "entityId": entity_id,
                    "entityType": "ENTITY",
                    "parameters": {
                        "action": "setBrightness",
                        "brightness": str(brightness),
                    },
                }
            )

        if color_name is not None:
            control_requests.append(
                {
                    "entityId": entity_id,
                    "entityType": "ENTITY",
                    "parameters": {"action": "setColor", "colorName": color_name},
                }
            )

        if color_temperature_name is not None:
            control_requests.append(
                {
                    "entityId": entity_id,
                    "entityType": "ENTITY",
                    "parameters": {
                        "action": "setColorTemperature",
                        "colorTemperatureName": color_temperature_name,
                    },
                }
            )

        data = {"controlRequests": control_requests}

        response = await AlexaAPI._static_request(
            "put", login, "/api/phoenix/state", data=data
        )
        response_json, *_ = await get_json_value(response, None, dict)
        _LOGGER.debug(
            "%s: set_light_state response: %s for data: %s ",
            hide_email(login.email),
            response_json,
            json.dumps(data),
        )
        return response_json

    @staticmethod
    @_catch_all_exceptions
    async def get_devices_gql(login: AlexaLogin) -> list[dict[str, Any]] | None:
        """Get devices of the Alexa network.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin

        Returns:
            Endpoint dictionaries containing id, model, dmsIdentifier and
            legacyAppliance, or None when the response has no endpoint list. The
            id is the endpoint ID that the smart-home mutations such as
            set_endpoint_friendly_name take. Model and identifier
            metadata may be null. Only PLAIN model values are readable descriptions;
            a model description does not necessarily include a hardware generation.
            Match dmsIdentifier.deviceType and dsn to the REST deviceType and
            serialNumber rather than matching by a customer-assigned device name.
            If Amazon rejects the expanded query, the original legacy-only query is
            used instead and the id, model and dmsIdentifier keys are absent.

        """
        email = login.email
        expanded = email not in AlexaAPI._gql_legacy_accounts
        response = await AlexaAPI._static_request(
            "post",
            login,
            "/nexus/v1/graphql",
            data={
                "query": GQL_SMARTHOME_QUERY if expanded else GQL_SMARTHOME_QUERY_LEGACY
            },
        )
        result, *_ = await get_json_value(response, "data.endpoints.items", list)
        if result is not None or not expanded:
            return result
        if await AlexaAPI._is_gql_throttled(response):
            return None
        # Amazon may reject the added metadata fields for some accounts or
        # marketplaces; keep device discovery working with the original query.
        _LOGGER.debug(
            "%s: Expanded smart-home query failed; retrying with the legacy query",
            hide_email(email),
        )
        response = await AlexaAPI._static_request(
            "post",
            login,
            "/nexus/v1/graphql",
            data={"query": GQL_SMARTHOME_QUERY_LEGACY},
        )
        result, *_ = await get_json_value(response, "data.endpoints.items", list)
        if result is not None:
            AlexaAPI._gql_legacy_accounts.add(email)
        return result

    @staticmethod
    async def _is_gql_throttled(response: ClientResponse | None) -> bool:
        """Return True if a GraphQL response reports throttling."""
        if response is None:
            return False
        try:
            body = await response.json(content_type=None)
        except Exception:
            return False
        errors = body.get("errors") if isinstance(body, dict) else None
        return any(
            isinstance(error, dict)
            and isinstance(error.get("extensions"), dict)
            and error["extensions"].get("errorCode") == "TOO_MANY_REQUESTS"
            for error in errors or []
        )

    @staticmethod
    @_catch_all_exceptions
    async def get_network_details(login: AlexaLogin) -> list[dict[str, Any]] | None:
        """Get the network of devices that Alexa is aware of.

        Args:
            login: (AlexaLogin): Successfully logged in AlexaLogin

        Returns:
            List of legacy appliance dicts, or None if no legacy appliances
            are present or the response is missing.
        """
        network_detail = await AlexaAPI.get_devices_gql(login)
        email = hide_email(login.email)
        if network_detail is None:
            _LOGGER.warning("%s: get_devices_gql returned None", email)
            return None

        details: list[dict[str, Any]] = []
        for el in network_detail:
            legacy = el.get("legacyAppliance")
            if isinstance(legacy, dict):
                details.append(legacy)
            else:
                _LOGGER.debug("%s: get_devices_gql skipped element: %s", email, el)

        _LOGGER.debug("%s: get_devices_gql raw response: %s", email, network_detail)
        return details or None

    @staticmethod
    @_catch_all_exceptions
    async def get_appliance_groups(login: AlexaLogin) -> list[dict[str, Any]] | None:
        """Get the smart-home groups (rooms) of the account.

        Args:
            login (AlexaLogin): Successfully logged in AlexaLogin

        Returns:
            The group documents as Amazon returns them, or None if the response
            has no group list. Each document has at least ``groupId``, ``name``
            and ``applianceIds``; the members are the ``applianceId`` values of
            ``get_network_details``.

        """
        response = await AlexaAPI._static_request("get", login, "/api/phoenix/group")
        result, *_ = await get_json_value(response, "applianceGroups", list)
        return result

    @staticmethod
    def _appliance_group_uri(group_id: str) -> str:
        """Return the URI of one smart-home group."""
        return f"/api/phoenix/group/{urllib.parse.quote(group_id, safe='')}"

    @staticmethod
    @_catch_all_exceptions
    async def create_appliance_group(
        login: AlexaLogin, name: str, appliance_ids: list[str] | None = None
    ) -> dict[str, Any] | None:
        """Create a smart-home group (room).

        Amazon answers without a body, so the groups are read before and after
        the request. The new group is the one with the given name that was not
        there before.

        Args:
            login (AlexaLogin): Successfully logged in AlexaLogin
            name (str): Name of the new group
            appliance_ids (list[str] | None): Members, as ``applianceId``
                values. Duplicates are dropped, the order is kept.

        Returns:
            The document of the new group, or None if the name is empty, the
            groups cannot be read, the request failed or the new group is not
            in the list afterwards.

        """
        if not name:
            return None
        before = await AlexaAPI.get_appliance_groups(login)
        if before is None:
            return None
        known = {group.get("groupId") for group in before}
        response = await AlexaAPI._static_request(
            "post",
            login,
            "/api/phoenix/group",
            data={
                "name": name,
                "type": "SPACE",
                "applianceIds": list(dict.fromkeys(appliance_ids or [])),
                "defaults": [],
                "childIds": [],
            },
        )
        if response is None:
            return None
        after = await AlexaAPI.get_appliance_groups(login)
        return next(
            (
                group
                for group in after or []
                if group.get("name") == name and group.get("groupId") not in known
            ),
            None,
        )

    @staticmethod
    async def _update_appliance_group(
        login: AlexaLogin, group_id: str, changes: dict[str, Any]
    ) -> bool:
        """Write changed fields of a group and send the rest back unchanged."""
        groups = await AlexaAPI.get_appliance_groups(login)
        group = next((g for g in groups or [] if g.get("groupId") == group_id), None)
        if group is None:
            _LOGGER.debug(
                "%s: Smart-home group %s not found", hide_email(login.email), group_id
            )
            return False
        response = await AlexaAPI._static_request(
            "put",
            login,
            AlexaAPI._appliance_group_uri(group_id),
            data={**group, **changes},
        )
        return response is not None

    @staticmethod
    @_catch_all_exceptions
    async def set_appliance_group_members(
        login: AlexaLogin, group_id: str, appliance_ids: list[str]
    ) -> bool:
        """Replace the members of a smart-home group (room).

        The group is read again right before writing, and only ``applianceIds``
        changes; the rest of Amazon's group document is sent back as it came.

        Args:
            login (AlexaLogin): Successfully logged in AlexaLogin
            group_id (str): ``groupId`` of the group
            appliance_ids (list[str]): New members, as ``applianceId`` values.
                Duplicates are dropped, the order is kept.

        Returns:
            True if Amazon accepted the change, False if the group does not
            exist or the request failed.

        """
        if not group_id:
            return False
        return await AlexaAPI._update_appliance_group(
            login, group_id, {"applianceIds": list(dict.fromkeys(appliance_ids))}
        )

    @staticmethod
    @_catch_all_exceptions
    async def rename_appliance_group(
        login: AlexaLogin, group_id: str, name: str
    ) -> bool:
        """Rename a smart-home group (room) and keep its members.

        Args:
            login (AlexaLogin): Successfully logged in AlexaLogin
            group_id (str): ``groupId`` of the group
            name (str): New name

        Returns:
            True if Amazon accepted the change, False if the name is empty, the
            group does not exist or the request failed.

        """
        if not group_id or not name:
            return False
        return await AlexaAPI._update_appliance_group(login, group_id, {"name": name})

    @staticmethod
    @_catch_all_exceptions
    async def delete_appliance_group(login: AlexaLogin, group_id: str) -> bool:
        """Delete a smart-home group (room). Its devices are kept.

        Args:
            login (AlexaLogin): Successfully logged in AlexaLogin
            group_id (str): ``groupId`` of the group

        Returns:
            True if Amazon accepted the request.

        """
        if not group_id:
            return False
        response = await AlexaAPI._static_request(
            "delete", login, AlexaAPI._appliance_group_uri(group_id)
        )
        return response is not None

    @staticmethod
    @_catch_all_exceptions
    async def discover_appliances(login: AlexaLogin) -> bool:
        """Ask Alexa to search for new smart-home devices.

        This is the device search of the Alexa app. Echo devices with a
        built-in Zigbee hub search as well, so the search can add devices
        that were not in the account before, for example lamps paired with
        an Echo. New devices are not in any group.

        Args:
            login (AlexaLogin): Successfully logged in AlexaLogin

        Returns:
            True if Amazon started the discovery. New devices appear later in
            ``get_devices_gql``.

        """
        response = await AlexaAPI._static_request(
            "post", login, "/api/phoenix/discovery"
        )
        return response is not None

    @staticmethod
    async def _endpoint_mutation(
        login: AlexaLogin, query: str, variables: dict[str, Any], field: str
    ) -> dict[str, Any] | None:
        """Run a smart-home GraphQL mutation and return its result object.

        Amazon reports rejected mutations with HTTP 200 and an ``errors`` list,
        so a response with errors counts as failed.
        """
        response = await AlexaAPI._static_request(
            "post",
            login,
            "/nexus/v1/graphql",
            data={"query": query, "variables": variables},
        )
        body, valid = await get_json_value(response, None, dict)
        if not valid:
            return None
        if body.get("errors"):
            _LOGGER.debug(
                "%s: GraphQL %s failed: %s",
                hide_email(login.email),
                field,
                body["errors"],
            )
            return None
        data = body.get("data")
        result = data.get(field) if isinstance(data, dict) else None
        return result if isinstance(result, dict) else None

    @staticmethod
    @_catch_all_exceptions
    async def set_endpoint_friendly_name(
        login: AlexaLogin, endpoint_id: str, name: str
    ) -> bool:
        """Rename a smart-home device.

        Amazon rejects some names, for example names with an underscore; the
        device then keeps its old name.

        Args:
            login (AlexaLogin): Successfully logged in AlexaLogin
            endpoint_id (str): Endpoint ``id`` from ``get_devices_gql``
                (``amzn1.alexa.endpoint...``), not the ``applianceId``
            name (str): New name

        Returns:
            True if Amazon accepted the new name.

        """
        if not endpoint_id or not name:
            return False
        result = await AlexaAPI._endpoint_mutation(
            login,
            GQL_SET_ENDPOINT_FRIENDLY_NAME,
            {"input": {"endpointId": endpoint_id, "friendlyName": name}},
            "setEndpointFriendlyName",
        )
        return result is not None

    @staticmethod
    @_catch_all_exceptions
    async def set_endpoint_enabled(
        login: AlexaLogin, endpoint_id: str, enabled: bool
    ) -> bool:
        """Enable or disable a smart-home device.

        A disabled device stays in the account, but Alexa does not control it.

        Args:
            login (AlexaLogin): Successfully logged in AlexaLogin
            endpoint_id (str): Endpoint ``id`` from ``get_devices_gql``
            enabled (bool): True to enable, False to disable

        Returns:
            True if Amazon accepted the change.

        """
        if not endpoint_id:
            return False
        result = await AlexaAPI._endpoint_mutation(
            login,
            GQL_SET_ENDPOINT_ENABLEMENT,
            {
                "input": {
                    "endpointId": endpoint_id,
                    "enablement": "ENABLED" if enabled else "DISABLED_BY_CUSTOMER",
                }
            },
            "setEndpointEnablement",
        )
        return result is not None and not result.get("error")

    @staticmethod
    @_catch_all_exceptions
    async def forget_endpoint(login: AlexaLogin, endpoint_id: str) -> bool:
        """Delete (forget) a smart-home device from the account.

        The request does not set ``allowDmsBackedEndpoint``, so it is not meant
        for Echo devices and other endpoints registered with Amazon.

        Args:
            login (AlexaLogin): Successfully logged in AlexaLogin
            endpoint_id (str): Endpoint ``id`` from ``get_devices_gql``

        Returns:
            True if Amazon accepted the request.

        """
        if not endpoint_id:
            return False
        result = await AlexaAPI._endpoint_mutation(
            login,
            GQL_FORGET_ENDPOINT,
            {"input": {"endpointId": endpoint_id}},
            "forgetEndpoint",
        )
        return result is not None

    @staticmethod
    def _should_skip_notifications(email: str, now: float) -> bool:
        """Return True if we should skip notifications due to cooldown."""
        if not hasattr(AlexaAPI, "_notif_last_call"):
            AlexaAPI._notif_last_call = {}

        last = AlexaAPI._notif_last_call.get(email, 0.0)
        cooldown = 10
        if now - last < cooldown:
            _LOGGER.debug(
                "%s: Skipping alexapy get_notifications; last %.1fs ago (cooldown %ss)",
                hide_email(email),
                now - last,
                cooldown,
            )
            return True

        AlexaAPI._notif_last_call[email] = now
        return False

    @staticmethod
    @_catch_all_exceptions
    async def get_notifications(login: AlexaLogin) -> list[dict[str, Any]] | None:
        """Get Alexa notifications using discovered API base."""
        email = login.email
        now = time.time()

        if AlexaAPI._should_skip_notifications(email, now):
            return None

        session = login.session
        if session.closed:
            raise AlexapyLoginError("Session is closed")

        # 🔹 Use discovered base instead of hard-coded NA
        api_base = await AlexaAPI._get_alexa_api_base(login)
        ts = int(time.time() * 1000)
        url = (
            URL(api_base)
            .with_path("/api/notifications")
            .update_query({"cached": "true", "_": str(ts)})
        )

        try:
            response = await send_request(
                session, "get", url, login, RequestProfile.NOTIFICATIONS_PITANGUI
            )
            body = await response.text()
        except ClientConnectionError as exc:
            raise AlexapyConnectionError(str(exc)) from exc

        if response.status == 401:
            login.status["login_successful"] = False
            raise AlexapyLoginError(response.reason)
        if response.status >= 400:
            return None

        with contextlib.suppress(ValueError):
            payload = json.loads(body)
            if isinstance(payload, dict):
                notifications = payload.get("notifications")
                if isinstance(notifications, list):
                    return notifications
        return None

    @staticmethod
    @_catch_all_exceptions
    async def set_notifications(login: AlexaLogin, data) -> dict[str, Any] | None:
        """Update Alexa notification.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        data : Data to pass to notifications

        Returns json

        """
        response = await AlexaAPI._static_request(
            "put", login, "/api/notifications", data=data
        )
        # _LOGGER.debug("%s: Response: %s", hide_email(login.email),
        #               response.json(content_type=None))
        response_json, *_ = await get_json_value(response, None, dict)
        return response_json

    @staticmethod
    async def _alarm_request(
        method: str,
        login: AlexaLogin,
        uri: str,
        data: dict[str, Any] | None = None,
    ) -> ClientResponse | None:
        """Send a request to the alarms API on the account's alexaApiUrl.

        This API takes the OAuth access token instead of cookies.

        Args:
        method (str): HTTP method
        login (AlexaLogin): Successfully logged in AlexaLogin
        uri (str): Path after /v1/alerts/alarms
        data (dict): JSON body

        Returns the response, or None on failure

        """
        api_url = getattr(login, "_alexa_alarms_api_url", None)
        # Going through _static_request again also refreshes an expired token.
        if not api_url or (login.expires_in and login.expires_in - time.time() < 0):
            response = await AlexaAPI._static_request("get", login, "/api/endpoints")
            api_url, valid = await get_json_value(response, "alexaApiUrl", str)
            if not valid:
                return None
            api_url = api_url.rstrip("/")
            login._alexa_alarms_api_url = api_url
        url = URL(f"{api_url}/v1/alerts/alarms{uri}")
        if not login.access_token:
            return None
        response = await send_request(
            login.session, method, url, login, RequestProfile.ALARMS, data=data
        )
        _LOGGER.debug(
            "%s: %s %s returned %s:%s",
            hide_email(login.email),
            method,
            url,
            response.status,
            response.reason,
        )
        return await AlexaAPI._process_response(response, login)

    @staticmethod
    @_catch_all_exceptions
    async def create_alarm(
        login: AlexaLogin,
        serial: str,
        device_type: str,
        scheduled_time: str,
        recurrence: dict[str, Any] | None = None,
        sound_id: str | None = None,
    ) -> bool:
        """Create an alarm on a device.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        serial (str): Device serial number
        device_type (str): Device type
        scheduled_time (str): First ring in the device's time, as YYYY-MM-DDTHH:MM:SS
        recurrence (dict): Repeat rule, such as {"freq": "DAILY", "byDay": []}
        sound_id (str): Alarm tone id

        Returns True if successful

        """
        trigger: dict[str, Any] = {"scheduledTime": scheduled_time}
        if recurrence:
            trigger["recurrence"] = recurrence
        data: dict[str, Any] = {
            "trigger": trigger,
            "extensions": [],
            "endpointId": f"{serial}@{device_type}",
        }
        if sound_id:
            data["assets"] = [{"type": "TONE", "assetId": sound_id}]
        response = await AlexaAPI._alarm_request("post", login, "", data)
        return response is not None

    @staticmethod
    @_catch_all_exceptions
    async def enable_alarm(
        login: AlexaLogin,
        notification_index: str,
        scheduled_time: str,
        sound_id: str | None = None,
    ) -> bool:
        """Turn an alarm on.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        notification_index (str): The alarm's notificationIndex
        scheduled_time (str): Next ring in the device's time, as YYYY-MM-DDTHH:MM:SS
        sound_id (str): The alarm's tone id

        Returns True if successful

        """
        data: dict[str, Any] = {
            "trigger": {"scheduledTime": scheduled_time},
            "extensions": [],
        }
        if sound_id:
            data["assets"] = [{"type": "TONE", "assetId": sound_id}]
        response = await AlexaAPI._alarm_request(
            "put", login, f"/{notification_index}/activate", data
        )
        return response is not None

    @staticmethod
    @_catch_all_exceptions
    async def update_alarm(
        login: AlexaLogin,
        notification_index: str,
        scheduled_time: str,
        recurrence: dict[str, Any] | None = None,
        sound_id: str | None = None,
    ) -> bool:
        """Change the time of an alarm.

        Amazon replaces the alarm's schedule, so pass the recurrence again to
        keep a repeating alarm repeating. The alarm is turned on.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        notification_index (str): The alarm's notificationIndex
        scheduled_time (str): Next ring in the device's time, as YYYY-MM-DDTHH:MM:SS
        recurrence (dict): Repeat rule, such as {"freq": "DAILY", "byDay": []}
        sound_id (str): The alarm's tone id

        Returns True if successful

        """
        trigger: dict[str, Any] = {"scheduledTime": scheduled_time}
        if recurrence:
            trigger["recurrence"] = recurrence
        data: dict[str, Any] = {"trigger": trigger, "extensions": []}
        if sound_id:
            data["assets"] = [{"type": "TONE", "assetId": sound_id}]
        response = await AlexaAPI._alarm_request(
            "put", login, f"/{notification_index}", data
        )
        return response is not None

    @staticmethod
    @_catch_all_exceptions
    async def disable_alarm(login: AlexaLogin, notification_index: str) -> bool:
        """Turn an alarm off without deleting it.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        notification_index (str): The alarm's notificationIndex

        Returns True if successful

        """
        response = await AlexaAPI._alarm_request(
            "put", login, f"/{notification_index}/cancel"
        )
        return response is not None

    @staticmethod
    @_catch_all_exceptions
    async def skip_next_alarm(login: AlexaLogin, notification_index: str) -> bool:
        """Request cancellation of the next occurrence of a recurring alarm.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        notification_index (str): The alarm's notificationIndex

        Returns True if the API accepted the request.

        """
        response = await AlexaAPI._alarm_request(
            "put", login, f"/{notification_index}/nextOccurrence/cancel"
        )
        return response is not None and 200 <= response.status < 300

    @staticmethod
    @_catch_all_exceptions
    async def delete_notification(
        login: AlexaLogin, notification: dict[str, Any]
    ) -> bool:
        """Delete an alarm, reminder or timer.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        notification (dict): The notification from get_notifications

        Returns True if successful

        """
        response = await AlexaAPI._static_request(
            "delete",
            login,
            f"/api/notifications/{notification['id']}",
            data=notification,
        )
        return response is not None

    @staticmethod
    @_catch_all_exceptions
    async def get_dnd_state(login: AlexaLogin) -> dict[str, Any] | None:
        """Get Alexa DND states.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin

        Returns json

        """
        response = await AlexaAPI._static_request(
            "get",
            login,
            "/api/dnd/device-status-list",
        )
        response_json, *_ = await get_json_value(response, None, dict)
        return response_json

    @staticmethod
    @_catch_all_exceptions
    async def get_ascending_alarm_states(
        login: AlexaLogin,
    ) -> list[dict[str, Any]] | None:
        """Get whether ascending alarm volume is on for all devices.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin

        Returns list of device states with ascendingAlarmEnabled

        """
        response = await AlexaAPI._static_request("get", login, "/api/ascending-alarm")
        states, valid = await get_json_value(response, "ascendingAlarmModelList", list)
        return states if valid else None

    @staticmethod
    @_catch_all_exceptions
    async def set_ascending_alarm(
        login: AlexaLogin, serial: str, device_type: str, enabled: bool
    ) -> bool:
        """Turn ascending alarm volume on or off for a device.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        serial (str): Device serial number
        device_type (str): Device type
        enabled (bool): True to start alarms quietly and get louder

        Returns True if successful

        """
        _LOGGER.debug(
            "%s: Setting ascending alarm of %s to %s",
            hide_email(login.email),
            hide_serial(serial),
            enabled,
        )
        response = await AlexaAPI._static_request(
            "put",
            login,
            f"/api/ascending-alarm/{serial}",
            data={
                "deviceSerialNumber": serial,
                "deviceType": device_type,
                "ascendingAlarmEnabled": enabled,
            },
        )
        return response is not None

    @staticmethod
    @_catch_all_exceptions
    async def get_notification_sounds(
        login: AlexaLogin,
        serial: str,
        device_type: str,
        software_version: str,
        notification_type: str = "Alarm",
    ) -> list[dict[str, Any]] | None:
        """Get the sounds a device can use for alarms or timers.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        serial (str): Device serial number
        device_type (str): Device type
        software_version (str): Device software version
        notification_type (str): "Alarm" or "Timer"

        Returns list of sounds with id and displayName

        """
        response = await AlexaAPI._static_request(
            "get",
            login,
            "/api/notification/sounds",
            query={
                "deviceType": device_type,
                "deviceSerialNumber": serial,
                "softwareVersion": software_version,
                "alertType": notification_type,
            },
        )
        sounds, valid = await get_json_value(response, "notificationSounds", list)
        return sounds if valid else None

    @staticmethod
    @_catch_all_exceptions
    async def get_default_notification_sound(
        login: AlexaLogin,
        serial: str,
        device_type: str,
        notification_type: str = "Alarm",
    ) -> dict[str, Any] | None:
        """Get the default alarm or timer sound of a device.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        serial (str): Device serial number
        device_type (str): Device type
        notification_type (str): "Alarm" or "Timer"

        Returns sound with id and displayName

        """
        response = await AlexaAPI._static_request(
            "get",
            login,
            "/api/notification/default-sound",
            query={
                "deviceType": device_type,
                "deviceSerialNumber": serial,
                "notificationType": notification_type,
            },
        )
        sound, valid = await get_json_value(response, "defaultNotificationSound", dict)
        return sound if valid else None

    @staticmethod
    @_catch_all_exceptions
    async def set_default_notification_sound(
        login: AlexaLogin,
        serial: str,
        device_type: str,
        sound_id: str,
        notification_type: str = "Alarm",
    ) -> bool:
        """Set the default alarm or timer sound of a device.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        serial (str): Device serial number
        device_type (str): Device type
        sound_id (str): Sound id from get_notification_sounds()
        notification_type (str): "Alarm" or "Timer"

        Returns True if successful

        """
        _LOGGER.debug(
            "%s: Setting default %s sound of %s to %s",
            hide_email(login.email),
            notification_type,
            hide_serial(serial),
            sound_id,
        )
        response = await AlexaAPI._static_request(
            "put",
            login,
            "/api/notification/default-sound",
            data={
                "deviceType": device_type,
                "deviceSerialNumber": serial,
                "notificationType": notification_type,
                "soundId": sound_id,
            },
        )
        return response is not None

    @staticmethod
    @_catch_all_exceptions
    async def get_notification_states(
        login: AlexaLogin,
    ) -> list[dict[str, Any]] | None:
        """Get the alarm, timer and notification volume of all devices.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin

        Returns list of device states with volumeLevel

        """
        response = await AlexaAPI._static_request(
            "get", login, "/api/device-notification-state"
        )
        states, valid = await get_json_value(response, "deviceNotificationStates", list)
        return states if valid else None

    @staticmethod
    @_catch_all_exceptions
    async def set_notification_volume(
        login: AlexaLogin,
        serial: str,
        device_type: str,
        software_version: str,
        volume: int,
    ) -> bool:
        """Set the "Alarms, Timers and Notifications" volume of a device.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        serial (str): Device serial number
        device_type (str): Device type
        software_version (str): Device software version
        volume (int): Volume from 0 to 100

        Returns True if successful

        """
        data = {
            "deviceSerialNumber": serial,
            "deviceType": device_type,
            "softwareVersion": software_version,
            "volumeLevel": volume,
        }
        _LOGGER.debug(
            "%s: Setting notification volume of %s to %s",
            hide_email(login.email),
            hide_serial(serial),
            volume,
        )
        response = await AlexaAPI._static_request(
            "put",
            login,
            f"/api/device-notification-state/{device_type}/{software_version}/{serial}",
            data=data,
        )
        return response is not None

    @staticmethod
    @_catch_all_exceptions
    async def get_equalizer(
        login: AlexaLogin, serial: str, device_type: str
    ) -> dict[str, Any] | None:
        """Get the bass, mid and treble of a device.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        serial (str): Device serial number
        device_type (str): Device type

        Returns dict with bass, mid and treble

        """
        response = await AlexaAPI._static_request(
            "get", login, f"/api/equalizer/{serial}/{device_type}"
        )
        response_json, valid = await get_json_value(response, None, dict)
        return response_json if valid else None

    @staticmethod
    @_catch_all_exceptions
    async def set_equalizer(
        login: AlexaLogin,
        serial: str,
        device_type: str,
        bass: int,
        mid: int,
        treble: int,
    ) -> bool:
        """Set the bass, mid and treble of a device.

        Amazon sets any band left out to 0, so all three are sent.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        serial (str): Device serial number
        device_type (str): Device type
        bass (int): Bass from -6 to 6
        mid (int): Mid from -6 to 6
        treble (int): Treble from -6 to 6

        Returns True if successful

        Raises:
        ValueError: A band is not an integer from -6 to 6; nothing is sent.

        """
        for name, value in (("bass", bass), ("mid", mid), ("treble", treble)):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(
                    f"{name} must be an integer from -6 to 6, got {value!r}"
                )
            if not -6 <= value <= 6:
                raise ValueError(f"{name} must be from -6 to 6, got {value}")
        _LOGGER.debug(
            "%s: Setting equalizer of %s to bass %s, mid %s, treble %s",
            hide_email(login.email),
            hide_serial(serial),
            bass,
            mid,
            treble,
        )
        response = await AlexaAPI._static_request(
            "post",
            login,
            f"/api/equalizer/{serial}/{device_type}",
            data={"bass": bass, "mid": mid, "treble": treble},
        )
        return response is not None

    @staticmethod
    @_catch_all_exceptions
    async def clear_history(login: AlexaLogin, items: int = 50) -> bool:
        """Clear entries in history."""
        email = login.email
        response = await AlexaAPI._static_request(
            "get", login, "/api/activities", query={"size": items, "offset": -1}
        )

        completed = True
        activities, *_ = await get_json_value(response, "activities", (list, NoneType))
        if not activities:
            _LOGGER.debug("%s: No history to delete.", hide_email(email))
            return True
        _LOGGER.debug(
            "%s:Attempting to delete %s items from history",
            hide_email(email),
            len(activities),
        )
        for activity in activities:
            if not isinstance(activity, dict) or not activity.get("id"):
                continue
            response = await AlexaAPI._static_request(
                "delete",
                login,
                f"/api/activities/{urllib.parse.quote_plus(activity['id'])}",
            )
            if response is None:
                _LOGGER.debug(
                    ("%s:Unable to connect to Alexa to delete %s"),
                    hide_email(email),
                    activity["id"],
                )
            elif response.status == 404:
                _LOGGER.warning(
                    (
                        "%s:Unable to delete %s: %s: \n"
                        "There is no voice recording to delete. "
                        "Please manually delete the entry in the Alexa app."
                    ),
                    hide_email(email),
                    activity["id"],
                    response.reason,
                )
                completed = False
            elif response.status == 200:
                _LOGGER.debug(
                    "%s: Successfully deleted %s",
                    hide_email(email),
                    activity["id"],
                )
        return completed

    @_catch_all_exceptions
    async def set_background(self, url: str) -> bool:
        """Set background for Echo Show.

        Sets the background to Alexa App Photo with the specific https url.

        Args
        url (URL): valid https url for the image

        Returns
        Whether the command was successful.

        """
        data = {
            "deviceSerialNumber": self._device.device_serial_number,
            "deviceType": self._device._device_type,
            "backgroundImageID": "JqIFZhtBTx25wLGTJGdNGQ",
            "backgroundImageType": "PERSONAL_PHOTOS",
            "backgroundImageURL": url,
        }
        _LOGGER.debug(
            "%s: Setting background of %s to: %s",
            hide_email(self._login.email),
            self._device,
            url,
        )
        if url.startswith("http://"):
            _LOGGER.warning("Background URL should be a valid https image")
        response = await self._post_request("/api/background-image", data=data)
        response_json, *_ = await get_json_value(response, None, dict)
        success = bool(response and response.status == 200)
        _LOGGER.debug(
            "%s: Success: %s Response: %s",
            hide_email(self._login.email),
            success,
            response_json,
        )
        return success

    @staticmethod
    @_catch_all_exceptions
    async def force_logout() -> None:
        """Force logout.

        Raises
            AlexapyLoginError: Raise AlexapyLoginError

        """
        raise AlexapyLoginError("Forced Logout")

    @staticmethod
    @_catch_all_exceptions
    async def ping(login: AlexaLogin) -> dict[str, Any] | None:
        """Ping.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin

        Returns json

        """
        response = await AlexaAPI._static_request(
            "get",
            login,
            "/api/ping",
        )
        return await response.json(content_type=None) if response else None
