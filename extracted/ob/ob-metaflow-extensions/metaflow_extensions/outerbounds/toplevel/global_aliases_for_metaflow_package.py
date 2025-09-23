# These two fields will show up within `metaflow_version` task metadata.
# Setting to major version of ob-metaflow-extensions only, so we don't keep trying
# (and failing) to keep this in sync with setup.py
# E.g. "2.7.22.1+ob(v1)"
__version__ = "v1"
__mf_extensions__ = "ob"

from metaflow_extensions.outerbounds.toplevel.s3_proxy import (
    get_aws_client_with_s3_proxy,
    get_S3_with_s3_proxy,
)

_S3_PROXY_CONFIG = None


def set_s3_proxy_config(config):
    global _S3_PROXY_CONFIG
    _S3_PROXY_CONFIG = config


def clear_s3_proxy_config():
    global _S3_PROXY_CONFIG
    _S3_PROXY_CONFIG = None


def get_s3_proxy_config():
    global _S3_PROXY_CONFIG
    if _S3_PROXY_CONFIG is None:
        set_s3_proxy_config(get_s3_proxy_config_from_env())
    return _S3_PROXY_CONFIG


# TODO: Refactor out the _S3_PROXY_CONFIG global variable and instead use the function that
# extracts it from the environment variables.

import os
import json


def get_s3_proxy_config_from_env():
    env_conf = os.environ.get("METAFLOW_S3_PROXY_USER_CODE_CONFIG")
    if env_conf:
        return json.loads(env_conf)
    return None


# Must match the signature of metaflow.plugins.aws.aws_client.get_aws_client
# This function is called by the "userland" code inside tasks. Metaflow internals
# will call the function in metaflow.plugins.aws.aws_client.get_aws_client directly.
#
# Unlike the original function, this wrapper will use the CSPR role if both of the following
# conditions are met:
#
#  1. CSPR is set
#  2. user didn't provide a role to assume explicitly.
#
def get_aws_client(
    module, with_error=False, role_arn=None, session_vars=None, client_params=None
):
    import metaflow.plugins.aws.aws_client
    import os

    from metaflow_extensions.outerbounds.plugins import USE_CSPR_ROLE_ARN_IF_SET
    from metaflow_extensions.outerbounds.plugins.aws.assume_role import (
        OBP_ASSUME_ROLE_ARN_ENV_VAR,
    )

    # Check if the assume_role decorator has set a role ARN via environment variable
    # This takes precedence over CSPR but not over explicitly passed role_arn
    if role_arn is None:
        decorator_role_arn = os.environ.get(OBP_ASSUME_ROLE_ARN_ENV_VAR)
        if decorator_role_arn:
            role_arn = decorator_role_arn

    if module == "s3" and get_s3_proxy_config() is not None:
        return get_aws_client_with_s3_proxy(
            module,
            with_error,
            role_arn,
            session_vars,
            client_params,
            get_s3_proxy_config(),
        )

    client = metaflow.plugins.aws.aws_client.get_aws_client(
        module,
        with_error=with_error,
        role_arn=role_arn or USE_CSPR_ROLE_ARN_IF_SET,
        session_vars=session_vars,
        client_params=client_params,
    )

    return client


# This should match the signature of metaflow.plugins.datatools.s3.S3.
#
# This assumes that "userland" code inside tasks will call this, while Metaflow
# internals will call metaflow.plugins.datatools.s3.S3 directly.
#
# This wrapper will make S3() use the CSPR role if its set, and user didn't provide
# a role to assume explicitly.
def S3(*args, **kwargs):
    import sys
    import metaflow.plugins.datatools.s3
    import os
    from metaflow_extensions.outerbounds.plugins import USE_CSPR_ROLE_ARN_IF_SET
    from metaflow_extensions.outerbounds.plugins.aws.assume_role import (
        OBP_ASSUME_ROLE_ARN_ENV_VAR,
    )

    # Check if the assume_role decorator has set a role ARN via environment variable
    # This takes precedence over CSPR but not over explicitly passed role
    if "role" not in kwargs or kwargs["role"] is None:
        decorator_role_arn = os.environ.get(OBP_ASSUME_ROLE_ARN_ENV_VAR)
        if decorator_role_arn:
            kwargs["role"] = decorator_role_arn
        else:
            kwargs["role"] = USE_CSPR_ROLE_ARN_IF_SET

    # Check if S3 proxy is active using module variable (like CSPR)
    if get_s3_proxy_config() is not None:
        return get_S3_with_s3_proxy(get_s3_proxy_config(), *args, **kwargs)

    return metaflow.plugins.datatools.s3.S3(*args, **kwargs)


# Setting the S3 client docstring in order to ensure that
# stubs get generated properly.
import metaflow.plugins.datatools.s3

S3.__doc__ = metaflow.plugins.datatools.s3.S3.__doc__

from .. import profilers
from ..plugins.snowflake import Snowflake
from ..plugins.checkpoint_datastores import nebius_checkpoints, coreweave_checkpoints
from ..plugins.aws import assume_role
from . import ob_internal
from .ob_internal import AppDeployer
