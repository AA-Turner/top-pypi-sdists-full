######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.515972                                                            #
######################################################################################################

from __future__ import annotations


from .... import profilers as profilers
from ..plugins.snowflake.snowflake import Snowflake as Snowflake
from ..plugins.checkpoint_datastores.nebius import nebius_checkpoints as nebius_checkpoints
from ..plugins.checkpoint_datastores.coreweave import coreweave_checkpoints as coreweave_checkpoints
from ..plugins.aws.assume_role_decorator import assume_role as assume_role
from .... import ob_internal as ob_internal
from ..plugins.apps.core.deployer import AppDeployer as AppDeployer

def get_aws_client(module, with_error = False, role_arn = None, session_vars = None, client_params = None):
    ...

def S3(*args, **kwargs):
    ...

