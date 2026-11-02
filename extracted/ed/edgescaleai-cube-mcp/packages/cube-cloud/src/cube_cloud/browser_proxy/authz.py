"""Scoped access authorization for the browser app proxy (spec §4.3, Phase 2b).

A session's profile decides which ``<app>-<env>`` it may reach: the app is reachable
when the profile holds one of the app's app companies. Both halves come from
``auth/app_companies.py`` -- the profile's set, and the one predicate that reads an
app's ``company`` label -- which ``expose``/``list_exposed`` and the console use too, so
no surface can show an app another refuses to open. The unscoped ``cube-mcp-bot`` role
(admin/esaiadmin) reaches everything, matching `expose`/`unexpose`'s own bypass.

Fail-closed: a profile whose app companies cannot be resolved, or an app whose company
label can't be read (not found, tbot not ready, tsh error), is denied -- never silently
allowed.
"""

from __future__ import annotations

import logging

from cube_cloud.auth.app_companies import app_companies
from cube_cloud.teleport.tbot_manager import tbot

logger = logging.getLogger(__name__)


async def authorize_app_access(profile: str, app_name: str) -> bool:
    """Return whether ``profile`` may reach the resolved Teleport app."""
    companies = app_companies(profile)
    if companies is None:
        logger.warning(
            "app_proxy authz: profile=%s has no resolvable app companies, denying (app=%s)",
            profile, app_name,
        )
        return False
    if companies.unscoped:
        return True

    app_company = await tbot.get_app_company(app_name)
    if app_company is None:
        logger.warning(
            "app_proxy authz: could not resolve company label for app=%s, denying (profile=%s)",
            app_name, profile,
        )
        return False

    return companies.can_see(app_company)
