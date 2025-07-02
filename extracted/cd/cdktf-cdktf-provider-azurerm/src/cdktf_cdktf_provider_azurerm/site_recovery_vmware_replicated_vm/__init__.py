r'''
# `azurerm_site_recovery_vmware_replicated_vm`

Refer to the Terraform Registry for docs: [`azurerm_site_recovery_vmware_replicated_vm`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm).
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


class SiteRecoveryVmwareReplicatedVm(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryVmwareReplicatedVm.SiteRecoveryVmwareReplicatedVm",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm azurerm_site_recovery_vmware_replicated_vm}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        appliance_name: builtins.str,
        name: builtins.str,
        physical_server_credential_name: builtins.str,
        recovery_replication_policy_id: builtins.str,
        recovery_vault_id: builtins.str,
        source_vm_name: builtins.str,
        target_resource_group_id: builtins.str,
        target_vm_name: builtins.str,
        default_log_storage_account_id: typing.Optional[builtins.str] = None,
        default_recovery_disk_type: typing.Optional[builtins.str] = None,
        default_target_disk_encryption_set_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        license_type: typing.Optional[builtins.str] = None,
        managed_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryVmwareReplicatedVmManagedDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        multi_vm_group_name: typing.Optional[builtins.str] = None,
        network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryVmwareReplicatedVmNetworkInterface", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_availability_set_id: typing.Optional[builtins.str] = None,
        target_boot_diagnostics_storage_account_id: typing.Optional[builtins.str] = None,
        target_network_id: typing.Optional[builtins.str] = None,
        target_proximity_placement_group_id: typing.Optional[builtins.str] = None,
        target_vm_size: typing.Optional[builtins.str] = None,
        target_zone: typing.Optional[builtins.str] = None,
        test_network_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SiteRecoveryVmwareReplicatedVmTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm azurerm_site_recovery_vmware_replicated_vm} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param appliance_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#appliance_name SiteRecoveryVmwareReplicatedVm#appliance_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#name SiteRecoveryVmwareReplicatedVm#name}.
        :param physical_server_credential_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#physical_server_credential_name SiteRecoveryVmwareReplicatedVm#physical_server_credential_name}.
        :param recovery_replication_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#recovery_replication_policy_id SiteRecoveryVmwareReplicatedVm#recovery_replication_policy_id}.
        :param recovery_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#recovery_vault_id SiteRecoveryVmwareReplicatedVm#recovery_vault_id}.
        :param source_vm_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#source_vm_name SiteRecoveryVmwareReplicatedVm#source_vm_name}.
        :param target_resource_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_resource_group_id SiteRecoveryVmwareReplicatedVm#target_resource_group_id}.
        :param target_vm_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_vm_name SiteRecoveryVmwareReplicatedVm#target_vm_name}.
        :param default_log_storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#default_log_storage_account_id SiteRecoveryVmwareReplicatedVm#default_log_storage_account_id}.
        :param default_recovery_disk_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#default_recovery_disk_type SiteRecoveryVmwareReplicatedVm#default_recovery_disk_type}.
        :param default_target_disk_encryption_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#default_target_disk_encryption_set_id SiteRecoveryVmwareReplicatedVm#default_target_disk_encryption_set_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#id SiteRecoveryVmwareReplicatedVm#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param license_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#license_type SiteRecoveryVmwareReplicatedVm#license_type}.
        :param managed_disk: managed_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#managed_disk SiteRecoveryVmwareReplicatedVm#managed_disk}
        :param multi_vm_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#multi_vm_group_name SiteRecoveryVmwareReplicatedVm#multi_vm_group_name}.
        :param network_interface: network_interface block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#network_interface SiteRecoveryVmwareReplicatedVm#network_interface}
        :param target_availability_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_availability_set_id SiteRecoveryVmwareReplicatedVm#target_availability_set_id}.
        :param target_boot_diagnostics_storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_boot_diagnostics_storage_account_id SiteRecoveryVmwareReplicatedVm#target_boot_diagnostics_storage_account_id}.
        :param target_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_network_id SiteRecoveryVmwareReplicatedVm#target_network_id}.
        :param target_proximity_placement_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_proximity_placement_group_id SiteRecoveryVmwareReplicatedVm#target_proximity_placement_group_id}.
        :param target_vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_vm_size SiteRecoveryVmwareReplicatedVm#target_vm_size}.
        :param target_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_zone SiteRecoveryVmwareReplicatedVm#target_zone}.
        :param test_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#test_network_id SiteRecoveryVmwareReplicatedVm#test_network_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#timeouts SiteRecoveryVmwareReplicatedVm#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a6fca263f17433b17ec53b43b872d9019a303559c28001274f5b1a766a59aa8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SiteRecoveryVmwareReplicatedVmConfig(
            appliance_name=appliance_name,
            name=name,
            physical_server_credential_name=physical_server_credential_name,
            recovery_replication_policy_id=recovery_replication_policy_id,
            recovery_vault_id=recovery_vault_id,
            source_vm_name=source_vm_name,
            target_resource_group_id=target_resource_group_id,
            target_vm_name=target_vm_name,
            default_log_storage_account_id=default_log_storage_account_id,
            default_recovery_disk_type=default_recovery_disk_type,
            default_target_disk_encryption_set_id=default_target_disk_encryption_set_id,
            id=id,
            license_type=license_type,
            managed_disk=managed_disk,
            multi_vm_group_name=multi_vm_group_name,
            network_interface=network_interface,
            target_availability_set_id=target_availability_set_id,
            target_boot_diagnostics_storage_account_id=target_boot_diagnostics_storage_account_id,
            target_network_id=target_network_id,
            target_proximity_placement_group_id=target_proximity_placement_group_id,
            target_vm_size=target_vm_size,
            target_zone=target_zone,
            test_network_id=test_network_id,
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
        '''Generates CDKTF code for importing a SiteRecoveryVmwareReplicatedVm resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SiteRecoveryVmwareReplicatedVm to import.
        :param import_from_id: The id of the existing SiteRecoveryVmwareReplicatedVm that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SiteRecoveryVmwareReplicatedVm to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c54888e33e7cbff8e3df7e7184939228ea325631f35e467d9c0fc64ab243957f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putManagedDisk")
    def put_managed_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryVmwareReplicatedVmManagedDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f242e8cbaac81f8d145e5bb3eceafdc16f61f994b8fac45c9fcc951984864a7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putManagedDisk", [value]))

    @jsii.member(jsii_name="putNetworkInterface")
    def put_network_interface(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryVmwareReplicatedVmNetworkInterface", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41f55fa5486669545bb925b997a725cbbcddeaf7dc73798b7bc51dda228f839f)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#create SiteRecoveryVmwareReplicatedVm#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#delete SiteRecoveryVmwareReplicatedVm#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#read SiteRecoveryVmwareReplicatedVm#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#update SiteRecoveryVmwareReplicatedVm#update}.
        '''
        value = SiteRecoveryVmwareReplicatedVmTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDefaultLogStorageAccountId")
    def reset_default_log_storage_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultLogStorageAccountId", []))

    @jsii.member(jsii_name="resetDefaultRecoveryDiskType")
    def reset_default_recovery_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultRecoveryDiskType", []))

    @jsii.member(jsii_name="resetDefaultTargetDiskEncryptionSetId")
    def reset_default_target_disk_encryption_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTargetDiskEncryptionSetId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLicenseType")
    def reset_license_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicenseType", []))

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

    @jsii.member(jsii_name="resetTargetBootDiagnosticsStorageAccountId")
    def reset_target_boot_diagnostics_storage_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetBootDiagnosticsStorageAccountId", []))

    @jsii.member(jsii_name="resetTargetNetworkId")
    def reset_target_network_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetNetworkId", []))

    @jsii.member(jsii_name="resetTargetProximityPlacementGroupId")
    def reset_target_proximity_placement_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetProximityPlacementGroupId", []))

    @jsii.member(jsii_name="resetTargetVmSize")
    def reset_target_vm_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetVmSize", []))

    @jsii.member(jsii_name="resetTargetZone")
    def reset_target_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetZone", []))

    @jsii.member(jsii_name="resetTestNetworkId")
    def reset_test_network_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTestNetworkId", []))

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
    @jsii.member(jsii_name="managedDisk")
    def managed_disk(self) -> "SiteRecoveryVmwareReplicatedVmManagedDiskList":
        return typing.cast("SiteRecoveryVmwareReplicatedVmManagedDiskList", jsii.get(self, "managedDisk"))

    @builtins.property
    @jsii.member(jsii_name="networkInterface")
    def network_interface(self) -> "SiteRecoveryVmwareReplicatedVmNetworkInterfaceList":
        return typing.cast("SiteRecoveryVmwareReplicatedVmNetworkInterfaceList", jsii.get(self, "networkInterface"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SiteRecoveryVmwareReplicatedVmTimeoutsOutputReference":
        return typing.cast("SiteRecoveryVmwareReplicatedVmTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="applianceNameInput")
    def appliance_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applianceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultLogStorageAccountIdInput")
    def default_log_storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultLogStorageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRecoveryDiskTypeInput")
    def default_recovery_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultRecoveryDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTargetDiskEncryptionSetIdInput")
    def default_target_disk_encryption_set_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTargetDiskEncryptionSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseTypeInput")
    def license_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="managedDiskInput")
    def managed_disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryVmwareReplicatedVmManagedDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryVmwareReplicatedVmManagedDisk"]]], jsii.get(self, "managedDiskInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryVmwareReplicatedVmNetworkInterface"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryVmwareReplicatedVmNetworkInterface"]]], jsii.get(self, "networkInterfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="physicalServerCredentialNameInput")
    def physical_server_credential_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "physicalServerCredentialNameInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryReplicationPolicyIdInput")
    def recovery_replication_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoveryReplicationPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryVaultIdInput")
    def recovery_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoveryVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceVmNameInput")
    def source_vm_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceVmNameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetAvailabilitySetIdInput")
    def target_availability_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetAvailabilitySetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetBootDiagnosticsStorageAccountIdInput")
    def target_boot_diagnostics_storage_account_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetBootDiagnosticsStorageAccountIdInput"))

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
    @jsii.member(jsii_name="targetResourceGroupIdInput")
    def target_resource_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetResourceGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetVmNameInput")
    def target_vm_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetVmNameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetVmSizeInput")
    def target_vm_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetVmSizeInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SiteRecoveryVmwareReplicatedVmTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SiteRecoveryVmwareReplicatedVmTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="applianceName")
    def appliance_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applianceName"))

    @appliance_name.setter
    def appliance_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0066c2de30f3eaa612c3d2fefd1ae414a2d38f5972897a7518963757c717870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applianceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultLogStorageAccountId")
    def default_log_storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultLogStorageAccountId"))

    @default_log_storage_account_id.setter
    def default_log_storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcde213adcd4b16d701747a47e9f51ac622df0d9a3c0817dd7ae248266936b35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLogStorageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRecoveryDiskType")
    def default_recovery_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultRecoveryDiskType"))

    @default_recovery_disk_type.setter
    def default_recovery_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc66f51c321de565df033d7c7862c42c48c774c0fc711cd1f2e1fcce846a4df1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecoveryDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTargetDiskEncryptionSetId")
    def default_target_disk_encryption_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultTargetDiskEncryptionSetId"))

    @default_target_disk_encryption_set_id.setter
    def default_target_disk_encryption_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10712789bb83b0d16cae63b140e72ff7b87e77a9aae0280b2a0cfe502562f43e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTargetDiskEncryptionSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c8e435a8705ed738ab29166bfde616a3b1aa0cef83398c72d632408219b37e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="licenseType")
    def license_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseType"))

    @license_type.setter
    def license_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d07560aec34fe365f9d88976357b363a790c869ede42b7a21972b713f87406b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiVmGroupName")
    def multi_vm_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "multiVmGroupName"))

    @multi_vm_group_name.setter
    def multi_vm_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d08e898911265e3877643763d8dbaa4dfc47dab06f4cac6117673dcfacb619c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiVmGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c09321f3235c4a3bbf3c5aba3fcbcfe00c2078b836474715bb99270c15d69b4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="physicalServerCredentialName")
    def physical_server_credential_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "physicalServerCredentialName"))

    @physical_server_credential_name.setter
    def physical_server_credential_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c92346336b442d5b1d63b1162cc45570bc8908f49220c76f4e0857e4b2c4ad3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "physicalServerCredentialName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryReplicationPolicyId")
    def recovery_replication_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recoveryReplicationPolicyId"))

    @recovery_replication_policy_id.setter
    def recovery_replication_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f98f0f0e0a81ca491609398cc5b2d83d291c150fa32dfcc990b7d4135045dfe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryReplicationPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryVaultId")
    def recovery_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recoveryVaultId"))

    @recovery_vault_id.setter
    def recovery_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b27b6ae8b225bb21a2181e5a1fec5ce623fc35f7fe0e67f7db66d49c923901eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceVmName")
    def source_vm_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceVmName"))

    @source_vm_name.setter
    def source_vm_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c089fc6a45814abcc9e2ff2f5420d067620e3029fc33a238407e8dd901b49f9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceVmName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetAvailabilitySetId")
    def target_availability_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetAvailabilitySetId"))

    @target_availability_set_id.setter
    def target_availability_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79ed7b6420b020727f70f23dfee133e574cc2b8f11dbec7a87050894938774e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetAvailabilitySetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetBootDiagnosticsStorageAccountId")
    def target_boot_diagnostics_storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetBootDiagnosticsStorageAccountId"))

    @target_boot_diagnostics_storage_account_id.setter
    def target_boot_diagnostics_storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd8d9c76ec3cef036b7362be72a141392e57bd4239e4c5b66c7f522ab738305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetBootDiagnosticsStorageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetNetworkId")
    def target_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetNetworkId"))

    @target_network_id.setter
    def target_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bf78782cdf244963a7bf2dbd28d041eea06f3bd7ffe19ff689c712c742c80b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetProximityPlacementGroupId")
    def target_proximity_placement_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetProximityPlacementGroupId"))

    @target_proximity_placement_group_id.setter
    def target_proximity_placement_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b532059fd0b973668b4a8144e0a48e6fdc591486ce80acd22584886e4568a4cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetProximityPlacementGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetResourceGroupId")
    def target_resource_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetResourceGroupId"))

    @target_resource_group_id.setter
    def target_resource_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3209acfaf3ee01a5f18b4ff16f51986a6e2754567b9e2cef8b694fd1a3e3387d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetResourceGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetVmName")
    def target_vm_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetVmName"))

    @target_vm_name.setter
    def target_vm_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee3d50754b09d2a2d0731aca4db868357b07abe820d700b8462d02e7a535f53f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetVmName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetVmSize")
    def target_vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetVmSize"))

    @target_vm_size.setter
    def target_vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c9fb2efd09401f64b773d9ef6b464083559f6bdb96d140fbdf23246e77f189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetVmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetZone")
    def target_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetZone"))

    @target_zone.setter
    def target_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d66bb39b86a005b0b632d3141693772b4c7cf4485330017d3adc3334cca7454e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="testNetworkId")
    def test_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "testNetworkId"))

    @test_network_id.setter
    def test_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8acef09a218463aa105ef6b3fa97b0c4f742297404dd38e979173113c922c43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "testNetworkId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryVmwareReplicatedVm.SiteRecoveryVmwareReplicatedVmConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "appliance_name": "applianceName",
        "name": "name",
        "physical_server_credential_name": "physicalServerCredentialName",
        "recovery_replication_policy_id": "recoveryReplicationPolicyId",
        "recovery_vault_id": "recoveryVaultId",
        "source_vm_name": "sourceVmName",
        "target_resource_group_id": "targetResourceGroupId",
        "target_vm_name": "targetVmName",
        "default_log_storage_account_id": "defaultLogStorageAccountId",
        "default_recovery_disk_type": "defaultRecoveryDiskType",
        "default_target_disk_encryption_set_id": "defaultTargetDiskEncryptionSetId",
        "id": "id",
        "license_type": "licenseType",
        "managed_disk": "managedDisk",
        "multi_vm_group_name": "multiVmGroupName",
        "network_interface": "networkInterface",
        "target_availability_set_id": "targetAvailabilitySetId",
        "target_boot_diagnostics_storage_account_id": "targetBootDiagnosticsStorageAccountId",
        "target_network_id": "targetNetworkId",
        "target_proximity_placement_group_id": "targetProximityPlacementGroupId",
        "target_vm_size": "targetVmSize",
        "target_zone": "targetZone",
        "test_network_id": "testNetworkId",
        "timeouts": "timeouts",
    },
)
class SiteRecoveryVmwareReplicatedVmConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        appliance_name: builtins.str,
        name: builtins.str,
        physical_server_credential_name: builtins.str,
        recovery_replication_policy_id: builtins.str,
        recovery_vault_id: builtins.str,
        source_vm_name: builtins.str,
        target_resource_group_id: builtins.str,
        target_vm_name: builtins.str,
        default_log_storage_account_id: typing.Optional[builtins.str] = None,
        default_recovery_disk_type: typing.Optional[builtins.str] = None,
        default_target_disk_encryption_set_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        license_type: typing.Optional[builtins.str] = None,
        managed_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryVmwareReplicatedVmManagedDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        multi_vm_group_name: typing.Optional[builtins.str] = None,
        network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryVmwareReplicatedVmNetworkInterface", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_availability_set_id: typing.Optional[builtins.str] = None,
        target_boot_diagnostics_storage_account_id: typing.Optional[builtins.str] = None,
        target_network_id: typing.Optional[builtins.str] = None,
        target_proximity_placement_group_id: typing.Optional[builtins.str] = None,
        target_vm_size: typing.Optional[builtins.str] = None,
        target_zone: typing.Optional[builtins.str] = None,
        test_network_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SiteRecoveryVmwareReplicatedVmTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param appliance_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#appliance_name SiteRecoveryVmwareReplicatedVm#appliance_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#name SiteRecoveryVmwareReplicatedVm#name}.
        :param physical_server_credential_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#physical_server_credential_name SiteRecoveryVmwareReplicatedVm#physical_server_credential_name}.
        :param recovery_replication_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#recovery_replication_policy_id SiteRecoveryVmwareReplicatedVm#recovery_replication_policy_id}.
        :param recovery_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#recovery_vault_id SiteRecoveryVmwareReplicatedVm#recovery_vault_id}.
        :param source_vm_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#source_vm_name SiteRecoveryVmwareReplicatedVm#source_vm_name}.
        :param target_resource_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_resource_group_id SiteRecoveryVmwareReplicatedVm#target_resource_group_id}.
        :param target_vm_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_vm_name SiteRecoveryVmwareReplicatedVm#target_vm_name}.
        :param default_log_storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#default_log_storage_account_id SiteRecoveryVmwareReplicatedVm#default_log_storage_account_id}.
        :param default_recovery_disk_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#default_recovery_disk_type SiteRecoveryVmwareReplicatedVm#default_recovery_disk_type}.
        :param default_target_disk_encryption_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#default_target_disk_encryption_set_id SiteRecoveryVmwareReplicatedVm#default_target_disk_encryption_set_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#id SiteRecoveryVmwareReplicatedVm#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param license_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#license_type SiteRecoveryVmwareReplicatedVm#license_type}.
        :param managed_disk: managed_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#managed_disk SiteRecoveryVmwareReplicatedVm#managed_disk}
        :param multi_vm_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#multi_vm_group_name SiteRecoveryVmwareReplicatedVm#multi_vm_group_name}.
        :param network_interface: network_interface block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#network_interface SiteRecoveryVmwareReplicatedVm#network_interface}
        :param target_availability_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_availability_set_id SiteRecoveryVmwareReplicatedVm#target_availability_set_id}.
        :param target_boot_diagnostics_storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_boot_diagnostics_storage_account_id SiteRecoveryVmwareReplicatedVm#target_boot_diagnostics_storage_account_id}.
        :param target_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_network_id SiteRecoveryVmwareReplicatedVm#target_network_id}.
        :param target_proximity_placement_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_proximity_placement_group_id SiteRecoveryVmwareReplicatedVm#target_proximity_placement_group_id}.
        :param target_vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_vm_size SiteRecoveryVmwareReplicatedVm#target_vm_size}.
        :param target_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_zone SiteRecoveryVmwareReplicatedVm#target_zone}.
        :param test_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#test_network_id SiteRecoveryVmwareReplicatedVm#test_network_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#timeouts SiteRecoveryVmwareReplicatedVm#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = SiteRecoveryVmwareReplicatedVmTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5575b6560804a88585f0d6787f484ae1ea3e63e1719a82d35f38c08eb668aee3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument appliance_name", value=appliance_name, expected_type=type_hints["appliance_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument physical_server_credential_name", value=physical_server_credential_name, expected_type=type_hints["physical_server_credential_name"])
            check_type(argname="argument recovery_replication_policy_id", value=recovery_replication_policy_id, expected_type=type_hints["recovery_replication_policy_id"])
            check_type(argname="argument recovery_vault_id", value=recovery_vault_id, expected_type=type_hints["recovery_vault_id"])
            check_type(argname="argument source_vm_name", value=source_vm_name, expected_type=type_hints["source_vm_name"])
            check_type(argname="argument target_resource_group_id", value=target_resource_group_id, expected_type=type_hints["target_resource_group_id"])
            check_type(argname="argument target_vm_name", value=target_vm_name, expected_type=type_hints["target_vm_name"])
            check_type(argname="argument default_log_storage_account_id", value=default_log_storage_account_id, expected_type=type_hints["default_log_storage_account_id"])
            check_type(argname="argument default_recovery_disk_type", value=default_recovery_disk_type, expected_type=type_hints["default_recovery_disk_type"])
            check_type(argname="argument default_target_disk_encryption_set_id", value=default_target_disk_encryption_set_id, expected_type=type_hints["default_target_disk_encryption_set_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument license_type", value=license_type, expected_type=type_hints["license_type"])
            check_type(argname="argument managed_disk", value=managed_disk, expected_type=type_hints["managed_disk"])
            check_type(argname="argument multi_vm_group_name", value=multi_vm_group_name, expected_type=type_hints["multi_vm_group_name"])
            check_type(argname="argument network_interface", value=network_interface, expected_type=type_hints["network_interface"])
            check_type(argname="argument target_availability_set_id", value=target_availability_set_id, expected_type=type_hints["target_availability_set_id"])
            check_type(argname="argument target_boot_diagnostics_storage_account_id", value=target_boot_diagnostics_storage_account_id, expected_type=type_hints["target_boot_diagnostics_storage_account_id"])
            check_type(argname="argument target_network_id", value=target_network_id, expected_type=type_hints["target_network_id"])
            check_type(argname="argument target_proximity_placement_group_id", value=target_proximity_placement_group_id, expected_type=type_hints["target_proximity_placement_group_id"])
            check_type(argname="argument target_vm_size", value=target_vm_size, expected_type=type_hints["target_vm_size"])
            check_type(argname="argument target_zone", value=target_zone, expected_type=type_hints["target_zone"])
            check_type(argname="argument test_network_id", value=test_network_id, expected_type=type_hints["test_network_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "appliance_name": appliance_name,
            "name": name,
            "physical_server_credential_name": physical_server_credential_name,
            "recovery_replication_policy_id": recovery_replication_policy_id,
            "recovery_vault_id": recovery_vault_id,
            "source_vm_name": source_vm_name,
            "target_resource_group_id": target_resource_group_id,
            "target_vm_name": target_vm_name,
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
        if default_log_storage_account_id is not None:
            self._values["default_log_storage_account_id"] = default_log_storage_account_id
        if default_recovery_disk_type is not None:
            self._values["default_recovery_disk_type"] = default_recovery_disk_type
        if default_target_disk_encryption_set_id is not None:
            self._values["default_target_disk_encryption_set_id"] = default_target_disk_encryption_set_id
        if id is not None:
            self._values["id"] = id
        if license_type is not None:
            self._values["license_type"] = license_type
        if managed_disk is not None:
            self._values["managed_disk"] = managed_disk
        if multi_vm_group_name is not None:
            self._values["multi_vm_group_name"] = multi_vm_group_name
        if network_interface is not None:
            self._values["network_interface"] = network_interface
        if target_availability_set_id is not None:
            self._values["target_availability_set_id"] = target_availability_set_id
        if target_boot_diagnostics_storage_account_id is not None:
            self._values["target_boot_diagnostics_storage_account_id"] = target_boot_diagnostics_storage_account_id
        if target_network_id is not None:
            self._values["target_network_id"] = target_network_id
        if target_proximity_placement_group_id is not None:
            self._values["target_proximity_placement_group_id"] = target_proximity_placement_group_id
        if target_vm_size is not None:
            self._values["target_vm_size"] = target_vm_size
        if target_zone is not None:
            self._values["target_zone"] = target_zone
        if test_network_id is not None:
            self._values["test_network_id"] = test_network_id
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
    def appliance_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#appliance_name SiteRecoveryVmwareReplicatedVm#appliance_name}.'''
        result = self._values.get("appliance_name")
        assert result is not None, "Required property 'appliance_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#name SiteRecoveryVmwareReplicatedVm#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def physical_server_credential_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#physical_server_credential_name SiteRecoveryVmwareReplicatedVm#physical_server_credential_name}.'''
        result = self._values.get("physical_server_credential_name")
        assert result is not None, "Required property 'physical_server_credential_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def recovery_replication_policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#recovery_replication_policy_id SiteRecoveryVmwareReplicatedVm#recovery_replication_policy_id}.'''
        result = self._values.get("recovery_replication_policy_id")
        assert result is not None, "Required property 'recovery_replication_policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def recovery_vault_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#recovery_vault_id SiteRecoveryVmwareReplicatedVm#recovery_vault_id}.'''
        result = self._values.get("recovery_vault_id")
        assert result is not None, "Required property 'recovery_vault_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_vm_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#source_vm_name SiteRecoveryVmwareReplicatedVm#source_vm_name}.'''
        result = self._values.get("source_vm_name")
        assert result is not None, "Required property 'source_vm_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_resource_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_resource_group_id SiteRecoveryVmwareReplicatedVm#target_resource_group_id}.'''
        result = self._values.get("target_resource_group_id")
        assert result is not None, "Required property 'target_resource_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_vm_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_vm_name SiteRecoveryVmwareReplicatedVm#target_vm_name}.'''
        result = self._values.get("target_vm_name")
        assert result is not None, "Required property 'target_vm_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_log_storage_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#default_log_storage_account_id SiteRecoveryVmwareReplicatedVm#default_log_storage_account_id}.'''
        result = self._values.get("default_log_storage_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_recovery_disk_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#default_recovery_disk_type SiteRecoveryVmwareReplicatedVm#default_recovery_disk_type}.'''
        result = self._values.get("default_recovery_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_target_disk_encryption_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#default_target_disk_encryption_set_id SiteRecoveryVmwareReplicatedVm#default_target_disk_encryption_set_id}.'''
        result = self._values.get("default_target_disk_encryption_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#id SiteRecoveryVmwareReplicatedVm#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#license_type SiteRecoveryVmwareReplicatedVm#license_type}.'''
        result = self._values.get("license_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryVmwareReplicatedVmManagedDisk"]]]:
        '''managed_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#managed_disk SiteRecoveryVmwareReplicatedVm#managed_disk}
        '''
        result = self._values.get("managed_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryVmwareReplicatedVmManagedDisk"]]], result)

    @builtins.property
    def multi_vm_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#multi_vm_group_name SiteRecoveryVmwareReplicatedVm#multi_vm_group_name}.'''
        result = self._values.get("multi_vm_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_interface(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryVmwareReplicatedVmNetworkInterface"]]]:
        '''network_interface block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#network_interface SiteRecoveryVmwareReplicatedVm#network_interface}
        '''
        result = self._values.get("network_interface")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryVmwareReplicatedVmNetworkInterface"]]], result)

    @builtins.property
    def target_availability_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_availability_set_id SiteRecoveryVmwareReplicatedVm#target_availability_set_id}.'''
        result = self._values.get("target_availability_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_boot_diagnostics_storage_account_id(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_boot_diagnostics_storage_account_id SiteRecoveryVmwareReplicatedVm#target_boot_diagnostics_storage_account_id}.'''
        result = self._values.get("target_boot_diagnostics_storage_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_network_id SiteRecoveryVmwareReplicatedVm#target_network_id}.'''
        result = self._values.get("target_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_proximity_placement_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_proximity_placement_group_id SiteRecoveryVmwareReplicatedVm#target_proximity_placement_group_id}.'''
        result = self._values.get("target_proximity_placement_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_vm_size(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_vm_size SiteRecoveryVmwareReplicatedVm#target_vm_size}.'''
        result = self._values.get("target_vm_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_zone SiteRecoveryVmwareReplicatedVm#target_zone}.'''
        result = self._values.get("target_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def test_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#test_network_id SiteRecoveryVmwareReplicatedVm#test_network_id}.'''
        result = self._values.get("test_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SiteRecoveryVmwareReplicatedVmTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#timeouts SiteRecoveryVmwareReplicatedVm#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SiteRecoveryVmwareReplicatedVmTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryVmwareReplicatedVmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryVmwareReplicatedVm.SiteRecoveryVmwareReplicatedVmManagedDisk",
    jsii_struct_bases=[],
    name_mapping={
        "disk_id": "diskId",
        "target_disk_type": "targetDiskType",
        "log_storage_account_id": "logStorageAccountId",
        "target_disk_encryption_set_id": "targetDiskEncryptionSetId",
    },
)
class SiteRecoveryVmwareReplicatedVmManagedDisk:
    def __init__(
        self,
        *,
        disk_id: builtins.str,
        target_disk_type: builtins.str,
        log_storage_account_id: typing.Optional[builtins.str] = None,
        target_disk_encryption_set_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#disk_id SiteRecoveryVmwareReplicatedVm#disk_id}.
        :param target_disk_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_disk_type SiteRecoveryVmwareReplicatedVm#target_disk_type}.
        :param log_storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#log_storage_account_id SiteRecoveryVmwareReplicatedVm#log_storage_account_id}.
        :param target_disk_encryption_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_disk_encryption_set_id SiteRecoveryVmwareReplicatedVm#target_disk_encryption_set_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0abb477ea24c00aec21bae232c4fc298ef41114493946f9398293a7d403d0130)
            check_type(argname="argument disk_id", value=disk_id, expected_type=type_hints["disk_id"])
            check_type(argname="argument target_disk_type", value=target_disk_type, expected_type=type_hints["target_disk_type"])
            check_type(argname="argument log_storage_account_id", value=log_storage_account_id, expected_type=type_hints["log_storage_account_id"])
            check_type(argname="argument target_disk_encryption_set_id", value=target_disk_encryption_set_id, expected_type=type_hints["target_disk_encryption_set_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disk_id": disk_id,
            "target_disk_type": target_disk_type,
        }
        if log_storage_account_id is not None:
            self._values["log_storage_account_id"] = log_storage_account_id
        if target_disk_encryption_set_id is not None:
            self._values["target_disk_encryption_set_id"] = target_disk_encryption_set_id

    @builtins.property
    def disk_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#disk_id SiteRecoveryVmwareReplicatedVm#disk_id}.'''
        result = self._values.get("disk_id")
        assert result is not None, "Required property 'disk_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_disk_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_disk_type SiteRecoveryVmwareReplicatedVm#target_disk_type}.'''
        result = self._values.get("target_disk_type")
        assert result is not None, "Required property 'target_disk_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_storage_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#log_storage_account_id SiteRecoveryVmwareReplicatedVm#log_storage_account_id}.'''
        result = self._values.get("log_storage_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_disk_encryption_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_disk_encryption_set_id SiteRecoveryVmwareReplicatedVm#target_disk_encryption_set_id}.'''
        result = self._values.get("target_disk_encryption_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryVmwareReplicatedVmManagedDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryVmwareReplicatedVmManagedDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryVmwareReplicatedVm.SiteRecoveryVmwareReplicatedVmManagedDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d763c8bddddda19c39af933f90b35d9564138176a79206b798f032036a63a32e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SiteRecoveryVmwareReplicatedVmManagedDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8171968706b498ffe8d58df863af47dfebc80af7cdd029fc6631a4e52201f9f4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SiteRecoveryVmwareReplicatedVmManagedDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30ecce40321f844dde9487d738364316c306543acce99ff359e41d5a2667402b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a506cc2220eb30bfe6cda819e082b2e76bb3c161b8d5113d62df8d6d996ed25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__600a935f1a6b8927f5b94b0ad788d56c2ae291bbfd31e890cfc72e776bf655d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryVmwareReplicatedVmManagedDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryVmwareReplicatedVmManagedDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryVmwareReplicatedVmManagedDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d323a5c211e6c4541dcc32526af616e6548245ca377a0d15439c9843b5dce25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SiteRecoveryVmwareReplicatedVmManagedDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryVmwareReplicatedVm.SiteRecoveryVmwareReplicatedVmManagedDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d8d7d5a13235876142a990c2a1ad1cdb7e2e3e7de2c8bff2bfaa068ffe6e93c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLogStorageAccountId")
    def reset_log_storage_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStorageAccountId", []))

    @jsii.member(jsii_name="resetTargetDiskEncryptionSetId")
    def reset_target_disk_encryption_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetDiskEncryptionSetId", []))

    @builtins.property
    @jsii.member(jsii_name="diskIdInput")
    def disk_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logStorageAccountIdInput")
    def log_storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStorageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetDiskEncryptionSetIdInput")
    def target_disk_encryption_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetDiskEncryptionSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetDiskTypeInput")
    def target_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="diskId")
    def disk_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskId"))

    @disk_id.setter
    def disk_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9379159da6aa1aa2902b46caa0fe4e67dfdf42a90460825d255788f78939efc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logStorageAccountId")
    def log_storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStorageAccountId"))

    @log_storage_account_id.setter
    def log_storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c54cb3344627e72e90523cfe5483dbed6a9bc05a34b673688002eb60c9b2f274)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStorageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetDiskEncryptionSetId")
    def target_disk_encryption_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetDiskEncryptionSetId"))

    @target_disk_encryption_set_id.setter
    def target_disk_encryption_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__852ff2fe024bc1f61417a72ff9aab4c9c225eb50f9b6bbe28068bbcc9addbf0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetDiskEncryptionSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetDiskType")
    def target_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetDiskType"))

    @target_disk_type.setter
    def target_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0d6c0e86f32d386a9906cc5633b0ea6fdece3e0918a54de607837a56f9c746)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryVmwareReplicatedVmManagedDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryVmwareReplicatedVmManagedDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryVmwareReplicatedVmManagedDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab5fb357a12c620a574f3f08d6a7767b15ca8ff7f4c3e1ae793a916afd4c0775)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryVmwareReplicatedVm.SiteRecoveryVmwareReplicatedVmNetworkInterface",
    jsii_struct_bases=[],
    name_mapping={
        "is_primary": "isPrimary",
        "source_mac_address": "sourceMacAddress",
        "target_static_ip": "targetStaticIp",
        "target_subnet_name": "targetSubnetName",
        "test_subnet_name": "testSubnetName",
    },
)
class SiteRecoveryVmwareReplicatedVmNetworkInterface:
    def __init__(
        self,
        *,
        is_primary: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        source_mac_address: builtins.str,
        target_static_ip: typing.Optional[builtins.str] = None,
        target_subnet_name: typing.Optional[builtins.str] = None,
        test_subnet_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param is_primary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#is_primary SiteRecoveryVmwareReplicatedVm#is_primary}.
        :param source_mac_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#source_mac_address SiteRecoveryVmwareReplicatedVm#source_mac_address}.
        :param target_static_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_static_ip SiteRecoveryVmwareReplicatedVm#target_static_ip}.
        :param target_subnet_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_subnet_name SiteRecoveryVmwareReplicatedVm#target_subnet_name}.
        :param test_subnet_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#test_subnet_name SiteRecoveryVmwareReplicatedVm#test_subnet_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39533a99e086ffb339df7393a2df7f009086d26c31fa7e83d68099c51bc8a157)
            check_type(argname="argument is_primary", value=is_primary, expected_type=type_hints["is_primary"])
            check_type(argname="argument source_mac_address", value=source_mac_address, expected_type=type_hints["source_mac_address"])
            check_type(argname="argument target_static_ip", value=target_static_ip, expected_type=type_hints["target_static_ip"])
            check_type(argname="argument target_subnet_name", value=target_subnet_name, expected_type=type_hints["target_subnet_name"])
            check_type(argname="argument test_subnet_name", value=test_subnet_name, expected_type=type_hints["test_subnet_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "is_primary": is_primary,
            "source_mac_address": source_mac_address,
        }
        if target_static_ip is not None:
            self._values["target_static_ip"] = target_static_ip
        if target_subnet_name is not None:
            self._values["target_subnet_name"] = target_subnet_name
        if test_subnet_name is not None:
            self._values["test_subnet_name"] = test_subnet_name

    @builtins.property
    def is_primary(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#is_primary SiteRecoveryVmwareReplicatedVm#is_primary}.'''
        result = self._values.get("is_primary")
        assert result is not None, "Required property 'is_primary' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def source_mac_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#source_mac_address SiteRecoveryVmwareReplicatedVm#source_mac_address}.'''
        result = self._values.get("source_mac_address")
        assert result is not None, "Required property 'source_mac_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_static_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_static_ip SiteRecoveryVmwareReplicatedVm#target_static_ip}.'''
        result = self._values.get("target_static_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_subnet_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#target_subnet_name SiteRecoveryVmwareReplicatedVm#target_subnet_name}.'''
        result = self._values.get("target_subnet_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def test_subnet_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#test_subnet_name SiteRecoveryVmwareReplicatedVm#test_subnet_name}.'''
        result = self._values.get("test_subnet_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryVmwareReplicatedVmNetworkInterface(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryVmwareReplicatedVmNetworkInterfaceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryVmwareReplicatedVm.SiteRecoveryVmwareReplicatedVmNetworkInterfaceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a18fe4680db172ba1eb53e69f1f08032d58944546dc8ba6cf73e29c01208972)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SiteRecoveryVmwareReplicatedVmNetworkInterfaceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1eeebfc0beda8b4a28bdacc1b2fdbb64d82373ff9cef1d7f7375400c121a1cb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SiteRecoveryVmwareReplicatedVmNetworkInterfaceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edc18f50b5c3f4654543d0b6fe4d12accb164115e61597fe9d3e02755ccf891d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b15cb2c59d8c44722503424d2b661602e1ed90f292e41203a65faacc735044b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca8e15c4c3d029b72bc63c83d26aecc454f43e9a22ad1089723ec64406885300)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryVmwareReplicatedVmNetworkInterface]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryVmwareReplicatedVmNetworkInterface]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryVmwareReplicatedVmNetworkInterface]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1aec63ce7d6e435761b2170014614d089fcf15a2cd1341823b369e2af6e942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SiteRecoveryVmwareReplicatedVmNetworkInterfaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryVmwareReplicatedVm.SiteRecoveryVmwareReplicatedVmNetworkInterfaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27c30053f6386fae136f086595f53805ecc470589630b9c9ea25cc6a7d85f63f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetTargetStaticIp")
    def reset_target_static_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetStaticIp", []))

    @jsii.member(jsii_name="resetTargetSubnetName")
    def reset_target_subnet_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetSubnetName", []))

    @jsii.member(jsii_name="resetTestSubnetName")
    def reset_test_subnet_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTestSubnetName", []))

    @builtins.property
    @jsii.member(jsii_name="isPrimaryInput")
    def is_primary_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isPrimaryInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceMacAddressInput")
    def source_mac_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceMacAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="targetStaticIpInput")
    def target_static_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetStaticIpInput"))

    @builtins.property
    @jsii.member(jsii_name="targetSubnetNameInput")
    def target_subnet_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetSubnetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="testSubnetNameInput")
    def test_subnet_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "testSubnetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="isPrimary")
    def is_primary(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isPrimary"))

    @is_primary.setter
    def is_primary(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f58504de0223ebe70c9921b8c9e25d08e5e4d49870aa5c40c7ee672ef22da125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isPrimary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceMacAddress")
    def source_mac_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceMacAddress"))

    @source_mac_address.setter
    def source_mac_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f008b6b1376ab405e560e3fcd91b99f7058e2bf82d9cc440d71893e881ef33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceMacAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetStaticIp")
    def target_static_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetStaticIp"))

    @target_static_ip.setter
    def target_static_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3aa95ceecb293a3f279e824f11dfc5672d1eb061f302daa5354dba74c137f86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetStaticIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetSubnetName")
    def target_subnet_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetSubnetName"))

    @target_subnet_name.setter
    def target_subnet_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bfcde550afe13d7408e97dbf4e8b9936c2e06c521fe3da49b299a66eba6a5ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetSubnetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="testSubnetName")
    def test_subnet_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "testSubnetName"))

    @test_subnet_name.setter
    def test_subnet_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0a6ae4ceeafc4edc177764187523fcc0d26ec5d9386b4150cc14a3dd3605442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "testSubnetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryVmwareReplicatedVmNetworkInterface]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryVmwareReplicatedVmNetworkInterface]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryVmwareReplicatedVmNetworkInterface]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4940bd2412636bae3247260cfc56863c82a4aa76201c7c10f2766b9280b952)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryVmwareReplicatedVm.SiteRecoveryVmwareReplicatedVmTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SiteRecoveryVmwareReplicatedVmTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#create SiteRecoveryVmwareReplicatedVm#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#delete SiteRecoveryVmwareReplicatedVm#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#read SiteRecoveryVmwareReplicatedVm#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#update SiteRecoveryVmwareReplicatedVm#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f614ab26307040c4b951521574b283ac1fefdb6105e8a5d7e66f2aa31822cf55)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#create SiteRecoveryVmwareReplicatedVm#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#delete SiteRecoveryVmwareReplicatedVm#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#read SiteRecoveryVmwareReplicatedVm#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_vmware_replicated_vm#update SiteRecoveryVmwareReplicatedVm#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryVmwareReplicatedVmTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryVmwareReplicatedVmTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryVmwareReplicatedVm.SiteRecoveryVmwareReplicatedVmTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70f82474bc1478546f4d25e856e1949ae3928027f4b03a51d99d43061536dbbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db4cf5373de841fb304eab5af18061c608471f6e8ba8559dd7f41ed9f2aeb721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff8091ebb43c06f8a8920689d81b81031f3b80a9cbc6a8d0c87aed56b0fddd1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b22e419218582f022b4e190172887fd32cc1bbdf1b8bdd2baa41aeaa913c8d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__657bf00154a3bc82cef815fa9241cd65913d6519969252ab061b363fb22b7202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryVmwareReplicatedVmTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryVmwareReplicatedVmTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryVmwareReplicatedVmTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a732814e8c028ea7b2c4d7d38a0933d4cc959214ab5e1b16cac94af6775c6e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SiteRecoveryVmwareReplicatedVm",
    "SiteRecoveryVmwareReplicatedVmConfig",
    "SiteRecoveryVmwareReplicatedVmManagedDisk",
    "SiteRecoveryVmwareReplicatedVmManagedDiskList",
    "SiteRecoveryVmwareReplicatedVmManagedDiskOutputReference",
    "SiteRecoveryVmwareReplicatedVmNetworkInterface",
    "SiteRecoveryVmwareReplicatedVmNetworkInterfaceList",
    "SiteRecoveryVmwareReplicatedVmNetworkInterfaceOutputReference",
    "SiteRecoveryVmwareReplicatedVmTimeouts",
    "SiteRecoveryVmwareReplicatedVmTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4a6fca263f17433b17ec53b43b872d9019a303559c28001274f5b1a766a59aa8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    appliance_name: builtins.str,
    name: builtins.str,
    physical_server_credential_name: builtins.str,
    recovery_replication_policy_id: builtins.str,
    recovery_vault_id: builtins.str,
    source_vm_name: builtins.str,
    target_resource_group_id: builtins.str,
    target_vm_name: builtins.str,
    default_log_storage_account_id: typing.Optional[builtins.str] = None,
    default_recovery_disk_type: typing.Optional[builtins.str] = None,
    default_target_disk_encryption_set_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    license_type: typing.Optional[builtins.str] = None,
    managed_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryVmwareReplicatedVmManagedDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    multi_vm_group_name: typing.Optional[builtins.str] = None,
    network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryVmwareReplicatedVmNetworkInterface, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_availability_set_id: typing.Optional[builtins.str] = None,
    target_boot_diagnostics_storage_account_id: typing.Optional[builtins.str] = None,
    target_network_id: typing.Optional[builtins.str] = None,
    target_proximity_placement_group_id: typing.Optional[builtins.str] = None,
    target_vm_size: typing.Optional[builtins.str] = None,
    target_zone: typing.Optional[builtins.str] = None,
    test_network_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SiteRecoveryVmwareReplicatedVmTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c54888e33e7cbff8e3df7e7184939228ea325631f35e467d9c0fc64ab243957f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f242e8cbaac81f8d145e5bb3eceafdc16f61f994b8fac45c9fcc951984864a7d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryVmwareReplicatedVmManagedDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f55fa5486669545bb925b997a725cbbcddeaf7dc73798b7bc51dda228f839f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryVmwareReplicatedVmNetworkInterface, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0066c2de30f3eaa612c3d2fefd1ae414a2d38f5972897a7518963757c717870(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcde213adcd4b16d701747a47e9f51ac622df0d9a3c0817dd7ae248266936b35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc66f51c321de565df033d7c7862c42c48c774c0fc711cd1f2e1fcce846a4df1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10712789bb83b0d16cae63b140e72ff7b87e77a9aae0280b2a0cfe502562f43e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c8e435a8705ed738ab29166bfde616a3b1aa0cef83398c72d632408219b37e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d07560aec34fe365f9d88976357b363a790c869ede42b7a21972b713f87406b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08e898911265e3877643763d8dbaa4dfc47dab06f4cac6117673dcfacb619c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c09321f3235c4a3bbf3c5aba3fcbcfe00c2078b836474715bb99270c15d69b4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92346336b442d5b1d63b1162cc45570bc8908f49220c76f4e0857e4b2c4ad3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f98f0f0e0a81ca491609398cc5b2d83d291c150fa32dfcc990b7d4135045dfe0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b27b6ae8b225bb21a2181e5a1fec5ce623fc35f7fe0e67f7db66d49c923901eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c089fc6a45814abcc9e2ff2f5420d067620e3029fc33a238407e8dd901b49f9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ed7b6420b020727f70f23dfee133e574cc2b8f11dbec7a87050894938774e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd8d9c76ec3cef036b7362be72a141392e57bd4239e4c5b66c7f522ab738305(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bf78782cdf244963a7bf2dbd28d041eea06f3bd7ffe19ff689c712c742c80b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b532059fd0b973668b4a8144e0a48e6fdc591486ce80acd22584886e4568a4cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3209acfaf3ee01a5f18b4ff16f51986a6e2754567b9e2cef8b694fd1a3e3387d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee3d50754b09d2a2d0731aca4db868357b07abe820d700b8462d02e7a535f53f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c9fb2efd09401f64b773d9ef6b464083559f6bdb96d140fbdf23246e77f189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66bb39b86a005b0b632d3141693772b4c7cf4485330017d3adc3334cca7454e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8acef09a218463aa105ef6b3fa97b0c4f742297404dd38e979173113c922c43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5575b6560804a88585f0d6787f484ae1ea3e63e1719a82d35f38c08eb668aee3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    appliance_name: builtins.str,
    name: builtins.str,
    physical_server_credential_name: builtins.str,
    recovery_replication_policy_id: builtins.str,
    recovery_vault_id: builtins.str,
    source_vm_name: builtins.str,
    target_resource_group_id: builtins.str,
    target_vm_name: builtins.str,
    default_log_storage_account_id: typing.Optional[builtins.str] = None,
    default_recovery_disk_type: typing.Optional[builtins.str] = None,
    default_target_disk_encryption_set_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    license_type: typing.Optional[builtins.str] = None,
    managed_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryVmwareReplicatedVmManagedDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    multi_vm_group_name: typing.Optional[builtins.str] = None,
    network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryVmwareReplicatedVmNetworkInterface, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_availability_set_id: typing.Optional[builtins.str] = None,
    target_boot_diagnostics_storage_account_id: typing.Optional[builtins.str] = None,
    target_network_id: typing.Optional[builtins.str] = None,
    target_proximity_placement_group_id: typing.Optional[builtins.str] = None,
    target_vm_size: typing.Optional[builtins.str] = None,
    target_zone: typing.Optional[builtins.str] = None,
    test_network_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SiteRecoveryVmwareReplicatedVmTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abb477ea24c00aec21bae232c4fc298ef41114493946f9398293a7d403d0130(
    *,
    disk_id: builtins.str,
    target_disk_type: builtins.str,
    log_storage_account_id: typing.Optional[builtins.str] = None,
    target_disk_encryption_set_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d763c8bddddda19c39af933f90b35d9564138176a79206b798f032036a63a32e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8171968706b498ffe8d58df863af47dfebc80af7cdd029fc6631a4e52201f9f4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ecce40321f844dde9487d738364316c306543acce99ff359e41d5a2667402b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a506cc2220eb30bfe6cda819e082b2e76bb3c161b8d5113d62df8d6d996ed25(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600a935f1a6b8927f5b94b0ad788d56c2ae291bbfd31e890cfc72e776bf655d2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d323a5c211e6c4541dcc32526af616e6548245ca377a0d15439c9843b5dce25(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryVmwareReplicatedVmManagedDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d8d7d5a13235876142a990c2a1ad1cdb7e2e3e7de2c8bff2bfaa068ffe6e93c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9379159da6aa1aa2902b46caa0fe4e67dfdf42a90460825d255788f78939efc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54cb3344627e72e90523cfe5483dbed6a9bc05a34b673688002eb60c9b2f274(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__852ff2fe024bc1f61417a72ff9aab4c9c225eb50f9b6bbe28068bbcc9addbf0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0d6c0e86f32d386a9906cc5633b0ea6fdece3e0918a54de607837a56f9c746(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5fb357a12c620a574f3f08d6a7767b15ca8ff7f4c3e1ae793a916afd4c0775(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryVmwareReplicatedVmManagedDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39533a99e086ffb339df7393a2df7f009086d26c31fa7e83d68099c51bc8a157(
    *,
    is_primary: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    source_mac_address: builtins.str,
    target_static_ip: typing.Optional[builtins.str] = None,
    target_subnet_name: typing.Optional[builtins.str] = None,
    test_subnet_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a18fe4680db172ba1eb53e69f1f08032d58944546dc8ba6cf73e29c01208972(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1eeebfc0beda8b4a28bdacc1b2fdbb64d82373ff9cef1d7f7375400c121a1cb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edc18f50b5c3f4654543d0b6fe4d12accb164115e61597fe9d3e02755ccf891d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b15cb2c59d8c44722503424d2b661602e1ed90f292e41203a65faacc735044b7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8e15c4c3d029b72bc63c83d26aecc454f43e9a22ad1089723ec64406885300(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1aec63ce7d6e435761b2170014614d089fcf15a2cd1341823b369e2af6e942(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryVmwareReplicatedVmNetworkInterface]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c30053f6386fae136f086595f53805ecc470589630b9c9ea25cc6a7d85f63f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58504de0223ebe70c9921b8c9e25d08e5e4d49870aa5c40c7ee672ef22da125(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f008b6b1376ab405e560e3fcd91b99f7058e2bf82d9cc440d71893e881ef33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3aa95ceecb293a3f279e824f11dfc5672d1eb061f302daa5354dba74c137f86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bfcde550afe13d7408e97dbf4e8b9936c2e06c521fe3da49b299a66eba6a5ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0a6ae4ceeafc4edc177764187523fcc0d26ec5d9386b4150cc14a3dd3605442(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4940bd2412636bae3247260cfc56863c82a4aa76201c7c10f2766b9280b952(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryVmwareReplicatedVmNetworkInterface]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f614ab26307040c4b951521574b283ac1fefdb6105e8a5d7e66f2aa31822cf55(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f82474bc1478546f4d25e856e1949ae3928027f4b03a51d99d43061536dbbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db4cf5373de841fb304eab5af18061c608471f6e8ba8559dd7f41ed9f2aeb721(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8091ebb43c06f8a8920689d81b81031f3b80a9cbc6a8d0c87aed56b0fddd1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22e419218582f022b4e190172887fd32cc1bbdf1b8bdd2baa41aeaa913c8d96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__657bf00154a3bc82cef815fa9241cd65913d6519969252ab061b363fb22b7202(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a732814e8c028ea7b2c4d7d38a0933d4cc959214ab5e1b16cac94af6775c6e4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryVmwareReplicatedVmTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
