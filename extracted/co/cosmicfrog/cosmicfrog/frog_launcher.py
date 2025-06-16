"""
    Launcher code for Cosmic Frog utilities. Allows utilities to launch with minimal code overhead
"""

import os
import argparse
import json
import inspect
import traceback
import contextlib
from cosmicfrog import FrogModel, Params
from .frog_utilitydetails import UtilityDetails

# Handles launch code for utilities (so you don't have to!)


def __parse_args():
    parser = argparse.ArgumentParser(
        description="This is a Cosmic Frog utility. Visit www.cosmicfrog.com."
    )

    exclusive_group = parser.add_mutually_exclusive_group(required=True)

    # Usage: either call a function e.g. run, or --details to call both description and parameters and get an info block for
    # the utility
    exclusive_group.add_argument("--run", action="store_true", help="Run the utility.")
    exclusive_group.add_argument(
        "--details", action="store_true", help="Get the info block for the utility."
    )

    # Addition information when calling run
    parser.add_argument(
        "--model_connection_string",
        type=str,
        help="Frog model connection string.",
        default=None,
    )
    parser.add_argument("--app_key", type=str, help="Frog user app key", default=None)
    parser.add_argument(
        "json_data",
        type=str,
        nargs="?",
        default=None,
        help="The JSON data payload passed to the function.",
    )

    return parser.parse_args()


def __call_utility_details(main_globals) -> None:
    """Calls the details method of a utility, used to populate CF UI with parameters"""

    details = main_globals.get("details")
    if not details:
        raise ValueError("Function 'details' not found")

    function_params = inspect.signature(details).parameters

    num_params = len(function_params)

    if num_params != 0:
        raise ValueError(f"Expecting 0 arguments for details function, found {num_params}")

    # TODO: Error handling, see frogspawn
    with contextlib.redirect_stdout(None):
        details = details()

    assert isinstance(details, UtilityDetails)
    assert isinstance(details.category, str)
    assert isinstance(details.description, str)
    assert isinstance(details.params, Params)

    print(details.to_json())


def __call_utility_run(args, data, main_globals):
    """Calls the run function, passing in a model connection and parameters from UI"""

    func = main_globals.get("run")
    if not func:
        raise ValueError("Function 'run' not found")

    function_params = inspect.signature(func).parameters

    num_params = len(function_params)

    if num_params != 2:
        raise ValueError(f"Expecting 2 arguments for 'run' function, found {num_params}")

    params = Params(data)

    print(f"Connecting to : {params.model_name}")

    connection_string = args.model_connection_string

    # If app key is specified, use it
    # Note: Give it to FrogModel to make connections just work
    # Also put it in params for util writer to consume

    if args.app_key:
        # Note: Using class variable method for app key, since this allows user creating
        # a utility to create other model connections without requiring app key to be
        # supplied for each
        FrogModel.class_app_key = args.app_key
        params.app_key = args.app_key
    else:
        params.app_key = os.environ.get("OPTILOGIC_JOB_APPKEY")

    # If no connection string supplied on command line, assume running in Andromeda
    # Initialise Frog model (quietly, no console output)
    if connection_string is None:
        with contextlib.redirect_stdout(None):
            model = FrogModel(params.model_name)
    else:
        with contextlib.redirect_stdout(None):
            model = FrogModel(connection_string=connection_string)

    func(model, params)


def start_utility(main_globals):
    """
    Passes off control to the requested function in the utility
    """
    try:
        args = __parse_args()

        if args.run:
            data = json.loads(args.json_data) if args.json_data else None

            # TODO: List for backcompat is deprecated (add warning here)
            assert isinstance(
                data, (dict, list)
            ), "The data is not a list or dict of parameter values"

            # Note: At a minimum, all utilities need the model name as a parameter
            assert len(data) > 0, "The parameter list is empty"

            __call_utility_run(args, data, main_globals)

            return

        assert args.details

        # TODO: Currently the details function does not get a connection, this may change
        return __call_utility_details(main_globals)

    except Exception as e:  # pylint: disable=broad-exception-caught
        # Handle the exception as needed. For now, just print the error message.
        print(f"An error occurred: {e}")
        traceback.print_exc()
