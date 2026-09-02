import ast
import base64
import json

from ipykernel.ipkernel import IPythonKernel
from IPython.display import publish_display_data
import re

from importlib_metadata import version
import os
import sys
import uuid
import requests
import subprocess


from aws_glue_interactive_sessions_kernel.glue_kernel_configs.AWSFileConfigRetriever import AWSFileConfigRetriever
from aws_glue_interactive_sessions_kernel.glue_kernel_configs.DefaultConfigRetriever import DefaultConfigRetriever
from aws_glue_interactive_sessions_kernel.glue_kernel_configs.GlueConfigManager import GlueConfigManager
from aws_glue_interactive_sessions_kernel.glue_kernel_configs.OverriddenConfigRetriever import OverriddenConfigRetriever
from aws_glue_interactive_sessions_kernel.glue_kernel_configs.SystemEnvConfigRetriever import SystemEnvConfigRetriever
from aws_glue_interactive_sessions_kernel.glue_kernel_configs.config import Config, default_configs

try:
    from asyncio import Future
except ImportError:

    class Future(object):
        """A class nothing will use."""

import time
import traceback
from collections import defaultdict

import botocore

from ..glue_kernel_utils.GlueSessionsConstants import *
from IPython import get_ipython
from ..glue_kernel_utils.KernelGateway import KernelGateway
from ..glue_kernel_utils.KernelMagics import KernelMagics
from collections import OrderedDict


