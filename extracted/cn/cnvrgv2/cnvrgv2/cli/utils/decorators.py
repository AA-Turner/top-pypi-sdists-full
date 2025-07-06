import inspect
from functools import wraps

import click

from cnvrgv2 import Cnvrg
from cnvrgv2.cli.logger.logger import CnvrgLogger
from cnvrgv2.cli.utils import messages
from cnvrgv2.cli.utils.validators import verify_login
from cnvrgv2.config import Config
from cnvrgv2.config import error_messages
from cnvrgv2.errors import CnvrgError
from cnvrgv2.modules.workflows.endpoint.endpoint import Endpoint
from cnvrgv2.modules.workflows.experiment.experiment import Experiment
from cnvrgv2.modules.workflows.webapp.webapp import Webapp
from cnvrgv2.modules.workflows.workspace.workspace import Workspace


def prepare_command():
    """
    This decorator logs a start log for a cli command, can validate if the user is logged in, and injects
    the cnvrg object and logger object to the cli command function, if the arguments are expected by the function
    @return: the decorator function
    """

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            verify_login()
            cnvrg = Cnvrg()
            config = Config()
            # In case the user logged in through the sdk, the config file might not exist. config.save will create it
            config.save()
            logger = CnvrgLogger(click)
            command_name = func.__name__

            log_message = messages.LOG_START_COMMAND.format(command_name, str(kwargs))
            logger.info(log_message)

            func_args = inspect.getfullargspec(func).args
            inject_args = dict()

            def _try_load_project():
                project_slug = config.data_owner_slug or kwargs.get("project_slug")
                return cnvrg.projects.get(project_slug)

            if "cnvrg" in func_args:
                inject_args["cnvrg"] = cnvrg
            if "logger" in func_args:
                inject_args["logger"] = logger
            if "project" in func_args:
                inject_args["project"] = _try_load_project()

            if "dataset" in func_args:
                dataset_slug = config.data_owner_slug
                if not dataset_slug:
                    logger.log_and_echo(error_messages.LOCAL_CONFIG_MISSING_DATA_OWNER_SLUG, error=True)
                inject_args["dataset"] = cnvrg.datasets.get(dataset_slug)

            if "experiment" in func_args:
                try:
                    inject_args["experiment"] = Experiment()
                except CnvrgError:
                    slug = kwargs.get("slug")
                    project = _try_load_project()
                    inject_args["experiment"] = project.experiments.get(slug)

            if "workspace" in func_args:
                try:
                    inject_args["workspace"] = Workspace()
                except CnvrgError:
                    slug = kwargs.get("slug")
                    project = _try_load_project()
                    inject_args["workspace"] = project.workspaces.get(slug)

            if "endpoint" in func_args:
                try:
                    inject_args["endpoint"] = Endpoint()
                except CnvrgError:
                    slug = kwargs.get("slug")
                    project = _try_load_project()
                    inject_args["endpoint"] = project.endpoints.get(slug)

            if "webapp" in func_args:
                try:
                    inject_args["webapp"] = Webapp()
                except CnvrgError:
                    slug = kwargs.get("slug")
                    project = _try_load_project()
                    inject_args["webapp"] = project.webapps.get(slug)

            n_kwargs = {**kwargs, **inject_args}
            func(*args, **n_kwargs)

        return inner

    return decorator


def prepare_command_without_context():
    """
    This decorator logs a start log for a cli command, can validate if the user is logged in, and injects
    the cnvrg object and logger object to the cli command function, if the arguments are expected by the function
    @return: the decorator function
    """

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            logger = CnvrgLogger(click)
            command_name = func.__name__

            log_message = messages.LOG_START_COMMAND.format(command_name, str(kwargs))
            logger.info(log_message)

            func_args = inspect.getfullargspec(func).args
            inject_args = dict()

            if "logger" in func_args:
                inject_args["logger"] = logger
            n_kwargs = {**kwargs, **inject_args}
            func(*args, **n_kwargs)

        return inner

    return decorator
