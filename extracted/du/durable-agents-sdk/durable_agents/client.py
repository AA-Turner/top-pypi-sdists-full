from __future__ import annotations

import os
from collections.abc import Iterator, Mapping
from types import TracebackType
from typing import Self
from urllib.parse import quote

import httpx

from ._build_info import DEFAULT_BASE_URL, SDK_VERSION
from .errors import error_from_response
from .pagination import paginate
from .streaming import DurableRunEvent, iter_sse_lines

JsonObject = Mapping[str, object]
QueryParams = Mapping[str, object]


class DurableClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | httpx.Timeout | None = None,
        headers: Mapping[str, str] | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("DURABLE_API_KEY")
        self.base_url = _strip_trailing_slash(
            base_url or os.getenv("DURABLE_API_BASE_URL") or DEFAULT_BASE_URL
        )
        default_headers = {
            "User-Agent": f"durable-agents-sdk-python/{SDK_VERSION}",
            **dict(headers or {}),
        }
        if self.api_key:
            default_headers["Authorization"] = f"Bearer {self.api_key}"

        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers=default_headers,
            transport=transport,
        )

        self.keys = _Keys(self)
        self.agents = _Agents(self)
        self.runs = _Runs(self)
        self.library = _Library(self)
        self.vfs = _Vfs(self)
        self.personas = _ResourceGroup(self, "/api/durable/personas")
        self.skills = _ResourceGroup(self, "/api/durable/skills")
        self.models = _Models(self)
        self.accounts = _Accounts(self)
        self.sources = _Sources(self)
        self.connectors = _Connectors(self)
        self.channels = _Channels(self)
        self.usage = _Usage(self)
        self.audit = _Audit(self)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        params: QueryParams | None = None,
        body: object | None = None,
        headers: Mapping[str, str] | None = None,
        files: object | None = None,
    ) -> object:
        kwargs: dict[str, object] = {
            "params": _clean_params(params),
            "headers": dict(headers or {}),
        }

        if files is not None:
            kwargs["files"] = files
            if isinstance(body, Mapping):
                kwargs["data"] = dict(body)
        elif body is not None:
            kwargs["json"] = body

        response = self._client.request(method, path, **kwargs)
        if response.is_error:
            raise error_from_response(response)
        if response.status_code == 204:
            return {}
        return response.json()


class _ResourceGroup:
    def __init__(self, client: DurableClient, path: str) -> None:
        self._client = client
        self._path = path

    def list(self, **params: object) -> object:
        return self._client.request("GET", self._path, params=params)

    def iterate(self, **params: object) -> Iterator[object]:
        return paginate(lambda page_params: _expect_mapping(self.list(**page_params)), params)

    def create(self, input: JsonObject) -> object:
        return self._client.request("POST", self._path, body=input)

    def get(self, id: str) -> object:
        return self._client.request("GET", f"{self._path}/{_path(id)}")

    def update(self, id: str, input: JsonObject) -> object:
        return self._client.request("PATCH", f"{self._path}/{_path(id)}", body=input)

    def delete(self, id: str) -> object:
        return self._client.request("DELETE", f"{self._path}/{_path(id)}")


class _Keys:
    def __init__(self, client: DurableClient) -> None:
        self._client = client

    def list(self, **params: object) -> object:
        return self._client.request("GET", "/api/durable/keys", params=params)

    def create(self, input: JsonObject) -> object:
        return self._client.request("POST", "/api/durable/keys", body=input)

    def claim(self, input: JsonObject) -> object:
        return self._client.request("POST", "/api/durable/keys/claim", body=input)

    def revoke(self, key: str) -> object:
        return self._client.request("DELETE", f"/api/durable/keys/{_path(key)}")


class _Agents(_ResourceGroup):
    def __init__(self, client: DurableClient) -> None:
        super().__init__(client, "/api/durable/agents")

    def prompt(self, agent_id: str, input: JsonObject) -> object:
        return self._client.request("POST", f"/api/durable/agents/{_path(agent_id)}/runs", body=input)


