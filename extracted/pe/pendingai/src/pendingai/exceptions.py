#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from typing import Any

# Validation errors are a separate subset of TypeError to handle the
# custom type validation defined for complex object data types and allow
# runtime type confidence.


class ValidationError(TypeError): ...


class TypeValidationError(ValidationError):
    def __init__(self, instance: Any, expected: type[Any] | None):
        self.typ_inp: str = type(instance).__name__
        self.typ_out: str = expected.__name__ if isinstance(expected, type) else "None"

    def __str__(self) -> str:
        return "Instance has invalid type, provided type '%s' but expected '%s'." % (
            self.typ_inp,
            self.typ_out,
        )


class PendingAiError(Exception): ...


# -----


class HttpError(PendingAiError): ...


class RequestError(HttpError):
    def __str__(self) -> str:
        return "A request to the Pending AI server failed. Please try again shortly or contact support via email at 'support@pending.ai'."


class RequestTimeoutError(HttpError):
    def __str__(self) -> str:
        return "A request to the Pending AI server timed out. Please try again shortly."


# -----


class AuthenticationError(PendingAiError): ...


class ClientError(PendingAiError):
    def __init__(self, service: str | None = None, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.service: str | None = service

    def __str__(self) -> str:
        if self.service:
            return (
                "An error occurred while handling your request to "
                f"the Pending AI '{self.service.title()}' service."
            )
        return "An error occurred while handling your request to the Pending AI service."


class ClientTimeout(ClientError): ...


class AuthError(PendingAiError): ...


class UnexpectedResponseError(PendingAiError):
    def __init__(self, method: str, name: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.method: str = method
        self.name: str = name

    def __str__(self) -> str:
        return (
            f"An unexpected error occurred from a {self.method.upper()} "
            f"'{self.name}' request. Please try again and if the "
            "issue persists contact Pending AI support via email "
            "at 'support@pending.ai'."
        )


class NotFoundError(ClientError):
    def __init__(
        self,
        resource_id: str,
        resource_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.resource_id: str = resource_id
        self.resource_name: str = resource_name

    def __str__(self) -> str:
        return (
            f"The requested '{self.resource_name.title()}' "
            "resource cannot be retrieved as it does not exist: "
            f"'{self.resource_id}'."
        )


class PaymentGatewayError(ClientError):
    def __str__(self) -> str:
        return (
            "A billing service error was encountered while handling "
            "your request. No changes were made during the process, "
            "please try again. If the error persists, contact Pending "
            "AI support via email at 'support@pending.ai'."
        )


class ServiceUnavailableError(ClientError):
    def __str__(self) -> str:
        return (
            "The requested service is currently unavailable, please "
            "try again shortly. If the error persists, contact Pending "
            "AI support via email at 'support@pending.ai'."
        )


class ContentTooLargeError(ClientError):
    def __init__(self, msg: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.msg: str = msg

    def __str__(self) -> str:
        return self.msg


class RequestValidationError(ClientError):
    def __init__(self, errors: list[dict], *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.errors: list[dict] = errors

    def __str__(self) -> str:
        return f"Invalid parameters provided for service request: {self.errors}."


class UnauthorizedError(ClientError):
    """
    HTTP response has status `401 Unauthorized`.
    """

    def __str__(self) -> str:
        return (
            "Unauthorized access to Pending AI services. Ensure an "
            "authenticated api key is provided to the Pending AI "
            "client. For further help, contact support via email at "
            "'support@pending.ai'."
        )


class ForbiddenError(ClientError):
    """
    HTTP response has status `403 Forbidden`.
    """

    def __str__(self) -> str:
        return (
            "Forbidden access to Pending AI services. The provided "
            "api key does not have sufficient permissions to access "
            "the requested services. For further help, contact support "
            "via email at 'support@pending.ai'."
        )


class UnsubscribedError(ClientError):
    """
    HTTP response has status `403 Forbidden` and `not_subscribed` in the
    response content.
    """

    def __str__(self) -> str:
        return (
            "Forbidden access to the requested Pending AI service due "
            "to no active subscription. For further help, reach out "
            "to Pending AI support via email at 'support@pending.ai' "
            "and setup a new subscription."
        )


class HtmlGenerationError(PendingAiError):
    """This error is raised if the HTML cannot be generated."""

    def __str__(self) -> str:
        original_message: str = super().__str__()
        return f"Failed to generate HTML report: {original_message}"
