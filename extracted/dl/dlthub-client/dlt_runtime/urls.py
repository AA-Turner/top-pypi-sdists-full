"""Web UI URL templates and builders. Mirrors `web/src/misc/routes.tsx`."""

import re
from typing import Union
from urllib.parse import quote, urlparse
from uuid import UUID

from dlt._workspace._workspace_context import active


_LEGACY_API_BASE_URL_RE = re.compile(
    r"^(?P<scheme>https?)://dlthub\.(?P<tld>app|net|test|dev)/api/(?:api|auth)/?$"
)


def normalize_api_base_url(url: str) -> str:
    """Rewrite legacy split-host URLs to the path-routed gateway form."""
    match = _LEGACY_API_BASE_URL_RE.match(url.strip())
    if not match:
        return url
    return f"{match['scheme']}://api.dlthub.{match['tld']}"


def web_ui_base() -> str:
    """Web UI base URL: strips `api.` prefix; prod uses the `app.dlthub.com` split."""
    api_base_url = normalize_api_base_url(active().runtime_config.api_base_url or "")
    parsed = urlparse(api_base_url)
    bare = parsed.netloc.removeprefix("api.")
    # Prod splits the web UI off the platform base domain: `dlthub.com`
    # serves marketing, the app lives on `app.dlthub.com`.
    host = f"app.{bare}" if bare.startswith("dlthub.com") else bare
    return f"{parsed.scheme}://{host}"


def _seg(value: Union[str, UUID]) -> str:
    # safe="" percent-encodes every reserved char so callers never produce broken URLs.
    return quote(str(value), safe="")


def workspace_url(ws_id: Union[str, UUID]) -> str:
    return f"{web_ui_base()}/w/{_seg(ws_id)}"


def pipeline_url(ws_id: Union[str, UUID], pipeline_name: str) -> str:
    return f"{web_ui_base()}/w/{_seg(ws_id)}/pipelines/{_seg(pipeline_name)}"


def job_url(ws_id: Union[str, UUID], job_ref_or_id: Union[str, UUID]) -> str:
    return f"{web_ui_base()}/w/{_seg(ws_id)}/jobs/{_seg(job_ref_or_id)}"


def job_run_url(ws_id: Union[str, UUID], run_id: Union[str, UUID]) -> str:
    return f"{web_ui_base()}/w/{_seg(ws_id)}/runs/{_seg(run_id)}"


def with_swap_code(url: str, swap_code: str) -> str:
    """Append a single-use `?swap=` login code to a web-app URL."""
    sep = "&" if urlparse(url).query else "?"
    return f"{url}{sep}swap={_seg(swap_code)}"


__all__ = [
    "normalize_api_base_url",
    "web_ui_base",
    "workspace_url",
    "pipeline_url",
    "job_url",
    "job_run_url",
    "with_swap_code",
]
