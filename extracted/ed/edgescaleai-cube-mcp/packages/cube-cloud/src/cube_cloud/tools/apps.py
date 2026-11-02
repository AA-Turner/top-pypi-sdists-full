"""Teleport app listing via tbot (server-side).

App listing is done server-side using tbot credentials — no local `tsh`.

The URL published per app is the **browser app proxy's**
(`https://<app-name>.<apex>`, built by `browser_proxy/resolver.py`), never the
Teleport `public_addr` the listing carries: reaching that redirects to Teleport
SSO, and those accounts are being retired. See `tools/expose.py`'s module
docstring for the full rule.
"""

from __future__ import annotations

import asyncio
import json
import logging

from cube_cloud.browser_proxy.resolver import browser_app_url_or_reason, is_http_app
from cube_cloud.teleport.tbot_manager import tbot

logger = logging.getLogger(__name__)


def _label_tokens(app: dict) -> list[str]:
    """The `company` label's tokens as written (trimmed), for display and filtering only."""
    label = _labels(app).get("company")
    return [t.strip() for t in label.split(",") if t.strip()] if isinstance(label, str) else []


def _labels(app: dict) -> dict:
    """The Teleport app's label map, defaulting to `{}` at every level.

    `tsh apps ls` omits `metadata.labels` entirely for an app with no labels, and
    a `.get("labels", {})` on a missing `metadata` raises — so both levels are
    defaulted here rather than at each of the three call sites.
    """
    return (app.get("metadata") or {}).get("labels") or {}


async def app_list(company: str | None = None, profile: str = "admin") -> str:
    """List available Teleport apps using tbot credentials.

    Uses `tctl` or Teleport API via tbot identity to list registered apps.
    Falls back to a curated list if tctl is not available.
    """
    if not tbot.is_ready:
        return "tbot credentials not ready. Server-side app listing is not available yet."

    # Try tsh apps ls with role-scoped tbot identity
    try:
        cmd = tbot.tsh_base_args(profile=profile) + ["apps", "ls", "--format=json"]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=tbot.tsh_env(),
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)

        if proc.returncode != 0:
            logger.warning("tsh apps ls failed: %s", stderr.decode())
            return f"Failed to list apps: {stderr.decode()}"

        apps = json.loads(stdout.decode())
    except FileNotFoundError:
        return "tsh not found in container. App listing requires tsh to be installed."
    except asyncio.TimeoutError:
        return "App listing timed out."
    except json.JSONDecodeError as e:
        return f"Failed to parse app list: {e}"

    # Filter by company: an app visible to several companies matches each of them. This is
    # a DISPLAY filter over a listing Teleport already scoped, not an authorization check,
    # so it matches the label's raw tokens, case-insensitively: `label_companies` would
    # drop a token that is not an app company name (a live `Groundcover`), answering
    # "no apps" for exactly the role an operator was auditing.
    if company:
        apps = [
            app for app in apps
            if company.strip().lower() in {t.lower() for t in _label_tokens(app)}
        ]

    if not apps:
        suffix = f" for company '{company}'" if company else ""
        return f"No apps found{suffix}."

    # Group by AUDIENCE: the header is every company the app is visible to.
    by_company: dict[str, list] = {}
    for app in apps:
        comp = ", ".join(sorted(_label_tokens(app))) or "unknown"
        by_company.setdefault(comp, []).append(app)

    lines = ["Available Apps:", "=" * 60]
    for comp in sorted(by_company):
        lines.append(f"\n[{comp}]")
        for app in sorted(by_company[comp], key=lambda x: x["metadata"]["name"]):
            name = app["metadata"]["name"]
            spec = app.get("spec", {})
            uri = spec.get("uri", "")
            app_type = "HTTP" if is_http_app(uri) else "TCP"
            # Unconditional, unlike the old `if public_addr:` gate: access dials the
            # app by NAME (`tunnel/relay.py` SNI, `browser_proxy/resolver.py` host
            # label), so an app with no Teleport public_addr registered still has a
            # working browser URL and used to be shown with no address at all.
            url, no_url_reason = browser_app_url_or_reason(name, uri)
            lines.append(f"  {name}")
            lines.append(f"    Type: {app_type}")
            lines.append(f"    URL:  {url or f'none -- {no_url_reason}'}")
            # URI + the remaining labels are what make this usable for migration
            # triage. A legacy app's Teleport name does NOT contain its cube
            # (`minio-s3-carrollton-1` lives on `cube-9likqvpd`), so the in-cluster
            # URI's namespace/service is often the only clue to which cube an app
            # is on, and an operator-set label like `app-type` is config that a
            # migration must carry across rather than silently drop.
            if uri:
                lines.append(f"    URI:  {uri}")
            # `company` is the grouping header above, so repeating it per app is
            # noise. Everything else is shown: this listing exists precisely to
            # surface labels we do not know the names of in advance.
            extra = {k: v for k, v in sorted(_labels(app).items()) if k not in ("company", "cube")}
            if extra:
                rendered = ", ".join(f"{k}={v}" for k, v in extra.items())
                lines.append(f"    Labels: {rendered}")

    lines.append("")
    lines.append("Access: open an app's URL in a browser and sign in with the same "
                 "login as cube-mcp (no Teleport account).")
    return "\n".join(lines)
