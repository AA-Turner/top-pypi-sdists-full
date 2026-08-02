# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Library for using matlab.

Called pt_matlab to not collide with Mathwork's matlab package.
"""

import logging
import os
import platform
import subprocess
import sys
import time

my_system = platform.system()
if my_system == "Darwin":
    MATLAB_BIN = os.environ.get(
        "MatInstl",
        os.environ.get("MatInstl2017", "/Applications/MATLAB_R2020a.app/bin/matlab")
    )
elif my_system == "Linux":
    MATLAB_BIN = os.environ.get("MatInstl", os.environ.get("MatInstl2017", "/usr/local/MATLAB/R2017b/bin/matlab"))
else:
    from . import pt_win32
    MATLAB_BIN = os.environ.get("MatInstl", os.environ.get("MatInstl2017", "C:\\MATLABR2017b_x64\\bin\\matlab.exe"))

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
RETRY_TIME = 10
POLL_TIME = 1


def get_env():
    """Get environment variables."""
    env = os.environ.copy()
    workspace = os.environ.get("WORKSPACE", "")
    if workspace:
        env["MATLAB_PREFDIR"] = os.path.join(workspace, "ConfigDocuments", "buildSlaveMatlabSettings")
    return env


def wrap_command(command):
    """Wrap a command in a try-catch with an exit at the end.

    Use this to be sure never to raise an error in matlab that causes a hanging matlab.
    This is useful when writing matlab scripts to be used in jenkins jobs.

    Args:
        command (str): command to wrap in try-catch-exit.
    Returns:
        command (str): the command wrapped in try-catch-exit
    """
    return f"try;exitcode=0;{command};catch err;disp(getReport(err));exitcode=1;end;exit(exitcode);"


def wrap_m_script(path_to_mscript):
    """Wrap a path to an m-script to ensure no jobs in jenkins are left hanging.

    This is useful when writing matlab scripts to be used in jenkins jobs.

    Args:
        path_to_mscript (str): file to run in matlab.
    Returns:
        command (str): the command to send to matlab to run the script
    """
    mscript_folder, mscript_file = os.path.split(path_to_mscript)
    LOGGER.debug("Using folder %s for the m-script", mscript_folder)
    if mscript_folder:
        command = wrap_command(
            f"addpath('{mscript_folder}');assert(boolean(exist('{mscript_file[:-2]}')));{mscript_file[:-2]}"
        )
    else:
        command = wrap_command(f"assert(boolean(exist('{mscript_file[:-2]}')));{mscript_file[:-2]}")
    return f'"{command}"'


def list_to_cell(python_list):
    """Convert a python list to a cell argument string for matlab.

    Args:
        python_list (list): A list in python
    Returns:
        cell (str): A cell to be read by Matlab.
    """
    matlab_list = "', '".join(python_list)
    return f"{{'{matlab_list}'}}"


def write_m_script(mfile, base_cmd, wrap_cmd=True):
    """Write an m-script to run from the command line.

    The m-script will exit Matlab with an exitcode.
    This exitcode can be set in the base_cmd if needed.

    Args:
        mfile (str): path to m-file to create
        base_cmd (str): Base command to run in Matlab
        wrap_cmd (bool): wrap command
    """
    if wrap_cmd:
        cmd = wrap_command(base_cmd)
    else:
        cmd = base_cmd
    LOGGER.debug("Writing %s", mfile)
    with open(mfile, mode="w", encoding="utf-8") as m_file:
        m_file.writelines(cmd.split(os.linesep))


def is_model(model_file):
    """Check if a file name is a simulink model or not.

    Args:
        model_file (str): filename to check
    """
    return model_file.endswith(".mdl") or model_file.endswith(".slx")


def extract_model_names(files, ending):
    """Find model names from path to files.

    Checks if the files corresponds to model files.

    Args:
        files (list): files that potentially corresponds to models
        ending (str): file ending that is used for models.
    Returns:
        found_models (list): Models to run checkscripts on.
    """
    found_models = []
    for found_file in files:
        name = os.path.basename(found_file)
        if name.endswith(ending):
            name = name[: -len(ending)]
            found_models.append(name)
    return found_models


def cmd_path(path, subdirs=False):
    """Generate Matlab command text for adding supplied path and subdirectories.

    Args:
        path (str): Path to generate commands for adding.
        subdirs (bool): If True, recursively adds subdirs. Default: False

    Returns:
        cmds (list): Commands as a list of strings.
    """
    return f"addpath(genpath('{path}'))" if subdirs else f"addpath('{path}')"


def cmd_callfunc(func, *args):
    """Generate Matlab command for calling a function with optional arguments.

    Example: cmd_callfunc('my_function')
             cmd_callfunc('my_function', 'argument 1', 'argument 2')

    Args:
        func (str): Name of function to call.
        args (argument list): Variadic argument list to pass to function.
    Returns:
        cmd (str): Command text for calling function.
    """
    args = ", ".join([cmd_arg(arg) for arg in args])
    return f"{func}({args})"


def cmd_arg(arg):
    """Transform Python argument to Matlab argument."""
    if isinstance(arg, str):
        return f"'{arg}'"
    if isinstance(arg, bool):
        return "true" if arg else "false"
    if isinstance(arg, list):
        return list_to_cell(arg)
    raise ValueError("Unable to convert argument to Matlab type")


def cmds_join(cmds):
    """Join several Matlab command strings together, separated by terminators and newlines.

    Args:
        cmds (list): List of command string to join together.
    Returns:
        cmds (str): Command text for executing all supplied commands.
    """
    return f";{os.linesep}".join(cmds)


class TargetlinkWatcher(logging.StreamHandler):
    """Class to check output log for known error messages."""

    intermittent_errors = [
        "Undefined function 'tl_pref' for input arguments of type 'char'",
        "Undefined function 'dsdd_manage_project' for input arguments of type 'char'.",
        "Exception: ACCESS_VIOLATION",
    ]

    def __init__(self, stream):
        """Init."""
        super().__init__(stream)
        self.targetlink_error = False

    def reset_errors(self):
        """Reset errors."""
        self.targetlink_error = False

    def emit(self, record):
        """Set error flag on error message in log."""
        for intermittent_error in self.intermittent_errors:
            if intermittent_error in record.getMessage():
                self.targetlink_error = True
        super().emit(record)


class MatlabWatcher(logging.StreamHandler):
    """Class to check output log for sucess message."""

    success_message = "Matlab task succeeded!"

    def __init__(self):
        """Init."""
        super().__init__()
        self.task_success = False

    def reset_errors(self):
        """Reset errors."""
        self.task_success = False

    def emit(self, record):
        """Set success flag on success message in log."""
        if self.success_message in record.getMessage():
            self.task_success = True


class Matlab:
    """Wrapper for calling matlab from python scripts.

    The wrapper runs a m-script and optionally pipes the logs to stdout.
    """

    def __init__(self, log=None, dry_run=False, matlab_bin=MATLAB_BIN, nojvm=True):
        """Init.

        Args:
            log (str): file name to log to. Default: None
            dry_run (bool): Run a mocked version of matlab. Default: False
            matlab_bin (str): path to matlab binary to use in execution
            nojvm (bool): False if jvm should be used. Default: True
        """
        self.log = log
        self.dry_run = dry_run
        self.nojvm = nojvm
        self.targetlink_watcher = TargetlinkWatcher(sys.stdout)
        self.matlab_watcher = MatlabWatcher()
        self.mlogger = self.create_logger()
        self.mlogger.addHandler(self.matlab_watcher)
        self.open_log_file = None
        self.matlab_bin = matlab_bin

    @staticmethod
    def add_args(parser):
        """Parse arguments."""
        matlab_parser = parser.add_argument_group("matlab arguments")
        matlab_parser.add_argument(
            "--matlab-bin",
            help=f"Path to the matlab binary to use. Defaults to {MATLAB_BIN}.",
            default=MATLAB_BIN,
        )

    def create_logger(self):
        """Create logger for matlab.

        Returns:
            logger (logging.Logger): Logger for matlab.
        """
        handler = self.targetlink_watcher
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(message)s"))
        logger = logging.getLogger("matlab")
        logger.addHandler(handler)
        return logger

    def sync_log(self, last_stat):
        """Read the latest loglines from the matlab log and write to log.

        Checks if the matlab log file has been updated since last call and
        redirects new entries to the python log.
        If self.log is None, this function returns None at once.

        Args:
            last_stat (os.stat): last timestamp for an updated log.
        Returns:
            new_stat (os.stat): new timestamp for an updated log.
        """
        if self.open_log_file is None:
            return None
        current_position = self.open_log_file.tell()
        if os.stat(self.open_log_file.name) == last_stat:
            return last_stat  # Do not read partial lines again.
        for line in self.open_log_file.readlines():
            # The non-finished lines behaviour was sometimes seen when using diary.
            # It should not hurt to have, but if it is causing problems, just remove it.
            # It is purely cosmetic.
            if line.endswith("\n"):
                if line != "\n":  # Skip the end of the line we jumped to from a non-finished line
                    self.mlogger.info(line[0:-1])
            else:
                LOGGER.debug("Partial line read. Go back and wait for update.")
                self.open_log_file.seek(current_position - len(line))
                break
            current_position = self.open_log_file.tell()
        return os.stat(self.open_log_file.name)

    def compose_m_script_cmd(self, mfile, wrap_cmd):
        """Compose batch script to run matlab."""

        if my_system in {"Darwin", "Linux"}:
            cmd = [
                self.matlab_bin if not self.dry_run else "echo",
                "-nodisplay",
                "-nodesktop",
            ]
        else:
            cmd = [
                self.matlab_bin if not self.dry_run else "cmd rem",
                "-nodisplay",
                "-nodesktop",
                "-wait",
                "-minimize",
            ]

        if self.log:
            cmd += ["-logfile", self.log]
        if self.nojvm:
            cmd += ["-nojvm"]
        if wrap_cmd:
            if my_system == "Darwin":
                cmd += ["<", wrap_m_script(mfile)]
            else:
                cmd += ["-r", wrap_m_script(mfile)]
        else:
            if my_system == "Darwin":
                cmd += ["<", mfile]
            else:  # Linux will be similar to Windows
                cmd += ["-r", mfile[:-2]]

        return cmd

    def run_m_script(self, mfile, wrap_cmd=True, attempts=10):
        """Run the composed m-script.

        Args:
            mfile (str): The composed m-script
            wrap_cmd (bool): wrap command (Default: True)
            attempts (int): Number of times to run the command again if an intermittent problem
                            is detected (Default: 1)
        Returns:
            process_status: Exitcode from Matlab (or 1 if Matlab was never started)
        """

        def wait_for_process(p_matlab, stat=None):
            stat = self.sync_log(None)  # Initial sync in case matlab has already finished

            if my_system in {"Darwin", "Linux"}:
                while p_matlab.poll() is None:
                    time.sleep(POLL_TIME)
                    stat = self.sync_log(stat)
            else:
                while p_matlab.poll() == pt_win32.STILL_ACTIVE:
                    time.sleep(POLL_TIME)
                    stat = self.sync_log(stat)

        if attempts <= 0:
            LOGGER.error("Already attempted this too many times. Exiting.")
            return 2  # Do not trust previous exit codes

        if self.log and os.path.isfile(self.log):
            os.remove(self.log)

        p_matlab = None
        process_status = 1  # Something could go wrong in the try, before the exitcode is set

        try:
            env = get_env()
            LOGGER.debug("Running in dry_run mode: %s", self.dry_run)
            cmd = self.compose_m_script_cmd(mfile, wrap_cmd)
            LOGGER.debug("Calling: %s", " ".join(cmd))

            if my_system in {"Darwin", "Linux"}:
                p_matlab = subprocess.Popen(cmd)
            else:
                p_matlab = pt_win32.PtWin32Process()
                p_matlab.set_environment(env)
                p_matlab.run(command=" ".join(cmd))

            if not self.dry_run:
                if self.log:
                    # Wait for log file to be created
                    if my_system in {"Darwin", "Linux"}:
                        while not os.path.isfile(self.log) and p_matlab.poll() is None:
                            time.sleep(POLL_TIME)
                    else:
                        while not os.path.isfile(self.log) and p_matlab.poll() == pt_win32.STILL_ACTIVE:
                            time.sleep(POLL_TIME)

                self.open_log_file = open(self.log, "r", encoding="utf-8", errors='ignore') if self.log else None

            wait_for_process(p_matlab)
            process_status = p_matlab.poll()

            LOGGER.info("Matlab returned with exitcode %s", process_status)
            if self.targetlink_watcher.targetlink_error:
                LOGGER.warning("Found an intermittent targetlink problem. Trying again, attempts left: %s", attempts)
                if self.open_log_file:
                    self.open_log_file.close()
                self.targetlink_watcher.reset_errors()
                time.sleep(RETRY_TIME)
                process_status = self.run_m_script(mfile, wrap_cmd=wrap_cmd, attempts=attempts - 1)
        finally:
            if my_system in {"Darwin", "Linux"}:
                if p_matlab.poll() is not None:
                    p_matlab.terminate()
                    p_matlab.wait()
            else:
                if p_matlab.poll() == pt_win32.STILL_ACTIVE:
                    p_matlab.terminate()

            if self.open_log_file:
                self.open_log_file.close()
        return process_status
