import sys
from botocore.config import Config
from urllib3.exceptions import InsecureRequestWarning
import warnings
warnings.filterwarnings('ignore', category=InsecureRequestWarning)

import time
import traceback

import re
import os

import boto3
import botocore
from botocore.exceptions import ClientError
from urllib3.util import parse_url

from ..glue_kernel_utils.GlueSessionsConstants import *


def split_s3_path(s3_path):
    path_parts = s3_path.replace("s3://", "").split("/")
    bucket = path_parts.pop(0)
    key = "/".join(path_parts)
    return bucket, key


class KernelGateway:
    # Configuring max_ties to 3 and min retry between calls to 0.5 seconds for retryable exceptions.
    max_tries = 3
    min_retry_time = 0.5

    def __init__(self):
        self.glue_client = None
        self.sts_client = None
        self.iam_client = None
        self.s3_client = None

    def initialize_clients(self, profile=None, region=None, endpoint_url=None, temp_credentials=None):
        if temp_credentials:
            self.initialize_clients_with_temp_credentials(temp_credentials, region)
            return
        self.sts_client = self.create_sts_client(profile, region)
        self.iam_client = self.create_iam_client(profile, region)
        self.s3_client = self.create_s3_client(profile, region)
        self.glue_client = self._authenticate(profile, region, endpoint_url)

    def initialize_clients_with_temp_credentials(self, temp_credentials, region):
        self.sts_client = boto3.Session().client("sts", region_name = region,  verify=False,
                                                 aws_access_key_id=temp_credentials['temp_aws_access_key_id'] ,
                                                 aws_secret_access_key=temp_credentials['temp_aws_secret_access_key'],
                                                 aws_session_token=temp_credentials['temp_aws_session_token'])
        self.iam_client = boto3.Session().client("iam", region_name = region,  verify=False,
                                                 aws_access_key_id=temp_credentials['temp_aws_access_key_id'] ,
                                                 aws_secret_access_key=temp_credentials['temp_aws_secret_access_key'],
                                                 aws_session_token=temp_credentials['temp_aws_session_token'])
        self.s3_client = boto3.Session().client("s3", region_name = region,
                                               aws_access_key_id=temp_credentials['temp_aws_access_key_id'] ,
                                               aws_secret_access_key=temp_credentials['temp_aws_secret_access_key'],
                                               aws_session_token=temp_credentials['temp_aws_session_token'])
        self.glue_client = boto3.Session().client("glue", region_name = region,  verify=False,
                                                  aws_access_key_id=temp_credentials['temp_aws_access_key_id'] ,
                                                  aws_secret_access_key=temp_credentials['temp_aws_secret_access_key'],
                                                  aws_session_token=temp_credentials['temp_aws_session_token'])


    def _authenticate(self, profile=None, region=None, endpoint_url=None):
        # region must be set
        if not region:
            raise ValueError(f"Region must be set.")
        # If we are using a custom endpoint
        if not endpoint_url:
            endpoint_url = self._format_endpoint_url(region)
        if profile:
            return self._authenticate_with_profile(profile, region, endpoint_url)
        else:
            return self._create_client(profile, region, endpoint_url)

    def _authenticate_with_profile(self, profile=None, region=None, endpoint_url=None):
        if profile not in self._get_available_profiles():
            raise ValueError(f"Profile {profile} not defined in config")
        return self._create_client(profile, region, endpoint_url)

    def _create_client(self, profile=None, region=None, endpoint_url=None):
        # Having a standard retry config for the boto3 client.
        # Retries on the following AWS Standard errors/exceptions:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/retries.html#standard-retry-mode
        config = Config(
            retries={
                'max_attempts': 1,
                'mode': 'standard'
            }
        )
        # boto3 will automatically look for env variables, config file, IMDS
        # for credentials in the order: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
        if profile:
            return boto3.Session(profile_name=profile).client("glue", region_name=region, config=config, verify=False)
        else:
            return boto3.Session().client("glue", region_name=region, endpoint_url=endpoint_url, config=config, verify=False)

    def create_session(self, role, default_arguments, new_session_id, command, **additional_args):
        for i in range(1, self.max_tries + 1):
            try:
                response = self.glue_client.create_session(
                    Role=role,
                    DefaultArguments=default_arguments,
                    Id=new_session_id,
                    Command=command,
                    **additional_args,
                )
                return response
                # All boto3 exceptions are classified under ClientError.
                # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html
            except botocore.exceptions.ClientError as e:
                error_code = e.response['Error']['Code']
                error_message = e.response['Error']['Message']
                if error_code in ('OperationTimeoutException', 'InternalServiceException',
                                  'ResourceNumberLimitExceededException'):
                    time.sleep(i * self.min_retry_time)
                    continue
                elif error_code in ('InvalidInputException', 'AlreadyExistsException', 'AccessDeniedException'):
                    sys.stderr.write("{}\n".format(f'Following exception encountered while creating session: {e} \n'))
                    sys.stderr.write("{}\n".format(f'Error message: {error_message} \n'))
                    sys.stderr.flush()
                    self._print_traceback(e)
                    raise
                else:
                    sys.stderr.write("{}\n".format(f'Unknown exception encountered while creating session: {e} \n'))
                    sys.stderr.write("{}\n".format(f'Error message: {error_message} \n'))
                    sys.stderr.flush()
                    self._print_traceback(e)
                    raise
        raise RuntimeError('Error while creating session')

    def stop_session(self, session_id):
        for i in range(1, self.max_tries + 1):
            if session_id:
                try:
                    response = self.glue_client.stop_session(Id=session_id)
                    return response
                except botocore.exceptions.ClientError as e:
                    error_code = e.response['Error']['Code']
                    if error_code in ('OperationTimeoutException', 'InternalServiceException'):
                        time.sleep(i * self.min_retry_time)
                        continue
                    else:
                        raise
        raise RuntimeError('Error while stopping session')

    def run_statement(self, session_id, code):
        for i in range(1, self.max_tries + 1):
            try:
                return self.glue_client.run_statement(
                    SessionId=session_id, Code=code
                )
            except botocore.exceptions.ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code in ('InternalServiceException', 'ResourceNumberLimitExceededException'):
                    time.sleep(i * self.min_retry_time)
                    continue
                else:
                    raise
        raise RuntimeError('Error while running statement')

    def cancel_statement(self, session_id, statement_id: str):
        for i in range(1, self.max_tries + 1):
            try:
                return self.glue_client.cancel_statement(SessionId=session_id, Id=statement_id)
            except botocore.exceptions.ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code in ('InternalServiceException', 'OperationTimeoutException'):
                    time.sleep(i * self.min_retry_time)
                    continue
                else:
                    raise
        raise RuntimeError('Error while canceling statement')

    def get_statement(self, session_id, statement_id: str):
        for i in range(1, self.max_tries + 1):
            try:
                return self.glue_client.get_statement(SessionId=session_id, Id=statement_id)
            except botocore.exceptions.ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code in ('InternalServiceException', 'OperationTimeoutException'):
                    time.sleep(i * self.min_retry_time)
                    continue
                else:
                    raise
        raise RuntimeError('Error while getting statement')

    def get_session(self, session_id):
        for i in range(1, self.max_tries + 1):
            try:
                return self.glue_client.get_session(Id=session_id)
            except botocore.exceptions.ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code in ('InternalServiceException', 'OperationTimeoutException'):
                    time.sleep(i * self.min_retry_time)
                    continue
                else:
                    raise
        raise RuntimeError('Error while getting session')

    def list_sessions(self):
        for i in range(1, self.max_tries + 1):
            try:
                return self.glue_client.list_sessions()
            except botocore.exceptions.ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code in ('InternalServiceException', 'OperationTimeoutException'):
                    time.sleep(i * self.min_retry_time)
                    continue
                else:
                    raise
        raise RuntimeError('Error while getting list of session')

    def list_statements(self, session_id):
        for i in range(1, self.max_tries + 1):
            try:
                return self.glue_client.list_statements(SessionId=session_id)
            except botocore.exceptions.ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code in ('InternalServiceException', 'OperationTimeoutException'):
                    time.sleep(i * self.min_retry_time)
                    continue
                else:
                    raise
        raise RuntimeError(f'Error while getting list of statements for session: {session_id}')

    def get_tags(self, resource_arn):
        for i in range(1, self.max_tries + 1):
            try:
                return self.glue_client.get_tags(ResourceArn=resource_arn).get("Tags")
            except botocore.exceptions.ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code in ('InternalServiceException', 'OperationTimeoutException'):
                    time.sleep(i * self.min_retry_time)
                    continue
                else:
                    raise
        raise RuntimeError('Error while fetching tags for the session')

    def tag_resource(self, resource_arn, tags):
        for i in range(1, self.max_tries + 1):
            try:
                return self.glue_client.tag_resource(ResourceArn=resource_arn, TagsToAdd=tags)
            except botocore.exceptions.ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code in ('InternalServiceException', 'OperationTimeoutException'):
                    time.sleep(i * self.min_retry_time)
                    continue
                else:
                    raise
        raise RuntimeError('Error while adding tags for the session')

    def get_results(self, s3_path):
        if not s3_path.startswith("s3"):
            print(f"No output file found at {s3_path}")
            return "No output file found"
        try:
            urlparts = parse_url(s3_path)
            s3_object = self.s3_client.get_object(Bucket=urlparts.host, Key=urlparts.path[1:])
            return s3_object["Body"].read().decode("utf-8")
        except botocore.exceptions.ClientError as e:
            print(f"Response from get_object with {s3_path} was {e}")
            raise RuntimeError("Error while getting calculation results", e)


    def _get_available_profiles(self):
        return boto3.session.Session().available_profiles

    def is_glue_client_initialized(self):
        if self.glue_client is None:
            return False
        return True

    def _print_traceback(self, e):
        traceback.print_exception(type(e), e, e.__traceback__)

    def get_iam_role_using_sts(self, profile=None, region=None):
        try:
            role_arn = self.sts_client.get_caller_identity().get("Arn")
        except Exception:
            return None
        regex = r"arn:aws[^:]*:sts::[0-9]*:assumed-role/(.+)/.+"
        m = re.match(regex, role_arn)
        if m:
            role_arn = self._get_role_arn_from_iam(m.group(1), region)
            return role_arn

        return None

    def _get_role_arn_from_iam(self, role_name, region=None):
        return self.iam_client.get_role(RoleName=role_name).get("Role", {}).get("Arn", None)

    def get_caller_identity(self, profile=None, region=None):
        return self.sts_client.get_caller_identity()

    def create_sts_client(self, profile=None, region=None):
        if not region:
            raise ValueError(f"Region must be set.")
        if profile:
            return boto3.Session(profile_name=profile).client(
                "sts", region_name=region, verify=False
            )
        else:
            return boto3.Session().client(
                "sts",
                region_name=region,
                endpoint_url=self._get_sts_endpoint_url(region), verify=False
            )

    def create_iam_client(self, profile=None, region=None):
        if not region:
                raise ValueError(f"Region must be set.")
        if profile:
            return boto3.Session(profile_name=profile).client(
                "iam", region_name=region, verify=False
            )
        else:
            return boto3.Session().client(
                "iam",
                region_name=region, verify=False
            )

    def create_s3_client(self, profile=None, region=None):
        if not region:
                raise ValueError(f"Region must be set.")
        if profile:
            return boto3.Session(profile_name=profile).client(
                "s3", region_name=region,
                config=Config(retries=dict(max_attempts=10))
            )
        else:
            return boto3.Session().client(
                "s3",
                region_name=region,
                config=Config(retries=dict(max_attempts=10))
            )

    def _get_sts_endpoint_url(self, region):
        if region in ADC_REGION_STS_ENDPOINTS:
            return ADC_REGION_STS_ENDPOINTS[region]
        elif region in CHINA_REGIONS:
            return f"https://sts.{region}.amazonaws.com.cn"
        else:
            return f"https://sts.{region}.amazonaws.com"

    def _format_endpoint_url(self, region):
        if region in ADC_REGION_ENDPOINTS:
            return ADC_REGION_ENDPOINTS[region]
        elif region in CHINA_REGIONS:
            return f"https://glue.{region}.amazonaws.com.cn"
        else:
            return f"https://glue.{region}.amazonaws.com"


