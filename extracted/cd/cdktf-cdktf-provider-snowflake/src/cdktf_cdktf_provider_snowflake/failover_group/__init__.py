r'''
# `snowflake_failover_group`

Refer to the Terraform Registry for docs: [`snowflake_failover_group`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group).
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


class FailoverGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.failoverGroup.FailoverGroup",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group snowflake_failover_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        allowed_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_databases: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_integration_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_shares: typing.Optional[typing.Sequence[builtins.str]] = None,
        from_replica: typing.Optional[typing.Union["FailoverGroupFromReplica", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_edition_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        object_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        replication_schedule: typing.Optional[typing.Union["FailoverGroupReplicationSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group snowflake_failover_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Specifies the identifier for the failover group. The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the identifier string is enclosed in double quotes (e.g. "My object"). Identifiers enclosed in double quotes are also case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#name FailoverGroup#name}
        :param allowed_accounts: Specifies the target account or list of target accounts to which replication and failover of specified objects from the source account is enabled. Secondary failover groups in the target accounts in this list can be promoted to serve as the primary failover group in case of failover. Expected in the form <org_name>.<target_account_name> Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#allowed_accounts FailoverGroup#allowed_accounts}
        :param allowed_databases: Specifies the database or list of databases for which you are enabling replication and failover from the source account to the target account. The OBJECT_TYPES list must include DATABASES to set this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#allowed_databases FailoverGroup#allowed_databases}
        :param allowed_integration_types: Type(s) of integrations for which you are enabling replication and failover from the source account to the target account. This property requires that the OBJECT_TYPES list include INTEGRATIONS to set this parameter. The following integration types are supported: "SECURITY INTEGRATIONS", "API INTEGRATIONS", "STORAGE INTEGRATIONS", "EXTERNAL ACCESS INTEGRATIONS", "NOTIFICATION INTEGRATIONS" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#allowed_integration_types FailoverGroup#allowed_integration_types}
        :param allowed_shares: Specifies the share or list of shares for which you are enabling replication and failover from the source account to the target account. The OBJECT_TYPES list must include SHARES to set this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#allowed_shares FailoverGroup#allowed_shares}
        :param from_replica: from_replica block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#from_replica FailoverGroup#from_replica}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#id FailoverGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_edition_check: Allows replicating objects to accounts on lower editions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#ignore_edition_check FailoverGroup#ignore_edition_check}
        :param object_types: Type(s) of objects for which you are enabling replication and failover from the source account to the target account. The following object types are supported: "ACCOUNT PARAMETERS", "DATABASES", "INTEGRATIONS", "NETWORK POLICIES", "RESOURCE MONITORS", "ROLES", "SHARES", "USERS", "WAREHOUSES" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#object_types FailoverGroup#object_types}
        :param replication_schedule: replication_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#replication_schedule FailoverGroup#replication_schedule}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f98c7a4d256f7b283e5b2b2e8e877934ef8cce7ba7f95f3e41e28a15f56dc572)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FailoverGroupConfig(
            name=name,
            allowed_accounts=allowed_accounts,
            allowed_databases=allowed_databases,
            allowed_integration_types=allowed_integration_types,
            allowed_shares=allowed_shares,
            from_replica=from_replica,
            id=id,
            ignore_edition_check=ignore_edition_check,
            object_types=object_types,
            replication_schedule=replication_schedule,
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
        '''Generates CDKTF code for importing a FailoverGroup resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FailoverGroup to import.
        :param import_from_id: The id of the existing FailoverGroup that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FailoverGroup to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f55d447539569a8860b77e2aad3d9990120f452ac006c1250a373fe61c628d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFromReplica")
    def put_from_replica(
        self,
        *,
        name: builtins.str,
        organization_name: builtins.str,
        source_account_name: builtins.str,
    ) -> None:
        '''
        :param name: Identifier for the primary failover group in the source account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#name FailoverGroup#name}
        :param organization_name: Name of your Snowflake organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#organization_name FailoverGroup#organization_name}
        :param source_account_name: Source account from which you are enabling replication and failover of the specified objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#source_account_name FailoverGroup#source_account_name}
        '''
        value = FailoverGroupFromReplica(
            name=name,
            organization_name=organization_name,
            source_account_name=source_account_name,
        )

        return typing.cast(None, jsii.invoke(self, "putFromReplica", [value]))

    @jsii.member(jsii_name="putReplicationSchedule")
    def put_replication_schedule(
        self,
        *,
        cron: typing.Optional[typing.Union["FailoverGroupReplicationScheduleCron", typing.Dict[builtins.str, typing.Any]]] = None,
        interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cron: cron block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#cron FailoverGroup#cron}
        :param interval: Specifies the interval in minutes for the replication schedule. The interval must be greater than 0 and less than 1440 (24 hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#interval FailoverGroup#interval}
        '''
        value = FailoverGroupReplicationSchedule(cron=cron, interval=interval)

        return typing.cast(None, jsii.invoke(self, "putReplicationSchedule", [value]))

    @jsii.member(jsii_name="resetAllowedAccounts")
    def reset_allowed_accounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedAccounts", []))

    @jsii.member(jsii_name="resetAllowedDatabases")
    def reset_allowed_databases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedDatabases", []))

    @jsii.member(jsii_name="resetAllowedIntegrationTypes")
    def reset_allowed_integration_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedIntegrationTypes", []))

    @jsii.member(jsii_name="resetAllowedShares")
    def reset_allowed_shares(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedShares", []))

    @jsii.member(jsii_name="resetFromReplica")
    def reset_from_replica(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFromReplica", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIgnoreEditionCheck")
    def reset_ignore_edition_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreEditionCheck", []))

    @jsii.member(jsii_name="resetObjectTypes")
    def reset_object_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectTypes", []))

    @jsii.member(jsii_name="resetReplicationSchedule")
    def reset_replication_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicationSchedule", []))

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
    @jsii.member(jsii_name="fromReplica")
    def from_replica(self) -> "FailoverGroupFromReplicaOutputReference":
        return typing.cast("FailoverGroupFromReplicaOutputReference", jsii.get(self, "fromReplica"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="replicationSchedule")
    def replication_schedule(self) -> "FailoverGroupReplicationScheduleOutputReference":
        return typing.cast("FailoverGroupReplicationScheduleOutputReference", jsii.get(self, "replicationSchedule"))

    @builtins.property
    @jsii.member(jsii_name="allowedAccountsInput")
    def allowed_accounts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedAccountsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedDatabasesInput")
    def allowed_databases_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedDatabasesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedIntegrationTypesInput")
    def allowed_integration_types_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedIntegrationTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedSharesInput")
    def allowed_shares_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedSharesInput"))

    @builtins.property
    @jsii.member(jsii_name="fromReplicaInput")
    def from_replica_input(self) -> typing.Optional["FailoverGroupFromReplica"]:
        return typing.cast(typing.Optional["FailoverGroupFromReplica"], jsii.get(self, "fromReplicaInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreEditionCheckInput")
    def ignore_edition_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreEditionCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="objectTypesInput")
    def object_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "objectTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationScheduleInput")
    def replication_schedule_input(
        self,
    ) -> typing.Optional["FailoverGroupReplicationSchedule"]:
        return typing.cast(typing.Optional["FailoverGroupReplicationSchedule"], jsii.get(self, "replicationScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedAccounts")
    def allowed_accounts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedAccounts"))

    @allowed_accounts.setter
    def allowed_accounts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d60f86ea501b56a11c19443e7e061c2c0e8ef1ec9fa3398fcf65ff831f6c523c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedAccounts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedDatabases")
    def allowed_databases(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedDatabases"))

    @allowed_databases.setter
    def allowed_databases(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b77df0c09e8cf7e6fbc41110510b690addc1bc452de005f31801f88526c5d56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedDatabases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedIntegrationTypes")
    def allowed_integration_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedIntegrationTypes"))

    @allowed_integration_types.setter
    def allowed_integration_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e629faba378871cb9995bb6ca7437506fdac3f1a48a5895e9cc89636f38201f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedIntegrationTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedShares")
    def allowed_shares(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedShares"))

    @allowed_shares.setter
    def allowed_shares(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a0b0eeed1a245f95e0e7f91e913570eaeb1e9feb0b62ec03836e12e618a6b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedShares", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b61ec0aee96eb5579d9e3a47e7719534934ee1a6bbcbe3a93a53a711cfdaa40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreEditionCheck")
    def ignore_edition_check(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreEditionCheck"))

    @ignore_edition_check.setter
    def ignore_edition_check(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af194c40fbb6f94104c77655060bacf8470aef1acb172dbdd838ccbfacd2582b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreEditionCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07895877e7f0ed52026db78fa02b5fd705a54419efa047874c4f28fccbf42ca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectTypes")
    def object_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "objectTypes"))

    @object_types.setter
    def object_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3abb48dc60b9e180d7526eeb6da1c278b3b6d6a7de4f17644469e364684e2d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectTypes", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.failoverGroup.FailoverGroupConfig",
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
        "allowed_accounts": "allowedAccounts",
        "allowed_databases": "allowedDatabases",
        "allowed_integration_types": "allowedIntegrationTypes",
        "allowed_shares": "allowedShares",
        "from_replica": "fromReplica",
        "id": "id",
        "ignore_edition_check": "ignoreEditionCheck",
        "object_types": "objectTypes",
        "replication_schedule": "replicationSchedule",
    },
)
class FailoverGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        allowed_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_databases: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_integration_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_shares: typing.Optional[typing.Sequence[builtins.str]] = None,
        from_replica: typing.Optional[typing.Union["FailoverGroupFromReplica", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_edition_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        object_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        replication_schedule: typing.Optional[typing.Union["FailoverGroupReplicationSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Specifies the identifier for the failover group. The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the identifier string is enclosed in double quotes (e.g. "My object"). Identifiers enclosed in double quotes are also case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#name FailoverGroup#name}
        :param allowed_accounts: Specifies the target account or list of target accounts to which replication and failover of specified objects from the source account is enabled. Secondary failover groups in the target accounts in this list can be promoted to serve as the primary failover group in case of failover. Expected in the form <org_name>.<target_account_name> Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#allowed_accounts FailoverGroup#allowed_accounts}
        :param allowed_databases: Specifies the database or list of databases for which you are enabling replication and failover from the source account to the target account. The OBJECT_TYPES list must include DATABASES to set this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#allowed_databases FailoverGroup#allowed_databases}
        :param allowed_integration_types: Type(s) of integrations for which you are enabling replication and failover from the source account to the target account. This property requires that the OBJECT_TYPES list include INTEGRATIONS to set this parameter. The following integration types are supported: "SECURITY INTEGRATIONS", "API INTEGRATIONS", "STORAGE INTEGRATIONS", "EXTERNAL ACCESS INTEGRATIONS", "NOTIFICATION INTEGRATIONS" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#allowed_integration_types FailoverGroup#allowed_integration_types}
        :param allowed_shares: Specifies the share or list of shares for which you are enabling replication and failover from the source account to the target account. The OBJECT_TYPES list must include SHARES to set this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#allowed_shares FailoverGroup#allowed_shares}
        :param from_replica: from_replica block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#from_replica FailoverGroup#from_replica}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#id FailoverGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_edition_check: Allows replicating objects to accounts on lower editions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#ignore_edition_check FailoverGroup#ignore_edition_check}
        :param object_types: Type(s) of objects for which you are enabling replication and failover from the source account to the target account. The following object types are supported: "ACCOUNT PARAMETERS", "DATABASES", "INTEGRATIONS", "NETWORK POLICIES", "RESOURCE MONITORS", "ROLES", "SHARES", "USERS", "WAREHOUSES" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#object_types FailoverGroup#object_types}
        :param replication_schedule: replication_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#replication_schedule FailoverGroup#replication_schedule}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(from_replica, dict):
            from_replica = FailoverGroupFromReplica(**from_replica)
        if isinstance(replication_schedule, dict):
            replication_schedule = FailoverGroupReplicationSchedule(**replication_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__798959c5f7f407f0844281464b14aa6b017c4917b4d7b345102e2efecd6d2067)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allowed_accounts", value=allowed_accounts, expected_type=type_hints["allowed_accounts"])
            check_type(argname="argument allowed_databases", value=allowed_databases, expected_type=type_hints["allowed_databases"])
            check_type(argname="argument allowed_integration_types", value=allowed_integration_types, expected_type=type_hints["allowed_integration_types"])
            check_type(argname="argument allowed_shares", value=allowed_shares, expected_type=type_hints["allowed_shares"])
            check_type(argname="argument from_replica", value=from_replica, expected_type=type_hints["from_replica"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ignore_edition_check", value=ignore_edition_check, expected_type=type_hints["ignore_edition_check"])
            check_type(argname="argument object_types", value=object_types, expected_type=type_hints["object_types"])
            check_type(argname="argument replication_schedule", value=replication_schedule, expected_type=type_hints["replication_schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if allowed_accounts is not None:
            self._values["allowed_accounts"] = allowed_accounts
        if allowed_databases is not None:
            self._values["allowed_databases"] = allowed_databases
        if allowed_integration_types is not None:
            self._values["allowed_integration_types"] = allowed_integration_types
        if allowed_shares is not None:
            self._values["allowed_shares"] = allowed_shares
        if from_replica is not None:
            self._values["from_replica"] = from_replica
        if id is not None:
            self._values["id"] = id
        if ignore_edition_check is not None:
            self._values["ignore_edition_check"] = ignore_edition_check
        if object_types is not None:
            self._values["object_types"] = object_types
        if replication_schedule is not None:
            self._values["replication_schedule"] = replication_schedule

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
        '''Specifies the identifier for the failover group.

        The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the identifier string is enclosed in double quotes (e.g. "My object"). Identifiers enclosed in double quotes are also case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#name FailoverGroup#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the target account or list of target accounts to which replication and failover of specified objects from the source account is enabled.

        Secondary failover groups in the target accounts in this list can be promoted to serve as the primary failover group in case of failover. Expected in the form <org_name>.<target_account_name>

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#allowed_accounts FailoverGroup#allowed_accounts}
        '''
        result = self._values.get("allowed_accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_databases(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the database or list of databases for which you are enabling replication and failover from the source account to the target account.

        The OBJECT_TYPES list must include DATABASES to set this parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#allowed_databases FailoverGroup#allowed_databases}
        '''
        result = self._values.get("allowed_databases")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_integration_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Type(s) of integrations for which you are enabling replication and failover from the source account to the target account.

        This property requires that the OBJECT_TYPES list include INTEGRATIONS to set this parameter. The following integration types are supported: "SECURITY INTEGRATIONS", "API INTEGRATIONS", "STORAGE INTEGRATIONS", "EXTERNAL ACCESS INTEGRATIONS", "NOTIFICATION INTEGRATIONS"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#allowed_integration_types FailoverGroup#allowed_integration_types}
        '''
        result = self._values.get("allowed_integration_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_shares(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the share or list of shares for which you are enabling replication and failover from the source account to the target account.

        The OBJECT_TYPES list must include SHARES to set this parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#allowed_shares FailoverGroup#allowed_shares}
        '''
        result = self._values.get("allowed_shares")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def from_replica(self) -> typing.Optional["FailoverGroupFromReplica"]:
        '''from_replica block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#from_replica FailoverGroup#from_replica}
        '''
        result = self._values.get("from_replica")
        return typing.cast(typing.Optional["FailoverGroupFromReplica"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#id FailoverGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_edition_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows replicating objects to accounts on lower editions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#ignore_edition_check FailoverGroup#ignore_edition_check}
        '''
        result = self._values.get("ignore_edition_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def object_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Type(s) of objects for which you are enabling replication and failover from the source account to the target account.

        The following object types are supported: "ACCOUNT PARAMETERS", "DATABASES", "INTEGRATIONS", "NETWORK POLICIES", "RESOURCE MONITORS", "ROLES", "SHARES", "USERS", "WAREHOUSES"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#object_types FailoverGroup#object_types}
        '''
        result = self._values.get("object_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def replication_schedule(
        self,
    ) -> typing.Optional["FailoverGroupReplicationSchedule"]:
        '''replication_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#replication_schedule FailoverGroup#replication_schedule}
        '''
        result = self._values.get("replication_schedule")
        return typing.cast(typing.Optional["FailoverGroupReplicationSchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FailoverGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.failoverGroup.FailoverGroupFromReplica",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "organization_name": "organizationName",
        "source_account_name": "sourceAccountName",
    },
)
class FailoverGroupFromReplica:
    def __init__(
        self,
        *,
        name: builtins.str,
        organization_name: builtins.str,
        source_account_name: builtins.str,
    ) -> None:
        '''
        :param name: Identifier for the primary failover group in the source account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#name FailoverGroup#name}
        :param organization_name: Name of your Snowflake organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#organization_name FailoverGroup#organization_name}
        :param source_account_name: Source account from which you are enabling replication and failover of the specified objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#source_account_name FailoverGroup#source_account_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b782ddcb129598845a210766383f2bf0cc56a06feb0744c7c2a9521bed8f4ca7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument organization_name", value=organization_name, expected_type=type_hints["organization_name"])
            check_type(argname="argument source_account_name", value=source_account_name, expected_type=type_hints["source_account_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "organization_name": organization_name,
            "source_account_name": source_account_name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Identifier for the primary failover group in the source account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#name FailoverGroup#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization_name(self) -> builtins.str:
        '''Name of your Snowflake organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#organization_name FailoverGroup#organization_name}
        '''
        result = self._values.get("organization_name")
        assert result is not None, "Required property 'organization_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_account_name(self) -> builtins.str:
        '''Source account from which you are enabling replication and failover of the specified objects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#source_account_name FailoverGroup#source_account_name}
        '''
        result = self._values.get("source_account_name")
        assert result is not None, "Required property 'source_account_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FailoverGroupFromReplica(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FailoverGroupFromReplicaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.failoverGroup.FailoverGroupFromReplicaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72456d6191625f0622e955766932389add44c17196fa87d0c5d2b3385e9f59fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationNameInput")
    def organization_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceAccountNameInput")
    def source_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c71544f32ddc54c851b6ad58a3631b882f5409695dc11bbf2964e112b2d3a28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationName")
    def organization_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationName"))

    @organization_name.setter
    def organization_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a1236ec89b5699da1bff46fad07f19484528b6392ec7211e9e26270e4fef0fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceAccountName")
    def source_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceAccountName"))

    @source_account_name.setter
    def source_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc2ec86eb50ef7f280e1571cd35a0d2884f4627109f924aed74d4810af5c396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceAccountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FailoverGroupFromReplica]:
        return typing.cast(typing.Optional[FailoverGroupFromReplica], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[FailoverGroupFromReplica]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbbc9c178e1225a10a52e2259469187dfec6778c7098e9635ccfe8f9b0ced1f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.failoverGroup.FailoverGroupReplicationSchedule",
    jsii_struct_bases=[],
    name_mapping={"cron": "cron", "interval": "interval"},
)
class FailoverGroupReplicationSchedule:
    def __init__(
        self,
        *,
        cron: typing.Optional[typing.Union["FailoverGroupReplicationScheduleCron", typing.Dict[builtins.str, typing.Any]]] = None,
        interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cron: cron block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#cron FailoverGroup#cron}
        :param interval: Specifies the interval in minutes for the replication schedule. The interval must be greater than 0 and less than 1440 (24 hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#interval FailoverGroup#interval}
        '''
        if isinstance(cron, dict):
            cron = FailoverGroupReplicationScheduleCron(**cron)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97260e85063d760634d1a8691292a30b106d61144a4ab5791da7a60f267a7258)
            check_type(argname="argument cron", value=cron, expected_type=type_hints["cron"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cron is not None:
            self._values["cron"] = cron
        if interval is not None:
            self._values["interval"] = interval

    @builtins.property
    def cron(self) -> typing.Optional["FailoverGroupReplicationScheduleCron"]:
        '''cron block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#cron FailoverGroup#cron}
        '''
        result = self._values.get("cron")
        return typing.cast(typing.Optional["FailoverGroupReplicationScheduleCron"], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Specifies the interval in minutes for the replication schedule.

        The interval must be greater than 0 and less than 1440 (24 hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#interval FailoverGroup#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FailoverGroupReplicationSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.failoverGroup.FailoverGroupReplicationScheduleCron",
    jsii_struct_bases=[],
    name_mapping={"expression": "expression", "time_zone": "timeZone"},
)
class FailoverGroupReplicationScheduleCron:
    def __init__(self, *, expression: builtins.str, time_zone: builtins.str) -> None:
        '''
        :param expression: Specifies the cron expression for the replication schedule. The cron expression must be in the following format: "minute hour day-of-month month day-of-week". The following values are supported: minute: 0-59 hour: 0-23 day-of-month: 1-31 month: 1-12 day-of-week: 0-6 (0 is Sunday) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#expression FailoverGroup#expression}
        :param time_zone: Specifies the time zone for secondary group refresh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#time_zone FailoverGroup#time_zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c7154ee1bb25cd9792172aef6fd6c93083f4324f1c00a1258ab77a5ee7e0d1c)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
            "time_zone": time_zone,
        }

    @builtins.property
    def expression(self) -> builtins.str:
        '''Specifies the cron expression for the replication schedule.

        The cron expression must be in the following format: "minute hour day-of-month month day-of-week". The following values are supported: minute: 0-59 hour: 0-23 day-of-month: 1-31 month: 1-12 day-of-week: 0-6 (0 is Sunday)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#expression FailoverGroup#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''Specifies the time zone for secondary group refresh.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#time_zone FailoverGroup#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FailoverGroupReplicationScheduleCron(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FailoverGroupReplicationScheduleCronOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.failoverGroup.FailoverGroupReplicationScheduleCronOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76feca3abe77b2b7ae0736a861deaba292e2f96fd374e4873540de143f2d149c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701b290235bacf81e52f2e5b505a572f8d743ee73e2f63012ff0248763d3f084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d42fc0a48219f6f7aa09ef335c8ea5a3f212353efe9211d3d86b27e764a1c91d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FailoverGroupReplicationScheduleCron]:
        return typing.cast(typing.Optional[FailoverGroupReplicationScheduleCron], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FailoverGroupReplicationScheduleCron],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d46a4fac49eeca15aad2676e7cfdfff8140598e487a32c28fb482d49ed4a5425)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FailoverGroupReplicationScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.failoverGroup.FailoverGroupReplicationScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aabd548e78ddde0a997da9b85ab863280b9fb167cf3eaa37ddfb6874c90b97bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCron")
    def put_cron(self, *, expression: builtins.str, time_zone: builtins.str) -> None:
        '''
        :param expression: Specifies the cron expression for the replication schedule. The cron expression must be in the following format: "minute hour day-of-month month day-of-week". The following values are supported: minute: 0-59 hour: 0-23 day-of-month: 1-31 month: 1-12 day-of-week: 0-6 (0 is Sunday) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#expression FailoverGroup#expression}
        :param time_zone: Specifies the time zone for secondary group refresh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/failover_group#time_zone FailoverGroup#time_zone}
        '''
        value = FailoverGroupReplicationScheduleCron(
            expression=expression, time_zone=time_zone
        )

        return typing.cast(None, jsii.invoke(self, "putCron", [value]))

    @jsii.member(jsii_name="resetCron")
    def reset_cron(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCron", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @builtins.property
    @jsii.member(jsii_name="cron")
    def cron(self) -> FailoverGroupReplicationScheduleCronOutputReference:
        return typing.cast(FailoverGroupReplicationScheduleCronOutputReference, jsii.get(self, "cron"))

    @builtins.property
    @jsii.member(jsii_name="cronInput")
    def cron_input(self) -> typing.Optional[FailoverGroupReplicationScheduleCron]:
        return typing.cast(typing.Optional[FailoverGroupReplicationScheduleCron], jsii.get(self, "cronInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e29596ac3800e8f332683d9fdf91bc80e3adca5e5b31ae7b84c317eb4fe831ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FailoverGroupReplicationSchedule]:
        return typing.cast(typing.Optional[FailoverGroupReplicationSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FailoverGroupReplicationSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9599a9a3fede65b2bb54905b1cfff9c9981b1b77a31de2ca80b5b4d11440f39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FailoverGroup",
    "FailoverGroupConfig",
    "FailoverGroupFromReplica",
    "FailoverGroupFromReplicaOutputReference",
    "FailoverGroupReplicationSchedule",
    "FailoverGroupReplicationScheduleCron",
    "FailoverGroupReplicationScheduleCronOutputReference",
    "FailoverGroupReplicationScheduleOutputReference",
]

publication.publish()

def _typecheckingstub__f98c7a4d256f7b283e5b2b2e8e877934ef8cce7ba7f95f3e41e28a15f56dc572(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    allowed_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_databases: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_integration_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_shares: typing.Optional[typing.Sequence[builtins.str]] = None,
    from_replica: typing.Optional[typing.Union[FailoverGroupFromReplica, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_edition_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    object_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    replication_schedule: typing.Optional[typing.Union[FailoverGroupReplicationSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__97f55d447539569a8860b77e2aad3d9990120f452ac006c1250a373fe61c628d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60f86ea501b56a11c19443e7e061c2c0e8ef1ec9fa3398fcf65ff831f6c523c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b77df0c09e8cf7e6fbc41110510b690addc1bc452de005f31801f88526c5d56(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e629faba378871cb9995bb6ca7437506fdac3f1a48a5895e9cc89636f38201f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a0b0eeed1a245f95e0e7f91e913570eaeb1e9feb0b62ec03836e12e618a6b1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b61ec0aee96eb5579d9e3a47e7719534934ee1a6bbcbe3a93a53a711cfdaa40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af194c40fbb6f94104c77655060bacf8470aef1acb172dbdd838ccbfacd2582b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07895877e7f0ed52026db78fa02b5fd705a54419efa047874c4f28fccbf42ca2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3abb48dc60b9e180d7526eeb6da1c278b3b6d6a7de4f17644469e364684e2d1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798959c5f7f407f0844281464b14aa6b017c4917b4d7b345102e2efecd6d2067(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    allowed_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_databases: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_integration_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_shares: typing.Optional[typing.Sequence[builtins.str]] = None,
    from_replica: typing.Optional[typing.Union[FailoverGroupFromReplica, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_edition_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    object_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    replication_schedule: typing.Optional[typing.Union[FailoverGroupReplicationSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b782ddcb129598845a210766383f2bf0cc56a06feb0744c7c2a9521bed8f4ca7(
    *,
    name: builtins.str,
    organization_name: builtins.str,
    source_account_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72456d6191625f0622e955766932389add44c17196fa87d0c5d2b3385e9f59fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c71544f32ddc54c851b6ad58a3631b882f5409695dc11bbf2964e112b2d3a28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a1236ec89b5699da1bff46fad07f19484528b6392ec7211e9e26270e4fef0fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc2ec86eb50ef7f280e1571cd35a0d2884f4627109f924aed74d4810af5c396(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbbc9c178e1225a10a52e2259469187dfec6778c7098e9635ccfe8f9b0ced1f2(
    value: typing.Optional[FailoverGroupFromReplica],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97260e85063d760634d1a8691292a30b106d61144a4ab5791da7a60f267a7258(
    *,
    cron: typing.Optional[typing.Union[FailoverGroupReplicationScheduleCron, typing.Dict[builtins.str, typing.Any]]] = None,
    interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7154ee1bb25cd9792172aef6fd6c93083f4324f1c00a1258ab77a5ee7e0d1c(
    *,
    expression: builtins.str,
    time_zone: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76feca3abe77b2b7ae0736a861deaba292e2f96fd374e4873540de143f2d149c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701b290235bacf81e52f2e5b505a572f8d743ee73e2f63012ff0248763d3f084(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42fc0a48219f6f7aa09ef335c8ea5a3f212353efe9211d3d86b27e764a1c91d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d46a4fac49eeca15aad2676e7cfdfff8140598e487a32c28fb482d49ed4a5425(
    value: typing.Optional[FailoverGroupReplicationScheduleCron],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aabd548e78ddde0a997da9b85ab863280b9fb167cf3eaa37ddfb6874c90b97bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29596ac3800e8f332683d9fdf91bc80e3adca5e5b31ae7b84c317eb4fe831ae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9599a9a3fede65b2bb54905b1cfff9c9981b1b77a31de2ca80b5b4d11440f39(
    value: typing.Optional[FailoverGroupReplicationSchedule],
) -> None:
    """Type checking stubs"""
    pass
