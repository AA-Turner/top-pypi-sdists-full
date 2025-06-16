import argparse
import os
import configparser
import tempfile
import sys
import subprocess
from pathlib import Path
import shutil
from enum import Enum
import time
from .consts import BASE_DIR_FOR_APP_ASSETS, APP_DAEMON_WORKSTAION_PATH


class SupervisorClientException(Exception):
    pass


class SupervisorClient:
    """
    A client for starting and stopping apps using supervisor.
    """

    def __init__(self, wait_time_seconds_for_app_start: int):
        self.supervisor_conf_loc = os.environ.get("SUPERVISOR_CONF_PATH")

        self.wait_time_seconds_for_app_start = wait_time_seconds_for_app_start
        if self.supervisor_conf_loc is None or not os.path.exists(
            self.supervisor_conf_loc
        ):
            raise SupervisorClientException(
                "This workstation does not support deploying apps! Please reach out to Outerbounds for support."
            )

        self.metaflow_envs_persistent_path = os.environ.get(
            "SUPERVISOR_PYTHON_ENVS_PATH"
        )
        if self.metaflow_envs_persistent_path is None:
            raise SupervisorClientException(
                "This workstation does not support deploying apps! Please reach out to Outerbounds for support."
            )

        # Check if supervisorctl is installed
        if not shutil.which("supervisorctl"):
            raise SupervisorClientException(
                "This workstation does not support deploying apps! Please reach out to Outerbounds for support."
            )

    def _stop_existing_app_at_port(self, app_port):
        supervisor_config = configparser.ConfigParser()
        supervisor_config.read(self.supervisor_conf_loc)

        for program in supervisor_config.sections():
            if "obp_app_port" in supervisor_config[program]:
                if supervisor_config[program]["obp_app_port"].strip() == str(app_port):
                    res = subprocess.run(
                        ["supervisorctl", "stop", program],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )

                    del supervisor_config[program]

        with tempfile.NamedTemporaryFile(
            "w", dir=os.path.dirname(self.supervisor_conf_loc), delete=False
        ) as f:
            supervisor_config.write(f)
            tmp_file = f.name

        os.rename(tmp_file, self.supervisor_conf_loc)

    def _create_supervisor_conf_entry(
        self, command, launch_directory, app_port, app_name
    ):
        entry = {
            "command": command,
            "directory": launch_directory,
            "autostart": "true",
            "autorestart": "true",
            "obp_app_port": app_port,  # Record the app port for internal reference. This is not used by supervisor.
        }

        supervisor_config = configparser.ConfigParser()
        supervisor_config.read(self.supervisor_conf_loc)

        supervisor_config[f"program:{app_name}"] = entry

        with tempfile.NamedTemporaryFile(
            "w", dir=os.path.dirname(self.supervisor_conf_loc), delete=False
        ) as f:
            supervisor_config.write(f)
            tmp_file = f.name

        os.rename(tmp_file, self.supervisor_conf_loc)

    def start_process_with_supervisord(
        self,
        app_name,
        app_port,
        user_provided_entrypoint,
        deploy_dir=None,
        app_dir=None,
    ):
        """
        Starts the app using supervisor.

        Args:
            app_name: The name of the app to start.
            app_port: The port to start the app on.
            user_provided_entrypoint: The entrypoint to start the app with.
            deploy_dir: The directory to copy the app to and deploy from.
            app_dir: The directory to copy the app from.
        """

        entrypoint = user_provided_entrypoint
        deploy_dir_for_port = os.path.join(BASE_DIR_FOR_APP_ASSETS, str(app_port))
        launch_directory = (
            BASE_DIR_FOR_APP_ASSETS
            if entrypoint is None
            else APP_DAEMON_WORKSTAION_PATH
        )

        # Stop any existing apps that are running on the same port.
        self._stop_existing_app_at_port(app_port)

        # This means the user has opted for either case 2 or case 3.
        # Cases 2 and 3 are handled the same way, the only thing that differs is self.app_dir.
        if user_provided_entrypoint is None:
            # Copy the app_dir to the deploy_dir.
            # This is also where all (if any) artifacts are written.
            recursive_copy(app_dir, deploy_dir)

            # Copy the entire deploy_dir to the port specific directory.
            # Clear out anything that was there before (maybe a different app's assets)
            if os.path.exists(deploy_dir_for_port):
                shutil.rmtree(deploy_dir_for_port)

            os.makedirs(deploy_dir_for_port)
            recursive_copy(deploy_dir, deploy_dir_for_port)

            # Apply default value
            # We launch the module from BASE_DIR_FOR_APP_ASSETS, so when we provide the -m flag we don't need (and can't use) the full path.
            # We just need to provide the port number (which is also the name of the folder where all app assets are stored)
            entrypoint = f"-m {str(app_port)}"

        # deploy_dir is meant to be temporary. No need to keep it around after everything has been copied over.
        shutil.rmtree(deploy_dir)

        # Metaflow by default generates the environment in /root/... (which is not persisted on workstations).
        # Since the environment is fully self contained, we can copy it to a persistent location.
        persistent_path_for_executable = (
            self._persist_metaflow_generated_python_environment()
        )

        # This is the command used by supervisord to launch the app.
        command = f"{persistent_path_for_executable} {entrypoint}"

        self._create_supervisor_conf_entry(
            command, launch_directory, app_port, app_name
        )

        # Execute supervisorctl reload
        # Capture the exit code
        exit_code = subprocess.run(
            ["supervisorctl", "reload"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode
        if exit_code != 0:
            raise SupervisorClientException(
                "Failed to start app! Contact Outerbounds for support."
            )

        print(
            f"Waiting for {self.wait_time_seconds_for_app_start} seconds for {app_name} to start..."
        )
        time.sleep(self.wait_time_seconds_for_app_start)

        self._raise_on_bad_status(app_name, command)

    def _get_launched_prcoess_status(self, app_name, debug_command):
        """
        Checks the status of the launched process. If the status is not RUNNING or STARTING, it raises an exception.
        Possible statuses: RUNNING, STARTING, STOPPED, BACKOFF, STOPPING, EXITED, FATAL, UNKNOWN

        Args:
            app_name: The name of the app to check the status of.
            debug_command: The command to run to debug the app.
        """
        status_cmd_output = subprocess.run(
            ["supervisorctl", "status", app_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout.decode("utf-8")

        status_cmd_output_parts = [
            x.strip() for x in status_cmd_output.split(" ") if x.strip()
        ]

        status_str = status_cmd_output_parts[1]

        if not status_str == "RUNNING" and not status_str == "STARTING":
            raise SupervisorClientException(
                f"Failed to start {app_name}! Try running {debug_command} manually to debug."
            )

    def _persist_metaflow_generated_python_environment(self):
        """
        Persists the metaflow generated python environment to a persistent location.
        The step already runs in the environment generated by Metaflow.
        """
        current_executable = sys.executable
        environment_path = Path(current_executable).parent.parent

        persistent_path_for_this_environment = os.path.join(
            self.metaflow_envs_persistent_path,
            environment_path.parent.name,
            environment_path.name,
        )

        final_executable_path = os.path.join(
            persistent_path_for_this_environment,
            Path(current_executable).parent.name,
            Path(current_executable).name,
        )

        if os.path.exists(final_executable_path):
            return final_executable_path

        os.makedirs(persistent_path_for_this_environment, exist_ok=True)

        recursive_copy(environment_path, persistent_path_for_this_environment)

        return final_executable_path


def recursive_copy(src, dst):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
