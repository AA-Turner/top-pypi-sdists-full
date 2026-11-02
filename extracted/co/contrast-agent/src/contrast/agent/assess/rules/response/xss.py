# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent import scope
from contrast.agent.assess.policy import trigger_policy
from contrast.agent.context import WebContext
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

# it is possible other forms (capital case) variants exist
SAFE_XSS_RESPONSE_CONTENT_TYPES = (
    "/csv",
    "/javascript",
    "/json",
    "/pdf",
    "/x-javascript",
    "/x-json",
    "+json",
    "/plain",
)


def is_safe_xss_content_type(content_type: str) -> bool:
    return any(name in content_type for name in SAFE_XSS_RESPONSE_CONTENT_TYPES)


def analyze_xss(trigger_node, web_context: WebContext):
    logger.debug("ASSESS: Running xss response analysis")

    content_type = web_context.response.headers.get("content-type", "")

    if not is_safe_xss_content_type(content_type):
        apply_policy(trigger_node, web_context)


def apply_policy(trigger_node, web_context: WebContext):
    """
    Evaluate xss rule for assess

    The xss rule is applied to the response body in order to determine whether it
    contains untrusted data. We rely on propagation through any template rendering
    and through the framework. The expectation is that untrusted data from
    a request will propagate successfully all the way to the response body, which
    we are able to see here.

    Each child middleware class must implement specific logic for the trigger node
    since the reporting will differ between frameworks.
    """
    from contrast.agent.policy import registry

    rule = registry.get_triggers_by_rule("reflected-xss")

    # We need to exit scope here in order to account for the fact that some
    # frameworks evaluate the content lazily. We don't want to be in scope when
    # that occurs since it would make us lose propagation. This would prevent us
    # from seeing the response as a tracked string, which we require in order to
    # apply the rule.
    with scope.pop_contrast_scope():
        result = web_context.response.body

    trigger_node, args = trigger_node

    trigger_policy.apply(rule, [trigger_node], result, args)
