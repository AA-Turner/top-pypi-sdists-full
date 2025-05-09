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
from ._enums import *

__all__ = [
    'ListAssetContainerSasResult',
    'AwaitableListAssetContainerSasResult',
    'list_asset_container_sas',
    'list_asset_container_sas_output',
]

@pulumi.output_type
class ListAssetContainerSasResult:
    """
    The Asset Storage container SAS URLs.
    """
    def __init__(__self__, asset_container_sas_urls=None):
        if asset_container_sas_urls and not isinstance(asset_container_sas_urls, list):
            raise TypeError("Expected argument 'asset_container_sas_urls' to be a list")
        pulumi.set(__self__, "asset_container_sas_urls", asset_container_sas_urls)

    @property
    @pulumi.getter(name="assetContainerSasUrls")
    def asset_container_sas_urls(self) -> Optional[Sequence[builtins.str]]:
        """
        The list of Asset container SAS URLs.
        """
        return pulumi.get(self, "asset_container_sas_urls")


class AwaitableListAssetContainerSasResult(ListAssetContainerSasResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListAssetContainerSasResult(
            asset_container_sas_urls=self.asset_container_sas_urls)


def list_asset_container_sas(account_name: Optional[builtins.str] = None,
                             asset_name: Optional[builtins.str] = None,
                             expiry_time: Optional[builtins.str] = None,
                             permissions: Optional[Union[builtins.str, 'AssetContainerPermission']] = None,
                             resource_group_name: Optional[builtins.str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListAssetContainerSasResult:
    """
    Lists storage container URLs with shared access signatures (SAS) for uploading and downloading Asset content. The signatures are derived from the storage account keys.

    Uses Azure REST API version 2023-01-01.

    Other available API versions: 2018-03-30-preview, 2018-06-01-preview, 2018-07-01, 2020-05-01, 2021-06-01, 2021-11-01, 2022-08-01. These can be accessed by generating a local SDK package using the CLI command `pulumi package add azure-native media [ApiVersion]`. See the [version guide](../../../version-guide/#accessing-any-api-version-via-local-packages) for details.


    :param builtins.str account_name: The Media Services account name.
    :param builtins.str asset_name: The Asset name.
    :param builtins.str expiry_time: The SAS URL expiration time.  This must be less than 24 hours from the current time.
    :param Union[builtins.str, 'AssetContainerPermission'] permissions: The permissions to set on the SAS URL.
    :param builtins.str resource_group_name: The name of the resource group within the Azure subscription.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['assetName'] = asset_name
    __args__['expiryTime'] = expiry_time
    __args__['permissions'] = permissions
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:media:listAssetContainerSas', __args__, opts=opts, typ=ListAssetContainerSasResult).value

    return AwaitableListAssetContainerSasResult(
        asset_container_sas_urls=pulumi.get(__ret__, 'asset_container_sas_urls'))
def list_asset_container_sas_output(account_name: Optional[pulumi.Input[builtins.str]] = None,
                                    asset_name: Optional[pulumi.Input[builtins.str]] = None,
                                    expiry_time: Optional[pulumi.Input[Optional[builtins.str]]] = None,
                                    permissions: Optional[pulumi.Input[Optional[Union[builtins.str, 'AssetContainerPermission']]]] = None,
                                    resource_group_name: Optional[pulumi.Input[builtins.str]] = None,
                                    opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[ListAssetContainerSasResult]:
    """
    Lists storage container URLs with shared access signatures (SAS) for uploading and downloading Asset content. The signatures are derived from the storage account keys.

    Uses Azure REST API version 2023-01-01.

    Other available API versions: 2018-03-30-preview, 2018-06-01-preview, 2018-07-01, 2020-05-01, 2021-06-01, 2021-11-01, 2022-08-01. These can be accessed by generating a local SDK package using the CLI command `pulumi package add azure-native media [ApiVersion]`. See the [version guide](../../../version-guide/#accessing-any-api-version-via-local-packages) for details.


    :param builtins.str account_name: The Media Services account name.
    :param builtins.str asset_name: The Asset name.
    :param builtins.str expiry_time: The SAS URL expiration time.  This must be less than 24 hours from the current time.
    :param Union[builtins.str, 'AssetContainerPermission'] permissions: The permissions to set on the SAS URL.
    :param builtins.str resource_group_name: The name of the resource group within the Azure subscription.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['assetName'] = asset_name
    __args__['expiryTime'] = expiry_time
    __args__['permissions'] = permissions
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure-native:media:listAssetContainerSas', __args__, opts=opts, typ=ListAssetContainerSasResult)
    return __ret__.apply(lambda __response__: ListAssetContainerSasResult(
        asset_container_sas_urls=pulumi.get(__response__, 'asset_container_sas_urls')))
