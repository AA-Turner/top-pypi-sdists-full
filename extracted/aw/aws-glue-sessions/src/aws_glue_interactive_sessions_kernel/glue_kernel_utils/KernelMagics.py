from __future__ import print_function
import re
import ast
import boto3
import botocore
from botocore.exceptions import ClientError
from IPython.core.display import display_markdown
from IPython.core.magic import Magics, cell_magic, line_magic, magics_class

from .GlueSessionsConstants import *


@magics_class
class KernelMagics(Magics):

    def __init__(self, shell, data, kernel):
        super(KernelMagics, self).__init__(shell)
        self.data = data
        self.kernel = kernel

    @line_magic('iam_role')
    def set_glue_role_arn(self, glue_role_arn):
        self._validate_magic()
        glue_role_arn = self._strip_quotes(glue_role_arn)
        self.kernel._send_output(f'Current iam_role is {self.kernel.get_glue_role_arn()}')
        self.kernel.set_glue_role_arn(glue_role_arn)
        self.kernel._send_output(f'iam_role has been set to {glue_role_arn}.')

    @line_magic('idle_timeout')
    def set_idle_timeout(self, idle_timeout=2880):
        self._validate_magic()
        idle_timeout = self._strip_quotes(idle_timeout)
        self.kernel._send_output(f'Current idle_timeout is {self.kernel.get_idle_timeout()} minutes.')
        self.kernel.set_idle_timeout(int(idle_timeout))
        self.kernel._send_output(f'idle_timeout has been set to {self.kernel.get_idle_timeout()} minutes.')

    @line_magic('timeout')
    def set_timeout(self, timeout=2880):
        self._validate_magic()
        timeout = self._strip_quotes(timeout)
        self.kernel._send_output(f'Current timeout is {self.kernel.get_timeout()} minutes.')
        self.kernel.set_timeout(int(timeout))
        self.kernel._send_output(f'timeout has been set to {self.kernel.get_timeout()} minutes.')

    @line_magic('profile')
    def set_profile(self, profile):
        self._validate_magic()
        profile = self._strip_quotes(profile)
        self.kernel._send_output(f'Previous profile: {self.kernel.get_profile()}')
        self.kernel._send_output(f'Setting new profile to: {profile}')
        self.kernel.set_profile(profile)

    @line_magic('status')
    def get_status(self, line=None):
        if not self.kernel.get_session_id():
            self.kernel._send_output('There is no current session.')
            return
        session = self.kernel.get_current_session()
        status = self.kernel.get_current_session_status()
        role = self.kernel.get_current_session_role()
        session_id = session['Id']
        created_on = session['CreatedOn']
        glue_version = session['GlueVersion']
        if session['Command']:
            session_type = session['Command']['Name']
        tags, exception_error = self.kernel.get_tags_from_resource()
        self.kernel._send_output(f'Session ID: {session_id}')
        self.kernel._send_output(f'Status: {status}')
        self.kernel._send_output(f'Role: {role}')
        self.kernel._send_output(f'CreatedOn: {created_on}')
        self.kernel._send_output(f'GlueVersion: {glue_version}')
        self.kernel._send_output(f'Session Type: {session_type}')
        self.kernel._send_output(f"Idle Timeout: {session['IdleTimeout']}")
        if 'Timeout' in session:
            self.kernel._send_output(f"Timeout: {session['Timeout']}")
        # Uncomment after introducing Timeout in GetSessionResponse
        # self.kernel._send_output(f"Timeout: {session['Timeout']}")
        if exception_error:
            self.kernel._send_output(exception_error)
        else:
            self.kernel._send_output(f'Tags: {tags}')
        # Print Max Capacity if it is set. Else print Number of Workers and Worker Type
        if self.kernel.get_max_capacity():
            self.kernel._send_output(f"Max Capacity: {session['MaxCapacity']}")
        else:
            if session['WorkerType']:
                self.kernel._send_output(f"Worker Type: {session['WorkerType']}")
            if session['NumberOfWorkers']:
                self.kernel._send_output(f"Number of Workers: {session['NumberOfWorkers']}")
        self.kernel._send_output(f'Region: {self.kernel.get_region()}')
        if self.kernel.get_connections():
            connections = self.kernel.get_connections()
            self.kernel._send_output(f"Connections: {connections}")
        default_arguments = self.kernel.get_default_arguments()
        args_list = [str(f"{k}: {v}") for k,v in default_arguments.items()]
        self.kernel._send_output(f"Arguments Passed: {args_list}")

    @line_magic('list_sessions')
    def list_sessions(self, line=None):
        sessions = self.kernel.get_sessions()
        if not sessions or not len(self.kernel.get_sessions().get('Ids')):
            self.kernel._send_output(f'There are no sessions to list.')
        else:
            ids = sessions.get('Ids')
            self.kernel._send_output(f'The first {len(ids)} sessions are:')
            session_table = SessionTable()

            for session in sessions.get('Sessions'):
                session_id = session['Id']
                status = session['Status']
                created_on = session['CreatedOn']
                session_table.add_session_info(session_id, status, created_on)

            table_output = session_table.format_session_info()
            self.kernel._send_output(table_output)

    @line_magic('stop_session')
    def stop_session(self, line=None):
        if not self.kernel.get_session_id():
            self.kernel._send_output('There is no current session.')
            return
        self.kernel.stop_session()
        self.kernel._send_output(f'Stopped session.')

    @line_magic('session_id')
    def set_session_id(self, line=None):
        if not self.kernel.get_session_id():
            self.kernel._send_output('There is no current session.')
        else:
            self.kernel._send_output(f'Current active Session ID: {self.kernel.get_session_id()}')

    @line_magic('reconnect')
    def reconnect_session(self, session_id):
        self._strip_quotes(session_id)
        if session_id:
            self.kernel._send_output(f'Trying to switch to Session: {session_id}')
            self.kernel._send_output(Colour.LightYellow + Colour.Bold + f'NOTE: Switching to a live session will not terminate the current session.' + Colour.Reset)
            self.kernel.switch_session(session_id)
        else:
            self._send_output(Colour.Red + Colour.Bold + f'Invalid input, Session Id: {session_id}.')
            self.kernel._send_output(f'Current active Session ID: {self.kernel.get_session_id()}')

    @line_magic('session_id_prefix')
    def set_session_id_prefix(self, line=None):
        formatted_line = self._strip_quotes(line)
        if not self._validate_prefix(formatted_line):
            self.kernel._send_output(f'Not a valid input, the prefix only accepts -._#/A-Za-z0-9')
        else:
            self.kernel.set_session_id_prefix(formatted_line)
            self.kernel._send_output(f'Setting session ID prefix to {self.kernel.get_session_id_prefix()}')

    @line_magic('extra_py_files')
    def set_extra_py_files(self, line=None):
        self._validate_magic()
        line = self._strip_quotes(line)
        line = self._validate_list(line)
        if not line:
            return
        self.kernel._send_output("Extra py files to be included:")
        for s3_path in line.split(','):
            self.kernel._send_output(s3_path)
        self.kernel.set_extra_py_files(line)

    @line_magic('additional_python_modules')
    def set_additional_python_modules(self, line=None):
        self._validate_magic()
        line = self._strip_quotes(line)
        line = self._validate_list(line)
        if not line:
            return
        self.kernel._send_output("Additional python modules to be included:")
        for module in line.split(','):
            self.kernel._send_output(module)
        self.kernel.set_additional_python_modules(line)

    @line_magic('extra_jars')
    def set_extra_jars(self, line=None):
        self._validate_magic()
        line = self._strip_quotes(line)
        line = self._validate_list(line)
        if not line:
            return
        self.kernel._send_output("Extra jars to be included:")
        for s3_path in line.split(','):
            self.kernel._send_output(s3_path)
        print(line)
        self.kernel.set_extra_jars(line)

    @line_magic('connections')
    def set_connections(self, line=None):
        self._validate_magic()
        line = self._strip_quotes(line)
        line = self._validate_list(line)
        if not line:
            return
        self.kernel._send_output("Connections to be included:")
        for connection in line.split(','):
            self.kernel._send_output(connection)
        self.kernel.set_connections(line)

    @line_magic('glue_version')
    def set_glue_version(self,line=None):
        self._validate_magic()
        line = self._strip_quotes(line)
        self.kernel._send_output(f"Setting Glue version to: {line}")
        self.kernel.set_glue_version(line)

    @line_magic('endpoint')
    def set_endpoint(self, line=None):
        self._validate_magic()
        line = self._strip_quotes(line)
        previous_endpoint = self.kernel.get_endpoint_url()
        self.kernel._send_output(f'Previous endpoint: {previous_endpoint}')
        self.kernel._send_output(f'Setting new endpoint to: {line}')
        self.kernel.set_endpoint_url(line)
        self.kernel._send_output(f'Endpoint is set to: {line}')

    @line_magic('region')
    def set_region(self, line=None):
        self._validate_magic()
        line = self._strip_quotes(line)
        line = line.lower()
        previous_region = self.kernel.get_region()
        self.kernel._send_output(f'Previous region: {previous_region}')
        self.kernel._send_output(f'Setting new region to: {line}')
        self.kernel.set_region(line)
        self.kernel._send_output(f'Region is set to: {line}')

    @line_magic('number_of_workers')
    def set_number_of_workers(self, line=None):
        self._validate_magic()
        line = self._strip_quotes(line)
        self.kernel._send_output(f'Previous number of workers: {self.kernel.get_number_of_workers()}')
        self.kernel._send_output(f'Setting new number of workers to: {int(line)}')
        self.kernel.set_number_of_workers(line)

    @line_magic('worker_type')
    def set_worker_type(self, line=None):
        self._validate_magic()
        line = self._strip_quotes(line)
        self.kernel._send_output(f'Previous worker type: {self.kernel.get_worker_type()}')
        self.kernel._send_output(f'Setting new worker type to: {line}')
        self.kernel.set_worker_type(line)

    @line_magic('streaming')
    def set_streaming(self, line=None):
        self._validate_magic()
        self.kernel._send_output(f'Previous session type: {self.kernel.get_session_type()}')
        self.kernel._send_output('Setting new session type to Streaming')
        self.kernel.set_session_type(SessionType.streaming.pretty_name())

    @line_magic('etl')
    def set_etl(self, line=None):
        self._validate_magic()
        self.kernel._send_output(f'Previous session type: {self.kernel.get_session_type()}')
        self.kernel._send_output('Setting new session type to ETL')
        self.kernel.set_session_type(SessionType.etl.pretty_name())

    @line_magic('security_config')
    def set_security_config(self, line=None):
        self._validate_magic()
        line = self._strip_quotes(line)
        self.kernel._send_output(f'Previous security_config: {self.kernel.get_security_config()}')
        self.kernel._send_output(f'Setting new security_config to: {line}')
        self.kernel.set_security_config(line)

    @line_magic('session_type')
    def set_session_type(self, line=None):
        line = self._strip_quotes(line)
        self.kernel.set_session_type(line)

    @cell_magic('sql')
    def run_sql(self, line=None, cell=None):
        # No functionality here. SQL code formatted and passed by _handle_sql_code()
        # This function exists to declare the existence of the %%sql cell magic
        return

    @cell_magic('configure')
    def configure(self, line=None, cell=None):
        self._validate_magic()
        self.kernel.configure(cell)

    @line_magic('spark_conf')
    def spark_conf(self, conf=None):
        current_conf = self.kernel.get_spark_conf()
        if not conf:
            if not current_conf:
                self.kernel._send_output("No Spark configuration set")
            else:
                self.kernel._send_output(current_conf)
        else:
            self.kernel.set_spark_conf(conf)
            self.kernel._send_output(f'Previous Spark configuration: {current_conf}')
            self.kernel._send_output(f'Setting new Spark configuration to: {conf}')

    @line_magic('help')
    def help(self, line=None):
        self.kernel._send_markdown_output(HELP_TEXT)

    @cell_magic('tags')
    def add_tags_to_session(self, line=None, cell=None):
        session_status = self.kernel.get_session_status()
        if cell:
            try:
                cell = ast.literal_eval(cell)
                valid_tags = self._validate_dict(cell)
                if session_status == READY_SESSION_STATUS:
                    exception_error = self.kernel.add_tags_to_resource_ready_state(valid_tags)
                    if exception_error:
                        self.kernel._send_output(exception_error)
                        return
                self.kernel.add_tag_to_resource(valid_tags)
                self.kernel._send_output(f'Tag {valid_tags} added')
            except Exception:
                self.kernel.handle_exception(Exception(f'Please provide magics like {{"tag_key":"tag_value"}} : {cell}'))
        return

    @cell_magic('assume_role')
    def assume_role_for_cross_account(self, line=None, cell=None):
        self._validate_magic()
        if cell:
            cell = ast.literal_eval(cell)
            try:
                if type(cell) is str:
                    response = boto3.client('sts').assume_role(RoleArn=cell, RoleSessionName=self.kernel.get_session_name())
                    self.kernel.set_temporary_credentials(response['Credentials']['AccessKeyId'], response['Credentials']['SecretAccessKey'], response['Credentials']['SessionToken'])
                elif type(cell) is dict:
                    valid_dict = self._validate_dict(cell)
                    self.kernel.set_temporary_credentials(valid_dict['aws_access_key_id'], valid_dict['aws_secret_access_key'], valid_dict['aws_session_token'])
                self.kernel._send_output('Role assumed successfully')
            except botocore.exceptions.ClientError as e:
                error_code = e.response['Error']['Code']
                error_message = e.response['Error']['Message']
                if error_code in ('MalformedPolicyDocumentException', 'PackedPolicyTooLargeException', 'RegionDisabledException', 'ExpiredTokenException'):
                    self.kernel._send_error_output(f'Following exception encountered while assuming role for cross account user: {e} \n')
                    self.kernel._send_error_output(f'Error message: {error_message} \n')
                    self.kernel._print_traceback(e)
                else:
                    self.kernel._send_error_output(f'Error message: {error_message} \n')
                    self.kernel._print_traceback(e)
            except Exception as e:
                self.kernel._send_error_output(f"Not a valid input type {e}")
                self.kernel._print_traceback(e)

    def _strip_quotes(self, line):
        if not line:
            return None
        # Remove quotes
        line = line.strip('"')
        line = line.strip("'")
        return line

    def _validate_dict(self, cell):
        if not cell:
            return None
        else:
            return dict((key.strip(), value.strip()) for key, value in cell.items())

    def _validate_list(self, line):
        if not line:
            return None
        try:
            line = line.strip("[]")
            value_list = line.split(",")
            # create new list and strip leading and trailing spaces
            values = []
            for val in list(value_list):
                next_val = str(val).strip()
                if not next_val:
                    self.kernel._send_output("Empty values are not allowed to be passed.")
                    return None
                elif " " in next_val:
                    if "--" in next_val:
                        pass
                    else:
                        self.kernel._send_output(f'Invalid value. There is at least one blank space present in this value: {next_val}')
                        return None
                values.append(next_val)
        except Exception as e:
            self.kernel._send_output(f'Invalid list of inputs provided: {line}')
            return None
        return ",".join(values)

    def _validate_magic(self):
        session_id = self.kernel.get_session_id()
        if session_id:
            session = self.kernel.get_current_session()
            session_type = session['Command']['Name'] if session and not session == NOT_FOUND_SESSION_STATUS else None
            if session_type:
                self.kernel._send_error_output(f'You are already connected to a {session_type} session {session_id}.\n\nNo change will be made to the current session that is set as {session_type}. The session configuration change will apply to newly created sessions.')
            else:
                self.kernel._send_error_output(f'You are already connected to a session {session_id}.\n\nNo change will be made to the current session. The session configuration change will apply to newly created sessions.\n')

    def _validate_prefix(self, line):
        pattern = re.compile("[-/._#A-Za-z0-9]+")
        if not pattern.fullmatch(line):
            return False
        return True
