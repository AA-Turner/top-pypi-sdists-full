# Copyright 2025 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.
from __future__ import annotations

from typing import TypedDict

QueryErrorField = str
QueryErrorMessage = str


class QueryError(TypedDict):
    """A GraphQL query error."""

    message: QueryErrorMessage
    fields: list[QueryErrorField] | None


class GraphQLClientError(Exception):
    """Base exception for client side GraphQL errors."""


class GraphQLQueryError(GraphQLClientError):
    """Errors that occurred while executing a GraphQL query."""

    _UNKNOWN_ERROR = "Unknown error"
    _EMPTY_ERRORS = "An error occurred while executing the query"

    def __init__(self, errors: list[QueryError]):
        super().__init__(errors)
        self._errors = errors

    def _format_error(self, error: QueryError) -> str:
        message = error.get("message", "")
        fields = error.get("fields") or []

        fields_str = self._format_error_fields(fields)

        if fields_str and not message:
            message = self._UNKNOWN_ERROR

        result = f"{message} {fields_str}"
        return result.strip()

    @staticmethod
    def _format_error_fields(fields: list[QueryErrorField]) -> str:
        result = ", ".join([field.strip() for field in fields if field.strip()])

        if result:
            result = f"(fields: {result})"

        return result

    def __str__(self) -> str:
        errors = [self._format_error(error) for error in self._errors]
        errors = [error for error in errors if error]

        if not errors:
            return self._EMPTY_ERRORS

        lines = ["The following errors occurred:"]
        lines.extend(f"- {error}" for error in errors)

        return "\n".join(lines)
