from __future__ import annotations

import asyncio
import hashlib
import json
import os
import platform
import re
import shutil
import site
import subprocess
import sys
import typing
from base64 import urlsafe_b64encode
from collections import defaultdict
from logging import getLogger
from pathlib import Path
from typing import Dict, List, Set, cast
from urllib.parse import urlparse

from importlib_metadata import Distribution, PackagePath, PathDistribution
from packaging.version import InvalidVersion
from packaging.version import parse as parse_version
from rich.progress import Progress
from typing_extensions import Literal

from coiled.pypi_conda_map import CONDA_TO_PYPI
from coiled.software_utils import make_coiled_local_name, set_auth_for_url
from coiled.types import CondaPackage, CondaPlaceHolder, PackageInfo
from coiled.utils import (
    get_encoding,
    parse_file_uri,
    recurse_importable_python_files,
    safe_path_resolve,
)

logger = getLogger("coiled.package_sync")
subdir_datas = {}
PYTHON_VERSION = platform.python_version_tuple()


class ResilientDistribution(PathDistribution):
    """Subclass of Distribution that adds more resilient methods for retrieving files"""

    def _read_files_egginfo_installed(self):
        """
        Read installed-files.txt and return lines in a similar
        CSV-parsable format as RECORD: each file should be placed
        relative to the site-packages directory and must be
        quoted (since file names can contain literal commas).

        This file is written when the package is installed by pip,
        but it might not be written for other installation methods.
        Assume the file is accurate if it exists.
        """
        text = self.read_text("installed-files.txt")
        # Prepend the .egg-info/ subdir to the lines in this file.
        # But this subdir is only available from PathDistribution's
        # self._path.
        subdir = self._path
        if not text or not subdir:
            return

        site_pkgs_path = cast(Path, self.locate_file("")).resolve()
        for name in text.splitlines():
            # relpath will add .. to a path to make it relative to site-packages,
            # so use that instead of Path.relative_to (which will raise an error)
            path = Path(os.path.relpath((subdir / name).resolve(), site_pkgs_path))
            yield f'"{path.as_posix()}"'


def convert_conda_to_pypi_name(name: str):
    return CONDA_TO_PYPI.get(name, name)


def normalize_version(version: str):
    """Attempt to normalize version between conda and pip without tripping over conda not supporting PEP440"""
    # Bail on non-PEP440 versions like 2023c, which will get parsed as 2023rc0
    if not len(version.split(".")) > 2:
        return version
    else:
        try:
            # Normalize things like 23.04.00 to 23.4.0
            return str(parse_version(version))
        # Fallback to original version if its unparseable like 1.7.1dev.rapidsai23.04
        except InvalidVersion:
            return version


async def scan_conda(prefix: Path, progress: Progress | None = None) -> typing.Dict[str, List[PackageInfo]]:
    conda_meta = prefix / "conda-meta"
    if conda_meta.exists() and conda_meta.is_dir():
        conda_packages = []
        for metafile in conda_meta.iterdir():
            if metafile.suffix == ".json":
                with metafile.open("r") as f:
                    conda_packages.append(CondaPackage(json.load(f), prefix=prefix))
        packages: List[PackageInfo] = []
        if progress:
            for task in progress.track(
                asyncio.as_completed([handle_conda_package(pkg=pkg) for pkg in conda_packages]),
                description=f"Scanning {len(conda_packages)} conda packages",
                total=len(conda_packages),
            ):
                r = await task
                if r:
                    packages.append(r)
        else:
            logger.info(f"Scanning {len(conda_packages)} conda packages...")
            packages = [
                pkg for pkg in await asyncio.gather(*[handle_conda_package(pkg=pkg) for pkg in conda_packages]) if pkg
            ]
        # it's possible for multiple similar packages to be "installed"
        # eg importlib-metadata & importlib_metadata
        # we have to check later which one is actually being imported
        result: Dict[str, List[PackageInfo]] = defaultdict(list)
        for pkg in packages:
            result[pkg["name"]].append(pkg)
        return result
    else:
        return {}


