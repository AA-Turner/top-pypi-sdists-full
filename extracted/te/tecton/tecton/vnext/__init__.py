from tecton._internals.find_spark import find_spark as __find_spark


__initializing__ = True


__find_spark()

# ruff: noqa: F401 E402
from tecton import version as __version_lib
from tecton.vnext.iceberg_config import IcebergConfig
from tecton.vnext.sink_config import PublishFeaturesConfig
from tecton.vnext.sink_config import sink_config


__version__ = __version_lib.get_version()
__initializing__ = False
