r'''
# `azurerm_site_recovery_replication_recovery_plan`

Refer to the Terraform Registry for docs: [`azurerm_site_recovery_replication_recovery_plan`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan).
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


class SiteRecoveryReplicationRecoveryPlan(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlan",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan azurerm_site_recovery_replication_recovery_plan}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        boot_recovery_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup", typing.Dict[builtins.str, typing.Any]]]],
        failover_recovery_group: typing.Union["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        recovery_vault_id: builtins.str,
        shutdown_recovery_group: typing.Union["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup", typing.Dict[builtins.str, typing.Any]],
        source_recovery_fabric_id: builtins.str,
        target_recovery_fabric_id: builtins.str,
        azure_to_azure_settings: typing.Optional[typing.Union["SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SiteRecoveryReplicationRecoveryPlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan azurerm_site_recovery_replication_recovery_plan} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param boot_recovery_group: boot_recovery_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#boot_recovery_group SiteRecoveryReplicationRecoveryPlan#boot_recovery_group}
        :param failover_recovery_group: failover_recovery_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#failover_recovery_group SiteRecoveryReplicationRecoveryPlan#failover_recovery_group}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#name SiteRecoveryReplicationRecoveryPlan#name}.
        :param recovery_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#recovery_vault_id SiteRecoveryReplicationRecoveryPlan#recovery_vault_id}.
        :param shutdown_recovery_group: shutdown_recovery_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#shutdown_recovery_group SiteRecoveryReplicationRecoveryPlan#shutdown_recovery_group}
        :param source_recovery_fabric_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#source_recovery_fabric_id SiteRecoveryReplicationRecoveryPlan#source_recovery_fabric_id}.
        :param target_recovery_fabric_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#target_recovery_fabric_id SiteRecoveryReplicationRecoveryPlan#target_recovery_fabric_id}.
        :param azure_to_azure_settings: azure_to_azure_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#azure_to_azure_settings SiteRecoveryReplicationRecoveryPlan#azure_to_azure_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#id SiteRecoveryReplicationRecoveryPlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#timeouts SiteRecoveryReplicationRecoveryPlan#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aedea51b38ad30e9028c148d4a78f46e5eb52a8b076de0aa694b0ae87dfd112a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SiteRecoveryReplicationRecoveryPlanConfig(
            boot_recovery_group=boot_recovery_group,
            failover_recovery_group=failover_recovery_group,
            name=name,
            recovery_vault_id=recovery_vault_id,
            shutdown_recovery_group=shutdown_recovery_group,
            source_recovery_fabric_id=source_recovery_fabric_id,
            target_recovery_fabric_id=target_recovery_fabric_id,
            azure_to_azure_settings=azure_to_azure_settings,
            id=id,
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
        '''Generates CDKTF code for importing a SiteRecoveryReplicationRecoveryPlan resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SiteRecoveryReplicationRecoveryPlan to import.
        :param import_from_id: The id of the existing SiteRecoveryReplicationRecoveryPlan that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SiteRecoveryReplicationRecoveryPlan to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d80dbe812bfab9f24b81ab9761a90e6d49a5641b1b4b08cf2cb66b4416c198d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAzureToAzureSettings")
    def put_azure_to_azure_settings(
        self,
        *,
        primary_edge_zone: typing.Optional[builtins.str] = None,
        primary_zone: typing.Optional[builtins.str] = None,
        recovery_edge_zone: typing.Optional[builtins.str] = None,
        recovery_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param primary_edge_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#primary_edge_zone SiteRecoveryReplicationRecoveryPlan#primary_edge_zone}.
        :param primary_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#primary_zone SiteRecoveryReplicationRecoveryPlan#primary_zone}.
        :param recovery_edge_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#recovery_edge_zone SiteRecoveryReplicationRecoveryPlan#recovery_edge_zone}.
        :param recovery_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#recovery_zone SiteRecoveryReplicationRecoveryPlan#recovery_zone}.
        '''
        value = SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings(
            primary_edge_zone=primary_edge_zone,
            primary_zone=primary_zone,
            recovery_edge_zone=recovery_edge_zone,
            recovery_zone=recovery_zone,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureToAzureSettings", [value]))

    @jsii.member(jsii_name="putBootRecoveryGroup")
    def put_boot_recovery_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8cf87bb246466cebb37e12ba1c9a4b735def5f448b7e9f256c72e40971c5382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBootRecoveryGroup", [value]))

    @jsii.member(jsii_name="putFailoverRecoveryGroup")
    def put_failover_recovery_group(
        self,
        *,
        post_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pre_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param post_action: post_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#post_action SiteRecoveryReplicationRecoveryPlan#post_action}
        :param pre_action: pre_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#pre_action SiteRecoveryReplicationRecoveryPlan#pre_action}
        '''
        value = SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup(
            post_action=post_action, pre_action=pre_action
        )

        return typing.cast(None, jsii.invoke(self, "putFailoverRecoveryGroup", [value]))

    @jsii.member(jsii_name="putShutdownRecoveryGroup")
    def put_shutdown_recovery_group(
        self,
        *,
        post_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pre_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param post_action: post_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#post_action SiteRecoveryReplicationRecoveryPlan#post_action}
        :param pre_action: pre_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#pre_action SiteRecoveryReplicationRecoveryPlan#pre_action}
        '''
        value = SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup(
            post_action=post_action, pre_action=pre_action
        )

        return typing.cast(None, jsii.invoke(self, "putShutdownRecoveryGroup", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#create SiteRecoveryReplicationRecoveryPlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#delete SiteRecoveryReplicationRecoveryPlan#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#read SiteRecoveryReplicationRecoveryPlan#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#update SiteRecoveryReplicationRecoveryPlan#update}.
        '''
        value = SiteRecoveryReplicationRecoveryPlanTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAzureToAzureSettings")
    def reset_azure_to_azure_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureToAzureSettings", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="azureToAzureSettings")
    def azure_to_azure_settings(
        self,
    ) -> "SiteRecoveryReplicationRecoveryPlanAzureToAzureSettingsOutputReference":
        return typing.cast("SiteRecoveryReplicationRecoveryPlanAzureToAzureSettingsOutputReference", jsii.get(self, "azureToAzureSettings"))

    @builtins.property
    @jsii.member(jsii_name="bootRecoveryGroup")
    def boot_recovery_group(
        self,
    ) -> "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupList":
        return typing.cast("SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupList", jsii.get(self, "bootRecoveryGroup"))

    @builtins.property
    @jsii.member(jsii_name="failoverRecoveryGroup")
    def failover_recovery_group(
        self,
    ) -> "SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupOutputReference":
        return typing.cast("SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupOutputReference", jsii.get(self, "failoverRecoveryGroup"))

    @builtins.property
    @jsii.member(jsii_name="shutdownRecoveryGroup")
    def shutdown_recovery_group(
        self,
    ) -> "SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupOutputReference":
        return typing.cast("SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupOutputReference", jsii.get(self, "shutdownRecoveryGroup"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SiteRecoveryReplicationRecoveryPlanTimeoutsOutputReference":
        return typing.cast("SiteRecoveryReplicationRecoveryPlanTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="azureToAzureSettingsInput")
    def azure_to_azure_settings_input(
        self,
    ) -> typing.Optional["SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings"]:
        return typing.cast(typing.Optional["SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings"], jsii.get(self, "azureToAzureSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="bootRecoveryGroupInput")
    def boot_recovery_group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup"]]], jsii.get(self, "bootRecoveryGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="failoverRecoveryGroupInput")
    def failover_recovery_group_input(
        self,
    ) -> typing.Optional["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup"]:
        return typing.cast(typing.Optional["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup"], jsii.get(self, "failoverRecoveryGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryVaultIdInput")
    def recovery_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoveryVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="shutdownRecoveryGroupInput")
    def shutdown_recovery_group_input(
        self,
    ) -> typing.Optional["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup"]:
        return typing.cast(typing.Optional["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup"], jsii.get(self, "shutdownRecoveryGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceRecoveryFabricIdInput")
    def source_recovery_fabric_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceRecoveryFabricIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRecoveryFabricIdInput")
    def target_recovery_fabric_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetRecoveryFabricIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SiteRecoveryReplicationRecoveryPlanTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SiteRecoveryReplicationRecoveryPlanTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee355680b8e194ef0876852c8dea1e27bc12d65a467f28ab108366411c7f183b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b3399611c4c5e49977e9de0cb86ddc8d51699822c5cf5754825f54ea41fba37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryVaultId")
    def recovery_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recoveryVaultId"))

    @recovery_vault_id.setter
    def recovery_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df87245229d2aac4c67cabbdfa5a394fd81b35a33765e47ab1190765d4be122e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceRecoveryFabricId")
    def source_recovery_fabric_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceRecoveryFabricId"))

    @source_recovery_fabric_id.setter
    def source_recovery_fabric_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbb2a5e3579d6168a5020c8ace78b19cb633865cb4ca99a424d8a191496a6126)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceRecoveryFabricId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetRecoveryFabricId")
    def target_recovery_fabric_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetRecoveryFabricId"))

    @target_recovery_fabric_id.setter
    def target_recovery_fabric_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4457f570effbf69c634f881a3d03a864d9ad62ec0ebf1f62317a8a3a39de28d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRecoveryFabricId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings",
    jsii_struct_bases=[],
    name_mapping={
        "primary_edge_zone": "primaryEdgeZone",
        "primary_zone": "primaryZone",
        "recovery_edge_zone": "recoveryEdgeZone",
        "recovery_zone": "recoveryZone",
    },
)
class SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings:
    def __init__(
        self,
        *,
        primary_edge_zone: typing.Optional[builtins.str] = None,
        primary_zone: typing.Optional[builtins.str] = None,
        recovery_edge_zone: typing.Optional[builtins.str] = None,
        recovery_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param primary_edge_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#primary_edge_zone SiteRecoveryReplicationRecoveryPlan#primary_edge_zone}.
        :param primary_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#primary_zone SiteRecoveryReplicationRecoveryPlan#primary_zone}.
        :param recovery_edge_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#recovery_edge_zone SiteRecoveryReplicationRecoveryPlan#recovery_edge_zone}.
        :param recovery_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#recovery_zone SiteRecoveryReplicationRecoveryPlan#recovery_zone}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db13e1ec6494fe3d59bb5bfe26b07705106599640f14d7f4880feb70d48d2c9)
            check_type(argname="argument primary_edge_zone", value=primary_edge_zone, expected_type=type_hints["primary_edge_zone"])
            check_type(argname="argument primary_zone", value=primary_zone, expected_type=type_hints["primary_zone"])
            check_type(argname="argument recovery_edge_zone", value=recovery_edge_zone, expected_type=type_hints["recovery_edge_zone"])
            check_type(argname="argument recovery_zone", value=recovery_zone, expected_type=type_hints["recovery_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if primary_edge_zone is not None:
            self._values["primary_edge_zone"] = primary_edge_zone
        if primary_zone is not None:
            self._values["primary_zone"] = primary_zone
        if recovery_edge_zone is not None:
            self._values["recovery_edge_zone"] = recovery_edge_zone
        if recovery_zone is not None:
            self._values["recovery_zone"] = recovery_zone

    @builtins.property
    def primary_edge_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#primary_edge_zone SiteRecoveryReplicationRecoveryPlan#primary_edge_zone}.'''
        result = self._values.get("primary_edge_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#primary_zone SiteRecoveryReplicationRecoveryPlan#primary_zone}.'''
        result = self._values.get("primary_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recovery_edge_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#recovery_edge_zone SiteRecoveryReplicationRecoveryPlan#recovery_edge_zone}.'''
        result = self._values.get("recovery_edge_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recovery_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#recovery_zone SiteRecoveryReplicationRecoveryPlan#recovery_zone}.'''
        result = self._values.get("recovery_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryReplicationRecoveryPlanAzureToAzureSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanAzureToAzureSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1de2ccdc63cd15e75fcc80a6d5021ce0954b055fd91a9d86d8d73f0a48dffae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPrimaryEdgeZone")
    def reset_primary_edge_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryEdgeZone", []))

    @jsii.member(jsii_name="resetPrimaryZone")
    def reset_primary_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryZone", []))

    @jsii.member(jsii_name="resetRecoveryEdgeZone")
    def reset_recovery_edge_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecoveryEdgeZone", []))

    @jsii.member(jsii_name="resetRecoveryZone")
    def reset_recovery_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecoveryZone", []))

    @builtins.property
    @jsii.member(jsii_name="primaryEdgeZoneInput")
    def primary_edge_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryEdgeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryZoneInput")
    def primary_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryEdgeZoneInput")
    def recovery_edge_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoveryEdgeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryZoneInput")
    def recovery_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoveryZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryEdgeZone")
    def primary_edge_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryEdgeZone"))

    @primary_edge_zone.setter
    def primary_edge_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__095f08cbc4ebcd820fb5cc38cdcaca2a716b2b0feb1c6699ec6b5d07b7ffc843)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryEdgeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryZone")
    def primary_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryZone"))

    @primary_zone.setter
    def primary_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed45b4466e9e75585f5d5c05e070b547b9ef2b830826ba4bbf3acd82ea0b4399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryEdgeZone")
    def recovery_edge_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recoveryEdgeZone"))

    @recovery_edge_zone.setter
    def recovery_edge_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a46a7db5ebbac14385f31b1910cb397f1dad5470fb8dfea31dd6fb91f99fed3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryEdgeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryZone")
    def recovery_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recoveryZone"))

    @recovery_zone.setter
    def recovery_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8405493fd92865d0b6b66e82ee9ac9ef8e3eadd509e3beda7ff24dd01abdd883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings]:
        return typing.cast(typing.Optional[SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a23cf0b0b9a0891573230a0c98c0a9b907179c4b5a1bc8fb649b35a65899abc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup",
    jsii_struct_bases=[],
    name_mapping={
        "post_action": "postAction",
        "pre_action": "preAction",
        "replicated_protected_items": "replicatedProtectedItems",
    },
)
class SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup:
    def __init__(
        self,
        *,
        post_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pre_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        replicated_protected_items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param post_action: post_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#post_action SiteRecoveryReplicationRecoveryPlan#post_action}
        :param pre_action: pre_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#pre_action SiteRecoveryReplicationRecoveryPlan#pre_action}
        :param replicated_protected_items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#replicated_protected_items SiteRecoveryReplicationRecoveryPlan#replicated_protected_items}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02c90eeb209696efac7a14d6d5547ea7555bc2609fbde1cff9d756a2b49b63b0)
            check_type(argname="argument post_action", value=post_action, expected_type=type_hints["post_action"])
            check_type(argname="argument pre_action", value=pre_action, expected_type=type_hints["pre_action"])
            check_type(argname="argument replicated_protected_items", value=replicated_protected_items, expected_type=type_hints["replicated_protected_items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post_action is not None:
            self._values["post_action"] = post_action
        if pre_action is not None:
            self._values["pre_action"] = pre_action
        if replicated_protected_items is not None:
            self._values["replicated_protected_items"] = replicated_protected_items

    @builtins.property
    def post_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction"]]]:
        '''post_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#post_action SiteRecoveryReplicationRecoveryPlan#post_action}
        '''
        result = self._values.get("post_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction"]]], result)

    @builtins.property
    def pre_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction"]]]:
        '''pre_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#pre_action SiteRecoveryReplicationRecoveryPlan#pre_action}
        '''
        result = self._values.get("pre_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction"]]], result)

    @builtins.property
    def replicated_protected_items(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#replicated_protected_items SiteRecoveryReplicationRecoveryPlan#replicated_protected_items}.'''
        result = self._values.get("replicated_protected_items")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a9d2e129cbf752e571cd9c764f5c587256e84f79ec7de168cdc32858de15a39)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cced8b592e07abfca7506d0cb9b62df0f6a90980b4889ffd73e0b6e8a88e6db9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c88c2e1a7f000b934b9b89d2cbd1674254ab99a4b8572fb171e28c35fae87c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2815d6ca839cd0ef038bb630d3ead594193564747c9076673a3d0335848e53a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e586eae0d0525a150bbd332eed2feeba518768f6f2160fc53db940e92c7b850d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72f4f5907f081eb932762d216c40f1c55d0fa8237476f4c3278f33784110c3e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51483dc50399f9a597368720c9d5014b06f0e0409febe748a090d64d16590697)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPostAction")
    def put_post_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9d813330572d9b913c7648363c1b81ffeef26e6e80b276fa3fc222f7dd2e591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPostAction", [value]))

    @jsii.member(jsii_name="putPreAction")
    def put_pre_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e828df7ff132fb35fa6dcd18ec9a20afd55f56eab1cd6e8829390707f087d203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPreAction", [value]))

    @jsii.member(jsii_name="resetPostAction")
    def reset_post_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostAction", []))

    @jsii.member(jsii_name="resetPreAction")
    def reset_pre_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreAction", []))

    @jsii.member(jsii_name="resetReplicatedProtectedItems")
    def reset_replicated_protected_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicatedProtectedItems", []))

    @builtins.property
    @jsii.member(jsii_name="postAction")
    def post_action(
        self,
    ) -> "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostActionList":
        return typing.cast("SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostActionList", jsii.get(self, "postAction"))

    @builtins.property
    @jsii.member(jsii_name="preAction")
    def pre_action(
        self,
    ) -> "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreActionList":
        return typing.cast("SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreActionList", jsii.get(self, "preAction"))

    @builtins.property
    @jsii.member(jsii_name="postActionInput")
    def post_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction"]]], jsii.get(self, "postActionInput"))

    @builtins.property
    @jsii.member(jsii_name="preActionInput")
    def pre_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction"]]], jsii.get(self, "preActionInput"))

    @builtins.property
    @jsii.member(jsii_name="replicatedProtectedItemsInput")
    def replicated_protected_items_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "replicatedProtectedItemsInput"))

    @builtins.property
    @jsii.member(jsii_name="replicatedProtectedItems")
    def replicated_protected_items(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "replicatedProtectedItems"))

    @replicated_protected_items.setter
    def replicated_protected_items(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5b9da7bbd198b60bb2f48b804b90b4db96a26b05bdebb39c639404bf3796bcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicatedProtectedItems", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__107478ac8e95356bccef019f28f052bf119dbbf677973d82c1d6635b6b9266b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction",
    jsii_struct_bases=[],
    name_mapping={
        "fail_over_directions": "failOverDirections",
        "fail_over_types": "failOverTypes",
        "name": "name",
        "type": "type",
        "fabric_location": "fabricLocation",
        "manual_action_instruction": "manualActionInstruction",
        "runbook_id": "runbookId",
        "script_path": "scriptPath",
    },
)
class SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction:
    def __init__(
        self,
        *,
        fail_over_directions: typing.Sequence[builtins.str],
        fail_over_types: typing.Sequence[builtins.str],
        name: builtins.str,
        type: builtins.str,
        fabric_location: typing.Optional[builtins.str] = None,
        manual_action_instruction: typing.Optional[builtins.str] = None,
        runbook_id: typing.Optional[builtins.str] = None,
        script_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fail_over_directions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_directions SiteRecoveryReplicationRecoveryPlan#fail_over_directions}.
        :param fail_over_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_types SiteRecoveryReplicationRecoveryPlan#fail_over_types}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#name SiteRecoveryReplicationRecoveryPlan#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#type SiteRecoveryReplicationRecoveryPlan#type}.
        :param fabric_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fabric_location SiteRecoveryReplicationRecoveryPlan#fabric_location}.
        :param manual_action_instruction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#manual_action_instruction SiteRecoveryReplicationRecoveryPlan#manual_action_instruction}.
        :param runbook_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#runbook_id SiteRecoveryReplicationRecoveryPlan#runbook_id}.
        :param script_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#script_path SiteRecoveryReplicationRecoveryPlan#script_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7c89d14aa4ba9d36dc909178bf6cffd26d79f31974126b2c5bc4b1d81b9e01)
            check_type(argname="argument fail_over_directions", value=fail_over_directions, expected_type=type_hints["fail_over_directions"])
            check_type(argname="argument fail_over_types", value=fail_over_types, expected_type=type_hints["fail_over_types"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument fabric_location", value=fabric_location, expected_type=type_hints["fabric_location"])
            check_type(argname="argument manual_action_instruction", value=manual_action_instruction, expected_type=type_hints["manual_action_instruction"])
            check_type(argname="argument runbook_id", value=runbook_id, expected_type=type_hints["runbook_id"])
            check_type(argname="argument script_path", value=script_path, expected_type=type_hints["script_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fail_over_directions": fail_over_directions,
            "fail_over_types": fail_over_types,
            "name": name,
            "type": type,
        }
        if fabric_location is not None:
            self._values["fabric_location"] = fabric_location
        if manual_action_instruction is not None:
            self._values["manual_action_instruction"] = manual_action_instruction
        if runbook_id is not None:
            self._values["runbook_id"] = runbook_id
        if script_path is not None:
            self._values["script_path"] = script_path

    @builtins.property
    def fail_over_directions(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_directions SiteRecoveryReplicationRecoveryPlan#fail_over_directions}.'''
        result = self._values.get("fail_over_directions")
        assert result is not None, "Required property 'fail_over_directions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def fail_over_types(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_types SiteRecoveryReplicationRecoveryPlan#fail_over_types}.'''
        result = self._values.get("fail_over_types")
        assert result is not None, "Required property 'fail_over_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#name SiteRecoveryReplicationRecoveryPlan#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#type SiteRecoveryReplicationRecoveryPlan#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fabric_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fabric_location SiteRecoveryReplicationRecoveryPlan#fabric_location}.'''
        result = self._values.get("fabric_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manual_action_instruction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#manual_action_instruction SiteRecoveryReplicationRecoveryPlan#manual_action_instruction}.'''
        result = self._values.get("manual_action_instruction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runbook_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#runbook_id SiteRecoveryReplicationRecoveryPlan#runbook_id}.'''
        result = self._values.get("runbook_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#script_path SiteRecoveryReplicationRecoveryPlan#script_path}.'''
        result = self._values.get("script_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__302a0a0ebcec62bb0b17f86c3891bfcb8716b4642a5e9e4c8d86f9d1133ddd74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17362306c4026a30a267c3dd7f7321f57d983a608fe4f791cbf8b1cfd27ade70)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65e1ca96f6910467f00c814587385981d0b9c94d935ec406a67d6e554686f95b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24399f45935b5f655d10041dd3c1e8187668f8fb35c30590988679a73dee6ff6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ed35eab052329c198fda77f15ca6a652d7942848160698d62e41cae6a3cc5e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fafd8a0544d73424277f08039f259a0dc27ac7f10bf1a931ebac69c013c42ffc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1adaf94f460e2407cee7ca0f5f6992d4ec19bbee0937f26ec94a143ba58660b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFabricLocation")
    def reset_fabric_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFabricLocation", []))

    @jsii.member(jsii_name="resetManualActionInstruction")
    def reset_manual_action_instruction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualActionInstruction", []))

    @jsii.member(jsii_name="resetRunbookId")
    def reset_runbook_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunbookId", []))

    @jsii.member(jsii_name="resetScriptPath")
    def reset_script_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptPath", []))

    @builtins.property
    @jsii.member(jsii_name="fabricLocationInput")
    def fabric_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fabricLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="failOverDirectionsInput")
    def fail_over_directions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "failOverDirectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="failOverTypesInput")
    def fail_over_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "failOverTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="manualActionInstructionInput")
    def manual_action_instruction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "manualActionInstructionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="runbookIdInput")
    def runbook_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runbookIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptPathInput")
    def script_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptPathInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="fabricLocation")
    def fabric_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fabricLocation"))

    @fabric_location.setter
    def fabric_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5737aa1ecaac0dc567a749069b09d7a1458a661922c163303774f3a8761fd03a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fabricLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOverDirections")
    def fail_over_directions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "failOverDirections"))

    @fail_over_directions.setter
    def fail_over_directions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1547e34022ba62032cdf0b8c3926f51b61a3233d3cb0df3e845a159212befd75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOverDirections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOverTypes")
    def fail_over_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "failOverTypes"))

    @fail_over_types.setter
    def fail_over_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c39c1cbed052facacfaa77bd2fc0e8d75e1d41715f0653abfcedc5b63a6eeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOverTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="manualActionInstruction")
    def manual_action_instruction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "manualActionInstruction"))

    @manual_action_instruction.setter
    def manual_action_instruction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba8bd66fdba9eaf751cae6e1eb0c3b39ab9782e863ce7a42ff1008f5885521d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualActionInstruction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87460da41cbc422aecf2d10755d68545ef1a5f62c6ee9ed82edd711b49d57827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runbookId")
    def runbook_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runbookId"))

    @runbook_id.setter
    def runbook_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66363525067c947e675fa7e266be303e4a2b837ca0c1e52331e4d80ad9e8bd41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runbookId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scriptPath")
    def script_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scriptPath"))

    @script_path.setter
    def script_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcce037c7bf0fab7d7dc32452ef58b78addd03f6d42802071fd0ddb58edbf50a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ea9410656bed37db43f41a795ec1ce54c85fa93d57a31276f94f3a02109c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d566f33e900aed3ea6723808d8c964de5473bcb26e2c0b921bddf20cee32342f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction",
    jsii_struct_bases=[],
    name_mapping={
        "fail_over_directions": "failOverDirections",
        "fail_over_types": "failOverTypes",
        "name": "name",
        "type": "type",
        "fabric_location": "fabricLocation",
        "manual_action_instruction": "manualActionInstruction",
        "runbook_id": "runbookId",
        "script_path": "scriptPath",
    },
)
class SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction:
    def __init__(
        self,
        *,
        fail_over_directions: typing.Sequence[builtins.str],
        fail_over_types: typing.Sequence[builtins.str],
        name: builtins.str,
        type: builtins.str,
        fabric_location: typing.Optional[builtins.str] = None,
        manual_action_instruction: typing.Optional[builtins.str] = None,
        runbook_id: typing.Optional[builtins.str] = None,
        script_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fail_over_directions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_directions SiteRecoveryReplicationRecoveryPlan#fail_over_directions}.
        :param fail_over_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_types SiteRecoveryReplicationRecoveryPlan#fail_over_types}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#name SiteRecoveryReplicationRecoveryPlan#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#type SiteRecoveryReplicationRecoveryPlan#type}.
        :param fabric_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fabric_location SiteRecoveryReplicationRecoveryPlan#fabric_location}.
        :param manual_action_instruction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#manual_action_instruction SiteRecoveryReplicationRecoveryPlan#manual_action_instruction}.
        :param runbook_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#runbook_id SiteRecoveryReplicationRecoveryPlan#runbook_id}.
        :param script_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#script_path SiteRecoveryReplicationRecoveryPlan#script_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1def9547d346bf4817906f5e6b47ffece3baaf1200698965779823d2dee8c90e)
            check_type(argname="argument fail_over_directions", value=fail_over_directions, expected_type=type_hints["fail_over_directions"])
            check_type(argname="argument fail_over_types", value=fail_over_types, expected_type=type_hints["fail_over_types"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument fabric_location", value=fabric_location, expected_type=type_hints["fabric_location"])
            check_type(argname="argument manual_action_instruction", value=manual_action_instruction, expected_type=type_hints["manual_action_instruction"])
            check_type(argname="argument runbook_id", value=runbook_id, expected_type=type_hints["runbook_id"])
            check_type(argname="argument script_path", value=script_path, expected_type=type_hints["script_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fail_over_directions": fail_over_directions,
            "fail_over_types": fail_over_types,
            "name": name,
            "type": type,
        }
        if fabric_location is not None:
            self._values["fabric_location"] = fabric_location
        if manual_action_instruction is not None:
            self._values["manual_action_instruction"] = manual_action_instruction
        if runbook_id is not None:
            self._values["runbook_id"] = runbook_id
        if script_path is not None:
            self._values["script_path"] = script_path

    @builtins.property
    def fail_over_directions(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_directions SiteRecoveryReplicationRecoveryPlan#fail_over_directions}.'''
        result = self._values.get("fail_over_directions")
        assert result is not None, "Required property 'fail_over_directions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def fail_over_types(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_types SiteRecoveryReplicationRecoveryPlan#fail_over_types}.'''
        result = self._values.get("fail_over_types")
        assert result is not None, "Required property 'fail_over_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#name SiteRecoveryReplicationRecoveryPlan#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#type SiteRecoveryReplicationRecoveryPlan#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fabric_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fabric_location SiteRecoveryReplicationRecoveryPlan#fabric_location}.'''
        result = self._values.get("fabric_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manual_action_instruction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#manual_action_instruction SiteRecoveryReplicationRecoveryPlan#manual_action_instruction}.'''
        result = self._values.get("manual_action_instruction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runbook_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#runbook_id SiteRecoveryReplicationRecoveryPlan#runbook_id}.'''
        result = self._values.get("runbook_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#script_path SiteRecoveryReplicationRecoveryPlan#script_path}.'''
        result = self._values.get("script_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d983b7cf24286e98103e691065b8cdb5bb7d2979fa9233ff9a0d7bae2c2f7914)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__330f5ebf08d0ef795a7a62d52f0b0e3f10a90ccf1ad8ed832aa1d200173ac0ff)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c23d093406f4170fb728f62e01568882cb540b5effca56be4325323341321aaf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__239d6676139a45c8b389b1530ac189720a01450f73ab82d15e7d6895918f5004)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7caf8affb09ec55592b1098a6c8d476a6fdc266c696fb176d9e617066a8183c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efb7f5594334b322521e752a80025b1760b14bffd2fb7735599c2a11121122bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83e4b03a728625161d6211046e7f54436e826cce5f56bab9a664bf488a69bb93)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFabricLocation")
    def reset_fabric_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFabricLocation", []))

    @jsii.member(jsii_name="resetManualActionInstruction")
    def reset_manual_action_instruction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualActionInstruction", []))

    @jsii.member(jsii_name="resetRunbookId")
    def reset_runbook_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunbookId", []))

    @jsii.member(jsii_name="resetScriptPath")
    def reset_script_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptPath", []))

    @builtins.property
    @jsii.member(jsii_name="fabricLocationInput")
    def fabric_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fabricLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="failOverDirectionsInput")
    def fail_over_directions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "failOverDirectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="failOverTypesInput")
    def fail_over_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "failOverTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="manualActionInstructionInput")
    def manual_action_instruction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "manualActionInstructionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="runbookIdInput")
    def runbook_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runbookIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptPathInput")
    def script_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptPathInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="fabricLocation")
    def fabric_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fabricLocation"))

    @fabric_location.setter
    def fabric_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd4f13b62161effc7c3b26499ff9751443e132aaeedec70380de1e3b438d7ff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fabricLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOverDirections")
    def fail_over_directions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "failOverDirections"))

    @fail_over_directions.setter
    def fail_over_directions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8e9c6d29836c62663345b99ce8bcc8d0a53cb8069247d0759c628361be336cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOverDirections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOverTypes")
    def fail_over_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "failOverTypes"))

    @fail_over_types.setter
    def fail_over_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0ea1c8d172ec8604a95b0896eff39bd10fd0c2cabe06f3173ab8c6fa354e8cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOverTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="manualActionInstruction")
    def manual_action_instruction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "manualActionInstruction"))

    @manual_action_instruction.setter
    def manual_action_instruction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48fe90856a6721efaf4076ccf27bc42325d6f30d08fbec5b65678591c111c868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualActionInstruction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd80f1eb3c85d8553a956d21681569abc96039b960395943f4bb913c15cb01d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runbookId")
    def runbook_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runbookId"))

    @runbook_id.setter
    def runbook_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbac8779deb4354a2ca5fcf99f5d11148e0d20c4f7a3928f965d77dd373b8565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runbookId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scriptPath")
    def script_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scriptPath"))

    @script_path.setter
    def script_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a730c2d69cb1d9a506efddc5df89508fb756e6ba5e62bec45296c7e01c51bb00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5c929ef61b3422b39b8db41f458cddcfd5fa534400f0e1567f64f486218458a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__479427db9287a461f893280d6b8d5e5af1fa9a50cc873e3c0dad55581fa37470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "boot_recovery_group": "bootRecoveryGroup",
        "failover_recovery_group": "failoverRecoveryGroup",
        "name": "name",
        "recovery_vault_id": "recoveryVaultId",
        "shutdown_recovery_group": "shutdownRecoveryGroup",
        "source_recovery_fabric_id": "sourceRecoveryFabricId",
        "target_recovery_fabric_id": "targetRecoveryFabricId",
        "azure_to_azure_settings": "azureToAzureSettings",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class SiteRecoveryReplicationRecoveryPlanConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        boot_recovery_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup, typing.Dict[builtins.str, typing.Any]]]],
        failover_recovery_group: typing.Union["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        recovery_vault_id: builtins.str,
        shutdown_recovery_group: typing.Union["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup", typing.Dict[builtins.str, typing.Any]],
        source_recovery_fabric_id: builtins.str,
        target_recovery_fabric_id: builtins.str,
        azure_to_azure_settings: typing.Optional[typing.Union[SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SiteRecoveryReplicationRecoveryPlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param boot_recovery_group: boot_recovery_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#boot_recovery_group SiteRecoveryReplicationRecoveryPlan#boot_recovery_group}
        :param failover_recovery_group: failover_recovery_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#failover_recovery_group SiteRecoveryReplicationRecoveryPlan#failover_recovery_group}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#name SiteRecoveryReplicationRecoveryPlan#name}.
        :param recovery_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#recovery_vault_id SiteRecoveryReplicationRecoveryPlan#recovery_vault_id}.
        :param shutdown_recovery_group: shutdown_recovery_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#shutdown_recovery_group SiteRecoveryReplicationRecoveryPlan#shutdown_recovery_group}
        :param source_recovery_fabric_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#source_recovery_fabric_id SiteRecoveryReplicationRecoveryPlan#source_recovery_fabric_id}.
        :param target_recovery_fabric_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#target_recovery_fabric_id SiteRecoveryReplicationRecoveryPlan#target_recovery_fabric_id}.
        :param azure_to_azure_settings: azure_to_azure_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#azure_to_azure_settings SiteRecoveryReplicationRecoveryPlan#azure_to_azure_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#id SiteRecoveryReplicationRecoveryPlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#timeouts SiteRecoveryReplicationRecoveryPlan#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(failover_recovery_group, dict):
            failover_recovery_group = SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup(**failover_recovery_group)
        if isinstance(shutdown_recovery_group, dict):
            shutdown_recovery_group = SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup(**shutdown_recovery_group)
        if isinstance(azure_to_azure_settings, dict):
            azure_to_azure_settings = SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings(**azure_to_azure_settings)
        if isinstance(timeouts, dict):
            timeouts = SiteRecoveryReplicationRecoveryPlanTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df27bcf614e7715749244a844445eab7b01373b56a2b4f8848018c1be15c8b0f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument boot_recovery_group", value=boot_recovery_group, expected_type=type_hints["boot_recovery_group"])
            check_type(argname="argument failover_recovery_group", value=failover_recovery_group, expected_type=type_hints["failover_recovery_group"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument recovery_vault_id", value=recovery_vault_id, expected_type=type_hints["recovery_vault_id"])
            check_type(argname="argument shutdown_recovery_group", value=shutdown_recovery_group, expected_type=type_hints["shutdown_recovery_group"])
            check_type(argname="argument source_recovery_fabric_id", value=source_recovery_fabric_id, expected_type=type_hints["source_recovery_fabric_id"])
            check_type(argname="argument target_recovery_fabric_id", value=target_recovery_fabric_id, expected_type=type_hints["target_recovery_fabric_id"])
            check_type(argname="argument azure_to_azure_settings", value=azure_to_azure_settings, expected_type=type_hints["azure_to_azure_settings"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "boot_recovery_group": boot_recovery_group,
            "failover_recovery_group": failover_recovery_group,
            "name": name,
            "recovery_vault_id": recovery_vault_id,
            "shutdown_recovery_group": shutdown_recovery_group,
            "source_recovery_fabric_id": source_recovery_fabric_id,
            "target_recovery_fabric_id": target_recovery_fabric_id,
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
        if azure_to_azure_settings is not None:
            self._values["azure_to_azure_settings"] = azure_to_azure_settings
        if id is not None:
            self._values["id"] = id
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
    def boot_recovery_group(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup]]:
        '''boot_recovery_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#boot_recovery_group SiteRecoveryReplicationRecoveryPlan#boot_recovery_group}
        '''
        result = self._values.get("boot_recovery_group")
        assert result is not None, "Required property 'boot_recovery_group' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup]], result)

    @builtins.property
    def failover_recovery_group(
        self,
    ) -> "SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup":
        '''failover_recovery_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#failover_recovery_group SiteRecoveryReplicationRecoveryPlan#failover_recovery_group}
        '''
        result = self._values.get("failover_recovery_group")
        assert result is not None, "Required property 'failover_recovery_group' is missing"
        return typing.cast("SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#name SiteRecoveryReplicationRecoveryPlan#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def recovery_vault_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#recovery_vault_id SiteRecoveryReplicationRecoveryPlan#recovery_vault_id}.'''
        result = self._values.get("recovery_vault_id")
        assert result is not None, "Required property 'recovery_vault_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def shutdown_recovery_group(
        self,
    ) -> "SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup":
        '''shutdown_recovery_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#shutdown_recovery_group SiteRecoveryReplicationRecoveryPlan#shutdown_recovery_group}
        '''
        result = self._values.get("shutdown_recovery_group")
        assert result is not None, "Required property 'shutdown_recovery_group' is missing"
        return typing.cast("SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup", result)

    @builtins.property
    def source_recovery_fabric_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#source_recovery_fabric_id SiteRecoveryReplicationRecoveryPlan#source_recovery_fabric_id}.'''
        result = self._values.get("source_recovery_fabric_id")
        assert result is not None, "Required property 'source_recovery_fabric_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_recovery_fabric_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#target_recovery_fabric_id SiteRecoveryReplicationRecoveryPlan#target_recovery_fabric_id}.'''
        result = self._values.get("target_recovery_fabric_id")
        assert result is not None, "Required property 'target_recovery_fabric_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def azure_to_azure_settings(
        self,
    ) -> typing.Optional[SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings]:
        '''azure_to_azure_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#azure_to_azure_settings SiteRecoveryReplicationRecoveryPlan#azure_to_azure_settings}
        '''
        result = self._values.get("azure_to_azure_settings")
        return typing.cast(typing.Optional[SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#id SiteRecoveryReplicationRecoveryPlan#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["SiteRecoveryReplicationRecoveryPlanTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#timeouts SiteRecoveryReplicationRecoveryPlan#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SiteRecoveryReplicationRecoveryPlanTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicationRecoveryPlanConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup",
    jsii_struct_bases=[],
    name_mapping={"post_action": "postAction", "pre_action": "preAction"},
)
class SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup:
    def __init__(
        self,
        *,
        post_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pre_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param post_action: post_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#post_action SiteRecoveryReplicationRecoveryPlan#post_action}
        :param pre_action: pre_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#pre_action SiteRecoveryReplicationRecoveryPlan#pre_action}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd6caab3495f946ddf542c356563e635e65726bd3d5575afbd67a76fed03b65)
            check_type(argname="argument post_action", value=post_action, expected_type=type_hints["post_action"])
            check_type(argname="argument pre_action", value=pre_action, expected_type=type_hints["pre_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post_action is not None:
            self._values["post_action"] = post_action
        if pre_action is not None:
            self._values["pre_action"] = pre_action

    @builtins.property
    def post_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction"]]]:
        '''post_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#post_action SiteRecoveryReplicationRecoveryPlan#post_action}
        '''
        result = self._values.get("post_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction"]]], result)

    @builtins.property
    def pre_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction"]]]:
        '''pre_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#pre_action SiteRecoveryReplicationRecoveryPlan#pre_action}
        '''
        result = self._values.get("pre_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6bfb48d2a9d5a3fc13affba959387ae75eff4ad3b0f1fbb7bd415da2830886b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPostAction")
    def put_post_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e3499a94a1083cc0616991f1d6f58707ed21f9f0dd7a24109d63bcbd7a17b38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPostAction", [value]))

    @jsii.member(jsii_name="putPreAction")
    def put_pre_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e638e736291cdc7b1e669a59843375a00d8f888294c6dd04f38e199bb025993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPreAction", [value]))

    @jsii.member(jsii_name="resetPostAction")
    def reset_post_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostAction", []))

    @jsii.member(jsii_name="resetPreAction")
    def reset_pre_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreAction", []))

    @builtins.property
    @jsii.member(jsii_name="postAction")
    def post_action(
        self,
    ) -> "SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostActionList":
        return typing.cast("SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostActionList", jsii.get(self, "postAction"))

    @builtins.property
    @jsii.member(jsii_name="preAction")
    def pre_action(
        self,
    ) -> "SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreActionList":
        return typing.cast("SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreActionList", jsii.get(self, "preAction"))

    @builtins.property
    @jsii.member(jsii_name="postActionInput")
    def post_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction"]]], jsii.get(self, "postActionInput"))

    @builtins.property
    @jsii.member(jsii_name="preActionInput")
    def pre_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction"]]], jsii.get(self, "preActionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup]:
        return typing.cast(typing.Optional[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a981f3c95c33ab0a76a96431a96447a10e69e71441b9abe4134aa1855b73a2f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction",
    jsii_struct_bases=[],
    name_mapping={
        "fail_over_directions": "failOverDirections",
        "fail_over_types": "failOverTypes",
        "name": "name",
        "type": "type",
        "fabric_location": "fabricLocation",
        "manual_action_instruction": "manualActionInstruction",
        "runbook_id": "runbookId",
        "script_path": "scriptPath",
    },
)
class SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction:
    def __init__(
        self,
        *,
        fail_over_directions: typing.Sequence[builtins.str],
        fail_over_types: typing.Sequence[builtins.str],
        name: builtins.str,
        type: builtins.str,
        fabric_location: typing.Optional[builtins.str] = None,
        manual_action_instruction: typing.Optional[builtins.str] = None,
        runbook_id: typing.Optional[builtins.str] = None,
        script_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fail_over_directions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_directions SiteRecoveryReplicationRecoveryPlan#fail_over_directions}.
        :param fail_over_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_types SiteRecoveryReplicationRecoveryPlan#fail_over_types}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#name SiteRecoveryReplicationRecoveryPlan#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#type SiteRecoveryReplicationRecoveryPlan#type}.
        :param fabric_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fabric_location SiteRecoveryReplicationRecoveryPlan#fabric_location}.
        :param manual_action_instruction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#manual_action_instruction SiteRecoveryReplicationRecoveryPlan#manual_action_instruction}.
        :param runbook_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#runbook_id SiteRecoveryReplicationRecoveryPlan#runbook_id}.
        :param script_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#script_path SiteRecoveryReplicationRecoveryPlan#script_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c3b6d45935a09c7c26a08b43d869d36dc0a96740feda183be4c8e018be75a5)
            check_type(argname="argument fail_over_directions", value=fail_over_directions, expected_type=type_hints["fail_over_directions"])
            check_type(argname="argument fail_over_types", value=fail_over_types, expected_type=type_hints["fail_over_types"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument fabric_location", value=fabric_location, expected_type=type_hints["fabric_location"])
            check_type(argname="argument manual_action_instruction", value=manual_action_instruction, expected_type=type_hints["manual_action_instruction"])
            check_type(argname="argument runbook_id", value=runbook_id, expected_type=type_hints["runbook_id"])
            check_type(argname="argument script_path", value=script_path, expected_type=type_hints["script_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fail_over_directions": fail_over_directions,
            "fail_over_types": fail_over_types,
            "name": name,
            "type": type,
        }
        if fabric_location is not None:
            self._values["fabric_location"] = fabric_location
        if manual_action_instruction is not None:
            self._values["manual_action_instruction"] = manual_action_instruction
        if runbook_id is not None:
            self._values["runbook_id"] = runbook_id
        if script_path is not None:
            self._values["script_path"] = script_path

    @builtins.property
    def fail_over_directions(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_directions SiteRecoveryReplicationRecoveryPlan#fail_over_directions}.'''
        result = self._values.get("fail_over_directions")
        assert result is not None, "Required property 'fail_over_directions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def fail_over_types(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_types SiteRecoveryReplicationRecoveryPlan#fail_over_types}.'''
        result = self._values.get("fail_over_types")
        assert result is not None, "Required property 'fail_over_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#name SiteRecoveryReplicationRecoveryPlan#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#type SiteRecoveryReplicationRecoveryPlan#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fabric_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fabric_location SiteRecoveryReplicationRecoveryPlan#fabric_location}.'''
        result = self._values.get("fabric_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manual_action_instruction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#manual_action_instruction SiteRecoveryReplicationRecoveryPlan#manual_action_instruction}.'''
        result = self._values.get("manual_action_instruction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runbook_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#runbook_id SiteRecoveryReplicationRecoveryPlan#runbook_id}.'''
        result = self._values.get("runbook_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#script_path SiteRecoveryReplicationRecoveryPlan#script_path}.'''
        result = self._values.get("script_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bd2a6210deeedd36a8c6af091ed40a4db72ab3c3db7c969d3ba37c081800dee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c980fafe0a233ae6a47bf12e210dc2cba3f9b9533d71928e501f75fa07685a2a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63288d3e3a081c6a7a6f5f4753e59d2b2c9e56fba22fc4e1b47a10b3f2809069)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eec8655c551f448e48d62ff532b796e8430dafbd501940d2a3700d9f2adfe8c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ddbf31b3a8cdce7975af6626d8c337eedb0c619d17034f98cf8ee846f4f1e04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47d13ae91ef669c93e99e1ae3f4ab5fe60ac556ead194f7a2f57899322a76081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46ac47616f631f5d301d07b23d395633d7c21f913aa10e25f1dde072a0edfe95)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFabricLocation")
    def reset_fabric_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFabricLocation", []))

    @jsii.member(jsii_name="resetManualActionInstruction")
    def reset_manual_action_instruction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualActionInstruction", []))

    @jsii.member(jsii_name="resetRunbookId")
    def reset_runbook_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunbookId", []))

    @jsii.member(jsii_name="resetScriptPath")
    def reset_script_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptPath", []))

    @builtins.property
    @jsii.member(jsii_name="fabricLocationInput")
    def fabric_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fabricLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="failOverDirectionsInput")
    def fail_over_directions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "failOverDirectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="failOverTypesInput")
    def fail_over_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "failOverTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="manualActionInstructionInput")
    def manual_action_instruction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "manualActionInstructionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="runbookIdInput")
    def runbook_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runbookIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptPathInput")
    def script_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptPathInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="fabricLocation")
    def fabric_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fabricLocation"))

    @fabric_location.setter
    def fabric_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbf27d2e3259b39e35f73697dd9a745fb376903127b4a9c008f38330f8005cb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fabricLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOverDirections")
    def fail_over_directions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "failOverDirections"))

    @fail_over_directions.setter
    def fail_over_directions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21c31036065be9e2d63f80e212ac74ecaf8e280e3707c87765f3c2ffe7026466)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOverDirections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOverTypes")
    def fail_over_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "failOverTypes"))

    @fail_over_types.setter
    def fail_over_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21c1a82d7e7f948d559457ab3f3e87446a2baa77b908b53c832c9ad6cb31fa61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOverTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="manualActionInstruction")
    def manual_action_instruction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "manualActionInstruction"))

    @manual_action_instruction.setter
    def manual_action_instruction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d82e02089f7c36bcc61d613647dac257e5d48dc9c0daf85d2d5457a5e0ac6982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualActionInstruction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea6b8eb4b5f39a5cffa95c28371a9604a2faf458073c8b1013dec6fd8efb78ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runbookId")
    def runbook_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runbookId"))

    @runbook_id.setter
    def runbook_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f186dcb3c0b8003d854498d05ef83ae66c67a7ebda0713eeae9e54b9a06a1254)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runbookId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scriptPath")
    def script_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scriptPath"))

    @script_path.setter
    def script_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29320935efa4cf749f156672bddf145209cd7454eab8ba0c5463a15138435679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a78bcbf65f4faebcd8ddb981c194997337aa488694c9deec948925e9e85a16f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02929c08245643f903569e1004e999eab6e0d431fa5c63e26d6d9c36cf20e7af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction",
    jsii_struct_bases=[],
    name_mapping={
        "fail_over_directions": "failOverDirections",
        "fail_over_types": "failOverTypes",
        "name": "name",
        "type": "type",
        "fabric_location": "fabricLocation",
        "manual_action_instruction": "manualActionInstruction",
        "runbook_id": "runbookId",
        "script_path": "scriptPath",
    },
)
class SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction:
    def __init__(
        self,
        *,
        fail_over_directions: typing.Sequence[builtins.str],
        fail_over_types: typing.Sequence[builtins.str],
        name: builtins.str,
        type: builtins.str,
        fabric_location: typing.Optional[builtins.str] = None,
        manual_action_instruction: typing.Optional[builtins.str] = None,
        runbook_id: typing.Optional[builtins.str] = None,
        script_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fail_over_directions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_directions SiteRecoveryReplicationRecoveryPlan#fail_over_directions}.
        :param fail_over_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_types SiteRecoveryReplicationRecoveryPlan#fail_over_types}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#name SiteRecoveryReplicationRecoveryPlan#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#type SiteRecoveryReplicationRecoveryPlan#type}.
        :param fabric_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fabric_location SiteRecoveryReplicationRecoveryPlan#fabric_location}.
        :param manual_action_instruction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#manual_action_instruction SiteRecoveryReplicationRecoveryPlan#manual_action_instruction}.
        :param runbook_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#runbook_id SiteRecoveryReplicationRecoveryPlan#runbook_id}.
        :param script_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#script_path SiteRecoveryReplicationRecoveryPlan#script_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06a640fa3de5bbf3e951e598f4023af764c6cbb5174fdbd06bdc81a470f8d2a7)
            check_type(argname="argument fail_over_directions", value=fail_over_directions, expected_type=type_hints["fail_over_directions"])
            check_type(argname="argument fail_over_types", value=fail_over_types, expected_type=type_hints["fail_over_types"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument fabric_location", value=fabric_location, expected_type=type_hints["fabric_location"])
            check_type(argname="argument manual_action_instruction", value=manual_action_instruction, expected_type=type_hints["manual_action_instruction"])
            check_type(argname="argument runbook_id", value=runbook_id, expected_type=type_hints["runbook_id"])
            check_type(argname="argument script_path", value=script_path, expected_type=type_hints["script_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fail_over_directions": fail_over_directions,
            "fail_over_types": fail_over_types,
            "name": name,
            "type": type,
        }
        if fabric_location is not None:
            self._values["fabric_location"] = fabric_location
        if manual_action_instruction is not None:
            self._values["manual_action_instruction"] = manual_action_instruction
        if runbook_id is not None:
            self._values["runbook_id"] = runbook_id
        if script_path is not None:
            self._values["script_path"] = script_path

    @builtins.property
    def fail_over_directions(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_directions SiteRecoveryReplicationRecoveryPlan#fail_over_directions}.'''
        result = self._values.get("fail_over_directions")
        assert result is not None, "Required property 'fail_over_directions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def fail_over_types(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_types SiteRecoveryReplicationRecoveryPlan#fail_over_types}.'''
        result = self._values.get("fail_over_types")
        assert result is not None, "Required property 'fail_over_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#name SiteRecoveryReplicationRecoveryPlan#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#type SiteRecoveryReplicationRecoveryPlan#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fabric_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fabric_location SiteRecoveryReplicationRecoveryPlan#fabric_location}.'''
        result = self._values.get("fabric_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manual_action_instruction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#manual_action_instruction SiteRecoveryReplicationRecoveryPlan#manual_action_instruction}.'''
        result = self._values.get("manual_action_instruction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runbook_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#runbook_id SiteRecoveryReplicationRecoveryPlan#runbook_id}.'''
        result = self._values.get("runbook_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#script_path SiteRecoveryReplicationRecoveryPlan#script_path}.'''
        result = self._values.get("script_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddc4a62b7e87bbdfc4894885ba7d1a885813c0ac1717dd69f42358a6d13d96bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2c2d67654e1737c7cfc7b3f61ecd0d0b05943780b10a5cc4e093efc2025f666)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc8d30d7226dcb827aa984acfeafb62581b701808cd359063c2c917338bb34d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef40574ddc605a0a04efe45ac8547a757e9d49c9acb1c25a069579eb6879b033)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd892718f24604683497a157d8325c731e5e34e14d97846eaa9ef4a780b769b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac687827f7b6aba6969e645e500c039636debd75b1cb803eee42597c52633ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3b7f185799192290ebc09c6401f6a0e98c1c3a8f0bc544d2d5b010c48881bfa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFabricLocation")
    def reset_fabric_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFabricLocation", []))

    @jsii.member(jsii_name="resetManualActionInstruction")
    def reset_manual_action_instruction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualActionInstruction", []))

    @jsii.member(jsii_name="resetRunbookId")
    def reset_runbook_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunbookId", []))

    @jsii.member(jsii_name="resetScriptPath")
    def reset_script_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptPath", []))

    @builtins.property
    @jsii.member(jsii_name="fabricLocationInput")
    def fabric_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fabricLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="failOverDirectionsInput")
    def fail_over_directions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "failOverDirectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="failOverTypesInput")
    def fail_over_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "failOverTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="manualActionInstructionInput")
    def manual_action_instruction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "manualActionInstructionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="runbookIdInput")
    def runbook_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runbookIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptPathInput")
    def script_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptPathInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="fabricLocation")
    def fabric_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fabricLocation"))

    @fabric_location.setter
    def fabric_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645bc1d64f49246174fa35dea42cb0320d1b36b1af17ac7b9efe3d92cfa0d472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fabricLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOverDirections")
    def fail_over_directions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "failOverDirections"))

    @fail_over_directions.setter
    def fail_over_directions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__786920ba628ed72b5cd41b834735d739ecce09d4ccaa0ee5a68b67c81b325005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOverDirections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOverTypes")
    def fail_over_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "failOverTypes"))

    @fail_over_types.setter
    def fail_over_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd949b6b4113a60d23ebff5abebb69f351275588d0fcd2981ef05bcbdcbdc546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOverTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="manualActionInstruction")
    def manual_action_instruction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "manualActionInstruction"))

    @manual_action_instruction.setter
    def manual_action_instruction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec8993174665b123f9127261b3b25f2b316bc41aed91240e25961bb6ee92d0a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualActionInstruction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df8a9e345555548ce36bfe33a78d70932ea6aaa5374559d29fe256404c51014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runbookId")
    def runbook_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runbookId"))

    @runbook_id.setter
    def runbook_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__067f18b7de4fa243b1ca6fc771b29e11b798c7aa1e1e1c385087d8767eb750d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runbookId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scriptPath")
    def script_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scriptPath"))

    @script_path.setter
    def script_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489f6d79aeb43abc3cdd6f7618c3ae0269cb3eb04ae9720b7682b1f45e757b09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be409a9400bf0a2941cd6c91d94867c98c74826d16e673a655325dffc47b1fe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1ebf11a89207667d253f5a801c5c1f9bce2faa777697a0fc19c5aaecd96a594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup",
    jsii_struct_bases=[],
    name_mapping={"post_action": "postAction", "pre_action": "preAction"},
)
class SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup:
    def __init__(
        self,
        *,
        post_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pre_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param post_action: post_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#post_action SiteRecoveryReplicationRecoveryPlan#post_action}
        :param pre_action: pre_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#pre_action SiteRecoveryReplicationRecoveryPlan#pre_action}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e281a7fedfbddd53714cd30f9d3589c104e5ba0b2fa990a2dec03faf0943a7d)
            check_type(argname="argument post_action", value=post_action, expected_type=type_hints["post_action"])
            check_type(argname="argument pre_action", value=pre_action, expected_type=type_hints["pre_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post_action is not None:
            self._values["post_action"] = post_action
        if pre_action is not None:
            self._values["pre_action"] = pre_action

    @builtins.property
    def post_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction"]]]:
        '''post_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#post_action SiteRecoveryReplicationRecoveryPlan#post_action}
        '''
        result = self._values.get("post_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction"]]], result)

    @builtins.property
    def pre_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction"]]]:
        '''pre_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#pre_action SiteRecoveryReplicationRecoveryPlan#pre_action}
        '''
        result = self._values.get("pre_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45c9875badd1dd15cf4b006fe53c4aef67416be055b805519e452118e9641852)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPostAction")
    def put_post_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__360e858f090e6ddc595e563b05979f508fdc473c02473223e82477be600f3ad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPostAction", [value]))

    @jsii.member(jsii_name="putPreAction")
    def put_pre_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5df77994626c2b2dd6adf11ef0b8e720071f4a57e58673c2585368fdef9c9396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPreAction", [value]))

    @jsii.member(jsii_name="resetPostAction")
    def reset_post_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostAction", []))

    @jsii.member(jsii_name="resetPreAction")
    def reset_pre_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreAction", []))

    @builtins.property
    @jsii.member(jsii_name="postAction")
    def post_action(
        self,
    ) -> "SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostActionList":
        return typing.cast("SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostActionList", jsii.get(self, "postAction"))

    @builtins.property
    @jsii.member(jsii_name="preAction")
    def pre_action(
        self,
    ) -> "SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreActionList":
        return typing.cast("SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreActionList", jsii.get(self, "preAction"))

    @builtins.property
    @jsii.member(jsii_name="postActionInput")
    def post_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction"]]], jsii.get(self, "postActionInput"))

    @builtins.property
    @jsii.member(jsii_name="preActionInput")
    def pre_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction"]]], jsii.get(self, "preActionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup]:
        return typing.cast(typing.Optional[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23d76189d6b17b149ecc500695db359931ed29ed04667f3e42c353f38e88fbb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction",
    jsii_struct_bases=[],
    name_mapping={
        "fail_over_directions": "failOverDirections",
        "fail_over_types": "failOverTypes",
        "name": "name",
        "type": "type",
        "fabric_location": "fabricLocation",
        "manual_action_instruction": "manualActionInstruction",
        "runbook_id": "runbookId",
        "script_path": "scriptPath",
    },
)
class SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction:
    def __init__(
        self,
        *,
        fail_over_directions: typing.Sequence[builtins.str],
        fail_over_types: typing.Sequence[builtins.str],
        name: builtins.str,
        type: builtins.str,
        fabric_location: typing.Optional[builtins.str] = None,
        manual_action_instruction: typing.Optional[builtins.str] = None,
        runbook_id: typing.Optional[builtins.str] = None,
        script_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fail_over_directions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_directions SiteRecoveryReplicationRecoveryPlan#fail_over_directions}.
        :param fail_over_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_types SiteRecoveryReplicationRecoveryPlan#fail_over_types}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#name SiteRecoveryReplicationRecoveryPlan#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#type SiteRecoveryReplicationRecoveryPlan#type}.
        :param fabric_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fabric_location SiteRecoveryReplicationRecoveryPlan#fabric_location}.
        :param manual_action_instruction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#manual_action_instruction SiteRecoveryReplicationRecoveryPlan#manual_action_instruction}.
        :param runbook_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#runbook_id SiteRecoveryReplicationRecoveryPlan#runbook_id}.
        :param script_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#script_path SiteRecoveryReplicationRecoveryPlan#script_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4818c3d1571f1dd9179753951729872abb8090834498e1ff9ab0df694a213860)
            check_type(argname="argument fail_over_directions", value=fail_over_directions, expected_type=type_hints["fail_over_directions"])
            check_type(argname="argument fail_over_types", value=fail_over_types, expected_type=type_hints["fail_over_types"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument fabric_location", value=fabric_location, expected_type=type_hints["fabric_location"])
            check_type(argname="argument manual_action_instruction", value=manual_action_instruction, expected_type=type_hints["manual_action_instruction"])
            check_type(argname="argument runbook_id", value=runbook_id, expected_type=type_hints["runbook_id"])
            check_type(argname="argument script_path", value=script_path, expected_type=type_hints["script_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fail_over_directions": fail_over_directions,
            "fail_over_types": fail_over_types,
            "name": name,
            "type": type,
        }
        if fabric_location is not None:
            self._values["fabric_location"] = fabric_location
        if manual_action_instruction is not None:
            self._values["manual_action_instruction"] = manual_action_instruction
        if runbook_id is not None:
            self._values["runbook_id"] = runbook_id
        if script_path is not None:
            self._values["script_path"] = script_path

    @builtins.property
    def fail_over_directions(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_directions SiteRecoveryReplicationRecoveryPlan#fail_over_directions}.'''
        result = self._values.get("fail_over_directions")
        assert result is not None, "Required property 'fail_over_directions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def fail_over_types(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_types SiteRecoveryReplicationRecoveryPlan#fail_over_types}.'''
        result = self._values.get("fail_over_types")
        assert result is not None, "Required property 'fail_over_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#name SiteRecoveryReplicationRecoveryPlan#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#type SiteRecoveryReplicationRecoveryPlan#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fabric_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fabric_location SiteRecoveryReplicationRecoveryPlan#fabric_location}.'''
        result = self._values.get("fabric_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manual_action_instruction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#manual_action_instruction SiteRecoveryReplicationRecoveryPlan#manual_action_instruction}.'''
        result = self._values.get("manual_action_instruction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runbook_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#runbook_id SiteRecoveryReplicationRecoveryPlan#runbook_id}.'''
        result = self._values.get("runbook_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#script_path SiteRecoveryReplicationRecoveryPlan#script_path}.'''
        result = self._values.get("script_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13c2c971656f1e541661837ccbcccb02ca5179ada247f402b411850f7f07ac7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf34df28c5c46193c508790ab93a1d41417022da001fe2b3811c1adbd8b8cc7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__669558a4b6ac3f7fc9b56bcc165fb5bfd17cdb24decfb2e253b680bfec2191fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ed4b27cd66ef558687a087a4731e02c9e89b47d94d57b65efe3e0d1e8bb64b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f973da94cbd0fbc2414a5084b0c53680a9a711a86573633e9da303bdadaed30a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f310b4b34aaf8e7cde926b73d86b2abb62b2599e9040957ee943ba683c63b9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9ca74657c9348a044a3f5f961ca96a48f5d6ad3ddaab0b7a66b890ca5add1f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFabricLocation")
    def reset_fabric_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFabricLocation", []))

    @jsii.member(jsii_name="resetManualActionInstruction")
    def reset_manual_action_instruction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualActionInstruction", []))

    @jsii.member(jsii_name="resetRunbookId")
    def reset_runbook_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunbookId", []))

    @jsii.member(jsii_name="resetScriptPath")
    def reset_script_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptPath", []))

    @builtins.property
    @jsii.member(jsii_name="fabricLocationInput")
    def fabric_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fabricLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="failOverDirectionsInput")
    def fail_over_directions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "failOverDirectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="failOverTypesInput")
    def fail_over_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "failOverTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="manualActionInstructionInput")
    def manual_action_instruction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "manualActionInstructionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="runbookIdInput")
    def runbook_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runbookIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptPathInput")
    def script_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptPathInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="fabricLocation")
    def fabric_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fabricLocation"))

    @fabric_location.setter
    def fabric_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e71288e524bc4621069ff0f0836c92af2d751825b09a7b2a0a7d471479c68c8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fabricLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOverDirections")
    def fail_over_directions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "failOverDirections"))

    @fail_over_directions.setter
    def fail_over_directions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38bf91ff9e9d865ca54065432bb53aeb088984879b2eb81082bbbebb407099cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOverDirections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOverTypes")
    def fail_over_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "failOverTypes"))

    @fail_over_types.setter
    def fail_over_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a1268652d895c25555bae79cb139759c98b06c60060e7feafdccec390ee73c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOverTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="manualActionInstruction")
    def manual_action_instruction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "manualActionInstruction"))

    @manual_action_instruction.setter
    def manual_action_instruction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a09e6fd3c89ff572b4e430575a63c5c9592f6951a11cf698cb1685c3cd4830f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualActionInstruction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13163e6f21b0dff8afcc77b7344e547abd2b6215e4a8b53a3e01c028ea7e9847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runbookId")
    def runbook_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runbookId"))

    @runbook_id.setter
    def runbook_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58ab2ec46130a47cf8d88500d2e9d2c37ece85e0ab4bace053ca77a0404c5e1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runbookId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scriptPath")
    def script_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scriptPath"))

    @script_path.setter
    def script_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c3b9a037feb5a51d629d1db71a06f670dc42a044b8013c0ef505cb8987a2b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002af75e5e44240ae5eae2795d5e1ac53c643e861536dc9f7cb6a8466de30743)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e5285dc5140cc36ef3765aaf31ed65dc9567712617afbb5ed0bb40d927d20ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction",
    jsii_struct_bases=[],
    name_mapping={
        "fail_over_directions": "failOverDirections",
        "fail_over_types": "failOverTypes",
        "name": "name",
        "type": "type",
        "fabric_location": "fabricLocation",
        "manual_action_instruction": "manualActionInstruction",
        "runbook_id": "runbookId",
        "script_path": "scriptPath",
    },
)
class SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction:
    def __init__(
        self,
        *,
        fail_over_directions: typing.Sequence[builtins.str],
        fail_over_types: typing.Sequence[builtins.str],
        name: builtins.str,
        type: builtins.str,
        fabric_location: typing.Optional[builtins.str] = None,
        manual_action_instruction: typing.Optional[builtins.str] = None,
        runbook_id: typing.Optional[builtins.str] = None,
        script_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fail_over_directions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_directions SiteRecoveryReplicationRecoveryPlan#fail_over_directions}.
        :param fail_over_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_types SiteRecoveryReplicationRecoveryPlan#fail_over_types}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#name SiteRecoveryReplicationRecoveryPlan#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#type SiteRecoveryReplicationRecoveryPlan#type}.
        :param fabric_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fabric_location SiteRecoveryReplicationRecoveryPlan#fabric_location}.
        :param manual_action_instruction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#manual_action_instruction SiteRecoveryReplicationRecoveryPlan#manual_action_instruction}.
        :param runbook_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#runbook_id SiteRecoveryReplicationRecoveryPlan#runbook_id}.
        :param script_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#script_path SiteRecoveryReplicationRecoveryPlan#script_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20c8260a699ad08e88aaad0d5772519368a10cec4f0841c676a790574192fff4)
            check_type(argname="argument fail_over_directions", value=fail_over_directions, expected_type=type_hints["fail_over_directions"])
            check_type(argname="argument fail_over_types", value=fail_over_types, expected_type=type_hints["fail_over_types"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument fabric_location", value=fabric_location, expected_type=type_hints["fabric_location"])
            check_type(argname="argument manual_action_instruction", value=manual_action_instruction, expected_type=type_hints["manual_action_instruction"])
            check_type(argname="argument runbook_id", value=runbook_id, expected_type=type_hints["runbook_id"])
            check_type(argname="argument script_path", value=script_path, expected_type=type_hints["script_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fail_over_directions": fail_over_directions,
            "fail_over_types": fail_over_types,
            "name": name,
            "type": type,
        }
        if fabric_location is not None:
            self._values["fabric_location"] = fabric_location
        if manual_action_instruction is not None:
            self._values["manual_action_instruction"] = manual_action_instruction
        if runbook_id is not None:
            self._values["runbook_id"] = runbook_id
        if script_path is not None:
            self._values["script_path"] = script_path

    @builtins.property
    def fail_over_directions(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_directions SiteRecoveryReplicationRecoveryPlan#fail_over_directions}.'''
        result = self._values.get("fail_over_directions")
        assert result is not None, "Required property 'fail_over_directions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def fail_over_types(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fail_over_types SiteRecoveryReplicationRecoveryPlan#fail_over_types}.'''
        result = self._values.get("fail_over_types")
        assert result is not None, "Required property 'fail_over_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#name SiteRecoveryReplicationRecoveryPlan#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#type SiteRecoveryReplicationRecoveryPlan#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fabric_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#fabric_location SiteRecoveryReplicationRecoveryPlan#fabric_location}.'''
        result = self._values.get("fabric_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manual_action_instruction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#manual_action_instruction SiteRecoveryReplicationRecoveryPlan#manual_action_instruction}.'''
        result = self._values.get("manual_action_instruction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runbook_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#runbook_id SiteRecoveryReplicationRecoveryPlan#runbook_id}.'''
        result = self._values.get("runbook_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#script_path SiteRecoveryReplicationRecoveryPlan#script_path}.'''
        result = self._values.get("script_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5aa8a39d362d87a2d880805f94767d4e900ed37ce5200f2daab7609ef85531f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38504cc8a2113f79805e5be319a6f0ee30157790c57e43daf1fe54c5bf76137a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ddf04a61d82f8b90f7bd968333e8be2d5a44f2497d42c2b3233ef05de783a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7e8e6ac77c89734ce1824bd61fb9b1f71e023f3428baa85ab529680fa9d6736)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdd28fa606f013028fc3017c653563e339e4477cdd6947fc1e37482606761c51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb3ae50d87f512ec02d5d4583413cdb3d0944978712637982f8b1658f5283a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e108ae7783a0fd66af001a9468834ba14d4004a1baf5769a1880508b364e540)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFabricLocation")
    def reset_fabric_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFabricLocation", []))

    @jsii.member(jsii_name="resetManualActionInstruction")
    def reset_manual_action_instruction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualActionInstruction", []))

    @jsii.member(jsii_name="resetRunbookId")
    def reset_runbook_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunbookId", []))

    @jsii.member(jsii_name="resetScriptPath")
    def reset_script_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptPath", []))

    @builtins.property
    @jsii.member(jsii_name="fabricLocationInput")
    def fabric_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fabricLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="failOverDirectionsInput")
    def fail_over_directions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "failOverDirectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="failOverTypesInput")
    def fail_over_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "failOverTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="manualActionInstructionInput")
    def manual_action_instruction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "manualActionInstructionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="runbookIdInput")
    def runbook_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runbookIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptPathInput")
    def script_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptPathInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="fabricLocation")
    def fabric_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fabricLocation"))

    @fabric_location.setter
    def fabric_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3b391fe256b10897bde65712cb3c11ddc80458ea43efe32a748ea56ba5464a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fabricLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOverDirections")
    def fail_over_directions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "failOverDirections"))

    @fail_over_directions.setter
    def fail_over_directions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba4bf91ffad6394068f6d89d69882eb55dca6bbfb7b6e114f68b9fe66765cbbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOverDirections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOverTypes")
    def fail_over_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "failOverTypes"))

    @fail_over_types.setter
    def fail_over_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51b4b8f2cf82e0b977b16afb6986372fd67b20109883417e1b1ac7b8ec71b146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOverTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="manualActionInstruction")
    def manual_action_instruction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "manualActionInstruction"))

    @manual_action_instruction.setter
    def manual_action_instruction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49be9f6bf8d643a339a2010d098ecac0cdc7ae8f43de782f5dafd8a825dde38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualActionInstruction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ad348828ed1edcc96e385cb913c0d8a34ff846899092b4e00f2cea5565a231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runbookId")
    def runbook_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runbookId"))

    @runbook_id.setter
    def runbook_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bcb1c70b2de968121d6f41a0598544dfd2c4ba2c29c7996cd3a2b9b3313301f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runbookId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scriptPath")
    def script_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scriptPath"))

    @script_path.setter
    def script_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d056b2e58755803212506517367d899fa1cf0352be744196d3c8fd92b26641fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d42a4fc69e68618622fe9b2d4d0e4c51e0fde0fca1f71955547d5ccbaff12d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ce7a545fc335065eef46fe7fc2deaedf62bc79b590bc8f21f4572d2fbd7d93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SiteRecoveryReplicationRecoveryPlanTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#create SiteRecoveryReplicationRecoveryPlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#delete SiteRecoveryReplicationRecoveryPlan#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#read SiteRecoveryReplicationRecoveryPlan#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#update SiteRecoveryReplicationRecoveryPlan#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58c92f3e49fca0fc57aea5c5fddcaab3ebfca0a3bf47820ea88dae027e17aff)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#create SiteRecoveryReplicationRecoveryPlan#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#delete SiteRecoveryReplicationRecoveryPlan#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#read SiteRecoveryReplicationRecoveryPlan#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/site_recovery_replication_recovery_plan#update SiteRecoveryReplicationRecoveryPlan#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SiteRecoveryReplicationRecoveryPlanTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SiteRecoveryReplicationRecoveryPlanTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.siteRecoveryReplicationRecoveryPlan.SiteRecoveryReplicationRecoveryPlanTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0e2b9a3e264550d284bf37c7d1f4f92e72d058f8efdcab71846db6ea7e6e8b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__908963d13a5a1fb00edb6b584aa07c1669f6bc8091c57b07168a2f90f2828e75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__973a8e3388b3332d4144b899051d1a3a9b6195d3c33fb66f2b9e80c0702c7d69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a8b8888e2cc3ea24e7ec3c7af0482db75a8e52280ee92df6a2c60c97d361b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d63d33082c458119de0b67f6cea4dfb247e7b48448d269afb214a2ebfc5fba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb913c8bb96af6173c654591aeb1db1fb3611d948b590a98c092813f26aa8f0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SiteRecoveryReplicationRecoveryPlan",
    "SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings",
    "SiteRecoveryReplicationRecoveryPlanAzureToAzureSettingsOutputReference",
    "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup",
    "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupList",
    "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupOutputReference",
    "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction",
    "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostActionList",
    "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostActionOutputReference",
    "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction",
    "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreActionList",
    "SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreActionOutputReference",
    "SiteRecoveryReplicationRecoveryPlanConfig",
    "SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup",
    "SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupOutputReference",
    "SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction",
    "SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostActionList",
    "SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostActionOutputReference",
    "SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction",
    "SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreActionList",
    "SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreActionOutputReference",
    "SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup",
    "SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupOutputReference",
    "SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction",
    "SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostActionList",
    "SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostActionOutputReference",
    "SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction",
    "SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreActionList",
    "SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreActionOutputReference",
    "SiteRecoveryReplicationRecoveryPlanTimeouts",
    "SiteRecoveryReplicationRecoveryPlanTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__aedea51b38ad30e9028c148d4a78f46e5eb52a8b076de0aa694b0ae87dfd112a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    boot_recovery_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup, typing.Dict[builtins.str, typing.Any]]]],
    failover_recovery_group: typing.Union[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    recovery_vault_id: builtins.str,
    shutdown_recovery_group: typing.Union[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup, typing.Dict[builtins.str, typing.Any]],
    source_recovery_fabric_id: builtins.str,
    target_recovery_fabric_id: builtins.str,
    azure_to_azure_settings: typing.Optional[typing.Union[SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SiteRecoveryReplicationRecoveryPlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8d80dbe812bfab9f24b81ab9761a90e6d49a5641b1b4b08cf2cb66b4416c198d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8cf87bb246466cebb37e12ba1c9a4b735def5f448b7e9f256c72e40971c5382(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee355680b8e194ef0876852c8dea1e27bc12d65a467f28ab108366411c7f183b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b3399611c4c5e49977e9de0cb86ddc8d51699822c5cf5754825f54ea41fba37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df87245229d2aac4c67cabbdfa5a394fd81b35a33765e47ab1190765d4be122e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb2a5e3579d6168a5020c8ace78b19cb633865cb4ca99a424d8a191496a6126(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4457f570effbf69c634f881a3d03a864d9ad62ec0ebf1f62317a8a3a39de28d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db13e1ec6494fe3d59bb5bfe26b07705106599640f14d7f4880feb70d48d2c9(
    *,
    primary_edge_zone: typing.Optional[builtins.str] = None,
    primary_zone: typing.Optional[builtins.str] = None,
    recovery_edge_zone: typing.Optional[builtins.str] = None,
    recovery_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1de2ccdc63cd15e75fcc80a6d5021ce0954b055fd91a9d86d8d73f0a48dffae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095f08cbc4ebcd820fb5cc38cdcaca2a716b2b0feb1c6699ec6b5d07b7ffc843(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed45b4466e9e75585f5d5c05e070b547b9ef2b830826ba4bbf3acd82ea0b4399(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a46a7db5ebbac14385f31b1910cb397f1dad5470fb8dfea31dd6fb91f99fed3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8405493fd92865d0b6b66e82ee9ac9ef8e3eadd509e3beda7ff24dd01abdd883(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a23cf0b0b9a0891573230a0c98c0a9b907179c4b5a1bc8fb649b35a65899abc(
    value: typing.Optional[SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c90eeb209696efac7a14d6d5547ea7555bc2609fbde1cff9d756a2b49b63b0(
    *,
    post_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pre_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    replicated_protected_items: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9d2e129cbf752e571cd9c764f5c587256e84f79ec7de168cdc32858de15a39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cced8b592e07abfca7506d0cb9b62df0f6a90980b4889ffd73e0b6e8a88e6db9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c88c2e1a7f000b934b9b89d2cbd1674254ab99a4b8572fb171e28c35fae87c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2815d6ca839cd0ef038bb630d3ead594193564747c9076673a3d0335848e53a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e586eae0d0525a150bbd332eed2feeba518768f6f2160fc53db940e92c7b850d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f4f5907f081eb932762d216c40f1c55d0fa8237476f4c3278f33784110c3e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51483dc50399f9a597368720c9d5014b06f0e0409febe748a090d64d16590697(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d813330572d9b913c7648363c1b81ffeef26e6e80b276fa3fc222f7dd2e591(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e828df7ff132fb35fa6dcd18ec9a20afd55f56eab1cd6e8829390707f087d203(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b9da7bbd198b60bb2f48b804b90b4db96a26b05bdebb39c639404bf3796bcf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__107478ac8e95356bccef019f28f052bf119dbbf677973d82c1d6635b6b9266b4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7c89d14aa4ba9d36dc909178bf6cffd26d79f31974126b2c5bc4b1d81b9e01(
    *,
    fail_over_directions: typing.Sequence[builtins.str],
    fail_over_types: typing.Sequence[builtins.str],
    name: builtins.str,
    type: builtins.str,
    fabric_location: typing.Optional[builtins.str] = None,
    manual_action_instruction: typing.Optional[builtins.str] = None,
    runbook_id: typing.Optional[builtins.str] = None,
    script_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__302a0a0ebcec62bb0b17f86c3891bfcb8716b4642a5e9e4c8d86f9d1133ddd74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17362306c4026a30a267c3dd7f7321f57d983a608fe4f791cbf8b1cfd27ade70(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e1ca96f6910467f00c814587385981d0b9c94d935ec406a67d6e554686f95b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24399f45935b5f655d10041dd3c1e8187668f8fb35c30590988679a73dee6ff6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ed35eab052329c198fda77f15ca6a652d7942848160698d62e41cae6a3cc5e0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fafd8a0544d73424277f08039f259a0dc27ac7f10bf1a931ebac69c013c42ffc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1adaf94f460e2407cee7ca0f5f6992d4ec19bbee0937f26ec94a143ba58660b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5737aa1ecaac0dc567a749069b09d7a1458a661922c163303774f3a8761fd03a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1547e34022ba62032cdf0b8c3926f51b61a3233d3cb0df3e845a159212befd75(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c39c1cbed052facacfaa77bd2fc0e8d75e1d41715f0653abfcedc5b63a6eeb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8bd66fdba9eaf751cae6e1eb0c3b39ab9782e863ce7a42ff1008f5885521d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87460da41cbc422aecf2d10755d68545ef1a5f62c6ee9ed82edd711b49d57827(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66363525067c947e675fa7e266be303e4a2b837ca0c1e52331e4d80ad9e8bd41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcce037c7bf0fab7d7dc32452ef58b78addd03f6d42802071fd0ddb58edbf50a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ea9410656bed37db43f41a795ec1ce54c85fa93d57a31276f94f3a02109c20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d566f33e900aed3ea6723808d8c964de5473bcb26e2c0b921bddf20cee32342f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPostAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1def9547d346bf4817906f5e6b47ffece3baaf1200698965779823d2dee8c90e(
    *,
    fail_over_directions: typing.Sequence[builtins.str],
    fail_over_types: typing.Sequence[builtins.str],
    name: builtins.str,
    type: builtins.str,
    fabric_location: typing.Optional[builtins.str] = None,
    manual_action_instruction: typing.Optional[builtins.str] = None,
    runbook_id: typing.Optional[builtins.str] = None,
    script_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d983b7cf24286e98103e691065b8cdb5bb7d2979fa9233ff9a0d7bae2c2f7914(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330f5ebf08d0ef795a7a62d52f0b0e3f10a90ccf1ad8ed832aa1d200173ac0ff(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c23d093406f4170fb728f62e01568882cb540b5effca56be4325323341321aaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__239d6676139a45c8b389b1530ac189720a01450f73ab82d15e7d6895918f5004(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7caf8affb09ec55592b1098a6c8d476a6fdc266c696fb176d9e617066a8183c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb7f5594334b322521e752a80025b1760b14bffd2fb7735599c2a11121122bb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e4b03a728625161d6211046e7f54436e826cce5f56bab9a664bf488a69bb93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd4f13b62161effc7c3b26499ff9751443e132aaeedec70380de1e3b438d7ff8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e9c6d29836c62663345b99ce8bcc8d0a53cb8069247d0759c628361be336cd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ea1c8d172ec8604a95b0896eff39bd10fd0c2cabe06f3173ab8c6fa354e8cd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48fe90856a6721efaf4076ccf27bc42325d6f30d08fbec5b65678591c111c868(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd80f1eb3c85d8553a956d21681569abc96039b960395943f4bb913c15cb01d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbac8779deb4354a2ca5fcf99f5d11148e0d20c4f7a3928f965d77dd373b8565(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a730c2d69cb1d9a506efddc5df89508fb756e6ba5e62bec45296c7e01c51bb00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c929ef61b3422b39b8db41f458cddcfd5fa534400f0e1567f64f486218458a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479427db9287a461f893280d6b8d5e5af1fa9a50cc873e3c0dad55581fa37470(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanBootRecoveryGroupPreAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df27bcf614e7715749244a844445eab7b01373b56a2b4f8848018c1be15c8b0f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    boot_recovery_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicationRecoveryPlanBootRecoveryGroup, typing.Dict[builtins.str, typing.Any]]]],
    failover_recovery_group: typing.Union[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    recovery_vault_id: builtins.str,
    shutdown_recovery_group: typing.Union[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup, typing.Dict[builtins.str, typing.Any]],
    source_recovery_fabric_id: builtins.str,
    target_recovery_fabric_id: builtins.str,
    azure_to_azure_settings: typing.Optional[typing.Union[SiteRecoveryReplicationRecoveryPlanAzureToAzureSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SiteRecoveryReplicationRecoveryPlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd6caab3495f946ddf542c356563e635e65726bd3d5575afbd67a76fed03b65(
    *,
    post_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pre_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6bfb48d2a9d5a3fc13affba959387ae75eff4ad3b0f1fbb7bd415da2830886b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e3499a94a1083cc0616991f1d6f58707ed21f9f0dd7a24109d63bcbd7a17b38(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e638e736291cdc7b1e669a59843375a00d8f888294c6dd04f38e199bb025993(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a981f3c95c33ab0a76a96431a96447a10e69e71441b9abe4134aa1855b73a2f7(
    value: typing.Optional[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c3b6d45935a09c7c26a08b43d869d36dc0a96740feda183be4c8e018be75a5(
    *,
    fail_over_directions: typing.Sequence[builtins.str],
    fail_over_types: typing.Sequence[builtins.str],
    name: builtins.str,
    type: builtins.str,
    fabric_location: typing.Optional[builtins.str] = None,
    manual_action_instruction: typing.Optional[builtins.str] = None,
    runbook_id: typing.Optional[builtins.str] = None,
    script_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd2a6210deeedd36a8c6af091ed40a4db72ab3c3db7c969d3ba37c081800dee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c980fafe0a233ae6a47bf12e210dc2cba3f9b9533d71928e501f75fa07685a2a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63288d3e3a081c6a7a6f5f4753e59d2b2c9e56fba22fc4e1b47a10b3f2809069(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec8655c551f448e48d62ff532b796e8430dafbd501940d2a3700d9f2adfe8c8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ddbf31b3a8cdce7975af6626d8c337eedb0c619d17034f98cf8ee846f4f1e04(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d13ae91ef669c93e99e1ae3f4ab5fe60ac556ead194f7a2f57899322a76081(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ac47616f631f5d301d07b23d395633d7c21f913aa10e25f1dde072a0edfe95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf27d2e3259b39e35f73697dd9a745fb376903127b4a9c008f38330f8005cb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c31036065be9e2d63f80e212ac74ecaf8e280e3707c87765f3c2ffe7026466(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c1a82d7e7f948d559457ab3f3e87446a2baa77b908b53c832c9ad6cb31fa61(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d82e02089f7c36bcc61d613647dac257e5d48dc9c0daf85d2d5457a5e0ac6982(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6b8eb4b5f39a5cffa95c28371a9604a2faf458073c8b1013dec6fd8efb78ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f186dcb3c0b8003d854498d05ef83ae66c67a7ebda0713eeae9e54b9a06a1254(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29320935efa4cf749f156672bddf145209cd7454eab8ba0c5463a15138435679(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a78bcbf65f4faebcd8ddb981c194997337aa488694c9deec948925e9e85a16f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02929c08245643f903569e1004e999eab6e0d431fa5c63e26d6d9c36cf20e7af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPostAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a640fa3de5bbf3e951e598f4023af764c6cbb5174fdbd06bdc81a470f8d2a7(
    *,
    fail_over_directions: typing.Sequence[builtins.str],
    fail_over_types: typing.Sequence[builtins.str],
    name: builtins.str,
    type: builtins.str,
    fabric_location: typing.Optional[builtins.str] = None,
    manual_action_instruction: typing.Optional[builtins.str] = None,
    runbook_id: typing.Optional[builtins.str] = None,
    script_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc4a62b7e87bbdfc4894885ba7d1a885813c0ac1717dd69f42358a6d13d96bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c2d67654e1737c7cfc7b3f61ecd0d0b05943780b10a5cc4e093efc2025f666(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8d30d7226dcb827aa984acfeafb62581b701808cd359063c2c917338bb34d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef40574ddc605a0a04efe45ac8547a757e9d49c9acb1c25a069579eb6879b033(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd892718f24604683497a157d8325c731e5e34e14d97846eaa9ef4a780b769b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac687827f7b6aba6969e645e500c039636debd75b1cb803eee42597c52633ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b7f185799192290ebc09c6401f6a0e98c1c3a8f0bc544d2d5b010c48881bfa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645bc1d64f49246174fa35dea42cb0320d1b36b1af17ac7b9efe3d92cfa0d472(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786920ba628ed72b5cd41b834735d739ecce09d4ccaa0ee5a68b67c81b325005(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd949b6b4113a60d23ebff5abebb69f351275588d0fcd2981ef05bcbdcbdc546(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec8993174665b123f9127261b3b25f2b316bc41aed91240e25961bb6ee92d0a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df8a9e345555548ce36bfe33a78d70932ea6aaa5374559d29fe256404c51014(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067f18b7de4fa243b1ca6fc771b29e11b798c7aa1e1e1c385087d8767eb750d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489f6d79aeb43abc3cdd6f7618c3ae0269cb3eb04ae9720b7682b1f45e757b09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be409a9400bf0a2941cd6c91d94867c98c74826d16e673a655325dffc47b1fe2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ebf11a89207667d253f5a801c5c1f9bce2faa777697a0fc19c5aaecd96a594(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanFailoverRecoveryGroupPreAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e281a7fedfbddd53714cd30f9d3589c104e5ba0b2fa990a2dec03faf0943a7d(
    *,
    post_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pre_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c9875badd1dd15cf4b006fe53c4aef67416be055b805519e452118e9641852(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360e858f090e6ddc595e563b05979f508fdc473c02473223e82477be600f3ad1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df77994626c2b2dd6adf11ef0b8e720071f4a57e58673c2585368fdef9c9396(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23d76189d6b17b149ecc500695db359931ed29ed04667f3e42c353f38e88fbb2(
    value: typing.Optional[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4818c3d1571f1dd9179753951729872abb8090834498e1ff9ab0df694a213860(
    *,
    fail_over_directions: typing.Sequence[builtins.str],
    fail_over_types: typing.Sequence[builtins.str],
    name: builtins.str,
    type: builtins.str,
    fabric_location: typing.Optional[builtins.str] = None,
    manual_action_instruction: typing.Optional[builtins.str] = None,
    runbook_id: typing.Optional[builtins.str] = None,
    script_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c2c971656f1e541661837ccbcccb02ca5179ada247f402b411850f7f07ac7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf34df28c5c46193c508790ab93a1d41417022da001fe2b3811c1adbd8b8cc7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__669558a4b6ac3f7fc9b56bcc165fb5bfd17cdb24decfb2e253b680bfec2191fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed4b27cd66ef558687a087a4731e02c9e89b47d94d57b65efe3e0d1e8bb64b2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f973da94cbd0fbc2414a5084b0c53680a9a711a86573633e9da303bdadaed30a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f310b4b34aaf8e7cde926b73d86b2abb62b2599e9040957ee943ba683c63b9f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ca74657c9348a044a3f5f961ca96a48f5d6ad3ddaab0b7a66b890ca5add1f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e71288e524bc4621069ff0f0836c92af2d751825b09a7b2a0a7d471479c68c8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38bf91ff9e9d865ca54065432bb53aeb088984879b2eb81082bbbebb407099cb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a1268652d895c25555bae79cb139759c98b06c60060e7feafdccec390ee73c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a09e6fd3c89ff572b4e430575a63c5c9592f6951a11cf698cb1685c3cd4830f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13163e6f21b0dff8afcc77b7344e547abd2b6215e4a8b53a3e01c028ea7e9847(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58ab2ec46130a47cf8d88500d2e9d2c37ece85e0ab4bace053ca77a0404c5e1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c3b9a037feb5a51d629d1db71a06f670dc42a044b8013c0ef505cb8987a2b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002af75e5e44240ae5eae2795d5e1ac53c643e861536dc9f7cb6a8466de30743(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e5285dc5140cc36ef3765aaf31ed65dc9567712617afbb5ed0bb40d927d20ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPostAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c8260a699ad08e88aaad0d5772519368a10cec4f0841c676a790574192fff4(
    *,
    fail_over_directions: typing.Sequence[builtins.str],
    fail_over_types: typing.Sequence[builtins.str],
    name: builtins.str,
    type: builtins.str,
    fabric_location: typing.Optional[builtins.str] = None,
    manual_action_instruction: typing.Optional[builtins.str] = None,
    runbook_id: typing.Optional[builtins.str] = None,
    script_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5aa8a39d362d87a2d880805f94767d4e900ed37ce5200f2daab7609ef85531f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38504cc8a2113f79805e5be319a6f0ee30157790c57e43daf1fe54c5bf76137a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ddf04a61d82f8b90f7bd968333e8be2d5a44f2497d42c2b3233ef05de783a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e8e6ac77c89734ce1824bd61fb9b1f71e023f3428baa85ab529680fa9d6736(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd28fa606f013028fc3017c653563e339e4477cdd6947fc1e37482606761c51(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb3ae50d87f512ec02d5d4583413cdb3d0944978712637982f8b1658f5283a1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e108ae7783a0fd66af001a9468834ba14d4004a1baf5769a1880508b364e540(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3b391fe256b10897bde65712cb3c11ddc80458ea43efe32a748ea56ba5464a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba4bf91ffad6394068f6d89d69882eb55dca6bbfb7b6e114f68b9fe66765cbbd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b4b8f2cf82e0b977b16afb6986372fd67b20109883417e1b1ac7b8ec71b146(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49be9f6bf8d643a339a2010d098ecac0cdc7ae8f43de782f5dafd8a825dde38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ad348828ed1edcc96e385cb913c0d8a34ff846899092b4e00f2cea5565a231(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bcb1c70b2de968121d6f41a0598544dfd2c4ba2c29c7996cd3a2b9b3313301f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d056b2e58755803212506517367d899fa1cf0352be744196d3c8fd92b26641fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d42a4fc69e68618622fe9b2d4d0e4c51e0fde0fca1f71955547d5ccbaff12d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ce7a545fc335065eef46fe7fc2deaedf62bc79b590bc8f21f4572d2fbd7d93(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanShutdownRecoveryGroupPreAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58c92f3e49fca0fc57aea5c5fddcaab3ebfca0a3bf47820ea88dae027e17aff(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e2b9a3e264550d284bf37c7d1f4f92e72d058f8efdcab71846db6ea7e6e8b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908963d13a5a1fb00edb6b584aa07c1669f6bc8091c57b07168a2f90f2828e75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973a8e3388b3332d4144b899051d1a3a9b6195d3c33fb66f2b9e80c0702c7d69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a8b8888e2cc3ea24e7ec3c7af0482db75a8e52280ee92df6a2c60c97d361b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d63d33082c458119de0b67f6cea4dfb247e7b48448d269afb214a2ebfc5fba6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb913c8bb96af6173c654591aeb1db1fb3611d948b590a98c092813f26aa8f0b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SiteRecoveryReplicationRecoveryPlanTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
