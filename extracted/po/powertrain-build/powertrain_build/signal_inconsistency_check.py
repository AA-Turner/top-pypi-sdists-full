# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

""" script for running running signal consistency check on specific models. Git HEAD or local.
"""

import argparse
import csv
import os
import sys
from collections import defaultdict
from os.path import join
from pathlib import Path
from typing import List, Optional

import git

from powertrain_build.build_proj_config import BuildProjConfig
from powertrain_build.feature_configs import FeatureConfigs
from powertrain_build.lib import helper_functions, logger
from powertrain_build.signal_incons_html_rep_all import SigConsHtmlReportAll
from powertrain_build.signal_interfaces import CsvSignalInterfaces, YamlSignalInterfaces
from powertrain_build.unit_configs import UnitConfigs
from powertrain_build.user_defined_types import UserDefinedTypes

LOGGER = logger.create_logger(__file__)
EXIT_CODE_OK = 0
EXIT_CODE_UNPRODUCED = 1
EXIT_CODE_MISSING_CONSUMER = 2
EXIT_CODE_INCORRECT_UNCONSUMED_CSV = 4
EXIT_CODE_INCORRECT_UNPRODUCED_CSV = 8
EXIT_CODE_NEVER_ACTIVE_SIGNALS = 16
UNCONSUMED_SIGNAL_FILE_PATTERN = "*_Unconsumed_Sig.csv"
UNPRODUCED_SIGNAL_FILE_PATTERN = "*_Unproduced_Sig.csv"
MODEL_ROOT_DIR = "Models"
REPO_ROOT = helper_functions.get_repo_root()
MISSING_CONSUMER_CONSOLE_MESSAGE = (
    "\n===============Unused signals===============\n{signals}"
)
UNPRODUCED_SIGNALS_CONSOLE_MESSAGE = (
    "\n=============Unproduced signals=============\n{signals}"
)
UNCONSUMED_CSV_CONSOLE_MESSAGE = "\n=========Signals defined in unconsumed.csv-s that are consumed=========\n{signals}"
UNPRODUCED_CSV_CONSOLE_MESSAGE = "\n=========Signals defined in unproduced.csv-s that are produced=========\n{signals}"
NEVER_ACTIVE_SIGNALS_CONSOLE_MESSAGE = (
    "\n============Never active signals=============\n{signals}"
)
INDEX_FILE = "Reports/Index_SigCheck_All.html"
TEMPLATE = """<!DOCTYPE html>
<!--[if IE 8]><html class="no-js lt-ie9" lang="en" > <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en" > <!--<![endif]-->

<body class="wy-body-for-nav">

<a class="icon icon-home">      Signal Consistency Report
</a>
<ul>
<li class="toctree-l1">
    <a class="reference internal" href="SigCheckAll_intro.html">Introduction</a>
</li>
{project_rows}
</ul>
</body>
</html>"""

PARSER_HELP = "Run signal inconsistency check."


def gen_sig_incons_index_file(project_list):
    """Generate Index_SigCheck_All.html."""
    # TODO Remove function and add as method in powertrain_build/signal_incons_html_rep_all.py
    rows = ""
    project_row = """<li class="toctree-l1"><a class="reference internal"
                   href="SigCheckAll_{project}.html">SigCheckAll {project}</a></li>\n"""
    for prj in project_list:
        rows += project_row.format(project=prj)
    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
    with open(INDEX_FILE, "w", encoding="utf-8") as f_h:
        f_h.write(TEMPLATE.format(project_rows=rows))


def configure_parser(parser: argparse.ArgumentParser):
    """Parse the arguments sent to the script."""
    parser.add_argument(
        '-p',
        '--project-folders',
        nargs='+',
        default=['Projects'],
        help='Directories to look for project configurations.'
    )
    parser.add_argument(
        "-m",
        "--models",
        nargs="+",
        help="Arguments for running in local repo. "
        "Name of models to run test on Ex: VcDepExt VcAcCtrl. "
        "If not supplied, changed files in current commit will be used. "
        "Reports are stored in local repo",
    )
    parser.add_argument(
        "-r", "--report", help="Create report for all projects", action="store_true"
    )
    parser.set_defaults(func=run_signal_inconsistency_check)


