from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from project.api.middleware.limit_content_length import LimitContentLengthMiddleware


def add_api_middlewares(*, app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LimitContentLengthMiddleware, max_body_size=5 * 1024 * 1024)
