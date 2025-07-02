r'''
# `azurerm_system_center_virtual_machine_manager_virtual_machine_instance`

Refer to the Terraform Registry for docs: [`azurerm_system_center_virtual_machine_manager_virtual_machine_instance`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance).
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


class SystemCenterVirtualMachineManagerVirtualMachineInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.systemCenterVirtualMachineManagerVirtualMachineInstance.SystemCenterVirtualMachineManagerVirtualMachineInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance azurerm_system_center_virtual_machine_manager_virtual_machine_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        custom_location_id: builtins.str,
        infrastructure: typing.Union["SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure", typing.Dict[builtins.str, typing.Any]],
        scoped_resource_id: builtins.str,
        hardware: typing.Optional[typing.Union["SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[typing.Union["SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        system_center_virtual_machine_manager_availability_set_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance azurerm_system_center_virtual_machine_manager_virtual_machine_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param custom_location_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#custom_location_id SystemCenterVirtualMachineManagerVirtualMachineInstance#custom_location_id}.
        :param infrastructure: infrastructure block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#infrastructure SystemCenterVirtualMachineManagerVirtualMachineInstance#infrastructure}
        :param scoped_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#scoped_resource_id SystemCenterVirtualMachineManagerVirtualMachineInstance#scoped_resource_id}.
        :param hardware: hardware block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#hardware SystemCenterVirtualMachineManagerVirtualMachineInstance#hardware}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#id SystemCenterVirtualMachineManagerVirtualMachineInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_interface: network_interface block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#network_interface SystemCenterVirtualMachineManagerVirtualMachineInstance#network_interface}
        :param operating_system: operating_system block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#operating_system SystemCenterVirtualMachineManagerVirtualMachineInstance#operating_system}
        :param storage_disk: storage_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#storage_disk SystemCenterVirtualMachineManagerVirtualMachineInstance#storage_disk}
        :param system_center_virtual_machine_manager_availability_set_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#system_center_virtual_machine_manager_availability_set_ids SystemCenterVirtualMachineManagerVirtualMachineInstance#system_center_virtual_machine_manager_availability_set_ids}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#timeouts SystemCenterVirtualMachineManagerVirtualMachineInstance#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f63c0f7072b30a94367b83c61483e3300b93db080d43bb249b83d2d4b74a4b55)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SystemCenterVirtualMachineManagerVirtualMachineInstanceConfig(
            custom_location_id=custom_location_id,
            infrastructure=infrastructure,
            scoped_resource_id=scoped_resource_id,
            hardware=hardware,
            id=id,
            network_interface=network_interface,
            operating_system=operating_system,
            storage_disk=storage_disk,
            system_center_virtual_machine_manager_availability_set_ids=system_center_virtual_machine_manager_availability_set_ids,
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
        '''Generates CDKTF code for importing a SystemCenterVirtualMachineManagerVirtualMachineInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SystemCenterVirtualMachineManagerVirtualMachineInstance to import.
        :param import_from_id: The id of the existing SystemCenterVirtualMachineManagerVirtualMachineInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SystemCenterVirtualMachineManagerVirtualMachineInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f25ec8da82723edd0b459f94af99fd341b5c308c82465c3750535c3adeab63)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putHardware")
    def put_hardware(
        self,
        *,
        cpu_count: typing.Optional[jsii.Number] = None,
        dynamic_memory_max_in_mb: typing.Optional[jsii.Number] = None,
        dynamic_memory_min_in_mb: typing.Optional[jsii.Number] = None,
        limit_cpu_for_migration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        memory_in_mb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#cpu_count SystemCenterVirtualMachineManagerVirtualMachineInstance#cpu_count}.
        :param dynamic_memory_max_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#dynamic_memory_max_in_mb SystemCenterVirtualMachineManagerVirtualMachineInstance#dynamic_memory_max_in_mb}.
        :param dynamic_memory_min_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#dynamic_memory_min_in_mb SystemCenterVirtualMachineManagerVirtualMachineInstance#dynamic_memory_min_in_mb}.
        :param limit_cpu_for_migration_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#limit_cpu_for_migration_enabled SystemCenterVirtualMachineManagerVirtualMachineInstance#limit_cpu_for_migration_enabled}.
        :param memory_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#memory_in_mb SystemCenterVirtualMachineManagerVirtualMachineInstance#memory_in_mb}.
        '''
        value = SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware(
            cpu_count=cpu_count,
            dynamic_memory_max_in_mb=dynamic_memory_max_in_mb,
            dynamic_memory_min_in_mb=dynamic_memory_min_in_mb,
            limit_cpu_for_migration_enabled=limit_cpu_for_migration_enabled,
            memory_in_mb=memory_in_mb,
        )

        return typing.cast(None, jsii.invoke(self, "putHardware", [value]))

    @jsii.member(jsii_name="putInfrastructure")
    def put_infrastructure(
        self,
        *,
        checkpoint_type: typing.Optional[builtins.str] = None,
        system_center_virtual_machine_manager_cloud_id: typing.Optional[builtins.str] = None,
        system_center_virtual_machine_manager_inventory_item_id: typing.Optional[builtins.str] = None,
        system_center_virtual_machine_manager_template_id: typing.Optional[builtins.str] = None,
        system_center_virtual_machine_manager_virtual_machine_server_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param checkpoint_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#checkpoint_type SystemCenterVirtualMachineManagerVirtualMachineInstance#checkpoint_type}.
        :param system_center_virtual_machine_manager_cloud_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#system_center_virtual_machine_manager_cloud_id SystemCenterVirtualMachineManagerVirtualMachineInstance#system_center_virtual_machine_manager_cloud_id}.
        :param system_center_virtual_machine_manager_inventory_item_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#system_center_virtual_machine_manager_inventory_item_id SystemCenterVirtualMachineManagerVirtualMachineInstance#system_center_virtual_machine_manager_inventory_item_id}.
        :param system_center_virtual_machine_manager_template_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#system_center_virtual_machine_manager_template_id SystemCenterVirtualMachineManagerVirtualMachineInstance#system_center_virtual_machine_manager_template_id}.
        :param system_center_virtual_machine_manager_virtual_machine_server_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#system_center_virtual_machine_manager_virtual_machine_server_id SystemCenterVirtualMachineManagerVirtualMachineInstance#system_center_virtual_machine_manager_virtual_machine_server_id}.
        '''
        value = SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure(
            checkpoint_type=checkpoint_type,
            system_center_virtual_machine_manager_cloud_id=system_center_virtual_machine_manager_cloud_id,
            system_center_virtual_machine_manager_inventory_item_id=system_center_virtual_machine_manager_inventory_item_id,
            system_center_virtual_machine_manager_template_id=system_center_virtual_machine_manager_template_id,
            system_center_virtual_machine_manager_virtual_machine_server_id=system_center_virtual_machine_manager_virtual_machine_server_id,
        )

        return typing.cast(None, jsii.invoke(self, "putInfrastructure", [value]))

    @jsii.member(jsii_name="putNetworkInterface")
    def put_network_interface(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aff86de8c991b6f88d385d82bf24de5d61bce58cc29af2ce433b582f86328f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkInterface", [value]))

    @jsii.member(jsii_name="putOperatingSystem")
    def put_operating_system(
        self,
        *,
        admin_password: typing.Optional[builtins.str] = None,
        computer_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param admin_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#admin_password SystemCenterVirtualMachineManagerVirtualMachineInstance#admin_password}.
        :param computer_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#computer_name SystemCenterVirtualMachineManagerVirtualMachineInstance#computer_name}.
        '''
        value = SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem(
            admin_password=admin_password, computer_name=computer_name
        )

        return typing.cast(None, jsii.invoke(self, "putOperatingSystem", [value]))

    @jsii.member(jsii_name="putStorageDisk")
    def put_storage_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c86ff5c8c4ac83906758bdd5cf083b240dd34e537219db5d0869ac63ede53103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStorageDisk", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#create SystemCenterVirtualMachineManagerVirtualMachineInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#delete SystemCenterVirtualMachineManagerVirtualMachineInstance#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#read SystemCenterVirtualMachineManagerVirtualMachineInstance#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#update SystemCenterVirtualMachineManagerVirtualMachineInstance#update}.
        '''
        value = SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetHardware")
    def reset_hardware(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHardware", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNetworkInterface")
    def reset_network_interface(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkInterface", []))

    @jsii.member(jsii_name="resetOperatingSystem")
    def reset_operating_system(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperatingSystem", []))

    @jsii.member(jsii_name="resetStorageDisk")
    def reset_storage_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageDisk", []))

    @jsii.member(jsii_name="resetSystemCenterVirtualMachineManagerAvailabilitySetIds")
    def reset_system_center_virtual_machine_manager_availability_set_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemCenterVirtualMachineManagerAvailabilitySetIds", []))

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
    @jsii.member(jsii_name="hardware")
    def hardware(
        self,
    ) -> "SystemCenterVirtualMachineManagerVirtualMachineInstanceHardwareOutputReference":
        return typing.cast("SystemCenterVirtualMachineManagerVirtualMachineInstanceHardwareOutputReference", jsii.get(self, "hardware"))

    @builtins.property
    @jsii.member(jsii_name="infrastructure")
    def infrastructure(
        self,
    ) -> "SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructureOutputReference":
        return typing.cast("SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructureOutputReference", jsii.get(self, "infrastructure"))

    @builtins.property
    @jsii.member(jsii_name="networkInterface")
    def network_interface(
        self,
    ) -> "SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterfaceList":
        return typing.cast("SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterfaceList", jsii.get(self, "networkInterface"))

    @builtins.property
    @jsii.member(jsii_name="operatingSystem")
    def operating_system(
        self,
    ) -> "SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystemOutputReference":
        return typing.cast("SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystemOutputReference", jsii.get(self, "operatingSystem"))

    @builtins.property
    @jsii.member(jsii_name="storageDisk")
    def storage_disk(
        self,
    ) -> "SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDiskList":
        return typing.cast("SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDiskList", jsii.get(self, "storageDisk"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeoutsOutputReference":
        return typing.cast("SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="customLocationIdInput")
    def custom_location_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customLocationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="hardwareInput")
    def hardware_input(
        self,
    ) -> typing.Optional["SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware"]:
        return typing.cast(typing.Optional["SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware"], jsii.get(self, "hardwareInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureInput")
    def infrastructure_input(
        self,
    ) -> typing.Optional["SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure"]:
        return typing.cast(typing.Optional["SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure"], jsii.get(self, "infrastructureInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceInput")
    def network_interface_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface"]]], jsii.get(self, "networkInterfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="operatingSystemInput")
    def operating_system_input(
        self,
    ) -> typing.Optional["SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem"]:
        return typing.cast(typing.Optional["SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem"], jsii.get(self, "operatingSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="scopedResourceIdInput")
    def scoped_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopedResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageDiskInput")
    def storage_disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk"]]], jsii.get(self, "storageDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="systemCenterVirtualMachineManagerAvailabilitySetIdsInput")
    def system_center_virtual_machine_manager_availability_set_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "systemCenterVirtualMachineManagerAvailabilitySetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="customLocationId")
    def custom_location_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customLocationId"))

    @custom_location_id.setter
    def custom_location_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__059be254bf3d2fb0cfec48cfe6f69fef9987921cce6919180a1ae833e4a0bbbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customLocationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20844a97f5c0d03eba2611b164f2f30edc93753665b920f03375d02cf56fb872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopedResourceId")
    def scoped_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopedResourceId"))

    @scoped_resource_id.setter
    def scoped_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e73ce77ff40f8941e4a90534a160bbb8422fa9f8c62b635c4a101ea40abb8037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopedResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemCenterVirtualMachineManagerAvailabilitySetIds")
    def system_center_virtual_machine_manager_availability_set_ids(
        self,
    ) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "systemCenterVirtualMachineManagerAvailabilitySetIds"))

    @system_center_virtual_machine_manager_availability_set_ids.setter
    def system_center_virtual_machine_manager_availability_set_ids(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8647ff5157e9870e1afe3591ee6e00bb6fe6c24958be823469de0402ac615d72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemCenterVirtualMachineManagerAvailabilitySetIds", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.systemCenterVirtualMachineManagerVirtualMachineInstance.SystemCenterVirtualMachineManagerVirtualMachineInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "custom_location_id": "customLocationId",
        "infrastructure": "infrastructure",
        "scoped_resource_id": "scopedResourceId",
        "hardware": "hardware",
        "id": "id",
        "network_interface": "networkInterface",
        "operating_system": "operatingSystem",
        "storage_disk": "storageDisk",
        "system_center_virtual_machine_manager_availability_set_ids": "systemCenterVirtualMachineManagerAvailabilitySetIds",
        "timeouts": "timeouts",
    },
)
class SystemCenterVirtualMachineManagerVirtualMachineInstanceConfig(
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
        custom_location_id: builtins.str,
        infrastructure: typing.Union["SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure", typing.Dict[builtins.str, typing.Any]],
        scoped_resource_id: builtins.str,
        hardware: typing.Optional[typing.Union["SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[typing.Union["SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        system_center_virtual_machine_manager_availability_set_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param custom_location_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#custom_location_id SystemCenterVirtualMachineManagerVirtualMachineInstance#custom_location_id}.
        :param infrastructure: infrastructure block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#infrastructure SystemCenterVirtualMachineManagerVirtualMachineInstance#infrastructure}
        :param scoped_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#scoped_resource_id SystemCenterVirtualMachineManagerVirtualMachineInstance#scoped_resource_id}.
        :param hardware: hardware block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#hardware SystemCenterVirtualMachineManagerVirtualMachineInstance#hardware}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#id SystemCenterVirtualMachineManagerVirtualMachineInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_interface: network_interface block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#network_interface SystemCenterVirtualMachineManagerVirtualMachineInstance#network_interface}
        :param operating_system: operating_system block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#operating_system SystemCenterVirtualMachineManagerVirtualMachineInstance#operating_system}
        :param storage_disk: storage_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#storage_disk SystemCenterVirtualMachineManagerVirtualMachineInstance#storage_disk}
        :param system_center_virtual_machine_manager_availability_set_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#system_center_virtual_machine_manager_availability_set_ids SystemCenterVirtualMachineManagerVirtualMachineInstance#system_center_virtual_machine_manager_availability_set_ids}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#timeouts SystemCenterVirtualMachineManagerVirtualMachineInstance#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(infrastructure, dict):
            infrastructure = SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure(**infrastructure)
        if isinstance(hardware, dict):
            hardware = SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware(**hardware)
        if isinstance(operating_system, dict):
            operating_system = SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem(**operating_system)
        if isinstance(timeouts, dict):
            timeouts = SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faf84b8ad1b11ac4ecdfa1bd6d00f65caff566531b7b5e1971cfa6fa8de0a67e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument custom_location_id", value=custom_location_id, expected_type=type_hints["custom_location_id"])
            check_type(argname="argument infrastructure", value=infrastructure, expected_type=type_hints["infrastructure"])
            check_type(argname="argument scoped_resource_id", value=scoped_resource_id, expected_type=type_hints["scoped_resource_id"])
            check_type(argname="argument hardware", value=hardware, expected_type=type_hints["hardware"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument network_interface", value=network_interface, expected_type=type_hints["network_interface"])
            check_type(argname="argument operating_system", value=operating_system, expected_type=type_hints["operating_system"])
            check_type(argname="argument storage_disk", value=storage_disk, expected_type=type_hints["storage_disk"])
            check_type(argname="argument system_center_virtual_machine_manager_availability_set_ids", value=system_center_virtual_machine_manager_availability_set_ids, expected_type=type_hints["system_center_virtual_machine_manager_availability_set_ids"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_location_id": custom_location_id,
            "infrastructure": infrastructure,
            "scoped_resource_id": scoped_resource_id,
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
        if hardware is not None:
            self._values["hardware"] = hardware
        if id is not None:
            self._values["id"] = id
        if network_interface is not None:
            self._values["network_interface"] = network_interface
        if operating_system is not None:
            self._values["operating_system"] = operating_system
        if storage_disk is not None:
            self._values["storage_disk"] = storage_disk
        if system_center_virtual_machine_manager_availability_set_ids is not None:
            self._values["system_center_virtual_machine_manager_availability_set_ids"] = system_center_virtual_machine_manager_availability_set_ids
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
    def custom_location_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#custom_location_id SystemCenterVirtualMachineManagerVirtualMachineInstance#custom_location_id}.'''
        result = self._values.get("custom_location_id")
        assert result is not None, "Required property 'custom_location_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def infrastructure(
        self,
    ) -> "SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure":
        '''infrastructure block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#infrastructure SystemCenterVirtualMachineManagerVirtualMachineInstance#infrastructure}
        '''
        result = self._values.get("infrastructure")
        assert result is not None, "Required property 'infrastructure' is missing"
        return typing.cast("SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure", result)

    @builtins.property
    def scoped_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#scoped_resource_id SystemCenterVirtualMachineManagerVirtualMachineInstance#scoped_resource_id}.'''
        result = self._values.get("scoped_resource_id")
        assert result is not None, "Required property 'scoped_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hardware(
        self,
    ) -> typing.Optional["SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware"]:
        '''hardware block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#hardware SystemCenterVirtualMachineManagerVirtualMachineInstance#hardware}
        '''
        result = self._values.get("hardware")
        return typing.cast(typing.Optional["SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#id SystemCenterVirtualMachineManagerVirtualMachineInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_interface(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface"]]]:
        '''network_interface block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#network_interface SystemCenterVirtualMachineManagerVirtualMachineInstance#network_interface}
        '''
        result = self._values.get("network_interface")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface"]]], result)

    @builtins.property
    def operating_system(
        self,
    ) -> typing.Optional["SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem"]:
        '''operating_system block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#operating_system SystemCenterVirtualMachineManagerVirtualMachineInstance#operating_system}
        '''
        result = self._values.get("operating_system")
        return typing.cast(typing.Optional["SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem"], result)

    @builtins.property
    def storage_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk"]]]:
        '''storage_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#storage_disk SystemCenterVirtualMachineManagerVirtualMachineInstance#storage_disk}
        '''
        result = self._values.get("storage_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk"]]], result)

    @builtins.property
    def system_center_virtual_machine_manager_availability_set_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#system_center_virtual_machine_manager_availability_set_ids SystemCenterVirtualMachineManagerVirtualMachineInstance#system_center_virtual_machine_manager_availability_set_ids}.'''
        result = self._values.get("system_center_virtual_machine_manager_availability_set_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#timeouts SystemCenterVirtualMachineManagerVirtualMachineInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SystemCenterVirtualMachineManagerVirtualMachineInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.systemCenterVirtualMachineManagerVirtualMachineInstance.SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware",
    jsii_struct_bases=[],
    name_mapping={
        "cpu_count": "cpuCount",
        "dynamic_memory_max_in_mb": "dynamicMemoryMaxInMb",
        "dynamic_memory_min_in_mb": "dynamicMemoryMinInMb",
        "limit_cpu_for_migration_enabled": "limitCpuForMigrationEnabled",
        "memory_in_mb": "memoryInMb",
    },
)
class SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware:
    def __init__(
        self,
        *,
        cpu_count: typing.Optional[jsii.Number] = None,
        dynamic_memory_max_in_mb: typing.Optional[jsii.Number] = None,
        dynamic_memory_min_in_mb: typing.Optional[jsii.Number] = None,
        limit_cpu_for_migration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        memory_in_mb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#cpu_count SystemCenterVirtualMachineManagerVirtualMachineInstance#cpu_count}.
        :param dynamic_memory_max_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#dynamic_memory_max_in_mb SystemCenterVirtualMachineManagerVirtualMachineInstance#dynamic_memory_max_in_mb}.
        :param dynamic_memory_min_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#dynamic_memory_min_in_mb SystemCenterVirtualMachineManagerVirtualMachineInstance#dynamic_memory_min_in_mb}.
        :param limit_cpu_for_migration_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#limit_cpu_for_migration_enabled SystemCenterVirtualMachineManagerVirtualMachineInstance#limit_cpu_for_migration_enabled}.
        :param memory_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#memory_in_mb SystemCenterVirtualMachineManagerVirtualMachineInstance#memory_in_mb}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44bc62bc1678bccab6f01c3418cd0da0401c74c7a4bbba058bfd46c185e09601)
            check_type(argname="argument cpu_count", value=cpu_count, expected_type=type_hints["cpu_count"])
            check_type(argname="argument dynamic_memory_max_in_mb", value=dynamic_memory_max_in_mb, expected_type=type_hints["dynamic_memory_max_in_mb"])
            check_type(argname="argument dynamic_memory_min_in_mb", value=dynamic_memory_min_in_mb, expected_type=type_hints["dynamic_memory_min_in_mb"])
            check_type(argname="argument limit_cpu_for_migration_enabled", value=limit_cpu_for_migration_enabled, expected_type=type_hints["limit_cpu_for_migration_enabled"])
            check_type(argname="argument memory_in_mb", value=memory_in_mb, expected_type=type_hints["memory_in_mb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu_count is not None:
            self._values["cpu_count"] = cpu_count
        if dynamic_memory_max_in_mb is not None:
            self._values["dynamic_memory_max_in_mb"] = dynamic_memory_max_in_mb
        if dynamic_memory_min_in_mb is not None:
            self._values["dynamic_memory_min_in_mb"] = dynamic_memory_min_in_mb
        if limit_cpu_for_migration_enabled is not None:
            self._values["limit_cpu_for_migration_enabled"] = limit_cpu_for_migration_enabled
        if memory_in_mb is not None:
            self._values["memory_in_mb"] = memory_in_mb

    @builtins.property
    def cpu_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#cpu_count SystemCenterVirtualMachineManagerVirtualMachineInstance#cpu_count}.'''
        result = self._values.get("cpu_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dynamic_memory_max_in_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#dynamic_memory_max_in_mb SystemCenterVirtualMachineManagerVirtualMachineInstance#dynamic_memory_max_in_mb}.'''
        result = self._values.get("dynamic_memory_max_in_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dynamic_memory_min_in_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#dynamic_memory_min_in_mb SystemCenterVirtualMachineManagerVirtualMachineInstance#dynamic_memory_min_in_mb}.'''
        result = self._values.get("dynamic_memory_min_in_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def limit_cpu_for_migration_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#limit_cpu_for_migration_enabled SystemCenterVirtualMachineManagerVirtualMachineInstance#limit_cpu_for_migration_enabled}.'''
        result = self._values.get("limit_cpu_for_migration_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def memory_in_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#memory_in_mb SystemCenterVirtualMachineManagerVirtualMachineInstance#memory_in_mb}.'''
        result = self._values.get("memory_in_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SystemCenterVirtualMachineManagerVirtualMachineInstanceHardwareOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.systemCenterVirtualMachineManagerVirtualMachineInstance.SystemCenterVirtualMachineManagerVirtualMachineInstanceHardwareOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67907b27b243a46b8380b3d597c6513a59657bb4563ba1e4a088a2ec04dc18b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpuCount")
    def reset_cpu_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuCount", []))

    @jsii.member(jsii_name="resetDynamicMemoryMaxInMb")
    def reset_dynamic_memory_max_in_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicMemoryMaxInMb", []))

    @jsii.member(jsii_name="resetDynamicMemoryMinInMb")
    def reset_dynamic_memory_min_in_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicMemoryMinInMb", []))

    @jsii.member(jsii_name="resetLimitCpuForMigrationEnabled")
    def reset_limit_cpu_for_migration_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimitCpuForMigrationEnabled", []))

    @jsii.member(jsii_name="resetMemoryInMb")
    def reset_memory_in_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryInMb", []))

    @builtins.property
    @jsii.member(jsii_name="cpuCountInput")
    def cpu_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuCountInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicMemoryMaxInMbInput")
    def dynamic_memory_max_in_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dynamicMemoryMaxInMbInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicMemoryMinInMbInput")
    def dynamic_memory_min_in_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dynamicMemoryMinInMbInput"))

    @builtins.property
    @jsii.member(jsii_name="limitCpuForMigrationEnabledInput")
    def limit_cpu_for_migration_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "limitCpuForMigrationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInMbInput")
    def memory_in_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryInMbInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCount")
    def cpu_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuCount"))

    @cpu_count.setter
    def cpu_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39641c2cb730929ca19c01674d236447b26a712ef07e215d73659cdd2b2d0328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dynamicMemoryMaxInMb")
    def dynamic_memory_max_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dynamicMemoryMaxInMb"))

    @dynamic_memory_max_in_mb.setter
    def dynamic_memory_max_in_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf82399eb1b9816849779a2c4f3289383018f7a819a31f298d4fb80772e31d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamicMemoryMaxInMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dynamicMemoryMinInMb")
    def dynamic_memory_min_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dynamicMemoryMinInMb"))

    @dynamic_memory_min_in_mb.setter
    def dynamic_memory_min_in_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85db7a6c84c02d630caad2d22461e7c62b11243556fc1a7476d90245dc7b0aa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamicMemoryMinInMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limitCpuForMigrationEnabled")
    def limit_cpu_for_migration_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "limitCpuForMigrationEnabled"))

    @limit_cpu_for_migration_enabled.setter
    def limit_cpu_for_migration_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00cc3d7f86e43c03a00255de6a419d619f082cf0aa4db06aef33a6c435a107ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limitCpuForMigrationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryInMb")
    def memory_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryInMb"))

    @memory_in_mb.setter
    def memory_in_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92df9007a327234048c583d11b9e40c0b7ed58d89f4d60a064268e7d09b2ec59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryInMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware]:
        return typing.cast(typing.Optional[SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60824f668ee878f4c24c396a61e69b8ff9af069c9de2c36f284fb69df2e74f65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.systemCenterVirtualMachineManagerVirtualMachineInstance.SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure",
    jsii_struct_bases=[],
    name_mapping={
        "checkpoint_type": "checkpointType",
        "system_center_virtual_machine_manager_cloud_id": "systemCenterVirtualMachineManagerCloudId",
        "system_center_virtual_machine_manager_inventory_item_id": "systemCenterVirtualMachineManagerInventoryItemId",
        "system_center_virtual_machine_manager_template_id": "systemCenterVirtualMachineManagerTemplateId",
        "system_center_virtual_machine_manager_virtual_machine_server_id": "systemCenterVirtualMachineManagerVirtualMachineServerId",
    },
)
class SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure:
    def __init__(
        self,
        *,
        checkpoint_type: typing.Optional[builtins.str] = None,
        system_center_virtual_machine_manager_cloud_id: typing.Optional[builtins.str] = None,
        system_center_virtual_machine_manager_inventory_item_id: typing.Optional[builtins.str] = None,
        system_center_virtual_machine_manager_template_id: typing.Optional[builtins.str] = None,
        system_center_virtual_machine_manager_virtual_machine_server_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param checkpoint_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#checkpoint_type SystemCenterVirtualMachineManagerVirtualMachineInstance#checkpoint_type}.
        :param system_center_virtual_machine_manager_cloud_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#system_center_virtual_machine_manager_cloud_id SystemCenterVirtualMachineManagerVirtualMachineInstance#system_center_virtual_machine_manager_cloud_id}.
        :param system_center_virtual_machine_manager_inventory_item_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#system_center_virtual_machine_manager_inventory_item_id SystemCenterVirtualMachineManagerVirtualMachineInstance#system_center_virtual_machine_manager_inventory_item_id}.
        :param system_center_virtual_machine_manager_template_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#system_center_virtual_machine_manager_template_id SystemCenterVirtualMachineManagerVirtualMachineInstance#system_center_virtual_machine_manager_template_id}.
        :param system_center_virtual_machine_manager_virtual_machine_server_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#system_center_virtual_machine_manager_virtual_machine_server_id SystemCenterVirtualMachineManagerVirtualMachineInstance#system_center_virtual_machine_manager_virtual_machine_server_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__551623dfa1a569b5f0bfefafa3a66e7b659bec9d0dc5307eee0956c03304111b)
            check_type(argname="argument checkpoint_type", value=checkpoint_type, expected_type=type_hints["checkpoint_type"])
            check_type(argname="argument system_center_virtual_machine_manager_cloud_id", value=system_center_virtual_machine_manager_cloud_id, expected_type=type_hints["system_center_virtual_machine_manager_cloud_id"])
            check_type(argname="argument system_center_virtual_machine_manager_inventory_item_id", value=system_center_virtual_machine_manager_inventory_item_id, expected_type=type_hints["system_center_virtual_machine_manager_inventory_item_id"])
            check_type(argname="argument system_center_virtual_machine_manager_template_id", value=system_center_virtual_machine_manager_template_id, expected_type=type_hints["system_center_virtual_machine_manager_template_id"])
            check_type(argname="argument system_center_virtual_machine_manager_virtual_machine_server_id", value=system_center_virtual_machine_manager_virtual_machine_server_id, expected_type=type_hints["system_center_virtual_machine_manager_virtual_machine_server_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if checkpoint_type is not None:
            self._values["checkpoint_type"] = checkpoint_type
        if system_center_virtual_machine_manager_cloud_id is not None:
            self._values["system_center_virtual_machine_manager_cloud_id"] = system_center_virtual_machine_manager_cloud_id
        if system_center_virtual_machine_manager_inventory_item_id is not None:
            self._values["system_center_virtual_machine_manager_inventory_item_id"] = system_center_virtual_machine_manager_inventory_item_id
        if system_center_virtual_machine_manager_template_id is not None:
            self._values["system_center_virtual_machine_manager_template_id"] = system_center_virtual_machine_manager_template_id
        if system_center_virtual_machine_manager_virtual_machine_server_id is not None:
            self._values["system_center_virtual_machine_manager_virtual_machine_server_id"] = system_center_virtual_machine_manager_virtual_machine_server_id

    @builtins.property
    def checkpoint_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#checkpoint_type SystemCenterVirtualMachineManagerVirtualMachineInstance#checkpoint_type}.'''
        result = self._values.get("checkpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_center_virtual_machine_manager_cloud_id(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#system_center_virtual_machine_manager_cloud_id SystemCenterVirtualMachineManagerVirtualMachineInstance#system_center_virtual_machine_manager_cloud_id}.'''
        result = self._values.get("system_center_virtual_machine_manager_cloud_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_center_virtual_machine_manager_inventory_item_id(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#system_center_virtual_machine_manager_inventory_item_id SystemCenterVirtualMachineManagerVirtualMachineInstance#system_center_virtual_machine_manager_inventory_item_id}.'''
        result = self._values.get("system_center_virtual_machine_manager_inventory_item_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_center_virtual_machine_manager_template_id(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#system_center_virtual_machine_manager_template_id SystemCenterVirtualMachineManagerVirtualMachineInstance#system_center_virtual_machine_manager_template_id}.'''
        result = self._values.get("system_center_virtual_machine_manager_template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_center_virtual_machine_manager_virtual_machine_server_id(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#system_center_virtual_machine_manager_virtual_machine_server_id SystemCenterVirtualMachineManagerVirtualMachineInstance#system_center_virtual_machine_manager_virtual_machine_server_id}.'''
        result = self._values.get("system_center_virtual_machine_manager_virtual_machine_server_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.systemCenterVirtualMachineManagerVirtualMachineInstance.SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4f29012c9e53d7b17b6956bd8afda90553be510a33ec9387f0e1ce82569513e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCheckpointType")
    def reset_checkpoint_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheckpointType", []))

    @jsii.member(jsii_name="resetSystemCenterVirtualMachineManagerCloudId")
    def reset_system_center_virtual_machine_manager_cloud_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemCenterVirtualMachineManagerCloudId", []))

    @jsii.member(jsii_name="resetSystemCenterVirtualMachineManagerInventoryItemId")
    def reset_system_center_virtual_machine_manager_inventory_item_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemCenterVirtualMachineManagerInventoryItemId", []))

    @jsii.member(jsii_name="resetSystemCenterVirtualMachineManagerTemplateId")
    def reset_system_center_virtual_machine_manager_template_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemCenterVirtualMachineManagerTemplateId", []))

    @jsii.member(jsii_name="resetSystemCenterVirtualMachineManagerVirtualMachineServerId")
    def reset_system_center_virtual_machine_manager_virtual_machine_server_id(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemCenterVirtualMachineManagerVirtualMachineServerId", []))

    @builtins.property
    @jsii.member(jsii_name="checkpointTypeInput")
    def checkpoint_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "checkpointTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="systemCenterVirtualMachineManagerCloudIdInput")
    def system_center_virtual_machine_manager_cloud_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "systemCenterVirtualMachineManagerCloudIdInput"))

    @builtins.property
    @jsii.member(jsii_name="systemCenterVirtualMachineManagerInventoryItemIdInput")
    def system_center_virtual_machine_manager_inventory_item_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "systemCenterVirtualMachineManagerInventoryItemIdInput"))

    @builtins.property
    @jsii.member(jsii_name="systemCenterVirtualMachineManagerTemplateIdInput")
    def system_center_virtual_machine_manager_template_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "systemCenterVirtualMachineManagerTemplateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="systemCenterVirtualMachineManagerVirtualMachineServerIdInput")
    def system_center_virtual_machine_manager_virtual_machine_server_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "systemCenterVirtualMachineManagerVirtualMachineServerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="checkpointType")
    def checkpoint_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "checkpointType"))

    @checkpoint_type.setter
    def checkpoint_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c55dbe8731731eda4de35d68c68617f37d28e0d5e50daf74c6f1b680dfcb689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkpointType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemCenterVirtualMachineManagerCloudId")
    def system_center_virtual_machine_manager_cloud_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemCenterVirtualMachineManagerCloudId"))

    @system_center_virtual_machine_manager_cloud_id.setter
    def system_center_virtual_machine_manager_cloud_id(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65eef97fa836f7520f43845a8707179d19c4beb87dccd4e58495b1247c2c8012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemCenterVirtualMachineManagerCloudId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemCenterVirtualMachineManagerInventoryItemId")
    def system_center_virtual_machine_manager_inventory_item_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemCenterVirtualMachineManagerInventoryItemId"))

    @system_center_virtual_machine_manager_inventory_item_id.setter
    def system_center_virtual_machine_manager_inventory_item_id(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9789051bab2f6f2bad8b0e119a87f1fb883662e0e8633237673f318a778794a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemCenterVirtualMachineManagerInventoryItemId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemCenterVirtualMachineManagerTemplateId")
    def system_center_virtual_machine_manager_template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemCenterVirtualMachineManagerTemplateId"))

    @system_center_virtual_machine_manager_template_id.setter
    def system_center_virtual_machine_manager_template_id(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ab387e680c86a024a43f0c6102062a4a792b0c10a9f8c1fff9c6b0286598c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemCenterVirtualMachineManagerTemplateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemCenterVirtualMachineManagerVirtualMachineServerId")
    def system_center_virtual_machine_manager_virtual_machine_server_id(
        self,
    ) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemCenterVirtualMachineManagerVirtualMachineServerId"))

    @system_center_virtual_machine_manager_virtual_machine_server_id.setter
    def system_center_virtual_machine_manager_virtual_machine_server_id(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3819e6f9c28810e9433d7338e26c48678425a15ab4f7d34c426e8ed419d0409d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemCenterVirtualMachineManagerVirtualMachineServerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure]:
        return typing.cast(typing.Optional[SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__460edd27798be1e2cb373569119ce9d4b361f19b78622ed753f4e8257fc6ca15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.systemCenterVirtualMachineManagerVirtualMachineInstance.SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "ipv4_address_type": "ipv4AddressType",
        "ipv6_address_type": "ipv6AddressType",
        "mac_address_type": "macAddressType",
        "virtual_network_id": "virtualNetworkId",
    },
)
class SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface:
    def __init__(
        self,
        *,
        name: builtins.str,
        ipv4_address_type: typing.Optional[builtins.str] = None,
        ipv6_address_type: typing.Optional[builtins.str] = None,
        mac_address_type: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#name SystemCenterVirtualMachineManagerVirtualMachineInstance#name}.
        :param ipv4_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#ipv4_address_type SystemCenterVirtualMachineManagerVirtualMachineInstance#ipv4_address_type}.
        :param ipv6_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#ipv6_address_type SystemCenterVirtualMachineManagerVirtualMachineInstance#ipv6_address_type}.
        :param mac_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#mac_address_type SystemCenterVirtualMachineManagerVirtualMachineInstance#mac_address_type}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#virtual_network_id SystemCenterVirtualMachineManagerVirtualMachineInstance#virtual_network_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc50d68b21ea422c44d8a749eac3a9c6ea58977a1d65ffab866913360bfbaec2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ipv4_address_type", value=ipv4_address_type, expected_type=type_hints["ipv4_address_type"])
            check_type(argname="argument ipv6_address_type", value=ipv6_address_type, expected_type=type_hints["ipv6_address_type"])
            check_type(argname="argument mac_address_type", value=mac_address_type, expected_type=type_hints["mac_address_type"])
            check_type(argname="argument virtual_network_id", value=virtual_network_id, expected_type=type_hints["virtual_network_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if ipv4_address_type is not None:
            self._values["ipv4_address_type"] = ipv4_address_type
        if ipv6_address_type is not None:
            self._values["ipv6_address_type"] = ipv6_address_type
        if mac_address_type is not None:
            self._values["mac_address_type"] = mac_address_type
        if virtual_network_id is not None:
            self._values["virtual_network_id"] = virtual_network_id

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#name SystemCenterVirtualMachineManagerVirtualMachineInstance#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ipv4_address_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#ipv4_address_type SystemCenterVirtualMachineManagerVirtualMachineInstance#ipv4_address_type}.'''
        result = self._values.get("ipv4_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6_address_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#ipv6_address_type SystemCenterVirtualMachineManagerVirtualMachineInstance#ipv6_address_type}.'''
        result = self._values.get("ipv6_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mac_address_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#mac_address_type SystemCenterVirtualMachineManagerVirtualMachineInstance#mac_address_type}.'''
        result = self._values.get("mac_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#virtual_network_id SystemCenterVirtualMachineManagerVirtualMachineInstance#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterfaceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.systemCenterVirtualMachineManagerVirtualMachineInstance.SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterfaceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13234bf9728394de9339d82212900d31587ec296fa8ccad8b15f0affb64dfffe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterfaceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__befb6c1022b25da003b7b2b0ca772405b55213a01b9a9ddcc1e057e42a82c5cb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterfaceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__774d00301ffa0edaa3f6ded39cfdb67d4b15569a8ae96bedd001b562dfee4280)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6075326d28315030e8aaf4749aa5dda7be546a47087862bb8e919ee02997968)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e62b620dc4f51714d1074db17e447128542d80f85f2981584c339e1c9fdf1b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b3f0193939acdc5c5f2098babb953408bfc76c43888317c2685acfd8ce1858e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterfaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.systemCenterVirtualMachineManagerVirtualMachineInstance.SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterfaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bc836184b40b434f61ab26054d58d38d485a98e07b442aa1dab689975bfb368)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIpv4AddressType")
    def reset_ipv4_address_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv4AddressType", []))

    @jsii.member(jsii_name="resetIpv6AddressType")
    def reset_ipv6_address_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6AddressType", []))

    @jsii.member(jsii_name="resetMacAddressType")
    def reset_mac_address_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMacAddressType", []))

    @jsii.member(jsii_name="resetVirtualNetworkId")
    def reset_virtual_network_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkId", []))

    @builtins.property
    @jsii.member(jsii_name="ipv4AddressTypeInput")
    def ipv4_address_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv4AddressTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AddressTypeInput")
    def ipv6_address_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6AddressTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="macAddressTypeInput")
    def mac_address_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "macAddressTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkIdInput")
    def virtual_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv4AddressType")
    def ipv4_address_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4AddressType"))

    @ipv4_address_type.setter
    def ipv4_address_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4101b47b2e2ff9b274e934aa6b7ec15393bc88d0bd163f3a5a84b5af4db176fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4AddressType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv6AddressType")
    def ipv6_address_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6AddressType"))

    @ipv6_address_type.setter
    def ipv6_address_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331fa42ca56f7e56a4c9c3346e3aaae149503b5cedbb7fd91c5a77d24a6143ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6AddressType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="macAddressType")
    def mac_address_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "macAddressType"))

    @mac_address_type.setter
    def mac_address_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26aac18be6bb5e91bd725d5fbbfc8b8a0790476f7aa339cd2c2313885f31a7cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "macAddressType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98ab25c1b01e3d9541c9e816143306926b6daafe38455e16c812309e5e4abaad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcaa697afd697f3b312f9cbd40ec0690d541840812f87f8156084f9bf13223ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2da82ff3936cb7ae91bb4965d47500f4a1421073f9157a33b78b35264194837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.systemCenterVirtualMachineManagerVirtualMachineInstance.SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem",
    jsii_struct_bases=[],
    name_mapping={"admin_password": "adminPassword", "computer_name": "computerName"},
)
class SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem:
    def __init__(
        self,
        *,
        admin_password: typing.Optional[builtins.str] = None,
        computer_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param admin_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#admin_password SystemCenterVirtualMachineManagerVirtualMachineInstance#admin_password}.
        :param computer_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#computer_name SystemCenterVirtualMachineManagerVirtualMachineInstance#computer_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f309b920275cdfd3db098c091badfb4d7ec075287bfd90c7a6cfb53dc8751a79)
            check_type(argname="argument admin_password", value=admin_password, expected_type=type_hints["admin_password"])
            check_type(argname="argument computer_name", value=computer_name, expected_type=type_hints["computer_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_password is not None:
            self._values["admin_password"] = admin_password
        if computer_name is not None:
            self._values["computer_name"] = computer_name

    @builtins.property
    def admin_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#admin_password SystemCenterVirtualMachineManagerVirtualMachineInstance#admin_password}.'''
        result = self._values.get("admin_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def computer_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#computer_name SystemCenterVirtualMachineManagerVirtualMachineInstance#computer_name}.'''
        result = self._values.get("computer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystemOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.systemCenterVirtualMachineManagerVirtualMachineInstance.SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystemOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60a86cd1df8bc070bbed30abdfd75fa2b20ac9dd815c2c696f21c2ae2c58f56f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdminPassword")
    def reset_admin_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminPassword", []))

    @jsii.member(jsii_name="resetComputerName")
    def reset_computer_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputerName", []))

    @builtins.property
    @jsii.member(jsii_name="adminPasswordInput")
    def admin_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="computerNameInput")
    def computer_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="adminPassword")
    def admin_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminPassword"))

    @admin_password.setter
    def admin_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0667580ff847e60a572ffb2a896fb38cf265d99565d10aa569081afb2617371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="computerName")
    def computer_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computerName"))

    @computer_name.setter
    def computer_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07873cc2b4215010bfe4975d45393215d40ced3051d256e3e3b7d1550db97f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem]:
        return typing.cast(typing.Optional[SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dacff723b59aae0e78df5ce7d085fac04e8a6d3ab86a1c457f99b52e02c315d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.systemCenterVirtualMachineManagerVirtualMachineInstance.SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk",
    jsii_struct_bases=[],
    name_mapping={
        "bus": "bus",
        "bus_type": "busType",
        "disk_size_gb": "diskSizeGb",
        "lun": "lun",
        "name": "name",
        "storage_qos_policy_name": "storageQosPolicyName",
        "template_disk_id": "templateDiskId",
        "vhd_type": "vhdType",
    },
)
class SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk:
    def __init__(
        self,
        *,
        bus: typing.Optional[jsii.Number] = None,
        bus_type: typing.Optional[builtins.str] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        lun: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        storage_qos_policy_name: typing.Optional[builtins.str] = None,
        template_disk_id: typing.Optional[builtins.str] = None,
        vhd_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#bus SystemCenterVirtualMachineManagerVirtualMachineInstance#bus}.
        :param bus_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#bus_type SystemCenterVirtualMachineManagerVirtualMachineInstance#bus_type}.
        :param disk_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#disk_size_gb SystemCenterVirtualMachineManagerVirtualMachineInstance#disk_size_gb}.
        :param lun: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#lun SystemCenterVirtualMachineManagerVirtualMachineInstance#lun}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#name SystemCenterVirtualMachineManagerVirtualMachineInstance#name}.
        :param storage_qos_policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#storage_qos_policy_name SystemCenterVirtualMachineManagerVirtualMachineInstance#storage_qos_policy_name}.
        :param template_disk_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#template_disk_id SystemCenterVirtualMachineManagerVirtualMachineInstance#template_disk_id}.
        :param vhd_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#vhd_type SystemCenterVirtualMachineManagerVirtualMachineInstance#vhd_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2daf45c6179e1de16dee712e8cb3f3572a4bce916a9dfa3f446aa6665b6c1f)
            check_type(argname="argument bus", value=bus, expected_type=type_hints["bus"])
            check_type(argname="argument bus_type", value=bus_type, expected_type=type_hints["bus_type"])
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument lun", value=lun, expected_type=type_hints["lun"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument storage_qos_policy_name", value=storage_qos_policy_name, expected_type=type_hints["storage_qos_policy_name"])
            check_type(argname="argument template_disk_id", value=template_disk_id, expected_type=type_hints["template_disk_id"])
            check_type(argname="argument vhd_type", value=vhd_type, expected_type=type_hints["vhd_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bus is not None:
            self._values["bus"] = bus
        if bus_type is not None:
            self._values["bus_type"] = bus_type
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if lun is not None:
            self._values["lun"] = lun
        if name is not None:
            self._values["name"] = name
        if storage_qos_policy_name is not None:
            self._values["storage_qos_policy_name"] = storage_qos_policy_name
        if template_disk_id is not None:
            self._values["template_disk_id"] = template_disk_id
        if vhd_type is not None:
            self._values["vhd_type"] = vhd_type

    @builtins.property
    def bus(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#bus SystemCenterVirtualMachineManagerVirtualMachineInstance#bus}.'''
        result = self._values.get("bus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bus_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#bus_type SystemCenterVirtualMachineManagerVirtualMachineInstance#bus_type}.'''
        result = self._values.get("bus_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#disk_size_gb SystemCenterVirtualMachineManagerVirtualMachineInstance#disk_size_gb}.'''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lun(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#lun SystemCenterVirtualMachineManagerVirtualMachineInstance#lun}.'''
        result = self._values.get("lun")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#name SystemCenterVirtualMachineManagerVirtualMachineInstance#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_qos_policy_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#storage_qos_policy_name SystemCenterVirtualMachineManagerVirtualMachineInstance#storage_qos_policy_name}.'''
        result = self._values.get("storage_qos_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_disk_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#template_disk_id SystemCenterVirtualMachineManagerVirtualMachineInstance#template_disk_id}.'''
        result = self._values.get("template_disk_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vhd_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#vhd_type SystemCenterVirtualMachineManagerVirtualMachineInstance#vhd_type}.'''
        result = self._values.get("vhd_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.systemCenterVirtualMachineManagerVirtualMachineInstance.SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93cf1a781a8a3a4b6e9d1f0d0cc60d9e27f057a2dd348319ab8f445ace230ac6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7870caf95f98f8501e2c81bc4916db19185de2ff00660d2fff396ae1f99837a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eface7aeb7aba19228f6acaf8222c1a2a860f707318bbf812c6436feca8dae1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d689d5c871b91e0dc8637d7cbeac1c6b4911e9c9bc652248468ea73849e4b06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ae4d0fd8b3a7eeb5114cbfb4cb2219b0b7c113c1feb14203629b593415eacb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85ffedac30033d3b0f66fa902089c092a13dab643a4da89909ceb99066a531c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.systemCenterVirtualMachineManagerVirtualMachineInstance.SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bde84b32ce5b6da1f981d6829b343db8d8e775b207c116efa7cf0b99c3e539b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBus")
    def reset_bus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBus", []))

    @jsii.member(jsii_name="resetBusType")
    def reset_bus_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBusType", []))

    @jsii.member(jsii_name="resetDiskSizeGb")
    def reset_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGb", []))

    @jsii.member(jsii_name="resetLun")
    def reset_lun(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLun", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetStorageQosPolicyName")
    def reset_storage_qos_policy_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageQosPolicyName", []))

    @jsii.member(jsii_name="resetTemplateDiskId")
    def reset_template_disk_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplateDiskId", []))

    @jsii.member(jsii_name="resetVhdType")
    def reset_vhd_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVhdType", []))

    @builtins.property
    @jsii.member(jsii_name="busInput")
    def bus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "busInput"))

    @builtins.property
    @jsii.member(jsii_name="busTypeInput")
    def bus_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "busTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="lunInput")
    def lun_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lunInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageQosPolicyNameInput")
    def storage_qos_policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageQosPolicyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="templateDiskIdInput")
    def template_disk_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateDiskIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vhdTypeInput")
    def vhd_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vhdTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="bus")
    def bus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bus"))

    @bus.setter
    def bus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca6707226f20468da9d2c8a6fca5e61dc067f348f16158e919c1ecf91665e532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="busType")
    def bus_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "busType"))

    @bus_type.setter
    def bus_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__843b0608a508ce4fd7c9db48e81ccd54ab3a0c7aecb058fa3d3b3a5bca77bf44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "busType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdbbe901910b9baf8fcd0644d12df5c8aed82b130e2a86a336ebedb0f8a46099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lun")
    def lun(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lun"))

    @lun.setter
    def lun(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeb5a0d7be1afcfad2e58652670844ca5a2ea13e597e698fef4e8d516ad895be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a9b473de43022c22b075101a09654b1f6f2ea0dd9ddd51dc69b7917ca7eb7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageQosPolicyName")
    def storage_qos_policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageQosPolicyName"))

    @storage_qos_policy_name.setter
    def storage_qos_policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38753eeb9a974b5571fe636520b6967d0ccad31eb569201d0c4df214e1b808c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageQosPolicyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateDiskId")
    def template_disk_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateDiskId"))

    @template_disk_id.setter
    def template_disk_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9db6febfb10bafe7017599269171f7ee0a460891415d048a6102ead4571e85b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateDiskId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vhdType")
    def vhd_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vhdType"))

    @vhd_type.setter
    def vhd_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__493d464d82403b28963fab8be25f969839d1abe141f9dd3e33cea7d2be2ec280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vhdType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea53180c8d983f70ec662ce66791c23315953b33d8fa1c0eb8a5ec9b0e5de229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.systemCenterVirtualMachineManagerVirtualMachineInstance.SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#create SystemCenterVirtualMachineManagerVirtualMachineInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#delete SystemCenterVirtualMachineManagerVirtualMachineInstance#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#read SystemCenterVirtualMachineManagerVirtualMachineInstance#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#update SystemCenterVirtualMachineManagerVirtualMachineInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de40354f62e167425069f1368e4224882c56b0b2a7f50681695cb83cd5a61bf1)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#create SystemCenterVirtualMachineManagerVirtualMachineInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#delete SystemCenterVirtualMachineManagerVirtualMachineInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#read SystemCenterVirtualMachineManagerVirtualMachineInstance#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/system_center_virtual_machine_manager_virtual_machine_instance#update SystemCenterVirtualMachineManagerVirtualMachineInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.systemCenterVirtualMachineManagerVirtualMachineInstance.SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11f052e11533d598a93aaca52f959ba4655b24eeca070b728f626fec95031b73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e550c8221b0f97cf4970d8b64c5e8db7e812573df06907e989a70be36dc3650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99705b2a8d0ccd1de380b91291777a2d8c56857595f16965cf53f143db098771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b3c1c22b781ace54363f00445459313c6c9d804043202fa8e9478b7db0c3124)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__554520ff1c885d32c5cce84a91cffe8bb669f7b313b8cfbd0e654342efb4a04c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fad4b0d20cbce7b8c1e8637034cf77a19bbcc3ee7c739d77b9657dba096c0f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SystemCenterVirtualMachineManagerVirtualMachineInstance",
    "SystemCenterVirtualMachineManagerVirtualMachineInstanceConfig",
    "SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware",
    "SystemCenterVirtualMachineManagerVirtualMachineInstanceHardwareOutputReference",
    "SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure",
    "SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructureOutputReference",
    "SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface",
    "SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterfaceList",
    "SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterfaceOutputReference",
    "SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem",
    "SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystemOutputReference",
    "SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk",
    "SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDiskList",
    "SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDiskOutputReference",
    "SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts",
    "SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f63c0f7072b30a94367b83c61483e3300b93db080d43bb249b83d2d4b74a4b55(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    custom_location_id: builtins.str,
    infrastructure: typing.Union[SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure, typing.Dict[builtins.str, typing.Any]],
    scoped_resource_id: builtins.str,
    hardware: typing.Optional[typing.Union[SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operating_system: typing.Optional[typing.Union[SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    system_center_virtual_machine_manager_availability_set_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d4f25ec8da82723edd0b459f94af99fd341b5c308c82465c3750535c3adeab63(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff86de8c991b6f88d385d82bf24de5d61bce58cc29af2ce433b582f86328f44(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86ff5c8c4ac83906758bdd5cf083b240dd34e537219db5d0869ac63ede53103(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__059be254bf3d2fb0cfec48cfe6f69fef9987921cce6919180a1ae833e4a0bbbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20844a97f5c0d03eba2611b164f2f30edc93753665b920f03375d02cf56fb872(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e73ce77ff40f8941e4a90534a160bbb8422fa9f8c62b635c4a101ea40abb8037(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8647ff5157e9870e1afe3591ee6e00bb6fe6c24958be823469de0402ac615d72(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faf84b8ad1b11ac4ecdfa1bd6d00f65caff566531b7b5e1971cfa6fa8de0a67e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_location_id: builtins.str,
    infrastructure: typing.Union[SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure, typing.Dict[builtins.str, typing.Any]],
    scoped_resource_id: builtins.str,
    hardware: typing.Optional[typing.Union[SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operating_system: typing.Optional[typing.Union[SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    system_center_virtual_machine_manager_availability_set_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44bc62bc1678bccab6f01c3418cd0da0401c74c7a4bbba058bfd46c185e09601(
    *,
    cpu_count: typing.Optional[jsii.Number] = None,
    dynamic_memory_max_in_mb: typing.Optional[jsii.Number] = None,
    dynamic_memory_min_in_mb: typing.Optional[jsii.Number] = None,
    limit_cpu_for_migration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    memory_in_mb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67907b27b243a46b8380b3d597c6513a59657bb4563ba1e4a088a2ec04dc18b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39641c2cb730929ca19c01674d236447b26a712ef07e215d73659cdd2b2d0328(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf82399eb1b9816849779a2c4f3289383018f7a819a31f298d4fb80772e31d07(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85db7a6c84c02d630caad2d22461e7c62b11243556fc1a7476d90245dc7b0aa9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00cc3d7f86e43c03a00255de6a419d619f082cf0aa4db06aef33a6c435a107ad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92df9007a327234048c583d11b9e40c0b7ed58d89f4d60a064268e7d09b2ec59(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60824f668ee878f4c24c396a61e69b8ff9af069c9de2c36f284fb69df2e74f65(
    value: typing.Optional[SystemCenterVirtualMachineManagerVirtualMachineInstanceHardware],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551623dfa1a569b5f0bfefafa3a66e7b659bec9d0dc5307eee0956c03304111b(
    *,
    checkpoint_type: typing.Optional[builtins.str] = None,
    system_center_virtual_machine_manager_cloud_id: typing.Optional[builtins.str] = None,
    system_center_virtual_machine_manager_inventory_item_id: typing.Optional[builtins.str] = None,
    system_center_virtual_machine_manager_template_id: typing.Optional[builtins.str] = None,
    system_center_virtual_machine_manager_virtual_machine_server_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f29012c9e53d7b17b6956bd8afda90553be510a33ec9387f0e1ce82569513e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c55dbe8731731eda4de35d68c68617f37d28e0d5e50daf74c6f1b680dfcb689(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65eef97fa836f7520f43845a8707179d19c4beb87dccd4e58495b1247c2c8012(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9789051bab2f6f2bad8b0e119a87f1fb883662e0e8633237673f318a778794a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ab387e680c86a024a43f0c6102062a4a792b0c10a9f8c1fff9c6b0286598c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3819e6f9c28810e9433d7338e26c48678425a15ab4f7d34c426e8ed419d0409d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460edd27798be1e2cb373569119ce9d4b361f19b78622ed753f4e8257fc6ca15(
    value: typing.Optional[SystemCenterVirtualMachineManagerVirtualMachineInstanceInfrastructure],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc50d68b21ea422c44d8a749eac3a9c6ea58977a1d65ffab866913360bfbaec2(
    *,
    name: builtins.str,
    ipv4_address_type: typing.Optional[builtins.str] = None,
    ipv6_address_type: typing.Optional[builtins.str] = None,
    mac_address_type: typing.Optional[builtins.str] = None,
    virtual_network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13234bf9728394de9339d82212900d31587ec296fa8ccad8b15f0affb64dfffe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__befb6c1022b25da003b7b2b0ca772405b55213a01b9a9ddcc1e057e42a82c5cb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774d00301ffa0edaa3f6ded39cfdb67d4b15569a8ae96bedd001b562dfee4280(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6075326d28315030e8aaf4749aa5dda7be546a47087862bb8e919ee02997968(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e62b620dc4f51714d1074db17e447128542d80f85f2981584c339e1c9fdf1b6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3f0193939acdc5c5f2098babb953408bfc76c43888317c2685acfd8ce1858e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bc836184b40b434f61ab26054d58d38d485a98e07b442aa1dab689975bfb368(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4101b47b2e2ff9b274e934aa6b7ec15393bc88d0bd163f3a5a84b5af4db176fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331fa42ca56f7e56a4c9c3346e3aaae149503b5cedbb7fd91c5a77d24a6143ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26aac18be6bb5e91bd725d5fbbfc8b8a0790476f7aa339cd2c2313885f31a7cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ab25c1b01e3d9541c9e816143306926b6daafe38455e16c812309e5e4abaad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcaa697afd697f3b312f9cbd40ec0690d541840812f87f8156084f9bf13223ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2da82ff3936cb7ae91bb4965d47500f4a1421073f9157a33b78b35264194837(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SystemCenterVirtualMachineManagerVirtualMachineInstanceNetworkInterface]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f309b920275cdfd3db098c091badfb4d7ec075287bfd90c7a6cfb53dc8751a79(
    *,
    admin_password: typing.Optional[builtins.str] = None,
    computer_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a86cd1df8bc070bbed30abdfd75fa2b20ac9dd815c2c696f21c2ae2c58f56f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0667580ff847e60a572ffb2a896fb38cf265d99565d10aa569081afb2617371(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07873cc2b4215010bfe4975d45393215d40ced3051d256e3e3b7d1550db97f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dacff723b59aae0e78df5ce7d085fac04e8a6d3ab86a1c457f99b52e02c315d(
    value: typing.Optional[SystemCenterVirtualMachineManagerVirtualMachineInstanceOperatingSystem],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2daf45c6179e1de16dee712e8cb3f3572a4bce916a9dfa3f446aa6665b6c1f(
    *,
    bus: typing.Optional[jsii.Number] = None,
    bus_type: typing.Optional[builtins.str] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    lun: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    storage_qos_policy_name: typing.Optional[builtins.str] = None,
    template_disk_id: typing.Optional[builtins.str] = None,
    vhd_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93cf1a781a8a3a4b6e9d1f0d0cc60d9e27f057a2dd348319ab8f445ace230ac6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7870caf95f98f8501e2c81bc4916db19185de2ff00660d2fff396ae1f99837a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eface7aeb7aba19228f6acaf8222c1a2a860f707318bbf812c6436feca8dae1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d689d5c871b91e0dc8637d7cbeac1c6b4911e9c9bc652248468ea73849e4b06(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae4d0fd8b3a7eeb5114cbfb4cb2219b0b7c113c1feb14203629b593415eacb2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ffedac30033d3b0f66fa902089c092a13dab643a4da89909ceb99066a531c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde84b32ce5b6da1f981d6829b343db8d8e775b207c116efa7cf0b99c3e539b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca6707226f20468da9d2c8a6fca5e61dc067f348f16158e919c1ecf91665e532(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__843b0608a508ce4fd7c9db48e81ccd54ab3a0c7aecb058fa3d3b3a5bca77bf44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdbbe901910b9baf8fcd0644d12df5c8aed82b130e2a86a336ebedb0f8a46099(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb5a0d7be1afcfad2e58652670844ca5a2ea13e597e698fef4e8d516ad895be(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a9b473de43022c22b075101a09654b1f6f2ea0dd9ddd51dc69b7917ca7eb7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38753eeb9a974b5571fe636520b6967d0ccad31eb569201d0c4df214e1b808c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db6febfb10bafe7017599269171f7ee0a460891415d048a6102ead4571e85b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493d464d82403b28963fab8be25f969839d1abe141f9dd3e33cea7d2be2ec280(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea53180c8d983f70ec662ce66791c23315953b33d8fa1c0eb8a5ec9b0e5de229(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SystemCenterVirtualMachineManagerVirtualMachineInstanceStorageDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de40354f62e167425069f1368e4224882c56b0b2a7f50681695cb83cd5a61bf1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f052e11533d598a93aaca52f959ba4655b24eeca070b728f626fec95031b73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e550c8221b0f97cf4970d8b64c5e8db7e812573df06907e989a70be36dc3650(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99705b2a8d0ccd1de380b91291777a2d8c56857595f16965cf53f143db098771(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b3c1c22b781ace54363f00445459313c6c9d804043202fa8e9478b7db0c3124(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__554520ff1c885d32c5cce84a91cffe8bb669f7b313b8cfbd0e654342efb4a04c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fad4b0d20cbce7b8c1e8637034cf77a19bbcc3ee7c739d77b9657dba096c0f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SystemCenterVirtualMachineManagerVirtualMachineInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
