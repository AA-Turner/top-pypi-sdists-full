"""Required standalone login, source and cookie-mint authority configuration."""
from __future__ import annotations

from dataclasses import dataclass

from matrx_connect.middleware.remote_file_session import RemoteFileSessionResolver
from matrx_connect.middleware.remote_session import RemoteSessionResolver
from matrx_files._config import IndependenceConfigError
from matrx_files.standalone.remote_mint import RemoteFileSessionMint


@dataclass(frozen=True)
class FileSessionPolicy:
    login: RemoteSessionResolver
    file: RemoteFileSessionResolver
    mint: RemoteFileSessionMint


def build_session_policy(cfg: dict[str, object]) -> FileSessionPolicy:
    required = {
        "db_host": "SUPABASE_MATRIX_HOST",
        "s3_bucket": "AWS_S3_DEFAULT_BUCKET",
        "supabase_url": "SUPABASE_URL",
        "session_authority_url": "MATRX_SESSION_AUTHORITY_URL",
        "file_session_authority_url": "MATRX_FILE_SESSION_AUTHORITY_URL",
        "file_session_mint_url": "MATRX_FILE_SESSION_MINT_URL",
        "guest_fingerprint_secret": "GUEST_FINGERPRINT_SECRET",
    }
    missing = [env for key, env in required.items() if not isinstance(cfg.get(key), str) or not str(cfg[key]).strip()]
    if missing:
        raise IndependenceConfigError("Standalone Files requires current-source authority; missing: " + ", ".join(missing))
    # Constructors validate explicit HTTPS URLs before any database/bootstrap work.
    secret = str(cfg["guest_fingerprint_secret"]).encode("utf-8")
    try:
        login = RemoteSessionResolver(str(cfg["session_authority_url"]))
        file = RemoteFileSessionResolver(str(cfg["file_session_authority_url"]), secret)
        mint = RemoteFileSessionMint(str(cfg["file_session_mint_url"]), str(cfg["file_session_authority_url"]), secret)
    except ValueError as exc:
        raise IndependenceConfigError("Standalone Files authority configuration is invalid; use explicit trusted HTTPS URLs") from exc
    return FileSessionPolicy(login, file, mint)


def session_policy_armed(app: object) -> bool:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from matrx_connect.middleware.auth import AuthMiddleware
    from matrx_files.standalone.remote_mint import RemoteFileSessionMintMiddleware

    if not isinstance(app, FastAPI):
        return False
    policy = getattr(app.state, "file_session_policy", None)
    if not isinstance(policy, FileSessionPolicy):
        return False
    stack = app.user_middleware
    mint = next((i for i, m in enumerate(stack) if m.cls is RemoteFileSessionMintMiddleware and m.kwargs.get("mint") is policy.mint), None)
    auth = next((i for i, m in enumerate(stack) if m.cls is AuthMiddleware
                 and m.kwargs.get("resolve_current_session") is policy.login
                 and m.kwargs.get("resolve_file_session") is policy.file
                 and m.kwargs.get("require_file_session_source") is True), None)
    cors = next((i for i, m in enumerate(stack) if m.cls is CORSMiddleware), None)
    return mint is not None and auth is not None and cors is not None and cors < mint < auth
