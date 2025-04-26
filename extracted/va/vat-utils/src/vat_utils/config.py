"""
Utilities for working with configuration
"""
import base64
import gzip
import io
import json
import os
import re
from typing import Optional

import boto3
import jsonpointer

def create_config_client(config_provider, config_source, boto3_session=None):
    """
    Create a config client of the specified type
    """
    if config_provider == 'environment' or config_provider is None:
        return EnvironmentVariableConfigClient()

    elif config_provider == 'aws_ssm':
        return SsmConfigClient(config_source, boto3_session=boto3_session)

    elif config_provider == 'aws_s3':
        return S3ConfigClient(config_source, boto3_session=boto3_session)

    elif config_provider == 'local_json_file':
        return LocalJsonFileConfigClient(config_source)

    elif config_provider == 'inline_json':
        return InlineJsonConfigClient(config_source)

    else:
        raise RuntimeError("Invalid config provider: {0}".format(config_provider))

def create_config_client_v2(config_source, boto3_session=None):
    provider, source = config_source.split(":")
    return create_config_client(provider, source, boto3_session=boto3_session)

def create_common_config_client(config_prefix, config_name, config_provider='aws_ssm'):
    config_source = "/{0}/{1}/config".format(config_prefix, config_name)
    return create_config_client(config_provider, config_source)

class BaseConfigClient(object):
    def get_value(self, parameter_path):
        raise NotImplementedError()

    def get_pointer_value(self, pointer):
        raise NotImplementedError()

    def get_root_json_value(self):
        raise NotImplementedError()

    def get_child_config_client(self, config_source_pointer):
        return create_config_client_v2(self.get_pointer_value(config_source_pointer))

    def get_child_config(self, config_source_pointer):
        child_config_client = create_config_client_v2(self.get_pointer_value(config_source_pointer))
        return child_config_client.get_root_json_value()

class BaseJsonConfigClient(BaseConfigClient):
    def get_value(self, parameter_path):
        data = self.get_root_json_value()
        return data[parameter_path]

    def get_pointer_value(self, pointer):
        data = self.get_root_json_value()
        return jsonpointer.resolve_pointer(data, pointer)

class EnvironmentVariableConfigClient(BaseConfigClient):
    """
    Config client getting values from environment variables
    """
    def get_value(self, parameter_path):
        return os.environ[parameter_path.upper()]

    def get_pointer_value(self, pointer):
        env_var_name = re.sub(r'/', '_', pointer.strip('/')).upper()
        return os.environ[env_var_name]

class BaseAwsJsonConfigClient(BaseJsonConfigClient):
    _boto3_session: Optional[boto3.Session]

    def get_child_config_client(self, config_source_pointer):
        return create_config_client_v2(
            self.get_pointer_value(config_source_pointer),
            boto3_session=self._boto3_session
        )

    def get_child_config(self, config_source_pointer):
        return self.get_child_config_client(config_source_pointer).get_root_json_value()

class SsmConfigClient(BaseAwsJsonConfigClient):
    """
    """
    def __init__(self, config_source, boto3_session=None):
        self._boto3_session = boto3_session

        if boto3_session is not None:
            self.ssm_client = boto3_session.client('ssm')
        else:
            self.ssm_client = boto3.client('ssm')

        self.config_source = config_source
        self.root_json_value = None

    def get_root_json_value(self):
        if self.root_json_value is None:
            self.root_json_value = self._fetch_root_json_value()

        return self.root_json_value

    def _fetch_root_json_value(self):
        response = self.ssm_client.get_parameter(
            Name=self.config_source,
            WithDecryption=True
        )
        value = response['Parameter']['Value']
        if value.startswith("{"):
            return json.loads(value)
        else:
            encoding, payload = re.match(r'^(?:([^:]+):)?([^:]+)$', value).groups()
            if encoding is None:
                return json.loads(base64.b64decode(payload).decode())
            elif encoding == 'b64gz':
                data = io.BytesIO(base64.b64decode(payload))
                with gzip.GzipFile(fileobj=data, mode='rb') as gz_data:
                    return json.loads(gz_data.read().decode())
            else:
                raise ValueError("Invalid parameter value")

class S3ConfigClient(BaseAwsJsonConfigClient):
    """
    """
    def __init__(self, config_source, boto3_session=None):
        self._boto3_session = boto3_session

        if boto3_session is not None:
            self.s3_client = boto3_session.client('s3')
        else:
            self.s3_client = boto3.client('s3')

        self.bucket, self.key = config_source.split("/", 1)
        self.root_json_value = None

    def get_root_json_value(self):
        if self.root_json_value is None:
            buffer = io.BytesIO()
            self.s3_client.download_fileobj(self.bucket, self.key, buffer)
            json_string = buffer.getvalue().decode()
            self.root_json_value = json.loads(json_string)

        return self.root_json_value

class LocalJsonFileConfigClient(BaseJsonConfigClient):
    """
    Config client reading config from a local JSON file
    """
    def __init__(self, config_source):
        with open(config_source) as json_file:
            self.config = json.load(json_file)

    def get_root_json_value(self):
        return self.config

class InlineJsonConfigClient(BaseJsonConfigClient):
    """
    Config client reading base64 encoded JSON config provided inline
    """
    def __init__(self, encoded_config):
            self.config = json.loads(base64.b64decode(encoded_config).decode())

    def get_root_json_value(self):
        return self.config

class CommonConfigClient(object):
    def __init__(self, config_prefix):
        self.config_prefix = config_prefix

    def get_config(self, config_name):
        config_client = create_common_config_client(self.config_prefix, config_name)
        return config_client.get_root_json_value()
