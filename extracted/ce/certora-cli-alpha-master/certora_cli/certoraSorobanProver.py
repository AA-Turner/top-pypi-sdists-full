#!/usr/bin/env python3
#     The Certora Prover
#     Copyright (C) 2025  Certora Ltd.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, version 3 of the License.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.


import sys
import time
import logging
from pathlib import Path
from rich.console import Console

scripts_dir_path = Path(__file__).parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))

from Shared.certoraLogging import LoggingManager
from Shared import certoraUtils as Util
from typing import List, Optional, Tuple, Dict

import CertoraProver.certoraContext as Ctx
import CertoraProver.certoraContextAttributes as Attrs
from CertoraProver import certoraContextValidator as Cv
from CertoraProver.certoraContextClass import CertoraContext
from CertoraProver.certoraCollectRunMetadata import collect_run_metadata
from CertoraProver.certoraCollectConfigurationLayout import collect_configuration_layout
from CertoraProver.certoraBuildRust import build_rust_app
from CertoraProver.certoraCloudIO import CloudVerification, validate_version_and_branch
from certoraRun import CertoraRunResult, VIOLATIONS_EXIT_CODE, CertoraFoundViolations


run_logger = logging.getLogger("run")

def setup_environment(args: List[str]) -> Tuple[CertoraContext, LoggingManager]:
    """
    Setup the environment for running the prover.
    This includes:
    1. Setting up the logging manager
    2. Parsing the arguments
    3. Setting up the context
    """
    Attrs.set_attribute_class(Attrs.SorobanProverAttributes)
    non_str_els = [x for x in args if not isinstance(x, str)]
    if non_str_els:
        print(f"args for run_certora that are not strings: {non_str_els}")
        exit(1)

    # If we are not in debug mode, we do not want to print the traceback in case of exceptions.
    if '--debug' not in args:  # We check manually, because we want no traceback in argument parsing exceptions
        sys.tracebacklimit = 0

    # creating the default internal dir, files may be copied to user defined build directory after
    # parsing the input

    if not ('--help' in args or '--version' in args):
        Util.reset_certora_internal_dir()
        Util.safe_create_dir(Util.get_build_dir())
        logging_manager = LoggingManager()

    Ctx.handle_flags_in_args(args)
    context = Ctx.get_args(args)  # Parse arguments

    assert logging_manager, "logging manager was not set"
    logging_manager.set_log_level_and_format(is_quiet=Ctx.is_minimal_cli_output(context),
                                             debug=context.debug,
                                             debug_topics=context.debug_topics,
                                             show_debug_topics=context.show_debug_topics)

    return context, logging_manager


def collect_and_validate_metadata(context: CertoraContext) -> None:
    """
    Collect and validate run metadata.

    Args:
        context: The Certora context containing verification settings

    Raises:
        Util.TestResultsReady: If this is a metadata test run
    """
    metadata = collect_run_metadata(wd=Path.cwd(), raw_args=sys.argv, context=context)

    if context.test == str(Util.TestValue.CHECK_METADATA):
        raise Util.TestResultsReady(metadata)

    metadata.dump()


def collect_and_dump(context: CertoraContext) -> None:
    """
    Collect and dump the configuration layout.

    Args:
        context: The Certora context containing verification settings

    Raises:
        Util.TestResultsReady: If this is a configuration layout test run
    """
    configuration_layout = collect_configuration_layout()

    if context.test == str(Util.TestValue.CHECK_CONFIG_LAYOUT):
        raise Util.TestResultsReady(configuration_layout)

    configuration_layout.dump()


def build_project(context: CertoraContext) -> Dict:
    """
    Build the Rust application.

    Args:
        context: The Certora context containing build settings

    Returns:
        Dict: Timing information for the build process

    Raises:
        Util.TestResultsReady: If this is a build test run
    """
    timings = {}
    run_logger.debug("Build Soroban target")

    build_start = time.perf_counter()
    build_rust_app(context)
    build_end = time.perf_counter()

    timings["buildTime"] = round(build_end - build_start, 4)

    if context.test == str(Util.TestValue.AFTER_BUILD):
        raise Util.TestResultsReady(context)

    return timings

