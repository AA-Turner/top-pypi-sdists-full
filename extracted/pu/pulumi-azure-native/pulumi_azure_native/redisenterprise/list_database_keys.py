# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import builtins
import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from .. import _utilities

__all__ = [
    'ListDatabaseKeysResult',
    'AwaitableListDatabaseKeysResult',
    'list_database_keys',
    'list_database_keys_output',
]

@pulumi.output_type
class ListDatabaseKeysResult:
    """
    The secret access keys used for authenticating connections to redis
    """
    def __init__(__self__, primary_key=None, secondary_key=None):
        if primary_key and not isinstance(primary_key, str):
            raise TypeError("Expected argument 'primary_key' to be a str")
        pulumi.set(__self__, "primary_key", primary_key)
        if secondary_key and not isinstance(secondary_key, str):
            raise TypeError("Expected argument 'secondary_key' to be a str")
        pulumi.set(__self__, "secondary_key", secondary_key)

    @property
    @pulumi.getter(name="primaryKey")
    def primary_key(self) -> builtins.str:
        """
        The current primary key that clients can use to authenticate
        """
        return pulumi.get(self, "primary_key")

    @property
    @pulumi.getter(name="secondaryKey")
    def secondary_key(self) -> builtins.str:
        """
        The current secondary key that clients can use to authenticate
        """
        return pulumi.get(self, "secondary_key")


class AwaitableListDatabaseKeysResult(ListDatabaseKeysResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListDatabaseKeysResult(
            primary_key=self.primary_key,
            secondary_key=self.secondary_key)


def list_database_keys(cluster_name: Optional[builtins.str] = None,
                       database_name: Optional[builtins.str] = None,
                       resource_group_name: Optional[builtins.str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListDatabaseKeysResult:
    """
    Retrieves the access keys for the RedisEnterprise database.

    Uses Azure REST API version 2024-03-01-preview.

    Other available API versions: 2020-10-01-preview, 2021-02-01-preview, 2021-03-01, 2021-08-01, 2022-01-01, 2022-11-01-preview, 2023-03-01-preview, 2023-07-01, 2023-08-01-preview, 2023-10-01-preview, 2023-11-01, 2024-02-01, 2024-06-01-preview, 2024-09-01-preview, 2024-10-01, 2025-04-01, 2025-05-01-preview. These can be accessed by generating a local SDK package using the CLI command `pulumi package add azure-native redisenterprise [ApiVersion]`. See the [version guide](../../../version-guide/#accessing-any-api-version-via-local-packages) for details.


    :param builtins.str cluster_name: The name of the Redis Enterprise cluster.
    :param builtins.str database_name: The name of the Redis Enterprise database.
    :param builtins.str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    __args__['databaseName'] = database_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:redisenterprise:listDatabaseKeys', __args__, opts=opts, typ=ListDatabaseKeysResult).value

    return AwaitableListDatabaseKeysResult(
        primary_key=pulumi.get(__ret__, 'primary_key'),
        secondary_key=pulumi.get(__ret__, 'secondary_key'))
def list_database_keys_output(cluster_name: Optional[pulumi.Input[builtins.str]] = None,
                              database_name: Optional[pulumi.Input[builtins.str]] = None,
                              resource_group_name: Optional[pulumi.Input[builtins.str]] = None,
                              opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[ListDatabaseKeysResult]:
    """
    Retrieves the access keys for the RedisEnterprise database.

    Uses Azure REST API version 2024-03-01-preview.

    Other available API versions: 2020-10-01-preview, 2021-02-01-preview, 2021-03-01, 2021-08-01, 2022-01-01, 2022-11-01-preview, 2023-03-01-preview, 2023-07-01, 2023-08-01-preview, 2023-10-01-preview, 2023-11-01, 2024-02-01, 2024-06-01-preview, 2024-09-01-preview, 2024-10-01, 2025-04-01, 2025-05-01-preview. These can be accessed by generating a local SDK package using the CLI command `pulumi package add azure-native redisenterprise [ApiVersion]`. See the [version guide](../../../version-guide/#accessing-any-api-version-via-local-packages) for details.


    :param builtins.str cluster_name: The name of the Redis Enterprise cluster.
    :param builtins.str database_name: The name of the Redis Enterprise database.
    :param builtins.str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    __args__['databaseName'] = database_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure-native:redisenterprise:listDatabaseKeys', __args__, opts=opts, typ=ListDatabaseKeysResult)
    return __ret__.apply(lambda __response__: ListDatabaseKeysResult(
        primary_key=pulumi.get(__response__, 'primary_key'),
        secondary_key=pulumi.get(__response__, 'secondary_key')))
