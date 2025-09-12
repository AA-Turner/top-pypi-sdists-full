import uvicorn
from fastapi import FastAPI, Request
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from project.api.api_error_codes import APIErrorCodes
from project.api.schema.out.common.error import ErrorCommonSO


class LimitContentLengthMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            max_body_size: int = 10 * 1024 * 1024  # 10 mb
    ):
        super().__init__(app)
        self.max_body_size = max_body_size

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length is None:
            return await call_next(request)
        if isinstance(content_length, str) and not content_length.isdigit():
            return await call_next(request)
        content_length = int(content_length)
        if content_length > self.max_body_size:
            return JSONResponse(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                content=ErrorCommonSO(
                    has_error=True,
                    error_code=APIErrorCodes.Common.content_length_is_too_big
                ).model_dump_json()
            )

        return await call_next(request)


def __example():
    app = FastAPI()
    app.add_middleware(LimitContentLengthMiddleware)  # 5 MB

    @app.post("/upload")
    async def upload_file(request: Request):
        data = await request.body()
        return {"size": len(data)}

    uvicorn.run(app)


if __name__ == '__main__':
    __example()
