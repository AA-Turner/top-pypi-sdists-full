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
    'GetFluidRelayServerResult',
    'AwaitableGetFluidRelayServerResult',
    'get_fluid_relay_server',
    'get_fluid_relay_server_output',
]

@pulumi.output_type
class GetFluidRelayServerResult:
    """
    A FluidRelay Server.
    """
    def __init__(__self__, azure_api_version=None, encryption=None, fluid_relay_endpoints=None, frs_tenant_id=None, id=None, identity=None, location=None, name=None, provisioning_state=None, storagesku=None, system_data=None, tags=None, type=None):
        if azure_api_version and not isinstance(azure_api_version, str):
            raise TypeError("Expected argument 'azure_api_version' to be a str")
        pulumi.set(__self__, "azure_api_version", azure_api_version)
        if encryption and not isinstance(encryption, dict):
            raise TypeError("Expected argument 'encryption' to be a dict")
        pulumi.set(__self__, "encryption", encryption)
        if fluid_relay_endpoints and not isinstance(fluid_relay_endpoints, dict):
            raise TypeError("Expected argument 'fluid_relay_endpoints' to be a dict")
        pulumi.set(__self__, "fluid_relay_endpoints", fluid_relay_endpoints)
        if frs_tenant_id and not isinstance(frs_tenant_id, str):
            raise TypeError("Expected argument 'frs_tenant_id' to be a str")
        pulumi.set(__self__, "frs_tenant_id", frs_tenant_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if storagesku and not isinstance(storagesku, str):
            raise TypeError("Expected argument 'storagesku' to be a str")
        pulumi.set(__self__, "storagesku", storagesku)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
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
    @pulumi.getter
    def encryption(self) -> Optional['outputs.EncryptionPropertiesResponse']:
        """
        All encryption configuration for a resource.
        """
        return pulumi.get(self, "encryption")

    @property
    @pulumi.getter(name="fluidRelayEndpoints")
    def fluid_relay_endpoints(self) -> 'outputs.FluidRelayEndpointsResponse':
        """
        The Fluid Relay Service endpoints for this server.
        """
        return pulumi.get(self, "fluid_relay_endpoints")

    @property
    @pulumi.getter(name="frsTenantId")
    def frs_tenant_id(self) -> builtins.str:
        """
        The Fluid tenantId for this server
        """
        return pulumi.get(self, "frs_tenant_id")

    @property
    @pulumi.getter
    def id(self) -> builtins.str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.IdentityResponse']:
        """
        The type of identity used for the resource.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> builtins.str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> builtins.str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[builtins.str]:
        """
        Provision states for FluidRelay RP
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def storagesku(self) -> Optional[builtins.str]:
        """
        Sku of the storage associated with the resource
        """
        return pulumi.get(self, "storagesku")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        System meta data for this resource, including creation and modification information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, builtins.str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> builtins.str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetFluidRelayServerResult(GetFluidRelayServerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFluidRelayServerResult(
            azure_api_version=self.azure_api_version,
            encryption=self.encryption,
            fluid_relay_endpoints=self.fluid_relay_endpoints,
            frs_tenant_id=self.frs_tenant_id,
            id=self.id,
            identity=self.identity,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            storagesku=self.storagesku,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_fluid_relay_server(fluid_relay_server_name: Optional[builtins.str] = None,
                           resource_group: Optional[builtins.str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFluidRelayServerResult:
    """
    A FluidRelay Server.

    Uses Azure REST API version 2022-06-01.


    :param builtins.str fluid_relay_server_name: The Fluid Relay server resource name.
    :param builtins.str resource_group: The resource group containing the resource.
    """
    __args__ = dict()
    __args__['fluidRelayServerName'] = fluid_relay_server_name
    __args__['resourceGroup'] = resource_group
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:fluidrelay:getFluidRelayServer', __args__, opts=opts, typ=GetFluidRelayServerResult).value

    return AwaitableGetFluidRelayServerResult(
        azure_api_version=pulumi.get(__ret__, 'azure_api_version'),
        encryption=pulumi.get(__ret__, 'encryption'),
        fluid_relay_endpoints=pulumi.get(__ret__, 'fluid_relay_endpoints'),
        frs_tenant_id=pulumi.get(__ret__, 'frs_tenant_id'),
        id=pulumi.get(__ret__, 'id'),
        identity=pulumi.get(__ret__, 'identity'),
        location=pulumi.get(__ret__, 'location'),
        name=pulumi.get(__ret__, 'name'),
        provisioning_state=pulumi.get(__ret__, 'provisioning_state'),
        storagesku=pulumi.get(__ret__, 'storagesku'),
        system_data=pulumi.get(__ret__, 'system_data'),
        tags=pulumi.get(__ret__, 'tags'),
        type=pulumi.get(__ret__, 'type'))
def get_fluid_relay_server_output(fluid_relay_server_name: Optional[pulumi.Input[builtins.str]] = None,
                                  resource_group: Optional[pulumi.Input[builtins.str]] = None,
                                  opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetFluidRelayServerResult]:
    """
    A FluidRelay Server.

    Uses Azure REST API version 2022-06-01.


    :param builtins.str fluid_relay_server_name: The Fluid Relay server resource name.
    :param builtins.str resource_group: The resource group containing the resource.
    """
    __args__ = dict()
    __args__['fluidRelayServerName'] = fluid_relay_server_name
    __args__['resourceGroup'] = resource_group
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('azure-native:fluidrelay:getFluidRelayServer', __args__, opts=opts, typ=GetFluidRelayServerResult)
    return __ret__.apply(lambda __response__: GetFluidRelayServerResult(
        azure_api_version=pulumi.get(__response__, 'azure_api_version'),
        encryption=pulumi.get(__response__, 'encryption'),
        fluid_relay_endpoints=pulumi.get(__response__, 'fluid_relay_endpoints'),
        frs_tenant_id=pulumi.get(__response__, 'frs_tenant_id'),
        id=pulumi.get(__response__, 'id'),
        identity=pulumi.get(__response__, 'identity'),
        location=pulumi.get(__response__, 'location'),
        name=pulumi.get(__response__, 'name'),
        provisioning_state=pulumi.get(__response__, 'provisioning_state'),
        storagesku=pulumi.get(__response__, 'storagesku'),
        system_data=pulumi.get(__response__, 'system_data'),
        tags=pulumi.get(__response__, 'tags'),
        type=pulumi.get(__response__, 'type')))
