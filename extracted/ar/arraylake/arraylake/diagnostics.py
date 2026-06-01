# Portions of this module were adapted from xarray.
# https://github.com/pydata/xarray/blob/44488288fd8309e3468ee45a5f7408d75a21f493/xarray/util/print_versions.py
# Xarray is licensed under the Appache 2.0 License with the following copyright notice:
#
#   Copyright 2014-2023, xarray Developers

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""Utility functions for printing version information."""

import importlib
import locale
import os
import platform
import struct
import sys
from pprint import pprint

import httpx

from arraylake.config import config
from arraylake.log_util import get_logger
from arraylake.types import UserDiagnostics

logger = get_logger(__name__)


def get_system_info() -> dict[str, str]:
    """Returns system information as a dict"""

    try:
        (sysname, _nodename, release, _version, machine, processor) = platform.uname()
        info = {
            "python": sys.version,
            "python-bits": str(struct.calcsize("P") * 8),
            "OS": f"{sysname}",
            "OS-release": f"{release}",
            "machine": f"{machine}",
            "processor": f"{processor}",
            "byteorder": f"{sys.byteorder}",
            "LC_ALL": f"{os.environ.get('LC_ALL', 'None')}",
            "LANG": f"{os.environ.get('LANG', 'None')}",
            "LOCALE": f"{locale.getlocale()}",
        }
    except Exception:
        logger.exception("failed to get system info")
        info = {}

    return info


def get_versions() -> dict[str, str]:
    """gather the versions of arraylake and its dependencies"""

    deps = [
        # (MODULE_NAME, f(mod) -> mod version)
        ("arraylake", lambda mod: mod.__version__),
        ("aiobotocore", lambda mod: mod.__version__),
        ("uvloop", lambda mod: mod.__version__),
        ("zarr", lambda mod: mod.__version__),
        ("numcodecs", lambda mod: mod.__version__),
        ("numpy", lambda mod: mod.__version__),
        ("donfig", lambda mod: mod.__version__),
        ("pydantic", lambda mod: mod.__version__),
        ("httpx", lambda mod: mod.__version__),
        ("ruamel.yaml", lambda mod: mod.__version__),
        ("typer", lambda mod: mod.__version__),
        ("rich", lambda mod: mod.__version__),
        ("fsspec", lambda mod: mod.__version__),
        ("kerchunk", lambda mod: mod.__version__),
        ("h5py", lambda mod: mod.__version__),
        ("s3fs", lambda mod: mod.__version__),
        ("cachetools", lambda mod: mod.__version__),
        ("structlog", lambda mod: mod.__version__),
        ("ipytree", lambda mod: mod.__version__),
        ("xarray", lambda mod: mod.__version__),
        ("dateutil", lambda mod: mod.__version__),
        ("click", lambda mod: mod.__version__),
        ("dask", lambda mod: mod.__version__),
        ("distributed", lambda mod: mod.__version__),
        ("icechunk", lambda mod: mod.__version__),
    ]
    versions: dict[str, str] = {}
    for modname, ver_f in deps:
        try:
            if modname in sys.modules:
                mod = sys.modules[modname]
            else:
                mod = importlib.import_module(modname)
        except Exception:
            versions[modname] = "none"
        else:
            try:
                ver = ver_f(mod)
                versions[modname] = ver
            except Exception:
                versions[modname] = "installed"
    return versions


def get_service_info(service_uri: str) -> dict[str, str]:
    with httpx.Client() as client:
        response = client.get(service_uri)
    data = response.json()
    info = {"service_uri": service_uri, "service_version": data["arraylake_api_version"]}
    return info


def get_config_info() -> dict[str, str]:
    """
    Returns a careful summary of the user config

    We don't want to leak any sensitive information, so we only return a subset of the config object.
    """
    info = {}
    for k in ["user.org", "log_level", "http_max_retries", "http_timeout"]:
        v = config.get(k, "__not_set__")  # note: None is a valid config in some cases
        if v != "__not_set__":
            info[k] = v
    return info


def get_diagnostics(service_uri: str | None = None) -> UserDiagnostics:
    """get the system and version diagnostics"""
    diagnostics = UserDiagnostics(system=get_system_info(), versions=get_versions(), config=get_config_info())

    if service_uri is not None:
        try:
            diagnostics.service = get_service_info(service_uri)
        except Exception:
            logger.exception("failed to get service diagnostics")

    return diagnostics


def print_diagnostics(**kwargs) -> None:
    diagnostics = get_diagnostics()
    pprint(diagnostics, sort_dicts=False)