class _Runs:
    def __init__(self, client: DurableClient) -> None:
        self._client = client

    def list(self, **params: object) -> object:
        return self._client.request("GET", "/api/durable/runs", params=params)

    def iterate(self, **params: object) -> Iterator[object]:
        return paginate(lambda page_params: _expect_mapping(self.list(**page_params)), params)

    def get(self, run_id: str) -> object:
        return self._client.request("GET", f"/api/durable/runs/{_path(run_id)}")

    def events(self, run_id: str, **params: object) -> object:
        return self._client.request("GET", f"/api/durable/runs/{_path(run_id)}/events", params=params)

    def watch(self, run_id: str, cursor: str | None = None) -> Iterator[DurableRunEvent]:
        params = {"cursor": cursor} if cursor else None
        with self._client._client.stream(
            "GET",
            f"/api/durable/runs/{_path(run_id)}/events",
            params=params,
            headers={"Accept": "text/event-stream"},
        ) as response:
            if response.is_error:
                response.read()
                raise error_from_response(response)
            yield from iter_sse_lines(response.iter_text())

    def replay(self, run_id: str) -> object:
        return self._client.request("POST", f"/api/durable/runs/{_path(run_id)}/replay")

    def cancel(self, run_id: str) -> object:
        return self._client.request("POST", f"/api/durable/runs/{_path(run_id)}/cancel")

    def pause(self, run_id: str) -> object:
        return self._client.request("POST", f"/api/durable/runs/{_path(run_id)}/pause")

    def resume(self, run_id: str) -> object:
        return self._client.request("POST", f"/api/durable/runs/{_path(run_id)}/resume")

    def prompt(self, run_id: str, input: JsonObject) -> object:
        return self._client.request("POST", f"/api/durable/runs/{_path(run_id)}/prompt", body=input)


class _Library:
    def __init__(self, client: DurableClient) -> None:
        self._client = client

    def list(self, **params: object) -> object:
        return self._client.request("GET", "/api/durable/content", params=params)

    def iterate(self, **params: object) -> Iterator[object]:
        return paginate(lambda page_params: _expect_mapping(self.list(**page_params)), params)

    def ingest(self, input: JsonObject | None = None, files: object | None = None) -> object:
        return self._client.request("POST", "/api/durable/content", body=input, files=files)

    def get(self, content_id: str) -> object:
        return self._client.request("GET", f"/api/durable/content/{_path(content_id)}")

    def update(self, content_id: str, input: JsonObject) -> object:
        return self._client.request("PATCH", f"/api/durable/content/{_path(content_id)}", body=input)

    def delete(self, content_id: str) -> object:
        return self._client.request("DELETE", f"/api/durable/content/{_path(content_id)}")


class _Vfs:
    def __init__(self, client: DurableClient) -> None:
        self._client = client

    def entries(self, **params: object) -> object:
        return self._client.request("GET", "/api/durable/vfs/entries", params=params)

    def item(self, **params: object) -> object:
        return self._client.request("GET", "/api/durable/vfs/item", params=params)

    def search(self, **params: object) -> object:
        return self._client.request("GET", "/api/durable/vfs/search", params=params)


class _Models:
    def __init__(self, client: DurableClient) -> None:
        self._client = client

    def list(self, **params: object) -> object:
        return self._client.request("GET", "/api/durable/models", params=params)


class _Accounts:
    def __init__(self, client: DurableClient) -> None:
        self._client = client

    def list(self, **params: object) -> object:
        return self._client.request("GET", "/api/durable/accounts", params=params)

    def create(self, input: JsonObject) -> object:
        return self._client.request("POST", "/api/durable/accounts", body=input)

    def get(self, account_id: str) -> object:
        return self._client.request("GET", f"/api/durable/accounts/{_path(account_id)}")

    def delete(self, account_id: str) -> object:
        return self._client.request("DELETE", f"/api/durable/accounts/{_path(account_id)}")

    def connect(self, account_id: str, input: JsonObject | None = None) -> object:
        return self._client.request(
            "POST",
            f"/api/durable/accounts/{_path(account_id)}/connect",
            body=input or {},
        )


class _Sources(_ResourceGroup):
    def __init__(self, client: DurableClient) -> None:
        super().__init__(client, "/api/durable/data-sources")

    def pause(self, source_id: str) -> object:
        return self._client.request("POST", f"/api/durable/data-sources/{_path(source_id)}/pause")

    def resume(self, source_id: str) -> object:
        return self._client.request("POST", f"/api/durable/data-sources/{_path(source_id)}/resume")

    def sync(self, source_id: str) -> object:
        return self._client.request("POST", f"/api/durable/data-sources/{_path(source_id)}/sync")

    def discover(self, source_type: str, **params: object) -> object:
        return self._client.request(
            "GET",
            f"/api/durable/data-sources/discover/{_path(source_type)}",
            params=params,
        )


class _Connectors(_ResourceGroup):
    def __init__(self, client: DurableClient) -> None:
        super().__init__(client, "/api/durable/connectors")

    def connect(self, connector_id: str, input: JsonObject | None = None) -> object:
        return self._client.request(
            "POST",
            f"/api/durable/connectors/{_path(connector_id)}/connect",
            body=input or {},
        )

    def disconnect(self, connector_id: str) -> object:
        return self._client.request(
            "POST",
            f"/api/durable/connectors/{_path(connector_id)}/disconnect",
        )


