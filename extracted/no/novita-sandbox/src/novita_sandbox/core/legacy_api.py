from datetime import datetime
from typing import Any, Optional

from dateutil.parser import isoparse

from novita_sandbox.core.api import SandboxCreateResponse
from novita_sandbox.core.api.client.models import Sandbox
from novita_sandbox.core.api.client.models.sandbox_state import SandboxState
from novita_sandbox.core.api.client.types import UNSET
from novita_sandbox.core.sandbox.sandbox_api import SandboxInfo
from novita_sandbox.core.template.types import TemplateInfo, TemplateList


def parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return isoparse(value)
    return datetime.fromtimestamp(0)


def sandbox_from_dict(data: dict[str, Any]) -> Sandbox:
    sandbox_id = data.get("sandboxID", "")
    client_id = data.get("clientID", "")
    return Sandbox.from_dict(
        {
            "clientID": client_id,
            "sandboxID": f"{sandbox_id}-{client_id}" if client_id else sandbox_id,
            "templateID": data.get("templateID", ""),
            "envdVersion": data.get("envdVersion", ""),
            "alias": data.get("alias", UNSET),
            "domain": data.get("domain", UNSET),
            "envdAccessToken": data.get("envdAccessToken", UNSET),
            "trafficAccessToken": data.get("trafficAccessToken", UNSET),
        }
    )


def sandbox_create_response_from_dict(data: dict[str, Any]) -> SandboxCreateResponse:
    sandbox_id = data.get("sandboxID", "")
    client_id = data.get("clientID")
    return SandboxCreateResponse(
        sandbox_id=f"{sandbox_id}-{client_id}" if client_id else sandbox_id,
        sandbox_domain=data.get("domain"),
        envd_version=data.get("envdVersion", ""),
        envd_access_token=data.get("envdAccessToken"),
        traffic_access_token=data.get("trafficAccessToken"),
    )


def sandbox_info_from_dict(data: dict[str, Any]) -> SandboxInfo:
    sandbox_id = data.get("sandboxID", "")
    client_id = data.get("clientID")
    return SandboxInfo(
        sandbox_id=f"{sandbox_id}-{client_id}" if client_id else sandbox_id,
        sandbox_domain=data.get("domain"),
        template_id=data.get("templateID", ""),
        name=data.get("alias"),
        metadata=data.get("metadata") or {},
        started_at=parse_datetime(data.get("startedAt")),
        end_at=parse_datetime(data.get("endAt")),
        state=SandboxState(data.get("state", SandboxState.RUNNING.value)),
        cpu_count=data.get("cpuCount") or 0,
        memory_mb=data.get("memoryMB") or 0,
        envd_version=data.get("envdVersion", ""),
        _envd_access_token=data.get("envdAccessToken"),
        allow_internet_access=data.get("allowInternetAccess"),
        volume_mounts=data.get("volumeMounts") or [],
    )


def template_list_from_dict(
    data: Optional[dict[str, Any]],
    template_type: str,
    page: int,
    limit: int,
) -> TemplateList:
    if not data:
        return TemplateList(items=[], total=0, page=page, limit=limit, total_pages=0)

    return TemplateList(
        items=[
            TemplateInfo.from_dict(template, template_type=template_type)
            for template in data.get("templates", [])
        ],
        total=data.get("total", 0),
        page=data.get("page", page),
        limit=data.get("limit", limit),
        total_pages=data.get("totalPages", 0),
    )
