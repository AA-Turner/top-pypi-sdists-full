import contextlib
import functools
import os
import pathlib
import warnings

from . import resolve
from ._functools import apply, bypass_when, result_invoke


@bypass_when(os.environ.get('COHERENT_LICENSED_UNUSED_ACTION', 'warn') == 'ignore')
def warn_if_false(enabled):
    enabled or warnings.warn(
        "Avoid installing this plugin for projects that don't depend on it."
    )


def dist_root(dist):
    return pathlib.Path(dist.src_root or '')


@result_invoke(warn_if_false)
@apply(bool)
def enabled(dist):
    root = dist_root(dist)
    with contextlib.suppress(FileNotFoundError):
        project = root.joinpath('pyproject.toml').read_text(encoding='utf-8')
        return 'coherent.licensed' in project


def _finalize_license_files(dist, orig):
    """
    Resolve the license expression into a license file.
    """
    if not enabled(dist):
        return orig()
    license = dist_root(dist) / 'LICENSE'
    dist.metadata.license_files = [str(license)]
    if license.exists():
        return
    license.write_text(resolve(dist.metadata.license_expression))


def inject(dist):
    """
    Patch the dist to resolve the license expression.

    This hook is called before `dist.parse_config_files` has been called, so
    the license expression has not been loaded yet, so patch _finalize_license_files
    to write out the license after expressions are loaded.
    """
    dist._finalize_license_files = functools.partial(
        _finalize_license_files, dist, orig=dist._finalize_license_files
    )
