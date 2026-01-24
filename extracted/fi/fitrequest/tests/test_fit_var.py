import os

import boto3
import botocore.exceptions
from moto import mock_aws
from pydantic import BaseModel

from fitrequest.aws_var import AWSSecretTypeEnum
from fitrequest.fit_var import FitVar, ValidFitVar


def test_default_value():
    assert str(FitVar()) == ''


def test_init_value():
    assert str(FitVar(init_value='toto')) == 'toto'


def test_env_value():
    env_name = 'SKCR_FIT_VAR'
    env_value = 'SKCR_ENV_VALUE'

    os.environ[env_name] = env_value
    assert str(FitVar(env_name=env_name)) == env_value
    os.environ.pop(env_name)


@mock_aws
def test_aws_value():
    ssm = boto3.client('ssm', region_name='eu-central-1')
    aws_var_value = 'SKCR_AWS_VAL'
    aws_var_path = '/dont_look_here/skcr_aws_var'

    ssm.put_parameter(
        Name=aws_var_path,
        Description='A test parameter',
        Value=aws_var_value,
        Type='SecureString',
    )
    assert str(FitVar(aws_path=aws_var_path, aws_type=AWSSecretTypeEnum.ssm)) == aws_var_value


@mock_aws
def test_value_priority():
    ssm = boto3.client('ssm', region_name='eu-central-1')
    aws_var_value = 'SKCR_AWS_VAL'
    aws_var_path = '/dont_look_here/skcr_aws_var'

    ssm.put_parameter(
        Name=aws_var_path,
        Description='A test parameter',
        Value=aws_var_value,
        Type='SecureString',
    )

    env_name = 'SKCR_FIT_VAR'
    env_value = 'SKCR_ENV_VALUE'
    os.environ[env_name] = env_value

    init_value = 'SKCR_INIT_VAL'
    should_be_init = FitVar(
        aws_path=aws_var_path,
        aws_type=AWSSecretTypeEnum.ssm,
        env_name=env_name,
        init_value=init_value,
    )
    should_be_env = FitVar(
        aws_path=aws_var_path,
        aws_type=AWSSecretTypeEnum.ssm,
        env_name=env_name,
    )
    should_be_aws = FitVar(
        aws_path=aws_var_path,
        aws_type=AWSSecretTypeEnum.ssm,
    )
    assert str(should_be_aws) == aws_var_value
    assert str(should_be_env) == env_value
    assert str(should_be_init) == init_value

    os.environ.pop(env_name)


def test_value_priority_with_aws_exception():
    def mocked_client() -> None:
        raise botocore.exceptions.ClientError(error_response={}, operation_name='test')

    boto3.client = mocked_client

    aws_var_path = '/dont_look_here/skcr_aws_var'

    env_name = 'SKCR_FIT_VAR'
    env_value = 'SKCR_ENV_VALUE'
    os.environ[env_name] = env_value

    init_value = 'SKCR_INIT_VAL'
    should_be_init = FitVar(
        aws_path=aws_var_path,
        aws_type=AWSSecretTypeEnum.ssm,
        env_name=env_name,
        init_value=init_value,
    )
    should_be_env = FitVar(
        aws_path=aws_var_path,
        aws_type=AWSSecretTypeEnum.ssm,
        env_name=env_name,
    )
    should_be_default = FitVar(
        aws_path=aws_var_path,
        aws_type=AWSSecretTypeEnum.ssm,
    )
    assert str(should_be_env) == env_value
    assert str(should_be_init) == init_value

    # No AWS value, so default value '' is returned
    assert str(should_be_default) == ''

    os.environ.pop(env_name)


class SomePydanticModel(BaseModel):
    var_default_none: ValidFitVar = None
    var_default_str: ValidFitVar = 'hello from str'
    var_default_dict: ValidFitVar = {'init_value': 'hello from dict'}
    var_default_fit_var: ValidFitVar = FitVar(init_value='hello from fit_var')


def test_defaults_validation():
    some_instance = SomePydanticModel()
    assert some_instance.var_default_none is None
    assert isinstance(some_instance.var_default_str, FitVar)
    assert isinstance(some_instance.var_default_dict, FitVar)
    assert isinstance(some_instance.var_default_fit_var, FitVar)
    assert str(some_instance.var_default_str) == 'hello from str'
    assert str(some_instance.var_default_dict) == 'hello from dict'
    assert str(some_instance.var_default_fit_var) == 'hello from fit_var'

    assert some_instance.model_dump() == {
        'var_default_none': None,
        'var_default_str': 'hello from str',
        'var_default_dict': 'hello from dict',
        'var_default_fit_var': 'hello from fit_var',
    }
