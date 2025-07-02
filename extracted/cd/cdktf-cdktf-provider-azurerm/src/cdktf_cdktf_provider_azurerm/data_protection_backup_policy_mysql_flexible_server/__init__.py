r'''
# `azurerm_data_protection_backup_policy_mysql_flexible_server`

Refer to the Terraform Registry for docs: [`azurerm_data_protection_backup_policy_mysql_flexible_server`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server).
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


class DataProtectionBackupPolicyMysqlFlexibleServer(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyMysqlFlexibleServer.DataProtectionBackupPolicyMysqlFlexibleServer",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server azurerm_data_protection_backup_policy_mysql_flexible_server}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        backup_repeating_time_intervals: typing.Sequence[builtins.str],
        default_retention_rule: typing.Union["DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        vault_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        retention_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["DataProtectionBackupPolicyMysqlFlexibleServerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server azurerm_data_protection_backup_policy_mysql_flexible_server} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param backup_repeating_time_intervals: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#backup_repeating_time_intervals DataProtectionBackupPolicyMysqlFlexibleServer#backup_repeating_time_intervals}.
        :param default_retention_rule: default_retention_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#default_retention_rule DataProtectionBackupPolicyMysqlFlexibleServer#default_retention_rule}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#name DataProtectionBackupPolicyMysqlFlexibleServer#name}.
        :param vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#vault_id DataProtectionBackupPolicyMysqlFlexibleServer#vault_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#id DataProtectionBackupPolicyMysqlFlexibleServer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param retention_rule: retention_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#retention_rule DataProtectionBackupPolicyMysqlFlexibleServer#retention_rule}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#timeouts DataProtectionBackupPolicyMysqlFlexibleServer#timeouts}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#time_zone DataProtectionBackupPolicyMysqlFlexibleServer#time_zone}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faae2e3aa6514ddaca21ad3a7696d0c4cc16ca2ac6d9dc714f83ed16c5fe7edf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataProtectionBackupPolicyMysqlFlexibleServerConfig(
            backup_repeating_time_intervals=backup_repeating_time_intervals,
            default_retention_rule=default_retention_rule,
            name=name,
            vault_id=vault_id,
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
        '''Generates CDKTF code for importing a DataProtectionBackupPolicyMysqlFlexibleServer resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataProtectionBackupPolicyMysqlFlexibleServer to import.
        :param import_from_id: The id of the existing DataProtectionBackupPolicyMysqlFlexibleServer that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataProtectionBackupPolicyMysqlFlexibleServer to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c802c9d7873897d404d7195dd0b18ddaa154308fa2c822d9697840e5c42221cd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDefaultRetentionRule")
    def put_default_retention_rule(
        self,
        *,
        life_cycle: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param life_cycle: life_cycle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#life_cycle DataProtectionBackupPolicyMysqlFlexibleServer#life_cycle}
        '''
        value = DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule(
            life_cycle=life_cycle
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultRetentionRule", [value]))

    @jsii.member(jsii_name="putRetentionRule")
    def put_retention_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__933b54e12f6a5900fa1a67af593f8ae7d64c2efdf10257d171c7910019f1cb17)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#create DataProtectionBackupPolicyMysqlFlexibleServer#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#delete DataProtectionBackupPolicyMysqlFlexibleServer#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#read DataProtectionBackupPolicyMysqlFlexibleServer#read}.
        '''
        value = DataProtectionBackupPolicyMysqlFlexibleServerTimeouts(
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
    ) -> "DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleOutputReference":
        return typing.cast("DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleOutputReference", jsii.get(self, "defaultRetentionRule"))

    @builtins.property
    @jsii.member(jsii_name="retentionRule")
    def retention_rule(
        self,
    ) -> "DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleList":
        return typing.cast("DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleList", jsii.get(self, "retentionRule"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "DataProtectionBackupPolicyMysqlFlexibleServerTimeoutsOutputReference":
        return typing.cast("DataProtectionBackupPolicyMysqlFlexibleServerTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule"]:
        return typing.cast(typing.Optional["DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule"], jsii.get(self, "defaultRetentionRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionRuleInput")
    def retention_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule"]]], jsii.get(self, "retentionRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataProtectionBackupPolicyMysqlFlexibleServerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataProtectionBackupPolicyMysqlFlexibleServerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="vaultIdInput")
    def vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="backupRepeatingTimeIntervals")
    def backup_repeating_time_intervals(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "backupRepeatingTimeIntervals"))

    @backup_repeating_time_intervals.setter
    def backup_repeating_time_intervals(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d581b0b9639335e956a7f632314ee3faf231b2d1bafa97a1b039aece0aea5d62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupRepeatingTimeIntervals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c8bc2e956771f698e144c66b2bcd936e277bb0efcb0836596c8e390bb44c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cff30d5164bd6aed1e6ce3c9080d4db6dc206fc9efa2577610670c58c6733ab6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__035da6542e8b37c8f28b37a9064bee40a26980de6e50c30bc958d8357198744e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vaultId")
    def vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vaultId"))

    @vault_id.setter
    def vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b225271281a2e4a41fdd71f6eaf4fd604279c2fbdde4d593e7b5ac4b29a5dfd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vaultId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyMysqlFlexibleServer.DataProtectionBackupPolicyMysqlFlexibleServerConfig",
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
        "vault_id": "vaultId",
        "id": "id",
        "retention_rule": "retentionRule",
        "timeouts": "timeouts",
        "time_zone": "timeZone",
    },
)
class DataProtectionBackupPolicyMysqlFlexibleServerConfig(
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
        default_retention_rule: typing.Union["DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        vault_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        retention_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["DataProtectionBackupPolicyMysqlFlexibleServerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param backup_repeating_time_intervals: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#backup_repeating_time_intervals DataProtectionBackupPolicyMysqlFlexibleServer#backup_repeating_time_intervals}.
        :param default_retention_rule: default_retention_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#default_retention_rule DataProtectionBackupPolicyMysqlFlexibleServer#default_retention_rule}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#name DataProtectionBackupPolicyMysqlFlexibleServer#name}.
        :param vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#vault_id DataProtectionBackupPolicyMysqlFlexibleServer#vault_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#id DataProtectionBackupPolicyMysqlFlexibleServer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param retention_rule: retention_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#retention_rule DataProtectionBackupPolicyMysqlFlexibleServer#retention_rule}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#timeouts DataProtectionBackupPolicyMysqlFlexibleServer#timeouts}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#time_zone DataProtectionBackupPolicyMysqlFlexibleServer#time_zone}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(default_retention_rule, dict):
            default_retention_rule = DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule(**default_retention_rule)
        if isinstance(timeouts, dict):
            timeouts = DataProtectionBackupPolicyMysqlFlexibleServerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca6d4fba2a0dd7bf0997b65b4aabc4025a4dabaab8578a25a7e6a7ac07dd483a)
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
            check_type(argname="argument vault_id", value=vault_id, expected_type=type_hints["vault_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument retention_rule", value=retention_rule, expected_type=type_hints["retention_rule"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_repeating_time_intervals": backup_repeating_time_intervals,
            "default_retention_rule": default_retention_rule,
            "name": name,
            "vault_id": vault_id,
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#backup_repeating_time_intervals DataProtectionBackupPolicyMysqlFlexibleServer#backup_repeating_time_intervals}.'''
        result = self._values.get("backup_repeating_time_intervals")
        assert result is not None, "Required property 'backup_repeating_time_intervals' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def default_retention_rule(
        self,
    ) -> "DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule":
        '''default_retention_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#default_retention_rule DataProtectionBackupPolicyMysqlFlexibleServer#default_retention_rule}
        '''
        result = self._values.get("default_retention_rule")
        assert result is not None, "Required property 'default_retention_rule' is missing"
        return typing.cast("DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#name DataProtectionBackupPolicyMysqlFlexibleServer#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vault_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#vault_id DataProtectionBackupPolicyMysqlFlexibleServer#vault_id}.'''
        result = self._values.get("vault_id")
        assert result is not None, "Required property 'vault_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#id DataProtectionBackupPolicyMysqlFlexibleServer#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule"]]]:
        '''retention_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#retention_rule DataProtectionBackupPolicyMysqlFlexibleServer#retention_rule}
        '''
        result = self._values.get("retention_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule"]]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["DataProtectionBackupPolicyMysqlFlexibleServerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#timeouts DataProtectionBackupPolicyMysqlFlexibleServer#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataProtectionBackupPolicyMysqlFlexibleServerTimeouts"], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#time_zone DataProtectionBackupPolicyMysqlFlexibleServer#time_zone}.'''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyMysqlFlexibleServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyMysqlFlexibleServer.DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule",
    jsii_struct_bases=[],
    name_mapping={"life_cycle": "lifeCycle"},
)
class DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule:
    def __init__(
        self,
        *,
        life_cycle: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param life_cycle: life_cycle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#life_cycle DataProtectionBackupPolicyMysqlFlexibleServer#life_cycle}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec7de939c1be30915ecc9627f7bf69ff087993f3716924fd7361bde8bb03054)
            check_type(argname="argument life_cycle", value=life_cycle, expected_type=type_hints["life_cycle"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "life_cycle": life_cycle,
        }

    @builtins.property
    def life_cycle(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle"]]:
        '''life_cycle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#life_cycle DataProtectionBackupPolicyMysqlFlexibleServer#life_cycle}
        '''
        result = self._values.get("life_cycle")
        assert result is not None, "Required property 'life_cycle' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyMysqlFlexibleServer.DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle",
    jsii_struct_bases=[],
    name_mapping={"data_store_type": "dataStoreType", "duration": "duration"},
)
class DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle:
    def __init__(
        self,
        *,
        data_store_type: builtins.str,
        duration: builtins.str,
    ) -> None:
        '''
        :param data_store_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#data_store_type DataProtectionBackupPolicyMysqlFlexibleServer#data_store_type}.
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#duration DataProtectionBackupPolicyMysqlFlexibleServer#duration}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7780516f1f23521a4c76c80b243c4c03a15299256f2ae439b5aab946fdc38d5a)
            check_type(argname="argument data_store_type", value=data_store_type, expected_type=type_hints["data_store_type"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_store_type": data_store_type,
            "duration": duration,
        }

    @builtins.property
    def data_store_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#data_store_type DataProtectionBackupPolicyMysqlFlexibleServer#data_store_type}.'''
        result = self._values.get("data_store_type")
        assert result is not None, "Required property 'data_store_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def duration(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#duration DataProtectionBackupPolicyMysqlFlexibleServer#duration}.'''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyMysqlFlexibleServer.DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3477dd6506f0e406f1edb0d7bfe2c73574bb7ab686c0b686daad58bc9a3ee720)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb2740bef1ee3c710422a2560dfb521ff0ca567b73dd6026a6f78de19d0c4c2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5989ccbdbac2f05b81f36c96a77a4dacdee858ae68e49e5cd883d090dfdedded)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07937da988619893a3ec9e356f9195415c0e8cf2df27dafe9d779c90821c0810)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4adfd3e30bf158d2ea1bc83195db6556e1bc10f421125b1889beb3da86c32b63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d06f06433986242315735d7e716a7200cbeb572ded1962af45f73d423c103a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyMysqlFlexibleServer.DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__028c9a5e831f92adc708a5c41f273e0c62c22746b9960fbd2c8618bf24ca3721)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c2fd2cde437d5047d58e75083feb331918405f62ff198123fc1bec7651bbf03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStoreType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f168661e67250a648398ccf533900d5a3996d75deb96549cff9c8523e10b98ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21aeef9ddd3a070ec12824ae39b69d240170640823a58b126a30775327249af1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyMysqlFlexibleServer.DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34f226d16874a59533a4a58d80f3008f6978c56ee4eb27ffb3cd0ce73583540b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLifeCycle")
    def put_life_cycle(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92928e092a6bc7e3896de25480dc2a8b255988f5cd54028c3959b8d7dc27c414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLifeCycle", [value]))

    @builtins.property
    @jsii.member(jsii_name="lifeCycle")
    def life_cycle(
        self,
    ) -> DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycleList:
        return typing.cast(DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycleList, jsii.get(self, "lifeCycle"))

    @builtins.property
    @jsii.member(jsii_name="lifeCycleInput")
    def life_cycle_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle]]], jsii.get(self, "lifeCycleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule]:
        return typing.cast(typing.Optional[DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e48478ea4d45d7f5c702a621618cc63d09d331bd5b853720db7d411a18613ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyMysqlFlexibleServer.DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule",
    jsii_struct_bases=[],
    name_mapping={
        "criteria": "criteria",
        "life_cycle": "lifeCycle",
        "name": "name",
        "priority": "priority",
    },
)
class DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule:
    def __init__(
        self,
        *,
        criteria: typing.Union["DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteria", typing.Dict[builtins.str, typing.Any]],
        life_cycle: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        priority: jsii.Number,
    ) -> None:
        '''
        :param criteria: criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#criteria DataProtectionBackupPolicyMysqlFlexibleServer#criteria}
        :param life_cycle: life_cycle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#life_cycle DataProtectionBackupPolicyMysqlFlexibleServer#life_cycle}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#name DataProtectionBackupPolicyMysqlFlexibleServer#name}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#priority DataProtectionBackupPolicyMysqlFlexibleServer#priority}.
        '''
        if isinstance(criteria, dict):
            criteria = DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteria(**criteria)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d51c2d78ceeb61b15bf9d734025fecc27f3d6f1083429f6b391bcb3a48781ff)
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
    ) -> "DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteria":
        '''criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#criteria DataProtectionBackupPolicyMysqlFlexibleServer#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast("DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteria", result)

    @builtins.property
    def life_cycle(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle"]]:
        '''life_cycle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#life_cycle DataProtectionBackupPolicyMysqlFlexibleServer#life_cycle}
        '''
        result = self._values.get("life_cycle")
        assert result is not None, "Required property 'life_cycle' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#name DataProtectionBackupPolicyMysqlFlexibleServer#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#priority DataProtectionBackupPolicyMysqlFlexibleServer#priority}.'''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyMysqlFlexibleServer.DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteria",
    jsii_struct_bases=[],
    name_mapping={
        "absolute_criteria": "absoluteCriteria",
        "days_of_week": "daysOfWeek",
        "months_of_year": "monthsOfYear",
        "scheduled_backup_times": "scheduledBackupTimes",
        "weeks_of_month": "weeksOfMonth",
    },
)
class DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteria:
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
        :param absolute_criteria: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#absolute_criteria DataProtectionBackupPolicyMysqlFlexibleServer#absolute_criteria}.
        :param days_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#days_of_week DataProtectionBackupPolicyMysqlFlexibleServer#days_of_week}.
        :param months_of_year: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#months_of_year DataProtectionBackupPolicyMysqlFlexibleServer#months_of_year}.
        :param scheduled_backup_times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#scheduled_backup_times DataProtectionBackupPolicyMysqlFlexibleServer#scheduled_backup_times}.
        :param weeks_of_month: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#weeks_of_month DataProtectionBackupPolicyMysqlFlexibleServer#weeks_of_month}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dfca4387262a29d4883627ba371451121d6e16554c594af9d7cb9de81635c48)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#absolute_criteria DataProtectionBackupPolicyMysqlFlexibleServer#absolute_criteria}.'''
        result = self._values.get("absolute_criteria")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def days_of_week(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#days_of_week DataProtectionBackupPolicyMysqlFlexibleServer#days_of_week}.'''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def months_of_year(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#months_of_year DataProtectionBackupPolicyMysqlFlexibleServer#months_of_year}.'''
        result = self._values.get("months_of_year")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def scheduled_backup_times(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#scheduled_backup_times DataProtectionBackupPolicyMysqlFlexibleServer#scheduled_backup_times}.'''
        result = self._values.get("scheduled_backup_times")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def weeks_of_month(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#weeks_of_month DataProtectionBackupPolicyMysqlFlexibleServer#weeks_of_month}.'''
        result = self._values.get("weeks_of_month")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyMysqlFlexibleServer.DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9609c46fcca138e585122ee54dd45add725ddea8e99907bc58c1500a2aec582b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5525fce1ecd2e6979fdcb14f3e2397fc5fa2a6f8a93734e75927a1367e0048ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "absoluteCriteria", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "daysOfWeek"))

    @days_of_week.setter
    def days_of_week(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eda687776bcb1671343cacde66926947a5265a5d54b371794a0125743a56aae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monthsOfYear")
    def months_of_year(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "monthsOfYear"))

    @months_of_year.setter
    def months_of_year(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc4d17df219c0a29b8651b638432618c9fa10e3274343333278234eb4cefccd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthsOfYear", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduledBackupTimes")
    def scheduled_backup_times(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scheduledBackupTimes"))

    @scheduled_backup_times.setter
    def scheduled_backup_times(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e85522fc95b5945e49fe8b54a1b6349cbc44af245cd6e1769efa510cc84c25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduledBackupTimes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeksOfMonth")
    def weeks_of_month(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weeksOfMonth"))

    @weeks_of_month.setter
    def weeks_of_month(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5e8ce1b106e1e37eb9e19ad729724970c4b4aebc485bfb7684bf72ab8091650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeksOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteria]:
        return typing.cast(typing.Optional[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__601a9a6d5e4c63d5bbbd06425bc537ab8510cc7c71566a4a48d88844e7f97d9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyMysqlFlexibleServer.DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle",
    jsii_struct_bases=[],
    name_mapping={"data_store_type": "dataStoreType", "duration": "duration"},
)
class DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle:
    def __init__(
        self,
        *,
        data_store_type: builtins.str,
        duration: builtins.str,
    ) -> None:
        '''
        :param data_store_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#data_store_type DataProtectionBackupPolicyMysqlFlexibleServer#data_store_type}.
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#duration DataProtectionBackupPolicyMysqlFlexibleServer#duration}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f33ad288456f43930510808646d54dff89fc82dfe4f3cd716309b78ccddee0)
            check_type(argname="argument data_store_type", value=data_store_type, expected_type=type_hints["data_store_type"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_store_type": data_store_type,
            "duration": duration,
        }

    @builtins.property
    def data_store_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#data_store_type DataProtectionBackupPolicyMysqlFlexibleServer#data_store_type}.'''
        result = self._values.get("data_store_type")
        assert result is not None, "Required property 'data_store_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def duration(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#duration DataProtectionBackupPolicyMysqlFlexibleServer#duration}.'''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyMysqlFlexibleServer.DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7dcbc5101790b39db838ab602cc809886e4ddb81de0f573b5bc2436889a2ba4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c26fad08ca1d0d4b6b4414887decc194fc90d3be536fddb4f310e2d461ba20e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334e39bd704bd69e105e77a5475e62f89d1d14ce6b7151a362434b3b52aac644)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d586a796e4d204446f11badd29682a16636486dc4491134aad5cd166de6c75b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b4ad2da0ff9b1fa5a6b5970d48fd67e76ee55e3975bd7d6414f6095f07c8742)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e1b9f20d690c715d56d98fbffcac353f6c4eed4a4f797a308af0cc0ad8813e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyMysqlFlexibleServer.DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85e99810a9d3e1fd4595fd22db6b5006d6f7c5323bf362bbab05db9c240f76d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18fb981aa0cc95e52bf703e2311eabd356e0351a8b46432409b0c396d682e95d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStoreType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b7021622929db171f0232de8357a30e5ec6a8caeb1301c7ec92a7f61c7bc56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ca9b9876b84516b30f3dc6950953d75951e0bd64555e22aac4df75e032ed4df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyMysqlFlexibleServer.DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a05393944d8c16c0a844b93d1184738f34e79def57d063a9c2145958a9a77523)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c290a183203cbad1b6a8462fd9ae32ff318932aa6efcdada1869690f5cb69a9c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d0a9e04b2929ee41cb3589144ecd17426d7bdfcf56a7af3a1cbd68a9fb6d2b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b7265a5b1d02a85efd5378022835af40f4ef4b7430cbf7193a3bf1d485f68ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f445948e67e20e6e0e8ae24f087cc7d65f43fab0d6a7af403434135c07548a4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a7561840294c661f99f5037bec2ed4ceff96ae933307e6f8d6c4a1ba50b54f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyMysqlFlexibleServer.DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8407eefc67f562b8b0bbc99b066952f1773b84765040067885e1bdbb58011c6a)
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
        :param absolute_criteria: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#absolute_criteria DataProtectionBackupPolicyMysqlFlexibleServer#absolute_criteria}.
        :param days_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#days_of_week DataProtectionBackupPolicyMysqlFlexibleServer#days_of_week}.
        :param months_of_year: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#months_of_year DataProtectionBackupPolicyMysqlFlexibleServer#months_of_year}.
        :param scheduled_backup_times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#scheduled_backup_times DataProtectionBackupPolicyMysqlFlexibleServer#scheduled_backup_times}.
        :param weeks_of_month: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#weeks_of_month DataProtectionBackupPolicyMysqlFlexibleServer#weeks_of_month}.
        '''
        value = DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteria(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e848bdefb6b64a9abab0b358efb2014647cca1e4d2d09dc7631460f4aeb1d251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLifeCycle", [value]))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(
        self,
    ) -> DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteriaOutputReference:
        return typing.cast(DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteriaOutputReference, jsii.get(self, "criteria"))

    @builtins.property
    @jsii.member(jsii_name="lifeCycle")
    def life_cycle(
        self,
    ) -> DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycleList:
        return typing.cast(DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycleList, jsii.get(self, "lifeCycle"))

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(
        self,
    ) -> typing.Optional[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteria]:
        return typing.cast(typing.Optional[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteria], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="lifeCycleInput")
    def life_cycle_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle]]], jsii.get(self, "lifeCycleInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__67810286ac96cdbfe5697c52d04abcbed6b7d8c1fbd47ab3da98c5442fe5f1fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__682937e9c19e19d168cca95c9bf0cce7d8887d216359fc64b95288bcaa7c12b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b109bc1c6280cec9187ab7942029c6c2f808f2431ec726f53e4c23ed54cd8917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyMysqlFlexibleServer.DataProtectionBackupPolicyMysqlFlexibleServerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class DataProtectionBackupPolicyMysqlFlexibleServerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#create DataProtectionBackupPolicyMysqlFlexibleServer#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#delete DataProtectionBackupPolicyMysqlFlexibleServer#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#read DataProtectionBackupPolicyMysqlFlexibleServer#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a6e6428eaa0c311c34eeefa233741150b4dc72bd57a135cd5f7c2b08e8cfbb)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#create DataProtectionBackupPolicyMysqlFlexibleServer#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#delete DataProtectionBackupPolicyMysqlFlexibleServer#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_mysql_flexible_server#read DataProtectionBackupPolicyMysqlFlexibleServer#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyMysqlFlexibleServerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProtectionBackupPolicyMysqlFlexibleServerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyMysqlFlexibleServer.DataProtectionBackupPolicyMysqlFlexibleServerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72b3fad46677a099d8b1296c5f10d856043d2a66bd89e2a146baea65673710af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca317f63dd9e2f4a822d8dab2d68d02102b3a127ccb99bffa9507e9741687e1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66e6ac7e5d9099efd0d11c688f1dec8361a735da6ebf015540db507ea751689d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8217d373a9732416d350bdddbddcdc0fe764256f010b49453f4297964e50784a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyMysqlFlexibleServerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyMysqlFlexibleServerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyMysqlFlexibleServerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe8749fb8bac39ca89ac6ce6d3d74b34ff0e4aac30e341e4e139f4a56f7f030d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataProtectionBackupPolicyMysqlFlexibleServer",
    "DataProtectionBackupPolicyMysqlFlexibleServerConfig",
    "DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule",
    "DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle",
    "DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycleList",
    "DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycleOutputReference",
    "DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleOutputReference",
    "DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule",
    "DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteria",
    "DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteriaOutputReference",
    "DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle",
    "DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycleList",
    "DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycleOutputReference",
    "DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleList",
    "DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleOutputReference",
    "DataProtectionBackupPolicyMysqlFlexibleServerTimeouts",
    "DataProtectionBackupPolicyMysqlFlexibleServerTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__faae2e3aa6514ddaca21ad3a7696d0c4cc16ca2ac6d9dc714f83ed16c5fe7edf(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    backup_repeating_time_intervals: typing.Sequence[builtins.str],
    default_retention_rule: typing.Union[DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    vault_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    retention_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[DataProtectionBackupPolicyMysqlFlexibleServerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c802c9d7873897d404d7195dd0b18ddaa154308fa2c822d9697840e5c42221cd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933b54e12f6a5900fa1a67af593f8ae7d64c2efdf10257d171c7910019f1cb17(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d581b0b9639335e956a7f632314ee3faf231b2d1bafa97a1b039aece0aea5d62(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c8bc2e956771f698e144c66b2bcd936e277bb0efcb0836596c8e390bb44c3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff30d5164bd6aed1e6ce3c9080d4db6dc206fc9efa2577610670c58c6733ab6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035da6542e8b37c8f28b37a9064bee40a26980de6e50c30bc958d8357198744e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b225271281a2e4a41fdd71f6eaf4fd604279c2fbdde4d593e7b5ac4b29a5dfd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca6d4fba2a0dd7bf0997b65b4aabc4025a4dabaab8578a25a7e6a7ac07dd483a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backup_repeating_time_intervals: typing.Sequence[builtins.str],
    default_retention_rule: typing.Union[DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    vault_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    retention_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[DataProtectionBackupPolicyMysqlFlexibleServerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec7de939c1be30915ecc9627f7bf69ff087993f3716924fd7361bde8bb03054(
    *,
    life_cycle: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7780516f1f23521a4c76c80b243c4c03a15299256f2ae439b5aab946fdc38d5a(
    *,
    data_store_type: builtins.str,
    duration: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3477dd6506f0e406f1edb0d7bfe2c73574bb7ab686c0b686daad58bc9a3ee720(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb2740bef1ee3c710422a2560dfb521ff0ca567b73dd6026a6f78de19d0c4c2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5989ccbdbac2f05b81f36c96a77a4dacdee858ae68e49e5cd883d090dfdedded(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07937da988619893a3ec9e356f9195415c0e8cf2df27dafe9d779c90821c0810(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4adfd3e30bf158d2ea1bc83195db6556e1bc10f421125b1889beb3da86c32b63(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d06f06433986242315735d7e716a7200cbeb572ded1962af45f73d423c103a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028c9a5e831f92adc708a5c41f273e0c62c22746b9960fbd2c8618bf24ca3721(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c2fd2cde437d5047d58e75083feb331918405f62ff198123fc1bec7651bbf03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f168661e67250a648398ccf533900d5a3996d75deb96549cff9c8523e10b98ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21aeef9ddd3a070ec12824ae39b69d240170640823a58b126a30775327249af1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f226d16874a59533a4a58d80f3008f6978c56ee4eb27ffb3cd0ce73583540b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92928e092a6bc7e3896de25480dc2a8b255988f5cd54028c3959b8d7dc27c414(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRuleLifeCycle, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e48478ea4d45d7f5c702a621618cc63d09d331bd5b853720db7d411a18613ac(
    value: typing.Optional[DataProtectionBackupPolicyMysqlFlexibleServerDefaultRetentionRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d51c2d78ceeb61b15bf9d734025fecc27f3d6f1083429f6b391bcb3a48781ff(
    *,
    criteria: typing.Union[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteria, typing.Dict[builtins.str, typing.Any]],
    life_cycle: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    priority: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dfca4387262a29d4883627ba371451121d6e16554c594af9d7cb9de81635c48(
    *,
    absolute_criteria: typing.Optional[builtins.str] = None,
    days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    months_of_year: typing.Optional[typing.Sequence[builtins.str]] = None,
    scheduled_backup_times: typing.Optional[typing.Sequence[builtins.str]] = None,
    weeks_of_month: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9609c46fcca138e585122ee54dd45add725ddea8e99907bc58c1500a2aec582b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5525fce1ecd2e6979fdcb14f3e2397fc5fa2a6f8a93734e75927a1367e0048ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda687776bcb1671343cacde66926947a5265a5d54b371794a0125743a56aae6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc4d17df219c0a29b8651b638432618c9fa10e3274343333278234eb4cefccd1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e85522fc95b5945e49fe8b54a1b6349cbc44af245cd6e1769efa510cc84c25(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e8ce1b106e1e37eb9e19ad729724970c4b4aebc485bfb7684bf72ab8091650(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__601a9a6d5e4c63d5bbbd06425bc537ab8510cc7c71566a4a48d88844e7f97d9f(
    value: typing.Optional[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f33ad288456f43930510808646d54dff89fc82dfe4f3cd716309b78ccddee0(
    *,
    data_store_type: builtins.str,
    duration: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7dcbc5101790b39db838ab602cc809886e4ddb81de0f573b5bc2436889a2ba4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c26fad08ca1d0d4b6b4414887decc194fc90d3be536fddb4f310e2d461ba20e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334e39bd704bd69e105e77a5475e62f89d1d14ce6b7151a362434b3b52aac644(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d586a796e4d204446f11badd29682a16636486dc4491134aad5cd166de6c75b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b4ad2da0ff9b1fa5a6b5970d48fd67e76ee55e3975bd7d6414f6095f07c8742(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1b9f20d690c715d56d98fbffcac353f6c4eed4a4f797a308af0cc0ad8813e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e99810a9d3e1fd4595fd22db6b5006d6f7c5323bf362bbab05db9c240f76d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18fb981aa0cc95e52bf703e2311eabd356e0351a8b46432409b0c396d682e95d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b7021622929db171f0232de8357a30e5ec6a8caeb1301c7ec92a7f61c7bc56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca9b9876b84516b30f3dc6950953d75951e0bd64555e22aac4df75e032ed4df(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a05393944d8c16c0a844b93d1184738f34e79def57d063a9c2145958a9a77523(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c290a183203cbad1b6a8462fd9ae32ff318932aa6efcdada1869690f5cb69a9c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0a9e04b2929ee41cb3589144ecd17426d7bdfcf56a7af3a1cbd68a9fb6d2b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b7265a5b1d02a85efd5378022835af40f4ef4b7430cbf7193a3bf1d485f68ba(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f445948e67e20e6e0e8ae24f087cc7d65f43fab0d6a7af403434135c07548a4c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a7561840294c661f99f5037bec2ed4ceff96ae933307e6f8d6c4a1ba50b54f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8407eefc67f562b8b0bbc99b066952f1773b84765040067885e1bdbb58011c6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e848bdefb6b64a9abab0b358efb2014647cca1e4d2d09dc7631460f4aeb1d251(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyMysqlFlexibleServerRetentionRuleLifeCycle, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67810286ac96cdbfe5697c52d04abcbed6b7d8c1fbd47ab3da98c5442fe5f1fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682937e9c19e19d168cca95c9bf0cce7d8887d216359fc64b95288bcaa7c12b7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b109bc1c6280cec9187ab7942029c6c2f808f2431ec726f53e4c23ed54cd8917(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyMysqlFlexibleServerRetentionRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a6e6428eaa0c311c34eeefa233741150b4dc72bd57a135cd5f7c2b08e8cfbb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b3fad46677a099d8b1296c5f10d856043d2a66bd89e2a146baea65673710af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca317f63dd9e2f4a822d8dab2d68d02102b3a127ccb99bffa9507e9741687e1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e6ac7e5d9099efd0d11c688f1dec8361a735da6ebf015540db507ea751689d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8217d373a9732416d350bdddbddcdc0fe764256f010b49453f4297964e50784a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe8749fb8bac39ca89ac6ce6d3d74b34ff0e4aac30e341e4e139f4a56f7f030d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyMysqlFlexibleServerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
