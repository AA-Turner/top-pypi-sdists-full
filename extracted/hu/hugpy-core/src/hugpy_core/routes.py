"""hugpy_core routes module: the blueprints, and the ONE merged route tree.

Each subpackage exposes one convention blueprint (``<sub>.routes.<sub>_bp``,
built with ``get_bp`` + ``register_categories``) and the category tree it was
built from (``<sub>.routes.ALL_CATEGORIES``). This module exposes the
blueprints at the top level — ``abstract_flask.get_Flask_app(routes=<this
module>, dual_prefix="/api", arms_group=None)`` discovers every ``*_bp``
here and mounts each bare and under ``/api``. Optional addon blueprints are
imported explicitly below. This module merges every section's tree into
``ALL_CATEGORIES``: the whole core surface as one explicit dict, which
``route_catalog`` describes as JSON for any arm or console that wants the
contract without walking Flask's url_map (served at ``/routes``).
"""
from __future__ import annotations

from abstract_flask import describe_categories, get_bp, merge_categories, register_categories, spec

from hugpy_core.web import routes as web
from hugpy_core.brain import routes as brain
from hugpy_core.config import routes as config
from hugpy_core.relay import routes as relay
from hugpy_core.discord import routes as discord
from hugpy_core.grading import routes as grading
from hugpy_core.models import routes as models
from hugpy_core.help import routes as help
from hugpy_core.registry import routes as registry
from hugpy_core.testfire import routes as testfire
from hugpy_core.calllog import routes as calllog
from hugpy_core.web import api_access, agent_proxy, agent_tools, agent_sessions, recovered_surfaces
from hugpy_core.web.inference import inference_bp
# The packaged console still uses worker/job IDs in the URL. Retain its
# method-specific routes and response/status contract alongside the convention.
from hugpy_core.testfire import testfire as testfire_legacy

web_bp = web.web_bp
brain_bp = brain.brain_bp
config_bp = config.config_bp
relay_bp = relay.relay_bp
discord_bp = discord.discord_bp
grading_bp = grading.grading_bp
models_bp = models.models_bp
help_bp = help.help_bp
registry_bp = registry.registry_bp
testfire_bp = testfire.testfire_bp
test_fire_bp = testfire_legacy.test_fire_bp
calllog_bp = calllog.calllog_bp
api_access_bp = api_access.api_access_bp
agent_proxy_bp = agent_proxy.agent_proxy_bp
recovered_surfaces_bp = recovered_surfaces.recovered_surfaces_bp
agent_tools_bp = agent_tools.agent_tools_bp
# Harness sessions registered by a box's hugpy-agent, each proxied as
# /api/sessions/<sid>/* — the session's one route from the fleet.
agent_sessions_bp = agent_sessions.agent_sessions_bp

# Optional external surfaces — exposed for discovery only when installed.
try:
    from hugpy_storage.api import storage_bp  # noqa: F401
except Exception:  # noqa: BLE001
    pass
try:
    from hugpy_storage.transfer_api import transfer_bp, set_authorizer as _set_transfer_authorizer  # noqa: F401
    from hugpy_core.web.transfer_relay import core_files_authorized as _core_files_authorized
    _set_transfer_authorizer(_core_files_authorized)
except Exception:  # noqa: BLE001
    pass
# Core relays model bytes between wrappers (web/transfer_relay.py)
from hugpy_core.web.transfer_relay import transfer_relay_bp  # noqa: F401,E402
# The Video arm, merged in-process (CORE-MERGE-PLAN.md §1/§7B): its blueprint
# is mounted and its category tree enters SECTIONS below. Mount the blueprint
# EXPLICITLY here — get_Flask_app discovers this *_bp and dual_prefix
# serves it bare and under /api. Core must NOT also enable arms_group="hugpy.arms"
# (web/app.py keeps it None): installed addons also publish hugpy.arms, and
# auto-discovery would double-register their blueprints (a startup failure).
# Guarded: a box without hugpy_video
# installed simply omits the surface.
video_routes = None
try:
    from hugpy_video import routes as video_routes
    video_bp = video_routes.video_bp  # noqa: F401
except Exception:  # noqa: BLE001
    import logging
    logging.getLogger(__name__).warning("Video addon routes unavailable", exc_info=True)

# Media shares this Flask process when installed, including its legacy session
# aliases. Its UI/startup hooks are loaded separately by web.app.
media_routes = None
try:
    from hugpy_media import routes as media_routes
    media_bp = media_routes.media_bp
except Exception:  # noqa: BLE001 — optional addons do not prevent Core startup
    import logging
    logging.getLogger(__name__).warning("Media addon routes unavailable", exc_info=True)

# ── the one tree ────────────────────────────────────────────────────────────
# Every section that is a category tree, by name. Order is only the catalog's
# section order; the merge refuses two sections claiming the same path.
SECTIONS = {
    "web": web, "brain": brain, "config": config, "relay": relay, "discord": discord,
    "grading": grading, "models": models, "help": help, "registry": registry,
    "testfire": testfire, "calllog": calllog,
    "agent_proxy": agent_proxy, "agent_tools": agent_tools, "agent_sessions": agent_sessions,
    "recovered_surfaces": recovered_surfaces,
}
if getattr(testfire_legacy, "ALL_CATEGORIES", None):
    SECTIONS["testfire_legacy"] = testfire_legacy
if media_routes is not None:
    SECTIONS["media"] = media_routes
if video_routes is not None:
    SECTIONS["video"] = video_routes

ALL_CATEGORIES = merge_categories(*(m.ALL_CATEGORIES for m in SECTIONS.values()), name="hugpy_core")


def route_catalog(section=None, path=None):
    """The core's route contract as data: one row per leaf of the merged tree
    (``path``, ``methods``, ``kind``, ``inputs``, ``response``, ``view``, ``doc``,
    ``params``). ``section=`` limits it to one section's tree; ``path=`` to rows
    whose path starts with the given prefix. Bare-served at /routes."""
    if section:
        mod = SECTIONS.get(str(section))
        if mod is None:
            return {"error": f"unknown section {section!r}", "sections": sorted(SECTIONS)}, 404
        rows = describe_categories(mod.ALL_CATEGORIES)
    else:
        rows = describe_categories(ALL_CATEGORIES)
    if path:
        rows = [r for r in rows if r["path"].startswith(str(path))]
    return {"sections": sorted(SECTIONS), "count": len(rows), "routes": rows}


def route_sections():
    """Each section with the paths it owns."""
    return {name: [r["path"] for r in describe_categories(mod.ALL_CATEGORIES)]
            for name, mod in SECTIONS.items()}


catalog_bp, _catalog_logger = get_bp("catalog_bp", __name__)
CATALOG_CATEGORIES = {
    "routes": {
        "": spec(route_catalog, "GET", response="native"),       # /routes?section=&path=
        "sections": spec(route_sections, "GET", response="native"),
    },
}
register_categories(catalog_bp, CATALOG_CATEGORIES)
