r'''
# `azurerm_workloads_sap_single_node_virtual_instance`

Refer to the Terraform Registry for docs: [`azurerm_workloads_sap_single_node_virtual_instance`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance).
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


class WorkloadsSapSingleNodeVirtualInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance azurerm_workloads_sap_single_node_virtual_instance}.'''

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
        single_server_configuration: typing.Union["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["WorkloadsSapSingleNodeVirtualInstanceIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_resource_group_name: typing.Optional[builtins.str] = None,
        managed_resources_network_access_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["WorkloadsSapSingleNodeVirtualInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance azurerm_workloads_sap_single_node_virtual_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param app_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#app_location WorkloadsSapSingleNodeVirtualInstance#app_location}.
        :param environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#environment WorkloadsSapSingleNodeVirtualInstance#environment}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#location WorkloadsSapSingleNodeVirtualInstance#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#name WorkloadsSapSingleNodeVirtualInstance#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#resource_group_name WorkloadsSapSingleNodeVirtualInstance#resource_group_name}.
        :param sap_fqdn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#sap_fqdn WorkloadsSapSingleNodeVirtualInstance#sap_fqdn}.
        :param sap_product: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#sap_product WorkloadsSapSingleNodeVirtualInstance#sap_product}.
        :param single_server_configuration: single_server_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#single_server_configuration WorkloadsSapSingleNodeVirtualInstance#single_server_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#id WorkloadsSapSingleNodeVirtualInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#identity WorkloadsSapSingleNodeVirtualInstance#identity}
        :param managed_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#managed_resource_group_name WorkloadsSapSingleNodeVirtualInstance#managed_resource_group_name}.
        :param managed_resources_network_access_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#managed_resources_network_access_type WorkloadsSapSingleNodeVirtualInstance#managed_resources_network_access_type}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#tags WorkloadsSapSingleNodeVirtualInstance#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#timeouts WorkloadsSapSingleNodeVirtualInstance#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf488d0bb9e807c3528010576f2ea2dfc963f228ed258b3711d1aec5265d82a0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WorkloadsSapSingleNodeVirtualInstanceConfig(
            app_location=app_location,
            environment=environment,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            sap_fqdn=sap_fqdn,
            sap_product=sap_product,
            single_server_configuration=single_server_configuration,
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
        '''Generates CDKTF code for importing a WorkloadsSapSingleNodeVirtualInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WorkloadsSapSingleNodeVirtualInstance to import.
        :param import_from_id: The id of the existing WorkloadsSapSingleNodeVirtualInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WorkloadsSapSingleNodeVirtualInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a27fcb4444c35b9927f50ce0fe8e8e28e40d185215331238ea9002095a53ed87)
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
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#identity_ids WorkloadsSapSingleNodeVirtualInstance#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#type WorkloadsSapSingleNodeVirtualInstance#type}.
        '''
        value = WorkloadsSapSingleNodeVirtualInstanceIdentity(
            identity_ids=identity_ids, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putSingleServerConfiguration")
    def put_single_server_configuration(
        self,
        *,
        app_resource_group_name: builtins.str,
        subnet_id: builtins.str,
        virtual_machine_configuration: typing.Union["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfiguration", typing.Dict[builtins.str, typing.Any]],
        database_type: typing.Optional[builtins.str] = None,
        disk_volume_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secondary_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        virtual_machine_resource_names: typing.Optional[typing.Union["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNames", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param app_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#app_resource_group_name WorkloadsSapSingleNodeVirtualInstance#app_resource_group_name}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#subnet_id WorkloadsSapSingleNodeVirtualInstance#subnet_id}.
        :param virtual_machine_configuration: virtual_machine_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#virtual_machine_configuration WorkloadsSapSingleNodeVirtualInstance#virtual_machine_configuration}
        :param database_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#database_type WorkloadsSapSingleNodeVirtualInstance#database_type}.
        :param disk_volume_configuration: disk_volume_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#disk_volume_configuration WorkloadsSapSingleNodeVirtualInstance#disk_volume_configuration}
        :param secondary_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#secondary_ip_enabled WorkloadsSapSingleNodeVirtualInstance#secondary_ip_enabled}.
        :param virtual_machine_resource_names: virtual_machine_resource_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#virtual_machine_resource_names WorkloadsSapSingleNodeVirtualInstance#virtual_machine_resource_names}
        '''
        value = WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration(
            app_resource_group_name=app_resource_group_name,
            subnet_id=subnet_id,
            virtual_machine_configuration=virtual_machine_configuration,
            database_type=database_type,
            disk_volume_configuration=disk_volume_configuration,
            secondary_ip_enabled=secondary_ip_enabled,
            virtual_machine_resource_names=virtual_machine_resource_names,
        )

        return typing.cast(None, jsii.invoke(self, "putSingleServerConfiguration", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#create WorkloadsSapSingleNodeVirtualInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#delete WorkloadsSapSingleNodeVirtualInstance#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#read WorkloadsSapSingleNodeVirtualInstance#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#update WorkloadsSapSingleNodeVirtualInstance#update}.
        '''
        value = WorkloadsSapSingleNodeVirtualInstanceTimeouts(
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
    def identity(
        self,
    ) -> "WorkloadsSapSingleNodeVirtualInstanceIdentityOutputReference":
        return typing.cast("WorkloadsSapSingleNodeVirtualInstanceIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="singleServerConfiguration")
    def single_server_configuration(
        self,
    ) -> "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationOutputReference":
        return typing.cast("WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationOutputReference", jsii.get(self, "singleServerConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "WorkloadsSapSingleNodeVirtualInstanceTimeoutsOutputReference":
        return typing.cast("WorkloadsSapSingleNodeVirtualInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["WorkloadsSapSingleNodeVirtualInstanceIdentity"]:
        return typing.cast(typing.Optional["WorkloadsSapSingleNodeVirtualInstanceIdentity"], jsii.get(self, "identityInput"))

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
    @jsii.member(jsii_name="singleServerConfigurationInput")
    def single_server_configuration_input(
        self,
    ) -> typing.Optional["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration"]:
        return typing.cast(typing.Optional["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration"], jsii.get(self, "singleServerConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WorkloadsSapSingleNodeVirtualInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WorkloadsSapSingleNodeVirtualInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="appLocation")
    def app_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appLocation"))

    @app_location.setter
    def app_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c56d3c51cf0ce2d8c6cf7e09d651caf57f9750f0c0abe4d22fdfb9634d95046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05082106c07538a7df7a7b388f17551cedeaecf50ef337e942b4df705c4b81d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361545523276c59338d96284fb662516211bf972518695f234867a0db5d0728f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ba2152431d57f0afaccef0b72d4f7e6da5b91f4586498cac6050be938b00191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedResourceGroupName")
    def managed_resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedResourceGroupName"))

    @managed_resource_group_name.setter
    def managed_resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6956f80b1c8dd8c57e0eeec53607f9b987d30a9786e3c77ec7e3d8051581b3fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedResourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedResourcesNetworkAccessType")
    def managed_resources_network_access_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedResourcesNetworkAccessType"))

    @managed_resources_network_access_type.setter
    def managed_resources_network_access_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f8ab49b16b6667f4029cc7c03c100799054b7e63c89bc71937b21a5c8a4f66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedResourcesNetworkAccessType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ce236582cdf9c3096abe311486e8b2d4729d4e2e5e951fbd777aba911e2815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b3da0c4cd368a29e7aa214d637e9813569d8e156faf38763743e811e27b5327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sapFqdn")
    def sap_fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sapFqdn"))

    @sap_fqdn.setter
    def sap_fqdn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4458f25f8cc9183d4ba45622c1c8655109bf68680ee563d749a7b98e134047a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sapFqdn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sapProduct")
    def sap_product(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sapProduct"))

    @sap_product.setter
    def sap_product(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db840884a22aa512b365d3f03b7d59e47d3ad9ed319c4ad27d8c9330e3d8f28d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sapProduct", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dad300af9bacdb83f8d4823e9a32ca5b65fcba38a843dc967031dfe0650b7c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceConfig",
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
        "single_server_configuration": "singleServerConfiguration",
        "id": "id",
        "identity": "identity",
        "managed_resource_group_name": "managedResourceGroupName",
        "managed_resources_network_access_type": "managedResourcesNetworkAccessType",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class WorkloadsSapSingleNodeVirtualInstanceConfig(
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
        single_server_configuration: typing.Union["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["WorkloadsSapSingleNodeVirtualInstanceIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_resource_group_name: typing.Optional[builtins.str] = None,
        managed_resources_network_access_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["WorkloadsSapSingleNodeVirtualInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param app_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#app_location WorkloadsSapSingleNodeVirtualInstance#app_location}.
        :param environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#environment WorkloadsSapSingleNodeVirtualInstance#environment}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#location WorkloadsSapSingleNodeVirtualInstance#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#name WorkloadsSapSingleNodeVirtualInstance#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#resource_group_name WorkloadsSapSingleNodeVirtualInstance#resource_group_name}.
        :param sap_fqdn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#sap_fqdn WorkloadsSapSingleNodeVirtualInstance#sap_fqdn}.
        :param sap_product: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#sap_product WorkloadsSapSingleNodeVirtualInstance#sap_product}.
        :param single_server_configuration: single_server_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#single_server_configuration WorkloadsSapSingleNodeVirtualInstance#single_server_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#id WorkloadsSapSingleNodeVirtualInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#identity WorkloadsSapSingleNodeVirtualInstance#identity}
        :param managed_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#managed_resource_group_name WorkloadsSapSingleNodeVirtualInstance#managed_resource_group_name}.
        :param managed_resources_network_access_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#managed_resources_network_access_type WorkloadsSapSingleNodeVirtualInstance#managed_resources_network_access_type}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#tags WorkloadsSapSingleNodeVirtualInstance#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#timeouts WorkloadsSapSingleNodeVirtualInstance#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(single_server_configuration, dict):
            single_server_configuration = WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration(**single_server_configuration)
        if isinstance(identity, dict):
            identity = WorkloadsSapSingleNodeVirtualInstanceIdentity(**identity)
        if isinstance(timeouts, dict):
            timeouts = WorkloadsSapSingleNodeVirtualInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__307163c5d1e12c7eb9b23e2b272398ea21877f7ae87df26a3ae6cd0044b4697d)
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
            check_type(argname="argument single_server_configuration", value=single_server_configuration, expected_type=type_hints["single_server_configuration"])
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
            "single_server_configuration": single_server_configuration,
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#app_location WorkloadsSapSingleNodeVirtualInstance#app_location}.'''
        result = self._values.get("app_location")
        assert result is not None, "Required property 'app_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#environment WorkloadsSapSingleNodeVirtualInstance#environment}.'''
        result = self._values.get("environment")
        assert result is not None, "Required property 'environment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#location WorkloadsSapSingleNodeVirtualInstance#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#name WorkloadsSapSingleNodeVirtualInstance#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#resource_group_name WorkloadsSapSingleNodeVirtualInstance#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sap_fqdn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#sap_fqdn WorkloadsSapSingleNodeVirtualInstance#sap_fqdn}.'''
        result = self._values.get("sap_fqdn")
        assert result is not None, "Required property 'sap_fqdn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sap_product(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#sap_product WorkloadsSapSingleNodeVirtualInstance#sap_product}.'''
        result = self._values.get("sap_product")
        assert result is not None, "Required property 'sap_product' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def single_server_configuration(
        self,
    ) -> "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration":
        '''single_server_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#single_server_configuration WorkloadsSapSingleNodeVirtualInstance#single_server_configuration}
        '''
        result = self._values.get("single_server_configuration")
        assert result is not None, "Required property 'single_server_configuration' is missing"
        return typing.cast("WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#id WorkloadsSapSingleNodeVirtualInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(
        self,
    ) -> typing.Optional["WorkloadsSapSingleNodeVirtualInstanceIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#identity WorkloadsSapSingleNodeVirtualInstance#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["WorkloadsSapSingleNodeVirtualInstanceIdentity"], result)

    @builtins.property
    def managed_resource_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#managed_resource_group_name WorkloadsSapSingleNodeVirtualInstance#managed_resource_group_name}.'''
        result = self._values.get("managed_resource_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_resources_network_access_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#managed_resources_network_access_type WorkloadsSapSingleNodeVirtualInstance#managed_resources_network_access_type}.'''
        result = self._values.get("managed_resources_network_access_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#tags WorkloadsSapSingleNodeVirtualInstance#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["WorkloadsSapSingleNodeVirtualInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#timeouts WorkloadsSapSingleNodeVirtualInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["WorkloadsSapSingleNodeVirtualInstanceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapSingleNodeVirtualInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceIdentity",
    jsii_struct_bases=[],
    name_mapping={"identity_ids": "identityIds", "type": "type"},
)
class WorkloadsSapSingleNodeVirtualInstanceIdentity:
    def __init__(
        self,
        *,
        identity_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#identity_ids WorkloadsSapSingleNodeVirtualInstance#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#type WorkloadsSapSingleNodeVirtualInstance#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0adcbe31116a4cad6bafccfb194ac02822382d55776be081e89c5af908d76537)
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identity_ids": identity_ids,
            "type": type,
        }

    @builtins.property
    def identity_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#identity_ids WorkloadsSapSingleNodeVirtualInstance#identity_ids}.'''
        result = self._values.get("identity_ids")
        assert result is not None, "Required property 'identity_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#type WorkloadsSapSingleNodeVirtualInstance#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapSingleNodeVirtualInstanceIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapSingleNodeVirtualInstanceIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aea0717a3db88de8e853bee00696ecf3ee4d8c6cdc94a9f34423f0b499fb80dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__770e6304d85eff8b17f50a10f7a6d10c67f9c66583f22aebe293a63879094204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec9d6e55335e1aceba7d7c2fcda21a0a82b38f1e08de877a82204fa2a328bf1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapSingleNodeVirtualInstanceIdentity]:
        return typing.cast(typing.Optional[WorkloadsSapSingleNodeVirtualInstanceIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapSingleNodeVirtualInstanceIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7c91b0ba57466846282c93364419ec5ba0e440efd58a635d24e79e236c8d360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "app_resource_group_name": "appResourceGroupName",
        "subnet_id": "subnetId",
        "virtual_machine_configuration": "virtualMachineConfiguration",
        "database_type": "databaseType",
        "disk_volume_configuration": "diskVolumeConfiguration",
        "secondary_ip_enabled": "secondaryIpEnabled",
        "virtual_machine_resource_names": "virtualMachineResourceNames",
    },
)
class WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration:
    def __init__(
        self,
        *,
        app_resource_group_name: builtins.str,
        subnet_id: builtins.str,
        virtual_machine_configuration: typing.Union["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfiguration", typing.Dict[builtins.str, typing.Any]],
        database_type: typing.Optional[builtins.str] = None,
        disk_volume_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secondary_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        virtual_machine_resource_names: typing.Optional[typing.Union["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNames", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param app_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#app_resource_group_name WorkloadsSapSingleNodeVirtualInstance#app_resource_group_name}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#subnet_id WorkloadsSapSingleNodeVirtualInstance#subnet_id}.
        :param virtual_machine_configuration: virtual_machine_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#virtual_machine_configuration WorkloadsSapSingleNodeVirtualInstance#virtual_machine_configuration}
        :param database_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#database_type WorkloadsSapSingleNodeVirtualInstance#database_type}.
        :param disk_volume_configuration: disk_volume_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#disk_volume_configuration WorkloadsSapSingleNodeVirtualInstance#disk_volume_configuration}
        :param secondary_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#secondary_ip_enabled WorkloadsSapSingleNodeVirtualInstance#secondary_ip_enabled}.
        :param virtual_machine_resource_names: virtual_machine_resource_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#virtual_machine_resource_names WorkloadsSapSingleNodeVirtualInstance#virtual_machine_resource_names}
        '''
        if isinstance(virtual_machine_configuration, dict):
            virtual_machine_configuration = WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfiguration(**virtual_machine_configuration)
        if isinstance(virtual_machine_resource_names, dict):
            virtual_machine_resource_names = WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNames(**virtual_machine_resource_names)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df1f7a61d530bb1b56caa2e65849e41ee51b41f3fa3a1ebe80405f0b218118cc)
            check_type(argname="argument app_resource_group_name", value=app_resource_group_name, expected_type=type_hints["app_resource_group_name"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument virtual_machine_configuration", value=virtual_machine_configuration, expected_type=type_hints["virtual_machine_configuration"])
            check_type(argname="argument database_type", value=database_type, expected_type=type_hints["database_type"])
            check_type(argname="argument disk_volume_configuration", value=disk_volume_configuration, expected_type=type_hints["disk_volume_configuration"])
            check_type(argname="argument secondary_ip_enabled", value=secondary_ip_enabled, expected_type=type_hints["secondary_ip_enabled"])
            check_type(argname="argument virtual_machine_resource_names", value=virtual_machine_resource_names, expected_type=type_hints["virtual_machine_resource_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_resource_group_name": app_resource_group_name,
            "subnet_id": subnet_id,
            "virtual_machine_configuration": virtual_machine_configuration,
        }
        if database_type is not None:
            self._values["database_type"] = database_type
        if disk_volume_configuration is not None:
            self._values["disk_volume_configuration"] = disk_volume_configuration
        if secondary_ip_enabled is not None:
            self._values["secondary_ip_enabled"] = secondary_ip_enabled
        if virtual_machine_resource_names is not None:
            self._values["virtual_machine_resource_names"] = virtual_machine_resource_names

    @builtins.property
    def app_resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#app_resource_group_name WorkloadsSapSingleNodeVirtualInstance#app_resource_group_name}.'''
        result = self._values.get("app_resource_group_name")
        assert result is not None, "Required property 'app_resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#subnet_id WorkloadsSapSingleNodeVirtualInstance#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_machine_configuration(
        self,
    ) -> "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfiguration":
        '''virtual_machine_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#virtual_machine_configuration WorkloadsSapSingleNodeVirtualInstance#virtual_machine_configuration}
        '''
        result = self._values.get("virtual_machine_configuration")
        assert result is not None, "Required property 'virtual_machine_configuration' is missing"
        return typing.cast("WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfiguration", result)

    @builtins.property
    def database_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#database_type WorkloadsSapSingleNodeVirtualInstance#database_type}.'''
        result = self._values.get("database_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_volume_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration"]]]:
        '''disk_volume_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#disk_volume_configuration WorkloadsSapSingleNodeVirtualInstance#disk_volume_configuration}
        '''
        result = self._values.get("disk_volume_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration"]]], result)

    @builtins.property
    def secondary_ip_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#secondary_ip_enabled WorkloadsSapSingleNodeVirtualInstance#secondary_ip_enabled}.'''
        result = self._values.get("secondary_ip_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def virtual_machine_resource_names(
        self,
    ) -> typing.Optional["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNames"]:
        '''virtual_machine_resource_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#virtual_machine_resource_names WorkloadsSapSingleNodeVirtualInstance#virtual_machine_resource_names}
        '''
        result = self._values.get("virtual_machine_resource_names")
        return typing.cast(typing.Optional["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNames"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "number_of_disks": "numberOfDisks",
        "size_in_gb": "sizeInGb",
        "sku_name": "skuName",
        "volume_name": "volumeName",
    },
)
class WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration:
    def __init__(
        self,
        *,
        number_of_disks: jsii.Number,
        size_in_gb: jsii.Number,
        sku_name: builtins.str,
        volume_name: builtins.str,
    ) -> None:
        '''
        :param number_of_disks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#number_of_disks WorkloadsSapSingleNodeVirtualInstance#number_of_disks}.
        :param size_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#size_in_gb WorkloadsSapSingleNodeVirtualInstance#size_in_gb}.
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#sku_name WorkloadsSapSingleNodeVirtualInstance#sku_name}.
        :param volume_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#volume_name WorkloadsSapSingleNodeVirtualInstance#volume_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b08c5bde9ab12864ddc0d728c89f0d49deb060ce9778bb707cafe4a1510617)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#number_of_disks WorkloadsSapSingleNodeVirtualInstance#number_of_disks}.'''
        result = self._values.get("number_of_disks")
        assert result is not None, "Required property 'number_of_disks' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def size_in_gb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#size_in_gb WorkloadsSapSingleNodeVirtualInstance#size_in_gb}.'''
        result = self._values.get("size_in_gb")
        assert result is not None, "Required property 'size_in_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def sku_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#sku_name WorkloadsSapSingleNodeVirtualInstance#sku_name}.'''
        result = self._values.get("sku_name")
        assert result is not None, "Required property 'sku_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#volume_name WorkloadsSapSingleNodeVirtualInstance#volume_name}.'''
        result = self._values.get("volume_name")
        assert result is not None, "Required property 'volume_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07b11635a3065c84c8d8584b453b8740a00ca17b29d1984a832c0e6d555a2683)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c22480ba44046923a1362d14ad543f0abe3f581f912273cb488f3b80c13162f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34c3c7e6ab1b4c715b52269cc8579817b9994386a722b445588f02d7d89df8b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44b3b744ecceac44e4e8a31c08426a0201d04af8465cd25d34f9402c4f241d4e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51d047f0407841f4d24bdde48b3f19fa981cb98a6f2ca13fa544b197a3b577cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5cea9ce2ead42a7cfc72ddd7f735cddd6fbbc93f45c0208c1c372a940fbf47b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67ce60b84963af19cbc3a1d56f2420c7daf2e93a558d80274c63e88812d577f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e11d708e1ce1bdfe15f7fcae65f463091cdd4860df4c3165f08bcb77c1d0be1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberOfDisks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeInGb")
    def size_in_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeInGb"))

    @size_in_gb.setter
    def size_in_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8628989943eb7b13ffb7d1c94d153ee98f17456a31644d98d37c64b79c7377c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeInGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skuName")
    def sku_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "skuName"))

    @sku_name.setter
    def sku_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51d2eff1d690506de8b65d9081c4e58fca856c7cee839ebbe74364cd70c44f0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skuName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeName")
    def volume_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeName"))

    @volume_name.setter
    def volume_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e581c29cf5801d2e50221d10c1bc2a8840aa3c530e027e0ebbe1aeada4d4d60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76898f73f432e411759db42427b5f2384b55281e58b24551d39dd8f369a7fc61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95f74e84c267702a3d714d8fc7ed72079db7de4ee9cdf900f6f070549051c0fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDiskVolumeConfiguration")
    def put_disk_volume_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ffb455d05c6b8d65f06c41151ce44e393f78ae497b88737ea32f182d8e5cf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDiskVolumeConfiguration", [value]))

    @jsii.member(jsii_name="putVirtualMachineConfiguration")
    def put_virtual_machine_configuration(
        self,
        *,
        image: typing.Union["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImage", typing.Dict[builtins.str, typing.Any]],
        os_profile: typing.Union["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfile", typing.Dict[builtins.str, typing.Any]],
        virtual_machine_size: builtins.str,
    ) -> None:
        '''
        :param image: image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#image WorkloadsSapSingleNodeVirtualInstance#image}
        :param os_profile: os_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#os_profile WorkloadsSapSingleNodeVirtualInstance#os_profile}
        :param virtual_machine_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#virtual_machine_size WorkloadsSapSingleNodeVirtualInstance#virtual_machine_size}.
        '''
        value = WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfiguration(
            image=image,
            os_profile=os_profile,
            virtual_machine_size=virtual_machine_size,
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualMachineConfiguration", [value]))

    @jsii.member(jsii_name="putVirtualMachineResourceNames")
    def put_virtual_machine_resource_names(
        self,
        *,
        data_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        host_name: typing.Optional[builtins.str] = None,
        network_interface_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        os_disk_name: typing.Optional[builtins.str] = None,
        virtual_machine_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_disk: data_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#data_disk WorkloadsSapSingleNodeVirtualInstance#data_disk}
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#host_name WorkloadsSapSingleNodeVirtualInstance#host_name}.
        :param network_interface_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#network_interface_names WorkloadsSapSingleNodeVirtualInstance#network_interface_names}.
        :param os_disk_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#os_disk_name WorkloadsSapSingleNodeVirtualInstance#os_disk_name}.
        :param virtual_machine_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#virtual_machine_name WorkloadsSapSingleNodeVirtualInstance#virtual_machine_name}.
        '''
        value = WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNames(
            data_disk=data_disk,
            host_name=host_name,
            network_interface_names=network_interface_names,
            os_disk_name=os_disk_name,
            virtual_machine_name=virtual_machine_name,
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualMachineResourceNames", [value]))

    @jsii.member(jsii_name="resetDatabaseType")
    def reset_database_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseType", []))

    @jsii.member(jsii_name="resetDiskVolumeConfiguration")
    def reset_disk_volume_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskVolumeConfiguration", []))

    @jsii.member(jsii_name="resetSecondaryIpEnabled")
    def reset_secondary_ip_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryIpEnabled", []))

    @jsii.member(jsii_name="resetVirtualMachineResourceNames")
    def reset_virtual_machine_resource_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualMachineResourceNames", []))

    @builtins.property
    @jsii.member(jsii_name="diskVolumeConfiguration")
    def disk_volume_configuration(
        self,
    ) -> WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfigurationList:
        return typing.cast(WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfigurationList, jsii.get(self, "diskVolumeConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineConfiguration")
    def virtual_machine_configuration(
        self,
    ) -> "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOutputReference":
        return typing.cast("WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOutputReference", jsii.get(self, "virtualMachineConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineResourceNames")
    def virtual_machine_resource_names(
        self,
    ) -> "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesOutputReference":
        return typing.cast("WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesOutputReference", jsii.get(self, "virtualMachineResourceNames"))

    @builtins.property
    @jsii.member(jsii_name="appResourceGroupNameInput")
    def app_resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appResourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseTypeInput")
    def database_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="diskVolumeConfigurationInput")
    def disk_volume_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration]]], jsii.get(self, "diskVolumeConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryIpEnabledInput")
    def secondary_ip_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "secondaryIpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineConfigurationInput")
    def virtual_machine_configuration_input(
        self,
    ) -> typing.Optional["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfiguration"]:
        return typing.cast(typing.Optional["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfiguration"], jsii.get(self, "virtualMachineConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineResourceNamesInput")
    def virtual_machine_resource_names_input(
        self,
    ) -> typing.Optional["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNames"]:
        return typing.cast(typing.Optional["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNames"], jsii.get(self, "virtualMachineResourceNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="appResourceGroupName")
    def app_resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appResourceGroupName"))

    @app_resource_group_name.setter
    def app_resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5845e5f7a4147861e20417d0c0877740b37014c786c981bc917091d4e2f86d28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appResourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseType")
    def database_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseType"))

    @database_type.setter
    def database_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8bd662cdcd932209817b01320d7f9d20d82a99439e88486c0db77cc8dbf7acd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseType", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__d5931982ca3906ab66d9973d85ab3ab6eff1a8e735d59c3d4976ed58c82a6895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryIpEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b72ac5ea38c34601850436b4481fd8d930b747ec7971374b8b13a6c365318218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration]:
        return typing.cast(typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4322e420fc573ae3ca7da100155a0509cedc0a9a8939cc6531d864a365bef6f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "os_profile": "osProfile",
        "virtual_machine_size": "virtualMachineSize",
    },
)
class WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfiguration:
    def __init__(
        self,
        *,
        image: typing.Union["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImage", typing.Dict[builtins.str, typing.Any]],
        os_profile: typing.Union["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfile", typing.Dict[builtins.str, typing.Any]],
        virtual_machine_size: builtins.str,
    ) -> None:
        '''
        :param image: image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#image WorkloadsSapSingleNodeVirtualInstance#image}
        :param os_profile: os_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#os_profile WorkloadsSapSingleNodeVirtualInstance#os_profile}
        :param virtual_machine_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#virtual_machine_size WorkloadsSapSingleNodeVirtualInstance#virtual_machine_size}.
        '''
        if isinstance(image, dict):
            image = WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImage(**image)
        if isinstance(os_profile, dict):
            os_profile = WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfile(**os_profile)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff17bc7203ec93798aceb9c50711a833f43bda2e3d14bbb7911f75213f345e6)
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
    ) -> "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImage":
        '''image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#image WorkloadsSapSingleNodeVirtualInstance#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast("WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImage", result)

    @builtins.property
    def os_profile(
        self,
    ) -> "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfile":
        '''os_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#os_profile WorkloadsSapSingleNodeVirtualInstance#os_profile}
        '''
        result = self._values.get("os_profile")
        assert result is not None, "Required property 'os_profile' is missing"
        return typing.cast("WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfile", result)

    @builtins.property
    def virtual_machine_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#virtual_machine_size WorkloadsSapSingleNodeVirtualInstance#virtual_machine_size}.'''
        result = self._values.get("virtual_machine_size")
        assert result is not None, "Required property 'virtual_machine_size' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImage",
    jsii_struct_bases=[],
    name_mapping={
        "offer": "offer",
        "publisher": "publisher",
        "sku": "sku",
        "version": "version",
    },
)
class WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImage:
    def __init__(
        self,
        *,
        offer: builtins.str,
        publisher: builtins.str,
        sku: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param offer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#offer WorkloadsSapSingleNodeVirtualInstance#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#publisher WorkloadsSapSingleNodeVirtualInstance#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#sku WorkloadsSapSingleNodeVirtualInstance#sku}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#version WorkloadsSapSingleNodeVirtualInstance#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__febe8cdd3458cfcfbf83354dc9faab72c373a821376679b91d2115b5c2d39b79)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#offer WorkloadsSapSingleNodeVirtualInstance#offer}.'''
        result = self._values.get("offer")
        assert result is not None, "Required property 'offer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def publisher(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#publisher WorkloadsSapSingleNodeVirtualInstance#publisher}.'''
        result = self._values.get("publisher")
        assert result is not None, "Required property 'publisher' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sku(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#sku WorkloadsSapSingleNodeVirtualInstance#sku}.'''
        result = self._values.get("sku")
        assert result is not None, "Required property 'sku' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#version WorkloadsSapSingleNodeVirtualInstance#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5751a586ba9378b94d03f0f7b505af33ca15ebdc2f6e50607ee5c74fc907fc15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea9b721d0a2b72f9ff37d320ddd13a3f4ffcf95a6462464f6f98cb7152e19e52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisher"))

    @publisher.setter
    def publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b32a82280c6ee519faa666f33eb0e66b94b3026a3c4760b292482a50a69beaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de4fb48c0dd435eaf54b04b97cbf0fbf40f9469758db12ea674e77da7a53c3ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9124d298dd5be0efbb1711bfd7ca124655a6da8720cd97b866d59cb0a3bd1b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImage]:
        return typing.cast(typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__041d6bf7b2fbfe49c771e995f618f854e09cfaa08172fbd67fe8076d2d4f98b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfile",
    jsii_struct_bases=[],
    name_mapping={
        "admin_username": "adminUsername",
        "ssh_private_key": "sshPrivateKey",
        "ssh_public_key": "sshPublicKey",
    },
)
class WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfile:
    def __init__(
        self,
        *,
        admin_username: builtins.str,
        ssh_private_key: builtins.str,
        ssh_public_key: builtins.str,
    ) -> None:
        '''
        :param admin_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#admin_username WorkloadsSapSingleNodeVirtualInstance#admin_username}.
        :param ssh_private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#ssh_private_key WorkloadsSapSingleNodeVirtualInstance#ssh_private_key}.
        :param ssh_public_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#ssh_public_key WorkloadsSapSingleNodeVirtualInstance#ssh_public_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c099b971f1df9919fab9833f20eba1702107814dab27829603625e1cc0eed67)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#admin_username WorkloadsSapSingleNodeVirtualInstance#admin_username}.'''
        result = self._values.get("admin_username")
        assert result is not None, "Required property 'admin_username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssh_private_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#ssh_private_key WorkloadsSapSingleNodeVirtualInstance#ssh_private_key}.'''
        result = self._values.get("ssh_private_key")
        assert result is not None, "Required property 'ssh_private_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssh_public_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#ssh_public_key WorkloadsSapSingleNodeVirtualInstance#ssh_public_key}.'''
        result = self._values.get("ssh_public_key")
        assert result is not None, "Required property 'ssh_public_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bb9f42e05c93beebe00aaffaf31dc2f02fb6c19ed2b48a0a7dd73f5d9a6ae96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce1da7f8995fbb1171ef909f0a0c14bdabc9bb2b480e18278d0211f08ae6dbab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPrivateKey")
    def ssh_private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshPrivateKey"))

    @ssh_private_key.setter
    def ssh_private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75049dfbc72a8fd552228a162e1113152bbee8722254859a216d543615ec8ed6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPrivateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPublicKey")
    def ssh_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshPublicKey"))

    @ssh_public_key.setter
    def ssh_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d06a9029de8f4bab0438d6ed574fe16c061f07d9491f3faa297978a49a75c33d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPublicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfile]:
        return typing.cast(typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2112f82ac2df25366e6fe24b11fd89606e847cdd7bc55a3d4ae40f46268983c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05094237a10375ac332c7dc785957caaec55fbc6f3c75304dfadda4288645d1f)
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
        :param offer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#offer WorkloadsSapSingleNodeVirtualInstance#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#publisher WorkloadsSapSingleNodeVirtualInstance#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#sku WorkloadsSapSingleNodeVirtualInstance#sku}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#version WorkloadsSapSingleNodeVirtualInstance#version}.
        '''
        value = WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImage(
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
        :param admin_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#admin_username WorkloadsSapSingleNodeVirtualInstance#admin_username}.
        :param ssh_private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#ssh_private_key WorkloadsSapSingleNodeVirtualInstance#ssh_private_key}.
        :param ssh_public_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#ssh_public_key WorkloadsSapSingleNodeVirtualInstance#ssh_public_key}.
        '''
        value = WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfile(
            admin_username=admin_username,
            ssh_private_key=ssh_private_key,
            ssh_public_key=ssh_public_key,
        )

        return typing.cast(None, jsii.invoke(self, "putOsProfile", [value]))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(
        self,
    ) -> WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImageOutputReference:
        return typing.cast(WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImageOutputReference, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="osProfile")
    def os_profile(
        self,
    ) -> WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfileOutputReference:
        return typing.cast(WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfileOutputReference, jsii.get(self, "osProfile"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(
        self,
    ) -> typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImage]:
        return typing.cast(typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImage], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="osProfileInput")
    def os_profile_input(
        self,
    ) -> typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfile]:
        return typing.cast(typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfile], jsii.get(self, "osProfileInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__750469ec19114265bedea10e0ff6bcef40016ab55eef17d0f2b32c73d5e427b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualMachineSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfiguration]:
        return typing.cast(typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf528085af7b6733ff2612f51af86b43534fc890b3bf385ff3cd56fcaa6ec2ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNames",
    jsii_struct_bases=[],
    name_mapping={
        "data_disk": "dataDisk",
        "host_name": "hostName",
        "network_interface_names": "networkInterfaceNames",
        "os_disk_name": "osDiskName",
        "virtual_machine_name": "virtualMachineName",
    },
)
class WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNames:
    def __init__(
        self,
        *,
        data_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        host_name: typing.Optional[builtins.str] = None,
        network_interface_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        os_disk_name: typing.Optional[builtins.str] = None,
        virtual_machine_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_disk: data_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#data_disk WorkloadsSapSingleNodeVirtualInstance#data_disk}
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#host_name WorkloadsSapSingleNodeVirtualInstance#host_name}.
        :param network_interface_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#network_interface_names WorkloadsSapSingleNodeVirtualInstance#network_interface_names}.
        :param os_disk_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#os_disk_name WorkloadsSapSingleNodeVirtualInstance#os_disk_name}.
        :param virtual_machine_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#virtual_machine_name WorkloadsSapSingleNodeVirtualInstance#virtual_machine_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f81fad9f3f0591a17b771100313bb1478e13c015fe00c4b547636a839b6e47)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk"]]]:
        '''data_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#data_disk WorkloadsSapSingleNodeVirtualInstance#data_disk}
        '''
        result = self._values.get("data_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk"]]], result)

    @builtins.property
    def host_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#host_name WorkloadsSapSingleNodeVirtualInstance#host_name}.'''
        result = self._values.get("host_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_interface_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#network_interface_names WorkloadsSapSingleNodeVirtualInstance#network_interface_names}.'''
        result = self._values.get("network_interface_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def os_disk_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#os_disk_name WorkloadsSapSingleNodeVirtualInstance#os_disk_name}.'''
        result = self._values.get("os_disk_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_machine_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#virtual_machine_name WorkloadsSapSingleNodeVirtualInstance#virtual_machine_name}.'''
        result = self._values.get("virtual_machine_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk",
    jsii_struct_bases=[],
    name_mapping={"names": "names", "volume_name": "volumeName"},
)
class WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk:
    def __init__(
        self,
        *,
        names: typing.Sequence[builtins.str],
        volume_name: builtins.str,
    ) -> None:
        '''
        :param names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#names WorkloadsSapSingleNodeVirtualInstance#names}.
        :param volume_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#volume_name WorkloadsSapSingleNodeVirtualInstance#volume_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9c3250d4ea8f3e32339cb754869417c9df5e2085414d406df48a6697053eb5)
            check_type(argname="argument names", value=names, expected_type=type_hints["names"])
            check_type(argname="argument volume_name", value=volume_name, expected_type=type_hints["volume_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "names": names,
            "volume_name": volume_name,
        }

    @builtins.property
    def names(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#names WorkloadsSapSingleNodeVirtualInstance#names}.'''
        result = self._values.get("names")
        assert result is not None, "Required property 'names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def volume_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#volume_name WorkloadsSapSingleNodeVirtualInstance#volume_name}.'''
        result = self._values.get("volume_name")
        assert result is not None, "Required property 'volume_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66cc96aac3f936fd8fa703a14a20cd45e6e8abe9e4f3e7207fa8bd2466276a1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0ddb708d0535c1268b3f80a3137368e58c5ee85a3beb9ce8529b11c45f774d9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__539e5eead34a4e76f570e4325e86f50572cceacda54532e6176cc1b505386959)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5dca8f145acead1e49976939181fbb13741c23c5823ded4045e972512d25f64b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f2f574a693e663c3f1f3cf76d283232ab27dab6e18312be6e93bc954660ce30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbda967a097d76dc634876b511270b103de994a75eb42c9109adfa45a90982ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5533d6e4db787dc6111e0d2e1d10067211ec47c555ce5d1638cfae691213125)
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
            type_hints = typing.get_type_hints(_typecheckingstub__601a1ee2c5689b4a8d9bef34e1dd1500b6fbdf82f5bd96b3dd5ffd1cc8073364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "names", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeName")
    def volume_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeName"))

    @volume_name.setter
    def volume_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e38e32f69f26b312abe0dbf8b77b9bedaab8abc0069953c91952ee6c635b20e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9723df30c80b67d76d08ab7c0cad19416faf032a025be5122b7cbbe2e24cf5ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c58dc1afd1ca20032aadd1c602dca6392da28780694ac92f3ecd2fe997e42dc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataDisk")
    def put_data_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b2b97fbc8425a3b6e34eb5bf8d51ff4155f3d7b4f05a5a3b9484a7f9cc10a9f)
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
    ) -> WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDiskList:
        return typing.cast(WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDiskList, jsii.get(self, "dataDisk"))

    @builtins.property
    @jsii.member(jsii_name="dataDiskInput")
    def data_disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk]]], jsii.get(self, "dataDiskInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c517e5244212cfb560f1489886d42be6e930fe999c6ed57dd48c7dd94f725f54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceNames")
    def network_interface_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkInterfaceNames"))

    @network_interface_names.setter
    def network_interface_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd31139c5b21a76fec14c5ae3516dd7e7e7a8b6a6d2201c8952e519149a5602c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkInterfaceNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osDiskName")
    def os_disk_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osDiskName"))

    @os_disk_name.setter
    def os_disk_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd5d48dd7d50c0aa9c7a344d3b13e98b6fe00e1f578762d74a7a7d2f775be60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osDiskName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualMachineName")
    def virtual_machine_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualMachineName"))

    @virtual_machine_name.setter
    def virtual_machine_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac301ce58bfc4eb6aa373a2a5d30cdcf7d35f3d1bda4cc40d86c049b62ded17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualMachineName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNames]:
        return typing.cast(typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNames], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNames],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ede63f8558329ed6a0932efe94ba8f574ef274ce431078b87ad5072e6500f8da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class WorkloadsSapSingleNodeVirtualInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#create WorkloadsSapSingleNodeVirtualInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#delete WorkloadsSapSingleNodeVirtualInstance#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#read WorkloadsSapSingleNodeVirtualInstance#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#update WorkloadsSapSingleNodeVirtualInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70d3fa06de41d53b015c99ad66f3b46787eb6973f489462774ae48905f7be52e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#create WorkloadsSapSingleNodeVirtualInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#delete WorkloadsSapSingleNodeVirtualInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#read WorkloadsSapSingleNodeVirtualInstance#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/workloads_sap_single_node_virtual_instance#update WorkloadsSapSingleNodeVirtualInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadsSapSingleNodeVirtualInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkloadsSapSingleNodeVirtualInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.workloadsSapSingleNodeVirtualInstance.WorkloadsSapSingleNodeVirtualInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4cfbfcf0e92d0b51bb6705dde50f7a5b6d830dbc2c2e2403ab9a8c4a2fe86a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44a63c12032de1492aa035b8a7fb6e121980461603acfb950fb635fada9a0e29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de73d160c5928dc67dc661b7a7e6d93459c01a1ffac61ed551c85b18253e6982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7bd3049571a1360c37162fcc99626c9ff5337f0dc4196708cad6fe0135c5cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__222e797aadb2f29ea9c2221f3ed59f4ae03ada25c88f80a39cdb5b74bf7f2849)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapSingleNodeVirtualInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapSingleNodeVirtualInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapSingleNodeVirtualInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7538709a5140c8b845d03c8a4e15bba4b3b01aea087d89ea401f7929075cebef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WorkloadsSapSingleNodeVirtualInstance",
    "WorkloadsSapSingleNodeVirtualInstanceConfig",
    "WorkloadsSapSingleNodeVirtualInstanceIdentity",
    "WorkloadsSapSingleNodeVirtualInstanceIdentityOutputReference",
    "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration",
    "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration",
    "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfigurationList",
    "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfigurationOutputReference",
    "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationOutputReference",
    "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfiguration",
    "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImage",
    "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImageOutputReference",
    "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfile",
    "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfileOutputReference",
    "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOutputReference",
    "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNames",
    "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk",
    "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDiskList",
    "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDiskOutputReference",
    "WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesOutputReference",
    "WorkloadsSapSingleNodeVirtualInstanceTimeouts",
    "WorkloadsSapSingleNodeVirtualInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__bf488d0bb9e807c3528010576f2ea2dfc963f228ed258b3711d1aec5265d82a0(
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
    single_server_configuration: typing.Union[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[WorkloadsSapSingleNodeVirtualInstanceIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_resource_group_name: typing.Optional[builtins.str] = None,
    managed_resources_network_access_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[WorkloadsSapSingleNodeVirtualInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a27fcb4444c35b9927f50ce0fe8e8e28e40d185215331238ea9002095a53ed87(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c56d3c51cf0ce2d8c6cf7e09d651caf57f9750f0c0abe4d22fdfb9634d95046(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05082106c07538a7df7a7b388f17551cedeaecf50ef337e942b4df705c4b81d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361545523276c59338d96284fb662516211bf972518695f234867a0db5d0728f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba2152431d57f0afaccef0b72d4f7e6da5b91f4586498cac6050be938b00191(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6956f80b1c8dd8c57e0eeec53607f9b987d30a9786e3c77ec7e3d8051581b3fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f8ab49b16b6667f4029cc7c03c100799054b7e63c89bc71937b21a5c8a4f66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ce236582cdf9c3096abe311486e8b2d4729d4e2e5e951fbd777aba911e2815(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3da0c4cd368a29e7aa214d637e9813569d8e156faf38763743e811e27b5327(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4458f25f8cc9183d4ba45622c1c8655109bf68680ee563d749a7b98e134047a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db840884a22aa512b365d3f03b7d59e47d3ad9ed319c4ad27d8c9330e3d8f28d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dad300af9bacdb83f8d4823e9a32ca5b65fcba38a843dc967031dfe0650b7c2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__307163c5d1e12c7eb9b23e2b272398ea21877f7ae87df26a3ae6cd0044b4697d(
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
    single_server_configuration: typing.Union[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[WorkloadsSapSingleNodeVirtualInstanceIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_resource_group_name: typing.Optional[builtins.str] = None,
    managed_resources_network_access_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[WorkloadsSapSingleNodeVirtualInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0adcbe31116a4cad6bafccfb194ac02822382d55776be081e89c5af908d76537(
    *,
    identity_ids: typing.Sequence[builtins.str],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea0717a3db88de8e853bee00696ecf3ee4d8c6cdc94a9f34423f0b499fb80dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770e6304d85eff8b17f50a10f7a6d10c67f9c66583f22aebe293a63879094204(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9d6e55335e1aceba7d7c2fcda21a0a82b38f1e08de877a82204fa2a328bf1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7c91b0ba57466846282c93364419ec5ba0e440efd58a635d24e79e236c8d360(
    value: typing.Optional[WorkloadsSapSingleNodeVirtualInstanceIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1f7a61d530bb1b56caa2e65849e41ee51b41f3fa3a1ebe80405f0b218118cc(
    *,
    app_resource_group_name: builtins.str,
    subnet_id: builtins.str,
    virtual_machine_configuration: typing.Union[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfiguration, typing.Dict[builtins.str, typing.Any]],
    database_type: typing.Optional[builtins.str] = None,
    disk_volume_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    secondary_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    virtual_machine_resource_names: typing.Optional[typing.Union[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNames, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b08c5bde9ab12864ddc0d728c89f0d49deb060ce9778bb707cafe4a1510617(
    *,
    number_of_disks: jsii.Number,
    size_in_gb: jsii.Number,
    sku_name: builtins.str,
    volume_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b11635a3065c84c8d8584b453b8740a00ca17b29d1984a832c0e6d555a2683(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c22480ba44046923a1362d14ad543f0abe3f581f912273cb488f3b80c13162f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c3c7e6ab1b4c715b52269cc8579817b9994386a722b445588f02d7d89df8b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44b3b744ecceac44e4e8a31c08426a0201d04af8465cd25d34f9402c4f241d4e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d047f0407841f4d24bdde48b3f19fa981cb98a6f2ca13fa544b197a3b577cd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5cea9ce2ead42a7cfc72ddd7f735cddd6fbbc93f45c0208c1c372a940fbf47b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ce60b84963af19cbc3a1d56f2420c7daf2e93a558d80274c63e88812d577f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e11d708e1ce1bdfe15f7fcae65f463091cdd4860df4c3165f08bcb77c1d0be1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8628989943eb7b13ffb7d1c94d153ee98f17456a31644d98d37c64b79c7377c7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d2eff1d690506de8b65d9081c4e58fca856c7cee839ebbe74364cd70c44f0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e581c29cf5801d2e50221d10c1bc2a8840aa3c530e027e0ebbe1aeada4d4d60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76898f73f432e411759db42427b5f2384b55281e58b24551d39dd8f369a7fc61(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f74e84c267702a3d714d8fc7ed72079db7de4ee9cdf900f6f070549051c0fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ffb455d05c6b8d65f06c41151ce44e393f78ae497b88737ea32f182d8e5cf8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationDiskVolumeConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5845e5f7a4147861e20417d0c0877740b37014c786c981bc917091d4e2f86d28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8bd662cdcd932209817b01320d7f9d20d82a99439e88486c0db77cc8dbf7acd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5931982ca3906ab66d9973d85ab3ab6eff1a8e735d59c3d4976ed58c82a6895(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b72ac5ea38c34601850436b4481fd8d930b747ec7971374b8b13a6c365318218(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4322e420fc573ae3ca7da100155a0509cedc0a9a8939cc6531d864a365bef6f6(
    value: typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff17bc7203ec93798aceb9c50711a833f43bda2e3d14bbb7911f75213f345e6(
    *,
    image: typing.Union[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImage, typing.Dict[builtins.str, typing.Any]],
    os_profile: typing.Union[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfile, typing.Dict[builtins.str, typing.Any]],
    virtual_machine_size: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__febe8cdd3458cfcfbf83354dc9faab72c373a821376679b91d2115b5c2d39b79(
    *,
    offer: builtins.str,
    publisher: builtins.str,
    sku: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5751a586ba9378b94d03f0f7b505af33ca15ebdc2f6e50607ee5c74fc907fc15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea9b721d0a2b72f9ff37d320ddd13a3f4ffcf95a6462464f6f98cb7152e19e52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b32a82280c6ee519faa666f33eb0e66b94b3026a3c4760b292482a50a69beaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de4fb48c0dd435eaf54b04b97cbf0fbf40f9469758db12ea674e77da7a53c3ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9124d298dd5be0efbb1711bfd7ca124655a6da8720cd97b866d59cb0a3bd1b41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041d6bf7b2fbfe49c771e995f618f854e09cfaa08172fbd67fe8076d2d4f98b4(
    value: typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c099b971f1df9919fab9833f20eba1702107814dab27829603625e1cc0eed67(
    *,
    admin_username: builtins.str,
    ssh_private_key: builtins.str,
    ssh_public_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb9f42e05c93beebe00aaffaf31dc2f02fb6c19ed2b48a0a7dd73f5d9a6ae96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1da7f8995fbb1171ef909f0a0c14bdabc9bb2b480e18278d0211f08ae6dbab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75049dfbc72a8fd552228a162e1113152bbee8722254859a216d543615ec8ed6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d06a9029de8f4bab0438d6ed574fe16c061f07d9491f3faa297978a49a75c33d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2112f82ac2df25366e6fe24b11fd89606e847cdd7bc55a3d4ae40f46268983c4(
    value: typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfigurationOsProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05094237a10375ac332c7dc785957caaec55fbc6f3c75304dfadda4288645d1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750469ec19114265bedea10e0ff6bcef40016ab55eef17d0f2b32c73d5e427b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf528085af7b6733ff2612f51af86b43534fc890b3bf385ff3cd56fcaa6ec2ae(
    value: typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f81fad9f3f0591a17b771100313bb1478e13c015fe00c4b547636a839b6e47(
    *,
    data_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    host_name: typing.Optional[builtins.str] = None,
    network_interface_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    os_disk_name: typing.Optional[builtins.str] = None,
    virtual_machine_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9c3250d4ea8f3e32339cb754869417c9df5e2085414d406df48a6697053eb5(
    *,
    names: typing.Sequence[builtins.str],
    volume_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cc96aac3f936fd8fa703a14a20cd45e6e8abe9e4f3e7207fa8bd2466276a1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ddb708d0535c1268b3f80a3137368e58c5ee85a3beb9ce8529b11c45f774d9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539e5eead34a4e76f570e4325e86f50572cceacda54532e6176cc1b505386959(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dca8f145acead1e49976939181fbb13741c23c5823ded4045e972512d25f64b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2f574a693e663c3f1f3cf76d283232ab27dab6e18312be6e93bc954660ce30(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbda967a097d76dc634876b511270b103de994a75eb42c9109adfa45a90982ab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5533d6e4db787dc6111e0d2e1d10067211ec47c555ce5d1638cfae691213125(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__601a1ee2c5689b4a8d9bef34e1dd1500b6fbdf82f5bd96b3dd5ffd1cc8073364(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e38e32f69f26b312abe0dbf8b77b9bedaab8abc0069953c91952ee6c635b20e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9723df30c80b67d76d08ab7c0cad19416faf032a025be5122b7cbbe2e24cf5ab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58dc1afd1ca20032aadd1c602dca6392da28780694ac92f3ecd2fe997e42dc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2b97fbc8425a3b6e34eb5bf8d51ff4155f3d7b4f05a5a3b9484a7f9cc10a9f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNamesDataDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c517e5244212cfb560f1489886d42be6e930fe999c6ed57dd48c7dd94f725f54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd31139c5b21a76fec14c5ae3516dd7e7e7a8b6a6d2201c8952e519149a5602c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd5d48dd7d50c0aa9c7a344d3b13e98b6fe00e1f578762d74a7a7d2f775be60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac301ce58bfc4eb6aa373a2a5d30cdcf7d35f3d1bda4cc40d86c049b62ded17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede63f8558329ed6a0932efe94ba8f574ef274ce431078b87ad5072e6500f8da(
    value: typing.Optional[WorkloadsSapSingleNodeVirtualInstanceSingleServerConfigurationVirtualMachineResourceNames],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d3fa06de41d53b015c99ad66f3b46787eb6973f489462774ae48905f7be52e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4cfbfcf0e92d0b51bb6705dde50f7a5b6d830dbc2c2e2403ab9a8c4a2fe86a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a63c12032de1492aa035b8a7fb6e121980461603acfb950fb635fada9a0e29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de73d160c5928dc67dc661b7a7e6d93459c01a1ffac61ed551c85b18253e6982(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7bd3049571a1360c37162fcc99626c9ff5337f0dc4196708cad6fe0135c5cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222e797aadb2f29ea9c2221f3ed59f4ae03ada25c88f80a39cdb5b74bf7f2849(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7538709a5140c8b845d03c8a4e15bba4b3b01aea087d89ea401f7929075cebef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkloadsSapSingleNodeVirtualInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
