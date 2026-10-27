"""The `Connector` a customer's connector.py creates, with the same constructor and public methods as the one that
runs on Fivetran.

There is no server: the in-process runner calls `get_schema`, `get_configuration_form`, `run_test` and `run_update`
directly, in the same process, with the same log lines and error messages.
"""
import atexit
import faulthandler
import os
import sys
import traceback

from types import GeneratorType

from fivetran_connector_sdk_common import __version__, constants
from fivetran_connector_sdk_common.configuration import check_dict
from fivetran_connector_sdk_common.constants import PYPROJECT_TOML
from fivetran_connector_sdk_common.helpers import print_library_log
from fivetran_connector_sdk_common.logger import Logging
from fivetran_connector_sdk_core import ConnectorTask, SchemaResult as SchemaResponse  # the tables the connector declares, or `not_supported`
from fivetran_connector_sdk_cli import configuration_command, core_adapter, schema_processing
from fivetran_connector_sdk_cli.cli_commands import _deploy_connector
from fivetran_connector_sdk_cli.cli_helpers import PromptMode, _resolve_existing_project_path, resolve_confirmation
from fivetran_connector_sdk_cli.connector_helper import (
    DeployOptions, check_newer_version, exit_check, update_base_url_if_required, validate_configuration,
    validate_pyproject_file, validate_requirements_file,
)
from fivetran_connector_sdk_cli.crash_report import build_debug_crash_report, save_crash_report
from fivetran_connector_sdk_cli.memory_tracker import DebugMemoryTracker
from fivetran_connector_sdk_cli.schema_processing import process_tables
from fivetran_connector_sdk_cli.test import TestResponse


class _ConnectorFailure(RuntimeError):
    """A failure of a handler, whose message already holds its traceback: whoever reports it has no traceback of its own to add."""


def _failure(error_message: str, error: BaseException) -> RuntimeError:
    """The error a failed handler raises: its message, then the whole traceback so that it is shown to the developer. It is shown
    where the failure is reported (the end of the run, or the command), and nowhere else: a handler does not log it too.

    A traceback ends with the exception and its message, which `error_message` has already said: that line says the type and points
    back, so that a message of several lines is not printed twice."""
    text = "".join(traceback.format_exception(error))
    last = "".join(traceback.format_exception_only(error))
    if last and text.endswith(last):
        text = f"{text[:-len(last)]}{type(error).__qualname__}: the message is above\n"
    return _ConnectorFailure(f"{error_message}\n{text}")


