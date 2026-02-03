# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING

import contrast_agent_lib
from contrast_fireball import (
    AttackInputType,
    OtelAttributes,
)

from contrast.agent import scope
from contrast.agent.agent_lib.input_tracing import (
    evaluate_input_by_type,
)
from contrast.agent.policy.handlers import EventDict, EventHandler
from contrast.agent.protect.input_analysis import agentlib_rules_mask
from contrast.agent.settings import Settings

if TYPE_CHECKING:
    from graphql import DocumentNode
    from graphql.language.ast import OperationDefinitionNode

from contrast.agent.request_context import RequestContext
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


def _select_operation(
    document: DocumentNode, requested_operation_name: str | None = None
) -> OperationDefinitionNode | None:
    """
    Given a parsed graphql document and (optionally) an operation name, select a single
    operation to report to the observability backend.

    In general, we expect there to be a single operation per document, since graphql
    clients tend to separate multi-operation documents into separate requests.
    """
    from graphql.language.ast import OperationDefinitionNode

    all_operations = [
        definition
        for definition in document.definitions
        if isinstance(definition, OperationDefinitionNode)
    ]

    if not all_operations:
        logger.debug("No operations found in parsed graphql query - will not report")
        return None

    filtered_operations = (
        [
            op
            for op in all_operations
            if op.name and op.name.value == requested_operation_name
        ]
        if requested_operation_name
        else all_operations
    )

    if len(filtered_operations) != 1:
        logger.debug(
            "Ambiguous graphql query - will not report",
            operations=[op.to_dict() for op in all_operations],
            requested_operation_name=requested_operation_name,
        )
        return None

    return filtered_operations[0]


def observe_handler_builder(
    event_dict: EventDict,
) -> EventHandler:
    def observe_handler(
        context: RequestContext | None, args: Mapping[str, object]
    ) -> Generator:
        from graphql import DocumentNode

        if (
            context is None
            or scope.in_observe_scope()
            or not (
                isinstance(args.get("context_value"), dict)
                and "request" in args["context_value"]
            )
        ):
            yield
            return
        with scope.observe_scope():
            if (trace := context.observability_trace) is None:
                yield
                return

            result = yield

            if not isinstance(result, DocumentNode):
                logger.debug(
                    "Found non-DocumentNode when observing a graphql request",
                    parsed_result=result,
                )
                return

            document = result
            requested_operation_name = args.get("data", {}).get("operationName", None)
            if not isinstance(requested_operation_name, (str, type(None))):
                logger.debug(
                    "Found invalid type for operationName in graphql request",
                    operation_name=requested_operation_name,
                )
                return

            operation = _select_operation(document, requested_operation_name)
            if operation is None:
                return

            attrs: OtelAttributes = {
                "graphql.operation.type": operation.operation.value,
            }
            if operation.name:
                attrs["graphql.operation.name"] = operation.name.value

            trace.update(attrs)

    return observe_handler


def protect_handler_builder(event_dict: EventDict) -> EventHandler:
    from graphql import DocumentNode
    from graphql.language import Visitor, visit
    from graphql.language.ast import NameNode, ValueNode

    class GraphQLValueVisitor(Visitor):
        def __init__(self) -> None:
            super().__init__()
            # values_to_analyze is a list of tuples of (path, value)
            self.values_to_analyze: list[tuple[str, str]] = []

        def enter(
            self,
            node: NameNode,
            key: str | int | None,
            parent: object | None,
            path: list[object | str] | None,
            ancestors: list[object | str] | None,
        ) -> None:
            if isinstance(node, (NameNode, ValueNode)) and isinstance(
                (value := getattr(node, "value", None)), str
            ):
                self.values_to_analyze.append((self.path_to_str(path), value))

        def path_to_str(self, path: list[object | str] | None) -> str:
            if path is None:
                return ""
            return ".".join(f"[{p}]" if isinstance(p, int) else str(p) for p in path)

    def protect_handler(
        context: RequestContext | None, args: Mapping[str, object]
    ) -> Generator:
        if context is None or not (
            isinstance(args.get("context_value"), dict)
            and "request" in args["context_value"]
        ):
            yield
            return

        result = yield
        if not isinstance(result, DocumentNode):
            logger.debug(
                "Found non-DocumentNode when protecting a graphql request",
                parsed_result=result,
            )
            return

        document = result
        value_collector = GraphQLValueVisitor()
        visit(document, value_collector)

        agentlib_rules = agentlib_rules_mask(list(Settings().protect_rules.values()))
        logger.debug(
            "Analyzing GraphQL values", values=value_collector.values_to_analyze
        )

        # remove json document value for "query". If we got this far, we must have
        # parsed the query successfully, so we should be able to safely remove this
        # input analysis result.
        _filter_previous_input_analysis_results(context)

        for path, value in value_collector.values_to_analyze:
            context.user_input_analysis.extend(
                evaluate_input_by_type(
                    contrast_agent_lib.constants.InputType["ParameterValue"],
                    value,
                    path,
                    agentlib_rules,
                    prefer_worth_watching=True,
                )
            )

    return protect_handler


GRAPHQL_QUERY_JSON_DOCUMENT_PATH = "$['query']"
"""
A graphql query sent in an HTTP request body with JSON encoding should be located under
a top-level key named "query". The current spec on this is here:

https://graphql.github.io/graphql-over-http/draft/#sec-JSON-Encoding

NOTE: if this is ever modified to contain uppercase characters, references to it likely
require an update too.
"""


def _filter_previous_input_analysis_results(context: RequestContext) -> None:
    """
    Input analysis for graphql queries occurs independently from the general input
    analysis we perform on every request. If we are able to run graphql-specific input
    analysis, we no longer need the less-specific results from generic input analysis.

    This function discards results from previous input analysis for the raw graphql
    query. We look specifically for JSON values whose document patch matches the
    expected location of the raw graphql query. This is essentially a best-effort to
    remove duplicate input analysis results.
    """
    for index, result in enumerate(context.user_input_analysis):
        if (
            result.input.input_type == AttackInputType.JSON_VALUE
            and result.input.document_path is not None
            # lower() _shouldn't_ be needed, but adds a bit of a safety net
            and result.input.document_path.lower() == GRAPHQL_QUERY_JSON_DOCUMENT_PATH
        ):
            logger.debug(
                "Filtering out JSON GraphQL query input analysis result",
                value=result.input.value[:100] + "..."
                if result.input.value and len(result.input.value) > 100
                else result.input.value,
            )
            context.user_input_analysis.pop(index)
