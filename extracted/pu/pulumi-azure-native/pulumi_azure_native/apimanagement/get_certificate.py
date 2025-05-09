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
from . import outputs

__all__ = [
    'GetCertificateResult',
    'AwaitableGetCertificateResult',
    'get_certificate',
    'get_certificate_output',
]

@pulumi.output_type
class GetCertificateResult:
    """
    Certificate details.
    """
    def __init__(__self__, azure_api_version=None, expiration_date=None, id=None, key_vault=None, name=None, subject=None, thumbprint=None, type=None):
        if azure_api_version and not isinstance(azure_api_version, str):
            raise TypeError("Expected argument 'azure_api_version' to be a str")
        pulumi.set(__self__, "azure_api_version", azure_api_version)
        if expiration_date and not isinstance(expiration_date, str):
            raise TypeError("Expected argument 'expiration_date' to be a str")
        pulumi.set(__self__, "expiration_date", expiration_date)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if key_vault and not isinstance(key_vault, dict):
            raise TypeError("Expected argument 'key_vault' to be a dict")
        pulumi.set(__self__, "key_vault", key_vault)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if subject and not isinstance(subject, str):
            raise TypeError("Expected argument 'subject' to be a str")
        pulumi.set(__self__, "subject", subject)
        if thumbprint and not isinstance(thumbprint, str):
            raise TypeError("Expected argument 'thumbprint' to be a str")
        pulumi.set(__self__, "thumbprint", thumbprint)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="azureApiVersion")
    def azure_api_version(self) -> builtins.str:
        """
        The Azure API version of the resource.
        """
        return pulumi.get(self, "azure_api_version")

    @property
    @pulumi.getter(name="expirationDate")
    def expiration_date(self) -> builtins.str:
        """
        Expiration date of the certificate. The date conforms to the following format: `yyyy-MM-ddTHH:mm:ssZ` as specified by the ISO 8601 standard.
        """
        return pulumi.get(self, "expiration_date")

    @property
    @pulumi.getter
    def id(self) -> builtins.str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="keyVault")
    def key_vault(self) -> Optional['outputs.KeyVaultContractPropertiesResponse']:
        """
        KeyVault location details of the certificate.
        """
        return pulumi.get(self, "key_vault")

    @property
    @pulumi.getter
    def name(self) -> builtins.str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def subject(self) -> builtins.str:
        """
        Subject attribute of the certificate.
        """
        return pulumi.get(self, "subject")

    @property
    @pulumi.getter
    def thumbprint(self) -> builtins.str:
        """
        Thumbprint of the certificate.
        """
        return pulumi.get(self, "thumbprint")

    @property
    @pulumi.getter
    def type(self) -> builtins.str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetCertificateResult(GetCertificateResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCertificateResult(
            azure_api_version=self.azure_api_version,
            expiration_date=self.expiration_date,
            id=self.id,
            key_vault=self.key_vault,
            name=self.name,
            subject=self.subject,
            thumbprint=self.thumbprint,
            type=self.type)


def get_certificate(certificate_id: Optional[builtins.str] = None,
                    resource_group_name: Optional[builtins.str] = None,
                    service_name: Optional[builtins.str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCertificateResult:
    """
    Gets the details of the certificate specified by its identifier.

    Uses Azure REST API version 2022-09-01-preview.

    Other available API versions: 2021-04-01-preview, 2021-08-01, 2021-12-01-preview, 2022-04-01-preview, 2022-08-01, 2023-03-01-preview, 2023-05-01-preview, 2023-09-01-preview, 2024-05-01, 2024-06-01-preview. These can be accessed by generating a local SDK package using the CLI command `pulumi package add azure-native apimanagement [ApiVersion]`. See the [version guide](../../../version-guide/#accessing-any-api-version-via-local-packages) for details.


    :param builtins.str certificate_id: Identifier of the certificate entity. Must be unique in the current API Management service instance.
    :param builtins.str resource_group_name: The name of the resource group. The name is case insensitive.
    :param builtins.str service_name: The name of the API Management service.
    """
    __args__ = dict()
    __args__['certificateId'] = certificate_id
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:apimanagement:getCertificate', __args__, opts=opts, typ=GetCertificateResult).value

    return AwaitableGetCertificateResult(
        azure_api_version=pulumi.get(__ret__, 'azure_api_version'),
        expiration_date=pulumi.get(__ret__, 'expiration_date'),
        id=pulumi.get(__ret__, 'id'),
        key_vault=pulumi.get(__ret__, 'key_vault'),
        name=pulumi.get(__ret__, 'name'),
        subject=pulumi.get(__ret__, 'subject'),
        thumbprint=pulumi.get(__ret__, 'thumbprint'),
        type=pulumi.get(__ret__, 'type'))
def get_certificate_output(certificate_id: Optional[pulumi.Input[builtins.str]] = None,
                           resource_group_name: Optional[pulumi.Input[builtins.str]] = None,
                           service_name: Optional[pulumi.Input[builtins.str]] = None,
                           opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetCertificateResult]:
    """
    Gets the details of the certificate specified by its identifier.

    Uses Azure REST API version 2022-09-01-preview.

    Other available API versions: 2021-04-01-preview, 2021-08-01, 2021-12-01-preview, 2022-04-01-preview, 2022-08-01, 2023-03-01-preview, 2023-05-01-preview, 2023-09-01-preview, 2024-05-01, 2024-06-01-preview. These can be accessed by generating a local SDK package using the CLI command `pulumi package add azure-native apimanagement [ApiVersion]`. See the [version guide](../../../version-guide/#accessing-any-api-version-via-local-packages) for details.


    :param builtins.str certificate_id: Identifier of the certificate entity. Must be unique in the current API Management service instance.
    :param builtins.str resource_group_name: The name of the resource group. The name is case insensitive.
    :param builtins.str service_name: The name of the API Management service.
    """
    __args__ = dict()
    __args__['certificateId'] = certificate_id
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure-native:apimanagement:getCertificate', __args__, opts=opts, typ=GetCertificateResult)
    return __ret__.apply(lambda __response__: GetCertificateResult(
        azure_api_version=pulumi.get(__response__, 'azure_api_version'),
        expiration_date=pulumi.get(__response__, 'expiration_date'),
        id=pulumi.get(__response__, 'id'),
        key_vault=pulumi.get(__response__, 'key_vault'),
        name=pulumi.get(__response__, 'name'),
        subject=pulumi.get(__response__, 'subject'),
        thumbprint=pulumi.get(__response__, 'thumbprint'),
        type=pulumi.get(__response__, 'type')))
