from __future__ import annotations

import json
from typing import Any

from matrx_ai._ext import get_ext

def _pf(name: str) -> Any:
    """Resolve one of the host's picklist fetchers LAZILY, at first use.

    Binding these at import time made ``import matrx_ai.db.content_types.picklists``
    raise ``ExtNotConfiguredError`` on a standalone install — an un-importable
    module, not a degraded capability. The package must import cleanly with no
    host configured; only actually *calling* a picklist fetcher requires one.
    """
    return get_ext("picklist_reference_fetch")[name]


def fetch_full_list(*args: Any, **kwargs: Any) -> Any:
    return _pf("fetch_full_list")(*args, **kwargs)


def fetch_list_group(*args: Any, **kwargs: Any) -> Any:
    return _pf("fetch_list_group")(*args, **kwargs)


def fetch_list_item(*args: Any, **kwargs: Any) -> Any:
    return _pf("fetch_list_item")(*args, **kwargs)


def fetch_list_items_flat(*args: Any, **kwargs: Any) -> Any:
    return _pf("fetch_list_items_flat")(*args, **kwargs)


def fetch_list_summary(*args: Any, **kwargs: Any) -> Any:
    return _pf("fetch_list_summary")(*args, **kwargs)


# ---------------------------------------------------------------------------
# XML rendering — controls how picklist items are presented to LLMs.
# ---------------------------------------------------------------------------

def _items_to_xml(items: list[dict[str, Any]], list_name: str, group_name: str | None = None) -> str:
    tag_attrs = f'name={json.dumps(list_name)}'
    if group_name is not None:
        tag_attrs += f' group={json.dumps(group_name)}'
    lines = [f"<list {tag_attrs}>"]
    for item in items:
        parts = [f'  <item id={json.dumps(str(item.get("id", "")))}']
        g = item.get("group_name")
        if g:
            parts[0] += f' group={json.dumps(g)}'
        parts[0] += ">"
        lines.append(parts[0])
        lines.append(f'    <label>{item.get("label", "")}</label>')
        if item.get("description"):
            lines.append(f'    <description>{item["description"]}</description>')
        if item.get("help_text"):
            lines.append(f'    <help_text>{item["help_text"]}</help_text>')
        lines.append("  </item>")
    lines.append("</list>")
    return "\n".join(lines)


def _full_list_to_xml(result: dict[str, Any]) -> str:
    meta = result.get("list") or {}
    list_name = meta.get("list_name", "")
    items = result.get("items", [])
    return _items_to_xml(items, list_name)


# ---------------------------------------------------------------------------
# Manager — backed by the udt_structured_lists / udt_structured_list_items tables (see
# aidream db migration 0011). Bookmark wire types are kept under their
# original names ("full_list", "list_group", "list_item") because frontends
# already serialize cookies that way.
# ---------------------------------------------------------------------------

class PicklistsManager:
    _instance: PicklistsManager | None = None

    def __new__(cls) -> PicklistsManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # ------------------------------------------------------------------
    # Raw fetch — returns plain Python data, no XML
    # ------------------------------------------------------------------

    def get_full_list(self, list_id: str) -> dict[str, Any]:
        try:
            result = fetch_full_list(list_id)
            return {"success": True, "list_id": list_id, **result}
        except Exception as e:
            return {"success": False, "operation": "get_full_list", "list_id": list_id, "error": str(e)}

    def get_list_summary(self, list_id: str) -> dict[str, Any]:
        try:
            meta = fetch_list_summary(list_id)
            return {"success": True, "list_id": list_id, "list": meta}
        except Exception as e:
            return {"success": False, "operation": "get_list_summary", "list_id": list_id, "error": str(e)}

    def get_list_items(self, list_id: str) -> dict[str, Any]:
        try:
            items = fetch_list_items_flat(list_id)
            return {"success": True, "list_id": list_id, "items": items, "item_count": len(items)}
        except Exception as e:
            return {"success": False, "operation": "get_list_items", "list_id": list_id, "error": str(e)}

    def get_list_group(self, list_id: str, group_name: str) -> dict[str, Any]:
        try:
            items = fetch_list_group(list_id, group_name)
            return {"success": True, "list_id": list_id, "group_name": group_name, "items": items}
        except Exception as e:
            return {"success": False, "operation": "get_list_group", "list_id": list_id, "error": str(e)}

    def get_list_item(self, list_id: str, item_id: str) -> dict[str, Any]:
        try:
            item = fetch_list_item(list_id, item_id)
            return {"success": True, "list_id": list_id, "item_id": item_id, "item": item}
        except Exception as e:
            return {"success": False, "operation": "get_list_item", "list_id": list_id, "error": str(e)}

    # ------------------------------------------------------------------
    # XML rendering — for injecting picklist content into LLM context
    # ------------------------------------------------------------------

    def get_full_list_as_xml(self, list_id: str) -> dict[str, Any]:
        try:
            result = fetch_full_list(list_id)
            xml = _full_list_to_xml(result)
            return {"success": True, "xml": xml}
        except Exception as e:
            return {"success": False, "operation": "get_full_list_as_xml", "list_id": list_id, "error": str(e)}


picklists_manager_instance = PicklistsManager()
