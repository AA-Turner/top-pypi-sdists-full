r'''
# `azurerm_orchestrated_virtual_machine_scale_set`

Refer to the Terraform Registry for docs: [`azurerm_orchestrated_virtual_machine_scale_set`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set).
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


class OrchestratedVirtualMachineScaleSet(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSet",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set azurerm_orchestrated_virtual_machine_scale_set}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        platform_fault_domain_count: jsii.Number,
        resource_group_name: builtins.str,
        additional_capabilities: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetAdditionalCapabilities", typing.Dict[builtins.str, typing.Any]]] = None,
        automatic_instance_repair: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair", typing.Dict[builtins.str, typing.Any]]] = None,
        boot_diagnostics: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetBootDiagnostics", typing.Dict[builtins.str, typing.Any]]] = None,
        capacity_reservation_group_id: typing.Optional[builtins.str] = None,
        data_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetDataDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        eviction_policy: typing.Optional[builtins.str] = None,
        extension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetExtension", typing.Dict[builtins.str, typing.Any]]]]] = None,
        extension_operations_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        extensions_time_budget: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        instances: typing.Optional[jsii.Number] = None,
        license_type: typing.Optional[builtins.str] = None,
        max_bid_price: typing.Optional[jsii.Number] = None,
        network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetNetworkInterface", typing.Dict[builtins.str, typing.Any]]]]] = None,
        os_disk: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetOsDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        os_profile: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetOsProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        plan: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetPlan", typing.Dict[builtins.str, typing.Any]]] = None,
        priority: typing.Optional[builtins.str] = None,
        priority_mix: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetPriorityMix", typing.Dict[builtins.str, typing.Any]]] = None,
        proximity_placement_group_id: typing.Optional[builtins.str] = None,
        rolling_upgrade_policy: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetRollingUpgradePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        single_placement_group: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sku_name: typing.Optional[builtins.str] = None,
        sku_profile: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetSkuProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        source_image_id: typing.Optional[builtins.str] = None,
        source_image_reference: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetSourceImageReference", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_notification: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetTerminationNotification", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_mode: typing.Optional[builtins.str] = None,
        user_data_base64: typing.Optional[builtins.str] = None,
        zone_balance: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set azurerm_orchestrated_virtual_machine_scale_set} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#location OrchestratedVirtualMachineScaleSet#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#name OrchestratedVirtualMachineScaleSet#name}.
        :param platform_fault_domain_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#platform_fault_domain_count OrchestratedVirtualMachineScaleSet#platform_fault_domain_count}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#resource_group_name OrchestratedVirtualMachineScaleSet#resource_group_name}.
        :param additional_capabilities: additional_capabilities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#additional_capabilities OrchestratedVirtualMachineScaleSet#additional_capabilities}
        :param automatic_instance_repair: automatic_instance_repair block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#automatic_instance_repair OrchestratedVirtualMachineScaleSet#automatic_instance_repair}
        :param boot_diagnostics: boot_diagnostics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#boot_diagnostics OrchestratedVirtualMachineScaleSet#boot_diagnostics}
        :param capacity_reservation_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#capacity_reservation_group_id OrchestratedVirtualMachineScaleSet#capacity_reservation_group_id}.
        :param data_disk: data_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#data_disk OrchestratedVirtualMachineScaleSet#data_disk}
        :param encryption_at_host_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#encryption_at_host_enabled OrchestratedVirtualMachineScaleSet#encryption_at_host_enabled}.
        :param eviction_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#eviction_policy OrchestratedVirtualMachineScaleSet#eviction_policy}.
        :param extension: extension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#extension OrchestratedVirtualMachineScaleSet#extension}
        :param extension_operations_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#extension_operations_enabled OrchestratedVirtualMachineScaleSet#extension_operations_enabled}.
        :param extensions_time_budget: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#extensions_time_budget OrchestratedVirtualMachineScaleSet#extensions_time_budget}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#id OrchestratedVirtualMachineScaleSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#identity OrchestratedVirtualMachineScaleSet#identity}
        :param instances: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#instances OrchestratedVirtualMachineScaleSet#instances}.
        :param license_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#license_type OrchestratedVirtualMachineScaleSet#license_type}.
        :param max_bid_price: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#max_bid_price OrchestratedVirtualMachineScaleSet#max_bid_price}.
        :param network_interface: network_interface block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#network_interface OrchestratedVirtualMachineScaleSet#network_interface}
        :param os_disk: os_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#os_disk OrchestratedVirtualMachineScaleSet#os_disk}
        :param os_profile: os_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#os_profile OrchestratedVirtualMachineScaleSet#os_profile}
        :param plan: plan block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#plan OrchestratedVirtualMachineScaleSet#plan}
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#priority OrchestratedVirtualMachineScaleSet#priority}.
        :param priority_mix: priority_mix block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#priority_mix OrchestratedVirtualMachineScaleSet#priority_mix}
        :param proximity_placement_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#proximity_placement_group_id OrchestratedVirtualMachineScaleSet#proximity_placement_group_id}.
        :param rolling_upgrade_policy: rolling_upgrade_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#rolling_upgrade_policy OrchestratedVirtualMachineScaleSet#rolling_upgrade_policy}
        :param single_placement_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#single_placement_group OrchestratedVirtualMachineScaleSet#single_placement_group}.
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#sku_name OrchestratedVirtualMachineScaleSet#sku_name}.
        :param sku_profile: sku_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#sku_profile OrchestratedVirtualMachineScaleSet#sku_profile}
        :param source_image_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#source_image_id OrchestratedVirtualMachineScaleSet#source_image_id}.
        :param source_image_reference: source_image_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#source_image_reference OrchestratedVirtualMachineScaleSet#source_image_reference}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#tags OrchestratedVirtualMachineScaleSet#tags}.
        :param termination_notification: termination_notification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#termination_notification OrchestratedVirtualMachineScaleSet#termination_notification}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#timeouts OrchestratedVirtualMachineScaleSet#timeouts}
        :param upgrade_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#upgrade_mode OrchestratedVirtualMachineScaleSet#upgrade_mode}.
        :param user_data_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#user_data_base64 OrchestratedVirtualMachineScaleSet#user_data_base64}.
        :param zone_balance: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#zone_balance OrchestratedVirtualMachineScaleSet#zone_balance}.
        :param zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#zones OrchestratedVirtualMachineScaleSet#zones}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd134486e9eea1733710a1ad9b3371fb284f2bbb6d5dddb862feee8176b9d2e5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OrchestratedVirtualMachineScaleSetConfig(
            location=location,
            name=name,
            platform_fault_domain_count=platform_fault_domain_count,
            resource_group_name=resource_group_name,
            additional_capabilities=additional_capabilities,
            automatic_instance_repair=automatic_instance_repair,
            boot_diagnostics=boot_diagnostics,
            capacity_reservation_group_id=capacity_reservation_group_id,
            data_disk=data_disk,
            encryption_at_host_enabled=encryption_at_host_enabled,
            eviction_policy=eviction_policy,
            extension=extension,
            extension_operations_enabled=extension_operations_enabled,
            extensions_time_budget=extensions_time_budget,
            id=id,
            identity=identity,
            instances=instances,
            license_type=license_type,
            max_bid_price=max_bid_price,
            network_interface=network_interface,
            os_disk=os_disk,
            os_profile=os_profile,
            plan=plan,
            priority=priority,
            priority_mix=priority_mix,
            proximity_placement_group_id=proximity_placement_group_id,
            rolling_upgrade_policy=rolling_upgrade_policy,
            single_placement_group=single_placement_group,
            sku_name=sku_name,
            sku_profile=sku_profile,
            source_image_id=source_image_id,
            source_image_reference=source_image_reference,
            tags=tags,
            termination_notification=termination_notification,
            timeouts=timeouts,
            upgrade_mode=upgrade_mode,
            user_data_base64=user_data_base64,
            zone_balance=zone_balance,
            zones=zones,
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
        '''Generates CDKTF code for importing a OrchestratedVirtualMachineScaleSet resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OrchestratedVirtualMachineScaleSet to import.
        :param import_from_id: The id of the existing OrchestratedVirtualMachineScaleSet that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OrchestratedVirtualMachineScaleSet to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce22f67369d675014b04b83ecdeb94876d3dfe53d699d1d3228614e3331bf080)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdditionalCapabilities")
    def put_additional_capabilities(
        self,
        *,
        ultra_ssd_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param ultra_ssd_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#ultra_ssd_enabled OrchestratedVirtualMachineScaleSet#ultra_ssd_enabled}.
        '''
        value = OrchestratedVirtualMachineScaleSetAdditionalCapabilities(
            ultra_ssd_enabled=ultra_ssd_enabled
        )

        return typing.cast(None, jsii.invoke(self, "putAdditionalCapabilities", [value]))

    @jsii.member(jsii_name="putAutomaticInstanceRepair")
    def put_automatic_instance_repair(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        action: typing.Optional[builtins.str] = None,
        grace_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#enabled OrchestratedVirtualMachineScaleSet#enabled}.
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#action OrchestratedVirtualMachineScaleSet#action}.
        :param grace_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#grace_period OrchestratedVirtualMachineScaleSet#grace_period}.
        '''
        value = OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair(
            enabled=enabled, action=action, grace_period=grace_period
        )

        return typing.cast(None, jsii.invoke(self, "putAutomaticInstanceRepair", [value]))

    @jsii.member(jsii_name="putBootDiagnostics")
    def put_boot_diagnostics(
        self,
        *,
        storage_account_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param storage_account_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#storage_account_uri OrchestratedVirtualMachineScaleSet#storage_account_uri}.
        '''
        value = OrchestratedVirtualMachineScaleSetBootDiagnostics(
            storage_account_uri=storage_account_uri
        )

        return typing.cast(None, jsii.invoke(self, "putBootDiagnostics", [value]))

    @jsii.member(jsii_name="putDataDisk")
    def put_data_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetDataDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5de5c17225494ab626364f2f0ebc184a341c157c6eeac32f172a314f0b5c9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataDisk", [value]))

    @jsii.member(jsii_name="putExtension")
    def put_extension(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetExtension", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d68feae112eaa798000ba2554c32a555540e2f783258fa45d0d72a0bae9366)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtension", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        identity_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#identity_ids OrchestratedVirtualMachineScaleSet#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#type OrchestratedVirtualMachineScaleSet#type}.
        '''
        value = OrchestratedVirtualMachineScaleSetIdentity(
            identity_ids=identity_ids, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putNetworkInterface")
    def put_network_interface(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetNetworkInterface", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f24fc99ec3fb45bea7dda5ce573a551f1336fe2298c2e835706f19cc3156328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkInterface", [value]))

    @jsii.member(jsii_name="putOsDisk")
    def put_os_disk(
        self,
        *,
        caching: builtins.str,
        storage_account_type: builtins.str,
        diff_disk_settings: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_encryption_set_id: typing.Optional[builtins.str] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        write_accelerator_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param caching: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#caching OrchestratedVirtualMachineScaleSet#caching}.
        :param storage_account_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#storage_account_type OrchestratedVirtualMachineScaleSet#storage_account_type}.
        :param diff_disk_settings: diff_disk_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#diff_disk_settings OrchestratedVirtualMachineScaleSet#diff_disk_settings}
        :param disk_encryption_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#disk_encryption_set_id OrchestratedVirtualMachineScaleSet#disk_encryption_set_id}.
        :param disk_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#disk_size_gb OrchestratedVirtualMachineScaleSet#disk_size_gb}.
        :param write_accelerator_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#write_accelerator_enabled OrchestratedVirtualMachineScaleSet#write_accelerator_enabled}.
        '''
        value = OrchestratedVirtualMachineScaleSetOsDisk(
            caching=caching,
            storage_account_type=storage_account_type,
            diff_disk_settings=diff_disk_settings,
            disk_encryption_set_id=disk_encryption_set_id,
            disk_size_gb=disk_size_gb,
            write_accelerator_enabled=write_accelerator_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putOsDisk", [value]))

    @jsii.member(jsii_name="putOsProfile")
    def put_os_profile(
        self,
        *,
        custom_data: typing.Optional[builtins.str] = None,
        linux_configuration: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetOsProfileLinuxConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        windows_configuration: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#custom_data OrchestratedVirtualMachineScaleSet#custom_data}.
        :param linux_configuration: linux_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#linux_configuration OrchestratedVirtualMachineScaleSet#linux_configuration}
        :param windows_configuration: windows_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#windows_configuration OrchestratedVirtualMachineScaleSet#windows_configuration}
        '''
        value = OrchestratedVirtualMachineScaleSetOsProfile(
            custom_data=custom_data,
            linux_configuration=linux_configuration,
            windows_configuration=windows_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putOsProfile", [value]))

    @jsii.member(jsii_name="putPlan")
    def put_plan(
        self,
        *,
        name: builtins.str,
        product: builtins.str,
        publisher: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#name OrchestratedVirtualMachineScaleSet#name}.
        :param product: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#product OrchestratedVirtualMachineScaleSet#product}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#publisher OrchestratedVirtualMachineScaleSet#publisher}.
        '''
        value = OrchestratedVirtualMachineScaleSetPlan(
            name=name, product=product, publisher=publisher
        )

        return typing.cast(None, jsii.invoke(self, "putPlan", [value]))

    @jsii.member(jsii_name="putPriorityMix")
    def put_priority_mix(
        self,
        *,
        base_regular_count: typing.Optional[jsii.Number] = None,
        regular_percentage_above_base: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param base_regular_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#base_regular_count OrchestratedVirtualMachineScaleSet#base_regular_count}.
        :param regular_percentage_above_base: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#regular_percentage_above_base OrchestratedVirtualMachineScaleSet#regular_percentage_above_base}.
        '''
        value = OrchestratedVirtualMachineScaleSetPriorityMix(
            base_regular_count=base_regular_count,
            regular_percentage_above_base=regular_percentage_above_base,
        )

        return typing.cast(None, jsii.invoke(self, "putPriorityMix", [value]))

    @jsii.member(jsii_name="putRollingUpgradePolicy")
    def put_rolling_upgrade_policy(
        self,
        *,
        max_batch_instance_percent: jsii.Number,
        max_unhealthy_instance_percent: jsii.Number,
        max_unhealthy_upgraded_instance_percent: jsii.Number,
        pause_time_between_batches: builtins.str,
        cross_zone_upgrades_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        maximum_surge_instances_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prioritize_unhealthy_instances_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param max_batch_instance_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#max_batch_instance_percent OrchestratedVirtualMachineScaleSet#max_batch_instance_percent}.
        :param max_unhealthy_instance_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#max_unhealthy_instance_percent OrchestratedVirtualMachineScaleSet#max_unhealthy_instance_percent}.
        :param max_unhealthy_upgraded_instance_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#max_unhealthy_upgraded_instance_percent OrchestratedVirtualMachineScaleSet#max_unhealthy_upgraded_instance_percent}.
        :param pause_time_between_batches: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#pause_time_between_batches OrchestratedVirtualMachineScaleSet#pause_time_between_batches}.
        :param cross_zone_upgrades_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#cross_zone_upgrades_enabled OrchestratedVirtualMachineScaleSet#cross_zone_upgrades_enabled}.
        :param maximum_surge_instances_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#maximum_surge_instances_enabled OrchestratedVirtualMachineScaleSet#maximum_surge_instances_enabled}.
        :param prioritize_unhealthy_instances_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#prioritize_unhealthy_instances_enabled OrchestratedVirtualMachineScaleSet#prioritize_unhealthy_instances_enabled}.
        '''
        value = OrchestratedVirtualMachineScaleSetRollingUpgradePolicy(
            max_batch_instance_percent=max_batch_instance_percent,
            max_unhealthy_instance_percent=max_unhealthy_instance_percent,
            max_unhealthy_upgraded_instance_percent=max_unhealthy_upgraded_instance_percent,
            pause_time_between_batches=pause_time_between_batches,
            cross_zone_upgrades_enabled=cross_zone_upgrades_enabled,
            maximum_surge_instances_enabled=maximum_surge_instances_enabled,
            prioritize_unhealthy_instances_enabled=prioritize_unhealthy_instances_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putRollingUpgradePolicy", [value]))

    @jsii.member(jsii_name="putSkuProfile")
    def put_sku_profile(
        self,
        *,
        allocation_strategy: builtins.str,
        vm_sizes: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param allocation_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#allocation_strategy OrchestratedVirtualMachineScaleSet#allocation_strategy}.
        :param vm_sizes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#vm_sizes OrchestratedVirtualMachineScaleSet#vm_sizes}.
        '''
        value = OrchestratedVirtualMachineScaleSetSkuProfile(
            allocation_strategy=allocation_strategy, vm_sizes=vm_sizes
        )

        return typing.cast(None, jsii.invoke(self, "putSkuProfile", [value]))

    @jsii.member(jsii_name="putSourceImageReference")
    def put_source_image_reference(
        self,
        *,
        offer: builtins.str,
        publisher: builtins.str,
        sku: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param offer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#offer OrchestratedVirtualMachineScaleSet#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#publisher OrchestratedVirtualMachineScaleSet#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#sku OrchestratedVirtualMachineScaleSet#sku}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#version OrchestratedVirtualMachineScaleSet#version}.
        '''
        value = OrchestratedVirtualMachineScaleSetSourceImageReference(
            offer=offer, publisher=publisher, sku=sku, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putSourceImageReference", [value]))

    @jsii.member(jsii_name="putTerminationNotification")
    def put_termination_notification(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#enabled OrchestratedVirtualMachineScaleSet#enabled}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#timeout OrchestratedVirtualMachineScaleSet#timeout}.
        '''
        value = OrchestratedVirtualMachineScaleSetTerminationNotification(
            enabled=enabled, timeout=timeout
        )

        return typing.cast(None, jsii.invoke(self, "putTerminationNotification", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#create OrchestratedVirtualMachineScaleSet#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#delete OrchestratedVirtualMachineScaleSet#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#read OrchestratedVirtualMachineScaleSet#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#update OrchestratedVirtualMachineScaleSet#update}.
        '''
        value = OrchestratedVirtualMachineScaleSetTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdditionalCapabilities")
    def reset_additional_capabilities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalCapabilities", []))

    @jsii.member(jsii_name="resetAutomaticInstanceRepair")
    def reset_automatic_instance_repair(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomaticInstanceRepair", []))

    @jsii.member(jsii_name="resetBootDiagnostics")
    def reset_boot_diagnostics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiagnostics", []))

    @jsii.member(jsii_name="resetCapacityReservationGroupId")
    def reset_capacity_reservation_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacityReservationGroupId", []))

    @jsii.member(jsii_name="resetDataDisk")
    def reset_data_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataDisk", []))

    @jsii.member(jsii_name="resetEncryptionAtHostEnabled")
    def reset_encryption_at_host_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionAtHostEnabled", []))

    @jsii.member(jsii_name="resetEvictionPolicy")
    def reset_eviction_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvictionPolicy", []))

    @jsii.member(jsii_name="resetExtension")
    def reset_extension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtension", []))

    @jsii.member(jsii_name="resetExtensionOperationsEnabled")
    def reset_extension_operations_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtensionOperationsEnabled", []))

    @jsii.member(jsii_name="resetExtensionsTimeBudget")
    def reset_extensions_time_budget(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtensionsTimeBudget", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetInstances")
    def reset_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstances", []))

    @jsii.member(jsii_name="resetLicenseType")
    def reset_license_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicenseType", []))

    @jsii.member(jsii_name="resetMaxBidPrice")
    def reset_max_bid_price(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxBidPrice", []))

    @jsii.member(jsii_name="resetNetworkInterface")
    def reset_network_interface(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkInterface", []))

    @jsii.member(jsii_name="resetOsDisk")
    def reset_os_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsDisk", []))

    @jsii.member(jsii_name="resetOsProfile")
    def reset_os_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsProfile", []))

    @jsii.member(jsii_name="resetPlan")
    def reset_plan(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlan", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetPriorityMix")
    def reset_priority_mix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriorityMix", []))

    @jsii.member(jsii_name="resetProximityPlacementGroupId")
    def reset_proximity_placement_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProximityPlacementGroupId", []))

    @jsii.member(jsii_name="resetRollingUpgradePolicy")
    def reset_rolling_upgrade_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRollingUpgradePolicy", []))

    @jsii.member(jsii_name="resetSinglePlacementGroup")
    def reset_single_placement_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSinglePlacementGroup", []))

    @jsii.member(jsii_name="resetSkuName")
    def reset_sku_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkuName", []))

    @jsii.member(jsii_name="resetSkuProfile")
    def reset_sku_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkuProfile", []))

    @jsii.member(jsii_name="resetSourceImageId")
    def reset_source_image_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceImageId", []))

    @jsii.member(jsii_name="resetSourceImageReference")
    def reset_source_image_reference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceImageReference", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTerminationNotification")
    def reset_termination_notification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminationNotification", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUpgradeMode")
    def reset_upgrade_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpgradeMode", []))

    @jsii.member(jsii_name="resetUserDataBase64")
    def reset_user_data_base64(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserDataBase64", []))

    @jsii.member(jsii_name="resetZoneBalance")
    def reset_zone_balance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneBalance", []))

    @jsii.member(jsii_name="resetZones")
    def reset_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZones", []))

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
    @jsii.member(jsii_name="additionalCapabilities")
    def additional_capabilities(
        self,
    ) -> "OrchestratedVirtualMachineScaleSetAdditionalCapabilitiesOutputReference":
        return typing.cast("OrchestratedVirtualMachineScaleSetAdditionalCapabilitiesOutputReference", jsii.get(self, "additionalCapabilities"))

    @builtins.property
    @jsii.member(jsii_name="automaticInstanceRepair")
    def automatic_instance_repair(
        self,
    ) -> "OrchestratedVirtualMachineScaleSetAutomaticInstanceRepairOutputReference":
        return typing.cast("OrchestratedVirtualMachineScaleSetAutomaticInstanceRepairOutputReference", jsii.get(self, "automaticInstanceRepair"))

    @builtins.property
    @jsii.member(jsii_name="bootDiagnostics")
    def boot_diagnostics(
        self,
    ) -> "OrchestratedVirtualMachineScaleSetBootDiagnosticsOutputReference":
        return typing.cast("OrchestratedVirtualMachineScaleSetBootDiagnosticsOutputReference", jsii.get(self, "bootDiagnostics"))

    @builtins.property
    @jsii.member(jsii_name="dataDisk")
    def data_disk(self) -> "OrchestratedVirtualMachineScaleSetDataDiskList":
        return typing.cast("OrchestratedVirtualMachineScaleSetDataDiskList", jsii.get(self, "dataDisk"))

    @builtins.property
    @jsii.member(jsii_name="extension")
    def extension(self) -> "OrchestratedVirtualMachineScaleSetExtensionList":
        return typing.cast("OrchestratedVirtualMachineScaleSetExtensionList", jsii.get(self, "extension"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "OrchestratedVirtualMachineScaleSetIdentityOutputReference":
        return typing.cast("OrchestratedVirtualMachineScaleSetIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="networkInterface")
    def network_interface(
        self,
    ) -> "OrchestratedVirtualMachineScaleSetNetworkInterfaceList":
        return typing.cast("OrchestratedVirtualMachineScaleSetNetworkInterfaceList", jsii.get(self, "networkInterface"))

    @builtins.property
    @jsii.member(jsii_name="osDisk")
    def os_disk(self) -> "OrchestratedVirtualMachineScaleSetOsDiskOutputReference":
        return typing.cast("OrchestratedVirtualMachineScaleSetOsDiskOutputReference", jsii.get(self, "osDisk"))

    @builtins.property
    @jsii.member(jsii_name="osProfile")
    def os_profile(
        self,
    ) -> "OrchestratedVirtualMachineScaleSetOsProfileOutputReference":
        return typing.cast("OrchestratedVirtualMachineScaleSetOsProfileOutputReference", jsii.get(self, "osProfile"))

    @builtins.property
    @jsii.member(jsii_name="plan")
    def plan(self) -> "OrchestratedVirtualMachineScaleSetPlanOutputReference":
        return typing.cast("OrchestratedVirtualMachineScaleSetPlanOutputReference", jsii.get(self, "plan"))

    @builtins.property
    @jsii.member(jsii_name="priorityMix")
    def priority_mix(
        self,
    ) -> "OrchestratedVirtualMachineScaleSetPriorityMixOutputReference":
        return typing.cast("OrchestratedVirtualMachineScaleSetPriorityMixOutputReference", jsii.get(self, "priorityMix"))

    @builtins.property
    @jsii.member(jsii_name="rollingUpgradePolicy")
    def rolling_upgrade_policy(
        self,
    ) -> "OrchestratedVirtualMachineScaleSetRollingUpgradePolicyOutputReference":
        return typing.cast("OrchestratedVirtualMachineScaleSetRollingUpgradePolicyOutputReference", jsii.get(self, "rollingUpgradePolicy"))

    @builtins.property
    @jsii.member(jsii_name="skuProfile")
    def sku_profile(
        self,
    ) -> "OrchestratedVirtualMachineScaleSetSkuProfileOutputReference":
        return typing.cast("OrchestratedVirtualMachineScaleSetSkuProfileOutputReference", jsii.get(self, "skuProfile"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageReference")
    def source_image_reference(
        self,
    ) -> "OrchestratedVirtualMachineScaleSetSourceImageReferenceOutputReference":
        return typing.cast("OrchestratedVirtualMachineScaleSetSourceImageReferenceOutputReference", jsii.get(self, "sourceImageReference"))

    @builtins.property
    @jsii.member(jsii_name="terminationNotification")
    def termination_notification(
        self,
    ) -> "OrchestratedVirtualMachineScaleSetTerminationNotificationOutputReference":
        return typing.cast("OrchestratedVirtualMachineScaleSetTerminationNotificationOutputReference", jsii.get(self, "terminationNotification"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "OrchestratedVirtualMachineScaleSetTimeoutsOutputReference":
        return typing.cast("OrchestratedVirtualMachineScaleSetTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uniqueId"))

    @builtins.property
    @jsii.member(jsii_name="additionalCapabilitiesInput")
    def additional_capabilities_input(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetAdditionalCapabilities"]:
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetAdditionalCapabilities"], jsii.get(self, "additionalCapabilitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="automaticInstanceRepairInput")
    def automatic_instance_repair_input(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair"]:
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair"], jsii.get(self, "automaticInstanceRepairInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiagnosticsInput")
    def boot_diagnostics_input(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetBootDiagnostics"]:
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetBootDiagnostics"], jsii.get(self, "bootDiagnosticsInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityReservationGroupIdInput")
    def capacity_reservation_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "capacityReservationGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDiskInput")
    def data_disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetDataDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetDataDisk"]]], jsii.get(self, "dataDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionAtHostEnabledInput")
    def encryption_at_host_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptionAtHostEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="evictionPolicyInput")
    def eviction_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "evictionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionInput")
    def extension_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetExtension"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetExtension"]]], jsii.get(self, "extensionInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionOperationsEnabledInput")
    def extension_operations_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "extensionOperationsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionsTimeBudgetInput")
    def extensions_time_budget_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extensionsTimeBudgetInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetIdentity"]:
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instancesInput")
    def instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instancesInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseTypeInput")
    def license_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxBidPriceInput")
    def max_bid_price_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBidPriceInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceInput")
    def network_interface_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetNetworkInterface"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetNetworkInterface"]]], jsii.get(self, "networkInterfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="osDiskInput")
    def os_disk_input(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetOsDisk"]:
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetOsDisk"], jsii.get(self, "osDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="osProfileInput")
    def os_profile_input(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetOsProfile"]:
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetOsProfile"], jsii.get(self, "osProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="planInput")
    def plan_input(self) -> typing.Optional["OrchestratedVirtualMachineScaleSetPlan"]:
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetPlan"], jsii.get(self, "planInput"))

    @builtins.property
    @jsii.member(jsii_name="platformFaultDomainCountInput")
    def platform_fault_domain_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "platformFaultDomainCountInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityMixInput")
    def priority_mix_input(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetPriorityMix"]:
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetPriorityMix"], jsii.get(self, "priorityMixInput"))

    @builtins.property
    @jsii.member(jsii_name="proximityPlacementGroupIdInput")
    def proximity_placement_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proximityPlacementGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rollingUpgradePolicyInput")
    def rolling_upgrade_policy_input(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetRollingUpgradePolicy"]:
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetRollingUpgradePolicy"], jsii.get(self, "rollingUpgradePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="singlePlacementGroupInput")
    def single_placement_group_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "singlePlacementGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="skuNameInput")
    def sku_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuNameInput"))

    @builtins.property
    @jsii.member(jsii_name="skuProfileInput")
    def sku_profile_input(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetSkuProfile"]:
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetSkuProfile"], jsii.get(self, "skuProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageIdInput")
    def source_image_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceImageIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageReferenceInput")
    def source_image_reference_input(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetSourceImageReference"]:
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetSourceImageReference"], jsii.get(self, "sourceImageReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="terminationNotificationInput")
    def termination_notification_input(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetTerminationNotification"]:
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetTerminationNotification"], jsii.get(self, "terminationNotificationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OrchestratedVirtualMachineScaleSetTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OrchestratedVirtualMachineScaleSetTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradeModeInput")
    def upgrade_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "upgradeModeInput"))

    @builtins.property
    @jsii.member(jsii_name="userDataBase64Input")
    def user_data_base64_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDataBase64Input"))

    @builtins.property
    @jsii.member(jsii_name="zoneBalanceInput")
    def zone_balance_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "zoneBalanceInput"))

    @builtins.property
    @jsii.member(jsii_name="zonesInput")
    def zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "zonesInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityReservationGroupId")
    def capacity_reservation_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "capacityReservationGroupId"))

    @capacity_reservation_group_id.setter
    def capacity_reservation_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14226bdf55f885eed35158fa9cbf0b6b4686ec5e26aa29a0ce4bf5c4e0c6350d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityReservationGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionAtHostEnabled")
    def encryption_at_host_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encryptionAtHostEnabled"))

    @encryption_at_host_enabled.setter
    def encryption_at_host_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__647856b4a6cc3d676a57689f4d2673b5a94b82188300b655b348568f870bb55c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionAtHostEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="evictionPolicy")
    def eviction_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "evictionPolicy"))

    @eviction_policy.setter
    def eviction_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f3b641d0267eb8675d02cf2ffc3224139184f1d3522dac61fa8a7be2097662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evictionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extensionOperationsEnabled")
    def extension_operations_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "extensionOperationsEnabled"))

    @extension_operations_enabled.setter
    def extension_operations_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da28b9a503930744e4d6f1d6959fbbe246cf678c4cabbced41d618bc7bcd55b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extensionOperationsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extensionsTimeBudget")
    def extensions_time_budget(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extensionsTimeBudget"))

    @extensions_time_budget.setter
    def extensions_time_budget(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__011b33db25aa4be45155c8ce1c260534031d9d691a651b683a00322f015dc135)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extensionsTimeBudget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee7289995d803fef88b77fa209c45754a2bcc16639125e052ebc3c197990080d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instances")
    def instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instances"))

    @instances.setter
    def instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2a48ca653a3e61310bbfdac8ad8712d048841c2e05d2fa6f54852a4c8a268b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="licenseType")
    def license_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseType"))

    @license_type.setter
    def license_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd75caa81ad5d30c639d0ecc20f1662dcef91dfdcabd4e841470e4e69baefd43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ee77803b27621457cfa2a535b90fbb90c23e4aa1c5c6043ce0d3a598a7aea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxBidPrice")
    def max_bid_price(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxBidPrice"))

    @max_bid_price.setter
    def max_bid_price(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc6266b726b6a7837cab8cb45a17503bc6970aa7092ccf98bdebf0b3ad065370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBidPrice", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26f1718a2da33d3fa86ea2512249b2d1363fbdeb9c8107b2387dd66d4eec1007)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="platformFaultDomainCount")
    def platform_fault_domain_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "platformFaultDomainCount"))

    @platform_fault_domain_count.setter
    def platform_fault_domain_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716c59427f0515500fe0e517c2e7ca0e06b3826db1674f5c887e04ae9d2143fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platformFaultDomainCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3518ecc085c9959fff5b01ae51dfe966831f99251a6c5dfc7d2fc999cc8f9f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proximityPlacementGroupId")
    def proximity_placement_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proximityPlacementGroupId"))

    @proximity_placement_group_id.setter
    def proximity_placement_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f71d62a19b040f21304db08d3458928cb94a84cb751668e5c5097fb27321df9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proximityPlacementGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__323cd1b99ef793a997ac65f54a6c31bd79a294b05b5bff0d735584a46c5cce6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="singlePlacementGroup")
    def single_placement_group(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "singlePlacementGroup"))

    @single_placement_group.setter
    def single_placement_group(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49aa2c9e82d5263f1d9928090b6884d6487c6747b5f000e61ae8c9fce4c19519)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "singlePlacementGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skuName")
    def sku_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "skuName"))

    @sku_name.setter
    def sku_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2350d293179c47593f2bfd76c2d822bf81c27057f21e0b12df86fda77114c445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skuName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceImageId")
    def source_image_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceImageId"))

    @source_image_id.setter
    def source_image_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fd4ef20a04a61fbfac4ecef73976402a57e1df891c40bbd43f223bed520b9f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceImageId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0e549815ef23a6c391304a566aec901429288311bd60ef671caa87436530a68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="upgradeMode")
    def upgrade_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "upgradeMode"))

    @upgrade_mode.setter
    def upgrade_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8adb266befe1147edb244f204dba8ec83e9db951015c2be4927f74b2ebe37af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "upgradeMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userDataBase64")
    def user_data_base64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userDataBase64"))

    @user_data_base64.setter
    def user_data_base64(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76da02c86134f24a4d50f175d329ba31fbddd900baf4638c4cbfac31484727e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userDataBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zoneBalance")
    def zone_balance(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "zoneBalance"))

    @zone_balance.setter
    def zone_balance(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b7578b0c1af6acae58e09fe1f9347c2ae6bbd5dba72fb3a1ca2c05098b8fb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneBalance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "zones"))

    @zones.setter
    def zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063b79d7cd130a070821287afece19d01acdf384f023aa4440d5ca4d17114036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zones", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetAdditionalCapabilities",
    jsii_struct_bases=[],
    name_mapping={"ultra_ssd_enabled": "ultraSsdEnabled"},
)
class OrchestratedVirtualMachineScaleSetAdditionalCapabilities:
    def __init__(
        self,
        *,
        ultra_ssd_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param ultra_ssd_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#ultra_ssd_enabled OrchestratedVirtualMachineScaleSet#ultra_ssd_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433e18491c3caca0b3b94cd4132e101f6a47519677c5f1a55a8580935b85af23)
            check_type(argname="argument ultra_ssd_enabled", value=ultra_ssd_enabled, expected_type=type_hints["ultra_ssd_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ultra_ssd_enabled is not None:
            self._values["ultra_ssd_enabled"] = ultra_ssd_enabled

    @builtins.property
    def ultra_ssd_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#ultra_ssd_enabled OrchestratedVirtualMachineScaleSet#ultra_ssd_enabled}.'''
        result = self._values.get("ultra_ssd_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetAdditionalCapabilities(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetAdditionalCapabilitiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetAdditionalCapabilitiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1183583eb02d461fe8ecf48c887946ac1326e42da6348eff6a2835a27a5a6b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUltraSsdEnabled")
    def reset_ultra_ssd_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUltraSsdEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="ultraSsdEnabledInput")
    def ultra_ssd_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ultraSsdEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ultraSsdEnabled")
    def ultra_ssd_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ultraSsdEnabled"))

    @ultra_ssd_enabled.setter
    def ultra_ssd_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6644af3013ac94098965397b682974f087ef58177cc9593e1229f593e1061b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ultraSsdEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetAdditionalCapabilities]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetAdditionalCapabilities], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrchestratedVirtualMachineScaleSetAdditionalCapabilities],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f35a2f9c16bc7daf5ab641a2f2805862d3e464f653be01b056f251c6564d79ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "action": "action",
        "grace_period": "gracePeriod",
    },
)
class OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        action: typing.Optional[builtins.str] = None,
        grace_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#enabled OrchestratedVirtualMachineScaleSet#enabled}.
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#action OrchestratedVirtualMachineScaleSet#action}.
        :param grace_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#grace_period OrchestratedVirtualMachineScaleSet#grace_period}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd8de20577085a936e8deee94a9fd7fb90452737de64fa96e20a82a90654362)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument grace_period", value=grace_period, expected_type=type_hints["grace_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if action is not None:
            self._values["action"] = action
        if grace_period is not None:
            self._values["grace_period"] = grace_period

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#enabled OrchestratedVirtualMachineScaleSet#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#action OrchestratedVirtualMachineScaleSet#action}.'''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grace_period(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#grace_period OrchestratedVirtualMachineScaleSet#grace_period}.'''
        result = self._values.get("grace_period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetAutomaticInstanceRepairOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetAutomaticInstanceRepairOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__368a3c1b86ceff713aedb358fffa75fecde0dc0bfe7b101107cf3127287dd849)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetGracePeriod")
    def reset_grace_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGracePeriod", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="gracePeriodInput")
    def grace_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gracePeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaad2969d653f44891428e60975021aeed9d1dcc282a18546379ac56eb6bbd49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ede52e9cf251a50895c73b508ae414a2b1eae5a69001ac31e173b5929e1da4f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gracePeriod")
    def grace_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gracePeriod"))

    @grace_period.setter
    def grace_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d1fe644fe3503f5f996fd3e18b0e302f93903fd4802d271f3769fe47217842d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gracePeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3641ef2aaa11cf79ef891300f15398b3548521b2001381b45c68abbe297dadce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetBootDiagnostics",
    jsii_struct_bases=[],
    name_mapping={"storage_account_uri": "storageAccountUri"},
)
class OrchestratedVirtualMachineScaleSetBootDiagnostics:
    def __init__(
        self,
        *,
        storage_account_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param storage_account_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#storage_account_uri OrchestratedVirtualMachineScaleSet#storage_account_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4301a129c36033fbffe3a12d7301310968c4b2b40cc4538d614543e1573e20f)
            check_type(argname="argument storage_account_uri", value=storage_account_uri, expected_type=type_hints["storage_account_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if storage_account_uri is not None:
            self._values["storage_account_uri"] = storage_account_uri

    @builtins.property
    def storage_account_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#storage_account_uri OrchestratedVirtualMachineScaleSet#storage_account_uri}.'''
        result = self._values.get("storage_account_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetBootDiagnostics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetBootDiagnosticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetBootDiagnosticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__022b5065d84fa9e0a7f884baf2f8acb583577680582eec092713f7e11e97fda9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetStorageAccountUri")
    def reset_storage_account_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountUri", []))

    @builtins.property
    @jsii.member(jsii_name="storageAccountUriInput")
    def storage_account_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountUriInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountUri")
    def storage_account_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountUri"))

    @storage_account_uri.setter
    def storage_account_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c03ebfd44930bd8a7e338849414919b8d78367350eb102a7cc45586be6f966fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetBootDiagnostics]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetBootDiagnostics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrchestratedVirtualMachineScaleSetBootDiagnostics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94b49f19e054c8f9f6496f2c4b390d3023029daed45abf363a5bfb07cfe381af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "platform_fault_domain_count": "platformFaultDomainCount",
        "resource_group_name": "resourceGroupName",
        "additional_capabilities": "additionalCapabilities",
        "automatic_instance_repair": "automaticInstanceRepair",
        "boot_diagnostics": "bootDiagnostics",
        "capacity_reservation_group_id": "capacityReservationGroupId",
        "data_disk": "dataDisk",
        "encryption_at_host_enabled": "encryptionAtHostEnabled",
        "eviction_policy": "evictionPolicy",
        "extension": "extension",
        "extension_operations_enabled": "extensionOperationsEnabled",
        "extensions_time_budget": "extensionsTimeBudget",
        "id": "id",
        "identity": "identity",
        "instances": "instances",
        "license_type": "licenseType",
        "max_bid_price": "maxBidPrice",
        "network_interface": "networkInterface",
        "os_disk": "osDisk",
        "os_profile": "osProfile",
        "plan": "plan",
        "priority": "priority",
        "priority_mix": "priorityMix",
        "proximity_placement_group_id": "proximityPlacementGroupId",
        "rolling_upgrade_policy": "rollingUpgradePolicy",
        "single_placement_group": "singlePlacementGroup",
        "sku_name": "skuName",
        "sku_profile": "skuProfile",
        "source_image_id": "sourceImageId",
        "source_image_reference": "sourceImageReference",
        "tags": "tags",
        "termination_notification": "terminationNotification",
        "timeouts": "timeouts",
        "upgrade_mode": "upgradeMode",
        "user_data_base64": "userDataBase64",
        "zone_balance": "zoneBalance",
        "zones": "zones",
    },
)
class OrchestratedVirtualMachineScaleSetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        platform_fault_domain_count: jsii.Number,
        resource_group_name: builtins.str,
        additional_capabilities: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetAdditionalCapabilities, typing.Dict[builtins.str, typing.Any]]] = None,
        automatic_instance_repair: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair, typing.Dict[builtins.str, typing.Any]]] = None,
        boot_diagnostics: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetBootDiagnostics, typing.Dict[builtins.str, typing.Any]]] = None,
        capacity_reservation_group_id: typing.Optional[builtins.str] = None,
        data_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetDataDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        eviction_policy: typing.Optional[builtins.str] = None,
        extension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetExtension", typing.Dict[builtins.str, typing.Any]]]]] = None,
        extension_operations_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        extensions_time_budget: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        instances: typing.Optional[jsii.Number] = None,
        license_type: typing.Optional[builtins.str] = None,
        max_bid_price: typing.Optional[jsii.Number] = None,
        network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetNetworkInterface", typing.Dict[builtins.str, typing.Any]]]]] = None,
        os_disk: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetOsDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        os_profile: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetOsProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        plan: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetPlan", typing.Dict[builtins.str, typing.Any]]] = None,
        priority: typing.Optional[builtins.str] = None,
        priority_mix: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetPriorityMix", typing.Dict[builtins.str, typing.Any]]] = None,
        proximity_placement_group_id: typing.Optional[builtins.str] = None,
        rolling_upgrade_policy: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetRollingUpgradePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        single_placement_group: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sku_name: typing.Optional[builtins.str] = None,
        sku_profile: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetSkuProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        source_image_id: typing.Optional[builtins.str] = None,
        source_image_reference: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetSourceImageReference", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_notification: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetTerminationNotification", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_mode: typing.Optional[builtins.str] = None,
        user_data_base64: typing.Optional[builtins.str] = None,
        zone_balance: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#location OrchestratedVirtualMachineScaleSet#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#name OrchestratedVirtualMachineScaleSet#name}.
        :param platform_fault_domain_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#platform_fault_domain_count OrchestratedVirtualMachineScaleSet#platform_fault_domain_count}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#resource_group_name OrchestratedVirtualMachineScaleSet#resource_group_name}.
        :param additional_capabilities: additional_capabilities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#additional_capabilities OrchestratedVirtualMachineScaleSet#additional_capabilities}
        :param automatic_instance_repair: automatic_instance_repair block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#automatic_instance_repair OrchestratedVirtualMachineScaleSet#automatic_instance_repair}
        :param boot_diagnostics: boot_diagnostics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#boot_diagnostics OrchestratedVirtualMachineScaleSet#boot_diagnostics}
        :param capacity_reservation_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#capacity_reservation_group_id OrchestratedVirtualMachineScaleSet#capacity_reservation_group_id}.
        :param data_disk: data_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#data_disk OrchestratedVirtualMachineScaleSet#data_disk}
        :param encryption_at_host_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#encryption_at_host_enabled OrchestratedVirtualMachineScaleSet#encryption_at_host_enabled}.
        :param eviction_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#eviction_policy OrchestratedVirtualMachineScaleSet#eviction_policy}.
        :param extension: extension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#extension OrchestratedVirtualMachineScaleSet#extension}
        :param extension_operations_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#extension_operations_enabled OrchestratedVirtualMachineScaleSet#extension_operations_enabled}.
        :param extensions_time_budget: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#extensions_time_budget OrchestratedVirtualMachineScaleSet#extensions_time_budget}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#id OrchestratedVirtualMachineScaleSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#identity OrchestratedVirtualMachineScaleSet#identity}
        :param instances: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#instances OrchestratedVirtualMachineScaleSet#instances}.
        :param license_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#license_type OrchestratedVirtualMachineScaleSet#license_type}.
        :param max_bid_price: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#max_bid_price OrchestratedVirtualMachineScaleSet#max_bid_price}.
        :param network_interface: network_interface block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#network_interface OrchestratedVirtualMachineScaleSet#network_interface}
        :param os_disk: os_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#os_disk OrchestratedVirtualMachineScaleSet#os_disk}
        :param os_profile: os_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#os_profile OrchestratedVirtualMachineScaleSet#os_profile}
        :param plan: plan block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#plan OrchestratedVirtualMachineScaleSet#plan}
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#priority OrchestratedVirtualMachineScaleSet#priority}.
        :param priority_mix: priority_mix block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#priority_mix OrchestratedVirtualMachineScaleSet#priority_mix}
        :param proximity_placement_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#proximity_placement_group_id OrchestratedVirtualMachineScaleSet#proximity_placement_group_id}.
        :param rolling_upgrade_policy: rolling_upgrade_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#rolling_upgrade_policy OrchestratedVirtualMachineScaleSet#rolling_upgrade_policy}
        :param single_placement_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#single_placement_group OrchestratedVirtualMachineScaleSet#single_placement_group}.
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#sku_name OrchestratedVirtualMachineScaleSet#sku_name}.
        :param sku_profile: sku_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#sku_profile OrchestratedVirtualMachineScaleSet#sku_profile}
        :param source_image_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#source_image_id OrchestratedVirtualMachineScaleSet#source_image_id}.
        :param source_image_reference: source_image_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#source_image_reference OrchestratedVirtualMachineScaleSet#source_image_reference}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#tags OrchestratedVirtualMachineScaleSet#tags}.
        :param termination_notification: termination_notification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#termination_notification OrchestratedVirtualMachineScaleSet#termination_notification}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#timeouts OrchestratedVirtualMachineScaleSet#timeouts}
        :param upgrade_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#upgrade_mode OrchestratedVirtualMachineScaleSet#upgrade_mode}.
        :param user_data_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#user_data_base64 OrchestratedVirtualMachineScaleSet#user_data_base64}.
        :param zone_balance: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#zone_balance OrchestratedVirtualMachineScaleSet#zone_balance}.
        :param zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#zones OrchestratedVirtualMachineScaleSet#zones}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(additional_capabilities, dict):
            additional_capabilities = OrchestratedVirtualMachineScaleSetAdditionalCapabilities(**additional_capabilities)
        if isinstance(automatic_instance_repair, dict):
            automatic_instance_repair = OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair(**automatic_instance_repair)
        if isinstance(boot_diagnostics, dict):
            boot_diagnostics = OrchestratedVirtualMachineScaleSetBootDiagnostics(**boot_diagnostics)
        if isinstance(identity, dict):
            identity = OrchestratedVirtualMachineScaleSetIdentity(**identity)
        if isinstance(os_disk, dict):
            os_disk = OrchestratedVirtualMachineScaleSetOsDisk(**os_disk)
        if isinstance(os_profile, dict):
            os_profile = OrchestratedVirtualMachineScaleSetOsProfile(**os_profile)
        if isinstance(plan, dict):
            plan = OrchestratedVirtualMachineScaleSetPlan(**plan)
        if isinstance(priority_mix, dict):
            priority_mix = OrchestratedVirtualMachineScaleSetPriorityMix(**priority_mix)
        if isinstance(rolling_upgrade_policy, dict):
            rolling_upgrade_policy = OrchestratedVirtualMachineScaleSetRollingUpgradePolicy(**rolling_upgrade_policy)
        if isinstance(sku_profile, dict):
            sku_profile = OrchestratedVirtualMachineScaleSetSkuProfile(**sku_profile)
        if isinstance(source_image_reference, dict):
            source_image_reference = OrchestratedVirtualMachineScaleSetSourceImageReference(**source_image_reference)
        if isinstance(termination_notification, dict):
            termination_notification = OrchestratedVirtualMachineScaleSetTerminationNotification(**termination_notification)
        if isinstance(timeouts, dict):
            timeouts = OrchestratedVirtualMachineScaleSetTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3618a83d9bd003d9eb504271e72a26410e135280507b06c2b6cc3c41e38b4db)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument platform_fault_domain_count", value=platform_fault_domain_count, expected_type=type_hints["platform_fault_domain_count"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument additional_capabilities", value=additional_capabilities, expected_type=type_hints["additional_capabilities"])
            check_type(argname="argument automatic_instance_repair", value=automatic_instance_repair, expected_type=type_hints["automatic_instance_repair"])
            check_type(argname="argument boot_diagnostics", value=boot_diagnostics, expected_type=type_hints["boot_diagnostics"])
            check_type(argname="argument capacity_reservation_group_id", value=capacity_reservation_group_id, expected_type=type_hints["capacity_reservation_group_id"])
            check_type(argname="argument data_disk", value=data_disk, expected_type=type_hints["data_disk"])
            check_type(argname="argument encryption_at_host_enabled", value=encryption_at_host_enabled, expected_type=type_hints["encryption_at_host_enabled"])
            check_type(argname="argument eviction_policy", value=eviction_policy, expected_type=type_hints["eviction_policy"])
            check_type(argname="argument extension", value=extension, expected_type=type_hints["extension"])
            check_type(argname="argument extension_operations_enabled", value=extension_operations_enabled, expected_type=type_hints["extension_operations_enabled"])
            check_type(argname="argument extensions_time_budget", value=extensions_time_budget, expected_type=type_hints["extensions_time_budget"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
            check_type(argname="argument license_type", value=license_type, expected_type=type_hints["license_type"])
            check_type(argname="argument max_bid_price", value=max_bid_price, expected_type=type_hints["max_bid_price"])
            check_type(argname="argument network_interface", value=network_interface, expected_type=type_hints["network_interface"])
            check_type(argname="argument os_disk", value=os_disk, expected_type=type_hints["os_disk"])
            check_type(argname="argument os_profile", value=os_profile, expected_type=type_hints["os_profile"])
            check_type(argname="argument plan", value=plan, expected_type=type_hints["plan"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument priority_mix", value=priority_mix, expected_type=type_hints["priority_mix"])
            check_type(argname="argument proximity_placement_group_id", value=proximity_placement_group_id, expected_type=type_hints["proximity_placement_group_id"])
            check_type(argname="argument rolling_upgrade_policy", value=rolling_upgrade_policy, expected_type=type_hints["rolling_upgrade_policy"])
            check_type(argname="argument single_placement_group", value=single_placement_group, expected_type=type_hints["single_placement_group"])
            check_type(argname="argument sku_name", value=sku_name, expected_type=type_hints["sku_name"])
            check_type(argname="argument sku_profile", value=sku_profile, expected_type=type_hints["sku_profile"])
            check_type(argname="argument source_image_id", value=source_image_id, expected_type=type_hints["source_image_id"])
            check_type(argname="argument source_image_reference", value=source_image_reference, expected_type=type_hints["source_image_reference"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument termination_notification", value=termination_notification, expected_type=type_hints["termination_notification"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument upgrade_mode", value=upgrade_mode, expected_type=type_hints["upgrade_mode"])
            check_type(argname="argument user_data_base64", value=user_data_base64, expected_type=type_hints["user_data_base64"])
            check_type(argname="argument zone_balance", value=zone_balance, expected_type=type_hints["zone_balance"])
            check_type(argname="argument zones", value=zones, expected_type=type_hints["zones"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "platform_fault_domain_count": platform_fault_domain_count,
            "resource_group_name": resource_group_name,
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
        if additional_capabilities is not None:
            self._values["additional_capabilities"] = additional_capabilities
        if automatic_instance_repair is not None:
            self._values["automatic_instance_repair"] = automatic_instance_repair
        if boot_diagnostics is not None:
            self._values["boot_diagnostics"] = boot_diagnostics
        if capacity_reservation_group_id is not None:
            self._values["capacity_reservation_group_id"] = capacity_reservation_group_id
        if data_disk is not None:
            self._values["data_disk"] = data_disk
        if encryption_at_host_enabled is not None:
            self._values["encryption_at_host_enabled"] = encryption_at_host_enabled
        if eviction_policy is not None:
            self._values["eviction_policy"] = eviction_policy
        if extension is not None:
            self._values["extension"] = extension
        if extension_operations_enabled is not None:
            self._values["extension_operations_enabled"] = extension_operations_enabled
        if extensions_time_budget is not None:
            self._values["extensions_time_budget"] = extensions_time_budget
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if instances is not None:
            self._values["instances"] = instances
        if license_type is not None:
            self._values["license_type"] = license_type
        if max_bid_price is not None:
            self._values["max_bid_price"] = max_bid_price
        if network_interface is not None:
            self._values["network_interface"] = network_interface
        if os_disk is not None:
            self._values["os_disk"] = os_disk
        if os_profile is not None:
            self._values["os_profile"] = os_profile
        if plan is not None:
            self._values["plan"] = plan
        if priority is not None:
            self._values["priority"] = priority
        if priority_mix is not None:
            self._values["priority_mix"] = priority_mix
        if proximity_placement_group_id is not None:
            self._values["proximity_placement_group_id"] = proximity_placement_group_id
        if rolling_upgrade_policy is not None:
            self._values["rolling_upgrade_policy"] = rolling_upgrade_policy
        if single_placement_group is not None:
            self._values["single_placement_group"] = single_placement_group
        if sku_name is not None:
            self._values["sku_name"] = sku_name
        if sku_profile is not None:
            self._values["sku_profile"] = sku_profile
        if source_image_id is not None:
            self._values["source_image_id"] = source_image_id
        if source_image_reference is not None:
            self._values["source_image_reference"] = source_image_reference
        if tags is not None:
            self._values["tags"] = tags
        if termination_notification is not None:
            self._values["termination_notification"] = termination_notification
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if upgrade_mode is not None:
            self._values["upgrade_mode"] = upgrade_mode
        if user_data_base64 is not None:
            self._values["user_data_base64"] = user_data_base64
        if zone_balance is not None:
            self._values["zone_balance"] = zone_balance
        if zones is not None:
            self._values["zones"] = zones

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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#location OrchestratedVirtualMachineScaleSet#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#name OrchestratedVirtualMachineScaleSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def platform_fault_domain_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#platform_fault_domain_count OrchestratedVirtualMachineScaleSet#platform_fault_domain_count}.'''
        result = self._values.get("platform_fault_domain_count")
        assert result is not None, "Required property 'platform_fault_domain_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#resource_group_name OrchestratedVirtualMachineScaleSet#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_capabilities(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetAdditionalCapabilities]:
        '''additional_capabilities block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#additional_capabilities OrchestratedVirtualMachineScaleSet#additional_capabilities}
        '''
        result = self._values.get("additional_capabilities")
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetAdditionalCapabilities], result)

    @builtins.property
    def automatic_instance_repair(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair]:
        '''automatic_instance_repair block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#automatic_instance_repair OrchestratedVirtualMachineScaleSet#automatic_instance_repair}
        '''
        result = self._values.get("automatic_instance_repair")
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair], result)

    @builtins.property
    def boot_diagnostics(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetBootDiagnostics]:
        '''boot_diagnostics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#boot_diagnostics OrchestratedVirtualMachineScaleSet#boot_diagnostics}
        '''
        result = self._values.get("boot_diagnostics")
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetBootDiagnostics], result)

    @builtins.property
    def capacity_reservation_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#capacity_reservation_group_id OrchestratedVirtualMachineScaleSet#capacity_reservation_group_id}.'''
        result = self._values.get("capacity_reservation_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetDataDisk"]]]:
        '''data_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#data_disk OrchestratedVirtualMachineScaleSet#data_disk}
        '''
        result = self._values.get("data_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetDataDisk"]]], result)

    @builtins.property
    def encryption_at_host_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#encryption_at_host_enabled OrchestratedVirtualMachineScaleSet#encryption_at_host_enabled}.'''
        result = self._values.get("encryption_at_host_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def eviction_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#eviction_policy OrchestratedVirtualMachineScaleSet#eviction_policy}.'''
        result = self._values.get("eviction_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extension(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetExtension"]]]:
        '''extension block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#extension OrchestratedVirtualMachineScaleSet#extension}
        '''
        result = self._values.get("extension")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetExtension"]]], result)

    @builtins.property
    def extension_operations_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#extension_operations_enabled OrchestratedVirtualMachineScaleSet#extension_operations_enabled}.'''
        result = self._values.get("extension_operations_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def extensions_time_budget(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#extensions_time_budget OrchestratedVirtualMachineScaleSet#extensions_time_budget}.'''
        result = self._values.get("extensions_time_budget")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#id OrchestratedVirtualMachineScaleSet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["OrchestratedVirtualMachineScaleSetIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#identity OrchestratedVirtualMachineScaleSet#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetIdentity"], result)

    @builtins.property
    def instances(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#instances OrchestratedVirtualMachineScaleSet#instances}.'''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def license_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#license_type OrchestratedVirtualMachineScaleSet#license_type}.'''
        result = self._values.get("license_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_bid_price(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#max_bid_price OrchestratedVirtualMachineScaleSet#max_bid_price}.'''
        result = self._values.get("max_bid_price")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network_interface(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetNetworkInterface"]]]:
        '''network_interface block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#network_interface OrchestratedVirtualMachineScaleSet#network_interface}
        '''
        result = self._values.get("network_interface")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetNetworkInterface"]]], result)

    @builtins.property
    def os_disk(self) -> typing.Optional["OrchestratedVirtualMachineScaleSetOsDisk"]:
        '''os_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#os_disk OrchestratedVirtualMachineScaleSet#os_disk}
        '''
        result = self._values.get("os_disk")
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetOsDisk"], result)

    @builtins.property
    def os_profile(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetOsProfile"]:
        '''os_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#os_profile OrchestratedVirtualMachineScaleSet#os_profile}
        '''
        result = self._values.get("os_profile")
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetOsProfile"], result)

    @builtins.property
    def plan(self) -> typing.Optional["OrchestratedVirtualMachineScaleSetPlan"]:
        '''plan block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#plan OrchestratedVirtualMachineScaleSet#plan}
        '''
        result = self._values.get("plan")
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetPlan"], result)

    @builtins.property
    def priority(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#priority OrchestratedVirtualMachineScaleSet#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority_mix(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetPriorityMix"]:
        '''priority_mix block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#priority_mix OrchestratedVirtualMachineScaleSet#priority_mix}
        '''
        result = self._values.get("priority_mix")
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetPriorityMix"], result)

    @builtins.property
    def proximity_placement_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#proximity_placement_group_id OrchestratedVirtualMachineScaleSet#proximity_placement_group_id}.'''
        result = self._values.get("proximity_placement_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rolling_upgrade_policy(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetRollingUpgradePolicy"]:
        '''rolling_upgrade_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#rolling_upgrade_policy OrchestratedVirtualMachineScaleSet#rolling_upgrade_policy}
        '''
        result = self._values.get("rolling_upgrade_policy")
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetRollingUpgradePolicy"], result)

    @builtins.property
    def single_placement_group(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#single_placement_group OrchestratedVirtualMachineScaleSet#single_placement_group}.'''
        result = self._values.get("single_placement_group")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sku_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#sku_name OrchestratedVirtualMachineScaleSet#sku_name}.'''
        result = self._values.get("sku_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sku_profile(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetSkuProfile"]:
        '''sku_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#sku_profile OrchestratedVirtualMachineScaleSet#sku_profile}
        '''
        result = self._values.get("sku_profile")
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetSkuProfile"], result)

    @builtins.property
    def source_image_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#source_image_id OrchestratedVirtualMachineScaleSet#source_image_id}.'''
        result = self._values.get("source_image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_image_reference(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetSourceImageReference"]:
        '''source_image_reference block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#source_image_reference OrchestratedVirtualMachineScaleSet#source_image_reference}
        '''
        result = self._values.get("source_image_reference")
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetSourceImageReference"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#tags OrchestratedVirtualMachineScaleSet#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def termination_notification(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetTerminationNotification"]:
        '''termination_notification block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#termination_notification OrchestratedVirtualMachineScaleSet#termination_notification}
        '''
        result = self._values.get("termination_notification")
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetTerminationNotification"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["OrchestratedVirtualMachineScaleSetTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#timeouts OrchestratedVirtualMachineScaleSet#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetTimeouts"], result)

    @builtins.property
    def upgrade_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#upgrade_mode OrchestratedVirtualMachineScaleSet#upgrade_mode}.'''
        result = self._values.get("upgrade_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_data_base64(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#user_data_base64 OrchestratedVirtualMachineScaleSet#user_data_base64}.'''
        result = self._values.get("user_data_base64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone_balance(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#zone_balance OrchestratedVirtualMachineScaleSet#zone_balance}.'''
        result = self._values.get("zone_balance")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#zones OrchestratedVirtualMachineScaleSet#zones}.'''
        result = self._values.get("zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetDataDisk",
    jsii_struct_bases=[],
    name_mapping={
        "caching": "caching",
        "storage_account_type": "storageAccountType",
        "create_option": "createOption",
        "disk_encryption_set_id": "diskEncryptionSetId",
        "disk_size_gb": "diskSizeGb",
        "lun": "lun",
        "ultra_ssd_disk_iops_read_write": "ultraSsdDiskIopsReadWrite",
        "ultra_ssd_disk_mbps_read_write": "ultraSsdDiskMbpsReadWrite",
        "write_accelerator_enabled": "writeAcceleratorEnabled",
    },
)
class OrchestratedVirtualMachineScaleSetDataDisk:
    def __init__(
        self,
        *,
        caching: builtins.str,
        storage_account_type: builtins.str,
        create_option: typing.Optional[builtins.str] = None,
        disk_encryption_set_id: typing.Optional[builtins.str] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        lun: typing.Optional[jsii.Number] = None,
        ultra_ssd_disk_iops_read_write: typing.Optional[jsii.Number] = None,
        ultra_ssd_disk_mbps_read_write: typing.Optional[jsii.Number] = None,
        write_accelerator_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param caching: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#caching OrchestratedVirtualMachineScaleSet#caching}.
        :param storage_account_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#storage_account_type OrchestratedVirtualMachineScaleSet#storage_account_type}.
        :param create_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#create_option OrchestratedVirtualMachineScaleSet#create_option}.
        :param disk_encryption_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#disk_encryption_set_id OrchestratedVirtualMachineScaleSet#disk_encryption_set_id}.
        :param disk_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#disk_size_gb OrchestratedVirtualMachineScaleSet#disk_size_gb}.
        :param lun: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#lun OrchestratedVirtualMachineScaleSet#lun}.
        :param ultra_ssd_disk_iops_read_write: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#ultra_ssd_disk_iops_read_write OrchestratedVirtualMachineScaleSet#ultra_ssd_disk_iops_read_write}.
        :param ultra_ssd_disk_mbps_read_write: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#ultra_ssd_disk_mbps_read_write OrchestratedVirtualMachineScaleSet#ultra_ssd_disk_mbps_read_write}.
        :param write_accelerator_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#write_accelerator_enabled OrchestratedVirtualMachineScaleSet#write_accelerator_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a714e2df2258705dcbbe01fb1100abacfdd8f5fa612205a70d0e2c3b9e895a4)
            check_type(argname="argument caching", value=caching, expected_type=type_hints["caching"])
            check_type(argname="argument storage_account_type", value=storage_account_type, expected_type=type_hints["storage_account_type"])
            check_type(argname="argument create_option", value=create_option, expected_type=type_hints["create_option"])
            check_type(argname="argument disk_encryption_set_id", value=disk_encryption_set_id, expected_type=type_hints["disk_encryption_set_id"])
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument lun", value=lun, expected_type=type_hints["lun"])
            check_type(argname="argument ultra_ssd_disk_iops_read_write", value=ultra_ssd_disk_iops_read_write, expected_type=type_hints["ultra_ssd_disk_iops_read_write"])
            check_type(argname="argument ultra_ssd_disk_mbps_read_write", value=ultra_ssd_disk_mbps_read_write, expected_type=type_hints["ultra_ssd_disk_mbps_read_write"])
            check_type(argname="argument write_accelerator_enabled", value=write_accelerator_enabled, expected_type=type_hints["write_accelerator_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "caching": caching,
            "storage_account_type": storage_account_type,
        }
        if create_option is not None:
            self._values["create_option"] = create_option
        if disk_encryption_set_id is not None:
            self._values["disk_encryption_set_id"] = disk_encryption_set_id
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if lun is not None:
            self._values["lun"] = lun
        if ultra_ssd_disk_iops_read_write is not None:
            self._values["ultra_ssd_disk_iops_read_write"] = ultra_ssd_disk_iops_read_write
        if ultra_ssd_disk_mbps_read_write is not None:
            self._values["ultra_ssd_disk_mbps_read_write"] = ultra_ssd_disk_mbps_read_write
        if write_accelerator_enabled is not None:
            self._values["write_accelerator_enabled"] = write_accelerator_enabled

    @builtins.property
    def caching(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#caching OrchestratedVirtualMachineScaleSet#caching}.'''
        result = self._values.get("caching")
        assert result is not None, "Required property 'caching' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#storage_account_type OrchestratedVirtualMachineScaleSet#storage_account_type}.'''
        result = self._values.get("storage_account_type")
        assert result is not None, "Required property 'storage_account_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def create_option(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#create_option OrchestratedVirtualMachineScaleSet#create_option}.'''
        result = self._values.get("create_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#disk_encryption_set_id OrchestratedVirtualMachineScaleSet#disk_encryption_set_id}.'''
        result = self._values.get("disk_encryption_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#disk_size_gb OrchestratedVirtualMachineScaleSet#disk_size_gb}.'''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lun(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#lun OrchestratedVirtualMachineScaleSet#lun}.'''
        result = self._values.get("lun")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ultra_ssd_disk_iops_read_write(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#ultra_ssd_disk_iops_read_write OrchestratedVirtualMachineScaleSet#ultra_ssd_disk_iops_read_write}.'''
        result = self._values.get("ultra_ssd_disk_iops_read_write")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ultra_ssd_disk_mbps_read_write(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#ultra_ssd_disk_mbps_read_write OrchestratedVirtualMachineScaleSet#ultra_ssd_disk_mbps_read_write}.'''
        result = self._values.get("ultra_ssd_disk_mbps_read_write")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def write_accelerator_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#write_accelerator_enabled OrchestratedVirtualMachineScaleSet#write_accelerator_enabled}.'''
        result = self._values.get("write_accelerator_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetDataDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetDataDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetDataDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f2efea5d49219b0f6434062205d59a7f177a5e5fb2f53bc1d93ffc773615b62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrchestratedVirtualMachineScaleSetDataDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__341d5207ab740ad37e780a10f7182b8e419a3f8c345345dc283b0531fea004e0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrchestratedVirtualMachineScaleSetDataDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783d035e45a4db7210867b515d8f4f8c84a7d106fd07bc19c8b3e78019f3dcb3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b56433e26aecb5a4618aa16169f7f41a4e49e1fc6fbcf76dae0113cddedd0fa0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__195b29312f2f0b759ebef845de17f8ad67c2651db037b19e752372208a1c11da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetDataDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetDataDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetDataDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0420d2d4e8ea4cea189032278ad2fc69b9c24b4c3c90c17e71f8293724793ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetDataDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetDataDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71e5e614e4c8fbb7e34cd33fd2cf2ca19d98da15d0eafbb67b5adce2557a8e48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCreateOption")
    def reset_create_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateOption", []))

    @jsii.member(jsii_name="resetDiskEncryptionSetId")
    def reset_disk_encryption_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionSetId", []))

    @jsii.member(jsii_name="resetDiskSizeGb")
    def reset_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGb", []))

    @jsii.member(jsii_name="resetLun")
    def reset_lun(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLun", []))

    @jsii.member(jsii_name="resetUltraSsdDiskIopsReadWrite")
    def reset_ultra_ssd_disk_iops_read_write(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUltraSsdDiskIopsReadWrite", []))

    @jsii.member(jsii_name="resetUltraSsdDiskMbpsReadWrite")
    def reset_ultra_ssd_disk_mbps_read_write(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUltraSsdDiskMbpsReadWrite", []))

    @jsii.member(jsii_name="resetWriteAcceleratorEnabled")
    def reset_write_accelerator_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteAcceleratorEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="cachingInput")
    def caching_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cachingInput"))

    @builtins.property
    @jsii.member(jsii_name="createOptionInput")
    def create_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionSetIdInput")
    def disk_encryption_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="lunInput")
    def lun_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lunInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountTypeInput")
    def storage_account_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="ultraSsdDiskIopsReadWriteInput")
    def ultra_ssd_disk_iops_read_write_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ultraSsdDiskIopsReadWriteInput"))

    @builtins.property
    @jsii.member(jsii_name="ultraSsdDiskMbpsReadWriteInput")
    def ultra_ssd_disk_mbps_read_write_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ultraSsdDiskMbpsReadWriteInput"))

    @builtins.property
    @jsii.member(jsii_name="writeAcceleratorEnabledInput")
    def write_accelerator_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "writeAcceleratorEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="caching")
    def caching(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caching"))

    @caching.setter
    def caching(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48f1482b2237e8b47690a5009818716ba687f13733d4bbbcb2605eb322fc7e4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caching", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createOption")
    def create_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createOption"))

    @create_option.setter
    def create_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ceaaf7f6456856dbfcc0349c8d448c5c9ace45515ed62eca19017b066cf700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionSetId")
    def disk_encryption_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionSetId"))

    @disk_encryption_set_id.setter
    def disk_encryption_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6a348080d69648abac7ad08a752595b21948b044dd17703257e04501bacfada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f8b11319949eaedf885253b31b4a47818983b2297fe2f84e30198b20a84e390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lun")
    def lun(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lun"))

    @lun.setter
    def lun(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1db950446fe47b9f3b4ba4f624f9e9e6fc2b171705a2bf570df7ec61d9a5b59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountType")
    def storage_account_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountType"))

    @storage_account_type.setter
    def storage_account_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__846fca0cf7361f927a9a6b0dbc3ce252f09516ee3ea0043258004230997e8f86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ultraSsdDiskIopsReadWrite")
    def ultra_ssd_disk_iops_read_write(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ultraSsdDiskIopsReadWrite"))

    @ultra_ssd_disk_iops_read_write.setter
    def ultra_ssd_disk_iops_read_write(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd5f77c494854ac75944100bdf7ecb92a321b79a6904d3086d2e876a71739f03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ultraSsdDiskIopsReadWrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ultraSsdDiskMbpsReadWrite")
    def ultra_ssd_disk_mbps_read_write(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ultraSsdDiskMbpsReadWrite"))

    @ultra_ssd_disk_mbps_read_write.setter
    def ultra_ssd_disk_mbps_read_write(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c3b54b03b7d1654089e6ad2b4347e8d4d170e1ea2504018096ecd5005ebd461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ultraSsdDiskMbpsReadWrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeAcceleratorEnabled")
    def write_accelerator_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "writeAcceleratorEnabled"))

    @write_accelerator_enabled.setter
    def write_accelerator_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333b43cf0cd633e49f049e612cd22f1ad52b6fc8e26b6c76e410aeb14bc4d905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeAcceleratorEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetDataDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetDataDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetDataDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a557db9cd5a2aafc256cc26554f2051357d049907a3818c73ea81f3f4a535260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetExtension",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "publisher": "publisher",
        "type": "type",
        "type_handler_version": "typeHandlerVersion",
        "auto_upgrade_minor_version_enabled": "autoUpgradeMinorVersionEnabled",
        "extensions_to_provision_after_vm_creation": "extensionsToProvisionAfterVmCreation",
        "failure_suppression_enabled": "failureSuppressionEnabled",
        "force_extension_execution_on_change": "forceExtensionExecutionOnChange",
        "protected_settings": "protectedSettings",
        "protected_settings_from_key_vault": "protectedSettingsFromKeyVault",
        "settings": "settings",
    },
)
class OrchestratedVirtualMachineScaleSetExtension:
    def __init__(
        self,
        *,
        name: builtins.str,
        publisher: builtins.str,
        type: builtins.str,
        type_handler_version: builtins.str,
        auto_upgrade_minor_version_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        extensions_to_provision_after_vm_creation: typing.Optional[typing.Sequence[builtins.str]] = None,
        failure_suppression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        force_extension_execution_on_change: typing.Optional[builtins.str] = None,
        protected_settings: typing.Optional[builtins.str] = None,
        protected_settings_from_key_vault: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVault", typing.Dict[builtins.str, typing.Any]]] = None,
        settings: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#name OrchestratedVirtualMachineScaleSet#name}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#publisher OrchestratedVirtualMachineScaleSet#publisher}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#type OrchestratedVirtualMachineScaleSet#type}.
        :param type_handler_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#type_handler_version OrchestratedVirtualMachineScaleSet#type_handler_version}.
        :param auto_upgrade_minor_version_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#auto_upgrade_minor_version_enabled OrchestratedVirtualMachineScaleSet#auto_upgrade_minor_version_enabled}.
        :param extensions_to_provision_after_vm_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#extensions_to_provision_after_vm_creation OrchestratedVirtualMachineScaleSet#extensions_to_provision_after_vm_creation}.
        :param failure_suppression_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#failure_suppression_enabled OrchestratedVirtualMachineScaleSet#failure_suppression_enabled}.
        :param force_extension_execution_on_change: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#force_extension_execution_on_change OrchestratedVirtualMachineScaleSet#force_extension_execution_on_change}.
        :param protected_settings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#protected_settings OrchestratedVirtualMachineScaleSet#protected_settings}.
        :param protected_settings_from_key_vault: protected_settings_from_key_vault block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#protected_settings_from_key_vault OrchestratedVirtualMachineScaleSet#protected_settings_from_key_vault}
        :param settings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#settings OrchestratedVirtualMachineScaleSet#settings}.
        '''
        if isinstance(protected_settings_from_key_vault, dict):
            protected_settings_from_key_vault = OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVault(**protected_settings_from_key_vault)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7cff06c3e3bb9b387beeb7836f0b6ae51a4ad13597ae9889743caa69ca943eb)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument type_handler_version", value=type_handler_version, expected_type=type_hints["type_handler_version"])
            check_type(argname="argument auto_upgrade_minor_version_enabled", value=auto_upgrade_minor_version_enabled, expected_type=type_hints["auto_upgrade_minor_version_enabled"])
            check_type(argname="argument extensions_to_provision_after_vm_creation", value=extensions_to_provision_after_vm_creation, expected_type=type_hints["extensions_to_provision_after_vm_creation"])
            check_type(argname="argument failure_suppression_enabled", value=failure_suppression_enabled, expected_type=type_hints["failure_suppression_enabled"])
            check_type(argname="argument force_extension_execution_on_change", value=force_extension_execution_on_change, expected_type=type_hints["force_extension_execution_on_change"])
            check_type(argname="argument protected_settings", value=protected_settings, expected_type=type_hints["protected_settings"])
            check_type(argname="argument protected_settings_from_key_vault", value=protected_settings_from_key_vault, expected_type=type_hints["protected_settings_from_key_vault"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "publisher": publisher,
            "type": type,
            "type_handler_version": type_handler_version,
        }
        if auto_upgrade_minor_version_enabled is not None:
            self._values["auto_upgrade_minor_version_enabled"] = auto_upgrade_minor_version_enabled
        if extensions_to_provision_after_vm_creation is not None:
            self._values["extensions_to_provision_after_vm_creation"] = extensions_to_provision_after_vm_creation
        if failure_suppression_enabled is not None:
            self._values["failure_suppression_enabled"] = failure_suppression_enabled
        if force_extension_execution_on_change is not None:
            self._values["force_extension_execution_on_change"] = force_extension_execution_on_change
        if protected_settings is not None:
            self._values["protected_settings"] = protected_settings
        if protected_settings_from_key_vault is not None:
            self._values["protected_settings_from_key_vault"] = protected_settings_from_key_vault
        if settings is not None:
            self._values["settings"] = settings

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#name OrchestratedVirtualMachineScaleSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def publisher(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#publisher OrchestratedVirtualMachineScaleSet#publisher}.'''
        result = self._values.get("publisher")
        assert result is not None, "Required property 'publisher' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#type OrchestratedVirtualMachineScaleSet#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type_handler_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#type_handler_version OrchestratedVirtualMachineScaleSet#type_handler_version}.'''
        result = self._values.get("type_handler_version")
        assert result is not None, "Required property 'type_handler_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_upgrade_minor_version_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#auto_upgrade_minor_version_enabled OrchestratedVirtualMachineScaleSet#auto_upgrade_minor_version_enabled}.'''
        result = self._values.get("auto_upgrade_minor_version_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def extensions_to_provision_after_vm_creation(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#extensions_to_provision_after_vm_creation OrchestratedVirtualMachineScaleSet#extensions_to_provision_after_vm_creation}.'''
        result = self._values.get("extensions_to_provision_after_vm_creation")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def failure_suppression_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#failure_suppression_enabled OrchestratedVirtualMachineScaleSet#failure_suppression_enabled}.'''
        result = self._values.get("failure_suppression_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def force_extension_execution_on_change(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#force_extension_execution_on_change OrchestratedVirtualMachineScaleSet#force_extension_execution_on_change}.'''
        result = self._values.get("force_extension_execution_on_change")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protected_settings(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#protected_settings OrchestratedVirtualMachineScaleSet#protected_settings}.'''
        result = self._values.get("protected_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protected_settings_from_key_vault(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVault"]:
        '''protected_settings_from_key_vault block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#protected_settings_from_key_vault OrchestratedVirtualMachineScaleSet#protected_settings_from_key_vault}
        '''
        result = self._values.get("protected_settings_from_key_vault")
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVault"], result)

    @builtins.property
    def settings(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#settings OrchestratedVirtualMachineScaleSet#settings}.'''
        result = self._values.get("settings")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetExtension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetExtensionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetExtensionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f409adfdb8056a8d9893847cb2f4626d93e7b7ff590501a6375c8283f40442ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrchestratedVirtualMachineScaleSetExtensionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80f987ed450913e2dce79fd3d1c73bc5888ce1b8d0a77e4f9bec60e321a5860f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrchestratedVirtualMachineScaleSetExtensionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b8a8997087b467b297e480d5441a7b7847de86a42a123e9dc48086d99e1a3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b956e97285317d8e3b8dc87092d14537bba14bfd9cc8c4e6d5a6adbb1abab7cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dad7274eb6cb956f1785452cbfcecb070fc5e4242e80c816edd0c15caf1fa34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetExtension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetExtension]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetExtension]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d49e39bed1328875fb80a8e11c161fd2c13ea73bd7eea71cb2f177b342b03a8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetExtensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetExtensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98af37116fdbf54765b43832e59c14820edb18f95931ff6a809ed1a1e35f9305)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putProtectedSettingsFromKeyVault")
    def put_protected_settings_from_key_vault(
        self,
        *,
        secret_url: builtins.str,
        source_vault_id: builtins.str,
    ) -> None:
        '''
        :param secret_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#secret_url OrchestratedVirtualMachineScaleSet#secret_url}.
        :param source_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#source_vault_id OrchestratedVirtualMachineScaleSet#source_vault_id}.
        '''
        value = OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVault(
            secret_url=secret_url, source_vault_id=source_vault_id
        )

        return typing.cast(None, jsii.invoke(self, "putProtectedSettingsFromKeyVault", [value]))

    @jsii.member(jsii_name="resetAutoUpgradeMinorVersionEnabled")
    def reset_auto_upgrade_minor_version_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoUpgradeMinorVersionEnabled", []))

    @jsii.member(jsii_name="resetExtensionsToProvisionAfterVmCreation")
    def reset_extensions_to_provision_after_vm_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtensionsToProvisionAfterVmCreation", []))

    @jsii.member(jsii_name="resetFailureSuppressionEnabled")
    def reset_failure_suppression_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureSuppressionEnabled", []))

    @jsii.member(jsii_name="resetForceExtensionExecutionOnChange")
    def reset_force_extension_execution_on_change(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceExtensionExecutionOnChange", []))

    @jsii.member(jsii_name="resetProtectedSettings")
    def reset_protected_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtectedSettings", []))

    @jsii.member(jsii_name="resetProtectedSettingsFromKeyVault")
    def reset_protected_settings_from_key_vault(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtectedSettingsFromKeyVault", []))

    @jsii.member(jsii_name="resetSettings")
    def reset_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSettings", []))

    @builtins.property
    @jsii.member(jsii_name="protectedSettingsFromKeyVault")
    def protected_settings_from_key_vault(
        self,
    ) -> "OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVaultOutputReference":
        return typing.cast("OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVaultOutputReference", jsii.get(self, "protectedSettingsFromKeyVault"))

    @builtins.property
    @jsii.member(jsii_name="autoUpgradeMinorVersionEnabledInput")
    def auto_upgrade_minor_version_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoUpgradeMinorVersionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionsToProvisionAfterVmCreationInput")
    def extensions_to_provision_after_vm_creation_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "extensionsToProvisionAfterVmCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="failureSuppressionEnabledInput")
    def failure_suppression_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failureSuppressionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="forceExtensionExecutionOnChangeInput")
    def force_extension_execution_on_change_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forceExtensionExecutionOnChangeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protectedSettingsFromKeyVaultInput")
    def protected_settings_from_key_vault_input(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVault"]:
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVault"], jsii.get(self, "protectedSettingsFromKeyVaultInput"))

    @builtins.property
    @jsii.member(jsii_name="protectedSettingsInput")
    def protected_settings_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protectedSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherInput")
    def publisher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="settingsInput")
    def settings_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "settingsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeHandlerVersionInput")
    def type_handler_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeHandlerVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="autoUpgradeMinorVersionEnabled")
    def auto_upgrade_minor_version_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoUpgradeMinorVersionEnabled"))

    @auto_upgrade_minor_version_enabled.setter
    def auto_upgrade_minor_version_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0b9b7e71d569a8a6625aa81d3b30ea809f23249a8dc3c8ee9bb04c5ae9a1e21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoUpgradeMinorVersionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extensionsToProvisionAfterVmCreation")
    def extensions_to_provision_after_vm_creation(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "extensionsToProvisionAfterVmCreation"))

    @extensions_to_provision_after_vm_creation.setter
    def extensions_to_provision_after_vm_creation(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b700d19cb46c4c86d7162fe218761d91abe81fbf58cb97283a21ddcb9a63e70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extensionsToProvisionAfterVmCreation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failureSuppressionEnabled")
    def failure_suppression_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failureSuppressionEnabled"))

    @failure_suppression_enabled.setter
    def failure_suppression_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e89a33bd084a7518224f42fa114c18b31e7345c1dafffb7908bf310d0428e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureSuppressionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceExtensionExecutionOnChange")
    def force_extension_execution_on_change(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forceExtensionExecutionOnChange"))

    @force_extension_execution_on_change.setter
    def force_extension_execution_on_change(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8cc45085fd0bafd85538030b37a67ecb9b02b4953325f682d76d86ff70861fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceExtensionExecutionOnChange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ace08426412e9572f53e9fe0e6619dc12fb08d0d1f0fc2d0c3f17ff07fb891e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protectedSettings")
    def protected_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectedSettings"))

    @protected_settings.setter
    def protected_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05eda88338f72d5da04eecfafaa56a0e457ed7f2b6ad86b3870e4f8f976a3970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protectedSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisher"))

    @publisher.setter
    def publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef4f946a59311920616adb70dfcf53ac13c253146e228ac1d9b2ff4b01cc7e66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "settings"))

    @settings.setter
    def settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828efe1149ed32a12ceb0a749f48e0eb7a376be8035d29b91fe4441422360573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "settings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32eb68f244ef92d49392ed4f992e184b18d8008f87eaec8d965c29df4bed71c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="typeHandlerVersion")
    def type_handler_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "typeHandlerVersion"))

    @type_handler_version.setter
    def type_handler_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06eb964ed683bada6ca4a12d88406e19449b17991f4f241ad943ec46f886b028)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeHandlerVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetExtension]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetExtension]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetExtension]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce77053e1de458e6dd4b6c028b7ba053de43b71eeaae33e9376058b678f6fb48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVault",
    jsii_struct_bases=[],
    name_mapping={"secret_url": "secretUrl", "source_vault_id": "sourceVaultId"},
)
class OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVault:
    def __init__(
        self,
        *,
        secret_url: builtins.str,
        source_vault_id: builtins.str,
    ) -> None:
        '''
        :param secret_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#secret_url OrchestratedVirtualMachineScaleSet#secret_url}.
        :param source_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#source_vault_id OrchestratedVirtualMachineScaleSet#source_vault_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7afe578da8943494d5e77d30f77fde07283c583d707f01c6e861d85ef9b28e)
            check_type(argname="argument secret_url", value=secret_url, expected_type=type_hints["secret_url"])
            check_type(argname="argument source_vault_id", value=source_vault_id, expected_type=type_hints["source_vault_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_url": secret_url,
            "source_vault_id": source_vault_id,
        }

    @builtins.property
    def secret_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#secret_url OrchestratedVirtualMachineScaleSet#secret_url}.'''
        result = self._values.get("secret_url")
        assert result is not None, "Required property 'secret_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_vault_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#source_vault_id OrchestratedVirtualMachineScaleSet#source_vault_id}.'''
        result = self._values.get("source_vault_id")
        assert result is not None, "Required property 'source_vault_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVault(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVaultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVaultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb1bd007d5f14857c587ddd72dcb09dda2f317cbbbf9020691df7fcd63544a89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f32ba669e679387b4087d37508489203df9731b8e27a108e883188c4c5eee887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceVaultId")
    def source_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceVaultId"))

    @source_vault_id.setter
    def source_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394fddac6dbf431131bb61265df7fbfe57b70447543794130917ff5d9a255efa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVault]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVault], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVault],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bffa8b0cebdb2861b6477431707fe1905e2c1d100d25c0524a70ec9dd49d051a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetIdentity",
    jsii_struct_bases=[],
    name_mapping={"identity_ids": "identityIds", "type": "type"},
)
class OrchestratedVirtualMachineScaleSetIdentity:
    def __init__(
        self,
        *,
        identity_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#identity_ids OrchestratedVirtualMachineScaleSet#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#type OrchestratedVirtualMachineScaleSet#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c899d4e834c265e558ef037ca78528306e0e63d5fb8f9ed2077de869eee6c208)
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identity_ids": identity_ids,
            "type": type,
        }

    @builtins.property
    def identity_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#identity_ids OrchestratedVirtualMachineScaleSet#identity_ids}.'''
        result = self._values.get("identity_ids")
        assert result is not None, "Required property 'identity_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#type OrchestratedVirtualMachineScaleSet#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d63280706381ad1e6a2bc1f2b8f3571b2cb8dcd08396ea11ad1f1e28b2bb83a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93f320b6049f4669a4c3707983fe297724af22173e578f9a3e78f33c62aab580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f896031045c219c2e5fbb530f5c05fccdbfbf21c60ec8f893c154ba8e10f26c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetIdentity]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrchestratedVirtualMachineScaleSetIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca20ead7a88e94723bac9b3564d6526c2aa480acf0c1d9bf5542bf0d89508e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetNetworkInterface",
    jsii_struct_bases=[],
    name_mapping={
        "ip_configuration": "ipConfiguration",
        "name": "name",
        "dns_servers": "dnsServers",
        "enable_accelerated_networking": "enableAcceleratedNetworking",
        "enable_ip_forwarding": "enableIpForwarding",
        "network_security_group_id": "networkSecurityGroupId",
        "primary": "primary",
    },
)
class OrchestratedVirtualMachineScaleSetNetworkInterface:
    def __init__(
        self,
        *,
        ip_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_accelerated_networking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_ip_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_security_group_id: typing.Optional[builtins.str] = None,
        primary: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param ip_configuration: ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#ip_configuration OrchestratedVirtualMachineScaleSet#ip_configuration}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#name OrchestratedVirtualMachineScaleSet#name}.
        :param dns_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#dns_servers OrchestratedVirtualMachineScaleSet#dns_servers}.
        :param enable_accelerated_networking: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#enable_accelerated_networking OrchestratedVirtualMachineScaleSet#enable_accelerated_networking}.
        :param enable_ip_forwarding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#enable_ip_forwarding OrchestratedVirtualMachineScaleSet#enable_ip_forwarding}.
        :param network_security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#network_security_group_id OrchestratedVirtualMachineScaleSet#network_security_group_id}.
        :param primary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#primary OrchestratedVirtualMachineScaleSet#primary}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1c17d92aa5daf1b2f35d6781c7067e1336908001c073abf4c13df8dbe6abe11)
            check_type(argname="argument ip_configuration", value=ip_configuration, expected_type=type_hints["ip_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument dns_servers", value=dns_servers, expected_type=type_hints["dns_servers"])
            check_type(argname="argument enable_accelerated_networking", value=enable_accelerated_networking, expected_type=type_hints["enable_accelerated_networking"])
            check_type(argname="argument enable_ip_forwarding", value=enable_ip_forwarding, expected_type=type_hints["enable_ip_forwarding"])
            check_type(argname="argument network_security_group_id", value=network_security_group_id, expected_type=type_hints["network_security_group_id"])
            check_type(argname="argument primary", value=primary, expected_type=type_hints["primary"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_configuration": ip_configuration,
            "name": name,
        }
        if dns_servers is not None:
            self._values["dns_servers"] = dns_servers
        if enable_accelerated_networking is not None:
            self._values["enable_accelerated_networking"] = enable_accelerated_networking
        if enable_ip_forwarding is not None:
            self._values["enable_ip_forwarding"] = enable_ip_forwarding
        if network_security_group_id is not None:
            self._values["network_security_group_id"] = network_security_group_id
        if primary is not None:
            self._values["primary"] = primary

    @builtins.property
    def ip_configuration(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration"]]:
        '''ip_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#ip_configuration OrchestratedVirtualMachineScaleSet#ip_configuration}
        '''
        result = self._values.get("ip_configuration")
        assert result is not None, "Required property 'ip_configuration' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#name OrchestratedVirtualMachineScaleSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dns_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#dns_servers OrchestratedVirtualMachineScaleSet#dns_servers}.'''
        result = self._values.get("dns_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_accelerated_networking(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#enable_accelerated_networking OrchestratedVirtualMachineScaleSet#enable_accelerated_networking}.'''
        result = self._values.get("enable_accelerated_networking")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_ip_forwarding(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#enable_ip_forwarding OrchestratedVirtualMachineScaleSet#enable_ip_forwarding}.'''
        result = self._values.get("enable_ip_forwarding")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def network_security_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#network_security_group_id OrchestratedVirtualMachineScaleSet#network_security_group_id}.'''
        result = self._values.get("network_security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#primary OrchestratedVirtualMachineScaleSet#primary}.'''
        result = self._values.get("primary")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetNetworkInterface(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "application_gateway_backend_address_pool_ids": "applicationGatewayBackendAddressPoolIds",
        "application_security_group_ids": "applicationSecurityGroupIds",
        "load_balancer_backend_address_pool_ids": "loadBalancerBackendAddressPoolIds",
        "primary": "primary",
        "public_ip_address": "publicIpAddress",
        "subnet_id": "subnetId",
        "version": "version",
    },
)
class OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration:
    def __init__(
        self,
        *,
        name: builtins.str,
        application_gateway_backend_address_pool_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        application_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        load_balancer_backend_address_pool_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        primary: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_ip_address: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress", typing.Dict[builtins.str, typing.Any]]]]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#name OrchestratedVirtualMachineScaleSet#name}.
        :param application_gateway_backend_address_pool_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#application_gateway_backend_address_pool_ids OrchestratedVirtualMachineScaleSet#application_gateway_backend_address_pool_ids}.
        :param application_security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#application_security_group_ids OrchestratedVirtualMachineScaleSet#application_security_group_ids}.
        :param load_balancer_backend_address_pool_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#load_balancer_backend_address_pool_ids OrchestratedVirtualMachineScaleSet#load_balancer_backend_address_pool_ids}.
        :param primary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#primary OrchestratedVirtualMachineScaleSet#primary}.
        :param public_ip_address: public_ip_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#public_ip_address OrchestratedVirtualMachineScaleSet#public_ip_address}
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#subnet_id OrchestratedVirtualMachineScaleSet#subnet_id}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#version OrchestratedVirtualMachineScaleSet#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__268f5ebd5a664895433e8fde830786bb07b1807a44266d81790cea62864413f8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument application_gateway_backend_address_pool_ids", value=application_gateway_backend_address_pool_ids, expected_type=type_hints["application_gateway_backend_address_pool_ids"])
            check_type(argname="argument application_security_group_ids", value=application_security_group_ids, expected_type=type_hints["application_security_group_ids"])
            check_type(argname="argument load_balancer_backend_address_pool_ids", value=load_balancer_backend_address_pool_ids, expected_type=type_hints["load_balancer_backend_address_pool_ids"])
            check_type(argname="argument primary", value=primary, expected_type=type_hints["primary"])
            check_type(argname="argument public_ip_address", value=public_ip_address, expected_type=type_hints["public_ip_address"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if application_gateway_backend_address_pool_ids is not None:
            self._values["application_gateway_backend_address_pool_ids"] = application_gateway_backend_address_pool_ids
        if application_security_group_ids is not None:
            self._values["application_security_group_ids"] = application_security_group_ids
        if load_balancer_backend_address_pool_ids is not None:
            self._values["load_balancer_backend_address_pool_ids"] = load_balancer_backend_address_pool_ids
        if primary is not None:
            self._values["primary"] = primary
        if public_ip_address is not None:
            self._values["public_ip_address"] = public_ip_address
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#name OrchestratedVirtualMachineScaleSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_gateway_backend_address_pool_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#application_gateway_backend_address_pool_ids OrchestratedVirtualMachineScaleSet#application_gateway_backend_address_pool_ids}.'''
        result = self._values.get("application_gateway_backend_address_pool_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def application_security_group_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#application_security_group_ids OrchestratedVirtualMachineScaleSet#application_security_group_ids}.'''
        result = self._values.get("application_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def load_balancer_backend_address_pool_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#load_balancer_backend_address_pool_ids OrchestratedVirtualMachineScaleSet#load_balancer_backend_address_pool_ids}.'''
        result = self._values.get("load_balancer_backend_address_pool_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def primary(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#primary OrchestratedVirtualMachineScaleSet#primary}.'''
        result = self._values.get("primary")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def public_ip_address(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress"]]]:
        '''public_ip_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#public_ip_address OrchestratedVirtualMachineScaleSet#public_ip_address}
        '''
        result = self._values.get("public_ip_address")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress"]]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#subnet_id OrchestratedVirtualMachineScaleSet#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#version OrchestratedVirtualMachineScaleSet#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efb1447a05c197087919937a384ec08f2722c1c5d4dd2c72d2fc6cf495d0c634)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b79ecc63f6f44caf5a856af1d870ae1ea8debaa80d434aa7431d89ea567c6996)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f63260e1bedd433ed6db13a0bf3918112316ff1d9049b9619c3fc8c89b168fd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2317c43ec5ae1a1659001e16a11cc0a247aaf8102c3c00c7276b013dd4f88e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2869ba412e87a3765dfa888362b1587a5bb5bd8ede6ddf5721238dbfc48e57ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__713383657af33c5704e89fcd787b45c076d52853527a7b024e14b32cf0da50f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bb7c9022e81a661a128fde33b009885a73862d754902eb988a9eaa22c994a4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPublicIpAddress")
    def put_public_ip_address(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6740c266c157b0a29fc01cfd7ffefa9ca6d20bef729b9c5d73376576232d6d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPublicIpAddress", [value]))

    @jsii.member(jsii_name="resetApplicationGatewayBackendAddressPoolIds")
    def reset_application_gateway_backend_address_pool_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationGatewayBackendAddressPoolIds", []))

    @jsii.member(jsii_name="resetApplicationSecurityGroupIds")
    def reset_application_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationSecurityGroupIds", []))

    @jsii.member(jsii_name="resetLoadBalancerBackendAddressPoolIds")
    def reset_load_balancer_backend_address_pool_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerBackendAddressPoolIds", []))

    @jsii.member(jsii_name="resetPrimary")
    def reset_primary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimary", []))

    @jsii.member(jsii_name="resetPublicIpAddress")
    def reset_public_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIpAddress", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="publicIpAddress")
    def public_ip_address(
        self,
    ) -> "OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressList":
        return typing.cast("OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressList", jsii.get(self, "publicIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="applicationGatewayBackendAddressPoolIdsInput")
    def application_gateway_backend_address_pool_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "applicationGatewayBackendAddressPoolIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationSecurityGroupIdsInput")
    def application_security_group_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "applicationSecurityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerBackendAddressPoolIdsInput")
    def load_balancer_backend_address_pool_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "loadBalancerBackendAddressPoolIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryInput")
    def primary_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "primaryInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressInput")
    def public_ip_address_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress"]]], jsii.get(self, "publicIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationGatewayBackendAddressPoolIds")
    def application_gateway_backend_address_pool_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "applicationGatewayBackendAddressPoolIds"))

    @application_gateway_backend_address_pool_ids.setter
    def application_gateway_backend_address_pool_ids(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdfb1bb7f171052d8237904a4c79058dfb45149974db5a15d2026e4659c76fef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationGatewayBackendAddressPoolIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationSecurityGroupIds")
    def application_security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "applicationSecurityGroupIds"))

    @application_security_group_ids.setter
    def application_security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5b32d8143e8b0e3154434e667d2a8d1d508af47b3dd040dc15a8fc5dce0468f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationSecurityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerBackendAddressPoolIds")
    def load_balancer_backend_address_pool_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loadBalancerBackendAddressPoolIds"))

    @load_balancer_backend_address_pool_ids.setter
    def load_balancer_backend_address_pool_ids(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb8327db691d81b532a819e50d8fd73aa8f0072606614ee7d9945b5907243ffd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerBackendAddressPoolIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29e01eb017181b4660cf96d3ec4544ad0455cb829ea8fc1c5800603bd91d4bde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primary")
    def primary(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "primary"))

    @primary.setter
    def primary(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4edce56a415bd77b8528d6e532addac1b8079c3959db7988be401c995308ee63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69ed692875848995e29815e0bc61d0f6bcfd214a00b3db13f9a2e353aa901f07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a17e62fd5a406bc37ce9ff887107e774d8e20c23720026fe84b8fdc4017c1b8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17bc5d26f2e5f1036e36c64528c62d0fb9d702648eca8bcb961b44f5fb597391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "domain_name_label": "domainNameLabel",
        "idle_timeout_in_minutes": "idleTimeoutInMinutes",
        "ip_tag": "ipTag",
        "public_ip_prefix_id": "publicIpPrefixId",
        "sku_name": "skuName",
        "version": "version",
    },
)
class OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress:
    def __init__(
        self,
        *,
        name: builtins.str,
        domain_name_label: typing.Optional[builtins.str] = None,
        idle_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        ip_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
        public_ip_prefix_id: typing.Optional[builtins.str] = None,
        sku_name: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#name OrchestratedVirtualMachineScaleSet#name}.
        :param domain_name_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#domain_name_label OrchestratedVirtualMachineScaleSet#domain_name_label}.
        :param idle_timeout_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#idle_timeout_in_minutes OrchestratedVirtualMachineScaleSet#idle_timeout_in_minutes}.
        :param ip_tag: ip_tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#ip_tag OrchestratedVirtualMachineScaleSet#ip_tag}
        :param public_ip_prefix_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#public_ip_prefix_id OrchestratedVirtualMachineScaleSet#public_ip_prefix_id}.
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#sku_name OrchestratedVirtualMachineScaleSet#sku_name}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#version OrchestratedVirtualMachineScaleSet#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c798fc5ca0a00abbd7a1855a73d73feb33138d3a9fd1128852787a128cad63b7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument domain_name_label", value=domain_name_label, expected_type=type_hints["domain_name_label"])
            check_type(argname="argument idle_timeout_in_minutes", value=idle_timeout_in_minutes, expected_type=type_hints["idle_timeout_in_minutes"])
            check_type(argname="argument ip_tag", value=ip_tag, expected_type=type_hints["ip_tag"])
            check_type(argname="argument public_ip_prefix_id", value=public_ip_prefix_id, expected_type=type_hints["public_ip_prefix_id"])
            check_type(argname="argument sku_name", value=sku_name, expected_type=type_hints["sku_name"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if domain_name_label is not None:
            self._values["domain_name_label"] = domain_name_label
        if idle_timeout_in_minutes is not None:
            self._values["idle_timeout_in_minutes"] = idle_timeout_in_minutes
        if ip_tag is not None:
            self._values["ip_tag"] = ip_tag
        if public_ip_prefix_id is not None:
            self._values["public_ip_prefix_id"] = public_ip_prefix_id
        if sku_name is not None:
            self._values["sku_name"] = sku_name
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#name OrchestratedVirtualMachineScaleSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name_label(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#domain_name_label OrchestratedVirtualMachineScaleSet#domain_name_label}.'''
        result = self._values.get("domain_name_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#idle_timeout_in_minutes OrchestratedVirtualMachineScaleSet#idle_timeout_in_minutes}.'''
        result = self._values.get("idle_timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ip_tag(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag"]]]:
        '''ip_tag block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#ip_tag OrchestratedVirtualMachineScaleSet#ip_tag}
        '''
        result = self._values.get("ip_tag")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag"]]], result)

    @builtins.property
    def public_ip_prefix_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#public_ip_prefix_id OrchestratedVirtualMachineScaleSet#public_ip_prefix_id}.'''
        result = self._values.get("public_ip_prefix_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sku_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#sku_name OrchestratedVirtualMachineScaleSet#sku_name}.'''
        result = self._values.get("sku_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#version OrchestratedVirtualMachineScaleSet#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag",
    jsii_struct_bases=[],
    name_mapping={"tag": "tag", "type": "type"},
)
class OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag:
    def __init__(self, *, tag: builtins.str, type: builtins.str) -> None:
        '''
        :param tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#tag OrchestratedVirtualMachineScaleSet#tag}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#type OrchestratedVirtualMachineScaleSet#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836345d09fb0d43cf0bd3bfd416edca332a28d6ea7be6d9823eb06bcd4ae1269)
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tag": tag,
            "type": type,
        }

    @builtins.property
    def tag(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#tag OrchestratedVirtualMachineScaleSet#tag}.'''
        result = self._values.get("tag")
        assert result is not None, "Required property 'tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#type OrchestratedVirtualMachineScaleSet#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35b495b5327af44d002129144fb25c3b3bcb1fa49cb5e7e4c8cec39b292784df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac46f162b366ae5995ca49032c7a9cc0e8fb0226f35169ed5bbab9321bce3ae1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff809daecedb8583ae62f84224496995857ff1416d2e9aa4e40e8823ffc16e55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c31202467e6da40f35e02167c50f0ea328e92c5064b84eb99700f39ab6d3c77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ba5d43215306cf4b44d906440f7c505f1a9f3ddd6e8334bdefa2f0772356b04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3346216a165c6fd6734df661fdfb97d4169863b5b2af7a79f6957d73d173cb3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54f506f403b8e7fac11f6a0dfd3960855efe714ebe188411ce02ed8942144870)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfe6b4f6e5d3a08d2a54d66ab3a37dca4c40706469ac7f43f8bd0710b21d8140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdf89cc4a6fda1f4a1f422faefee78e4918504f2a68402573f2e3c566b7aa3b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7615e94a303eb0d8016e0744de0574da7eaab79adcc4b4111c25efdd42b268ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14a34c5b3fd60d01d5c018c18694a978d9b288f8bc0a77d829d1c6fee467f86a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e53f239aaca722862c26dc353108c8e34d47dc536006df33120dad7456d5ad97)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11c10d31b50464575973513109f34d6a77ef78fc592718d87f0f3fde432e44dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9315710f0b62204a651e49ebe341c3120ce95f2bd15f6e8a96b982eb38da8737)
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
            type_hints = typing.get_type_hints(_typecheckingstub__340b9f5dbfb4758f193e9e04a1afa27802e737e10d2dbae98630767670aae5f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12c1f038c1db59791913ef6496e5598153447c2093954287880058cf1c527af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8deb6ef39a58782be1bc21bf3e8183bf96370c49fcda2a20a8c30a23744f9c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIpTag")
    def put_ip_tag(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f3cfec6bbc136615eef00c93e636f743f90a8ad2eb369199cff52e9a1ef2f09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpTag", [value]))

    @jsii.member(jsii_name="resetDomainNameLabel")
    def reset_domain_name_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainNameLabel", []))

    @jsii.member(jsii_name="resetIdleTimeoutInMinutes")
    def reset_idle_timeout_in_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleTimeoutInMinutes", []))

    @jsii.member(jsii_name="resetIpTag")
    def reset_ip_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpTag", []))

    @jsii.member(jsii_name="resetPublicIpPrefixId")
    def reset_public_ip_prefix_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIpPrefixId", []))

    @jsii.member(jsii_name="resetSkuName")
    def reset_sku_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkuName", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="ipTag")
    def ip_tag(
        self,
    ) -> OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTagList:
        return typing.cast(OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTagList, jsii.get(self, "ipTag"))

    @builtins.property
    @jsii.member(jsii_name="domainNameLabelInput")
    def domain_name_label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="idleTimeoutInMinutesInput")
    def idle_timeout_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "idleTimeoutInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="ipTagInput")
    def ip_tag_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag]]], jsii.get(self, "ipTagInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpPrefixIdInput")
    def public_ip_prefix_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicIpPrefixIdInput"))

    @builtins.property
    @jsii.member(jsii_name="skuNameInput")
    def sku_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuNameInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameLabel")
    def domain_name_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainNameLabel"))

    @domain_name_label.setter
    def domain_name_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ded8af95a7c62b780311c025c33bb18a91cb1f1ddd8a93ec374e086d2a0eec44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainNameLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idleTimeoutInMinutes")
    def idle_timeout_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "idleTimeoutInMinutes"))

    @idle_timeout_in_minutes.setter
    def idle_timeout_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84e2b061123503ba90bf4ab8c6cff786600514285ceb59478594474107293f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleTimeoutInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44997a13e1a77f20b7f8cbc518a0eec7d6d0c984d02b078f6ae9f36c2c442ff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpPrefixId")
    def public_ip_prefix_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpPrefixId"))

    @public_ip_prefix_id.setter
    def public_ip_prefix_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e9cb7923132d1d00af1ecbb067c945552ae287f77ad925891c39c44640b047b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpPrefixId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skuName")
    def sku_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "skuName"))

    @sku_name.setter
    def sku_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b3e0e87f0b1d4791357b428bf77a2cf6ae44426e187aa10b57484e0ff9c240a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skuName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76ea5908cf9f3cc74754c460e05ee7c6656ddd12f0c9c978a5e1f8ccbd26ce8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__082dbaddcb65bc35aa3f40266c52f9e0a4f66b5c1b5a48617e67048516e6c81d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetNetworkInterfaceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetNetworkInterfaceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4c26ec0610f9ff790be83a6cd4f2a49e04fd26e7da23e59ccbf7a752da1d627)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrchestratedVirtualMachineScaleSetNetworkInterfaceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__898b0df05f282bc4aecf51ae9a71ceabd6b8a86e9696857a9bfaa1955636e542)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrchestratedVirtualMachineScaleSetNetworkInterfaceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__384df1b9370605e1e6967d2e0186fe56bd8503088f1c8e8e7cdb2ca123362b4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c1df26c7b97068e569d11c62430a80fbf55415480c2b9aa9a1ad1655635847a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7585b04735a3d2fb3ca40e30b97f57cc026a5cb274387c8ee700b44a248d5dd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterface]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterface]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterface]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79fa732f52ec97fbba0844b2a67e9ee16df88f431512141644b4cd957a96d751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetNetworkInterfaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetNetworkInterfaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b4ed4ead3d99faf388766439bc634902a3ac8b3c22b7ef885ccdcc11671856e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIpConfiguration")
    def put_ip_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a01a75be676afa5889ec76749de461311c8695324b442f7f04b67598882516da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpConfiguration", [value]))

    @jsii.member(jsii_name="resetDnsServers")
    def reset_dns_servers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsServers", []))

    @jsii.member(jsii_name="resetEnableAcceleratedNetworking")
    def reset_enable_accelerated_networking(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAcceleratedNetworking", []))

    @jsii.member(jsii_name="resetEnableIpForwarding")
    def reset_enable_ip_forwarding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableIpForwarding", []))

    @jsii.member(jsii_name="resetNetworkSecurityGroupId")
    def reset_network_security_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkSecurityGroupId", []))

    @jsii.member(jsii_name="resetPrimary")
    def reset_primary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimary", []))

    @builtins.property
    @jsii.member(jsii_name="ipConfiguration")
    def ip_configuration(
        self,
    ) -> OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationList:
        return typing.cast(OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationList, jsii.get(self, "ipConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="dnsServersInput")
    def dns_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsServersInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAcceleratedNetworkingInput")
    def enable_accelerated_networking_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableAcceleratedNetworkingInput"))

    @builtins.property
    @jsii.member(jsii_name="enableIpForwardingInput")
    def enable_ip_forwarding_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableIpForwardingInput"))

    @builtins.property
    @jsii.member(jsii_name="ipConfigurationInput")
    def ip_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration]]], jsii.get(self, "ipConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkSecurityGroupIdInput")
    def network_security_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkSecurityGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryInput")
    def primary_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "primaryInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsServers")
    def dns_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsServers"))

    @dns_servers.setter
    def dns_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7471bbd07680f0ed44efbc487391bc1f52036dd32ea2725b9c9109434662dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableAcceleratedNetworking")
    def enable_accelerated_networking(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableAcceleratedNetworking"))

    @enable_accelerated_networking.setter
    def enable_accelerated_networking(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4fbd9924183db48b09946522d288cb3e1e40a749da7775279b9fc9217b2dd0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAcceleratedNetworking", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableIpForwarding")
    def enable_ip_forwarding(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableIpForwarding"))

    @enable_ip_forwarding.setter
    def enable_ip_forwarding(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af60615b11a3bf78900cb4b917b27db5f6ff96dd2281f945b05966f84f0ebf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIpForwarding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e697655850f92ef7d1e2f196887de46fd3263a35a0760371acd5c87f69d45c6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkSecurityGroupId")
    def network_security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkSecurityGroupId"))

    @network_security_group_id.setter
    def network_security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2766d011a59f32d05fc8c30d92e4c46fe35a23bbe0222e2a27e03e21d3b6e00a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkSecurityGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primary")
    def primary(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "primary"))

    @primary.setter
    def primary(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc37f7745d3727d72b36be07fb895636cbc274290a13e669594d47e60ecf17ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetNetworkInterface]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetNetworkInterface]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetNetworkInterface]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e70e0ee8622d07f3364bc9f6596214ce6c7ee69255c754bf708f10e47213328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsDisk",
    jsii_struct_bases=[],
    name_mapping={
        "caching": "caching",
        "storage_account_type": "storageAccountType",
        "diff_disk_settings": "diffDiskSettings",
        "disk_encryption_set_id": "diskEncryptionSetId",
        "disk_size_gb": "diskSizeGb",
        "write_accelerator_enabled": "writeAcceleratorEnabled",
    },
)
class OrchestratedVirtualMachineScaleSetOsDisk:
    def __init__(
        self,
        *,
        caching: builtins.str,
        storage_account_type: builtins.str,
        diff_disk_settings: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_encryption_set_id: typing.Optional[builtins.str] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        write_accelerator_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param caching: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#caching OrchestratedVirtualMachineScaleSet#caching}.
        :param storage_account_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#storage_account_type OrchestratedVirtualMachineScaleSet#storage_account_type}.
        :param diff_disk_settings: diff_disk_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#diff_disk_settings OrchestratedVirtualMachineScaleSet#diff_disk_settings}
        :param disk_encryption_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#disk_encryption_set_id OrchestratedVirtualMachineScaleSet#disk_encryption_set_id}.
        :param disk_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#disk_size_gb OrchestratedVirtualMachineScaleSet#disk_size_gb}.
        :param write_accelerator_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#write_accelerator_enabled OrchestratedVirtualMachineScaleSet#write_accelerator_enabled}.
        '''
        if isinstance(diff_disk_settings, dict):
            diff_disk_settings = OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettings(**diff_disk_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c01b5d6f4567ea9538517921d25308cbb84e09122817ff66e5b608fb79576d8e)
            check_type(argname="argument caching", value=caching, expected_type=type_hints["caching"])
            check_type(argname="argument storage_account_type", value=storage_account_type, expected_type=type_hints["storage_account_type"])
            check_type(argname="argument diff_disk_settings", value=diff_disk_settings, expected_type=type_hints["diff_disk_settings"])
            check_type(argname="argument disk_encryption_set_id", value=disk_encryption_set_id, expected_type=type_hints["disk_encryption_set_id"])
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument write_accelerator_enabled", value=write_accelerator_enabled, expected_type=type_hints["write_accelerator_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "caching": caching,
            "storage_account_type": storage_account_type,
        }
        if diff_disk_settings is not None:
            self._values["diff_disk_settings"] = diff_disk_settings
        if disk_encryption_set_id is not None:
            self._values["disk_encryption_set_id"] = disk_encryption_set_id
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if write_accelerator_enabled is not None:
            self._values["write_accelerator_enabled"] = write_accelerator_enabled

    @builtins.property
    def caching(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#caching OrchestratedVirtualMachineScaleSet#caching}.'''
        result = self._values.get("caching")
        assert result is not None, "Required property 'caching' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#storage_account_type OrchestratedVirtualMachineScaleSet#storage_account_type}.'''
        result = self._values.get("storage_account_type")
        assert result is not None, "Required property 'storage_account_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def diff_disk_settings(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettings"]:
        '''diff_disk_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#diff_disk_settings OrchestratedVirtualMachineScaleSet#diff_disk_settings}
        '''
        result = self._values.get("diff_disk_settings")
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettings"], result)

    @builtins.property
    def disk_encryption_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#disk_encryption_set_id OrchestratedVirtualMachineScaleSet#disk_encryption_set_id}.'''
        result = self._values.get("disk_encryption_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#disk_size_gb OrchestratedVirtualMachineScaleSet#disk_size_gb}.'''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def write_accelerator_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#write_accelerator_enabled OrchestratedVirtualMachineScaleSet#write_accelerator_enabled}.'''
        result = self._values.get("write_accelerator_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetOsDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettings",
    jsii_struct_bases=[],
    name_mapping={"option": "option", "placement": "placement"},
)
class OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettings:
    def __init__(
        self,
        *,
        option: builtins.str,
        placement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#option OrchestratedVirtualMachineScaleSet#option}.
        :param placement: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#placement OrchestratedVirtualMachineScaleSet#placement}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__103234cded650a69a0b7980237c0d94c5ab31e083c2e2a9b5e68c1b9f2afe061)
            check_type(argname="argument option", value=option, expected_type=type_hints["option"])
            check_type(argname="argument placement", value=placement, expected_type=type_hints["placement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "option": option,
        }
        if placement is not None:
            self._values["placement"] = placement

    @builtins.property
    def option(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#option OrchestratedVirtualMachineScaleSet#option}.'''
        result = self._values.get("option")
        assert result is not None, "Required property 'option' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def placement(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#placement OrchestratedVirtualMachineScaleSet#placement}.'''
        result = self._values.get("placement")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b140aa3ff13a7fd4a5629039feb783906709da04f2d3a550f4a5619ceff6e8de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPlacement")
    def reset_placement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlacement", []))

    @builtins.property
    @jsii.member(jsii_name="optionInput")
    def option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "optionInput"))

    @builtins.property
    @jsii.member(jsii_name="placementInput")
    def placement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "placementInput"))

    @builtins.property
    @jsii.member(jsii_name="option")
    def option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "option"))

    @option.setter
    def option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d531878f3102b767e6ff3d3a50548bbd895ea1cd76f5dd52218d29881cb611b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "option", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="placement")
    def placement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "placement"))

    @placement.setter
    def placement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a9288d2681136a2a9985f258927873c40e75aa2106e10e9eb5cc789a967dea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "placement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettings]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c674050c249031bf9f61f00a7609f42e0e4a43acd836a496f57fc70e71d3d93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetOsDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__980e2c83e532b8cf5edbe77e05c228cc53c1327618565f70d1c3a10da37071de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDiffDiskSettings")
    def put_diff_disk_settings(
        self,
        *,
        option: builtins.str,
        placement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#option OrchestratedVirtualMachineScaleSet#option}.
        :param placement: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#placement OrchestratedVirtualMachineScaleSet#placement}.
        '''
        value = OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettings(
            option=option, placement=placement
        )

        return typing.cast(None, jsii.invoke(self, "putDiffDiskSettings", [value]))

    @jsii.member(jsii_name="resetDiffDiskSettings")
    def reset_diff_disk_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiffDiskSettings", []))

    @jsii.member(jsii_name="resetDiskEncryptionSetId")
    def reset_disk_encryption_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionSetId", []))

    @jsii.member(jsii_name="resetDiskSizeGb")
    def reset_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGb", []))

    @jsii.member(jsii_name="resetWriteAcceleratorEnabled")
    def reset_write_accelerator_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteAcceleratorEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="diffDiskSettings")
    def diff_disk_settings(
        self,
    ) -> OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettingsOutputReference:
        return typing.cast(OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettingsOutputReference, jsii.get(self, "diffDiskSettings"))

    @builtins.property
    @jsii.member(jsii_name="cachingInput")
    def caching_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cachingInput"))

    @builtins.property
    @jsii.member(jsii_name="diffDiskSettingsInput")
    def diff_disk_settings_input(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettings]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettings], jsii.get(self, "diffDiskSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionSetIdInput")
    def disk_encryption_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountTypeInput")
    def storage_account_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="writeAcceleratorEnabledInput")
    def write_accelerator_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "writeAcceleratorEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="caching")
    def caching(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caching"))

    @caching.setter
    def caching(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcae24fed6b8a83fb4b116e6fb544cbd475cdc35fbb5e34e2e0710e9159c9ac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caching", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionSetId")
    def disk_encryption_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionSetId"))

    @disk_encryption_set_id.setter
    def disk_encryption_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d416ac985b1ee8fd46879a128429b0f947e93cbabd3eec56c34a689eae8aa19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958b3664f7ebadc98c250e305e5bb2ee1e6f51a08b105107eb7c2c2870213374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountType")
    def storage_account_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountType"))

    @storage_account_type.setter
    def storage_account_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42bba04b7e9e1c6a46857fb48c34f6760c89eb4e6ed99b8de67521c8c95d68f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeAcceleratorEnabled")
    def write_accelerator_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "writeAcceleratorEnabled"))

    @write_accelerator_enabled.setter
    def write_accelerator_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d1eddd915c54b97b02be7e07ea623aab96c8b71a5ddbad8b6fe366c05b5f559)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeAcceleratorEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetOsDisk]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetOsDisk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrchestratedVirtualMachineScaleSetOsDisk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7220e21ef76493650b38a62696ba420441fc77b161a3a1b22e193c0d2d70121b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfile",
    jsii_struct_bases=[],
    name_mapping={
        "custom_data": "customData",
        "linux_configuration": "linuxConfiguration",
        "windows_configuration": "windowsConfiguration",
    },
)
class OrchestratedVirtualMachineScaleSetOsProfile:
    def __init__(
        self,
        *,
        custom_data: typing.Optional[builtins.str] = None,
        linux_configuration: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetOsProfileLinuxConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        windows_configuration: typing.Optional[typing.Union["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#custom_data OrchestratedVirtualMachineScaleSet#custom_data}.
        :param linux_configuration: linux_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#linux_configuration OrchestratedVirtualMachineScaleSet#linux_configuration}
        :param windows_configuration: windows_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#windows_configuration OrchestratedVirtualMachineScaleSet#windows_configuration}
        '''
        if isinstance(linux_configuration, dict):
            linux_configuration = OrchestratedVirtualMachineScaleSetOsProfileLinuxConfiguration(**linux_configuration)
        if isinstance(windows_configuration, dict):
            windows_configuration = OrchestratedVirtualMachineScaleSetOsProfileWindowsConfiguration(**windows_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1110dc9bc9155e779a049b64c51218fc6f39580d5406211ce1d2a6a0bb162d6f)
            check_type(argname="argument custom_data", value=custom_data, expected_type=type_hints["custom_data"])
            check_type(argname="argument linux_configuration", value=linux_configuration, expected_type=type_hints["linux_configuration"])
            check_type(argname="argument windows_configuration", value=windows_configuration, expected_type=type_hints["windows_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_data is not None:
            self._values["custom_data"] = custom_data
        if linux_configuration is not None:
            self._values["linux_configuration"] = linux_configuration
        if windows_configuration is not None:
            self._values["windows_configuration"] = windows_configuration

    @builtins.property
    def custom_data(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#custom_data OrchestratedVirtualMachineScaleSet#custom_data}.'''
        result = self._values.get("custom_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def linux_configuration(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetOsProfileLinuxConfiguration"]:
        '''linux_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#linux_configuration OrchestratedVirtualMachineScaleSet#linux_configuration}
        '''
        result = self._values.get("linux_configuration")
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetOsProfileLinuxConfiguration"], result)

    @builtins.property
    def windows_configuration(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfiguration"]:
        '''windows_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#windows_configuration OrchestratedVirtualMachineScaleSet#windows_configuration}
        '''
        result = self._values.get("windows_configuration")
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetOsProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileLinuxConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "admin_username": "adminUsername",
        "admin_password": "adminPassword",
        "admin_ssh_key": "adminSshKey",
        "computer_name_prefix": "computerNamePrefix",
        "disable_password_authentication": "disablePasswordAuthentication",
        "patch_assessment_mode": "patchAssessmentMode",
        "patch_mode": "patchMode",
        "provision_vm_agent": "provisionVmAgent",
        "secret": "secret",
    },
)
class OrchestratedVirtualMachineScaleSetOsProfileLinuxConfiguration:
    def __init__(
        self,
        *,
        admin_username: builtins.str,
        admin_password: typing.Optional[builtins.str] = None,
        admin_ssh_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey", typing.Dict[builtins.str, typing.Any]]]]] = None,
        computer_name_prefix: typing.Optional[builtins.str] = None,
        disable_password_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        patch_assessment_mode: typing.Optional[builtins.str] = None,
        patch_mode: typing.Optional[builtins.str] = None,
        provision_vm_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param admin_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#admin_username OrchestratedVirtualMachineScaleSet#admin_username}.
        :param admin_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#admin_password OrchestratedVirtualMachineScaleSet#admin_password}.
        :param admin_ssh_key: admin_ssh_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#admin_ssh_key OrchestratedVirtualMachineScaleSet#admin_ssh_key}
        :param computer_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#computer_name_prefix OrchestratedVirtualMachineScaleSet#computer_name_prefix}.
        :param disable_password_authentication: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#disable_password_authentication OrchestratedVirtualMachineScaleSet#disable_password_authentication}.
        :param patch_assessment_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#patch_assessment_mode OrchestratedVirtualMachineScaleSet#patch_assessment_mode}.
        :param patch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#patch_mode OrchestratedVirtualMachineScaleSet#patch_mode}.
        :param provision_vm_agent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#provision_vm_agent OrchestratedVirtualMachineScaleSet#provision_vm_agent}.
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#secret OrchestratedVirtualMachineScaleSet#secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a9d6a91dcc93dd2a4118339f9a49573ff6918e4ee6456423d1a407831ecc3bf)
            check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
            check_type(argname="argument admin_password", value=admin_password, expected_type=type_hints["admin_password"])
            check_type(argname="argument admin_ssh_key", value=admin_ssh_key, expected_type=type_hints["admin_ssh_key"])
            check_type(argname="argument computer_name_prefix", value=computer_name_prefix, expected_type=type_hints["computer_name_prefix"])
            check_type(argname="argument disable_password_authentication", value=disable_password_authentication, expected_type=type_hints["disable_password_authentication"])
            check_type(argname="argument patch_assessment_mode", value=patch_assessment_mode, expected_type=type_hints["patch_assessment_mode"])
            check_type(argname="argument patch_mode", value=patch_mode, expected_type=type_hints["patch_mode"])
            check_type(argname="argument provision_vm_agent", value=provision_vm_agent, expected_type=type_hints["provision_vm_agent"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_username": admin_username,
        }
        if admin_password is not None:
            self._values["admin_password"] = admin_password
        if admin_ssh_key is not None:
            self._values["admin_ssh_key"] = admin_ssh_key
        if computer_name_prefix is not None:
            self._values["computer_name_prefix"] = computer_name_prefix
        if disable_password_authentication is not None:
            self._values["disable_password_authentication"] = disable_password_authentication
        if patch_assessment_mode is not None:
            self._values["patch_assessment_mode"] = patch_assessment_mode
        if patch_mode is not None:
            self._values["patch_mode"] = patch_mode
        if provision_vm_agent is not None:
            self._values["provision_vm_agent"] = provision_vm_agent
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def admin_username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#admin_username OrchestratedVirtualMachineScaleSet#admin_username}.'''
        result = self._values.get("admin_username")
        assert result is not None, "Required property 'admin_username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#admin_password OrchestratedVirtualMachineScaleSet#admin_password}.'''
        result = self._values.get("admin_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def admin_ssh_key(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey"]]]:
        '''admin_ssh_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#admin_ssh_key OrchestratedVirtualMachineScaleSet#admin_ssh_key}
        '''
        result = self._values.get("admin_ssh_key")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey"]]], result)

    @builtins.property
    def computer_name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#computer_name_prefix OrchestratedVirtualMachineScaleSet#computer_name_prefix}.'''
        result = self._values.get("computer_name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_password_authentication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#disable_password_authentication OrchestratedVirtualMachineScaleSet#disable_password_authentication}.'''
        result = self._values.get("disable_password_authentication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def patch_assessment_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#patch_assessment_mode OrchestratedVirtualMachineScaleSet#patch_assessment_mode}.'''
        result = self._values.get("patch_assessment_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def patch_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#patch_mode OrchestratedVirtualMachineScaleSet#patch_mode}.'''
        result = self._values.get("patch_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provision_vm_agent(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#provision_vm_agent OrchestratedVirtualMachineScaleSet#provision_vm_agent}.'''
        result = self._values.get("provision_vm_agent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secret(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret"]]]:
        '''secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#secret OrchestratedVirtualMachineScaleSet#secret}
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey",
    jsii_struct_bases=[],
    name_mapping={"public_key": "publicKey", "username": "username"},
)
class OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey:
    def __init__(self, *, public_key: builtins.str, username: builtins.str) -> None:
        '''
        :param public_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#public_key OrchestratedVirtualMachineScaleSet#public_key}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#username OrchestratedVirtualMachineScaleSet#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe4d04648b916990dec1ff8390876169d955b4123ea6d66ec0240706ea1fa690)
            check_type(argname="argument public_key", value=public_key, expected_type=type_hints["public_key"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "public_key": public_key,
            "username": username,
        }

    @builtins.property
    def public_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#public_key OrchestratedVirtualMachineScaleSet#public_key}.'''
        result = self._values.get("public_key")
        assert result is not None, "Required property 'public_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#username OrchestratedVirtualMachineScaleSet#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKeyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKeyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e40311ef55010b4e0cf1475f5b0a54a86ac0d06a3b4d6b9fe395c0c88c10e46a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKeyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b91ebc599d07e2b74824113e9d281271389bad8a8fbebcf547b1e451bc031800)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKeyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53d7ff7bf1b8119eb43f1789fb687ee2f20dc492f5755f076acf4bd551bda4ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__251fc0b26409ec0f25d16db36a2d8b60a9787b9090bdda5fd40eda7e8677a5f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a268fe6e9c94f5ec734bfebee60f930873495f03c8169ab963a31887dda55733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2ad284a1b20fc9e495c7e1818b0434e081792c3cd7661a551b9be5c030a0f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d1da6675b2035060bd260c3e9ba993e1bd20adad7cb5c54957ca179bd0bf27d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="publicKeyInput")
    def public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKey"))

    @public_key.setter
    def public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__147e0c21b840758ecc29b90d21a295b2f11482b3497081640992bb22c9da7231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77559cfe35fe5aa74b9c407c451405ae48202b2951e0b06d3829bb3c390548fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b463d8974ce63d6be02911e65ccebab2814ae61ad3514ba298e29a2877a858de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb2e2601dd7234e5bdcc1001ff102a1b72b34d98882b4b08b583d44fda4bd512)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminSshKey")
    def put_admin_ssh_key(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__506c4c39eb2d5b972d2d2f4b482b29f374c659a5ece26c527fcaedfea3fd2a14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdminSshKey", [value]))

    @jsii.member(jsii_name="putSecret")
    def put_secret(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e702d8f3648f4fafeba236ff5706e3bee4c43405c4fbcc1567cf782df11a02c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecret", [value]))

    @jsii.member(jsii_name="resetAdminPassword")
    def reset_admin_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminPassword", []))

    @jsii.member(jsii_name="resetAdminSshKey")
    def reset_admin_ssh_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminSshKey", []))

    @jsii.member(jsii_name="resetComputerNamePrefix")
    def reset_computer_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputerNamePrefix", []))

    @jsii.member(jsii_name="resetDisablePasswordAuthentication")
    def reset_disable_password_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisablePasswordAuthentication", []))

    @jsii.member(jsii_name="resetPatchAssessmentMode")
    def reset_patch_assessment_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPatchAssessmentMode", []))

    @jsii.member(jsii_name="resetPatchMode")
    def reset_patch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPatchMode", []))

    @jsii.member(jsii_name="resetProvisionVmAgent")
    def reset_provision_vm_agent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionVmAgent", []))

    @jsii.member(jsii_name="resetSecret")
    def reset_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecret", []))

    @builtins.property
    @jsii.member(jsii_name="adminSshKey")
    def admin_ssh_key(
        self,
    ) -> OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKeyList:
        return typing.cast(OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKeyList, jsii.get(self, "adminSshKey"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(
        self,
    ) -> "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretList":
        return typing.cast("OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretList", jsii.get(self, "secret"))

    @builtins.property
    @jsii.member(jsii_name="adminPasswordInput")
    def admin_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="adminSshKeyInput")
    def admin_ssh_key_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey]]], jsii.get(self, "adminSshKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="adminUsernameInput")
    def admin_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="computerNamePrefixInput")
    def computer_name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computerNamePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="disablePasswordAuthenticationInput")
    def disable_password_authentication_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disablePasswordAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="patchAssessmentModeInput")
    def patch_assessment_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patchAssessmentModeInput"))

    @builtins.property
    @jsii.member(jsii_name="patchModeInput")
    def patch_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionVmAgentInput")
    def provision_vm_agent_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "provisionVmAgentInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret"]]], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="adminPassword")
    def admin_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminPassword"))

    @admin_password.setter
    def admin_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98687c5c406324072fbb3e8a7ed943c64db8639c322c3f9e35bc3c79b05e5473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="adminUsername")
    def admin_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminUsername"))

    @admin_username.setter
    def admin_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba8cb5aa489162f13f1df94331a62354a777fc3a551edc64da71e423f153f4e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="computerNamePrefix")
    def computer_name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computerNamePrefix"))

    @computer_name_prefix.setter
    def computer_name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ea8916bedefccceafd03ae33a5d15be7835e3894378361f07e22d87cf40c90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computerNamePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disablePasswordAuthentication")
    def disable_password_authentication(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disablePasswordAuthentication"))

    @disable_password_authentication.setter
    def disable_password_authentication(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__501cfea71e2be65d7c409ba890e13719fb2e469278cd7d571b5b18b575ca7afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disablePasswordAuthentication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="patchAssessmentMode")
    def patch_assessment_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "patchAssessmentMode"))

    @patch_assessment_mode.setter
    def patch_assessment_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee171e087543e736430fe23211d96a9b5a83d0826e067c4aefcc3d274e7c41e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "patchAssessmentMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="patchMode")
    def patch_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "patchMode"))

    @patch_mode.setter
    def patch_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20424fd37a6c5552ce6813b4e6bc1e85f9ffa1f6b1cde1518d026e66603e4f8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "patchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionVmAgent")
    def provision_vm_agent(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "provisionVmAgent"))

    @provision_vm_agent.setter
    def provision_vm_agent(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3254336637187915e08e4a98ab5d8759e2cc9332463ba082328db7f385c471f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionVmAgent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfiguration]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a79e1299f6cdffec5b4856294f2e1192178be78eaae54ca2c880d3e79fb94c22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret",
    jsii_struct_bases=[],
    name_mapping={"certificate": "certificate", "key_vault_id": "keyVaultId"},
)
class OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret:
    def __init__(
        self,
        *,
        certificate: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate", typing.Dict[builtins.str, typing.Any]]]],
        key_vault_id: builtins.str,
    ) -> None:
        '''
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#certificate OrchestratedVirtualMachineScaleSet#certificate}
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#key_vault_id OrchestratedVirtualMachineScaleSet#key_vault_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__054ce969d04a6c8350f5f8e6ee048c9a40f9aa71d384dd84e0bd687bf81a45b0)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate": certificate,
            "key_vault_id": key_vault_id,
        }

    @builtins.property
    def certificate(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate"]]:
        '''certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#certificate OrchestratedVirtualMachineScaleSet#certificate}
        '''
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate"]], result)

    @builtins.property
    def key_vault_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#key_vault_id OrchestratedVirtualMachineScaleSet#key_vault_id}.'''
        result = self._values.get("key_vault_id")
        assert result is not None, "Required property 'key_vault_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate",
    jsii_struct_bases=[],
    name_mapping={"url": "url"},
)
class OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate:
    def __init__(self, *, url: builtins.str) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#url OrchestratedVirtualMachineScaleSet#url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72f3f479fef772d3e2dd12ff9f1da99b278cdc7984c1b120afff425090e75ba8)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#url OrchestratedVirtualMachineScaleSet#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71f303340cb7402c4fbb794b3405ee8e32db4f3acb93af497ef90ef5141fa82a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e50e856679add2dd86188129b7674d76a26f6a8b1b6b1d7d813d032b834529)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a9ba427972a5a1c79764ec84fde0b3453feb988887c82f1c982a9c94359e22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76e780ca12fb7e60f70d280b1aacb74d0406ba4263af47ce8c41a57f0736bc04)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d408f8ab0fc4ffd4edd2194da04a199d6102ad5b7863ab57e8374d10c22c5f56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__297769fadea8546d80a8b8ac65f9201611a31e339698fc10aaae9d548a83a8f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__becf8073bbcf93c9e41c560773051b954b617adba2f11cc6e4a75515fbb8bc15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b32c19bfb672d5f75612c4216ee4e3bbf293ded2655cf2b01035ac1e6c1d09f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__483b61bdf2c937bc182bf5652bfea99520bdeac968b2ba3c18e6bc1c0630dcae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a40f99f5249de1f1c32e052378346ffc01f7d88cd963890c75e2a6ed3e3e295)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e2c4cb9efa7073204ecaaed31336e8db2fb4ba686bfa6f9d2091287072bd34c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df15b345fbd9fd53502ed49b9f0571e99040cf4f9376f2c4ac9d33204ba262c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f33edd15a4be4715792badaf8ffb5a59ac2b8400cba66a36f3c4a5e59005fc89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69114c37d80c73c0051f0e1e2c87b1d4998e45a3205251db3f45c8fb37e6af7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de01847416357430bc9900126eb6f6d448e6462cb2eff27604ab137645653c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9615ea539855fbfcb6373991139adb01da6715b14482bf90f8c87752b56f4f80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCertificate")
    def put_certificate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb8f08a5f32a24e8ce399402992918b11de5f20a44ad803192d2ec43998e54c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCertificate", [value]))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(
        self,
    ) -> OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificateList:
        return typing.cast(OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificateList, jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate]]], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultIdInput")
    def key_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultId")
    def key_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultId"))

    @key_vault_id.setter
    def key_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ca909b6bf0dba149eafdf117cce7bfbb43773e5639f7d54f482ec4c5952502)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__206519535460cc18c9937242a46f8c3a28dd69458a88ced96ca4a7b10aff5e3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetOsProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfa24715257c008df41fd7ad02c339e1b6e4711d59e72bc79cdafed4157b9706)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLinuxConfiguration")
    def put_linux_configuration(
        self,
        *,
        admin_username: builtins.str,
        admin_password: typing.Optional[builtins.str] = None,
        admin_ssh_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
        computer_name_prefix: typing.Optional[builtins.str] = None,
        disable_password_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        patch_assessment_mode: typing.Optional[builtins.str] = None,
        patch_mode: typing.Optional[builtins.str] = None,
        provision_vm_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param admin_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#admin_username OrchestratedVirtualMachineScaleSet#admin_username}.
        :param admin_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#admin_password OrchestratedVirtualMachineScaleSet#admin_password}.
        :param admin_ssh_key: admin_ssh_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#admin_ssh_key OrchestratedVirtualMachineScaleSet#admin_ssh_key}
        :param computer_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#computer_name_prefix OrchestratedVirtualMachineScaleSet#computer_name_prefix}.
        :param disable_password_authentication: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#disable_password_authentication OrchestratedVirtualMachineScaleSet#disable_password_authentication}.
        :param patch_assessment_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#patch_assessment_mode OrchestratedVirtualMachineScaleSet#patch_assessment_mode}.
        :param patch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#patch_mode OrchestratedVirtualMachineScaleSet#patch_mode}.
        :param provision_vm_agent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#provision_vm_agent OrchestratedVirtualMachineScaleSet#provision_vm_agent}.
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#secret OrchestratedVirtualMachineScaleSet#secret}
        '''
        value = OrchestratedVirtualMachineScaleSetOsProfileLinuxConfiguration(
            admin_username=admin_username,
            admin_password=admin_password,
            admin_ssh_key=admin_ssh_key,
            computer_name_prefix=computer_name_prefix,
            disable_password_authentication=disable_password_authentication,
            patch_assessment_mode=patch_assessment_mode,
            patch_mode=patch_mode,
            provision_vm_agent=provision_vm_agent,
            secret=secret,
        )

        return typing.cast(None, jsii.invoke(self, "putLinuxConfiguration", [value]))

    @jsii.member(jsii_name="putWindowsConfiguration")
    def put_windows_configuration(
        self,
        *,
        admin_password: builtins.str,
        admin_username: builtins.str,
        additional_unattend_content: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent", typing.Dict[builtins.str, typing.Any]]]]] = None,
        computer_name_prefix: typing.Optional[builtins.str] = None,
        enable_automatic_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hotpatching_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        patch_assessment_mode: typing.Optional[builtins.str] = None,
        patch_mode: typing.Optional[builtins.str] = None,
        provision_vm_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timezone: typing.Optional[builtins.str] = None,
        winrm_listener: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param admin_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#admin_password OrchestratedVirtualMachineScaleSet#admin_password}.
        :param admin_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#admin_username OrchestratedVirtualMachineScaleSet#admin_username}.
        :param additional_unattend_content: additional_unattend_content block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#additional_unattend_content OrchestratedVirtualMachineScaleSet#additional_unattend_content}
        :param computer_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#computer_name_prefix OrchestratedVirtualMachineScaleSet#computer_name_prefix}.
        :param enable_automatic_updates: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#enable_automatic_updates OrchestratedVirtualMachineScaleSet#enable_automatic_updates}.
        :param hotpatching_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#hotpatching_enabled OrchestratedVirtualMachineScaleSet#hotpatching_enabled}.
        :param patch_assessment_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#patch_assessment_mode OrchestratedVirtualMachineScaleSet#patch_assessment_mode}.
        :param patch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#patch_mode OrchestratedVirtualMachineScaleSet#patch_mode}.
        :param provision_vm_agent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#provision_vm_agent OrchestratedVirtualMachineScaleSet#provision_vm_agent}.
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#secret OrchestratedVirtualMachineScaleSet#secret}
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#timezone OrchestratedVirtualMachineScaleSet#timezone}.
        :param winrm_listener: winrm_listener block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#winrm_listener OrchestratedVirtualMachineScaleSet#winrm_listener}
        '''
        value = OrchestratedVirtualMachineScaleSetOsProfileWindowsConfiguration(
            admin_password=admin_password,
            admin_username=admin_username,
            additional_unattend_content=additional_unattend_content,
            computer_name_prefix=computer_name_prefix,
            enable_automatic_updates=enable_automatic_updates,
            hotpatching_enabled=hotpatching_enabled,
            patch_assessment_mode=patch_assessment_mode,
            patch_mode=patch_mode,
            provision_vm_agent=provision_vm_agent,
            secret=secret,
            timezone=timezone,
            winrm_listener=winrm_listener,
        )

        return typing.cast(None, jsii.invoke(self, "putWindowsConfiguration", [value]))

    @jsii.member(jsii_name="resetCustomData")
    def reset_custom_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomData", []))

    @jsii.member(jsii_name="resetLinuxConfiguration")
    def reset_linux_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinuxConfiguration", []))

    @jsii.member(jsii_name="resetWindowsConfiguration")
    def reset_windows_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowsConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="linuxConfiguration")
    def linux_configuration(
        self,
    ) -> OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationOutputReference:
        return typing.cast(OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationOutputReference, jsii.get(self, "linuxConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="windowsConfiguration")
    def windows_configuration(
        self,
    ) -> "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationOutputReference":
        return typing.cast("OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationOutputReference", jsii.get(self, "windowsConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="customDataInput")
    def custom_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customDataInput"))

    @builtins.property
    @jsii.member(jsii_name="linuxConfigurationInput")
    def linux_configuration_input(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfiguration]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfiguration], jsii.get(self, "linuxConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsConfigurationInput")
    def windows_configuration_input(
        self,
    ) -> typing.Optional["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfiguration"]:
        return typing.cast(typing.Optional["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfiguration"], jsii.get(self, "windowsConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="customData")
    def custom_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customData"))

    @custom_data.setter
    def custom_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d937114de282a2bd890f55f1e31657abf741ff1a394bbc7eb0530bb15c0f7610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetOsProfile]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetOsProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrchestratedVirtualMachineScaleSetOsProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff3c7a75b2464e267ce39a4455950fc0ce438b0c681ebf003f4d36c1ee1fa445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileWindowsConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "admin_password": "adminPassword",
        "admin_username": "adminUsername",
        "additional_unattend_content": "additionalUnattendContent",
        "computer_name_prefix": "computerNamePrefix",
        "enable_automatic_updates": "enableAutomaticUpdates",
        "hotpatching_enabled": "hotpatchingEnabled",
        "patch_assessment_mode": "patchAssessmentMode",
        "patch_mode": "patchMode",
        "provision_vm_agent": "provisionVmAgent",
        "secret": "secret",
        "timezone": "timezone",
        "winrm_listener": "winrmListener",
    },
)
class OrchestratedVirtualMachineScaleSetOsProfileWindowsConfiguration:
    def __init__(
        self,
        *,
        admin_password: builtins.str,
        admin_username: builtins.str,
        additional_unattend_content: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent", typing.Dict[builtins.str, typing.Any]]]]] = None,
        computer_name_prefix: typing.Optional[builtins.str] = None,
        enable_automatic_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hotpatching_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        patch_assessment_mode: typing.Optional[builtins.str] = None,
        patch_mode: typing.Optional[builtins.str] = None,
        provision_vm_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timezone: typing.Optional[builtins.str] = None,
        winrm_listener: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param admin_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#admin_password OrchestratedVirtualMachineScaleSet#admin_password}.
        :param admin_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#admin_username OrchestratedVirtualMachineScaleSet#admin_username}.
        :param additional_unattend_content: additional_unattend_content block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#additional_unattend_content OrchestratedVirtualMachineScaleSet#additional_unattend_content}
        :param computer_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#computer_name_prefix OrchestratedVirtualMachineScaleSet#computer_name_prefix}.
        :param enable_automatic_updates: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#enable_automatic_updates OrchestratedVirtualMachineScaleSet#enable_automatic_updates}.
        :param hotpatching_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#hotpatching_enabled OrchestratedVirtualMachineScaleSet#hotpatching_enabled}.
        :param patch_assessment_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#patch_assessment_mode OrchestratedVirtualMachineScaleSet#patch_assessment_mode}.
        :param patch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#patch_mode OrchestratedVirtualMachineScaleSet#patch_mode}.
        :param provision_vm_agent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#provision_vm_agent OrchestratedVirtualMachineScaleSet#provision_vm_agent}.
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#secret OrchestratedVirtualMachineScaleSet#secret}
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#timezone OrchestratedVirtualMachineScaleSet#timezone}.
        :param winrm_listener: winrm_listener block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#winrm_listener OrchestratedVirtualMachineScaleSet#winrm_listener}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__988b44d0c470cf35e19a409e19851cee15a08d7937fa7c3c34720083831622e2)
            check_type(argname="argument admin_password", value=admin_password, expected_type=type_hints["admin_password"])
            check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
            check_type(argname="argument additional_unattend_content", value=additional_unattend_content, expected_type=type_hints["additional_unattend_content"])
            check_type(argname="argument computer_name_prefix", value=computer_name_prefix, expected_type=type_hints["computer_name_prefix"])
            check_type(argname="argument enable_automatic_updates", value=enable_automatic_updates, expected_type=type_hints["enable_automatic_updates"])
            check_type(argname="argument hotpatching_enabled", value=hotpatching_enabled, expected_type=type_hints["hotpatching_enabled"])
            check_type(argname="argument patch_assessment_mode", value=patch_assessment_mode, expected_type=type_hints["patch_assessment_mode"])
            check_type(argname="argument patch_mode", value=patch_mode, expected_type=type_hints["patch_mode"])
            check_type(argname="argument provision_vm_agent", value=provision_vm_agent, expected_type=type_hints["provision_vm_agent"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            check_type(argname="argument winrm_listener", value=winrm_listener, expected_type=type_hints["winrm_listener"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_password": admin_password,
            "admin_username": admin_username,
        }
        if additional_unattend_content is not None:
            self._values["additional_unattend_content"] = additional_unattend_content
        if computer_name_prefix is not None:
            self._values["computer_name_prefix"] = computer_name_prefix
        if enable_automatic_updates is not None:
            self._values["enable_automatic_updates"] = enable_automatic_updates
        if hotpatching_enabled is not None:
            self._values["hotpatching_enabled"] = hotpatching_enabled
        if patch_assessment_mode is not None:
            self._values["patch_assessment_mode"] = patch_assessment_mode
        if patch_mode is not None:
            self._values["patch_mode"] = patch_mode
        if provision_vm_agent is not None:
            self._values["provision_vm_agent"] = provision_vm_agent
        if secret is not None:
            self._values["secret"] = secret
        if timezone is not None:
            self._values["timezone"] = timezone
        if winrm_listener is not None:
            self._values["winrm_listener"] = winrm_listener

    @builtins.property
    def admin_password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#admin_password OrchestratedVirtualMachineScaleSet#admin_password}.'''
        result = self._values.get("admin_password")
        assert result is not None, "Required property 'admin_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#admin_username OrchestratedVirtualMachineScaleSet#admin_username}.'''
        result = self._values.get("admin_username")
        assert result is not None, "Required property 'admin_username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_unattend_content(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent"]]]:
        '''additional_unattend_content block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#additional_unattend_content OrchestratedVirtualMachineScaleSet#additional_unattend_content}
        '''
        result = self._values.get("additional_unattend_content")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent"]]], result)

    @builtins.property
    def computer_name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#computer_name_prefix OrchestratedVirtualMachineScaleSet#computer_name_prefix}.'''
        result = self._values.get("computer_name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_automatic_updates(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#enable_automatic_updates OrchestratedVirtualMachineScaleSet#enable_automatic_updates}.'''
        result = self._values.get("enable_automatic_updates")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hotpatching_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#hotpatching_enabled OrchestratedVirtualMachineScaleSet#hotpatching_enabled}.'''
        result = self._values.get("hotpatching_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def patch_assessment_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#patch_assessment_mode OrchestratedVirtualMachineScaleSet#patch_assessment_mode}.'''
        result = self._values.get("patch_assessment_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def patch_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#patch_mode OrchestratedVirtualMachineScaleSet#patch_mode}.'''
        result = self._values.get("patch_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provision_vm_agent(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#provision_vm_agent OrchestratedVirtualMachineScaleSet#provision_vm_agent}.'''
        result = self._values.get("provision_vm_agent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secret(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret"]]]:
        '''secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#secret OrchestratedVirtualMachineScaleSet#secret}
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret"]]], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#timezone OrchestratedVirtualMachineScaleSet#timezone}.'''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def winrm_listener(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener"]]]:
        '''winrm_listener block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#winrm_listener OrchestratedVirtualMachineScaleSet#winrm_listener}
        '''
        result = self._values.get("winrm_listener")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "setting": "setting"},
)
class OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent:
    def __init__(self, *, content: builtins.str, setting: builtins.str) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#content OrchestratedVirtualMachineScaleSet#content}.
        :param setting: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#setting OrchestratedVirtualMachineScaleSet#setting}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__769d4052ccd6f87d75ff7f31e2ca2050f557fd00d6c12d3f0d79a69a36869d80)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument setting", value=setting, expected_type=type_hints["setting"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "setting": setting,
        }

    @builtins.property
    def content(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#content OrchestratedVirtualMachineScaleSet#content}.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def setting(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#setting OrchestratedVirtualMachineScaleSet#setting}.'''
        result = self._values.get("setting")
        assert result is not None, "Required property 'setting' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c40e1ba7749130505b03ce34cc5872bb0a7afac4fc19418e017192afe19beeeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fcf09bdface6f796740997a5a88a936ca07176cbc7e994e57cf66554e71a54e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebadc82f703aee4f2b40c5e7105235e733cea6690a9644c1d248c7db5d08130b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__114d810244873f81b2f9dd579a3625d171a6cade11c84795dc9bcaf3d55c112b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85a798a949b58e221e252d879b71a6d02040c2daf2209aa2f0fb23c2abc0735d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdaa5847f542cd6ad2ca2eb674742a9e9b59319ecda1273ba7784da11ed646e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf72b0347e6e7cfe7dd8a0d3191d33eef49535c665bf67e27085d75aece2b5eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="settingInput")
    def setting_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "settingInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4032291aa9a3469352e5fbcc64afd50199b9dfa4b95a47c1e848c3245f4cdd1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="setting")
    def setting(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "setting"))

    @setting.setter
    def setting(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd92ce7ac98f69e412c180129597b2a6df65c22bf5e2c3568821a55ee7ddfd32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "setting", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__871d6513fae1374920c38eca87674d1504f283fe2477a9af4dfe5a44740ad7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__422acc1e02d5a56d41fb8e84037308a331a7fe75d35e2b7b3c301d3b02ec8c62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalUnattendContent")
    def put_additional_unattend_content(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80a53ef56162b7c85fe19e1c242cb8cc4d3d5313402d64386c1176d1d5ef5758)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalUnattendContent", [value]))

    @jsii.member(jsii_name="putSecret")
    def put_secret(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701df14dd68e37e017ee3d6f63f534214cc981cead2d81f0d9929d0bf6009124)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecret", [value]))

    @jsii.member(jsii_name="putWinrmListener")
    def put_winrm_listener(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a14b7c98d31dc048a31cbd5e234aedf932e7418c33b115afcffdef2f87019c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWinrmListener", [value]))

    @jsii.member(jsii_name="resetAdditionalUnattendContent")
    def reset_additional_unattend_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalUnattendContent", []))

    @jsii.member(jsii_name="resetComputerNamePrefix")
    def reset_computer_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputerNamePrefix", []))

    @jsii.member(jsii_name="resetEnableAutomaticUpdates")
    def reset_enable_automatic_updates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAutomaticUpdates", []))

    @jsii.member(jsii_name="resetHotpatchingEnabled")
    def reset_hotpatching_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHotpatchingEnabled", []))

    @jsii.member(jsii_name="resetPatchAssessmentMode")
    def reset_patch_assessment_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPatchAssessmentMode", []))

    @jsii.member(jsii_name="resetPatchMode")
    def reset_patch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPatchMode", []))

    @jsii.member(jsii_name="resetProvisionVmAgent")
    def reset_provision_vm_agent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionVmAgent", []))

    @jsii.member(jsii_name="resetSecret")
    def reset_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecret", []))

    @jsii.member(jsii_name="resetTimezone")
    def reset_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimezone", []))

    @jsii.member(jsii_name="resetWinrmListener")
    def reset_winrm_listener(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWinrmListener", []))

    @builtins.property
    @jsii.member(jsii_name="additionalUnattendContent")
    def additional_unattend_content(
        self,
    ) -> OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContentList:
        return typing.cast(OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContentList, jsii.get(self, "additionalUnattendContent"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(
        self,
    ) -> "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretList":
        return typing.cast("OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretList", jsii.get(self, "secret"))

    @builtins.property
    @jsii.member(jsii_name="winrmListener")
    def winrm_listener(
        self,
    ) -> "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListenerList":
        return typing.cast("OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListenerList", jsii.get(self, "winrmListener"))

    @builtins.property
    @jsii.member(jsii_name="additionalUnattendContentInput")
    def additional_unattend_content_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent]]], jsii.get(self, "additionalUnattendContentInput"))

    @builtins.property
    @jsii.member(jsii_name="adminPasswordInput")
    def admin_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="adminUsernameInput")
    def admin_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="computerNamePrefixInput")
    def computer_name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computerNamePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAutomaticUpdatesInput")
    def enable_automatic_updates_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableAutomaticUpdatesInput"))

    @builtins.property
    @jsii.member(jsii_name="hotpatchingEnabledInput")
    def hotpatching_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hotpatchingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="patchAssessmentModeInput")
    def patch_assessment_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patchAssessmentModeInput"))

    @builtins.property
    @jsii.member(jsii_name="patchModeInput")
    def patch_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionVmAgentInput")
    def provision_vm_agent_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "provisionVmAgentInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret"]]], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="winrmListenerInput")
    def winrm_listener_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener"]]], jsii.get(self, "winrmListenerInput"))

    @builtins.property
    @jsii.member(jsii_name="adminPassword")
    def admin_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminPassword"))

    @admin_password.setter
    def admin_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b70b784f41808aab8cbc2855942a81fafddfa76e024dc43b4d7ffcc336e1a60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="adminUsername")
    def admin_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminUsername"))

    @admin_username.setter
    def admin_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea5dec36ef77a2c756ce372b28efa1a4f5059137d7f3d02b9511e39fc851a2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="computerNamePrefix")
    def computer_name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computerNamePrefix"))

    @computer_name_prefix.setter
    def computer_name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d3e13f0140e356ab085c909e367d8b15d3b8665c51326a593ace448a3760d4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computerNamePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableAutomaticUpdates")
    def enable_automatic_updates(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableAutomaticUpdates"))

    @enable_automatic_updates.setter
    def enable_automatic_updates(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ad0b181bfe202736e2cbce219d0ea33c28b78251412e22a4d97aada5285afb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAutomaticUpdates", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hotpatchingEnabled")
    def hotpatching_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hotpatchingEnabled"))

    @hotpatching_enabled.setter
    def hotpatching_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b07d3d8eb6648c2439d76969e46144f133135f7d59b76c6a33d19cab559b7c96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hotpatchingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="patchAssessmentMode")
    def patch_assessment_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "patchAssessmentMode"))

    @patch_assessment_mode.setter
    def patch_assessment_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e202f7de32da1362c2c1a092c37b43be8ad6a8ff0b4d94667ad802c5ff4effc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "patchAssessmentMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="patchMode")
    def patch_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "patchMode"))

    @patch_mode.setter
    def patch_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74014a8eb70b0775001247cff0730ea7164639ffc042ca5f1c7e4331a7d7a876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "patchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionVmAgent")
    def provision_vm_agent(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "provisionVmAgent"))

    @provision_vm_agent.setter
    def provision_vm_agent(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7366deffdc557631832c72724473175e7331924bc58b0e5831d66117ad847a83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionVmAgent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d095b32fa3f8054a24f3c0e92ff6251c527db19083bfeb9b86d06f885deae19b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfiguration]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd7c035607f3d65769e228784cd2a8a92b010d34d0df8b7bd743cb5589cd222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret",
    jsii_struct_bases=[],
    name_mapping={"certificate": "certificate", "key_vault_id": "keyVaultId"},
)
class OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret:
    def __init__(
        self,
        *,
        certificate: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate", typing.Dict[builtins.str, typing.Any]]]],
        key_vault_id: builtins.str,
    ) -> None:
        '''
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#certificate OrchestratedVirtualMachineScaleSet#certificate}
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#key_vault_id OrchestratedVirtualMachineScaleSet#key_vault_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826165f22325c6146bdf60a52177288bfe10bff5703c93a1fc8a53b364f40aea)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate": certificate,
            "key_vault_id": key_vault_id,
        }

    @builtins.property
    def certificate(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate"]]:
        '''certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#certificate OrchestratedVirtualMachineScaleSet#certificate}
        '''
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate"]], result)

    @builtins.property
    def key_vault_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#key_vault_id OrchestratedVirtualMachineScaleSet#key_vault_id}.'''
        result = self._values.get("key_vault_id")
        assert result is not None, "Required property 'key_vault_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate",
    jsii_struct_bases=[],
    name_mapping={"store": "store", "url": "url"},
)
class OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate:
    def __init__(self, *, store: builtins.str, url: builtins.str) -> None:
        '''
        :param store: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#store OrchestratedVirtualMachineScaleSet#store}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#url OrchestratedVirtualMachineScaleSet#url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9acf2b4cce7cdac235eedce6f2c48547246e0c70976619f4433c50cb4c9b129)
            check_type(argname="argument store", value=store, expected_type=type_hints["store"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "store": store,
            "url": url,
        }

    @builtins.property
    def store(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#store OrchestratedVirtualMachineScaleSet#store}.'''
        result = self._values.get("store")
        assert result is not None, "Required property 'store' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#url OrchestratedVirtualMachineScaleSet#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9d2d22ad53cf10ab50d657114614e4ce4db5d90a47e9d0c6a3b21e2029691df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dff855ee61364c4581ebb688424428c85b8a0997572905aa396d1c11fe707d9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc0729518f72d15f2806f302546a2a6a9a55734f555cf148f58b2aaeba444db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d58e6eb4b4028d05c0f672e30a36ee0f8363737907c35aee7693bca59042f46b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be7da5932fd4f40ab662c6223db1498a6433440113a78cc7f13cac2d5dc7b85c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3acdc2f672e155ce94461674faa7ee85af918f79ea79173a27657270a3807cea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a35130c78886a2359ff000e66694d223013a6487a451ab06029d88de187081b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="storeInput")
    def store_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storeInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "store"))

    @store.setter
    def store(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c29eb899aca15787df953beeacd346b0b8ac1847e4dc7ac76ae788b80dc5c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "store", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e14efeab39130f60188502bba190f66124d865554a1fb0082553de81454a9f41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a76c6ae47d43947376de6bf1004a0d6a7165ff407283d91bc42c261d5c60197f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f81bbe6044c2f8c0eb360ebd2654467b475fcc5f811cb662c5c1c5b44caa563)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc10c0104a14dfedfede667a72358d6de6b590dc43307321245d3af7e1c38c59)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0df993155735b6f90b77279f142ae92ad7c48e6a94ce13b2352deab800edea8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c386c17ce2dd3aff363c25a4d4d7841895d5919b9bf1db367cf538b8272db1e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c40991d1a8711c546c6347d55ccca79b06e390f2371d67f9bd66bc0332cd9883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff7453b93f5c05c97aec5f7842f685813c2c4a259cb75ac4b311efe24cccebe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae350eaf97b3e1ecf4b7768b1bdc0fc03d9c16d00bdfc1d1023836a88f71109c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCertificate")
    def put_certificate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c13a5dbac2a6d2e57f7f7a3edb1231416270b74e86bacc83d6465aabbf14da6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCertificate", [value]))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(
        self,
    ) -> OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificateList:
        return typing.cast(OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificateList, jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate]]], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultIdInput")
    def key_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultId")
    def key_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultId"))

    @key_vault_id.setter
    def key_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb23ffbdb59c4a882e8f5f5b1b86e576210548025caf481c1c95227e3d4c5fa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab587eb41099caccfa822225e9c61bd394ed595edf28face7022695f9db7df7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener",
    jsii_struct_bases=[],
    name_mapping={"protocol": "protocol", "certificate_url": "certificateUrl"},
)
class OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener:
    def __init__(
        self,
        *,
        protocol: builtins.str,
        certificate_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#protocol OrchestratedVirtualMachineScaleSet#protocol}.
        :param certificate_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#certificate_url OrchestratedVirtualMachineScaleSet#certificate_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a176fb40770015a7da77594914d84446a32f29e6ef4fcd63943a968d22fc3c)
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument certificate_url", value=certificate_url, expected_type=type_hints["certificate_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "protocol": protocol,
        }
        if certificate_url is not None:
            self._values["certificate_url"] = certificate_url

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#protocol OrchestratedVirtualMachineScaleSet#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#certificate_url OrchestratedVirtualMachineScaleSet#certificate_url}.'''
        result = self._values.get("certificate_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListenerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListenerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae173619755fcc6b723cef84c8250bedfacb9acba832b68704bcda0a3424236e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListenerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0afaf7cd27f0cddaf880e2a25279d2698b814328fde5e68adb7c5b741031705e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListenerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0d7cd855d2c51a03fc45cb34cfd271c02cb1e97e718a3c9b0f1ac72d6fc1fce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3b71e7acec70ab8916952f30c96e1ebf8bd5348f630c6fa835a0c4ad94d4446)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75db382037c41fb58603b2b949dc382ac818a93b971dd1376b839c5d156c8354)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a8d2622e1a17fa3434782e1577afa085bed24d05f9e6540ff64b802640251ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListenerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListenerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d2080f9df7de5bede9ad68408d2169c76c65bfb80c59a86156f01df381ce46d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCertificateUrl")
    def reset_certificate_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateUrl", []))

    @builtins.property
    @jsii.member(jsii_name="certificateUrlInput")
    def certificate_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateUrl")
    def certificate_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateUrl"))

    @certificate_url.setter
    def certificate_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b72f0aae242849e76fc09a6fb748f3709c2ba797d8d717f1f3fcc5810f9d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9786b8f98ec0f5ae52a9ef56a13eec8f2cfa12c026ffc390b1c7b400498a04d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0472d49b1c31ef5a54fdf10587fd1a8e7c56c2dc0e36d807cefcca44c99be1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetPlan",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "product": "product", "publisher": "publisher"},
)
class OrchestratedVirtualMachineScaleSetPlan:
    def __init__(
        self,
        *,
        name: builtins.str,
        product: builtins.str,
        publisher: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#name OrchestratedVirtualMachineScaleSet#name}.
        :param product: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#product OrchestratedVirtualMachineScaleSet#product}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#publisher OrchestratedVirtualMachineScaleSet#publisher}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__735b94acf60ac1519ff80684faa76da16b37c559fb64bc7a96d6bfc38882971f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "product": product,
            "publisher": publisher,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#name OrchestratedVirtualMachineScaleSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#product OrchestratedVirtualMachineScaleSet#product}.'''
        result = self._values.get("product")
        assert result is not None, "Required property 'product' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def publisher(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#publisher OrchestratedVirtualMachineScaleSet#publisher}.'''
        result = self._values.get("publisher")
        assert result is not None, "Required property 'publisher' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetPlan(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetPlanOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetPlanOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd566051bf3f37ad60a854243334e498a5b183874a6d14f801b672f2345a6568)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="productInput")
    def product_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "productInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherInput")
    def publisher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52358ac313866abd2d98a8f4164401b3a9de60d3dca636bf1aceefb8d87428cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="product")
    def product(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "product"))

    @product.setter
    def product(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4499e248d53386eaa2766c162da5649b87398fabcf2df358b9c1e65f78541545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "product", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisher"))

    @publisher.setter
    def publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fd50e4d9a65b6665c3342a01f69e5b835749df94632b9778d0a3374bd6fc484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrchestratedVirtualMachineScaleSetPlan]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetPlan], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrchestratedVirtualMachineScaleSetPlan],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aac438a44400748b8d4521672917280aff69d2d6accea77270771681fd30b2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetPriorityMix",
    jsii_struct_bases=[],
    name_mapping={
        "base_regular_count": "baseRegularCount",
        "regular_percentage_above_base": "regularPercentageAboveBase",
    },
)
class OrchestratedVirtualMachineScaleSetPriorityMix:
    def __init__(
        self,
        *,
        base_regular_count: typing.Optional[jsii.Number] = None,
        regular_percentage_above_base: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param base_regular_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#base_regular_count OrchestratedVirtualMachineScaleSet#base_regular_count}.
        :param regular_percentage_above_base: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#regular_percentage_above_base OrchestratedVirtualMachineScaleSet#regular_percentage_above_base}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b204e14d112f996e4cb9d906ec52fcb59489ac4c0c58b14ce88a1ca49459603)
            check_type(argname="argument base_regular_count", value=base_regular_count, expected_type=type_hints["base_regular_count"])
            check_type(argname="argument regular_percentage_above_base", value=regular_percentage_above_base, expected_type=type_hints["regular_percentage_above_base"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if base_regular_count is not None:
            self._values["base_regular_count"] = base_regular_count
        if regular_percentage_above_base is not None:
            self._values["regular_percentage_above_base"] = regular_percentage_above_base

    @builtins.property
    def base_regular_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#base_regular_count OrchestratedVirtualMachineScaleSet#base_regular_count}.'''
        result = self._values.get("base_regular_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def regular_percentage_above_base(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#regular_percentage_above_base OrchestratedVirtualMachineScaleSet#regular_percentage_above_base}.'''
        result = self._values.get("regular_percentage_above_base")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetPriorityMix(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetPriorityMixOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetPriorityMixOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dded1a31cb47e9cc3501c4cdbd8680bac22e20e4e54507e2d35ce4aec4201b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBaseRegularCount")
    def reset_base_regular_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseRegularCount", []))

    @jsii.member(jsii_name="resetRegularPercentageAboveBase")
    def reset_regular_percentage_above_base(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegularPercentageAboveBase", []))

    @builtins.property
    @jsii.member(jsii_name="baseRegularCountInput")
    def base_regular_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "baseRegularCountInput"))

    @builtins.property
    @jsii.member(jsii_name="regularPercentageAboveBaseInput")
    def regular_percentage_above_base_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "regularPercentageAboveBaseInput"))

    @builtins.property
    @jsii.member(jsii_name="baseRegularCount")
    def base_regular_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "baseRegularCount"))

    @base_regular_count.setter
    def base_regular_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef3ebea8d3c0c8565adf6f794d4029e7cf5c02b923e00286c7d82e2d075a4e45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseRegularCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regularPercentageAboveBase")
    def regular_percentage_above_base(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "regularPercentageAboveBase"))

    @regular_percentage_above_base.setter
    def regular_percentage_above_base(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__090e4950eaa5d1d89d547f7ff3bf90fffd9f2bcc524d1e34103619df4b8147f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regularPercentageAboveBase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetPriorityMix]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetPriorityMix], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrchestratedVirtualMachineScaleSetPriorityMix],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff7aeceeb53c904a5d567c25e24d3120a3d23912700f0c1e3ef3e1d6b542abc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetRollingUpgradePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "max_batch_instance_percent": "maxBatchInstancePercent",
        "max_unhealthy_instance_percent": "maxUnhealthyInstancePercent",
        "max_unhealthy_upgraded_instance_percent": "maxUnhealthyUpgradedInstancePercent",
        "pause_time_between_batches": "pauseTimeBetweenBatches",
        "cross_zone_upgrades_enabled": "crossZoneUpgradesEnabled",
        "maximum_surge_instances_enabled": "maximumSurgeInstancesEnabled",
        "prioritize_unhealthy_instances_enabled": "prioritizeUnhealthyInstancesEnabled",
    },
)
class OrchestratedVirtualMachineScaleSetRollingUpgradePolicy:
    def __init__(
        self,
        *,
        max_batch_instance_percent: jsii.Number,
        max_unhealthy_instance_percent: jsii.Number,
        max_unhealthy_upgraded_instance_percent: jsii.Number,
        pause_time_between_batches: builtins.str,
        cross_zone_upgrades_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        maximum_surge_instances_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prioritize_unhealthy_instances_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param max_batch_instance_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#max_batch_instance_percent OrchestratedVirtualMachineScaleSet#max_batch_instance_percent}.
        :param max_unhealthy_instance_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#max_unhealthy_instance_percent OrchestratedVirtualMachineScaleSet#max_unhealthy_instance_percent}.
        :param max_unhealthy_upgraded_instance_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#max_unhealthy_upgraded_instance_percent OrchestratedVirtualMachineScaleSet#max_unhealthy_upgraded_instance_percent}.
        :param pause_time_between_batches: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#pause_time_between_batches OrchestratedVirtualMachineScaleSet#pause_time_between_batches}.
        :param cross_zone_upgrades_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#cross_zone_upgrades_enabled OrchestratedVirtualMachineScaleSet#cross_zone_upgrades_enabled}.
        :param maximum_surge_instances_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#maximum_surge_instances_enabled OrchestratedVirtualMachineScaleSet#maximum_surge_instances_enabled}.
        :param prioritize_unhealthy_instances_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#prioritize_unhealthy_instances_enabled OrchestratedVirtualMachineScaleSet#prioritize_unhealthy_instances_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a58b98a9cecc31fa75dcd1d299b0f94c45383c62d3b875674cfb795a7b115a7c)
            check_type(argname="argument max_batch_instance_percent", value=max_batch_instance_percent, expected_type=type_hints["max_batch_instance_percent"])
            check_type(argname="argument max_unhealthy_instance_percent", value=max_unhealthy_instance_percent, expected_type=type_hints["max_unhealthy_instance_percent"])
            check_type(argname="argument max_unhealthy_upgraded_instance_percent", value=max_unhealthy_upgraded_instance_percent, expected_type=type_hints["max_unhealthy_upgraded_instance_percent"])
            check_type(argname="argument pause_time_between_batches", value=pause_time_between_batches, expected_type=type_hints["pause_time_between_batches"])
            check_type(argname="argument cross_zone_upgrades_enabled", value=cross_zone_upgrades_enabled, expected_type=type_hints["cross_zone_upgrades_enabled"])
            check_type(argname="argument maximum_surge_instances_enabled", value=maximum_surge_instances_enabled, expected_type=type_hints["maximum_surge_instances_enabled"])
            check_type(argname="argument prioritize_unhealthy_instances_enabled", value=prioritize_unhealthy_instances_enabled, expected_type=type_hints["prioritize_unhealthy_instances_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_batch_instance_percent": max_batch_instance_percent,
            "max_unhealthy_instance_percent": max_unhealthy_instance_percent,
            "max_unhealthy_upgraded_instance_percent": max_unhealthy_upgraded_instance_percent,
            "pause_time_between_batches": pause_time_between_batches,
        }
        if cross_zone_upgrades_enabled is not None:
            self._values["cross_zone_upgrades_enabled"] = cross_zone_upgrades_enabled
        if maximum_surge_instances_enabled is not None:
            self._values["maximum_surge_instances_enabled"] = maximum_surge_instances_enabled
        if prioritize_unhealthy_instances_enabled is not None:
            self._values["prioritize_unhealthy_instances_enabled"] = prioritize_unhealthy_instances_enabled

    @builtins.property
    def max_batch_instance_percent(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#max_batch_instance_percent OrchestratedVirtualMachineScaleSet#max_batch_instance_percent}.'''
        result = self._values.get("max_batch_instance_percent")
        assert result is not None, "Required property 'max_batch_instance_percent' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_unhealthy_instance_percent(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#max_unhealthy_instance_percent OrchestratedVirtualMachineScaleSet#max_unhealthy_instance_percent}.'''
        result = self._values.get("max_unhealthy_instance_percent")
        assert result is not None, "Required property 'max_unhealthy_instance_percent' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_unhealthy_upgraded_instance_percent(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#max_unhealthy_upgraded_instance_percent OrchestratedVirtualMachineScaleSet#max_unhealthy_upgraded_instance_percent}.'''
        result = self._values.get("max_unhealthy_upgraded_instance_percent")
        assert result is not None, "Required property 'max_unhealthy_upgraded_instance_percent' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def pause_time_between_batches(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#pause_time_between_batches OrchestratedVirtualMachineScaleSet#pause_time_between_batches}.'''
        result = self._values.get("pause_time_between_batches")
        assert result is not None, "Required property 'pause_time_between_batches' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cross_zone_upgrades_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#cross_zone_upgrades_enabled OrchestratedVirtualMachineScaleSet#cross_zone_upgrades_enabled}.'''
        result = self._values.get("cross_zone_upgrades_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def maximum_surge_instances_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#maximum_surge_instances_enabled OrchestratedVirtualMachineScaleSet#maximum_surge_instances_enabled}.'''
        result = self._values.get("maximum_surge_instances_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prioritize_unhealthy_instances_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#prioritize_unhealthy_instances_enabled OrchestratedVirtualMachineScaleSet#prioritize_unhealthy_instances_enabled}.'''
        result = self._values.get("prioritize_unhealthy_instances_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetRollingUpgradePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetRollingUpgradePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetRollingUpgradePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7d0aaf5b4c4d2989f80a8079ea20b9c60564a42e0a9a5ddf7af51e4c8195eae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCrossZoneUpgradesEnabled")
    def reset_cross_zone_upgrades_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossZoneUpgradesEnabled", []))

    @jsii.member(jsii_name="resetMaximumSurgeInstancesEnabled")
    def reset_maximum_surge_instances_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumSurgeInstancesEnabled", []))

    @jsii.member(jsii_name="resetPrioritizeUnhealthyInstancesEnabled")
    def reset_prioritize_unhealthy_instances_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrioritizeUnhealthyInstancesEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="crossZoneUpgradesEnabledInput")
    def cross_zone_upgrades_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "crossZoneUpgradesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="maxBatchInstancePercentInput")
    def max_batch_instance_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBatchInstancePercentInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumSurgeInstancesEnabledInput")
    def maximum_surge_instances_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "maximumSurgeInstancesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUnhealthyInstancePercentInput")
    def max_unhealthy_instance_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUnhealthyInstancePercentInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUnhealthyUpgradedInstancePercentInput")
    def max_unhealthy_upgraded_instance_percent_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUnhealthyUpgradedInstancePercentInput"))

    @builtins.property
    @jsii.member(jsii_name="pauseTimeBetweenBatchesInput")
    def pause_time_between_batches_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pauseTimeBetweenBatchesInput"))

    @builtins.property
    @jsii.member(jsii_name="prioritizeUnhealthyInstancesEnabledInput")
    def prioritize_unhealthy_instances_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "prioritizeUnhealthyInstancesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="crossZoneUpgradesEnabled")
    def cross_zone_upgrades_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "crossZoneUpgradesEnabled"))

    @cross_zone_upgrades_enabled.setter
    def cross_zone_upgrades_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0170f1f34e1d4a53b43c1cac65550414eb0b90e5e7dd6a26e88830b5b344be5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossZoneUpgradesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxBatchInstancePercent")
    def max_batch_instance_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxBatchInstancePercent"))

    @max_batch_instance_percent.setter
    def max_batch_instance_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c801b943811eac062071e8864865a4ac1ca97845c0bb9472019bf54c30f66103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBatchInstancePercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumSurgeInstancesEnabled")
    def maximum_surge_instances_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "maximumSurgeInstancesEnabled"))

    @maximum_surge_instances_enabled.setter
    def maximum_surge_instances_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5518f914adbd34e7a2bd0a705a01d637ef5506cf7b5b80f6036381da6789c7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumSurgeInstancesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUnhealthyInstancePercent")
    def max_unhealthy_instance_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnhealthyInstancePercent"))

    @max_unhealthy_instance_percent.setter
    def max_unhealthy_instance_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3c99f4a90a6af45fac1d7f26fe36ac9d87fb85a6027c1a4e6e9030bccc5af94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnhealthyInstancePercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUnhealthyUpgradedInstancePercent")
    def max_unhealthy_upgraded_instance_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnhealthyUpgradedInstancePercent"))

    @max_unhealthy_upgraded_instance_percent.setter
    def max_unhealthy_upgraded_instance_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a43c510e0345ca7c07f54ad935240ac0b0354c725e440eecba24c0de57694c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnhealthyUpgradedInstancePercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pauseTimeBetweenBatches")
    def pause_time_between_batches(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pauseTimeBetweenBatches"))

    @pause_time_between_batches.setter
    def pause_time_between_batches(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df85e2d52558b475a0d62fdf489c8f5f6031f9a19fbff0cfc9cd79a8cacdf1da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pauseTimeBetweenBatches", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prioritizeUnhealthyInstancesEnabled")
    def prioritize_unhealthy_instances_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "prioritizeUnhealthyInstancesEnabled"))

    @prioritize_unhealthy_instances_enabled.setter
    def prioritize_unhealthy_instances_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdc9af0364ac00a747c16831614c29091ba99b46c0289a2e45cbf15a8948929e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prioritizeUnhealthyInstancesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetRollingUpgradePolicy]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetRollingUpgradePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrchestratedVirtualMachineScaleSetRollingUpgradePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61005ca01602209a4a2b34f389307ae401cdb534d6e7b4f7c57a31f139798370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetSkuProfile",
    jsii_struct_bases=[],
    name_mapping={"allocation_strategy": "allocationStrategy", "vm_sizes": "vmSizes"},
)
class OrchestratedVirtualMachineScaleSetSkuProfile:
    def __init__(
        self,
        *,
        allocation_strategy: builtins.str,
        vm_sizes: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param allocation_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#allocation_strategy OrchestratedVirtualMachineScaleSet#allocation_strategy}.
        :param vm_sizes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#vm_sizes OrchestratedVirtualMachineScaleSet#vm_sizes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff8b236977890621b8a98df8f47ed016b15f01dc267577ed102228fc2c01f15c)
            check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
            check_type(argname="argument vm_sizes", value=vm_sizes, expected_type=type_hints["vm_sizes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allocation_strategy": allocation_strategy,
            "vm_sizes": vm_sizes,
        }

    @builtins.property
    def allocation_strategy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#allocation_strategy OrchestratedVirtualMachineScaleSet#allocation_strategy}.'''
        result = self._values.get("allocation_strategy")
        assert result is not None, "Required property 'allocation_strategy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_sizes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#vm_sizes OrchestratedVirtualMachineScaleSet#vm_sizes}.'''
        result = self._values.get("vm_sizes")
        assert result is not None, "Required property 'vm_sizes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetSkuProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetSkuProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetSkuProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1e21451b45a430ed2a82ac9222a0a638df7c220916bcf7e30614cb8ba15e8eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="allocationStrategyInput")
    def allocation_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allocationStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSizesInput")
    def vm_sizes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "vmSizesInput"))

    @builtins.property
    @jsii.member(jsii_name="allocationStrategy")
    def allocation_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allocationStrategy"))

    @allocation_strategy.setter
    def allocation_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24ed840ddc8d9548e2c9ae7a8bc0da2a74c60c321118d9eca4956c00c2d45b23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocationStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSizes")
    def vm_sizes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vmSizes"))

    @vm_sizes.setter
    def vm_sizes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62f967fc1eaffbcd2c4e412941ef09940c582e67b39cde3ff6518c2c4edc9556)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSizes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetSkuProfile]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetSkuProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrchestratedVirtualMachineScaleSetSkuProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d481db8fa1b0dd9d519138896b88e2ec5bc5ad433562fe85abcc96cb66cab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetSourceImageReference",
    jsii_struct_bases=[],
    name_mapping={
        "offer": "offer",
        "publisher": "publisher",
        "sku": "sku",
        "version": "version",
    },
)
class OrchestratedVirtualMachineScaleSetSourceImageReference:
    def __init__(
        self,
        *,
        offer: builtins.str,
        publisher: builtins.str,
        sku: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param offer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#offer OrchestratedVirtualMachineScaleSet#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#publisher OrchestratedVirtualMachineScaleSet#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#sku OrchestratedVirtualMachineScaleSet#sku}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#version OrchestratedVirtualMachineScaleSet#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f7466fa15dd13412e4f5ec7798e74b3658d301010fc9f26c8b38e219a05b380)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#offer OrchestratedVirtualMachineScaleSet#offer}.'''
        result = self._values.get("offer")
        assert result is not None, "Required property 'offer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def publisher(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#publisher OrchestratedVirtualMachineScaleSet#publisher}.'''
        result = self._values.get("publisher")
        assert result is not None, "Required property 'publisher' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sku(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#sku OrchestratedVirtualMachineScaleSet#sku}.'''
        result = self._values.get("sku")
        assert result is not None, "Required property 'sku' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#version OrchestratedVirtualMachineScaleSet#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetSourceImageReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetSourceImageReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetSourceImageReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ca410b699df20c026cffa43a1babc39e8a03804bb5121e6009d2823070e1908)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51c6e3fba9b6ef0a2638c0244de2c6285a4c3be5f8dd7aa07f9ed6102ce21b58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisher"))

    @publisher.setter
    def publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cad971e6d72dea04970ae30a55a7619dccceaefde1e0dceb3b896e5f656e732e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d674672d300137aafc5c187998d689697e6da95cc3631dd58e3d67f65efad8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6548f2d0d914e01d8c588ba8b327660fcfbccb9e0c237e4fb9e76d3923c9e44e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetSourceImageReference]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetSourceImageReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrchestratedVirtualMachineScaleSetSourceImageReference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441996ceb08fe17a26492d9364171d6772569061a20f0061611949cc49613314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetTerminationNotification",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "timeout": "timeout"},
)
class OrchestratedVirtualMachineScaleSetTerminationNotification:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#enabled OrchestratedVirtualMachineScaleSet#enabled}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#timeout OrchestratedVirtualMachineScaleSet#timeout}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61cdfb160be8a9898bc9e5f9bbd430633f2b2a5223f3a1696dcdff0bc939f9d8)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#enabled OrchestratedVirtualMachineScaleSet#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#timeout OrchestratedVirtualMachineScaleSet#timeout}.'''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetTerminationNotification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetTerminationNotificationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetTerminationNotificationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fec6ac32bcc5400d94dbfd969722a59b3a187fa347246ff7a2b9927a448f00d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcbf67176b62e95e67f04fa4b394cae2e0dac1f0e111a3e05e2c4b095fbd3260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fb2ef774a6624305fcde82675cb6a8847af62a23a605ac9f47b7afe2aa3aecc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrchestratedVirtualMachineScaleSetTerminationNotification]:
        return typing.cast(typing.Optional[OrchestratedVirtualMachineScaleSetTerminationNotification], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrchestratedVirtualMachineScaleSetTerminationNotification],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e236bd3b6993994fd54662a35ee712bfa78b62e21200ea1e42b405e4f02669f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class OrchestratedVirtualMachineScaleSetTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#create OrchestratedVirtualMachineScaleSet#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#delete OrchestratedVirtualMachineScaleSet#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#read OrchestratedVirtualMachineScaleSet#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#update OrchestratedVirtualMachineScaleSet#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9751597143ce26825f87029a076f81a19065df31dd4bb798e458cf40ac4d1d0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#create OrchestratedVirtualMachineScaleSet#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#delete OrchestratedVirtualMachineScaleSet#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#read OrchestratedVirtualMachineScaleSet#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orchestrated_virtual_machine_scale_set#update OrchestratedVirtualMachineScaleSet#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrchestratedVirtualMachineScaleSetTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrchestratedVirtualMachineScaleSetTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orchestratedVirtualMachineScaleSet.OrchestratedVirtualMachineScaleSetTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__775e7ec7a76e65ad3a843b1890a0467cce9539d01b82b2d6ddfd393e60270214)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f1b39d051f67967df3ca65c58b7d1622986ef2216384331f7ff08f0251b0059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b5328df40ca78b131db750e310228a37b888cc7fb000058cdd89772ab4a22eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__391921f2abd84cc0026c1600b41df86477f428f617e51ba35c5f8639a1f759be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfcb0334fc6fe834ef5420f4c14f34b3c459e92b8c2065fc4902a81e6fe32176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc00f9d89951aa8327353a15270a9117774e74ac2bf48f7c3cd26224873cef0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OrchestratedVirtualMachineScaleSet",
    "OrchestratedVirtualMachineScaleSetAdditionalCapabilities",
    "OrchestratedVirtualMachineScaleSetAdditionalCapabilitiesOutputReference",
    "OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair",
    "OrchestratedVirtualMachineScaleSetAutomaticInstanceRepairOutputReference",
    "OrchestratedVirtualMachineScaleSetBootDiagnostics",
    "OrchestratedVirtualMachineScaleSetBootDiagnosticsOutputReference",
    "OrchestratedVirtualMachineScaleSetConfig",
    "OrchestratedVirtualMachineScaleSetDataDisk",
    "OrchestratedVirtualMachineScaleSetDataDiskList",
    "OrchestratedVirtualMachineScaleSetDataDiskOutputReference",
    "OrchestratedVirtualMachineScaleSetExtension",
    "OrchestratedVirtualMachineScaleSetExtensionList",
    "OrchestratedVirtualMachineScaleSetExtensionOutputReference",
    "OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVault",
    "OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVaultOutputReference",
    "OrchestratedVirtualMachineScaleSetIdentity",
    "OrchestratedVirtualMachineScaleSetIdentityOutputReference",
    "OrchestratedVirtualMachineScaleSetNetworkInterface",
    "OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration",
    "OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationList",
    "OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationOutputReference",
    "OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress",
    "OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag",
    "OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTagList",
    "OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTagOutputReference",
    "OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressList",
    "OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressOutputReference",
    "OrchestratedVirtualMachineScaleSetNetworkInterfaceList",
    "OrchestratedVirtualMachineScaleSetNetworkInterfaceOutputReference",
    "OrchestratedVirtualMachineScaleSetOsDisk",
    "OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettings",
    "OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettingsOutputReference",
    "OrchestratedVirtualMachineScaleSetOsDiskOutputReference",
    "OrchestratedVirtualMachineScaleSetOsProfile",
    "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfiguration",
    "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey",
    "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKeyList",
    "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKeyOutputReference",
    "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationOutputReference",
    "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret",
    "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate",
    "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificateList",
    "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificateOutputReference",
    "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretList",
    "OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretOutputReference",
    "OrchestratedVirtualMachineScaleSetOsProfileOutputReference",
    "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfiguration",
    "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent",
    "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContentList",
    "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContentOutputReference",
    "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationOutputReference",
    "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret",
    "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate",
    "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificateList",
    "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificateOutputReference",
    "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretList",
    "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretOutputReference",
    "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener",
    "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListenerList",
    "OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListenerOutputReference",
    "OrchestratedVirtualMachineScaleSetPlan",
    "OrchestratedVirtualMachineScaleSetPlanOutputReference",
    "OrchestratedVirtualMachineScaleSetPriorityMix",
    "OrchestratedVirtualMachineScaleSetPriorityMixOutputReference",
    "OrchestratedVirtualMachineScaleSetRollingUpgradePolicy",
    "OrchestratedVirtualMachineScaleSetRollingUpgradePolicyOutputReference",
    "OrchestratedVirtualMachineScaleSetSkuProfile",
    "OrchestratedVirtualMachineScaleSetSkuProfileOutputReference",
    "OrchestratedVirtualMachineScaleSetSourceImageReference",
    "OrchestratedVirtualMachineScaleSetSourceImageReferenceOutputReference",
    "OrchestratedVirtualMachineScaleSetTerminationNotification",
    "OrchestratedVirtualMachineScaleSetTerminationNotificationOutputReference",
    "OrchestratedVirtualMachineScaleSetTimeouts",
    "OrchestratedVirtualMachineScaleSetTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__cd134486e9eea1733710a1ad9b3371fb284f2bbb6d5dddb862feee8176b9d2e5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    platform_fault_domain_count: jsii.Number,
    resource_group_name: builtins.str,
    additional_capabilities: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetAdditionalCapabilities, typing.Dict[builtins.str, typing.Any]]] = None,
    automatic_instance_repair: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair, typing.Dict[builtins.str, typing.Any]]] = None,
    boot_diagnostics: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetBootDiagnostics, typing.Dict[builtins.str, typing.Any]]] = None,
    capacity_reservation_group_id: typing.Optional[builtins.str] = None,
    data_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetDataDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    eviction_policy: typing.Optional[builtins.str] = None,
    extension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetExtension, typing.Dict[builtins.str, typing.Any]]]]] = None,
    extension_operations_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    extensions_time_budget: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    instances: typing.Optional[jsii.Number] = None,
    license_type: typing.Optional[builtins.str] = None,
    max_bid_price: typing.Optional[jsii.Number] = None,
    network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetNetworkInterface, typing.Dict[builtins.str, typing.Any]]]]] = None,
    os_disk: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    os_profile: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetOsProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    plan: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetPlan, typing.Dict[builtins.str, typing.Any]]] = None,
    priority: typing.Optional[builtins.str] = None,
    priority_mix: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetPriorityMix, typing.Dict[builtins.str, typing.Any]]] = None,
    proximity_placement_group_id: typing.Optional[builtins.str] = None,
    rolling_upgrade_policy: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetRollingUpgradePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    single_placement_group: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sku_name: typing.Optional[builtins.str] = None,
    sku_profile: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetSkuProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    source_image_id: typing.Optional[builtins.str] = None,
    source_image_reference: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_notification: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetTerminationNotification, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_mode: typing.Optional[builtins.str] = None,
    user_data_base64: typing.Optional[builtins.str] = None,
    zone_balance: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__ce22f67369d675014b04b83ecdeb94876d3dfe53d699d1d3228614e3331bf080(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5de5c17225494ab626364f2f0ebc184a341c157c6eeac32f172a314f0b5c9e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetDataDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d68feae112eaa798000ba2554c32a555540e2f783258fa45d0d72a0bae9366(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetExtension, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f24fc99ec3fb45bea7dda5ce573a551f1336fe2298c2e835706f19cc3156328(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetNetworkInterface, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14226bdf55f885eed35158fa9cbf0b6b4686ec5e26aa29a0ce4bf5c4e0c6350d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647856b4a6cc3d676a57689f4d2673b5a94b82188300b655b348568f870bb55c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f3b641d0267eb8675d02cf2ffc3224139184f1d3522dac61fa8a7be2097662(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da28b9a503930744e4d6f1d6959fbbe246cf678c4cabbced41d618bc7bcd55b9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__011b33db25aa4be45155c8ce1c260534031d9d691a651b683a00322f015dc135(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee7289995d803fef88b77fa209c45754a2bcc16639125e052ebc3c197990080d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2a48ca653a3e61310bbfdac8ad8712d048841c2e05d2fa6f54852a4c8a268b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd75caa81ad5d30c639d0ecc20f1662dcef91dfdcabd4e841470e4e69baefd43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ee77803b27621457cfa2a535b90fbb90c23e4aa1c5c6043ce0d3a598a7aea4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6266b726b6a7837cab8cb45a17503bc6970aa7092ccf98bdebf0b3ad065370(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26f1718a2da33d3fa86ea2512249b2d1363fbdeb9c8107b2387dd66d4eec1007(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716c59427f0515500fe0e517c2e7ca0e06b3826db1674f5c887e04ae9d2143fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3518ecc085c9959fff5b01ae51dfe966831f99251a6c5dfc7d2fc999cc8f9f62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f71d62a19b040f21304db08d3458928cb94a84cb751668e5c5097fb27321df9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323cd1b99ef793a997ac65f54a6c31bd79a294b05b5bff0d735584a46c5cce6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49aa2c9e82d5263f1d9928090b6884d6487c6747b5f000e61ae8c9fce4c19519(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2350d293179c47593f2bfd76c2d822bf81c27057f21e0b12df86fda77114c445(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fd4ef20a04a61fbfac4ecef73976402a57e1df891c40bbd43f223bed520b9f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e549815ef23a6c391304a566aec901429288311bd60ef671caa87436530a68(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8adb266befe1147edb244f204dba8ec83e9db951015c2be4927f74b2ebe37af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76da02c86134f24a4d50f175d329ba31fbddd900baf4638c4cbfac31484727e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b7578b0c1af6acae58e09fe1f9347c2ae6bbd5dba72fb3a1ca2c05098b8fb9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063b79d7cd130a070821287afece19d01acdf384f023aa4440d5ca4d17114036(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433e18491c3caca0b3b94cd4132e101f6a47519677c5f1a55a8580935b85af23(
    *,
    ultra_ssd_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1183583eb02d461fe8ecf48c887946ac1326e42da6348eff6a2835a27a5a6b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6644af3013ac94098965397b682974f087ef58177cc9593e1229f593e1061b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f35a2f9c16bc7daf5ab641a2f2805862d3e464f653be01b056f251c6564d79ad(
    value: typing.Optional[OrchestratedVirtualMachineScaleSetAdditionalCapabilities],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd8de20577085a936e8deee94a9fd7fb90452737de64fa96e20a82a90654362(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    action: typing.Optional[builtins.str] = None,
    grace_period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__368a3c1b86ceff713aedb358fffa75fecde0dc0bfe7b101107cf3127287dd849(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaad2969d653f44891428e60975021aeed9d1dcc282a18546379ac56eb6bbd49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede52e9cf251a50895c73b508ae414a2b1eae5a69001ac31e173b5929e1da4f6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d1fe644fe3503f5f996fd3e18b0e302f93903fd4802d271f3769fe47217842d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3641ef2aaa11cf79ef891300f15398b3548521b2001381b45c68abbe297dadce(
    value: typing.Optional[OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4301a129c36033fbffe3a12d7301310968c4b2b40cc4538d614543e1573e20f(
    *,
    storage_account_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__022b5065d84fa9e0a7f884baf2f8acb583577680582eec092713f7e11e97fda9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03ebfd44930bd8a7e338849414919b8d78367350eb102a7cc45586be6f966fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b49f19e054c8f9f6496f2c4b390d3023029daed45abf363a5bfb07cfe381af(
    value: typing.Optional[OrchestratedVirtualMachineScaleSetBootDiagnostics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3618a83d9bd003d9eb504271e72a26410e135280507b06c2b6cc3c41e38b4db(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    platform_fault_domain_count: jsii.Number,
    resource_group_name: builtins.str,
    additional_capabilities: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetAdditionalCapabilities, typing.Dict[builtins.str, typing.Any]]] = None,
    automatic_instance_repair: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetAutomaticInstanceRepair, typing.Dict[builtins.str, typing.Any]]] = None,
    boot_diagnostics: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetBootDiagnostics, typing.Dict[builtins.str, typing.Any]]] = None,
    capacity_reservation_group_id: typing.Optional[builtins.str] = None,
    data_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetDataDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    eviction_policy: typing.Optional[builtins.str] = None,
    extension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetExtension, typing.Dict[builtins.str, typing.Any]]]]] = None,
    extension_operations_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    extensions_time_budget: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    instances: typing.Optional[jsii.Number] = None,
    license_type: typing.Optional[builtins.str] = None,
    max_bid_price: typing.Optional[jsii.Number] = None,
    network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetNetworkInterface, typing.Dict[builtins.str, typing.Any]]]]] = None,
    os_disk: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    os_profile: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetOsProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    plan: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetPlan, typing.Dict[builtins.str, typing.Any]]] = None,
    priority: typing.Optional[builtins.str] = None,
    priority_mix: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetPriorityMix, typing.Dict[builtins.str, typing.Any]]] = None,
    proximity_placement_group_id: typing.Optional[builtins.str] = None,
    rolling_upgrade_policy: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetRollingUpgradePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    single_placement_group: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sku_name: typing.Optional[builtins.str] = None,
    sku_profile: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetSkuProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    source_image_id: typing.Optional[builtins.str] = None,
    source_image_reference: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_notification: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetTerminationNotification, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_mode: typing.Optional[builtins.str] = None,
    user_data_base64: typing.Optional[builtins.str] = None,
    zone_balance: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a714e2df2258705dcbbe01fb1100abacfdd8f5fa612205a70d0e2c3b9e895a4(
    *,
    caching: builtins.str,
    storage_account_type: builtins.str,
    create_option: typing.Optional[builtins.str] = None,
    disk_encryption_set_id: typing.Optional[builtins.str] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    lun: typing.Optional[jsii.Number] = None,
    ultra_ssd_disk_iops_read_write: typing.Optional[jsii.Number] = None,
    ultra_ssd_disk_mbps_read_write: typing.Optional[jsii.Number] = None,
    write_accelerator_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f2efea5d49219b0f6434062205d59a7f177a5e5fb2f53bc1d93ffc773615b62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__341d5207ab740ad37e780a10f7182b8e419a3f8c345345dc283b0531fea004e0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783d035e45a4db7210867b515d8f4f8c84a7d106fd07bc19c8b3e78019f3dcb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b56433e26aecb5a4618aa16169f7f41a4e49e1fc6fbcf76dae0113cddedd0fa0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195b29312f2f0b759ebef845de17f8ad67c2651db037b19e752372208a1c11da(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0420d2d4e8ea4cea189032278ad2fc69b9c24b4c3c90c17e71f8293724793ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetDataDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e5e614e4c8fbb7e34cd33fd2cf2ca19d98da15d0eafbb67b5adce2557a8e48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f1482b2237e8b47690a5009818716ba687f13733d4bbbcb2605eb322fc7e4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ceaaf7f6456856dbfcc0349c8d448c5c9ace45515ed62eca19017b066cf700(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a348080d69648abac7ad08a752595b21948b044dd17703257e04501bacfada(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f8b11319949eaedf885253b31b4a47818983b2297fe2f84e30198b20a84e390(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1db950446fe47b9f3b4ba4f624f9e9e6fc2b171705a2bf570df7ec61d9a5b59(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846fca0cf7361f927a9a6b0dbc3ce252f09516ee3ea0043258004230997e8f86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5f77c494854ac75944100bdf7ecb92a321b79a6904d3086d2e876a71739f03(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3b54b03b7d1654089e6ad2b4347e8d4d170e1ea2504018096ecd5005ebd461(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333b43cf0cd633e49f049e612cd22f1ad52b6fc8e26b6c76e410aeb14bc4d905(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a557db9cd5a2aafc256cc26554f2051357d049907a3818c73ea81f3f4a535260(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetDataDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7cff06c3e3bb9b387beeb7836f0b6ae51a4ad13597ae9889743caa69ca943eb(
    *,
    name: builtins.str,
    publisher: builtins.str,
    type: builtins.str,
    type_handler_version: builtins.str,
    auto_upgrade_minor_version_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    extensions_to_provision_after_vm_creation: typing.Optional[typing.Sequence[builtins.str]] = None,
    failure_suppression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    force_extension_execution_on_change: typing.Optional[builtins.str] = None,
    protected_settings: typing.Optional[builtins.str] = None,
    protected_settings_from_key_vault: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVault, typing.Dict[builtins.str, typing.Any]]] = None,
    settings: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f409adfdb8056a8d9893847cb2f4626d93e7b7ff590501a6375c8283f40442ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f987ed450913e2dce79fd3d1c73bc5888ce1b8d0a77e4f9bec60e321a5860f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b8a8997087b467b297e480d5441a7b7847de86a42a123e9dc48086d99e1a3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b956e97285317d8e3b8dc87092d14537bba14bfd9cc8c4e6d5a6adbb1abab7cc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dad7274eb6cb956f1785452cbfcecb070fc5e4242e80c816edd0c15caf1fa34(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d49e39bed1328875fb80a8e11c161fd2c13ea73bd7eea71cb2f177b342b03a8a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetExtension]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98af37116fdbf54765b43832e59c14820edb18f95931ff6a809ed1a1e35f9305(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b9b7e71d569a8a6625aa81d3b30ea809f23249a8dc3c8ee9bb04c5ae9a1e21(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b700d19cb46c4c86d7162fe218761d91abe81fbf58cb97283a21ddcb9a63e70(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e89a33bd084a7518224f42fa114c18b31e7345c1dafffb7908bf310d0428e2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8cc45085fd0bafd85538030b37a67ecb9b02b4953325f682d76d86ff70861fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ace08426412e9572f53e9fe0e6619dc12fb08d0d1f0fc2d0c3f17ff07fb891e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05eda88338f72d5da04eecfafaa56a0e457ed7f2b6ad86b3870e4f8f976a3970(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef4f946a59311920616adb70dfcf53ac13c253146e228ac1d9b2ff4b01cc7e66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828efe1149ed32a12ceb0a749f48e0eb7a376be8035d29b91fe4441422360573(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32eb68f244ef92d49392ed4f992e184b18d8008f87eaec8d965c29df4bed71c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06eb964ed683bada6ca4a12d88406e19449b17991f4f241ad943ec46f886b028(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce77053e1de458e6dd4b6c028b7ba053de43b71eeaae33e9376058b678f6fb48(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetExtension]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7afe578da8943494d5e77d30f77fde07283c583d707f01c6e861d85ef9b28e(
    *,
    secret_url: builtins.str,
    source_vault_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1bd007d5f14857c587ddd72dcb09dda2f317cbbbf9020691df7fcd63544a89(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32ba669e679387b4087d37508489203df9731b8e27a108e883188c4c5eee887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394fddac6dbf431131bb61265df7fbfe57b70447543794130917ff5d9a255efa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bffa8b0cebdb2861b6477431707fe1905e2c1d100d25c0524a70ec9dd49d051a(
    value: typing.Optional[OrchestratedVirtualMachineScaleSetExtensionProtectedSettingsFromKeyVault],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c899d4e834c265e558ef037ca78528306e0e63d5fb8f9ed2077de869eee6c208(
    *,
    identity_ids: typing.Sequence[builtins.str],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63280706381ad1e6a2bc1f2b8f3571b2cb8dcd08396ea11ad1f1e28b2bb83a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f320b6049f4669a4c3707983fe297724af22173e578f9a3e78f33c62aab580(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f896031045c219c2e5fbb530f5c05fccdbfbf21c60ec8f893c154ba8e10f26c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca20ead7a88e94723bac9b3564d6526c2aa480acf0c1d9bf5542bf0d89508e1(
    value: typing.Optional[OrchestratedVirtualMachineScaleSetIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1c17d92aa5daf1b2f35d6781c7067e1336908001c073abf4c13df8dbe6abe11(
    *,
    ip_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_accelerated_networking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_ip_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network_security_group_id: typing.Optional[builtins.str] = None,
    primary: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__268f5ebd5a664895433e8fde830786bb07b1807a44266d81790cea62864413f8(
    *,
    name: builtins.str,
    application_gateway_backend_address_pool_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    application_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    load_balancer_backend_address_pool_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    primary: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_ip_address: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress, typing.Dict[builtins.str, typing.Any]]]]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb1447a05c197087919937a384ec08f2722c1c5d4dd2c72d2fc6cf495d0c634(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b79ecc63f6f44caf5a856af1d870ae1ea8debaa80d434aa7431d89ea567c6996(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63260e1bedd433ed6db13a0bf3918112316ff1d9049b9619c3fc8c89b168fd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2317c43ec5ae1a1659001e16a11cc0a247aaf8102c3c00c7276b013dd4f88e9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2869ba412e87a3765dfa888362b1587a5bb5bd8ede6ddf5721238dbfc48e57ad(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__713383657af33c5704e89fcd787b45c076d52853527a7b024e14b32cf0da50f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb7c9022e81a661a128fde33b009885a73862d754902eb988a9eaa22c994a4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6740c266c157b0a29fc01cfd7ffefa9ca6d20bef729b9c5d73376576232d6d4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdfb1bb7f171052d8237904a4c79058dfb45149974db5a15d2026e4659c76fef(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b32d8143e8b0e3154434e667d2a8d1d508af47b3dd040dc15a8fc5dce0468f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb8327db691d81b532a819e50d8fd73aa8f0072606614ee7d9945b5907243ffd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e01eb017181b4660cf96d3ec4544ad0455cb829ea8fc1c5800603bd91d4bde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4edce56a415bd77b8528d6e532addac1b8079c3959db7988be401c995308ee63(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ed692875848995e29815e0bc61d0f6bcfd214a00b3db13f9a2e353aa901f07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17e62fd5a406bc37ce9ff887107e774d8e20c23720026fe84b8fdc4017c1b8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17bc5d26f2e5f1036e36c64528c62d0fb9d702648eca8bcb961b44f5fb597391(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c798fc5ca0a00abbd7a1855a73d73feb33138d3a9fd1128852787a128cad63b7(
    *,
    name: builtins.str,
    domain_name_label: typing.Optional[builtins.str] = None,
    idle_timeout_in_minutes: typing.Optional[jsii.Number] = None,
    ip_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
    public_ip_prefix_id: typing.Optional[builtins.str] = None,
    sku_name: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836345d09fb0d43cf0bd3bfd416edca332a28d6ea7be6d9823eb06bcd4ae1269(
    *,
    tag: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b495b5327af44d002129144fb25c3b3bcb1fa49cb5e7e4c8cec39b292784df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac46f162b366ae5995ca49032c7a9cc0e8fb0226f35169ed5bbab9321bce3ae1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff809daecedb8583ae62f84224496995857ff1416d2e9aa4e40e8823ffc16e55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c31202467e6da40f35e02167c50f0ea328e92c5064b84eb99700f39ab6d3c77(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba5d43215306cf4b44d906440f7c505f1a9f3ddd6e8334bdefa2f0772356b04(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3346216a165c6fd6734df661fdfb97d4169863b5b2af7a79f6957d73d173cb3b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f506f403b8e7fac11f6a0dfd3960855efe714ebe188411ce02ed8942144870(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe6b4f6e5d3a08d2a54d66ab3a37dca4c40706469ac7f43f8bd0710b21d8140(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf89cc4a6fda1f4a1f422faefee78e4918504f2a68402573f2e3c566b7aa3b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7615e94a303eb0d8016e0744de0574da7eaab79adcc4b4111c25efdd42b268ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a34c5b3fd60d01d5c018c18694a978d9b288f8bc0a77d829d1c6fee467f86a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53f239aaca722862c26dc353108c8e34d47dc536006df33120dad7456d5ad97(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11c10d31b50464575973513109f34d6a77ef78fc592718d87f0f3fde432e44dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9315710f0b62204a651e49ebe341c3120ce95f2bd15f6e8a96b982eb38da8737(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340b9f5dbfb4758f193e9e04a1afa27802e737e10d2dbae98630767670aae5f7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12c1f038c1db59791913ef6496e5598153447c2093954287880058cf1c527af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8deb6ef39a58782be1bc21bf3e8183bf96370c49fcda2a20a8c30a23744f9c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f3cfec6bbc136615eef00c93e636f743f90a8ad2eb369199cff52e9a1ef2f09(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddressIpTag, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded8af95a7c62b780311c025c33bb18a91cb1f1ddd8a93ec374e086d2a0eec44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84e2b061123503ba90bf4ab8c6cff786600514285ceb59478594474107293f1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44997a13e1a77f20b7f8cbc518a0eec7d6d0c984d02b078f6ae9f36c2c442ff8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9cb7923132d1d00af1ecbb067c945552ae287f77ad925891c39c44640b047b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3e0e87f0b1d4791357b428bf77a2cf6ae44426e187aa10b57484e0ff9c240a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76ea5908cf9f3cc74754c460e05ee7c6656ddd12f0c9c978a5e1f8ccbd26ce8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082dbaddcb65bc35aa3f40266c52f9e0a4f66b5c1b5a48617e67048516e6c81d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c26ec0610f9ff790be83a6cd4f2a49e04fd26e7da23e59ccbf7a752da1d627(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__898b0df05f282bc4aecf51ae9a71ceabd6b8a86e9696857a9bfaa1955636e542(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__384df1b9370605e1e6967d2e0186fe56bd8503088f1c8e8e7cdb2ca123362b4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c1df26c7b97068e569d11c62430a80fbf55415480c2b9aa9a1ad1655635847a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7585b04735a3d2fb3ca40e30b97f57cc026a5cb274387c8ee700b44a248d5dd1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79fa732f52ec97fbba0844b2a67e9ee16df88f431512141644b4cd957a96d751(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetNetworkInterface]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4ed4ead3d99faf388766439bc634902a3ac8b3c22b7ef885ccdcc11671856e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01a75be676afa5889ec76749de461311c8695324b442f7f04b67598882516da(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetNetworkInterfaceIpConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7471bbd07680f0ed44efbc487391bc1f52036dd32ea2725b9c9109434662dc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4fbd9924183db48b09946522d288cb3e1e40a749da7775279b9fc9217b2dd0f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af60615b11a3bf78900cb4b917b27db5f6ff96dd2281f945b05966f84f0ebf0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e697655850f92ef7d1e2f196887de46fd3263a35a0760371acd5c87f69d45c6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2766d011a59f32d05fc8c30d92e4c46fe35a23bbe0222e2a27e03e21d3b6e00a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc37f7745d3727d72b36be07fb895636cbc274290a13e669594d47e60ecf17ea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e70e0ee8622d07f3364bc9f6596214ce6c7ee69255c754bf708f10e47213328(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetNetworkInterface]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c01b5d6f4567ea9538517921d25308cbb84e09122817ff66e5b608fb79576d8e(
    *,
    caching: builtins.str,
    storage_account_type: builtins.str,
    diff_disk_settings: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_encryption_set_id: typing.Optional[builtins.str] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    write_accelerator_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103234cded650a69a0b7980237c0d94c5ab31e083c2e2a9b5e68c1b9f2afe061(
    *,
    option: builtins.str,
    placement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b140aa3ff13a7fd4a5629039feb783906709da04f2d3a550f4a5619ceff6e8de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d531878f3102b767e6ff3d3a50548bbd895ea1cd76f5dd52218d29881cb611b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a9288d2681136a2a9985f258927873c40e75aa2106e10e9eb5cc789a967dea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c674050c249031bf9f61f00a7609f42e0e4a43acd836a496f57fc70e71d3d93(
    value: typing.Optional[OrchestratedVirtualMachineScaleSetOsDiskDiffDiskSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980e2c83e532b8cf5edbe77e05c228cc53c1327618565f70d1c3a10da37071de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcae24fed6b8a83fb4b116e6fb544cbd475cdc35fbb5e34e2e0710e9159c9ac0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d416ac985b1ee8fd46879a128429b0f947e93cbabd3eec56c34a689eae8aa19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958b3664f7ebadc98c250e305e5bb2ee1e6f51a08b105107eb7c2c2870213374(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42bba04b7e9e1c6a46857fb48c34f6760c89eb4e6ed99b8de67521c8c95d68f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d1eddd915c54b97b02be7e07ea623aab96c8b71a5ddbad8b6fe366c05b5f559(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7220e21ef76493650b38a62696ba420441fc77b161a3a1b22e193c0d2d70121b(
    value: typing.Optional[OrchestratedVirtualMachineScaleSetOsDisk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1110dc9bc9155e779a049b64c51218fc6f39580d5406211ce1d2a6a0bb162d6f(
    *,
    custom_data: typing.Optional[builtins.str] = None,
    linux_configuration: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    windows_configuration: typing.Optional[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9d6a91dcc93dd2a4118339f9a49573ff6918e4ee6456423d1a407831ecc3bf(
    *,
    admin_username: builtins.str,
    admin_password: typing.Optional[builtins.str] = None,
    admin_ssh_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
    computer_name_prefix: typing.Optional[builtins.str] = None,
    disable_password_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    patch_assessment_mode: typing.Optional[builtins.str] = None,
    patch_mode: typing.Optional[builtins.str] = None,
    provision_vm_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4d04648b916990dec1ff8390876169d955b4123ea6d66ec0240706ea1fa690(
    *,
    public_key: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40311ef55010b4e0cf1475f5b0a54a86ac0d06a3b4d6b9fe395c0c88c10e46a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91ebc599d07e2b74824113e9d281271389bad8a8fbebcf547b1e451bc031800(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d7ff7bf1b8119eb43f1789fb687ee2f20dc492f5755f076acf4bd551bda4ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__251fc0b26409ec0f25d16db36a2d8b60a9787b9090bdda5fd40eda7e8677a5f1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a268fe6e9c94f5ec734bfebee60f930873495f03c8169ab963a31887dda55733(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2ad284a1b20fc9e495c7e1818b0434e081792c3cd7661a551b9be5c030a0f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d1da6675b2035060bd260c3e9ba993e1bd20adad7cb5c54957ca179bd0bf27d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__147e0c21b840758ecc29b90d21a295b2f11482b3497081640992bb22c9da7231(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77559cfe35fe5aa74b9c407c451405ae48202b2951e0b06d3829bb3c390548fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b463d8974ce63d6be02911e65ccebab2814ae61ad3514ba298e29a2877a858de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2e2601dd7234e5bdcc1001ff102a1b72b34d98882b4b08b583d44fda4bd512(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506c4c39eb2d5b972d2d2f4b482b29f374c659a5ece26c527fcaedfea3fd2a14(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationAdminSshKey, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e702d8f3648f4fafeba236ff5706e3bee4c43405c4fbcc1567cf782df11a02c8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98687c5c406324072fbb3e8a7ed943c64db8639c322c3f9e35bc3c79b05e5473(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8cb5aa489162f13f1df94331a62354a777fc3a551edc64da71e423f153f4e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ea8916bedefccceafd03ae33a5d15be7835e3894378361f07e22d87cf40c90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__501cfea71e2be65d7c409ba890e13719fb2e469278cd7d571b5b18b575ca7afa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee171e087543e736430fe23211d96a9b5a83d0826e067c4aefcc3d274e7c41e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20424fd37a6c5552ce6813b4e6bc1e85f9ffa1f6b1cde1518d026e66603e4f8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3254336637187915e08e4a98ab5d8759e2cc9332463ba082328db7f385c471f8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a79e1299f6cdffec5b4856294f2e1192178be78eaae54ca2c880d3e79fb94c22(
    value: typing.Optional[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054ce969d04a6c8350f5f8e6ee048c9a40f9aa71d384dd84e0bd687bf81a45b0(
    *,
    certificate: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate, typing.Dict[builtins.str, typing.Any]]]],
    key_vault_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f3f479fef772d3e2dd12ff9f1da99b278cdc7984c1b120afff425090e75ba8(
    *,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f303340cb7402c4fbb794b3405ee8e32db4f3acb93af497ef90ef5141fa82a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e50e856679add2dd86188129b7674d76a26f6a8b1b6b1d7d813d032b834529(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a9ba427972a5a1c79764ec84fde0b3453feb988887c82f1c982a9c94359e22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e780ca12fb7e60f70d280b1aacb74d0406ba4263af47ce8c41a57f0736bc04(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d408f8ab0fc4ffd4edd2194da04a199d6102ad5b7863ab57e8374d10c22c5f56(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297769fadea8546d80a8b8ac65f9201611a31e339698fc10aaae9d548a83a8f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__becf8073bbcf93c9e41c560773051b954b617adba2f11cc6e4a75515fbb8bc15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b32c19bfb672d5f75612c4216ee4e3bbf293ded2655cf2b01035ac1e6c1d09f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__483b61bdf2c937bc182bf5652bfea99520bdeac968b2ba3c18e6bc1c0630dcae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a40f99f5249de1f1c32e052378346ffc01f7d88cd963890c75e2a6ed3e3e295(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e2c4cb9efa7073204ecaaed31336e8db2fb4ba686bfa6f9d2091287072bd34c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df15b345fbd9fd53502ed49b9f0571e99040cf4f9376f2c4ac9d33204ba262c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f33edd15a4be4715792badaf8ffb5a59ac2b8400cba66a36f3c4a5e59005fc89(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69114c37d80c73c0051f0e1e2c87b1d4998e45a3205251db3f45c8fb37e6af7b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de01847416357430bc9900126eb6f6d448e6462cb2eff27604ab137645653c4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9615ea539855fbfcb6373991139adb01da6715b14482bf90f8c87752b56f4f80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb8f08a5f32a24e8ce399402992918b11de5f20a44ad803192d2ec43998e54c9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecretCertificate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ca909b6bf0dba149eafdf117cce7bfbb43773e5639f7d54f482ec4c5952502(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__206519535460cc18c9937242a46f8c3a28dd69458a88ced96ca4a7b10aff5e3c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileLinuxConfigurationSecret]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa24715257c008df41fd7ad02c339e1b6e4711d59e72bc79cdafed4157b9706(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d937114de282a2bd890f55f1e31657abf741ff1a394bbc7eb0530bb15c0f7610(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3c7a75b2464e267ce39a4455950fc0ce438b0c681ebf003f4d36c1ee1fa445(
    value: typing.Optional[OrchestratedVirtualMachineScaleSetOsProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__988b44d0c470cf35e19a409e19851cee15a08d7937fa7c3c34720083831622e2(
    *,
    admin_password: builtins.str,
    admin_username: builtins.str,
    additional_unattend_content: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent, typing.Dict[builtins.str, typing.Any]]]]] = None,
    computer_name_prefix: typing.Optional[builtins.str] = None,
    enable_automatic_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hotpatching_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    patch_assessment_mode: typing.Optional[builtins.str] = None,
    patch_mode: typing.Optional[builtins.str] = None,
    provision_vm_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timezone: typing.Optional[builtins.str] = None,
    winrm_listener: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769d4052ccd6f87d75ff7f31e2ca2050f557fd00d6c12d3f0d79a69a36869d80(
    *,
    content: builtins.str,
    setting: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c40e1ba7749130505b03ce34cc5872bb0a7afac4fc19418e017192afe19beeeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fcf09bdface6f796740997a5a88a936ca07176cbc7e994e57cf66554e71a54e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebadc82f703aee4f2b40c5e7105235e733cea6690a9644c1d248c7db5d08130b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114d810244873f81b2f9dd579a3625d171a6cade11c84795dc9bcaf3d55c112b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a798a949b58e221e252d879b71a6d02040c2daf2209aa2f0fb23c2abc0735d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdaa5847f542cd6ad2ca2eb674742a9e9b59319ecda1273ba7784da11ed646e4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf72b0347e6e7cfe7dd8a0d3191d33eef49535c665bf67e27085d75aece2b5eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4032291aa9a3469352e5fbcc64afd50199b9dfa4b95a47c1e848c3245f4cdd1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd92ce7ac98f69e412c180129597b2a6df65c22bf5e2c3568821a55ee7ddfd32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__871d6513fae1374920c38eca87674d1504f283fe2477a9af4dfe5a44740ad7eb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422acc1e02d5a56d41fb8e84037308a331a7fe75d35e2b7b3c301d3b02ec8c62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a53ef56162b7c85fe19e1c242cb8cc4d3d5313402d64386c1176d1d5ef5758(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationAdditionalUnattendContent, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701df14dd68e37e017ee3d6f63f534214cc981cead2d81f0d9929d0bf6009124(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a14b7c98d31dc048a31cbd5e234aedf932e7418c33b115afcffdef2f87019c7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b70b784f41808aab8cbc2855942a81fafddfa76e024dc43b4d7ffcc336e1a60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea5dec36ef77a2c756ce372b28efa1a4f5059137d7f3d02b9511e39fc851a2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3e13f0140e356ab085c909e367d8b15d3b8665c51326a593ace448a3760d4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad0b181bfe202736e2cbce219d0ea33c28b78251412e22a4d97aada5285afb2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07d3d8eb6648c2439d76969e46144f133135f7d59b76c6a33d19cab559b7c96(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e202f7de32da1362c2c1a092c37b43be8ad6a8ff0b4d94667ad802c5ff4effc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74014a8eb70b0775001247cff0730ea7164639ffc042ca5f1c7e4331a7d7a876(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7366deffdc557631832c72724473175e7331924bc58b0e5831d66117ad847a83(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d095b32fa3f8054a24f3c0e92ff6251c527db19083bfeb9b86d06f885deae19b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd7c035607f3d65769e228784cd2a8a92b010d34d0df8b7bd743cb5589cd222(
    value: typing.Optional[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826165f22325c6146bdf60a52177288bfe10bff5703c93a1fc8a53b364f40aea(
    *,
    certificate: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate, typing.Dict[builtins.str, typing.Any]]]],
    key_vault_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9acf2b4cce7cdac235eedce6f2c48547246e0c70976619f4433c50cb4c9b129(
    *,
    store: builtins.str,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d2d22ad53cf10ab50d657114614e4ce4db5d90a47e9d0c6a3b21e2029691df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dff855ee61364c4581ebb688424428c85b8a0997572905aa396d1c11fe707d9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc0729518f72d15f2806f302546a2a6a9a55734f555cf148f58b2aaeba444db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58e6eb4b4028d05c0f672e30a36ee0f8363737907c35aee7693bca59042f46b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be7da5932fd4f40ab662c6223db1498a6433440113a78cc7f13cac2d5dc7b85c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3acdc2f672e155ce94461674faa7ee85af918f79ea79173a27657270a3807cea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a35130c78886a2359ff000e66694d223013a6487a451ab06029d88de187081b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c29eb899aca15787df953beeacd346b0b8ac1847e4dc7ac76ae788b80dc5c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14efeab39130f60188502bba190f66124d865554a1fb0082553de81454a9f41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a76c6ae47d43947376de6bf1004a0d6a7165ff407283d91bc42c261d5c60197f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f81bbe6044c2f8c0eb360ebd2654467b475fcc5f811cb662c5c1c5b44caa563(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc10c0104a14dfedfede667a72358d6de6b590dc43307321245d3af7e1c38c59(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df993155735b6f90b77279f142ae92ad7c48e6a94ce13b2352deab800edea8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c386c17ce2dd3aff363c25a4d4d7841895d5919b9bf1db367cf538b8272db1e1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c40991d1a8711c546c6347d55ccca79b06e390f2371d67f9bd66bc0332cd9883(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff7453b93f5c05c97aec5f7842f685813c2c4a259cb75ac4b311efe24cccebe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae350eaf97b3e1ecf4b7768b1bdc0fc03d9c16d00bdfc1d1023836a88f71109c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c13a5dbac2a6d2e57f7f7a3edb1231416270b74e86bacc83d6465aabbf14da6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecretCertificate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb23ffbdb59c4a882e8f5f5b1b86e576210548025caf481c1c95227e3d4c5fa9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab587eb41099caccfa822225e9c61bd394ed595edf28face7022695f9db7df7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationSecret]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a176fb40770015a7da77594914d84446a32f29e6ef4fcd63943a968d22fc3c(
    *,
    protocol: builtins.str,
    certificate_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae173619755fcc6b723cef84c8250bedfacb9acba832b68704bcda0a3424236e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0afaf7cd27f0cddaf880e2a25279d2698b814328fde5e68adb7c5b741031705e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0d7cd855d2c51a03fc45cb34cfd271c02cb1e97e718a3c9b0f1ac72d6fc1fce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3b71e7acec70ab8916952f30c96e1ebf8bd5348f630c6fa835a0c4ad94d4446(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75db382037c41fb58603b2b949dc382ac818a93b971dd1376b839c5d156c8354(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a8d2622e1a17fa3434782e1577afa085bed24d05f9e6540ff64b802640251ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d2080f9df7de5bede9ad68408d2169c76c65bfb80c59a86156f01df381ce46d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b72f0aae242849e76fc09a6fb748f3709c2ba797d8d717f1f3fcc5810f9d59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9786b8f98ec0f5ae52a9ef56a13eec8f2cfa12c026ffc390b1c7b400498a04d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0472d49b1c31ef5a54fdf10587fd1a8e7c56c2dc0e36d807cefcca44c99be1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetOsProfileWindowsConfigurationWinrmListener]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735b94acf60ac1519ff80684faa76da16b37c559fb64bc7a96d6bfc38882971f(
    *,
    name: builtins.str,
    product: builtins.str,
    publisher: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd566051bf3f37ad60a854243334e498a5b183874a6d14f801b672f2345a6568(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52358ac313866abd2d98a8f4164401b3a9de60d3dca636bf1aceefb8d87428cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4499e248d53386eaa2766c162da5649b87398fabcf2df358b9c1e65f78541545(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fd50e4d9a65b6665c3342a01f69e5b835749df94632b9778d0a3374bd6fc484(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aac438a44400748b8d4521672917280aff69d2d6accea77270771681fd30b2a(
    value: typing.Optional[OrchestratedVirtualMachineScaleSetPlan],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b204e14d112f996e4cb9d906ec52fcb59489ac4c0c58b14ce88a1ca49459603(
    *,
    base_regular_count: typing.Optional[jsii.Number] = None,
    regular_percentage_above_base: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dded1a31cb47e9cc3501c4cdbd8680bac22e20e4e54507e2d35ce4aec4201b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef3ebea8d3c0c8565adf6f794d4029e7cf5c02b923e00286c7d82e2d075a4e45(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090e4950eaa5d1d89d547f7ff3bf90fffd9f2bcc524d1e34103619df4b8147f7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff7aeceeb53c904a5d567c25e24d3120a3d23912700f0c1e3ef3e1d6b542abc4(
    value: typing.Optional[OrchestratedVirtualMachineScaleSetPriorityMix],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58b98a9cecc31fa75dcd1d299b0f94c45383c62d3b875674cfb795a7b115a7c(
    *,
    max_batch_instance_percent: jsii.Number,
    max_unhealthy_instance_percent: jsii.Number,
    max_unhealthy_upgraded_instance_percent: jsii.Number,
    pause_time_between_batches: builtins.str,
    cross_zone_upgrades_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    maximum_surge_instances_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prioritize_unhealthy_instances_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d0aaf5b4c4d2989f80a8079ea20b9c60564a42e0a9a5ddf7af51e4c8195eae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0170f1f34e1d4a53b43c1cac65550414eb0b90e5e7dd6a26e88830b5b344be5a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c801b943811eac062071e8864865a4ac1ca97845c0bb9472019bf54c30f66103(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5518f914adbd34e7a2bd0a705a01d637ef5506cf7b5b80f6036381da6789c7e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c99f4a90a6af45fac1d7f26fe36ac9d87fb85a6027c1a4e6e9030bccc5af94(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a43c510e0345ca7c07f54ad935240ac0b0354c725e440eecba24c0de57694c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df85e2d52558b475a0d62fdf489c8f5f6031f9a19fbff0cfc9cd79a8cacdf1da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc9af0364ac00a747c16831614c29091ba99b46c0289a2e45cbf15a8948929e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61005ca01602209a4a2b34f389307ae401cdb534d6e7b4f7c57a31f139798370(
    value: typing.Optional[OrchestratedVirtualMachineScaleSetRollingUpgradePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8b236977890621b8a98df8f47ed016b15f01dc267577ed102228fc2c01f15c(
    *,
    allocation_strategy: builtins.str,
    vm_sizes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e21451b45a430ed2a82ac9222a0a638df7c220916bcf7e30614cb8ba15e8eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ed840ddc8d9548e2c9ae7a8bc0da2a74c60c321118d9eca4956c00c2d45b23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f967fc1eaffbcd2c4e412941ef09940c582e67b39cde3ff6518c2c4edc9556(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d481db8fa1b0dd9d519138896b88e2ec5bc5ad433562fe85abcc96cb66cab3(
    value: typing.Optional[OrchestratedVirtualMachineScaleSetSkuProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7466fa15dd13412e4f5ec7798e74b3658d301010fc9f26c8b38e219a05b380(
    *,
    offer: builtins.str,
    publisher: builtins.str,
    sku: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca410b699df20c026cffa43a1babc39e8a03804bb5121e6009d2823070e1908(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c6e3fba9b6ef0a2638c0244de2c6285a4c3be5f8dd7aa07f9ed6102ce21b58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad971e6d72dea04970ae30a55a7619dccceaefde1e0dceb3b896e5f656e732e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d674672d300137aafc5c187998d689697e6da95cc3631dd58e3d67f65efad8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6548f2d0d914e01d8c588ba8b327660fcfbccb9e0c237e4fb9e76d3923c9e44e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441996ceb08fe17a26492d9364171d6772569061a20f0061611949cc49613314(
    value: typing.Optional[OrchestratedVirtualMachineScaleSetSourceImageReference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61cdfb160be8a9898bc9e5f9bbd430633f2b2a5223f3a1696dcdff0bc939f9d8(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec6ac32bcc5400d94dbfd969722a59b3a187fa347246ff7a2b9927a448f00d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcbf67176b62e95e67f04fa4b394cae2e0dac1f0e111a3e05e2c4b095fbd3260(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb2ef774a6624305fcde82675cb6a8847af62a23a605ac9f47b7afe2aa3aecc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e236bd3b6993994fd54662a35ee712bfa78b62e21200ea1e42b405e4f02669f4(
    value: typing.Optional[OrchestratedVirtualMachineScaleSetTerminationNotification],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9751597143ce26825f87029a076f81a19065df31dd4bb798e458cf40ac4d1d0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775e7ec7a76e65ad3a843b1890a0467cce9539d01b82b2d6ddfd393e60270214(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1b39d051f67967df3ca65c58b7d1622986ef2216384331f7ff08f0251b0059(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b5328df40ca78b131db750e310228a37b888cc7fb000058cdd89772ab4a22eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391921f2abd84cc0026c1600b41df86477f428f617e51ba35c5f8639a1f759be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfcb0334fc6fe834ef5420f4c14f34b3c459e92b8c2065fc4902a81e6fe32176(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc00f9d89951aa8327353a15270a9117774e74ac2bf48f7c3cd26224873cef0d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrchestratedVirtualMachineScaleSetTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
