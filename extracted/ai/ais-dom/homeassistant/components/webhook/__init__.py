"""Webhooks for Home Assistant."""
from __future__ import annotations

from collections.abc import Awaitable, Callable, Iterable
from http import HTTPStatus
from ipaddress import ip_address
import logging
import secrets
from typing import TYPE_CHECKING, Any

from aiohttp import StreamReader
from aiohttp.hdrs import METH_GET, METH_HEAD, METH_POST, METH_PUT
from aiohttp.web import Request, Response
import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.components.http.view import HomeAssistantView
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.network import get_url
from homeassistant.helpers.typing import ConfigType
from homeassistant.loader import bind_hass
from homeassistant.util import network
from homeassistant.util.aiohttp import MockRequest, MockStreamReader, serialize_response

_LOGGER = logging.getLogger(__name__)

DOMAIN = "webhook"

DEFAULT_METHODS = (METH_POST, METH_PUT)
SUPPORTED_METHODS = (METH_GET, METH_HEAD, METH_POST, METH_PUT)
URL_WEBHOOK_PATH = "/api/webhook/{webhook_id}"

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


@callback
@bind_hass
def async_register(
    hass: HomeAssistant,
    domain: str,
    name: str,
    webhook_id: str,
    handler: Callable[[HomeAssistant, str, Request], Awaitable[Response | None]],
    *,
    local_only: bool | None = False,
    allowed_methods: Iterable[str] | None = None,
) -> None:
    """Register a webhook."""
    handlers = hass.data.setdefault(DOMAIN, {})

    if webhook_id in handlers:
        raise ValueError("Handler is already defined!")

    if allowed_methods is None:
        allowed_methods = DEFAULT_METHODS
    allowed_methods = frozenset(allowed_methods)

    if not allowed_methods.issubset(SUPPORTED_METHODS):
        raise ValueError(
            f"Unexpected method: {allowed_methods.difference(SUPPORTED_METHODS)}"
        )

    handlers[webhook_id] = {
        "domain": domain,
        "name": name,
        "handler": handler,
        "local_only": local_only,
        "allowed_methods": allowed_methods,
    }


@callback
@bind_hass
def async_unregister(hass: HomeAssistant, webhook_id: str) -> None:
    """Remove a webhook."""
    handlers = hass.data.setdefault(DOMAIN, {})
    handlers.pop(webhook_id, None)


@callback
def async_generate_id() -> str:
    """Generate a webhook_id."""
    return secrets.token_hex(32)


@callback
@bind_hass
def async_generate_url(hass: HomeAssistant, webhook_id: str) -> str:
    """Generate the full URL for a webhook_id."""
    # TODO check if this is needed
    # "ais-dom gate_id fix"
    # from homeassistant.components.ais_dom import ais_global
    #
    # gate_id = ais_global.get_sercure_android_id_dom()
    # return "{}{}".format(
    #     "https://" + gate_id + ".paczka.pro", async_generate_path(webhook_id)
    return "{}{}".format(
        get_url(hass, prefer_external=True, allow_cloud=False),
        async_generate_path(webhook_id),
    )


@callback
def async_generate_path(webhook_id: str) -> str:
    """Generate the path component for a webhook_id."""
    return URL_WEBHOOK_PATH.format(webhook_id=webhook_id)


