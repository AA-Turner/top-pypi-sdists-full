# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

from typing import TYPE_CHECKING, Literal, cast, get_args

import contrast_fireball

from contrast.reporting import fireball
from contrast.utils.stack_trace_utils import StackSummary, build_stack

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from contrast.agent.policy.handlers import EventDict

ApiProvider = Literal[
    "anthropic",
    "bedrock-agent",
    "bedrock",
    "deepseek",
    "gemini",
    # NOTE: Google moved "vertex" to the Gemini terminology umbrella, so we don't report
    # it separately anymore.
    "openai",
]


def ai_usage_event(
    api_url: str,
    api_provider: ApiProvider | None,
    model: str | None,
    stack: StackSummary | None = None,
) -> fireball.LogRecordEvent:
    """
    Creates a LogRecordEvent for AI usage.
    """
    if api_provider is not None and api_provider not in get_args(ApiProvider):
        raise ValueError(
            f"Invalid API provider '{api_provider}'. Must be one of: {get_args(ApiProvider)}."
        )
    event_details = {
        "ai_usage.api_provider": api_provider,
        "ai_usage.api_url": api_url,
        "ai_usage.model": model,
    }
    return fireball.LogRecordEvent(
        contrast_fireball.LogRecordEventType.AiUsage,
        event_details,
        stack=stack,
    )


def stainless_log_event_builder(
    event_dict: EventDict,
) -> Callable[
    [Mapping[str, object], object],
    fireball.LogRecordEvent | None,
]:
    if "client_type_to_api_provider" not in event_dict or not isinstance(
        event_dict["client_type_to_api_provider"], dict
    ):
        raise ValueError(
            "Event dict must contain 'client_type_to_api_provider' dict. "
            "Set the key to an empty dict if the provider is unknown."
        )
    client_type_to_api_provider = event_dict["client_type_to_api_provider"]
    for provider in client_type_to_api_provider.values():
        if provider is not None and provider not in get_args(ApiProvider):
            raise ValueError(
                f"Unknown API provider '{provider}' in client_type_to_api_provider. "
                f"Known providers are: {get_args(ApiProvider)}."
            )
    client_type_to_api_provider = cast(
        "dict[str, ApiProvider]", client_type_to_api_provider
    )

    def log_record_attrs(args: Mapping[str, object], result: object):
        model = args.get("model")
        client = args["self"]._client
        api_provider = client_type_to_api_provider.get(
            type(client).__module__ + "." + type(client).__name__, None
        )
        api_url = str(client.base_url)

        return ai_usage_event(
            api_provider=api_provider,
            api_url=api_url,
            model=model,
        )

    return log_record_attrs


def botocore_log_event_builder(
    event_dict: EventDict,
) -> Callable[
    [Mapping[str, object], object],
    fireball.LogRecordEvent | None,
]:
    def log_record_attrs(args: Mapping[str, object], result: object):
        self = args["self"]
        op_name = args["operation_name"]
        service = self.meta.service_model.service_name.lower()
        if (service, op_name) not in (
            ("bedrock-runtime", "InvokeModel"),
            ("bedrock-runtime", "InvokeModelWithResponseStream"),
            ("bedrock-runtime", "Converse"),
            ("bedrock-runtime", "ConverseStream"),
            ("bedrock-runtime", "StartAsyncInvoke"),
            ("bedrock-agent-runtime", "InvokeAgent"),
            ("bedrock-agent-runtime", "InvokeFlow"),
            ("bedrock-agent-runtime", "InvokeInlineAgent"),
            ("bedrock-agent-runtime", "StartFlowExecution"),
        ):
            return None  # Not an ai-usage call, don't create an event

        api_provider = service.removesuffix("-runtime")
        api_url = self.meta.endpoint_url
        params = args["api_params"]
        model = params.get("modelId") or params.get("foundationModel")

        stack = build_stack()[:-1]  # Exclude the botocore frame.

        return ai_usage_event(
            api_provider=api_provider,
            api_url=api_url,
            model=model,
            stack=stack,
        )

    return log_record_attrs


def google_genai_log_event_builder(
    event_dict: EventDict,
) -> Callable[
    [Mapping[str, object], object],
    fireball.LogRecordEvent,
]:
    def log_record_attrs(args: Mapping[str, object], result: object):
        self = args["self"]
        model = args.get("model")
        # Starting in google-genai v2.9.0, the Interactions API accepts model via **body
        # rather than as a dedicated keyword argument.
        if model is None:
            body = args.get("body")
            if isinstance(body, dict):
                model = body.get("model")

        # Get API URL from config if present, otherwise from client
        api_url = None
        config = args.get("config")
        if config is not None:
            # config can be a class or dict
            http_options = (
                getattr(config, "http_options", None)
                if not isinstance(config, dict)
                else config.get("http_options")
            )
            if http_options is not None:
                api_url = (
                    getattr(http_options, "base_url", None)
                    if not isinstance(http_options, dict)
                    else http_options.get("base_url")
                )

        # Get the API client - some objects have _api_client directly (Models, Batches),
        # others have it through _modules (Chats), others have _client (pre-2.9.0
        # Interactions)
        api_client = getattr(self, "_api_client", None)
        if api_client is None:
            api_client = getattr(self, "_client", None)
        if api_client is None:
            modules = getattr(self, "_modules", None)
            api_client = getattr(modules, "_api_client", None)

        if api_client is not None:
            if api_url is None:
                http_options = getattr(api_client, "_http_options", None)
                if http_options is not None:
                    api_url = str(http_options.base_url)
                else:
                    api_url = str(api_client.base_url)
        else:
            # The v2.9.0+ Interactions API exposes neither an api client nor an
            # http options object; its server URL is available through the SDK
            # configuration instead. Access it defensively so that future
            # library changes degrade gracefully rather than raising.
            sdk_configuration = getattr(self, "sdk_configuration", None)
            get_server_details = getattr(sdk_configuration, "get_server_details", None)
            server_url = ""
            if get_server_details is not None:
                server_url, _ = get_server_details()
            if api_url is None and server_url:
                api_url = server_url.rstrip("/") + "/"

        return ai_usage_event(
            api_provider="gemini",
            api_url=api_url,
            model=model,
        )

    return log_record_attrs