async def handle_conda_package(pkg: CondaPackage) -> PackageInfo | None:
    # Are there conda packages that install multiple python packages?
    metadata_location = next(
        (pkg.prefix / Path(fp).parent for fp in pkg.files if fp.endswith(("METADATA", "PKG-INFO"))), None
    )
    if metadata_location:
        if not metadata_location.exists():
            # a file for this package no longer exists
            # likely pip installed a new version
            # removing the conda installed version
            return None
        else:
            dist = ResilientDistribution(pkg.prefix / metadata_location)  # type: ignore
            name = dist.metadata.get("Name") or pkg.name
            path = Path(str(dist._path))
    else:
        name = pkg.name
        path = (
            # Just pick a file so we can know this isn't a metapackage
            Path(pkg.prefix / pkg.files[0]) if pkg.files else None
        )
    pkg.channel_url = set_auth_for_url(pkg.channel_url)
    return {
        "channel": pkg.channel,
        "path": path,
        "channel_url": pkg.channel_url,
        "source": "conda",
        "conda_name": pkg.name,
        "subdir": pkg.subdir,
        "name": convert_conda_to_pypi_name(name),
        "version": pkg.version,
        "wheel_target": None,
    }


async def handle_dist(dist: Distribution, locations: List[Path]) -> PackageInfo | CondaPlaceHolder | None:
    # Sometimes the dist name is blank (seemingly only on Windows?)
    try:
        if not dist.name:
            return
    # Newer versions of importlib_metadata will raise a KeyError instead
    # of returning None
    except KeyError:
        return
    installer = dist.read_text("INSTALLER") or ""
    installer = installer.rstrip()
    # dist._path can sometimes be a zipp.Path or something else
    dist_path = Path(str(dist._path))  # type: ignore
    if installer == "conda":
        return CondaPlaceHolder(name=convert_conda_to_pypi_name(dist.name), path=dist_path)
    elif dist_path.parent.suffix == ".egg":
        # egg files can be a directory OR a zip file
        # the zipp implementation of Path always uses
        # linux style seperators so we strip them too
        return {
            "name": dist.name,
            "path": dist_path.parent,
            "source": "pip",
            "channel": None,
            "subdir": None,
            "channel_url": None,
            "conda_name": None,
            "version": dist.version,
            "wheel_target": str(dist_path.parent).rstrip(os.sep + "/"),
        }
    else:
        direct_url_metadata = dist.read_text("direct_url.json")
        if direct_url_metadata:
            url_metadata = json.loads(direct_url_metadata)
            url = url_metadata.get("url")
            if not url:
                # no url in this file
                # invalid PEP-610 so don't do anything
                pass
            elif url_metadata.get("vcs_info"):
                # PEP-610 Source is VCS
                vcs_info = url_metadata["vcs_info"]
                if not isinstance(vcs_info, dict) or "vcs" not in vcs_info:
                    # PEP-610 requires vcs_info to be a dict with a vcs key
                    pass
                vcs: Literal["git", "hg", "bzr", "svn"] = vcs_info["vcs"]
                commit = vcs_info.get("commit_id")
                url = url_metadata["url"]
                pip_url = f"{vcs}+{url}"
                # uv < 0.5.23 doesn't include commit_id, so we cannot pin
                # to a specific commit.
                if commit is not None:
                    pip_url += f"@{commit}"
                return {
                    "name": dist.name,
                    "path": dist_path,
                    "source": "pip",
                    "channel": None,
                    "channel_url": None,
                    "subdir": None,
                    "conda_name": None,
                    "version": dist.version,
                    "wheel_target": pip_url,
                }
            elif str((Path("pypoetry") / "artifacts")) in url_metadata["url"]:
                # if the install source is actually the pre 1.2 poetry cache location
                # they this is actually just normal a pypi
                # and we can ignore direct_url.json
                pass
            elif url_metadata.get("archive_info") is not None:
                # PEP-610 - Source is an archive/wheel, somewhere!
                p = urlparse(url)
                if p.scheme == "file":
                    url = str(parse_file_uri(url))
                return {
                    "name": dist.name,
                    "path": dist_path,
                    "source": "pip",
                    "channel": None,
                    "channel_url": None,
                    "subdir": None,
                    "conda_name": None,
                    "version": dist.version,
                    "wheel_target": url,
                }
            elif url_metadata.get("dir_info") is not None:
                # PEP-610 - Source is a local directory
                path = parse_file_uri(url)
                return {
                    "name": dist.name,
                    "path": path,
                    "source": "pip",
                    "channel": None,
                    "channel_url": None,
                    "subdir": None,
                    "conda_name": None,
                    "version": dist.version,
                    "wheel_target": str(path),
                }
        egg_links = []
        for location in locations:
            egg_link_pth = location / Path(dist.name).with_suffix(".egg-link")
            if egg_link_pth.is_file():
                egg_links.append(location / Path(dist.name).with_suffix(".egg-link"))
        if egg_links:
            return {
                "name": dist.name,
                "path": dist_path.parent,
                "source": "pip",
                "channel": None,
                "channel_url": None,
                "subdir": None,
                "conda_name": None,
                "version": dist.version,
                "wheel_target": str(dist_path.parent),
            }
        return {
            "name": dist.name,
            "path": dist_path,
            "source": "pip",
            "channel": None,
            "channel_url": None,
            "subdir": None,
            "conda_name": None,
            "version": dist.version,
            "wheel_target": None,
        }


