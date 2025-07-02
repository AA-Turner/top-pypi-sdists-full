r'''
# `azurerm_data_protection_backup_policy_blob_storage`

Refer to the Terraform Registry for docs: [`azurerm_data_protection_backup_policy_blob_storage`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage).
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


class DataProtectionBackupPolicyBlobStorage(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyBlobStorage.DataProtectionBackupPolicyBlobStorage",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage azurerm_data_protection_backup_policy_blob_storage}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        vault_id: builtins.str,
        backup_repeating_time_intervals: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        operational_default_retention_duration: typing.Optional[builtins.str] = None,
        retention_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProtectionBackupPolicyBlobStorageRetentionRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["DataProtectionBackupPolicyBlobStorageTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        vault_default_retention_duration: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage azurerm_data_protection_backup_policy_blob_storage} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#name DataProtectionBackupPolicyBlobStorage#name}.
        :param vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#vault_id DataProtectionBackupPolicyBlobStorage#vault_id}.
        :param backup_repeating_time_intervals: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#backup_repeating_time_intervals DataProtectionBackupPolicyBlobStorage#backup_repeating_time_intervals}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#id DataProtectionBackupPolicyBlobStorage#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param operational_default_retention_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#operational_default_retention_duration DataProtectionBackupPolicyBlobStorage#operational_default_retention_duration}.
        :param retention_rule: retention_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#retention_rule DataProtectionBackupPolicyBlobStorage#retention_rule}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#timeouts DataProtectionBackupPolicyBlobStorage#timeouts}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#time_zone DataProtectionBackupPolicyBlobStorage#time_zone}.
        :param vault_default_retention_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#vault_default_retention_duration DataProtectionBackupPolicyBlobStorage#vault_default_retention_duration}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9ca5bac359f40e315bc5fd09d4b03fcd40ba18840c5f1f4c9947116ab2b147)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataProtectionBackupPolicyBlobStorageConfig(
            name=name,
            vault_id=vault_id,
            backup_repeating_time_intervals=backup_repeating_time_intervals,
            id=id,
            operational_default_retention_duration=operational_default_retention_duration,
            retention_rule=retention_rule,
            timeouts=timeouts,
            time_zone=time_zone,
            vault_default_retention_duration=vault_default_retention_duration,
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
        '''Generates CDKTF code for importing a DataProtectionBackupPolicyBlobStorage resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataProtectionBackupPolicyBlobStorage to import.
        :param import_from_id: The id of the existing DataProtectionBackupPolicyBlobStorage that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataProtectionBackupPolicyBlobStorage to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029b85ac2122e0922f3aeb965d6b1ec702fb2435d2a418191ea3e342b44a8801)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRetentionRule")
    def put_retention_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProtectionBackupPolicyBlobStorageRetentionRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b464a30350cd6780c62ea0ffd233bfec9f3c68513ceec4baf446af0bd1e3763)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#create DataProtectionBackupPolicyBlobStorage#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#delete DataProtectionBackupPolicyBlobStorage#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#read DataProtectionBackupPolicyBlobStorage#read}.
        '''
        value = DataProtectionBackupPolicyBlobStorageTimeouts(
            create=create, delete=delete, read=read
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBackupRepeatingTimeIntervals")
    def reset_backup_repeating_time_intervals(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupRepeatingTimeIntervals", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOperationalDefaultRetentionDuration")
    def reset_operational_default_retention_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperationalDefaultRetentionDuration", []))

    @jsii.member(jsii_name="resetRetentionRule")
    def reset_retention_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionRule", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

    @jsii.member(jsii_name="resetVaultDefaultRetentionDuration")
    def reset_vault_default_retention_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVaultDefaultRetentionDuration", []))

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
    @jsii.member(jsii_name="retentionRule")
    def retention_rule(
        self,
    ) -> "DataProtectionBackupPolicyBlobStorageRetentionRuleList":
        return typing.cast("DataProtectionBackupPolicyBlobStorageRetentionRuleList", jsii.get(self, "retentionRule"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "DataProtectionBackupPolicyBlobStorageTimeoutsOutputReference":
        return typing.cast("DataProtectionBackupPolicyBlobStorageTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="backupRepeatingTimeIntervalsInput")
    def backup_repeating_time_intervals_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "backupRepeatingTimeIntervalsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="operationalDefaultRetentionDurationInput")
    def operational_default_retention_duration_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationalDefaultRetentionDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionRuleInput")
    def retention_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyBlobStorageRetentionRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyBlobStorageRetentionRule"]]], jsii.get(self, "retentionRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataProtectionBackupPolicyBlobStorageTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataProtectionBackupPolicyBlobStorageTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="vaultDefaultRetentionDurationInput")
    def vault_default_retention_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vaultDefaultRetentionDurationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4b258909182a5f7442b136520e3f327af88029407aacbf6fc3810b6468d08b97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupRepeatingTimeIntervals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df5a7a8cfbdd4780b252eea74907683cdaadadabdf5cda4fe8d731632a1b51a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4729bf4ec528285e1f6f8526fc9468c617fee7a52e821b874ff3bd380bc24f72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operationalDefaultRetentionDuration")
    def operational_default_retention_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationalDefaultRetentionDuration"))

    @operational_default_retention_duration.setter
    def operational_default_retention_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f85105f570a8cb985db366e1c1b3c5074cdaae779909b7e0ac15cc5ca2ad5ca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationalDefaultRetentionDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6cc2227f21e37133f4b4b9c1c7e026d87723334ace830a383bd9b77bedd353e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vaultDefaultRetentionDuration")
    def vault_default_retention_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vaultDefaultRetentionDuration"))

    @vault_default_retention_duration.setter
    def vault_default_retention_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__372e1498e0b1a1b8c1882b377915546291f0ffe5d66fbb7eb095bf5ea52e746e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vaultDefaultRetentionDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vaultId")
    def vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vaultId"))

    @vault_id.setter
    def vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed01649f15c2ffaf65a99b129a63d0e16e7d9db0115aef15dca61a25c38edb85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vaultId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyBlobStorage.DataProtectionBackupPolicyBlobStorageConfig",
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
        "vault_id": "vaultId",
        "backup_repeating_time_intervals": "backupRepeatingTimeIntervals",
        "id": "id",
        "operational_default_retention_duration": "operationalDefaultRetentionDuration",
        "retention_rule": "retentionRule",
        "timeouts": "timeouts",
        "time_zone": "timeZone",
        "vault_default_retention_duration": "vaultDefaultRetentionDuration",
    },
)
class DataProtectionBackupPolicyBlobStorageConfig(
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
        name: builtins.str,
        vault_id: builtins.str,
        backup_repeating_time_intervals: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        operational_default_retention_duration: typing.Optional[builtins.str] = None,
        retention_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProtectionBackupPolicyBlobStorageRetentionRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["DataProtectionBackupPolicyBlobStorageTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        vault_default_retention_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#name DataProtectionBackupPolicyBlobStorage#name}.
        :param vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#vault_id DataProtectionBackupPolicyBlobStorage#vault_id}.
        :param backup_repeating_time_intervals: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#backup_repeating_time_intervals DataProtectionBackupPolicyBlobStorage#backup_repeating_time_intervals}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#id DataProtectionBackupPolicyBlobStorage#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param operational_default_retention_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#operational_default_retention_duration DataProtectionBackupPolicyBlobStorage#operational_default_retention_duration}.
        :param retention_rule: retention_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#retention_rule DataProtectionBackupPolicyBlobStorage#retention_rule}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#timeouts DataProtectionBackupPolicyBlobStorage#timeouts}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#time_zone DataProtectionBackupPolicyBlobStorage#time_zone}.
        :param vault_default_retention_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#vault_default_retention_duration DataProtectionBackupPolicyBlobStorage#vault_default_retention_duration}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DataProtectionBackupPolicyBlobStorageTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__179b6e30e49928be582025347e6b25ff70f1b769490ff2e4f9f51f0c3d5b6643)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vault_id", value=vault_id, expected_type=type_hints["vault_id"])
            check_type(argname="argument backup_repeating_time_intervals", value=backup_repeating_time_intervals, expected_type=type_hints["backup_repeating_time_intervals"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument operational_default_retention_duration", value=operational_default_retention_duration, expected_type=type_hints["operational_default_retention_duration"])
            check_type(argname="argument retention_rule", value=retention_rule, expected_type=type_hints["retention_rule"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument vault_default_retention_duration", value=vault_default_retention_duration, expected_type=type_hints["vault_default_retention_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if backup_repeating_time_intervals is not None:
            self._values["backup_repeating_time_intervals"] = backup_repeating_time_intervals
        if id is not None:
            self._values["id"] = id
        if operational_default_retention_duration is not None:
            self._values["operational_default_retention_duration"] = operational_default_retention_duration
        if retention_rule is not None:
            self._values["retention_rule"] = retention_rule
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if time_zone is not None:
            self._values["time_zone"] = time_zone
        if vault_default_retention_duration is not None:
            self._values["vault_default_retention_duration"] = vault_default_retention_duration

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#name DataProtectionBackupPolicyBlobStorage#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vault_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#vault_id DataProtectionBackupPolicyBlobStorage#vault_id}.'''
        result = self._values.get("vault_id")
        assert result is not None, "Required property 'vault_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_repeating_time_intervals(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#backup_repeating_time_intervals DataProtectionBackupPolicyBlobStorage#backup_repeating_time_intervals}.'''
        result = self._values.get("backup_repeating_time_intervals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#id DataProtectionBackupPolicyBlobStorage#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operational_default_retention_duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#operational_default_retention_duration DataProtectionBackupPolicyBlobStorage#operational_default_retention_duration}.'''
        result = self._values.get("operational_default_retention_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyBlobStorageRetentionRule"]]]:
        '''retention_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#retention_rule DataProtectionBackupPolicyBlobStorage#retention_rule}
        '''
        result = self._values.get("retention_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProtectionBackupPolicyBlobStorageRetentionRule"]]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["DataProtectionBackupPolicyBlobStorageTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#timeouts DataProtectionBackupPolicyBlobStorage#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataProtectionBackupPolicyBlobStorageTimeouts"], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#time_zone DataProtectionBackupPolicyBlobStorage#time_zone}.'''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vault_default_retention_duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#vault_default_retention_duration DataProtectionBackupPolicyBlobStorage#vault_default_retention_duration}.'''
        result = self._values.get("vault_default_retention_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyBlobStorageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyBlobStorage.DataProtectionBackupPolicyBlobStorageRetentionRule",
    jsii_struct_bases=[],
    name_mapping={
        "criteria": "criteria",
        "life_cycle": "lifeCycle",
        "name": "name",
        "priority": "priority",
    },
)
class DataProtectionBackupPolicyBlobStorageRetentionRule:
    def __init__(
        self,
        *,
        criteria: typing.Union["DataProtectionBackupPolicyBlobStorageRetentionRuleCriteria", typing.Dict[builtins.str, typing.Any]],
        life_cycle: typing.Union["DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycle", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        priority: jsii.Number,
    ) -> None:
        '''
        :param criteria: criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#criteria DataProtectionBackupPolicyBlobStorage#criteria}
        :param life_cycle: life_cycle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#life_cycle DataProtectionBackupPolicyBlobStorage#life_cycle}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#name DataProtectionBackupPolicyBlobStorage#name}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#priority DataProtectionBackupPolicyBlobStorage#priority}.
        '''
        if isinstance(criteria, dict):
            criteria = DataProtectionBackupPolicyBlobStorageRetentionRuleCriteria(**criteria)
        if isinstance(life_cycle, dict):
            life_cycle = DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycle(**life_cycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8824e8a456ce442fec6975af67de85ef6e8b1c5a0f30960e740d6903354cb884)
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
    def criteria(self) -> "DataProtectionBackupPolicyBlobStorageRetentionRuleCriteria":
        '''criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#criteria DataProtectionBackupPolicyBlobStorage#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast("DataProtectionBackupPolicyBlobStorageRetentionRuleCriteria", result)

    @builtins.property
    def life_cycle(
        self,
    ) -> "DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycle":
        '''life_cycle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#life_cycle DataProtectionBackupPolicyBlobStorage#life_cycle}
        '''
        result = self._values.get("life_cycle")
        assert result is not None, "Required property 'life_cycle' is missing"
        return typing.cast("DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycle", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#name DataProtectionBackupPolicyBlobStorage#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#priority DataProtectionBackupPolicyBlobStorage#priority}.'''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyBlobStorageRetentionRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyBlobStorage.DataProtectionBackupPolicyBlobStorageRetentionRuleCriteria",
    jsii_struct_bases=[],
    name_mapping={
        "absolute_criteria": "absoluteCriteria",
        "days_of_month": "daysOfMonth",
        "days_of_week": "daysOfWeek",
        "months_of_year": "monthsOfYear",
        "scheduled_backup_times": "scheduledBackupTimes",
        "weeks_of_month": "weeksOfMonth",
    },
)
class DataProtectionBackupPolicyBlobStorageRetentionRuleCriteria:
    def __init__(
        self,
        *,
        absolute_criteria: typing.Optional[builtins.str] = None,
        days_of_month: typing.Optional[typing.Sequence[jsii.Number]] = None,
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
        months_of_year: typing.Optional[typing.Sequence[builtins.str]] = None,
        scheduled_backup_times: typing.Optional[typing.Sequence[builtins.str]] = None,
        weeks_of_month: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param absolute_criteria: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#absolute_criteria DataProtectionBackupPolicyBlobStorage#absolute_criteria}.
        :param days_of_month: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#days_of_month DataProtectionBackupPolicyBlobStorage#days_of_month}.
        :param days_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#days_of_week DataProtectionBackupPolicyBlobStorage#days_of_week}.
        :param months_of_year: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#months_of_year DataProtectionBackupPolicyBlobStorage#months_of_year}.
        :param scheduled_backup_times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#scheduled_backup_times DataProtectionBackupPolicyBlobStorage#scheduled_backup_times}.
        :param weeks_of_month: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#weeks_of_month DataProtectionBackupPolicyBlobStorage#weeks_of_month}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eefc91078e05cfd381d518cf5d4c75440a11b5fb032ec5bd6a2e9c622594a3d)
            check_type(argname="argument absolute_criteria", value=absolute_criteria, expected_type=type_hints["absolute_criteria"])
            check_type(argname="argument days_of_month", value=days_of_month, expected_type=type_hints["days_of_month"])
            check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
            check_type(argname="argument months_of_year", value=months_of_year, expected_type=type_hints["months_of_year"])
            check_type(argname="argument scheduled_backup_times", value=scheduled_backup_times, expected_type=type_hints["scheduled_backup_times"])
            check_type(argname="argument weeks_of_month", value=weeks_of_month, expected_type=type_hints["weeks_of_month"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if absolute_criteria is not None:
            self._values["absolute_criteria"] = absolute_criteria
        if days_of_month is not None:
            self._values["days_of_month"] = days_of_month
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#absolute_criteria DataProtectionBackupPolicyBlobStorage#absolute_criteria}.'''
        result = self._values.get("absolute_criteria")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def days_of_month(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#days_of_month DataProtectionBackupPolicyBlobStorage#days_of_month}.'''
        result = self._values.get("days_of_month")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def days_of_week(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#days_of_week DataProtectionBackupPolicyBlobStorage#days_of_week}.'''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def months_of_year(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#months_of_year DataProtectionBackupPolicyBlobStorage#months_of_year}.'''
        result = self._values.get("months_of_year")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def scheduled_backup_times(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#scheduled_backup_times DataProtectionBackupPolicyBlobStorage#scheduled_backup_times}.'''
        result = self._values.get("scheduled_backup_times")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def weeks_of_month(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#weeks_of_month DataProtectionBackupPolicyBlobStorage#weeks_of_month}.'''
        result = self._values.get("weeks_of_month")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyBlobStorageRetentionRuleCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProtectionBackupPolicyBlobStorageRetentionRuleCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyBlobStorage.DataProtectionBackupPolicyBlobStorageRetentionRuleCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__508800a1fd23818c75543116251ee81d91b0c5b57909d8f860bbe86938801f4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAbsoluteCriteria")
    def reset_absolute_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAbsoluteCriteria", []))

    @jsii.member(jsii_name="resetDaysOfMonth")
    def reset_days_of_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysOfMonth", []))

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
    @jsii.member(jsii_name="daysOfMonthInput")
    def days_of_month_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "daysOfMonthInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__acf48575047caa148a1c4d2500a07dcbc5cc0bd7bd886ef039e3628a0121d8e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "absoluteCriteria", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="daysOfMonth")
    def days_of_month(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "daysOfMonth"))

    @days_of_month.setter
    def days_of_month(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c0f2848d220e434cce9298135647cbeb5857673c641cab961f6d4e3d3a60671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "daysOfWeek"))

    @days_of_week.setter
    def days_of_week(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16684cb924eb3b334c4c536801ef69be6af50a01f6b68a9ae4d07d0dd490624e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monthsOfYear")
    def months_of_year(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "monthsOfYear"))

    @months_of_year.setter
    def months_of_year(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d86f23dd29f71dd91db0897e0c2e7da13c31a5c9ade5982ad8b1cd4657da573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthsOfYear", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduledBackupTimes")
    def scheduled_backup_times(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scheduledBackupTimes"))

    @scheduled_backup_times.setter
    def scheduled_backup_times(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b67f1d7a6aea33cd47de5510510262097651af6752573342534d804ce9235ba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduledBackupTimes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeksOfMonth")
    def weeks_of_month(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weeksOfMonth"))

    @weeks_of_month.setter
    def weeks_of_month(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b41543f21b8a528e3cdb7e1fa42218ac9ea858e948341f04de15813a24a692f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeksOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataProtectionBackupPolicyBlobStorageRetentionRuleCriteria]:
        return typing.cast(typing.Optional[DataProtectionBackupPolicyBlobStorageRetentionRuleCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataProtectionBackupPolicyBlobStorageRetentionRuleCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c186246a094e9263d4b9cefe5abd8e3fa56f8c060f8047d018e3adbe1cb558e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyBlobStorage.DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycle",
    jsii_struct_bases=[],
    name_mapping={"data_store_type": "dataStoreType", "duration": "duration"},
)
class DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycle:
    def __init__(
        self,
        *,
        data_store_type: builtins.str,
        duration: builtins.str,
    ) -> None:
        '''
        :param data_store_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#data_store_type DataProtectionBackupPolicyBlobStorage#data_store_type}.
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#duration DataProtectionBackupPolicyBlobStorage#duration}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c5fc8e540e6d383452b679c3e4311b9e1906699f710bb62901de1123604b7f1)
            check_type(argname="argument data_store_type", value=data_store_type, expected_type=type_hints["data_store_type"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_store_type": data_store_type,
            "duration": duration,
        }

    @builtins.property
    def data_store_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#data_store_type DataProtectionBackupPolicyBlobStorage#data_store_type}.'''
        result = self._values.get("data_store_type")
        assert result is not None, "Required property 'data_store_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def duration(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#duration DataProtectionBackupPolicyBlobStorage#duration}.'''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyBlobStorage.DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70b9c2a48b6db757804439b6038670b07adcfd0bf6fd837324235a1fff7ad7fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__8384465eb7a8575145c4a3f20992d0b6f4660f301128620131c90eb23dc522bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStoreType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f36339663d75cd29e29799b99e2a07387004844b1953fd5c2085b911eae4924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycle]:
        return typing.cast(typing.Optional[DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1faafc857f1d1ed63a0655d3ed37b7569c71885a2295e03dc00f95bfbb3f1ce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataProtectionBackupPolicyBlobStorageRetentionRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyBlobStorage.DataProtectionBackupPolicyBlobStorageRetentionRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1e60e290894e81e22d9498554c3536231bead870be0946eff6affc1158547c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataProtectionBackupPolicyBlobStorageRetentionRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__942caee456914b291b2c2adceadaacb106891afbb9822671d05d93a66ce3d63c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataProtectionBackupPolicyBlobStorageRetentionRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8f832619e7dcb1502a294898dddb0ac35635c98c7e0896b9517af9709e2c529)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bc4b6185035bad9b4c554ef15b872cdee5c1ac19a2dfca032a0e5586d7980d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2a7f85ee612fd42a6ec57a1d159fd33f45e44f48d9956fc2105ae3b09ee26b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyBlobStorageRetentionRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyBlobStorageRetentionRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyBlobStorageRetentionRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6db1dd1f1b49901011d8d77d4f027e6366d8d117796b3c6363228911db609e34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataProtectionBackupPolicyBlobStorageRetentionRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyBlobStorage.DataProtectionBackupPolicyBlobStorageRetentionRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c12ff9e4af159ae72d6e9021e8d222d56639a8afc15435427b1ecaa1253b89a3)
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
        days_of_month: typing.Optional[typing.Sequence[jsii.Number]] = None,
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
        months_of_year: typing.Optional[typing.Sequence[builtins.str]] = None,
        scheduled_backup_times: typing.Optional[typing.Sequence[builtins.str]] = None,
        weeks_of_month: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param absolute_criteria: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#absolute_criteria DataProtectionBackupPolicyBlobStorage#absolute_criteria}.
        :param days_of_month: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#days_of_month DataProtectionBackupPolicyBlobStorage#days_of_month}.
        :param days_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#days_of_week DataProtectionBackupPolicyBlobStorage#days_of_week}.
        :param months_of_year: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#months_of_year DataProtectionBackupPolicyBlobStorage#months_of_year}.
        :param scheduled_backup_times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#scheduled_backup_times DataProtectionBackupPolicyBlobStorage#scheduled_backup_times}.
        :param weeks_of_month: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#weeks_of_month DataProtectionBackupPolicyBlobStorage#weeks_of_month}.
        '''
        value = DataProtectionBackupPolicyBlobStorageRetentionRuleCriteria(
            absolute_criteria=absolute_criteria,
            days_of_month=days_of_month,
            days_of_week=days_of_week,
            months_of_year=months_of_year,
            scheduled_backup_times=scheduled_backup_times,
            weeks_of_month=weeks_of_month,
        )

        return typing.cast(None, jsii.invoke(self, "putCriteria", [value]))

    @jsii.member(jsii_name="putLifeCycle")
    def put_life_cycle(
        self,
        *,
        data_store_type: builtins.str,
        duration: builtins.str,
    ) -> None:
        '''
        :param data_store_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#data_store_type DataProtectionBackupPolicyBlobStorage#data_store_type}.
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#duration DataProtectionBackupPolicyBlobStorage#duration}.
        '''
        value = DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycle(
            data_store_type=data_store_type, duration=duration
        )

        return typing.cast(None, jsii.invoke(self, "putLifeCycle", [value]))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(
        self,
    ) -> DataProtectionBackupPolicyBlobStorageRetentionRuleCriteriaOutputReference:
        return typing.cast(DataProtectionBackupPolicyBlobStorageRetentionRuleCriteriaOutputReference, jsii.get(self, "criteria"))

    @builtins.property
    @jsii.member(jsii_name="lifeCycle")
    def life_cycle(
        self,
    ) -> DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycleOutputReference:
        return typing.cast(DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycleOutputReference, jsii.get(self, "lifeCycle"))

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(
        self,
    ) -> typing.Optional[DataProtectionBackupPolicyBlobStorageRetentionRuleCriteria]:
        return typing.cast(typing.Optional[DataProtectionBackupPolicyBlobStorageRetentionRuleCriteria], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="lifeCycleInput")
    def life_cycle_input(
        self,
    ) -> typing.Optional[DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycle]:
        return typing.cast(typing.Optional[DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycle], jsii.get(self, "lifeCycleInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3bffacb5e05ee14f83cd2d9501b93dffbf3d94573fdf54d1330dbb373e28fba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18b9685dc19025056421028f3f7b9de5b4c672f2827a846a3c34d5cca78ad03e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyBlobStorageRetentionRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyBlobStorageRetentionRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyBlobStorageRetentionRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1188d084d38322d7e5c7aae15d6c51111f49e928f1245fec6e35399ff06d784e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyBlobStorage.DataProtectionBackupPolicyBlobStorageTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class DataProtectionBackupPolicyBlobStorageTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#create DataProtectionBackupPolicyBlobStorage#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#delete DataProtectionBackupPolicyBlobStorage#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#read DataProtectionBackupPolicyBlobStorage#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84fe5cc24db9464e2a22809c2919508cbbeda1fdf4b59d4cf536530824bfb7c6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#create DataProtectionBackupPolicyBlobStorage#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#delete DataProtectionBackupPolicyBlobStorage#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_policy_blob_storage#read DataProtectionBackupPolicyBlobStorage#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupPolicyBlobStorageTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProtectionBackupPolicyBlobStorageTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupPolicyBlobStorage.DataProtectionBackupPolicyBlobStorageTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf5bb43e3121365847b46deab7dd437786528fb1062460c46104979e923901ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc74cf3bdf11087acb055cdaecc89426ee2395f56098cf96680bd9123c7eec30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a0993395cc6b29bff13219b6f04ddbf8cda578374adfd20a5fed04987dc09f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac899740734404834ea236dd685a58311290d5916102a7f9bff8a4cc91ce68ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyBlobStorageTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyBlobStorageTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyBlobStorageTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e5275e52ab37f15edbcf1ef5f1aa34f0beb794d932465e954c693d352133ae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataProtectionBackupPolicyBlobStorage",
    "DataProtectionBackupPolicyBlobStorageConfig",
    "DataProtectionBackupPolicyBlobStorageRetentionRule",
    "DataProtectionBackupPolicyBlobStorageRetentionRuleCriteria",
    "DataProtectionBackupPolicyBlobStorageRetentionRuleCriteriaOutputReference",
    "DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycle",
    "DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycleOutputReference",
    "DataProtectionBackupPolicyBlobStorageRetentionRuleList",
    "DataProtectionBackupPolicyBlobStorageRetentionRuleOutputReference",
    "DataProtectionBackupPolicyBlobStorageTimeouts",
    "DataProtectionBackupPolicyBlobStorageTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2e9ca5bac359f40e315bc5fd09d4b03fcd40ba18840c5f1f4c9947116ab2b147(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    vault_id: builtins.str,
    backup_repeating_time_intervals: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    operational_default_retention_duration: typing.Optional[builtins.str] = None,
    retention_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyBlobStorageRetentionRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[DataProtectionBackupPolicyBlobStorageTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
    vault_default_retention_duration: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__029b85ac2122e0922f3aeb965d6b1ec702fb2435d2a418191ea3e342b44a8801(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b464a30350cd6780c62ea0ffd233bfec9f3c68513ceec4baf446af0bd1e3763(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyBlobStorageRetentionRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b258909182a5f7442b136520e3f327af88029407aacbf6fc3810b6468d08b97(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5a7a8cfbdd4780b252eea74907683cdaadadabdf5cda4fe8d731632a1b51a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4729bf4ec528285e1f6f8526fc9468c617fee7a52e821b874ff3bd380bc24f72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85105f570a8cb985db366e1c1b3c5074cdaae779909b7e0ac15cc5ca2ad5ca2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6cc2227f21e37133f4b4b9c1c7e026d87723334ace830a383bd9b77bedd353e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__372e1498e0b1a1b8c1882b377915546291f0ffe5d66fbb7eb095bf5ea52e746e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed01649f15c2ffaf65a99b129a63d0e16e7d9db0115aef15dca61a25c38edb85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179b6e30e49928be582025347e6b25ff70f1b769490ff2e4f9f51f0c3d5b6643(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    vault_id: builtins.str,
    backup_repeating_time_intervals: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    operational_default_retention_duration: typing.Optional[builtins.str] = None,
    retention_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProtectionBackupPolicyBlobStorageRetentionRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[DataProtectionBackupPolicyBlobStorageTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
    vault_default_retention_duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8824e8a456ce442fec6975af67de85ef6e8b1c5a0f30960e740d6903354cb884(
    *,
    criteria: typing.Union[DataProtectionBackupPolicyBlobStorageRetentionRuleCriteria, typing.Dict[builtins.str, typing.Any]],
    life_cycle: typing.Union[DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycle, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    priority: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eefc91078e05cfd381d518cf5d4c75440a11b5fb032ec5bd6a2e9c622594a3d(
    *,
    absolute_criteria: typing.Optional[builtins.str] = None,
    days_of_month: typing.Optional[typing.Sequence[jsii.Number]] = None,
    days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    months_of_year: typing.Optional[typing.Sequence[builtins.str]] = None,
    scheduled_backup_times: typing.Optional[typing.Sequence[builtins.str]] = None,
    weeks_of_month: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__508800a1fd23818c75543116251ee81d91b0c5b57909d8f860bbe86938801f4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf48575047caa148a1c4d2500a07dcbc5cc0bd7bd886ef039e3628a0121d8e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c0f2848d220e434cce9298135647cbeb5857673c641cab961f6d4e3d3a60671(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16684cb924eb3b334c4c536801ef69be6af50a01f6b68a9ae4d07d0dd490624e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d86f23dd29f71dd91db0897e0c2e7da13c31a5c9ade5982ad8b1cd4657da573(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67f1d7a6aea33cd47de5510510262097651af6752573342534d804ce9235ba5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41543f21b8a528e3cdb7e1fa42218ac9ea858e948341f04de15813a24a692f1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c186246a094e9263d4b9cefe5abd8e3fa56f8c060f8047d018e3adbe1cb558e6(
    value: typing.Optional[DataProtectionBackupPolicyBlobStorageRetentionRuleCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c5fc8e540e6d383452b679c3e4311b9e1906699f710bb62901de1123604b7f1(
    *,
    data_store_type: builtins.str,
    duration: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b9c2a48b6db757804439b6038670b07adcfd0bf6fd837324235a1fff7ad7fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8384465eb7a8575145c4a3f20992d0b6f4660f301128620131c90eb23dc522bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f36339663d75cd29e29799b99e2a07387004844b1953fd5c2085b911eae4924(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1faafc857f1d1ed63a0655d3ed37b7569c71885a2295e03dc00f95bfbb3f1ce9(
    value: typing.Optional[DataProtectionBackupPolicyBlobStorageRetentionRuleLifeCycle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e60e290894e81e22d9498554c3536231bead870be0946eff6affc1158547c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__942caee456914b291b2c2adceadaacb106891afbb9822671d05d93a66ce3d63c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f832619e7dcb1502a294898dddb0ac35635c98c7e0896b9517af9709e2c529(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc4b6185035bad9b4c554ef15b872cdee5c1ac19a2dfca032a0e5586d7980d4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a7f85ee612fd42a6ec57a1d159fd33f45e44f48d9956fc2105ae3b09ee26b6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db1dd1f1b49901011d8d77d4f027e6366d8d117796b3c6363228911db609e34(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProtectionBackupPolicyBlobStorageRetentionRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c12ff9e4af159ae72d6e9021e8d222d56639a8afc15435427b1ecaa1253b89a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bffacb5e05ee14f83cd2d9501b93dffbf3d94573fdf54d1330dbb373e28fba8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b9685dc19025056421028f3f7b9de5b4c672f2827a846a3c34d5cca78ad03e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1188d084d38322d7e5c7aae15d6c51111f49e928f1245fec6e35399ff06d784e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyBlobStorageRetentionRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84fe5cc24db9464e2a22809c2919508cbbeda1fdf4b59d4cf536530824bfb7c6(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf5bb43e3121365847b46deab7dd437786528fb1062460c46104979e923901ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc74cf3bdf11087acb055cdaecc89426ee2395f56098cf96680bd9123c7eec30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a0993395cc6b29bff13219b6f04ddbf8cda578374adfd20a5fed04987dc09f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac899740734404834ea236dd685a58311290d5916102a7f9bff8a4cc91ce68ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e5275e52ab37f15edbcf1ef5f1aa34f0beb794d932465e954c693d352133ae8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupPolicyBlobStorageTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
