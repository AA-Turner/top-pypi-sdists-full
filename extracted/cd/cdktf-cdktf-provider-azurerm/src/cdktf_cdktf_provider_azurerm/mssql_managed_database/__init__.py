r'''
# `azurerm_mssql_managed_database`

Refer to the Terraform Registry for docs: [`azurerm_mssql_managed_database`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database).
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


class MssqlManagedDatabase(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlManagedDatabase.MssqlManagedDatabase",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database azurerm_mssql_managed_database}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        managed_instance_id: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        long_term_retention_policy: typing.Optional[typing.Union["MssqlManagedDatabaseLongTermRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        point_in_time_restore: typing.Optional[typing.Union["MssqlManagedDatabasePointInTimeRestore", typing.Dict[builtins.str, typing.Any]]] = None,
        short_term_retention_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MssqlManagedDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database azurerm_mssql_managed_database} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param managed_instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#managed_instance_id MssqlManagedDatabase#managed_instance_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#name MssqlManagedDatabase#name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#id MssqlManagedDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param long_term_retention_policy: long_term_retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#long_term_retention_policy MssqlManagedDatabase#long_term_retention_policy}
        :param point_in_time_restore: point_in_time_restore block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#point_in_time_restore MssqlManagedDatabase#point_in_time_restore}
        :param short_term_retention_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#short_term_retention_days MssqlManagedDatabase#short_term_retention_days}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#tags MssqlManagedDatabase#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#timeouts MssqlManagedDatabase#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60470c7799150cdac0f149e15ff3fc22438abe39809c307ab57236f2e60c53f1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MssqlManagedDatabaseConfig(
            managed_instance_id=managed_instance_id,
            name=name,
            id=id,
            long_term_retention_policy=long_term_retention_policy,
            point_in_time_restore=point_in_time_restore,
            short_term_retention_days=short_term_retention_days,
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
        '''Generates CDKTF code for importing a MssqlManagedDatabase resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MssqlManagedDatabase to import.
        :param import_from_id: The id of the existing MssqlManagedDatabase that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MssqlManagedDatabase to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d46534f226fba8b0c7ec367b6253f3a5366490dc4888bd96f6ea63a4f67d3d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLongTermRetentionPolicy")
    def put_long_term_retention_policy(
        self,
        *,
        immutable_backups_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monthly_retention: typing.Optional[builtins.str] = None,
        weekly_retention: typing.Optional[builtins.str] = None,
        week_of_year: typing.Optional[jsii.Number] = None,
        yearly_retention: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param immutable_backups_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#immutable_backups_enabled MssqlManagedDatabase#immutable_backups_enabled}.
        :param monthly_retention: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#monthly_retention MssqlManagedDatabase#monthly_retention}.
        :param weekly_retention: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#weekly_retention MssqlManagedDatabase#weekly_retention}.
        :param week_of_year: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#week_of_year MssqlManagedDatabase#week_of_year}.
        :param yearly_retention: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#yearly_retention MssqlManagedDatabase#yearly_retention}.
        '''
        value = MssqlManagedDatabaseLongTermRetentionPolicy(
            immutable_backups_enabled=immutable_backups_enabled,
            monthly_retention=monthly_retention,
            weekly_retention=weekly_retention,
            week_of_year=week_of_year,
            yearly_retention=yearly_retention,
        )

        return typing.cast(None, jsii.invoke(self, "putLongTermRetentionPolicy", [value]))

    @jsii.member(jsii_name="putPointInTimeRestore")
    def put_point_in_time_restore(
        self,
        *,
        restore_point_in_time: builtins.str,
        source_database_id: builtins.str,
    ) -> None:
        '''
        :param restore_point_in_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#restore_point_in_time MssqlManagedDatabase#restore_point_in_time}.
        :param source_database_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#source_database_id MssqlManagedDatabase#source_database_id}.
        '''
        value = MssqlManagedDatabasePointInTimeRestore(
            restore_point_in_time=restore_point_in_time,
            source_database_id=source_database_id,
        )

        return typing.cast(None, jsii.invoke(self, "putPointInTimeRestore", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#create MssqlManagedDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#delete MssqlManagedDatabase#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#read MssqlManagedDatabase#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#update MssqlManagedDatabase#update}.
        '''
        value = MssqlManagedDatabaseTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLongTermRetentionPolicy")
    def reset_long_term_retention_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongTermRetentionPolicy", []))

    @jsii.member(jsii_name="resetPointInTimeRestore")
    def reset_point_in_time_restore(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPointInTimeRestore", []))

    @jsii.member(jsii_name="resetShortTermRetentionDays")
    def reset_short_term_retention_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShortTermRetentionDays", []))

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
    @jsii.member(jsii_name="longTermRetentionPolicy")
    def long_term_retention_policy(
        self,
    ) -> "MssqlManagedDatabaseLongTermRetentionPolicyOutputReference":
        return typing.cast("MssqlManagedDatabaseLongTermRetentionPolicyOutputReference", jsii.get(self, "longTermRetentionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="pointInTimeRestore")
    def point_in_time_restore(
        self,
    ) -> "MssqlManagedDatabasePointInTimeRestoreOutputReference":
        return typing.cast("MssqlManagedDatabasePointInTimeRestoreOutputReference", jsii.get(self, "pointInTimeRestore"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MssqlManagedDatabaseTimeoutsOutputReference":
        return typing.cast("MssqlManagedDatabaseTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="longTermRetentionPolicyInput")
    def long_term_retention_policy_input(
        self,
    ) -> typing.Optional["MssqlManagedDatabaseLongTermRetentionPolicy"]:
        return typing.cast(typing.Optional["MssqlManagedDatabaseLongTermRetentionPolicy"], jsii.get(self, "longTermRetentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="managedInstanceIdInput")
    def managed_instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedInstanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pointInTimeRestoreInput")
    def point_in_time_restore_input(
        self,
    ) -> typing.Optional["MssqlManagedDatabasePointInTimeRestore"]:
        return typing.cast(typing.Optional["MssqlManagedDatabasePointInTimeRestore"], jsii.get(self, "pointInTimeRestoreInput"))

    @builtins.property
    @jsii.member(jsii_name="shortTermRetentionDaysInput")
    def short_term_retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "shortTermRetentionDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MssqlManagedDatabaseTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MssqlManagedDatabaseTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5b54a826d5aa3f0dabad0118e39bfe76793edf2d9d6c33301d2ed1d274ca9ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedInstanceId")
    def managed_instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedInstanceId"))

    @managed_instance_id.setter
    def managed_instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__503d46964e61479aae52565d7b54e618458012b07aa1cfe6389e604f181ee92d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedInstanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e631807dc92104b98e7f79d7db9ab9a351fa96dc485a3a3b162ff13fe453bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shortTermRetentionDays")
    def short_term_retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "shortTermRetentionDays"))

    @short_term_retention_days.setter
    def short_term_retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1684bf8e1f5370abf94b8dc14ece63231032a1f39e67d63ba0f481f2146d3379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shortTermRetentionDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a74f367b961c31bb9469f4baa56f37f90847dbc336c954be1a242bf6a4b26777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlManagedDatabase.MssqlManagedDatabaseConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "managed_instance_id": "managedInstanceId",
        "name": "name",
        "id": "id",
        "long_term_retention_policy": "longTermRetentionPolicy",
        "point_in_time_restore": "pointInTimeRestore",
        "short_term_retention_days": "shortTermRetentionDays",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class MssqlManagedDatabaseConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        managed_instance_id: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        long_term_retention_policy: typing.Optional[typing.Union["MssqlManagedDatabaseLongTermRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        point_in_time_restore: typing.Optional[typing.Union["MssqlManagedDatabasePointInTimeRestore", typing.Dict[builtins.str, typing.Any]]] = None,
        short_term_retention_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MssqlManagedDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param managed_instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#managed_instance_id MssqlManagedDatabase#managed_instance_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#name MssqlManagedDatabase#name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#id MssqlManagedDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param long_term_retention_policy: long_term_retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#long_term_retention_policy MssqlManagedDatabase#long_term_retention_policy}
        :param point_in_time_restore: point_in_time_restore block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#point_in_time_restore MssqlManagedDatabase#point_in_time_restore}
        :param short_term_retention_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#short_term_retention_days MssqlManagedDatabase#short_term_retention_days}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#tags MssqlManagedDatabase#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#timeouts MssqlManagedDatabase#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(long_term_retention_policy, dict):
            long_term_retention_policy = MssqlManagedDatabaseLongTermRetentionPolicy(**long_term_retention_policy)
        if isinstance(point_in_time_restore, dict):
            point_in_time_restore = MssqlManagedDatabasePointInTimeRestore(**point_in_time_restore)
        if isinstance(timeouts, dict):
            timeouts = MssqlManagedDatabaseTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e198584fbcf370ab10aa0746b81bd6f417096bab5575f797a04461d60ac420e6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument managed_instance_id", value=managed_instance_id, expected_type=type_hints["managed_instance_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument long_term_retention_policy", value=long_term_retention_policy, expected_type=type_hints["long_term_retention_policy"])
            check_type(argname="argument point_in_time_restore", value=point_in_time_restore, expected_type=type_hints["point_in_time_restore"])
            check_type(argname="argument short_term_retention_days", value=short_term_retention_days, expected_type=type_hints["short_term_retention_days"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "managed_instance_id": managed_instance_id,
            "name": name,
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
        if long_term_retention_policy is not None:
            self._values["long_term_retention_policy"] = long_term_retention_policy
        if point_in_time_restore is not None:
            self._values["point_in_time_restore"] = point_in_time_restore
        if short_term_retention_days is not None:
            self._values["short_term_retention_days"] = short_term_retention_days
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
    def managed_instance_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#managed_instance_id MssqlManagedDatabase#managed_instance_id}.'''
        result = self._values.get("managed_instance_id")
        assert result is not None, "Required property 'managed_instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#name MssqlManagedDatabase#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#id MssqlManagedDatabase#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def long_term_retention_policy(
        self,
    ) -> typing.Optional["MssqlManagedDatabaseLongTermRetentionPolicy"]:
        '''long_term_retention_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#long_term_retention_policy MssqlManagedDatabase#long_term_retention_policy}
        '''
        result = self._values.get("long_term_retention_policy")
        return typing.cast(typing.Optional["MssqlManagedDatabaseLongTermRetentionPolicy"], result)

    @builtins.property
    def point_in_time_restore(
        self,
    ) -> typing.Optional["MssqlManagedDatabasePointInTimeRestore"]:
        '''point_in_time_restore block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#point_in_time_restore MssqlManagedDatabase#point_in_time_restore}
        '''
        result = self._values.get("point_in_time_restore")
        return typing.cast(typing.Optional["MssqlManagedDatabasePointInTimeRestore"], result)

    @builtins.property
    def short_term_retention_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#short_term_retention_days MssqlManagedDatabase#short_term_retention_days}.'''
        result = self._values.get("short_term_retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#tags MssqlManagedDatabase#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MssqlManagedDatabaseTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#timeouts MssqlManagedDatabase#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MssqlManagedDatabaseTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlManagedDatabaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlManagedDatabase.MssqlManagedDatabaseLongTermRetentionPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "immutable_backups_enabled": "immutableBackupsEnabled",
        "monthly_retention": "monthlyRetention",
        "weekly_retention": "weeklyRetention",
        "week_of_year": "weekOfYear",
        "yearly_retention": "yearlyRetention",
    },
)
class MssqlManagedDatabaseLongTermRetentionPolicy:
    def __init__(
        self,
        *,
        immutable_backups_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monthly_retention: typing.Optional[builtins.str] = None,
        weekly_retention: typing.Optional[builtins.str] = None,
        week_of_year: typing.Optional[jsii.Number] = None,
        yearly_retention: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param immutable_backups_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#immutable_backups_enabled MssqlManagedDatabase#immutable_backups_enabled}.
        :param monthly_retention: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#monthly_retention MssqlManagedDatabase#monthly_retention}.
        :param weekly_retention: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#weekly_retention MssqlManagedDatabase#weekly_retention}.
        :param week_of_year: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#week_of_year MssqlManagedDatabase#week_of_year}.
        :param yearly_retention: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#yearly_retention MssqlManagedDatabase#yearly_retention}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54a4f0ff040a82c135a2b732545fdf9780405cd4d98f429da03856e9ea3b6d6)
            check_type(argname="argument immutable_backups_enabled", value=immutable_backups_enabled, expected_type=type_hints["immutable_backups_enabled"])
            check_type(argname="argument monthly_retention", value=monthly_retention, expected_type=type_hints["monthly_retention"])
            check_type(argname="argument weekly_retention", value=weekly_retention, expected_type=type_hints["weekly_retention"])
            check_type(argname="argument week_of_year", value=week_of_year, expected_type=type_hints["week_of_year"])
            check_type(argname="argument yearly_retention", value=yearly_retention, expected_type=type_hints["yearly_retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if immutable_backups_enabled is not None:
            self._values["immutable_backups_enabled"] = immutable_backups_enabled
        if monthly_retention is not None:
            self._values["monthly_retention"] = monthly_retention
        if weekly_retention is not None:
            self._values["weekly_retention"] = weekly_retention
        if week_of_year is not None:
            self._values["week_of_year"] = week_of_year
        if yearly_retention is not None:
            self._values["yearly_retention"] = yearly_retention

    @builtins.property
    def immutable_backups_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#immutable_backups_enabled MssqlManagedDatabase#immutable_backups_enabled}.'''
        result = self._values.get("immutable_backups_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monthly_retention(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#monthly_retention MssqlManagedDatabase#monthly_retention}.'''
        result = self._values.get("monthly_retention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weekly_retention(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#weekly_retention MssqlManagedDatabase#weekly_retention}.'''
        result = self._values.get("weekly_retention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def week_of_year(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#week_of_year MssqlManagedDatabase#week_of_year}.'''
        result = self._values.get("week_of_year")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def yearly_retention(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#yearly_retention MssqlManagedDatabase#yearly_retention}.'''
        result = self._values.get("yearly_retention")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlManagedDatabaseLongTermRetentionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlManagedDatabaseLongTermRetentionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlManagedDatabase.MssqlManagedDatabaseLongTermRetentionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d44a0f85d99d04c011719d1f4dee3618cf16d3299bfcec4342f7c1d6bafaea31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetImmutableBackupsEnabled")
    def reset_immutable_backups_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImmutableBackupsEnabled", []))

    @jsii.member(jsii_name="resetMonthlyRetention")
    def reset_monthly_retention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthlyRetention", []))

    @jsii.member(jsii_name="resetWeeklyRetention")
    def reset_weekly_retention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeklyRetention", []))

    @jsii.member(jsii_name="resetWeekOfYear")
    def reset_week_of_year(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekOfYear", []))

    @jsii.member(jsii_name="resetYearlyRetention")
    def reset_yearly_retention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYearlyRetention", []))

    @builtins.property
    @jsii.member(jsii_name="immutableBackupsEnabledInput")
    def immutable_backups_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "immutableBackupsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="monthlyRetentionInput")
    def monthly_retention_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monthlyRetentionInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyRetentionInput")
    def weekly_retention_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "weeklyRetentionInput"))

    @builtins.property
    @jsii.member(jsii_name="weekOfYearInput")
    def week_of_year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weekOfYearInput"))

    @builtins.property
    @jsii.member(jsii_name="yearlyRetentionInput")
    def yearly_retention_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "yearlyRetentionInput"))

    @builtins.property
    @jsii.member(jsii_name="immutableBackupsEnabled")
    def immutable_backups_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "immutableBackupsEnabled"))

    @immutable_backups_enabled.setter
    def immutable_backups_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c41e0f5cd4e92152bf73a04f1223c7f4ef16c55b496d8d904bb94d45096a7662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "immutableBackupsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monthlyRetention")
    def monthly_retention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monthlyRetention"))

    @monthly_retention.setter
    def monthly_retention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28e525855562dd281a24ea398d0ce23c64f1fcde3b4b34b24413453c26106dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthlyRetention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeklyRetention")
    def weekly_retention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "weeklyRetention"))

    @weekly_retention.setter
    def weekly_retention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9a556834e460bd7a80e0ad35c1bfb5709fdd7c7aae469786bddc4bdf027d4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeklyRetention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekOfYear")
    def week_of_year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weekOfYear"))

    @week_of_year.setter
    def week_of_year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8df7caaa97d1d9dd67f7b2142a22b1432bd98bb11bf04bfe30eb40a6f2ca2ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekOfYear", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="yearlyRetention")
    def yearly_retention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "yearlyRetention"))

    @yearly_retention.setter
    def yearly_retention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1e6a04fccca468993e43676d6c1c1c6c090f6f6e40bfa28cd6a253cf7a02984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "yearlyRetention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MssqlManagedDatabaseLongTermRetentionPolicy]:
        return typing.cast(typing.Optional[MssqlManagedDatabaseLongTermRetentionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlManagedDatabaseLongTermRetentionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf9699ab969fb4088f2e4777cb5ff337c9823a6f0e3cca0a36c4691e49e0595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlManagedDatabase.MssqlManagedDatabasePointInTimeRestore",
    jsii_struct_bases=[],
    name_mapping={
        "restore_point_in_time": "restorePointInTime",
        "source_database_id": "sourceDatabaseId",
    },
)
class MssqlManagedDatabasePointInTimeRestore:
    def __init__(
        self,
        *,
        restore_point_in_time: builtins.str,
        source_database_id: builtins.str,
    ) -> None:
        '''
        :param restore_point_in_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#restore_point_in_time MssqlManagedDatabase#restore_point_in_time}.
        :param source_database_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#source_database_id MssqlManagedDatabase#source_database_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22b3b0d0cf074e4080f29096c70313ed660339e47aeeb2303776f0d2aa7466a2)
            check_type(argname="argument restore_point_in_time", value=restore_point_in_time, expected_type=type_hints["restore_point_in_time"])
            check_type(argname="argument source_database_id", value=source_database_id, expected_type=type_hints["source_database_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "restore_point_in_time": restore_point_in_time,
            "source_database_id": source_database_id,
        }

    @builtins.property
    def restore_point_in_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#restore_point_in_time MssqlManagedDatabase#restore_point_in_time}.'''
        result = self._values.get("restore_point_in_time")
        assert result is not None, "Required property 'restore_point_in_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_database_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#source_database_id MssqlManagedDatabase#source_database_id}.'''
        result = self._values.get("source_database_id")
        assert result is not None, "Required property 'source_database_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlManagedDatabasePointInTimeRestore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlManagedDatabasePointInTimeRestoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlManagedDatabase.MssqlManagedDatabasePointInTimeRestoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c85a7d190bb2ae7438f2b92137c28b89509d50dd0b561377beb622b34c335970)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="restorePointInTimeInput")
    def restore_point_in_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "restorePointInTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceDatabaseIdInput")
    def source_database_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceDatabaseIdInput"))

    @builtins.property
    @jsii.member(jsii_name="restorePointInTime")
    def restore_point_in_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "restorePointInTime"))

    @restore_point_in_time.setter
    def restore_point_in_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8af85057ce2126c3b51f8aca70576302b589eac714e0ca659b36abed231a4f5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restorePointInTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceDatabaseId")
    def source_database_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceDatabaseId"))

    @source_database_id.setter
    def source_database_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99198407061b291cff99ef236e737762f2ad1cefd6026c04f0a8336d76d05d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceDatabaseId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MssqlManagedDatabasePointInTimeRestore]:
        return typing.cast(typing.Optional[MssqlManagedDatabasePointInTimeRestore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlManagedDatabasePointInTimeRestore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a4442f273b208b1a91b76fd683d0834e9f9ee248eba47c2fa5525216e3fffcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlManagedDatabase.MssqlManagedDatabaseTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MssqlManagedDatabaseTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#create MssqlManagedDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#delete MssqlManagedDatabase#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#read MssqlManagedDatabase#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#update MssqlManagedDatabase#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__963450535c8ff764cca75c0b7a84cd47eaab4b2dc87b1ed21c94b3b5ff24f53c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#create MssqlManagedDatabase#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#delete MssqlManagedDatabase#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#read MssqlManagedDatabase#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_managed_database#update MssqlManagedDatabase#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlManagedDatabaseTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlManagedDatabaseTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlManagedDatabase.MssqlManagedDatabaseTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddf09dd584cafe57b60e3620a9059f9019176856d4cebf3461b18735d0aa42aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__131f7f8cac744371857fa607411d65edd8de1bfc5967af445618852cc993887f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac2b64f44549cc0ec3a72f6ce1a55d37c3a54a2c5983c4f08b1ec2035fe7682c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33dfa6a6c1bbbe7bcc7a91a6abb9c68846e19ccd2d3492d79946ad4ecc875903)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9346f27480566fa96b1e116c568f1cf09dce48fdbf933ce8e38c1455fd7a4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlManagedDatabaseTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlManagedDatabaseTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlManagedDatabaseTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a987b1a58521b1c8e99eb8352c77aa6107bd81da75c43472388cc051e7d01858)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MssqlManagedDatabase",
    "MssqlManagedDatabaseConfig",
    "MssqlManagedDatabaseLongTermRetentionPolicy",
    "MssqlManagedDatabaseLongTermRetentionPolicyOutputReference",
    "MssqlManagedDatabasePointInTimeRestore",
    "MssqlManagedDatabasePointInTimeRestoreOutputReference",
    "MssqlManagedDatabaseTimeouts",
    "MssqlManagedDatabaseTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__60470c7799150cdac0f149e15ff3fc22438abe39809c307ab57236f2e60c53f1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    managed_instance_id: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    long_term_retention_policy: typing.Optional[typing.Union[MssqlManagedDatabaseLongTermRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    point_in_time_restore: typing.Optional[typing.Union[MssqlManagedDatabasePointInTimeRestore, typing.Dict[builtins.str, typing.Any]]] = None,
    short_term_retention_days: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MssqlManagedDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f6d46534f226fba8b0c7ec367b6253f3a5366490dc4888bd96f6ea63a4f67d3d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b54a826d5aa3f0dabad0118e39bfe76793edf2d9d6c33301d2ed1d274ca9ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503d46964e61479aae52565d7b54e618458012b07aa1cfe6389e604f181ee92d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e631807dc92104b98e7f79d7db9ab9a351fa96dc485a3a3b162ff13fe453bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1684bf8e1f5370abf94b8dc14ece63231032a1f39e67d63ba0f481f2146d3379(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74f367b961c31bb9469f4baa56f37f90847dbc336c954be1a242bf6a4b26777(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e198584fbcf370ab10aa0746b81bd6f417096bab5575f797a04461d60ac420e6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    managed_instance_id: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    long_term_retention_policy: typing.Optional[typing.Union[MssqlManagedDatabaseLongTermRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    point_in_time_restore: typing.Optional[typing.Union[MssqlManagedDatabasePointInTimeRestore, typing.Dict[builtins.str, typing.Any]]] = None,
    short_term_retention_days: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MssqlManagedDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54a4f0ff040a82c135a2b732545fdf9780405cd4d98f429da03856e9ea3b6d6(
    *,
    immutable_backups_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monthly_retention: typing.Optional[builtins.str] = None,
    weekly_retention: typing.Optional[builtins.str] = None,
    week_of_year: typing.Optional[jsii.Number] = None,
    yearly_retention: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44a0f85d99d04c011719d1f4dee3618cf16d3299bfcec4342f7c1d6bafaea31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c41e0f5cd4e92152bf73a04f1223c7f4ef16c55b496d8d904bb94d45096a7662(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e525855562dd281a24ea398d0ce23c64f1fcde3b4b34b24413453c26106dbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9a556834e460bd7a80e0ad35c1bfb5709fdd7c7aae469786bddc4bdf027d4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8df7caaa97d1d9dd67f7b2142a22b1432bd98bb11bf04bfe30eb40a6f2ca2ca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e6a04fccca468993e43676d6c1c1c6c090f6f6e40bfa28cd6a253cf7a02984(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf9699ab969fb4088f2e4777cb5ff337c9823a6f0e3cca0a36c4691e49e0595(
    value: typing.Optional[MssqlManagedDatabaseLongTermRetentionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b3b0d0cf074e4080f29096c70313ed660339e47aeeb2303776f0d2aa7466a2(
    *,
    restore_point_in_time: builtins.str,
    source_database_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85a7d190bb2ae7438f2b92137c28b89509d50dd0b561377beb622b34c335970(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8af85057ce2126c3b51f8aca70576302b589eac714e0ca659b36abed231a4f5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99198407061b291cff99ef236e737762f2ad1cefd6026c04f0a8336d76d05d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4442f273b208b1a91b76fd683d0834e9f9ee248eba47c2fa5525216e3fffcd(
    value: typing.Optional[MssqlManagedDatabasePointInTimeRestore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963450535c8ff764cca75c0b7a84cd47eaab4b2dc87b1ed21c94b3b5ff24f53c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddf09dd584cafe57b60e3620a9059f9019176856d4cebf3461b18735d0aa42aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131f7f8cac744371857fa607411d65edd8de1bfc5967af445618852cc993887f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2b64f44549cc0ec3a72f6ce1a55d37c3a54a2c5983c4f08b1ec2035fe7682c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33dfa6a6c1bbbe7bcc7a91a6abb9c68846e19ccd2d3492d79946ad4ecc875903(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9346f27480566fa96b1e116c568f1cf09dce48fdbf933ce8e38c1455fd7a4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a987b1a58521b1c8e99eb8352c77aa6107bd81da75c43472388cc051e7d01858(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlManagedDatabaseTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
