"""`sl-python pabot`: the parent process, and nothing more.

The parent resolves configuration once, publishes it as `sl_configuration`,
registers the listener, and hands the rest to pabot. It opens **no** execution
and closes none: each worker is a bare `robot` process that owns exactly one
execution and behaves as a serial run (contract C9). The worker side of that
lives in the listener, not here.

Four traps, each with a failure mode that reads as something else:

1. `pabot.pabot.main` is `sys.exit(main_program(args))`, so it terminates this
   process before the return code can be propagated. `main_program` is the entry
   point that returns.
2. `main_program` falls back to `sys.argv[1:]` when handed a falsy argument
   list, which here is the agent's own command line.
3. pabot forwards options it does not recognize to Robot's parser, which rejects
   them with 252 and a normalized name that does not match what the customer
   typed. Every Sealights option is consumed by Click before this point.
4. pabot spawns workers as the bare command `robot` from `PATH`, not through
   `sys.executable`. Without the pre-flight below, every worker dies with
   `FileNotFoundError`, pabot exits 252 having run no tests, and the stderr files
   it tells the customer to read are empty.
"""

import json
import logging
import os
import shutil
import sys

from python_agent.common import constants
from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates
from python_agent.test_listener.executors.test_frameworks.agent_execution import (
    AgentExecution,
)
from python_agent.test_listener.executors.test_frameworks.robot_execution import (
    ROBOT_INVALID_INVOCATION,
    SEALIGHTS_LISTENER,
    sealights_listener_already_registered,
    warn_if_coloring_is_degraded,
)

log = logging.getLogger(__name__)

WORKER_COMMAND = "robot"


def resolve_pabot_main_program():
    """Return pabot's `main_program`, or None when pabot is not installed.

    The attribute is probed rather than trusting `ImportError`, for the reason
    `robot_execution.resolve_robot_run_cli` documents: inside a checkout of this
    repository a directory can satisfy the import as a namespace package.
    """
    try:
        import pabot.pabot
    except ImportError:
        return None
    return getattr(pabot.pabot, "main_program", None)


class PabotAgentExecution(AgentExecution):
    def __init__(self, config_data, labid, test_stage, test_group_id, args):
        # Contract C11, as for `robot`: no in-process Python coverage here, so
        # no BuildMapper scan and no coverage.py tracer. Set before the base
        # constructor, which is what builds the AgentManager.
        config_data.skipFootprintsPipeline = True
        self.args = args
        self.is_sealights_agent_ready = False
        try:
            super(PabotAgentExecution, self).__init__(
                config_data,
                labid,
                test_stage,
                test_group_id=test_group_id,
            )
            self.is_sealights_agent_ready = not config_data.get_is_disabled()
        except Exception as e:
            # A Sealights failure must never abort the customer's run
            # (SPEC §Never).
            log.error("Failed initializing AgentExecution. Error: %s" % str(e))

    def publish_configuration(self):
        """Hand the resolved configuration to the workers through the environment.

        This is the only channel: a worker is a bare `robot` process with no
        Sealights arguments, and it is what lets the whole run resolve
        configuration and the build session **once**, in this process (AC42).
        """
        os.environ[constants.CONFIG_ENV_VARIABLE] = json.dumps(
            self.config_data,
            default=lambda m: m.__dict__ if hasattr(m, "__dict__") else str(m),
        )

    def build_pabot_args(self):
        """The customer's argument list with the listener registered ahead of it.

        First, not last: Robot treats everything after the first data path as
        another data path, and pabot passes these through to Robot.
        """
        args = list(self.args)
        if not self.is_sealights_agent_ready:
            # Rule 15, AC18: unusable configuration disables Sealights and the
            # customer's run still executes and still reports its own results.
            log.warning("Sealights agent is disabled")
            return args
        if sealights_listener_already_registered(args):
            # Rule 20, AC28. The pabot shape of this is specific: pabot copies
            # ROBOT_OPTIONS into the worker argument file, and the worker also
            # re-applies ROBOT_OPTIONS from the inherited environment, so one
            # registration there arrives twice.
            log.warning(
                "A Sealights listener is already registered through ROBOT_OPTIONS "
                "or the pabot arguments, so a second one was not added. Two "
                "registrations report every test twice."
            )
            return args
        return ["--listener", SEALIGHTS_LISTENER] + args

    def execute(self):
        ConsoleMessageTemplates.render_and_print(
            "common.test-listener.test-framework-detected",
            testFramework="pabot",
        )
        main_program = resolve_pabot_main_program()
        if main_program is None:
            log.error(
                "pabot is not installed, so 'sl-python pabot' cannot run. "
                "Install it with: pip install robotframework-pabot"
            )
            sys.exit(ROBOT_INVALID_INVOCATION)
        if shutil.which(WORKER_COMMAND) is None:
            log.error(
                "The 'robot' command is not on PATH, and pabot starts every "
                "worker by running it. Install Robot Framework into the "
                "environment on PATH, or add that environment's scripts "
                "directory to PATH, then run 'sl-python pabot' again."
            )
            sys.exit(ROBOT_INVALID_INVOCATION)
        # Warned here rather than in the listener so a --processes 8 run says it
        # once instead of eight times. This reads the version this process
        # imports, which is the same distribution the workers load unless the
        # `robot` on PATH belongs to a different environment entirely.
        warn_if_coloring_is_degraded()
        args = self.build_pabot_args()
        if not args:
            # Trap 2. Bare `pabot` with no arguments refuses with 252 as well, so
            # this matches what the customer would have seen without the agent.
            log.error(
                "No arguments were given to 'sl-python pabot', so there is "
                "nothing to run. Pass the suites to execute, as you would to "
                "pabot itself."
            )
            sys.exit(ROBOT_INVALID_INVOCATION)
        if self.is_sealights_agent_ready:
            self.publish_configuration()
        # Terminating with pabot's own code is the contract (Rule 17, AC37):
        # returning it from the Click callback yields exit 0 and a success banner
        # over a failed run.
        sys.exit(main_program(args))
