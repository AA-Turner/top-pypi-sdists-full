"""Run target, auth, and smart detection.

Three orthogonal flags:
- run_target: "local" (default) or "cloud". Only "cloud" connects to LT CDP.
- lt_auth:    LT creds available. Enables ATMS/automind/downloads/API proxy
              regardless of run target.
- smart:      AI/heal features. Requires lt_auth; validated at testmu.run().

Call-time getters (`get_api_proxy_url`, `get_har_url`) resolve URLs from env
vars at each call so consumers (e.g. the host runtime) can publish env after import.
PORT is the activation key — when set, env wins unconditionally; otherwise
fall back to the cloud-only default when TESTMU_RUN_TARGET=cloud, else None.
"""
import os
from typing import Optional

run_target = os.getenv("TESTMU_RUN_TARGET", "local").lower()
lt_auth = bool(os.getenv("LT_USERNAME")) and bool(os.getenv("LT_ACCESS_KEY"))
smart = os.getenv("TESTMU_SMART", "0") == "1"


def get_ai_api_host() -> str:
    """The v16-server host, read per call.

    Read here rather than at import because auteur publishes TESTMU_AI_API_HOST
    per session, long after the first `import testmu` — a constant frozen at
    import pinned every AI call to the prod default and answered 401 on stage
    (TE-28542).
    """
    return os.getenv("TESTMU_AI_API_HOST", "https://kaneai-api.lambdatest.com/v16-server")


def get_api_proxy_url() -> Optional[str]:
    port = os.getenv("TESTMU_API_PROXY_PORT")
    if port:
        host = os.getenv("TESTMU_API_PROXY_HOST", "127.0.0.1")
        return f"http://{host}:{port}"
    if os.getenv("TESTMU_RUN_TARGET") == "cloud":
        return "http://127.0.0.1:22000"
    return None


def get_har_url() -> Optional[str]:
    port = os.getenv("TESTMU_HAR_PORT")
    if port:
        host = os.getenv("TESTMU_HAR_HOST", "127.0.0.1")
        return f"http://{host}:{port}"
    if os.getenv("TESTMU_RUN_TARGET") == "cloud":
        return "http://127.0.0.1:8181"
    return None
