# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

# -*- coding: utf-8 -*-
"""Python module used for building a Vcc SPM SW release.

This is the entry point to powertrain-build which includes all other needed modules.
Loads configuration files and sequences the code generation steps.
"""

import glob
import logging
import os
import shutil
import sys
import time
from os.path import join as pjoin
from pathlib import Path

from powertrain_build import __config_version__, __version__
from powertrain_build.a2l_merge import A2lMerge
from powertrain_build.build_proj_config import BuildProjConfig
from powertrain_build.core import Core, HICore, ZCCore
from powertrain_build.core_dummy import CoreDummy
from powertrain_build.create_conversion_table import create_conversion_table
from powertrain_build.dids import DIDs, HIDIDs, ZCDIDs
from powertrain_build.dummy import DummyVar
from powertrain_build.dummy_spm import DummySpm
from powertrain_build.ext_dbg import ExtDbg
from powertrain_build.ext_var import ExtVarCsv, ExtVarCsvAsil, ExtVarYaml
from powertrain_build.feature_configs import FeatureConfigs
from powertrain_build.lib import logger
from powertrain_build.lib.helper_functions import create_dir, get_repo_root, merge_dicts
from powertrain_build.memory_section import MemorySection
from powertrain_build.nvm_def import NVMDef, ZCNVMDef
from powertrain_build.problem_logger import ProblemLogger
from powertrain_build.replace_compu_tab_ref import replace_tab_verb
from powertrain_build.rte_dummy import RteDummy
from powertrain_build.sched_funcs import SchedFuncs
from powertrain_build.signal_if_html_rep import SigIfHtmlReport
from powertrain_build.signal_incons_html_rep import SigConsHtmlReport
from powertrain_build.signal_interfaces import CsvSignalInterfaces, YamlSignalInterfaces
from powertrain_build.unit_configs import CodeGenerators, UnitConfigs
from powertrain_build.user_defined_types import UserDefinedTypes
from powertrain_build.zone_controller.calibration import ZoneControllerCalibration
from powertrain_build.zone_controller.composition_yaml import CompositionYaml

LOGGER = logger.create_logger(__file__)
REPO_ROOT = get_repo_root()


def setup_logging(log_dst_dir, problem_logger, debug=True, quiet=False):
    """Set up the python logger for the build environment.

    Three logger streams are set up. One that log to stdout (info level),
    and one to a build.log file (info level), and finally, on stream that
    logs to build_dbg.log (debug level log). The log files are put in the
    directory configured in the config file.

    Args:
        log_dst_dir (str): the path to where the log file should be stored
        problem_logger (obj): the ProblemLogger object to initialise
        debug (bool): True - if debug log shall be generated
        quiet (bool): False - disable logging to stdout

    """
    LOGGER.handlers.clear()
    LOGGER.setLevel(logging.INFO)
    logging.captureWarnings(True)
    # Setup debug build logger
    log_file = pjoin(log_dst_dir, "build_dbg.log")
    if debug:
        dbg = logging.FileHandler(log_file)
        dbg.setLevel(logging.DEBUG)
        dbg_formatter = logger.CustomFormatting()
        dbg.setFormatter(dbg_formatter)
        LOGGER.addHandler(dbg)
    # Setup normal build logger
    log_file = pjoin(log_dst_dir, "build.log")
    nrm = logging.FileHandler(log_file)
    nrm.setLevel(logging.INFO)
    build_log_frmt = logger.CustomFormatting()
    nrm.setFormatter(build_log_frmt)
    LOGGER.addHandler(nrm)

    if not quiet:
        nrm_strm = logging.StreamHandler(sys.stdout)
        nrm_strm.setLevel(logging.INFO)
        nrm_strm.setFormatter(build_log_frmt)
        LOGGER.addHandler(nrm_strm)

        error_strm = logging.StreamHandler(sys.stderr)
        error_strm.setLevel(logging.CRITICAL)
        error_strm.setFormatter(build_log_frmt)
        LOGGER.addHandler(error_strm)

    problem_logger.init_logger(LOGGER)


def check_interfaces(build_cfg, signal_if):
    """Check the interfaces.

    Checks interfaces in all configurations, and generates a html
    report with the result of the checks.

    Args:
        build_cfg (BuildProjConfig): Build project class holding where
            files should be stored
        signal_if (SignalInterfaces): class holding signal interface information

    """
    LOGGER.info("******************************************************")
    LOGGER.info("Start check interface inconsistencies")
    start_time = time.time()
    report_dst_dir = build_cfg.get_reports_dst_dir()
    signal_inconsistency_result = signal_if.check_config()
    sig_report = SigConsHtmlReport(signal_inconsistency_result)
    LOGGER.info(
        "Finished check interface inconsistencies (in %4.2f s)",
        time.time() - start_time,
    )

    start_time = time.time()
    LOGGER.info("******************************************************")
    LOGGER.info("Start generating interface inconsistencies html-report")
    sig_report.generate_report_file(pjoin(report_dst_dir, "SigCheck.html"))
    LOGGER.info(
        "Finished - generating interface inconsistencies html-report (in %4.2f s)",
        time.time() - start_time,
    )


def interface_report(build_cfg, unit_cfg, signal_if):
    """Create report of signal interfaces.

    Creates a report of interfaces in all configurations, and generates
    a html-report with the result of the checks.

    Args:
        build_cfg (BuildProjConfig): Build project class holding where
            files should be stored.
        unit_cfg (UnitConfigs): Class holding all unit interfaces.
        signal_if (SignalInterfaces): class holding signal interface information.

    """
    LOGGER.info("******************************************************")
    LOGGER.info("Start creating interface report")
    start_time = time.time()
    report_dst_dir = build_cfg.get_reports_dst_dir()

    sig_if = SigIfHtmlReport(build_cfg, unit_cfg, signal_if)
    sig_if.generate_report_file(pjoin(report_dst_dir, "SigIf.html"))
    LOGGER.info(
        "Finished - create interface report (in %4.2f s)", time.time() - start_time
    )


