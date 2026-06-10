######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.33.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-06-09T20:21:00.266851                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import typing
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.dependencies
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.app_config

from .app_config import AppConfig as AppConfig
from .utils import TODOException as TODOException
from ......metaflow_config import get_pinned_conda_libs as get_pinned_conda_libs

DEFAULT_DATASTORE: str

KUBERNETES_CONTAINER_IMAGE: None

class BakingStatus(tuple, metaclass=type):
    """
    BakingStatus(image_should_be_baked, python_path, resolved_image)
    """
    @staticmethod
    def __new__(_cls, image_should_be_baked, python_path, resolved_image):
        """
        Create new instance of BakingStatus(image_should_be_baked, python_path, resolved_image)
        """
        ...
    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...
    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...
    ...

class ImageBakingException(Exception, metaclass=type):
    ...

def bake_deployment_image(app_config: metaflow.mf_extensions.outerbounds.plugins.apps.core.app_config.AppConfig, cache_file_path: str, logger: typing.Union[typing.Callable[[str], typing.Any], None] = None) -> BakingStatus:
    ...

