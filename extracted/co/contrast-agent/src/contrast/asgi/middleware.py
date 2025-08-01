# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from functools import cached_property, lru_cache

import contrast
from contrast.agent import agent_state, request_state, scope as scope_
from contrast.agent.framework import UNKNOWN_FRAMEWORK
from contrast.agent.policy.trigger_node import TriggerNode
from contrast.agent.middlewares.base_middleware import (
    BaseMiddleware,
)
from contrast.agent.asgi import (
    track_scope_sources,
    ASGIRequest,
    ASGIResponse,
)
from contrast.agent.request_context import RequestContext
from contrast.utils.safe_import import safe_import_list
from contrast.utils.assess.duck_utils import safe_getattr_list

from contrast_vendor import structlog as logging


logger = logging.getLogger("contrast")

DEFAULT_ASGI_NAME = "asgi_app"


@lru_cache(maxsize=1)
def _get_quart_types():
    return tuple(safe_import_list("quart.Quart"))


class ASGIMiddleware(BaseMiddleware):
    @scope_.contrast_scope()
    def __init__(
        self,
        app,
        app_name=None,
        original_app=None,
        *,
        framework_name: str = UNKNOWN_FRAMEWORK.name,
    ):
        """
        Contrast middleware - ASGI 3.0

        The `app` argument here must be named "app" exactly to support FastAPI's
        middleware system, which uses the kwarg when calling this method.

        We need to keep the `original_app` kwarg for now to prevent a breaking API
        change.
        """
        del original_app

        # TODO: PYT-2852 Revisit application name detection
        self.app_name = (
            app_name
            if app_name is not None
            else safe_getattr_list(
                app,
                [
                    "__name__",
                    "name",
                    "title",
                ],
                DEFAULT_ASGI_NAME,
            )
        )
        self.framework_name = framework_name
        agent_state.set_detected_framework(self.framework_name)

        super().__init__()

        if not agent_state.in_automatic_middleware() and isinstance(
            app, _get_quart_types()
        ):
            # we need this to prevent a breaking API change when wrapping Quart apps
            app = app.asgi_app

        self.asgi_app = app

    async def __call__(self, scope, receive, send) -> None:
        if request_state.get_request_id() is not None:
            # This can happen if a single app is wrapped by multiple instances of the
            # middleware (usually caused by automatic instrumentation)
            logger.debug("Detected preexisting request_id - passing through")
            await self.asgi_app(scope, receive, send)
            return

        request_path = scope.get("path", "")
        request_method = scope.get("method", "")

        if scope.get("type") != "http":
            logger.debug("Detected non-http request - cannot analyze", scope=scope)
            await self.call_without_agent_async(scope, receive, send)
            return

        with self.request_context_stack(
            request_method, request_path
        ) as request_context_stack:
            request = ASGIRequest(scope, receive)
            environ = await request.to_wsgi_environ()

            context = self.should_analyze_request(environ)
            if context:
                self.enter_agent_call_contexts(request_context_stack, context)
                await self.call_with_agent(context, request, send)
                return

            await self.call_without_agent_async(scope, request.contrast__receive, send)

    async def call_with_agent(self, context: RequestContext, request, send) -> None:
        with scope_.contrast_scope():
            track_scope_sources(context, request.scope)

            try:
                self.prefilter(context)

                response = ASGIResponse(send)
                with scope_.pop_contrast_scope():
                    try:
                        await self.asgi_app(
                            request.scope,
                            request.contrast__receive,
                            response.contrast__send,
                        )
                        context.extract_response(response)
                    except Exception as exc:
                        context.response_exception = exc
                        raise

                self.postfilter(context)
                self.check_for_blocked(context)

            finally:
                self.handle_ensure(context, context.request)
                if context.assess_enabled:
                    contrast.STRING_TRACKER.ageoff()

    async def call_without_agent_async(self, scope, receive, send) -> None:
        with scope_.contrast_scope():
            await self.asgi_app(scope, receive, send)

    @cached_property
    def trigger_node(self):
        """
        trigger node used by reflected xss postfilter rule
        """
        method_name = self.app_name

        module, class_name, args, instance_method = self._process_trigger_handler(
            self.asgi_app
        )

        return (
            TriggerNode(module, class_name, instance_method, method_name, "RETURN"),
            args,
        )

    @cached_property
    def name(self):
        return "asgi"
