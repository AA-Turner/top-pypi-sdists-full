"""Headless fleet release inventory shared by HTTP and Harness callers.

An operator-managed catalog points at wheel bundles on existing Secure Files.
Absent a catalog entry, published PyPI releases remain the source of versions.
"""
import json
import logging
import os
from pathlib import Path

log = logging.getLogger(__name__)


def catalog():
    path = Path(os.environ.get('HUGPY_CORE_RELEASE_CATALOG', '/etc/hugpy/releases.json'))
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError('Release catalog must map package names to releases')
    return data


def release(package='hugpy-wrapper', version=None):
    value = catalog().get(package)
    if value is None or (version is not None and value.get('version') != version):
        return None
    from packaging.version import Version
    Version(value['version'])
    if value.get('artifact') is not None:
        from fitevict.cli.update import validate_artifact
        validate_artifact(value['artifact'])
    return value


# Box packages and where they come from. A release = publishing to PyPI; every
# box converges to the latest published versions (no wheels built or served here).
FLEET_PACKAGES = [p for p in os.environ.get(
    "HUGPY_CORE_FLEET_PACKAGES", "hugpy-wrapper,hugpy-worker").split(",") if p]
PYPI_JSON = os.environ.get("HUGPY_CORE_PYPI_JSON", "https://pypi.org/pypi/{name}/json")
PYPI_TTL = 300.0
_pypi = {"at": 0.0, "versions": {}, "running": False}


def _ver_key(v):
    try:
        from packaging.version import Version
        return Version(str(v))
    except Exception:  # noqa: BLE001
        import re
        return tuple(int(x) if x.isdigit() else -1 for x in re.split(r"[.+-]", str(v or "")))


def fleet_versions() -> dict:
    """{package: latest PyPI version} for the box packages. Refreshed in the
    background every PYPI_TTL; a failed lookup keeps the last known version."""
    import threading
    import time
    import urllib.request
    if time.time() - _pypi["at"] >= PYPI_TTL and not _pypi["running"]:
        _pypi["running"] = True

        def run():
            try:
                got = dict(_pypi["versions"])
                for name in FLEET_PACKAGES:
                    try:
                        with urllib.request.urlopen(PYPI_JSON.format(name=name), timeout=15) as r:
                            got[name] = json.loads(r.read().decode("utf-8"))["info"]["version"]
                    except Exception as exc:  # noqa: BLE001
                        log.warning("PyPI version lookup failed for %s: %s", name, exc)
                # never go backwards: PyPI's JSON can lag a fresh release for a
                # minute or two; keep the newest version ever seen per package
                prev = _pypi["versions"]
                for k, v in list(got.items()):
                    if k in prev and prev[k] and _ver_key(v) < _ver_key(prev[k]):
                        got[k] = prev[k]
                _pypi["versions"] = got
            finally:
                _pypi["at"] = time.time()
                _pypi["running"] = False

        threading.Thread(target=run, name="pypi-versions", daemon=True).start()
    versions = dict(_pypi["versions"])
    for name in catalog():
        selected = release(name)
        versions[name] = selected['version']
    return versions


