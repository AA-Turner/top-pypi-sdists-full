# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

# -*- coding: utf-8 -*-

"""Python module used for calculating interfaces for CSP"""


import argparse
import os
import re
import sys
from itertools import product
from pathlib import Path
from textwrap import dedent
from typing import List, Optional

import git

from powertrain_build.interface.application import Application, Model, get_active_signals
from powertrain_build.interface.ems import CsvEMS
from powertrain_build.lib import logger

LOGGER = logger.create_logger("Check interface")


def process_app(config):
    """Get an app specification for the current project

    Entrypoint for external scripts.

    Args:
        config (pathlib.Path): Path to the ProjectCfg.json
    Returns:
        app (Application): pybuild project
    """
    app = Application()
    app.parse_definition(config)
    return app


def model_app_consistency(model, app_models, app, errors):
    """Compare model signal interface with list of models.

    Args:
        model (Model): model to compare against application
        app_models (list(Model)): list of models to compare with
        app (Application): pybuild project
        errors (dict): Object for counting errors of different types
    """

    for compare_model in app_models:
        LOGGER.debug("Comparing %s with %s in %s", model.name, compare_model.name, app.name)
        active_model_outsignals = get_active_signals(model.outsignals, app.pybuild["feature_cfg"])
        active_model_insignals = get_active_signals(model.insignals, app.pybuild["feature_cfg"])
        active_compare_outsignals = get_active_signals(compare_model.outsignals, app.pybuild["feature_cfg"])
        active_compare_insignals = get_active_signals(compare_model.insignals, app.pybuild["feature_cfg"])
        check_signals(
            active_model_insignals,
            active_compare_outsignals,
            errors,
            [app.name, model.name],
            [app.name, compare_model.name],
        )
        check_signals(
            active_model_outsignals,
            active_compare_insignals,
            errors,
            [app.name, model.name],
            [app.name, compare_model.name],
        )


def check_internal_signals(app, model_names=None):
    """Look for all internal signal mismatches.

    Args:
        app (Application): pybuild project
        model_names (list(Model)): models based on parsed config jsons
    Returns:
        serious_mismatch (bool): A serious mismatch was found
    """
    serious_mismatch = False
    LOGGER.debug("Checking internal signals")
    LOGGER.debug("Checking against %s", app.signals)
    errors = {"type": 0, "range": 0, "unit": 0, "width": 0}
    app_models = app.get_models()
    for signal in app.signals:
        LOGGER.debug(signal.properties)

    for model in app_models:
        if model_names is not None and model.name not in model_names:
            LOGGER.debug("Skipping %s", model.name)
            continue
        LOGGER.debug("Checking %s in %s", model.name, app.name)
        active_insignals = get_active_signals(model.insignals, app.pybuild["feature_cfg"])
        insignal_mismatch = check_signals(active_insignals, app.signals, errors, [app.name, model.name], [app.name])
        active_outsignals = get_active_signals(model.outsignals, app.pybuild["feature_cfg"])
        outsignal_mismatch = check_signals(active_outsignals, app.signals, errors, [app.name, model.name], [app.name])
        if insignal_mismatch or outsignal_mismatch:
            serious_mismatch = True
            model_app_consistency(model, app_models, app, errors)
        # Only compare with all models if a mismatch is found
    LOGGER.debug("Total errors: %s", errors)
    return serious_mismatch


def check_models_generic(all_models, model_names, emses):
    """Check filtered models against all models and external interfaces."""
    serious_mismatch = False
    for model in all_models:
        LOGGER.info("Checking signals attributes for %s", model.name)
        if model.name not in model_names:
            continue
        errors = {"type": 0, "range": 0, "unit": 0, "width": 0}
        LOGGER.debug("Checking internal signals for %s", model.name)
        for corresponding_model in all_models:
            serious_mismatch |= check_signals(
                model.insignals, corresponding_model.outsignals, errors, [model.name], [corresponding_model.name]
            )
            serious_mismatch |= check_signals(
                model.outsignals, corresponding_model.insignals, errors, [model.name], [corresponding_model.name]
            )
        if emses:
            LOGGER.debug("Checking external signals for %s", model.name)
        for ems in emses:
            serious_mismatch |= check_signals(
                model.insignals, ems.outsignals, errors, [model.name], [ems.name]
            )
            serious_mismatch |= check_signals(
                model.outsignals, ems.insignals, errors, [model.name], [ems.name]
            )
        LOGGER.debug("Total errors for %s: %s", model.name, errors)
    return serious_mismatch