def generate_dummy_spm(build_cfg, unit_cfg, feature_cfg, signal_if, udt, polyspace_comments):
    """Generate c-files that define unit output signals.

    Args:
        build_cfg (BuildProjConfig): Build project class holding where files should be stored.
        unit_cfg (UnitConfigs): Aggregated unit configs class.
        feature_cfg (FeatureConfigs): Used as a library to generate C-macros.
        signal_if (SignalInterfaces): Class holding signal interface information.
        udt (UserDefinedTypes): Class holding user defined data types.
        polyspace_comments (bool): Whether to insert polyspace comments for the variable definitions.
    """

    def _add_undefined_signals_from_unit(data):
        """Add undefined signals from unit.

        Includes included configs.
        Arguments:
        data (dict): Data for the unit
        """
        for signal_name, inport_attributes in data.get("inports", {}).items():
            if signal_name in defined_ports:
                continue
            if (
                feature_cfg.check_if_active_in_config(inport_attributes["configs"])
                or not build_cfg.allow_undefined_unused
            ):
                defined_ports.append(signal_name)
                undefined_outports.append(inport_attributes)
        for include_unit in data.get("includes", []):
            include_data = unit_cfg.get_unit_config(include_unit)
            _add_undefined_signals_from_unit(include_data)

    LOGGER.info("******************************************************")
    LOGGER.info("Start generating output vars")
    start_time = time.time()
    dst_dir = build_cfg.get_src_code_dst_dir()
    # Get out ports for all units in project regardless of code switches
    unit_vars = unit_cfg.get_per_unit_cfg_total()
    undefined_outports = []
    defined_ports = []

    for data in unit_vars.values():
        for outport_name, outport_data in data.get("outports", {}).items():
            if not feature_cfg.check_if_active_in_config(outport_data["configs"]):
                LOGGER.debug("Outport %s not active in current project", outport_name)
            elif outport_name not in defined_ports:
                if not outport_data.get("class").startswith("CVC_EXT"):
                    defined_ports.append(outport_name)
    defined_ports.extend(signal_if.get_externally_defined_ports())

    for data in unit_vars.values():
        _add_undefined_signals_from_unit(data)

    dummy_spm = DummySpm(
        undefined_outports, build_cfg, feature_cfg, unit_cfg, udt, "VcDummy_spm", polyspace_comments
    )
    dummy_spm.generate_files(dst_dir)
    LOGGER.info("Finished generating output vars (in %4.2f s)", time.time() - start_time)


def generate_did_files(build_cfg, unit_cfg):
    """Generate DIDAPI definition files.

    Args:
        build_cfg (BuildProjConfig): Build project class holding where
            files should be stored
        unit_cfg (UnitConfigs): class holding units definitions,
            and which units to include
    """
    start_time = time.time()
    did_defs_files = pjoin(build_cfg.get_src_code_dst_dir(), "VcDIDDefinition")
    car_com_file = build_cfg.get_car_com_dst()
    LOGGER.info("******************************************************")
    LOGGER.info("Start generating %s.c&h", did_defs_files)
    dids = DIDs(build_cfg, unit_cfg)
    dids.gen_did_def_files(did_defs_files)
    LOGGER.info(
        "Finished generating %s.c&h  (in %4.2f s)",
        did_defs_files,
        time.time() - start_time,
    )
    LOGGER.info("******************************************************")
    LOGGER.info("Start generating %s", car_com_file)
    start_time = time.time()
    dids.gen_did_carcom_extract(car_com_file)
    LOGGER.info(
        "Finished generating %s  (in %4.2f s)", car_com_file, time.time() - start_time
    )
    LOGGER.info("******************************************************")


def generate_core_dummy(build_cfg, core, unit_cfg):
    """Generate the Core dummy files.

    The core dummy creates RTE dummy functions,
    and Id variables for enabling testing of VCC Software. If this dummy is not
    included, it is not possible to build the project until the supplier deliver
    an updated diagnostic core SW.

    Note:
        These dummy files shall not be delivered to the supplier!

    Args:
        build_cfg (BuildProjConfig): Build project class holding where
            files should be stored
        core (Core): class holding core configuration information
    """
    core_dummy_fname = build_cfg.get_core_dummy_name()
    LOGGER.info("******************************************************")
    LOGGER.info("Start generating Core Dummy - %s", core_dummy_fname)
    start_time = time.time()
    core_dummy = CoreDummy(core.get_current_core_config(), unit_cfg)
    ecu_supplier = build_cfg.get_ecu_info()[0]
    if ecu_supplier in ["Denso", "CSP"]:
        core_dummy.generate_dg2_core_dummy_files(core_dummy_fname)
    elif ecu_supplier == 'Phinia':
        core_dummy.generate_phinia_core_dummy_files(core_dummy_fname)
    elif ecu_supplier == "RB":
        core_dummy.generate_rb_core_dummy_files(core_dummy_fname)
    elif ecu_supplier == 'APP' or ecu_supplier == 'EURO7':
        core_dummy.generate_generic_core_dummy_files(core_dummy_fname)
    else:
        msg = f"Could not generate VcCoreDummy, cannot identify the supplier {ecu_supplier}."
        LOGGER.critical(msg)
        raise ValueError(msg)
    LOGGER.info("Finished generating Core Dummy (in %4.2f s)", time.time() - start_time)


