import os
os.environ["GRPC_VERBOSITY"] = "ERROR"
import sys
import grpc
import json
import atexit
import time
import traceback
import faulthandler
import threading
import queue
import subprocess
from collections import defaultdict
from types import GeneratorType
from concurrent import futures

from fivetran_connector_sdk_common.crash_report import build_debug_crash_report, save_crash_report
from fivetran_connector_sdk.protos import common_pb2
from fivetran_connector_sdk.protos import connector_sdk_pb2
from fivetran_connector_sdk.protos import connector_sdk_pb2_grpc

from fivetran_connector_sdk_common.logger import Logging
from fivetran_connector_sdk.file_upload import ByteStream, FileUpload
from fivetran_connector_sdk.operations import Operations
from fivetran_connector_sdk.configuration_form import ConfigurationForm
from fivetran_connector_sdk.test import Test
from fivetran_connector_sdk import form_field
from fivetran_connector_sdk_common import __version__, constants as common_constants
from fivetran_connector_sdk_common.memory_tracker import get_memory_tracker
from fivetran_connector_sdk_common.constants import TABLES, PYPROJECT_TOML
from fivetran_connector_sdk.constants import (
    CAPTURE_PERFORMANCE_METRICS_ENABLED,
    SDK_BUILD_NS, QUEUE_WAIT_NS, SDK_ASSEMBLY_NS, QUEUE_BACKPRESSURE_NS, CHECKPOINT_WAIT_NS,
    GRPC_FIRST_SEND_MS, GRPC_SEND_RELATIVE_TOTAL_MS, GRPC_SEND_COUNT, GRPC_TIMESTAMP_OVERFLOW,
    PRODUCER_WALL_NS
)
from fivetran_connector_sdk_common.helpers import print_library_log, PromptMode, _resolve_existing_project_path
from fivetran_connector_sdk.schema_processing import process_tables
from fivetran_connector_sdk_common.cli_commands import main, _deploy_connector
from fivetran_connector_sdk_common.connector_helper import (
    validate_requirements_file, validate_pyproject_file, run_tester, run_configuration_tester,
    ensure_tester_installed, update_base_url_if_required, exit_check, get_available_port, check_dict,
    check_newer_version, validate_configuration, DeployOptions
)

MAX_MESSAGE_LENGTH = 128 * 1024 * 1024 # 128MB

__all__ = [cls.__name__ for cls in [ByteStream, FileUpload, Logging, Operations, ConfigurationForm, Test]] + ["form_field"]

def _format_runtime_error_message(error_message):
    # The stacktrace is appended to the RuntimeError message so it is shown to the developer
    # (locally) and surfaced by the java client in the user task (when running in production).
    return f"{error_message}\n{traceback.format_exc()}"

def _build_schema_response():
    """Builds the SchemaResponse from TABLES (keyed by (schema, table), see constants.TABLES).

    Branches on common_constants.SCHEMA_QUALIFIED (whether any schema() entry declared an explicit 'schema'): an
    entirely unqualified schema() produces without_schema, byte-identical to before multiple-schema support.
    Otherwise the response is with_schema, and entries without a 'schema' (which belong to the connection's own
    schema) are sent as the schema with an empty name. An empty name can never be a declared schema, so it can't
    be confused with a schema that happens to be named like the connection.
    """
    if not common_constants.SCHEMA_QUALIFIED:
        return connector_sdk_pb2.SchemaResponse(without_schema=common_pb2.TableList(tables=TABLES.values()))

    tables_by_schema = defaultdict(list)
    for (schema, _table_name), table in TABLES.items():
        tables_by_schema[schema].append(table)
    schemas = [common_pb2.Schema(name=schema or "", tables=tables) for schema, tables in tables_by_schema.items()]
    return connector_sdk_pb2.SchemaResponse(with_schema=common_pb2.SchemaList(schemas=schemas))

