import asyncio
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from functools import wraps
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from maleo_foundation.models.responses import BaseResponses
from maleo_foundation.models.transfers.results.service.general \
    import BaseServiceGeneralResultsTransfers
from maleo_foundation.models.transfers.results.service.repository \
    import BaseServiceRepositoryResultsTransfers
from maleo_foundation.utils.logging import BaseLogger

class BaseExceptions:
    @staticmethod
    def authentication_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            content=BaseResponses.Unauthorized(other=str(exc)).model_dump(mode="json"),
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    @staticmethod
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        serialized_error = jsonable_encoder(exc.errors())
        return JSONResponse(
            content=BaseResponses.ValidationError(other=serialized_error).model_dump(mode="json"),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    @staticmethod
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        if exc.status_code in BaseResponses.other_responses:
            return JSONResponse(
                content=BaseResponses.other_responses[exc.status_code]["model"]().model_dump(mode="json"),
                status_code=exc.status_code
            )

        return JSONResponse(
            content=BaseResponses.ServerError().model_dump(mode="json"),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @staticmethod
    def repository_exception_handler(
        operation: str,
        logger: Optional[BaseLogger] = None,
        fail_result_class: type[BaseServiceRepositoryResultsTransfers.Fail] = BaseServiceRepositoryResultsTransfers.Fail
    ):
        """Decorator to handle repository-related exceptions consistently for sync and async functions."""
        def decorator(func):
            def _handler(e: Exception, category: str, description: str):
                if logger:
                    logger.error(
                        f"{category} occurred while {operation}: '{str(e)}'",
                        exc_info=True
                    )
                return fail_result_class(
                    message=f"Failed {operation}",
                    description=description,
                    other=category
                )
            if asyncio.iscoroutinefunction(func):
                @wraps(func)
                async def async_wrapper(*args, **kwargs):
                    try:
                        return await func(*args, **kwargs)
                    except ValidationError as e:
                        return _handler(
                            e,
                            category="Validation error",
                            description=f"A validation error occurred while {operation}. Please try again later or contact administrator."
                        )
                    except SQLAlchemyError as e:
                        return _handler(
                            e,
                            category="Database operation failed",
                            description=f"A database error occurred while {operation}. Please try again later or contact administrator."
                        )
                    except Exception as e:
                        return _handler(
                            e,
                            category="Internal processing error",
                            description=f"An unexpected error occurred while {operation}. Please try again later or contact administrator."
                        )
                return async_wrapper
            else:
                @wraps(func)
                def sync_wrapper(*args, **kwargs):
                    try:
                        return func(*args, **kwargs)
                    except ValidationError as e:
                        return _handler(
                            e,
                            category="Validation error",
                            description=f"A validation error occurred while {operation}. Please try again later or contact administrator."
                        )
                    except SQLAlchemyError as e:
                        return _handler(
                            e,
                            category="Database operation failed",
                            description=f"A database error occurred while {operation}. Please try again later or contact administrator."
                        )
                    except Exception as e:
                        return _handler(
                            e,
                            category="Internal processing error",
                            description=f"An unexpected error occurred while {operation}. Please try again later or contact administrator."
                        )
                return sync_wrapper
        return decorator

    @staticmethod
    def service_exception_handler(
        operation: str,
        logger: Optional[BaseLogger] = None,
        fail_result_class: type[BaseServiceGeneralResultsTransfers.Fail] = BaseServiceGeneralResultsTransfers.Fail
    ):
        """Decorator to handle service-related exceptions consistently."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error("Unexpected error occurred while %s: '%s'", operation, str(e), exc_info=True)
                    return fail_result_class(
                        message=f"Failed {operation}",
                        description=f"An unexpected error occurred while {operation}. Please try again later or contact administrator.",
                        other="Internal processing error"
                    )
            return wrapper
        return decorator