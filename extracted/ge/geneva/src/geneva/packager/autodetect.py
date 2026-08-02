# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# a module for automatically inspecting path and capturing the local env

import contextlib
import logging
import shutil
import site
import tempfile
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import emoji

from geneva.packager.uploader import Uploader
from geneva.packager.zip import _DEFAULT_IGNORES, WorkspaceZipper
from geneva.tqdm import tqdm

_LOG = logging.getLogger(__name__)


def _maybe_pyproject() -> Path | None:
    """
    Inspect the current working directory and return the path to the
    source root if it's in a python project.
    """

    # don't resolve because we could be inside a link
    cwd = Path.cwd().absolute()
    assert cwd.root == "/", "cwd is not absolute"

    root = Path("/")
    cur = cwd

    while not list(cur.glob("pyproject.toml")) and (cur := cur.parent) != root:
        ...

    # TODO: use the packaging tool configured in pyproject.toml
    # to determine the source root
    if list(cur.glob("pyproject.toml")):
        return cur / "src"

    return None


def _maybe_src() -> Path | None:
    """
    Inspect the current working directory and return the path to the
    source root if it's in a python project.
    """

    # don't resolve because we could be inside a link
    cwd = Path.cwd().absolute()
    assert cwd.root == "/", "cwd is not absolute"

    root = Path("/")
    cur = cwd

    while not list(cur.glob("src")) and (cur := cur.parent) != root:
        ...

    if list(cur.glob("src")):
        return cur / "src"

    return None


def _maybe_python_repo() -> Path | None:
    """
    Inspect the current working directory and return the path to the
    source root if it's in a python project.
    """

    return _maybe_pyproject() or _maybe_src()


def _find_workspace() -> Path:
    """
    Inspect the current working directory and return the path to the
    source root if it's in a python project. If we can not find a
    python source root, return the current working directory.
    """

    return _maybe_python_repo() or Path.cwd()


def get_paths_to_package(
    *,
    skip_site_packages: bool,
) -> list[Path]:
    """
    Inspect the current working directory and return the path to the
    source root if it's in a python project. If we can not find a
    python source root, return the current working directory.
    """

    paths = sorted(
        {
            Path(p).resolve().absolute()
            for p in [
                _find_workspace(),
                Path.cwd(),
                *(site.getsitepackages() if not skip_site_packages else []),
            ]
        }
    )

    _LOG.info("found paths to package: %s", paths)

    return paths


def package_local_env_into_zips(
    output_dir: Path | str,
    *,
    skip_site_packages: bool = False,
    create_zips=True,
    exclude_files: list[Path] | None = None,
) -> list[list[Path]]:
    """
    Package the local environment into zip files.

    return a list of the paths to the zip files.
    """

    paths = get_paths_to_package(skip_site_packages=skip_site_packages)

    zips = []

    for p in paths:
        if not p.exists():
            _LOG.warning("path %s does not exist", p)
            continue

        if not p.is_dir():
            _LOG.warning("path %s is not a directory", p)
            continue

        _LOG.info("packaging %s", p)

        ignores = _DEFAULT_IGNORES.copy()
        if skip_site_packages:
            ignores.append(".*/site-packages/.*")
        zip_path, _ = WorkspaceZipper(p, output_dir, ignore_regexs=ignores).zip(
            create_zips=create_zips, excludes=exclude_files
        )

        if len(zip_path) > 0:
            zips.append(zip_path)

    # Claim newly zipped files and previous zipped + shipped files
    zips.append(exclude_files or [])
    return zips


@contextlib.contextmanager
def _or_tempdir(
    zip_output_dir: Path | str | None = None,
    delete: bool = False,
) -> Generator[Path, None, None]:
    """
    Get the output directory for the zip files. If None, a temporary
    directory will be used. If a path is provided, it will be used as the
    output directory.

    Parameters
    ----------
        delete
            If True, the temporary directory will be deleted after the
            context manager is exited. If False, the directory will be kept.
    """
    # no path provided, use a temporary directory
    if zip_output_dir is None:
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    else:
        try:
            path = Path(zip_output_dir)
            yield path
        finally:
            # delete the directory if requested
            if delete:
                try:
                    shutil.rmtree(path.as_posix())
                except Exception as e:
                    _LOG.warning("failed to delete %s: %s", path, e)


