# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from functools import cached_property

import contrast

from aiohttp.web import StreamResponse
from aiohttp.web_urldispatcher import DynamicResource

from contrast.agent.request_context import RequestContext
from contrast.aiohttp import sources
from contrast.agent import scope, request_state, agent_state
from contrast.agent.middlewares.route_coverage.aiohttp_routes import (
    create_aiohttp_routes,
)
from contrast.agent.middlewares.route_coverage import common
from contrast.agent.policy.trigger_node import TriggerNode
from contrast_vendor import structlog as logging
from contrast.agent.middlewares.base_middleware import (
    BaseMiddleware,
)
from contrast.agent.middlewares.response_wrappers.aiohttp_response_wrapper import (
    AioHttpResponseWrapper,
)

from contrast.utils.decorators import fail_quietly

logger = logging.getLogger("contrast")


class AioHttpMiddleware(BaseMiddleware):
    __middleware_version__ = 1  # Aiohttp new-style middleware

    # Since there is no way to get the `app` instance, on startup of AioHttp,
    # until the first request, hence we will not have `app` finder logic.
    @scope.contrast_scope()
    def __init__(self, app_name: str | None = None) -> None:
        self.app = None
        self.app_name = app_name or "aiohttp"
        agent_state.set_detected_framework("aiohttp")
        super().__init__()

    async def __call__(self, request, handler) -> StreamResponse:
        if request_state.get_request_id() is not None:
            # This can happen if a single app is wrapped by multiple instances of the
            # middleware (usually caused by automatic instrumentation)
            logger.debug("Detected preexisting request_id - passing through")
            return await handler(request)

        self.app = request.app

        with self.request_context_stack(
            request.method, request.path
        ) as request_context_stack:
            with scope.contrast_scope():
                environ = await sources.aiohttp_request_to_environ(request)

            context = self.should_analyze_request(environ)
            if context:
                self.enter_agent_call_contexts(request_context_stack, context)
                return await self.call_with_agent(context, request, handler)

            return await self.call_without_agent_async(request, handler)

    async def call_with_agent(
        self, context: RequestContext, request, handler
    ) -> StreamResponse:
        with scope.contrast_scope():
            sources.track_aiohttp_request_sources(context, request)

            try:
                self.prefilter(context)

                with scope.pop_contrast_scope():
                    try:
                        response = await handler(request)
                        wrapped_response = AioHttpResponseWrapper(response)
                        context.extract_response(wrapped_response)
                    except Exception as exc:
                        context.response_exception = exc
                        raise

                self.postfilter(context)
                self.check_for_blocked(context)

                return response

            finally:
                if context.assess_enabled:
                    self.do_aiohttp_first_request_analysis()
                    self.do_aiohttp_route_observation(context, request)
                self.handle_ensure(context, request)
                if context.assess_enabled:
                    contrast.STRING_TRACKER.ageoff()

    async def call_without_agent_async(self, request, handler) -> StreamResponse:
        with scope.contrast_scope():
            return await handler(request)

    @fail_quietly()
    def do_aiohttp_first_request_analysis(self) -> None:
        if not agent_state.is_first_request():
            return

        common.handle_route_discovery("aiohttp", create_aiohttp_routes, (self.app,))

    @fail_quietly()
    def do_aiohttp_route_observation(self, context, request) -> None:
        view_func = self.get_aiohttp_view_func(request)
        if view_func is None:
            logger.debug("unable to get view function for aiohttp route observation")
            return

        context.signature = common.build_signature(view_func.__name__, view_func)
        logger.debug("Observed aiohttp route", signature=context.signature)

    @fail_quietly("Unable to get view func")
    def get_aiohttp_view_func(self, request):
        """
        This intentionally does not override get_view_func. We're generally making route
        coverage more framework-specific; this minimizes shared machinery between
        aiohttp middleware and its base classes.
        """
        if not request.path:
            return None

        view_func = None

        # This approach has at worst O(_resources) performance
        # but it's a first attempt at implementing a sync
        # version of aiohttp.web_urldispatches.UrlDispatcher.resolve
        for app_route in self.app.router._resources:
            _app_route = (
                app_route._formatter
                if isinstance(app_route, DynamicResource)
                else app_route._path
            )
            if _app_route == request.path:
                routes = app_route._routes
                for route in routes:
                    if route.method == request.method:
                        return route.handler

        return view_func

    @cached_property
    def trigger_node(self):
        """
        Used by reflected xss postfilter rule
        """
        method_name = self.app_name

        module, class_name, args, instance_method = self._process_trigger_handler(
            self.app
        )

        return (
            TriggerNode(module, class_name, instance_method, method_name, "RETURN"),
            args,
        )

    @cached_property
    def name(self):
        return "aiohttp"
