from importlib.metadata import PackageNotFoundError

from abstra_internals.utils import packages as pkg_utils


def version() -> None:
    try:
        print(pkg_utils.get_local_package_version())
    except PackageNotFoundError:
        print("0.0.0 (abstra not installed; running from source)")
