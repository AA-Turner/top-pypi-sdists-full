# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import xml.etree.ElementTree
from typing import TYPE_CHECKING, Any
from xml.etree.ElementTree import ParseError

from contrast_agent_lib import constants
from contrast_fireball import DocumentType

import contrast
from contrast.agent.agent_lib import input_tracing
from contrast.utils.decorators import fail_quietly
from contrast_vendor import structlog as logging

if TYPE_CHECKING:
    from contrast.agent.exclusions import Exclusions
    from contrast.agent.protect.rule.base_rule import BaseRule
    from contrast.agent.request_context import RequestContext
    from contrast_vendor.webob.multidict import MultiDict

logger = logging.getLogger("contrast")


def agentlib_rules_mask(rules: list[BaseRule]) -> int:
    """
    Converts a list of rules to an integer bitmask for agent-lib.
    """
    mask = 0
    for rule in rules:
        if not rule.enabled:
            continue
        mask |= constants.RuleType.get(rule.RULE_NAME, 0)
    return mask


def analyze_inputs(rules: list[BaseRule]) -> None:
    """
    Perform input analysis through agent-lib. Results are stored on
    context.user_input_analysis, which is reset every time this function is called.

    Some rules have a special "worth watching" analysis mode. In prefilter, we use this
    more liberal mode to ensure we don't miss attacks that should be blocked at trigger
    time. However, if we make it to the end of the request (without raising a
    SecurityException), we redo input analysis with worth watching mode disabled, which
    leads to more accurate PROBED results (fewer PROBED FPs).
    """
    context = contrast.REQUEST_CONTEXT.get()
    if context is None:
        return

    agentlib_rules = agentlib_rules_mask(rules)

    results: list[input_tracing.InputAnalysisResult] = []

    results.extend(_evaluate_headers(context, agentlib_rules))
    results.extend(_evaluate_cookies(context, agentlib_rules))
    results.extend(_evaluate_body(context, agentlib_rules))
    results.extend(_call_check_method_tampering(context))
    results.extend(_evaluate_query_string_params(context, agentlib_rules))
    results.extend(
        _call_agent_lib_evaluate_input(
            constants.InputType["UriPath"],
            context.request.path,
            agentlib_rules,
        )
    )
    results.extend(_evaluate_path_params(context, agentlib_rules))
    results.extend(_evaluate_multipart_request(context, agentlib_rules))

    context.user_input_analysis = results


def _evaluate_headers(
    context: RequestContext, rules: int
) -> list[input_tracing.InputAnalysisResult]:
    results: list[input_tracing.InputAnalysisResult] = []
    for header_name, header_value in context.request.headers.items():
        if "cookie" in header_name.lower() or check_param_input_exclusions(
            context.exclusions, "HEADER", header_name
        ):
            continue

        input_analysis = input_tracing.evaluate_header_input(
            header_name,
            header_value,
            rules,
            prefer_worth_watching=True,
        )

        if input_analysis:
            results.extend(input_analysis)

    return results


def _evaluate_cookies(
    context: RequestContext, rules: int
) -> list[input_tracing.InputAnalysisResult]:
    results: list[input_tracing.InputAnalysisResult] = []
    for cookie_name, cookie_value in context.request.cookies.items():
        if check_param_input_exclusions(context.exclusions, "COOKIE", cookie_name):
            continue

        results.extend(
            _call_agent_lib_evaluate_input(
                constants.InputType["CookieName"],
                cookie_name,
                rules,
            )
        )
        results.extend(
            _call_agent_lib_evaluate_input(
                constants.InputType["CookieValue"],
                cookie_value,
                rules,
                input_key=cookie_name,
            )
        )

    return results


@fail_quietly("Failed to evaluate body")
def _evaluate_body(
    context: RequestContext, rules: int
) -> list[input_tracing.InputAnalysisResult]:
    results: list[input_tracing.InputAnalysisResult] = []

    if not context.request.is_body_readable:
        return results
    if check_url_input_exclusion(context.exclusions, "BODY", context.request.url):
        return results

    body_type = context.request._get_document_type()
    if body_type == DocumentType.JSON:
        try:
            json_body = context.request.json
        except Exception as e:
            logger.debug("WARNING: Failed to parse JSON in request body", exc_info=e)
            return results
        results.extend(_evaluate_body_json(context, rules, json_body))
    elif body_type == DocumentType.XML:
        try:
            data = xml.etree.ElementTree.fromstring(context.request.body)
        except ParseError as e:
            logger.debug("WARNING: Failed to parse XML in request body", exc_info=e)
            return results

        text_list = [element.text for element in data]

        for text in text_list:
            if not str(text).startswith("\n"):
                results.extend(
                    _call_agent_lib_evaluate_input(
                        constants.InputType["XmlValue"],
                        str(text),
                        rules,
                    )
                )
    else:
        results.extend(_evaluate_key_value_parameters(context.request.POST, rules))

    return results


