import logging
import os

import requests

from testmu_selenium._downloads_path import _resolve_downloads_dir
from testmu_selenium._vars import _ATMS_DEFAULT_URL, _atms_auth_headers, _variable_store

_log = logging.getLogger("testmu")


def download_uploaded_files(files) -> None:
    if not files:
        return
    if not (os.getenv("LT_USERNAME") and os.getenv("LT_ACCESS_KEY")):
        _log.warning("Cannot download files — no LT credentials")
        return
    headers = {"Authorization": _atms_auth_headers()["Authorization"]}
    dl_dir = _resolve_downloads_dir()
    os.makedirs(dl_dir, exist_ok=True)
    for f in files:
        url = f.get("media_url", "")
        name = f.get("name", "")
        alias = f.get("alias", "")
        if alias and not alias.startswith("local."):
            resolved = _resolve_test_file(alias, headers)
            url = resolved.get("media_url") or url
            name = name or resolved.get("file_name", "")
        if not url or not name:
            continue
        if not url.startswith("http"):
            url = f"https://{url}"
        dest = os.path.join(dl_dir, name)
        try:
            with requests.get(url, headers=headers, stream=True, timeout=300) as resp:
                resp.raise_for_status()
                with open(dest, "wb") as out:
                    for chunk in resp.iter_content(8192):
                        out.write(chunk)
            _log.info("Downloaded: %s -> %s", name, dest)
        except Exception as e:
            _log.warning("Failed to download %s: %s", name, e)
            continue
        if alias:
            _variable_store[f"file.{alias}"] = os.path.abspath(dest)


def _resolve_test_file(alias: str, headers: dict) -> dict:
    """Current media-store copy of a File; {} on failure (caller keeps the entry's media_url)."""
    atms_url = os.getenv("ATMS_URL", _ATMS_DEFAULT_URL).rstrip("/")
    try:
        resp = requests.get(f"{atms_url}/api/v1/files/resolve", params={"alias": alias}, headers=headers, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        _log.warning("Failed to resolve file %s: %s", alias, e)
        return {}
