import os
import sys
import traceback

import importlib.util
import importlib
import importlib.machinery

from python_agent.common.configuration_manager import ConfigurationManager
from python_agent.test_listener.executors.test_frameworks.agent_execution import (
    AgentExecution,
)

boot_directory = os.path.dirname(__file__)
root_directory = os.path.dirname(os.path.dirname(boot_directory))

path = list(sys.path)

if boot_directory in path:
    del path[path.index(boot_directory)]

try:
    # Search for sitecustomize.py in the specified paths (excluding current directory)
    for search_path in path:
        try:
            spec = importlib.machinery.PathFinder.find_spec(
                "sitecustomize", [search_path]
            )
            if spec is not None and spec.origin and spec.origin != __file__:
                # Found a different sitecustomize module, load it
                module = importlib.util.module_from_spec(spec)
                sys.modules["sitecustomize"] = module
                spec.loader.exec_module(module)
                break
        except (ImportError, AttributeError, TypeError):
            continue
except ImportError:
    pass

if root_directory not in sys.path:
    sys.path.insert(0, root_directory)

try:
    cm = ConfigurationManager()
    cm.try_load_configuration_from_config_environment_variable()
    cm.init_features()

    if os.getenv("IS_MAIN_PROCESS") == "1":
        os.environ["IS_MAIN_PROCESS"] = "0"
        AgentExecution(
            cm.config_data, cm.config_data.labId, cov_report=cm.config_data.covReport
        )
except SystemExit as e:
    if getattr(e, "code", 1) != 0:
        sys.exit(4)
except BaseException as e:
    result = {
        "PYTHONPATH": os.environ.get("PYTHONPATH"),
        "error": str(e),
        "traceback": traceback.format_exc(),
    }
    sys.exit(result)