def generate_external_var_asil(build_cfg, unit_cfg, udt, qm, asil_a, asil_b, asil_c, polyspace_comments):
    """Generate two c-files that define the signal interface to the supplier, divided by ASIL level.

    The VcExtVar function assigns all variables to the CVC_DISP memory area
    for the specified ASIL level as defined in the IF List
    Note that this function only declares the variables
    in the supplier interface, which the supplier writes to. All other
    variables shall be declared by the function which writes to the variable.
    Note that dummy functionality/variables should be created in the function
    to keep the signalling interface consistent!

    Args:
        build_cfg (BuildProjConfig): Build project class holding where files should be stored.
        unit_cfg (UnitConfigs) : Aggregated unit configs class.
        udt (UserDefinedTypes): Class holding user defined data types.
        qm (dict): Dictionary with QM variables.
        asil_a (dict): Dictionary with ASIL A variables.
        asil_b (dict): Dictionary with ASIL B variables.
        asil_c (dict): Dictionary with ASIL C variables.
        polyspace_comments (bool): Whether to insert polyspace comments for the variable definitions.
    """
    ext_var_instances = {
        ExtVarCsvAsil(qm, build_cfg, unit_cfg, udt, "QM", polyspace_comments): "VcExtVarQM",
        ExtVarCsvAsil(asil_a, build_cfg, unit_cfg, udt, "A", polyspace_comments): "VcExtVarASIL_A",
        ExtVarCsvAsil(asil_b, build_cfg, unit_cfg, udt, "B", polyspace_comments): "VcExtVarASIL_B",
        ExtVarCsvAsil(asil_c, build_cfg, unit_cfg, udt, "C", polyspace_comments): "VcExtVarASIL_C"
    }
    for instance, dir_name in ext_var_instances.items():
        ext_var_path = Path(build_cfg.get_src_code_dst_dir(), dir_name)
        instance.generate_files(ext_var_path)


def generate_external_var(build_cfg, unit_cfg, udt, nrm_dict, dep_dict, sec_dict, polyspace_comments):
    """Generate two c-files that define the signal interface to the supplier.

    The VcExtVar function assigns all variables to the CVC_DISP memory area,
    while the ExtVarSafe.c are allocated to the CVC_DISP_ASIL_B memory area.
    Note that this function only declares the variables
    in the supplier interface, which the supplier writes to. All other
    variables shall be declared by the function which writes to the variable.
    Note that dummy functionality/variables should be created in the function
    to keep the signalling interface consistent!

    Args:
        build_cfg (BuildProjConfig): Build project class holding where files should be stored.
        unit_cfg (UnitConfigs) : Aggregated unit configs class.
        udt (UserDefinedTypes): Class holding user defined data types.
        nrm_dict (dict): Dictionary with normal variables.
        dep_dict (dict): Dictionary with dependability variables.
        sec_dict (dict): Dictionary with secure variables.
        polyspace_comments (bool): Whether to insert polyspace comments for the variable definitions.
    """
    if build_cfg.has_yaml_interface:
        ext_var_nrm = ExtVarYaml(nrm_dict, build_cfg, unit_cfg, udt, "normal", polyspace_comments)
        ext_var_dep = ExtVarYaml(dep_dict, build_cfg, unit_cfg, udt, "dependability", polyspace_comments)
    else:
        ext_var_nrm = ExtVarCsv(nrm_dict, build_cfg, unit_cfg, udt, "normal", polyspace_comments)
        ext_var_dep = ExtVarCsv(dep_dict, build_cfg, unit_cfg, udt, "dependability", polyspace_comments)
        ext_var_sec = ExtVarCsv(sec_dict, build_cfg, unit_cfg, udt, "secure", polyspace_comments)

    ext_var_instances = {
        ext_var_nrm: "VcExtVar",
        ext_var_dep: "VcExtVarSafe",
    }

    if not build_cfg.has_yaml_interface:
        ext_var_instances[ext_var_sec] = "VcExtVarSecure"

    for instance, dir_name in ext_var_instances.items():
        ext_var_path = Path(build_cfg.get_src_code_dst_dir(), dir_name)
        instance.generate_files(ext_var_path)


def generate_external_debug_var(build_cfg, unit_cfg, dbg_dict, dbg_asil_dict, polyspace_comments):
    """Generate c-files that define the debug variables in the signal interface to the supplier.

    Args:
        build_cfg (BuildProjConfig): Build project class holding where files should be stored.
        unit_cfg (UnitConfigs) : Aggregated unit configs class.
        dbg_dict (dict): Dictionary with debug variables.
        dbg_asil_dict (dict): Dictionary with ASIL debug variables.
        polyspace_comments (bool): Whether to insert polyspace comments for the variable definitions.
    """
    restructured_dbg_dict = {}
    dbg_instances = {
        ExtDbg(dbg_dict, build_cfg, unit_cfg, False, polyspace_comments): ("VcDebug", "VcDebugOutput"),
        ExtDbg(dbg_asil_dict, build_cfg, unit_cfg, True, polyspace_comments): ("VcDebugSafe", "VcDebugOutputSafe")
    }
    for instance, dir_names in dbg_instances.items():
        restructured_dbg_dict.update({
            dir_names[0]: instance.dbg_dict["inputs"],
            dir_names[1]: instance.dbg_dict["outputs"]
        })
        instance.gen_dbg_files(
            pjoin(build_cfg.get_src_code_dst_dir(), dir_names[0]),
            pjoin(build_cfg.get_src_code_dst_dir(), dir_names[1])
        )
    return restructured_dbg_dict