class Connector(connector_sdk_pb2_grpc.SourceConnectorServicer):
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

        if not common_constants.EXECUTED_VIA_CLI:
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

    # Call this method to run the connector in production
    def run(self,
            port: int = 50049,
            configuration: dict = None,
            state: dict = None,
            log_level: Logging.Level = Logging.Level.INFO) -> grpc.Server:
        """Runs the connector server.

        Args:
            port (int): The port number to listen for incoming requests.
            configuration (dict): The configuration dictionary.
            state (dict): The state dictionary.
            log_level (Logging.Level): The logging level.

        Returns:
            grpc.Server: The gRPC server instance.
        """
        self.configuration = check_dict(configuration, True)
        self.state = check_dict(state)
        Logging.LOG_LEVEL = log_level

        if not common_constants.DEBUGGING:
            """
                DO NOT MODIFY THE LOG MESSAGE BELOW
                This is used to identify the readiness of the connector to run the code.
                Any changes may break integration or automated workflows.
                This is referenced at https://github.com/fivetran/engineering/blob/main/connector_sdk/core/src/com/fivetran/connector_sdk/core/ConnectorSdkUtils.java#L73
            """
            print_library_log(f"Running on fivetran_connector_sdk: {__version__}")

        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10),
            options=[
                ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
            ]
        )
        connector_sdk_pb2_grpc.add_SourceConnectorServicer_to_server(self, server)
        bind_address = "127.0.0.1" if common_constants.DEBUGGING else "[::]"
        server.add_insecure_port(bind_address + ":" + str(port))
        server.start()
        if common_constants.DEBUGGING:
            return server
        server.wait_for_termination()

    # This method starts both the server and the local testing environment
    def debug(self,
              project_path: str = None,
              configuration: dict = None,
              state: dict = None,
              naming: str = None,
              log_level: Logging.Level = Logging.Level.DEBUG):
        """Tests the connector code by running it with the connector tester.\n
        state.json docs: https://fivetran.com/docs/connector-sdk/connector-sdk-concepts/state-management#statemanagement\n
        configuration.json docs: https://fivetran.com/docs/connector-sdk/connector-development-and-configuration/configuration-json#workingwithconfigurationjson

        Args:
            project_path (str): The path to the project.
            configuration (dict): The configuration dictionary, same as configuration.json if present.
            state (dict): The state dictionary, same as state.json if present.
            log_level (Logging.Level): The logging level.
            naming (str): The formatted naming strategy (e.g., "FIVETRAN_NAMING" or "SOURCE_NAMING").
        """
        common_constants.DEBUGGING = True
        validate_configuration(configuration)

        check_newer_version(__version__)

        Logging.LOG_LEVEL = log_level
        java_exe, tester_root_dir = ensure_tester_installed()

        project_path = os.getcwd() if project_path is None else project_path
        project_path = _resolve_existing_project_path(project_path)
        self.project_path = project_path
        pyproject_path = os.path.join(project_path, PYPROJECT_TOML)
        if os.path.exists(pyproject_path):
            validate_pyproject_file(project_path, False)
        else:
            validate_requirements_file(project_path, False, __version__)
        print_library_log(f"debugging connector at: {project_path}", log_icon=Logging.LogIcon.STEP)
        self._register_debug_crash_report_at_exit()
        try:
            faulthandler.enable()
        except (RuntimeError, OSError):
            pass
        
        available_port = get_available_port()
        exit_check(project_path)

        if available_port is None:
            raise RuntimeError("failed to allocate port error: no available port in range 50049-50060")

        server = self.run(available_port, configuration, state, log_level=log_level)

        # Uncomment this to run the tester manually
        # server.wait_for_termination()

        try:
            print_library_log("starting connector tester", log_icon=Logging.LogIcon.STEP)
            for log_msg in run_tester(
                java_exe, tester_root_dir, project_path, available_port,
                json.dumps(self.state), self.configuration, naming):
                print(log_msg, end="")
        finally:
            server.stop(grace=2.0)

    def _validate_and_cache_form(self, run_tests: bool):
        if self.configuration_form_method is None:
            print_library_log(
                "Your connector does not implement the configuration_form() method. Please implement it and re-run."
                "\nFor more information, see https://fivetran.com/docs/connector-sdk/technical-reference/connector-sdk-setup-form",
                Logging.Level.SEVERE
            )
            sys.exit(1)

        common_constants.DEBUGGING = True
        Logging.LOG_LEVEL = Logging.Level.INFO
        try:
            self._cached_form = self.configuration_form_method()
        except Exception as e:
            self._set_debug_crash_report(e, "configuration_form()")
            raise

        if run_tests and not self._cached_form._tests:
            print_library_log(
                "Your connector does not provide any configuration tests to run.",
                Logging.Level.SEVERE
            )
            sys.exit(1)

    def _confirm_configuration_override(self, project_path: str):
        config_path = os.path.join(project_path, common_constants.CONFIGURATION_JSON)
        if os.path.exists(config_path):
            confirm = input(
                f"'{common_constants.CONFIGURATION_JSON}' already exists in '{project_path}'\n"
                f"running this command will override it\n"
                f"continue? (y/N): "
            )
            if confirm.lower() != "y":
                print_library_log(f"'{common_constants.CONFIGURATION_JSON}' already exists; creating new file and overriding values cancelled")
                sys.exit(0)

    def generate_configuration(self, project_path: str, run_tests: bool = False, disable_encryption: bool = False):
        """Runs the fivetran configuration command via the connector tester.

        Starts the gRPC server and invokes the Java tester in configuration mode.
        The tester calls ConfigurationForm to get fields, prompts the user interactively,
        and saves configuration.json. With run_tests=True, it calls Test for each registered
        test and displays results.

        Args:
            project_path: Path to the connector project directory.
            run_tests: If True, run setup tests instead of collecting configuration.
            disable_encryption: If True, skip encryption of sensitive fields. Defaults to False.
        """
        project_path = os.getcwd() if project_path is None else project_path
        self.project_path = project_path
        self._register_debug_crash_report_at_exit()

        self._validate_and_cache_form(run_tests)
        check_newer_version(__version__)

        if not run_tests:
            self._confirm_configuration_override(project_path)

        java_exe, tester_root_dir = ensure_tester_installed()

        available_port = get_available_port()
        if available_port is None:
            raise RuntimeError("failed to allocate port error: no available port in range 50049-50060")

        server = self.run(available_port, {}, log_level=Logging.Level.INFO)
        try:
            print_library_log("starting connector tester", log_icon=Logging.LogIcon.STEP)
            run_configuration_tester(java_exe, tester_root_dir, project_path, available_port, run_tests, disable_encryption)
        except subprocess.CalledProcessError:
            raise
        except Exception as e:
            print(traceback.format_exc())
            raise e
        finally:
            server.stop(grace=2.0)

    def _register_debug_crash_report_at_exit(self):
        # Registered at exit so the report prints after the java tester's failure
        # summary, which is emitted when the tester subprocess is torn down.
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
        if not common_constants.DEBUGGING:
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

    # -- Methods below override ConnectorServicer methods
    def ConfigurationForm(self, request, context):
        """Overrides the ConfigurationForm method from ConnectorServicer.

        Args:
            request: The gRPC request.
            context: The gRPC context.

        Returns:
            common_pb2.ConfigurationFormResponse: The configuration form response.
        """
        if self.configuration_form_method is None:
            return common_pb2.ConfigurationFormResponse()

        try:
            if Logging.LOG_LEVEL is None:
                Logging.LOG_LEVEL = Logging.Level.INFO
            print_library_log("calling configuration_form()", Logging.Level.INFO)
            form = self._get_configuration_form()
            return form._to_proto()
        except Exception as e:
            self._set_debug_crash_report(e, "configuration_form()")
            error_message = f"failed while executing configuration_form() error: {str(e)}"
            print_library_log(error_message, Logging.Level.SEVERE)
            raise RuntimeError(_format_runtime_error_message(error_message)) from e

    def Test(self, request, context):
        """Overrides the Test method from ConnectorServicer.

        Dispatches to the test function registered in ConfigurationForm whose __name__
        matches request.name.

        Args:
            request: The gRPC request containing name and configuration.
            context: The gRPC context.

        Returns:
            common_pb2.TestResponse: The test result.
        """
        if self.configuration_form_method is None:
            return common_pb2.TestResponse(success=True)

        try:
            if Logging.LOG_LEVEL is None:
                Logging.LOG_LEVEL = Logging.Level.INFO
            form = self._get_configuration_form()
            test_fn = form._get_test_function_by_name(request.name)
            if test_fn is None:
                raise RuntimeError(f"no test registered with name '{request.name}'")
            configuration = self.configuration if self.configuration else dict(request.configuration)
            print_library_log(f"calling test '{request.name}'", Logging.Level.INFO)
            result = test_fn(configuration)
            if not isinstance(result, common_pb2.TestResponse):
                return common_pb2.TestResponse(
                    failure=f"test '{request.name}' must return Test.success() or Test.failure(...), got {type(result).__name__}"
                )
            return result
        except Exception as e:
            self._set_debug_crash_report(e, "test()")
            error_message = f"failed while executing test '{request.name}' error: {str(e)}"
            print_library_log(error_message, Logging.Level.SEVERE)
            raise RuntimeError(_format_runtime_error_message(error_message)) from e

    def _get_configuration_form(self):
        if self._cached_form is None:
            self._cached_form = self.configuration_form_method()
        return self._cached_form

    def Schema(self, request, context):
        """Overrides the Schema method from ConnectorServicer.

        Args:
            request: The gRPC request.
            context: The gRPC context.

        Returns:
            connector_sdk_pb2.SchemaResponse: The schema response.
        """

        table_list = {}

        if not self.schema_method:
            return connector_sdk_pb2.SchemaResponse(schema_response_not_supported=True)
        else:
            try:
                configuration = self.configuration if self.configuration else dict(request.configuration)
                print_library_log("calling schema()", Logging.Level.INFO)
                response = self.schema_method(configuration)
                process_tables(response, table_list)
                return _build_schema_response()

            except Exception as e:
                self._set_debug_crash_report(e, "schema()")
                error_message = f"failed while executing schema() error: {str(e)}"
                print_library_log(error_message, Logging.Level.SEVERE)
                raise RuntimeError(_format_runtime_error_message(error_message)) from e

    def Update(self, request, context):
        """Overrides the Update method from ConnectorServicer.

        Args:
            request: The gRPC request.
            context: The gRPC context.

        Yields:
            connector_sdk_pb2.UpdateResponse: The update response.
        """
        configuration = self.configuration if self.configuration else dict(request.configuration)
        state = self.state if self.state else json.loads(request.state_json)
        exception_queue = queue.Queue()
        memory_tracker = None

        try:
            # Create memory tracker for both debug and sync modes
            memory_tracker = get_memory_tracker()
            memory_tracker.start()

            print_library_log("calling update()", Logging.Level.INFO)

            def run_update():
                t_producer_start = time.perf_counter_ns() if CAPTURE_PERFORMANCE_METRICS_ENABLED else None
                try:
                    result = self.update_method(configuration=configuration, state=state)
                    # If the customer's update method returns a generator (i.e., uses yield),
                    # exhaust the generator responses, they are None. From this point on, all operations
                    # push update_response to a queue, and we yield from the queue instead.
                    # We return None here intentionally.
                    if isinstance(result, GeneratorType):
                        for _ in result:
                            pass
                    # If the update method doesn't use yield, skip the response returned.
                    else:
                        pass
                except Exception as exc:
                    exception_queue.put(exc)
                finally:
                    if t_producer_start is not None:
                        Operations.operation_stream._producer_wall_ns = time.perf_counter_ns() - t_producer_start
                    Operations.operation_stream.mark_done()

            thread = None
            try:
                thread = threading.Thread(target=run_update)
                thread.start()

                # consumer - yield the operations in the operation_stream.
                for response in Operations.operation_stream:
                    # checkpoint and file-upload-chunk flushes both return a list of responses.
                    if isinstance(response, list):
                        for res in response:
                            Operations.operation_stream.record_grpc_send_timestamp()
                            yield res
                        # add_checkpoint blocks the producer until its checkpoint response is yielded.
                        # File-upload flushes also return lists, but they do not block the producer, so
                        # unblock only when this batch contains a checkpoint.
                        if any(res.WhichOneof("operation") == "checkpoint" for res in response):
                            Operations.operation_stream.unblock()
                    else:
                        Operations.operation_stream.record_grpc_send_timestamp()
                        yield response
            finally:
                memory_tracker.stop()
                if thread is not None:
                    thread.join()

            # Check if any exception was raised during the update
            if not exception_queue.empty():
                raise exception_queue.get()

            print_library_log("finished receiving records from customer's update().", Logging.Level.INFO, True)

        except Exception as e:
            self._set_debug_crash_report(e, "update()", state=state, memory_tracker=memory_tracker)
            error_message = f"failed while executing update() error: {str(e)}"
            print_library_log(error_message, Logging.Level.SEVERE)
            raise RuntimeError(_format_runtime_error_message(error_message)) from e
        finally:
            # Send per-sync timing breakdown as gRPC trailing metadata, only when perf-metric capture is enabled.
            if CAPTURE_PERFORMANCE_METRICS_ENABLED:
                context.set_trailing_metadata([
                    (SDK_BUILD_NS, str(Operations.operation_stream._sdk_build_ns)),
                    (QUEUE_WAIT_NS, str(Operations.operation_stream._queue_wait_ns)),
                    (SDK_ASSEMBLY_NS, str(Operations.operation_stream._sdk_batch_assembly_ns)),
                    (QUEUE_BACKPRESSURE_NS, str(Operations.operation_stream._queue_backpressure_ns)),
                    (CHECKPOINT_WAIT_NS, str(Operations.operation_stream._checkpoint_wait_ns)),
                    (GRPC_FIRST_SEND_MS, str(Operations.operation_stream._grpc_first_send_ms)),
                    (GRPC_SEND_RELATIVE_TOTAL_MS, str(Operations.operation_stream._grpc_send_relative_total_ms)),
                    (GRPC_SEND_COUNT, str(Operations.operation_stream._grpc_send_count)),
                    (GRPC_TIMESTAMP_OVERFLOW, str(Operations.operation_stream._grpc_timestamp_overflow).lower()),
                    (PRODUCER_WALL_NS, str(Operations.operation_stream._producer_wall_ns)),
                ])



if __name__ == "__main__":
    main()
