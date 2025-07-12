######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.534535                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import typing
    import metaflow.mf_extensions.outerbounds.plugins.fast_bakery.fast_bakery
    import metaflow.exception

from .....exception import MetaflowException as MetaflowException
from .fast_bakery import FastBakery as FastBakery
from .fast_bakery import FastBakeryApiResponse as FastBakeryApiResponse
from .fast_bakery import FastBakeryException as FastBakeryException
from .docker_environment import cache_request as cache_request

FAST_BAKERY_URL: None

BAKERY_METAFILE: str

class BakerException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

def bake_image(cache_file_path: str, ref: typing.Optional[str] = None, python: typing.Optional[str] = None, pypi_packages: typing.Optional[typing.Dict[str, str]] = None, conda_packages: typing.Optional[typing.Dict[str, str]] = None, base_image: typing.Optional[str] = None, logger: typing.Optional[typing.Callable[[str], typing.Any]] = None) -> metaflow.mf_extensions.outerbounds.plugins.fast_bakery.fast_bakery.FastBakeryApiResponse:
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
    ...

