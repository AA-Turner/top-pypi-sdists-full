r'''
# `azurerm_managed_disk`

Refer to the Terraform Registry for docs: [`azurerm_managed_disk`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk).
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


class ManagedDisk(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.managedDisk.ManagedDisk",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk azurerm_managed_disk}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        create_option: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        storage_account_type: builtins.str,
        disk_access_id: typing.Optional[builtins.str] = None,
        disk_encryption_set_id: typing.Optional[builtins.str] = None,
        disk_iops_read_only: typing.Optional[jsii.Number] = None,
        disk_iops_read_write: typing.Optional[jsii.Number] = None,
        disk_mbps_read_only: typing.Optional[jsii.Number] = None,
        disk_mbps_read_write: typing.Optional[jsii.Number] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        edge_zone: typing.Optional[builtins.str] = None,
        encryption_settings: typing.Optional[typing.Union["ManagedDiskEncryptionSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        gallery_image_reference_id: typing.Optional[builtins.str] = None,
        hyper_v_generation: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_reference_id: typing.Optional[builtins.str] = None,
        logical_sector_size: typing.Optional[jsii.Number] = None,
        max_shares: typing.Optional[jsii.Number] = None,
        network_access_policy: typing.Optional[builtins.str] = None,
        on_demand_bursting_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        optimized_frequent_attach_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        os_type: typing.Optional[builtins.str] = None,
        performance_plus_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secure_vm_disk_encryption_set_id: typing.Optional[builtins.str] = None,
        security_type: typing.Optional[builtins.str] = None,
        source_resource_id: typing.Optional[builtins.str] = None,
        source_uri: typing.Optional[builtins.str] = None,
        storage_account_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tier: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ManagedDiskTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trusted_launch_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        upload_size_bytes: typing.Optional[jsii.Number] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk azurerm_managed_disk} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param create_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#create_option ManagedDisk#create_option}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#location ManagedDisk#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#name ManagedDisk#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#resource_group_name ManagedDisk#resource_group_name}.
        :param storage_account_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#storage_account_type ManagedDisk#storage_account_type}.
        :param disk_access_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_access_id ManagedDisk#disk_access_id}.
        :param disk_encryption_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_encryption_set_id ManagedDisk#disk_encryption_set_id}.
        :param disk_iops_read_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_iops_read_only ManagedDisk#disk_iops_read_only}.
        :param disk_iops_read_write: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_iops_read_write ManagedDisk#disk_iops_read_write}.
        :param disk_mbps_read_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_mbps_read_only ManagedDisk#disk_mbps_read_only}.
        :param disk_mbps_read_write: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_mbps_read_write ManagedDisk#disk_mbps_read_write}.
        :param disk_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_size_gb ManagedDisk#disk_size_gb}.
        :param edge_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#edge_zone ManagedDisk#edge_zone}.
        :param encryption_settings: encryption_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#encryption_settings ManagedDisk#encryption_settings}
        :param gallery_image_reference_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#gallery_image_reference_id ManagedDisk#gallery_image_reference_id}.
        :param hyper_v_generation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#hyper_v_generation ManagedDisk#hyper_v_generation}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#id ManagedDisk#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_reference_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#image_reference_id ManagedDisk#image_reference_id}.
        :param logical_sector_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#logical_sector_size ManagedDisk#logical_sector_size}.
        :param max_shares: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#max_shares ManagedDisk#max_shares}.
        :param network_access_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#network_access_policy ManagedDisk#network_access_policy}.
        :param on_demand_bursting_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#on_demand_bursting_enabled ManagedDisk#on_demand_bursting_enabled}.
        :param optimized_frequent_attach_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#optimized_frequent_attach_enabled ManagedDisk#optimized_frequent_attach_enabled}.
        :param os_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#os_type ManagedDisk#os_type}.
        :param performance_plus_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#performance_plus_enabled ManagedDisk#performance_plus_enabled}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#public_network_access_enabled ManagedDisk#public_network_access_enabled}.
        :param secure_vm_disk_encryption_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#secure_vm_disk_encryption_set_id ManagedDisk#secure_vm_disk_encryption_set_id}.
        :param security_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#security_type ManagedDisk#security_type}.
        :param source_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#source_resource_id ManagedDisk#source_resource_id}.
        :param source_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#source_uri ManagedDisk#source_uri}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#storage_account_id ManagedDisk#storage_account_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#tags ManagedDisk#tags}.
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#tier ManagedDisk#tier}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#timeouts ManagedDisk#timeouts}
        :param trusted_launch_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#trusted_launch_enabled ManagedDisk#trusted_launch_enabled}.
        :param upload_size_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#upload_size_bytes ManagedDisk#upload_size_bytes}.
        :param zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#zone ManagedDisk#zone}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fadb273c20201a8b7700be6b69e6a818c40ccb3a25501ed98b6e8612f0fd8a8f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ManagedDiskConfig(
            create_option=create_option,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            storage_account_type=storage_account_type,
            disk_access_id=disk_access_id,
            disk_encryption_set_id=disk_encryption_set_id,
            disk_iops_read_only=disk_iops_read_only,
            disk_iops_read_write=disk_iops_read_write,
            disk_mbps_read_only=disk_mbps_read_only,
            disk_mbps_read_write=disk_mbps_read_write,
            disk_size_gb=disk_size_gb,
            edge_zone=edge_zone,
            encryption_settings=encryption_settings,
            gallery_image_reference_id=gallery_image_reference_id,
            hyper_v_generation=hyper_v_generation,
            id=id,
            image_reference_id=image_reference_id,
            logical_sector_size=logical_sector_size,
            max_shares=max_shares,
            network_access_policy=network_access_policy,
            on_demand_bursting_enabled=on_demand_bursting_enabled,
            optimized_frequent_attach_enabled=optimized_frequent_attach_enabled,
            os_type=os_type,
            performance_plus_enabled=performance_plus_enabled,
            public_network_access_enabled=public_network_access_enabled,
            secure_vm_disk_encryption_set_id=secure_vm_disk_encryption_set_id,
            security_type=security_type,
            source_resource_id=source_resource_id,
            source_uri=source_uri,
            storage_account_id=storage_account_id,
            tags=tags,
            tier=tier,
            timeouts=timeouts,
            trusted_launch_enabled=trusted_launch_enabled,
            upload_size_bytes=upload_size_bytes,
            zone=zone,
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
        '''Generates CDKTF code for importing a ManagedDisk resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ManagedDisk to import.
        :param import_from_id: The id of the existing ManagedDisk that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ManagedDisk to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88cf4e1618190ab6d5f156374e7626007e762e5bf95cd9bcd9bb3904fa8b45f8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEncryptionSettings")
    def put_encryption_settings(
        self,
        *,
        disk_encryption_key: typing.Union["ManagedDiskEncryptionSettingsDiskEncryptionKey", typing.Dict[builtins.str, typing.Any]],
        key_encryption_key: typing.Optional[typing.Union["ManagedDiskEncryptionSettingsKeyEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param disk_encryption_key: disk_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_encryption_key ManagedDisk#disk_encryption_key}
        :param key_encryption_key: key_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#key_encryption_key ManagedDisk#key_encryption_key}
        '''
        value = ManagedDiskEncryptionSettings(
            disk_encryption_key=disk_encryption_key,
            key_encryption_key=key_encryption_key,
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionSettings", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#create ManagedDisk#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#delete ManagedDisk#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#read ManagedDisk#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#update ManagedDisk#update}.
        '''
        value = ManagedDiskTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDiskAccessId")
    def reset_disk_access_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskAccessId", []))

    @jsii.member(jsii_name="resetDiskEncryptionSetId")
    def reset_disk_encryption_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionSetId", []))

    @jsii.member(jsii_name="resetDiskIopsReadOnly")
    def reset_disk_iops_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskIopsReadOnly", []))

    @jsii.member(jsii_name="resetDiskIopsReadWrite")
    def reset_disk_iops_read_write(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskIopsReadWrite", []))

    @jsii.member(jsii_name="resetDiskMbpsReadOnly")
    def reset_disk_mbps_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskMbpsReadOnly", []))

    @jsii.member(jsii_name="resetDiskMbpsReadWrite")
    def reset_disk_mbps_read_write(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskMbpsReadWrite", []))

    @jsii.member(jsii_name="resetDiskSizeGb")
    def reset_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGb", []))

    @jsii.member(jsii_name="resetEdgeZone")
    def reset_edge_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeZone", []))

    @jsii.member(jsii_name="resetEncryptionSettings")
    def reset_encryption_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionSettings", []))

    @jsii.member(jsii_name="resetGalleryImageReferenceId")
    def reset_gallery_image_reference_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGalleryImageReferenceId", []))

    @jsii.member(jsii_name="resetHyperVGeneration")
    def reset_hyper_v_generation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHyperVGeneration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageReferenceId")
    def reset_image_reference_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageReferenceId", []))

    @jsii.member(jsii_name="resetLogicalSectorSize")
    def reset_logical_sector_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogicalSectorSize", []))

    @jsii.member(jsii_name="resetMaxShares")
    def reset_max_shares(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxShares", []))

    @jsii.member(jsii_name="resetNetworkAccessPolicy")
    def reset_network_access_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkAccessPolicy", []))

    @jsii.member(jsii_name="resetOnDemandBurstingEnabled")
    def reset_on_demand_bursting_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnDemandBurstingEnabled", []))

    @jsii.member(jsii_name="resetOptimizedFrequentAttachEnabled")
    def reset_optimized_frequent_attach_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptimizedFrequentAttachEnabled", []))

    @jsii.member(jsii_name="resetOsType")
    def reset_os_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsType", []))

    @jsii.member(jsii_name="resetPerformancePlusEnabled")
    def reset_performance_plus_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerformancePlusEnabled", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

    @jsii.member(jsii_name="resetSecureVmDiskEncryptionSetId")
    def reset_secure_vm_disk_encryption_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecureVmDiskEncryptionSetId", []))

    @jsii.member(jsii_name="resetSecurityType")
    def reset_security_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityType", []))

    @jsii.member(jsii_name="resetSourceResourceId")
    def reset_source_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceResourceId", []))

    @jsii.member(jsii_name="resetSourceUri")
    def reset_source_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceUri", []))

    @jsii.member(jsii_name="resetStorageAccountId")
    def reset_storage_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTier")
    def reset_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTier", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTrustedLaunchEnabled")
    def reset_trusted_launch_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedLaunchEnabled", []))

    @jsii.member(jsii_name="resetUploadSizeBytes")
    def reset_upload_size_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUploadSizeBytes", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

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
    @jsii.member(jsii_name="encryptionSettings")
    def encryption_settings(self) -> "ManagedDiskEncryptionSettingsOutputReference":
        return typing.cast("ManagedDiskEncryptionSettingsOutputReference", jsii.get(self, "encryptionSettings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ManagedDiskTimeoutsOutputReference":
        return typing.cast("ManagedDiskTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="createOptionInput")
    def create_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="diskAccessIdInput")
    def disk_access_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskAccessIdInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionSetIdInput")
    def disk_encryption_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="diskIopsReadOnlyInput")
    def disk_iops_read_only_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskIopsReadOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="diskIopsReadWriteInput")
    def disk_iops_read_write_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskIopsReadWriteInput"))

    @builtins.property
    @jsii.member(jsii_name="diskMbpsReadOnlyInput")
    def disk_mbps_read_only_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskMbpsReadOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="diskMbpsReadWriteInput")
    def disk_mbps_read_write_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskMbpsReadWriteInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeZoneInput")
    def edge_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionSettingsInput")
    def encryption_settings_input(
        self,
    ) -> typing.Optional["ManagedDiskEncryptionSettings"]:
        return typing.cast(typing.Optional["ManagedDiskEncryptionSettings"], jsii.get(self, "encryptionSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="galleryImageReferenceIdInput")
    def gallery_image_reference_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "galleryImageReferenceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="hyperVGenerationInput")
    def hyper_v_generation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hyperVGenerationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageReferenceIdInput")
    def image_reference_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageReferenceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="logicalSectorSizeInput")
    def logical_sector_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "logicalSectorSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSharesInput")
    def max_shares_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxSharesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkAccessPolicyInput")
    def network_access_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkAccessPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="onDemandBurstingEnabledInput")
    def on_demand_bursting_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "onDemandBurstingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="optimizedFrequentAttachEnabledInput")
    def optimized_frequent_attach_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "optimizedFrequentAttachEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="osTypeInput")
    def os_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="performancePlusEnabledInput")
    def performance_plus_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "performancePlusEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabledInput")
    def public_network_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicNetworkAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secureVmDiskEncryptionSetIdInput")
    def secure_vm_disk_encryption_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secureVmDiskEncryptionSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="securityTypeInput")
    def security_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceResourceIdInput")
    def source_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceUriInput")
    def source_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceUriInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountIdInput")
    def storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountTypeInput")
    def storage_account_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ManagedDiskTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ManagedDiskTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedLaunchEnabledInput")
    def trusted_launch_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "trustedLaunchEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="uploadSizeBytesInput")
    def upload_size_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "uploadSizeBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="createOption")
    def create_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createOption"))

    @create_option.setter
    def create_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cffae0eb777d7c8b2174f637af110741aaa262cfbe8c665a85b6c29eac8ec1e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskAccessId")
    def disk_access_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskAccessId"))

    @disk_access_id.setter
    def disk_access_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6318b292acd96401a4fcca6cd06520368cc36d7e0849988e719f3a454d6ae02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskAccessId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionSetId")
    def disk_encryption_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionSetId"))

    @disk_encryption_set_id.setter
    def disk_encryption_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09d596e8720d7ebbdd8f5413736939886516c8f7bc40ecb942032c31e44d2c07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskIopsReadOnly")
    def disk_iops_read_only(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskIopsReadOnly"))

    @disk_iops_read_only.setter
    def disk_iops_read_only(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5970e6f2ef6fe9bae0c71e23aef9fc2b35d3adc3ad79a2497a027aec1294847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskIopsReadOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskIopsReadWrite")
    def disk_iops_read_write(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskIopsReadWrite"))

    @disk_iops_read_write.setter
    def disk_iops_read_write(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8837605941139c76bd30ac350f3feff94420921ef701426a931e1cb8390f07e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskIopsReadWrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskMbpsReadOnly")
    def disk_mbps_read_only(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskMbpsReadOnly"))

    @disk_mbps_read_only.setter
    def disk_mbps_read_only(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c18163d92e57c48af6d179f1c72021a4631912d775e6d5419685ed4a070c327f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskMbpsReadOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskMbpsReadWrite")
    def disk_mbps_read_write(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskMbpsReadWrite"))

    @disk_mbps_read_write.setter
    def disk_mbps_read_write(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e80606cb4c2d3d3dd7358c69ec8b54b1cd7e273104fc3157f07d4dd63117bcec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskMbpsReadWrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd94b16fee19df182cb677f5e4296a8f89b82aee2baadbe240b9b2f974a21cbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgeZone")
    def edge_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeZone"))

    @edge_zone.setter
    def edge_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187088e2c7c372cda91b70dfaf1a044da3b9fa441e58cb07642e0cb18469701c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="galleryImageReferenceId")
    def gallery_image_reference_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "galleryImageReferenceId"))

    @gallery_image_reference_id.setter
    def gallery_image_reference_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13f24f9717f6d126f6e61266549fff9711b416dd8cf8877d23157df70c2df63e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "galleryImageReferenceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hyperVGeneration")
    def hyper_v_generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hyperVGeneration"))

    @hyper_v_generation.setter
    def hyper_v_generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2508046ad09a05ded697f6dc8f34bff1583f7eae84f22210556f4fca6a7c57a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hyperVGeneration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76c46fb4b507bf63cab27cf7e378238622f4d3fdfafe634c28967db709ff9f8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageReferenceId")
    def image_reference_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageReferenceId"))

    @image_reference_id.setter
    def image_reference_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7db6721dd337af5d8b5d7f97bf88dc3d090fd38bb57755c4b2d9ff12b8bd4a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageReferenceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6330186b165b7f5e8170914c4b50d674e4bf11d831668c1cbe710d3c9db22e47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logicalSectorSize")
    def logical_sector_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "logicalSectorSize"))

    @logical_sector_size.setter
    def logical_sector_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80494ca1dec83fae3ca9a03a17f6cd9847fc181efee49cec62bbb980bf7cdfa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logicalSectorSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxShares")
    def max_shares(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxShares"))

    @max_shares.setter
    def max_shares(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3256c0d84d06eaab0a51d62b3da67bb336bbb06ac01252326635c5316ecf776)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxShares", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a3ffb31cf58cb79c6b01cfe500abe7a7036c2913b0e5a23784aeda2fdf2fb5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkAccessPolicy")
    def network_access_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkAccessPolicy"))

    @network_access_policy.setter
    def network_access_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91edc5196320deb4a948bad76dc7529c6ebf8bee5e83191d82e285121f124ade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkAccessPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onDemandBurstingEnabled")
    def on_demand_bursting_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "onDemandBurstingEnabled"))

    @on_demand_bursting_enabled.setter
    def on_demand_bursting_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3985ebc8f48a9f10bc769eb53d8dfdc5073303ac727647456c154d17982cf2c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onDemandBurstingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optimizedFrequentAttachEnabled")
    def optimized_frequent_attach_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "optimizedFrequentAttachEnabled"))

    @optimized_frequent_attach_enabled.setter
    def optimized_frequent_attach_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e524092c088bda174df18113b6dfdf84b387b2b5ab5f4e65dbde1e843969f0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optimizedFrequentAttachEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @os_type.setter
    def os_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a189808ea2e8be1526ae38615c9775197017d8b069c08f7a4b981c5d1c09eae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="performancePlusEnabled")
    def performance_plus_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "performancePlusEnabled"))

    @performance_plus_enabled.setter
    def performance_plus_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42fb3c973f88e471c1ed87f41b90bf2b13f53f5d62998e66c31d83e2e82df54b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "performancePlusEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabled")
    def public_network_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publicNetworkAccessEnabled"))

    @public_network_access_enabled.setter
    def public_network_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca82d39a3b415f4d78bccae4920eac43d01e3954092e6f0c02d9cde03187adf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f24c9fdb64c4e24327075fe7eff9fc8a36b12ef3dce9b04ebe8569fd9562c45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secureVmDiskEncryptionSetId")
    def secure_vm_disk_encryption_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secureVmDiskEncryptionSetId"))

    @secure_vm_disk_encryption_set_id.setter
    def secure_vm_disk_encryption_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f6df24406ce512a1559a3594bce3b80a0f0793b7fdefece9c817185abb9d25c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secureVmDiskEncryptionSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityType")
    def security_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityType"))

    @security_type.setter
    def security_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa858d35b1c4b6ecf33a2f005ee5ba11c963a04a734146844005a8d9dd5e69c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceResourceId")
    def source_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceResourceId"))

    @source_resource_id.setter
    def source_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f3cbf4ea2362ad94444bac6b1c41c562bba441b5ae44ec5fb26b25867cb824)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceUri")
    def source_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceUri"))

    @source_uri.setter
    def source_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96baad71f948e3b2f7876f6b201015f2516e7bb381885b2e8cd4aebba06e43ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountId")
    def storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountId"))

    @storage_account_id.setter
    def storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50e4f06e901b59eea740a5054a6e4f87138eef1fa6a39d3bdd30ad0f5fd4f21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountType")
    def storage_account_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountType"))

    @storage_account_type.setter
    def storage_account_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7551b0dbddbbb25824812a3dfb0fa73dd087c818ee729e535497fa83ced5b11e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d756504fd96347fce8428c63e0d7566237416b2fe5a74e00a71621c6f795564f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be05305320a35c260308b8f7659651e476fd7d74f626c4f4a926025947ad8ff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustedLaunchEnabled")
    def trusted_launch_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "trustedLaunchEnabled"))

    @trusted_launch_enabled.setter
    def trusted_launch_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58e188230059a97d10a63651086e841d0928ce8a7e41e92c2ac456414898455)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedLaunchEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uploadSizeBytes")
    def upload_size_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "uploadSizeBytes"))

    @upload_size_bytes.setter
    def upload_size_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d01d5511b185249dcef90906613f400b45f0095c5ba506f6f5b5623a033dd734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uploadSizeBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b26cfcc69c5d046bf8692af92a3012a17d1f680c488567a5e7255da49521c909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.managedDisk.ManagedDiskConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "create_option": "createOption",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "storage_account_type": "storageAccountType",
        "disk_access_id": "diskAccessId",
        "disk_encryption_set_id": "diskEncryptionSetId",
        "disk_iops_read_only": "diskIopsReadOnly",
        "disk_iops_read_write": "diskIopsReadWrite",
        "disk_mbps_read_only": "diskMbpsReadOnly",
        "disk_mbps_read_write": "diskMbpsReadWrite",
        "disk_size_gb": "diskSizeGb",
        "edge_zone": "edgeZone",
        "encryption_settings": "encryptionSettings",
        "gallery_image_reference_id": "galleryImageReferenceId",
        "hyper_v_generation": "hyperVGeneration",
        "id": "id",
        "image_reference_id": "imageReferenceId",
        "logical_sector_size": "logicalSectorSize",
        "max_shares": "maxShares",
        "network_access_policy": "networkAccessPolicy",
        "on_demand_bursting_enabled": "onDemandBurstingEnabled",
        "optimized_frequent_attach_enabled": "optimizedFrequentAttachEnabled",
        "os_type": "osType",
        "performance_plus_enabled": "performancePlusEnabled",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "secure_vm_disk_encryption_set_id": "secureVmDiskEncryptionSetId",
        "security_type": "securityType",
        "source_resource_id": "sourceResourceId",
        "source_uri": "sourceUri",
        "storage_account_id": "storageAccountId",
        "tags": "tags",
        "tier": "tier",
        "timeouts": "timeouts",
        "trusted_launch_enabled": "trustedLaunchEnabled",
        "upload_size_bytes": "uploadSizeBytes",
        "zone": "zone",
    },
)
class ManagedDiskConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        create_option: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        storage_account_type: builtins.str,
        disk_access_id: typing.Optional[builtins.str] = None,
        disk_encryption_set_id: typing.Optional[builtins.str] = None,
        disk_iops_read_only: typing.Optional[jsii.Number] = None,
        disk_iops_read_write: typing.Optional[jsii.Number] = None,
        disk_mbps_read_only: typing.Optional[jsii.Number] = None,
        disk_mbps_read_write: typing.Optional[jsii.Number] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        edge_zone: typing.Optional[builtins.str] = None,
        encryption_settings: typing.Optional[typing.Union["ManagedDiskEncryptionSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        gallery_image_reference_id: typing.Optional[builtins.str] = None,
        hyper_v_generation: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_reference_id: typing.Optional[builtins.str] = None,
        logical_sector_size: typing.Optional[jsii.Number] = None,
        max_shares: typing.Optional[jsii.Number] = None,
        network_access_policy: typing.Optional[builtins.str] = None,
        on_demand_bursting_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        optimized_frequent_attach_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        os_type: typing.Optional[builtins.str] = None,
        performance_plus_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secure_vm_disk_encryption_set_id: typing.Optional[builtins.str] = None,
        security_type: typing.Optional[builtins.str] = None,
        source_resource_id: typing.Optional[builtins.str] = None,
        source_uri: typing.Optional[builtins.str] = None,
        storage_account_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tier: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ManagedDiskTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trusted_launch_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        upload_size_bytes: typing.Optional[jsii.Number] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param create_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#create_option ManagedDisk#create_option}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#location ManagedDisk#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#name ManagedDisk#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#resource_group_name ManagedDisk#resource_group_name}.
        :param storage_account_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#storage_account_type ManagedDisk#storage_account_type}.
        :param disk_access_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_access_id ManagedDisk#disk_access_id}.
        :param disk_encryption_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_encryption_set_id ManagedDisk#disk_encryption_set_id}.
        :param disk_iops_read_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_iops_read_only ManagedDisk#disk_iops_read_only}.
        :param disk_iops_read_write: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_iops_read_write ManagedDisk#disk_iops_read_write}.
        :param disk_mbps_read_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_mbps_read_only ManagedDisk#disk_mbps_read_only}.
        :param disk_mbps_read_write: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_mbps_read_write ManagedDisk#disk_mbps_read_write}.
        :param disk_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_size_gb ManagedDisk#disk_size_gb}.
        :param edge_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#edge_zone ManagedDisk#edge_zone}.
        :param encryption_settings: encryption_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#encryption_settings ManagedDisk#encryption_settings}
        :param gallery_image_reference_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#gallery_image_reference_id ManagedDisk#gallery_image_reference_id}.
        :param hyper_v_generation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#hyper_v_generation ManagedDisk#hyper_v_generation}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#id ManagedDisk#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_reference_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#image_reference_id ManagedDisk#image_reference_id}.
        :param logical_sector_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#logical_sector_size ManagedDisk#logical_sector_size}.
        :param max_shares: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#max_shares ManagedDisk#max_shares}.
        :param network_access_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#network_access_policy ManagedDisk#network_access_policy}.
        :param on_demand_bursting_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#on_demand_bursting_enabled ManagedDisk#on_demand_bursting_enabled}.
        :param optimized_frequent_attach_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#optimized_frequent_attach_enabled ManagedDisk#optimized_frequent_attach_enabled}.
        :param os_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#os_type ManagedDisk#os_type}.
        :param performance_plus_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#performance_plus_enabled ManagedDisk#performance_plus_enabled}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#public_network_access_enabled ManagedDisk#public_network_access_enabled}.
        :param secure_vm_disk_encryption_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#secure_vm_disk_encryption_set_id ManagedDisk#secure_vm_disk_encryption_set_id}.
        :param security_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#security_type ManagedDisk#security_type}.
        :param source_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#source_resource_id ManagedDisk#source_resource_id}.
        :param source_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#source_uri ManagedDisk#source_uri}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#storage_account_id ManagedDisk#storage_account_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#tags ManagedDisk#tags}.
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#tier ManagedDisk#tier}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#timeouts ManagedDisk#timeouts}
        :param trusted_launch_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#trusted_launch_enabled ManagedDisk#trusted_launch_enabled}.
        :param upload_size_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#upload_size_bytes ManagedDisk#upload_size_bytes}.
        :param zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#zone ManagedDisk#zone}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(encryption_settings, dict):
            encryption_settings = ManagedDiskEncryptionSettings(**encryption_settings)
        if isinstance(timeouts, dict):
            timeouts = ManagedDiskTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a37a5b0622a17eaf7afb7e3c113d9788517026ea809ca1a844d08b006871c992)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument create_option", value=create_option, expected_type=type_hints["create_option"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument storage_account_type", value=storage_account_type, expected_type=type_hints["storage_account_type"])
            check_type(argname="argument disk_access_id", value=disk_access_id, expected_type=type_hints["disk_access_id"])
            check_type(argname="argument disk_encryption_set_id", value=disk_encryption_set_id, expected_type=type_hints["disk_encryption_set_id"])
            check_type(argname="argument disk_iops_read_only", value=disk_iops_read_only, expected_type=type_hints["disk_iops_read_only"])
            check_type(argname="argument disk_iops_read_write", value=disk_iops_read_write, expected_type=type_hints["disk_iops_read_write"])
            check_type(argname="argument disk_mbps_read_only", value=disk_mbps_read_only, expected_type=type_hints["disk_mbps_read_only"])
            check_type(argname="argument disk_mbps_read_write", value=disk_mbps_read_write, expected_type=type_hints["disk_mbps_read_write"])
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument edge_zone", value=edge_zone, expected_type=type_hints["edge_zone"])
            check_type(argname="argument encryption_settings", value=encryption_settings, expected_type=type_hints["encryption_settings"])
            check_type(argname="argument gallery_image_reference_id", value=gallery_image_reference_id, expected_type=type_hints["gallery_image_reference_id"])
            check_type(argname="argument hyper_v_generation", value=hyper_v_generation, expected_type=type_hints["hyper_v_generation"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_reference_id", value=image_reference_id, expected_type=type_hints["image_reference_id"])
            check_type(argname="argument logical_sector_size", value=logical_sector_size, expected_type=type_hints["logical_sector_size"])
            check_type(argname="argument max_shares", value=max_shares, expected_type=type_hints["max_shares"])
            check_type(argname="argument network_access_policy", value=network_access_policy, expected_type=type_hints["network_access_policy"])
            check_type(argname="argument on_demand_bursting_enabled", value=on_demand_bursting_enabled, expected_type=type_hints["on_demand_bursting_enabled"])
            check_type(argname="argument optimized_frequent_attach_enabled", value=optimized_frequent_attach_enabled, expected_type=type_hints["optimized_frequent_attach_enabled"])
            check_type(argname="argument os_type", value=os_type, expected_type=type_hints["os_type"])
            check_type(argname="argument performance_plus_enabled", value=performance_plus_enabled, expected_type=type_hints["performance_plus_enabled"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument secure_vm_disk_encryption_set_id", value=secure_vm_disk_encryption_set_id, expected_type=type_hints["secure_vm_disk_encryption_set_id"])
            check_type(argname="argument security_type", value=security_type, expected_type=type_hints["security_type"])
            check_type(argname="argument source_resource_id", value=source_resource_id, expected_type=type_hints["source_resource_id"])
            check_type(argname="argument source_uri", value=source_uri, expected_type=type_hints["source_uri"])
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument trusted_launch_enabled", value=trusted_launch_enabled, expected_type=type_hints["trusted_launch_enabled"])
            check_type(argname="argument upload_size_bytes", value=upload_size_bytes, expected_type=type_hints["upload_size_bytes"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "create_option": create_option,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "storage_account_type": storage_account_type,
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
        if disk_access_id is not None:
            self._values["disk_access_id"] = disk_access_id
        if disk_encryption_set_id is not None:
            self._values["disk_encryption_set_id"] = disk_encryption_set_id
        if disk_iops_read_only is not None:
            self._values["disk_iops_read_only"] = disk_iops_read_only
        if disk_iops_read_write is not None:
            self._values["disk_iops_read_write"] = disk_iops_read_write
        if disk_mbps_read_only is not None:
            self._values["disk_mbps_read_only"] = disk_mbps_read_only
        if disk_mbps_read_write is not None:
            self._values["disk_mbps_read_write"] = disk_mbps_read_write
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if edge_zone is not None:
            self._values["edge_zone"] = edge_zone
        if encryption_settings is not None:
            self._values["encryption_settings"] = encryption_settings
        if gallery_image_reference_id is not None:
            self._values["gallery_image_reference_id"] = gallery_image_reference_id
        if hyper_v_generation is not None:
            self._values["hyper_v_generation"] = hyper_v_generation
        if id is not None:
            self._values["id"] = id
        if image_reference_id is not None:
            self._values["image_reference_id"] = image_reference_id
        if logical_sector_size is not None:
            self._values["logical_sector_size"] = logical_sector_size
        if max_shares is not None:
            self._values["max_shares"] = max_shares
        if network_access_policy is not None:
            self._values["network_access_policy"] = network_access_policy
        if on_demand_bursting_enabled is not None:
            self._values["on_demand_bursting_enabled"] = on_demand_bursting_enabled
        if optimized_frequent_attach_enabled is not None:
            self._values["optimized_frequent_attach_enabled"] = optimized_frequent_attach_enabled
        if os_type is not None:
            self._values["os_type"] = os_type
        if performance_plus_enabled is not None:
            self._values["performance_plus_enabled"] = performance_plus_enabled
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if secure_vm_disk_encryption_set_id is not None:
            self._values["secure_vm_disk_encryption_set_id"] = secure_vm_disk_encryption_set_id
        if security_type is not None:
            self._values["security_type"] = security_type
        if source_resource_id is not None:
            self._values["source_resource_id"] = source_resource_id
        if source_uri is not None:
            self._values["source_uri"] = source_uri
        if storage_account_id is not None:
            self._values["storage_account_id"] = storage_account_id
        if tags is not None:
            self._values["tags"] = tags
        if tier is not None:
            self._values["tier"] = tier
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if trusted_launch_enabled is not None:
            self._values["trusted_launch_enabled"] = trusted_launch_enabled
        if upload_size_bytes is not None:
            self._values["upload_size_bytes"] = upload_size_bytes
        if zone is not None:
            self._values["zone"] = zone

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
    def create_option(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#create_option ManagedDisk#create_option}.'''
        result = self._values.get("create_option")
        assert result is not None, "Required property 'create_option' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#location ManagedDisk#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#name ManagedDisk#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#resource_group_name ManagedDisk#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#storage_account_type ManagedDisk#storage_account_type}.'''
        result = self._values.get("storage_account_type")
        assert result is not None, "Required property 'storage_account_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk_access_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_access_id ManagedDisk#disk_access_id}.'''
        result = self._values.get("disk_access_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_encryption_set_id ManagedDisk#disk_encryption_set_id}.'''
        result = self._values.get("disk_encryption_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_iops_read_only(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_iops_read_only ManagedDisk#disk_iops_read_only}.'''
        result = self._values.get("disk_iops_read_only")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_iops_read_write(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_iops_read_write ManagedDisk#disk_iops_read_write}.'''
        result = self._values.get("disk_iops_read_write")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_mbps_read_only(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_mbps_read_only ManagedDisk#disk_mbps_read_only}.'''
        result = self._values.get("disk_mbps_read_only")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_mbps_read_write(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_mbps_read_write ManagedDisk#disk_mbps_read_write}.'''
        result = self._values.get("disk_mbps_read_write")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_size_gb ManagedDisk#disk_size_gb}.'''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def edge_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#edge_zone ManagedDisk#edge_zone}.'''
        result = self._values.get("edge_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_settings(self) -> typing.Optional["ManagedDiskEncryptionSettings"]:
        '''encryption_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#encryption_settings ManagedDisk#encryption_settings}
        '''
        result = self._values.get("encryption_settings")
        return typing.cast(typing.Optional["ManagedDiskEncryptionSettings"], result)

    @builtins.property
    def gallery_image_reference_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#gallery_image_reference_id ManagedDisk#gallery_image_reference_id}.'''
        result = self._values.get("gallery_image_reference_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hyper_v_generation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#hyper_v_generation ManagedDisk#hyper_v_generation}.'''
        result = self._values.get("hyper_v_generation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#id ManagedDisk#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_reference_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#image_reference_id ManagedDisk#image_reference_id}.'''
        result = self._values.get("image_reference_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logical_sector_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#logical_sector_size ManagedDisk#logical_sector_size}.'''
        result = self._values.get("logical_sector_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_shares(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#max_shares ManagedDisk#max_shares}.'''
        result = self._values.get("max_shares")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network_access_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#network_access_policy ManagedDisk#network_access_policy}.'''
        result = self._values.get("network_access_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_demand_bursting_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#on_demand_bursting_enabled ManagedDisk#on_demand_bursting_enabled}.'''
        result = self._values.get("on_demand_bursting_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def optimized_frequent_attach_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#optimized_frequent_attach_enabled ManagedDisk#optimized_frequent_attach_enabled}.'''
        result = self._values.get("optimized_frequent_attach_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def os_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#os_type ManagedDisk#os_type}.'''
        result = self._values.get("os_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def performance_plus_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#performance_plus_enabled ManagedDisk#performance_plus_enabled}.'''
        result = self._values.get("performance_plus_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#public_network_access_enabled ManagedDisk#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secure_vm_disk_encryption_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#secure_vm_disk_encryption_set_id ManagedDisk#secure_vm_disk_encryption_set_id}.'''
        result = self._values.get("secure_vm_disk_encryption_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#security_type ManagedDisk#security_type}.'''
        result = self._values.get("security_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#source_resource_id ManagedDisk#source_resource_id}.'''
        result = self._values.get("source_resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#source_uri ManagedDisk#source_uri}.'''
        result = self._values.get("source_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#storage_account_id ManagedDisk#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#tags ManagedDisk#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#tier ManagedDisk#tier}.'''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ManagedDiskTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#timeouts ManagedDisk#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ManagedDiskTimeouts"], result)

    @builtins.property
    def trusted_launch_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#trusted_launch_enabled ManagedDisk#trusted_launch_enabled}.'''
        result = self._values.get("trusted_launch_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def upload_size_bytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#upload_size_bytes ManagedDisk#upload_size_bytes}.'''
        result = self._values.get("upload_size_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#zone ManagedDisk#zone}.'''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedDiskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.managedDisk.ManagedDiskEncryptionSettings",
    jsii_struct_bases=[],
    name_mapping={
        "disk_encryption_key": "diskEncryptionKey",
        "key_encryption_key": "keyEncryptionKey",
    },
)
class ManagedDiskEncryptionSettings:
    def __init__(
        self,
        *,
        disk_encryption_key: typing.Union["ManagedDiskEncryptionSettingsDiskEncryptionKey", typing.Dict[builtins.str, typing.Any]],
        key_encryption_key: typing.Optional[typing.Union["ManagedDiskEncryptionSettingsKeyEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param disk_encryption_key: disk_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_encryption_key ManagedDisk#disk_encryption_key}
        :param key_encryption_key: key_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#key_encryption_key ManagedDisk#key_encryption_key}
        '''
        if isinstance(disk_encryption_key, dict):
            disk_encryption_key = ManagedDiskEncryptionSettingsDiskEncryptionKey(**disk_encryption_key)
        if isinstance(key_encryption_key, dict):
            key_encryption_key = ManagedDiskEncryptionSettingsKeyEncryptionKey(**key_encryption_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bc527a6cdc3e705ed587e1b1887858b93f03c8873d0c88d1db1f2a5e44fd14d)
            check_type(argname="argument disk_encryption_key", value=disk_encryption_key, expected_type=type_hints["disk_encryption_key"])
            check_type(argname="argument key_encryption_key", value=key_encryption_key, expected_type=type_hints["key_encryption_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disk_encryption_key": disk_encryption_key,
        }
        if key_encryption_key is not None:
            self._values["key_encryption_key"] = key_encryption_key

    @builtins.property
    def disk_encryption_key(self) -> "ManagedDiskEncryptionSettingsDiskEncryptionKey":
        '''disk_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#disk_encryption_key ManagedDisk#disk_encryption_key}
        '''
        result = self._values.get("disk_encryption_key")
        assert result is not None, "Required property 'disk_encryption_key' is missing"
        return typing.cast("ManagedDiskEncryptionSettingsDiskEncryptionKey", result)

    @builtins.property
    def key_encryption_key(
        self,
    ) -> typing.Optional["ManagedDiskEncryptionSettingsKeyEncryptionKey"]:
        '''key_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#key_encryption_key ManagedDisk#key_encryption_key}
        '''
        result = self._values.get("key_encryption_key")
        return typing.cast(typing.Optional["ManagedDiskEncryptionSettingsKeyEncryptionKey"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedDiskEncryptionSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.managedDisk.ManagedDiskEncryptionSettingsDiskEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={"secret_url": "secretUrl", "source_vault_id": "sourceVaultId"},
)
class ManagedDiskEncryptionSettingsDiskEncryptionKey:
    def __init__(
        self,
        *,
        secret_url: builtins.str,
        source_vault_id: builtins.str,
    ) -> None:
        '''
        :param secret_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#secret_url ManagedDisk#secret_url}.
        :param source_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#source_vault_id ManagedDisk#source_vault_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20423e145772e308dabd944cc5e305b38bf916975f94c8a6554054be945c37cd)
            check_type(argname="argument secret_url", value=secret_url, expected_type=type_hints["secret_url"])
            check_type(argname="argument source_vault_id", value=source_vault_id, expected_type=type_hints["source_vault_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_url": secret_url,
            "source_vault_id": source_vault_id,
        }

    @builtins.property
    def secret_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#secret_url ManagedDisk#secret_url}.'''
        result = self._values.get("secret_url")
        assert result is not None, "Required property 'secret_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_vault_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#source_vault_id ManagedDisk#source_vault_id}.'''
        result = self._values.get("source_vault_id")
        assert result is not None, "Required property 'source_vault_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedDiskEncryptionSettingsDiskEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ManagedDiskEncryptionSettingsDiskEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.managedDisk.ManagedDiskEncryptionSettingsDiskEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3df6775d2f31ca0a6d9855ed7a92b1e7c57df7acd00bc50ef1d00ddf8d53f96f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretUrlInput")
    def secret_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceVaultIdInput")
    def source_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="secretUrl")
    def secret_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretUrl"))

    @secret_url.setter
    def secret_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc2fca080e4a8745af876660acf7bcc69876160055f1348fbc539bc912586be6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceVaultId")
    def source_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceVaultId"))

    @source_vault_id.setter
    def source_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e1af33cebd030f538e6d75b8937c0d87c3af2f92c99e84eb73bf17f3b048856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ManagedDiskEncryptionSettingsDiskEncryptionKey]:
        return typing.cast(typing.Optional[ManagedDiskEncryptionSettingsDiskEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ManagedDiskEncryptionSettingsDiskEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a5579e34efe24b5d2e3273df45991eeb6f5ca1652aa66e9e20a686ce658e3b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.managedDisk.ManagedDiskEncryptionSettingsKeyEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={"key_url": "keyUrl", "source_vault_id": "sourceVaultId"},
)
class ManagedDiskEncryptionSettingsKeyEncryptionKey:
    def __init__(self, *, key_url: builtins.str, source_vault_id: builtins.str) -> None:
        '''
        :param key_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#key_url ManagedDisk#key_url}.
        :param source_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#source_vault_id ManagedDisk#source_vault_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b85553bec70aee0347e11974bbdf8f61ba3684c2ef3f9597537ffde9981fd23c)
            check_type(argname="argument key_url", value=key_url, expected_type=type_hints["key_url"])
            check_type(argname="argument source_vault_id", value=source_vault_id, expected_type=type_hints["source_vault_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_url": key_url,
            "source_vault_id": source_vault_id,
        }

    @builtins.property
    def key_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#key_url ManagedDisk#key_url}.'''
        result = self._values.get("key_url")
        assert result is not None, "Required property 'key_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_vault_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#source_vault_id ManagedDisk#source_vault_id}.'''
        result = self._values.get("source_vault_id")
        assert result is not None, "Required property 'source_vault_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedDiskEncryptionSettingsKeyEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ManagedDiskEncryptionSettingsKeyEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.managedDisk.ManagedDiskEncryptionSettingsKeyEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0be97e191e9cf7e4eab1024fb8814aadbdbf5255e1c522824ea2ea8f3dec51c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyUrlInput")
    def key_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceVaultIdInput")
    def source_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyUrl")
    def key_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyUrl"))

    @key_url.setter
    def key_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f97975e624c9faddd38bf7a427f99c94c9608c2e7a1abca2c6ae981354e9660b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceVaultId")
    def source_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceVaultId"))

    @source_vault_id.setter
    def source_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__948cb7652f78ae10b8bf7c31a00d91249329ff89afcd7ed25d15f8ac3bd6da04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ManagedDiskEncryptionSettingsKeyEncryptionKey]:
        return typing.cast(typing.Optional[ManagedDiskEncryptionSettingsKeyEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ManagedDiskEncryptionSettingsKeyEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e361e1bb35f4f6120a4d6d4b22f00cb497ab235d6e63ffef50c3c822a0eb38b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ManagedDiskEncryptionSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.managedDisk.ManagedDiskEncryptionSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68cca702a624401318fdda309ffdb12887ab5b8c3f35d4b1c173db0ddaf8da3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDiskEncryptionKey")
    def put_disk_encryption_key(
        self,
        *,
        secret_url: builtins.str,
        source_vault_id: builtins.str,
    ) -> None:
        '''
        :param secret_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#secret_url ManagedDisk#secret_url}.
        :param source_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#source_vault_id ManagedDisk#source_vault_id}.
        '''
        value = ManagedDiskEncryptionSettingsDiskEncryptionKey(
            secret_url=secret_url, source_vault_id=source_vault_id
        )

        return typing.cast(None, jsii.invoke(self, "putDiskEncryptionKey", [value]))

    @jsii.member(jsii_name="putKeyEncryptionKey")
    def put_key_encryption_key(
        self,
        *,
        key_url: builtins.str,
        source_vault_id: builtins.str,
    ) -> None:
        '''
        :param key_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#key_url ManagedDisk#key_url}.
        :param source_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#source_vault_id ManagedDisk#source_vault_id}.
        '''
        value = ManagedDiskEncryptionSettingsKeyEncryptionKey(
            key_url=key_url, source_vault_id=source_vault_id
        )

        return typing.cast(None, jsii.invoke(self, "putKeyEncryptionKey", [value]))

    @jsii.member(jsii_name="resetKeyEncryptionKey")
    def reset_key_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyEncryptionKey", []))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKey")
    def disk_encryption_key(
        self,
    ) -> ManagedDiskEncryptionSettingsDiskEncryptionKeyOutputReference:
        return typing.cast(ManagedDiskEncryptionSettingsDiskEncryptionKeyOutputReference, jsii.get(self, "diskEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="keyEncryptionKey")
    def key_encryption_key(
        self,
    ) -> ManagedDiskEncryptionSettingsKeyEncryptionKeyOutputReference:
        return typing.cast(ManagedDiskEncryptionSettingsKeyEncryptionKeyOutputReference, jsii.get(self, "keyEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeyInput")
    def disk_encryption_key_input(
        self,
    ) -> typing.Optional[ManagedDiskEncryptionSettingsDiskEncryptionKey]:
        return typing.cast(typing.Optional[ManagedDiskEncryptionSettingsDiskEncryptionKey], jsii.get(self, "diskEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="keyEncryptionKeyInput")
    def key_encryption_key_input(
        self,
    ) -> typing.Optional[ManagedDiskEncryptionSettingsKeyEncryptionKey]:
        return typing.cast(typing.Optional[ManagedDiskEncryptionSettingsKeyEncryptionKey], jsii.get(self, "keyEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ManagedDiskEncryptionSettings]:
        return typing.cast(typing.Optional[ManagedDiskEncryptionSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ManagedDiskEncryptionSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb16f9dfe59c7f906506ccce05bd29a53f965637577de4f5958223a616082a42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.managedDisk.ManagedDiskTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ManagedDiskTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#create ManagedDisk#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#delete ManagedDisk#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#read ManagedDisk#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#update ManagedDisk#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773c27be63374ebc2566f6b46601dabe637b46bd0b7ca36372da6bee26e06113)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#create ManagedDisk#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#delete ManagedDisk#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#read ManagedDisk#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/managed_disk#update ManagedDisk#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedDiskTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ManagedDiskTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.managedDisk.ManagedDiskTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0720078a46357dcbfcc9ea6430c092c27e17dfb98856ab7bd5a2cdb5fa31011b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e98f52f1086eb4f9918cb9c97225d556c9ce793d286a0b82a37d449d9339f90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71609a437d5305a9b996407e92158eea0cbbb7f72a2ee897fbdb83368b63187c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ca40a6d0a380c52ff6c95c2b293a238ec2afd836c45a7d63b3dd9951c34b2ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__810cee9318ca083923a58b7b78980269c2f2a5b27b57a44ade2676d66591bff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ManagedDiskTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ManagedDiskTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ManagedDiskTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5597a545ac6511a972207b9b5d33603ea12da0c6f4d4dabd5d24fdfbf2e22b35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ManagedDisk",
    "ManagedDiskConfig",
    "ManagedDiskEncryptionSettings",
    "ManagedDiskEncryptionSettingsDiskEncryptionKey",
    "ManagedDiskEncryptionSettingsDiskEncryptionKeyOutputReference",
    "ManagedDiskEncryptionSettingsKeyEncryptionKey",
    "ManagedDiskEncryptionSettingsKeyEncryptionKeyOutputReference",
    "ManagedDiskEncryptionSettingsOutputReference",
    "ManagedDiskTimeouts",
    "ManagedDiskTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__fadb273c20201a8b7700be6b69e6a818c40ccb3a25501ed98b6e8612f0fd8a8f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    create_option: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    storage_account_type: builtins.str,
    disk_access_id: typing.Optional[builtins.str] = None,
    disk_encryption_set_id: typing.Optional[builtins.str] = None,
    disk_iops_read_only: typing.Optional[jsii.Number] = None,
    disk_iops_read_write: typing.Optional[jsii.Number] = None,
    disk_mbps_read_only: typing.Optional[jsii.Number] = None,
    disk_mbps_read_write: typing.Optional[jsii.Number] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    edge_zone: typing.Optional[builtins.str] = None,
    encryption_settings: typing.Optional[typing.Union[ManagedDiskEncryptionSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    gallery_image_reference_id: typing.Optional[builtins.str] = None,
    hyper_v_generation: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_reference_id: typing.Optional[builtins.str] = None,
    logical_sector_size: typing.Optional[jsii.Number] = None,
    max_shares: typing.Optional[jsii.Number] = None,
    network_access_policy: typing.Optional[builtins.str] = None,
    on_demand_bursting_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    optimized_frequent_attach_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    os_type: typing.Optional[builtins.str] = None,
    performance_plus_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secure_vm_disk_encryption_set_id: typing.Optional[builtins.str] = None,
    security_type: typing.Optional[builtins.str] = None,
    source_resource_id: typing.Optional[builtins.str] = None,
    source_uri: typing.Optional[builtins.str] = None,
    storage_account_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tier: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ManagedDiskTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trusted_launch_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    upload_size_bytes: typing.Optional[jsii.Number] = None,
    zone: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__88cf4e1618190ab6d5f156374e7626007e762e5bf95cd9bcd9bb3904fa8b45f8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cffae0eb777d7c8b2174f637af110741aaa262cfbe8c665a85b6c29eac8ec1e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6318b292acd96401a4fcca6cd06520368cc36d7e0849988e719f3a454d6ae02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d596e8720d7ebbdd8f5413736939886516c8f7bc40ecb942032c31e44d2c07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5970e6f2ef6fe9bae0c71e23aef9fc2b35d3adc3ad79a2497a027aec1294847(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8837605941139c76bd30ac350f3feff94420921ef701426a931e1cb8390f07e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18163d92e57c48af6d179f1c72021a4631912d775e6d5419685ed4a070c327f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80606cb4c2d3d3dd7358c69ec8b54b1cd7e273104fc3157f07d4dd63117bcec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd94b16fee19df182cb677f5e4296a8f89b82aee2baadbe240b9b2f974a21cbe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187088e2c7c372cda91b70dfaf1a044da3b9fa441e58cb07642e0cb18469701c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f24f9717f6d126f6e61266549fff9711b416dd8cf8877d23157df70c2df63e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2508046ad09a05ded697f6dc8f34bff1583f7eae84f22210556f4fca6a7c57a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c46fb4b507bf63cab27cf7e378238622f4d3fdfafe634c28967db709ff9f8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7db6721dd337af5d8b5d7f97bf88dc3d090fd38bb57755c4b2d9ff12b8bd4a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6330186b165b7f5e8170914c4b50d674e4bf11d831668c1cbe710d3c9db22e47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80494ca1dec83fae3ca9a03a17f6cd9847fc181efee49cec62bbb980bf7cdfa3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3256c0d84d06eaab0a51d62b3da67bb336bbb06ac01252326635c5316ecf776(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3ffb31cf58cb79c6b01cfe500abe7a7036c2913b0e5a23784aeda2fdf2fb5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91edc5196320deb4a948bad76dc7529c6ebf8bee5e83191d82e285121f124ade(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3985ebc8f48a9f10bc769eb53d8dfdc5073303ac727647456c154d17982cf2c5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e524092c088bda174df18113b6dfdf84b387b2b5ab5f4e65dbde1e843969f0c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a189808ea2e8be1526ae38615c9775197017d8b069c08f7a4b981c5d1c09eae4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42fb3c973f88e471c1ed87f41b90bf2b13f53f5d62998e66c31d83e2e82df54b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca82d39a3b415f4d78bccae4920eac43d01e3954092e6f0c02d9cde03187adf9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f24c9fdb64c4e24327075fe7eff9fc8a36b12ef3dce9b04ebe8569fd9562c45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f6df24406ce512a1559a3594bce3b80a0f0793b7fdefece9c817185abb9d25c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa858d35b1c4b6ecf33a2f005ee5ba11c963a04a734146844005a8d9dd5e69c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f3cbf4ea2362ad94444bac6b1c41c562bba441b5ae44ec5fb26b25867cb824(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96baad71f948e3b2f7876f6b201015f2516e7bb381885b2e8cd4aebba06e43ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50e4f06e901b59eea740a5054a6e4f87138eef1fa6a39d3bdd30ad0f5fd4f21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7551b0dbddbbb25824812a3dfb0fa73dd087c818ee729e535497fa83ced5b11e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d756504fd96347fce8428c63e0d7566237416b2fe5a74e00a71621c6f795564f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be05305320a35c260308b8f7659651e476fd7d74f626c4f4a926025947ad8ff4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58e188230059a97d10a63651086e841d0928ce8a7e41e92c2ac456414898455(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d01d5511b185249dcef90906613f400b45f0095c5ba506f6f5b5623a033dd734(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26cfcc69c5d046bf8692af92a3012a17d1f680c488567a5e7255da49521c909(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a37a5b0622a17eaf7afb7e3c113d9788517026ea809ca1a844d08b006871c992(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    create_option: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    storage_account_type: builtins.str,
    disk_access_id: typing.Optional[builtins.str] = None,
    disk_encryption_set_id: typing.Optional[builtins.str] = None,
    disk_iops_read_only: typing.Optional[jsii.Number] = None,
    disk_iops_read_write: typing.Optional[jsii.Number] = None,
    disk_mbps_read_only: typing.Optional[jsii.Number] = None,
    disk_mbps_read_write: typing.Optional[jsii.Number] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    edge_zone: typing.Optional[builtins.str] = None,
    encryption_settings: typing.Optional[typing.Union[ManagedDiskEncryptionSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    gallery_image_reference_id: typing.Optional[builtins.str] = None,
    hyper_v_generation: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_reference_id: typing.Optional[builtins.str] = None,
    logical_sector_size: typing.Optional[jsii.Number] = None,
    max_shares: typing.Optional[jsii.Number] = None,
    network_access_policy: typing.Optional[builtins.str] = None,
    on_demand_bursting_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    optimized_frequent_attach_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    os_type: typing.Optional[builtins.str] = None,
    performance_plus_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secure_vm_disk_encryption_set_id: typing.Optional[builtins.str] = None,
    security_type: typing.Optional[builtins.str] = None,
    source_resource_id: typing.Optional[builtins.str] = None,
    source_uri: typing.Optional[builtins.str] = None,
    storage_account_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tier: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ManagedDiskTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trusted_launch_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    upload_size_bytes: typing.Optional[jsii.Number] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc527a6cdc3e705ed587e1b1887858b93f03c8873d0c88d1db1f2a5e44fd14d(
    *,
    disk_encryption_key: typing.Union[ManagedDiskEncryptionSettingsDiskEncryptionKey, typing.Dict[builtins.str, typing.Any]],
    key_encryption_key: typing.Optional[typing.Union[ManagedDiskEncryptionSettingsKeyEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20423e145772e308dabd944cc5e305b38bf916975f94c8a6554054be945c37cd(
    *,
    secret_url: builtins.str,
    source_vault_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df6775d2f31ca0a6d9855ed7a92b1e7c57df7acd00bc50ef1d00ddf8d53f96f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2fca080e4a8745af876660acf7bcc69876160055f1348fbc539bc912586be6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1af33cebd030f538e6d75b8937c0d87c3af2f92c99e84eb73bf17f3b048856(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5579e34efe24b5d2e3273df45991eeb6f5ca1652aa66e9e20a686ce658e3b5(
    value: typing.Optional[ManagedDiskEncryptionSettingsDiskEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85553bec70aee0347e11974bbdf8f61ba3684c2ef3f9597537ffde9981fd23c(
    *,
    key_url: builtins.str,
    source_vault_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be97e191e9cf7e4eab1024fb8814aadbdbf5255e1c522824ea2ea8f3dec51c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f97975e624c9faddd38bf7a427f99c94c9608c2e7a1abca2c6ae981354e9660b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__948cb7652f78ae10b8bf7c31a00d91249329ff89afcd7ed25d15f8ac3bd6da04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e361e1bb35f4f6120a4d6d4b22f00cb497ab235d6e63ffef50c3c822a0eb38b8(
    value: typing.Optional[ManagedDiskEncryptionSettingsKeyEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68cca702a624401318fdda309ffdb12887ab5b8c3f35d4b1c173db0ddaf8da3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb16f9dfe59c7f906506ccce05bd29a53f965637577de4f5958223a616082a42(
    value: typing.Optional[ManagedDiskEncryptionSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773c27be63374ebc2566f6b46601dabe637b46bd0b7ca36372da6bee26e06113(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0720078a46357dcbfcc9ea6430c092c27e17dfb98856ab7bd5a2cdb5fa31011b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e98f52f1086eb4f9918cb9c97225d556c9ce793d286a0b82a37d449d9339f90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71609a437d5305a9b996407e92158eea0cbbb7f72a2ee897fbdb83368b63187c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca40a6d0a380c52ff6c95c2b293a238ec2afd836c45a7d63b3dd9951c34b2ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__810cee9318ca083923a58b7b78980269c2f2a5b27b57a44ade2676d66591bff2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5597a545ac6511a972207b9b5d33603ea12da0c6f4d4dabd5d24fdfbf2e22b35(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ManagedDiskTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
