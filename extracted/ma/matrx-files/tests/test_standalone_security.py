from __future__ import annotations

import pytest
from fastapi import Depends, FastAPI
from typing import Any, cast

from matrx_files._config import IndependenceConfigError
from matrx_files.api import build_asset_router, build_file_router, build_share_router
from matrx_files.standalone.security import assert_route_auth_coverage


def _auth_dependency() -> str:
    return "user"


def _audit(app: FastAPI) -> None:
    assert_route_auth_coverage(
        app,
        auth_dependency=_auth_dependency,
        public_paths=frozenset({"/health"}),
        public_prefixes=("/share/",),
    )


def test_auth_coverage_accepts_protected_and_allowlisted_routes() -> None:
    app = FastAPI()

    @app.get("/health")
    async def health() -> dict[str, bool]:
        return {"ok": True}

    @app.get("/share/{token}")
    async def share(token: str) -> dict[str, str]:
        return {"token": token}

    @app.get("/files/{file_id}")
    async def file(file_id: str, _user: str = Depends(_auth_dependency)) -> dict[str, str]:
        return {"id": file_id}

    _audit(app)


def test_auth_coverage_refuses_a_new_fail_open_route() -> None:
    app = FastAPI()

    @app.get("/files/leaked")
    async def leaked() -> dict[str, bool]:
        return {"leaked": True}

    with pytest.raises(IndependenceConfigError, match="GET /files/leaked"):
        _audit(app)


def test_every_package_data_route_is_protected_or_explicitly_public() -> None:
    app = FastAPI()
    service = cast(Any, object())
    app.include_router(build_file_router(service, user_id_dep=_auth_dependency))
    app.include_router(build_asset_router(service, user_id_dep=_auth_dependency))
    app.include_router(build_share_router(service))

    assert_route_auth_coverage(
        app,
        auth_dependency=_auth_dependency,
        public_paths=frozenset({"/assets/presets"}),
        public_prefixes=("/share/",),
    )
