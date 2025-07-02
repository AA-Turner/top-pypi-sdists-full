r'''
# `azurerm_workloads_sap_three_tier_virtual_instance`

Refer to the Terraform Registry for docs: [`azurerm_workloads_sap_three_tier_virtual_instance`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class WorkloadsSapThreeTierVirtualInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance azurerm_workloads_sap_three_tier_virtual_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        app_location: builtins.str,
        environment: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sap_fqdn: builtins.str,
        sap_product: builtins.str,
        three_tier_configuration: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_resource_group_name: typing.Optional[builtins.str] = None,
        managed_resources_network_access_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance azurerm_workloads_sap_three_tier_virtual_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param app_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#app_location WorkloadsSapThreeTierVirtualInstance#app_location}.
        :param environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#environment WorkloadsSapThreeTierVirtualInstance#environment}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#location WorkloadsSapThreeTierVirtualInstance#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#name WorkloadsSapThreeTierVirtualInstance#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#resource_group_name WorkloadsSapThreeTierVirtualInstance#resource_group_name}.
        :param sap_fqdn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#sap_fqdn WorkloadsSapThreeTierVirtualInstance#sap_fqdn}.
        :param sap_product: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#sap_product WorkloadsSapThreeTierVirtualInstance#sap_product}.
        :param three_tier_configuration: three_tier_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#three_tier_configuration WorkloadsSapThreeTierVirtualInstance#three_tier_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#id WorkloadsSapThreeTierVirtualInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#identity WorkloadsSapThreeTierVirtualInstance#identity}
        :param managed_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#managed_resource_group_name WorkloadsSapThreeTierVirtualInstance#managed_resource_group_name}.
        :param managed_resources_network_access_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#managed_resources_network_access_type WorkloadsSapThreeTierVirtualInstance#managed_resources_network_access_type}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#tags WorkloadsSapThreeTierVirtualInstance#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#timeouts WorkloadsSapThreeTierVirtualInstance#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdfa6a36d5f8d2cda30ef1b557a6010e16aa4c0b0f0e51fc0d2386e07f78cfa7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WorkloadsSapThreeTierVirtualInstanceConfig(
            app_location=app_location,
            environment=environment,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            sap_fqdn=sap_fqdn,
            sap_product=sap_product,
            three_tier_configuration=three_tier_configuration,
            id=id,
            identity=identity,
            managed_resource_group_name=managed_resource_group_name,
            managed_resources_network_access_type=managed_resources_network_access_type,
            tags=tags,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a WorkloadsSapThreeTierVirtualInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WorkloadsSapThreeTierVirtualInstance to import.
        :param import_from_id: The id of the existing WorkloadsSapThreeTierVirtualInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WorkloadsSapThreeTierVirtualInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b14bde042042bb6fc23832c3873ff2dc0279656b6857951b716964050215d4c0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        identity_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#identity_ids WorkloadsSapThreeTierVirtualInstance#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#type WorkloadsSapThreeTierVirtualInstance#type}.
        '''
        value = WorkloadsSapThreeTierVirtualInstanceIdentity(
            identity_ids=identity_ids, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putThreeTierConfiguration")
    def put_three_tier_configuration(
        self,
        *,
        application_server_configuration: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfiguration", typing.Dict[builtins.str, typing.Any]],
        app_resource_group_name: builtins.str,
        central_server_configuration: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfiguration", typing.Dict[builtins.str, typing.Any]],
        database_server_configuration: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfiguration", typing.Dict[builtins.str, typing.Any]],
        high_availability_type: typing.Optional[builtins.str] = None,
        resource_names: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNames", typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transport_create_and_mount: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMount", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param application_server_configuration: application_server_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#application_server_configuration WorkloadsSapThreeTierVirtualInstance#application_server_configuration}
        :param app_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#app_resource_group_name WorkloadsSapThreeTierVirtualInstance#app_resource_group_name}.
        :param central_server_configuration: central_server_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#central_server_configuration WorkloadsSapThreeTierVirtualInstance#central_server_configuration}
        :param database_server_configuration: database_server_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#database_server_configuration WorkloadsSapThreeTierVirtualInstance#database_server_configuration}
        :param high_availability_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#high_availability_type WorkloadsSapThreeTierVirtualInstance#high_availability_type}.
        :param resource_names: resource_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#resource_names WorkloadsSapThreeTierVirtualInstance#resource_names}
        :param secondary_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#secondary_ip_enabled WorkloadsSapThreeTierVirtualInstance#secondary_ip_enabled}.
        :param transport_create_and_mount: transport_create_and_mount block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#transport_create_and_mount WorkloadsSapThreeTierVirtualInstance#transport_create_and_mount}
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration(
            application_server_configuration=application_server_configuration,
            app_resource_group_name=app_resource_group_name,
            central_server_configuration=central_server_configuration,
            database_server_configuration=database_server_configuration,
            high_availability_type=high_availability_type,
            resource_names=resource_names,
            secondary_ip_enabled=secondary_ip_enabled,
            transport_create_and_mount=transport_create_and_mount,
        )

        return typing.cast(None, jsii.invoke(self, "putThreeTierConfiguration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#create WorkloadsSapThreeTierVirtualInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#delete WorkloadsSapThreeTierVirtualInstance#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#read WorkloadsSapThreeTierVirtualInstance#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#update WorkloadsSapThreeTierVirtualInstance#update}.
        '''
        value = WorkloadsSapThreeTierVirtualInstanceTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetManagedResourceGroupName")
    def reset_managed_resource_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedResourceGroupName", []))

    @jsii.member(jsii_name="resetManagedResourcesNetworkAccessType")
    def reset_managed_resources_network_access_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedResourcesNetworkAccessType", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "WorkloadsSapThreeTierVirtualInstanceIdentityOutputReference":
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="threeTierConfiguration")
    def three_tier_configuration(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationOutputReference":
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationOutputReference", jsii.get(self, "threeTierConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "WorkloadsSapThreeTierVirtualInstanceTimeoutsOutputReference":
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="appLocationInput")
    def app_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceIdentity"]:
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="managedResourceGroupNameInput")
    def managed_resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedResourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="managedResourcesNetworkAccessTypeInput")
    def managed_resources_network_access_type_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedResourcesNetworkAccessTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sapFqdnInput")
    def sap_fqdn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sapFqdnInput"))

    @builtins.property
    @jsii.member(jsii_name="sapProductInput")
    def sap_product_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sapProductInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="threeTierConfigurationInput")
    def three_tier_configuration_input(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration"]:
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration"], jsii.get(self, "threeTierConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WorkloadsSapThreeTierVirtualInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WorkloadsSapThreeTierVirtualInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="appLocation")
    def app_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appLocation"))

    @app_location.setter
    def app_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__777076b8675f505bab929a97108bb7d6388d9d615667bdadddedd40e58c516c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1000b5ea13668428dff1bef7f42ede145884ca26b28578eea387d1d463793285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__069022931f64f8d41dd5a5d35f69022936511b252643ded9b8288aa23a8dc6da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df926a48687fcf0f12cbc7605356740e04bccbfaf1e28d70bd814545908423e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedResourceGroupName")
    def managed_resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedResourceGroupName"))

    @managed_resource_group_name.setter
    def managed_resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef2131e6fd64917c3728439f764cddaa8f1543afd0900501d5d8385f77a8e336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedResourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedResourcesNetworkAccessType")
    def managed_resources_network_access_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedResourcesNetworkAccessType"))

    @managed_resources_network_access_type.setter
    def managed_resources_network_access_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__effb27f016d632165c6c988c09ea4f43007c981bff6b8494239475a04b025a94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedResourcesNetworkAccessType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864034fe0389ed0ddf828a90e7d5c3692f02d75a8df31139404f44671f374dab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4949909849e91d387643c8f4410df8b9de1260e81f95007475d6ca9b82672aea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sapFqdn")
    def sap_fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sapFqdn"))

    @sap_fqdn.setter
    def sap_fqdn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02675678340ffd85856cf59ec490b15f9528e0f1416bf19bab08b134223f5580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sapFqdn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sapProduct")
    def sap_product(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sapProduct"))

    @sap_product.setter
    def sap_product(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5615ee020c3a87341f20b66566040c9739d981398f6a668fd35d69bfaa486d4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sapProduct", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83dcc9356073839721301df57d30436b3304f37f6b5bf2830fb4b99b05c50108)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "app_location": "appLocation",
        "environment": "environment",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "sap_fqdn": "sapFqdn",
        "sap_product": "sapProduct",
        "three_tier_configuration": "threeTierConfiguration",
        "id": "id",
        "identity": "identity",
        "managed_resource_group_name": "managedResourceGroupName",
        "managed_resources_network_access_type": "managedResourcesNetworkAccessType",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class WorkloadsSapThreeTierVirtualInstanceConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        app_location: builtins.str,
        environment: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sap_fqdn: builtins.str,
        sap_product: builtins.str,
        three_tier_configuration: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_resource_group_name: typing.Optional[builtins.str] = None,
        managed_resources_network_access_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param app_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#app_location WorkloadsSapThreeTierVirtualInstance#app_location}.
        :param environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#environment WorkloadsSapThreeTierVirtualInstance#environment}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#location WorkloadsSapThreeTierVirtualInstance#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#name WorkloadsSapThreeTierVirtualInstance#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#resource_group_name WorkloadsSapThreeTierVirtualInstance#resource_group_name}.
        :param sap_fqdn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#sap_fqdn WorkloadsSapThreeTierVirtualInstance#sap_fqdn}.
        :param sap_product: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#sap_product WorkloadsSapThreeTierVirtualInstance#sap_product}.
        :param three_tier_configuration: three_tier_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#three_tier_configuration WorkloadsSapThreeTierVirtualInstance#three_tier_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#id WorkloadsSapThreeTierVirtualInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#identity WorkloadsSapThreeTierVirtualInstance#identity}
        :param managed_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#managed_resource_group_name WorkloadsSapThreeTierVirtualInstance#managed_resource_group_name}.
        :param managed_resources_network_access_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#managed_resources_network_access_type WorkloadsSapThreeTierVirtualInstance#managed_resources_network_access_type}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#tags WorkloadsSapThreeTierVirtualInstance#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#timeouts WorkloadsSapThreeTierVirtualInstance#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(three_tier_configuration, dict):
            three_tier_configuration = WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration(**three_tier_configuration)
        if isinstance(identity, dict):
            identity = WorkloadsSapThreeTierVirtualInstanceIdentity(**identity)
        if isinstance(timeouts, dict):
            timeouts = WorkloadsSapThreeTierVirtualInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63d8db2f9430a436f6c93dac43ef08a712adea1b9630f8a9b56e9e8ddf043cad)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument app_location", value=app_location, expected_type=type_hints["app_location"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument sap_fqdn", value=sap_fqdn, expected_type=type_hints["sap_fqdn"])
            check_type(argname="argument sap_product", value=sap_product, expected_type=type_hints["sap_product"])
            check_type(argname="argument three_tier_configuration", value=three_tier_configuration, expected_type=type_hints["three_tier_configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument managed_resource_group_name", value=managed_resource_group_name, expected_type=type_hints["managed_resource_group_name"])
            check_type(argname="argument managed_resources_network_access_type", value=managed_resources_network_access_type, expected_type=type_hints["managed_resources_network_access_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_location": app_location,
            "environment": environment,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "sap_fqdn": sap_fqdn,
            "sap_product": sap_product,
            "three_tier_configuration": three_tier_configuration,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if managed_resource_group_name is not None:
            self._values["managed_resource_group_name"] = managed_resource_group_name
        if managed_resources_network_access_type is not None:
            self._values["managed_resources_network_access_type"] = managed_resources_network_access_type
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def app_location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#app_location WorkloadsSapThreeTierVirtualInstance#app_location}.'''
        result = self._values.get("app_location")
        assert result is not None, "Required property 'app_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#environment WorkloadsSapThreeTierVirtualInstance#environment}.'''
        result = self._values.get("environment")
        assert result is not None, "Required property 'environment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#location WorkloadsSapThreeTierVirtualInstance#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#name WorkloadsSapThreeTierVirtualInstance#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#resource_group_name WorkloadsSapThreeTierVirtualInstance#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sap_fqdn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#sap_fqdn WorkloadsSapThreeTierVirtualInstance#sap_fqdn}.'''
        result = self._values.get("sap_fqdn")
        assert result is not None, "Required property 'sap_fqdn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sap_product(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#sap_product WorkloadsSapThreeTierVirtualInstance#sap_product}.'''
        result = self._values.get("sap_product")
        assert result is not None, "Required property 'sap_product' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def three_tier_configuration(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration":
        '''three_tier_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#three_tier_configuration WorkloadsSapThreeTierVirtualInstance#three_tier_configuration}
        '''
        result = self._values.get("three_tier_configuration")
        assert result is not None, "Required property 'three_tier_configuration' is missing"
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#id WorkloadsSapThreeTierVirtualInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#identity WorkloadsSapThreeTierVirtualInstance#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceIdentity"], result)

    @builtins.property
    def managed_resource_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#managed_resource_group_name WorkloadsSapThreeTierVirtualInstance#managed_resource_group_name}.'''
        result = self._values.get("managed_resource_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_resources_network_access_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#managed_resources_network_access_type WorkloadsSapThreeTierVirtualInstance#managed_resources_network_access_type}.'''
        result = self._values.get("managed_resources_network_access_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#tags WorkloadsSapThreeTierVirtualInstance#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#timeouts WorkloadsSapThreeTierVirtualInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceIdentity",
    jsii_struct_bases=[],
    name_mapping={"identity_ids": "identityIds", "type": "type"},
)
class WorkloadsSapThreeTierVirtualInstanceIdentity:
    def __init__(
        self,
        *,
        identity_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#identity_ids WorkloadsSapThreeTierVirtualInstance#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#type WorkloadsSapThreeTierVirtualInstance#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2971667f78cf95069a3d81fc41eb69163f3074e9a9c688f13874e903f0e8408c)
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identity_ids": identity_ids,
            "type": type,
        }

    @builtins.property
    def identity_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#identity_ids WorkloadsSapThreeTierVirtualInstance#identity_ids}.'''
        result = self._values.get("identity_ids")
        assert result is not None, "Required property 'identity_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#type WorkloadsSapThreeTierVirtualInstance#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceIdentityOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4db8214a84892969b6a5517a3124985345fce6987f12e5395620ec012c6197e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="identityIdsInput")
    def identity_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identityIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @identity_ids.setter
    def identity_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0790a469ec4ee0002b4118747c217652fe4b60265e8c095b12f726066904e1b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5843d15afe0e2d7a0da19fa147d31b6ce18769922654efbed5bd85461ed13568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceIdentity]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79b8ec70276e31466bf4b4f52a8af77b04abce61dccd4dc1fb35c83d9a0ce7de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "application_server_configuration": "applicationServerConfiguration",
        "app_resource_group_name": "appResourceGroupName",
        "central_server_configuration": "centralServerConfiguration",
        "database_server_configuration": "databaseServerConfiguration",
        "high_availability_type": "highAvailabilityType",
        "resource_names": "resourceNames",
        "secondary_ip_enabled": "secondaryIpEnabled",
        "transport_create_and_mount": "transportCreateAndMount",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration:
    def __init__(
        self,
        *,
        application_server_configuration: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfiguration", typing.Dict[builtins.str, typing.Any]],
        app_resource_group_name: builtins.str,
        central_server_configuration: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfiguration", typing.Dict[builtins.str, typing.Any]],
        database_server_configuration: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfiguration", typing.Dict[builtins.str, typing.Any]],
        high_availability_type: typing.Optional[builtins.str] = None,
        resource_names: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNames", typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transport_create_and_mount: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMount", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param application_server_configuration: application_server_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#application_server_configuration WorkloadsSapThreeTierVirtualInstance#application_server_configuration}
        :param app_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#app_resource_group_name WorkloadsSapThreeTierVirtualInstance#app_resource_group_name}.
        :param central_server_configuration: central_server_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#central_server_configuration WorkloadsSapThreeTierVirtualInstance#central_server_configuration}
        :param database_server_configuration: database_server_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#database_server_configuration WorkloadsSapThreeTierVirtualInstance#database_server_configuration}
        :param high_availability_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#high_availability_type WorkloadsSapThreeTierVirtualInstance#high_availability_type}.
        :param resource_names: resource_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#resource_names WorkloadsSapThreeTierVirtualInstance#resource_names}
        :param secondary_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#secondary_ip_enabled WorkloadsSapThreeTierVirtualInstance#secondary_ip_enabled}.
        :param transport_create_and_mount: transport_create_and_mount block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#transport_create_and_mount WorkloadsSapThreeTierVirtualInstance#transport_create_and_mount}
        '''
        if isinstance(application_server_configuration, dict):
            application_server_configuration = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfiguration(**application_server_configuration)
        if isinstance(central_server_configuration, dict):
            central_server_configuration = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfiguration(**central_server_configuration)
        if isinstance(database_server_configuration, dict):
            database_server_configuration = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfiguration(**database_server_configuration)
        if isinstance(resource_names, dict):
            resource_names = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNames(**resource_names)
        if isinstance(transport_create_and_mount, dict):
            transport_create_and_mount = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMount(**transport_create_and_mount)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e44b46aef0eb9bcf1f19334d1ab3c3f7324dd13fa24d1e5b1dbd67351dfee1a)
            check_type(argname="argument application_server_configuration", value=application_server_configuration, expected_type=type_hints["application_server_configuration"])
            check_type(argname="argument app_resource_group_name", value=app_resource_group_name, expected_type=type_hints["app_resource_group_name"])
            check_type(argname="argument central_server_configuration", value=central_server_configuration, expected_type=type_hints["central_server_configuration"])
            check_type(argname="argument database_server_configuration", value=database_server_configuration, expected_type=type_hints["database_server_configuration"])
            check_type(argname="argument high_availability_type", value=high_availability_type, expected_type=type_hints["high_availability_type"])
            check_type(argname="argument resource_names", value=resource_names, expected_type=type_hints["resource_names"])
            check_type(argname="argument secondary_ip_enabled", value=secondary_ip_enabled, expected_type=type_hints["secondary_ip_enabled"])
            check_type(argname="argument transport_create_and_mount", value=transport_create_and_mount, expected_type=type_hints["transport_create_and_mount"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_server_configuration": application_server_configuration,
            "app_resource_group_name": app_resource_group_name,
            "central_server_configuration": central_server_configuration,
            "database_server_configuration": database_server_configuration,
        }
        if high_availability_type is not None:
            self._values["high_availability_type"] = high_availability_type
        if resource_names is not None:
            self._values["resource_names"] = resource_names
        if secondary_ip_enabled is not None:
            self._values["secondary_ip_enabled"] = secondary_ip_enabled
        if transport_create_and_mount is not None:
            self._values["transport_create_and_mount"] = transport_create_and_mount

    @builtins.property
    def application_server_configuration(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfiguration":
        '''application_server_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#application_server_configuration WorkloadsSapThreeTierVirtualInstance#application_server_configuration}
        '''
        result = self._values.get("application_server_configuration")
        assert result is not None, "Required property 'application_server_configuration' is missing"
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfiguration", result)

    @builtins.property
    def app_resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#app_resource_group_name WorkloadsSapThreeTierVirtualInstance#app_resource_group_name}.'''
        result = self._values.get("app_resource_group_name")
        assert result is not None, "Required property 'app_resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def central_server_configuration(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfiguration":
        '''central_server_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#central_server_configuration WorkloadsSapThreeTierVirtualInstance#central_server_configuration}
        '''
        result = self._values.get("central_server_configuration")
        assert result is not None, "Required property 'central_server_configuration' is missing"
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfiguration", result)

    @builtins.property
    def database_server_configuration(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfiguration":
        '''database_server_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#database_server_configuration WorkloadsSapThreeTierVirtualInstance#database_server_configuration}
        '''
        result = self._values.get("database_server_configuration")
        assert result is not None, "Required property 'database_server_configuration' is missing"
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfiguration", result)

    @builtins.property
    def high_availability_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#high_availability_type WorkloadsSapThreeTierVirtualInstance#high_availability_type}.'''
        result = self._values.get("high_availability_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_names(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNames"]:
        '''resource_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#resource_names WorkloadsSapThreeTierVirtualInstance#resource_names}
        '''
        result = self._values.get("resource_names")
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNames"], result)

    @builtins.property
    def secondary_ip_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#secondary_ip_enabled WorkloadsSapThreeTierVirtualInstance#secondary_ip_enabled}.'''
        result = self._values.get("secondary_ip_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transport_create_and_mount(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMount"]:
        '''transport_create_and_mount block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#transport_create_and_mount WorkloadsSapThreeTierVirtualInstance#transport_create_and_mount}
        '''
        result = self._values.get("transport_create_and_mount")
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMount"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "instance_count": "instanceCount",
        "subnet_id": "subnetId",
        "virtual_machine_configuration": "virtualMachineConfiguration",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfiguration:
    def __init__(
        self,
        *,
        instance_count: jsii.Number,
        subnet_id: builtins.str,
        virtual_machine_configuration: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfiguration", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#instance_count WorkloadsSapThreeTierVirtualInstance#instance_count}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#subnet_id WorkloadsSapThreeTierVirtualInstance#subnet_id}.
        :param virtual_machine_configuration: virtual_machine_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_configuration WorkloadsSapThreeTierVirtualInstance#virtual_machine_configuration}
        '''
        if isinstance(virtual_machine_configuration, dict):
            virtual_machine_configuration = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfiguration(**virtual_machine_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f76b5d01e374c8aa2d1e18a7ba17618a52b09f72d2fc532f0f1214c003ac7729)
            check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument virtual_machine_configuration", value=virtual_machine_configuration, expected_type=type_hints["virtual_machine_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_count": instance_count,
            "subnet_id": subnet_id,
            "virtual_machine_configuration": virtual_machine_configuration,
        }

    @builtins.property
    def instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#instance_count WorkloadsSapThreeTierVirtualInstance#instance_count}.'''
        result = self._values.get("instance_count")
        assert result is not None, "Required property 'instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#subnet_id WorkloadsSapThreeTierVirtualInstance#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_machine_configuration(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfiguration":
        '''virtual_machine_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_configuration WorkloadsSapThreeTierVirtualInstance#virtual_machine_configuration}
        '''
        result = self._values.get("virtual_machine_configuration")
        assert result is not None, "Required property 'virtual_machine_configuration' is missing"
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfiguration", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f28581289a979d5ee48367a44e6923d03bc3042bb509b8a3b9b2ec2d741bb71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVirtualMachineConfiguration")
    def put_virtual_machine_configuration(
        self,
        *,
        image: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImage", typing.Dict[builtins.str, typing.Any]],
        os_profile: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfile", typing.Dict[builtins.str, typing.Any]],
        virtual_machine_size: builtins.str,
    ) -> None:
        '''
        :param image: image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#image WorkloadsSapThreeTierVirtualInstance#image}
        :param os_profile: os_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#os_profile WorkloadsSapThreeTierVirtualInstance#os_profile}
        :param virtual_machine_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_size WorkloadsSapThreeTierVirtualInstance#virtual_machine_size}.
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfiguration(
            image=image,
            os_profile=os_profile,
            virtual_machine_size=virtual_machine_size,
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualMachineConfiguration", [value]))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineConfiguration")
    def virtual_machine_configuration(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOutputReference":
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOutputReference", jsii.get(self, "virtualMachineConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="instanceCountInput")
    def instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineConfigurationInput")
    def virtual_machine_configuration_input(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfiguration"]:
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfiguration"], jsii.get(self, "virtualMachineConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceCount")
    def instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instanceCount"))

    @instance_count.setter
    def instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9afe951b50b3c606a62b956c6ecb7fde51fd1227590a30f444c4f9feae579433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e70f05a0bda28a3eda634a97d896d3f5e0f4ff2750537be780b4af0c6b22e86f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfiguration]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631b6094af24bb7ce29d92b871121ad284e4fed69de6fffdc327f0005004bf40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "os_profile": "osProfile",
        "virtual_machine_size": "virtualMachineSize",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfiguration:
    def __init__(
        self,
        *,
        image: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImage", typing.Dict[builtins.str, typing.Any]],
        os_profile: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfile", typing.Dict[builtins.str, typing.Any]],
        virtual_machine_size: builtins.str,
    ) -> None:
        '''
        :param image: image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#image WorkloadsSapThreeTierVirtualInstance#image}
        :param os_profile: os_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#os_profile WorkloadsSapThreeTierVirtualInstance#os_profile}
        :param virtual_machine_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_size WorkloadsSapThreeTierVirtualInstance#virtual_machine_size}.
        '''
        if isinstance(image, dict):
            image = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImage(**image)
        if isinstance(os_profile, dict):
            os_profile = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfile(**os_profile)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__263abe3b6ddcb87ad0ef510aec101d5ed51dd8c8e503386f0780a68392303d84)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument os_profile", value=os_profile, expected_type=type_hints["os_profile"])
            check_type(argname="argument virtual_machine_size", value=virtual_machine_size, expected_type=type_hints["virtual_machine_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
            "os_profile": os_profile,
            "virtual_machine_size": virtual_machine_size,
        }

    @builtins.property
    def image(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImage":
        '''image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#image WorkloadsSapThreeTierVirtualInstance#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImage", result)

    @builtins.property
    def os_profile(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfile":
        '''os_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#os_profile WorkloadsSapThreeTierVirtualInstance#os_profile}
        '''
        result = self._values.get("os_profile")
        assert result is not None, "Required property 'os_profile' is missing"
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfile", result)

    @builtins.property
    def virtual_machine_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_size WorkloadsSapThreeTierVirtualInstance#virtual_machine_size}.'''
        result = self._values.get("virtual_machine_size")
        assert result is not None, "Required property 'virtual_machine_size' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImage",
    jsii_struct_bases=[],
    name_mapping={
        "offer": "offer",
        "publisher": "publisher",
        "sku": "sku",
        "version": "version",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImage:
    def __init__(
        self,
        *,
        offer: builtins.str,
        publisher: builtins.str,
        sku: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param offer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#offer WorkloadsSapThreeTierVirtualInstance#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#publisher WorkloadsSapThreeTierVirtualInstance#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#sku WorkloadsSapThreeTierVirtualInstance#sku}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#version WorkloadsSapThreeTierVirtualInstance#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd270f98d2c7f907ba67547dbd9abf1a40c33ab33363eda624984642cee5212)
            check_type(argname="argument offer", value=offer, expected_type=type_hints["offer"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "offer": offer,
            "publisher": publisher,
            "sku": sku,
            "version": version,
        }

    @builtins.property
    def offer(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#offer WorkloadsSapThreeTierVirtualInstance#offer}.'''
        result = self._values.get("offer")
        assert result is not None, "Required property 'offer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def publisher(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#publisher WorkloadsSapThreeTierVirtualInstance#publisher}.'''
        result = self._values.get("publisher")
        assert result is not None, "Required property 'publisher' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sku(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#sku WorkloadsSapThreeTierVirtualInstance#sku}.'''
        result = self._values.get("sku")
        assert result is not None, "Required property 'sku' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#version WorkloadsSapThreeTierVirtualInstance#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImageOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e1616d97cf8956fa8b8bd5140edf05e0f8dbc9238e18604dff9b4f07e2ab56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="offerInput")
    def offer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "offerInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherInput")
    def publisher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="skuInput")
    def sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="offer")
    def offer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "offer"))

    @offer.setter
    def offer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad3e186c10f3acfb2a6deba731d08e4db52897dc3a985df77af55db858a581b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisher"))

    @publisher.setter
    def publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e8f7cf42a6c3903a6955119204f9ca64ab428cda1b375342f7e8d9abc458b56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5ae0fa021853fc77ccb30e8dfacfd130a7769d611c45827cf17a6870cacfe00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2226ebd4d902ccc6e8fd07046acf7f83e3f40f670f9d0461c2915a79cb05c199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImage]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d596ce8a6de6e6642cf1de56d3d7c0cf5a391ee81fd7ceb14a5b100692ffbd8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfile",
    jsii_struct_bases=[],
    name_mapping={
        "admin_username": "adminUsername",
        "ssh_private_key": "sshPrivateKey",
        "ssh_public_key": "sshPublicKey",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfile:
    def __init__(
        self,
        *,
        admin_username: builtins.str,
        ssh_private_key: builtins.str,
        ssh_public_key: builtins.str,
    ) -> None:
        '''
        :param admin_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#admin_username WorkloadsSapThreeTierVirtualInstance#admin_username}.
        :param ssh_private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_private_key WorkloadsSapThreeTierVirtualInstance#ssh_private_key}.
        :param ssh_public_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_public_key WorkloadsSapThreeTierVirtualInstance#ssh_public_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__107843aa13f0e9404b71d23693c15eccc03d3944216c4ce941b1995436f98f0a)
            check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
            check_type(argname="argument ssh_private_key", value=ssh_private_key, expected_type=type_hints["ssh_private_key"])
            check_type(argname="argument ssh_public_key", value=ssh_public_key, expected_type=type_hints["ssh_public_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_username": admin_username,
            "ssh_private_key": ssh_private_key,
            "ssh_public_key": ssh_public_key,
        }

    @builtins.property
    def admin_username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#admin_username WorkloadsSapThreeTierVirtualInstance#admin_username}.'''
        result = self._values.get("admin_username")
        assert result is not None, "Required property 'admin_username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssh_private_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_private_key WorkloadsSapThreeTierVirtualInstance#ssh_private_key}.'''
        result = self._values.get("ssh_private_key")
        assert result is not None, "Required property 'ssh_private_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssh_public_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_public_key WorkloadsSapThreeTierVirtualInstance#ssh_public_key}.'''
        result = self._values.get("ssh_public_key")
        assert result is not None, "Required property 'ssh_public_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfileOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fce1cdf57475cb310c5c32e7efe738c0540531102680a39e12bd674f81345044)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="adminUsernameInput")
    def admin_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPrivateKeyInput")
    def ssh_private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshPrivateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeyInput")
    def ssh_public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="adminUsername")
    def admin_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminUsername"))

    @admin_username.setter
    def admin_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f726e27d819d0cb72c6b981a305a879174e131069bde5e5c4de22b8d491f9922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPrivateKey")
    def ssh_private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshPrivateKey"))

    @ssh_private_key.setter
    def ssh_private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d266050ec4dcb85fbf66236cfad8559726483130e6a846e5f3f27f424ade21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPrivateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPublicKey")
    def ssh_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshPublicKey"))

    @ssh_public_key.setter
    def ssh_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cfd497c08e925edab0ce2723842edc464183f7952c414cb5184520858b71e1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPublicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfile]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b4873106d3b7fa979ca54e85da2299653aa4a9c86fc8d8fe847e2ae9228d0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e3c6a41dc73534b9f40728c3060a3ba9b131445f98f643bda019d27738b694f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putImage")
    def put_image(
        self,
        *,
        offer: builtins.str,
        publisher: builtins.str,
        sku: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param offer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#offer WorkloadsSapThreeTierVirtualInstance#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#publisher WorkloadsSapThreeTierVirtualInstance#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#sku WorkloadsSapThreeTierVirtualInstance#sku}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#version WorkloadsSapThreeTierVirtualInstance#version}.
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImage(
            offer=offer, publisher=publisher, sku=sku, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putImage", [value]))

    @jsii.member(jsii_name="putOsProfile")
    def put_os_profile(
        self,
        *,
        admin_username: builtins.str,
        ssh_private_key: builtins.str,
        ssh_public_key: builtins.str,
    ) -> None:
        '''
        :param admin_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#admin_username WorkloadsSapThreeTierVirtualInstance#admin_username}.
        :param ssh_private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_private_key WorkloadsSapThreeTierVirtualInstance#ssh_private_key}.
        :param ssh_public_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_public_key WorkloadsSapThreeTierVirtualInstance#ssh_public_key}.
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfile(
            admin_username=admin_username,
            ssh_private_key=ssh_private_key,
            ssh_public_key=ssh_public_key,
        )

        return typing.cast(None, jsii.invoke(self, "putOsProfile", [value]))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImageOutputReference:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImageOutputReference, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="osProfile")
    def os_profile(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfileOutputReference:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfileOutputReference, jsii.get(self, "osProfile"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImage]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImage], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="osProfileInput")
    def os_profile_input(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfile]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfile], jsii.get(self, "osProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineSizeInput")
    def virtual_machine_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualMachineSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineSize")
    def virtual_machine_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualMachineSize"))

    @virtual_machine_size.setter
    def virtual_machine_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c7dd83bf56d4dd4c3fe8b80ea2a87acf44c1a8323dfb9782c2714545cb1dd8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualMachineSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfiguration]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a0373cf71fb41def783789415246f709caf839860d361062fec05773709f819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "instance_count": "instanceCount",
        "subnet_id": "subnetId",
        "virtual_machine_configuration": "virtualMachineConfiguration",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfiguration:
    def __init__(
        self,
        *,
        instance_count: jsii.Number,
        subnet_id: builtins.str,
        virtual_machine_configuration: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfiguration", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#instance_count WorkloadsSapThreeTierVirtualInstance#instance_count}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#subnet_id WorkloadsSapThreeTierVirtualInstance#subnet_id}.
        :param virtual_machine_configuration: virtual_machine_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_configuration WorkloadsSapThreeTierVirtualInstance#virtual_machine_configuration}
        '''
        if isinstance(virtual_machine_configuration, dict):
            virtual_machine_configuration = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfiguration(**virtual_machine_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ac3dc3916ce65ade807ea54b52ee647b445dcfcec2904cdabfac7938489040)
            check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument virtual_machine_configuration", value=virtual_machine_configuration, expected_type=type_hints["virtual_machine_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_count": instance_count,
            "subnet_id": subnet_id,
            "virtual_machine_configuration": virtual_machine_configuration,
        }

    @builtins.property
    def instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#instance_count WorkloadsSapThreeTierVirtualInstance#instance_count}.'''
        result = self._values.get("instance_count")
        assert result is not None, "Required property 'instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#subnet_id WorkloadsSapThreeTierVirtualInstance#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_machine_configuration(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfiguration":
        '''virtual_machine_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_configuration WorkloadsSapThreeTierVirtualInstance#virtual_machine_configuration}
        '''
        result = self._values.get("virtual_machine_configuration")
        assert result is not None, "Required property 'virtual_machine_configuration' is missing"
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfiguration", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc838f07c76095e9aa675ab732d96d730f6709daa72dd0f68c7c3a145304465)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVirtualMachineConfiguration")
    def put_virtual_machine_configuration(
        self,
        *,
        image: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImage", typing.Dict[builtins.str, typing.Any]],
        os_profile: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfile", typing.Dict[builtins.str, typing.Any]],
        virtual_machine_size: builtins.str,
    ) -> None:
        '''
        :param image: image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#image WorkloadsSapThreeTierVirtualInstance#image}
        :param os_profile: os_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#os_profile WorkloadsSapThreeTierVirtualInstance#os_profile}
        :param virtual_machine_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_size WorkloadsSapThreeTierVirtualInstance#virtual_machine_size}.
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfiguration(
            image=image,
            os_profile=os_profile,
            virtual_machine_size=virtual_machine_size,
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualMachineConfiguration", [value]))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineConfiguration")
    def virtual_machine_configuration(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOutputReference":
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOutputReference", jsii.get(self, "virtualMachineConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="instanceCountInput")
    def instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineConfigurationInput")
    def virtual_machine_configuration_input(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfiguration"]:
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfiguration"], jsii.get(self, "virtualMachineConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceCount")
    def instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instanceCount"))

    @instance_count.setter
    def instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c65c41335778c896ead3cee941639622dfa636e1308045b683870f574cce5b00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c2fe8d8659f1d2c9536f63d5c7100235c30e7716ddae1e578da7159dd6cd6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfiguration]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1917c9ca51898019ed9bce5688e463f500a2dfbbf9de99898a4e0ed535daa02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "os_profile": "osProfile",
        "virtual_machine_size": "virtualMachineSize",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfiguration:
    def __init__(
        self,
        *,
        image: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImage", typing.Dict[builtins.str, typing.Any]],
        os_profile: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfile", typing.Dict[builtins.str, typing.Any]],
        virtual_machine_size: builtins.str,
    ) -> None:
        '''
        :param image: image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#image WorkloadsSapThreeTierVirtualInstance#image}
        :param os_profile: os_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#os_profile WorkloadsSapThreeTierVirtualInstance#os_profile}
        :param virtual_machine_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_size WorkloadsSapThreeTierVirtualInstance#virtual_machine_size}.
        '''
        if isinstance(image, dict):
            image = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImage(**image)
        if isinstance(os_profile, dict):
            os_profile = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfile(**os_profile)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d298b6b4a7cee03955caed2ce08a9cbc1e085986b7e0afd4c8e4a02ba85e2c9b)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument os_profile", value=os_profile, expected_type=type_hints["os_profile"])
            check_type(argname="argument virtual_machine_size", value=virtual_machine_size, expected_type=type_hints["virtual_machine_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
            "os_profile": os_profile,
            "virtual_machine_size": virtual_machine_size,
        }

    @builtins.property
    def image(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImage":
        '''image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#image WorkloadsSapThreeTierVirtualInstance#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImage", result)

    @builtins.property
    def os_profile(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfile":
        '''os_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#os_profile WorkloadsSapThreeTierVirtualInstance#os_profile}
        '''
        result = self._values.get("os_profile")
        assert result is not None, "Required property 'os_profile' is missing"
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfile", result)

    @builtins.property
    def virtual_machine_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_size WorkloadsSapThreeTierVirtualInstance#virtual_machine_size}.'''
        result = self._values.get("virtual_machine_size")
        assert result is not None, "Required property 'virtual_machine_size' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImage",
    jsii_struct_bases=[],
    name_mapping={
        "offer": "offer",
        "publisher": "publisher",
        "sku": "sku",
        "version": "version",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImage:
    def __init__(
        self,
        *,
        offer: builtins.str,
        publisher: builtins.str,
        sku: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param offer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#offer WorkloadsSapThreeTierVirtualInstance#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#publisher WorkloadsSapThreeTierVirtualInstance#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#sku WorkloadsSapThreeTierVirtualInstance#sku}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#version WorkloadsSapThreeTierVirtualInstance#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7945693ad1c2449011dfab442f0f94d7e46199794ee8db763930a6c982c52e9e)
            check_type(argname="argument offer", value=offer, expected_type=type_hints["offer"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "offer": offer,
            "publisher": publisher,
            "sku": sku,
            "version": version,
        }

    @builtins.property
    def offer(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#offer WorkloadsSapThreeTierVirtualInstance#offer}.'''
        result = self._values.get("offer")
        assert result is not None, "Required property 'offer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def publisher(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#publisher WorkloadsSapThreeTierVirtualInstance#publisher}.'''
        result = self._values.get("publisher")
        assert result is not None, "Required property 'publisher' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sku(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#sku WorkloadsSapThreeTierVirtualInstance#sku}.'''
        result = self._values.get("sku")
        assert result is not None, "Required property 'sku' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#version WorkloadsSapThreeTierVirtualInstance#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImageOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db893328795cfdc19bad10cbcd94798f7f00219078bb06677642b2343bd0b0ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="offerInput")
    def offer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "offerInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherInput")
    def publisher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="skuInput")
    def sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="offer")
    def offer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "offer"))

    @offer.setter
    def offer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46466264c4cc89cb60e2b233f9686e487204606b0c22fc4c92433f0739ac60f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisher"))

    @publisher.setter
    def publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4afc9d234a9d5b6e8c5d4686d36c0f21fbe79362be767d4b8adcbc7f0fb99a78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bda37e030c9452c37187cf3ea76ee67f6e3d6fee7d7f52110ab2ffab81460d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ed83c6a6779aa3e892f2f3d1c7e4bc9650c9c54ca535d0c7d74717004667b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImage]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030e5ec24ed0403d813d18fe1d7c6fa81a89d30685f069c19093e3f0bc3d878d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfile",
    jsii_struct_bases=[],
    name_mapping={
        "admin_username": "adminUsername",
        "ssh_private_key": "sshPrivateKey",
        "ssh_public_key": "sshPublicKey",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfile:
    def __init__(
        self,
        *,
        admin_username: builtins.str,
        ssh_private_key: builtins.str,
        ssh_public_key: builtins.str,
    ) -> None:
        '''
        :param admin_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#admin_username WorkloadsSapThreeTierVirtualInstance#admin_username}.
        :param ssh_private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_private_key WorkloadsSapThreeTierVirtualInstance#ssh_private_key}.
        :param ssh_public_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_public_key WorkloadsSapThreeTierVirtualInstance#ssh_public_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60d44eccfbdc56409b13a84f03467a6307553f62d106b03e7fada52856f525de)
            check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
            check_type(argname="argument ssh_private_key", value=ssh_private_key, expected_type=type_hints["ssh_private_key"])
            check_type(argname="argument ssh_public_key", value=ssh_public_key, expected_type=type_hints["ssh_public_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_username": admin_username,
            "ssh_private_key": ssh_private_key,
            "ssh_public_key": ssh_public_key,
        }

    @builtins.property
    def admin_username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#admin_username WorkloadsSapThreeTierVirtualInstance#admin_username}.'''
        result = self._values.get("admin_username")
        assert result is not None, "Required property 'admin_username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssh_private_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_private_key WorkloadsSapThreeTierVirtualInstance#ssh_private_key}.'''
        result = self._values.get("ssh_private_key")
        assert result is not None, "Required property 'ssh_private_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssh_public_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_public_key WorkloadsSapThreeTierVirtualInstance#ssh_public_key}.'''
        result = self._values.get("ssh_public_key")
        assert result is not None, "Required property 'ssh_public_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfileOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f48aec87befa5770ab8e6bdd00c931d1727284fb741c9c521b37d4f166cc7ab7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="adminUsernameInput")
    def admin_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPrivateKeyInput")
    def ssh_private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshPrivateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeyInput")
    def ssh_public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="adminUsername")
    def admin_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminUsername"))

    @admin_username.setter
    def admin_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__172613268e4f9876bf9494c3e73618460caa71f28bce9e2c938943f2b5973200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPrivateKey")
    def ssh_private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshPrivateKey"))

    @ssh_private_key.setter
    def ssh_private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e222a118902fc8ce58a7838752581d5051481ded4cb4e6ee5608c49ed75d372)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPrivateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPublicKey")
    def ssh_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshPublicKey"))

    @ssh_public_key.setter
    def ssh_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b9689ac795912193e546e286c5c320b38155afec985accbd43d142afd844e82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPublicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfile]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43e61acba2e13832a60dc8670ff4984523a765bedc80a2fbbda6aec4414542d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09e94b8c7a80db526358a713095ac3e00da1febca670f3ca67ba03941d8e0395)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putImage")
    def put_image(
        self,
        *,
        offer: builtins.str,
        publisher: builtins.str,
        sku: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param offer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#offer WorkloadsSapThreeTierVirtualInstance#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#publisher WorkloadsSapThreeTierVirtualInstance#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#sku WorkloadsSapThreeTierVirtualInstance#sku}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#version WorkloadsSapThreeTierVirtualInstance#version}.
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImage(
            offer=offer, publisher=publisher, sku=sku, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putImage", [value]))

    @jsii.member(jsii_name="putOsProfile")
    def put_os_profile(
        self,
        *,
        admin_username: builtins.str,
        ssh_private_key: builtins.str,
        ssh_public_key: builtins.str,
    ) -> None:
        '''
        :param admin_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#admin_username WorkloadsSapThreeTierVirtualInstance#admin_username}.
        :param ssh_private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_private_key WorkloadsSapThreeTierVirtualInstance#ssh_private_key}.
        :param ssh_public_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_public_key WorkloadsSapThreeTierVirtualInstance#ssh_public_key}.
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfile(
            admin_username=admin_username,
            ssh_private_key=ssh_private_key,
            ssh_public_key=ssh_public_key,
        )

        return typing.cast(None, jsii.invoke(self, "putOsProfile", [value]))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImageOutputReference:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImageOutputReference, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="osProfile")
    def os_profile(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfileOutputReference:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfileOutputReference, jsii.get(self, "osProfile"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImage]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImage], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="osProfileInput")
    def os_profile_input(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfile]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfile], jsii.get(self, "osProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineSizeInput")
    def virtual_machine_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualMachineSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineSize")
    def virtual_machine_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualMachineSize"))

    @virtual_machine_size.setter
    def virtual_machine_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc3ec4c51f5af181ba627016d75306abca39dc0a5d7e7beb2b8faa6ebcac99d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualMachineSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfiguration]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__821650fb00c9fc44f359da0cc8a4c0d60dc778ced5c4b659e8adecc7a72494db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "instance_count": "instanceCount",
        "subnet_id": "subnetId",
        "virtual_machine_configuration": "virtualMachineConfiguration",
        "database_type": "databaseType",
        "disk_volume_configuration": "diskVolumeConfiguration",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfiguration:
    def __init__(
        self,
        *,
        instance_count: jsii.Number,
        subnet_id: builtins.str,
        virtual_machine_configuration: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfiguration", typing.Dict[builtins.str, typing.Any]],
        database_type: typing.Optional[builtins.str] = None,
        disk_volume_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#instance_count WorkloadsSapThreeTierVirtualInstance#instance_count}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#subnet_id WorkloadsSapThreeTierVirtualInstance#subnet_id}.
        :param virtual_machine_configuration: virtual_machine_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_configuration WorkloadsSapThreeTierVirtualInstance#virtual_machine_configuration}
        :param database_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#database_type WorkloadsSapThreeTierVirtualInstance#database_type}.
        :param disk_volume_configuration: disk_volume_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#disk_volume_configuration WorkloadsSapThreeTierVirtualInstance#disk_volume_configuration}
        '''
        if isinstance(virtual_machine_configuration, dict):
            virtual_machine_configuration = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfiguration(**virtual_machine_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f100608658a19fa7cd931d6706eaaa4692abe56e3b053750ff038be4daf31514)
            check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument virtual_machine_configuration", value=virtual_machine_configuration, expected_type=type_hints["virtual_machine_configuration"])
            check_type(argname="argument database_type", value=database_type, expected_type=type_hints["database_type"])
            check_type(argname="argument disk_volume_configuration", value=disk_volume_configuration, expected_type=type_hints["disk_volume_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_count": instance_count,
            "subnet_id": subnet_id,
            "virtual_machine_configuration": virtual_machine_configuration,
        }
        if database_type is not None:
            self._values["database_type"] = database_type
        if disk_volume_configuration is not None:
            self._values["disk_volume_configuration"] = disk_volume_configuration

    @builtins.property
    def instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#instance_count WorkloadsSapThreeTierVirtualInstance#instance_count}.'''
        result = self._values.get("instance_count")
        assert result is not None, "Required property 'instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#subnet_id WorkloadsSapThreeTierVirtualInstance#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_machine_configuration(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfiguration":
        '''virtual_machine_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_configuration WorkloadsSapThreeTierVirtualInstance#virtual_machine_configuration}
        '''
        result = self._values.get("virtual_machine_configuration")
        assert result is not None, "Required property 'virtual_machine_configuration' is missing"
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfiguration", result)

    @builtins.property
    def database_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#database_type WorkloadsSapThreeTierVirtualInstance#database_type}.'''
        result = self._values.get("database_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_volume_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration"]]]:
        '''disk_volume_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#disk_volume_configuration WorkloadsSapThreeTierVirtualInstance#disk_volume_configuration}
        '''
        result = self._values.get("disk_volume_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "number_of_disks": "numberOfDisks",
        "size_in_gb": "sizeInGb",
        "sku_name": "skuName",
        "volume_name": "volumeName",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration:
    def __init__(
        self,
        *,
        number_of_disks: jsii.Number,
        size_in_gb: jsii.Number,
        sku_name: builtins.str,
        volume_name: builtins.str,
    ) -> None:
        '''
        :param number_of_disks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#number_of_disks WorkloadsSapThreeTierVirtualInstance#number_of_disks}.
        :param size_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#size_in_gb WorkloadsSapThreeTierVirtualInstance#size_in_gb}.
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#sku_name WorkloadsSapThreeTierVirtualInstance#sku_name}.
        :param volume_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#volume_name WorkloadsSapThreeTierVirtualInstance#volume_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2f5dc65b90fbb808b52bb5b6d1732321cd7e3f05b4a35123f55e1b45994c654)
            check_type(argname="argument number_of_disks", value=number_of_disks, expected_type=type_hints["number_of_disks"])
            check_type(argname="argument size_in_gb", value=size_in_gb, expected_type=type_hints["size_in_gb"])
            check_type(argname="argument sku_name", value=sku_name, expected_type=type_hints["sku_name"])
            check_type(argname="argument volume_name", value=volume_name, expected_type=type_hints["volume_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "number_of_disks": number_of_disks,
            "size_in_gb": size_in_gb,
            "sku_name": sku_name,
            "volume_name": volume_name,
        }

    @builtins.property
    def number_of_disks(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#number_of_disks WorkloadsSapThreeTierVirtualInstance#number_of_disks}.'''
        result = self._values.get("number_of_disks")
        assert result is not None, "Required property 'number_of_disks' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def size_in_gb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#size_in_gb WorkloadsSapThreeTierVirtualInstance#size_in_gb}.'''
        result = self._values.get("size_in_gb")
        assert result is not None, "Required property 'size_in_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def sku_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#sku_name WorkloadsSapThreeTierVirtualInstance#sku_name}.'''
        result = self._values.get("sku_name")
        assert result is not None, "Required property 'sku_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#volume_name WorkloadsSapThreeTierVirtualInstance#volume_name}.'''
        result = self._values.get("volume_name")
        assert result is not None, "Required property 'volume_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfigurationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d73ce010a944509ea365d9cc39664375571698960def9a1245957012f572177e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4296a830b9f468fc3d7dc626d9bb2369ae3443e06382c88ea361f551717ee0db)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01b53633cd0dc0331be156a6691729e9ccea4b038ec5fc6133ab710b298760c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a86a226ea025cb75dbf2caffbeeddfca66794b5214f12ce7fc4e06347dc7ce3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f1d7a9f289db806c6f4cf6d02317a096e5773ed8b3994e77cdb52448833d18e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f7e1dd23f7474be90dd3cc72d74d48cf349131d14b1dd04e9dd559cc13ba0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11d02c7f6101219e14e304c0024b417f470a8909b5cf95c566b1aceb983facc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="numberOfDisksInput")
    def number_of_disks_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberOfDisksInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInGbInput")
    def size_in_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInGbInput"))

    @builtins.property
    @jsii.member(jsii_name="skuNameInput")
    def sku_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuNameInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeNameInput")
    def volume_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="numberOfDisks")
    def number_of_disks(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfDisks"))

    @number_of_disks.setter
    def number_of_disks(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a3f33b3f20bdc0da9187ab20136bee5dc33371fd51f21c03afc1fd2c16da160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberOfDisks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeInGb")
    def size_in_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeInGb"))

    @size_in_gb.setter
    def size_in_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__151c13dc59acdbe4507a6d2314fc5fe69a35123ae413e58d7639d8dd3f2af56d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeInGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skuName")
    def sku_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "skuName"))

    @sku_name.setter
    def sku_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9390847c56999ea3d15c4522a7a2a5544e0ee09681c82856efdc1350ebe581bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skuName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeName")
    def volume_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeName"))

    @volume_name.setter
    def volume_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7b6a41b415a4f9b6b50a2441d2381b48c1f6bb33b480fa4b6cf90d62e87209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27ae4b77406f5ce827fa288b783c4c4d37facdd9ef327a1671f3f0c94b673bdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a191c507f15bb9ee9e1efc490b9a36202c3b17aa1e8621d0129c3b760fe494bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDiskVolumeConfiguration")
    def put_disk_volume_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eff0778afbb0ef1237d974aff6e124bc4ab743e4c9a45aaac76817b39fed933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDiskVolumeConfiguration", [value]))

    @jsii.member(jsii_name="putVirtualMachineConfiguration")
    def put_virtual_machine_configuration(
        self,
        *,
        image: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImage", typing.Dict[builtins.str, typing.Any]],
        os_profile: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfile", typing.Dict[builtins.str, typing.Any]],
        virtual_machine_size: builtins.str,
    ) -> None:
        '''
        :param image: image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#image WorkloadsSapThreeTierVirtualInstance#image}
        :param os_profile: os_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#os_profile WorkloadsSapThreeTierVirtualInstance#os_profile}
        :param virtual_machine_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_size WorkloadsSapThreeTierVirtualInstance#virtual_machine_size}.
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfiguration(
            image=image,
            os_profile=os_profile,
            virtual_machine_size=virtual_machine_size,
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualMachineConfiguration", [value]))

    @jsii.member(jsii_name="resetDatabaseType")
    def reset_database_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseType", []))

    @jsii.member(jsii_name="resetDiskVolumeConfiguration")
    def reset_disk_volume_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskVolumeConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="diskVolumeConfiguration")
    def disk_volume_configuration(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfigurationList:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfigurationList, jsii.get(self, "diskVolumeConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineConfiguration")
    def virtual_machine_configuration(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOutputReference":
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOutputReference", jsii.get(self, "virtualMachineConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="databaseTypeInput")
    def database_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="diskVolumeConfigurationInput")
    def disk_volume_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration]]], jsii.get(self, "diskVolumeConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceCountInput")
    def instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineConfigurationInput")
    def virtual_machine_configuration_input(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfiguration"]:
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfiguration"], jsii.get(self, "virtualMachineConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseType")
    def database_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseType"))

    @database_type.setter
    def database_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6860ffba26b0fae4892a8027274e60d435195703f077452d7264734784df5ca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceCount")
    def instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instanceCount"))

    @instance_count.setter
    def instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07814d7f43e3181726ce1e477b8c80dd613935689eb96b0f242f007e2f57dd01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6088a938c821e039d9e37d26133080fb9e3dceb465232cb34d678853f8d6cc08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfiguration]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7708699b6b1916cc9eeb6d758b22f328c9695462cb9eeb36fec8a1cd13b9f270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "os_profile": "osProfile",
        "virtual_machine_size": "virtualMachineSize",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfiguration:
    def __init__(
        self,
        *,
        image: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImage", typing.Dict[builtins.str, typing.Any]],
        os_profile: typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfile", typing.Dict[builtins.str, typing.Any]],
        virtual_machine_size: builtins.str,
    ) -> None:
        '''
        :param image: image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#image WorkloadsSapThreeTierVirtualInstance#image}
        :param os_profile: os_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#os_profile WorkloadsSapThreeTierVirtualInstance#os_profile}
        :param virtual_machine_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_size WorkloadsSapThreeTierVirtualInstance#virtual_machine_size}.
        '''
        if isinstance(image, dict):
            image = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImage(**image)
        if isinstance(os_profile, dict):
            os_profile = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfile(**os_profile)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77fc7182677f32e5d587ca03f64b76eeea4792505a8551e25c488cc70dc3684d)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument os_profile", value=os_profile, expected_type=type_hints["os_profile"])
            check_type(argname="argument virtual_machine_size", value=virtual_machine_size, expected_type=type_hints["virtual_machine_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
            "os_profile": os_profile,
            "virtual_machine_size": virtual_machine_size,
        }

    @builtins.property
    def image(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImage":
        '''image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#image WorkloadsSapThreeTierVirtualInstance#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImage", result)

    @builtins.property
    def os_profile(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfile":
        '''os_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#os_profile WorkloadsSapThreeTierVirtualInstance#os_profile}
        '''
        result = self._values.get("os_profile")
        assert result is not None, "Required property 'os_profile' is missing"
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfile", result)

    @builtins.property
    def virtual_machine_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_size WorkloadsSapThreeTierVirtualInstance#virtual_machine_size}.'''
        result = self._values.get("virtual_machine_size")
        assert result is not None, "Required property 'virtual_machine_size' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImage",
    jsii_struct_bases=[],
    name_mapping={
        "offer": "offer",
        "publisher": "publisher",
        "sku": "sku",
        "version": "version",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImage:
    def __init__(
        self,
        *,
        offer: builtins.str,
        publisher: builtins.str,
        sku: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param offer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#offer WorkloadsSapThreeTierVirtualInstance#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#publisher WorkloadsSapThreeTierVirtualInstance#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#sku WorkloadsSapThreeTierVirtualInstance#sku}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#version WorkloadsSapThreeTierVirtualInstance#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48b23d8487c2be126128819ac919fa57a44869591ba843a3fb11d4d4d8cc0393)
            check_type(argname="argument offer", value=offer, expected_type=type_hints["offer"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "offer": offer,
            "publisher": publisher,
            "sku": sku,
            "version": version,
        }

    @builtins.property
    def offer(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#offer WorkloadsSapThreeTierVirtualInstance#offer}.'''
        result = self._values.get("offer")
        assert result is not None, "Required property 'offer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def publisher(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#publisher WorkloadsSapThreeTierVirtualInstance#publisher}.'''
        result = self._values.get("publisher")
        assert result is not None, "Required property 'publisher' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sku(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#sku WorkloadsSapThreeTierVirtualInstance#sku}.'''
        result = self._values.get("sku")
        assert result is not None, "Required property 'sku' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#version WorkloadsSapThreeTierVirtualInstance#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImageOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c77bea3e67f91d6d753db8110ce08b2838187b43a678fef4c07bc76c706c31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="offerInput")
    def offer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "offerInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherInput")
    def publisher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="skuInput")
    def sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="offer")
    def offer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "offer"))

    @offer.setter
    def offer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac73ededb93de8808bfa31b12208c6860d17a3530baf97b0cae3960dd5860cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisher"))

    @publisher.setter
    def publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d06f9df3851b9387ea3cd94d2728be0de1c6c844f8a2660aa2a71721ee6184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2be112590b25d3246fa810b03d7b9ed340766a5a9a50308b2648a92439eef60a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__495b2f22ef83bcc253b18ef81d1f8dff7856731be84ad7860ae8aaca25a1a01b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImage]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d0aa70e6e02d570e853be67d0df59645068e671a6a5c8a9db6184e613c12aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfile",
    jsii_struct_bases=[],
    name_mapping={
        "admin_username": "adminUsername",
        "ssh_private_key": "sshPrivateKey",
        "ssh_public_key": "sshPublicKey",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfile:
    def __init__(
        self,
        *,
        admin_username: builtins.str,
        ssh_private_key: builtins.str,
        ssh_public_key: builtins.str,
    ) -> None:
        '''
        :param admin_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#admin_username WorkloadsSapThreeTierVirtualInstance#admin_username}.
        :param ssh_private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_private_key WorkloadsSapThreeTierVirtualInstance#ssh_private_key}.
        :param ssh_public_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_public_key WorkloadsSapThreeTierVirtualInstance#ssh_public_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a4b788a284c2bb74caf0f4421a0aa7956f5f6e97c11f9621bc4ba9bb5eed35)
            check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
            check_type(argname="argument ssh_private_key", value=ssh_private_key, expected_type=type_hints["ssh_private_key"])
            check_type(argname="argument ssh_public_key", value=ssh_public_key, expected_type=type_hints["ssh_public_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_username": admin_username,
            "ssh_private_key": ssh_private_key,
            "ssh_public_key": ssh_public_key,
        }

    @builtins.property
    def admin_username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#admin_username WorkloadsSapThreeTierVirtualInstance#admin_username}.'''
        result = self._values.get("admin_username")
        assert result is not None, "Required property 'admin_username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssh_private_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_private_key WorkloadsSapThreeTierVirtualInstance#ssh_private_key}.'''
        result = self._values.get("ssh_private_key")
        assert result is not None, "Required property 'ssh_private_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssh_public_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_public_key WorkloadsSapThreeTierVirtualInstance#ssh_public_key}.'''
        result = self._values.get("ssh_public_key")
        assert result is not None, "Required property 'ssh_public_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfileOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8386f0bd340de39bfe0f12e194818fb1284ed956f81e340cf9f270a1a80a84a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="adminUsernameInput")
    def admin_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPrivateKeyInput")
    def ssh_private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshPrivateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeyInput")
    def ssh_public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="adminUsername")
    def admin_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminUsername"))

    @admin_username.setter
    def admin_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b8f164e07172fe9138a440854dcbb5bf4545b26af0504ff899c590f683e42a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPrivateKey")
    def ssh_private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshPrivateKey"))

    @ssh_private_key.setter
    def ssh_private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2da562511c9c67c1e0a502cdc9570469c91351a4acf93d824d70a03f60bbdb84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPrivateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPublicKey")
    def ssh_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshPublicKey"))

    @ssh_public_key.setter
    def ssh_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14f8ccb2769f09eb05a04ee0bd7450398da6a7c8c811c77f4fd8afd6ccae5a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPublicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfile]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__534e46ba81581bb21671b9896c9ece200dea68a8951caa6d5bc33d913f584534)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f28c7891a605959255c54e34fc0f82729451d86a0fe8639de5d5fc7b8da2cb12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putImage")
    def put_image(
        self,
        *,
        offer: builtins.str,
        publisher: builtins.str,
        sku: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param offer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#offer WorkloadsSapThreeTierVirtualInstance#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#publisher WorkloadsSapThreeTierVirtualInstance#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#sku WorkloadsSapThreeTierVirtualInstance#sku}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#version WorkloadsSapThreeTierVirtualInstance#version}.
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImage(
            offer=offer, publisher=publisher, sku=sku, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putImage", [value]))

    @jsii.member(jsii_name="putOsProfile")
    def put_os_profile(
        self,
        *,
        admin_username: builtins.str,
        ssh_private_key: builtins.str,
        ssh_public_key: builtins.str,
    ) -> None:
        '''
        :param admin_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#admin_username WorkloadsSapThreeTierVirtualInstance#admin_username}.
        :param ssh_private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_private_key WorkloadsSapThreeTierVirtualInstance#ssh_private_key}.
        :param ssh_public_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#ssh_public_key WorkloadsSapThreeTierVirtualInstance#ssh_public_key}.
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfile(
            admin_username=admin_username,
            ssh_private_key=ssh_private_key,
            ssh_public_key=ssh_public_key,
        )

        return typing.cast(None, jsii.invoke(self, "putOsProfile", [value]))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImageOutputReference:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImageOutputReference, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="osProfile")
    def os_profile(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfileOutputReference:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfileOutputReference, jsii.get(self, "osProfile"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImage]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImage], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="osProfileInput")
    def os_profile_input(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfile]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfile], jsii.get(self, "osProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineSizeInput")
    def virtual_machine_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualMachineSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineSize")
    def virtual_machine_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualMachineSize"))

    @virtual_machine_size.setter
    def virtual_machine_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37942a45647842d4fcffb3bb0ac60ba25c804599b4fb522050f40dcf6f8efbf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualMachineSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfiguration]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1123affe4d3bd146ef800c096da94408afca9eeabe453220f74cc9f68e6c3d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2ba556c3b73acddca05b5dad8d56bcbd769aeccf712b222b512c2f498ea2118)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApplicationServerConfiguration")
    def put_application_server_configuration(
        self,
        *,
        instance_count: jsii.Number,
        subnet_id: builtins.str,
        virtual_machine_configuration: typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfiguration, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#instance_count WorkloadsSapThreeTierVirtualInstance#instance_count}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#subnet_id WorkloadsSapThreeTierVirtualInstance#subnet_id}.
        :param virtual_machine_configuration: virtual_machine_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_configuration WorkloadsSapThreeTierVirtualInstance#virtual_machine_configuration}
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfiguration(
            instance_count=instance_count,
            subnet_id=subnet_id,
            virtual_machine_configuration=virtual_machine_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putApplicationServerConfiguration", [value]))

    @jsii.member(jsii_name="putCentralServerConfiguration")
    def put_central_server_configuration(
        self,
        *,
        instance_count: jsii.Number,
        subnet_id: builtins.str,
        virtual_machine_configuration: typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfiguration, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#instance_count WorkloadsSapThreeTierVirtualInstance#instance_count}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#subnet_id WorkloadsSapThreeTierVirtualInstance#subnet_id}.
        :param virtual_machine_configuration: virtual_machine_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_configuration WorkloadsSapThreeTierVirtualInstance#virtual_machine_configuration}
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfiguration(
            instance_count=instance_count,
            subnet_id=subnet_id,
            virtual_machine_configuration=virtual_machine_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putCentralServerConfiguration", [value]))

    @jsii.member(jsii_name="putDatabaseServerConfiguration")
    def put_database_server_configuration(
        self,
        *,
        instance_count: jsii.Number,
        subnet_id: builtins.str,
        virtual_machine_configuration: typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfiguration, typing.Dict[builtins.str, typing.Any]],
        database_type: typing.Optional[builtins.str] = None,
        disk_volume_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#instance_count WorkloadsSapThreeTierVirtualInstance#instance_count}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#subnet_id WorkloadsSapThreeTierVirtualInstance#subnet_id}.
        :param virtual_machine_configuration: virtual_machine_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_configuration WorkloadsSapThreeTierVirtualInstance#virtual_machine_configuration}
        :param database_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#database_type WorkloadsSapThreeTierVirtualInstance#database_type}.
        :param disk_volume_configuration: disk_volume_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#disk_volume_configuration WorkloadsSapThreeTierVirtualInstance#disk_volume_configuration}
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfiguration(
            instance_count=instance_count,
            subnet_id=subnet_id,
            virtual_machine_configuration=virtual_machine_configuration,
            database_type=database_type,
            disk_volume_configuration=disk_volume_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putDatabaseServerConfiguration", [value]))

    @jsii.member(jsii_name="putResourceNames")
    def put_resource_names(
        self,
        *,
        application_server: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServer", typing.Dict[builtins.str, typing.Any]]] = None,
        central_server: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServer", typing.Dict[builtins.str, typing.Any]]] = None,
        database_server: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServer", typing.Dict[builtins.str, typing.Any]]] = None,
        shared_storage: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorage", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param application_server: application_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#application_server WorkloadsSapThreeTierVirtualInstance#application_server}
        :param central_server: central_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#central_server WorkloadsSapThreeTierVirtualInstance#central_server}
        :param database_server: database_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#database_server WorkloadsSapThreeTierVirtualInstance#database_server}
        :param shared_storage: shared_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#shared_storage WorkloadsSapThreeTierVirtualInstance#shared_storage}
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNames(
            application_server=application_server,
            central_server=central_server,
            database_server=database_server,
            shared_storage=shared_storage,
        )

        return typing.cast(None, jsii.invoke(self, "putResourceNames", [value]))

    @jsii.member(jsii_name="putTransportCreateAndMount")
    def put_transport_create_and_mount(
        self,
        *,
        resource_group_id: typing.Optional[builtins.str] = None,
        storage_account_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#resource_group_id WorkloadsSapThreeTierVirtualInstance#resource_group_id}.
        :param storage_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#storage_account_name WorkloadsSapThreeTierVirtualInstance#storage_account_name}.
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMount(
            resource_group_id=resource_group_id,
            storage_account_name=storage_account_name,
        )

        return typing.cast(None, jsii.invoke(self, "putTransportCreateAndMount", [value]))

    @jsii.member(jsii_name="resetHighAvailabilityType")
    def reset_high_availability_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHighAvailabilityType", []))

    @jsii.member(jsii_name="resetResourceNames")
    def reset_resource_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceNames", []))

    @jsii.member(jsii_name="resetSecondaryIpEnabled")
    def reset_secondary_ip_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryIpEnabled", []))

    @jsii.member(jsii_name="resetTransportCreateAndMount")
    def reset_transport_create_and_mount(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransportCreateAndMount", []))

    @builtins.property
    @jsii.member(jsii_name="applicationServerConfiguration")
    def application_server_configuration(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationOutputReference:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationOutputReference, jsii.get(self, "applicationServerConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="centralServerConfiguration")
    def central_server_configuration(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationOutputReference:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationOutputReference, jsii.get(self, "centralServerConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="databaseServerConfiguration")
    def database_server_configuration(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationOutputReference:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationOutputReference, jsii.get(self, "databaseServerConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="resourceNames")
    def resource_names(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesOutputReference":
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesOutputReference", jsii.get(self, "resourceNames"))

    @builtins.property
    @jsii.member(jsii_name="transportCreateAndMount")
    def transport_create_and_mount(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMountOutputReference":
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMountOutputReference", jsii.get(self, "transportCreateAndMount"))

    @builtins.property
    @jsii.member(jsii_name="applicationServerConfigurationInput")
    def application_server_configuration_input(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfiguration]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfiguration], jsii.get(self, "applicationServerConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="appResourceGroupNameInput")
    def app_resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appResourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="centralServerConfigurationInput")
    def central_server_configuration_input(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfiguration]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfiguration], jsii.get(self, "centralServerConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseServerConfigurationInput")
    def database_server_configuration_input(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfiguration]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfiguration], jsii.get(self, "databaseServerConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="highAvailabilityTypeInput")
    def high_availability_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "highAvailabilityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceNamesInput")
    def resource_names_input(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNames"]:
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNames"], jsii.get(self, "resourceNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryIpEnabledInput")
    def secondary_ip_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "secondaryIpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="transportCreateAndMountInput")
    def transport_create_and_mount_input(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMount"]:
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMount"], jsii.get(self, "transportCreateAndMountInput"))

    @builtins.property
    @jsii.member(jsii_name="appResourceGroupName")
    def app_resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appResourceGroupName"))

    @app_resource_group_name.setter
    def app_resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4257e360138f60e09c83519836acface9cbb0cb9da91e7bc2f6544594a911e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appResourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="highAvailabilityType")
    def high_availability_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "highAvailabilityType"))

    @high_availability_type.setter
    def high_availability_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e63446bb0bebfaf2aaccbd1c6777a792e2559b7d7674e570c86ef28d3363a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "highAvailabilityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secondaryIpEnabled")
    def secondary_ip_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "secondaryIpEnabled"))

    @secondary_ip_enabled.setter
    def secondary_ip_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43b18d06bc6c33e2c6e874480e41b8b36aaa59d29dbb73a7fb0651b0d80ef35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryIpEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3017ad1d7c3348b877bb3adf583c57fe48d777a249d738e9c013dd3dc519497e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNames",
    jsii_struct_bases=[],
    name_mapping={
        "application_server": "applicationServer",
        "central_server": "centralServer",
        "database_server": "databaseServer",
        "shared_storage": "sharedStorage",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNames:
    def __init__(
        self,
        *,
        application_server: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServer", typing.Dict[builtins.str, typing.Any]]] = None,
        central_server: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServer", typing.Dict[builtins.str, typing.Any]]] = None,
        database_server: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServer", typing.Dict[builtins.str, typing.Any]]] = None,
        shared_storage: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorage", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param application_server: application_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#application_server WorkloadsSapThreeTierVirtualInstance#application_server}
        :param central_server: central_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#central_server WorkloadsSapThreeTierVirtualInstance#central_server}
        :param database_server: database_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#database_server WorkloadsSapThreeTierVirtualInstance#database_server}
        :param shared_storage: shared_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#shared_storage WorkloadsSapThreeTierVirtualInstance#shared_storage}
        '''
        if isinstance(application_server, dict):
            application_server = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServer(**application_server)
        if isinstance(central_server, dict):
            central_server = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServer(**central_server)
        if isinstance(database_server, dict):
            database_server = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServer(**database_server)
        if isinstance(shared_storage, dict):
            shared_storage = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorage(**shared_storage)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e71c4c7b72dfabd1bcb5639ebbd44f22751f3833c2bd686d3911d61ca88e8952)
            check_type(argname="argument application_server", value=application_server, expected_type=type_hints["application_server"])
            check_type(argname="argument central_server", value=central_server, expected_type=type_hints["central_server"])
            check_type(argname="argument database_server", value=database_server, expected_type=type_hints["database_server"])
            check_type(argname="argument shared_storage", value=shared_storage, expected_type=type_hints["shared_storage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_server is not None:
            self._values["application_server"] = application_server
        if central_server is not None:
            self._values["central_server"] = central_server
        if database_server is not None:
            self._values["database_server"] = database_server
        if shared_storage is not None:
            self._values["shared_storage"] = shared_storage

    @builtins.property
    def application_server(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServer"]:
        '''application_server block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#application_server WorkloadsSapThreeTierVirtualInstance#application_server}
        '''
        result = self._values.get("application_server")
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServer"], result)

    @builtins.property
    def central_server(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServer"]:
        '''central_server block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#central_server WorkloadsSapThreeTierVirtualInstance#central_server}
        '''
        result = self._values.get("central_server")
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServer"], result)

    @builtins.property
    def database_server(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServer"]:
        '''database_server block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#database_server WorkloadsSapThreeTierVirtualInstance#database_server}
        '''
        result = self._values.get("database_server")
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServer"], result)

    @builtins.property
    def shared_storage(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorage"]:
        '''shared_storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#shared_storage WorkloadsSapThreeTierVirtualInstance#shared_storage}
        '''
        result = self._values.get("shared_storage")
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorage"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServer",
    jsii_struct_bases=[],
    name_mapping={
        "availability_set_name": "availabilitySetName",
        "virtual_machine": "virtualMachine",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServer:
    def __init__(
        self,
        *,
        availability_set_name: typing.Optional[builtins.str] = None,
        virtual_machine: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param availability_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#availability_set_name WorkloadsSapThreeTierVirtualInstance#availability_set_name}.
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine WorkloadsSapThreeTierVirtualInstance#virtual_machine}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5684ef52c9ea09657b3938e1b349cbea0f5c4c0555a733f2c1d06193611de07)
            check_type(argname="argument availability_set_name", value=availability_set_name, expected_type=type_hints["availability_set_name"])
            check_type(argname="argument virtual_machine", value=virtual_machine, expected_type=type_hints["virtual_machine"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_set_name is not None:
            self._values["availability_set_name"] = availability_set_name
        if virtual_machine is not None:
            self._values["virtual_machine"] = virtual_machine

    @builtins.property
    def availability_set_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#availability_set_name WorkloadsSapThreeTierVirtualInstance#availability_set_name}.'''
        result = self._values.get("availability_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_machine(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine"]]]:
        '''virtual_machine block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine WorkloadsSapThreeTierVirtualInstance#virtual_machine}
        '''
        result = self._values.get("virtual_machine")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d034ca891c29df2813ffc4104faf5bb2e8dccdd91b5d0096e9e77a2d40db6c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVirtualMachine")
    def put_virtual_machine(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da75d05412efb549b69b806e902272448fbacdfabadee59b4de38530d0e93193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVirtualMachine", [value]))

    @jsii.member(jsii_name="resetAvailabilitySetName")
    def reset_availability_set_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilitySetName", []))

    @jsii.member(jsii_name="resetVirtualMachine")
    def reset_virtual_machine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualMachine", []))

    @builtins.property
    @jsii.member(jsii_name="virtualMachine")
    def virtual_machine(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineList":
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineList", jsii.get(self, "virtualMachine"))

    @builtins.property
    @jsii.member(jsii_name="availabilitySetNameInput")
    def availability_set_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilitySetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineInput")
    def virtual_machine_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine"]]], jsii.get(self, "virtualMachineInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilitySetName")
    def availability_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilitySetName"))

    @availability_set_name.setter
    def availability_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3595d365e32283e1775fc7850132e515b98868b67c3ce534a5348fe5e9be86bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilitySetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServer]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5f7919d45acd76f0a8ce1d4b75af0acf8a8b5c556a2207b23c25bc6cb2bffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine",
    jsii_struct_bases=[],
    name_mapping={
        "data_disk": "dataDisk",
        "host_name": "hostName",
        "network_interface_names": "networkInterfaceNames",
        "os_disk_name": "osDiskName",
        "virtual_machine_name": "virtualMachineName",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine:
    def __init__(
        self,
        *,
        data_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        host_name: typing.Optional[builtins.str] = None,
        network_interface_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        os_disk_name: typing.Optional[builtins.str] = None,
        virtual_machine_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_disk: data_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#data_disk WorkloadsSapThreeTierVirtualInstance#data_disk}
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#host_name WorkloadsSapThreeTierVirtualInstance#host_name}.
        :param network_interface_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#network_interface_names WorkloadsSapThreeTierVirtualInstance#network_interface_names}.
        :param os_disk_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#os_disk_name WorkloadsSapThreeTierVirtualInstance#os_disk_name}.
        :param virtual_machine_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_name WorkloadsSapThreeTierVirtualInstance#virtual_machine_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc20761971e61b56e27619c0904bffeb0873600ca43334614996759ecbcbd711)
            check_type(argname="argument data_disk", value=data_disk, expected_type=type_hints["data_disk"])
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument network_interface_names", value=network_interface_names, expected_type=type_hints["network_interface_names"])
            check_type(argname="argument os_disk_name", value=os_disk_name, expected_type=type_hints["os_disk_name"])
            check_type(argname="argument virtual_machine_name", value=virtual_machine_name, expected_type=type_hints["virtual_machine_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_disk is not None:
            self._values["data_disk"] = data_disk
        if host_name is not None:
            self._values["host_name"] = host_name
        if network_interface_names is not None:
            self._values["network_interface_names"] = network_interface_names
        if os_disk_name is not None:
            self._values["os_disk_name"] = os_disk_name
        if virtual_machine_name is not None:
            self._values["virtual_machine_name"] = virtual_machine_name

    @builtins.property
    def data_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk"]]]:
        '''data_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#data_disk WorkloadsSapThreeTierVirtualInstance#data_disk}
        '''
        result = self._values.get("data_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk"]]], result)

    @builtins.property
    def host_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#host_name WorkloadsSapThreeTierVirtualInstance#host_name}.'''
        result = self._values.get("host_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_interface_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#network_interface_names WorkloadsSapThreeTierVirtualInstance#network_interface_names}.'''
        result = self._values.get("network_interface_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def os_disk_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#os_disk_name WorkloadsSapThreeTierVirtualInstance#os_disk_name}.'''
        result = self._values.get("os_disk_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_machine_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_name WorkloadsSapThreeTierVirtualInstance#virtual_machine_name}.'''
        result = self._values.get("virtual_machine_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk",
    jsii_struct_bases=[],
    name_mapping={"names": "names", "volume_name": "volumeName"},
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk:
    def __init__(
        self,
        *,
        names: typing.Sequence[builtins.str],
        volume_name: builtins.str,
    ) -> None:
        '''
        :param names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#names WorkloadsSapThreeTierVirtualInstance#names}.
        :param volume_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#volume_name WorkloadsSapThreeTierVirtualInstance#volume_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__993c62a3f7fab97789310191ac6481ca41617a4b994cfe08ca7cf9775b6c459d)
            check_type(argname="argument names", value=names, expected_type=type_hints["names"])
            check_type(argname="argument volume_name", value=volume_name, expected_type=type_hints["volume_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "names": names,
            "volume_name": volume_name,
        }

    @builtins.property
    def names(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#names WorkloadsSapThreeTierVirtualInstance#names}.'''
        result = self._values.get("names")
        assert result is not None, "Required property 'names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def volume_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#volume_name WorkloadsSapThreeTierVirtualInstance#volume_name}.'''
        result = self._values.get("volume_name")
        assert result is not None, "Required property 'volume_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDiskList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83bad5286a7b5187da21fa9343f2d78c13a242f5c1dc0d4eea6ac8900ab9e49e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0d58c9abd5196911c9386fd536cf50601c881928c293d9affdf6d1d76182d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa89bf95096d3fc1f106031bc0f63522749c956dd6b05f14ddfcf5c77ad41c4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__777c6ea0b44448261555e51b439f3f39f62dd8f44bf381c952737f78419c6a08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c95931d07413d98883c10c35d0e123de99d3567df50f7bae6cc53ee701b6d765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b810a38cf2608d6f97b54ffb65a5c68af7c6442ba228ccfc79e45b543f1b17c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDiskOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a4b40200a602fa736c65f3593b00f63c0ab6a3e805c87748c6ac15eb60c8dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="namesInput")
    def names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "namesInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeNameInput")
    def volume_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="names")
    def names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "names"))

    @names.setter
    def names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee5d226a831c67c827dae8f46cec80e59315f5b1c27c7a8aef28a7c8bb85b31a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "names", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeName")
    def volume_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeName"))

    @volume_name.setter
    def volume_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__933ccaacad4d6faebd71af8357ccd28c2a50f60bce60d5e424d8888585830fa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fddc75c90c5134da0fcba4c37b0aea9ed5744eea70fa460b8a2fd0e1b3e08ce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6245d183ceb585bd215ea35217f913ebc75ef904b1a5cf531c8d349771408f2d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2731aa0b78bc9725a943945942ece00a49fc33a1f5b35faa7ca140ca63f15652)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0697ac0902e7fe0f2663af7dcdd32ea898f8a36ac283595d00380c7891a09a9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d96cc336d8040c2e6e8937039dde15f6dbb0d7c59781ee6a61ac8f015d85433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__790f923f538c4db927a265d58f84b379e0e8ab41fe2d73837adb8519a070dc82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__921697e5540376d74dd44e2a6341cd0e7ddf42bbf391b5b731bb8ddaac6c9faf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc296c06b925c91761ef126cd1274af86439c6b7fe6d37db77b5d4f8666b4f0c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDataDisk")
    def put_data_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__988f350306766a26773171be6af2aef078e212fbb4d8c570c2701f267e91f7d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataDisk", [value]))

    @jsii.member(jsii_name="resetDataDisk")
    def reset_data_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataDisk", []))

    @jsii.member(jsii_name="resetHostName")
    def reset_host_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostName", []))

    @jsii.member(jsii_name="resetNetworkInterfaceNames")
    def reset_network_interface_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkInterfaceNames", []))

    @jsii.member(jsii_name="resetOsDiskName")
    def reset_os_disk_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsDiskName", []))

    @jsii.member(jsii_name="resetVirtualMachineName")
    def reset_virtual_machine_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualMachineName", []))

    @builtins.property
    @jsii.member(jsii_name="dataDisk")
    def data_disk(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDiskList:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDiskList, jsii.get(self, "dataDisk"))

    @builtins.property
    @jsii.member(jsii_name="dataDiskInput")
    def data_disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk]]], jsii.get(self, "dataDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceNamesInput")
    def network_interface_names_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "networkInterfaceNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="osDiskNameInput")
    def os_disk_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osDiskNameInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineNameInput")
    def virtual_machine_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualMachineNameInput"))

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2eb166356d8f378f4241532c6d06d4cd126a752152b4ff951dc34bd7fae49b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceNames")
    def network_interface_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkInterfaceNames"))

    @network_interface_names.setter
    def network_interface_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91706935fc42aac82838cfdc38211e3fc8fcc84478fa0b0241d7bd6a9ce86540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkInterfaceNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osDiskName")
    def os_disk_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osDiskName"))

    @os_disk_name.setter
    def os_disk_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c9d3cc6bef6e17049a41d2ea5116b7d47b6533d843af0a454f8ec8a4c42ee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osDiskName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualMachineName")
    def virtual_machine_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualMachineName"))

    @virtual_machine_name.setter
    def virtual_machine_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08396adeb098d993e1071078c37cfbeb2adadbe5c8e019b5a2021289fae9d4d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualMachineName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c2d99d15bc9aaef81e21960415bda6232df4524c41a74a33fa76adfddcbd2ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServer",
    jsii_struct_bases=[],
    name_mapping={
        "availability_set_name": "availabilitySetName",
        "load_balancer": "loadBalancer",
        "virtual_machine": "virtualMachine",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServer:
    def __init__(
        self,
        *,
        availability_set_name: typing.Optional[builtins.str] = None,
        load_balancer: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancer", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param availability_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#availability_set_name WorkloadsSapThreeTierVirtualInstance#availability_set_name}.
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#load_balancer WorkloadsSapThreeTierVirtualInstance#load_balancer}
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine WorkloadsSapThreeTierVirtualInstance#virtual_machine}
        '''
        if isinstance(load_balancer, dict):
            load_balancer = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancer(**load_balancer)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d0664e6eeae1043e17b6464b94466760225183562ba774169377c9892a8e951)
            check_type(argname="argument availability_set_name", value=availability_set_name, expected_type=type_hints["availability_set_name"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument virtual_machine", value=virtual_machine, expected_type=type_hints["virtual_machine"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_set_name is not None:
            self._values["availability_set_name"] = availability_set_name
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if virtual_machine is not None:
            self._values["virtual_machine"] = virtual_machine

    @builtins.property
    def availability_set_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#availability_set_name WorkloadsSapThreeTierVirtualInstance#availability_set_name}.'''
        result = self._values.get("availability_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancer"]:
        '''load_balancer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#load_balancer WorkloadsSapThreeTierVirtualInstance#load_balancer}
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancer"], result)

    @builtins.property
    def virtual_machine(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine"]]]:
        '''virtual_machine block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine WorkloadsSapThreeTierVirtualInstance#virtual_machine}
        '''
        result = self._values.get("virtual_machine")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancer",
    jsii_struct_bases=[],
    name_mapping={
        "backend_pool_names": "backendPoolNames",
        "frontend_ip_configuration_names": "frontendIpConfigurationNames",
        "health_probe_names": "healthProbeNames",
        "name": "name",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancer:
    def __init__(
        self,
        *,
        backend_pool_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        frontend_ip_configuration_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        health_probe_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backend_pool_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#backend_pool_names WorkloadsSapThreeTierVirtualInstance#backend_pool_names}.
        :param frontend_ip_configuration_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#frontend_ip_configuration_names WorkloadsSapThreeTierVirtualInstance#frontend_ip_configuration_names}.
        :param health_probe_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#health_probe_names WorkloadsSapThreeTierVirtualInstance#health_probe_names}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#name WorkloadsSapThreeTierVirtualInstance#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4e7b05ebe3b5a905121edaa9074bd425d84cf4017b38405db7658aa89752d35)
            check_type(argname="argument backend_pool_names", value=backend_pool_names, expected_type=type_hints["backend_pool_names"])
            check_type(argname="argument frontend_ip_configuration_names", value=frontend_ip_configuration_names, expected_type=type_hints["frontend_ip_configuration_names"])
            check_type(argname="argument health_probe_names", value=health_probe_names, expected_type=type_hints["health_probe_names"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backend_pool_names is not None:
            self._values["backend_pool_names"] = backend_pool_names
        if frontend_ip_configuration_names is not None:
            self._values["frontend_ip_configuration_names"] = frontend_ip_configuration_names
        if health_probe_names is not None:
            self._values["health_probe_names"] = health_probe_names
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def backend_pool_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#backend_pool_names WorkloadsSapThreeTierVirtualInstance#backend_pool_names}.'''
        result = self._values.get("backend_pool_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def frontend_ip_configuration_names(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#frontend_ip_configuration_names WorkloadsSapThreeTierVirtualInstance#frontend_ip_configuration_names}.'''
        result = self._values.get("frontend_ip_configuration_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def health_probe_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#health_probe_names WorkloadsSapThreeTierVirtualInstance#health_probe_names}.'''
        result = self._values.get("health_probe_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#name WorkloadsSapThreeTierVirtualInstance#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancerOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b942f8444c1573af0c20f3d43dc81a2ea363c105be47eac8bc044f535834287)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBackendPoolNames")
    def reset_backend_pool_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendPoolNames", []))

    @jsii.member(jsii_name="resetFrontendIpConfigurationNames")
    def reset_frontend_ip_configuration_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrontendIpConfigurationNames", []))

    @jsii.member(jsii_name="resetHealthProbeNames")
    def reset_health_probe_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthProbeNames", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="backendPoolNamesInput")
    def backend_pool_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "backendPoolNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendIpConfigurationNamesInput")
    def frontend_ip_configuration_names_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "frontendIpConfigurationNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="healthProbeNamesInput")
    def health_probe_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "healthProbeNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="backendPoolNames")
    def backend_pool_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "backendPoolNames"))

    @backend_pool_names.setter
    def backend_pool_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7596e56b4a77812eba84b4eb9a2583986a36720abf25f82042a604ea7f6b43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backendPoolNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frontendIpConfigurationNames")
    def frontend_ip_configuration_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "frontendIpConfigurationNames"))

    @frontend_ip_configuration_names.setter
    def frontend_ip_configuration_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0dcc4c0e170ea18f65778e003d086ecd8083194646495cdd615890b8d89560a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frontendIpConfigurationNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthProbeNames")
    def health_probe_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "healthProbeNames"))

    @health_probe_names.setter
    def health_probe_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03fe0b5e12066e2411314b0ce76ef185a84cbbd30120eade6d8fd17c6287a16c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthProbeNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b5e224e892670842e19bfe33858a06155b787738187349b1b3d00fad0178d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancer]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6b82975271de266e49dc0c0b1205a195a24a0a7dcd56d136fe9e3bec1014b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4991e1f2597765e6a6de639e8a32ffc8d492617091af7cab21c7a6508a9116c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoadBalancer")
    def put_load_balancer(
        self,
        *,
        backend_pool_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        frontend_ip_configuration_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        health_probe_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backend_pool_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#backend_pool_names WorkloadsSapThreeTierVirtualInstance#backend_pool_names}.
        :param frontend_ip_configuration_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#frontend_ip_configuration_names WorkloadsSapThreeTierVirtualInstance#frontend_ip_configuration_names}.
        :param health_probe_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#health_probe_names WorkloadsSapThreeTierVirtualInstance#health_probe_names}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#name WorkloadsSapThreeTierVirtualInstance#name}.
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancer(
            backend_pool_names=backend_pool_names,
            frontend_ip_configuration_names=frontend_ip_configuration_names,
            health_probe_names=health_probe_names,
            name=name,
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancer", [value]))

    @jsii.member(jsii_name="putVirtualMachine")
    def put_virtual_machine(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a793e62ede6658957d8464bfc50390ab5cc81e74b96ebd3a7a3c388556b2c71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVirtualMachine", [value]))

    @jsii.member(jsii_name="resetAvailabilitySetName")
    def reset_availability_set_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilitySetName", []))

    @jsii.member(jsii_name="resetLoadBalancer")
    def reset_load_balancer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancer", []))

    @jsii.member(jsii_name="resetVirtualMachine")
    def reset_virtual_machine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualMachine", []))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancerOutputReference:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancerOutputReference, jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachine")
    def virtual_machine(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineList":
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineList", jsii.get(self, "virtualMachine"))

    @builtins.property
    @jsii.member(jsii_name="availabilitySetNameInput")
    def availability_set_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilitySetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerInput")
    def load_balancer_input(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancer]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancer], jsii.get(self, "loadBalancerInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineInput")
    def virtual_machine_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine"]]], jsii.get(self, "virtualMachineInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilitySetName")
    def availability_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilitySetName"))

    @availability_set_name.setter
    def availability_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a35c8fad159555928013e8a674630f7bbe0b0ec456c4cc65e9570dd834f2dcbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilitySetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServer]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978e2913de397da40760e95b258a7bc1a850d5a02e80e875f3e7faae4f1a7792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine",
    jsii_struct_bases=[],
    name_mapping={
        "data_disk": "dataDisk",
        "host_name": "hostName",
        "network_interface_names": "networkInterfaceNames",
        "os_disk_name": "osDiskName",
        "virtual_machine_name": "virtualMachineName",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine:
    def __init__(
        self,
        *,
        data_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        host_name: typing.Optional[builtins.str] = None,
        network_interface_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        os_disk_name: typing.Optional[builtins.str] = None,
        virtual_machine_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_disk: data_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#data_disk WorkloadsSapThreeTierVirtualInstance#data_disk}
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#host_name WorkloadsSapThreeTierVirtualInstance#host_name}.
        :param network_interface_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#network_interface_names WorkloadsSapThreeTierVirtualInstance#network_interface_names}.
        :param os_disk_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#os_disk_name WorkloadsSapThreeTierVirtualInstance#os_disk_name}.
        :param virtual_machine_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_name WorkloadsSapThreeTierVirtualInstance#virtual_machine_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84f7e037e4c3a5da53394772c5c1a598d0a445793df4e0cd60d5815f2ebb7c0f)
            check_type(argname="argument data_disk", value=data_disk, expected_type=type_hints["data_disk"])
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument network_interface_names", value=network_interface_names, expected_type=type_hints["network_interface_names"])
            check_type(argname="argument os_disk_name", value=os_disk_name, expected_type=type_hints["os_disk_name"])
            check_type(argname="argument virtual_machine_name", value=virtual_machine_name, expected_type=type_hints["virtual_machine_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_disk is not None:
            self._values["data_disk"] = data_disk
        if host_name is not None:
            self._values["host_name"] = host_name
        if network_interface_names is not None:
            self._values["network_interface_names"] = network_interface_names
        if os_disk_name is not None:
            self._values["os_disk_name"] = os_disk_name
        if virtual_machine_name is not None:
            self._values["virtual_machine_name"] = virtual_machine_name

    @builtins.property
    def data_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk"]]]:
        '''data_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#data_disk WorkloadsSapThreeTierVirtualInstance#data_disk}
        '''
        result = self._values.get("data_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk"]]], result)

    @builtins.property
    def host_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#host_name WorkloadsSapThreeTierVirtualInstance#host_name}.'''
        result = self._values.get("host_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_interface_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#network_interface_names WorkloadsSapThreeTierVirtualInstance#network_interface_names}.'''
        result = self._values.get("network_interface_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def os_disk_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#os_disk_name WorkloadsSapThreeTierVirtualInstance#os_disk_name}.'''
        result = self._values.get("os_disk_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_machine_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_name WorkloadsSapThreeTierVirtualInstance#virtual_machine_name}.'''
        result = self._values.get("virtual_machine_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk",
    jsii_struct_bases=[],
    name_mapping={"names": "names", "volume_name": "volumeName"},
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk:
    def __init__(
        self,
        *,
        names: typing.Sequence[builtins.str],
        volume_name: builtins.str,
    ) -> None:
        '''
        :param names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#names WorkloadsSapThreeTierVirtualInstance#names}.
        :param volume_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#volume_name WorkloadsSapThreeTierVirtualInstance#volume_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__776757a3d78aa5dd77e0adf78c3fd0ab8ec1353c4c89214c320bc29ded60b246)
            check_type(argname="argument names", value=names, expected_type=type_hints["names"])
            check_type(argname="argument volume_name", value=volume_name, expected_type=type_hints["volume_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "names": names,
            "volume_name": volume_name,
        }

    @builtins.property
    def names(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#names WorkloadsSapThreeTierVirtualInstance#names}.'''
        result = self._values.get("names")
        assert result is not None, "Required property 'names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def volume_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#volume_name WorkloadsSapThreeTierVirtualInstance#volume_name}.'''
        result = self._values.get("volume_name")
        assert result is not None, "Required property 'volume_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDiskList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c5a09e85c51435349f1e32dedb323b8114eb0e880c49944e8e958c612d6c092)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530e561b1c0491d890138740e350c490fc4497c47af6df48d10f1156e2b09bc8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3380741e74e3f6521789951ed203bd55316f85549d1fb3f7cd1edd7e4b4f3abf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844aa0cb88b87cdf791764ee15a0666be1ef7397241bdda3060451a816b385c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a63f41f678c81c0d14d92c309af803c255105e29b57c191f48ad30586400d27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b1760c3229db44e4911d30948cc09d4bc29063a7f4ce86863883de39eea3fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDiskOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__335aee7c8dc747037cd6fe870f7dc6473775f283275af72f5a68916374af45a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="namesInput")
    def names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "namesInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeNameInput")
    def volume_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="names")
    def names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "names"))

    @names.setter
    def names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae728efc54b274c8ddaca748373afb04e9509230694d586bd8aabee12d62f1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "names", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeName")
    def volume_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeName"))

    @volume_name.setter
    def volume_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cb32256389b86536b8cbed4b1d72a8334b16bd82e0f9c7637bd9c1418072339)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc8e2faa28406fc31aa2acd6c2cd779aeacd1b41c37eabbfa63a64dfd871819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__124b9073811e8a49895eda2813b64457f9ba427221d62626ab2e92bfbc82be5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dac4d4ddf6afdb93b7319f4a213a235099f982c313b9a4d68cae765c428e9701)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb73a62515b721b4981906cd152492376b246659bfebb303e489b1cd8f080a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b08294e0035d743198effff4f25a458fc3fec778e4ce9d5ae8e76ba7ac28a9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d456636e66da3cd2d9bfd86c3529e00222c15a79109b5f86064557e3f0975570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a349bc644b3f3682476ac8741c0bc5a28c20147990d50b35f926251f9e3897)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0961345860790411447044a6cb159033878115f47fe02bf0937780ac980b162)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDataDisk")
    def put_data_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b34c1ecf18b3ec56df1ddb50b16d9091991640013bc3d0100db7ae7c1ae1862e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataDisk", [value]))

    @jsii.member(jsii_name="resetDataDisk")
    def reset_data_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataDisk", []))

    @jsii.member(jsii_name="resetHostName")
    def reset_host_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostName", []))

    @jsii.member(jsii_name="resetNetworkInterfaceNames")
    def reset_network_interface_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkInterfaceNames", []))

    @jsii.member(jsii_name="resetOsDiskName")
    def reset_os_disk_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsDiskName", []))

    @jsii.member(jsii_name="resetVirtualMachineName")
    def reset_virtual_machine_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualMachineName", []))

    @builtins.property
    @jsii.member(jsii_name="dataDisk")
    def data_disk(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDiskList:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDiskList, jsii.get(self, "dataDisk"))

    @builtins.property
    @jsii.member(jsii_name="dataDiskInput")
    def data_disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk]]], jsii.get(self, "dataDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceNamesInput")
    def network_interface_names_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "networkInterfaceNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="osDiskNameInput")
    def os_disk_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osDiskNameInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineNameInput")
    def virtual_machine_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualMachineNameInput"))

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c1491cac7298b5b9bccd786bd9cb39f261ced136e894fe9938f3f2bd5102a5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceNames")
    def network_interface_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkInterfaceNames"))

    @network_interface_names.setter
    def network_interface_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__454298aef440e38c3922615e1d9921eb061ee59bc8128bbcb73ff7fae0e06e8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkInterfaceNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osDiskName")
    def os_disk_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osDiskName"))

    @os_disk_name.setter
    def os_disk_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__564395f9688b3d67583ee6b8bfe350da29b94cd9e699b3b72ed829dffab82d8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osDiskName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualMachineName")
    def virtual_machine_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualMachineName"))

    @virtual_machine_name.setter
    def virtual_machine_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd0d962d5ccd27344c62ca8275c9a9c8547b56e69fef71299f268e6e1f3e5b7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualMachineName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7768ddc824d5489e109e3f65e3cbc4557c60d6843288395c8e2b8f499705c52e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServer",
    jsii_struct_bases=[],
    name_mapping={
        "availability_set_name": "availabilitySetName",
        "load_balancer": "loadBalancer",
        "virtual_machine": "virtualMachine",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServer:
    def __init__(
        self,
        *,
        availability_set_name: typing.Optional[builtins.str] = None,
        load_balancer: typing.Optional[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancer", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param availability_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#availability_set_name WorkloadsSapThreeTierVirtualInstance#availability_set_name}.
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#load_balancer WorkloadsSapThreeTierVirtualInstance#load_balancer}
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine WorkloadsSapThreeTierVirtualInstance#virtual_machine}
        '''
        if isinstance(load_balancer, dict):
            load_balancer = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancer(**load_balancer)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__883aeb439bf5e2eeecda0c5fd5f1459c32211c580ef072c91bae1a63ec98de99)
            check_type(argname="argument availability_set_name", value=availability_set_name, expected_type=type_hints["availability_set_name"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument virtual_machine", value=virtual_machine, expected_type=type_hints["virtual_machine"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_set_name is not None:
            self._values["availability_set_name"] = availability_set_name
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if virtual_machine is not None:
            self._values["virtual_machine"] = virtual_machine

    @builtins.property
    def availability_set_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#availability_set_name WorkloadsSapThreeTierVirtualInstance#availability_set_name}.'''
        result = self._values.get("availability_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancer"]:
        '''load_balancer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#load_balancer WorkloadsSapThreeTierVirtualInstance#load_balancer}
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancer"], result)

    @builtins.property
    def virtual_machine(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine"]]]:
        '''virtual_machine block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine WorkloadsSapThreeTierVirtualInstance#virtual_machine}
        '''
        result = self._values.get("virtual_machine")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancer",
    jsii_struct_bases=[],
    name_mapping={
        "backend_pool_names": "backendPoolNames",
        "frontend_ip_configuration_names": "frontendIpConfigurationNames",
        "health_probe_names": "healthProbeNames",
        "name": "name",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancer:
    def __init__(
        self,
        *,
        backend_pool_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        frontend_ip_configuration_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        health_probe_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backend_pool_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#backend_pool_names WorkloadsSapThreeTierVirtualInstance#backend_pool_names}.
        :param frontend_ip_configuration_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#frontend_ip_configuration_names WorkloadsSapThreeTierVirtualInstance#frontend_ip_configuration_names}.
        :param health_probe_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#health_probe_names WorkloadsSapThreeTierVirtualInstance#health_probe_names}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#name WorkloadsSapThreeTierVirtualInstance#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c03f558d4ca5176074a882a4077c0aeb13656ea5e6c3344b8bfedeedd68837)
            check_type(argname="argument backend_pool_names", value=backend_pool_names, expected_type=type_hints["backend_pool_names"])
            check_type(argname="argument frontend_ip_configuration_names", value=frontend_ip_configuration_names, expected_type=type_hints["frontend_ip_configuration_names"])
            check_type(argname="argument health_probe_names", value=health_probe_names, expected_type=type_hints["health_probe_names"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backend_pool_names is not None:
            self._values["backend_pool_names"] = backend_pool_names
        if frontend_ip_configuration_names is not None:
            self._values["frontend_ip_configuration_names"] = frontend_ip_configuration_names
        if health_probe_names is not None:
            self._values["health_probe_names"] = health_probe_names
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def backend_pool_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#backend_pool_names WorkloadsSapThreeTierVirtualInstance#backend_pool_names}.'''
        result = self._values.get("backend_pool_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def frontend_ip_configuration_names(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#frontend_ip_configuration_names WorkloadsSapThreeTierVirtualInstance#frontend_ip_configuration_names}.'''
        result = self._values.get("frontend_ip_configuration_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def health_probe_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#health_probe_names WorkloadsSapThreeTierVirtualInstance#health_probe_names}.'''
        result = self._values.get("health_probe_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#name WorkloadsSapThreeTierVirtualInstance#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancerOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b454df771ff196a17c5dc4d1ca2e71e142dba06037b122860b919fc05d6b424d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBackendPoolNames")
    def reset_backend_pool_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendPoolNames", []))

    @jsii.member(jsii_name="resetFrontendIpConfigurationNames")
    def reset_frontend_ip_configuration_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrontendIpConfigurationNames", []))

    @jsii.member(jsii_name="resetHealthProbeNames")
    def reset_health_probe_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthProbeNames", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="backendPoolNamesInput")
    def backend_pool_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "backendPoolNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendIpConfigurationNamesInput")
    def frontend_ip_configuration_names_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "frontendIpConfigurationNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="healthProbeNamesInput")
    def health_probe_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "healthProbeNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="backendPoolNames")
    def backend_pool_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "backendPoolNames"))

    @backend_pool_names.setter
    def backend_pool_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaec77adb4e188db6c3393d4bedeced46f6156ae0556990f5266b38ab72896d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backendPoolNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frontendIpConfigurationNames")
    def frontend_ip_configuration_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "frontendIpConfigurationNames"))

    @frontend_ip_configuration_names.setter
    def frontend_ip_configuration_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b79f781d2f6fe94e5a6c9f176fbb1daf35d862c47a714883e23577551178a31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frontendIpConfigurationNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthProbeNames")
    def health_probe_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "healthProbeNames"))

    @health_probe_names.setter
    def health_probe_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__934d21e7caa9120e5b47443a84cfa042ebbdca2437819f20482b16de64f2a02e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthProbeNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3134ddc0c1d361c061fcc0299e9ea26f3d38364cffbe031ebce4ac1b7c7d5373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancer]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71b0bae47e00eedac91380e65daa5a67d9693b540e2fc93f982e2b8c2bc6ba67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1028e771532aea32138d228ea7042e52e8e5372ca68cc5751c6edc53990c486b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoadBalancer")
    def put_load_balancer(
        self,
        *,
        backend_pool_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        frontend_ip_configuration_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        health_probe_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backend_pool_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#backend_pool_names WorkloadsSapThreeTierVirtualInstance#backend_pool_names}.
        :param frontend_ip_configuration_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#frontend_ip_configuration_names WorkloadsSapThreeTierVirtualInstance#frontend_ip_configuration_names}.
        :param health_probe_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#health_probe_names WorkloadsSapThreeTierVirtualInstance#health_probe_names}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#name WorkloadsSapThreeTierVirtualInstance#name}.
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancer(
            backend_pool_names=backend_pool_names,
            frontend_ip_configuration_names=frontend_ip_configuration_names,
            health_probe_names=health_probe_names,
            name=name,
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancer", [value]))

    @jsii.member(jsii_name="putVirtualMachine")
    def put_virtual_machine(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__627554668bacefe9bb268ffc74a3a2ebda03bd47f1911ff6a3ece4a4e915a11a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVirtualMachine", [value]))

    @jsii.member(jsii_name="resetAvailabilitySetName")
    def reset_availability_set_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilitySetName", []))

    @jsii.member(jsii_name="resetLoadBalancer")
    def reset_load_balancer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancer", []))

    @jsii.member(jsii_name="resetVirtualMachine")
    def reset_virtual_machine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualMachine", []))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancerOutputReference:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancerOutputReference, jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachine")
    def virtual_machine(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineList":
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineList", jsii.get(self, "virtualMachine"))

    @builtins.property
    @jsii.member(jsii_name="availabilitySetNameInput")
    def availability_set_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilitySetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerInput")
    def load_balancer_input(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancer]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancer], jsii.get(self, "loadBalancerInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineInput")
    def virtual_machine_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine"]]], jsii.get(self, "virtualMachineInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilitySetName")
    def availability_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilitySetName"))

    @availability_set_name.setter
    def availability_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__522ad4d6c37e1a2cc2fbb367af85c2e04202f76c0f30a8f0d739e9aa62dca61d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilitySetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServer]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c41561d20b48a085985a6c2a76f4e5c67e09861475a0eba43c7d16e7ec0460)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine",
    jsii_struct_bases=[],
    name_mapping={
        "data_disk": "dataDisk",
        "host_name": "hostName",
        "network_interface_names": "networkInterfaceNames",
        "os_disk_name": "osDiskName",
        "virtual_machine_name": "virtualMachineName",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine:
    def __init__(
        self,
        *,
        data_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        host_name: typing.Optional[builtins.str] = None,
        network_interface_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        os_disk_name: typing.Optional[builtins.str] = None,
        virtual_machine_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_disk: data_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#data_disk WorkloadsSapThreeTierVirtualInstance#data_disk}
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#host_name WorkloadsSapThreeTierVirtualInstance#host_name}.
        :param network_interface_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#network_interface_names WorkloadsSapThreeTierVirtualInstance#network_interface_names}.
        :param os_disk_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#os_disk_name WorkloadsSapThreeTierVirtualInstance#os_disk_name}.
        :param virtual_machine_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_name WorkloadsSapThreeTierVirtualInstance#virtual_machine_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5780553542ef25c909e36410fb7646512a7cc8047b8fac56bc108c70bf3c584)
            check_type(argname="argument data_disk", value=data_disk, expected_type=type_hints["data_disk"])
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument network_interface_names", value=network_interface_names, expected_type=type_hints["network_interface_names"])
            check_type(argname="argument os_disk_name", value=os_disk_name, expected_type=type_hints["os_disk_name"])
            check_type(argname="argument virtual_machine_name", value=virtual_machine_name, expected_type=type_hints["virtual_machine_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_disk is not None:
            self._values["data_disk"] = data_disk
        if host_name is not None:
            self._values["host_name"] = host_name
        if network_interface_names is not None:
            self._values["network_interface_names"] = network_interface_names
        if os_disk_name is not None:
            self._values["os_disk_name"] = os_disk_name
        if virtual_machine_name is not None:
            self._values["virtual_machine_name"] = virtual_machine_name

    @builtins.property
    def data_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk"]]]:
        '''data_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#data_disk WorkloadsSapThreeTierVirtualInstance#data_disk}
        '''
        result = self._values.get("data_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk"]]], result)

    @builtins.property
    def host_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#host_name WorkloadsSapThreeTierVirtualInstance#host_name}.'''
        result = self._values.get("host_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_interface_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#network_interface_names WorkloadsSapThreeTierVirtualInstance#network_interface_names}.'''
        result = self._values.get("network_interface_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def os_disk_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#os_disk_name WorkloadsSapThreeTierVirtualInstance#os_disk_name}.'''
        result = self._values.get("os_disk_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_machine_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine_name WorkloadsSapThreeTierVirtualInstance#virtual_machine_name}.'''
        result = self._values.get("virtual_machine_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk",
    jsii_struct_bases=[],
    name_mapping={"names": "names", "volume_name": "volumeName"},
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk:
    def __init__(
        self,
        *,
        names: typing.Sequence[builtins.str],
        volume_name: builtins.str,
    ) -> None:
        '''
        :param names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#names WorkloadsSapThreeTierVirtualInstance#names}.
        :param volume_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#volume_name WorkloadsSapThreeTierVirtualInstance#volume_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d63765bbadfc0af69c2cabc6fccba6fb41f0557dadfa73d320f6fc4348cf241b)
            check_type(argname="argument names", value=names, expected_type=type_hints["names"])
            check_type(argname="argument volume_name", value=volume_name, expected_type=type_hints["volume_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "names": names,
            "volume_name": volume_name,
        }

    @builtins.property
    def names(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#names WorkloadsSapThreeTierVirtualInstance#names}.'''
        result = self._values.get("names")
        assert result is not None, "Required property 'names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def volume_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#volume_name WorkloadsSapThreeTierVirtualInstance#volume_name}.'''
        result = self._values.get("volume_name")
        assert result is not None, "Required property 'volume_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDiskList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4d451aa2bb9eceec58810fc20e3e13952177a9812e313d549a4af88467f0ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b9705ba49496c3343161922f02f0d7a355acd0412c054a3a8485f5cf4318e0c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3512c1aa70e0abc456686106295a19a084f9b45a5491b1f25d4f68c443bae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe7b4977d713c6566cd99f9316c1fb265e676105e88f4ca6fb6b2a5ff71e5123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e8186f771cb16aa80e8891ff21f9f87d8d3cb6f59e0fae8b41af036950ccdc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc97c6046baeec9148598828c1279145d6551dc57a5eef2c17bc835b2b3ec1cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDiskOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__688f45ee72792e114e7687ac593f595e682f1158de1e05ce5e015a869eeef694)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="namesInput")
    def names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "namesInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeNameInput")
    def volume_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="names")
    def names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "names"))

    @names.setter
    def names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47fe3662e2d622aa86dc51ba449f8f78b2ceb9ed8e3607da8355f6cb4a734a07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "names", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeName")
    def volume_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeName"))

    @volume_name.setter
    def volume_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f44a483cd135f801384a2eeec1ef053d7ea2e830836cfe84585474c6116c9255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd54a4fbda72076ff5638e75bf9ec5a8bad75ef102249e6040c4536188468115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee21a707bf17263a789f677d4720186e2a50f16962974a76751b0c2f0f0e4486)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b08485ce846a7236197d7ef3586b65336cd15aab5308775290f32b47cb8e28ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__131e8c1c3bcdc6ea84bee8dc7459f5549d738207fa7c52ccc957a7f0bdc4c6f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__899bf00a6f8be4198c8639d9bc7bf7b6bb388d6e0903a6b771f148b386500048)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da44d41ba8b411868dd62a063cb774081b64bbfd5110e652adbd236cc6d0daca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857eb95a10d8158db8c636305155fc777c8675ffd9cee6604f031a0edb7929ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad6fc6172b2aeabd2ec118102d410eb0a8bf4897cc5272fee3735b7909e24055)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDataDisk")
    def put_data_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74037575f9fbfc85bdeb8e2ed0268343e9fd3858fbf9304148ec34027b6c2fc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataDisk", [value]))

    @jsii.member(jsii_name="resetDataDisk")
    def reset_data_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataDisk", []))

    @jsii.member(jsii_name="resetHostName")
    def reset_host_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostName", []))

    @jsii.member(jsii_name="resetNetworkInterfaceNames")
    def reset_network_interface_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkInterfaceNames", []))

    @jsii.member(jsii_name="resetOsDiskName")
    def reset_os_disk_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsDiskName", []))

    @jsii.member(jsii_name="resetVirtualMachineName")
    def reset_virtual_machine_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualMachineName", []))

    @builtins.property
    @jsii.member(jsii_name="dataDisk")
    def data_disk(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDiskList:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDiskList, jsii.get(self, "dataDisk"))

    @builtins.property
    @jsii.member(jsii_name="dataDiskInput")
    def data_disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk]]], jsii.get(self, "dataDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceNamesInput")
    def network_interface_names_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "networkInterfaceNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="osDiskNameInput")
    def os_disk_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osDiskNameInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineNameInput")
    def virtual_machine_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualMachineNameInput"))

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f805383c51ce5b42088aac7d2f7a4492d50c8d7c9a74a4ad7d92295ff04523c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceNames")
    def network_interface_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkInterfaceNames"))

    @network_interface_names.setter
    def network_interface_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d1ef13fb59ee83764c415d648c998732ebde7f62b32b675aa852c5768025626)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkInterfaceNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osDiskName")
    def os_disk_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osDiskName"))

    @os_disk_name.setter
    def os_disk_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d00c9fdb1f4339d781294b9133b53f33f8c6df986e17441fef0e5414181e7d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osDiskName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualMachineName")
    def virtual_machine_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualMachineName"))

    @virtual_machine_name.setter
    def virtual_machine_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10fb765985d63af6ed506230b3639beff23accfb082e9e7170c40a437d71a7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualMachineName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ce619d1002dce953a4d085a6bd697366f0e3f5f29f0bc34042545315bb46ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4caad0986ff070748abc7426bf4a5c04c11037b155efdf6d0053586fd0384dd8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApplicationServer")
    def put_application_server(
        self,
        *,
        availability_set_name: typing.Optional[builtins.str] = None,
        virtual_machine: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param availability_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#availability_set_name WorkloadsSapThreeTierVirtualInstance#availability_set_name}.
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine WorkloadsSapThreeTierVirtualInstance#virtual_machine}
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServer(
            availability_set_name=availability_set_name,
            virtual_machine=virtual_machine,
        )

        return typing.cast(None, jsii.invoke(self, "putApplicationServer", [value]))

    @jsii.member(jsii_name="putCentralServer")
    def put_central_server(
        self,
        *,
        availability_set_name: typing.Optional[builtins.str] = None,
        load_balancer: typing.Optional[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param availability_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#availability_set_name WorkloadsSapThreeTierVirtualInstance#availability_set_name}.
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#load_balancer WorkloadsSapThreeTierVirtualInstance#load_balancer}
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine WorkloadsSapThreeTierVirtualInstance#virtual_machine}
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServer(
            availability_set_name=availability_set_name,
            load_balancer=load_balancer,
            virtual_machine=virtual_machine,
        )

        return typing.cast(None, jsii.invoke(self, "putCentralServer", [value]))

    @jsii.member(jsii_name="putDatabaseServer")
    def put_database_server(
        self,
        *,
        availability_set_name: typing.Optional[builtins.str] = None,
        load_balancer: typing.Optional[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param availability_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#availability_set_name WorkloadsSapThreeTierVirtualInstance#availability_set_name}.
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#load_balancer WorkloadsSapThreeTierVirtualInstance#load_balancer}
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#virtual_machine WorkloadsSapThreeTierVirtualInstance#virtual_machine}
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServer(
            availability_set_name=availability_set_name,
            load_balancer=load_balancer,
            virtual_machine=virtual_machine,
        )

        return typing.cast(None, jsii.invoke(self, "putDatabaseServer", [value]))

    @jsii.member(jsii_name="putSharedStorage")
    def put_shared_storage(
        self,
        *,
        account_name: typing.Optional[builtins.str] = None,
        private_endpoint_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#account_name WorkloadsSapThreeTierVirtualInstance#account_name}.
        :param private_endpoint_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#private_endpoint_name WorkloadsSapThreeTierVirtualInstance#private_endpoint_name}.
        '''
        value = WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorage(
            account_name=account_name, private_endpoint_name=private_endpoint_name
        )

        return typing.cast(None, jsii.invoke(self, "putSharedStorage", [value]))

    @jsii.member(jsii_name="resetApplicationServer")
    def reset_application_server(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationServer", []))

    @jsii.member(jsii_name="resetCentralServer")
    def reset_central_server(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCentralServer", []))

    @jsii.member(jsii_name="resetDatabaseServer")
    def reset_database_server(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseServer", []))

    @jsii.member(jsii_name="resetSharedStorage")
    def reset_shared_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedStorage", []))

    @builtins.property
    @jsii.member(jsii_name="applicationServer")
    def application_server(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerOutputReference:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerOutputReference, jsii.get(self, "applicationServer"))

    @builtins.property
    @jsii.member(jsii_name="centralServer")
    def central_server(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerOutputReference:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerOutputReference, jsii.get(self, "centralServer"))

    @builtins.property
    @jsii.member(jsii_name="databaseServer")
    def database_server(
        self,
    ) -> WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerOutputReference:
        return typing.cast(WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerOutputReference, jsii.get(self, "databaseServer"))

    @builtins.property
    @jsii.member(jsii_name="sharedStorage")
    def shared_storage(
        self,
    ) -> "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorageOutputReference":
        return typing.cast("WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorageOutputReference", jsii.get(self, "sharedStorage"))

    @builtins.property
    @jsii.member(jsii_name="applicationServerInput")
    def application_server_input(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServer]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServer], jsii.get(self, "applicationServerInput"))

    @builtins.property
    @jsii.member(jsii_name="centralServerInput")
    def central_server_input(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServer]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServer], jsii.get(self, "centralServerInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseServerInput")
    def database_server_input(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServer]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServer], jsii.get(self, "databaseServerInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedStorageInput")
    def shared_storage_input(
        self,
    ) -> typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorage"]:
        return typing.cast(typing.Optional["WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorage"], jsii.get(self, "sharedStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNames]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNames], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNames],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de6eec62ee36a330fef3f07a1b951dbfe8c2d745be2e59c5c81c808f227491d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorage",
    jsii_struct_bases=[],
    name_mapping={
        "account_name": "accountName",
        "private_endpoint_name": "privateEndpointName",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorage:
    def __init__(
        self,
        *,
        account_name: typing.Optional[builtins.str] = None,
        private_endpoint_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#account_name WorkloadsSapThreeTierVirtualInstance#account_name}.
        :param private_endpoint_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#private_endpoint_name WorkloadsSapThreeTierVirtualInstance#private_endpoint_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20791ed00181511b0578f3b0c2b9e3ff57ef7a100e859c91e022158c36d8f640)
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument private_endpoint_name", value=private_endpoint_name, expected_type=type_hints["private_endpoint_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_name is not None:
            self._values["account_name"] = account_name
        if private_endpoint_name is not None:
            self._values["private_endpoint_name"] = private_endpoint_name

    @builtins.property
    def account_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#account_name WorkloadsSapThreeTierVirtualInstance#account_name}.'''
        result = self._values.get("account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_endpoint_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#private_endpoint_name WorkloadsSapThreeTierVirtualInstance#private_endpoint_name}.'''
        result = self._values.get("private_endpoint_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorageOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cded6fb9d967f38b97bcc9c0d7e9bb2610a29cb7fda33f6c45f1f139549de8ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccountName")
    def reset_account_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountName", []))

    @jsii.member(jsii_name="resetPrivateEndpointName")
    def reset_private_endpoint_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateEndpointName", []))

    @builtins.property
    @jsii.member(jsii_name="accountNameInput")
    def account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="privateEndpointNameInput")
    def private_endpoint_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateEndpointNameInput"))

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a852ea21ac01766e235d23589577d439780e3d03c9ab1bfd748cddca54a84fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateEndpointName")
    def private_endpoint_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateEndpointName"))

    @private_endpoint_name.setter
    def private_endpoint_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f84180fac9f724acc606c499ca9989b379208fe2e51dcd378bc101d2fa2fdbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateEndpointName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorage]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf09937423f988b2aa5e246eb20169be8a6b7cc2a6a8182128555c49089b355f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMount",
    jsii_struct_bases=[],
    name_mapping={
        "resource_group_id": "resourceGroupId",
        "storage_account_name": "storageAccountName",
    },
)
class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMount:
    def __init__(
        self,
        *,
        resource_group_id: typing.Optional[builtins.str] = None,
        storage_account_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#resource_group_id WorkloadsSapThreeTierVirtualInstance#resource_group_id}.
        :param storage_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#storage_account_name WorkloadsSapThreeTierVirtualInstance#storage_account_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__490bbc7228d427121472ecabe3f997012cd7cbbca31fe71490e3b62fd118e392)
            check_type(argname="argument resource_group_id", value=resource_group_id, expected_type=type_hints["resource_group_id"])
            check_type(argname="argument storage_account_name", value=storage_account_name, expected_type=type_hints["storage_account_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_group_id is not None:
            self._values["resource_group_id"] = resource_group_id
        if storage_account_name is not None:
            self._values["storage_account_name"] = storage_account_name

    @builtins.property
    def resource_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#resource_group_id WorkloadsSapThreeTierVirtualInstance#resource_group_id}.'''
        result = self._values.get("resource_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#storage_account_name WorkloadsSapThreeTierVirtualInstance#storage_account_name}.'''
        result = self._values.get("storage_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMountOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1c343666cfa33e2a422efd7a33d0521929aaf358cba95f2c2dbbc281205d1a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetResourceGroupId")
    def reset_resource_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroupId", []))

    @jsii.member(jsii_name="resetStorageAccountName")
    def reset_storage_account_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountName", []))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupIdInput")
    def resource_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountNameInput")
    def storage_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupId")
    def resource_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupId"))

    @resource_group_id.setter
    def resource_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b6835d441d4e5babe464d0840afbdb53f8a84309a9f85e5b986c4c3fc76c894)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountName")
    def storage_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountName"))

    @storage_account_name.setter
    def storage_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d52113814dc83352782ced381193ca68eb275e29f9feca4354b56128c3cb7f60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMount]:
        return typing.cast(typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b93952e3a1c721d84c06c08d9031eefe22d8ef59abc62e42fda220b29994e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class WorkloadsSapThreeTierVirtualInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#create WorkloadsSapThreeTierVirtualInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#delete WorkloadsSapThreeTierVirtualInstance#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#read WorkloadsSapThreeTierVirtualInstance#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#update WorkloadsSapThreeTierVirtualInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26e92bed51d8c26dc98520bace903c06987b635f50713019bced0c51c1868b5b)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#create WorkloadsSapThreeTierVirtualInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#delete WorkloadsSapThreeTierVirtualInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#read WorkloadsSapThreeTierVirtualInstance#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_three_tier_virtual_instance#update WorkloadsSapThreeTierVirtualInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapThreeTierVirtualInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapThreeTierVirtualInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapThreeTierVirtualInstance.WorkloadsSapThreeTierVirtualInstanceTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df5d6295804012f43a530733f03a0b991f105319c7ef97f3094cbc2f51e21d60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5258d7a7aa63d92b32b4614fc1518a21543483470618f93efadcb54571a5f461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ffcafc814f45139b659b09131c88c0bf8374f17bcc835b313a876bccdf10b8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__293df0c0f1591cb414de675c4e56fe95c195f78ad598c09242d355b0b419f2d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3a8e8ce8f62a5c3108354d8875017c35a1f031304f95838be4bd5c419c3f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e1474a2530f3749fdf1aac309228ed93a09633617ec53aa86544f1cdccde772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WorkloadsSapThreeTierVirtualInstance",
    "WorkloadsSapThreeTierVirtualInstanceConfig",
    "WorkloadsSapThreeTierVirtualInstanceIdentity",
    "WorkloadsSapThreeTierVirtualInstanceIdentityOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfiguration",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfiguration",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImage",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImageOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfile",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfileOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfiguration",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfiguration",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImage",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImageOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfile",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfileOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfiguration",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfigurationList",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfigurationOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfiguration",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImage",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImageOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfile",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfileOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNames",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServer",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDiskList",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDiskOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineList",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServer",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancer",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancerOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDiskList",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDiskOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineList",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServer",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancer",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancerOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDiskList",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDiskOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineList",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorage",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorageOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMount",
    "WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMountOutputReference",
    "WorkloadsSapThreeTierVirtualInstanceTimeouts",
    "WorkloadsSapThreeTierVirtualInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__fdfa6a36d5f8d2cda30ef1b557a6010e16aa4c0b0f0e51fc0d2386e07f78cfa7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    app_location: builtins.str,
    environment: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sap_fqdn: builtins.str,
    sap_product: builtins.str,
    three_tier_configuration: typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[WorkloadsSapThreeTierVirtualInstanceIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_resource_group_name: typing.Optional[builtins.str] = None,
    managed_resources_network_access_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[WorkloadsSapThreeTierVirtualInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14bde042042bb6fc23832c3873ff2dc0279656b6857951b716964050215d4c0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777076b8675f505bab929a97108bb7d6388d9d615667bdadddedd40e58c516c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1000b5ea13668428dff1bef7f42ede145884ca26b28578eea387d1d463793285(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069022931f64f8d41dd5a5d35f69022936511b252643ded9b8288aa23a8dc6da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df926a48687fcf0f12cbc7605356740e04bccbfaf1e28d70bd814545908423e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef2131e6fd64917c3728439f764cddaa8f1543afd0900501d5d8385f77a8e336(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__effb27f016d632165c6c988c09ea4f43007c981bff6b8494239475a04b025a94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864034fe0389ed0ddf828a90e7d5c3692f02d75a8df31139404f44671f374dab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4949909849e91d387643c8f4410df8b9de1260e81f95007475d6ca9b82672aea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02675678340ffd85856cf59ec490b15f9528e0f1416bf19bab08b134223f5580(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5615ee020c3a87341f20b66566040c9739d981398f6a668fd35d69bfaa486d4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83dcc9356073839721301df57d30436b3304f37f6b5bf2830fb4b99b05c50108(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d8db2f9430a436f6c93dac43ef08a712adea1b9630f8a9b56e9e8ddf043cad(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_location: builtins.str,
    environment: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sap_fqdn: builtins.str,
    sap_product: builtins.str,
    three_tier_configuration: typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[WorkloadsSapThreeTierVirtualInstanceIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_resource_group_name: typing.Optional[builtins.str] = None,
    managed_resources_network_access_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[WorkloadsSapThreeTierVirtualInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2971667f78cf95069a3d81fc41eb69163f3074e9a9c688f13874e903f0e8408c(
    *,
    identity_ids: typing.Sequence[builtins.str],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4db8214a84892969b6a5517a3124985345fce6987f12e5395620ec012c6197e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0790a469ec4ee0002b4118747c217652fe4b60265e8c095b12f726066904e1b5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5843d15afe0e2d7a0da19fa147d31b6ce18769922654efbed5bd85461ed13568(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b8ec70276e31466bf4b4f52a8af77b04abce61dccd4dc1fb35c83d9a0ce7de(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e44b46aef0eb9bcf1f19334d1ab3c3f7324dd13fa24d1e5b1dbd67351dfee1a(
    *,
    application_server_configuration: typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfiguration, typing.Dict[builtins.str, typing.Any]],
    app_resource_group_name: builtins.str,
    central_server_configuration: typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfiguration, typing.Dict[builtins.str, typing.Any]],
    database_server_configuration: typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfiguration, typing.Dict[builtins.str, typing.Any]],
    high_availability_type: typing.Optional[builtins.str] = None,
    resource_names: typing.Optional[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNames, typing.Dict[builtins.str, typing.Any]]] = None,
    secondary_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transport_create_and_mount: typing.Optional[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMount, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f76b5d01e374c8aa2d1e18a7ba17618a52b09f72d2fc532f0f1214c003ac7729(
    *,
    instance_count: jsii.Number,
    subnet_id: builtins.str,
    virtual_machine_configuration: typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfiguration, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f28581289a979d5ee48367a44e6923d03bc3042bb509b8a3b9b2ec2d741bb71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9afe951b50b3c606a62b956c6ecb7fde51fd1227590a30f444c4f9feae579433(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70f05a0bda28a3eda634a97d896d3f5e0f4ff2750537be780b4af0c6b22e86f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631b6094af24bb7ce29d92b871121ad284e4fed69de6fffdc327f0005004bf40(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__263abe3b6ddcb87ad0ef510aec101d5ed51dd8c8e503386f0780a68392303d84(
    *,
    image: typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImage, typing.Dict[builtins.str, typing.Any]],
    os_profile: typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfile, typing.Dict[builtins.str, typing.Any]],
    virtual_machine_size: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd270f98d2c7f907ba67547dbd9abf1a40c33ab33363eda624984642cee5212(
    *,
    offer: builtins.str,
    publisher: builtins.str,
    sku: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e1616d97cf8956fa8b8bd5140edf05e0f8dbc9238e18604dff9b4f07e2ab56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad3e186c10f3acfb2a6deba731d08e4db52897dc3a985df77af55db858a581b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e8f7cf42a6c3903a6955119204f9ca64ab428cda1b375342f7e8d9abc458b56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5ae0fa021853fc77ccb30e8dfacfd130a7769d611c45827cf17a6870cacfe00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2226ebd4d902ccc6e8fd07046acf7f83e3f40f670f9d0461c2915a79cb05c199(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d596ce8a6de6e6642cf1de56d3d7c0cf5a391ee81fd7ceb14a5b100692ffbd8f(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__107843aa13f0e9404b71d23693c15eccc03d3944216c4ce941b1995436f98f0a(
    *,
    admin_username: builtins.str,
    ssh_private_key: builtins.str,
    ssh_public_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce1cdf57475cb310c5c32e7efe738c0540531102680a39e12bd674f81345044(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f726e27d819d0cb72c6b981a305a879174e131069bde5e5c4de22b8d491f9922(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d266050ec4dcb85fbf66236cfad8559726483130e6a846e5f3f27f424ade21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cfd497c08e925edab0ce2723842edc464183f7952c414cb5184520858b71e1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b4873106d3b7fa979ca54e85da2299653aa4a9c86fc8d8fe847e2ae9228d0c(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfigurationOsProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3c6a41dc73534b9f40728c3060a3ba9b131445f98f643bda019d27738b694f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c7dd83bf56d4dd4c3fe8b80ea2a87acf44c1a8323dfb9782c2714545cb1dd8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0373cf71fb41def783789415246f709caf839860d361062fec05773709f819(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationApplicationServerConfigurationVirtualMachineConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ac3dc3916ce65ade807ea54b52ee647b445dcfcec2904cdabfac7938489040(
    *,
    instance_count: jsii.Number,
    subnet_id: builtins.str,
    virtual_machine_configuration: typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfiguration, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc838f07c76095e9aa675ab732d96d730f6709daa72dd0f68c7c3a145304465(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65c41335778c896ead3cee941639622dfa636e1308045b683870f574cce5b00(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c2fe8d8659f1d2c9536f63d5c7100235c30e7716ddae1e578da7159dd6cd6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1917c9ca51898019ed9bce5688e463f500a2dfbbf9de99898a4e0ed535daa02(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d298b6b4a7cee03955caed2ce08a9cbc1e085986b7e0afd4c8e4a02ba85e2c9b(
    *,
    image: typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImage, typing.Dict[builtins.str, typing.Any]],
    os_profile: typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfile, typing.Dict[builtins.str, typing.Any]],
    virtual_machine_size: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7945693ad1c2449011dfab442f0f94d7e46199794ee8db763930a6c982c52e9e(
    *,
    offer: builtins.str,
    publisher: builtins.str,
    sku: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db893328795cfdc19bad10cbcd94798f7f00219078bb06677642b2343bd0b0ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46466264c4cc89cb60e2b233f9686e487204606b0c22fc4c92433f0739ac60f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4afc9d234a9d5b6e8c5d4686d36c0f21fbe79362be767d4b8adcbc7f0fb99a78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bda37e030c9452c37187cf3ea76ee67f6e3d6fee7d7f52110ab2ffab81460d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ed83c6a6779aa3e892f2f3d1c7e4bc9650c9c54ca535d0c7d74717004667b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030e5ec24ed0403d813d18fe1d7c6fa81a89d30685f069c19093e3f0bc3d878d(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d44eccfbdc56409b13a84f03467a6307553f62d106b03e7fada52856f525de(
    *,
    admin_username: builtins.str,
    ssh_private_key: builtins.str,
    ssh_public_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48aec87befa5770ab8e6bdd00c931d1727284fb741c9c521b37d4f166cc7ab7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__172613268e4f9876bf9494c3e73618460caa71f28bce9e2c938943f2b5973200(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e222a118902fc8ce58a7838752581d5051481ded4cb4e6ee5608c49ed75d372(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9689ac795912193e546e286c5c320b38155afec985accbd43d142afd844e82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43e61acba2e13832a60dc8670ff4984523a765bedc80a2fbbda6aec4414542d(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfigurationOsProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e94b8c7a80db526358a713095ac3e00da1febca670f3ca67ba03941d8e0395(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc3ec4c51f5af181ba627016d75306abca39dc0a5d7e7beb2b8faa6ebcac99d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821650fb00c9fc44f359da0cc8a4c0d60dc778ced5c4b659e8adecc7a72494db(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationCentralServerConfigurationVirtualMachineConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f100608658a19fa7cd931d6706eaaa4692abe56e3b053750ff038be4daf31514(
    *,
    instance_count: jsii.Number,
    subnet_id: builtins.str,
    virtual_machine_configuration: typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfiguration, typing.Dict[builtins.str, typing.Any]],
    database_type: typing.Optional[builtins.str] = None,
    disk_volume_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f5dc65b90fbb808b52bb5b6d1732321cd7e3f05b4a35123f55e1b45994c654(
    *,
    number_of_disks: jsii.Number,
    size_in_gb: jsii.Number,
    sku_name: builtins.str,
    volume_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73ce010a944509ea365d9cc39664375571698960def9a1245957012f572177e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4296a830b9f468fc3d7dc626d9bb2369ae3443e06382c88ea361f551717ee0db(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b53633cd0dc0331be156a6691729e9ccea4b038ec5fc6133ab710b298760c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a86a226ea025cb75dbf2caffbeeddfca66794b5214f12ce7fc4e06347dc7ce3f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1d7a9f289db806c6f4cf6d02317a096e5773ed8b3994e77cdb52448833d18e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f7e1dd23f7474be90dd3cc72d74d48cf349131d14b1dd04e9dd559cc13ba0b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11d02c7f6101219e14e304c0024b417f470a8909b5cf95c566b1aceb983facc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3f33b3f20bdc0da9187ab20136bee5dc33371fd51f21c03afc1fd2c16da160(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151c13dc59acdbe4507a6d2314fc5fe69a35123ae413e58d7639d8dd3f2af56d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9390847c56999ea3d15c4522a7a2a5544e0ee09681c82856efdc1350ebe581bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7b6a41b415a4f9b6b50a2441d2381b48c1f6bb33b480fa4b6cf90d62e87209(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ae4b77406f5ce827fa288b783c4c4d37facdd9ef327a1671f3f0c94b673bdb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a191c507f15bb9ee9e1efc490b9a36202c3b17aa1e8621d0129c3b760fe494bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eff0778afbb0ef1237d974aff6e124bc4ab743e4c9a45aaac76817b39fed933(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationDiskVolumeConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6860ffba26b0fae4892a8027274e60d435195703f077452d7264734784df5ca9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07814d7f43e3181726ce1e477b8c80dd613935689eb96b0f242f007e2f57dd01(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6088a938c821e039d9e37d26133080fb9e3dceb465232cb34d678853f8d6cc08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7708699b6b1916cc9eeb6d758b22f328c9695462cb9eeb36fec8a1cd13b9f270(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77fc7182677f32e5d587ca03f64b76eeea4792505a8551e25c488cc70dc3684d(
    *,
    image: typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImage, typing.Dict[builtins.str, typing.Any]],
    os_profile: typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfile, typing.Dict[builtins.str, typing.Any]],
    virtual_machine_size: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48b23d8487c2be126128819ac919fa57a44869591ba843a3fb11d4d4d8cc0393(
    *,
    offer: builtins.str,
    publisher: builtins.str,
    sku: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c77bea3e67f91d6d753db8110ce08b2838187b43a678fef4c07bc76c706c31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac73ededb93de8808bfa31b12208c6860d17a3530baf97b0cae3960dd5860cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d06f9df3851b9387ea3cd94d2728be0de1c6c844f8a2660aa2a71721ee6184(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be112590b25d3246fa810b03d7b9ed340766a5a9a50308b2648a92439eef60a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__495b2f22ef83bcc253b18ef81d1f8dff7856731be84ad7860ae8aaca25a1a01b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d0aa70e6e02d570e853be67d0df59645068e671a6a5c8a9db6184e613c12aa(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a4b788a284c2bb74caf0f4421a0aa7956f5f6e97c11f9621bc4ba9bb5eed35(
    *,
    admin_username: builtins.str,
    ssh_private_key: builtins.str,
    ssh_public_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8386f0bd340de39bfe0f12e194818fb1284ed956f81e340cf9f270a1a80a84a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8f164e07172fe9138a440854dcbb5bf4545b26af0504ff899c590f683e42a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da562511c9c67c1e0a502cdc9570469c91351a4acf93d824d70a03f60bbdb84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f8ccb2769f09eb05a04ee0bd7450398da6a7c8c811c77f4fd8afd6ccae5a53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__534e46ba81581bb21671b9896c9ece200dea68a8951caa6d5bc33d913f584534(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfigurationOsProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28c7891a605959255c54e34fc0f82729451d86a0fe8639de5d5fc7b8da2cb12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37942a45647842d4fcffb3bb0ac60ba25c804599b4fb522050f40dcf6f8efbf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1123affe4d3bd146ef800c096da94408afca9eeabe453220f74cc9f68e6c3d7(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationDatabaseServerConfigurationVirtualMachineConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2ba556c3b73acddca05b5dad8d56bcbd769aeccf712b222b512c2f498ea2118(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4257e360138f60e09c83519836acface9cbb0cb9da91e7bc2f6544594a911e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e63446bb0bebfaf2aaccbd1c6777a792e2559b7d7674e570c86ef28d3363a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43b18d06bc6c33e2c6e874480e41b8b36aaa59d29dbb73a7fb0651b0d80ef35(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3017ad1d7c3348b877bb3adf583c57fe48d777a249d738e9c013dd3dc519497e(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e71c4c7b72dfabd1bcb5639ebbd44f22751f3833c2bd686d3911d61ca88e8952(
    *,
    application_server: typing.Optional[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServer, typing.Dict[builtins.str, typing.Any]]] = None,
    central_server: typing.Optional[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServer, typing.Dict[builtins.str, typing.Any]]] = None,
    database_server: typing.Optional[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServer, typing.Dict[builtins.str, typing.Any]]] = None,
    shared_storage: typing.Optional[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorage, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5684ef52c9ea09657b3938e1b349cbea0f5c4c0555a733f2c1d06193611de07(
    *,
    availability_set_name: typing.Optional[builtins.str] = None,
    virtual_machine: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d034ca891c29df2813ffc4104faf5bb2e8dccdd91b5d0096e9e77a2d40db6c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da75d05412efb549b69b806e902272448fbacdfabadee59b4de38530d0e93193(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3595d365e32283e1775fc7850132e515b98868b67c3ce534a5348fe5e9be86bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5f7919d45acd76f0a8ce1d4b75af0acf8a8b5c556a2207b23c25bc6cb2bffa(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc20761971e61b56e27619c0904bffeb0873600ca43334614996759ecbcbd711(
    *,
    data_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    host_name: typing.Optional[builtins.str] = None,
    network_interface_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    os_disk_name: typing.Optional[builtins.str] = None,
    virtual_machine_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993c62a3f7fab97789310191ac6481ca41617a4b994cfe08ca7cf9775b6c459d(
    *,
    names: typing.Sequence[builtins.str],
    volume_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83bad5286a7b5187da21fa9343f2d78c13a242f5c1dc0d4eea6ac8900ab9e49e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0d58c9abd5196911c9386fd536cf50601c881928c293d9affdf6d1d76182d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa89bf95096d3fc1f106031bc0f63522749c956dd6b05f14ddfcf5c77ad41c4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777c6ea0b44448261555e51b439f3f39f62dd8f44bf381c952737f78419c6a08(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c95931d07413d98883c10c35d0e123de99d3567df50f7bae6cc53ee701b6d765(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b810a38cf2608d6f97b54ffb65a5c68af7c6442ba228ccfc79e45b543f1b17c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a4b40200a602fa736c65f3593b00f63c0ab6a3e805c87748c6ac15eb60c8dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee5d226a831c67c827dae8f46cec80e59315f5b1c27c7a8aef28a7c8bb85b31a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933ccaacad4d6faebd71af8357ccd28c2a50f60bce60d5e424d8888585830fa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fddc75c90c5134da0fcba4c37b0aea9ed5744eea70fa460b8a2fd0e1b3e08ce9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6245d183ceb585bd215ea35217f913ebc75ef904b1a5cf531c8d349771408f2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2731aa0b78bc9725a943945942ece00a49fc33a1f5b35faa7ca140ca63f15652(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0697ac0902e7fe0f2663af7dcdd32ea898f8a36ac283595d00380c7891a09a9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d96cc336d8040c2e6e8937039dde15f6dbb0d7c59781ee6a61ac8f015d85433(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__790f923f538c4db927a265d58f84b379e0e8ab41fe2d73837adb8519a070dc82(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921697e5540376d74dd44e2a6341cd0e7ddf42bbf391b5b731bb8ddaac6c9faf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc296c06b925c91761ef126cd1274af86439c6b7fe6d37db77b5d4f8666b4f0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__988f350306766a26773171be6af2aef078e212fbb4d8c570c2701f267e91f7d6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachineDataDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2eb166356d8f378f4241532c6d06d4cd126a752152b4ff951dc34bd7fae49b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91706935fc42aac82838cfdc38211e3fc8fcc84478fa0b0241d7bd6a9ce86540(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c9d3cc6bef6e17049a41d2ea5116b7d47b6533d843af0a454f8ec8a4c42ee5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08396adeb098d993e1071078c37cfbeb2adadbe5c8e019b5a2021289fae9d4d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2d99d15bc9aaef81e21960415bda6232df4524c41a74a33fa76adfddcbd2ec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesApplicationServerVirtualMachine]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0664e6eeae1043e17b6464b94466760225183562ba774169377c9892a8e951(
    *,
    availability_set_name: typing.Optional[builtins.str] = None,
    load_balancer: typing.Optional[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e7b05ebe3b5a905121edaa9074bd425d84cf4017b38405db7658aa89752d35(
    *,
    backend_pool_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    frontend_ip_configuration_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    health_probe_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b942f8444c1573af0c20f3d43dc81a2ea363c105be47eac8bc044f535834287(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7596e56b4a77812eba84b4eb9a2583986a36720abf25f82042a604ea7f6b43(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0dcc4c0e170ea18f65778e003d086ecd8083194646495cdd615890b8d89560a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03fe0b5e12066e2411314b0ce76ef185a84cbbd30120eade6d8fd17c6287a16c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b5e224e892670842e19bfe33858a06155b787738187349b1b3d00fad0178d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6b82975271de266e49dc0c0b1205a195a24a0a7dcd56d136fe9e3bec1014b9d(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerLoadBalancer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4991e1f2597765e6a6de639e8a32ffc8d492617091af7cab21c7a6508a9116c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a793e62ede6658957d8464bfc50390ab5cc81e74b96ebd3a7a3c388556b2c71(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35c8fad159555928013e8a674630f7bbe0b0ec456c4cc65e9570dd834f2dcbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978e2913de397da40760e95b258a7bc1a850d5a02e80e875f3e7faae4f1a7792(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f7e037e4c3a5da53394772c5c1a598d0a445793df4e0cd60d5815f2ebb7c0f(
    *,
    data_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    host_name: typing.Optional[builtins.str] = None,
    network_interface_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    os_disk_name: typing.Optional[builtins.str] = None,
    virtual_machine_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776757a3d78aa5dd77e0adf78c3fd0ab8ec1353c4c89214c320bc29ded60b246(
    *,
    names: typing.Sequence[builtins.str],
    volume_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5a09e85c51435349f1e32dedb323b8114eb0e880c49944e8e958c612d6c092(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530e561b1c0491d890138740e350c490fc4497c47af6df48d10f1156e2b09bc8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3380741e74e3f6521789951ed203bd55316f85549d1fb3f7cd1edd7e4b4f3abf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844aa0cb88b87cdf791764ee15a0666be1ef7397241bdda3060451a816b385c2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a63f41f678c81c0d14d92c309af803c255105e29b57c191f48ad30586400d27(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b1760c3229db44e4911d30948cc09d4bc29063a7f4ce86863883de39eea3fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__335aee7c8dc747037cd6fe870f7dc6473775f283275af72f5a68916374af45a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae728efc54b274c8ddaca748373afb04e9509230694d586bd8aabee12d62f1e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cb32256389b86536b8cbed4b1d72a8334b16bd82e0f9c7637bd9c1418072339(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc8e2faa28406fc31aa2acd6c2cd779aeacd1b41c37eabbfa63a64dfd871819(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__124b9073811e8a49895eda2813b64457f9ba427221d62626ab2e92bfbc82be5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dac4d4ddf6afdb93b7319f4a213a235099f982c313b9a4d68cae765c428e9701(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb73a62515b721b4981906cd152492376b246659bfebb303e489b1cd8f080a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b08294e0035d743198effff4f25a458fc3fec778e4ce9d5ae8e76ba7ac28a9f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d456636e66da3cd2d9bfd86c3529e00222c15a79109b5f86064557e3f0975570(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a349bc644b3f3682476ac8741c0bc5a28c20147990d50b35f926251f9e3897(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0961345860790411447044a6cb159033878115f47fe02bf0937780ac980b162(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34c1ecf18b3ec56df1ddb50b16d9091991640013bc3d0100db7ae7c1ae1862e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachineDataDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1491cac7298b5b9bccd786bd9cb39f261ced136e894fe9938f3f2bd5102a5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__454298aef440e38c3922615e1d9921eb061ee59bc8128bbcb73ff7fae0e06e8d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__564395f9688b3d67583ee6b8bfe350da29b94cd9e699b3b72ed829dffab82d8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd0d962d5ccd27344c62ca8275c9a9c8547b56e69fef71299f268e6e1f3e5b7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7768ddc824d5489e109e3f65e3cbc4557c60d6843288395c8e2b8f499705c52e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesCentralServerVirtualMachine]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883aeb439bf5e2eeecda0c5fd5f1459c32211c580ef072c91bae1a63ec98de99(
    *,
    availability_set_name: typing.Optional[builtins.str] = None,
    load_balancer: typing.Optional[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c03f558d4ca5176074a882a4077c0aeb13656ea5e6c3344b8bfedeedd68837(
    *,
    backend_pool_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    frontend_ip_configuration_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    health_probe_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b454df771ff196a17c5dc4d1ca2e71e142dba06037b122860b919fc05d6b424d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaec77adb4e188db6c3393d4bedeced46f6156ae0556990f5266b38ab72896d4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b79f781d2f6fe94e5a6c9f176fbb1daf35d862c47a714883e23577551178a31(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934d21e7caa9120e5b47443a84cfa042ebbdca2437819f20482b16de64f2a02e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3134ddc0c1d361c061fcc0299e9ea26f3d38364cffbe031ebce4ac1b7c7d5373(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71b0bae47e00eedac91380e65daa5a67d9693b540e2fc93f982e2b8c2bc6ba67(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerLoadBalancer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1028e771532aea32138d228ea7042e52e8e5372ca68cc5751c6edc53990c486b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627554668bacefe9bb268ffc74a3a2ebda03bd47f1911ff6a3ece4a4e915a11a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522ad4d6c37e1a2cc2fbb367af85c2e04202f76c0f30a8f0d739e9aa62dca61d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c41561d20b48a085985a6c2a76f4e5c67e09861475a0eba43c7d16e7ec0460(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5780553542ef25c909e36410fb7646512a7cc8047b8fac56bc108c70bf3c584(
    *,
    data_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    host_name: typing.Optional[builtins.str] = None,
    network_interface_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    os_disk_name: typing.Optional[builtins.str] = None,
    virtual_machine_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63765bbadfc0af69c2cabc6fccba6fb41f0557dadfa73d320f6fc4348cf241b(
    *,
    names: typing.Sequence[builtins.str],
    volume_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4d451aa2bb9eceec58810fc20e3e13952177a9812e313d549a4af88467f0ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9705ba49496c3343161922f02f0d7a355acd0412c054a3a8485f5cf4318e0c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3512c1aa70e0abc456686106295a19a084f9b45a5491b1f25d4f68c443bae0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe7b4977d713c6566cd99f9316c1fb265e676105e88f4ca6fb6b2a5ff71e5123(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e8186f771cb16aa80e8891ff21f9f87d8d3cb6f59e0fae8b41af036950ccdc0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc97c6046baeec9148598828c1279145d6551dc57a5eef2c17bc835b2b3ec1cc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688f45ee72792e114e7687ac593f595e682f1158de1e05ce5e015a869eeef694(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47fe3662e2d622aa86dc51ba449f8f78b2ceb9ed8e3607da8355f6cb4a734a07(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44a483cd135f801384a2eeec1ef053d7ea2e830836cfe84585474c6116c9255(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd54a4fbda72076ff5638e75bf9ec5a8bad75ef102249e6040c4536188468115(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee21a707bf17263a789f677d4720186e2a50f16962974a76751b0c2f0f0e4486(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b08485ce846a7236197d7ef3586b65336cd15aab5308775290f32b47cb8e28ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131e8c1c3bcdc6ea84bee8dc7459f5549d738207fa7c52ccc957a7f0bdc4c6f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899bf00a6f8be4198c8639d9bc7bf7b6bb388d6e0903a6b771f148b386500048(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da44d41ba8b411868dd62a063cb774081b64bbfd5110e652adbd236cc6d0daca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857eb95a10d8158db8c636305155fc777c8675ffd9cee6604f031a0edb7929ba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6fc6172b2aeabd2ec118102d410eb0a8bf4897cc5272fee3735b7909e24055(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74037575f9fbfc85bdeb8e2ed0268343e9fd3858fbf9304148ec34027b6c2fc5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachineDataDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f805383c51ce5b42088aac7d2f7a4492d50c8d7c9a74a4ad7d92295ff04523c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d1ef13fb59ee83764c415d648c998732ebde7f62b32b675aa852c5768025626(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d00c9fdb1f4339d781294b9133b53f33f8c6df986e17441fef0e5414181e7d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10fb765985d63af6ed506230b3639beff23accfb082e9e7170c40a437d71a7bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ce619d1002dce953a4d085a6bd697366f0e3f5f29f0bc34042545315bb46ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesDatabaseServerVirtualMachine]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4caad0986ff070748abc7426bf4a5c04c11037b155efdf6d0053586fd0384dd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de6eec62ee36a330fef3f07a1b951dbfe8c2d745be2e59c5c81c808f227491d(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNames],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20791ed00181511b0578f3b0c2b9e3ff57ef7a100e859c91e022158c36d8f640(
    *,
    account_name: typing.Optional[builtins.str] = None,
    private_endpoint_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cded6fb9d967f38b97bcc9c0d7e9bb2610a29cb7fda33f6c45f1f139549de8ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a852ea21ac01766e235d23589577d439780e3d03c9ab1bfd748cddca54a84fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f84180fac9f724acc606c499ca9989b379208fe2e51dcd378bc101d2fa2fdbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf09937423f988b2aa5e246eb20169be8a6b7cc2a6a8182128555c49089b355f(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationResourceNamesSharedStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490bbc7228d427121472ecabe3f997012cd7cbbca31fe71490e3b62fd118e392(
    *,
    resource_group_id: typing.Optional[builtins.str] = None,
    storage_account_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c343666cfa33e2a422efd7a33d0521929aaf358cba95f2c2dbbc281205d1a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6835d441d4e5babe464d0840afbdb53f8a84309a9f85e5b986c4c3fc76c894(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d52113814dc83352782ced381193ca68eb275e29f9feca4354b56128c3cb7f60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b93952e3a1c721d84c06c08d9031eefe22d8ef59abc62e42fda220b29994e8(
    value: typing.Optional[WorkloadsSapThreeTierVirtualInstanceThreeTierConfigurationTransportCreateAndMount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e92bed51d8c26dc98520bace903c06987b635f50713019bced0c51c1868b5b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5d6295804012f43a530733f03a0b991f105319c7ef97f3094cbc2f51e21d60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5258d7a7aa63d92b32b4614fc1518a21543483470618f93efadcb54571a5f461(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ffcafc814f45139b659b09131c88c0bf8374f17bcc835b313a876bccdf10b8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__293df0c0f1591cb414de675c4e56fe95c195f78ad598c09242d355b0b419f2d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3a8e8ce8f62a5c3108354d8875017c35a1f031304f95838be4bd5c419c3f13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1474a2530f3749fdf1aac309228ed93a09633617ec53aa86544f1cdccde772(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapThreeTierVirtualInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
