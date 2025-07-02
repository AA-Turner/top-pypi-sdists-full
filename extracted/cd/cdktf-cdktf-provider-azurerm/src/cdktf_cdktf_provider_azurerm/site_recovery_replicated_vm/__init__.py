r'''
# `azurerm_site_recovery_replicated_vm`

Refer to the Terraform Registry for docs: [`azurerm_site_recovery_replicated_vm`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm).
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


class SiteRecoveryReplicatedVm(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVm",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm azurerm_site_recovery_replicated_vm}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        recovery_replication_policy_id: builtins.str,
        recovery_vault_name: builtins.str,
        resource_group_name: builtins.str,
        source_recovery_fabric_name: builtins.str,
        source_recovery_protection_container_name: builtins.str,
        source_vm_id: builtins.str,
        target_recovery_fabric_id: builtins.str,
        target_recovery_protection_container_id: builtins.str,
        target_resource_group_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        managed_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicatedVmManagedDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        multi_vm_group_name: typing.Optional[builtins.str] = None,
        network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicatedVmNetworkInterface", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_availability_set_id: typing.Optional[builtins.str] = None,
        target_boot_diagnostic_storage_account_id: typing.Optional[builtins.str] = None,
        target_capacity_reservation_group_id: typing.Optional[builtins.str] = None,
        target_edge_zone: typing.Optional[builtins.str] = None,
        target_network_id: typing.Optional[builtins.str] = None,
        target_proximity_placement_group_id: typing.Optional[builtins.str] = None,
        target_virtual_machine_scale_set_id: typing.Optional[builtins.str] = None,
        target_virtual_machine_size: typing.Optional[builtins.str] = None,
        target_zone: typing.Optional[builtins.str] = None,
        test_network_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SiteRecoveryReplicatedVmTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        unmanaged_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicatedVmUnmanagedDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm azurerm_site_recovery_replicated_vm} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#name SiteRecoveryReplicatedVm#name}.
        :param recovery_replication_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#recovery_replication_policy_id SiteRecoveryReplicatedVm#recovery_replication_policy_id}.
        :param recovery_vault_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#recovery_vault_name SiteRecoveryReplicatedVm#recovery_vault_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#resource_group_name SiteRecoveryReplicatedVm#resource_group_name}.
        :param source_recovery_fabric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#source_recovery_fabric_name SiteRecoveryReplicatedVm#source_recovery_fabric_name}.
        :param source_recovery_protection_container_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#source_recovery_protection_container_name SiteRecoveryReplicatedVm#source_recovery_protection_container_name}.
        :param source_vm_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#source_vm_id SiteRecoveryReplicatedVm#source_vm_id}.
        :param target_recovery_fabric_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_recovery_fabric_id SiteRecoveryReplicatedVm#target_recovery_fabric_id}.
        :param target_recovery_protection_container_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_recovery_protection_container_id SiteRecoveryReplicatedVm#target_recovery_protection_container_id}.
        :param target_resource_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_resource_group_id SiteRecoveryReplicatedVm#target_resource_group_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#id SiteRecoveryReplicatedVm#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param managed_disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#managed_disk SiteRecoveryReplicatedVm#managed_disk}.
        :param multi_vm_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#multi_vm_group_name SiteRecoveryReplicatedVm#multi_vm_group_name}.
        :param network_interface: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#network_interface SiteRecoveryReplicatedVm#network_interface}.
        :param target_availability_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_availability_set_id SiteRecoveryReplicatedVm#target_availability_set_id}.
        :param target_boot_diagnostic_storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_boot_diagnostic_storage_account_id SiteRecoveryReplicatedVm#target_boot_diagnostic_storage_account_id}.
        :param target_capacity_reservation_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_capacity_reservation_group_id SiteRecoveryReplicatedVm#target_capacity_reservation_group_id}.
        :param target_edge_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_edge_zone SiteRecoveryReplicatedVm#target_edge_zone}.
        :param target_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_network_id SiteRecoveryReplicatedVm#target_network_id}.
        :param target_proximity_placement_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_proximity_placement_group_id SiteRecoveryReplicatedVm#target_proximity_placement_group_id}.
        :param target_virtual_machine_scale_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_virtual_machine_scale_set_id SiteRecoveryReplicatedVm#target_virtual_machine_scale_set_id}.
        :param target_virtual_machine_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_virtual_machine_size SiteRecoveryReplicatedVm#target_virtual_machine_size}.
        :param target_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_zone SiteRecoveryReplicatedVm#target_zone}.
        :param test_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#test_network_id SiteRecoveryReplicatedVm#test_network_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#timeouts SiteRecoveryReplicatedVm#timeouts}
        :param unmanaged_disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#unmanaged_disk SiteRecoveryReplicatedVm#unmanaged_disk}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8efed12cf94e269cd8c870a559284db5c0d8f297dcef209d76f9f9532c8548b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SiteRecoveryReplicatedVmConfig(
            name=name,
            recovery_replication_policy_id=recovery_replication_policy_id,
            recovery_vault_name=recovery_vault_name,
            resource_group_name=resource_group_name,
            source_recovery_fabric_name=source_recovery_fabric_name,
            source_recovery_protection_container_name=source_recovery_protection_container_name,
            source_vm_id=source_vm_id,
            target_recovery_fabric_id=target_recovery_fabric_id,
            target_recovery_protection_container_id=target_recovery_protection_container_id,
            target_resource_group_id=target_resource_group_id,
            id=id,
            managed_disk=managed_disk,
            multi_vm_group_name=multi_vm_group_name,
            network_interface=network_interface,
            target_availability_set_id=target_availability_set_id,
            target_boot_diagnostic_storage_account_id=target_boot_diagnostic_storage_account_id,
            target_capacity_reservation_group_id=target_capacity_reservation_group_id,
            target_edge_zone=target_edge_zone,
            target_network_id=target_network_id,
            target_proximity_placement_group_id=target_proximity_placement_group_id,
            target_virtual_machine_scale_set_id=target_virtual_machine_scale_set_id,
            target_virtual_machine_size=target_virtual_machine_size,
            target_zone=target_zone,
            test_network_id=test_network_id,
            timeouts=timeouts,
            unmanaged_disk=unmanaged_disk,
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
        '''Generates CDKTF code for importing a SiteRecoveryReplicatedVm resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SiteRecoveryReplicatedVm to import.
        :param import_from_id: The id of the existing SiteRecoveryReplicatedVm that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SiteRecoveryReplicatedVm to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca8f2075100bb85fe1b0484c86ac4ed963e8e72305d1301769aef3d273eac818)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putManagedDisk")
    def put_managed_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicatedVmManagedDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53fb6859d5965f11fc25461ab53fd2872f013371524184f3c92fe97f5a8c31a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putManagedDisk", [value]))

    @jsii.member(jsii_name="putNetworkInterface")
    def put_network_interface(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicatedVmNetworkInterface", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d5e274e976bf2004ebed07e5fca3e8a4197df6a92dd54749806b808ea240378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkInterface", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#create SiteRecoveryReplicatedVm#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#delete SiteRecoveryReplicatedVm#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#read SiteRecoveryReplicatedVm#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#update SiteRecoveryReplicatedVm#update}.
        '''
        value = SiteRecoveryReplicatedVmTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUnmanagedDisk")
    def put_unmanaged_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicatedVmUnmanagedDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2601348383b122b2056459338c0ecade99e20cda398849a7b776905ceec4e6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUnmanagedDisk", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetManagedDisk")
    def reset_managed_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedDisk", []))

    @jsii.member(jsii_name="resetMultiVmGroupName")
    def reset_multi_vm_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiVmGroupName", []))

    @jsii.member(jsii_name="resetNetworkInterface")
    def reset_network_interface(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkInterface", []))

    @jsii.member(jsii_name="resetTargetAvailabilitySetId")
    def reset_target_availability_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetAvailabilitySetId", []))

    @jsii.member(jsii_name="resetTargetBootDiagnosticStorageAccountId")
    def reset_target_boot_diagnostic_storage_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetBootDiagnosticStorageAccountId", []))

    @jsii.member(jsii_name="resetTargetCapacityReservationGroupId")
    def reset_target_capacity_reservation_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetCapacityReservationGroupId", []))

    @jsii.member(jsii_name="resetTargetEdgeZone")
    def reset_target_edge_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetEdgeZone", []))

    @jsii.member(jsii_name="resetTargetNetworkId")
    def reset_target_network_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetNetworkId", []))

    @jsii.member(jsii_name="resetTargetProximityPlacementGroupId")
    def reset_target_proximity_placement_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetProximityPlacementGroupId", []))

    @jsii.member(jsii_name="resetTargetVirtualMachineScaleSetId")
    def reset_target_virtual_machine_scale_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetVirtualMachineScaleSetId", []))

    @jsii.member(jsii_name="resetTargetVirtualMachineSize")
    def reset_target_virtual_machine_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetVirtualMachineSize", []))

    @jsii.member(jsii_name="resetTargetZone")
    def reset_target_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetZone", []))

    @jsii.member(jsii_name="resetTestNetworkId")
    def reset_test_network_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTestNetworkId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUnmanagedDisk")
    def reset_unmanaged_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnmanagedDisk", []))

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
    @jsii.member(jsii_name="managedDisk")
    def managed_disk(self) -> "SiteRecoveryReplicatedVmManagedDiskList":
        return typing.cast("SiteRecoveryReplicatedVmManagedDiskList", jsii.get(self, "managedDisk"))

    @builtins.property
    @jsii.member(jsii_name="networkInterface")
    def network_interface(self) -> "SiteRecoveryReplicatedVmNetworkInterfaceList":
        return typing.cast("SiteRecoveryReplicatedVmNetworkInterfaceList", jsii.get(self, "networkInterface"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SiteRecoveryReplicatedVmTimeoutsOutputReference":
        return typing.cast("SiteRecoveryReplicatedVmTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="unmanagedDisk")
    def unmanaged_disk(self) -> "SiteRecoveryReplicatedVmUnmanagedDiskList":
        return typing.cast("SiteRecoveryReplicatedVmUnmanagedDiskList", jsii.get(self, "unmanagedDisk"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="managedDiskInput")
    def managed_disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmManagedDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmManagedDisk"]]], jsii.get(self, "managedDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="multiVmGroupNameInput")
    def multi_vm_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "multiVmGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceInput")
    def network_interface_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmNetworkInterface"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmNetworkInterface"]]], jsii.get(self, "networkInterfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryReplicationPolicyIdInput")
    def recovery_replication_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoveryReplicationPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryVaultNameInput")
    def recovery_vault_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoveryVaultNameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceRecoveryFabricNameInput")
    def source_recovery_fabric_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceRecoveryFabricNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceRecoveryProtectionContainerNameInput")
    def source_recovery_protection_container_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceRecoveryProtectionContainerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceVmIdInput")
    def source_vm_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceVmIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetAvailabilitySetIdInput")
    def target_availability_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetAvailabilitySetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetBootDiagnosticStorageAccountIdInput")
    def target_boot_diagnostic_storage_account_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetBootDiagnosticStorageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetCapacityReservationGroupIdInput")
    def target_capacity_reservation_group_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetCapacityReservationGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetEdgeZoneInput")
    def target_edge_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetEdgeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="targetNetworkIdInput")
    def target_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetProximityPlacementGroupIdInput")
    def target_proximity_placement_group_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetProximityPlacementGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRecoveryFabricIdInput")
    def target_recovery_fabric_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetRecoveryFabricIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRecoveryProtectionContainerIdInput")
    def target_recovery_protection_container_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetRecoveryProtectionContainerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceGroupIdInput")
    def target_resource_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetResourceGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetVirtualMachineScaleSetIdInput")
    def target_virtual_machine_scale_set_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetVirtualMachineScaleSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetVirtualMachineSizeInput")
    def target_virtual_machine_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetVirtualMachineSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetZoneInput")
    def target_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="testNetworkIdInput")
    def test_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "testNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SiteRecoveryReplicatedVmTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SiteRecoveryReplicatedVmTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="unmanagedDiskInput")
    def unmanaged_disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmUnmanagedDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmUnmanagedDisk"]]], jsii.get(self, "unmanagedDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95ce38d4938b6f71b54a2fe56e63cb5ddcda05de802e8e2f12d655568ed6edd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiVmGroupName")
    def multi_vm_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "multiVmGroupName"))

    @multi_vm_group_name.setter
    def multi_vm_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0bcfb839302e71e46d87f6c79e7d17263489513b9c65c8fca8646bfb1d3915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiVmGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b8ef2ce19656b125fe0e5cc1f8a0403b033b6ca1a2b914dbd94f2d983ad918f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryReplicationPolicyId")
    def recovery_replication_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recoveryReplicationPolicyId"))

    @recovery_replication_policy_id.setter
    def recovery_replication_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d893a1ec226d4e48e03b6074e035bf6dfe2c30cc69415ccdf284ad0644667e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryReplicationPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryVaultName")
    def recovery_vault_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recoveryVaultName"))

    @recovery_vault_name.setter
    def recovery_vault_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8db6b4db8bb6ee0fa79a08e8d64f5c87049d4195edd06ba7cc49c4efe85c8f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryVaultName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624fb5d8d4f0c1b5e843b58aeea10d16dbae897e1e9e921655b17667590aca7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceRecoveryFabricName")
    def source_recovery_fabric_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceRecoveryFabricName"))

    @source_recovery_fabric_name.setter
    def source_recovery_fabric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1160c9e69f91529aeab7f343e748969025e5e4c741031400ab742939db0281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceRecoveryFabricName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceRecoveryProtectionContainerName")
    def source_recovery_protection_container_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceRecoveryProtectionContainerName"))

    @source_recovery_protection_container_name.setter
    def source_recovery_protection_container_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e908b03c6e65b7e6be2387ae0db2d15fa09b6a4e6dd6f3ab6f5f21faf514cc12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceRecoveryProtectionContainerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceVmId")
    def source_vm_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceVmId"))

    @source_vm_id.setter
    def source_vm_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767e5544544955b09b6d9dc4595f3915e6ad22f1416786481f407ffea6d208aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceVmId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetAvailabilitySetId")
    def target_availability_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetAvailabilitySetId"))

    @target_availability_set_id.setter
    def target_availability_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b38412c3f6c7f981f892c0710a30024f8d947d0c340b70c71d0934fccb55631e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetAvailabilitySetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetBootDiagnosticStorageAccountId")
    def target_boot_diagnostic_storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetBootDiagnosticStorageAccountId"))

    @target_boot_diagnostic_storage_account_id.setter
    def target_boot_diagnostic_storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0198ad6155715194fff5c2943702dfd5ec01b3b64b732e5fbf175873a14b7fb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetBootDiagnosticStorageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetCapacityReservationGroupId")
    def target_capacity_reservation_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetCapacityReservationGroupId"))

    @target_capacity_reservation_group_id.setter
    def target_capacity_reservation_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ffffa3061c6393b19e15c7f4ecde4869d68080827eb6bcc62da10031409e8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetCapacityReservationGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetEdgeZone")
    def target_edge_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetEdgeZone"))

    @target_edge_zone.setter
    def target_edge_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37a9a78cc81cc4d875c617f143942564ecbece3dce00f38af6ed2aea9741fc27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetEdgeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetNetworkId")
    def target_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetNetworkId"))

    @target_network_id.setter
    def target_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ec118488ce4ee3fc7384332d2788698b089ef68cbc5fe8472e10abd9d44cd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetProximityPlacementGroupId")
    def target_proximity_placement_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetProximityPlacementGroupId"))

    @target_proximity_placement_group_id.setter
    def target_proximity_placement_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a0bc801d6fa9130ccdf7184b2797003657b38683d52d06bfe10f84378a7cd06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetProximityPlacementGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetRecoveryFabricId")
    def target_recovery_fabric_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetRecoveryFabricId"))

    @target_recovery_fabric_id.setter
    def target_recovery_fabric_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03e2dcd012dba7b5f92627a43e5ec9a387385bb365b9212a3850433bef527af6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRecoveryFabricId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetRecoveryProtectionContainerId")
    def target_recovery_protection_container_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetRecoveryProtectionContainerId"))

    @target_recovery_protection_container_id.setter
    def target_recovery_protection_container_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61fdebd7e414c43f8e9f98fce12253eef69a112fe5f77f5ef5b2cded609b2354)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRecoveryProtectionContainerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetResourceGroupId")
    def target_resource_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetResourceGroupId"))

    @target_resource_group_id.setter
    def target_resource_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a477da8f5a72d9ac7be75203e24dc4a2ec8b10f863c1586ba5dbf8887272083b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetResourceGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetVirtualMachineScaleSetId")
    def target_virtual_machine_scale_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetVirtualMachineScaleSetId"))

    @target_virtual_machine_scale_set_id.setter
    def target_virtual_machine_scale_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b82a5384aead2e505629d242c0e1f6c3e58076dbd645ea9e4b0955243e1a2a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetVirtualMachineScaleSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetVirtualMachineSize")
    def target_virtual_machine_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetVirtualMachineSize"))

    @target_virtual_machine_size.setter
    def target_virtual_machine_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d15674b7348ba5be89adf30eed74b6330bd0efc079874a8d3055f481fb2366d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetVirtualMachineSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetZone")
    def target_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetZone"))

    @target_zone.setter
    def target_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1b025f1db286ce0f46ec229857ce77977ee2a525fdcacbda5f480841bc8f7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="testNetworkId")
    def test_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "testNetworkId"))

    @test_network_id.setter
    def test_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3715aff2f2a2f14c98458252660599f7532e12c482d610cc0ddc50ab0d5f9f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "testNetworkId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "recovery_replication_policy_id": "recoveryReplicationPolicyId",
        "recovery_vault_name": "recoveryVaultName",
        "resource_group_name": "resourceGroupName",
        "source_recovery_fabric_name": "sourceRecoveryFabricName",
        "source_recovery_protection_container_name": "sourceRecoveryProtectionContainerName",
        "source_vm_id": "sourceVmId",
        "target_recovery_fabric_id": "targetRecoveryFabricId",
        "target_recovery_protection_container_id": "targetRecoveryProtectionContainerId",
        "target_resource_group_id": "targetResourceGroupId",
        "id": "id",
        "managed_disk": "managedDisk",
        "multi_vm_group_name": "multiVmGroupName",
        "network_interface": "networkInterface",
        "target_availability_set_id": "targetAvailabilitySetId",
        "target_boot_diagnostic_storage_account_id": "targetBootDiagnosticStorageAccountId",
        "target_capacity_reservation_group_id": "targetCapacityReservationGroupId",
        "target_edge_zone": "targetEdgeZone",
        "target_network_id": "targetNetworkId",
        "target_proximity_placement_group_id": "targetProximityPlacementGroupId",
        "target_virtual_machine_scale_set_id": "targetVirtualMachineScaleSetId",
        "target_virtual_machine_size": "targetVirtualMachineSize",
        "target_zone": "targetZone",
        "test_network_id": "testNetworkId",
        "timeouts": "timeouts",
        "unmanaged_disk": "unmanagedDisk",
    },
)
class SiteRecoveryReplicatedVmConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        recovery_replication_policy_id: builtins.str,
        recovery_vault_name: builtins.str,
        resource_group_name: builtins.str,
        source_recovery_fabric_name: builtins.str,
        source_recovery_protection_container_name: builtins.str,
        source_vm_id: builtins.str,
        target_recovery_fabric_id: builtins.str,
        target_recovery_protection_container_id: builtins.str,
        target_resource_group_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        managed_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicatedVmManagedDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        multi_vm_group_name: typing.Optional[builtins.str] = None,
        network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicatedVmNetworkInterface", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_availability_set_id: typing.Optional[builtins.str] = None,
        target_boot_diagnostic_storage_account_id: typing.Optional[builtins.str] = None,
        target_capacity_reservation_group_id: typing.Optional[builtins.str] = None,
        target_edge_zone: typing.Optional[builtins.str] = None,
        target_network_id: typing.Optional[builtins.str] = None,
        target_proximity_placement_group_id: typing.Optional[builtins.str] = None,
        target_virtual_machine_scale_set_id: typing.Optional[builtins.str] = None,
        target_virtual_machine_size: typing.Optional[builtins.str] = None,
        target_zone: typing.Optional[builtins.str] = None,
        test_network_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SiteRecoveryReplicatedVmTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        unmanaged_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicatedVmUnmanagedDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#name SiteRecoveryReplicatedVm#name}.
        :param recovery_replication_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#recovery_replication_policy_id SiteRecoveryReplicatedVm#recovery_replication_policy_id}.
        :param recovery_vault_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#recovery_vault_name SiteRecoveryReplicatedVm#recovery_vault_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#resource_group_name SiteRecoveryReplicatedVm#resource_group_name}.
        :param source_recovery_fabric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#source_recovery_fabric_name SiteRecoveryReplicatedVm#source_recovery_fabric_name}.
        :param source_recovery_protection_container_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#source_recovery_protection_container_name SiteRecoveryReplicatedVm#source_recovery_protection_container_name}.
        :param source_vm_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#source_vm_id SiteRecoveryReplicatedVm#source_vm_id}.
        :param target_recovery_fabric_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_recovery_fabric_id SiteRecoveryReplicatedVm#target_recovery_fabric_id}.
        :param target_recovery_protection_container_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_recovery_protection_container_id SiteRecoveryReplicatedVm#target_recovery_protection_container_id}.
        :param target_resource_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_resource_group_id SiteRecoveryReplicatedVm#target_resource_group_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#id SiteRecoveryReplicatedVm#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param managed_disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#managed_disk SiteRecoveryReplicatedVm#managed_disk}.
        :param multi_vm_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#multi_vm_group_name SiteRecoveryReplicatedVm#multi_vm_group_name}.
        :param network_interface: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#network_interface SiteRecoveryReplicatedVm#network_interface}.
        :param target_availability_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_availability_set_id SiteRecoveryReplicatedVm#target_availability_set_id}.
        :param target_boot_diagnostic_storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_boot_diagnostic_storage_account_id SiteRecoveryReplicatedVm#target_boot_diagnostic_storage_account_id}.
        :param target_capacity_reservation_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_capacity_reservation_group_id SiteRecoveryReplicatedVm#target_capacity_reservation_group_id}.
        :param target_edge_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_edge_zone SiteRecoveryReplicatedVm#target_edge_zone}.
        :param target_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_network_id SiteRecoveryReplicatedVm#target_network_id}.
        :param target_proximity_placement_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_proximity_placement_group_id SiteRecoveryReplicatedVm#target_proximity_placement_group_id}.
        :param target_virtual_machine_scale_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_virtual_machine_scale_set_id SiteRecoveryReplicatedVm#target_virtual_machine_scale_set_id}.
        :param target_virtual_machine_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_virtual_machine_size SiteRecoveryReplicatedVm#target_virtual_machine_size}.
        :param target_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_zone SiteRecoveryReplicatedVm#target_zone}.
        :param test_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#test_network_id SiteRecoveryReplicatedVm#test_network_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#timeouts SiteRecoveryReplicatedVm#timeouts}
        :param unmanaged_disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#unmanaged_disk SiteRecoveryReplicatedVm#unmanaged_disk}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = SiteRecoveryReplicatedVmTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c052d80b27126cce1524b21d47ea01a7544154071fc321787e4a923fcec4a2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument recovery_replication_policy_id", value=recovery_replication_policy_id, expected_type=type_hints["recovery_replication_policy_id"])
            check_type(argname="argument recovery_vault_name", value=recovery_vault_name, expected_type=type_hints["recovery_vault_name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument source_recovery_fabric_name", value=source_recovery_fabric_name, expected_type=type_hints["source_recovery_fabric_name"])
            check_type(argname="argument source_recovery_protection_container_name", value=source_recovery_protection_container_name, expected_type=type_hints["source_recovery_protection_container_name"])
            check_type(argname="argument source_vm_id", value=source_vm_id, expected_type=type_hints["source_vm_id"])
            check_type(argname="argument target_recovery_fabric_id", value=target_recovery_fabric_id, expected_type=type_hints["target_recovery_fabric_id"])
            check_type(argname="argument target_recovery_protection_container_id", value=target_recovery_protection_container_id, expected_type=type_hints["target_recovery_protection_container_id"])
            check_type(argname="argument target_resource_group_id", value=target_resource_group_id, expected_type=type_hints["target_resource_group_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument managed_disk", value=managed_disk, expected_type=type_hints["managed_disk"])
            check_type(argname="argument multi_vm_group_name", value=multi_vm_group_name, expected_type=type_hints["multi_vm_group_name"])
            check_type(argname="argument network_interface", value=network_interface, expected_type=type_hints["network_interface"])
            check_type(argname="argument target_availability_set_id", value=target_availability_set_id, expected_type=type_hints["target_availability_set_id"])
            check_type(argname="argument target_boot_diagnostic_storage_account_id", value=target_boot_diagnostic_storage_account_id, expected_type=type_hints["target_boot_diagnostic_storage_account_id"])
            check_type(argname="argument target_capacity_reservation_group_id", value=target_capacity_reservation_group_id, expected_type=type_hints["target_capacity_reservation_group_id"])
            check_type(argname="argument target_edge_zone", value=target_edge_zone, expected_type=type_hints["target_edge_zone"])
            check_type(argname="argument target_network_id", value=target_network_id, expected_type=type_hints["target_network_id"])
            check_type(argname="argument target_proximity_placement_group_id", value=target_proximity_placement_group_id, expected_type=type_hints["target_proximity_placement_group_id"])
            check_type(argname="argument target_virtual_machine_scale_set_id", value=target_virtual_machine_scale_set_id, expected_type=type_hints["target_virtual_machine_scale_set_id"])
            check_type(argname="argument target_virtual_machine_size", value=target_virtual_machine_size, expected_type=type_hints["target_virtual_machine_size"])
            check_type(argname="argument target_zone", value=target_zone, expected_type=type_hints["target_zone"])
            check_type(argname="argument test_network_id", value=test_network_id, expected_type=type_hints["test_network_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument unmanaged_disk", value=unmanaged_disk, expected_type=type_hints["unmanaged_disk"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "recovery_replication_policy_id": recovery_replication_policy_id,
            "recovery_vault_name": recovery_vault_name,
            "resource_group_name": resource_group_name,
            "source_recovery_fabric_name": source_recovery_fabric_name,
            "source_recovery_protection_container_name": source_recovery_protection_container_name,
            "source_vm_id": source_vm_id,
            "target_recovery_fabric_id": target_recovery_fabric_id,
            "target_recovery_protection_container_id": target_recovery_protection_container_id,
            "target_resource_group_id": target_resource_group_id,
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
        if managed_disk is not None:
            self._values["managed_disk"] = managed_disk
        if multi_vm_group_name is not None:
            self._values["multi_vm_group_name"] = multi_vm_group_name
        if network_interface is not None:
            self._values["network_interface"] = network_interface
        if target_availability_set_id is not None:
            self._values["target_availability_set_id"] = target_availability_set_id
        if target_boot_diagnostic_storage_account_id is not None:
            self._values["target_boot_diagnostic_storage_account_id"] = target_boot_diagnostic_storage_account_id
        if target_capacity_reservation_group_id is not None:
            self._values["target_capacity_reservation_group_id"] = target_capacity_reservation_group_id
        if target_edge_zone is not None:
            self._values["target_edge_zone"] = target_edge_zone
        if target_network_id is not None:
            self._values["target_network_id"] = target_network_id
        if target_proximity_placement_group_id is not None:
            self._values["target_proximity_placement_group_id"] = target_proximity_placement_group_id
        if target_virtual_machine_scale_set_id is not None:
            self._values["target_virtual_machine_scale_set_id"] = target_virtual_machine_scale_set_id
        if target_virtual_machine_size is not None:
            self._values["target_virtual_machine_size"] = target_virtual_machine_size
        if target_zone is not None:
            self._values["target_zone"] = target_zone
        if test_network_id is not None:
            self._values["test_network_id"] = test_network_id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if unmanaged_disk is not None:
            self._values["unmanaged_disk"] = unmanaged_disk

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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#name SiteRecoveryReplicatedVm#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def recovery_replication_policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#recovery_replication_policy_id SiteRecoveryReplicatedVm#recovery_replication_policy_id}.'''
        result = self._values.get("recovery_replication_policy_id")
        assert result is not None, "Required property 'recovery_replication_policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def recovery_vault_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#recovery_vault_name SiteRecoveryReplicatedVm#recovery_vault_name}.'''
        result = self._values.get("recovery_vault_name")
        assert result is not None, "Required property 'recovery_vault_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#resource_group_name SiteRecoveryReplicatedVm#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_recovery_fabric_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#source_recovery_fabric_name SiteRecoveryReplicatedVm#source_recovery_fabric_name}.'''
        result = self._values.get("source_recovery_fabric_name")
        assert result is not None, "Required property 'source_recovery_fabric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_recovery_protection_container_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#source_recovery_protection_container_name SiteRecoveryReplicatedVm#source_recovery_protection_container_name}.'''
        result = self._values.get("source_recovery_protection_container_name")
        assert result is not None, "Required property 'source_recovery_protection_container_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_vm_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#source_vm_id SiteRecoveryReplicatedVm#source_vm_id}.'''
        result = self._values.get("source_vm_id")
        assert result is not None, "Required property 'source_vm_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_recovery_fabric_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_recovery_fabric_id SiteRecoveryReplicatedVm#target_recovery_fabric_id}.'''
        result = self._values.get("target_recovery_fabric_id")
        assert result is not None, "Required property 'target_recovery_fabric_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_recovery_protection_container_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_recovery_protection_container_id SiteRecoveryReplicatedVm#target_recovery_protection_container_id}.'''
        result = self._values.get("target_recovery_protection_container_id")
        assert result is not None, "Required property 'target_recovery_protection_container_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_resource_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_resource_group_id SiteRecoveryReplicatedVm#target_resource_group_id}.'''
        result = self._values.get("target_resource_group_id")
        assert result is not None, "Required property 'target_resource_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#id SiteRecoveryReplicatedVm#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmManagedDisk"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#managed_disk SiteRecoveryReplicatedVm#managed_disk}.'''
        result = self._values.get("managed_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmManagedDisk"]]], result)

    @builtins.property
    def multi_vm_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#multi_vm_group_name SiteRecoveryReplicatedVm#multi_vm_group_name}.'''
        result = self._values.get("multi_vm_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_interface(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmNetworkInterface"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#network_interface SiteRecoveryReplicatedVm#network_interface}.'''
        result = self._values.get("network_interface")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmNetworkInterface"]]], result)

    @builtins.property
    def target_availability_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_availability_set_id SiteRecoveryReplicatedVm#target_availability_set_id}.'''
        result = self._values.get("target_availability_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_boot_diagnostic_storage_account_id(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_boot_diagnostic_storage_account_id SiteRecoveryReplicatedVm#target_boot_diagnostic_storage_account_id}.'''
        result = self._values.get("target_boot_diagnostic_storage_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_capacity_reservation_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_capacity_reservation_group_id SiteRecoveryReplicatedVm#target_capacity_reservation_group_id}.'''
        result = self._values.get("target_capacity_reservation_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_edge_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_edge_zone SiteRecoveryReplicatedVm#target_edge_zone}.'''
        result = self._values.get("target_edge_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_network_id SiteRecoveryReplicatedVm#target_network_id}.'''
        result = self._values.get("target_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_proximity_placement_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_proximity_placement_group_id SiteRecoveryReplicatedVm#target_proximity_placement_group_id}.'''
        result = self._values.get("target_proximity_placement_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_virtual_machine_scale_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_virtual_machine_scale_set_id SiteRecoveryReplicatedVm#target_virtual_machine_scale_set_id}.'''
        result = self._values.get("target_virtual_machine_scale_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_virtual_machine_size(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_virtual_machine_size SiteRecoveryReplicatedVm#target_virtual_machine_size}.'''
        result = self._values.get("target_virtual_machine_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_zone SiteRecoveryReplicatedVm#target_zone}.'''
        result = self._values.get("target_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def test_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#test_network_id SiteRecoveryReplicatedVm#test_network_id}.'''
        result = self._values.get("test_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SiteRecoveryReplicatedVmTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#timeouts SiteRecoveryReplicatedVm#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SiteRecoveryReplicatedVmTimeouts"], result)

    @builtins.property
    def unmanaged_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmUnmanagedDisk"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#unmanaged_disk SiteRecoveryReplicatedVm#unmanaged_disk}.'''
        result = self._values.get("unmanaged_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmUnmanagedDisk"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicatedVmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmManagedDisk",
    jsii_struct_bases=[],
    name_mapping={
        "disk_id": "diskId",
        "staging_storage_account_id": "stagingStorageAccountId",
        "target_disk_encryption": "targetDiskEncryption",
        "target_disk_encryption_set_id": "targetDiskEncryptionSetId",
        "target_disk_type": "targetDiskType",
        "target_replica_disk_type": "targetReplicaDiskType",
        "target_resource_group_id": "targetResourceGroupId",
    },
)
class SiteRecoveryReplicatedVmManagedDisk:
    def __init__(
        self,
        *,
        disk_id: typing.Optional[builtins.str] = None,
        staging_storage_account_id: typing.Optional[builtins.str] = None,
        target_disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_disk_encryption_set_id: typing.Optional[builtins.str] = None,
        target_disk_type: typing.Optional[builtins.str] = None,
        target_replica_disk_type: typing.Optional[builtins.str] = None,
        target_resource_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#disk_id SiteRecoveryReplicatedVm#disk_id}.
        :param staging_storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#staging_storage_account_id SiteRecoveryReplicatedVm#staging_storage_account_id}.
        :param target_disk_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_disk_encryption SiteRecoveryReplicatedVm#target_disk_encryption}.
        :param target_disk_encryption_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_disk_encryption_set_id SiteRecoveryReplicatedVm#target_disk_encryption_set_id}.
        :param target_disk_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_disk_type SiteRecoveryReplicatedVm#target_disk_type}.
        :param target_replica_disk_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_replica_disk_type SiteRecoveryReplicatedVm#target_replica_disk_type}.
        :param target_resource_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_resource_group_id SiteRecoveryReplicatedVm#target_resource_group_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51cea3acd5ebf07391c70753005724165db986668fb03eb6abdba4be643745a2)
            check_type(argname="argument disk_id", value=disk_id, expected_type=type_hints["disk_id"])
            check_type(argname="argument staging_storage_account_id", value=staging_storage_account_id, expected_type=type_hints["staging_storage_account_id"])
            check_type(argname="argument target_disk_encryption", value=target_disk_encryption, expected_type=type_hints["target_disk_encryption"])
            check_type(argname="argument target_disk_encryption_set_id", value=target_disk_encryption_set_id, expected_type=type_hints["target_disk_encryption_set_id"])
            check_type(argname="argument target_disk_type", value=target_disk_type, expected_type=type_hints["target_disk_type"])
            check_type(argname="argument target_replica_disk_type", value=target_replica_disk_type, expected_type=type_hints["target_replica_disk_type"])
            check_type(argname="argument target_resource_group_id", value=target_resource_group_id, expected_type=type_hints["target_resource_group_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_id is not None:
            self._values["disk_id"] = disk_id
        if staging_storage_account_id is not None:
            self._values["staging_storage_account_id"] = staging_storage_account_id
        if target_disk_encryption is not None:
            self._values["target_disk_encryption"] = target_disk_encryption
        if target_disk_encryption_set_id is not None:
            self._values["target_disk_encryption_set_id"] = target_disk_encryption_set_id
        if target_disk_type is not None:
            self._values["target_disk_type"] = target_disk_type
        if target_replica_disk_type is not None:
            self._values["target_replica_disk_type"] = target_replica_disk_type
        if target_resource_group_id is not None:
            self._values["target_resource_group_id"] = target_resource_group_id

    @builtins.property
    def disk_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#disk_id SiteRecoveryReplicatedVm#disk_id}.'''
        result = self._values.get("disk_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def staging_storage_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#staging_storage_account_id SiteRecoveryReplicatedVm#staging_storage_account_id}.'''
        result = self._values.get("staging_storage_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_disk_encryption(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_disk_encryption SiteRecoveryReplicatedVm#target_disk_encryption}.'''
        result = self._values.get("target_disk_encryption")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption"]]], result)

    @builtins.property
    def target_disk_encryption_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_disk_encryption_set_id SiteRecoveryReplicatedVm#target_disk_encryption_set_id}.'''
        result = self._values.get("target_disk_encryption_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_disk_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_disk_type SiteRecoveryReplicatedVm#target_disk_type}.'''
        result = self._values.get("target_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_replica_disk_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_replica_disk_type SiteRecoveryReplicatedVm#target_replica_disk_type}.'''
        result = self._values.get("target_replica_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_resource_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_resource_group_id SiteRecoveryReplicatedVm#target_resource_group_id}.'''
        result = self._values.get("target_resource_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicatedVmManagedDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryReplicatedVmManagedDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmManagedDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63f913b129d292cdea1d51dc84b840262da8ee1ad9bddbce668be90efc592208)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SiteRecoveryReplicatedVmManagedDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74e642bf61288eabb80042ed0501f94a55b0a790bb9a08bf8b881151181d8873)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SiteRecoveryReplicatedVmManagedDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__362117f511ce1b2288399579fefee3e7e823c3b488229edf5c16d407a809f25f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6247b365933b9a18d5136d450a968a65106ca0e073c7d5884dccb5be72e84a05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__438537280b6b6fba4c9854f86ff4f63d8a2f6fac55b0fca06ec3832bfd8bb37b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25e83457815efc2283f9a4365eeb0f223e5138431cbeefeeac4088d87f57905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SiteRecoveryReplicatedVmManagedDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmManagedDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38ec60f51679593d84c6db0f621ad69085634f835284cb58e729805eb56f844c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTargetDiskEncryption")
    def put_target_disk_encryption(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5160e09c3ec35589fa1ebd4f4fa1d4cd4cbe6ba53244b68262b819cbc06f8fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargetDiskEncryption", [value]))

    @jsii.member(jsii_name="resetDiskId")
    def reset_disk_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskId", []))

    @jsii.member(jsii_name="resetStagingStorageAccountId")
    def reset_staging_storage_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStagingStorageAccountId", []))

    @jsii.member(jsii_name="resetTargetDiskEncryption")
    def reset_target_disk_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetDiskEncryption", []))

    @jsii.member(jsii_name="resetTargetDiskEncryptionSetId")
    def reset_target_disk_encryption_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetDiskEncryptionSetId", []))

    @jsii.member(jsii_name="resetTargetDiskType")
    def reset_target_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetDiskType", []))

    @jsii.member(jsii_name="resetTargetReplicaDiskType")
    def reset_target_replica_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetReplicaDiskType", []))

    @jsii.member(jsii_name="resetTargetResourceGroupId")
    def reset_target_resource_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetResourceGroupId", []))

    @builtins.property
    @jsii.member(jsii_name="targetDiskEncryption")
    def target_disk_encryption(
        self,
    ) -> "SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionList":
        return typing.cast("SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionList", jsii.get(self, "targetDiskEncryption"))

    @builtins.property
    @jsii.member(jsii_name="diskIdInput")
    def disk_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskIdInput"))

    @builtins.property
    @jsii.member(jsii_name="stagingStorageAccountIdInput")
    def staging_storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stagingStorageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetDiskEncryptionInput")
    def target_disk_encryption_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption"]]], jsii.get(self, "targetDiskEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="targetDiskEncryptionSetIdInput")
    def target_disk_encryption_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetDiskEncryptionSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetDiskTypeInput")
    def target_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetReplicaDiskTypeInput")
    def target_replica_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetReplicaDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceGroupIdInput")
    def target_resource_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetResourceGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="diskId")
    def disk_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskId"))

    @disk_id.setter
    def disk_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06af984aeada6727eee114f0a600dc7622e5d33d2c9865020ff69e4102133710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stagingStorageAccountId")
    def staging_storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stagingStorageAccountId"))

    @staging_storage_account_id.setter
    def staging_storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0df637f1bda8eefe3784a7786d901250368a9e6fbfce05b1ebf2c135943ca0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stagingStorageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetDiskEncryptionSetId")
    def target_disk_encryption_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetDiskEncryptionSetId"))

    @target_disk_encryption_set_id.setter
    def target_disk_encryption_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52d2bda658ca94f026e845bf78a91b643e0dc7c11823486a4e59c2df4fc50313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetDiskEncryptionSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetDiskType")
    def target_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetDiskType"))

    @target_disk_type.setter
    def target_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c45734d4030ec4c90956e93cb3148d7bc900782070c1e1e47645ab5ab3465727)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetReplicaDiskType")
    def target_replica_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetReplicaDiskType"))

    @target_replica_disk_type.setter
    def target_replica_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5c016167ddcef0e6be67413821a2ace37c102f3cb48de21498eb0b7ddcec0c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetReplicaDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetResourceGroupId")
    def target_resource_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetResourceGroupId"))

    @target_resource_group_id.setter
    def target_resource_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b5d250b8fb5e0f32fea37106da095e726fda398a0069de0414a09787f0d6b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetResourceGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmManagedDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmManagedDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmManagedDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0bbebbb447b790167ec261ba6061f5ab05728dbcaabac19aff2603fa8f99d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption",
    jsii_struct_bases=[],
    name_mapping={
        "disk_encryption_key": "diskEncryptionKey",
        "key_encryption_key": "keyEncryptionKey",
    },
)
class SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption:
    def __init__(
        self,
        *,
        disk_encryption_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey", typing.Dict[builtins.str, typing.Any]]]]] = None,
        key_encryption_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param disk_encryption_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#disk_encryption_key SiteRecoveryReplicatedVm#disk_encryption_key}.
        :param key_encryption_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#key_encryption_key SiteRecoveryReplicatedVm#key_encryption_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f9181fa25a2eee7f11431ff3d14d05b190589a5bb1e717b1f963c7529b2bb0f)
            check_type(argname="argument disk_encryption_key", value=disk_encryption_key, expected_type=type_hints["disk_encryption_key"])
            check_type(argname="argument key_encryption_key", value=key_encryption_key, expected_type=type_hints["key_encryption_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_encryption_key is not None:
            self._values["disk_encryption_key"] = disk_encryption_key
        if key_encryption_key is not None:
            self._values["key_encryption_key"] = key_encryption_key

    @builtins.property
    def disk_encryption_key(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#disk_encryption_key SiteRecoveryReplicatedVm#disk_encryption_key}.'''
        result = self._values.get("disk_encryption_key")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey"]]], result)

    @builtins.property
    def key_encryption_key(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#key_encryption_key SiteRecoveryReplicatedVm#key_encryption_key}.'''
        result = self._values.get("key_encryption_key")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={"secret_url": "secretUrl", "vault_id": "vaultId"},
)
class SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey:
    def __init__(
        self,
        *,
        secret_url: typing.Optional[builtins.str] = None,
        vault_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#secret_url SiteRecoveryReplicatedVm#secret_url}.
        :param vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#vault_id SiteRecoveryReplicatedVm#vault_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__139490f4a2b73d6258221abd4efd193a28a572da4be77e190eb8509d64f57a92)
            check_type(argname="argument secret_url", value=secret_url, expected_type=type_hints["secret_url"])
            check_type(argname="argument vault_id", value=vault_id, expected_type=type_hints["vault_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if secret_url is not None:
            self._values["secret_url"] = secret_url
        if vault_id is not None:
            self._values["vault_id"] = vault_id

    @builtins.property
    def secret_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#secret_url SiteRecoveryReplicatedVm#secret_url}.'''
        result = self._values.get("secret_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vault_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#vault_id SiteRecoveryReplicatedVm#vault_id}.'''
        result = self._values.get("vault_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKeyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKeyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed4643f7d0f16d62543709a9fb34703f5ef6f87336618090e7777571c6a3cd5c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKeyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faa8eaf19e5823c1d258f09a726bb9c4b885e7197e5fd268d85a292d3419bc08)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKeyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7840d9ff803a6993bfdda68891bf2806c65d4ab211c01cb9a0998133352f169c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cc698e9b1bc5fdb7a6bb264e56d07dfc80032bbc6e59507b1545df60522630f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67380da37ca1dd07dddc96578f1cfc2a4f51b6831db1d18b94d0b503e3fd6602)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1d09994f1762e392a928bef3196b422610f10c730cb4b7368452d7dab50f9c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b6f40a42a2bd6369b36e0d315b708add1b748d8031752ee21d740f824b6fc55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSecretUrl")
    def reset_secret_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretUrl", []))

    @jsii.member(jsii_name="resetVaultId")
    def reset_vault_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVaultId", []))

    @builtins.property
    @jsii.member(jsii_name="secretUrlInput")
    def secret_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="vaultIdInput")
    def vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="secretUrl")
    def secret_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretUrl"))

    @secret_url.setter
    def secret_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16ef7752f6e0845e0f5a899f32a68accce70d45a037e1fb83a71ac63683f8a71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vaultId")
    def vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vaultId"))

    @vault_id.setter
    def vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af188e89cf4f961450244362eb68b3350c9b5c49b996373598dc15df4af6ed3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e40d6a24bc6373709cd3c3b00b1bd82d6fbe06ec741e55e85218fc0ed59d2099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={"key_url": "keyUrl", "vault_id": "vaultId"},
)
class SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey:
    def __init__(
        self,
        *,
        key_url: typing.Optional[builtins.str] = None,
        vault_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#key_url SiteRecoveryReplicatedVm#key_url}.
        :param vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#vault_id SiteRecoveryReplicatedVm#vault_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dfef0fa9fd86f83edaad7ed146564911b8278ee2ea3f19bcfb7f4033f68adcd)
            check_type(argname="argument key_url", value=key_url, expected_type=type_hints["key_url"])
            check_type(argname="argument vault_id", value=vault_id, expected_type=type_hints["vault_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key_url is not None:
            self._values["key_url"] = key_url
        if vault_id is not None:
            self._values["vault_id"] = vault_id

    @builtins.property
    def key_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#key_url SiteRecoveryReplicatedVm#key_url}.'''
        result = self._values.get("key_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vault_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#vault_id SiteRecoveryReplicatedVm#vault_id}.'''
        result = self._values.get("vault_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKeyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKeyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__150280b33fd729de7cf9d2cc126446f3415635d57c30cfacf7c5783af51f32ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKeyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6006991ae03ac5d79484fcb829d97cf1126bb319233b3764dd92d0b2ca15347a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKeyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c6f2eb0d4a714757e43dc5a8c5581ddf1c1ed95e335e0492a64207a1f5fa82c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cb35927623f117ccc1eaaed45040f85a59fc68aded94ed8c13aab144aa2c656)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8d595397095388f34e679ac97c11149fe781d8aaeb053ed6c45af0819371a82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aebb11694de52420f18baae5f6b115c41e4549a2716331cadd6af1eaa847d9fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f82951bef34186aec115df37856c71355c3eab65ac3e0e09337671dce82c4194)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKeyUrl")
    def reset_key_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyUrl", []))

    @jsii.member(jsii_name="resetVaultId")
    def reset_vault_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVaultId", []))

    @builtins.property
    @jsii.member(jsii_name="keyUrlInput")
    def key_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="vaultIdInput")
    def vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyUrl")
    def key_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyUrl"))

    @key_url.setter
    def key_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d981751f97d79c76026ba6ab6509c9448966bf8efbaefe360fe03d806e22ddec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vaultId")
    def vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vaultId"))

    @vault_id.setter
    def vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d3c77871e2020d83d169892085313c36e675512c8356f2a7cb974dd5f1a812a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5917da5ff21dc1928fe870f5fa858b30291e2dee4229615c2cd184015e21bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28e5c11dd8fdbe10fe251d316d329afa8d1147bc41231178237b342d23c918fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3badd5a0dae5c6f446a45ed7f09a94ca540c47552b90fd307b93ca6f30c36e4b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2f4b303baf7960f3308d6f94b2422542ea11063a0819401d2645da155f8ba3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__233dbdf1a0bba5b3a3b5a98f203028c6aca5b0147e4fe32475c7793f21943fa5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e04f566bd7a45cebaeba57d6505e0c5491abd7e51028652a70ab9f2cf07cd92f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__018dbd0f66121433dc8b792c8daf67820640d96b3dde7d0d772344a2a4c683db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64464825d46e9f727bfdaf66ca2685be1049afddee9d270d82b3235b5858396b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDiskEncryptionKey")
    def put_disk_encryption_key(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d3abc09d9dc18d7eb468f29cb2d670a40881ccf163dea973f47a7fdf7300544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDiskEncryptionKey", [value]))

    @jsii.member(jsii_name="putKeyEncryptionKey")
    def put_key_encryption_key(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6791f339f83c93692d4740b87e7f7a56f8a7b8714a303ae9881a26d0ca9e34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKeyEncryptionKey", [value]))

    @jsii.member(jsii_name="resetDiskEncryptionKey")
    def reset_disk_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionKey", []))

    @jsii.member(jsii_name="resetKeyEncryptionKey")
    def reset_key_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyEncryptionKey", []))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKey")
    def disk_encryption_key(
        self,
    ) -> SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKeyList:
        return typing.cast(SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKeyList, jsii.get(self, "diskEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="keyEncryptionKey")
    def key_encryption_key(
        self,
    ) -> SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKeyList:
        return typing.cast(SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKeyList, jsii.get(self, "keyEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeyInput")
    def disk_encryption_key_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey]]], jsii.get(self, "diskEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="keyEncryptionKeyInput")
    def key_encryption_key_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey]]], jsii.get(self, "keyEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__626c34ad7e8facba662253ba2d6842e83a17ffffdbceb15454404a9dd0e70321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmNetworkInterface",
    jsii_struct_bases=[],
    name_mapping={
        "failover_test_public_ip_address_id": "failoverTestPublicIpAddressId",
        "failover_test_static_ip": "failoverTestStaticIp",
        "failover_test_subnet_name": "failoverTestSubnetName",
        "recovery_load_balancer_backend_address_pool_ids": "recoveryLoadBalancerBackendAddressPoolIds",
        "recovery_public_ip_address_id": "recoveryPublicIpAddressId",
        "source_network_interface_id": "sourceNetworkInterfaceId",
        "target_static_ip": "targetStaticIp",
        "target_subnet_name": "targetSubnetName",
    },
)
class SiteRecoveryReplicatedVmNetworkInterface:
    def __init__(
        self,
        *,
        failover_test_public_ip_address_id: typing.Optional[builtins.str] = None,
        failover_test_static_ip: typing.Optional[builtins.str] = None,
        failover_test_subnet_name: typing.Optional[builtins.str] = None,
        recovery_load_balancer_backend_address_pool_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        recovery_public_ip_address_id: typing.Optional[builtins.str] = None,
        source_network_interface_id: typing.Optional[builtins.str] = None,
        target_static_ip: typing.Optional[builtins.str] = None,
        target_subnet_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param failover_test_public_ip_address_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#failover_test_public_ip_address_id SiteRecoveryReplicatedVm#failover_test_public_ip_address_id}.
        :param failover_test_static_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#failover_test_static_ip SiteRecoveryReplicatedVm#failover_test_static_ip}.
        :param failover_test_subnet_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#failover_test_subnet_name SiteRecoveryReplicatedVm#failover_test_subnet_name}.
        :param recovery_load_balancer_backend_address_pool_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#recovery_load_balancer_backend_address_pool_ids SiteRecoveryReplicatedVm#recovery_load_balancer_backend_address_pool_ids}.
        :param recovery_public_ip_address_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#recovery_public_ip_address_id SiteRecoveryReplicatedVm#recovery_public_ip_address_id}.
        :param source_network_interface_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#source_network_interface_id SiteRecoveryReplicatedVm#source_network_interface_id}.
        :param target_static_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_static_ip SiteRecoveryReplicatedVm#target_static_ip}.
        :param target_subnet_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_subnet_name SiteRecoveryReplicatedVm#target_subnet_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae06ab7804ee879779d6084bf6a07ad63a1afe60537790e28905e03e9938a84d)
            check_type(argname="argument failover_test_public_ip_address_id", value=failover_test_public_ip_address_id, expected_type=type_hints["failover_test_public_ip_address_id"])
            check_type(argname="argument failover_test_static_ip", value=failover_test_static_ip, expected_type=type_hints["failover_test_static_ip"])
            check_type(argname="argument failover_test_subnet_name", value=failover_test_subnet_name, expected_type=type_hints["failover_test_subnet_name"])
            check_type(argname="argument recovery_load_balancer_backend_address_pool_ids", value=recovery_load_balancer_backend_address_pool_ids, expected_type=type_hints["recovery_load_balancer_backend_address_pool_ids"])
            check_type(argname="argument recovery_public_ip_address_id", value=recovery_public_ip_address_id, expected_type=type_hints["recovery_public_ip_address_id"])
            check_type(argname="argument source_network_interface_id", value=source_network_interface_id, expected_type=type_hints["source_network_interface_id"])
            check_type(argname="argument target_static_ip", value=target_static_ip, expected_type=type_hints["target_static_ip"])
            check_type(argname="argument target_subnet_name", value=target_subnet_name, expected_type=type_hints["target_subnet_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if failover_test_public_ip_address_id is not None:
            self._values["failover_test_public_ip_address_id"] = failover_test_public_ip_address_id
        if failover_test_static_ip is not None:
            self._values["failover_test_static_ip"] = failover_test_static_ip
        if failover_test_subnet_name is not None:
            self._values["failover_test_subnet_name"] = failover_test_subnet_name
        if recovery_load_balancer_backend_address_pool_ids is not None:
            self._values["recovery_load_balancer_backend_address_pool_ids"] = recovery_load_balancer_backend_address_pool_ids
        if recovery_public_ip_address_id is not None:
            self._values["recovery_public_ip_address_id"] = recovery_public_ip_address_id
        if source_network_interface_id is not None:
            self._values["source_network_interface_id"] = source_network_interface_id
        if target_static_ip is not None:
            self._values["target_static_ip"] = target_static_ip
        if target_subnet_name is not None:
            self._values["target_subnet_name"] = target_subnet_name

    @builtins.property
    def failover_test_public_ip_address_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#failover_test_public_ip_address_id SiteRecoveryReplicatedVm#failover_test_public_ip_address_id}.'''
        result = self._values.get("failover_test_public_ip_address_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failover_test_static_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#failover_test_static_ip SiteRecoveryReplicatedVm#failover_test_static_ip}.'''
        result = self._values.get("failover_test_static_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failover_test_subnet_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#failover_test_subnet_name SiteRecoveryReplicatedVm#failover_test_subnet_name}.'''
        result = self._values.get("failover_test_subnet_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recovery_load_balancer_backend_address_pool_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#recovery_load_balancer_backend_address_pool_ids SiteRecoveryReplicatedVm#recovery_load_balancer_backend_address_pool_ids}.'''
        result = self._values.get("recovery_load_balancer_backend_address_pool_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def recovery_public_ip_address_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#recovery_public_ip_address_id SiteRecoveryReplicatedVm#recovery_public_ip_address_id}.'''
        result = self._values.get("recovery_public_ip_address_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_network_interface_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#source_network_interface_id SiteRecoveryReplicatedVm#source_network_interface_id}.'''
        result = self._values.get("source_network_interface_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_static_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_static_ip SiteRecoveryReplicatedVm#target_static_ip}.'''
        result = self._values.get("target_static_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_subnet_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_subnet_name SiteRecoveryReplicatedVm#target_subnet_name}.'''
        result = self._values.get("target_subnet_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicatedVmNetworkInterface(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryReplicatedVmNetworkInterfaceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmNetworkInterfaceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dbfe4353bdea44bb14b14e7304641a1aa1097066f6486208b2e8e1a78e4ab15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SiteRecoveryReplicatedVmNetworkInterfaceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0151a9e4443e068f48f6ea6e64f71b5abe107e03496822f593e6fe4f3030ea40)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SiteRecoveryReplicatedVmNetworkInterfaceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95a9ed6393e4e99ab97a0329cfbc9956a1a55062dea779f0b63359a6151de6a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e6ea04b0e812cfb66e6d8dfc50d30962377c6185ad6fe984f865ead3ab47da0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d0774567876036ad901fb1ffc164d57bc8623895e06df510dcbd7cbf45d0082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmNetworkInterface]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmNetworkInterface]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmNetworkInterface]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0adf21cb6996f7cef0b537e015e7a4ebc3fb387c0ced91f93b7245c3ab3ea018)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SiteRecoveryReplicatedVmNetworkInterfaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmNetworkInterfaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9e82f126e9639e73c7b7e2ef035bf5481f810529b8f1a76153998ab71dbdb6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFailoverTestPublicIpAddressId")
    def reset_failover_test_public_ip_address_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailoverTestPublicIpAddressId", []))

    @jsii.member(jsii_name="resetFailoverTestStaticIp")
    def reset_failover_test_static_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailoverTestStaticIp", []))

    @jsii.member(jsii_name="resetFailoverTestSubnetName")
    def reset_failover_test_subnet_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailoverTestSubnetName", []))

    @jsii.member(jsii_name="resetRecoveryLoadBalancerBackendAddressPoolIds")
    def reset_recovery_load_balancer_backend_address_pool_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecoveryLoadBalancerBackendAddressPoolIds", []))

    @jsii.member(jsii_name="resetRecoveryPublicIpAddressId")
    def reset_recovery_public_ip_address_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecoveryPublicIpAddressId", []))

    @jsii.member(jsii_name="resetSourceNetworkInterfaceId")
    def reset_source_network_interface_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceNetworkInterfaceId", []))

    @jsii.member(jsii_name="resetTargetStaticIp")
    def reset_target_static_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetStaticIp", []))

    @jsii.member(jsii_name="resetTargetSubnetName")
    def reset_target_subnet_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetSubnetName", []))

    @builtins.property
    @jsii.member(jsii_name="failoverTestPublicIpAddressIdInput")
    def failover_test_public_ip_address_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "failoverTestPublicIpAddressIdInput"))

    @builtins.property
    @jsii.member(jsii_name="failoverTestStaticIpInput")
    def failover_test_static_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "failoverTestStaticIpInput"))

    @builtins.property
    @jsii.member(jsii_name="failoverTestSubnetNameInput")
    def failover_test_subnet_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "failoverTestSubnetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryLoadBalancerBackendAddressPoolIdsInput")
    def recovery_load_balancer_backend_address_pool_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "recoveryLoadBalancerBackendAddressPoolIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryPublicIpAddressIdInput")
    def recovery_public_ip_address_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoveryPublicIpAddressIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceNetworkInterfaceIdInput")
    def source_network_interface_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceNetworkInterfaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetStaticIpInput")
    def target_static_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetStaticIpInput"))

    @builtins.property
    @jsii.member(jsii_name="targetSubnetNameInput")
    def target_subnet_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetSubnetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="failoverTestPublicIpAddressId")
    def failover_test_public_ip_address_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failoverTestPublicIpAddressId"))

    @failover_test_public_ip_address_id.setter
    def failover_test_public_ip_address_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70aaf87fe7ee281e1a7e074ec634c0f6c4ea0043997f41647c64c427084400a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failoverTestPublicIpAddressId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failoverTestStaticIp")
    def failover_test_static_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failoverTestStaticIp"))

    @failover_test_static_ip.setter
    def failover_test_static_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a092216c68a301b5d3499e00119b09c5093727258f5122d34a809a19eb4a4796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failoverTestStaticIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failoverTestSubnetName")
    def failover_test_subnet_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failoverTestSubnetName"))

    @failover_test_subnet_name.setter
    def failover_test_subnet_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a5c1a67507b50b84dda378d7dca440fa9b89297dc80c8c13e2866f36605ef54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failoverTestSubnetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryLoadBalancerBackendAddressPoolIds")
    def recovery_load_balancer_backend_address_pool_ids(
        self,
    ) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "recoveryLoadBalancerBackendAddressPoolIds"))

    @recovery_load_balancer_backend_address_pool_ids.setter
    def recovery_load_balancer_backend_address_pool_ids(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e01ff0d023567f169558f29e85ecea48606e0ca5a445a0d8899bf72b096aade6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryLoadBalancerBackendAddressPoolIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryPublicIpAddressId")
    def recovery_public_ip_address_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recoveryPublicIpAddressId"))

    @recovery_public_ip_address_id.setter
    def recovery_public_ip_address_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa1625779d3b7e9c471782048430ea710ce1d7ed69695c4c4752bb37114c669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryPublicIpAddressId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceNetworkInterfaceId")
    def source_network_interface_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceNetworkInterfaceId"))

    @source_network_interface_id.setter
    def source_network_interface_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76822ae431aa93f711cfdc52a997a57a895036be39c53b87cb0584adf041c26a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceNetworkInterfaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetStaticIp")
    def target_static_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetStaticIp"))

    @target_static_ip.setter
    def target_static_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a01eaa931312e5d3bdb7a4972aa841469c94d46a2a7a6f8ebc3a0e94370f07d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetStaticIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetSubnetName")
    def target_subnet_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetSubnetName"))

    @target_subnet_name.setter
    def target_subnet_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e19985c61448aa51f423082137e7940e1589994fbfe54a16725355cd0a178806)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetSubnetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmNetworkInterface]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmNetworkInterface]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmNetworkInterface]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb47f7fad336b48f22fae272183253fc3094218888993d70de4301c80bc2d463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SiteRecoveryReplicatedVmTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#create SiteRecoveryReplicatedVm#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#delete SiteRecoveryReplicatedVm#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#read SiteRecoveryReplicatedVm#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#update SiteRecoveryReplicatedVm#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f36a469156cae8e0c220ae212ded7668cc519480e5ca7278ff8284885e9362)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#create SiteRecoveryReplicatedVm#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#delete SiteRecoveryReplicatedVm#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#read SiteRecoveryReplicatedVm#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#update SiteRecoveryReplicatedVm#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicatedVmTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryReplicatedVmTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aefa5cf134b2bb29f7c9be7f77b1e406f3b2040b89179765fd1b4af24e155c52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18dd199d48828fd2769498c1c8d370197537fc3f1df4aa4f31731f8ab2736b96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd006ce5a89ab5715febbe09d506d9a3dabf5226c21b8ec8345a25d3d7510fda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__881e68af098f980c027c7ac4e42d038c0ed61fec5499b05d016abce0566d32c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f162e7ca448412936d90ff498197558322c5084b0b0602f926765d5f0698ae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a8a65132370293b29fe363eea14145d1c091474376557069db007bf443d35e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmUnmanagedDisk",
    jsii_struct_bases=[],
    name_mapping={
        "disk_uri": "diskUri",
        "staging_storage_account_id": "stagingStorageAccountId",
        "target_storage_account_id": "targetStorageAccountId",
    },
)
class SiteRecoveryReplicatedVmUnmanagedDisk:
    def __init__(
        self,
        *,
        disk_uri: typing.Optional[builtins.str] = None,
        staging_storage_account_id: typing.Optional[builtins.str] = None,
        target_storage_account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#disk_uri SiteRecoveryReplicatedVm#disk_uri}.
        :param staging_storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#staging_storage_account_id SiteRecoveryReplicatedVm#staging_storage_account_id}.
        :param target_storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_storage_account_id SiteRecoveryReplicatedVm#target_storage_account_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7912d71802c44bafc15b04d54875737302051223e944b07affdd3529f1d56428)
            check_type(argname="argument disk_uri", value=disk_uri, expected_type=type_hints["disk_uri"])
            check_type(argname="argument staging_storage_account_id", value=staging_storage_account_id, expected_type=type_hints["staging_storage_account_id"])
            check_type(argname="argument target_storage_account_id", value=target_storage_account_id, expected_type=type_hints["target_storage_account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_uri is not None:
            self._values["disk_uri"] = disk_uri
        if staging_storage_account_id is not None:
            self._values["staging_storage_account_id"] = staging_storage_account_id
        if target_storage_account_id is not None:
            self._values["target_storage_account_id"] = target_storage_account_id

    @builtins.property
    def disk_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#disk_uri SiteRecoveryReplicatedVm#disk_uri}.'''
        result = self._values.get("disk_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def staging_storage_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#staging_storage_account_id SiteRecoveryReplicatedVm#staging_storage_account_id}.'''
        result = self._values.get("staging_storage_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_storage_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replicated_vm#target_storage_account_id SiteRecoveryReplicatedVm#target_storage_account_id}.'''
        result = self._values.get("target_storage_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicatedVmUnmanagedDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryReplicatedVmUnmanagedDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmUnmanagedDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27d0f6f1d0b860acaba6582b819ffa6579772271a17e981eb0f6d13f677d1849)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SiteRecoveryReplicatedVmUnmanagedDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bf84113066fc819a90aab803264e8e82c48153d9ecba2f0bce3870c88acf5dd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SiteRecoveryReplicatedVmUnmanagedDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e7b293c58490cf871c2ca1881803119713e303ad9b93a8264692aea8485602)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a079ca9430c82446faca4fde2383b8b78bfd642b1e23eba40205859c8ac68152)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c18b8cee44cf8e54a7384c713afa3aa81625ce6b6d157766d77aa48361d7324a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmUnmanagedDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmUnmanagedDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmUnmanagedDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55428740f16fca962a82ee98223b80bd3273759e2a6bd11dbe777378e2ccd5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SiteRecoveryReplicatedVmUnmanagedDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicatedVm.SiteRecoveryReplicatedVmUnmanagedDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b60bdf57baaa2260486c9046aecb6b4539daf97a5562ec85f38dc0c4a4a699a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDiskUri")
    def reset_disk_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskUri", []))

    @jsii.member(jsii_name="resetStagingStorageAccountId")
    def reset_staging_storage_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStagingStorageAccountId", []))

    @jsii.member(jsii_name="resetTargetStorageAccountId")
    def reset_target_storage_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetStorageAccountId", []))

    @builtins.property
    @jsii.member(jsii_name="diskUriInput")
    def disk_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskUriInput"))

    @builtins.property
    @jsii.member(jsii_name="stagingStorageAccountIdInput")
    def staging_storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stagingStorageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetStorageAccountIdInput")
    def target_storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetStorageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="diskUri")
    def disk_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskUri"))

    @disk_uri.setter
    def disk_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a565e5e3cf03044dc32d96adcffee5a5fc10199f70c641e2a484f550df623ae9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stagingStorageAccountId")
    def staging_storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stagingStorageAccountId"))

    @staging_storage_account_id.setter
    def staging_storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c2461d853001dadc3ba7a87166ec471b3f480a85f6a43e5915a29d57187941c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stagingStorageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetStorageAccountId")
    def target_storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetStorageAccountId"))

    @target_storage_account_id.setter
    def target_storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc2d1dbbf3480d56f8401e347d037f325e66cd4a343c3db2ab2c9556ed125de1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetStorageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmUnmanagedDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmUnmanagedDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmUnmanagedDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7c4e8e7a4ab5bf6502281d5953b29cf8ce26e7f5075ccb5a0bfcd6cfc46f4cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SiteRecoveryReplicatedVm",
    "SiteRecoveryReplicatedVmConfig",
    "SiteRecoveryReplicatedVmManagedDisk",
    "SiteRecoveryReplicatedVmManagedDiskList",
    "SiteRecoveryReplicatedVmManagedDiskOutputReference",
    "SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption",
    "SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey",
    "SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKeyList",
    "SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKeyOutputReference",
    "SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey",
    "SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKeyList",
    "SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKeyOutputReference",
    "SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionList",
    "SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionOutputReference",
    "SiteRecoveryReplicatedVmNetworkInterface",
    "SiteRecoveryReplicatedVmNetworkInterfaceList",
    "SiteRecoveryReplicatedVmNetworkInterfaceOutputReference",
    "SiteRecoveryReplicatedVmTimeouts",
    "SiteRecoveryReplicatedVmTimeoutsOutputReference",
    "SiteRecoveryReplicatedVmUnmanagedDisk",
    "SiteRecoveryReplicatedVmUnmanagedDiskList",
    "SiteRecoveryReplicatedVmUnmanagedDiskOutputReference",
]

publication.publish()

def _typecheckingstub__b8efed12cf94e269cd8c870a559284db5c0d8f297dcef209d76f9f9532c8548b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    recovery_replication_policy_id: builtins.str,
    recovery_vault_name: builtins.str,
    resource_group_name: builtins.str,
    source_recovery_fabric_name: builtins.str,
    source_recovery_protection_container_name: builtins.str,
    source_vm_id: builtins.str,
    target_recovery_fabric_id: builtins.str,
    target_recovery_protection_container_id: builtins.str,
    target_resource_group_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    managed_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicatedVmManagedDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    multi_vm_group_name: typing.Optional[builtins.str] = None,
    network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicatedVmNetworkInterface, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_availability_set_id: typing.Optional[builtins.str] = None,
    target_boot_diagnostic_storage_account_id: typing.Optional[builtins.str] = None,
    target_capacity_reservation_group_id: typing.Optional[builtins.str] = None,
    target_edge_zone: typing.Optional[builtins.str] = None,
    target_network_id: typing.Optional[builtins.str] = None,
    target_proximity_placement_group_id: typing.Optional[builtins.str] = None,
    target_virtual_machine_scale_set_id: typing.Optional[builtins.str] = None,
    target_virtual_machine_size: typing.Optional[builtins.str] = None,
    target_zone: typing.Optional[builtins.str] = None,
    test_network_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SiteRecoveryReplicatedVmTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    unmanaged_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicatedVmUnmanagedDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__ca8f2075100bb85fe1b0484c86ac4ed963e8e72305d1301769aef3d273eac818(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53fb6859d5965f11fc25461ab53fd2872f013371524184f3c92fe97f5a8c31a8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicatedVmManagedDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d5e274e976bf2004ebed07e5fca3e8a4197df6a92dd54749806b808ea240378(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicatedVmNetworkInterface, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2601348383b122b2056459338c0ecade99e20cda398849a7b776905ceec4e6b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicatedVmUnmanagedDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ce38d4938b6f71b54a2fe56e63cb5ddcda05de802e8e2f12d655568ed6edd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0bcfb839302e71e46d87f6c79e7d17263489513b9c65c8fca8646bfb1d3915(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b8ef2ce19656b125fe0e5cc1f8a0403b033b6ca1a2b914dbd94f2d983ad918f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d893a1ec226d4e48e03b6074e035bf6dfe2c30cc69415ccdf284ad0644667e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8db6b4db8bb6ee0fa79a08e8d64f5c87049d4195edd06ba7cc49c4efe85c8f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624fb5d8d4f0c1b5e843b58aeea10d16dbae897e1e9e921655b17667590aca7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1160c9e69f91529aeab7f343e748969025e5e4c741031400ab742939db0281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e908b03c6e65b7e6be2387ae0db2d15fa09b6a4e6dd6f3ab6f5f21faf514cc12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767e5544544955b09b6d9dc4595f3915e6ad22f1416786481f407ffea6d208aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38412c3f6c7f981f892c0710a30024f8d947d0c340b70c71d0934fccb55631e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0198ad6155715194fff5c2943702dfd5ec01b3b64b732e5fbf175873a14b7fb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ffffa3061c6393b19e15c7f4ecde4869d68080827eb6bcc62da10031409e8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a9a78cc81cc4d875c617f143942564ecbece3dce00f38af6ed2aea9741fc27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ec118488ce4ee3fc7384332d2788698b089ef68cbc5fe8472e10abd9d44cd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0bc801d6fa9130ccdf7184b2797003657b38683d52d06bfe10f84378a7cd06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e2dcd012dba7b5f92627a43e5ec9a387385bb365b9212a3850433bef527af6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61fdebd7e414c43f8e9f98fce12253eef69a112fe5f77f5ef5b2cded609b2354(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a477da8f5a72d9ac7be75203e24dc4a2ec8b10f863c1586ba5dbf8887272083b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b82a5384aead2e505629d242c0e1f6c3e58076dbd645ea9e4b0955243e1a2a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d15674b7348ba5be89adf30eed74b6330bd0efc079874a8d3055f481fb2366d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1b025f1db286ce0f46ec229857ce77977ee2a525fdcacbda5f480841bc8f7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3715aff2f2a2f14c98458252660599f7532e12c482d610cc0ddc50ab0d5f9f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c052d80b27126cce1524b21d47ea01a7544154071fc321787e4a923fcec4a2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    recovery_replication_policy_id: builtins.str,
    recovery_vault_name: builtins.str,
    resource_group_name: builtins.str,
    source_recovery_fabric_name: builtins.str,
    source_recovery_protection_container_name: builtins.str,
    source_vm_id: builtins.str,
    target_recovery_fabric_id: builtins.str,
    target_recovery_protection_container_id: builtins.str,
    target_resource_group_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    managed_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicatedVmManagedDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    multi_vm_group_name: typing.Optional[builtins.str] = None,
    network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicatedVmNetworkInterface, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_availability_set_id: typing.Optional[builtins.str] = None,
    target_boot_diagnostic_storage_account_id: typing.Optional[builtins.str] = None,
    target_capacity_reservation_group_id: typing.Optional[builtins.str] = None,
    target_edge_zone: typing.Optional[builtins.str] = None,
    target_network_id: typing.Optional[builtins.str] = None,
    target_proximity_placement_group_id: typing.Optional[builtins.str] = None,
    target_virtual_machine_scale_set_id: typing.Optional[builtins.str] = None,
    target_virtual_machine_size: typing.Optional[builtins.str] = None,
    target_zone: typing.Optional[builtins.str] = None,
    test_network_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SiteRecoveryReplicatedVmTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    unmanaged_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicatedVmUnmanagedDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51cea3acd5ebf07391c70753005724165db986668fb03eb6abdba4be643745a2(
    *,
    disk_id: typing.Optional[builtins.str] = None,
    staging_storage_account_id: typing.Optional[builtins.str] = None,
    target_disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_disk_encryption_set_id: typing.Optional[builtins.str] = None,
    target_disk_type: typing.Optional[builtins.str] = None,
    target_replica_disk_type: typing.Optional[builtins.str] = None,
    target_resource_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f913b129d292cdea1d51dc84b840262da8ee1ad9bddbce668be90efc592208(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e642bf61288eabb80042ed0501f94a55b0a790bb9a08bf8b881151181d8873(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362117f511ce1b2288399579fefee3e7e823c3b488229edf5c16d407a809f25f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6247b365933b9a18d5136d450a968a65106ca0e073c7d5884dccb5be72e84a05(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__438537280b6b6fba4c9854f86ff4f63d8a2f6fac55b0fca06ec3832bfd8bb37b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25e83457815efc2283f9a4365eeb0f223e5138431cbeefeeac4088d87f57905(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ec60f51679593d84c6db0f621ad69085634f835284cb58e729805eb56f844c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5160e09c3ec35589fa1ebd4f4fa1d4cd4cbe6ba53244b68262b819cbc06f8fc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06af984aeada6727eee114f0a600dc7622e5d33d2c9865020ff69e4102133710(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0df637f1bda8eefe3784a7786d901250368a9e6fbfce05b1ebf2c135943ca0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d2bda658ca94f026e845bf78a91b643e0dc7c11823486a4e59c2df4fc50313(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45734d4030ec4c90956e93cb3148d7bc900782070c1e1e47645ab5ab3465727(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c016167ddcef0e6be67413821a2ace37c102f3cb48de21498eb0b7ddcec0c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b5d250b8fb5e0f32fea37106da095e726fda398a0069de0414a09787f0d6b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0bbebbb447b790167ec261ba6061f5ab05728dbcaabac19aff2603fa8f99d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmManagedDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9181fa25a2eee7f11431ff3d14d05b190589a5bb1e717b1f963c7529b2bb0f(
    *,
    disk_encryption_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key_encryption_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139490f4a2b73d6258221abd4efd193a28a572da4be77e190eb8509d64f57a92(
    *,
    secret_url: typing.Optional[builtins.str] = None,
    vault_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4643f7d0f16d62543709a9fb34703f5ef6f87336618090e7777571c6a3cd5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa8eaf19e5823c1d258f09a726bb9c4b885e7197e5fd268d85a292d3419bc08(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7840d9ff803a6993bfdda68891bf2806c65d4ab211c01cb9a0998133352f169c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc698e9b1bc5fdb7a6bb264e56d07dfc80032bbc6e59507b1545df60522630f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67380da37ca1dd07dddc96578f1cfc2a4f51b6831db1d18b94d0b503e3fd6602(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d09994f1762e392a928bef3196b422610f10c730cb4b7368452d7dab50f9c4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6f40a42a2bd6369b36e0d315b708add1b748d8031752ee21d740f824b6fc55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ef7752f6e0845e0f5a899f32a68accce70d45a037e1fb83a71ac63683f8a71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af188e89cf4f961450244362eb68b3350c9b5c49b996373598dc15df4af6ed3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40d6a24bc6373709cd3c3b00b1bd82d6fbe06ec741e55e85218fc0ed59d2099(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dfef0fa9fd86f83edaad7ed146564911b8278ee2ea3f19bcfb7f4033f68adcd(
    *,
    key_url: typing.Optional[builtins.str] = None,
    vault_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150280b33fd729de7cf9d2cc126446f3415635d57c30cfacf7c5783af51f32ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6006991ae03ac5d79484fcb829d97cf1126bb319233b3764dd92d0b2ca15347a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6f2eb0d4a714757e43dc5a8c5581ddf1c1ed95e335e0492a64207a1f5fa82c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb35927623f117ccc1eaaed45040f85a59fc68aded94ed8c13aab144aa2c656(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d595397095388f34e679ac97c11149fe781d8aaeb053ed6c45af0819371a82(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aebb11694de52420f18baae5f6b115c41e4549a2716331cadd6af1eaa847d9fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82951bef34186aec115df37856c71355c3eab65ac3e0e09337671dce82c4194(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d981751f97d79c76026ba6ab6509c9448966bf8efbaefe360fe03d806e22ddec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d3c77871e2020d83d169892085313c36e675512c8356f2a7cb974dd5f1a812a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5917da5ff21dc1928fe870f5fa858b30291e2dee4229615c2cd184015e21bc8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e5c11dd8fdbe10fe251d316d329afa8d1147bc41231178237b342d23c918fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3badd5a0dae5c6f446a45ed7f09a94ca540c47552b90fd307b93ca6f30c36e4b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2f4b303baf7960f3308d6f94b2422542ea11063a0819401d2645da155f8ba3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__233dbdf1a0bba5b3a3b5a98f203028c6aca5b0147e4fe32475c7793f21943fa5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04f566bd7a45cebaeba57d6505e0c5491abd7e51028652a70ab9f2cf07cd92f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__018dbd0f66121433dc8b792c8daf67820640d96b3dde7d0d772344a2a4c683db(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64464825d46e9f727bfdaf66ca2685be1049afddee9d270d82b3235b5858396b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3abc09d9dc18d7eb468f29cb2d670a40881ccf163dea973f47a7fdf7300544(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionDiskEncryptionKey, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6791f339f83c93692d4740b87e7f7a56f8a7b8714a303ae9881a26d0ca9e34(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryptionKeyEncryptionKey, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626c34ad7e8facba662253ba2d6842e83a17ffffdbceb15454404a9dd0e70321(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmManagedDiskTargetDiskEncryption]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae06ab7804ee879779d6084bf6a07ad63a1afe60537790e28905e03e9938a84d(
    *,
    failover_test_public_ip_address_id: typing.Optional[builtins.str] = None,
    failover_test_static_ip: typing.Optional[builtins.str] = None,
    failover_test_subnet_name: typing.Optional[builtins.str] = None,
    recovery_load_balancer_backend_address_pool_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    recovery_public_ip_address_id: typing.Optional[builtins.str] = None,
    source_network_interface_id: typing.Optional[builtins.str] = None,
    target_static_ip: typing.Optional[builtins.str] = None,
    target_subnet_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dbfe4353bdea44bb14b14e7304641a1aa1097066f6486208b2e8e1a78e4ab15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0151a9e4443e068f48f6ea6e64f71b5abe107e03496822f593e6fe4f3030ea40(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95a9ed6393e4e99ab97a0329cfbc9956a1a55062dea779f0b63359a6151de6a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e6ea04b0e812cfb66e6d8dfc50d30962377c6185ad6fe984f865ead3ab47da0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d0774567876036ad901fb1ffc164d57bc8623895e06df510dcbd7cbf45d0082(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0adf21cb6996f7cef0b537e015e7a4ebc3fb387c0ced91f93b7245c3ab3ea018(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmNetworkInterface]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e82f126e9639e73c7b7e2ef035bf5481f810529b8f1a76153998ab71dbdb6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70aaf87fe7ee281e1a7e074ec634c0f6c4ea0043997f41647c64c427084400a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a092216c68a301b5d3499e00119b09c5093727258f5122d34a809a19eb4a4796(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5c1a67507b50b84dda378d7dca440fa9b89297dc80c8c13e2866f36605ef54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01ff0d023567f169558f29e85ecea48606e0ca5a445a0d8899bf72b096aade6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa1625779d3b7e9c471782048430ea710ce1d7ed69695c4c4752bb37114c669(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76822ae431aa93f711cfdc52a997a57a895036be39c53b87cb0584adf041c26a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01eaa931312e5d3bdb7a4972aa841469c94d46a2a7a6f8ebc3a0e94370f07d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19985c61448aa51f423082137e7940e1589994fbfe54a16725355cd0a178806(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb47f7fad336b48f22fae272183253fc3094218888993d70de4301c80bc2d463(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmNetworkInterface]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f36a469156cae8e0c220ae212ded7668cc519480e5ca7278ff8284885e9362(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aefa5cf134b2bb29f7c9be7f77b1e406f3b2040b89179765fd1b4af24e155c52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18dd199d48828fd2769498c1c8d370197537fc3f1df4aa4f31731f8ab2736b96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd006ce5a89ab5715febbe09d506d9a3dabf5226c21b8ec8345a25d3d7510fda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881e68af098f980c027c7ac4e42d038c0ed61fec5499b05d016abce0566d32c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f162e7ca448412936d90ff498197558322c5084b0b0602f926765d5f0698ae2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a8a65132370293b29fe363eea14145d1c091474376557069db007bf443d35e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7912d71802c44bafc15b04d54875737302051223e944b07affdd3529f1d56428(
    *,
    disk_uri: typing.Optional[builtins.str] = None,
    staging_storage_account_id: typing.Optional[builtins.str] = None,
    target_storage_account_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d0f6f1d0b860acaba6582b819ffa6579772271a17e981eb0f6d13f677d1849(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bf84113066fc819a90aab803264e8e82c48153d9ecba2f0bce3870c88acf5dd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e7b293c58490cf871c2ca1881803119713e303ad9b93a8264692aea8485602(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a079ca9430c82446faca4fde2383b8b78bfd642b1e23eba40205859c8ac68152(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18b8cee44cf8e54a7384c713afa3aa81625ce6b6d157766d77aa48361d7324a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55428740f16fca962a82ee98223b80bd3273759e2a6bd11dbe777378e2ccd5c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicatedVmUnmanagedDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b60bdf57baaa2260486c9046aecb6b4539daf97a5562ec85f38dc0c4a4a699a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a565e5e3cf03044dc32d96adcffee5a5fc10199f70c641e2a484f550df623ae9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c2461d853001dadc3ba7a87166ec471b3f480a85f6a43e5915a29d57187941c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2d1dbbf3480d56f8401e347d037f325e66cd4a343c3db2ab2c9556ed125de1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7c4e8e7a4ab5bf6502281d5953b29cf8ce26e7f5075ccb5a0bfcd6cfc46f4cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicatedVmUnmanagedDisk]],
) -> None:
    """Type checking stubs"""
    pass
