import httpx

from mistralai.workflows._version import USER_AGENT as _MISTRAL_USER_AGENT

from .types import BeforeRequestContext, BeforeRequestHook, Hooks

# This file is only ever generated once on the first generation and then is free to be modified.
# Any hooks you wish to add should be registered in the init_hooks function. Feel free to define them
# in this file or in separate files in the hooks folder.


class _AppendMistralUserAgentHook(BeforeRequestHook):
    """Append the Mistral worker user-agent to the Speakeasy-generated one.

    The Speakeasy basesdk unconditionally sets ``user-agent`` to its own value
    on every request, overriding the httpx client's default headers.  This hook
    runs after that assignment and appends our identifier so both values are
    preserved in the final header.
    """

    def before_request(self, hook_ctx: BeforeRequestContext, request: httpx.Request) -> httpx.Request:
        existing = request.headers.get("user-agent", "")
        new_value = f"{existing} {_MISTRAL_USER_AGENT}".strip() if existing else _MISTRAL_USER_AGENT
        headers = dict(request.headers)
        headers["user-agent"] = new_value
        return httpx.Request(
            method=request.method,
            url=request.url,
            headers=headers,
            content=request.content,
            extensions=request.extensions,
        )


def init_hooks(hooks: Hooks):
    # pylint: disable=unused-argument
    """Add hooks by calling hooks.register{sdk_init/before_request/after_success/after_error}Hook
    with an instance of a hook that implements that specific Hook interface
    Hooks are registered per SDK instance, and are valid for the lifetime of the SDK instance"""
    hooks.register_before_request_hook(_AppendMistralUserAgentHook())
