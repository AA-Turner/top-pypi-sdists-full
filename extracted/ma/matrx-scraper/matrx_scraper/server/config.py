"""
Server configuration — loaded from environment variables or .env file.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class ServerConfig:
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    base_dir: str = "/tmp/matrx-scraper"

    # NOTE: there is intentionally NO database_url / DATABASE_URL here. The
    # scraper connects to the ONE database (Matrx Main) via SUPABASE_MATRIX_*,
    # resolved in matrx_scraper.db.register_platform_db. A service-local
    # connection string is how `scraper.*` forked onto a second Postgres.
    supabase_url: str = ""
    supabase_jwt_secret: str = ""
    admin_api_token: str = ""
    cors_allowed_origins: str = ""
    cors_allowed_origin_regex: str = ""

    brave_api_key: str = ""

    # NOTE: browser pool SIZE is intentionally NOT here. A concurrency ceiling
    # is not configuration — it lives in code as DEFAULT_BROWSER_POOL_SIZE
    # (browser_pool.py). An env var for it silently drifts between hosts.
    #
    # NOTE: there are intentionally NO feature toggles here either. The page
    # cache, the domain-config store, and the browser pool used to be gated by
    # ENABLE_CACHE / ENABLE_DOMAIN_CONFIG / ENABLE_BROWSER_POOL (deleted
    # 2026-08-09). A feature switch in env fails SILENTLY: the host that never
    # got the var takes the old path with nothing broken and nothing logged.
    # All three were unset on every real deployment, so they only ever
    # defaulted to on — the capabilities are now unconditional, and the one
    # thing that genuinely varies by image shape (is Playwright installed?) is
    # answered by a real capability probe, PLAYWRIGHT_AVAILABLE in
    # browser_pool.py, which cannot drift from reality. Do not add another.

    log_level: str = "info"

    @classmethod
    def from_env(cls) -> ServerConfig:
        try:
            from dotenv import load_dotenv

            load_dotenv()
        except ImportError:
            pass

        return cls(
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            workers=int(os.getenv("WORKERS", "1")),
            base_dir=os.getenv("MATRX_SCRAPER_BASE_DIR", "/tmp/matrx-scraper"),
            supabase_url=(os.getenv("SUPABASE_MATRIX_URL", "") or os.getenv("SUPABASE_URL", "")),
            # Accept either the modern SUPABASE_JWT_SECRET name OR the legacy
            # SUPABASE_MATRIX_JWT_SECRET (which is what aidream's .env has).
            # Without this fallback, inter-service calls from aidream → scraper
            # fail 401 because the scraper-service can't validate the JWT
            # signature (no secret) even though aidream signed it correctly.
            supabase_jwt_secret=(
                os.getenv("SUPABASE_JWT_SECRET", "") or os.getenv("SUPABASE_MATRIX_JWT_SECRET", "")
            ),
            admin_api_token=os.getenv("ADMIN_API_TOKEN", ""),
            cors_allowed_origins=os.getenv("MATRX_SCRAPER_CORS_ALLOWED_ORIGINS", ""),
            cors_allowed_origin_regex=os.getenv("MATRX_SCRAPER_CORS_ALLOWED_ORIGIN_REGEX", ""),
            brave_api_key=os.getenv("BRAVE_SEARCH_API_KEY_PRO_AI", ""),
            log_level=os.getenv("LOG_LEVEL", "info"),
        )