class _Channels:
    def __init__(self, client: DurableClient) -> None:
        self.connectors = _ChannelConnectors(client)
        self.email = _EmailChannels(client)
        self.messaging = _MessagingChannels(client)
        self.slack = _SlackChannels(client)
        self.endpoints = _ChannelEndpoints(client)
        self.bindings = _ChannelBindings(client)


class _ChannelConnectors(_ResourceGroup):
    def __init__(self, client: DurableClient) -> None:
        super().__init__(client, "/api/durable/channels/connectors")

    def get(self, id: str) -> object:
        raise NotImplementedError("Channel connectors do not expose a get endpoint.")

    def update(self, id: str, input: JsonObject) -> object:
        raise NotImplementedError("Channel connectors do not expose an update endpoint.")


class _EmailChannels:
    def __init__(self, client: DurableClient) -> None:
        self.inboxes = _EmailInboxes(client)


class _EmailInboxes:
    def __init__(self, client: DurableClient) -> None:
        self._client = client
        self.messages = _EmailInboxMessages(client)

    def list(self, **params: object) -> object:
        return self._client.request("GET", "/api/durable/channels/email/inboxes", params=params)

    def create(self, input: JsonObject) -> object:
        return self._client.request("POST", "/api/durable/channels/email/inboxes", body=input)

    def delete(self, inbox_id: str) -> object:
        return self._client.request("DELETE", f"/api/durable/channels/email/inboxes/{_path(inbox_id)}")


class _EmailInboxMessages:
    def __init__(self, client: DurableClient) -> None:
        self._client = client

    def list(self, inbox_id: str, **params: object) -> object:
        return self._client.request(
            "GET",
            f"/api/durable/channels/email/inboxes/{_path(inbox_id)}/messages",
            params=params,
        )

    def send(self, inbox_id: str, input: JsonObject) -> object:
        return self._client.request(
            "POST",
            f"/api/durable/channels/email/inboxes/{_path(inbox_id)}/messages",
            body=input,
        )

    def get(self, inbox_id: str, message_id: str) -> object:
        return self._client.request(
            "GET",
            f"/api/durable/channels/email/inboxes/{_path(inbox_id)}/messages/{_path(message_id)}",
        )


class _MessagingChannels:
    def __init__(self, client: DurableClient) -> None:
        self._client = client
        self.phones = _MessagingPhones(client)

    def status(self) -> object:
        return self._client.request("GET", "/api/durable/channels/messaging/status")


class _MessagingPhones:
    def __init__(self, client: DurableClient) -> None:
        self._client = client

    def list(self, **params: object) -> object:
        return self._client.request("GET", "/api/durable/channels/messaging/phones", params=params)

    def verify(self, input: JsonObject) -> object:
        return self._client.request("POST", "/api/durable/channels/messaging/phones/verify", body=input)

    def confirm(self, input: JsonObject) -> object:
        return self._client.request("POST", "/api/durable/channels/messaging/phones/confirm", body=input)

    def delete(self, phone_id: str) -> object:
        return self._client.request("DELETE", f"/api/durable/channels/messaging/phones/{_path(phone_id)}")


class _SlackChannels:
    def __init__(self, client: DurableClient) -> None:
        self._client = client

    def manifest(self, **params: object) -> object:
        return self._client.request("GET", "/api/durable/channels/slack/manifest", params=params)


class _ChannelEndpoints:
    def __init__(self, client: DurableClient) -> None:
        self._client = client

    def list(self, **params: object) -> object:
        return self._client.request("GET", "/api/durable/channels/endpoints", params=params)


class _ChannelBindings:
    def __init__(self, client: DurableClient) -> None:
        self._client = client

    def put(self, input: JsonObject) -> object:
        return self._client.request("POST", "/api/durable/channels/bindings", body=input)

    def delete(self, input: JsonObject) -> object:
        return self._client.request("DELETE", "/api/durable/channels/bindings", body=input)


class _Usage:
    def __init__(self, client: DurableClient) -> None:
        self._client = client

    def get(self) -> object:
        return self._client.request("GET", "/api/durable/billing/usage")


class _Audit:
    def __init__(self, client: DurableClient) -> None:
        self._client = client

    def list(self, **params: object) -> object:
        return self._client.request("GET", "/api/durable/audit", params=params)

    def iterate(self, **params: object) -> Iterator[object]:
        return paginate(lambda page_params: _expect_mapping(self.list(**page_params)), params)


def _path(value: str) -> str:
    return quote(value, safe="")


def _strip_trailing_slash(value: str) -> str:
    return value.rstrip("/")


def _clean_params(params: QueryParams | None) -> dict[str, object]:
    return {key: value for key, value in dict(params or {}).items() if value is not None}


def _expect_mapping(value: object) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise TypeError("Expected Durable API page response to be a mapping.")
    return value
