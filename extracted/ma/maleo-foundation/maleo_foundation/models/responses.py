from __future__ import annotations
from fastapi import status
from pydantic import Field, model_validator
from typing import Dict, Type, Union
from maleo_foundation.models.schemas.result import BaseResultSchemas
from maleo_foundation.types import BaseTypes

class BaseResponses:
    class Fail(BaseResultSchemas.Fail):
        other: BaseTypes.OptionalAny = Field("Please try again later or contact administrator.", description="Response's other information")

    class BadRequest(Fail):
        code: str = "MAL-BDR-001"
        message: str = "Bad Request"
        description: str = "Bad/Unexpected parameters given in the request"

    class InvalidExpand(BadRequest):
        code: str = "MAL-INE-001"
        message: str = "Invalid expand"
        description: str = "Invalid expand field(s) configuration are given. Check 'other' for more information."

    class InvalidParameter(BadRequest):
        code: str = "MAL-IPR-001"
        message: str = "Invalid parameters"
        description: str = "Invalid parameters and/or parameters combinations is given. Check 'other' for more information."

    class InvalidSystemRole(BadRequest):
        code: str = "MAL-ISR-001"
        message: str = "Invalid system role"
        description: str = "Invalid system role is detected in authorization token. Check 'other' for more information."

    class Unauthorized(Fail):
        code: str = "MAL-ATH-001"
        message: str = "Unauthorized Request"
        description: str = "You are unauthorized to request this resource"

    class Forbidden(Fail):
        code: str = "MAL-ATH-002"
        message: str = "Forbidden Request"
        description: str = "You are forbidden from requesting this resource"

    class MethodNotAllowed(Fail):
        code: str = "MAL-MTA-002"
        message: str = "Method Not Allowed"
        description: str = "Method not allowed for requesting this resource"

    class ValidationError(Fail):
        code: str = "MAL-VLD-001"
        message: str = "Validation Error"
        description: str = "Request validation failed due to missing or invalid fields. Check other for more info."

    class RateLimitExceeded(Fail):
        code: str = "MAL-RTL-001"
        message: str = "Rate Limit Exceeded"
        description: str = "This resource is requested too many times. Please try again later."

    class ServerError(Fail):
        code: str = "MAL-EXC-001"
        message: str = "Unexpected Server Error"
        description: str = "An unexpected error occurred while processing your request."

    class NotImplemented(Fail):
        code: str = "MAL-NIM-001"
        message: str = "Not Implemented"
        description: str = "This request is not yet implemented by the system."

    class NotFound(BaseResultSchemas.NotFound): pass

    class NoData(BaseResultSchemas.NoData): pass

    class SingleData(BaseResultSchemas.SingleData): pass

    class UnpaginatedMultipleData(BaseResultSchemas.UnpaginatedMultipleData): pass

    class PaginatedMultipleData(BaseResultSchemas.PaginatedMultipleData):
        page: int = Field(1, ge=1, description="Page number, must be >= 1.", exclude=True)
        limit: int = Field(10, ge=1, le=100, description="Page size, must be 1 <= limit <= 100.", exclude=True)
        total_data: int = Field(..., ge=0, description="Total data count", exclude=True)

        @model_validator(mode="before")
        @classmethod
        def calculate_pagination(cls, values: dict) -> dict:
            """Calculates pagination metadata before validation."""
            total_data = values.get("total_data", 0)
            data = values.get("data", [])

            #* Get pagination values from inherited SimplePagination
            page = values.get("page", 1)
            limit = values.get("limit", 10)

            #* Calculate total pages
            total_pages = (total_data // limit) + (1 if total_data % limit > 0 else 0)

            #* Assign computed pagination object before validation
            values["pagination"] = BaseResultSchemas.ExtendedPagination(
                page=page,
                limit=limit,
                data_count=len(data),
                total_data=total_data,
                total_pages=total_pages
            )
            return values

    #* ----- ----- Responses Class ----- ----- *#
    other_responses:Dict[int, Dict[str, Union[str, Type[Fail]]]]={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request Response",
            "model": BadRequest
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized Response",
            "model": Unauthorized
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden Response",
            "model": Forbidden
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Response",
            "model": NotFound
        },
        status.HTTP_405_METHOD_NOT_ALLOWED: {
            "description": "Method Not Allowed Response",
            "model": MethodNotAllowed
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation Error Response",
            "model": ValidationError
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            "description": "Rate Limit Exceeded Response",
            "model": RateLimitExceeded
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error Response",
            "model": ServerError
        },
        status.HTTP_501_NOT_IMPLEMENTED: {
            "description": "Not Implemented Response",
            "model": ServerError
        }
    }