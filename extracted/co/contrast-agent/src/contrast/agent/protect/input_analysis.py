# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations


from typing import Any
import contrast

import xml.etree.ElementTree
from xml.etree.ElementTree import ParseError

from contrast.agent.exclusions import Exclusions
from contrast.agent.request_context import RequestContext
from contrast.api.user_input import DocumentType
from contrast.agent.settings import Settings
from contrast.agent.agent_lib import input_tracing
from contrast_vendor import structlog as logging
from contrast.utils.decorators import fail_quietly
from contrast_agent_lib import constants

logger = logging.getLogger("contrast")


def _get_enabled_rules() -> int:
    """
    This converts our list of enabled rules to an integer value as the bitmask that the
    Agent Library expects.
    """
    rules = 0
    settings = Settings()

    for rule_tuple in settings.protect_rules.items():
        if (
            rule_tuple
            and rule_tuple[1]
            and rule_tuple[1].enabled
            and rule_tuple[1].RULE_NAME in constants.RuleType
        ):
            rules |= constants.RuleType[rule_tuple[1].RULE_NAME]
    return rules


def analyze_inputs() -> None:
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

    context.user_input_analysis = []

    rules = _get_enabled_rules()

    # Input analysis for all the input_tracing.InputType enum values
    _evaluate_headers(context, rules)
    _evaluate_cookies(context, rules)
    _evaluate_body(context, rules)
    _call_check_method_tampering(context)
    _evaluate_query_string_params(context, rules)
    _call_agent_lib_evaluate_input(
        constants.InputType["UriPath"],
        context.request.path,
        rules,
        context,
    )
    _evaluate_path_params(context, rules)
    _evaluate_multipart_request(context, rules)


def _evaluate_headers(context: RequestContext, rules: int) -> None:
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
            context.user_input_analysis.extend(input_analysis)
            # Report and block attack if necessary
            _report_and_block_at_perimeter(
                input_analysis,
                ["bot-blocker", "reflected-xss", "unsafe-file-upload"],
                context,
            )


def _evaluate_cookies(context: RequestContext, rules: int) -> None:
    for cookie_name, cookie_value in context.request.cookies.items():
        if check_param_input_exclusions(context.exclusions, "COOKIE", cookie_name):
            continue

        _call_agent_lib_evaluate_input(
            constants.InputType["CookieName"],
            cookie_name,
            rules,
            context,
        )
        _call_agent_lib_evaluate_input(
            constants.InputType["CookieValue"],
            cookie_value,
            rules,
            context,
            input_key=cookie_name,
        )


@fail_quietly("Failed to evaluate body")
def _evaluate_body(context: RequestContext, rules: int) -> None:
    if not context.request.is_body_readable:
        return
    if check_url_input_exclusion(context.exclusions, "BODY", context.request.url):
        return

    body_type = context.request._get_document_type()
    if body_type == DocumentType.JSON:
        try:
            json_body = context.request.json
        except Exception as e:
            logger.debug("WARNING: Failed to parse JSON in request body", exc_info=e)
            return
        _evaluate_body_json(context, rules, json_body)
    elif body_type == DocumentType.XML:
        try:
            data = xml.etree.ElementTree.fromstring(context.request.body)
        except ParseError as e:
            logger.debug("WARNING: Failed to parse XML in request body", exc_info=e)
            return

        text_list = [element.text for element in data]

        for text in text_list:
            if not str(text).startswith("\n"):
                _call_agent_lib_evaluate_input(
                    constants.InputType["XmlValue"],
                    str(text),
                    rules,
                    context,
                )
    else:
        _evaluate_key_value_parameters(context, rules, querystring=False)


def _evaluate_body_json(context: RequestContext, rules: int, body: Any) -> None:
    # Using recursion for now to get all the json values and keys and pass them
    # through agent_lib until agent_lib implements parsing of the body for python
    if isinstance(body, dict):
        for key, value in body.items():
            _call_agent_lib_evaluate_input(
                constants.InputType["JsonKey"],
                key,
                rules,
                context,
            )
            _evaluate_body_json(context, rules, value)
    elif isinstance(body, list):
        for item in body:
            _evaluate_body_json(context, rules, item)
    elif isinstance(body, str):
        _call_agent_lib_evaluate_input(
            constants.InputType["JsonValue"],
            body,
            rules,
            context,
        )


