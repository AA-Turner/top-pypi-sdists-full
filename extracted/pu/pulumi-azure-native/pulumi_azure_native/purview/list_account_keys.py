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
    'ListAccountKeysResult',
    'AwaitableListAccountKeysResult',
    'list_account_keys',
    'list_account_keys_output',
]

@pulumi.output_type
class ListAccountKeysResult:
    """
    The Purview Account access keys.
    """
    def __init__(__self__, atlas_kafka_primary_endpoint=None, atlas_kafka_secondary_endpoint=None):
        if atlas_kafka_primary_endpoint and not isinstance(atlas_kafka_primary_endpoint, str):
            raise TypeError("Expected argument 'atlas_kafka_primary_endpoint' to be a str")
        pulumi.set(__self__, "atlas_kafka_primary_endpoint", atlas_kafka_primary_endpoint)
        if atlas_kafka_secondary_endpoint and not isinstance(atlas_kafka_secondary_endpoint, str):
            raise TypeError("Expected argument 'atlas_kafka_secondary_endpoint' to be a str")
        pulumi.set(__self__, "atlas_kafka_secondary_endpoint", atlas_kafka_secondary_endpoint)

    @property
    @pulumi.getter(name="atlasKafkaPrimaryEndpoint")
    def atlas_kafka_primary_endpoint(self) -> Optional[builtins.str]:
        """
        Gets or sets the primary connection string.
        """
        return pulumi.get(self, "atlas_kafka_primary_endpoint")

    @property
    @pulumi.getter(name="atlasKafkaSecondaryEndpoint")
    def atlas_kafka_secondary_endpoint(self) -> Optional[builtins.str]:
        """
        Gets or sets the secondary connection string.
        """
        return pulumi.get(self, "atlas_kafka_secondary_endpoint")


class AwaitableListAccountKeysResult(ListAccountKeysResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListAccountKeysResult(
            atlas_kafka_primary_endpoint=self.atlas_kafka_primary_endpoint,
            atlas_kafka_secondary_endpoint=self.atlas_kafka_secondary_endpoint)


def list_account_keys(account_name: Optional[builtins.str] = None,
                      resource_group_name: Optional[builtins.str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListAccountKeysResult:
    """
    List the authorization keys associated with this account.

    Uses Azure REST API version 2024-04-01-preview.

    Other available API versions: 2021-12-01, 2023-05-01-preview. These can be accessed by generating a local SDK package using the CLI command `pulumi package add azure-native purview [ApiVersion]`. See the [version guide](../../../version-guide/#accessing-any-api-version-via-local-packages) for details.


    :param builtins.str account_name: The name of the account.
    :param builtins.str resource_group_name: The resource group name.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:purview:listAccountKeys', __args__, opts=opts, typ=ListAccountKeysResult).value

    return AwaitableListAccountKeysResult(
        atlas_kafka_primary_endpoint=pulumi.get(__ret__, 'atlas_kafka_primary_endpoint'),
        atlas_kafka_secondary_endpoint=pulumi.get(__ret__, 'atlas_kafka_secondary_endpoint'))
def list_account_keys_output(account_name: Optional[pulumi.Input[builtins.str]] = None,
                             resource_group_name: Optional[pulumi.Input[builtins.str]] = None,
                             opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[ListAccountKeysResult]:
    """
    List the authorization keys associated with this account.

    Uses Azure REST API version 2024-04-01-preview.

    Other available API versions: 2021-12-01, 2023-05-01-preview. These can be accessed by generating a local SDK package using the CLI command `pulumi package add azure-native purview [ApiVersion]`. See the [version guide](../../../version-guide/#accessing-any-api-version-via-local-packages) for details.


    :param builtins.str account_name: The name of the account.
    :param builtins.str resource_group_name: The resource group name.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure-native:purview:listAccountKeys', __args__, opts=opts, typ=ListAccountKeysResult)
    return __ret__.apply(lambda __response__: ListAccountKeysResult(
        atlas_kafka_primary_endpoint=pulumi.get(__response__, 'atlas_kafka_primary_endpoint'),
        atlas_kafka_secondary_endpoint=pulumi.get(__response__, 'atlas_kafka_secondary_endpoint')))