def _evaluate_body_json(
    context: RequestContext, rules: int, body: Any
) -> list[input_tracing.InputAnalysisResult]:
    # Using recursion for now to get all the json values and keys and pass them
    # through agent_lib until agent_lib implements parsing of the body for python
    results: list[input_tracing.InputAnalysisResult] = []

    if isinstance(body, dict):
        for key, value in body.items():
            results.extend(
                _call_agent_lib_evaluate_input(
                    constants.InputType["JsonKey"],
                    key,
                    rules,
                )
            )
            results.extend(_evaluate_body_json(context, rules, value))
    elif isinstance(body, list):
        for item in body:
            results.extend(_evaluate_body_json(context, rules, item))
    elif isinstance(body, str):
        results.extend(
            _call_agent_lib_evaluate_input(
                constants.InputType["JsonValue"],
                body,
                rules,
            )
        )

    return results


def _evaluate_query_string_params(
    context: RequestContext, rules: int
) -> list[input_tracing.InputAnalysisResult]:
    """
    Get agent-lib input analysis for all query parameters. This information is stored on
    request context.
    """
    if check_url_input_exclusion(
        context.exclusions, "QUERYSTRING", context.request.url
    ):
        return []

    return _evaluate_key_value_parameters(
        context.request.GET,
        rules,
    )


def _evaluate_key_value_parameters(
    param_dict: MultiDict,
    rules: int,
) -> list[input_tracing.InputAnalysisResult]:
    """
    Used for both form parameters (from the request body) and query string parameters
    """
    results: list[input_tracing.InputAnalysisResult] = []

    for param_key, param_value in param_dict.items():
        if not isinstance(param_value, str):
            continue

        results.extend(
            _call_agent_lib_evaluate_input(
                constants.InputType["ParameterKey"],
                param_key,
                rules,
                input_key=param_key,
            )
        )
        results.extend(
            _call_agent_lib_evaluate_input(
                constants.InputType["ParameterValue"],
                param_value,
                rules,
                input_key=param_key,
            )
        )

    return results


def _evaluate_path_params(
    context: RequestContext, rules: int
) -> list[input_tracing.InputAnalysisResult]:
    """
    Get agent-lib input analysis for all path parameters. This information is
    stored on request context.
    """
    results: list[input_tracing.InputAnalysisResult] = []
    for param in context.request.get_url_parameters():
        if check_param_input_exclusions(context.exclusions, "PARAMETER", param):
            continue

        results.extend(
            _call_agent_lib_evaluate_input(
                constants.InputType["UrlParameter"],
                param,
                rules,
            )
        )

    return results


def _evaluate_multipart_request(
    context: RequestContext, rules: int
) -> list[input_tracing.InputAnalysisResult]:
    """
    This is refering to Content-Type: multipart/form-data and checking the file_name for every
    multipart request if there is none it checks the name
    """
    results: list[input_tracing.InputAnalysisResult] = []
    for key, value in context.request.get_multipart_headers().items():
        if value is None and key is None:
            continue

        multipart_name = value if value is not None else key
        results.extend(
            _call_agent_lib_evaluate_input(
                constants.InputType["MultipartName"],
                multipart_name,
                rules,
            )
        )

    return results


def _call_check_method_tampering(
    context: RequestContext,
) -> list[input_tracing.InputAnalysisResult]:
    input_analysis_value = input_tracing.check_method_tampering(context.request.method)

    if input_analysis_value:
        return list(input_analysis_value)
    return []


def _call_agent_lib_evaluate_input(
    input_type: int,
    input_value: str,
    rule_set: int,
    *,
    input_key="",
) -> list[input_tracing.InputAnalysisResult]:
    input_analysis_results = input_tracing.evaluate_input_by_type(
        input_type, input_value, input_key, rule_set, prefer_worth_watching=True
    )

    if input_analysis_results:
        return list(input_analysis_results)
    return []


def check_url_input_exclusion(
    exclusions: Exclusions | None, input_type: str, input_name: str
) -> bool:
    if not exclusions:
        return False

    return exclusions.evaluate_input_exclusions_url(
        exclusions, input_type, input_name, mode="defend"
    )


def check_param_input_exclusions(
    exclusions: Exclusions | None, input_type: str, input_name: str
) -> bool:
    if not exclusions:
        return False

    return exclusions.evaluate_input_exclusions(
        exclusions, input_type, input_name, mode="defend"
    )