def generate_dummy_var(build_cfg, unit_cfg, signal_if, udt, polyspace_comments):
    """Generate c-file that define the missing signals.

    Args:
        build_cfg (BuildProjConfig): Build project class holding where files should be stored.
        unit_cfg (UnitConfigs) : Aggregated unit configs class.
        signal_if (SignalInterfaces): class holding signal interface information.
        udt (UserDefinedTypes): Class holding user defined data types.
        polyspace_comments (bool): Whether to insert polyspace comments for the variable definitions.
    """
    LOGGER.info("******************************************************")
    LOGGER.info("Start generating VcDummy")
    start_time = time.time()
    dst_dir = build_cfg.get_src_code_dst_dir()
    nrm_dict, dep_dict, sec_dict, _ = signal_if.get_external_io()
    nrm_dict = merge_dicts(nrm_dict, dep_dict, merge_recursively=True)
    nrm_dict = merge_dicts(nrm_dict, sec_dict, merge_recursively=True)
    res_dict = signal_if.check_config()
    dummy = DummyVar(unit_cfg, nrm_dict, res_dict, build_cfg, udt, polyspace_comments)
    dummy.generate_file(pjoin(dst_dir, "VcDummy"))
    LOGGER.info("Finished generating VcDummy (in %4.2f s)", time.time() - start_time)


def generate_nvm_def(build_cfg, unit_cfg, no_nvm_a2l):
    """Generate the c&h-files which declares the NVM-ram.

    The NVM-ram is declared in a struct per datatype length, in order
    to provide a defined order in RAM/FLASH/EEPROM for the tester
    communication service. Furthermore, # defines with the variables are
    created to minimize the needed model changes for access to the memory.

    Args:
        build_cfg (BuildProjConfig): Build project class holding where files should be stored.
        unit_cfg (UnitConfigs): class holding units definitions, and which units to include.
        no_nvm_a2l (bool): Do not generate A2L for NVM structs.
    """
    LOGGER.info("******************************************************")
    LOGGER.info("Start generating NVMDefinitions")
    start_time = time.time()
    tot_vars_nvm = unit_cfg.get_per_cfg_unit_cfg().get("nvm", {})
    nvm_def = NVMDef(build_cfg, unit_cfg, tot_vars_nvm)
    nvm_def.generate_nvm_config_files(no_nvm_a2l)
    LOGGER.info(
        "Finished generating NVMDefinitions (in %4.2f s)", time.time() - start_time
    )


def copy_unit_src_to_src_out(build_cfg, include_model_a2l):
    """Copy unit source code to delivery folder.

    Function to copy all relevant .c, .h and .a2l files to the src
    delivery folder (defined in the config file for the project),
    from the units that are included in the project.

    Args:
        build_cfg (BuildProjConfig): Build project class holding where
            files should be stored
        include_model_a2l (bool): Move model a2l files to output folder.
    """
    LOGGER.info("******************************************************")
    LOGGER.info("Start copying unit source files")
    start_time = time.time()
    src_dirs = build_cfg.get_unit_src_dirs()
    src_dst_dir = build_cfg.get_src_code_dst_dir()
    files = []
    for src_dir in src_dirs.values():
        files.extend(glob.glob(pjoin(src_dir, "*.c")))
        files.extend(glob.glob(pjoin(src_dir, "*.cpp")))
        files.extend(glob.glob(pjoin(src_dir, "*.h")))
        if include_model_a2l:
            files.extend(glob.glob(pjoin(src_dir, '*.a2l')))
    for file_ in files:
        shutil.copy2(file_, src_dst_dir)
        LOGGER.debug("copied %s to %s", file_, src_dst_dir)
    LOGGER.info(
        "Finished copying unit source files (in %4.2f s)", time.time() - start_time
    )


def copy_common_src_to_src_out(build_cfg):
    """Copy source code to delivery folder.

    Function to copy all relevant .c and .h files to the src
    delivery folder (defined in the config file for the project),
    from the units that are included in the project.

    Optionally, also patch the defined functions with the "schedulerPrefix".

    Args:
        build_cfg (BuildProjConfig): Build project class holding where files should be stored.
    """
    LOGGER.info("******************************************************")
    prefix = build_cfg.get_scheduler_prefix()
    if prefix:
        LOGGER.info("Start copying and patching common source files")
    else:
        LOGGER.info("Start copying common source files")

    start_time = time.time()
    src_dir = build_cfg.get_common_src_dir()
    src_dst_dir = build_cfg.get_src_code_dst_dir()
    included_common_files = build_cfg.get_included_common_files()

    files = [
        pjoin(src_dir, common_file + ".c") for common_file in included_common_files
    ]
    files.extend(
        [pjoin(src_dir, common_file + ".h") for common_file in included_common_files]
    )

    files_to_copy = filter(os.path.isfile, files)
    for file_ in files_to_copy:
        if prefix:
            patch_and_copy_common_src_to_src_out(prefix, Path(file_), Path(src_dst_dir))
        else:
            shutil.copy2(file_, src_dst_dir)
        LOGGER.debug("copied %s to %s", file_, src_dst_dir)

    LOGGER.info(
        "Finished copying common source files (in %4.2f s)", time.time() - start_time
    )


def patch_and_copy_common_src_to_src_out(prefix, file_path, dest_dir):
    """Copy common source code to delivery folder, patched with "schedulerPrefix" as prefix.

    Args:
        prefix (str): Prefix.
        file_path (Path): Path to file to patch and copy.
        dest_dir (Path): Destination directory for the patched file.
    """
    with file_path.open(mode="r", encoding="utf-8") as file_handle:
        content = file_handle.read()

    new_function = f"{prefix}{file_path.stem}"
    new_content = content.replace(f"{file_path.stem}(", f"{new_function}(")
    new_content_lines = new_content.splitlines()

    if file_path.suffix == ".h":
        defines_index = next(
            (idx for idx, line in enumerate(new_content_lines) if "DEFINES" in line and "(OPT)" not in line),
            None
        )
        if defines_index is not None:
            # Insert at defines_index + 2, +1 to get to the next line and +1 to get after multiline comment
            new_content_lines.insert(defines_index + 2, f"#define {file_path.stem} {new_function}")

    with Path(dest_dir, file_path.name).open(mode="w", encoding="utf-8") as file_handle:
        file_handle.write("\n".join(new_content_lines))