def get_all_models(model_root):
    """Find, filter and parse all model configurations."""
    LOGGER.info("Parsing all models")
    prefix = "config_"
    suffix = ".json"
    models = []
    for dirpath, _, filenames in os.walk(model_root):
        dirpath = Path(dirpath)
        for filename in [f for f in filenames if f.startswith(prefix) and f.endswith(suffix)]:
            name = filename[len(prefix): -len(suffix)]
            if name == dirpath.parent.stem:
                model = Model(None)
                model.parse_definition((name, Path(dirpath, filename)))
                models.append(model)
    return models


def get_projects(root, project_names):
    """Find, parse and filter all project configurations."""
    LOGGER.info("Parsing all projects")
    projects = []
    for dirpath, _, filenames in os.walk(root):
        dirpath = Path(dirpath)
        for filename in [f for f in filenames if f == "ProjectCfg.json"]:
            config = Path(dirpath, filename)
            app = Application()
            app_name = app.get_name(config)
            if project_names is not None and app_name not in project_names:
                if config.parent.stem not in project_names:
                    LOGGER.info("%s or %s does not match %s", app_name, config.parent.stem, project_names)
                    continue
            app.parse_definition(config)
            if app.pybuild["build_cfg"].has_yaml_interface:
                LOGGER.warning("Interface checks for yaml-interface projects are not implemtented yet")
                LOGGER.info("Adding empty interface for %s", app_name)
                projects.append((app, None))
            else:
                ems = CsvEMS()
                ems.parse_definition(config)
                projects.append((app, ems))
    return projects


def correct_type(left_spec, right_spec):
    """Check if the type is the same in two specifications.

    Args:
        left_spec (dict): Signal specification
        right_spec (dict): Signal specification to compare with
    Returns:
        matches (bool): Spec1 and Spec2 has the same type
    """
    return left_spec["type"] == right_spec["type"]


def correct_attribute(left_spec, right_spec, attribute, default=None, check_bool=True):
    """Check attributes other than type.

    Args:
        left_spec (dict): Signal specification
        right_spec (dict): Signal specification to compare with
        attribute (string): Attribute to check
        default (value): Default value for the attribute (default: None)
        check_bool (bool): Check signals of type Bool (default: True)
    Returns:
        matches (bool): Spec1 and Spec2 has the same value for the attribute
    """

    def _format(value):
        if isinstance(value, str):
            value = value.strip()
            if re.fullmatch("[+-]?[0-9]+", value):
                value = int(value)
            elif re.fullmatch("[+-]?[0-9]+[0-9.,eE+]*", value):
                value = float(value.replace(",", "."))
        return value

    if not check_bool and left_spec["type"] == "Bool":
        return True
    return _format(left_spec.get(attribute, default)) == _format(right_spec.get(attribute, default))


def found_mismatch(name, left_spec, right_spec, attribute, left_path, right_path):
    """Handle finding a mismatch.

    Args:
        name (string): Name of signal
        left_spec (dict): Spec of signal
        right_spec (dict): Signal specification to compare with
        attribute (string): Attribute to check
        left_path (list(str)): Path for where the left signals' definitions come from
        right_path (list(str)): Path for where the right signals' definitions come from
    """
    if attribute in ["type", "width"]:
        # TODO: Add more properties as serious when the interfaces are more cleaned up
        LOGGER.error(
            "%s has %ss: %s in %s and %s in %s",
            name,
            attribute,
            left_spec.get(attribute),
            left_path,
            right_spec.get(attribute),
            right_path,
        )
        return True
    LOGGER.info(
        "%s has %ss: %s in %s and %s in %s",
        name,
        attribute,
        left_spec.get(attribute),
        left_path,
        right_spec.get(attribute),
        right_path,
    )
    return False


