"""Default actuator plugin that serves build-time service metadata."""

import json
import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from fastapi import APIRouter, FastAPI

from .base import ActuatorLink, BaseActuatorPlugin

_DEFAULT_INFO_PATH = "service_info.json"
_INFO_SECTIONS = ("git", "build")

# Nested key-order schema — mirrors the JSON shape so preferred insertion
# order is readable at a glance.  ``None`` leaves mean "no child ordering".
_KEY_ORDER: dict[str, dict | None] = {
    "git": {
        "branch": None,
        "commit": {
            "time": None,
            "message": {"full": None, "short": None},
            "id": {"describe": None, "abbrev": None, "full": None},
            "user": {"email": None, "name": None},
        },
        "build": {
            "version": None,
            "user": {"name": None, "email": None},
            "host": None,
        },
        "dirty": None,
        "tags": None,
        "total": {"commit": {"count": None}},
        "closest": {"tag": {"commit": {"count": None}, "name": None}},
        "remote": {"origin": {"url": None}},
    },
    "build": {
        "artifact": None,
        "name": None,
        "time": None,
        "version": None,
        "group": None,
    },
}


def _reorder(value: Any, order: dict | None = None) -> Any:
    """Recursively reorder dict keys according to *order*, preserving extras."""
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        if order:
            for key in order:
                if key in value:
                    result[key] = _reorder(value[key], order[key])
        for key, child in value.items():
            if key not in result:
                result[key] = _reorder(child)
        return result

    if isinstance(value, list):
        return [_reorder(item) for item in value]

    return value


def _build_info_payload(loaded: dict[str, Any]) -> dict[str, Any]:
    payload: dict[str, Any] = {}

    for section in _INFO_SECTIONS:
        section_value = loaded.get(section)
        if isinstance(section_value, dict):
            payload[section] = section_value

    return dict(_reorder(payload, _KEY_ORDER))


class InfoActuatorPlugin(BaseActuatorPlugin):
    """Expose Spring-style ``/actuator/info`` from a baked JSON file."""

    name = "info"

    def register(
        self,
        router: APIRouter,
        *,
        app: FastAPI,
        prefix: str,
    ) -> Mapping[str, ActuatorLink]:
        path = self._resolve_info_path()

        if not path.exists():
            return {}

        @router.get("/info", include_in_schema=False)
        async def info() -> dict[str, Any]:
            return self._load_info(path)

        return {"info": self.build_link(prefix=prefix, route_path="/info")}

    def _resolve_info_path(self) -> Path:
        path_value = os.getenv("ACTUATOR_INFO_PATH")
        return Path(path_value or _DEFAULT_INFO_PATH)

    def _load_info(self, path: Path) -> dict[str, Any]:
        def _load() -> dict[str, Any]:
            if not path.exists():
                return {}

            try:
                loaded = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                return {}

            if isinstance(loaded, dict):
                return _build_info_payload(loaded)

            return {}

        return self.memoized_payload(cache_key=str(path), loader=_load)
