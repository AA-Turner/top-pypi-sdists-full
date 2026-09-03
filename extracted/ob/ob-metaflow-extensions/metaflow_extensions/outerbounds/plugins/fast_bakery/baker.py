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
    fast_bakery_url: Optional[str] = None,
    channels: Optional[list] = None,
    extra_configs: Optional[Dict[str, str]] = None,
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
        fast_bakery_url: Optional FB URL
        channels: Optional list of conda channels to use
        extra_configs: Optional dictionary of extra configuration values passed
            through to the bakery

    Returns:
        FastBakeryApiResponse: The response from the bakery service

    Raises:
        BakerException: If the baking process fails
    """
    # Default logger if none provided
    if logger is None:
        logger = partial(print, file=sys.stderr)

    if all([fast_bakery_url is None and FAST_BAKERY_URL is None]):
        raise BakerException(
            "Image Bakery endpoint missing. METAFLOW_FAST_BAKERY_URL environment/configuration variable not found."
        )

    fast_bakery_url = fast_bakery_url or FAST_BAKERY_URL

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
        channels=None,
        extra_configs=None,
    ):
        try:
            bakery = FastBakery(url=fast_bakery_url)
            bakery._reset_payload()
            bakery.python_version(python)
            bakery.pypi_packages(pypi_packages)
            bakery.conda_packages(conda_packages)
            if channels:
                bakery.default_conda_channel(channels[0])
                bakery.conda_channels(channels)
            bakery.base_image(base_image)
            bakery.extra_configs(extra_configs)
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

                if extra_configs:
                    logger(f"     🧩 Extra configs will be used")
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

    # Call the cached bake function with the provided parameters.
    # `extra_configs` is only passed when set, so that cache keys for callers
    # that do not use it remain unchanged.
    extra_kwargs = {"extra_configs": extra_configs} if extra_configs else {}
    return _cached_bake(
        ref=ref,
        python=python,
        pypi_packages=pypi_packages,
        conda_packages=conda_packages,
        base_image=base_image,
        channels=channels,
        **extra_kwargs,
    )
