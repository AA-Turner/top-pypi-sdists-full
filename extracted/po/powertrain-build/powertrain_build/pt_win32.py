# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Wrapper for win32api to simplify it's use.

See pywin32 documentation or windows api documentation for more information.
"""

from powertrain_build.lib.helper_functions import merge_dicts

STILL_ACTIVE = 259

try:
    import win32job
    import win32process

    class PtWin32Process:
        """Alternative to python subprocess.

        This adds functionality to add processes to win32 job containers
        to force processes to terminate after it's parent process dies.
        """

        def __init__(self, kill_on_job_close=True):
            """Set up default values.

            arguments:
            kill_on_job_close (boolean): If True the process will be terminated when all job
                                         handles are closed.
            """
            self.process_handle = None
            self.thread_handle = None
            self.job_handle = None
            self.process_id = None
            self.thread_id = None
            self.process_attributes = None
            self.thread_attributes = None
            self.b_inherit_handles = True
            self.dw_creation_flags = 0
            self.new_environment = None
            self.current_directory = None
            self.job_limit_flag_list = []
            self.startup_info = win32process.STARTUPINFO()
            self.limit_info_dict = {"BasicLimitInformation": {"LimitFlags": 0}}

            if kill_on_job_close:
                self.add_limit_flags(win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE)

        def run(self, app_name=None, command=None):
            """Run process.

            Can be run with either a specified application, a command line string or both.

            Keyword arguments:
            app_name (string): path to application to execute.
            command (string): command line string to use in execution.
            """
            self.process_handle, self.thread_handle, self.process_id, self.thread_id = win32process.CreateProcess(
                app_name,
                command,
                self.process_attributes,
                self.thread_attributes,
                self.b_inherit_handles,
                self.dw_creation_flags,
                self.new_environment,
                self.current_directory,
                self.startup_info,
            )

            self.job_handle = win32job.CreateJobObject(None, "")
            limit_information = self.get_extended_limit_information()
            limit_information = merge_dicts(self.limit_info_dict, limit_information, merge_recursively=True)
            win32job.SetInformationJobObject(
                self.job_handle, win32job.JobObjectExtendedLimitInformation, limit_information
            )
            win32job.AssignProcessToJobObject(self.job_handle, self.process_handle)

        def get_extended_limit_information(self):
            """Get extended limit information."""
            return win32job.QueryInformationJobObject(self.job_handle, win32job.JobObjectExtendedLimitInformation)

        def set_current_directory(self, current_directory):
            """Set process working directory."""
            self.current_directory = current_directory

        def set_environment(self, environment):
            """Set process environment variables.

            If not set the process will inherit parent process environment.

            arguments:
            environment (dict): a dictionary with environment variables to be set.
            """
            self.new_environment = environment

        def set_creation_flags(self, creation_flags):
            """Set creation flags.

            arguments:
            creation_flags (int): See pywin32 documentation or windows api for documentation.
            """
            self.dw_creation_flags = creation_flags

        def add_limit_flags(self, limit_flags):
            """Add limit flag."""
            new_limit_flags = self.get_limit_flags() | limit_flags
            self.set_limit_flags(new_limit_flags)

        def remove_limit_flags(self, limit_flags):
            """Remove limit flag."""
            new_limit_flags = self.get_limit_flags() & ~limit_flags
            self.set_limit_flags(new_limit_flags)

        def get_limit_flags(self):
            """Get limit flags."""
            return self.limit_info_dict["BasicLimitInformation"]["LimitFlags"]

        def set_limit_flags(self, win32job_limit):
            """Set limit flags.

            arguments:
            win32job_limit (int): See pywin32 documentation or windows api documentation.
            """
            self.limit_info_dict.update({"BasicLimitInformation": {"LimitFlags": win32job_limit}})

        def poll(self):
            """Return process status.

            If process is still running it will return exitcode 259 (STILL_ACTIVE).
            """
            return win32process.GetExitCodeProcess(self.process_handle)

        def terminate(self):
            """Terminate all processes associated with the job."""
            return win32job.TerminateJobObject(self.job_handle)

except ImportError:

    class PtWin32Process:
        """Dummy."""

        def __init__(self, kill_on_job_close=True):
            """Dummy."""
            raise OSError("pywin32 is not installed or is not compatible with this platform")
