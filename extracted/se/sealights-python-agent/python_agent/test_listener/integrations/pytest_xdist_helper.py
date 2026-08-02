import logging
import importlib

from python_agent.common import constants

log = logging.getLogger(__name__)


def override_xdist_exit_timeout():
    try_load_and_set_timeout("workermanage") or try_load_and_set_timeout("slavemanage")


def try_load_and_set_timeout(module_name):
    try:
        module = importlib.import_module("xdist.%s" % module_name)
        module.NodeManager.EXIT_TIMEOUT = constants.XDIST_EXIT_TIMEOUT_IN_SECONDS
        log.info(
            "Overridden xdist exit timeout to = %s"
            % constants.XDIST_EXIT_TIMEOUT_IN_SECONDS
        )
        return True
    except ImportError:
        return False
    except Exception as e:
        log.error(
            "Failed overriding xdist exit timeout to = %s. Error=%s"
            % (constants.XDIST_EXIT_TIMEOUT_IN_SECONDS, str(e))
        )
        return False
