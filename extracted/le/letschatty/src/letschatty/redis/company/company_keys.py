"""The Redis keys of a company outside the asset's own, in one place: the facade `Companies` of api-chatty reads them
(the routing lookups, its settings and betas) and `letschatty/redis/company/` writes and forgets them."""
from __future__ import annotations

from datetime import datetime
from typing import Any, List

from ...models.company.empresa import EmpresaModel

ROUTING_KEY_TTL = 86400  # 24 hours


def routing_key_phone(phone_number_id: str) -> str:
    return f"company_routing:phone:{phone_number_id}"


def routing_key_alias(alias: str) -> str:
    return f"company_routing:alias:{alias}"


def routing_key_origin(origin: str) -> str:
    return f"company_routing:origin:{origin}"


def settings_key(company_id: str) -> str:
    return f"empresas:messaging_settings:{company_id}"


def betas_key(company_id: str) -> str:
    return f"empresas:betas:{company_id}"


def version_key(company_id: str) -> str:
    return f"company_version:{company_id}"


def is_deleted(company: Any) -> bool:
    # `isinstance`: a company that is not a real one (a mock) is not deleted.
    return isinstance(getattr(company, "deleted_at", None), datetime)


def routing_keys_of(company: EmpresaModel) -> List[str]:
    if not company.active_for_messaging:
        return []
    keys = []
    try:
        keys.append(routing_key_phone(company.phone_number_id_value))
    except ValueError:
        pass
    for alias in company.friendly_aliases or []:
        keys.append(routing_key_alias(alias))
    for origin in company.allowed_origins or []:
        keys.append(routing_key_origin(origin))
    return keys