def get_project_configs(project_folders):
    """Wrapper for creating project configs for all projects.

    Args:
        project_folders (list): List of project folders to look for project configs in.
    Returns
        prj_cfgs (dict): Project configs.
    """
    project_config_files = []
    root_path = Path().resolve()
    for project_folder in project_folders:
        found_files = root_path.glob(f"{project_folder}/**/ProjectCfg.json")
        project_config_files.extend(list(map(lambda x: x.as_posix(), found_files)))
    prj_cfgs = {}
    for project_config_file in project_config_files:
        LOGGER.debug("Get project config for %s", project_config_file)
        project_config = BuildProjConfig(os.path.normpath(project_config_file))
        prj_cfgs.update({project_config.name: project_config})
    return prj_cfgs


def check_inconsistency(signal_ifs, never_active_signals):
    """Check signal inconsistency.
    Args:
        signal_ifs (CsvSignalInterfaces): class holding signal interface information.
        never_active_signals (dict): Dict of projects mapped to units mapped to "NEVER_ACTIVE" signals.
    Returns:
        inconsistency result (dict)
    """
    signal_inconsistency_results = {}
    for key, signal_if in signal_ifs.items():
        partial_result = signal_if.check_config()
        signal_inconsistency_results.update({key: partial_result})
        signal_inconsistency_results[key].update(
            {"never_active_signals": never_active_signals[key]}
        )
    return signal_inconsistency_results


def get_signal_interfaces(prj_cfgs, models):
    """Wrapper for creating signal interface dict for all configs.
    Args:
        Project config.
    Returns:
           Signal interface dict.
    """
    signal_ifs = {}
    per_unit_cfgs = {}
    for prj, prj_cfg in prj_cfgs.items():
        LOGGER.info("Parsing interface %s", prj)

        feature_cfg = FeatureConfigs(prj_cfg)
        unit_cfg = UnitConfigs(prj_cfg, feature_cfg)
        user_defined_types = UserDefinedTypes(prj_cfg, unit_cfg)

        if prj_cfg.has_yaml_interface:
            signal_if = YamlSignalInterfaces(
                prj_cfg, unit_cfg, feature_cfg, user_defined_types, model_names=models
            )
        else:
            signal_if = CsvSignalInterfaces(prj_cfg, unit_cfg, models)

        signal_ifs.update({prj: signal_if})
        per_unit_cfgs.update({prj: unit_cfg.get_per_unit_cfg()})

    return signal_ifs, per_unit_cfgs


def get_never_active_signals(prj_cfgs, models):
    """Functions for getting all signals marked as "NEVER_ACTIVE" in all projects.

    Args:
        prj_cfgs (list(BuildProjConfig)): List of project configurations to look for never active signals in.
        models (list): List of Simulink models to check.
    Returns:
        never_active_signals (dict): Dict of projects mapped to units mapped to its "NEVER_ACTIVE" signals.
    """
    never_active_signals = {}
    for prj, prj_cfg in prj_cfgs.items():
        LOGGER.info("searching for never active signals in %s", prj)
        feature_cfg = FeatureConfigs(prj_cfg)
        unit_cfg = UnitConfigs(prj_cfg, feature_cfg)
        per_unit_cfg_total = unit_cfg.get_per_unit_cfg_total()
        never_active_signals[prj] = {}
        for unit, unit_data in per_unit_cfg_total.items():
            if unit not in models:
                continue
            inactive_inports = []
            inactive_outports = []
            for inport, inport_data in unit_data["inports"].items():
                if "NEVER_ACTIVE" in inport_data["configs"]:
                    inactive_inports.append(inport)
            for outport, outport_data in unit_data["outports"].items():
                if "NEVER_ACTIVE" in outport_data["configs"]:
                    inactive_outports.append(outport)
            if inactive_inports or inactive_outports:
                never_active_signals[prj].update(
                    {unit: inactive_inports + inactive_outports}
                )

    return never_active_signals