def _evaluate_query_string_params(context: RequestContext, rules: int) -> None:
    """
    Get agent-lib input analysis for all query parameters. This information is stored on
    request context.
    """
    if check_url_input_exclusion(
        context.exclusions, "QUERYSTRING", context.request.url
    ):
        return

    _evaluate_key_value_parameters(context, rules, querystring=True)


def _evaluate_key_value_parameters(
    context: RequestContext, rules: int, *, querystring: bool
) -> None:
    """
    Used for both form parameters (from the request body) and query string parameters
    """
    param_dict = context.request.GET if querystring else context.request.POST

    for param_key, param_value in param_dict.items():
        if not isinstance(param_value, str):
            continue

        _call_agent_lib_evaluate_input(
            constants.InputType["ParameterKey"],
            param_key,
            rules,
            context,
            input_key=param_key,
        )
        _call_agent_lib_evaluate_input(
            constants.InputType["ParameterValue"],
            param_value,
            rules,
            context,
            input_key=param_key,
        )


def _evaluate_path_params(context: RequestContext, rules: int) -> None:
    """
    Get agent-lib input analysis for all path parameters. This information is
    stored on request context.
    """
    for param in context.request.get_url_parameters():
        if check_param_input_exclusions(context.exclusions, "PARAMETER", param):
            continue

        _call_agent_lib_evaluate_input(
            constants.InputType["UrlParameter"],
            param,
            rules,
            context,
        )


def _evaluate_multipart_request(context: RequestContext, rules: int):
    """
    This is refering to Content-Type: multipart/form-data and checking the file_name for every
    multipart request if there is none it checks the name
    """
    for key, value in context.request.get_multipart_headers().items():
        if value is None and key is None:
            continue

        multipart_name = value if value is not None else key
        _call_agent_lib_evaluate_input(
            constants.InputType["MultipartName"],
            multipart_name,
            rules,
            context,
        )


def _call_check_method_tampering(context: RequestContext) -> None:
    input_analysis_value = input_tracing.check_method_tampering(context.request.method)

    if input_analysis_value:
        context.user_input_analysis.extend(input_analysis_value)
        _report_and_block_at_perimeter(
            input_analysis_value, ["reflected-xss", "unsafe-file-upload"], context
        )


def _call_agent_lib_evaluate_input(
    input_type: int,
    input_value: str,
    rule_set: int,
    context: RequestContext,
    *,
    input_key="",
) -> None:
    input_analysis_results = input_tracing.evaluate_input_by_type(
        input_type, input_value, input_key, rule_set, prefer_worth_watching=True
    )

    if input_analysis_results:
        context.user_input_analysis.extend(input_analysis_results)
        _report_and_block_at_perimeter(
            input_analysis_results, ["reflected-xss", "unsafe-file-upload"], context
        )


def _report_and_block_at_perimeter(
    input_analysis: list[input_tracing.InputAnalysisResult],
    perimeter_rule_names: list[str],
    context: RequestContext,
) -> None:
    """
    Checks a list of rules and reports if it finds a score(int with value 0-100 indicating percentage
    of certainty of attack) higher than 90 and blocks if the agent is configured in block mode.
    """
    settings = Settings()
    for result in input_analysis:
        if result.rule_id not in perimeter_rule_names:
            continue
        if rule := settings.protect_rules.get(result.rule_id):
            attack = rule.build_attack_with_match(result.input.value, result, None)
            context.attacks.append(attack)

            if result.score >= 90:
                logger.debug(
                    f"Input analysis found a value '{result.input.value}' "
                    f"that violated {rule.RULE_NAME} rule!"
                )

                if rule.is_blocked():
                    raise contrast.SecurityException(rule_name=rule.RULE_NAME)


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