def check_external_signals(ems, app, model_names=None):
    """Look for external signal mismatches.

    Args:
        ems (CsvEMS): Parsed signal interface cvs:s
        app (Application): Parsed project config
        model_names (list(Model)): models based on parsed config jsons
    Returns:
        serious_mismatch (bool): A serious mismatch was found
    """
    serious_mismatch = False

    LOGGER.debug("Checking insignals")
    errors = {"type": 0, "range": 0, "unit": 0, "width": 0}
    app_models = app.get_models()
    for model in app_models:
        if model_names is not None and model.name not in model_names:
            LOGGER.debug("Skipping %s in %s", model.name, app.name)
            continue
        LOGGER.debug("Checking %s in %s", model.name, app.name)
        serious_mismatch |= check_signals(
            get_active_signals(model.insignals, app.pybuild["feature_cfg"]),
            ems.outsignals,
            errors,
            [app.name, model.name],
            [ems.name],
        )
        serious_mismatch |= check_signals(
            get_active_signals(model.outsignals, app.pybuild["feature_cfg"]),
            ems.insignals,
            errors,
            [app.name, model.name],
            [ems.name],
        )
    LOGGER.debug("Total errors: %s", errors)
    return serious_mismatch


def check_signals(left_signals, right_signals, errors, left_path=None, right_path=None):
    """Compares insignals from one system with the outsignals of another.

    Args:
        left_signals (list(Signal)): Insignals of one system such as a model
        right_signals (list(Signal)): Outsignals of system to compare with
        errors (dict): Object for counting errors of different types
        left_path (list(str)): Path for where the left signals' definitions come from
        right_path (list(str)): Path for where the right signals' definitions come from
    Returns:
        serious_mismatch (bool): A serious mismatch was found
    """
    left_path = [] if left_path is None else left_path
    right_path = [] if right_path is None else right_path
    serious_mismatch = False
    LOGGER.debug("Checking from %s", left_signals)
    LOGGER.debug("Checking against %s", right_signals)
    for (left_signal, right_signal) in [
        (left, right) for left, right in product(left_signals, right_signals) if left.name == right.name
    ]:
        LOGGER.debug("Comparing %s and %s", left_signal, right_signal)
        left_properties = left_signal.properties
        right_properties = right_signal.properties
        LOGGER.debug("Properties left: %s", left_properties)
        LOGGER.debug("Properties right: %s", right_properties)
        if not correct_type(left_properties, right_properties):
            serious_mismatch |= found_mismatch(
                left_signal.name, left_properties, right_properties, "type", left_path, right_path
            )
            errors["type"] += 1
        if not correct_attribute(left_properties, right_properties, "min", check_bool=False):
            serious_mismatch |= found_mismatch(
                left_signal.name, left_properties, right_properties, "min", left_path, right_path
            )
            errors["range"] += 1
        if not correct_attribute(left_properties, right_properties, "max", check_bool=False):
            serious_mismatch |= found_mismatch(
                left_signal.name, left_properties, right_properties, "max", left_path, right_path
            )
            errors["range"] += 1
        if not correct_attribute(left_properties, right_properties, "unit", default="", check_bool=False):
            serious_mismatch |= found_mismatch(
                left_signal.name, left_properties, right_properties, "unit", left_path, right_path
            )
            errors["unit"] += 1
        if not correct_attribute(left_properties, right_properties, "width", default=1):
            serious_mismatch |= found_mismatch(
                left_signal.name, left_properties, right_properties, "width", left_path, right_path
            )
            errors["width"] += 1
    return serious_mismatch


