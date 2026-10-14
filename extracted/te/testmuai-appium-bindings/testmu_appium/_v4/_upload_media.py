import logging
import os

import requests

from testmu_appium._v4._vars import _ATMS_DEFAULT_URL, _atms_auth_headers

_log = logging.getLogger("testmu")


def _current_media_id(item: dict) -> str:
    """The File's current media id from Test Manager, else the id the entry was saved with (always for ``local.``)."""
    alias = item.get("alias") or ""
    if alias and not alias.startswith("local."):
        atms_url = os.getenv("ATMS_URL", _ATMS_DEFAULT_URL).rstrip("/")
        try:
            resp = requests.get(f"{atms_url}/api/v1/files/resolve", params={"alias": alias}, headers=_atms_auth_headers(), timeout=60)
            resp.raise_for_status()
            media_id = resp.json().get("media_id") or ""
            if media_id:
                return str(media_id).removeprefix("lt://")
        except Exception as e:
            _log.warning("Failed to resolve file %s: %s", alias, e)
    return str(item.get("media_id") or "").removeprefix("lt://")


def upload_media_ids(items: list) -> list:
    ids = []
    for item in items or []:
        if isinstance(item, str):
            if item:
                ids.append(item)
            continue
        if not isinstance(item, dict):
            continue
        media_id = _current_media_id(item)
        if media_id:
            ids.append(f"lt://{media_id}")
    return ids