class Connector:
    # noinspection PyShadowingNames
    def __init__(self, update, schema=None, configuration_form=None):
        """Initializes the Connector instance.
        Args:
            update: The update method.
            schema: The schema method.
            configuration_form: Optional callable returning a ConfigurationForm instance.
        """

        self.schema_method = schema
        self.update_method = update
        self.configuration_form_method = configuration_form
        self._cached_form = None

        self.configuration = None
        self.state = None
        self.project_path = None
        self._debug_crash_report = None

        if not constants.EXECUTED_VIA_CLI:
            update_base_url_if_required()

    # Call this method to deploy the connector to Fivetran platform
    def deploy(self, project_path: str, deploy_key: str, group: str, connection: str, hd_agent_id: str,
               configuration: dict = None, config_path = None, python_version: str = None,
               prompt_mode: PromptMode = PromptMode.INTERACTIVE, naming: str = None,
               proxy_id: str = None, proxy_host_config_key: str = None, target_package_id: str = None):
        """Deploys the connector to the Fivetran platform.

        Args:
            project_path (str): The path to the project.
            deploy_key (str): The deployment key.
            group (str): The group name.
            connection (str): The connection name.
            hd_agent_id (str): The hybrid deployment agent ID within the Fivetran system.
            configuration (dict): The configuration dictionary.
            config_path (str): The path to the configuration file.
            python_version (str): The Python version to use.
            prompt_mode (PromptMode): Controls how prompts are answered. Defaults to INTERACTIVE.
            naming (str): The formatted naming strategy (e.g., "FIVETRAN_NAMING" or "SOURCE_NAMING").
            proxy_id (str): Proxy Agent ID used for proxy routing.
            proxy_host_config_key (str): Configuration key that contains the proxied host details.
            target_package_id (str): Existing package ID for creating or rebinding the connection, skipping local packaging and upload.
        """
        _deploy_connector(project_path, deploy_key, group, connection, hd_agent_id, DeployOptions(
            configuration=configuration, config_path=config_path, python_version=python_version,
            prompt_mode=prompt_mode, naming=naming, proxy_id=proxy_id, proxy_host_config_key=proxy_host_config_key,
            target_package_id=target_package_id), configuration_form_method=self.configuration_form_method)

    def debug(self,
              project_path: str = None,
              configuration: dict = None,
              state: dict = None,
              naming: str = None,
              log_level: Logging.Level = Logging.Level.DEBUG,
              state_path: str = None):
        """Tests the connector code by running it in this process, writing what it emits to files/warehouse.db.\n
        state.json docs: https://fivetran.com/docs/connector-sdk/connector-sdk-concepts/state-management#statemanagement\n
        configuration.json docs: https://fivetran.com/docs/connector-sdk/connector-development-and-configuration/configuration-json#workingwithconfigurationjson

        Args:
            project_path (str): The path to the project.
            configuration (dict): The configuration dictionary, same as configuration.json if present.
            state (dict): The state dictionary, same as state.json if present.
            log_level (Logging.Level): The logging level.
            naming (str): The formatted naming strategy (e.g., "FIVETRAN_NAMING" or "SOURCE_NAMING").
            state_path (str): The file the state was read from, which the checkpoints update; files/state.json if None.
        """
        self._run_locally("debugging", project_path, configuration, state, naming, log_level, None, state_path)

    def run(self,
            destination: dict,
            project_path: str = None,
            configuration: dict = None,
            state: dict = None,
            naming: str = None,
            log_level: Logging.Level = Logging.Level.DEBUG,
            state_path: str = None):
        """Runs the connector in this process like `debug`, but writes what it emits to the Iceberg catalog `destination` describes.

        Args:
            destination (dict): The content of destination.json.
            project_path (str): The path to the project.
            configuration (dict): The configuration dictionary, same as configuration.json if present.
            state (dict): The state dictionary, same as state.json if present.
            naming (str): The formatted naming strategy (e.g., "FIVETRAN_NAMING" or "SOURCE_NAMING").
            log_level (Logging.Level): The logging level.
            state_path (str): The file the state was read from, which the checkpoints update; files/state.json if None.
        """
        if not isinstance(destination, dict):  # None would be taken by the core for the local file: the run would write nothing to Iceberg
            raise ValueError("destination must be the content of destination.json, a JSON object")
        self._run_locally("running", project_path, configuration, state, naming, log_level, destination, state_path)

    def _run_locally(self, verb, project_path, configuration, state, naming, log_level, destination, state_path):
        constants.DEBUGGING = True
        validate_configuration(configuration)

        check_newer_version(__version__)

        Logging.LOG_LEVEL = log_level

        project_path = os.getcwd() if project_path is None else project_path
        project_path = _resolve_existing_project_path(project_path)
        self.project_path = project_path
        pyproject_path = os.path.join(project_path, PYPROJECT_TOML)
        if os.path.exists(pyproject_path):
            validate_pyproject_file(project_path, False)
        else:
            validate_requirements_file(project_path, False, __version__)
        print_library_log(f"{verb} connector at: {project_path}", log_icon=Logging.LogIcon.STEP)
        self._register_debug_crash_report_at_exit()
        try:
            faulthandler.enable()
        except (RuntimeError, OSError):
            pass

        exit_check(project_path)

        self.configuration = check_dict(configuration, True)
        self.state = check_dict(state)

        print_library_log("running the connector", log_icon=Logging.LogIcon.STEP)
        try:
            core_adapter.run(self, project_path, self.configuration, self.state, apply_renaming=naming != "SOURCE_NAMING",
                             destination=destination, state_path=state_path)
        except (Exception, ConnectorTask):
            sys.exit(1)

    def generate_configuration(self, project_path: str, run_tests: bool = False, disable_encryption: bool = False,
                               prompt_mode: PromptMode = PromptMode.INTERACTIVE):
        """Collects the connector's configuration from its setup form, or runs the form's setup tests.

        The form is asked for each field in turn and the answers, with password fields encrypted, are saved to
        configuration.json. With run_tests=True the setup tests registered on the form run against the saved
        configuration instead.

        Args:
            project_path: Path to the connector project directory.
            run_tests: If True, run setup tests instead of collecting configuration.
            disable_encryption: If True, skip encryption of sensitive fields. Defaults to False.
            prompt_mode: Controls how the override confirmation is answered. Defaults to INTERACTIVE.
        """
        project_path = os.getcwd() if project_path is None else project_path
        self.project_path = project_path
        self._register_debug_crash_report_at_exit()

        self._validate_and_cache_form(run_tests)
        check_newer_version(__version__)

        if not run_tests:
            self._confirm_configuration_override(project_path, prompt_mode)

        config_path = os.path.join(project_path, constants.CONFIGURATION_JSON)
        print_library_log("Fetching configuration form")
        form = self.get_configuration_form()
        try:
            if run_tests:
                code = configuration_command.run_configuration_tests(self, form, config_path)
            else:
                code = configuration_command.run_configuration_form(form, config_path, disable_encryption)
        except (configuration_command.ConfigurationError, _ConnectorFailure):
            raise  # the form or the file is wrong (its message says what to fix, a traceback would not), or a handler failed, and its message holds the traceback
        except Exception as e:  # nothing has said what happened yet
            print(traceback.format_exc())
            raise e
        if code != 0:
            sys.exit(code)

    def _validate_and_cache_form(self, run_tests: bool):
        if self.configuration_form_method is None:
            print_library_log(constants.CONFIGURATION_FORM_MISSING, Logging.Level.SEVERE)
            sys.exit(1)

        constants.DEBUGGING = True
        Logging.LOG_LEVEL = Logging.Level.INFO
        try:
            self._cached_form = self.configuration_form_method()
        except Exception as e:
            self._set_debug_crash_report(e, "configuration_form()")
            raise

        if run_tests and not self._cached_form._tests:
            print_library_log(constants.CONFIGURATION_TESTS_MISSING, Logging.Level.SEVERE)
            sys.exit(1)

    def _confirm_configuration_override(self, project_path: str, prompt_mode: PromptMode = PromptMode.INTERACTIVE):
        config_path = os.path.join(project_path, constants.CONFIGURATION_JSON)
        if os.path.exists(config_path):
            prompt = (
                f"'{constants.CONFIGURATION_JSON}' already exists in '{project_path}'\n"
                f"running this command will override it\n"
                f"continue? (y/N): "
            )
            if not resolve_confirmation(prompt, default=False, prompt_mode=prompt_mode):
                print_library_log(f"'{constants.CONFIGURATION_JSON}' already exists; creating new file and overriding values cancelled")
                sys.exit(0)

    def _register_debug_crash_report_at_exit(self):
        # Registered at exit so the report prints after the runner's failure summary.
        atexit.register(self._print_debug_crash_report)

    def _print_debug_crash_report(self):
        if not self._debug_crash_report:
            return
        try:
            crash_report_path = save_crash_report(self._debug_crash_report, self.project_path)
            print(Logging.colorize(f"crash report saved to {crash_report_path}", Logging.Level.SEVERE))
        except Exception as save_error:
            print_library_log(f"failed to save crash report: {save_error}", Logging.Level.WARNING)
            print(Logging.colorize(self._debug_crash_report, Logging.Level.SEVERE))
        self._debug_crash_report = None
        atexit.unregister(self._print_debug_crash_report)

    def _set_debug_crash_report(self, exception, handler, state=None, memory_tracker=None):
        if not constants.DEBUGGING:
            return

        try:
            self._debug_crash_report = build_debug_crash_report(
                exception,
                self.project_path,
                configuration=self.configuration,
                handler=handler,
                sdk_version=__version__,
                state=state,
                memory_tracker=memory_tracker,
            )
        except Exception as report_error:
            # Crash reports are best-effort diagnostics and must not replace the customer exception.
            print_library_log(f"failed to build crash report: {report_error}. Please contact support: https://support.fivetran.com/", Logging.Level.WARNING)

    # -- What the runner calls; each is the counterpart of the production servicer method of the same job.
    def get_configuration_form(self, configuration: dict = None):
        """The setup form, or `None` if the connector has no `configuration_form()`."""
        if self.configuration_form_method is None:
            return None

        try:
            if Logging.LOG_LEVEL is None:
                Logging.LOG_LEVEL = Logging.Level.INFO
            print_library_log("calling configuration_form()", Logging.Level.INFO)
            form = self._get_configuration_form()
            return form.to_response()
        except Exception as e:
            self._set_debug_crash_report(e, "configuration_form()")
            error_message = f"failed while executing configuration_form() error: {str(e)}"
            raise _failure(error_message, e) from e

    def run_test(self, name: str, configuration: dict = None) -> TestResponse:
        """Runs the setup test registered under `name`, as the platform does through `Test`."""
        if self.configuration_form_method is None:
            return TestResponse(success=True)

        try:
            if Logging.LOG_LEVEL is None:
                Logging.LOG_LEVEL = Logging.Level.INFO
            form = self._get_configuration_form()
            test_fn = form._get_test_function_by_name(name)
            if test_fn is None:
                raise RuntimeError(f"no test registered with name '{name}'")
            configuration = self.configuration if self.configuration else dict(configuration or {})
            print_library_log(f"calling test '{name}'", Logging.Level.INFO)
            result = test_fn(configuration)
            if not isinstance(result, TestResponse):
                return TestResponse(
                    failure=f"test '{name}' must return Test.success() or Test.failure(...), got {type(result).__name__}"
                )
            return result
        except Exception as e:
            self._set_debug_crash_report(e, "test()")
            error_message = f"failed while executing test '{name}' error: {str(e)}"
            raise _failure(error_message, e) from e

    def _get_configuration_form(self):
        if self._cached_form is None:
            self._cached_form = self.configuration_form_method()
        return self._cached_form

    def get_schema(self, configuration: dict = None) -> SchemaResponse:
        """The tables the connector declares through `schema()`."""
        table_list = {}

        if not self.schema_method:
            return SchemaResponse(not_supported=True)
        else:
            try:
                configuration = self.configuration if self.configuration else dict(configuration or {})
                print_library_log("calling schema()", Logging.Level.INFO)
                response = self.schema_method(configuration)
                process_tables(response, table_list)
                return SchemaResponse(tables=list(schema_processing.TABLES.values()))

            except Exception as e:
                self._set_debug_crash_report(e, "schema()")
                error_message = f"failed while executing schema() error: {str(e)}"
                raise _failure(error_message, e) from e

    def run_update(self, configuration: dict = None, state: dict = None):
        """Runs the connector's `update()` in the calling thread, emitting through the installed runtime."""
        configuration = self.configuration if self.configuration else dict(configuration or {})
        state = self.state if self.state else dict(state or {})
        memory_tracker = None

        try:
            memory_tracker = DebugMemoryTracker()
            memory_tracker.start()

            print_library_log("calling update()", Logging.Level.INFO)

            try:
                result = self.update_method(configuration=configuration, state=state)
                # If the customer's update method returns a generator (i.e., uses yield), run it to the end;
                # what it yields is None. Operations reach the runner as they are called.
                if isinstance(result, GeneratorType):
                    for _ in result:
                        pass
            finally:
                memory_tracker.stop()

            print_library_log("finished receiving records from customer's update().", Logging.Level.INFO, True)

        except Exception as e:
            self._set_debug_crash_report(e, "update()", state=state, memory_tracker=memory_tracker)
            error_message = f"failed while executing update() error: {str(e)}"
            raise _failure(error_message, e) from e