class SignalInconsistency:
    """Class for running signal consistency check on specific models. Git HEAD or local."""

    def __init__(self, args):
        """Models in local repo."""
        self.never_active_signals = {}
        self.signal_inconsistency_results = {}
        self.per_unit_cfgs = {}
        self.signal_ifs = {}
        self.repo = git.Repo()
        if args.models:
            self.models = args.models
        else:
            mdl_file_paths = self.get_changed_models()
            self.models = self._get_model_names(mdl_file_paths)

    @staticmethod
    def _get_model_names(mdl_paths):
        """Get Change Model names."""
        mdl_index = 1
        return [os.path.split(i)[mdl_index].replace(".mdl", "") for i in mdl_paths]

    def _create_reports(self):
        """Create reports for all projects."""
        sig_report = SigConsHtmlReportAll(self.signal_inconsistency_results)
        sig_report.generate_report_file_signal_check(
            join(REPO_ROOT, "Reports", "SigCheckAll")
        )

    def _sort_internal_inconsistency_by_model(self):
        """Sort inconsistency by model."""
        sig = self.signal_inconsistency_results
        no_producer_int = {}
        missing_consumer_int = {}
        never_active_int = {}
        for project, val in sig.items():
            int_dict = val["sigs"]["int"]
            for mdl, data in int_dict.items():
                if data.get("missing"):
                    if mdl not in no_producer_int:
                        no_producer_int[mdl] = self._to_tuple_list(
                            project, data["missing"]
                        )
                    else:
                        no_producer_int[mdl] += self._to_tuple_list(
                            project, data["missing"]
                        )
                if data.get("unused"):
                    if mdl not in missing_consumer_int:
                        missing_consumer_int[mdl] = self._to_tuple_list(
                            project, data["unused"]
                        )
                    else:
                        missing_consumer_int[mdl] += self._to_tuple_list(
                            project, data["unused"]
                        )
            for mdl, never_active_signals in val["never_active_signals"].items():
                never_active_int[mdl] = [
                    (signal, {project}) for signal in never_active_signals
                ]

        return (
            self._merge_tuple_list(no_producer_int),
            self._merge_tuple_list(missing_consumer_int),
            self._merge_tuple_list(never_active_int),
        )

    def _analyse_inconsistency(self):
        """Collect signals.

        Args:
            no_producer_int (dict): Consumed signals but not produced.
            missing_consumer_int (dict): Produced signals but not consumed.
        """
        exit_code = EXIT_CODE_OK
        log_message = ""
        (
            no_producer_int,
            missing_consumer_int,
            never_active_int,
        ) = self._sort_internal_inconsistency_by_model()
        used_model_inports = self.aggregate_model_inports()
        used_model_outports = self.aggregate_model_outports()
        used_external_outports = self.aggregate_supplier_inports()
        used_external_inports = self.aggregate_supplier_outports()
        exit_code_unproduced, unproduced_message = self.check_unproduced_signals(
            no_producer_int
        )
        (
            exit_code_missing_consumer,
            missing_consumer_message,
        ) = self.check_missing_consumer_signals(missing_consumer_int)
        exit_code_used_inports, used_inports_message = self.check_unconsumed_files(
            used_model_inports, used_external_outports
        )
        exit_code_used_outports, used_outports_message = self.check_unproduced_files(
            used_model_outports, used_external_inports
        )
        exit_code_never_active, never_active_message = self.check_never_active_signals(
            never_active_int
        )
        log_message += unproduced_message
        log_message += missing_consumer_message
        log_message += used_inports_message
        log_message += used_outports_message
        log_message += never_active_message
        exit_code += exit_code_unproduced
        exit_code += exit_code_missing_consumer
        exit_code += exit_code_used_inports
        exit_code += exit_code_used_outports
        exit_code += exit_code_never_active
        return exit_code, log_message

    def get_changed_models(self):
        """Get changed models in current commit."""
        changed_files_tmp = self.repo.git.diff(
            "--diff-filter=d", "--name-only", "HEAD~1"
        )
        changed_files = changed_files_tmp.splitlines()
        changed_models = [
            m for m in changed_files if m.endswith(".mdl") or m.endswith(".slx")
        ]
        return changed_models

    def check_unproduced_signals(self, unproduced_signals):
        """Check if models expects signals that is not produced.
        Args:
            unproduced_signals (dict):
                                     mdl:{signals:{projects...}...}...
        Returns:
               exit_code (int):
                              Number of unproduced signals in checked models.
               console message (string):
                                      Shows if models has unproduced signals.
        """
        error_message = ""
        exit_code = EXIT_CODE_OK
        unproduced_skip_list = self.fetch_signals_to_skip(skip_list_file_pattern=UNPRODUCED_SIGNAL_FILE_PATTERN)
        models_with_unproduced_signals = {
            m for m in unproduced_signals.keys() if m in self.models
        }
        for mdl in models_with_unproduced_signals:
            sigs = unproduced_signals[mdl]
            for k in set(sigs.keys()):
                if mdl in unproduced_skip_list and k in unproduced_skip_list[mdl]:
                    del sigs[k]
            if mdl in unproduced_signals and unproduced_signals[mdl]:
                error_message += self._format_console_output(mdl, unproduced_signals[mdl])
                exit_code = EXIT_CODE_UNPRODUCED
        return exit_code, UNPRODUCED_SIGNALS_CONSOLE_MESSAGE.format(
            signals=error_message
        )

    def check_missing_consumer_signals(self, missing_consumer_signals):
        """Check if models expect signals that is not produced.
        Args:
            missing_consumer_signals (dict):
                                     mdl:{signals:{projects...}...}...
        Returns:
               exit_code (int):
                              Number of unproduced signals in checked models.
               console message (string):
                                      Shows if models has unproduced signals.
        """
        error_message = ""
        exit_code = EXIT_CODE_OK
        unconsumed_skip_list = self.fetch_signals_to_skip()
        models_producing_not_consumed_signals = {
            m for m in missing_consumer_signals.keys() if m in self.models
        }
        for mdl in models_producing_not_consumed_signals:
            sigs = missing_consumer_signals[mdl]
            for k in set(sigs.keys()):
                if mdl in unconsumed_skip_list and k in unconsumed_skip_list[mdl]:
                    del sigs[k]
            if mdl in missing_consumer_signals and missing_consumer_signals[mdl]:
                error_message += self._format_console_output(mdl, missing_consumer_signals[mdl])
                exit_code = EXIT_CODE_MISSING_CONSUMER
        return exit_code, MISSING_CONSUMER_CONSOLE_MESSAGE.format(signals=error_message)

    def check_unconsumed_files(self, inports, ifs_outports):
        """Check that signals defined in unconsumed.csv files are not being consumed
        Args:
            inports (set): all models inports in all projects.
            ifs_outports (set): all outports, all projects and all interfaces.
        Returns:
               exit_code (int):
               console message (string): Console error message (if test fail)
        """
        error_message_int = ""
        error_message_ext = ""
        error_message = ""
        exit_code = EXIT_CODE_OK
        unconsumed_skip_list = self.fetch_signals_to_skip()

        for producing_mdl, signals in unconsumed_skip_list.items():
            signal_intersect_int = signals & inports
            signal_intersect_ext = signals & ifs_outports
            if signal_intersect_int:
                exit_code, error_message_int = self.get_unconsumed_intersect_exit_code(
                    producing_mdl, signal_intersect_int
                )
            if signal_intersect_ext:
                exit_code, error_message_int = self.get_unconsumed_intersect_exit_code(
                    producing_mdl, signal_intersect_ext, False
                )
        error_message += error_message_int
        error_message += error_message_ext
        return exit_code, UNCONSUMED_CSV_CONSOLE_MESSAGE.format(signals=error_message)

    def check_unproduced_files(self, outports, ifs_inports):
        """Check that signals defined in unproduced.csv files are not being produced
        Args:
            outports (set): all models outports in all projects.
            ifs_inports (set): all inports, all projects and all interfaces.
        Returns:
               exit_code (int):
               console message (string): Console error message (if test fail)
        """
        error_message_int = ""
        error_message_ext = ""
        error_message = ""
        exit_code = EXIT_CODE_OK
        unproduced_skip_list = self.fetch_signals_to_skip(
            skip_list_file_pattern=UNPRODUCED_SIGNAL_FILE_PATTERN
        )
        for consuming_mdl, signals in unproduced_skip_list.items():
            signal_intersect_int = signals & outports
            signal_intersect_ext = signals & ifs_inports
            if signal_intersect_int:
                exit_code, error_message_int = self.get_unproduced_intersect_exit_code(
                    consuming_mdl, signal_intersect_int
                )
            if signal_intersect_ext:
                exit_code, error_message_int = self.get_unproduced_intersect_exit_code(
                    consuming_mdl, signal_intersect_ext, False
                )
        error_message += error_message_int
        error_message += error_message_ext
        return exit_code, UNPRODUCED_CSV_CONSOLE_MESSAGE.format(signals=error_message)

    def check_never_active_signals(self, never_active_signals):
        """Check if there are any never active signals.
        Produce corresponding error code and message.

        Args:
            never_active_signals (dict): Dict mapping models to never active signals in projects.
        Returns:
            exit_code (int):
            console message (string): Console error message (if test fail)
        """
        error_message = ""
        exit_code = EXIT_CODE_OK
        if never_active_signals:
            exit_code = EXIT_CODE_NEVER_ACTIVE_SIGNALS
            for mdl, signals in never_active_signals.items():
                error_message += self._format_console_output(mdl, signals)

        return exit_code, NEVER_ACTIVE_SIGNALS_CONSOLE_MESSAGE.format(
            signals=error_message
        )

    def get_unconsumed_intersect_exit_code(self, producing_mdl, signal_intersect, int_signals=True):
        """Determine if Unconsumed.csv and used inport signals overlap per project.
        Return exit code and which consumer and project is cause of failure.
        Args:
            producing_mdl (String): Model name.
            signal_intersect (set): Unconsumed.csv signals and used inports that overlap.
            int_signals (bool):
                              True: Set exit code for internally overlaping signals (Models)
                              False: Set exit code for external overlaping signals (Supplier)
        Returns:
               exit_code (int): Fail or succes
               error_message (String): Consumers.
        """
        exit_code = EXIT_CODE_OK
        console_message = "{producer}\n {signal} is consumed by {consumer} in {prj}\n"
        error_message = ""
        for sig in signal_intersect:
            if int_signals:
                consumers = self.get_users_int(sig)
            else:
                consumers = self.get_users_ext(sig)
            for unit, prj in consumers:
                if self.mdl_is_user_in_prj(producing_mdl, prj, sig):
                    error_message += console_message.format(
                        producer=producing_mdl, signal=sig, consumer=unit, prj=prj
                    )
                    exit_code = EXIT_CODE_INCORRECT_UNCONSUMED_CSV
        return exit_code, error_message

    def get_unproduced_intersect_exit_code(self, producing_mdl, signal_intersect, int_signals=True):
        """Determine if Unproduced.csv and used outport signals overlap per project.
        Return exit code and which producer and project is cause of failure.
        Args:
            producing_mdl (String): Model name.
            signal_intersect (set): Unproduced.csv signals and used outports that overlap.
            int_signals (bool):
                              True: Set exit code for internally overlaping signals (Models)
                              False: Set exit code for external overlaping signals (Supplier)
        Returns:
               exit_code (int): Fail or succes
               error_message (String): Producers.
        """
        exit_code = EXIT_CODE_OK
        console_message = "{consumer}\n {signal} is produced by {producer} in {prj}\n"
        error_message = ""
        for sig in signal_intersect:
            if int_signals:
                producers = self.get_users_int(sig, direction="outports")
            else:
                producers = self.get_users_ext(sig, direction="outports")
            for unit, prj in producers:
                if self.mdl_is_user_in_prj(producing_mdl, prj, sig, direction="inports"):
                    error_message += console_message.format(
                        consumer=producing_mdl, signal=sig, producer=unit, prj=prj
                    )
                    exit_code = EXIT_CODE_INCORRECT_UNPRODUCED_CSV
        return exit_code, error_message

    def mdl_is_user_in_prj(self, mdl, prj, signal, direction="outports"):
        """Check that defined signal in <mdl>un-consumed/produced.csv is used in project"""
        try:
            return signal in self.per_unit_cfgs[prj][mdl][direction].keys()
        except KeyError:
            return False

    def get_users_int(self, signal, direction="inports"):
        """Find internal users of signal"""
        signal_users = []
        for prj, unit_cfgs in self.per_unit_cfgs.items():
            for unit, unit_cfg in unit_cfgs.items():
                if signal in unit_cfg[direction].keys():
                    signal_users.append((unit, prj))
        return signal_users

    def get_users_ext(self, signal, direction="inports"):
        """Find external users of signal.
        Reverse logic, "inports" direction means external outputs and vice versa.
        """
        signal_users = []
        for prj, if_output in self.signal_ifs.items():
            if direction == "inports":
                signal_data = if_output.get_external_outputs()
            else:
                signal_data = if_output.get_external_inputs()
            for sig_type, signals in signal_data.items():

                if signal in signals.keys():
                    signal_users.append((sig_type, prj))
        return signal_users

    @staticmethod
    def _format_console_output(mdl, signal_dict):
        out = ""
        for signal, projects in signal_dict.items():
            out += " " + str(signal) + str(projects) + "\n"
        return f"\n{mdl}\n{out} \n"

    @staticmethod
    def _to_tuple_list(project, signal_project_dict):
        """Create list of tuples.

        NOTE: signal_project_dict is no longer a signal to project mapping.
        It was when PyBuild handled multiple projects at once.

        Args:
            project (str): project name.
            signal_project_dict (dict): signal1: {}, signal2: {}...
        Returns:
               list: [(signal1, {project}), (signal2, {project})...]
        """
        return [(signal, {project}) for signal in signal_project_dict.keys()]

    @staticmethod
    def _merge_tuple_list(t_list):
        """Merged list of tuples.
        Args (list(tuple...)):
                             [(A,1), (A,2), (C,1)]

        Returns (list(tuple...)):
                                [(A,[1,2]), (C,1)]
        """
        model_confs = {}
        for mdl, sig_prj_pair in t_list.items():
            model_conf = defaultdict(list)
            for signal, prj in sig_prj_pair:
                model_conf[signal].append(prj)
            model_confs[mdl] = model_conf
        return model_confs

    def fetch_signals_to_skip(
        self, model_root_dir=MODEL_ROOT_DIR, skip_list_file_pattern=UNCONSUMED_SIGNAL_FILE_PATTERN
    ):
        """fetch signals to skip from csv files.
        Returns:
               signals_to_skip (dict):
                                        {model: {sig1, sig2...}, model2: {sig1, sig2...}}
        """
        signals_to_skip = {mdl: set() for mdl in self.models}
        # "mdl_name" = "mdl folder name". '..\\..\\mdl_name\\pybuild_cfg\\mdl_pattern_Sig.csv'
        model_dir_index = -3
        signal_col_index = 0
        for file_name in Path(model_root_dir).glob(
            "**/" + skip_list_file_pattern
        ):
            mdl_name = str(file_name).split(os.sep)[model_dir_index]
            if mdl_name in self.models:
                with file_name.open() as csv_file:
                    csv_reader = csv.reader(csv_file)
                    next(csv_reader)  # Skip header.
                    for row in csv_reader:
                        signals_to_skip[mdl_name].add(row[signal_col_index])
        return signals_to_skip

    @staticmethod
    def _print_console_log_info(exit_code):
        """Prints explanatory message to console.
        NOTE: The exit_codes_messages variable needs the messages to be in increasing order,
        according to the exit code constans above.
        """
        missing_producer = (
            "Model/Models is configured to consume signals that are not produced. "
            "Remove signal or fix/add producer."
        )
        missing_consumer = (
            "Model/Models creates signals that are not consumed. "
            "Remove or add to <mdl>_Unconsumed.csv."
        )
        incorrect_unconsumed_csv = (
            "Consumed signals is defined in <mdl>_Unconsumed.csv. "
            "Remove signals or fix/remove consumer."
        )
        incorrect_unproduced_csv = (
            "Produced signals is defined in <mdl>_Unproduced.csv. "
            "Remove signals or fix/remove producer."
        )
        never_active_signals = (
            "Never active signals will not appear in generated .c file. "
            "Remove corresponding part in Simulink model, signals probablty lead to terminators."
        )
        exit_codes_messages = [
            missing_producer,
            missing_consumer,
            incorrect_unconsumed_csv,
            incorrect_unproduced_csv,
            never_active_signals,
        ]
        exit_code_bit_field = [
            bool(int(b)) for b in bin(exit_code)[2:]
        ]  # [2:] gets rid of 0b part
        exit_code_bit_field.reverse()  # Reverse to match exit_codes_messages order
        for idx, value in enumerate(exit_code_bit_field):
            if value:
                LOGGER.info(exit_codes_messages[idx])

    def aggregate_model_inports(self):
        """Aggregate inport signals from models"""
        used_inports = set()
        for unit_cfg in self.per_unit_cfgs.values():
            for inp in unit_cfg.values():
                used_inports = used_inports.union(set(inp["inports"].keys()))
        return used_inports

    def aggregate_supplier_inports(self):
        """Aggregate outports from signal interface (supplier inports)"""
        external_outports = set()
        for if_output in self.signal_ifs.values():
            for signals in if_output.get_external_outputs().values():
                external_outports = external_outports.union(set(signals.keys()))
        return external_outports

    def aggregate_model_outports(self):
        """Aggregate outport signals from models"""
        used_outports = set()
        for unit_cfg in self.per_unit_cfgs.values():
            for inp in unit_cfg.values():
                used_outports = used_outports.union(set(inp["outports"].keys()))
        return used_outports

    def aggregate_supplier_outports(self):
        """Aggregate inports from signal interface (supplier outports)"""
        external_inports = set()
        for if_output in self.signal_ifs.values():
            for signals in if_output.get_external_inputs().values():
                external_inports = external_inports.union(set(signals.keys()))
        return external_inports

    def run(self, args):
        """Run signal inconsistency check."""
        exit_code = EXIT_CODE_OK
        if self.models:
            prj_cfs = get_project_configs(args.project_folders)
            self.signal_ifs, self.per_unit_cfgs = get_signal_interfaces(
                prj_cfs, self.models
            )
            self.never_active_signals = get_never_active_signals(prj_cfs, self.models)
            LOGGER.info("Start check signal inconsistencies for: %s", self.models)
            self.signal_inconsistency_results = check_inconsistency(
                self.signal_ifs, self.never_active_signals
            )
            exit_code, log_output = self._analyse_inconsistency()
            LOGGER.info("Finished check signal inconsistencies %s", log_output)
            self._print_console_log_info(exit_code)
            if args.report:
                LOGGER.info(
                    "Start generating interface inconsistencies html-report for all projects"
                )
                gen_sig_incons_index_file(
                    list(self.signal_inconsistency_results.keys())
                )
                self._create_reports()
                LOGGER.info("Finished - generating inconsistencies html-reports")
        else:
            LOGGER.info("No models in change")
        return exit_code


def run_signal_inconsistency_check(args: argparse.Namespace) -> int:
    """Create Signal Inconsistency instance and run checks."""
    sig_in = SignalInconsistency(args)
    return sig_in.run(args)


def main(argv: Optional[List[str]] = None) -> int:
    """Create Signal Inconsistency instance and run checks."""
    parser = argparse.ArgumentParser(description=PARSER_HELP)
    configure_parser(parser)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
