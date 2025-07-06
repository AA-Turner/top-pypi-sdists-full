from typing import Union

from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def http422_error_handler(
        _: Request,
        exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    return JSONResponse(
        {"errors": exc.errors()},
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )


validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},
    },
}


async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    # print(exc)
    content = {
        "error":
            {
                "message": f"{exc}",
                "type": "RequestValidationError",
            }
    }
    return JSONResponse(
        content=content,
        status_code=status.HTTP_400_BAD_REQUEST
    )
