"""Installed image/configuration checks before replacing a Files container."""
from __future__ import annotations

import asyncio

from fastapi import FastAPI
from matrx_connect.middleware.remote_authority import fetch_authority_response
from matrx_files.standalone.session_policy import FileSessionPolicy, session_policy_armed


async def verify_candidate(app: FastAPI) -> None:
    if not session_policy_armed(app):
        raise RuntimeError("Files source-aware mint and admission policy is not armed")
    from matrx_files.db.readiness import probe_database_readiness

    policy = app.state.file_session_policy
    async with asyncio.timeout(15.0):
        probe = await probe_database_readiness(max_age_seconds=0)
        if not probe.ready:
            raise RuntimeError("Files candidate database is not ready")
        await verify_authority_contracts(policy)


async def verify_authority_contracts(policy: FileSessionPolicy) -> None:
    async with asyncio.timeout(9.0):
        for method, url, credential in [
            ("GET", policy.login.authority_url, "Bearer preflight-invalid-login"),
            ("GET", policy.file.authority_url, "FileSession preflight-invalid-source"),
            ("POST", policy.mint.mint_url, "Bearer preflight-invalid-login"),
        ]:
            response = await fetch_authority_response(method, url, {"Authorization": credential}, 3.0)
            if response.status_code != 401 or response.headers.get_list("cache-control") != ["no-store"]:
                raise RuntimeError("Files central authority refusal contract is unavailable")


async def main() -> None:
    from matrx_files.standalone.app import create_app

    await verify_candidate(create_app())
    print("FILES_SOURCE_POLICY_V2_PREFLIGHT_OK")


if __name__ == "__main__":
    asyncio.run(main())