def run_local_verification(context: CertoraContext) -> int:
    """
    Run verification locally.

    Args:
        context: The Certora context containing verification settings

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    check_cmd = Ctx.get_local_run_cmd(context)
    run_logger.info(f"Verifier run command:\n {check_cmd}")

    run_result = Util.run_jar_cmd(
        check_cmd, override_exit_code=False, logger_topic="verification", print_output=True
    )

    if run_result == 0:
        Util.print_completion_message("Finished running verifier:")
        run_logger.info(f"\t{check_cmd}")
        return 0
    else:
        return 1


def run_cloud_verification(context: CertoraContext, args: List[str],
                           timings: dict) -> Tuple[int, Optional[CertoraRunResult]]:
    """
    Run verification in the cloud.

    Args:
        context: The Certora context containing verification settings
        args: Command line arguments
        timings: Dict containing timing information

    Returns:
        Tuple[int, Optional[CertoraRunResult]]: Exit code and result object
    """
    if context.compilation_steps_only:
        return 0, CertoraRunResult(None, False, Util.get_certora_sources_dir(), None)

    context.key = Cv.validate_certora_key()
    cloud_verifier = CloudVerification(context, timings)

    # Wrap strings with space with ' so it can be copied and pasted to shell
    pretty_args = [f"'{arg}'" if ' ' in arg else arg for arg in args]
    cl_args = ' '.join(pretty_args)

    exit_code = 0
    return_value = None

    if not cloud_verifier.cli_verify_and_report(cl_args, context.wait_for_results):
        exit_code = VIOLATIONS_EXIT_CODE

    if cloud_verifier.statusUrl:
        return_value = CertoraRunResult(
            cloud_verifier.statusUrl, False,
            Util.get_certora_sources_dir(), cloud_verifier.reportUrl
        )

    return exit_code, return_value


def run_soroban_prover(args: List[str]) -> Optional[CertoraRunResult]:
    """
    The main function that is responsible for the general flow of the script.
    The general flow is:
    1. Parse program arguments
    2. Run the necessary steps (build/ cloud verification/ local verification)
    """

    context, logging_manager = setup_environment(args)
    timings = {}
    exit_code = 0  # The exit code of the script. 0 means success, any other number is an error.
    return_value = None

    # Collect and validate metadata and configuration layout
    collect_and_validate_metadata(context)
    collect_and_dump(context)

    # Version validation
    if not context.local and not context.build_only and not context.compilation_steps_only:
        """
        The line below will raise an exception if the local version is incompatible.
        """
        validate_version_and_branch(context)

    # Build the application
    timings.update(build_project(context))

    # Run verification if requested
    if not context.build_only:

        if context.local:
            exit_code = run_local_verification(context)
        else:
            # Remove debug logger before running cloud verification
            logging_manager.remove_debug_logger()
            exit_code, return_value = run_cloud_verification(context, args, timings)

    # Handle exit codes and return
    if exit_code == VIOLATIONS_EXIT_CODE:
        raise CertoraFoundViolations("violations were found", return_value)
    if exit_code != 0:
        raise Util.CertoraUserInputError(f"certoraSorobanProver failed (code {exit_code})")
    return return_value


def entry_point() -> None:
    """
    This function is the entry point of the certora_cli customer-facing package, as well as this script.
    It is important this function gets no arguments!
    """
    try:
        run_soroban_prover(sys.argv[1:])
        sys.exit(0)
    except KeyboardInterrupt:
        Console().print("[bold red]\nInterrupted by user")
        sys.exit(1)
    except CertoraFoundViolations as e:
        try:
            if e.results and e.results.rule_report_link:
                print(f"report url: {e.results.rule_report_link}")
        except Exception:
            pass
        Console().print("[bold red]\nViolations were found\n")
        sys.exit(1)
    except Util.CertoraUserInputError as e:
        if e.orig:
            print(f"\n{str(e.orig).strip()}")
        if e.more_info:
            print(f"\n{e.more_info.strip()}")
        Console().print(f"[bold red]\n{e}\n")
        sys.exit(1)
    except Exception as e:
        Console().print(f"[bold red]{e}")
        sys.exit(1)


if __name__ == '__main__':
    entry_point()
