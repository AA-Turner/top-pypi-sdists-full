# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

from collections.abc import Mapping
from typing import Callable, Literal, cast, get_args

import contrast_fireball

from contrast.agent.policy.handlers import EventDict
from contrast.reporting import fireball

ApiProvider = Literal[
    "anthropic",
    "bedrock",
    "bedrock-agent",
    "deepseek",
    "openai",
    "vertex",
]


def ai_usage_event(
    api_url: str,
    api_provider: ApiProvider | None,
    model: str | None,
) -> fireball.LogRecordEvent:
    """
    Creates a LogRecordEvent for AI usage.
    """
    event_details = {
        "ai_usage.api_provider": api_provider,
        "ai_usage.api_url": api_url,
        "ai_usage.model": model,
    }
    return fireball.LogRecordEvent(
        contrast_fireball.LogRecordEventType.AiUsage,
        event_details,
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
        dict[str, ApiProvider], client_type_to_api_provider
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

        api_url = self.meta.endpoint_url
        params = args["api_params"]
        model = params.get("modelId") or params.get("foundationModel")

        return ai_usage_event(
            api_provider=service,
            api_url=api_url,
            model=model,
        )

    return log_record_attrs