PARSER_HELP = dedent(r"""
    Checks attributes and existence of signals

    Produced but not consumed signals are giving warnings
    Consumed but not produced signals are giving errors

    Attributes checked are: types, ranges, units and widths
    Mismatches in types or widths give errors
    Mismatches in min, max or unit gives warnings

    Examples:
    py -3.6 -m powertrain_build.check_interface models_in_projects <Projects> <Models/ModelGroup>\
            --projects <ProjectOne> <ProjectTwo>
    Checks models in Models/ModelGroup against ProjectOne and ProjectTwo in the folder Projects

    py -3.6 -m powertrain_build.check_interface models <Models> --models <ModelOne> <ModelTwo>
    Checks models ModelOne and ModelTwo against all other models in the folder Models

    py -3.6 -m powertrain_build.check_interface projects <Projects> \
            --projects ProjectOne ProjectTwo ProjectThree
    Checks the interfaces of ProjectOne, ProjectTwo and ProjectThree in the folder Projects
""").strip()


def configure_parser(parser: argparse.ArgumentParser):
    """Configure arguments in parser."""
    subparsers = parser.add_subparsers(
        help="help for subcommand",
        dest="mode",
        required=True,
    )

    # create the parser for the different commands
    model = subparsers.add_parser(
        "models",
        description=dedent("""
            Check models independently of projects.

            All signals are assumed to be active.
            Any signal that gives and error is used in a model but is not produced in any model or project
            interface.
        """).strip(),
    )
    add_model_args(model)
    model.set_defaults(func=model_check)

    project = subparsers.add_parser(
        "projects",
        description=dedent("""
            Check projects as a whole.

            It checks all models intenally and the SPM vs the interface.
        """).strip(),
    )
    add_project_args(project)
    project.set_defaults(func=projects_check)

    models_in_projects = subparsers.add_parser(
        "models_in_projects",
        description=dedent("""
            Check models specifically for projects.

            Codeswitches are used to determine if the signals are produced and consumed in each model.
        """).strip(),
    )
    add_project_args(models_in_projects)
    add_model_args(models_in_projects)
    models_in_projects.add_argument("--properties", help="Check properties such as type", action="store_true")
    models_in_projects.add_argument("--existence", help="Check signal existence consistency", action="store_true")
    models_in_projects.set_defaults(func=models_in_projects_check)


def add_project_args(parser: argparse.ArgumentParser):
    """Add project arguments to subparser"""
    parser.add_argument("project_root", help="Path to start looking for projects", type=Path)
    parser.add_argument(
        "--projects", help="Name of projects to check. Matches both path and interface name.", nargs="+"
    )


def add_model_args(parser: argparse.ArgumentParser):
    """Add model arguments to subparser"""
    parser.add_argument("model_root", help="Path to start looking for models", type=Path)
    parser.add_argument("--models", help="Name of models to check", nargs="+")
    parser.add_argument("--gerrit", action="store_true", help="Deprecated")
    parser.add_argument("--git", action="store_true", help="Get models to check from git HEAD")


def get_changed_models():
    """Get changed models in current commit."""
    repo = git.Repo()
    changed_files_tmp = repo.git.diff("--diff-filter=d", "--name-only", "HEAD~1")
    changed_files = changed_files_tmp.splitlines()
    changed_models = [m for m in changed_files if m.endswith(".mdl") or m.endswith(".slx")]
    return changed_models


def model_path_to_name(model_paths):
    """Extract model names from a list of model paths."""
    model_names = []
    for model_path in model_paths:
        model_name_with_extension = model_path.split("/")[-1]
        model_name = model_name_with_extension.split(".")[0]
        model_names.append(model_name)
    return model_names


def model_check(args: argparse.Namespace):
    """Entry point for models command."""
    serious_mismatch = False
    all_models = get_all_models(args.model_root)
    if args.models is not None:
        model_names = args.models
    elif args.git or args.gerrit:
        # Still checking args.gerrit due to common-linux-signal_consistency in pt-zuul-jobs
        model_paths = get_changed_models()
        model_names = model_path_to_name(model_paths)
    else:
        model_names = [model.name for model in all_models]

    serious_mismatch |= check_models_generic(all_models, model_names, [])

    if serious_mismatch:
        LOGGER.error("Serious interface errors found.")

    return serious_mismatch


