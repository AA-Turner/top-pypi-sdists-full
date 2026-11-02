"""Named local profiles: which Zitadel issuer and Lakekeeper warehouse to use.

One environment — one Zitadel instance, one Lakekeeper — is one profile. A
machine can hold several (dev, a customer's prod, ...), selected with
``--profile``/``DATABAAS_PROFILE``, with one marked default. ``discover()``
fills a profile in from the portal's public discovery document rather than
requiring the values to be typed in by hand.
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests

from databaas_utils.errors import ConfigurationError
from databaas_utils.settings import DEFAULT_WAREHOUSE
from databaas_utils.tokenstore import config_dir

DEFAULT_REGION = "nl-ams"
_REQUEST_TIMEOUT = 15


@dataclass(frozen=True)
class Profile:
    """Everything needed to log in and reach one warehouse as one identity.

    Profiles live in ``~/.config/databaas/config.toml`` and are written by
    ``databaas login``. Most code loads one with :func:`load_profile` or, more
    often, never touches it: ``LakehouseSettings.from_profile()`` does.

    Args:
        name: Profile name.
        issuer: The Zitadel issuer URL.
        client_id: The Native app's client id.
        project_id: The Zitadel project id, requested as an extra token
            audience. Empty relies on the app's own project being in the
            audience, which Zitadel adds by default.
        catalog_url: The Lakekeeper server root.
        warehouse: Warehouse name, ``databaas-lakehouse`` by default.
        region: Storage region.
        redirect_port: Fixed loopback port for the browser login; ``0`` picks
            a free one.

    Raises:
        ConfigurationError: If a required field is empty.
    """

    name: str
    issuer: str
    client_id: str
    project_id: str
    catalog_url: str
    warehouse: str = DEFAULT_WAREHOUSE
    region: str = DEFAULT_REGION
    redirect_port: int = 0

    def __post_init__(self) -> None:
        """Reject a profile with an empty required field."""
        required = {
            "issuer": self.issuer,
            "client_id": self.client_id,
            "catalog_url": self.catalog_url,
            "warehouse": self.warehouse,
        }
        missing = [field for field, value in required.items() if not value]
        if missing:
            raise ConfigurationError(
                f"profile {self.name!r} is missing {', '.join(missing)}"
            )


def _config_path() -> Path:
    return config_dir() / "config.toml"


def _load_raw() -> dict[str, Any]:
    path = _config_path()
    if not path.exists():
        return {}
    with path.open("rb") as fh:
        return tomllib.load(fh)


def _profile_from_mapping(name: str, values: dict[str, Any]) -> Profile:
    return Profile(
        name=name,
        issuer=str(values.get("issuer", "")),
        client_id=str(values.get("client_id", "")),
        project_id=str(values.get("project_id", "")),
        catalog_url=str(values.get("catalog_url", "")),
        warehouse=str(values.get("warehouse") or DEFAULT_WAREHOUSE),
        region=str(values.get("region") or DEFAULT_REGION),
        redirect_port=int(values.get("redirect_port") or 0),
    )


def list_profiles() -> dict[str, Profile]:
    """Every profile in the config file, keyed by name."""
    raw = _load_raw()
    profiles = raw.get("profiles", {})
    return {
        name: _profile_from_mapping(name, values) for name, values in profiles.items()
    }


def load_profile(name: str | None = None) -> Profile:
    """Resolve: an explicit name, then ``DATABAAS_PROFILE``, else the default.

    Raises:
        ConfigurationError: If no profile is configured or the name is unknown.
    """
    raw = _load_raw()
    profiles = raw.get("profiles", {})
    resolved = name or os.environ.get("DATABAAS_PROFILE") or raw.get("default")
    if not resolved:
        raise ConfigurationError(
            "no profile given and none configured — run `databaas login` first"
        )
    if resolved not in profiles:
        raise ConfigurationError(
            f"no profile named {resolved!r} in {_config_path()} — "
            f"known profiles: {sorted(profiles) or 'none'}"
        )
    return _profile_from_mapping(resolved, profiles[resolved])


def save_profile(profile: Profile, *, make_default: bool = False) -> None:
    """Write or overwrite ``profile`` in the config file, creating it if absent."""
    raw = _load_raw()
    profiles = raw.setdefault("profiles", {})
    profiles[profile.name] = {
        "issuer": profile.issuer,
        "client_id": profile.client_id,
        "project_id": profile.project_id,
        "catalog_url": profile.catalog_url,
        "warehouse": profile.warehouse,
        "region": profile.region,
        "redirect_port": profile.redirect_port,
    }
    if make_default or "default" not in raw:
        raw["default"] = profile.name
    _write_raw(raw)


def delete_profile(name: str) -> bool:
    """Remove ``name`` from the config file. Its stored session is untouched.

    Returns:
        Whether it was the default profile; the config then has no default.

    Raises:
        ConfigurationError: If there is no profile called ``name``.
    """
    raw = _load_raw()
    profiles = raw.get("profiles", {})
    if name not in profiles:
        raise ConfigurationError(
            f"no profile named {name!r} in {_config_path()} — "
            f"known profiles: {sorted(profiles) or 'none'}"
        )
    del profiles[name]
    was_default = raw.get("default") == name
    if was_default:
        del raw["default"]
    _write_raw(raw)
    return was_default


def _write_raw(raw: dict[str, Any]) -> None:
    """Serialize ``raw`` by hand.

    The config's shape is flat enough that a real TOML writer dependency isn't
    worth adding; ``tomllib`` (stdlib) reads it back.
    """
    path = _config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    if "default" in raw:
        lines.append(f"default = {_toml_str(raw['default'])}")
        lines.append("")
    for name, values in raw.get("profiles", {}).items():
        lines.append(f"[profiles.{_toml_key(name)}]")
        for key, value in values.items():
            lines.append(f"{key} = {_toml_value(value)}")
        lines.append("")
    path.write_text("\n".join(lines))


def _toml_key(name: str) -> str:
    if name and all(c.isalnum() or c in "-_" for c in name):
        return name
    return _toml_str(name)


def _toml_str(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _toml_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return _toml_str(str(value))


def _hostname(base_url: str) -> str:
    url = base_url if "://" in base_url else f"https://{base_url}"
    return urlparse(url).hostname or base_url


def endpoints_from_base_url(base_url: str) -> tuple[str, str]:
    """The Zitadel issuer and Lakekeeper root of the environment at ``base_url``.

    A Databaas environment serves Zitadel on ``auth.<host>`` and Lakekeeper on
    ``catalog.<host>``, next to the portal on ``<host>``.

    Args:
        base_url: The environment's portal address, e.g.
            ``https://next.dev.databaas.app``. The scheme may be left out.

    Returns:
        ``(issuer, catalog_url)``.

    Raises:
        ConfigurationError: If ``base_url`` is already the ``auth.`` or
            ``catalog.`` address.

    Example:
        >>> endpoints_from_base_url("https://next.dev.databaas.app")
        ('https://auth.next.dev.databaas.app', 'https://catalog.next.dev.databaas.app')
    """
    host = _hostname(base_url)
    if host.split(".")[0] in ("auth", "catalog"):
        raise ConfigurationError(
            f"{base_url!r} is the {host.split('.')[0]} address; pass the portal's "
            "base URL instead, e.g. https://next.dev.databaas.app"
        )
    return f"https://auth.{host}", f"https://catalog.{host}"


def default_profile_name(base_url: str) -> str:
    """The profile name used when none is given: the host's first label.

    Args:
        base_url: The environment's portal address.
    """
    return _hostname(base_url).split(".")[0]


def discover(portal_url: str, *, name: str | None = None) -> Profile:
    """Fetch a profile's settings from the portal's public discovery document.

    ``portal_url`` is the environment's own address (e.g.
    ``https://infoplaza.databaas.eu``), not the Zitadel issuer or the catalog.
    The document needs only ``client_id``: the issuer and catalog default to
    the ``auth.`` and ``catalog.`` addresses next to the portal, and the
    warehouse to ``databaas-lakehouse``.

    Args:
        portal_url: The environment's portal address.
        name: Profile name; the portal's first hostname label by default.

    Raises:
        requests.HTTPError: If the portal serves no discovery document.
    """
    url = portal_url.rstrip("/") + "/.well-known/databaas-client.json"
    response = requests.get(url, timeout=_REQUEST_TIMEOUT)
    response.raise_for_status()
    issuer, catalog_url = endpoints_from_base_url(portal_url)
    values = {"issuer": issuer, "catalog_url": catalog_url, **response.json()}
    return _profile_from_mapping(name or default_profile_name(portal_url), values)


@lru_cache(maxsize=32)
def oidc_metadata(issuer: str) -> dict[str, Any]:
    """The issuer's ``/.well-known/openid-configuration``, cached per process."""
    url = issuer.rstrip("/") + "/.well-known/openid-configuration"
    response = requests.get(url, timeout=_REQUEST_TIMEOUT)
    response.raise_for_status()
    return dict(response.json())
