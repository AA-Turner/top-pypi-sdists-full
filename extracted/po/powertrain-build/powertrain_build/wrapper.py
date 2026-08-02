# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Performs compatibility upgrade of models to PyBuild using Matlab."""

import argparse
import hashlib
import json
import os
import platform
import sys
from pathlib import Path
from re import search
from typing import List, Optional

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files
import shutil

import git
from powertrain_build import build, pt_matlab
from powertrain_build.interface import export_global_vars
from powertrain_build.lib import logger, helper_functions

LOGGER = logger.create_logger(__file__)


class PyBuildWrapper(pt_matlab.Matlab):
    """Performs upgrade of Matlab models to PyBuild system."""

    HASH_FILE_NAME = "pybuild_file_hashes.json"
    PARSER_HELP = "Run PyBuild, update and/or generate code for selected models and/or build."

    def __init__(self, args):
        """Constructor, initializes paths for PyBuild upgrader.

        Args:
            args (argument parser): see add_args static method.
        """
        super().__init__(dry_run=args.dry_run, matlab_bin=args.matlab_bin, nojvm=False)

        self.root_path = helper_functions.get_repo_root()

        self.target_link_settings_hash_file_path = Path("ConfigDocuments", "target_link_settings_file_hashes.json")
        self.target_link_settings_folders = [
            Path("ConfigDocuments", "targetlinkSettings"),
            Path("ConfigDocuments", "TL4_3_settings"),
        ]

        self.update = args.update
        self.codegen = args.codegen
        self.generate_files_hashes = args.generate_files_hashes

        self.build = args.build
        self.build_specific = getattr(args, "project_config", None) is not None
        self.project_config = self._set_project_configuration(args)
        self.generate_system_info = getattr(args, "generate_system_info", False)
        self.core_dummy = getattr(args, "core_dummy", True)
        self.rte_dummy = getattr(args, "rte_dummy", False)
        self.debug = getattr(args, "debug", True)
        self.no_abort = getattr(args, "no_abort", True)
        self.no_nvm_a2l = getattr(args, "no_nvm_a2l", False)
        self.complete_a2l = getattr(args, "complete_a2l", False)
        self.silver_a2l = getattr(args, "silver_a2l", False)
        self.generate_rte_checkpoint_calls = getattr(args, "generate_rte_checkpoint_calls", False)
        self.polyspace_comments = getattr(args, "polyspace_comments", False)
        self.interface = args.interface
        self.matlab_include = args.include
        # Always default to conversion table in pytools/config/conversion_table.json.
        # Unless otherwise specified.
        conv_tab_path = getattr(args, "generate_custom_conv_tab", None)
        default_conv_tab_path = os.path.join("ConfigDocuments", "pytools_settings", "conversion_table.json")
        self.conv_tab = conv_tab_path if conv_tab_path is not None else default_conv_tab_path

        self.should_run, self.models = self._evaluate_run_and_models(args)

    @staticmethod
    def _set_project_configuration(args):
        """Evaluate path to project configuration file.

        Args:
            args (argument parser): see add_args static method.
        Returns:
            project_config: Path to project configuration file.
        """
        if getattr(args, "project_config", None) is not None:
            project_config = args.project_config.replace("/", os.sep)
        elif args.build is not None:
            if args.build.lower() == "custom":
                # TODO: Change other scripts to accept custom config
                #       Change this to point to a config file instead
                project_config = os.path.join(os.environ.get("PROJECT_DIR"), "ProjectCfg.json")
            else:
                project_config = os.path.join("Projects", args.build, "ProjectCfg.json")
        else:
            project_config = None

        return project_config

    @staticmethod
    def convert_path_sep(paths):
        """Matlab requires forward-spaces for model paths. Convert backslashes.

        Args:
            paths (list): Model paths to fix path separators for.
        Returns:
            (list): Models paths separated with forward slashes.
        """
        return [path.replace("\\", "/") for path in paths]

    @staticmethod
    def get_matlab_scripts_commit_sha():
        """Get current commit sha of matlab-scripts submodule, if available.

        Returns:
            matlab_scripts_commit_sha (str): Commit sha of matlab-scripts submodule.
                None, if not available.
        """
        repo = git.Repo(search_parent_directories=True)
        try:
            matlab_scripts = repo.submodule("matlab-scripts")
            matlab_scripts_commit_sha = matlab_scripts.hexsha
        except ValueError:
            LOGGER.info("Submodule matlab-scripts not available, " "skipping adding its commit sha to hash file.")
            matlab_scripts_commit_sha = None
        return matlab_scripts_commit_sha

    @staticmethod
    def read_bytes(file_path):
        """Read file contents in byte mode.

        Args:
            file_path (Path): Path to file.
        Returns:
            file_bytes (bytes): Content of file read in binary mode.
        """
        if file_path.suffix in [".slx", ".mdl", ".mexw64"]:
            # Already treated as binary file
            file_bytes = file_path.read_bytes()
        else:
            # Hack to make this script os independent
            with file_path.open(encoding="iso-8859-1") as file_handle:
                content = file_handle.read()
                file_bytes = content.encode("iso-8859-1")
        return file_bytes

    @staticmethod
    def get_files_to_hash(model_folder):
        """Get files to generate hashes for (PyBuild specific files).

        Args:
            model_folder (Path): Path to model folder.
        Returns:
            files_to_hash (list): List of, pybuild specific, files to generate hashes for.
        """
        valid_file_endings = [
            # source files
            ".a2l",
            ".c",
            ".h",
            ".mexw64",
            ".tlc",
            # config files
            ".json",
            # model files
            ".mdl",
            ".m",
        ]
        valid_folders = [
            model_folder,
            Path(model_folder, "matlab_src"),
            Path(model_folder, "pybuild_cfg"),
            Path(model_folder, "pybuild_src"),
        ]
        hash_file_path = Path(model_folder, PyBuildWrapper.HASH_FILE_NAME)

        model_files = list(model_folder.rglob("*.*"))
        if hash_file_path.exists():
            model_files.remove(hash_file_path)
        files_to_hash = [f for f in model_files if f.parent in valid_folders and f.suffix in valid_file_endings]
        return files_to_hash

    @staticmethod
    def get_shared_function_files():
        """Get shared function files, files generated by VcSharedFunctions.mdl.

        Returns:
            shared_function_files (list): List of files generated by VcSharedFunctions.mdl.
        """
        shared_function_files = []
        common_source_folder = Path("Models/Common/pybuild_src")
        for source_file in common_source_folder.glob("*.*"):
            with source_file.open() as file_handle:
                content = file_handle.read()
            if search(r"Simulink model\s+: VcSharedFunctions", content) is not None:
                shared_function_files.append(source_file)
        return shared_function_files

    @staticmethod
    def get_file_hashes(model_paths, write_to_file=True):
        """Calculate SHA256 file hashes for files in given model folders.

        Args:
            model_paths (list): List of model paths.
            write_to_file (bool): True/False whether calculated hashes should be written to file.
        Returns:
            model_to_files_hash_dict (dict): Dict mapping model name to files and its hashes.
        """
        model_to_files_hash_dict = {}
        model_folders = [(Path(m).parent, Path(m).stem) for m in model_paths]
        for model_folder, model_name in model_folders:
            file_to_hash_dict = {}
            files_to_hash = PyBuildWrapper.get_files_to_hash(model_folder)
            if "VcSharedFunctions" in model_folder.as_posix():
                shared_function_files = PyBuildWrapper.get_shared_function_files()
                files_to_hash.extend(shared_function_files)
            for file_to_hash in files_to_hash:
                file_bytes = PyBuildWrapper.read_bytes(file_to_hash)
                file_to_hash_dict[file_to_hash.name] = hashlib.sha256(file_bytes).hexdigest()
            commit_sha = PyBuildWrapper.get_matlab_scripts_commit_sha()
            if commit_sha is not None:
                file_to_hash_dict["matlab-scripts"] = commit_sha
            if write_to_file:
                with Path(model_folder, PyBuildWrapper.HASH_FILE_NAME).open("w", encoding="utf-8") as file_handle:
                    json.dump(file_to_hash_dict, file_handle, indent=4)
            model_to_files_hash_dict[model_name] = file_to_hash_dict
        return model_to_files_hash_dict

    def _evaluate_run_and_models(self, args):
        """Evaluate if PyBuild should run or not.

        Additionally, it sets which models to update and/or generate code for, based on arguments.
        NOTE: Building a project should be possible without invoking git.

        Args:
            args (argument parser): see add_args static method.
        Returns:
            should_run: True/False whether PyBuild should run or not.
            model_list: List of models to update/generate code for.
        """
        run_build = args.build is not None or getattr(args, "project_config", None) is not None
        run_models = args.update or args.codegen
        if run_build and not run_models:
            return True, []
        model_list = args.models if args.models is not None else self.get_changed_models()
        if not model_list:
            return run_build, []
        LOGGER.info("Affected models: %s", ", ".join(model_list))
        return run_build or run_models, model_list

    def regenerate_target_link_settings_file_hashes(self):
        """Regenerate the file mapping TargetLink settings files to their hashes."""
        target_link_settings_file_hashes = self.calculate_target_link_settings_file_hashes()
        with self.target_link_settings_hash_file_path.open("w", encoding="utf-8") as file_handle:
            json.dump(target_link_settings_file_hashes, file_handle, indent=4)

    def calculate_target_link_settings_file_hashes(self):
        """Calculate SHA256 file hashes for files in TargetLink settings folders.

        Returns:
            file_to_hash_dict (dict): Dict mapping settings files and their hashes.
        """
        file_to_hash_dict = {}
        for settings_folder in self.target_link_settings_folders:
            for settings_file in settings_folder.rglob("*.*"):
                file_bytes = self.read_bytes(settings_file)
                file_to_hash_dict[settings_file.name] = hashlib.sha256(file_bytes).hexdigest()
        return file_to_hash_dict

    def verify_target_link_settings(self):
        """Verify current TargetLink settings, comparing against commited file hashes file.

        Returns:
            (bool): True/False, depending on if the TargetLink settings have changed.
        """
        if not self.target_link_settings_hash_file_path.exists():
            message = (
                "Could not read TargetLink settings file hashes file: "
                f"{self.target_link_settings_hash_file_path.as_posix()}.\n"
                "If your repo runs the jobb PyBuildDiff in hash mode, make sure to generate one."
                "Ignoring settings verification."
            )
            LOGGER.warning(message)
            return True

        with self.target_link_settings_hash_file_path.open(encoding="utf-8") as file_handle:
            current_file_hashes_dict = json.load(file_handle)

        new_file_hashes_dict = self.calculate_target_link_settings_file_hashes()

        return new_file_hashes_dict == current_file_hashes_dict

    def export_global_variables(self, export_type):
        """Export global variables as yaml file.

        Args:
            export_type (str): Type of variables to export, either "default" or "inports" too.
        """
        if self.project_config is None:
            LOGGER.critical("Project configuration file not specified, cannot export global variables.")
            return
        include_inports = export_type == "inports"
        output_file = Path(self.project_config).parent / "output" / "global_variables.yaml"
        export_global_vars.export_global_vars(
            argparse.Namespace(
                project_config=self.project_config,
                output_file=output_file.as_posix(),
                include_inports=include_inports,
            )
        )

    def get_changed_models(self):
        """Get changed models in current commit."""
        repo = git.Repo(self.root_path)
        changed_files_tmp = repo.git.diff("--diff-filter=d", "--name-only", "HEAD~1")
        changed_files = changed_files_tmp.splitlines()
        changed_models = [m for m in changed_files if m.endswith(".mdl") or m.endswith(".slx")]
        return changed_models

    def check_generate_shared_functions(self, matlab_command_list):
        """Check if shared function files should be generated.

        Args:
            matlab_command_list ([str]): list of matlab commands.
        """
        if [model for model in self.models if model.endswith("VcSharedFunctions.mdl")]:
            matlab_command_list.append(pt_matlab.cmd_callfunc("generateSharedFunctions", True))

    def build_automation(self, mode):
        """Run Matlab with a specific task and specific models.

        Args:
            mode (str): Matlab run mode (update, codegen).
        Returns:
            exit_code (int): Exit code from Matlab.
        """
        # Will be used in submodule matlab-scripts (if up to date), CodeGen/updateCodeSwConfig.m
        calling_python = sys.version_info
        calling_python_version_string = f"{calling_python.major}.{calling_python.minor}"
        if platform.system() == "Linux":
            calling_python_string = f"python{calling_python_version_string}"
        else:
            calling_python_string = f"py -{calling_python_version_string}"
        os.environ.setdefault("CALLING_PYTHON", calling_python_string)

        # Specify a new script and log file name for each run
        script_name = f"powertrain_build_matlab_{mode}.m"
        self.log = f"powertrain_build_matlab_{mode}.log"

        # Set up matlab path
        matlab_scripts_path = os.path.join("powertrain_build_matlab_scripts")

        # Copy matlab-scripts to the project root
        matlab_script_folder = files("powertrain_build.matlab_scripts")
        shutil.rmtree(matlab_scripts_path, ignore_errors=True)
        shutil.copytree(matlab_script_folder, matlab_scripts_path)

        cmds = []
        cmds.append(f"cd '{Path.cwd()}'")
        cmds.append(pt_matlab.cmd_path(matlab_scripts_path, True))
        cmds.append(pt_matlab.cmd_path(self.matlab_include, True))

        if mode == "codegen":
            cmds.append(pt_matlab.cmd_callfunc("loadLibraries", self.matlab_include))

        # Generate the command for calling the main build script:
        args = [mode, True]
        if self.models:
            self.check_generate_shared_functions(cmds)
            args.append(self.convert_path_sep(self.models))

        cmds.append(pt_matlab.cmd_callfunc("BuildAutomationPyBuild", *args))
        pt_matlab.write_m_script(script_name, pt_matlab.cmds_join(cmds), wrap_cmd=False)

        # Reset the Matlab watcher before running a new m-script
        self.matlab_watcher.reset_errors()

        self.run_m_script(script_name, wrap_cmd=False, attempts=2)

        if not self.matlab_watcher.task_success:
            LOGGER.error("PyBuild %s error!", mode)
            return 1

        if not self.verify_target_link_settings():
            LOGGER.error("Your TargetLink settings differ from the ones set by current branch.")
            return 1

        if self.generate_files_hashes:
            self.get_file_hashes(self.models)
        return 0

    def run_powertrain_build(self):
        """Execute powertrain-build.

        Returns:
            exit_code: Exit code from powertrain-build build step.
        """
        try:
            exit_code = build.build(
                self.project_config,
                interface=self.interface,
                core_dummy=self.core_dummy,
                rte_dummy=self.rte_dummy,
                no_abort=self.no_abort,
                no_nvm_a2l=self.no_nvm_a2l,
                debug=self.debug,
                generate_system_info=self.generate_system_info,
                generate_custom_conversion_table=self.conv_tab,
                complete_a2l=self.complete_a2l,
                silver_a2l=self.silver_a2l,
                generate_rte_checkpoint_calls=self.generate_rte_checkpoint_calls,
                polyspace_comments=self.polyspace_comments
            )
        except (FileNotFoundError, PermissionError) as ex:
            LOGGER.error(ex)
            exit_code = 1
        return exit_code

    def run(self):
        """Run PyBuild, update and/or generate code for selected models and/or build.

        Returns:
            exit_code: Exit code from Matlab and build step.
        """
        if not self.should_run:
            return 0

        LOGGER.info("Preparing workspace for PyBuild!")

        exit_code = 0
        if self.update:
            LOGGER.info("Running PyBuild update!")
            exit_code |= self.build_automation(mode="update")

        if self.codegen:
            LOGGER.info("Running PyBuild generate code!")

            exit_code |= self.build_automation(mode="codegen")

        if self.build:
            LOGGER.info("Running PyBuild.build for %s!", self.build)
            exit_code |= self.run_powertrain_build()

        if self.build_specific:
            LOGGER.info("Running PyBuild specific build for %s!", self.project_config)
            exit_code |= self.run_powertrain_build()

        return exit_code

    @staticmethod
    def add_args(parser):
        """Add expected arguments to the supplied parser.

        Args:
            parser (ArgumentParser): parser to add arguments to.
        """
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Dry run: No changes, simulation only (default: False).",
        )
        parser.add_argument("--repo-root", help="Path to repository where work should be done")
        parser.add_argument(
            "--interface",
            action="store_true",
            help="Create interface consistency report (default: False)" "NOTE: This requires the --build flag.",
        )
        parser.add_argument(
            "--models",
            nargs="+",
            default=None,
            help="List of model files (full path, "
            "e.g. Models/<SSP>/<MODEL>/<MDL-FILE>) to upgrade, separated with "
            "spaces. Takes precedence over Git HEAD.",
        )
        parser.add_argument(
            "--update",
            action="store_true",
            help="Run PyBuild update on models (default: False).",
        )
        parser.add_argument(
            "--codegen",
            action="store_true",
            help="Run PyBuild code generation on models (default: False). "
            "NOTE: This requires either the --update flag or already updated models.",
        )
        parser.add_argument(
            "--generate-files-hashes",
            action="store_true",
            help="Generating a file containing file hashes for the output of the --codegen option (default: False).",
        )
        parser.add_argument(
            "--build",
            default=None,
            help="Run PyBuild for project with standard settings, VCC SPM SW release (default: None).",
        )
        parser.add_argument(
            "--regenerate-tl-settings-hashes",
            action="store_true",
            help="Regenerate the file mapping TargetLink settings files to their hashes.",
        )
        parser.add_argument(
            "--export-global-vars",
            choices=["default", "inports"],
            help="Export global variables as yaml file. "
            "default exports outports, local variables, calibration constants and nvm variables. "
            "inports also exports inport variables.",
        )
        parser.add_argument(
            "--include",
            default="matlab-scripts",
            help="Path to folder containing Matlab scripts and simulink libraries to include.",
        )
        parser.set_defaults(func=run_wrapper)

        subparsers = parser.add_subparsers(help="PyBuild specific build.")
        build_specific_parser = subparsers.add_parser(
            "build-specific", help="Run PyBuild for project with specific settings."
        )
        build.add_args(build_specific_parser)

        # Matlab arguments added by parent:
        pt_matlab.Matlab.add_args(parser)


def run_wrapper(args: argparse.Namespace) -> int:
    """Run PyBuildWrapper."""
    if args.build is not None and getattr(args, "project_config", None) is not None:
        LOGGER.error("Cannot run both PyBuild quick build (--build <PROJECT>) " "and specific build (build-specific).")
        return 1

    wrapper = PyBuildWrapper(args)

    if args.regenerate_tl_settings_hashes:
        wrapper.regenerate_target_link_settings_file_hashes()

    if args.export_global_vars is not None:
        wrapper.export_global_variables(args.export_global_vars)

    return wrapper.run()


def main(argv: Optional[List[str]] = None) -> int:
    """Run PyBuildWrapper"""
    parser = argparse.ArgumentParser("PyBuild Wrapper")
    PyBuildWrapper.add_args(parser)
    args = parser.parse_args(argv)
    return run_wrapper(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