def copy_files_to_include(build_cfg):
    """Copy source code to delivery folder.

    Function to copy all extra include files to the src delivery folder
    (defined in the config file for the project),
    from the units that are included in the project.

    Args:
        build_cfg (BuildProjConfig): Build project class holding where
            files should be stored
    """
    LOGGER.info("******************************************************")
    LOGGER.info("Start copying extra included source files")
    start_time = time.time()
    src_dst_dir = build_cfg.get_src_code_dst_dir()

    # Copy some files flat to the destination directory
    include_paths = build_cfg.get_includes_paths_flat()
    files = []
    for include_path in include_paths:
        if os.path.isdir(include_path):
            files.extend(
                [
                    Path(include_path, file_name)
                    for file_name in Path(include_path).iterdir()
                    if not file_name.is_dir()
                ]
            )
        elif os.path.isfile(include_path):
            files.append(include_path)
        else:
            LOGGER.critical("File or directory %s not found", include_path)
    for file_ in files:
        shutil.copy2(file_, src_dst_dir)
        LOGGER.debug("copied %s to %s", file_, src_dst_dir)

    # Copy some directories as is to the destination directory
    include_tree_paths = [Path(p) for p in build_cfg.get_includes_paths_tree()]
    existing_tree_paths = [p for p in include_tree_paths if p.exists()]
    missing_tree_paths = [p for p in include_tree_paths if not p.exists()]
    if missing_tree_paths:
        LOGGER.warning(f"Missing include paths: {missing_tree_paths}")
    for path in existing_tree_paths:
        for file_ in path.rglob("*"):
            if file_.is_file():
                new_path = Path(src_dst_dir, file_.relative_to(path))
                create_dir(new_path.parent)
                shutil.copy2(file_, new_path)
                LOGGER.debug("copied %s to %s", file_, new_path)
    LOGGER.info(
        "Finished copying extra included files (in %4.2f s)", time.time() - start_time
    )


def copy_unit_cfgs_to_output(build_cfg):
    """Copy all relevant unit configuration files to delivery folder.

    Function to copy all relevant unit config .json files to the UnitCfg
    delivery folder (defined in the config file for the project),
    from the units that are included in the project.

    Args:
        build_cfg (BuildProjConfig): Build project class holding where
            files should be stored
    """
    cfg_dst_dir = build_cfg.get_unit_cfg_deliv_dir()
    if cfg_dst_dir is not None:
        LOGGER.info("******************************************************")
        LOGGER.info("Start copying the unit config files")
        start_time = time.time()
        cfg_dirs = build_cfg.get_unit_cfg_dirs()
        files = []
        for cfg_dir in cfg_dirs.values():
            files.extend(glob.glob(pjoin(cfg_dir, "*.json")))
        for file_ in files:
            shutil.copy2(file_, cfg_dst_dir)
            LOGGER.debug("copied %s to %s", file_, cfg_dst_dir)
        LOGGER.info(
            "Finished copying the unit config files (in %4.2f s)",
            time.time() - start_time,
        )


def merge_a2l_files(build_cfg, unit_cfg, complete_a2l=False, silver_a2l=False):
    """Merge a2l-files.

    Args:
        build_cfg (BuildProjConfig): Build project class holding where
            files should be stored
        unit_cfg (UnitConfigs): class holding units definitions,
            and which units to include
    Returns:
        a2l (A2lMerge): A2lMerge class holding the merged a2l data.
    """
    LOGGER.info("******************************************************")
    LOGGER.info("Start merging A2L-files")
    start_time = time.time()
    src_dirs = build_cfg.get_unit_src_dirs()
    src_dst_dir = build_cfg.get_src_code_dst_dir()
    a2l_files_unit = []
    for src_dir in src_dirs.values():
        a2l_files_unit.extend(glob.glob(pjoin(src_dir, "*.a2l")))
    a2l_files_gen = glob.glob(pjoin(src_dst_dir, "*.a2l"))
    a2l = A2lMerge(build_cfg, unit_cfg, a2l_files_unit, a2l_files_gen)
    new_a2l_file = os.path.join(src_dst_dir, build_cfg.get_a2l_name())
    # LOGGER.debug(new_a2l_file)
    a2l.merge(new_a2l_file, complete_a2l, silver_a2l)
    LOGGER.info("Finished merging A2L-files (in %4.2f s)", time.time() - start_time)
    return a2l


def find_all_project_configs(prj_cfg_file):
    """Find all Project config files."""
    prj_root_dir, _ = os.path.split(prj_cfg_file)
    prj_root_dir = os.path.abspath(prj_root_dir)
    all_cfg_path = os.path.join(prj_root_dir, "..", "*", "ProjectCfg.json")
    return glob.glob(all_cfg_path, recursive=True)