class BaseKernel(IPythonKernel):
    time_out = float("inf")
    session_id = None
    new_session_id = None
    session_id_prefix = None
    request_origin = None

    def __init__(self, **kwargs):
        super(BaseKernel, self).__init__(**kwargs)
        self.execution_counter = 1
        self._set_default_arguments()
        self.session_name = "AssumeRoleSession"
        self.should_print_startup_text = True
        self.kernel_gateway = KernelGateway()
        self._register_magics()
        self._setup_terminal_logging()

        # Setup environment variables
        os_env_request_origin = self._retrieve_os_env_variable(REQUEST_ORIGIN)
        if os_env_request_origin:
            self.set_request_origin(os_env_request_origin)
        self.overrides = Config()
        self.retrievers = self._initialize_retrievers(self.overrides)
        self.config_manager = GlueConfigManager(self.retrievers)
        # Once the initialization is complete, check if there is a sessionId to be used.
        os_env_session_id = self._retrieve_os_env_variable(SESSION_ID)
        if os_env_session_id:
            self.set_new_session_id(os_env_session_id)

    def _set_default_arguments(self):
        self.default_arguments = {
            "--glue_kernel_version": self._get_current_kernel_version("aws-glue-sessions"),
            "--enable-glue-datacatalog": "true",
        }

    def display_result(self, statement_output):
        if 'Data' in statement_output:
            statement_output_data = statement_output['Data']

            # The default case would be a text/plain response, but an image result may also be accompanied by a text output.
            if MimeTypes.TextPlain.name in statement_output_data and len(statement_output_data) == 1:
                # The value for dictionary key in the result is: text/plain
                self._send_output(statement_output_data[MimeTypes.TextPlain.name])
            elif 'MimeType' in statement_output_data:
                result = statement_output_data['Result']
                mime_type = statement_output_data['MimeType']
                stdout_text = None
                stderr_text = None

                # Unpack the inline vs. indirect std streams
                if mime_type == MimeTypes.S3URI.value:
                    stdout_text = self.kernel_gateway.get_results(statement_output_data['StdOut']) if 'StdOut' in statement_output_data else ""
                    stderr_text = self.kernel_gateway.get_results(statement_output_data['StdErr']) if 'StdErr' in statement_output_data else ""
                else:
                    stdout_text = statement_output_data['StdOut'] if 'StdOut' in statement_output_data else ""
                    stderr_text = statement_output_data['StdErr'] if 'StdErr' in statement_output_data else ""

                if mime_type == MimeTypes.S3URI.value:
                    response = self.kernel_gateway.get_results(statement_output_data['Result'])
                    result = json.loads(response)
                    if len(result) == 0:
                        # Semantically this case corresponds to the 'stream' result,
                        # which is is meant to be "send_output'd" and actually
                        # arrives on stdout which is headed there anyway.
                        result = None
                        mime_type = None
                    elif result.get(MimeTypes.ImagePng.value):
                        result = result.get(MimeTypes.ImagePng.value)
                        mime_type = MimeTypes.ImagePng.value
                    elif result.get(MimeTypes.TextPlain.value):
                        result = result.get(MimeTypes.TextPlain.value)
                        mime_type = MimeTypes.TextPlain.value

                if mime_type and ';' in mime_type:
                    mime_type_list = mime_type.replace(' ','').split(';')
                    if 'base64' in mime_type_list:
                        result = base64.b64decode(str(result))
                        mime_type_list.remove('base64')
                        mime_type = ';'.join(mime_type_list)

                # Dispatch of results for display
                if stdout_text:
                    self._send_output(stdout_text)
                if stderr_text:
                    self._send_error_output(stderr_text)

                if result and mime_type:
                    display_data = {
                        mime_type: result
                    }
                    publish_display_data(data=display_data, metadata={mime_type: {"width": 640, "height": 480}})

    async def do_execute(
            self, code: str, silent: bool, store_history=True, user_expressions=None, allow_stdin=False
    ):
        # VSCode silently executes few statements that are not giving customers opportunity to configure their session.
        # All those statements have store_history flag set to False.
        # Ignoring those statements when a session is not yet created allowing customers to configure their session.
        if not store_history and (
            not self.get_session_id()
                or self.get_current_session_status() in UNHEALTHY_SESSION_STATUS):
            return await self._complete_cell()
        # Print help text upon startup
        if self.should_print_startup_text:
            await self._print_startup_text()
        code = await self._execute_magics(
            code, silent, store_history, user_expressions, allow_stdin
        )
        statement_id = None

        if not code:
            return await self._complete_cell()

        try:
            if (
                    not self.get_session_id()
                    or self.get_current_session_status() in UNHEALTHY_SESSION_STATUS
            ):
                self.kernel_gateway.initialize_clients(profile=self.get_profile(),
                                                       region=self.get_region(), endpoint_url=self.get_endpoint_url(),
                                                       temp_credentials=self.get_temp_credentials())
                self.create_session()
                if self.get_current_session_status() in UNHEALTHY_SESSION_STATUS:
                    self._send_error_output(f'Current session is in an unhealthy terminal state. If you wish to create a new session use %stop_session before executing any further statements.')
                    return await self._complete_cell()
        except Exception as e:
                sys.stderr.write(f"Exception encountered while creating session: {e} \n")
                self._print_traceback(e)
                return await self._complete_cell()

        try:
            # Run statement
            statement_id = self.kernel_gateway.run_statement(
                self.get_session_id(), code
            )["Id"]
            start_time = time.time()

            try:
                while time.time() - start_time <= self.time_out:
                    statement = self.kernel_gateway.get_statement(self.get_session_id(), statement_id)["Statement"]
                    if statement["State"] in FINAL_STATEMENT_STATUS:
                        return self._construct_reply_content(statement)

                    time.sleep(WAIT_TIME)

                sys.stderr.write(f"Timeout occurred with statement (statement_id={statement_id})")

            except KeyboardInterrupt:
                self._send_output(
                    f"Execution Interrupted. Attempting to cancel the statement (statement_id={statement_id})"
                )
                self.kernel_gateway.cancel_statement(self.get_session_id(), statement_id)
        except botocore.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']

            if error_code in 'InvalidInputException':
                if self.get_current_session_status() == TIMEOUT_SESSION_STATUS:
                    self._send_error_output(
                        f"session_id={self.get_session_id()} has reached {self.get_current_session_status()} status. ")
                    self._send_error_output(
                        f"Please re-run the same cell to restart the session. You may also need to re-run "
                        f"previous cells if trying to use pre-defined variables.")
                    self.reset_kernel()
                return await self._complete_cell()

            else:
                self._send_error_output(error_message)
                self._cancel_statement(statement_id)
                return await self._complete_cell()

        except Exception as e:
            sys.stderr.write(f"Exception encountered while running statement: {e} \n")
            self._print_traceback(e)
            self.kernel_gateway.cancel_statement(self.get_session_id(), statement_id)
            return await self._complete_cell()

    def set_temporary_credentials(self, aws_access_key_id, aws_secret_access_key, aws_session_token):
        temp_credentials = defaultdict()
        temp_credentials['temp_aws_access_key_id'] = aws_access_key_id
        temp_credentials['temp_aws_secret_access_key'] = aws_secret_access_key
        temp_credentials['temp_aws_session_token'] = aws_session_token
        setattr(self.overrides, TEMP_CREDENTIALS, temp_credentials)

    def get_temp_credentials(self):
        return self.config_manager.get_config_by_priority(TEMP_CREDENTIALS)

    def configure(self, configs_json):
        kernel_managed_params = {
            "profile",
            "endpoint",
            "region",
            "iam_role",
            "session_id",
            "max_capacity",
            "number_of_workers",
            "worker_type",
            "connections",
            "glue_version",
            "security_config",
            "idle_timeout",
            "tags",
            "timeout"
        }
        try:
            configs = ast.literal_eval(configs_json)
            if "profile" in configs:
                self.set_profile(configs.get("profile"))
            if "endpoint" in configs:
                self.set_endpoint_url(configs.get("endpoint"))
            if "region" in configs:
                self.set_region(configs.get("region"))
            if "iam_role" in configs:
                self.set_glue_role_arn(configs.get("iam_role"))
            if "session_id" in configs:
                self.set_new_session_id(configs.get("session_id"))
            if "max_capacity" in configs:
                self.set_max_capacity(configs.get("max_capacity"))
            if "number_of_workers" in configs:
                self.set_number_of_workers(configs.get("number_of_workers"))
            if "worker_type" in configs:
                self.set_worker_type(configs.get("worker_type"))
            if "extra_jars" in configs:
                self.set_extra_jars(configs.get("extra_jars"))
            if "connections" in configs:
                self.set_connections(configs.get("connections"))
            if "security_config" in configs:
                self.set_security_config(configs.get("security_config"))
            if "glue_version" in configs:
                self.set_glue_version(configs.get("glue_version"))
            if "idle_timeout" in configs:
                self.set_idle_timeout(configs.get("idle_timeout"))
            if "timeout" in configs:
                self.set_timeout(configs.get("timeout"))
            if "tags" in configs:
                self.add_tag_to_resource(configs.get("tags"))
            for arg, val in configs.items():
                if arg not in kernel_managed_params:
                    self.add_default_argument(arg, val)
        except Exception as e:
            sys.stderr.write(
                f"The following exception was encountered while parsing the configurations provided: {e} \n"
            )
            self._print_traceback(e)
            return
        if not configs:
            sys.stderr.write("No configuration values were provided.")
        else:
            self._send_output(f"The following configurations have been updated: {configs}")

    def do_shutdown(self, restart):
        self.stop_session()
        return self._do_shutdown(restart)

    def _do_shutdown(self, restart):
        return super(BaseKernel, self).do_shutdown(restart)

    def set_profile(self, profile):
        setattr(self.overrides, PROFILE, profile)
        # Injecting the new profile into the AWS config file retriever.
        aws_config_retriever = self.retrievers.get(AWS_CONFIG_RETRIEVER)
        setattr(aws_config_retriever, PROFILE, profile)

    def set_glue_role_arn(self, glue_role_arn):
        setattr(self.overrides, IAM_ROLE, glue_role_arn)

    def get_profile(self):
        # Attempt to retrieve default profile if a profile is not already set
        profile = self.config_manager.get_config_by_priority(PROFILE)
        if not profile and botocore.session.Session().full_config["profiles"].get("default"):
            setattr(self.overrides, PROFILE, profile)
        return self.config_manager.get_config_by_priority(PROFILE)

    def get_glue_role_arn(self):
        return self.config_manager.get_config_by_priority(IAM_ROLE)

    def get_sessions(self):
        if not self.kernel_gateway.is_glue_client_initialized():
            self.kernel_gateway.initialize_clients(profile=self.get_profile(), region=self.get_region(), endpoint_url=self.get_endpoint_url(), temp_credentials=self.get_temp_credentials())
        return self.kernel_gateway.list_sessions()

    def get_session_id(self):
        return self.session_id

    def get_new_session_id(self):
        return self.new_session_id

    def set_session_id(self, session_id):
        self.session_id = session_id

    def set_new_session_id(self, new_session_id=None):
        self.new_session_id = self._generate_session_id(new_session_id)

    def set_endpoint_url(self, endpoint_url):
        setattr(self.overrides, ENDPOINT_URL, endpoint_url)

    def get_endpoint_url(self):
        return self.config_manager.get_config_by_priority(ENDPOINT_URL)

    def set_region(self, region):
        region = region.lower()
        setattr(self.overrides, REGION, region)

    def get_region(self):
        return self.config_manager.get_config_by_priority(REGION)

    # Stores the pretty name for the SessionType Enum.
    def set_session_type(self, session_type):
        setattr(self.overrides, SESSION_TYPE, session_type)

    def get_session_type(self):
        return self.config_manager.get_config_by_priority(SESSION_TYPE)

    def add_default_argument(self, arg, val):

        arg = str(arg) if str(arg).startswith("--") else f'--{arg}'
        val = str(val)

        self.default_arguments[arg] = val

    # Default arguments are not directly exposed to the customer. Hence, config priority is not needed.
    def get_default_arguments(self):
        # Adding additional arguments to the list of default arguments if set by the customer.
        self.add_default_arguments_with_config_priority()

        if self.default_arguments:
            self._send_output(f"Applying the following default arguments:")
            for arg, val in self.default_arguments.items():
                self._send_output(f"{arg} {val}")
        return self.default_arguments

    def add_default_arguments_with_config_priority(self):
        if self.config_manager.get_config_by_priority(ENABLE_DATA_CATALOG):
            self.add_default_argument("enable-glue-datacatalog",self.config_manager.get_config_by_priority(
                ENABLE_DATA_CATALOG))
        if self.config_manager.get_config_by_priority(EXTRA_PY_FILES):
            self.add_default_argument("extra-py-files",self.config_manager.get_config_by_priority(EXTRA_PY_FILES))
        if self.config_manager.get_config_by_priority(EXTRA_JARS):
            self.add_default_argument("extra-jars", self.config_manager.get_config_by_priority(EXTRA_JARS))
        if self.config_manager.get_config_by_priority(ADDITIONAL_PYTHON_MODULES):
            self.add_default_argument("additional-python-modules", self.config_manager.get_config_by_priority(
                ADDITIONAL_PYTHON_MODULES))
        if self.config_manager.get_config_by_priority(SPARK_CONF):
            self.add_default_argument("conf",self.config_manager.get_config_by_priority(SPARK_CONF))

    def set_enable_glue_datacatalog(self):
        setattr(self.overrides, ENABLE_DATA_CATALOG, True)

    def set_extra_py_files(self, extra_py_files):
        setattr(self.overrides, EXTRA_PY_FILES, extra_py_files)

    def set_extra_jars(self, extra_jars):
        setattr(self.overrides, EXTRA_JARS, extra_jars)

    def set_additional_python_modules(self, modules):
        setattr(self.overrides, ADDITIONAL_PYTHON_MODULES, modules)

    def get_connections(self):
        return self.config_manager.get_config_by_priority(CONNECTIONS)

    def set_connections(self, connections):
        setattr(self.overrides, CONNECTIONS, connections)

    def get_account_id(self):
        response = self.kernel_gateway.get_caller_identity(self.get_profile(), self.get_region())
        return response.get('Account')

    def get_tags(self):
        return self.config_manager.get_config_from_all_retrievers(TAGS)

    def create_resource_arn(self):
        region = self.get_region()
        if region in CHINA_REGIONS:
            resource_arn = 'arn:aws-cn:glue:' + str(self.get_region()) + ':' + str(self.get_account_id()) + ':session/' + str(self.get_session_id())
        elif region in US_GOV_REGIONS:
            resource_arn = 'arn:aws-us-gov:glue:' + str(self.get_region()) + ':' + str(self.get_account_id()) + ':session/' + str(self.get_session_id())
        else:
            resource_arn = 'arn:aws:glue:' + str(self.get_region()) + ':' + str(self.get_account_id()) + ':session/' + str(self.get_session_id())
        return resource_arn

    def get_tags_from_resource(self):
        resource_arn = self.create_resource_arn()
        session_id = self.get_session_id()
        try:
            response = self.kernel_gateway.get_tags(resource_arn)
            return response, None
        except botocore.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code in ('AccessDeniedException'):
                return None, "Tags: Unable to display tags due to missing glue:GetTags permission. Please update your IAM policy."
            else:
                return None, f"Unable to fetch tags for the session: {session_id} due to error {error_code}"

    def add_tags_to_resource_ready_state(self, tags):
        resource_arn = self.create_resource_arn()
        session_id = self.get_session_id()
        if tags:
            try:
                response = self.kernel_gateway.tag_resource(resource_arn, tags)
                return None
            except botocore.exceptions.ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code in ('AccessDeniedException'):
                    return "Tags: Unable to add tags due to missing glue:TagResource permission. Please update your IAM policy."
                else:
                    return f"Unable to add tags for the session: {session_id} due to error {error_code}"
        else:
            return

    def set_tags(self, tags):
        if isinstance(tags, str):
            tags_dict = json.loads(tags)
            setattr(self.overrides, TAGS, tags_dict)
        else:
            setattr(self.overrides, TAGS, tags)

    def add_tag(self, key, value):
        tags = getattr(self.overrides, TAGS, defaultdict())
        tags[key] = value

    def add_tag_to_resource(self, tags):
        if tags:
            for (key, value) in tags.items():
                self.add_tag(key, value)

    def get_request_origin(self):
        return self.request_origin

    def set_request_origin(self, request_origin):
        self.request_origin = request_origin

    def get_glue_version(self):
        return self.config_manager.get_config_by_priority(GLUE_VERSION)

    def set_glue_version(self, glue_version):
        setattr(self.overrides, GLUE_VERSION, glue_version)

    def get_session_name(self):
        return self.session_name

    def get_max_capacity(self):
        return self.config_manager.get_config_by_priority(MAX_CAPACITY)

    def set_max_capacity(self, max_capacity):
        setattr(self.overrides, MAX_CAPACITY, max_capacity)

    def get_number_of_workers(self):
        return self.config_manager.get_config_by_priority(NUMBER_OF_WORKERS)

    def set_number_of_workers(self, number_of_workers):
        setattr(self.overrides, NUMBER_OF_WORKERS, number_of_workers)

    def get_worker_type(self):
        return self.config_manager.get_config_by_priority(WORKER_TYPE)

    def set_worker_type(self, worker_type):
        setattr(self.overrides, WORKER_TYPE, worker_type)

    def get_security_config(self):
        return self.config_manager.get_config_by_priority(SECURITY_CONFIG)

    def set_security_config(self, security_config):
        setattr(self.overrides, SECURITY_CONFIG, security_config)

    def get_idle_timeout(self):
        return self.config_manager.get_config_by_priority(IDLE_TIMEOUT)

    def set_idle_timeout(self, idle_timeout):
        setattr(self.overrides, IDLE_TIMEOUT, idle_timeout)

    def get_timeout(self):
        return self.config_manager.get_config_by_priority(TIMEOUT)

    def set_timeout(self, timeout):
        setattr(self.overrides, TIMEOUT, timeout)

    def set_spark_conf(self, conf):
        setattr(self.overrides, SPARK_CONF, conf)

    def get_spark_conf(self):
        return self.config_manager.get_config_by_priority(SPARK_CONF)

    def set_session_id_prefix(self, session_id_prefix):
        setattr(self.overrides, SESSION_ID_PREFIX, session_id_prefix)

    def get_session_id_prefix(self):
        return self.config_manager.get_config_by_priority(SESSION_ID_PREFIX)

    def _generate_session_id(self, custom_id=None):
        prefix = self.get_session_id_prefix()
        if prefix:
            if not custom_id:
                return f"{prefix}-{uuid.uuid4()}"
            return f"{prefix}-{custom_id}"
        else:
            if not custom_id:
                return f"{uuid.uuid4()}"
            return custom_id

    def create_session(self):
        glue_role_arn = self.get_glue_role_arn()
        if not glue_role_arn:
            glue_arn_from_sts = self.kernel_gateway.get_iam_role_using_sts(self.get_profile(), self.get_region())
            if glue_arn_from_sts:
                self.set_glue_role_arn(glue_arn_from_sts)
            else:
                raise ValueError('Glue Role ARN not provided')

        self._send_output("Trying to create a Glue session for the kernel.")
        if self.get_max_capacity() and (self.get_number_of_workers() and self.get_worker_type()):
            raise ValueError(
                f"Either max_capacity or worker_type and number_of_workers must be set, but not both."
            )

        # Generate new session ID with UUID if no custom ID is set
        if not self.get_new_session_id():
            self.set_new_session_id()
            if not self.get_new_session_id():
                raise ValueError(f"Session ID was not set.")
        session_type_enum = None
        try:
            session_type = self._convert_to_pretty_name(self.get_session_type())
            session_type_enum = SessionType[session_type]
            self._send_output(f"Session Type: {self.get_session_type()}")
        except KeyError:
            raise ValueError(f"Unsupported session type {self.get_session_type()}")

        # Print Max Capacity if it is set. Else print Number of Workers and Worker Type
        if self.get_max_capacity():
            self._send_output(f"Max Capacity: {self.get_max_capacity()}")
        else:
            if self.get_worker_type():
                self._send_output(f"Worker Type: {self.get_worker_type()}")
            if self.get_number_of_workers():
                self._send_output(f"Number of Workers: {self.get_number_of_workers()}")

        if self.get_idle_timeout():
            self._send_output(f"Idle Timeout: {self.get_idle_timeout()}")
        if self.get_timeout():
            self._send_output(f"Timeout: {self.get_timeout()}")

        self._send_output(f"Session ID: {self.get_new_session_id()}")

        additional_args = self._get_additional_arguments()

        response = self.kernel_gateway.create_session(
            self.get_glue_role_arn(),
            self.get_default_arguments(),
            self.get_new_session_id(),
            {"Name": session_type_enum.session_type(), "PythonVersion": session_type_enum.python_version()},
            **additional_args,
        )
        self.set_session_id(
            response["Session"]["Id"]
        )

        self._send_output(
            f"Waiting for session {self.get_session_id()} to get into ready status..."
        )
        start_time = time.time()
        current_status = None
        while time.time() - start_time <= self.time_out:
            current_status = self.get_current_session_status()
            if current_status == READY_SESSION_STATUS:
                break
            elif current_status == PROVISIONING_SESSION_STATUS:
                time.sleep(WAIT_TIME)
                continue
            elif current_status in UNHEALTHY_SESSION_STATUS:
                break
            else:
                time.sleep(WAIT_TIME)
                continue

        if time.time() - start_time > self.time_out:
            self._send_error_output(f"Timed out after {self.time_out} seconds waiting for session to reach {READY_SESSION_STATUS} status.")
        elif current_status in UNHEALTHY_SESSION_STATUS:
            self._send_error_output(f"Session failed to reach {READY_SESSION_STATUS} instead reaching terminal state {self.get_current_session_status()}.")
        elif current_status != READY_SESSION_STATUS:
            self._send_error_output(f"Session failed to reach {READY_SESSION_STATUS} status.")
        else:
            self._send_output(f"Session {self.get_session_id()} has been created.")

    def _get_additional_arguments(self):
        additional_args = {}
        if self.get_max_capacity():
            additional_args["MaxCapacity"] = float(self.get_max_capacity())
        if self.get_number_of_workers():
            additional_args["NumberOfWorkers"] = int(self.get_number_of_workers())
        if self.get_worker_type():
            additional_args["WorkerType"] = self.get_worker_type()
        if self.get_security_config():
            additional_args["SecurityConfiguration"] = self.get_security_config()
        if self.get_idle_timeout():
            additional_args["IdleTimeout"] = int(self.get_idle_timeout())
        if self.get_timeout():
            additional_args["Timeout"] = int(self.get_timeout())
        if self.get_connections():
            additional_args["Connections"] = {"Connections" : list(self.get_connections().split(","))}
        if self.get_glue_version():
            additional_args["GlueVersion"] = self.get_glue_version()
        if self.get_request_origin():
            additional_args["RequestOrigin"] = self.get_request_origin()

        # add tags
        if self.get_request_origin() == GLUE_STUDIO_NOTEBOOK_IDENTIFIER:
            user_id = self._retrieve_os_env_variable(USER_ID)
        else:
            user_id = self._get_user_id()
        if user_id:  # check if user ID exists and if so, add it as a tag
            self.add_tag(OWNER_TAG, re.sub(",", "", user_id))
        tags = self.get_tags()
        if len(tags) > 0:
            additional_args["Tags"] = tags

        return additional_args

    def stop_session(self):
        if self.get_session_id():
            try:
                self._send_output(f"Stopping session: {self.get_session_id()}")
                # TODO: how do we stop session if our security token expires?
                if not self.kernel_gateway.is_glue_client_initialized():
                    self.kernel_gateway.initialize_clients(profile=self.get_profile(), region=self.get_region(),
                                                           endpoint_url=self.get_endpoint_url(), temp_credentials=self.get_temp_credentials)
                self.kernel_gateway.stop_session(self.get_session_id())
                self.reset_kernel()
            except Exception as e:
                sys.stderr.write(f"Exception encountered while stopping session {self.get_session_id()}: {e} \n")
                self._print_traceback(e)

    def _cancel_statement(self, statement_id: str):
        if not statement_id:
            return

        try:
            self.kernel_gateway.cancel_statement(self.get_session_id(), statement_id)
            start_time = time.time()
            is_ready = False

            while time.time() - start_time <= self.time_out and not is_ready:
                status = self.kernel_gateway.get_statement(self.get_session_id(), statement_id)["Statement"]["State"]
                if status == CANCELLED_STATEMENT_STATUS:
                    self._send_output(f"Statement {statement_id} has been cancelled")
                    is_ready = True

                time.sleep(WAIT_TIME)

            if not is_ready:
                sys.stderr.write(f"Failed to cancel the statement {statement_id}")
        except Exception as e:
            sys.stderr.write(
                f"Exception encountered while canceling statement {statement_id}: {e} \n"
            )
            self._print_traceback(e)

    def get_session_status(self):
        if self.get_session_id() is None:
            return
        else:
            try:
                return self.kernel_gateway.get_session(self.get_session_id())["Session"].get("Status")
            except Exception as e:
                return None

    def get_current_session_status(self):
        try:
            return self.get_current_session()["Status"]
        except Exception as e:
            sys.stderr.write(f"Failed to retrieve session status \n")

    def get_current_session_role(self):
        try:
            return self.get_current_session()["Role"]
        except Exception as e:
            sys.stderr.write(f"Failed to retrieve session role \n")

    def get_current_session(self):
        if self.get_session_id() is None:
            sys.stderr.write(f"No current session.")
        else:
            try:
                current_session = self.kernel_gateway.get_session(self.get_session_id())["Session"]
                return NOT_FOUND_SESSION_STATUS if not current_session else current_session
            except Exception as e:
                sys.stderr.write(f"Exception encountered while retrieving session: {e} \n")
                self._print_traceback(e)

    def _handle_sql_code(self, lines):
        sql_code = "\n".join(lines[1:])
        return f'spark.sql("""{sql_code.rstrip()}""").show()'


    def _send_markdown_output(self, output):
        self.send_response(self.iopub_socket, 'display_data', {
            'metadata': {},
            'data': {
                'text/markdown': output
            }
        })

    def _send_output(self, output):
        stream_content = {"name": "stdout", "text": f"{output}\n"}
        self.send_response(self.iopub_socket, "stream", stream_content)

    def _send_error_output(self, output):
        stream_content = {"name": "stderr", "text": f"{output}\n"}
        self.send_response(self.iopub_socket, "stream", stream_content)

    def _construct_reply_content(self, statement):

        statement_output = statement["Output"]
        status = statement["State"]
        reply_content = {
            "execution_count": self.execution_counter,
            "user_expressions": {},
            "payload": [],
        }

        if status in (AVAILABLE_STATEMENT_STATUS, COMPLETED_STATEMENT_STATUS):
            self.execution_counter += 1
            if status == COMPLETED_STATEMENT_STATUS or ('Status' in statement_output and statement_output["Status"] == "ok"):
                reply_content["status"] = "ok"
                self.display_result(statement_output)
            else:
                reply_content["status"] = "error"
                reply_content.update(
                    {
                        "traceback": statement_output["Traceback"],
                        "ename": statement_output["ErrorName"],
                        "evalue": statement_output["ErrorValue"],
                    }
                )
                self._send_output(
                    f"{statement_output['ErrorName']}: {statement_output['ErrorValue']}"
                )
        elif status == ERROR_STATEMENT_STATUS:
            self.execution_counter += 1
            sys.stderr.write(str(statement_output))
            reply_content.update(self._construct_reply_error(statement_output))
        elif status == FAILED_STATEMENT_STATUS:
            self.execution_counter += 1
            reply_content.update(self._construct_reply_error(statement_output))
            if 'Data' in statement_output:
                statement_output_data = statement_output['Data']
                stdout_text = self.kernel_gateway.get_results(statement_output_data['StdOut']) if 'StdOut' in statement_output_data else ""
                if len(stdout_text):
                    self._send_output(stdout_text)
                failure_reason = self.kernel_gateway.get_results(statement_output_data['Result']) if 'Result' in statement_output_data else ""
                if len(failure_reason):
                    self._send_error_output(failure_reason)
                stderr_text = self.kernel_gateway.get_results(statement_output_data['StdErr']) if 'StdErr' in statement_output_data else ""
                if len(stderr_text):
                    self._send_error_output(stderr_text)

        elif status == CANCELLED_STATEMENT_STATUS:
            self.execution_counter += 1
            reply_content.update(self._construct_reply_error(statement_output))
            self._send_output("This statement is cancelled")

        return reply_content

    def _construct_reply_error(self, statement_output):
        if (not statement_output) or (not all(map(lambda x: x in statement_output, ['TraceBack', 'ErrorName', 'ErrorValue']))):
            return dict({"status": "abort"})
        else:
            return dict({
                "status": "error",
                "traceback": statement_output["Traceback"],
                "ename": statement_output["ErrorName"],
                "evalue": statement_output["ErrorValue"],
            })

    async def _do_execute(self, code, silent, store_history, user_expressions, allow_stdin):
        res = await self._execute_cell(code, silent, store_history, user_expressions, allow_stdin)
        return res

    async def _execute_cell(
            self, code, silent, store_history=True, user_expressions=None, allow_stdin=False
    ):
        reply_content = await self._execute_cell_for_user(
            code, silent, store_history, user_expressions, allow_stdin
        )
        return reply_content

    async def _execute_cell_for_user(
            self, code, silent, store_history=True, user_expressions=None, allow_stdin=False
    ):
        result = await super(BaseKernel, self).do_execute(
            code, silent, store_history, user_expressions, allow_stdin
        )
        if isinstance(result, Future):
            result = result.result()
        return result

    async def _execute_magics(self, code, silent, store_history, user_expressions, allow_stdin):
        try:
            magic_lines = 0
            lines = code.splitlines()
            for line in lines:
                # If there is a cell magic, we simply treat all the remaining code as part of the cell magic
                if any(line.startswith(cell_magic) for cell_magic in CELL_MAGICS):
                    if line.startswith(SQL_CELL_MAGIC):
                        return self._handle_sql_code(lines)
                    else:
                        code = "\n".join(lines[magic_lines:])
                        await self._do_execute(
                            code, silent, store_history, user_expressions, allow_stdin
                        )
                    return None
                # If we encounter a line magic, we execute this line magic and continue
                if line.startswith("%") or line.startswith("!"):
                    await self._do_execute(
                        line, silent, store_history, user_expressions, allow_stdin
                    )
                    magic_lines += 1
                # We ignore comments and empty lines
                elif line.startswith("#") or not line:
                    magic_lines += 1
                else:
                    break
            code = "\n".join(lines[magic_lines:])
            return code
        except Exception as e:
            sys.stderr.write(f"Exception encountered: {e} \n")
            self._print_traceback(e)
            return await self._complete_cell()

    async def _complete_cell(self):
        """A method that runs a cell with no effect. Call this and return the value it
        returns when there's some sort of error preventing the user's cell from executing; this
        will register the cell from the Jupyter UI as being completed."""
        return await self._execute_cell("None", False, True, None, False)

    def _register_magics(self):
        ip = get_ipython()
        magics = KernelMagics(ip, "", self)
        ip.register_magics(magics)

    def _initialize_retrievers(self, overrides):
        # Config priority is Overridden Config (Magics) > Env variables > Config File > Defaults.
        # OrderedDict is explicitly used to show config priority.
        retrievers = OrderedDict()
        retrievers[OVERRIDES_RETRIEVER] = OverriddenConfigRetriever(overrides)
        retrievers[SYSTEM_ENV_RETRIEVER] = SystemEnvConfigRetriever(self.get_request_origin())
        retrievers[AWS_CONFIG_RETRIEVER] = AWSFileConfigRetriever()
        retrievers[DEFAULT_RETRIEVER] = DefaultConfigRetriever(default_configs)
        return retrievers

    def _print_traceback(self, e):
        traceback.print_exception(type(e), e, e.__traceback__)

    async def _print_startup_text(self):
        self._send_output("Welcome to the Glue Interactive Sessions Kernel")
        self._send_output(
            "For more information on available magic commands, please type %help in any new cell.\n"
        )
        self._send_output(
            "Please view our Getting Started page to access the most up-to-date information on the Interactive Sessions kernel: https://docs.aws.amazon.com/glue/latest/dg/interactive-sessions.html"
        )
        self.should_print_startup_text = False
        current_kernel_version = self._get_current_kernel_version("aws-glue-sessions")
        latest_kernel_version = self._get_latest_kernel_version("aws-glue-sessions")
        if (
                latest_kernel_version
                and current_kernel_version
                and latest_kernel_version != current_kernel_version
        ):
            self._send_output(
                f"It looks like there is a newer version of the kernel available. The latest version is {latest_kernel_version} and you have {current_kernel_version} installed."
            )
            self._send_output(
                "Please run `pip install --upgrade aws-glue-sessions` to upgrade your kernel"
            )
        elif latest_kernel_version is None and current_kernel_version is not None:
            self._send_output(f"Installed kernel version: {current_kernel_version} ")

    def _get_latest_kernel_version(self, name):
        if not (self.request_origin == "GlueStudioNotebook"
                or self.request_origin in SAGEMAKER_STUDIO_NOTEBOOK_IDENTIFIERS):
            try:
                response = requests.get("https://pypi.org/pypi/{}/json".format(name))
                data = response.json()
                latest_version = data["info"]["version"]
                return str(latest_version)
            except Exception:
                return None

    def _get_current_kernel_version(self, name):
        try:
            current_version = version(name)
            return str(current_version)
        except Exception:
            return None

    def reset_kernel(self):
        self.set_session_id(None)
        self.set_new_session_id(None)
        self.execution_counter = 1
        self.kernel_gateway = KernelGateway()

    def switch_session(self, session_id):
        if session_id == self.get_session_id():
            self._send_output(f'Session: {session_id} is already active.')
            return
        self.kernel_gateway.initialize_clients(profile=self.get_profile(), region=self.get_region(), endpoint_url=self.get_endpoint_url(), temp_credentials=self.get_temp_credentials())
        session = None
        try:
            session = self.kernel_gateway.get_session(session_id)['Session']
        except Exception as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            if error_code in 'EntityNotFoundException':
                self._send_output(Colour.Red + Colour.Bold + f"Exception encountered while retrieving session: {error_message}"
                                                             f" Please make sure the session exists for the account in the configured region.")
                return
            else:
                self._send_output(Colour.Red + Colour.Bold + f"Exception encountered while retrieving session: {error_message} \n")
                return
        if session is None or session['Status'] in UNHEALTHY_SESSION_STATUS:
            self._send_output(Colour.Red + Colour.Bold + f'Failed to switch, Session: {session_id} is not in {READY_SESSION_STATUS} state.')
            return
        # Not printing statement history, once we have customer feedback on whether we should have it & how, implement
        # statements = self.kernel_gateway.list_statements(session_id)
        self.set_session_id(session_id)
        self.set_new_session_id(None)
        self._send_output(f'Switched to Session: {session_id}.')
        self.execution_counter = 1

    # https://github.com/ipython/ipykernel/issues/795
    # Redirect logs to only print in terminal

    def _setup_terminal_logging(self):
        for std, __std__ in [
            (sys.stdout, sys.__stdout__),
            (sys.stderr, sys.__stderr__),
        ]:
            if getattr(std, "_original_stdstream_copy", None) is not None:
                # redirect captured pipe back to original FD
                os.dup2(std._original_stdstream_copy, __std__.fileno())
                std._original_stdstream_copy = None

    def _log_to_terminal(self, log):
        print(f"LOG: {log}", file=sys.__stdout__, flush=True)

    def _get_user_id(self):
        response = self.kernel_gateway.get_caller_identity(self.get_profile(), self.get_region())
        return response.get("UserId")

    def _retrieve_from_aws_config(self, key):
        custom_profile_session = botocore.session.Session(profile=self.get_profile())
        return custom_profile_session.full_config["profiles"][self.get_profile()].get(key)

    def _retrieve_os_env_variable(self, key):
        if self.get_request_origin() not in SAGEMAKER_STUDIO_NOTEBOOK_IDENTIFIERS:
            return os.environ.get(key)
        else:
            _, output = subprocess.getstatusoutput(f"echo ${key}")
            return os.getenv(key, output)

    def handle_exception(self, e):
        print(Colour.Red + "Error: " + str(e))

    def _format_endpoint_url(self, region):
        if region in ADC_REGION_ENDPOINTS:
            return ADC_REGION_ENDPOINTS[region]
        elif region in CHINA_REGIONS:
            return f"https://glue.{region}.amazonaws.com.cn"
        else:
            return f"https://glue.{region}.amazonaws.com"

    def _convert_to_pretty_name(self, session_type):
        # Some systems are already passing the session_type as the actual value and other systems are passing it as pretty name.
        # Handling both the cases irrespective of what's given, converting it to pretty name and looking up the ENUM
        if session_type.lower() in [SessionType.etl.session_type().lower(), SessionType.etl.pretty_name().lower()]:
            return SessionType.etl.pretty_name()
        elif session_type.lower() in [SessionType.streaming.session_type().lower(), SessionType.streaming.pretty_name().lower()]:
            return SessionType.streaming.pretty_name()

