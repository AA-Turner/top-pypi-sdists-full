# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from functools import cached_property, lru_cache
from contrast.agent.framework import UNKNOWN_FRAMEWORK
from contrast.agent.request_context import RequestContext
from contrast_vendor.webob import Request

import contrast
from contrast.agent import agent_state, scope, request_state
from contrast.agent.policy.trigger_node import TriggerNode
from contrast.agent.middlewares.base_middleware import (
    BaseMiddleware,
)
from contrast.agent.middlewares.environ_tracker import track_environ_sources
from contrast.utils.safe_import import safe_import_list
from contrast.utils.assess.duck_utils import safe_getattr_list

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")
DEFAULT_WSGI_NAME = "wsgi_app"


@lru_cache(maxsize=1)
def _get_flask_types():
    return tuple(safe_import_list("flask.Flask"))


class WSGIMiddleware(BaseMiddleware):
    """
    Contrast middleware; PEP-333(3) WSGI-compliant
    """

    @scope.contrast_scope()
    def __init__(
        self,
        wsgi_app,
        app_name=None,
        original_app=None,
        orig_pyramid_registry=None,
        *,
        framework_name: str = UNKNOWN_FRAMEWORK.name,
    ):
        # We need to keep the `original_app` `orig_pyramid_registry` kwarg for now to prevent a breaking API
        # change
        del original_app
        del orig_pyramid_registry

        # TODO: PYT-2852 Revisit application name detection
        self.app_name = (
            app_name
            if app_name is not None
            else safe_getattr_list(
                wsgi_app,
                [
                    "__name__",
                    "name",
                ],
                DEFAULT_WSGI_NAME,
            )
        )
        self.framework_name = framework_name
        agent_state.set_detected_framework(self.framework_name)

        super().__init__()

        if not agent_state.in_automatic_middleware() and isinstance(
            wsgi_app, _get_flask_types()
        ):
            # we need this to prevent a breaking API change when wrapping Flask apps
            wsgi_app = wsgi_app.wsgi_app

        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        if request_state.get_request_id() is not None:
            # This can happen if a single app is wrapped by multiple instances of the
            # middleware (usually caused by automatic instrumentation)
            logger.debug("Detected preexisting request_id - passing through")
            return self.wsgi_app(environ, start_response)

        request_path = environ.get("PATH_INFO", "")
        request_method = environ.get("REQUEST_METHOD", "")

        with self.request_context_stack(
            request_method, request_path
        ) as request_context_stack:
            context = self.should_analyze_request(environ)
            if context:
                self.enter_agent_call_contexts(request_context_stack, context)
                return self.call_with_agent(context, environ, start_response)

            return self.call_without_agent(environ, start_response)

    @scope.contrast_scope()
    def call_with_agent(self, context: RequestContext, environ, start_response):
        track_environ_sources("wsgi", context, environ)

        try:
            self.prefilter(context)

            webob_request = Request(environ)
            with scope.pop_contrast_scope():
                try:
                    response = webob_request.get_response(self.wsgi_app)
                    context.extract_response(response)
                except Exception as exc:
                    context.response_exception = exc
                    raise

            self.postfilter(context)
            self.check_for_blocked(context)

            return response(environ, start_response)

        finally:
            self.handle_ensure(context, context.request)
            if context.assess_enabled:
                contrast.STRING_TRACKER.ageoff()

    @scope.contrast_scope()
    def call_without_agent(self, environ, start_response):
        """
        Normal without middleware call
        """
        return self.wsgi_app(environ, start_response)

    @cached_property
    def trigger_node(self):
        """
        WSGI-specific trigger node used by reflected xss postfilter rule

        The rule itself is implemented in the base middleware but we need to
        provide a WSGI-specific trigger node for reporting purposes.
        """
        method_name = self.app_name

        module, class_name, args, instance_method = self._process_trigger_handler(
            self.wsgi_app
        )

        return (
            TriggerNode(module, class_name, instance_method, method_name, "RETURN"),
            args,
        )

    @cached_property
    def name(self):
        return "wsgi"