def propagate_release_info(build_cfg, tag_name, problem_logger):
    """Set tag name in relevant files, for release builds.

    Args:
        build_cfg (BuildProjConfig): Build project class holding where files should be stored.
        tag_name (str): git tag name.
        problem_logger (object): logger for powertrain_build.
    """
    LOGGER.info("******************************************************")
    LOGGER.info("Propagating tag name: %s", tag_name)
    start_time = time.time()

    src_dst_dir = build_cfg.get_src_code_dst_dir()
    h_file_path = os.path.join(src_dst_dir, "vcc_sp_version.h")

    if not os.path.isfile(h_file_path):
        problem_logger.critical("Missing %s", h_file_path)
        return

    part_numbers = build_cfg.get_project_default_cfg()
    part_number_SWLM = part_numbers[0]
    part_number_SWCE = part_numbers[1]

    with open(h_file_path, 'r+') as file_handle:
        contents = file_handle.read()
        file_handle.seek(0)
        file_handle.truncate(0)
        contents = contents.replace(
            '#define VCC_SOFTWARE_NAME "tagname"',
            '#define VCC_SOFTWARE_NAME "%s"' % tag_name
        )  # Denso
        contents = contents.replace(
            '#define SW_PARTNO_SWLM "partnumber_SWLM"',
            '#define SW_PARTNO_SWLM "%s"' % part_number_SWLM
        )
        contents = contents.replace(
            '#define SW_PARTNO_SWCE "partnumber_SWCE"',
            '#define SW_PARTNO_SWCE "%s"' % part_number_SWCE
        )
        file_handle.write(contents)

    LOGGER.info("Finished propagating tag name (in %4.2f s)", time.time() - start_time)


def add_args(parser):
    """Add command line arguments for powertrain_build.

    This is useful when powertrain-build should be run through a command line wrapper function.

    Args:
        parser (argparse.ArgumentParser): Parser instance to add arguments to.
    """
    powertrain_build_parser = parser.add_argument_group("powertrain-build arguments")
    powertrain_build_parser.add_argument(
        "--project-config", required=True, help="Project root configuration file"
    )
    powertrain_build_parser.add_argument(
        "--generate-system-info", action="store_true", help="Generate AllSystemInfo.mat"
    )
    powertrain_build_parser.add_argument(
        "--generate-custom-conv-tab",
        default=None,
        help="Path to conversion table file. Useful for TargetLink enums in A2L file.",
    )
    powertrain_build_parser.add_argument(
        "--core-dummy",
        action="store_true",
        help="Generate core dummy code to enable integration with old supplier code",
    )
    powertrain_build_parser.add_argument(
        "--rte-dummy",
        action="store_true",
        help="Generate RTE dummy code to enable e.g. Silver testing",
    )
    powertrain_build_parser.add_argument(
        "--debug", action="store_true", help="Activate the debug log"
    )
    powertrain_build_parser.add_argument(
        "--no-abort", action="store_true", help="Do not abort due to errors"
    )
    powertrain_build_parser.add_argument(
        "--include-model-a2l",
        action="store_true",
        help="Move model a2l files to output folder",
    )
    powertrain_build_parser.add_argument(
        "--no-nvm-a2l",
        action="store_true",
        help="Do not generate a2l file for NVM structs",
    )
    powertrain_build_parser.add_argument(
        "--complete-a2l", action="store_true", help="Generate A2L with project info"
    )
    powertrain_build_parser.add_argument(
        "--silver-a2l",
        action="store_true",
        help="Generate A2L file with Silver patching. Complete A2L argument takes precedence.",
    )
    powertrain_build_parser.add_argument(
        "--interface", action="store_true", help="Generate interface report"
    )
    powertrain_build_parser.add_argument(
        "--generate-rte-checkpoint-calls",
        action="store_true",
        help="Generate RTE function checkpoint calls",
    )
    powertrain_build_parser.add_argument(
        "--polyspace-comments",
        action="store_true",
        help="Add Polyspace justification comments in the generated code for identified violations",
    )
    powertrain_build_parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Display program version",
    )


