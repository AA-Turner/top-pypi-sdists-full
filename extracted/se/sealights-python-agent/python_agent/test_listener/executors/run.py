import datetime
import json
import logging
import os

from python_agent.common import constants
from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates

log = logging.getLogger(__name__)


class Run(object):
    def __init__(self, config_data):
        self.config_data = config_data
        os.environ["IS_MAIN_PROCESS"] = "1"

    def execute(self, args):
        try:
            log.info("Running program: %s" % " ".join(args))
            ConsoleMessageTemplates.render_and_print(
                "common.general.command-line-executed",
                parameters=" ".join(args),
            )
            self.inject_bootstrap_dir_to_python_path()
            program_exe_path = self.find_program_exe_path(args)
            if not program_exe_path:
                log.warning("No program was found to run")
                return
            self.save_config_as_env_variable()
            self.run_program(program_exe_path, args)
        except Exception as e:
            log.error("Error running program: %s" % str(e))
            ConsoleMessageTemplates.render_and_print(
                "common.general.agent-ended-error",
                command="run",
                dateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

    def inject_bootstrap_dir_to_python_path(self):
        from python_agent import __file__ as root_directory

        root_directory = os.path.dirname(root_directory)
        boot_directory = os.path.join(root_directory, "bootstrap")

        python_path = boot_directory

        if "PYTHONPATH" in os.environ:
            path = os.environ["PYTHONPATH"].split(os.path.pathsep)
            if boot_directory not in path:
                python_path = "%s%s%s" % (
                    boot_directory,
                    os.path.pathsep,
                    os.environ["PYTHONPATH"],
                )

        os.environ["PYTHONPATH"] = python_path

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
