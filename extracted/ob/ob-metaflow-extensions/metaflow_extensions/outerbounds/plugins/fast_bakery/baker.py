import threading
import time
import sys
from typing import Dict, Optional, Any, Callable
from functools import partial
from metaflow.exception import MetaflowException
from metaflow.metaflow_config import FAST_BAKERY_URL

from .fast_bakery import FastBakery, FastBakeryApiResponse, FastBakeryException
from .docker_environment import cache_request

BAKERY_METAFILE = ".imagebakery-cache"


class BakerException(MetaflowException):
    headline = "Ran into an error while baking image"

    def __init__(self, msg):
        super(BakerException, self).__init__(msg)


def bake_image(
    cache_file_path: str,
    ref: Optional[str] = None,
    python: Optional[str] = None,
    pypi_packages: Optional[Dict[str, str]] = None,
    conda_packages: Optional[Dict[str, str]] = None,
    base_image: Optional[str] = None,
    logger: Optional[Callable[[str], Any]] = None,
) -> FastBakeryApiResponse:
    """
    Bakes a Docker image with the specified dependencies.

    Args:
        cache_file_path: Path to the cache file
        ref: Reference identifier for this bake (for logging purposes)
        python: Python version to use
        pypi_packages: Dictionary of PyPI packages and versions
        conda_packages: Dictionary of Conda packages and versions
        base_image: Base Docker image to use
        logger: Optional logger function to output progress

    Returns:
        FastBakeryApiResponse: The response from the bakery service

    Raises:
        BakerException: If the baking process fails
    """
    # Default logger if none provided
    if logger is None:
        logger = partial(print, file=sys.stderr)

    # Thread lock for logging
    logger_lock = threading.Lock()
    images_baked = 0

    @cache_request(cache_file_path)
    def _cached_bake(
        ref=None,
        python=None,
        pypi_packages=None,
        conda_packages=None,
        base_image=None,
    ):
        try:
            bakery = FastBakery(url=FAST_BAKERY_URL)
            bakery._reset_payload()
            bakery.python_version(python)
            bakery.pypi_packages(pypi_packages)
            bakery.conda_packages(conda_packages)
            bakery.base_image(base_image)
            # bakery.ignore_cache()

            with logger_lock:
                logger(f"🍳 Baking [{ref}] ...")
                logger(f"     🐍 Python: {python}")

                if pypi_packages:
                    logger(f"     📦 PyPI packages:")
                    for package, version in pypi_packages.items():
                        logger(f"        🔧 {package}: {version}")

                if conda_packages:
                    logger(f"     📦 Conda packages:")
                    for package, version in conda_packages.items():
                        logger(f"        🔧 {package}: {version}")

                logger(f"     🏗️  Base image: {base_image}")

            start_time = time.time()
            res = bakery.bake()
            # TODO: Get actual bake time from bakery
            bake_time = time.time() - start_time

            with logger_lock:
                logger(f"🏁 Baked [{ref}] in {bake_time:.2f} seconds!")
            nonlocal images_baked
            images_baked += 1
            return res
        except FastBakeryException as ex:
            raise BakerException(f"Bake [{ref}] failed: {str(ex)}")

    # Call the cached bake function with the provided parameters
    return _cached_bake(
        ref=ref,
        python=python,
        pypi_packages=pypi_packages,
        conda_packages=conda_packages,
        base_image=base_image,
    )