def _is_hash_match(dist: Distribution, pkg_paths: Dict[str, PackagePath], path: str):
    dist_path = Path(str(dist._path)).parent  # type: ignore
    pkg_path = pkg_paths.get(path)
    if pkg_path is not None and pkg_path.hash is not None:  # type: ignore
        pkg_hash = pkg_path.hash  # type: ignore
        hash_func = getattr(hashlib, pkg_hash.mode)
        absolute_path = dist_path / pkg_path
        if absolute_path.exists() and absolute_path.is_file():
            with absolute_path.open("rb") as f:
                actual_hash = urlsafe_b64encode(hash_func(f.read()).digest()).strip(b"=").decode()
                if actual_hash == pkg_hash.value:
                    return True
    return False


async def scan_pip(
    locations: List[Path], progress: Progress | None = None
) -> typing.Dict[str, PackageInfo | CondaPlaceHolder]:
    # distributions returns ALL distributions
    # even ones that are not active
    # this is a trick so we only get the distribution
    # that is last in stack
    locations = [location for location in locations if location.exists() and location.is_dir()]
    paths: List[str] = [str(location) for location in locations]
    encoding = get_encoding()
    for location in locations:
        for fp in location.iterdir():
            if fp.suffix in [".pth", ".egg-link"]:
                try:
                    file_text = fp.read_text()
                except UnicodeDecodeError:
                    try:
                        file_text = fp.read_text(encoding=encoding)
                    except UnicodeDecodeError:
                        logger.debug("Could not read file %s with encoding %s", fp, encoding, exc_info=True)
                        continue

                for line in file_text.split("\n"):
                    if line.startswith("#"):
                        continue
                    elif line.startswith(("import", "import\t")):
                        continue
                    elif line.rstrip() == ".":
                        continue
                    else:
                        p = location / Path(line.rstrip())
                        full_path = str(safe_path_resolve(p))
                        if p.exists() and full_path not in paths:
                            paths.append(full_path)
    # can't use ResilientDistribution here properly without monkey patching it
    dists: List[Distribution] = [dist for dist in Distribution.discover(path=list(paths))]
    packages = []
    if progress:
        for task in progress.track(
            asyncio.as_completed([handle_dist(dist, locations) for dist in dists]),
            total=len(dists),
            description=f"Scanning {len(dists)} python packages",
        ):
            packages.append(await task)
    else:
        logger.info(f"Scanning {len(dists)} python packages...")
        packages = await asyncio.gather(*(handle_dist(dist, locations) for dist in dists))

    # Resolve duplicate packages
    pkgs_by_name = {}
    for pkg in packages:
        if pkg:
            pkg_name = pkg["name"]
            # For duplicate .dist-info directories, we need to check which
            # version is actually importable
            existing_pkg = pkgs_by_name.get(pkg_name)
            if existing_pkg is None:
                pkgs_by_name[pkg_name] = pkg
            else:
                # Compare hashes to actual files
                new_dist = ResilientDistribution(pkg["path"])  # type: ignore
                old_dist = ResilientDistribution(existing_pkg["path"])
                new_dist_path = new_dist._path
                old_dist_path = old_dist._path
                new_is_egg_info = new_dist_path.name.endswith(".egg-info")  # type: ignore
                old_is_egg_info = old_dist_path.name.endswith(".egg-info")  # type: ignore
                new_is_dist_info = new_dist_path.name.endswith(".dist-info")  # type: ignore
                old_is_dist_info = old_dist_path.name.endswith(".dist-info")  # type: ignore
                if (new_is_egg_info and not old_is_egg_info) or (new_is_dist_info and not old_is_dist_info):
                    continue
                if (not new_is_egg_info and old_is_egg_info) or (not new_is_dist_info and old_is_dist_info):
                    pkgs_by_name[pkg_name] = pkg
                    continue

                if new_is_egg_info and old_is_egg_info:
                    # This should never happen
                    logger.debug(
                        "Found two egg-info directories with the same name: %s and %s", new_dist_path, old_dist_path
                    )

                new_pkg_paths = {
                    str(f): f
                    for f in (new_dist.files or [])
                    if (
                        not f.name.endswith(".pyc")
                        and f.parent.name != new_dist_path.name  # type: ignore
                        and f.hash is not None  # type: ignore
                    )
                }
                old_pkg_paths = {
                    str(f): f
                    for f in (old_dist.files or [])
                    if (
                        not f.name.endswith(".pyc")
                        and f.parent.name != old_dist_path.name  # type: ignore
                        and f.hash is not None  # type: ignore
                    )
                }
                old_paths = set(old_pkg_paths.keys())
                new_paths = set(new_pkg_paths.keys())
                same_hashes = {
                    path
                    for path in old_paths.intersection(new_paths)
                    if old_pkg_paths[path].hash.mode == new_pkg_paths[path].hash.mode  # type: ignore
                    and old_pkg_paths[path].hash.value == new_pkg_paths[path].hash.value  # type: ignore
                }
                paths_to_check = new_paths.union(old_paths) - same_hashes

                for path in paths_to_check:
                    # Since we are only checking files that have different hashes,
                    # we can just assume the new version is correct on the first
                    # match.
                    if _is_hash_match(new_dist, new_pkg_paths, path):
                        pkgs_by_name[pkg_name] = pkg
                        break
                    if not _is_hash_match(old_dist, old_pkg_paths, path):
                        logger.debug("Encountered path that does not match either version: %s", path)

    return pkgs_by_name


