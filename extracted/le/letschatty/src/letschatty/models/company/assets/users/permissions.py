"""Authorization model — the single source of truth for "who can do what".

Permissions are declared per **Module** (the ~14 things a user sees on the Home
screen), NOT per ``CompanyAssetType``: several asset types have no screen and one
module can span several asset types (e.g. ``AI_AGENTS``). Each role maps to a
default permission level per module in :data:`ROLE_DEFAULTS`; a user's effective
level is the highest across their roles, optionally replaced by an explicit
per-user override.

To change who-can-do-what, edit :data:`ROLE_DEFAULTS`. To add a module, add a
:class:`Module` value + one entry per role here (and one guard line on its router
in api-chatty). This module imports nothing from ``user.py`` (``ROLE_DEFAULTS`` is
keyed by the role *string* value) so it can be imported from the ``User`` model
without a circular import.
"""
from __future__ import annotations

from enum import StrEnum
from typing import Dict, List, Optional

from ..company_assets import CompanyAssetType
from .user_asset_permission import Permission


class Module(StrEnum):
    """User-facing product modules (the cards on the Home screen)."""

    INBOX = "inbox"                    # Bandeja / Vista WhatsApp — operate chats
    CRM = "crm"                        # Vista CRM / tablero de embudos
    TAGS = "tags"
    PRODUCTS = "products"
    FAST_ANSWERS = "fast_answers"
    TEMPLATES = "templates"            # send / author WhatsApp templates
    CAMPAIGNS = "campaigns"            # acciones masivas / campañas
    SOURCES = "sources"               # fuentes de origen
    SMART_MESSAGES = "smart_messages"  # topics
    WORKFLOWS = "workflows"
    FORM_FIELDS = "form_fields"        # campos de datos
    AI_AGENTS = "ai_agents"
    ANALYTICS = "analytics"
    INTEGRATIONS = "integrations"
    CONFIG = "config"                  # configuración de la empresa
    USERS = "users"                    # equipo y permisos
    # NOTE: Backoffice is mega_admin-only and cross-company, so it is not a
    # per-company module and intentionally absent from this enum.


# --- the permission ladder: NONE < VIEW < USE < ADMIN --------------------------

_PERMISSION_RANK: Dict[Permission, int] = {
    Permission.NONE: 0,
    Permission.VIEW: 1,
    Permission.USE: 2,
    Permission.ADMIN: 3,
}


def permission_rank(permission: Permission) -> int:
    """Numeric rank of a permission on the NONE<VIEW<USE<ADMIN ladder."""
    return _PERMISSION_RANK[permission]


def permission_satisfies(held: Permission, required: Permission) -> bool:
    """True if ``held`` grants at least ``required`` (higher rank includes lower)."""
    return _PERMISSION_RANK[held] >= _PERMISSION_RANK[required]


# --- module → underlying asset type(s) (for asset-level detail where needed) ----

MODULE_ASSET_TYPES: Dict[Module, List[CompanyAssetType]] = {
    Module.INBOX: [CompanyAssetType.CHATS],
    Module.CRM: [
        CompanyAssetType.FUNNELS,
        CompanyAssetType.FUNNEL_STAGES,
        CompanyAssetType.FUNNEL_MEMBERS,
    ],
    Module.TAGS: [CompanyAssetType.TAGS],
    Module.PRODUCTS: [CompanyAssetType.PRODUCTS, CompanyAssetType.SALES],
    Module.FAST_ANSWERS: [CompanyAssetType.FAST_ANSWERS],
    Module.TEMPLATES: [CompanyAssetType.TEMPLATES],
    Module.CAMPAIGNS: [CompanyAssetType.TEMPLATE_CAMPAIGNS],
    Module.SOURCES: [CompanyAssetType.SOURCES],
    Module.SMART_MESSAGES: [CompanyAssetType.TOPICS, CompanyAssetType.MEDIA],
    Module.WORKFLOWS: [CompanyAssetType.WORKFLOWS],
    Module.FORM_FIELDS: [CompanyAssetType.FORM_FIELDS],
    Module.AI_AGENTS: [
        CompanyAssetType.CHATTY_AI_AGENTS,
        CompanyAssetType.AI_AGENT_CONTEXT,
        CompanyAssetType.AI_AGENT_CHAT_EXAMPLE,
        CompanyAssetType.AI_AGENT_INSTRUCTION,
        CompanyAssetType.CS_SCENARIO,
    ],
    Module.ANALYTICS: [CompanyAssetType.ANALYTICS],
    Module.INTEGRATIONS: [],  # company-level OAuth, no dedicated asset type
    Module.CONFIG: [CompanyAssetType.COMPANY],
    Module.USERS: [
        CompanyAssetType.USERS,
        CompanyAssetType.BUSINESS_AREAS,
        CompanyAssetType.FUNNEL_MEMBERS,
    ],
}


