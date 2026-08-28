import json
import logging
import os

from python_agent.common import constants
from python_agent.test_listener.executors.test_frameworks.agent_execution import (
    AgentExecution,
)

log = logging.getLogger(__name__)


class Run(AgentExecution):
    def __init__(self, config_data, labid, cov_report, per_test, interval):
        super(Run, self).__init__(
            config_data,
            labid,
            cov_report=cov_report,
            per_test=per_test,
            interval=interval,
            init_agent=False,
        )

    def execute(self, args):
        try:
            log.info("Running program: %s" % " ".join(args))
            self.inject_bootstrap_dir_to_python_path()
            program_exe_path = self.find_program_exe_path(args)
            if not program_exe_path:
                log.warning("No program was found to run")
                return
            self.save_config_as_env_variable()
            self.run_program(program_exe_path, args)
        except Exception as e:
            log.error("Error running program: %s" % str(e))

    def inject_bootstrap_dir_to_python_path(self):
        from python_agent import __file__ as root_directory

        root_directory = os.path.dirname(root_directory)
        boot_directory = os.path.join(root_directory, "bootstrap")

        # Keep bootstrap first exactly once. The previous "not in path" guard
        # skipped the rebuild when bootstrap was already present (container-wide
        # PYTHONPATH injection, SLDEV-28572), which wiped every other entry.
        existing = []
        if "PYTHONPATH" in os.environ:
            existing = [
                entry
                for entry in os.environ["PYTHONPATH"].split(os.path.pathsep)
                if entry and entry != boot_directory
            ]
        os.environ["PYTHONPATH"] = os.path.pathsep.join([boot_directory] + existing)

    def find_program_exe_path(self, args):
        if not args:
            return None
        program_exe_path = args[0]
        if not os.path.dirname(program_exe_path):
            program_search_path = os.environ.get("PATH", "").split(os.path.pathsep)
            for path in program_search_path:
                path = os.path.join(path, program_exe_path)
                if os.path.exists(path) and os.access(path, os.X_OK):
                    program_exe_path = path
                    break
        self.config_data.program = program_exe_path
        return program_exe_path

    def run_program(self, program_exe_path, args):
        os.execl(program_exe_path, *(list(args)))

    def save_config_as_env_variable(self):
        os.environ[constants.CONFIG_ENV_VARIABLE] = json.dumps(
            self.config_data,
            default=lambda m: m.__dict__ if hasattr(m, "__dict__") else str(m),
        )