async def scan_prefix(
    prefix: Path | None = None,
    base_prefix: Path | None = None,
    progress: Progress | None = None,
    locations: List[Path] | None = None,
    site_pkgs_paths: Set[Path] | None = None,
) -> typing.List[PackageInfo]:
    # TODO: detect pre-releases and only set --pre flag for those packages (for conda)

    if not prefix:
        prefix = Path(sys.prefix).resolve()
    if not base_prefix:
        base_prefix = Path(sys.base_prefix).resolve()
    if not locations:
        # We need to use safe_path_resolve here because sys.path can contain
        # "" to represent the current working directory.
        locations = [resolved_path for p in sys.path if (resolved_path := safe_path_resolve(Path(p)))]
        try:
            cwd = Path.cwd().resolve()
            if cwd not in locations:
                locations.insert(0, cwd)
        # cwd was deleted
        except FileNotFoundError:
            logger.debug("Current working directory was deleted")
    if not site_pkgs_paths:
        site_pkgs_paths = {Path(p).resolve() for p in site.getsitepackages() + [site.getusersitepackages()]}
    conda_env_future = asyncio.create_task(scan_conda(prefix=prefix, progress=progress))
    # only pass locations to support testing, otherwise we should be using sys.path
    pip_env_future = asyncio.create_task(scan_pip(locations=locations, progress=progress))
    conda_env = await conda_env_future
    pip_env = await pip_env_future
    filtered_conda = {}
    # the pip list is the "truth" of what is imported for python deps
    for pypi_name, packages in conda_env.items():
        # if a package exists in the pip list but is not a conda place holder
        # then the conda package wont be imported and should be discarded
        found = False
        if pip_env.get(pypi_name):
            found = True
            pip_package = pip_env[pypi_name]
            if isinstance(pip_package, CondaPlaceHolder):
                del pip_env[pypi_name]
                # find the conda package that actually matches with what is importable
                importable_package = next(
                    (p for p in packages if p["path"]),
                    None,
                )
                if importable_package is None:
                    logger.warning("Could not find importable conda package for %s", pypi_name)
                else:
                    filtered_conda[pypi_name] = importable_package
            else:
                matching_package = next(
                    (
                        p
                        for p in packages
                        if normalize_version(p["version"]) == normalize_version(pip_package["version"])
                    ),
                    None,
                )
                if matching_package:
                    # if the versions match, we can fall back to using the conda version
                    del pip_env[pypi_name]
                    filtered_conda[pypi_name] = matching_package
        if not found:
            # a non python package and safe to include
            filtered_conda[pypi_name] = packages[0]
    # remove conda placeholders (there won't be any by here but this makes pyright happy)
    pip_env = {pkg_name: pkg for pkg_name, pkg in pip_env.items() if not isinstance(pkg, CondaPlaceHolder)}
    results = sorted(
        list(pip_env.values()) + list(filtered_conda.values()),
        key=lambda pkg: pkg["name"],
    )
    # get set of urls for all packages that were installed via pip
    pkg_urls = set()
    for pkg in results:
        if pkg["wheel_target"]:
            url = cast(str, pkg["wheel_target"])
            if "http://" in url or "https://" in url:
                url = re.sub(r"^(git|hg|svn|bzr)\+", "", url)
                url = re.sub(r"@\w+$", "", url)
                url = url.rstrip("/")
                pkg_urls.add(url)

    # Handle modules that are not installed via pip or conda
    pkg_paths = {pkg["path"].resolve() for pkg in results if pkg["path"]}
    extra_paths = (
        {
            p
            for p in locations
            if p not in (prefix, base_prefix) and prefix not in p.parents and base_prefix not in p.parents
        }
        - pkg_paths
        - site_pkgs_paths
    )
    for extra_path in extra_paths:
        if not extra_path.is_dir():
            continue
        if any(recurse_importable_python_files(extra_path)):
            # Skip directories that are the same as a package that was installed via pip
            git_dir = extra_path / ".git"
            if git_dir.exists():
                git_path = shutil.which("git") or "git"
                try:
                    encoding = get_encoding()
                    remote_output = subprocess.check_output(
                        [git_path, "remote", "-v"],
                        cwd=extra_path,
                        encoding=encoding,
                    )
                    remote_urls = set()
                    for line in remote_output.splitlines():
                        url = line.split()[1].strip()
                        if url.startswith("git@"):
                            url = "https://" + url[4:].replace(":", "/")
                        if url.endswith(".git"):
                            url = url[:-4]
                        url = url.rstrip("/")
                        remote_urls.add(url)

                except (subprocess.CalledProcessError, FileNotFoundError):
                    remote_urls = {}
                if pkg_urls.intersection(remote_urls):
                    continue

            results.append({
                "name": make_coiled_local_name(extra_path.name),
                "path": extra_path,
                "source": "pip",
                "version": "0.0.0",
                "channel_url": None,
                "channel": None,
                "subdir": None,
                "conda_name": None,
                "wheel_target": str(extra_path),
            })
    for pkg in results:
        if pkg["wheel_target"]:
            p = urlparse(pkg["wheel_target"])
            if len(p.scheme) <= 1 and not Path(pkg["wheel_target"]).exists():
                # lack of scheme (or it being a 1-char drive letter) means a local file
                # sometimes the wheel target taken from
                # direct_url.json references a file that does not exist
                # skip over trying to sync that and treat it like a normal package
                # this can happen in conda/system packages
                # where the package metadata was generated on a build system and not locally
                pkg["wheel_target"] = None
                pkg["path"] = None

    return sorted(results, key=lambda pkg: pkg["name"])