# --- role → default permission per module (THE matrix) --------------------------
# Keyed by the UserRole *string* value (see module docstring). One level per
# (role, module): the max the role may reach on that module. Because VIEW<USE<ADMIN
# is a ladder, a single level covers view/use/manage (e.g. TAGS=USE lets an agent
# view the page and apply tags to a chat, but not create/edit tag definitions).

_N, _V, _U, _A = Permission.NONE, Permission.VIEW, Permission.USE, Permission.ADMIN


def _all_modules_at(level: Permission) -> Dict[Module, Permission]:
    return {module: level for module in Module}


_AGENT: Dict[Module, Permission] = {
    Module.INBOX: _U, Module.CRM: _U, Module.TAGS: _U, Module.PRODUCTS: _U,
    Module.FAST_ANSWERS: _U, Module.TEMPLATES: _U, Module.CAMPAIGNS: _N,
    Module.SOURCES: _N, Module.SMART_MESSAGES: _N, Module.WORKFLOWS: _V,
    Module.FORM_FIELDS: _V, Module.AI_AGENTS: _N, Module.ANALYTICS: _N,
    Module.INTEGRATIONS: _N, Module.CONFIG: _N, Module.USERS: _N,
}

_SUPER_AGENT: Dict[Module, Permission] = {
    **_AGENT,
    Module.SOURCES: _V, Module.SMART_MESSAGES: _V, Module.ANALYTICS: _V,
}

_MARKETER: Dict[Module, Permission] = {
    Module.INBOX: _U, Module.CRM: _V, Module.TAGS: _U, Module.PRODUCTS: _U,
    Module.FAST_ANSWERS: _U, Module.TEMPLATES: _A, Module.CAMPAIGNS: _A,
    Module.SOURCES: _A, Module.SMART_MESSAGES: _A, Module.WORKFLOWS: _V,
    Module.FORM_FIELDS: _V, Module.AI_AGENTS: _N, Module.ANALYTICS: _V,
    Module.INTEGRATIONS: _N, Module.CONFIG: _N, Module.USERS: _N,
}

_OVERVIEWER: Dict[Module, Permission] = {
    **_all_modules_at(_V),
    Module.INTEGRATIONS: _N, Module.CONFIG: _N, Module.USERS: _N,
}

# admin/super_admin/copilot/mega_admin get full ADMIN on every module. The
# Owner-only "ceiling" (delete company, grant super_admin, un-deletable root) is
# NOT a module permission — it is enforced separately in api-chatty. mega_admin is
# also short-circuited in effective_permission()/can().
_ADMIN_ALL: Dict[Module, Permission] = _all_modules_at(_A)

ROLE_DEFAULTS: Dict[str, Dict[Module, Permission]] = {
    "agent": _AGENT,
    "super_agent": _SUPER_AGENT,
    "marketer": _MARKETER,
    "overviewer": _OVERVIEWER,
    "admin": _ADMIN_ALL,
    "super_admin": _ADMIN_ALL,
    "copilot": _ADMIN_ALL,
    "mega_admin": _ADMIN_ALL,
}


# --- resolution ----------------------------------------------------------------

def role_default(role_value: str, module: Module) -> Permission:
    """The default permission a single role grants on a module (NONE if unknown)."""
    return ROLE_DEFAULTS.get(role_value, {}).get(module, Permission.NONE)


def effective_permission(
    role_values: List[str],
    module: Module,
    overrides: Optional[Dict[Module, Permission]] = None,
    is_mega_admin: bool = False,
) -> Permission:
    """A user's effective permission on a module.

    = max default across the user's roles, then replaced by an explicit per-user
    override if one exists for the module. mega_admin is god everywhere.
    """
    if is_mega_admin:
        return Permission.ADMIN
    best = Permission.NONE
    for role_value in role_values:
        level = role_default(role_value, module)
        if _PERMISSION_RANK[level] > _PERMISSION_RANK[best]:
            best = level
    if overrides is not None and module in overrides:
        return overrides[module]  # explicit per-user setting wins (up or down)
    return best


def can(
    role_values: List[str],
    module: Module,
    required: Permission,
    overrides: Optional[Dict[Module, Permission]] = None,
    is_mega_admin: bool = False,
) -> bool:
    """True if the user may perform an action requiring ``required`` on ``module``."""
    return permission_satisfies(
        effective_permission(role_values, module, overrides, is_mega_admin),
        required,
    )
