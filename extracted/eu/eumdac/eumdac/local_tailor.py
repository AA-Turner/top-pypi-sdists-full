"""Module for interfacing with local Data Tailor instances."""

from pathlib import Path
from urllib.parse import urlparse

from eumdac.config import get_url_path
from eumdac.datatailor import DataTailor
from eumdac.errors import EumdacError
from eumdac.token import AnonymousAccessToken, URLs

import sys

if sys.version_info < (3, 9):
    from typing import Iterable
else:
    from collections.abc import Iterable


def get_tailor_id(filepath: Path) -> str:
    """get a tailor id from a configuration file path"""
    return filepath.stem


def get_tailor_path(tailor_id: str) -> Path:
    """get a configuration file path from a tailor id"""
    for fn in all_url_filenames():
        if tailor_id == get_tailor_id(fn):
            return fn

    raise EumdacError(f"local-tailor id not found: {tailor_id}")


def get_urls(filepath: Path) -> URLs:
    """retrieve a URLs instance from an INI file path"""
    return URLs(str(filepath))


def all_url_filenames(prefix: str = "") -> Iterable[Path]:
    """retrieve file Paths of configured URL files"""
    url_dir = get_url_path()
    glob = "*.ini"
    if len(prefix) > 0:
        glob = f"{prefix}#*.ini"
    return sorted(url_dir.glob(glob))


def new_url_filename(tailor_id: str) -> Path:
    """create a Path pointing to a URLs configuration INI file that can be created subsequently"""
    return get_url_path() / Path(f"{tailor_id}.ini")


def remove_url(url_name: str) -> None:
    """remove a URLs configuration INI from configuration directory"""
    p = get_url_path() / Path(f"{url_name}.ini")
    if p.exists():
        p.unlink()


def resolve_url(url_name: str) -> URLs:
    """retrieve a URLs instance from an identifier"""
    p = get_url_path() / Path(f"{url_name}.ini")
    if p.exists():
        return URLs(str(p))
    else:
        raise EumdacError(f"{url_name} not found at {str(p)}.")


def get_local_tailor(tailor_id: str) -> DataTailor:
    """create a DataTailor instance using a URLs configuration identified via configuration identifier"""
    url = resolve_url(tailor_id)
    token = AnonymousAccessToken(urls=url)
    return DataTailor(token)


def new_local_tailor(tailor_id: str, tailor_url: str) -> Path:
    """create a configuration for a local-tailor instance specifying an identifer and base url"""
    parsed_url = urlparse(tailor_url)

    if not parsed_url.scheme:
        raise EumdacError("No scheme provided")
    if not parsed_url.hostname:
        raise EumdacError("No hostname provided")
    if not parsed_url.port:
        raise EumdacError("No port provided")

    filepath = new_url_filename(tailor_id)
    with filepath.open("w") as f:
        new_url = URLs()
        new_url.set("tailor", "epcs", f"{tailor_url}/api/v1")
        new_url.write(f)
    return filepath


def remove_local_tailor(tailor_id: str) -> None:
    """remove a local-tailor configuration by specifying its' identifier"""
    remove_url(tailor_id)


def is_online(filepath: Path) -> bool:
    """determine the state of a local-tailor instance by specifying Path to configuration file"""
    try:
        dt = get_local_tailor(get_tailor_id(filepath))
        _ = dt.info
        return True
    except Exception:
        return False


def get_api_url(filepath: Path) -> str:
    """retrieve local-tailor base api url from a given local-tailor configuration file path"""
    urls = get_urls(filepath)
    return urls.get("tailor", "epcs")
