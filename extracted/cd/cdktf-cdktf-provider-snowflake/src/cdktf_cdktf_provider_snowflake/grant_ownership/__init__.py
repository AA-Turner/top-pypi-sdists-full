r'''
# `snowflake_grant_ownership`

Refer to the Terraform Registry for docs: [`snowflake_grant_ownership`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership).
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


class GrantOwnership(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.grantOwnership.GrantOwnership",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership snowflake_grant_ownership}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        on: typing.Union["GrantOwnershipOn", typing.Dict[builtins.str, typing.Any]],
        account_role_name: typing.Optional[builtins.str] = None,
        database_role_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        outbound_privileges: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership snowflake_grant_ownership} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param on: on block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#on GrantOwnership#on}
        :param account_role_name: The fully qualified name of the account role to which privileges will be granted. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#account_role_name GrantOwnership#account_role_name}
        :param database_role_name: The fully qualified name of the database role to which privileges will be granted. For more information about this resource, see `docs <./database_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#database_role_name GrantOwnership#database_role_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#id GrantOwnership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param outbound_privileges: Specifies whether to remove or transfer all existing outbound privileges on the object when ownership is transferred to a new role. Available options are: REVOKE for removing existing privileges and COPY to transfer them with ownership. For more information head over to `Snowflake documentation <https://docs.snowflake.com/en/sql-reference/sql/grant-ownership#optional-parameters>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#outbound_privileges GrantOwnership#outbound_privileges}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee66262eb9f353f7b7e21182c2d9fafa5357724c9eec0b975187d44e464d1178)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GrantOwnershipConfig(
            on=on,
            account_role_name=account_role_name,
            database_role_name=database_role_name,
            id=id,
            outbound_privileges=outbound_privileges,
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
        '''Generates CDKTF code for importing a GrantOwnership resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GrantOwnership to import.
        :param import_from_id: The id of the existing GrantOwnership that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GrantOwnership to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ccf76e393878d437bb69a260a440eb8591804cf93402c0391218fea2ee88327)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putOn")
    def put_on(
        self,
        *,
        all: typing.Optional[typing.Union["GrantOwnershipOnAll", typing.Dict[builtins.str, typing.Any]]] = None,
        future: typing.Optional[typing.Union["GrantOwnershipOnFuture", typing.Dict[builtins.str, typing.Any]]] = None,
        object_name: typing.Optional[builtins.str] = None,
        object_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param all: all block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#all GrantOwnership#all}
        :param future: future block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#future GrantOwnership#future}
        :param object_name: Specifies the identifier for the object on which you are transferring ownership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#object_name GrantOwnership#object_name}
        :param object_type: Specifies the type of object on which you are transferring ownership. Available values are: AGGREGATION POLICY | ALERT | AUTHENTICATION POLICY | COMPUTE POOL | DATA METRIC FUNCTION | DATABASE | DATABASE ROLE | DYNAMIC TABLE | EVENT TABLE | EXTERNAL TABLE | EXTERNAL VOLUME | FAILOVER GROUP | FILE FORMAT | FUNCTION | GIT REPOSITORY | HYBRID TABLE | ICEBERG TABLE | IMAGE REPOSITORY | INTEGRATION | MATERIALIZED VIEW | NETWORK POLICY | NETWORK RULE | PACKAGES POLICY | PIPE | PROCEDURE | MASKING POLICY | PASSWORD POLICY | PROJECTION POLICY | REPLICATION GROUP | RESOURCE MONITOR | ROLE | ROW ACCESS POLICY | SCHEMA | SESSION POLICY | SECRET | SEQUENCE | STAGE | STREAM | TABLE | TAG | TASK | USER | VIEW | WAREHOUSE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#object_type GrantOwnership#object_type}
        '''
        value = GrantOwnershipOn(
            all=all, future=future, object_name=object_name, object_type=object_type
        )

        return typing.cast(None, jsii.invoke(self, "putOn", [value]))

    @jsii.member(jsii_name="resetAccountRoleName")
    def reset_account_role_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountRoleName", []))

    @jsii.member(jsii_name="resetDatabaseRoleName")
    def reset_database_role_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseRoleName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOutboundPrivileges")
    def reset_outbound_privileges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutboundPrivileges", []))

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
    @jsii.member(jsii_name="on")
    def on(self) -> "GrantOwnershipOnOutputReference":
        return typing.cast("GrantOwnershipOnOutputReference", jsii.get(self, "on"))

    @builtins.property
    @jsii.member(jsii_name="accountRoleNameInput")
    def account_role_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountRoleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseRoleNameInput")
    def database_role_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseRoleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="onInput")
    def on_input(self) -> typing.Optional["GrantOwnershipOn"]:
        return typing.cast(typing.Optional["GrantOwnershipOn"], jsii.get(self, "onInput"))

    @builtins.property
    @jsii.member(jsii_name="outboundPrivilegesInput")
    def outbound_privileges_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outboundPrivilegesInput"))

    @builtins.property
    @jsii.member(jsii_name="accountRoleName")
    def account_role_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountRoleName"))

    @account_role_name.setter
    def account_role_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25fba6a608695977b563127328451b3508d84c54f6662843c90bccec596a818b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountRoleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseRoleName")
    def database_role_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseRoleName"))

    @database_role_name.setter
    def database_role_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889e17549d799029598a9a5130a183de49749427975ad12f19901fa5d9f331d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseRoleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3049eb80d0f400312ab0ac8a7c935d43b97ad96a23f675d6a8da8b8f72eb75c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outboundPrivileges")
    def outbound_privileges(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outboundPrivileges"))

    @outbound_privileges.setter
    def outbound_privileges(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f39247fce9a4e9ee1072b7b973eb6d65011fdeb96aa662174aa1e0d6ff4f63c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundPrivileges", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.grantOwnership.GrantOwnershipConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "on": "on",
        "account_role_name": "accountRoleName",
        "database_role_name": "databaseRoleName",
        "id": "id",
        "outbound_privileges": "outboundPrivileges",
    },
)
class GrantOwnershipConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        on: typing.Union["GrantOwnershipOn", typing.Dict[builtins.str, typing.Any]],
        account_role_name: typing.Optional[builtins.str] = None,
        database_role_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        outbound_privileges: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param on: on block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#on GrantOwnership#on}
        :param account_role_name: The fully qualified name of the account role to which privileges will be granted. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#account_role_name GrantOwnership#account_role_name}
        :param database_role_name: The fully qualified name of the database role to which privileges will be granted. For more information about this resource, see `docs <./database_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#database_role_name GrantOwnership#database_role_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#id GrantOwnership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param outbound_privileges: Specifies whether to remove or transfer all existing outbound privileges on the object when ownership is transferred to a new role. Available options are: REVOKE for removing existing privileges and COPY to transfer them with ownership. For more information head over to `Snowflake documentation <https://docs.snowflake.com/en/sql-reference/sql/grant-ownership#optional-parameters>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#outbound_privileges GrantOwnership#outbound_privileges}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(on, dict):
            on = GrantOwnershipOn(**on)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__667093d5b33de68451fd58ff8cf759e543f82a79fa7ca3976ece1e8ac1e0c9e8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument on", value=on, expected_type=type_hints["on"])
            check_type(argname="argument account_role_name", value=account_role_name, expected_type=type_hints["account_role_name"])
            check_type(argname="argument database_role_name", value=database_role_name, expected_type=type_hints["database_role_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument outbound_privileges", value=outbound_privileges, expected_type=type_hints["outbound_privileges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "on": on,
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
        if account_role_name is not None:
            self._values["account_role_name"] = account_role_name
        if database_role_name is not None:
            self._values["database_role_name"] = database_role_name
        if id is not None:
            self._values["id"] = id
        if outbound_privileges is not None:
            self._values["outbound_privileges"] = outbound_privileges

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
    def on(self) -> "GrantOwnershipOn":
        '''on block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#on GrantOwnership#on}
        '''
        result = self._values.get("on")
        assert result is not None, "Required property 'on' is missing"
        return typing.cast("GrantOwnershipOn", result)

    @builtins.property
    def account_role_name(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the account role to which privileges will be granted.

        For more information about this resource, see `docs <./account_role>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#account_role_name GrantOwnership#account_role_name}
        '''
        result = self._values.get("account_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_role_name(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the database role to which privileges will be granted.

        For more information about this resource, see `docs <./database_role>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#database_role_name GrantOwnership#database_role_name}
        '''
        result = self._values.get("database_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#id GrantOwnership#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outbound_privileges(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to remove or transfer all existing outbound privileges on the object when ownership is transferred to a new role.

        Available options are: REVOKE for removing existing privileges and COPY to transfer them with ownership. For more information head over to `Snowflake documentation <https://docs.snowflake.com/en/sql-reference/sql/grant-ownership#optional-parameters>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#outbound_privileges GrantOwnership#outbound_privileges}
        '''
        result = self._values.get("outbound_privileges")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantOwnershipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.grantOwnership.GrantOwnershipOn",
    jsii_struct_bases=[],
    name_mapping={
        "all": "all",
        "future": "future",
        "object_name": "objectName",
        "object_type": "objectType",
    },
)
class GrantOwnershipOn:
    def __init__(
        self,
        *,
        all: typing.Optional[typing.Union["GrantOwnershipOnAll", typing.Dict[builtins.str, typing.Any]]] = None,
        future: typing.Optional[typing.Union["GrantOwnershipOnFuture", typing.Dict[builtins.str, typing.Any]]] = None,
        object_name: typing.Optional[builtins.str] = None,
        object_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param all: all block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#all GrantOwnership#all}
        :param future: future block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#future GrantOwnership#future}
        :param object_name: Specifies the identifier for the object on which you are transferring ownership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#object_name GrantOwnership#object_name}
        :param object_type: Specifies the type of object on which you are transferring ownership. Available values are: AGGREGATION POLICY | ALERT | AUTHENTICATION POLICY | COMPUTE POOL | DATA METRIC FUNCTION | DATABASE | DATABASE ROLE | DYNAMIC TABLE | EVENT TABLE | EXTERNAL TABLE | EXTERNAL VOLUME | FAILOVER GROUP | FILE FORMAT | FUNCTION | GIT REPOSITORY | HYBRID TABLE | ICEBERG TABLE | IMAGE REPOSITORY | INTEGRATION | MATERIALIZED VIEW | NETWORK POLICY | NETWORK RULE | PACKAGES POLICY | PIPE | PROCEDURE | MASKING POLICY | PASSWORD POLICY | PROJECTION POLICY | REPLICATION GROUP | RESOURCE MONITOR | ROLE | ROW ACCESS POLICY | SCHEMA | SESSION POLICY | SECRET | SEQUENCE | STAGE | STREAM | TABLE | TAG | TASK | USER | VIEW | WAREHOUSE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#object_type GrantOwnership#object_type}
        '''
        if isinstance(all, dict):
            all = GrantOwnershipOnAll(**all)
        if isinstance(future, dict):
            future = GrantOwnershipOnFuture(**future)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0fbecc29e9e21b15966513fecaa9cdfc75982a27bfc8bce40cd174ef08a268f)
            check_type(argname="argument all", value=all, expected_type=type_hints["all"])
            check_type(argname="argument future", value=future, expected_type=type_hints["future"])
            check_type(argname="argument object_name", value=object_name, expected_type=type_hints["object_name"])
            check_type(argname="argument object_type", value=object_type, expected_type=type_hints["object_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all is not None:
            self._values["all"] = all
        if future is not None:
            self._values["future"] = future
        if object_name is not None:
            self._values["object_name"] = object_name
        if object_type is not None:
            self._values["object_type"] = object_type

    @builtins.property
    def all(self) -> typing.Optional["GrantOwnershipOnAll"]:
        '''all block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#all GrantOwnership#all}
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional["GrantOwnershipOnAll"], result)

    @builtins.property
    def future(self) -> typing.Optional["GrantOwnershipOnFuture"]:
        '''future block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#future GrantOwnership#future}
        '''
        result = self._values.get("future")
        return typing.cast(typing.Optional["GrantOwnershipOnFuture"], result)

    @builtins.property
    def object_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the identifier for the object on which you are transferring ownership.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#object_name GrantOwnership#object_name}
        '''
        result = self._values.get("object_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of object on which you are transferring ownership.

        Available values are: AGGREGATION POLICY | ALERT | AUTHENTICATION POLICY | COMPUTE POOL | DATA METRIC FUNCTION | DATABASE | DATABASE ROLE | DYNAMIC TABLE | EVENT TABLE | EXTERNAL TABLE | EXTERNAL VOLUME | FAILOVER GROUP | FILE FORMAT | FUNCTION | GIT REPOSITORY | HYBRID TABLE | ICEBERG TABLE | IMAGE REPOSITORY | INTEGRATION | MATERIALIZED VIEW | NETWORK POLICY | NETWORK RULE | PACKAGES POLICY | PIPE | PROCEDURE | MASKING POLICY | PASSWORD POLICY | PROJECTION POLICY | REPLICATION GROUP | RESOURCE MONITOR | ROLE | ROW ACCESS POLICY | SCHEMA | SESSION POLICY | SECRET | SEQUENCE | STAGE | STREAM | TABLE | TAG | TASK | USER | VIEW | WAREHOUSE

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#object_type GrantOwnership#object_type}
        '''
        result = self._values.get("object_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantOwnershipOn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.grantOwnership.GrantOwnershipOnAll",
    jsii_struct_bases=[],
    name_mapping={
        "object_type_plural": "objectTypePlural",
        "in_database": "inDatabase",
        "in_schema": "inSchema",
    },
)
class GrantOwnershipOnAll:
    def __init__(
        self,
        *,
        object_type_plural: builtins.str,
        in_database: typing.Optional[builtins.str] = None,
        in_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_type_plural: Specifies the type of object in plural form on which you are transferring ownership. Available values are: AGGREGATION POLICIES | ALERTS | AUTHENTICATION POLICIES | COMPUTE POOLS | DATA METRIC FUNCTIONS | DATABASES | DATABASE ROLES | DYNAMIC TABLES | EVENT TABLES | EXTERNAL TABLES | EXTERNAL VOLUMES | FAILOVER GROUPS | FILE FORMATS | FUNCTIONS | GIT REPOSITORIES | HYBRID TABLES | ICEBERG TABLES | IMAGE REPOSITORIES | INTEGRATIONS | MATERIALIZED VIEWS | NETWORK POLICIES | NETWORK RULES | PACKAGES POLICIES | PIPES | PROCEDURES | MASKING POLICIES | PASSWORD POLICIES | PROJECTION POLICIES | REPLICATION GROUPS | RESOURCE MONITORS | ROLES | ROW ACCESS POLICIES | SCHEMAS | SESSION POLICIES | SECRETS | SEQUENCES | STAGES | STREAMS | TABLES | TAGS | TASKS | USERS | VIEWS | WAREHOUSES. For more information head over to `Snowflake documentation <https://docs.snowflake.com/en/sql-reference/sql/grant-ownership#required-parameters>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#object_type_plural GrantOwnership#object_type_plural}
        :param in_database: The fully qualified name of the database. For more information about this resource, see `docs <./database>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#in_database GrantOwnership#in_database}
        :param in_schema: The fully qualified name of the schema. For more information about this resource, see `docs <./schema>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#in_schema GrantOwnership#in_schema}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d36ca1dab57427ba36b98fcde8887523198fdc63ac285737909cd3739c90ab5e)
            check_type(argname="argument object_type_plural", value=object_type_plural, expected_type=type_hints["object_type_plural"])
            check_type(argname="argument in_database", value=in_database, expected_type=type_hints["in_database"])
            check_type(argname="argument in_schema", value=in_schema, expected_type=type_hints["in_schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_type_plural": object_type_plural,
        }
        if in_database is not None:
            self._values["in_database"] = in_database
        if in_schema is not None:
            self._values["in_schema"] = in_schema

    @builtins.property
    def object_type_plural(self) -> builtins.str:
        '''Specifies the type of object in plural form on which you are transferring ownership.

        Available values are: AGGREGATION POLICIES | ALERTS | AUTHENTICATION POLICIES | COMPUTE POOLS | DATA METRIC FUNCTIONS | DATABASES | DATABASE ROLES | DYNAMIC TABLES | EVENT TABLES | EXTERNAL TABLES | EXTERNAL VOLUMES | FAILOVER GROUPS | FILE FORMATS | FUNCTIONS | GIT REPOSITORIES | HYBRID TABLES | ICEBERG TABLES | IMAGE REPOSITORIES | INTEGRATIONS | MATERIALIZED VIEWS | NETWORK POLICIES | NETWORK RULES | PACKAGES POLICIES | PIPES | PROCEDURES | MASKING POLICIES | PASSWORD POLICIES | PROJECTION POLICIES | REPLICATION GROUPS | RESOURCE MONITORS | ROLES | ROW ACCESS POLICIES | SCHEMAS | SESSION POLICIES | SECRETS | SEQUENCES | STAGES | STREAMS | TABLES | TAGS | TASKS | USERS | VIEWS | WAREHOUSES. For more information head over to `Snowflake documentation <https://docs.snowflake.com/en/sql-reference/sql/grant-ownership#required-parameters>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#object_type_plural GrantOwnership#object_type_plural}
        '''
        result = self._values.get("object_type_plural")
        assert result is not None, "Required property 'object_type_plural' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def in_database(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the database. For more information about this resource, see `docs <./database>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#in_database GrantOwnership#in_database}
        '''
        result = self._values.get("in_database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def in_schema(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the schema. For more information about this resource, see `docs <./schema>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#in_schema GrantOwnership#in_schema}
        '''
        result = self._values.get("in_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantOwnershipOnAll(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GrantOwnershipOnAllOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.grantOwnership.GrantOwnershipOnAllOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d63da4509551cd9d45ddf47ef7d1b8580e0852b8eca7e90926fbde46eb462a74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInDatabase")
    def reset_in_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInDatabase", []))

    @jsii.member(jsii_name="resetInSchema")
    def reset_in_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInSchema", []))

    @builtins.property
    @jsii.member(jsii_name="inDatabaseInput")
    def in_database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inDatabaseInput"))

    @builtins.property
    @jsii.member(jsii_name="inSchemaInput")
    def in_schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="objectTypePluralInput")
    def object_type_plural_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectTypePluralInput"))

    @builtins.property
    @jsii.member(jsii_name="inDatabase")
    def in_database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inDatabase"))

    @in_database.setter
    def in_database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ea4101718529c25a4405420b9dd083c97a41fc6ebdd43e328028454aeedb98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inDatabase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inSchema")
    def in_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inSchema"))

    @in_schema.setter
    def in_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93aba394a142085339010c07859edcd79ca4afde363b2da62acd841c9ca9d647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectTypePlural")
    def object_type_plural(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectTypePlural"))

    @object_type_plural.setter
    def object_type_plural(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d002890fb731660a25d772f60be903a98504c76ebf761dbd23ab230d07810b8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectTypePlural", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GrantOwnershipOnAll]:
        return typing.cast(typing.Optional[GrantOwnershipOnAll], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GrantOwnershipOnAll]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0a4ca3127aba5279710fc780cc677de6482df2d54c7ba7084b8f0f11534da9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.grantOwnership.GrantOwnershipOnFuture",
    jsii_struct_bases=[],
    name_mapping={
        "object_type_plural": "objectTypePlural",
        "in_database": "inDatabase",
        "in_schema": "inSchema",
    },
)
class GrantOwnershipOnFuture:
    def __init__(
        self,
        *,
        object_type_plural: builtins.str,
        in_database: typing.Optional[builtins.str] = None,
        in_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_type_plural: Specifies the type of object in plural form on which you are transferring ownership. Available values are: AGGREGATION POLICIES | ALERTS | AUTHENTICATION POLICIES | COMPUTE POOLS | DATA METRIC FUNCTIONS | DATABASES | DATABASE ROLES | DYNAMIC TABLES | EVENT TABLES | EXTERNAL TABLES | EXTERNAL VOLUMES | FAILOVER GROUPS | FILE FORMATS | FUNCTIONS | GIT REPOSITORIES | HYBRID TABLES | ICEBERG TABLES | IMAGE REPOSITORIES | INTEGRATIONS | MATERIALIZED VIEWS | NETWORK POLICIES | NETWORK RULES | PACKAGES POLICIES | PIPES | PROCEDURES | MASKING POLICIES | PASSWORD POLICIES | PROJECTION POLICIES | REPLICATION GROUPS | RESOURCE MONITORS | ROLES | ROW ACCESS POLICIES | SCHEMAS | SESSION POLICIES | SECRETS | SEQUENCES | STAGES | STREAMS | TABLES | TAGS | TASKS | USERS | VIEWS | WAREHOUSES. For more information head over to `Snowflake documentation <https://docs.snowflake.com/en/sql-reference/sql/grant-ownership#required-parameters>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#object_type_plural GrantOwnership#object_type_plural}
        :param in_database: The fully qualified name of the database. For more information about this resource, see `docs <./database>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#in_database GrantOwnership#in_database}
        :param in_schema: The fully qualified name of the schema. For more information about this resource, see `docs <./schema>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#in_schema GrantOwnership#in_schema}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93dc2a3d46c8de683b44434565a5523d62d97c0d4d14cea6e54cec2ffff5995c)
            check_type(argname="argument object_type_plural", value=object_type_plural, expected_type=type_hints["object_type_plural"])
            check_type(argname="argument in_database", value=in_database, expected_type=type_hints["in_database"])
            check_type(argname="argument in_schema", value=in_schema, expected_type=type_hints["in_schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_type_plural": object_type_plural,
        }
        if in_database is not None:
            self._values["in_database"] = in_database
        if in_schema is not None:
            self._values["in_schema"] = in_schema

    @builtins.property
    def object_type_plural(self) -> builtins.str:
        '''Specifies the type of object in plural form on which you are transferring ownership.

        Available values are: AGGREGATION POLICIES | ALERTS | AUTHENTICATION POLICIES | COMPUTE POOLS | DATA METRIC FUNCTIONS | DATABASES | DATABASE ROLES | DYNAMIC TABLES | EVENT TABLES | EXTERNAL TABLES | EXTERNAL VOLUMES | FAILOVER GROUPS | FILE FORMATS | FUNCTIONS | GIT REPOSITORIES | HYBRID TABLES | ICEBERG TABLES | IMAGE REPOSITORIES | INTEGRATIONS | MATERIALIZED VIEWS | NETWORK POLICIES | NETWORK RULES | PACKAGES POLICIES | PIPES | PROCEDURES | MASKING POLICIES | PASSWORD POLICIES | PROJECTION POLICIES | REPLICATION GROUPS | RESOURCE MONITORS | ROLES | ROW ACCESS POLICIES | SCHEMAS | SESSION POLICIES | SECRETS | SEQUENCES | STAGES | STREAMS | TABLES | TAGS | TASKS | USERS | VIEWS | WAREHOUSES. For more information head over to `Snowflake documentation <https://docs.snowflake.com/en/sql-reference/sql/grant-ownership#required-parameters>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#object_type_plural GrantOwnership#object_type_plural}
        '''
        result = self._values.get("object_type_plural")
        assert result is not None, "Required property 'object_type_plural' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def in_database(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the database. For more information about this resource, see `docs <./database>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#in_database GrantOwnership#in_database}
        '''
        result = self._values.get("in_database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def in_schema(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the schema. For more information about this resource, see `docs <./schema>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#in_schema GrantOwnership#in_schema}
        '''
        result = self._values.get("in_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantOwnershipOnFuture(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GrantOwnershipOnFutureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.grantOwnership.GrantOwnershipOnFutureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a3058afe466e7ff3a5c7e143d7cb4fe38811b3e35e91e6961ffabba768f5a67)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInDatabase")
    def reset_in_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInDatabase", []))

    @jsii.member(jsii_name="resetInSchema")
    def reset_in_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInSchema", []))

    @builtins.property
    @jsii.member(jsii_name="inDatabaseInput")
    def in_database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inDatabaseInput"))

    @builtins.property
    @jsii.member(jsii_name="inSchemaInput")
    def in_schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="objectTypePluralInput")
    def object_type_plural_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectTypePluralInput"))

    @builtins.property
    @jsii.member(jsii_name="inDatabase")
    def in_database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inDatabase"))

    @in_database.setter
    def in_database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32bf940fd8d36392f857b1f56f5cb2b5c9def81dc6a9ee4a77a2f1f06d2a4bb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inDatabase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inSchema")
    def in_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inSchema"))

    @in_schema.setter
    def in_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd1307a959ff589cd07e93e0bd6102ba89304a60a6903c6672884e78bfdf6cde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectTypePlural")
    def object_type_plural(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectTypePlural"))

    @object_type_plural.setter
    def object_type_plural(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea01cb225edcfef3583b4deb8b5a6dfbbf3ffffdcb9612c60207a3f2beb8c04e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectTypePlural", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GrantOwnershipOnFuture]:
        return typing.cast(typing.Optional[GrantOwnershipOnFuture], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GrantOwnershipOnFuture]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3ab17274fa9732e8e9f0c384c59d89d2c2027cbeb6c3c2f055a452ef929313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GrantOwnershipOnOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.grantOwnership.GrantOwnershipOnOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3042e02f19a6d8207aa702fef3643b5975475ac1749466611a283e48985cdf28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAll")
    def put_all(
        self,
        *,
        object_type_plural: builtins.str,
        in_database: typing.Optional[builtins.str] = None,
        in_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_type_plural: Specifies the type of object in plural form on which you are transferring ownership. Available values are: AGGREGATION POLICIES | ALERTS | AUTHENTICATION POLICIES | COMPUTE POOLS | DATA METRIC FUNCTIONS | DATABASES | DATABASE ROLES | DYNAMIC TABLES | EVENT TABLES | EXTERNAL TABLES | EXTERNAL VOLUMES | FAILOVER GROUPS | FILE FORMATS | FUNCTIONS | GIT REPOSITORIES | HYBRID TABLES | ICEBERG TABLES | IMAGE REPOSITORIES | INTEGRATIONS | MATERIALIZED VIEWS | NETWORK POLICIES | NETWORK RULES | PACKAGES POLICIES | PIPES | PROCEDURES | MASKING POLICIES | PASSWORD POLICIES | PROJECTION POLICIES | REPLICATION GROUPS | RESOURCE MONITORS | ROLES | ROW ACCESS POLICIES | SCHEMAS | SESSION POLICIES | SECRETS | SEQUENCES | STAGES | STREAMS | TABLES | TAGS | TASKS | USERS | VIEWS | WAREHOUSES. For more information head over to `Snowflake documentation <https://docs.snowflake.com/en/sql-reference/sql/grant-ownership#required-parameters>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#object_type_plural GrantOwnership#object_type_plural}
        :param in_database: The fully qualified name of the database. For more information about this resource, see `docs <./database>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#in_database GrantOwnership#in_database}
        :param in_schema: The fully qualified name of the schema. For more information about this resource, see `docs <./schema>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#in_schema GrantOwnership#in_schema}
        '''
        value = GrantOwnershipOnAll(
            object_type_plural=object_type_plural,
            in_database=in_database,
            in_schema=in_schema,
        )

        return typing.cast(None, jsii.invoke(self, "putAll", [value]))

    @jsii.member(jsii_name="putFuture")
    def put_future(
        self,
        *,
        object_type_plural: builtins.str,
        in_database: typing.Optional[builtins.str] = None,
        in_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_type_plural: Specifies the type of object in plural form on which you are transferring ownership. Available values are: AGGREGATION POLICIES | ALERTS | AUTHENTICATION POLICIES | COMPUTE POOLS | DATA METRIC FUNCTIONS | DATABASES | DATABASE ROLES | DYNAMIC TABLES | EVENT TABLES | EXTERNAL TABLES | EXTERNAL VOLUMES | FAILOVER GROUPS | FILE FORMATS | FUNCTIONS | GIT REPOSITORIES | HYBRID TABLES | ICEBERG TABLES | IMAGE REPOSITORIES | INTEGRATIONS | MATERIALIZED VIEWS | NETWORK POLICIES | NETWORK RULES | PACKAGES POLICIES | PIPES | PROCEDURES | MASKING POLICIES | PASSWORD POLICIES | PROJECTION POLICIES | REPLICATION GROUPS | RESOURCE MONITORS | ROLES | ROW ACCESS POLICIES | SCHEMAS | SESSION POLICIES | SECRETS | SEQUENCES | STAGES | STREAMS | TABLES | TAGS | TASKS | USERS | VIEWS | WAREHOUSES. For more information head over to `Snowflake documentation <https://docs.snowflake.com/en/sql-reference/sql/grant-ownership#required-parameters>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#object_type_plural GrantOwnership#object_type_plural}
        :param in_database: The fully qualified name of the database. For more information about this resource, see `docs <./database>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#in_database GrantOwnership#in_database}
        :param in_schema: The fully qualified name of the schema. For more information about this resource, see `docs <./schema>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_ownership#in_schema GrantOwnership#in_schema}
        '''
        value = GrantOwnershipOnFuture(
            object_type_plural=object_type_plural,
            in_database=in_database,
            in_schema=in_schema,
        )

        return typing.cast(None, jsii.invoke(self, "putFuture", [value]))

    @jsii.member(jsii_name="resetAll")
    def reset_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAll", []))

    @jsii.member(jsii_name="resetFuture")
    def reset_future(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFuture", []))

    @jsii.member(jsii_name="resetObjectName")
    def reset_object_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectName", []))

    @jsii.member(jsii_name="resetObjectType")
    def reset_object_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectType", []))

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> GrantOwnershipOnAllOutputReference:
        return typing.cast(GrantOwnershipOnAllOutputReference, jsii.get(self, "all"))

    @builtins.property
    @jsii.member(jsii_name="future")
    def future(self) -> GrantOwnershipOnFutureOutputReference:
        return typing.cast(GrantOwnershipOnFutureOutputReference, jsii.get(self, "future"))

    @builtins.property
    @jsii.member(jsii_name="allInput")
    def all_input(self) -> typing.Optional[GrantOwnershipOnAll]:
        return typing.cast(typing.Optional[GrantOwnershipOnAll], jsii.get(self, "allInput"))

    @builtins.property
    @jsii.member(jsii_name="futureInput")
    def future_input(self) -> typing.Optional[GrantOwnershipOnFuture]:
        return typing.cast(typing.Optional[GrantOwnershipOnFuture], jsii.get(self, "futureInput"))

    @builtins.property
    @jsii.member(jsii_name="objectNameInput")
    def object_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectNameInput"))

    @builtins.property
    @jsii.member(jsii_name="objectTypeInput")
    def object_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="objectName")
    def object_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectName"))

    @object_name.setter
    def object_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e74ef1483ac218207a420819b77865797eb5a6cb579a5d0f68965e74a060f26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectType")
    def object_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectType"))

    @object_type.setter
    def object_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0e2bfaaa6f27de1aedfff2bbd1208d48516dc70567de38d8498a12150c0b49e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GrantOwnershipOn]:
        return typing.cast(typing.Optional[GrantOwnershipOn], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GrantOwnershipOn]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90dc67081395c7710c27160f282489c5fff8f0832059bf543acdf99556445840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GrantOwnership",
    "GrantOwnershipConfig",
    "GrantOwnershipOn",
    "GrantOwnershipOnAll",
    "GrantOwnershipOnAllOutputReference",
    "GrantOwnershipOnFuture",
    "GrantOwnershipOnFutureOutputReference",
    "GrantOwnershipOnOutputReference",
]

publication.publish()

def _typecheckingstub__ee66262eb9f353f7b7e21182c2d9fafa5357724c9eec0b975187d44e464d1178(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    on: typing.Union[GrantOwnershipOn, typing.Dict[builtins.str, typing.Any]],
    account_role_name: typing.Optional[builtins.str] = None,
    database_role_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    outbound_privileges: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__9ccf76e393878d437bb69a260a440eb8591804cf93402c0391218fea2ee88327(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25fba6a608695977b563127328451b3508d84c54f6662843c90bccec596a818b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889e17549d799029598a9a5130a183de49749427975ad12f19901fa5d9f331d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3049eb80d0f400312ab0ac8a7c935d43b97ad96a23f675d6a8da8b8f72eb75c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f39247fce9a4e9ee1072b7b973eb6d65011fdeb96aa662174aa1e0d6ff4f63c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667093d5b33de68451fd58ff8cf759e543f82a79fa7ca3976ece1e8ac1e0c9e8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    on: typing.Union[GrantOwnershipOn, typing.Dict[builtins.str, typing.Any]],
    account_role_name: typing.Optional[builtins.str] = None,
    database_role_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    outbound_privileges: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0fbecc29e9e21b15966513fecaa9cdfc75982a27bfc8bce40cd174ef08a268f(
    *,
    all: typing.Optional[typing.Union[GrantOwnershipOnAll, typing.Dict[builtins.str, typing.Any]]] = None,
    future: typing.Optional[typing.Union[GrantOwnershipOnFuture, typing.Dict[builtins.str, typing.Any]]] = None,
    object_name: typing.Optional[builtins.str] = None,
    object_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36ca1dab57427ba36b98fcde8887523198fdc63ac285737909cd3739c90ab5e(
    *,
    object_type_plural: builtins.str,
    in_database: typing.Optional[builtins.str] = None,
    in_schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63da4509551cd9d45ddf47ef7d1b8580e0852b8eca7e90926fbde46eb462a74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ea4101718529c25a4405420b9dd083c97a41fc6ebdd43e328028454aeedb98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93aba394a142085339010c07859edcd79ca4afde363b2da62acd841c9ca9d647(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d002890fb731660a25d772f60be903a98504c76ebf761dbd23ab230d07810b8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0a4ca3127aba5279710fc780cc677de6482df2d54c7ba7084b8f0f11534da9(
    value: typing.Optional[GrantOwnershipOnAll],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93dc2a3d46c8de683b44434565a5523d62d97c0d4d14cea6e54cec2ffff5995c(
    *,
    object_type_plural: builtins.str,
    in_database: typing.Optional[builtins.str] = None,
    in_schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3058afe466e7ff3a5c7e143d7cb4fe38811b3e35e91e6961ffabba768f5a67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32bf940fd8d36392f857b1f56f5cb2b5c9def81dc6a9ee4a77a2f1f06d2a4bb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1307a959ff589cd07e93e0bd6102ba89304a60a6903c6672884e78bfdf6cde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea01cb225edcfef3583b4deb8b5a6dfbbf3ffffdcb9612c60207a3f2beb8c04e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3ab17274fa9732e8e9f0c384c59d89d2c2027cbeb6c3c2f055a452ef929313(
    value: typing.Optional[GrantOwnershipOnFuture],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3042e02f19a6d8207aa702fef3643b5975475ac1749466611a283e48985cdf28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e74ef1483ac218207a420819b77865797eb5a6cb579a5d0f68965e74a060f26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e2bfaaa6f27de1aedfff2bbd1208d48516dc70567de38d8498a12150c0b49e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90dc67081395c7710c27160f282489c5fff8f0832059bf543acdf99556445840(
    value: typing.Optional[GrantOwnershipOn],
) -> None:
    """Type checking stubs"""
    pass
