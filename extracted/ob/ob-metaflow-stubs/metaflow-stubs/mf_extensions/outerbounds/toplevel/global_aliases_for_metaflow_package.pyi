######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.34.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-08-13T18:38:42.548625                                                            #
######################################################################################################

from __future__ import annotations


from .s3_proxy import get_aws_client_with_s3_proxy as get_aws_client_with_s3_proxy
from .s3_proxy import get_S3_with_s3_proxy as get_S3_with_s3_proxy
from .... import profilers as profilers
from ..plugins.profilers.gpu_profile_decorator import gpu_profile as gpu_profile
from ..plugins.snowflake.snowflake import Snowflake as Snowflake
from ..plugins.checkpoint_datastores.nebius import nebius_checkpoints as nebius_checkpoints
from ..plugins.checkpoint_datastores.coreweave import coreweave_checkpoints as coreweave_checkpoints
from ..plugins.aws.assume_role_decorator import assume_role as assume_role
from .... import ob_internal as ob_internal
from ..plugins.apps.core.app_deploy_decorator import app_deploy as app_deploy
from ..plugins.anaconda_models.decorator import anaconda_models as anaconda_models
from .... import apps as apps
from ....metaflow_current import current as current

def set_s3_proxy_config(config):
    ...

def clear_s3_proxy_config():
    ...

def get_s3_proxy_config():
    ...

def get_s3_proxy_config_from_env():
    ...

def get_aws_client(module, with_error = False, role_arn = None, session_vars = None, client_params = None):
    ...

def S3(*args, **kwargs):
    """
    The Metaflow S3 client.
    
    This object manages the connection to S3 and a temporary diretory that is used
    to download objects. Note that in most cases when the data fits in memory, no local
    disk IO is needed as operations are cached by the operating system, which makes
    operations fast as long as there is enough memory available.
    
    The easiest way is to use this object as a context manager:
    ```
    with S3() as s3:
        data = [obj.blob for obj in s3.get_many(urls)]
    print(data)
    ```
    The context manager takes care of creating and deleting a temporary directory
    automatically. Without a context manager, you must call `.close()` to delete
    the directory explicitly:
    ```
    s3 = S3()
    data = [obj.blob for obj in s3.get_many(urls)]
    s3.close()
    ```
    You can customize the location of the temporary directory with `tmproot`. It
    defaults to the current working directory.
    
    To make it easier to deal with object locations, the client can be initialized
    with an S3 path prefix. There are three ways to handle locations:
    
    1. Use a `metaflow.Run` object or `self`, e.g. `S3(run=self)` which
       initializes the prefix with the global `DATATOOLS_S3ROOT` path, combined
       with the current run ID. This mode makes it easy to version data based
       on the run ID consistently. You can use the `bucket` and `prefix` to
       override parts of `DATATOOLS_S3ROOT`.
    
    2. Specify an S3 prefix explicitly with `s3root`,
       e.g. `S3(s3root='s3://mybucket/some/path')`.
    
    3. Specify nothing, i.e. `S3()`, in which case all operations require
       a full S3 url prefixed with `s3://`.
    
    Parameters
    ----------
    tmproot : str, default '.'
        Where to store the temporary directory.
    bucket : str, optional, default None
        Override the bucket from `DATATOOLS_S3ROOT` when `run` is specified.
    prefix : str, optional, default None
        Override the path from `DATATOOLS_S3ROOT` when `run` is specified.
    run : FlowSpec or Run, optional, default None
        Derive path prefix from the current or a past run ID, e.g. S3(run=self).
    s3root : str, optional, default None
        If `run` is not specified, use this as the S3 prefix.
    encryption : str, optional, default None
        Server-side encryption to use when uploading objects to S3.
    """
    ...