def projects_check(args: argparse.Namespace):
    """Entry point for projects command."""
    serious_mismatch = False
    projects = get_projects(args.project_root, args.projects)
    for app, ems in projects:
        LOGGER.info("Checking interfaces for %s", app.name)
        serious_mismatch |= check_internal_signals(app, None)
        if ems is not None:
            serious_mismatch |= check_external_signals(ems, app, None)

    if serious_mismatch:
        LOGGER.error("Serious interface errors found.")

    return serious_mismatch


def models_in_projects_check(args: argparse.Namespace):
    """Entry point for models_in_projects command."""
    serious_mismatch = False
    projects = get_projects(args.project_root, args.projects)
    LOGGER.debug("Checking projects: %s", projects)
    if args.properties:
        for app, ems in projects:
            serious_mismatch |= check_internal_signals(app, None or args.models)
            if ems is not None:
                serious_mismatch |= check_external_signals(ems, app, None or args.models)
    if args.existence:
        all_models = get_all_models(args.model_root)
        model_names = [model.name for model in all_models] if args.models is None else args.models
        serious_mismatch |= signal_existence(projects, model_names)

    if serious_mismatch:
        LOGGER.error("Serious interface errors found.")

    return serious_mismatch


def signal_existence(projects, model_names):
    """Check which signals are consumed and produced in each project."""
    serious_mismatch = False
    for app, ems in projects:
        app_models = app.get_models()
        LOGGER.info("Checking %s", app.name)
        for project_model in app_models:
            if project_model.name not in model_names:
                continue
            LOGGER.debug("Checking signal existence for %s", project_model.name)
            active_insignals = get_active_signals(project_model.insignals, app.pybuild["feature_cfg"])
            active_outsignals = get_active_signals(project_model.outsignals, app.pybuild["feature_cfg"])
            insignal_matches = {}
            outsignal_matches = {}
            for check_model in app_models:
                signal_match(
                    active_insignals,
                    get_active_signals(check_model.outsignals, app.pybuild["feature_cfg"]),
                    insignal_matches,
                )
                signal_match(
                    active_outsignals,
                    get_active_signals(check_model.insignals, app.pybuild["feature_cfg"]),
                    outsignal_matches,
                )
            if ems is not None:
                signal_match(active_insignals, ems.outsignals, insignal_matches)
                signal_match(active_outsignals, ems.insignals, outsignal_matches)
            for missing_signal in [signal for signal, matched in insignal_matches.items() if not matched]:
                # serious_mismatch = True  # TODO: Activate this code when we want to gate on it.
                LOGGER.warning(
                    "%s is consumed in %s but never produced in %s", missing_signal, project_model.name, app.name
                )
            for missing_signal in [signal for signal, matched in insignal_matches.items() if not matched]:
                LOGGER.debug("%s is consumed in %s and produced in %s", missing_signal, project_model.name, app.name)
            for missing_signal in [signal for signal, matched in outsignal_matches.items() if not matched]:
                LOGGER.info(
                    "%s is produced in %s but never consumed in %s", missing_signal, project_model.name, app.name
                )
            for missing_signal in [signal for signal, matched in outsignal_matches.items() if not matched]:
                LOGGER.debug("%s is consumed in %s and produced in %s", missing_signal, project_model.name, app.name)
    return serious_mismatch


def signal_match(signals_to_check, signals_to_check_against, matches):
    """Check for matches in signal names."""
    for a_signal in signals_to_check:
        matches[a_signal.name] = matches.get(a_signal.name, False)
        for b_signal in signals_to_check_against:
            if b_signal.name == a_signal.name:
                matches[a_signal.name] = True


def main(argv: Optional[List[str]] = None):
    """Main function for stand alone execution."""
    parser = argparse.ArgumentParser(
        description=PARSER_HELP,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    configure_parser(parser)
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])
