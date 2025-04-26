import sys

import distributed
from importlib_metadata import version
from packaging.version import Version

COILED_VERSION = version("coiled")

PY_VERSION = Version(".".join(map(str, sys.version_info[:3])))

DISTRIBUTED_VERSION = Version(distributed.__version__)


def register_plugin(client, plugin, **kwargs):
    if DISTRIBUTED_VERSION >= Version("2023.9.2"):
        return client.register_plugin(plugin, **kwargs)
    elif isinstance(plugin, distributed.SchedulerPlugin):
        return client.register_scheduler_plugin(plugin, **kwargs)
    elif isinstance(plugin, (distributed.WorkerPlugin, distributed.NannyPlugin)):
        return client.register_worker_plugin(plugin, **kwargs)
    else:
        raise TypeError(f"Invalid plugin type {type(plugin)}")
