import datetime
import functools
import logging
import os
import sys

import requests

from python_agent import __legacy_mode__ as is_legacy_mode
from python_agent import __version__ as AGENT_VERSION
from python_agent.build_scanner.executors.build import Build
from python_agent.build_scanner.executors.config import Config
from python_agent.build_scanner.executors.pr_config import PrConfig
from python_agent.common import constants
from python_agent.common.config_data import ConfigData, ScmConfigArgs
from python_agent.common.configuration_manager import ConfigurationManager
from python_agent.common.constants import DEFAULT_WORKSPACEPATH
from python_agent.common.constants import (
    TOKEN_FILE,
    BUILD_SESSION_ID_FILE,
    TEST_RECOMMENDATION,
    DEFAULT_BRANCH_NAME,
)
from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates
from python_agent.packages import click
from python_agent.packages.coverage.cmdline import Opts, unshell_list
from python_agent.serverless.serverless import Serverless
from python_agent.test_listener.executors.end_execution import EndAnonymousExecution
from python_agent import __version__


if is_legacy_mode:
    from python_agent.test_listener.executors.run_legacy import Run
    from python_agent.test_listener.executors.send_footprints_legacy import (
        SendFootprintsAnonymousExecution,
    )

    CONTEXT_SETTINGS = dict(
        token_normalize_func=lambda x: x.lower(),
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
else:
    from python_agent.test_listener.executors.run import Run
    from python_agent.test_listener.executors.send_footprints import (
        SendFootprintsAnonymousExecution,
    )

    CONTEXT_SETTINGS = dict(
        token_normalize_func=lambda x: x.lower(),
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
from python_agent.test_listener.executors.start_execution import StartAnonymousExecution
from python_agent.test_listener.executors.test_frameworks.agent_execution import (
    AgentExecution,
)
from python_agent.test_listener.executors.test_frameworks.behave_execution import (
    BROWSER_PAGE_ATTR_DEFAULT,
    BehaveAgentExecution,
)
from python_agent.test_listener.executors.test_frameworks.nose_execution import (
    NoseAgentExecution,
)
from python_agent.test_listener.executors.test_frameworks.pabot_execution import (
    PabotAgentExecution,
)
from python_agent.test_listener.executors.test_frameworks.pytest_execution import (
    PytestAgentExecution,
)
from python_agent.test_listener.executors.test_frameworks.robot_execution import (
    RobotAgentExecution,
)
from python_agent.test_listener.executors.test_frameworks.unittest_execution import (
    UnittestAgentExecution,
)
from python_agent.test_listener.executors.upload_reports import UploadReports
from python_agent.utils import CommandType, generate_random_build_name

log = logging.getLogger(__name__)

# Mapping of new command name aliases to existing command names.
# Keys are lowercase because Click's token_normalize_func lowercases user input
# before our alias lookup in AliasedGroup.get_command().
COMMAND_ALIASES = {
    "openteststage": "start",
    "startteststage": "start",
    "closeteststage": "end",
    "endteststage": "end",
}


def handle_executor_exceptions(f):
    """
    Decorator that catches exceptions from executor.execute() calls.
    Backend-related errors (connection, timeout, HTTP 5xx) respect
    SL_FAIL_ON_ERROR: when false (default) the CI continues (exit 0),
    when true the CI breaks (exit 1). All other exceptions always exit 1.
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (
            ConnectionError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
        ) as e:
            fail_on_error = (
                os.environ.get("SL_FAIL_ON_ERROR", "false").lower() == "true"
            )
            if fail_on_error:
                sys.exit(1)
            log.warning(
                "Sealights backend unavailable: %s. "
                "CI will continue without Sealights." % str(e)
            )
            sys.exit(0)
        except Exception:
            sys.exit(1)

    return wrapper


def set_quiet_mode(ctx, param, value):
    """Callback to set quiet mode in ConsoleMessageTemplates when --quiet is used."""
    ConsoleMessageTemplates.set_quiet(value)
    return value


_common_options = [
    click.option(
        "--token",
        help="Token (mandatory. Can also be provided by 'tokenFile' argument). Case-sensitive.",
    ),
    click.option(
        "--tokenFile",
        default=TOKEN_FILE,
        help="A path to a file where the program can find the token. Case-sensitive.",
    ),
    click.option("--proxy", help="Proxy. Must be of the form: http[s]://<server>"),
    click.option(
        "--quiet",
        is_flag=True,
        default=False,
        callback=set_quiet_mode,
        is_eager=True,
        expose_value=False,
        help="Suppress console messages",
    ),
]

_build_session_options = [
    click.option(
        "--buildSessionId", help="Provide build session id manually, case-sensitive."
    ),
    click.option(
        "--buildSessionIdFile",
        default=BUILD_SESSION_ID_FILE,
        help="Path to a file to save the build session id in (default: <user.dir>/buildSessionId.txt).",
    ),
]

_scm_options = [
    click.option(
        "--scmProvider",
        required=False,
        help="The provider name of your Source Control Management (SCM) tool. "
        "Supported values are 'Github', 'Bitbucket' and 'Gitlab'. "
        "If not used, 'Github' is assumed.",
    ),
    click.option(
        "--scmVersion",
        required=False,
        help="The version of your Source Control Management (SCM) tool. "
        "If left blank, cloud version is assumed. "
        "Otherwise, specify the version of your on-premise server.",
    ),
    click.option(
        "--repositoryUrl",
        "--scmUrl",
        "--scmbaseurl",
        "scmbaseurl",
        required=False,
        help="The URL to the repository which contains the code. "
        "If left blank, the url of the remote GIT origin is being used.",
    ),
    click.option(
        "--scmType",
        "--scm",
        "scm",
        required=False,
        help="The name of your Source Control Management (SCM) tool. "
        "Supported values are 'git' and 'none'. If not used, 'git' is assumed.",
    ),
]


_robot_runner_options = [
    click.option("--labId", help="Lab Id, case-sensitive."),
    click.option(
        "--testStage",
        required=True,
        default=constants.DEFAULT_ENV,
        help="The tests stage (e.g 'integration tests', 'regression'). The default will be 'Unit Tests'",
    ),
    click.option(
        "--disableTia",
        "-tsd",
        "--test-selection-disable",
        "test_selection_disable",
        is_flag=True,
        help="A flag to disable the test selection otherwise enable",
    ),
    click.option(
        "-tsri",
        "--test-selection-retry-interval",
        default=TEST_RECOMMENDATION.interval_sec,
        help="Test recommendation retry interval in sec",
    ),
    click.option(
        "-tsrt",
        "--test-selection-retry-timeout",
        default=TEST_RECOMMENDATION.timeout_sec,
        help="Test recommendation retry timeout in sec",
    ),
    click.option("--testGroupId", required=False, default="", help="The Test Group Id"),
    click.option("--testProjectId", required=False, help="The Test Project Id"),
    click.option("--prid", required=False, help="The PR Id"),
    click.option(
        "--testNameFormat",
        type=click.Choice(constants.TEST_NAME_FORMATS),
        default=constants.TEST_NAME_FORMAT_FULL,
        help="How Robot tests are named to Sealights: 'full' (suite-qualified, "
        "the default) or 'short' (the bare test name, as the standalone "
        "robot/SLListener.py reports it). Changing it retrains TIA. "
        "Environment form: SL_TEST_NAME_FORMAT.",
    ),
]


def common_options(f):
    options = (
        _common_options
        if (f.__name__ == "config" or f.__name__ == "prconfig")
        else _common_options + _build_session_options
    )
    for option in options:
        f = option(f)
    return f


def robot_runner_options(f):
    """Sealights option stack shared by the Robot Framework subcommands.

    Declared once so `robot` and `pabot` cannot drift apart (contract C1,
    AC2, AC38). It deliberately carries no footprints or coverage flag
    (`--per-test`, `--interval`, `--cov-report`, the three `--footprints*`):
    neither command constructs a footprints pipeline, so a knob for one would
    be a knob for nothing (Business Rule 5, contract C11).
    """
    for option in reversed(_robot_runner_options):
        f = option(f)
    return f


def get_config_data(
    ctx,
    token,
    tokenfile,
    buildsessionid,
    buildsessionidfile,
    proxy,
    labid,
    test_project_id=None,
    prid=None,
    scm_args=None,
    # New CLI-derived values (SLDEV-26009). All optional; None means the
    # caller did not pass the corresponding CLI flag.
    interval=None,
    per_test=None,
    footprints_send_interval_secs=None,
    footprints_collect_interval_secs=None,
    footprints_buffer_threshold_mb=None,
    test_name_format=None,
):
    configuration_manager = ConfigurationManager()
    command_type = getattr(ctx, "command_type", CommandType.OTHER)
    config_data = configuration_manager.init_configuration(
        command_type,
        token,
        buildsessionid,
        labid,
        tokenfile,
        buildsessionidfile,
        proxy,
        test_project_id,
        prid,
        scm_args,
        interval=interval,
        per_test=per_test,
        footprints_send_interval_secs=footprints_send_interval_secs,
        footprints_collect_interval_secs=footprints_collect_interval_secs,
        footprints_buffer_threshold_mb=footprints_buffer_threshold_mb,
        test_name_format=test_name_format,
    )
    return config_data


def strtobool(val):
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError(f"Invalid truth value {val}")


class AliasedGroup(click.Group):
    """A Click Group that supports command aliases.

    Allows new command names (e.g., openTestStage) to resolve
    to existing commands (e.g., start) while maintaining backward compatibility.
    """

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        # Check alias mapping (cmd_name is already lowercased by token_normalize_func)
        actual_name = COMMAND_ALIASES.get(cmd_name)
        if actual_name is not None:
            return click.Group.get_command(self, ctx, actual_name)
        return None

    def format_commands(self, ctx, formatter):
        # Show original commands, then an aliases section in --help output
        super().format_commands(ctx, formatter)
        alias_rows = []
        for alias, target in sorted(COMMAND_ALIASES.items()):
            alias_rows.append((alias, f"Alias for {target}"))
        if alias_rows:
            with formatter.section("Command Aliases"):
                formatter.write_dl(alias_rows)


@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.version_option(version=AGENT_VERSION, prog_name="SeaLights Python Agent")
def cli():
    # entry point for the CLI. Reference from below and from setup.py -> console_scripts
    pass


@cli.command(context_settings=CONTEXT_SETTINGS)
@common_options
@click.option("--appName", required=True, help="Application name, case-sensitive.")
@click.option(
    "--branchName", help="Branch name, case-sensitive.", default=DEFAULT_BRANCH_NAME
)
@click.option(
    "--buildName",
    help="Build id, case-sensitive. Should be unique between builds.",
    default=generate_random_build_name(),
)
@click.option(
    "--buildSessionId",
    required=False,
    help="Provide build session id manually, case-sensitive.",
)
@click.option(
    "--scanDir",
    "--workspacePath",
    "workspacepath",
    help="Path to the workspace where the source code exists",
    default=DEFAULT_WORKSPACEPATH,
)
@click.option(
    "--includeFiles",
    "--include",
    "include",
    help=Opts.include.help,
    default=None,
    type=unshell_list,
)
@click.option(
    "--excludeFiles",
    "--exclude",
    "exclude",
    help=Opts.omit.help,
    default="*venv*,*sealights_layer*",
    type=unshell_list,
)
@click.pass_context
@handle_executor_exceptions
def config(
    ctx,
    token,
    tokenfile,
    proxy,
    appname,
    branchname,
    buildname,
    buildsessionid,
    workspacepath,
    include,
    exclude,
):
    ctx.command_type = CommandType.CONFIG
    config_data = get_config_data(ctx, token, tokenfile, None, None, proxy, None)
    print_agent_started_message(config_data, "config")
    Config(
        config_data,
        appname,
        branchname,
        buildname,
        buildsessionid,
        workspacepath,
        include,
        exclude,
    ).execute()
    print_agent_ended_success_message("success", "config")


@cli.command(context_settings=CONTEXT_SETTINGS)
@common_options
@click.option("--appName", required=True, help="Application name, case-sensitive.")
@click.option(
    "--targetBranch",
    required=True,
    help="The branch to which this PR will be merged into (already reported to SeaLights)",
)
@click.option(
    "--latestCommit",
    required=True,
    help="The full SHA of the last commit made to the Pull Request",
)
@click.option(
    "--pullRequestNumber",
    "--pullrequestnumber",
    "pullrequestnumber",
    required=True,
    help="The number assigned to the Pull Request from the source control",
)
@click.option(
    "--repositoryUrl",
    "--repourl",
    "repourl",
    required=True,
    help="The pull request URL for the PR to be scanned, up until the section before the pullRequestNumber value",
)
@click.option(
    "--buildSessionId",
    required=False,
    help="Provide build session id manually, case-sensitive.",
)
@click.option(
    "--scanDir",
    "--workspacePath",
    "workspacepath",
    help="Path to the workspace where the source code exists",
    default=DEFAULT_WORKSPACEPATH,
)
@click.option(
    "--includeFiles",
    "--include",
    "include",
    help=Opts.include.help,
    default=None,
    type=unshell_list,
)
@click.option(
    "--excludeFiles",
    "--exclude",
    "exclude",
    help=Opts.omit.help,
    default="*venv*",
    type=unshell_list,
)
@click.pass_context
def prconfig(
    ctx,
    token,
    tokenfile,
    proxy,
    appname,
    targetbranch,
    latestcommit,
    pullrequestnumber,
    repourl,
    buildsessionid,
    workspacepath,
    include,
    exclude,
):
    ctx.command_type = CommandType.CONFIG
    config_data = get_config_data(ctx, token, tokenfile, None, None, proxy, None)
    PrConfig(
        config_data,
        appname,
        targetbranch,
        latestcommit,
        pullrequestnumber,
        repourl,
        buildsessionid,
        workspacepath,
        include,
        exclude,
    ).execute()


def scm_options(f):
    for option in _scm_options:
        f = option(f)
    return f


@cli.command(context_settings=CONTEXT_SETTINGS)
@common_options
@scm_options
@click.pass_context
@handle_executor_exceptions
def scan(
    ctx,
    token,
    tokenfile,
    proxy,
    buildsessionid,
    buildsessionidfile,
    scmprovider,
    scmversion,
    scmbaseurl,
    scm,
):
    scm_args = ScmConfigArgs(scmprovider, scmversion, scmbaseurl, scm)
    ctx.command_type = CommandType.SCAN
    config_data = get_config_data(
        ctx,
        token,
        tokenfile,
        buildsessionid,
        buildsessionidfile,
        proxy,
        None,
        scm_args=scm_args,
    )
    print_agent_started_message(config_data, "scan")
    Build(config_data).execute()
    print_agent_ended_success_message("success", "scan")


@cli.command(context_settings=CONTEXT_SETTINGS)
@common_options
@click.option(
    "--collectorUrl",
    required=False,
    help="Provide collector url for lambda functions.",
    default=None,
    type=str,
)
@click.option(
    "--exportlayerpath",
    required=False,
    help="Set export Sealights layer path",
    default=None,
    type=click.Path(),
)
@click.option(
    "--slconfigpaths",
    required=True,
    help="Set list of paths of lambdas functions to save Sealights configuration files",
    default=None,
    type=unshell_list,
)
@click.pass_context
def configlambda(
    ctx,
    token,
    tokenfile,
    proxy,
    buildsessionid,
    buildsessionidfile,
    collectorurl,
    exportlayerpath,
    slconfigpaths,
):
    try:
        ctx.command_type = CommandType.OTHER
        config_data = get_config_data(
            ctx, token, tokenfile, buildsessionid, buildsessionidfile, proxy, None, None
        )
        Serverless(config_data, collectorurl, exportlayerpath, slconfigpaths).execute()
    except Exception as e:
        log.exception(str(e))


@cli.command(context_settings=CONTEXT_SETTINGS)
@common_options
@click.option("--labId", help="Lab Id, case-sensitive.")
@click.option(
    "--testStage",
    required=True,
    default=constants.DEFAULT_ENV,
    help="The tests stage (e.g 'integration tests', 'regression'). The default will be 'Unit Tests'",
)
@click.option(
    "--cov-report", type=click.Path(writable=True), help="generate xml coverage report"
)
@click.option(
    "--per-test", default="true", type=strtobool, help="collect coverage per test"
)
@click.option(
    "--interval",
    default=constants.INTERVAL_IN_MILLISECONDS,
    type=int,
    help="interval in milliseconds to send data",
)
@click.option(
    "--footprintsSendIntervalSecs",
    "footprints_send_interval_secs",
    default=None,
    type=int,
    help="Seconds between footprint uploads to the backend. Alias for the legacy "
    "--interval flag; takes precedence when both are set. Remote config wins over both.",
)
@click.option(
    "--footprintsCollectIntervalSecs",
    "footprints_collect_interval_secs",
    default=None,
    type=int,
    help="Seconds between coverage pulls from the tracer into the in-memory "
    "buffer. Default 1s when unset.",
)
@click.option(
    "--footprintsBufferThresholdMB",
    "footprints_buffer_threshold_mb",
    default=None,
    type=int,
    help="Flush the footprints buffer early if it grows beyond this many MB. "
    "Default 2 MB.",
)
@click.option(
    "--disableTia",
    "-tsd",
    "--test-selection-disable",
    "test_selection_disable",
    is_flag=True,
    help="A flag to disable the test selection otherwise enable",
)
@click.option(
    "-tsri",
    "--test-selection-retry-interval",
    default=TEST_RECOMMENDATION.interval_sec,
    help="Test recommendation retry interval in sec",
)
@click.option(
    "-tsrt",
    "--test-selection-retry-timeout",
    default=TEST_RECOMMENDATION.timeout_sec,
    help="Test recommendation retry timeout in sec",
)
@click.option("--testGroupId", required=False, default="", help="The Test Group Id")
@click.option("--testProjectId", required=False, help="The Test Project Id")
@click.option("--prid", required=False, help="The PR Id")
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def pytest(
    ctx,
    token,
    tokenfile,
    proxy,
    buildsessionid,
    buildsessionidfile,
    labid,
    teststage,
    cov_report,
    per_test,
    interval,
    footprints_send_interval_secs,
    footprints_collect_interval_secs,
    footprints_buffer_threshold_mb,
    test_selection_disable,
    test_selection_retry_interval,
    test_selection_retry_timeout,
    testgroupid,
    testprojectid,
    prid,
    args,
):
    ctx.command_type = CommandType.TEST
    config_data = get_config_data(
        ctx,
        token,
        tokenfile,
        buildsessionid,
        buildsessionidfile,
        proxy,
        labid,
        testprojectid,
        prid,
        interval=interval,
        per_test=per_test,
        footprints_send_interval_secs=footprints_send_interval_secs,
        footprints_collect_interval_secs=footprints_collect_interval_secs,
        footprints_buffer_threshold_mb=footprints_buffer_threshold_mb,
    )
    config_data.command_name = "pytest"
    print_agent_started_message(config_data, "pytest")
    config_data.testSelection.update(
        {
            "enable": not test_selection_disable,
            "interval": test_selection_retry_interval,
            "timeout": test_selection_retry_timeout,
        }
    )
    if teststage == constants.DEFAULT_ENV:
        log.warn("Test stage was not provided. Defaulting to 'Unit Tests'")
    PytestAgentExecution(
        config_data, labid, teststage, cov_report, per_test, interval, testgroupid, args
    ).execute()


@cli.command(context_settings=CONTEXT_SETTINGS)
@common_options
@click.option("--labId", help="Lab Id, case-sensitive.")
@click.option(
    "--testStage",
    required=True,
    default=constants.DEFAULT_ENV,
    help="The tests stage (e.g 'integration tests', 'regression'). The default will be 'Unit Tests'",
)
@click.option(
    "--cov-report", type=click.Path(writable=True), help="generate xml coverage report"
)
@click.option(
    "--per-test", default="true", type=strtobool, help="collect coverage per test"
)
@click.option(
    "--interval",
    default=constants.INTERVAL_IN_MILLISECONDS,
    type=int,
    help="interval in milliseconds to send data",
)
@click.option(
    "--footprintsSendIntervalSecs",
    "footprints_send_interval_secs",
    default=None,
    type=int,
    help="Seconds between footprint uploads to the backend. Alias for the legacy "
    "--interval flag; takes precedence when both are set. Remote config wins over both.",
)
@click.option(
    "--footprintsCollectIntervalSecs",
    "footprints_collect_interval_secs",
    default=None,
    type=int,
    help="Seconds between coverage pulls from the tracer into the in-memory "
    "buffer. Default 1s when unset.",
)
@click.option(
    "--footprintsBufferThresholdMB",
    "footprints_buffer_threshold_mb",
    default=None,
    type=int,
    help="Flush the footprints buffer early if it grows beyond this many MB. "
    "Default 2 MB.",
)
@click.option(
    "--disableTia",
    "-tsd",
    "--test-selection-disable",
    "test_selection_disable",
    is_flag=True,
    help="A flag to disable the test selection otherwise enable",
)
@click.option(
    "-tsri",
    "--test-selection-retry-interval",
    default=TEST_RECOMMENDATION.interval_sec,
    help="Test recommendation retry interval in sec",
)
@click.option(
    "-tsrt",
    "--test-selection-retry-timeout",
    default=TEST_RECOMMENDATION.timeout_sec,
    help="Test recommendation retry timeout in sec",
)
@click.option("--testGroupId", required=False, default="", help="The Test Group Id")
@click.option("--testProjectId", required=False, help="The Test Project Id")
@click.option("--prid", required=False, help="The PR Id")
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def nose(
    ctx,
    token,
    tokenfile,
    proxy,
    buildsessionid,
    buildsessionidfile,
    labid,
    teststage,
    cov_report,
    per_test,
    interval,
    footprints_send_interval_secs,
    footprints_collect_interval_secs,
    footprints_buffer_threshold_mb,
    test_selection_disable,
    test_selection_retry_interval,
    test_selection_retry_timeout,
    testgroupid,
    testprojectid,
    prid,
    args,
):
    ctx.command_type = CommandType.TEST
    args = list(args)
    config_data = get_config_data(
        ctx,
        token,
        tokenfile,
        buildsessionid,
        buildsessionidfile,
        proxy,
        labid,
        testprojectid,
        prid,
        interval=interval,
        per_test=per_test,
        footprints_send_interval_secs=footprints_send_interval_secs,
        footprints_collect_interval_secs=footprints_collect_interval_secs,
        footprints_buffer_threshold_mb=footprints_buffer_threshold_mb,
    )
    config_data.command_name = "nose"
    print_agent_started_message(config_data, "nose")
    config_data.testSelection.update(
        {
            "enable": not test_selection_disable,
            "interval": test_selection_retry_interval,
            "timeout": test_selection_retry_timeout,
        }
    )
    if teststage == constants.DEFAULT_ENV:
        log.warn("Test stage was not provided. Defaulting to 'Unit Tests'")
    NoseAgentExecution(
        config_data, labid, teststage, cov_report, per_test, interval, testgroupid, args
    ).execute()


@cli.command(context_settings=CONTEXT_SETTINGS)
@common_options
@click.option("--labId", help="Lab Id, case-sensitive.")
@click.option(
    "--testStage",
    required=True,
    default=constants.DEFAULT_ENV,
    help="The tests stage (e.g 'integration tests', 'regression'). The default will be 'Unit Tests'",
)
@click.option(
    "--cov-report", type=click.Path(writable=True), help="generate xml coverage report"
)
@click.option(
    "--per-test", default="true", type=strtobool, help="collect coverage per test"
)
@click.option(
    "--interval",
    default=constants.INTERVAL_IN_MILLISECONDS,
    type=int,
    help="interval in milliseconds to send data",
)
@click.option(
    "--footprintsSendIntervalSecs",
    "footprints_send_interval_secs",
    default=None,
    type=int,
    help="Seconds between footprint uploads to the backend. Alias for the legacy "
    "--interval flag; takes precedence when both are set. Remote config wins over both.",
)
@click.option(
    "--footprintsCollectIntervalSecs",
    "footprints_collect_interval_secs",
    default=None,
    type=int,
    help="Seconds between coverage pulls from the tracer into the in-memory "
    "buffer. Default 1s when unset.",
)
@click.option(
    "--footprintsBufferThresholdMB",
    "footprints_buffer_threshold_mb",
    default=None,
    type=int,
    help="Flush the footprints buffer early if it grows beyond this many MB. "
    "Default 2 MB.",
)
@click.option(
    "--disableTia",
    "-tsd",
    "--test-selection-disable",
    "test_selection_disable",
    is_flag=True,
    help="A flag to disable the test selection otherwise enable",
)
@click.option(
    "-tsri",
    "--test-selection-retry-interval",
    default=TEST_RECOMMENDATION.interval_sec,
    help="Test recommendation retry interval in sec",
)
@click.option(
    "-tsrt",
    "--test-selection-retry-timeout",
    default=TEST_RECOMMENDATION.timeout_sec,
    help="Test recommendation retry timeout in sec",
)
@click.option("--testGroupId", required=False, default="", help="The Test Group Id")
@click.option("--testProjectId", required=False, help="The Test Project Id")
@click.option("--prid", required=False, help="The PR Id")
@click.option(
    "--browser-page-attr",
    default=BROWSER_PAGE_ATTR_DEFAULT,
    help="Behave context attribute holding the Playwright page object "
    f"(default: {BROWSER_PAGE_ATTR_DEFAULT}). Browser integration is "
    "auto-detected when this attribute is set to a Playwright page.",
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def behave(
    ctx,
    token,
    tokenfile,
    proxy,
    buildsessionid,
    buildsessionidfile,
    labid,
    teststage,
    cov_report,
    per_test,
    interval,
    footprints_send_interval_secs,
    footprints_collect_interval_secs,
    footprints_buffer_threshold_mb,
    test_selection_disable,
    test_selection_retry_interval,
    test_selection_retry_timeout,
    testgroupid,
    testprojectid,
    prid,
    browser_page_attr,
    args,
):
    ctx.command_type = CommandType.TEST
    args = list(args)
    config_data = get_config_data(
        ctx,
        token,
        tokenfile,
        buildsessionid,
        buildsessionidfile,
        proxy,
        labid,
        testprojectid,
        prid,
        interval=interval,
        per_test=per_test,
        footprints_send_interval_secs=footprints_send_interval_secs,
        footprints_collect_interval_secs=footprints_collect_interval_secs,
        footprints_buffer_threshold_mb=footprints_buffer_threshold_mb,
    )
    config_data.command_name = "behave"
    print_agent_started_message(config_data, "behave")
    config_data.testSelection.update(
        {
            "enable": not test_selection_disable,
            "interval": test_selection_retry_interval,
            "timeout": test_selection_retry_timeout,
        }
    )
    if teststage == constants.DEFAULT_ENV:
        log.warn("Test stage was not provided. Defaulting to 'Unit Tests'")
    BehaveAgentExecution(
        config_data,
        labid,
        teststage,
        cov_report,
        per_test,
        interval,
        testgroupid,
        args,
        browser_page_attr=browser_page_attr,
    ).execute()


@cli.command(context_settings=CONTEXT_SETTINGS)
@common_options
@robot_runner_options
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def robot(
    ctx,
    token,
    tokenfile,
    proxy,
    buildsessionid,
    buildsessionidfile,
    labid,
    teststage,
    test_selection_disable,
    test_selection_retry_interval,
    test_selection_retry_timeout,
    testgroupid,
    testprojectid,
    prid,
    testnameformat,
    args,
):
    ctx.command_type = CommandType.TEST
    args = list(args)
    try:
        config_data = get_config_data(
            ctx,
            token,
            tokenfile,
            buildsessionid,
            buildsessionidfile,
            proxy,
            labid,
            testprojectid,
            prid,
            test_name_format=testnameformat,
        )
    except Exception as e:
        # Rule 15, AC18: unusable configuration disables Sealights and the
        # customer's Robot run still executes and still reports its own
        # results. init_configuration renders the failure banner and re-raises,
        # which every other subcommand lets abort the run; Robot must not.
        log.error("Sealights is disabled. Error: %s" % str(e))
        config_data = ConfigData()
        config_data.isDisabled = True
    config_data.command_name = "robot"
    print_agent_started_message(config_data, "robot")
    config_data.testSelection.update(
        {
            "enable": not test_selection_disable,
            "interval": test_selection_retry_interval,
            "timeout": test_selection_retry_timeout,
        }
    )
    if teststage == constants.DEFAULT_ENV:
        log.warning("Test stage was not provided. Defaulting to 'Unit Tests'")
    RobotAgentExecution(
        config_data,
        labid,
        teststage,
        testgroupid,
        args,
    ).execute()


@cli.command(context_settings=CONTEXT_SETTINGS)
@common_options
@robot_runner_options
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def pabot(
    ctx,
    token,
    tokenfile,
    proxy,
    buildsessionid,
    buildsessionidfile,
    labid,
    teststage,
    test_selection_disable,
    test_selection_retry_interval,
    test_selection_retry_timeout,
    testgroupid,
    testprojectid,
    prid,
    testnameformat,
    args,
):
    ctx.command_type = CommandType.TEST
    args = list(args)
    try:
        config_data = get_config_data(
            ctx,
            token,
            tokenfile,
            buildsessionid,
            buildsessionidfile,
            proxy,
            labid,
            testprojectid,
            prid,
            test_name_format=testnameformat,
        )
    except Exception as e:
        # Rule 15, AC18, as for `robot`: unusable configuration disables
        # Sealights and the customer's run still executes.
        log.error("Sealights is disabled. Error: %s" % str(e))
        config_data = ConfigData()
        config_data.isDisabled = True
    config_data.command_name = "pabot"
    print_agent_started_message(config_data, "pabot")
    config_data.testSelection.update(
        {
            "enable": not test_selection_disable,
            "interval": test_selection_retry_interval,
            "timeout": test_selection_retry_timeout,
        }
    )
    if teststage == constants.DEFAULT_ENV:
        log.warning("Test stage was not provided. Defaulting to 'Unit Tests'")
    PabotAgentExecution(
        config_data,
        labid,
        teststage,
        testgroupid,
        args,
    ).execute()


@cli.command(context_settings=CONTEXT_SETTINGS)
@common_options
@click.option("--labId", help="Lab Id, case-sensitive.")
@click.option(
    "--testStage",
    required=True,
    default=constants.DEFAULT_ENV,
    help="The tests stage (e.g 'integration tests', 'regression'). The default will be 'Unit Tests'",
)
@click.option(
    "--cov-report", type=click.Path(writable=True), help="generate xml coverage report"
)
@click.option(
    "--per-test", default="true", type=strtobool, help="collect coverage per test"
)
@click.option(
    "--interval",
    default=constants.INTERVAL_IN_MILLISECONDS,
    type=int,
    help="interval in milliseconds to send data",
)
@click.option(
    "--footprintsSendIntervalSecs",
    "footprints_send_interval_secs",
    default=None,
    type=int,
    help="Seconds between footprint uploads to the backend. Alias for the legacy "
    "--interval flag; takes precedence when both are set. Remote config wins over both.",
)
@click.option(
    "--footprintsCollectIntervalSecs",
    "footprints_collect_interval_secs",
    default=None,
    type=int,
    help="Seconds between coverage pulls from the tracer into the in-memory "
    "buffer. Default 1s when unset.",
)
@click.option(
    "--footprintsBufferThresholdMB",
    "footprints_buffer_threshold_mb",
    default=None,
    type=int,
    help="Flush the footprints buffer early if it grows beyond this many MB. "
    "Default 2 MB.",
)
@click.option(
    "--disableTia",
    "-tsd",
    "--test-selection-disable",
    "test_selection_disable",
    is_flag=True,
    help="A flag to disable the test selection otherwise enable",
)
@click.option(
    "-tsri",
    "--test-selection-retry-interval",
    default=TEST_RECOMMENDATION.interval_sec,
    help="Test recommendation retry interval in sec",
)
@click.option(
    "-tsrt",
    "--test-selection-retry-timeout",
    default=TEST_RECOMMENDATION.timeout_sec,
    help="Test recommendation retry timeout in sec",
)
@click.option("--testGroupId", required=False, default="", help="The Test Group Id")
@click.option("--testProjectId", required=False, help="The Test Project Id")
@click.option("--prid", required=False, help="The PR Id")
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def unittest(
    ctx,
    token,
    tokenfile,
    proxy,
    buildsessionid,
    buildsessionidfile,
    labid,
    teststage,
    cov_report,
    per_test,
    interval,
    footprints_send_interval_secs,
    footprints_collect_interval_secs,
    footprints_buffer_threshold_mb,
    test_selection_disable,
    test_selection_retry_interval,
    test_selection_retry_timeout,
    testgroupid,
    testprojectid,
    prid,
    args,
):
    ctx.command_type = CommandType.TEST
    config_data = get_config_data(
        ctx,
        token,
        tokenfile,
        buildsessionid,
        buildsessionidfile,
        proxy,
        labid,
        testprojectid,
        prid,
        interval=interval,
        per_test=per_test,
        footprints_send_interval_secs=footprints_send_interval_secs,
        footprints_collect_interval_secs=footprints_collect_interval_secs,
        footprints_buffer_threshold_mb=footprints_buffer_threshold_mb,
    )
    config_data.command_name = "unittest"
    print_agent_started_message(config_data, "unittest")
    config_data.testSelection.update(
        {
            "enable": not test_selection_disable,
            "interval": test_selection_retry_interval,
            "timeout": test_selection_retry_timeout,
        }
    )
    if teststage == constants.DEFAULT_ENV:
        log.warn("Test stage was not provided. Defaulting to 'Unit Tests'")
    UnittestAgentExecution(
        config_data, labid, teststage, cov_report, per_test, interval, testgroupid, args
    ).execute()


@cli.command(context_settings=CONTEXT_SETTINGS)
@common_options
@click.option(
    "--testStage",
    required=True,
    default=constants.DEFAULT_ENV,
    help="The tests stage (e.g 'integration tests', 'regression'). The default will be 'Unit Tests'",
)
@click.option("--labId", help="Lab Id, case-sensitive.")
@click.option("--testGroupId", required=False, default="", help="The Test Group Id")
@click.option("--testProjectId", required=False, help="The Test Project Id")
@click.option("--prid", required=False, help="The PR Id")
@click.option(
    "--waitAfterStart",
    required=False,
    default=0,
    help="The time to wait after starting the execution",
)
@click.pass_context
def start(
    ctx,
    token,
    tokenfile,
    proxy,
    buildsessionid,
    buildsessionidfile,
    teststage,
    labid,
    testgroupid,
    testprojectid,
    prid,
    waitafterstart,
):
    ctx.command_type = CommandType.START
    try:
        config_data = get_config_data(
            ctx,
            token,
            tokenfile,
            buildsessionid,
            buildsessionidfile,
            proxy,
            labid,
            testprojectid,
            prid,
        )
        if getattr(config_data, "isDisabled", False):
            fail_on_error = (
                os.environ.get("SL_FAIL_ON_ERROR", "false").lower() == "true"
            )
            if fail_on_error:
                sys.exit(1)
            log.warning("Sealights is disabled. CI will continue without Sealights.")
            return
        if teststage == constants.DEFAULT_ENV:
            log.warn("Test stage was not provided. Defaulting to 'Unit Tests'")
        StartAnonymousExecution(config_data, teststage, labid, testgroupid).execute()
    except (
        ConnectionError,
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.HTTPError,
    ) as e:
        fail_on_error = os.environ.get("SL_FAIL_ON_ERROR", "false").lower() == "true"
        if fail_on_error:
            sys.exit(1)
        log.warning(
            "Sealights backend unavailable: %s. "
            "CI will continue without Sealights." % str(e)
        )
        return
    if waitafterstart > 0:
        log.info(f"Waiting for {waitafterstart} seconds after starting the execution")
        import time

        time.sleep(waitafterstart)


@cli.command(context_settings=CONTEXT_SETTINGS)
@common_options
@click.option("--labId", help="Lab Id, case-sensitive.")
@click.option("--testGroupId", required=False, default="", help="The Test Group Id")
@click.option(
    "--waitBeforeEnd",
    required=False,
    default=0,
    help="The time to wait before ending the execution",
)
@click.pass_context
def end(
    ctx,
    token,
    tokenfile,
    proxy,
    buildsessionid,
    buildsessionidfile,
    labid,
    testgroupid,
    waitbeforeend,
):
    try:
        config_data = get_config_data(
            ctx, token, tokenfile, buildsessionid, buildsessionidfile, proxy, labid
        )
        if getattr(config_data, "isDisabled", False):
            fail_on_error = (
                os.environ.get("SL_FAIL_ON_ERROR", "false").lower() == "true"
            )
            if fail_on_error:
                sys.exit(1)
            log.warning("Sealights is disabled. CI will continue without Sealights.")
            return
        if waitbeforeend > 0:
            log.info(f"Waiting for {waitbeforeend} seconds before ending the execution")
            import time

            time.sleep(waitbeforeend)
        EndAnonymousExecution(config_data, labid, testgroupid).execute()
    except (
        ConnectionError,
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.HTTPError,
    ) as e:
        fail_on_error = os.environ.get("SL_FAIL_ON_ERROR", "false").lower() == "true"
        if fail_on_error:
            sys.exit(1)
        log.warning(
            "Sealights backend unavailable: %s. "
            "CI will continue without Sealights." % str(e)
        )


@cli.command(context_settings=CONTEXT_SETTINGS)
@common_options
@click.option("--labId", help="Lab Id, case-sensitive.")
@click.option(
    "--file",
    "--reportfile",
    "reportfile",
    type=unshell_list,
    help="Report files. This argument can be declared multiple times in order to upload multiple files.",
)
@click.option(
    "--filesFolder",
    "--reportfilesfolder",
    "reportfilesfolder",
    type=unshell_list,
    help="Folders that contains nothing but report files. All files in folder will be uploaded. This argument can be declared multiple times in order to upload multiple files from multiple folders.",
)
@click.option(
    "--source",
    default="Junit xml report",
    help="The reports provider. If not set, the default will be 'Junit xml report'",
)
@click.option(
    "--type",
    default="JunitReport",
    help="The report type. If not set, the default will be 'JunitReport'",
)
@click.option(
    "--hasMoreRequests",
    default="true",
    type=strtobool,
    help="flag indicating if test results contains multiple reports. True for multiple reports. False otherwise",
)
@click.pass_context
def uploadreports(
    ctx,
    token,
    tokenfile,
    proxy,
    buildsessionid,
    buildsessionidfile,
    labid,
    reportfile,
    reportfilesfolder,
    source,
    type,
    hasmorerequests,
):
    ctx.command_type = CommandType.OTHER
    config_data = get_config_data(
        ctx, token, tokenfile, buildsessionid, buildsessionidfile, proxy, labid
    )
    UploadReports(
        config_data, labid, reportfile, reportfilesfolder, source, type, hasmorerequests
    ).execute()


@cli.command(context_settings=CONTEXT_SETTINGS)
@common_options
@click.option("--labId", help="Lab Id, case-sensitive.")
@click.option(
    "--cov-report",
    type=click.Path(writable=True),
    help="generate xml coverage report",
)
@click.option(
    "--testStage",
    required=False,
    help="The tests stage (e.g 'integration tests', 'regression'). The default will be 'Unit Tests'",
)
@click.option("--testGroupId", required=False, help="The Test Group Id")
@click.option(
    "--autoExecution",
    is_flag=True,
    default=False,
    help="Run with auto execution (start and end execution)",
)
@click.option(
    "--dropInitFootprints",
    is_flag=True,
    default=False,
    help="Drop initial footprints (ignore coverage data before execution starts)",
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def run(
    ctx,
    token,
    tokenfile,
    proxy,
    buildsessionid,
    buildsessionidfile,
    labid,
    cov_report,
    teststage,
    testgroupid,
    autoexecution,
    dropinitfootprints,
    args,
):
    ctx.command_type = CommandType.RUN
    config_data = get_config_data(
        ctx, token, tokenfile, buildsessionid, buildsessionidfile, proxy, labid
    )
    config_data.args = sys.argv
    config_data.covReport = cov_report
    config_data.auto_execution = autoexecution
    config_data.drop_init_footprints = dropinitfootprints
    if autoexecution:
        log.info(
            "Running with auto execution (Start execution and End execution will be automatically executed)"
        )
        if not teststage:
            log.error("Test stage is required for auto execution")
            return
        config_data.testStage = teststage
        config_data.testGroupId = testgroupid
    Run(config_data).execute(args)


@cli.command(hidden=True, context_settings=CONTEXT_SETTINGS)
@common_options
@click.option("--labId", help="Lab Id, case-sensitive.")
@click.pass_context
def sendfootprints(
    ctx, token, tokenfile, proxy, buildsessionid, buildsessionidfile, labid
):
    ctx.command_type = CommandType.OTHER
    config_data = get_config_data(
        ctx, token, tokenfile, buildsessionid, buildsessionidfile, proxy, None
    )
    config_data.isOfflineMode = True
    SendFootprintsAnonymousExecution(config_data, labid).execute()


@cli.command(hidden=True, context_settings=CONTEXT_SETTINGS)
@common_options
@click.pass_context
def init(ctx, token, tokenfile, proxy, buildsessionid, buildsessionidfile):
    ctx.command_type = CommandType.RUN

    # Get full configuration from CLI args/files (token, server, buildsessionid, etc.)
    config_data = get_config_data(
        ctx, token, tokenfile, buildsessionid, buildsessionidfile, proxy, None
    )
    config_data.auto_execution = False

    # Try to load additional config from sl_configuration environment variable
    # (set by the 'run' command for app server use cases like uWSGI/Gunicorn)
    # This may contain labId and covReport that were configured via the run command
    cm = ConfigurationManager()
    cm.try_load_configuration_from_config_environment_variable()

    # Merge: use labId and covReport from env var config if available
    labid = cm.config_data.labId if cm.config_data.labId else config_data.labId
    cov_report = (
        cm.config_data.covReport if cm.config_data.covReport else config_data.covReport
    )

    AgentExecution(config_data, labid, cov_report=cov_report)


def print_agent_started_message(config_data, command_type):
    ConsoleMessageTemplates.render_and_print(
        "common.general.agent-started",
        version=__version__,
        command=command_type,
        agent_id=config_data.agentId,
        technology="python",
        dateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


def print_agent_ended_success_message(result, command_type):
    if result == "success":
        ConsoleMessageTemplates.render_and_print(
            "common.general.agent-ended-succeeded",
            command=command_type,
            dateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
    elif result == "warning":
        ConsoleMessageTemplates.render_and_print(
            "common.general.agent-ended-warnings",
            command=command_type,
            dateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
    else:
        ConsoleMessageTemplates.render_and_print(
            "common.general.agent-ended-error",
            command=command_type,
            error=result,
            dateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )


if __name__ == "__main__":
    cli()
