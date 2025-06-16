from metaflow.exception import MetaflowException
from metaflow.decorators import StepDecorator
from metaflow import current
from .app_utils import start_app
from .supervisord_utils import SupervisorClient, SupervisorClientException
import os
import random
import string
import tempfile
import sys
from .consts import (
    BASE_DIR_FOR_APP_ASSETS,
    DEFAULT_WAIT_TIME_SECONDS_FOR_PROCESS_TO_START,
)

"""
There are 3 variants of starting apps that we support through this function. Which variant is applied is
a result of the user setting (or not setting) self.entrypoint and self.app_dir.

The chosen variant determines whether or not the user will have an easy (auto-magical) way to write their
Metaflow artifacts the the directory where their app will be run from. This will simplify managing models
from inside the code.

Case 1:
    Desired Behavior:
        The user doesn't care about auto-magical artifact management, they just have a server.py somewhere and
        they want to run it.
    How:
        The user sets self.entrypoint to the name of their file (optionally with any args).
        The value of self.app_dir is irrelevant.
        Example: self.entrypoint = "/home/ob-workspace/my_random_directory/my_subfolder/server.py --my_arg 764"
    Expected Behavior:
        The users app will be started using a conda environment built by Metaflow, that's it.

Case 2:
    Desired Behavior:
        The user has defined a clean package/module structure with a __main__.py in a folder somewhere. They would like
        to run this module as an app. They would like to access models in the same top level directory as their app.
    How:
        The user sets self.entrypoint to None.
        The user sets self.app_dir to the top level directory of their app.
        Example: self.app_dir = "/home/ob-workspace/my_random_directory/my_subfolder"
        (my_subfolder HAS to contain a __main__.py file.)
    Expected Behavior:
        The users app will be started using a conda environment built by Metaflow. The user gets access to self.deploy_dir where they
        write their artifacts. After the user writes their artifacts to self.deploy_dir, the artifacts and the app is copied over
        to an internal directory where we will deploy the app from.
        The internal directory is: /home/ob-workspace/.appdaemon/apps/<app_port>.
        <app_port> will contain user's __main__.py and other files (copied recursively), as well as their artifacts that they wrote to
        self.deploy_dir. self.deploy_dir/my_model becomes <app_port>/my_model. my_subfolder/__main__.py becomes <app_port>/__main__.py.

Case 3:
    Desired Behavior:
        The user follows the Outerbounds convention, which is the same as Case 2, except the app is actually in the same top level folder
        as the Deployer flow. They would like to access models as usual.
    How:
        The user sets self.entrypoint to None (or doesn't set it at all).
        The user sets self.app_dir to None (or doesn't set it at all).
    Expected Behavior:
        The users app will be started using a conda environment built by Metaflow. Everything else is exactly the same as Case 2.
"""


class WorkstationAppDeployDecorator(StepDecorator):
    """
    Specifies that this step is used to deploy an instance of the app.
    Requires that self.app_name, self.app_port, self.entrypoint and self.deployDir is set.

    Parameters
    ----------
    app_port : int
        Number of GPUs to use.
    app_name : str
        Name of the app to deploy.
    """

    name = "app_deploy"
    defaults = {"app_port": 8080, "app_name": "app"}

    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        if any([deco.name == "kubernetes" for deco in decos]):
            raise MetaflowException(
                "@app_deploy decorator is only supported locally and does not work with remote execution environments like @kubernetes, @nvidia."
            )

        # We always need to have some environment defined through the flow to deploy and app.
        # Which means either step decorators like @pypi / @conda must be defined.
        # or flow level decorators like @conda_base / @pypi_base.
        if not any([deco.name == "pypi" or deco.name == "conda" for deco in decos]):
            flow_decorators = flow._flow_decorators.keys()
            if (
                "conda_base" not in flow_decorators
                and "pypi_base" not in flow_decorators
            ):
                raise MetaflowException(
                    "@app_deploy requires either step decorators like @pypi / @conda or flow level decorators like @conda_base / @pypi_base to be defined."
                )

        app_port = self.attributes["app_port"]
        app_name = self.attributes["app_name"]

        # Currently this decorator is expected to only execute on workstation.
        if app_port is None or app_port < 6000 or app_port > 6002:
            raise MetaflowException(
                "AppDeployDecorator requires app_port to be between 6000 and 6002."
            )

        if app_name is None:
            raise MetaflowException("AppDeployDecorator requires app_name to be set.")

    def task_pre_step(
        self,
        step_name,
        task_datastore,
        metadata,
        run_id,
        task_id,
        flow,
        graph,
        retry_count,
        max_user_code_retries,
        ubf_context,
        inputs,
    ):
        """
        Runs before the step decorated with @app_deploy has started.
        We create a directory where the user can write their artifacts and expose it via self.deploy_dir.
        """
        os.makedirs(BASE_DIR_FOR_APP_ASSETS, exist_ok=True)
        # First we want to create a directory where the user's app directory and artifacts can be stored.
        with tempfile.TemporaryDirectory(
            prefix=BASE_DIR_FOR_APP_ASSETS, delete=False
        ) as temp_dir:
            launch_temp_dir = temp_dir

        # Expose this to the user, so that they can use it write their artifacts.
        setattr(flow, "deploy_dir", launch_temp_dir)

        # Make sure to record deploy_dir so that the user cannot accidentally override it.
        self._deploy_dir = launch_temp_dir

    def task_post_step(
        self, step_name, flow, graph, retry_count, max_user_code_retries
    ):
        """
        Runs after the step decorated with @app_deploy has finished.
        Based on the cases above, things that we care about are self.entrypoint and self.app_dir.
        """

        deploy_dir = self._deploy_dir

        # By default we assume that the user has a __main__.py file in their app directory.
        # They can always override this behavior.
        user_provided_entrypoint = getattr(flow, "entrypoint", None)

        if user_provided_entrypoint is not None and not isinstance(
            user_provided_entrypoint, str
        ):
            raise MetaflowException(
                f"@app_deploy requires entrypoint to be set to a string. The current value of entrypoint {user_provided_entrypoint} is not valid."
            )

        flow_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

        app_location = getattr(
            flow, "app_dir", os.path.join(flow_directory, self.attributes["app_name"])
        )

        if user_provided_entrypoint is None and not os.path.exists(app_location):
            raise MetaflowException(f"App directory {app_location} does not exist.")

        wait_time_for_app_start = getattr(
            flow,
            "wait_time_for_app_start",
            DEFAULT_WAIT_TIME_SECONDS_FOR_PROCESS_TO_START,
        )

        try:
            supervisor_client = SupervisorClient(
                wait_time_seconds_for_app_start=wait_time_for_app_start
            )

            # First, let's deploy the app.
            start_app(
                port=self.attributes["app_port"], name=self.attributes["app_name"]
            )

            # Now, let's add the app to supervisor.
            supervisor_client.start_process_with_supervisord(
                self.attributes["app_name"],
                self.attributes["app_port"],
                user_provided_entrypoint,
                deploy_dir,
                app_location,
            )
        except SupervisorClientException as e:
            raise MetaflowException(str(e))
        except Exception as e:
            raise MetaflowException(
                f"Failed to start {self.attributes['app_name']}! Cause: {str(e)}"
            ) from e