def build(
    project_config,
    interface=False,
    core_dummy=False,
    rte_dummy=False,
    no_abort=False,
    include_model_a2l=False,
    no_nvm_a2l=False,
    debug=False,
    quiet=False,
    generate_system_info=False,
    generate_custom_conversion_table=None,
    complete_a2l=False,
    silver_a2l=False,
    generate_rte_checkpoint_calls=False,
    polyspace_comments=False
):
    """Execute the build.

    Args:
        project_config (str): Project configuration file.
        interface (bool): Generate interface report. Default=False.
        core_dummy (bool): Generate core dummy code. Default=False.
        rte_dummy (bool): Generate RTE dummy code. Default=False.
        no_abort (bool): Do not abort due to errors. Default=False.
        include_model_a2l (bool): Move model a2l files to output folder. Default=False.
        no_nvm_a2l (bool): Do not generate A2L for NVM structs. Default=False.
        debug (bool): Activate the debug log. Default=False.
        quiet (bool): Disable logging to stdout. Default=False.
        generate_system_info (bool): Generate AllSystemInfo.mat for DocGen compatibility. Default=False.
        generate_custom_conversion_table (str): Path to conversion table file.
            Useful for TargetLink enums in A2L file. Default=None.
        complete_a2l (bool): Add an a2l header plus additional content such as XCP data.
        silver_a2l (bool): Add an a2l header plus additional patching required for Silver.
        generate_rte_checkpoint_calls (bool): Generate RTE function checkpoint calls.
        polyspace_comments (bool): Add Polyspace justification comments in the generated code for identified violations.
    """
    try:
        problem_logger = ProblemLogger()
        tot_start_time = time.time()
        project_config_files = find_all_project_configs(project_config)
        prj_cfgs = {}

        for project_config_file in project_config_files:
            conf = BuildProjConfig(os.path.normpath(project_config_file))
            prj_cfgs.update({conf.name: conf})

        prj_cfgs = {}
        build_cfg = BuildProjConfig(os.path.normpath(project_config))
        prj_cfgs.update({build_cfg.name: build_cfg})

        build_cfg.create_build_dirs()
        src_dst_dir = build_cfg.get_src_code_dst_dir()

        setup_logging(build_cfg.get_log_dst_dir(), problem_logger, debug, quiet)
        LOGGER.info("Starting build")
        LOGGER.info("powertrain_build version is: %s", __version__)
        LOGGER.info("Project/Model config file version is: %s", __config_version__)
        LOGGER.info("Read SPM code switches")
        start_time = time.time()
        feature_cfg = FeatureConfigs(build_cfg)
        LOGGER.info(
            "Finished reading SPM code switches (in %4.2f s)", time.time() - start_time
        )

        LOGGER.info("******************************************************")
        LOGGER.info("Start generating per project unit config data")
        start_time = time.time()
        unit_cfg = UnitConfigs(build_cfg, feature_cfg)
        LOGGER.info(
            "Finished generating per project unit config data (in %4.2f s)",
            time.time() - start_time,
        )

        code_generation_config = build_cfg.get_code_generation_config()

        udt = UserDefinedTypes(build_cfg, unit_cfg)
        udt.generate_common_header_files()

        start_time = time.time()
        cnf_header = pjoin(src_dst_dir, build_cfg.get_feature_conf_header_name())
        LOGGER.info("******************************************************")
        LOGGER.info("Generate compiler switches header file %s", cnf_header)
        feature_cfg.gen_unit_cfg_header_file(cnf_header)
        LOGGER.info(
            "Finished generating compiler switches header file (in %4.2f s)",
            time.time() - start_time,
        )
        if build_cfg.has_yaml_interface:
            signal_if = YamlSignalInterfaces(build_cfg, unit_cfg, feature_cfg, udt)
        else:
            signal_if = CsvSignalInterfaces(build_cfg, unit_cfg)
            check_interfaces(build_cfg, signal_if)
        if interface:
            interface_report(build_cfg, unit_cfg, signal_if)

        LOGGER.info("******************************************************")
        LOGGER.info("Start generating VcExtVar and VcDebug")
        start_time = time.time()
        use_external_asil_config = code_generation_config['useExternalAsilConfig']
        if use_external_asil_config:
            if build_cfg.has_yaml_interface:
                LOGGER.critical("External ASIL config is not supported for YAML interface")
            else:
                qm, asil_a, asil_b, asil_c, dbg_qm_a, dbg_b_c = signal_if.get_asil_config()
                generate_external_var_asil(build_cfg, unit_cfg, udt, qm, asil_a, asil_b, asil_c, polyspace_comments)
                restructured_dbg_dict = generate_external_debug_var(
                    build_cfg, unit_cfg, dbg_qm_a, dbg_b_c, polyspace_comments
                )
        else:
            nrm_dict, dep_dict, sec_dict, dbg_dict = signal_if.get_external_io()
            generate_external_var(build_cfg, unit_cfg, udt, nrm_dict, dep_dict, sec_dict, polyspace_comments)
            restructured_dbg_dict = generate_external_debug_var(
                build_cfg, unit_cfg, dbg_dict, dep_dict, polyspace_comments
            )
        LOGGER.info("Finished generating VcExtVar and VcDebug (in %4.2f s)", time.time() - start_time)

        if not code_generation_config["generateDummyVar"]:
            LOGGER.info("******************************************************")
            LOGGER.info("Skip generating VcDummy file")
        else:
            generate_dummy_var(build_cfg, unit_cfg, signal_if, udt, polyspace_comments)

        custom_dummy_spm = build_cfg.get_use_custom_dummy_spm()
        if custom_dummy_spm is not None:
            LOGGER.info("******************************************************")
            if os.path.isfile(custom_dummy_spm):
                LOGGER.info("Copying custom dummy spm file (%s)", custom_dummy_spm)
                shutil.copy2(custom_dummy_spm, build_cfg.get_src_code_dst_dir())
            else:
                LOGGER.warning(
                    "Cannot find desired custom dummy spm file: %s", custom_dummy_spm
                )
                generate_dummy_spm(build_cfg, unit_cfg, feature_cfg, signal_if, udt, polyspace_comments)
        else:
            generate_dummy_spm(build_cfg, unit_cfg, feature_cfg, signal_if, udt, polyspace_comments)

        custom_sources = build_cfg.get_use_custom_sources()
        if custom_sources is not None:
            LOGGER.info("******************************************************")
            for custom_src in custom_sources:
                if os.path.isfile(custom_src):
                    LOGGER.info("Copying custom sourcefile (%s)", custom_src)
                    shutil.copy2(custom_src, build_cfg.get_src_code_dst_dir())
                else:
                    LOGGER.warning("Cannot find desired custom sourcefile: %s", custom_src)

        LOGGER.info("******************************************************")
        LOGGER.info("Start generating the scheduling functions")
        start_time = time.time()
        gen_schd = SchedFuncs(build_cfg, unit_cfg, restructured_dbg_dict)
        gen_schd.generate_sched_c_fncs(generate_rte_checkpoint_calls)
        LOGGER.info("Finished generating the scheduling functions (in %4.2f s)", time.time() - start_time)

        LOGGER.info("******************************************************")
        LOGGER.info("Start generating the ts header file")
        start_time = time.time()
        gen_schd.generate_ts_defines(pjoin(src_dst_dir, build_cfg.get_ts_header_name()))
        LOGGER.info("Finished generating ts header file (in %4.2f s)", time.time() - start_time)

        # Generate AllSystemInfo.mat for DocGen compatibility
        if generate_system_info:
            from powertrain_build.gen_allsysteminfo import GenAllSystemInfo

            gen_all_system_info = GenAllSystemInfo(signal_if, unit_cfg)
            gen_all_system_info.build()

        # Check if errors
        if not no_abort:
            if problem_logger.errors():
                nbr_err = problem_logger.get_nbr_problems()
                problem_logger.info(
                    "Aborting build due to errors (# critical:%s, # warnings:%s"
                    " after %4.2f s.",
                    nbr_err["critical"],
                    nbr_err["warning"],
                    time.time() - tot_start_time,
                )
                return 1

        # Copy files to output folder
        copy_unit_src_to_src_out(build_cfg, include_model_a2l)
        copy_common_src_to_src_out(build_cfg)
        copy_unit_cfgs_to_output(build_cfg)
        copy_files_to_include(build_cfg)
        if code_generation_config["generateInterfaceHeaders"]:
            memory_section = MemorySection(build_cfg, unit_cfg, polyspace_comments)
            memory_section.generate_required_header_files()
            memory_section.generate_optional_header_files()

        # Propagate release information for release builds, TAG_NAME must be set in environment
        tag_name = os.environ.get("TAG_NAME", "")
        if tag_name and code_generation_config["propagateReleaseInfo"]:
            propagate_release_info(build_cfg, tag_name, problem_logger)

        # Copy header files (subversion is using an external that points to
        # the correct set of pragma section header_files

        # Make A2L-file
        if generate_custom_conversion_table is not None:
            ctable_json = Path(generate_custom_conversion_table).resolve()
            ctable_a2l = Path(build_cfg.get_src_code_dst_dir(), "custom_tabs.a2l")
            create_conversion_table(ctable_json, ctable_a2l)
        merged_a2l = merge_a2l_files(build_cfg, unit_cfg, complete_a2l, silver_a2l)
        a2l_file_path = Path(build_cfg.get_src_code_dst_dir(), build_cfg.get_a2l_name())
        replace_tab_verb(a2l_file_path)

        # Generate interface files
        if code_generation_config["generateYamlInterfaceFile"]:
            zc_core = ZCCore(build_cfg, unit_cfg)
            zc_dids = ZCDIDs(build_cfg, unit_cfg)
            LOGGER.info("******************************************************")
            LOGGER.info("Start generating NVMDefinitions")
            start_time = time.time()
            project_nvm_defintions = unit_cfg.get_per_cfg_unit_cfg().get("nvm", {})
            zc_nvm = ZCNVMDef(build_cfg, unit_cfg, project_nvm_defintions)
            LOGGER.info(
                "Finished generating NVMDefinitions (in %4.2f s)", time.time() - start_time
            )
            LOGGER.info("******************************************************")
            axis_data = merged_a2l.get_characteristic_axis_data()
            composition_yaml = CompositionYaml(
                build_cfg,
                signal_if,
                unit_cfg,
                zc_core,
                zc_dids,
                zc_nvm,
                axis_data,
                udt.get_enumerations()
            )
            composition_yaml.generate_yaml()
            LOGGER.info("******************************************************")
            LOGGER.info("Generating Core header")
            zc_core.generate_dtc_files()
            LOGGER.info("******************************************************")
            LOGGER.info("Generating DID files")
            zc_dids.generate_did_files()
            LOGGER.info("******************************************************")
            LOGGER.info("Generating NVM definitions")
            zc_nvm.generate_nvm_rte_files()

            if rte_dummy:
                LOGGER.info("******************************************************")
                LOGGER.info("Generating RTE dummy files")
                zc_rte = RteDummy(build_cfg, zc_core, zc_nvm, composition_yaml.cal_class_info["tl"])
                zc_rte.generate_rte_dummy()

            if code_generation_config["generateCalibrationInterfaceFiles"]:
                LOGGER.info("******************************************************")
                if code_generation_config["useCalibrationRteMacroExpansion"]:
                    LOGGER.warning(
                        "Skip generating calibration interface files as useCalibrationRteMacroExpansion is set to true"
                    )
                else:
                    LOGGER.info("Generating calibration interface files")
                    zc_calibration = ZoneControllerCalibration(
                        build_cfg, composition_yaml.cal_class_info["tl"]
                    )
                    zc_calibration.generate_calibration_interface_files()
        elif build_cfg.get_ecu_info()[0] == "HI":
            generate_nvm_def(build_cfg, unit_cfg, no_nvm_a2l)
            LOGGER.info("******************************************************")
            LOGGER.info("Generating Core header")
            hi_core = HICore(build_cfg, unit_cfg)
            hi_core.generate_dtc_files()
            LOGGER.info("******************************************************")
            LOGGER.info("Generating DID files")
            dids = HIDIDs(build_cfg, unit_cfg)
            dids.generate_did_files()
        else:
            generate_nvm_def(build_cfg, unit_cfg, no_nvm_a2l)
            generate_did_files(build_cfg, unit_cfg)
            # generate core dummy files if requested
            if core_dummy:
                core_dummy_fname = os.path.basename(build_cfg.get_core_dummy_name())
                if CodeGenerators.embedded_coder in unit_cfg.code_generators:
                    LOGGER.info("******************************************************")
                    LOGGER.info("Skip generating %s for EC projects", core_dummy_fname)
                elif not code_generation_config["generateCoreDummy"]:
                    LOGGER.info("******************************************************")
                    LOGGER.info("Skip generating %s since generateCoreDummy is set to False", core_dummy_fname)
                else:
                    core = Core(build_cfg, unit_cfg)
                    generate_core_dummy(build_cfg, core, unit_cfg)

        if problem_logger.errors():
            problem_logger.info(
                "Critical errors were detected, aborting" " after %4.2f s.",
                time.time() - tot_start_time,
            )
            return 1

        LOGGER.info("Finished build in %4.2f s", time.time() - tot_start_time)
        return 0

    finally:
        logging.shutdown()