@contextlib.contextmanager
def upload_local_env(
    *,
    zip_output_dir: Path | str | None = None,
    uploader: Uploader | None = None,
    delete_local_zips=False,
    skip_site_packages: bool = False,
) -> Generator[list[list[str]], None, None]:
    """
    A context manager that packages the local environment into zip files and
    upload them to the specified uploader.

    Parameters
    ----------
        zip_output_dir
            The directory to store the zip files in. If None, a
            temporary directory will be used. If a path is provided, it will
            be used as the output directory.
        uploader
            The uploader to use. If None, the default uploader will be
            used.
        delete_local_zips
            If True, the zip files will be deleted after the
            upload is complete. If False, the zip files will be kept in the
            output directory. DOES NOT delete the uploaded zips.
        skip_site_packages
            If True, the site packages will be skipped when
            packaging the local environment. This is useful if you want to
            package only the source code and not the dependencies, assuming
            that the dependencies are already installed in the docker image
    """
    with _or_tempdir(zip_output_dir, delete=delete_local_zips) as zip_output_dir:
        # get the names of the files to generate
        zip_paths = package_local_env_into_zips(
            zip_output_dir, skip_site_packages=skip_site_packages, create_zips=False
        )

        try:
            # NOTE: uploader=None on a namespace/remote connection cannot be
            # resolved here. _set_upload_dir() intentionally skips global
            # config for those connections, expecting a Connection-aware
            # Uploader to be passed in instead. The ad-hoc (no-manifest)
            # cluster-bootstrap path doesn't pass one yet, so a vending-off
            # namespace connection that bootstraps a cluster without a manifest
            # lands here and fails. Follow-up: build a lazy Connection-scoped
            # Uploader for that path. The standard define_manifest() + backfill
            # flow is unaffected (it takes the manifest branch in ray_cluster).
            uploader = uploader or Uploader.get()
        except (TypeError, ValueError) as e:
            raise ValueError(
                "Geneva was not initialized. Create the cluster through "
                "`geneva.connect(...).context(...)` or pass an uploader derived from "
                "a Geneva connection before packaging the local environment."
            ) from e

        _LOG.info(f"Using uploader: {uploader}")

        # Find which files have been uploaded already
        exclude_files = []
        for zip_path in zip_paths:
            if all(uploader._file_exists(f) for f in zip_path):
                # TODO maybe its a partial upload and we should check size too?
                _LOG.debug(
                    f"File {zip_path} already exists in {uploader.upload_dir}, skipping"
                    " zipping and upload"
                )
                exclude_files.extend(zip_path)

        _LOG.debug(f"excluding files: {exclude_files}")
        # package the local environment into zip files and ship them.
        zips = package_local_env_into_zips(
            zip_output_dir,
            skip_site_packages=skip_site_packages,
            exclude_files=exclude_files,
        )
        sizes = []
        with ThreadPoolExecutor(max_workers=8) as executor:
            res = []
            for zip_paths in zips:
                res.append([])
                _LOG.info(f"Uploading {len(zip_paths)} zip files")
                _LOG.debug(f"zip paths: {zip_paths}")
                for zip_path in zip_paths:
                    fut = executor.submit(
                        uploader.upload,
                        zip_path,
                    )
                    try:
                        sizes.append(zip_path.stat().st_size)
                    except FileNotFoundError:
                        sizes.append(0)  # needed by loop below
                        _LOG.debug(
                            f"skipping file {zip_path}, does not exist, assuming"
                            " uploaded previously"
                        )
                    res[-1].append(fut)

            with tqdm(
                total=sum(sizes),
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                smoothing=0,
            ) as pbar:
                pbar.set_description(emoji.emojize(":rocket: uploading zips"))
                for i in range(len(res)):
                    uploaded_uris = []
                    for p in as_completed(res[i]):
                        pbar.update(sizes.pop(0))
                        uploaded_uris.append(p.result())
                    res[i] = uploaded_uris
                _LOG.info(
                    f"Uploaded {len(res)} zip path file sets to {uploader.upload_dir}"
                )
                _LOG.debug(res)

        yield res