@bind_hass
async def async_handle_webhook(
    hass: HomeAssistant, webhook_id: str, request: Request | MockRequest
) -> Response:
    """Handle a webhook."""
    handlers: dict[str, dict[str, Any]] = hass.data.setdefault(DOMAIN, {})

    content_stream: StreamReader | MockStreamReader
    if isinstance(request, MockRequest):
        received_from = request.mock_source
        content_stream = request.content
        method_name = request.method
    else:
        received_from = request.remote
        content_stream = request.content
        method_name = request.method

    # Always respond successfully to not give away if a hook exists or not.
    if (
        webhook := handlers.get(webhook_id)
    ) is None and webhook_id != "aisdomprocesscommandfromframe":
        _LOGGER.info(
            "Received message for unregistered webhook %s from %s",
            webhook_id,
            received_from,
        )
        # Look at content to provide some context for received webhook
        # Limit to 64 chars to avoid flooding the log
        content = await content_stream.read(64)
        _LOGGER.debug("%s", content)
        return Response(status=HTTPStatus.OK)

    if method_name not in webhook["allowed_methods"]:
        if method_name == METH_HEAD:
            # Allow websites to verify that the URL exists.
            return Response(status=HTTPStatus.OK)

        _LOGGER.warning(
            "Webhook %s only supports %s methods but %s was received from %s",
            webhook_id,
            ",".join(webhook["allowed_methods"]),
            method_name,
            received_from,
        )
        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)

    if webhook["local_only"] in (True, None) and not isinstance(request, MockRequest):
        if has_cloud := "cloud" in hass.config.components:
            from hass_nabucasa import remote  # pylint: disable=import-outside-toplevel

        is_local = True
        if has_cloud and remote.is_cloud_request.get():
            is_local = False
        else:
            if TYPE_CHECKING:
                assert isinstance(request, Request)
                assert request.remote is not None

            try:
                request_remote = ip_address(request.remote)
            except ValueError:
                _LOGGER.debug("Unable to parse remote ip %s", request.remote)
                return Response(status=HTTPStatus.OK)

            is_local = network.is_local(request_remote)

        if not is_local:
            _LOGGER.warning("Received remote request for local webhook %s", webhook_id)
            if webhook["local_only"]:
                return Response(status=HTTPStatus.OK)
            if not webhook.get("warned_about_deprecation"):
                webhook["warned_about_deprecation"] = True
                _LOGGER.warning(
                    "Deprecation warning: "
                    "Webhook '%s' does not provide a value for local_only. "
                    "This webhook will be blocked after the 2023.11.0 release. "
                    "Use `local_only: false` to keep this webhook operating as-is",
                    webhook_id,
                )

    try:
        # ais
        response = None
        if webhook_id == "aisdomprocesscommandfromframe":
            # TODO check the ais_ha_webhook_id
            # except ais/register_wear_os
            import homeassistant.components.ais_ai_service as ai

            try:
                rj = await request.json()
                if "ais_gate_client_id" in rj:
                    # new way with answer
                    response = await ai.async_process_json_from_frame(hass, rj)
                else:
                    # TODO remove this old way
                    await hass.services.async_call(
                        "ais_ai_service", "process_command_from_frame", rj
                    )
            except Exception:
                response = None
        if response is None and webhook is not None:
            response = await webhook["handler"](hass, webhook_id, request)
        if response is None:
            response = Response(status=HTTPStatus.OK)
        return response
    except Exception:  # pylint: disable=broad-except
        _LOGGER.exception("Error processing webhook %s", webhook_id)
        return Response(status=HTTPStatus.OK)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Initialize the webhook component."""
    hass.http.register_view(WebhookView)
    websocket_api.async_register_command(hass, websocket_list)
    websocket_api.async_register_command(hass, websocket_handle)
    return True


class WebhookView(HomeAssistantView):
    """Handle incoming webhook requests."""

    url = URL_WEBHOOK_PATH
    name = "api:webhook"
    requires_auth = False
    cors_allowed = True

    async def _handle(self, request: Request, webhook_id: str) -> Response:
        """Handle webhook call."""
        _LOGGER.debug("Handling webhook %s payload for %s", request.method, webhook_id)
        hass = request.app["hass"]
        return await async_handle_webhook(hass, webhook_id, request)

    get = _handle
    head = _handle
    post = _handle
    put = _handle
    get = _handle


@websocket_api.websocket_command(
    {
        "type": "webhook/list",
    }
)
@callback
def websocket_list(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return a list of webhooks."""
    handlers = hass.data.setdefault(DOMAIN, {})
    result = [
        {
            "webhook_id": webhook_id,
            "domain": info["domain"],
            "name": info["name"],
            "local_only": info["local_only"],
            "allowed_methods": sorted(info["allowed_methods"]),
        }
        for webhook_id, info in handlers.items()
    ]

    connection.send_message(websocket_api.result_message(msg["id"], result))


@websocket_api.websocket_command(
    {
        vol.Required("type"): "webhook/handle",
        vol.Required("webhook_id"): str,
        vol.Required("method"): vol.In(SUPPORTED_METHODS),
        vol.Optional("body", default=""): str,
        vol.Optional("headers", default={}): {str: str},
        vol.Optional("query", default=""): str,
    }
)
@websocket_api.async_response
async def websocket_handle(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle an incoming webhook via the WS API."""
    request = MockRequest(
        content=msg["body"].encode("utf-8"),
        headers=msg["headers"],
        method=msg["method"],
        query_string=msg["query"],
        mock_source=f"{DOMAIN}/ws",
    )

    response = await async_handle_webhook(hass, msg["webhook_id"], request)

    response_dict = serialize_response(response)
    body = response_dict.get("body")

    connection.send_result(
        msg["id"],
        {
            "body": body,
            "status": response_dict["status"],
            "headers": {"Content-Type": response.content_type},
        },
    )
