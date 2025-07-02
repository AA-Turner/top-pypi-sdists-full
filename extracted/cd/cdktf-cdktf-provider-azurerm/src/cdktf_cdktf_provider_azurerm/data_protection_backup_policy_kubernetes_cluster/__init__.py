r'''
# `azurerm_data_protection_backup_policy_kubernetes_cluster`

Refer to the Terraform Registry for docs: [`azurerm_data_protection_backup_policy_kubernetes_cluster`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster).
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


class DataProtectionBackupPolicyKubernetesCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyKubernetesCluster.DataProtectionBackupPolicyKubernetesCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster azurerm_data_protection_backup_policy_kubernetes_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        backup_repeating_time_intervals: typing.Sequence[builtins.str],
        default_retention_rule: typing.Union["DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        resource_group_name: builtins.str,
        vault_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        retention_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProtectionBackupPolicyKubernetesClusterRetentionRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["DataProtectionBackupPolicyKubernetesClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster azurerm_data_protection_backup_policy_kubernetes_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param backup_repeating_time_intervals: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#backup_repeating_time_intervals DataProtectionBackupPolicyKubernetesCluster#backup_repeating_time_intervals}.
        :param default_retention_rule: default_retention_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#default_retention_rule DataProtectionBackupPolicyKubernetesCluster#default_retention_rule}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#name DataProtectionBackupPolicyKubernetesCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#resource_group_name DataProtectionBackupPolicyKubernetesCluster#resource_group_name}.
        :param vault_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#vault_name DataProtectionBackupPolicyKubernetesCluster#vault_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#id DataProtectionBackupPolicyKubernetesCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param retention_rule: retention_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#retention_rule DataProtectionBackupPolicyKubernetesCluster#retention_rule}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#timeouts DataProtectionBackupPolicyKubernetesCluster#timeouts}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#time_zone DataProtectionBackupPolicyKubernetesCluster#time_zone}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22e07317ed4705141cfe42c0dbb98b748e70cdc1d5c1692dc589977689907d7a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataProtectionBackupPolicyKubernetesClusterConfig(
            backup_repeating_time_intervals=backup_repeating_time_intervals,
            default_retention_rule=default_retention_rule,
            name=name,
            resource_group_name=resource_group_name,
            vault_name=vault_name,
            id=id,
            retention_rule=retention_rule,
            timeouts=timeouts,
            time_zone=time_zone,
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
        '''Generates CDKTF code for importing a DataProtectionBackupPolicyKubernetesCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataProtectionBackupPolicyKubernetesCluster to import.
        :param import_from_id: The id of the existing DataProtectionBackupPolicyKubernetesCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataProtectionBackupPolicyKubernetesCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee07f5487f927e3d78dda13e03a2dabe639a2d28f82d6531a996850153bf13d8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDefaultRetentionRule")
    def put_default_retention_rule(
        self,
        *,
        life_cycle: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param life_cycle: life_cycle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#life_cycle DataProtectionBackupPolicyKubernetesCluster#life_cycle}
        '''
        value = DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule(
            life_cycle=life_cycle
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultRetentionRule", [value]))

    @jsii.member(jsii_name="putRetentionRule")
    def put_retention_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProtectionBackupPolicyKubernetesClusterRetentionRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c718f171aa938da7ccfe86986bee542b91ccc1b29f5b45a1dd8df7db7e81a63b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRetentionRule", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#create DataProtectionBackupPolicyKubernetesCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#delete DataProtectionBackupPolicyKubernetesCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#read DataProtectionBackupPolicyKubernetesCluster#read}.
        '''
        value = DataProtectionBackupPolicyKubernetesClusterTimeouts(
            create=create, delete=delete, read=read
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRetentionRule")
    def reset_retention_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionRule", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

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
    @jsii.member(jsii_name="defaultRetentionRule")
    def default_retention_rule(
        self,
    ) -> "DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleOutputReference":
        return typing.cast("DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleOutputReference", jsii.get(self, "defaultRetentionRule"))

    @builtins.property
    @jsii.member(jsii_name="retentionRule")
    def retention_rule(
        self,
    ) -> "DataProtectionBackupPolicyKubernetesClusterRetentionRuleList":
        return typing.cast("DataProtectionBackupPolicyKubernetesClusterRetentionRuleList", jsii.get(self, "retentionRule"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "DataProtectionBackupPolicyKubernetesClusterTimeoutsOutputReference":
        return typing.cast("DataProtectionBackupPolicyKubernetesClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="backupRepeatingTimeIntervalsInput")
    def backup_repeating_time_intervals_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "backupRepeatingTimeIntervalsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRetentionRuleInput")
    def default_retention_rule_input(
        self,
    ) -> typing.Optional["DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule"]:
        return typing.cast(typing.Optional["DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule"], jsii.get(self, "defaultRetentionRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionRuleInput")
    def retention_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyKubernetesClusterRetentionRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyKubernetesClusterRetentionRule"]]], jsii.get(self, "retentionRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataProtectionBackupPolicyKubernetesClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataProtectionBackupPolicyKubernetesClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="vaultNameInput")
    def vault_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vaultNameInput"))

    @builtins.property
    @jsii.member(jsii_name="backupRepeatingTimeIntervals")
    def backup_repeating_time_intervals(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "backupRepeatingTimeIntervals"))

    @backup_repeating_time_intervals.setter
    def backup_repeating_time_intervals(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1b1b835e3540ab344c3da107be2462044c4263c8919b12599b7827a58189ec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupRepeatingTimeIntervals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01bca4b7d9ed763b11122dd0eca6db45d265f6ac280e0e812084ee66311c0058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb3bfbcabd69b56eb05528f6e5753568b42f9a47f7026371c4998bc21c4ff1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2681c84ec56dd580ca6b37cfbe3fdffe0cba7d8c4d6566648ea34d44580849f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b7b3e3fe0d5e21fb0f3ee5ef472f26f4e662659c942e47ad17094a7ca86bfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vaultName")
    def vault_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vaultName"))

    @vault_name.setter
    def vault_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e2320081fe81b7472d02935611dd526952586e90ee297917d5e9df97e29f140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vaultName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyKubernetesCluster.DataProtectionBackupPolicyKubernetesClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "backup_repeating_time_intervals": "backupRepeatingTimeIntervals",
        "default_retention_rule": "defaultRetentionRule",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "vault_name": "vaultName",
        "id": "id",
        "retention_rule": "retentionRule",
        "timeouts": "timeouts",
        "time_zone": "timeZone",
    },
)
class DataProtectionBackupPolicyKubernetesClusterConfig(
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
        backup_repeating_time_intervals: typing.Sequence[builtins.str],
        default_retention_rule: typing.Union["DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        resource_group_name: builtins.str,
        vault_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        retention_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProtectionBackupPolicyKubernetesClusterRetentionRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["DataProtectionBackupPolicyKubernetesClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param backup_repeating_time_intervals: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#backup_repeating_time_intervals DataProtectionBackupPolicyKubernetesCluster#backup_repeating_time_intervals}.
        :param default_retention_rule: default_retention_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#default_retention_rule DataProtectionBackupPolicyKubernetesCluster#default_retention_rule}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#name DataProtectionBackupPolicyKubernetesCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#resource_group_name DataProtectionBackupPolicyKubernetesCluster#resource_group_name}.
        :param vault_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#vault_name DataProtectionBackupPolicyKubernetesCluster#vault_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#id DataProtectionBackupPolicyKubernetesCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param retention_rule: retention_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#retention_rule DataProtectionBackupPolicyKubernetesCluster#retention_rule}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#timeouts DataProtectionBackupPolicyKubernetesCluster#timeouts}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#time_zone DataProtectionBackupPolicyKubernetesCluster#time_zone}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(default_retention_rule, dict):
            default_retention_rule = DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule(**default_retention_rule)
        if isinstance(timeouts, dict):
            timeouts = DataProtectionBackupPolicyKubernetesClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed04c5d75ed9496dcb745d85aed75e491b4c1c150c3b7b85e48b0f96089fa8a1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument backup_repeating_time_intervals", value=backup_repeating_time_intervals, expected_type=type_hints["backup_repeating_time_intervals"])
            check_type(argname="argument default_retention_rule", value=default_retention_rule, expected_type=type_hints["default_retention_rule"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument vault_name", value=vault_name, expected_type=type_hints["vault_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument retention_rule", value=retention_rule, expected_type=type_hints["retention_rule"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_repeating_time_intervals": backup_repeating_time_intervals,
            "default_retention_rule": default_retention_rule,
            "name": name,
            "resource_group_name": resource_group_name,
            "vault_name": vault_name,
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
        if retention_rule is not None:
            self._values["retention_rule"] = retention_rule
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if time_zone is not None:
            self._values["time_zone"] = time_zone

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
    def backup_repeating_time_intervals(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#backup_repeating_time_intervals DataProtectionBackupPolicyKubernetesCluster#backup_repeating_time_intervals}.'''
        result = self._values.get("backup_repeating_time_intervals")
        assert result is not None, "Required property 'backup_repeating_time_intervals' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def default_retention_rule(
        self,
    ) -> "DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule":
        '''default_retention_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#default_retention_rule DataProtectionBackupPolicyKubernetesCluster#default_retention_rule}
        '''
        result = self._values.get("default_retention_rule")
        assert result is not None, "Required property 'default_retention_rule' is missing"
        return typing.cast("DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#name DataProtectionBackupPolicyKubernetesCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#resource_group_name DataProtectionBackupPolicyKubernetesCluster#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vault_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#vault_name DataProtectionBackupPolicyKubernetesCluster#vault_name}.'''
        result = self._values.get("vault_name")
        assert result is not None, "Required property 'vault_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#id DataProtectionBackupPolicyKubernetesCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyKubernetesClusterRetentionRule"]]]:
        '''retention_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#retention_rule DataProtectionBackupPolicyKubernetesCluster#retention_rule}
        '''
        result = self._values.get("retention_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyKubernetesClusterRetentionRule"]]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["DataProtectionBackupPolicyKubernetesClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#timeouts DataProtectionBackupPolicyKubernetesCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataProtectionBackupPolicyKubernetesClusterTimeouts"], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#time_zone DataProtectionBackupPolicyKubernetesCluster#time_zone}.'''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyKubernetesClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyKubernetesCluster.DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule",
    jsii_struct_bases=[],
    name_mapping={"life_cycle": "lifeCycle"},
)
class DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule:
    def __init__(
        self,
        *,
        life_cycle: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param life_cycle: life_cycle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#life_cycle DataProtectionBackupPolicyKubernetesCluster#life_cycle}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0f9336405c912c24a5a0c50dc8e8d485cebf38ffdf25c06cacbfb057168821c)
            check_type(argname="argument life_cycle", value=life_cycle, expected_type=type_hints["life_cycle"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "life_cycle": life_cycle,
        }

    @builtins.property
    def life_cycle(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle"]]:
        '''life_cycle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#life_cycle DataProtectionBackupPolicyKubernetesCluster#life_cycle}
        '''
        result = self._values.get("life_cycle")
        assert result is not None, "Required property 'life_cycle' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyKubernetesCluster.DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle",
    jsii_struct_bases=[],
    name_mapping={"data_store_type": "dataStoreType", "duration": "duration"},
)
class DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle:
    def __init__(
        self,
        *,
        data_store_type: builtins.str,
        duration: builtins.str,
    ) -> None:
        '''
        :param data_store_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#data_store_type DataProtectionBackupPolicyKubernetesCluster#data_store_type}.
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#duration DataProtectionBackupPolicyKubernetesCluster#duration}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b10476143bfd8a130db36415e786e8f9109c0d35db9fa5bd353c316b6f338fd)
            check_type(argname="argument data_store_type", value=data_store_type, expected_type=type_hints["data_store_type"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_store_type": data_store_type,
            "duration": duration,
        }

    @builtins.property
    def data_store_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#data_store_type DataProtectionBackupPolicyKubernetesCluster#data_store_type}.'''
        result = self._values.get("data_store_type")
        assert result is not None, "Required property 'data_store_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def duration(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#duration DataProtectionBackupPolicyKubernetesCluster#duration}.'''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyKubernetesCluster.DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdd4f3437543c22a8af035710b27e4cb64e0a13f12be8dc948c8314eb39d3993)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a47c42ca1b5c8772a2fe6a92517b6d251a7e4aedfb4b119c5a30ae44397afd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea6b7bcd381e9fb7a6c7e7b46ae245c4483f5428dfec4f32bb6c1b1d23b80a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c4d562b3f2f5a598d63eed9fe34e7db555f6831fca8c83d4819cfa2c65eff5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe2ecb0e8a55d6bbc830f358e34dc686915f406a79b02fdb9df822ddd371dbfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2a39dd48f6bd5e0264c6c9ab555b668abdac7382ab8b22f67a56cf64f899de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyKubernetesCluster.DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50517f138e4356e6eba2f14f3d46f1e4449bd8b20a76cdfaf37611a4b4d70ac7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dataStoreTypeInput")
    def data_store_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataStoreTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStoreType")
    def data_store_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataStoreType"))

    @data_store_type.setter
    def data_store_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b919bdaa819112c4fb680b24a370b869d139df9e3e6260f38a9116e909f17a79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStoreType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25acca700655ebd0d16e6c82a750aa629cc182bd92eccf8defdcb2b0d7f95907)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__439ccbe3b475eaa717b13f894c9f7466a9ff950915d81cec16dafd350ea0f89e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyKubernetesCluster.DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c663ec2265bb335b4d8cf8a101b980b6ebc532cfa06cf482ac4882538ebbd72)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLifeCycle")
    def put_life_cycle(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241a83896ef97c117d5017a7a797da3297f541ac0f8bd9a47c40f35d3caba1fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLifeCycle", [value]))

    @builtins.property
    @jsii.member(jsii_name="lifeCycle")
    def life_cycle(
        self,
    ) -> DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycleList:
        return typing.cast(DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycleList, jsii.get(self, "lifeCycle"))

    @builtins.property
    @jsii.member(jsii_name="lifeCycleInput")
    def life_cycle_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle]]], jsii.get(self, "lifeCycleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule]:
        return typing.cast(typing.Optional[DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f53b866a5aa3a7ec757d5b696d5bfa3f7b0a1b1a33e3bd4ade3018e31d1deb5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyKubernetesCluster.DataProtectionBackupPolicyKubernetesClusterRetentionRule",
    jsii_struct_bases=[],
    name_mapping={
        "criteria": "criteria",
        "life_cycle": "lifeCycle",
        "name": "name",
        "priority": "priority",
    },
)
class DataProtectionBackupPolicyKubernetesClusterRetentionRule:
    def __init__(
        self,
        *,
        criteria: typing.Union["DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteria", typing.Dict[builtins.str, typing.Any]],
        life_cycle: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        priority: jsii.Number,
    ) -> None:
        '''
        :param criteria: criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#criteria DataProtectionBackupPolicyKubernetesCluster#criteria}
        :param life_cycle: life_cycle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#life_cycle DataProtectionBackupPolicyKubernetesCluster#life_cycle}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#name DataProtectionBackupPolicyKubernetesCluster#name}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#priority DataProtectionBackupPolicyKubernetesCluster#priority}.
        '''
        if isinstance(criteria, dict):
            criteria = DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteria(**criteria)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a89dffb340f24ff56991bc87dd77cf35d987e2b7a9e06645dee0aa961da8b897)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument life_cycle", value=life_cycle, expected_type=type_hints["life_cycle"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "life_cycle": life_cycle,
            "name": name,
            "priority": priority,
        }

    @builtins.property
    def criteria(
        self,
    ) -> "DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteria":
        '''criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#criteria DataProtectionBackupPolicyKubernetesCluster#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast("DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteria", result)

    @builtins.property
    def life_cycle(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle"]]:
        '''life_cycle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#life_cycle DataProtectionBackupPolicyKubernetesCluster#life_cycle}
        '''
        result = self._values.get("life_cycle")
        assert result is not None, "Required property 'life_cycle' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#name DataProtectionBackupPolicyKubernetesCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#priority DataProtectionBackupPolicyKubernetesCluster#priority}.'''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyKubernetesClusterRetentionRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyKubernetesCluster.DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteria",
    jsii_struct_bases=[],
    name_mapping={
        "absolute_criteria": "absoluteCriteria",
        "days_of_week": "daysOfWeek",
        "months_of_year": "monthsOfYear",
        "scheduled_backup_times": "scheduledBackupTimes",
        "weeks_of_month": "weeksOfMonth",
    },
)
class DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteria:
    def __init__(
        self,
        *,
        absolute_criteria: typing.Optional[builtins.str] = None,
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
        months_of_year: typing.Optional[typing.Sequence[builtins.str]] = None,
        scheduled_backup_times: typing.Optional[typing.Sequence[builtins.str]] = None,
        weeks_of_month: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param absolute_criteria: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#absolute_criteria DataProtectionBackupPolicyKubernetesCluster#absolute_criteria}.
        :param days_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#days_of_week DataProtectionBackupPolicyKubernetesCluster#days_of_week}.
        :param months_of_year: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#months_of_year DataProtectionBackupPolicyKubernetesCluster#months_of_year}.
        :param scheduled_backup_times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#scheduled_backup_times DataProtectionBackupPolicyKubernetesCluster#scheduled_backup_times}.
        :param weeks_of_month: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#weeks_of_month DataProtectionBackupPolicyKubernetesCluster#weeks_of_month}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b80e5283be4b37c625ee4f720b0c5b3b9d615418943ce4667cfdc5b739ef584a)
            check_type(argname="argument absolute_criteria", value=absolute_criteria, expected_type=type_hints["absolute_criteria"])
            check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
            check_type(argname="argument months_of_year", value=months_of_year, expected_type=type_hints["months_of_year"])
            check_type(argname="argument scheduled_backup_times", value=scheduled_backup_times, expected_type=type_hints["scheduled_backup_times"])
            check_type(argname="argument weeks_of_month", value=weeks_of_month, expected_type=type_hints["weeks_of_month"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if absolute_criteria is not None:
            self._values["absolute_criteria"] = absolute_criteria
        if days_of_week is not None:
            self._values["days_of_week"] = days_of_week
        if months_of_year is not None:
            self._values["months_of_year"] = months_of_year
        if scheduled_backup_times is not None:
            self._values["scheduled_backup_times"] = scheduled_backup_times
        if weeks_of_month is not None:
            self._values["weeks_of_month"] = weeks_of_month

    @builtins.property
    def absolute_criteria(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#absolute_criteria DataProtectionBackupPolicyKubernetesCluster#absolute_criteria}.'''
        result = self._values.get("absolute_criteria")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def days_of_week(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#days_of_week DataProtectionBackupPolicyKubernetesCluster#days_of_week}.'''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def months_of_year(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#months_of_year DataProtectionBackupPolicyKubernetesCluster#months_of_year}.'''
        result = self._values.get("months_of_year")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def scheduled_backup_times(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#scheduled_backup_times DataProtectionBackupPolicyKubernetesCluster#scheduled_backup_times}.'''
        result = self._values.get("scheduled_backup_times")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def weeks_of_month(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#weeks_of_month DataProtectionBackupPolicyKubernetesCluster#weeks_of_month}.'''
        result = self._values.get("weeks_of_month")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyKubernetesCluster.DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dc7e0d187b846a42544a2ea0dc8738017a23d026b8a45bee90a0856fed25646)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAbsoluteCriteria")
    def reset_absolute_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAbsoluteCriteria", []))

    @jsii.member(jsii_name="resetDaysOfWeek")
    def reset_days_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysOfWeek", []))

    @jsii.member(jsii_name="resetMonthsOfYear")
    def reset_months_of_year(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthsOfYear", []))

    @jsii.member(jsii_name="resetScheduledBackupTimes")
    def reset_scheduled_backup_times(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduledBackupTimes", []))

    @jsii.member(jsii_name="resetWeeksOfMonth")
    def reset_weeks_of_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeksOfMonth", []))

    @builtins.property
    @jsii.member(jsii_name="absoluteCriteriaInput")
    def absolute_criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "absoluteCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeekInput")
    def days_of_week_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "daysOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="monthsOfYearInput")
    def months_of_year_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "monthsOfYearInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledBackupTimesInput")
    def scheduled_backup_times_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scheduledBackupTimesInput"))

    @builtins.property
    @jsii.member(jsii_name="weeksOfMonthInput")
    def weeks_of_month_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "weeksOfMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="absoluteCriteria")
    def absolute_criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "absoluteCriteria"))

    @absolute_criteria.setter
    def absolute_criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52901134ba87d883d07fe766e5434f43a2e6b7625befc724d3e3776ae9090a02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "absoluteCriteria", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "daysOfWeek"))

    @days_of_week.setter
    def days_of_week(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889280224fd555fd3de3ccc54f4dff072038d72dcb329c373e836e26383f4395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monthsOfYear")
    def months_of_year(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "monthsOfYear"))

    @months_of_year.setter
    def months_of_year(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7debb91a2cfa2c4e771fb70e56eeef839f40814eac0e656822d89967e77929f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthsOfYear", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduledBackupTimes")
    def scheduled_backup_times(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scheduledBackupTimes"))

    @scheduled_backup_times.setter
    def scheduled_backup_times(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b5fe8885547d1397223dbb6ef4fdda9448b610eb6591b6b8b54c52f7252e723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduledBackupTimes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeksOfMonth")
    def weeks_of_month(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weeksOfMonth"))

    @weeks_of_month.setter
    def weeks_of_month(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecda183444b928e7c57105e5569caee911365a6f19928918a3ab0c810e6a7231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeksOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteria]:
        return typing.cast(typing.Optional[DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e9ceb06a0885997313982f82cc107eb8d00e90e6e75dc1ad3d016c940507d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyKubernetesCluster.DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle",
    jsii_struct_bases=[],
    name_mapping={"data_store_type": "dataStoreType", "duration": "duration"},
)
class DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle:
    def __init__(
        self,
        *,
        data_store_type: builtins.str,
        duration: builtins.str,
    ) -> None:
        '''
        :param data_store_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#data_store_type DataProtectionBackupPolicyKubernetesCluster#data_store_type}.
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#duration DataProtectionBackupPolicyKubernetesCluster#duration}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02eddd5121ee1b66916d98601a9bc5c7b9c5e840961c8f11a848afa0a92ff181)
            check_type(argname="argument data_store_type", value=data_store_type, expected_type=type_hints["data_store_type"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_store_type": data_store_type,
            "duration": duration,
        }

    @builtins.property
    def data_store_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#data_store_type DataProtectionBackupPolicyKubernetesCluster#data_store_type}.'''
        result = self._values.get("data_store_type")
        assert result is not None, "Required property 'data_store_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def duration(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#duration DataProtectionBackupPolicyKubernetesCluster#duration}.'''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyKubernetesCluster.DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6be83b8b7e76c653fbce4b29e79da9deb8eab5ff9835906b702f7e5c18cc2d38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7df109dcee80cd18090c4dff0c167ab7d485bd9684c5c5b07c3f45b98f2e3a96)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c507cb73b830ca7b60ca331261af8bcff9b563f56a9990253b9fc8384eaee1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e3c868c1e1e3b201021ffba9e8c416fbf9b5125b002df80164d4609f3fe733e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3cdd91c2f65907e49a87bf7fbbd7e8ddcf079bca3815f1a84732eda2926c64f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aac8424ffbb1d4b97796e741228f9c0366c26f075b115e7207263e7d24e9099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyKubernetesCluster.DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f62438d1c52992f28e22970817c19ddc824811becfc335960114ea3b7e4cf2cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dataStoreTypeInput")
    def data_store_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataStoreTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStoreType")
    def data_store_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataStoreType"))

    @data_store_type.setter
    def data_store_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc157ac3fdfddd1b7799978ae2dbb8fef659000af23d6b9c4d14dfae87f0de1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStoreType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff480c7ee2dad6cf44d0ebf14fc688b7f665798afcbd9a7b497cffd5d600c37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b8261304058e0cb8825aea3476d49fb641095b6df89d85b0e7ff3178aa4ae2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataProtectionBackupPolicyKubernetesClusterRetentionRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyKubernetesCluster.DataProtectionBackupPolicyKubernetesClusterRetentionRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68c249b18d71498cd704406ee93a8e7d734c8a193e52ae8e40310894e243c97d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataProtectionBackupPolicyKubernetesClusterRetentionRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12083cd9b475bb0bb63db502cf0ff555ac50af8386d0d34b809f881875329d63)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataProtectionBackupPolicyKubernetesClusterRetentionRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__962c3abd810adb920cbf0a03cd618551683478693eeba0d604e9eaea0ac3edef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d4afac594781895bb94d446302aafc8e06dd2e2443c6754ae88d546748e2ab0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e08c6ab11c768f2325e2953d326f68419d9028e33eb3c80c83e6408d7b2b31f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyKubernetesClusterRetentionRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyKubernetesClusterRetentionRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyKubernetesClusterRetentionRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03b8f44cc4aabcdf3a67bccf35c0b67d66bda3c18ad4f8ae8b3a7dd6e67c8e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataProtectionBackupPolicyKubernetesClusterRetentionRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyKubernetesCluster.DataProtectionBackupPolicyKubernetesClusterRetentionRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e0a2d8ca771d3fc4fc3553fa41f183de876987cebedb6f5ecffadeefd162825)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCriteria")
    def put_criteria(
        self,
        *,
        absolute_criteria: typing.Optional[builtins.str] = None,
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
        months_of_year: typing.Optional[typing.Sequence[builtins.str]] = None,
        scheduled_backup_times: typing.Optional[typing.Sequence[builtins.str]] = None,
        weeks_of_month: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param absolute_criteria: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#absolute_criteria DataProtectionBackupPolicyKubernetesCluster#absolute_criteria}.
        :param days_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#days_of_week DataProtectionBackupPolicyKubernetesCluster#days_of_week}.
        :param months_of_year: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#months_of_year DataProtectionBackupPolicyKubernetesCluster#months_of_year}.
        :param scheduled_backup_times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#scheduled_backup_times DataProtectionBackupPolicyKubernetesCluster#scheduled_backup_times}.
        :param weeks_of_month: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#weeks_of_month DataProtectionBackupPolicyKubernetesCluster#weeks_of_month}.
        '''
        value = DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteria(
            absolute_criteria=absolute_criteria,
            days_of_week=days_of_week,
            months_of_year=months_of_year,
            scheduled_backup_times=scheduled_backup_times,
            weeks_of_month=weeks_of_month,
        )

        return typing.cast(None, jsii.invoke(self, "putCriteria", [value]))

    @jsii.member(jsii_name="putLifeCycle")
    def put_life_cycle(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce459719eb2ce918ac3fdd58580d59a19d317ccb1058a16dd33d92bf72e7d8ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLifeCycle", [value]))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(
        self,
    ) -> DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteriaOutputReference:
        return typing.cast(DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteriaOutputReference, jsii.get(self, "criteria"))

    @builtins.property
    @jsii.member(jsii_name="lifeCycle")
    def life_cycle(
        self,
    ) -> DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycleList:
        return typing.cast(DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycleList, jsii.get(self, "lifeCycle"))

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(
        self,
    ) -> typing.Optional[DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteria]:
        return typing.cast(typing.Optional[DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteria], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="lifeCycleInput")
    def life_cycle_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle]]], jsii.get(self, "lifeCycleInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce58d70350bc542588ddf496c9edb55fdebdc6f621a8a5ada1edc0fd040c942d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c9e9216bff52aeab6eab3004bb8404104a65cd822825a1e280cd192a7d232ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyKubernetesClusterRetentionRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyKubernetesClusterRetentionRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyKubernetesClusterRetentionRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f69f63828718cb400dd0c2ef2a061e72ff50d48fcb47220e1907443321cf666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyKubernetesCluster.DataProtectionBackupPolicyKubernetesClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class DataProtectionBackupPolicyKubernetesClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#create DataProtectionBackupPolicyKubernetesCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#delete DataProtectionBackupPolicyKubernetesCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#read DataProtectionBackupPolicyKubernetesCluster#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67103ecb8c83d0533eb604d747a617ecd52d25f19a63a7a7f9e8ecc35fcd9fe)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#create DataProtectionBackupPolicyKubernetesCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#delete DataProtectionBackupPolicyKubernetesCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_kubernetes_cluster#read DataProtectionBackupPolicyKubernetesCluster#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyKubernetesClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProtectionBackupPolicyKubernetesClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyKubernetesCluster.DataProtectionBackupPolicyKubernetesClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0dbb152b66a94b87d9f7f69fe0a557089af5a53154c9035c5f115b9a0733861)
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
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d123f0692f4e1e9bda085b7b50869e762340f94709d54b82a6ba908b6a23ba15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78650e124328d6fd60a16d9cc3fa17cb83800c0be4c7f8da51fe63561dcc0b8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b17a5899736918853c10b3e7f97744f55b22740a04dd83d9ea19bc64c05f362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyKubernetesClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyKubernetesClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyKubernetesClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8989390977bcf227917ac8cfed59a55657950ca09548831a3e9a7fae8c4b7a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataProtectionBackupPolicyKubernetesCluster",
    "DataProtectionBackupPolicyKubernetesClusterConfig",
    "DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule",
    "DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle",
    "DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycleList",
    "DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycleOutputReference",
    "DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleOutputReference",
    "DataProtectionBackupPolicyKubernetesClusterRetentionRule",
    "DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteria",
    "DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteriaOutputReference",
    "DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle",
    "DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycleList",
    "DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycleOutputReference",
    "DataProtectionBackupPolicyKubernetesClusterRetentionRuleList",
    "DataProtectionBackupPolicyKubernetesClusterRetentionRuleOutputReference",
    "DataProtectionBackupPolicyKubernetesClusterTimeouts",
    "DataProtectionBackupPolicyKubernetesClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__22e07317ed4705141cfe42c0dbb98b748e70cdc1d5c1692dc589977689907d7a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    backup_repeating_time_intervals: typing.Sequence[builtins.str],
    default_retention_rule: typing.Union[DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    resource_group_name: builtins.str,
    vault_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    retention_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyKubernetesClusterRetentionRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[DataProtectionBackupPolicyKubernetesClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__ee07f5487f927e3d78dda13e03a2dabe639a2d28f82d6531a996850153bf13d8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c718f171aa938da7ccfe86986bee542b91ccc1b29f5b45a1dd8df7db7e81a63b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyKubernetesClusterRetentionRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b1b835e3540ab344c3da107be2462044c4263c8919b12599b7827a58189ec0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01bca4b7d9ed763b11122dd0eca6db45d265f6ac280e0e812084ee66311c0058(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb3bfbcabd69b56eb05528f6e5753568b42f9a47f7026371c4998bc21c4ff1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2681c84ec56dd580ca6b37cfbe3fdffe0cba7d8c4d6566648ea34d44580849f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b7b3e3fe0d5e21fb0f3ee5ef472f26f4e662659c942e47ad17094a7ca86bfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2320081fe81b7472d02935611dd526952586e90ee297917d5e9df97e29f140(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed04c5d75ed9496dcb745d85aed75e491b4c1c150c3b7b85e48b0f96089fa8a1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backup_repeating_time_intervals: typing.Sequence[builtins.str],
    default_retention_rule: typing.Union[DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    resource_group_name: builtins.str,
    vault_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    retention_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyKubernetesClusterRetentionRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[DataProtectionBackupPolicyKubernetesClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0f9336405c912c24a5a0c50dc8e8d485cebf38ffdf25c06cacbfb057168821c(
    *,
    life_cycle: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b10476143bfd8a130db36415e786e8f9109c0d35db9fa5bd353c316b6f338fd(
    *,
    data_store_type: builtins.str,
    duration: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd4f3437543c22a8af035710b27e4cb64e0a13f12be8dc948c8314eb39d3993(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a47c42ca1b5c8772a2fe6a92517b6d251a7e4aedfb4b119c5a30ae44397afd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea6b7bcd381e9fb7a6c7e7b46ae245c4483f5428dfec4f32bb6c1b1d23b80a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c4d562b3f2f5a598d63eed9fe34e7db555f6831fca8c83d4819cfa2c65eff5b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2ecb0e8a55d6bbc830f358e34dc686915f406a79b02fdb9df822ddd371dbfa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2a39dd48f6bd5e0264c6c9ab555b668abdac7382ab8b22f67a56cf64f899de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50517f138e4356e6eba2f14f3d46f1e4449bd8b20a76cdfaf37611a4b4d70ac7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b919bdaa819112c4fb680b24a370b869d139df9e3e6260f38a9116e909f17a79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25acca700655ebd0d16e6c82a750aa629cc182bd92eccf8defdcb2b0d7f95907(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439ccbe3b475eaa717b13f894c9f7466a9ff950915d81cec16dafd350ea0f89e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c663ec2265bb335b4d8cf8a101b980b6ebc532cfa06cf482ac4882538ebbd72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241a83896ef97c117d5017a7a797da3297f541ac0f8bd9a47c40f35d3caba1fe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRuleLifeCycle, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53b866a5aa3a7ec757d5b696d5bfa3f7b0a1b1a33e3bd4ade3018e31d1deb5e(
    value: typing.Optional[DataProtectionBackupPolicyKubernetesClusterDefaultRetentionRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89dffb340f24ff56991bc87dd77cf35d987e2b7a9e06645dee0aa961da8b897(
    *,
    criteria: typing.Union[DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteria, typing.Dict[builtins.str, typing.Any]],
    life_cycle: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    priority: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b80e5283be4b37c625ee4f720b0c5b3b9d615418943ce4667cfdc5b739ef584a(
    *,
    absolute_criteria: typing.Optional[builtins.str] = None,
    days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    months_of_year: typing.Optional[typing.Sequence[builtins.str]] = None,
    scheduled_backup_times: typing.Optional[typing.Sequence[builtins.str]] = None,
    weeks_of_month: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc7e0d187b846a42544a2ea0dc8738017a23d026b8a45bee90a0856fed25646(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52901134ba87d883d07fe766e5434f43a2e6b7625befc724d3e3776ae9090a02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889280224fd555fd3de3ccc54f4dff072038d72dcb329c373e836e26383f4395(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7debb91a2cfa2c4e771fb70e56eeef839f40814eac0e656822d89967e77929f6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b5fe8885547d1397223dbb6ef4fdda9448b610eb6591b6b8b54c52f7252e723(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecda183444b928e7c57105e5569caee911365a6f19928918a3ab0c810e6a7231(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e9ceb06a0885997313982f82cc107eb8d00e90e6e75dc1ad3d016c940507d5(
    value: typing.Optional[DataProtectionBackupPolicyKubernetesClusterRetentionRuleCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02eddd5121ee1b66916d98601a9bc5c7b9c5e840961c8f11a848afa0a92ff181(
    *,
    data_store_type: builtins.str,
    duration: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be83b8b7e76c653fbce4b29e79da9deb8eab5ff9835906b702f7e5c18cc2d38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df109dcee80cd18090c4dff0c167ab7d485bd9684c5c5b07c3f45b98f2e3a96(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c507cb73b830ca7b60ca331261af8bcff9b563f56a9990253b9fc8384eaee1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3c868c1e1e3b201021ffba9e8c416fbf9b5125b002df80164d4609f3fe733e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3cdd91c2f65907e49a87bf7fbbd7e8ddcf079bca3815f1a84732eda2926c64f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aac8424ffbb1d4b97796e741228f9c0366c26f075b115e7207263e7d24e9099(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62438d1c52992f28e22970817c19ddc824811becfc335960114ea3b7e4cf2cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc157ac3fdfddd1b7799978ae2dbb8fef659000af23d6b9c4d14dfae87f0de1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff480c7ee2dad6cf44d0ebf14fc688b7f665798afcbd9a7b497cffd5d600c37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8261304058e0cb8825aea3476d49fb641095b6df89d85b0e7ff3178aa4ae2c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c249b18d71498cd704406ee93a8e7d734c8a193e52ae8e40310894e243c97d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12083cd9b475bb0bb63db502cf0ff555ac50af8386d0d34b809f881875329d63(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__962c3abd810adb920cbf0a03cd618551683478693eeba0d604e9eaea0ac3edef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d4afac594781895bb94d446302aafc8e06dd2e2443c6754ae88d546748e2ab0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08c6ab11c768f2325e2953d326f68419d9028e33eb3c80c83e6408d7b2b31f5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03b8f44cc4aabcdf3a67bccf35c0b67d66bda3c18ad4f8ae8b3a7dd6e67c8e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyKubernetesClusterRetentionRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0a2d8ca771d3fc4fc3553fa41f183de876987cebedb6f5ecffadeefd162825(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce459719eb2ce918ac3fdd58580d59a19d317ccb1058a16dd33d92bf72e7d8ec(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyKubernetesClusterRetentionRuleLifeCycle, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce58d70350bc542588ddf496c9edb55fdebdc6f621a8a5ada1edc0fd040c942d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9e9216bff52aeab6eab3004bb8404104a65cd822825a1e280cd192a7d232ca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f69f63828718cb400dd0c2ef2a061e72ff50d48fcb47220e1907443321cf666(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyKubernetesClusterRetentionRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67103ecb8c83d0533eb604d747a617ecd52d25f19a63a7a7f9e8ecc35fcd9fe(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0dbb152b66a94b87d9f7f69fe0a557089af5a53154c9035c5f115b9a0733861(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d123f0692f4e1e9bda085b7b50869e762340f94709d54b82a6ba908b6a23ba15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78650e124328d6fd60a16d9cc3fa17cb83800c0be4c7f8da51fe63561dcc0b8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b17a5899736918853c10b3e7f97744f55b22740a04dd83d9ea19bc64c05f362(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8989390977bcf227917ac8cfed59a55657950ca09548831a3e9a7fae8c4b7a33(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyKubernetesClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
