import logging
import os
import re
import shlex
import sys

from python_agent.common.constants import WINDOWS
from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates
from python_agent.test_listener.executors.test_frameworks.agent_execution import (
    AgentExecution,
)

log = logging.getLogger(__name__)

# Robot's "invalid data or command line option" code. Reused for a refusal so
# a CI job that could not run Robot at all does not report success.
ROBOT_INVALID_INVOCATION = 252

# Listener API v3 gained start_keyword and end_keyword only in Robot Framework
# 7.0; on 6.x Robot assigns both to None and never calls them, reducing the C7
# coloring to start_test alone. The [robot] extra pins this floor, so a run
# below it means the pin was bypassed (a plain install, --no-deps, a
# constraints file, or a later downgrade) rather than a supported setup.
COLORING_MIN_ROBOT_VERSION = (7, 0)

SEALIGHTS_LISTENER_MODULE = "python_agent.test_listener.integrations.robot_helper"
SEALIGHTS_LISTENER = "%s.SealightsRobotListener" % SEALIGHTS_LISTENER_MODULE


def sealights_listener_already_registered(args):
    """True when a Sealights listener can already reach this run.

    Rule 20: a second registration duplicates every test event and reports no
    error anywhere. `ROBOT_OPTIONS` is the channel that causes it in practice,
    because pabot copies it into the worker argument file while the worker also
    re-applies it from the inherited environment.

    `posix=not WINDOWS`: POSIX-mode splitting treats backslash as an escape
    character, which mangles Windows listener paths (and can raise on a
    trailing backslash). A malformed `ROBOT_OPTIONS` must still not abort the
    customer's run (SPEC §Never), so a split failure is swallowed and the
    check falls back to `args` alone.
    """
    robot_options = os.environ.get("ROBOT_OPTIONS", "")
    try:
        option_candidates = shlex.split(robot_options, posix=not WINDOWS)
    except ValueError:
        log.warning("Could not parse ROBOT_OPTIONS %r; ignoring it for the duplicate-listener check." % robot_options)
        option_candidates = []
    candidates = list(args) + option_candidates
    return any(SEALIGHTS_LISTENER_MODULE in str(candidate) for candidate in candidates)


def resolve_robot_run_cli():
    """Return Robot Framework's ``run_cli``, or None when it is not installed.

    Never trust ``ImportError`` here. Run from a checkout of this repository,
    the name ``robot`` resolves to the repository's own ``robot/`` directory as
    a namespace package (``__file__`` is None), so ``import robot`` succeeds
    whether or not Robot Framework is installed and the real failure would
    surface later as ``AttributeError: module 'robot' has no attribute
    'run_cli'``. Probe for the attribute instead.
    """
    try:
        import robot
    except ImportError:
        return None
    return getattr(robot, "run_cli", None)


def resolve_robot_version():
    """Robot Framework's version string, or None when it cannot be read.

    Probed like ``run_cli`` above: inside a checkout of this repository the name
    ``robot`` resolves to a directory, so the attribute rather than the import is
    what tells the two apart.
    """
    try:
        import robot
    except ImportError:
        return None
    return getattr(getattr(robot, "version", None), "VERSION", None)


def coloring_is_degraded(version):
    """True when this Robot Framework never calls the hooks C7 needs.

    Unreadable and unparseable versions answer False. A wrong warning about a
    version that is in fact supported would send a customer chasing an upgrade
    they do not need, and the pin already covers the case this guards.
    """
    numbers = re.findall(r"\d+", version or "")
    if not numbers:
        return False
    parsed = tuple(int(number) for number in numbers[:2])
    if len(parsed) == 1:
        parsed += (0,)
    return parsed < COLORING_MIN_ROBOT_VERSION


def warn_if_coloring_is_degraded():
    """Say so, once, when the Robot in play silently cannot colour properly.

    A console message rather than a log record because the agent's default log
    level is ERROR, which would leave a warning unread; not `log.error`, because
    nothing here is fatal and the run is worth continuing. Never raises, and
    never changes the outcome of the run.
    """
    version = resolve_robot_version()
    if not coloring_is_degraded(version):
        return
    ConsoleMessageTemplates.render_and_print(
        "common.test-listener.robot-version-degrades-coloring",
        version=version,
        minVersion="%d.%d" % COLORING_MIN_ROBOT_VERSION,
    )
    log.warning(
        "Robot Framework %s is older than %d.%d, so per-keyword listener hooks "
        "are never called and browser coverage is limited to what exists at "
        "the start of each test."
        % (version, COLORING_MIN_ROBOT_VERSION[0], COLORING_MIN_ROBOT_VERSION[1])
    )


class RobotAgentExecution(AgentExecution):
    def __init__(self, config_data, labid, test_stage, test_group_id, args):
        # Contract C11: a Robot process collects no in-process Python
        # coverage, so it must not pay the BuildMapper scan or start the
        # coverage.py tracer. Set before the base constructor, which is what
        # builds the AgentManager.
        config_data.skipFootprintsPipeline = True
        self.args = args
        self.is_sealights_agent_ready = False
        try:
            super(RobotAgentExecution, self).__init__(
                config_data,
                labid,
                test_stage,
                test_group_id=test_group_id,
            )
            self.is_sealights_agent_ready = not config_data.get_is_disabled()
        except Exception as e:
            # A Sealights failure must never abort the customer's Robot run
            # (SPEC §Never). Agent construction reaches the backend, so this
            # catch is what keeps an unreachable server from turning into a
            # traceback instead of a test report.
            log.error("Failed initializing AgentExecution. Error: %s" % str(e))

    def build_robot_args(self):
        """The customer's argument list, with the listener registered ahead of it.

        The listener option goes **first**, not last: Robot treats everything
        after the first data path as another data path, so a trailing
        `--listener X` fails the run with "File or directory to execute does not
        exist" rather than registering anything.
        """
        args = list(self.args)
        if not self.is_sealights_agent_ready:
            # Rule 15, AC18: unusable configuration disables Sealights and
            # Robot still runs and still reports its own results. Registering
            # the listener anyway would only produce per-hook errors.
            log.warning("Sealights agent is disabled")
            return args
        if sealights_listener_already_registered(args):
            log.warning(
                "A Sealights listener is already registered through ROBOT_OPTIONS "
                "or the Robot arguments, so a second one was not added. Two "
                "registrations report every test twice."
            )
            return args
        return ["--listener", SEALIGHTS_LISTENER] + args

    def execute(self):
        ConsoleMessageTemplates.render_and_print(
            "common.test-listener.test-framework-detected",
            testFramework="robot",
        )
        run_cli = resolve_robot_run_cli()
        if run_cli is None:
            log.error(
                "Robot Framework is not installed, so 'sl-python robot' cannot "
                "run. Install it with: pip install 'sealights-python-agent[robot]' "
                "(Robot Framework 7.0 or newer is required)."
            )
            sys.exit(ROBOT_INVALID_INVOCATION)
        warn_if_coloring_is_degraded()
        # exit=False returns Robot's code instead of terminating, but Robot's
        # argument parser still raises SystemExit before that flag is
        # consulted (--help, --version, an empty argument list, any
        # unrecognized option). Let it propagate.
        return_code = run_cli(self.build_robot_args(), exit=False)
        # Terminating with Robot's own code is the contract (Rule 17): merely
        # returning it from the Click callback yields exit 0 and a success
        # banner over a failed run.
        sys.exit(return_code)
