"""The configure() seam — INDEPENDENCE.md law #2 made executable.

Required config is validated ALL-ERRORS-AT-ONCE and a violation screams a red
banner naming every missing value and how to supply it. There is no silent
default and no legacy fallback: a package that boots is a package that is
correctly configured.

Extend ``PackageConfig`` with your package's opinionated inputs (bucket names,
schema names, table maps, provider keys...). Mark host-injectable seams
Optional ONLY when the package owns a real standalone fallback for them.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

_BANNER = "\033[91m"  # bright red
_RESET = "\033[0m"


class IndependenceConfigError(RuntimeError):
    """Raised when configure() is missing required values, or when code touches
    config before configure() ran. Never catch-and-continue this error."""


class PackageConfig(BaseModel):
    """Everything this package is opinionated about, handed in explicitly."""

    model_config = ConfigDict(frozen=True)

    # --- required: no default, no fallback -------------------------------
    # example_database_url: str

    # --- host-injectable seams (package ships its own duplicate fallback) --
    # Public base URL the durable file routes are served from, e.g.
    # "https://server.app.matrxserver.com" (aidream host) or
    # "https://files.matrxserver.com" (standalone service). Consumed by
    # cloud_sync/render_urls.py to build the never-expiring
    # /files/{id}/download URLs that replaced signed URLs on every client
    # shape. Standalone fallback: the PUBLIC_URL setting/env.
    files_public_base_url: str | None = None


_config: PackageConfig | None = None


def configure(**kwargs: object) -> PackageConfig:
    """Validate and install the package config. Call once at startup.

    Raises IndependenceConfigError listing EVERY problem at once — startup
    wiring gets fixed in one pass, never by whack-a-mole.
    """
    global _config
    try:
        cfg = PackageConfig(**kwargs)  # type: ignore[arg-type]
    except Exception as exc:  # pydantic ValidationError → one screaming banner
        problems = _explain(exc)
        banner = (
            f"\n{_BANNER}{'=' * 78}\n"
            f"🚨 Matrx Files CONFIGURATION IS INVALID — the process will not start.\n"
            f"{'=' * 78}{_RESET}\n"
            + "\n".join(f"  ✗ {p}" for p in problems)
            + "\n\nFix: pass every required value to matrx_files.configure(...).\n"
            "Contract: INDEPENDENCE.md at the package root.\n"
        )
        print(banner, flush=True)
        raise IndependenceConfigError(
            f"matrx-files configure() rejected: {len(problems)} problem(s) — see banner above"
        ) from exc
    _config = cfg
    return cfg


def _explain(exc: Exception) -> list[str]:
    errors = getattr(exc, "errors", None)
    if callable(errors):
        return [
            f"{'.'.join(str(p) for p in e.get('loc', ())) or '<root>'}: {e.get('msg', 'invalid')}"
            for e in errors()
        ]
    return [str(exc)]


def is_configured() -> bool:
    return _config is not None


def get_config() -> PackageConfig:
    if _config is None:
        raise IndependenceConfigError(
            "matrx-files is not configured. The host (or standalone/app.py) must call "
            "matrx_files.configure(...) before any package functionality is used. "
            "This is a wiring bug at the call site — never work around it here."
        )
    return _config
