r'''
# `snowflake_grant_privileges_to_database_role`

Refer to the Terraform Registry for docs: [`snowflake_grant_privileges_to_database_role`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role).
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


class GrantPrivilegesToDatabaseRole(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToDatabaseRole.GrantPrivilegesToDatabaseRole",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role snowflake_grant_privileges_to_database_role}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database_role_name: builtins.str,
        all_privileges: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        always_apply: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        always_apply_trigger: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        on_database: typing.Optional[builtins.str] = None,
        on_schema: typing.Optional[typing.Union["GrantPrivilegesToDatabaseRoleOnSchema", typing.Dict[builtins.str, typing.Any]]] = None,
        on_schema_object: typing.Optional[typing.Union["GrantPrivilegesToDatabaseRoleOnSchemaObject", typing.Dict[builtins.str, typing.Any]]] = None,
        privileges: typing.Optional[typing.Sequence[builtins.str]] = None,
        with_grant_option: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role snowflake_grant_privileges_to_database_role} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database_role_name: The fully qualified name of the database role to which privileges will be granted. For more information about this resource, see `docs <./database_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#database_role_name GrantPrivilegesToDatabaseRole#database_role_name}
        :param all_privileges: Grant all privileges on the database role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#all_privileges GrantPrivilegesToDatabaseRole#all_privileges}
        :param always_apply: If true, the resource will always produce a “plan” and on “apply” it will re-grant defined privileges. It is supposed to be used only in “grant privileges on all X’s in database / schema Y” or “grant all privileges to X” scenarios to make sure that every new object in a given database / schema is granted by the account role and every new privilege is granted to the database role. Important note: this flag is not compliant with the Terraform assumptions of the config being eventually convergent (producing an empty plan). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#always_apply GrantPrivilegesToDatabaseRole#always_apply}
        :param always_apply_trigger: This is a helper field and should not be set. Its main purpose is to help to achieve the functionality described by the always_apply field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#always_apply_trigger GrantPrivilegesToDatabaseRole#always_apply_trigger}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#id GrantPrivilegesToDatabaseRole#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param on_database: The fully qualified name of the database on which privileges will be granted. For more information about this resource, see `docs <./database>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#on_database GrantPrivilegesToDatabaseRole#on_database}
        :param on_schema: on_schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#on_schema GrantPrivilegesToDatabaseRole#on_schema}
        :param on_schema_object: on_schema_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#on_schema_object GrantPrivilegesToDatabaseRole#on_schema_object}
        :param privileges: The privileges to grant on the database role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#privileges GrantPrivilegesToDatabaseRole#privileges}
        :param with_grant_option: If specified, allows the recipient role to grant the privileges to other roles. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#with_grant_option GrantPrivilegesToDatabaseRole#with_grant_option}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02d7ad43ea8f91f0d10978caf4a9250c54b3ca7c7d61ea040d3ac99e454cab0c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GrantPrivilegesToDatabaseRoleConfig(
            database_role_name=database_role_name,
            all_privileges=all_privileges,
            always_apply=always_apply,
            always_apply_trigger=always_apply_trigger,
            id=id,
            on_database=on_database,
            on_schema=on_schema,
            on_schema_object=on_schema_object,
            privileges=privileges,
            with_grant_option=with_grant_option,
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
        '''Generates CDKTF code for importing a GrantPrivilegesToDatabaseRole resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GrantPrivilegesToDatabaseRole to import.
        :param import_from_id: The id of the existing GrantPrivilegesToDatabaseRole that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GrantPrivilegesToDatabaseRole to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22217f71b53ff727e01696aa73e681840cc9da7abb1e86427909fdbac1b15396)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putOnSchema")
    def put_on_schema(
        self,
        *,
        all_schemas_in_database: typing.Optional[builtins.str] = None,
        future_schemas_in_database: typing.Optional[builtins.str] = None,
        schema_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param all_schemas_in_database: The fully qualified name of the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#all_schemas_in_database GrantPrivilegesToDatabaseRole#all_schemas_in_database}
        :param future_schemas_in_database: The fully qualified name of the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#future_schemas_in_database GrantPrivilegesToDatabaseRole#future_schemas_in_database}
        :param schema_name: The fully qualified name of the schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#schema_name GrantPrivilegesToDatabaseRole#schema_name}
        '''
        value = GrantPrivilegesToDatabaseRoleOnSchema(
            all_schemas_in_database=all_schemas_in_database,
            future_schemas_in_database=future_schemas_in_database,
            schema_name=schema_name,
        )

        return typing.cast(None, jsii.invoke(self, "putOnSchema", [value]))

    @jsii.member(jsii_name="putOnSchemaObject")
    def put_on_schema_object(
        self,
        *,
        all: typing.Optional[typing.Union["GrantPrivilegesToDatabaseRoleOnSchemaObjectAll", typing.Dict[builtins.str, typing.Any]]] = None,
        future: typing.Optional[typing.Union["GrantPrivilegesToDatabaseRoleOnSchemaObjectFuture", typing.Dict[builtins.str, typing.Any]]] = None,
        object_name: typing.Optional[builtins.str] = None,
        object_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param all: all block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#all GrantPrivilegesToDatabaseRole#all}
        :param future: future block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#future GrantPrivilegesToDatabaseRole#future}
        :param object_name: The fully qualified name of the object on which privileges will be granted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#object_name GrantPrivilegesToDatabaseRole#object_name}
        :param object_type: The object type of the schema object on which privileges will be granted. Valid values are: AGGREGATION POLICY | ALERT | AUTHENTICATION POLICY | CORTEX SEARCH SERVICE | DATA METRIC FUNCTION | DYNAMIC TABLE | EVENT TABLE | EXTERNAL TABLE | FILE FORMAT | FUNCTION | GIT REPOSITORY | HYBRID TABLE | IMAGE REPOSITORY | ICEBERG TABLE | MASKING POLICY | MATERIALIZED VIEW | MODEL | NETWORK RULE | NOTEBOOK | PACKAGES POLICY | PASSWORD POLICY | PIPE | PROCEDURE | PROJECTION POLICY | ROW ACCESS POLICY | SECRET | SERVICE | SESSION POLICY | SEQUENCE | SNAPSHOT | STAGE | STREAM | TABLE | TAG | TASK | VIEW | STREAMLIT | DATASET Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#object_type GrantPrivilegesToDatabaseRole#object_type}
        '''
        value = GrantPrivilegesToDatabaseRoleOnSchemaObject(
            all=all, future=future, object_name=object_name, object_type=object_type
        )

        return typing.cast(None, jsii.invoke(self, "putOnSchemaObject", [value]))

    @jsii.member(jsii_name="resetAllPrivileges")
    def reset_all_privileges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllPrivileges", []))

    @jsii.member(jsii_name="resetAlwaysApply")
    def reset_always_apply(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlwaysApply", []))

    @jsii.member(jsii_name="resetAlwaysApplyTrigger")
    def reset_always_apply_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlwaysApplyTrigger", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOnDatabase")
    def reset_on_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnDatabase", []))

    @jsii.member(jsii_name="resetOnSchema")
    def reset_on_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnSchema", []))

    @jsii.member(jsii_name="resetOnSchemaObject")
    def reset_on_schema_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnSchemaObject", []))

    @jsii.member(jsii_name="resetPrivileges")
    def reset_privileges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivileges", []))

    @jsii.member(jsii_name="resetWithGrantOption")
    def reset_with_grant_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithGrantOption", []))

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
    @jsii.member(jsii_name="onSchema")
    def on_schema(self) -> "GrantPrivilegesToDatabaseRoleOnSchemaOutputReference":
        return typing.cast("GrantPrivilegesToDatabaseRoleOnSchemaOutputReference", jsii.get(self, "onSchema"))

    @builtins.property
    @jsii.member(jsii_name="onSchemaObject")
    def on_schema_object(
        self,
    ) -> "GrantPrivilegesToDatabaseRoleOnSchemaObjectOutputReference":
        return typing.cast("GrantPrivilegesToDatabaseRoleOnSchemaObjectOutputReference", jsii.get(self, "onSchemaObject"))

    @builtins.property
    @jsii.member(jsii_name="allPrivilegesInput")
    def all_privileges_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allPrivilegesInput"))

    @builtins.property
    @jsii.member(jsii_name="alwaysApplyInput")
    def always_apply_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "alwaysApplyInput"))

    @builtins.property
    @jsii.member(jsii_name="alwaysApplyTriggerInput")
    def always_apply_trigger_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alwaysApplyTriggerInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseRoleNameInput")
    def database_role_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseRoleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="onDatabaseInput")
    def on_database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onDatabaseInput"))

    @builtins.property
    @jsii.member(jsii_name="onSchemaInput")
    def on_schema_input(
        self,
    ) -> typing.Optional["GrantPrivilegesToDatabaseRoleOnSchema"]:
        return typing.cast(typing.Optional["GrantPrivilegesToDatabaseRoleOnSchema"], jsii.get(self, "onSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="onSchemaObjectInput")
    def on_schema_object_input(
        self,
    ) -> typing.Optional["GrantPrivilegesToDatabaseRoleOnSchemaObject"]:
        return typing.cast(typing.Optional["GrantPrivilegesToDatabaseRoleOnSchemaObject"], jsii.get(self, "onSchemaObjectInput"))

    @builtins.property
    @jsii.member(jsii_name="privilegesInput")
    def privileges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "privilegesInput"))

    @builtins.property
    @jsii.member(jsii_name="withGrantOptionInput")
    def with_grant_option_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withGrantOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="allPrivileges")
    def all_privileges(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allPrivileges"))

    @all_privileges.setter
    def all_privileges(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06657da865051e79467d93ff025a73a0dec63b038ffd421303960324e1cd21e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allPrivileges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alwaysApply")
    def always_apply(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "alwaysApply"))

    @always_apply.setter
    def always_apply(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663e44b835f6ee3a2a5e66203448f0b1fd553048d60c146fd7bca8c962642fe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alwaysApply", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alwaysApplyTrigger")
    def always_apply_trigger(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alwaysApplyTrigger"))

    @always_apply_trigger.setter
    def always_apply_trigger(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9406fc9e16dca18d81093d9dc61c2729de3c9a33badbc0493709a42f9adb4088)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alwaysApplyTrigger", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseRoleName")
    def database_role_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseRoleName"))

    @database_role_name.setter
    def database_role_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edaada8cd2f15dc8e669cdac70298254d701cedfd9d360d77cf127d00410cbfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseRoleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cab57df862a8b450e58dbea75b1d61929eb7991db9d55f786c4a19c59d8b06a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onDatabase")
    def on_database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onDatabase"))

    @on_database.setter
    def on_database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7452b3d3071e10972d5a815bd386d7bfc3376b576bb0596cdfbbfb454c1470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onDatabase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privileges")
    def privileges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "privileges"))

    @privileges.setter
    def privileges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69cec71a3d146dd6c919a83e6b045906aa7bcfd274fa4b3c57a247d46d63b97e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privileges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withGrantOption")
    def with_grant_option(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "withGrantOption"))

    @with_grant_option.setter
    def with_grant_option(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83794808274aa5d5076aedec292e7e84b2816e34bff0f4728359e1d9716bdc98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withGrantOption", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToDatabaseRole.GrantPrivilegesToDatabaseRoleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "database_role_name": "databaseRoleName",
        "all_privileges": "allPrivileges",
        "always_apply": "alwaysApply",
        "always_apply_trigger": "alwaysApplyTrigger",
        "id": "id",
        "on_database": "onDatabase",
        "on_schema": "onSchema",
        "on_schema_object": "onSchemaObject",
        "privileges": "privileges",
        "with_grant_option": "withGrantOption",
    },
)
class GrantPrivilegesToDatabaseRoleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        database_role_name: builtins.str,
        all_privileges: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        always_apply: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        always_apply_trigger: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        on_database: typing.Optional[builtins.str] = None,
        on_schema: typing.Optional[typing.Union["GrantPrivilegesToDatabaseRoleOnSchema", typing.Dict[builtins.str, typing.Any]]] = None,
        on_schema_object: typing.Optional[typing.Union["GrantPrivilegesToDatabaseRoleOnSchemaObject", typing.Dict[builtins.str, typing.Any]]] = None,
        privileges: typing.Optional[typing.Sequence[builtins.str]] = None,
        with_grant_option: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param database_role_name: The fully qualified name of the database role to which privileges will be granted. For more information about this resource, see `docs <./database_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#database_role_name GrantPrivilegesToDatabaseRole#database_role_name}
        :param all_privileges: Grant all privileges on the database role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#all_privileges GrantPrivilegesToDatabaseRole#all_privileges}
        :param always_apply: If true, the resource will always produce a “plan” and on “apply” it will re-grant defined privileges. It is supposed to be used only in “grant privileges on all X’s in database / schema Y” or “grant all privileges to X” scenarios to make sure that every new object in a given database / schema is granted by the account role and every new privilege is granted to the database role. Important note: this flag is not compliant with the Terraform assumptions of the config being eventually convergent (producing an empty plan). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#always_apply GrantPrivilegesToDatabaseRole#always_apply}
        :param always_apply_trigger: This is a helper field and should not be set. Its main purpose is to help to achieve the functionality described by the always_apply field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#always_apply_trigger GrantPrivilegesToDatabaseRole#always_apply_trigger}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#id GrantPrivilegesToDatabaseRole#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param on_database: The fully qualified name of the database on which privileges will be granted. For more information about this resource, see `docs <./database>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#on_database GrantPrivilegesToDatabaseRole#on_database}
        :param on_schema: on_schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#on_schema GrantPrivilegesToDatabaseRole#on_schema}
        :param on_schema_object: on_schema_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#on_schema_object GrantPrivilegesToDatabaseRole#on_schema_object}
        :param privileges: The privileges to grant on the database role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#privileges GrantPrivilegesToDatabaseRole#privileges}
        :param with_grant_option: If specified, allows the recipient role to grant the privileges to other roles. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#with_grant_option GrantPrivilegesToDatabaseRole#with_grant_option}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(on_schema, dict):
            on_schema = GrantPrivilegesToDatabaseRoleOnSchema(**on_schema)
        if isinstance(on_schema_object, dict):
            on_schema_object = GrantPrivilegesToDatabaseRoleOnSchemaObject(**on_schema_object)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45d6b8de65d8dc580a3c825b8df5fae6970b8ac80df6abcac8e16480969f441)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument database_role_name", value=database_role_name, expected_type=type_hints["database_role_name"])
            check_type(argname="argument all_privileges", value=all_privileges, expected_type=type_hints["all_privileges"])
            check_type(argname="argument always_apply", value=always_apply, expected_type=type_hints["always_apply"])
            check_type(argname="argument always_apply_trigger", value=always_apply_trigger, expected_type=type_hints["always_apply_trigger"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument on_database", value=on_database, expected_type=type_hints["on_database"])
            check_type(argname="argument on_schema", value=on_schema, expected_type=type_hints["on_schema"])
            check_type(argname="argument on_schema_object", value=on_schema_object, expected_type=type_hints["on_schema_object"])
            check_type(argname="argument privileges", value=privileges, expected_type=type_hints["privileges"])
            check_type(argname="argument with_grant_option", value=with_grant_option, expected_type=type_hints["with_grant_option"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_role_name": database_role_name,
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
        if all_privileges is not None:
            self._values["all_privileges"] = all_privileges
        if always_apply is not None:
            self._values["always_apply"] = always_apply
        if always_apply_trigger is not None:
            self._values["always_apply_trigger"] = always_apply_trigger
        if id is not None:
            self._values["id"] = id
        if on_database is not None:
            self._values["on_database"] = on_database
        if on_schema is not None:
            self._values["on_schema"] = on_schema
        if on_schema_object is not None:
            self._values["on_schema_object"] = on_schema_object
        if privileges is not None:
            self._values["privileges"] = privileges
        if with_grant_option is not None:
            self._values["with_grant_option"] = with_grant_option

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
    def database_role_name(self) -> builtins.str:
        '''The fully qualified name of the database role to which privileges will be granted.

        For more information about this resource, see `docs <./database_role>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#database_role_name GrantPrivilegesToDatabaseRole#database_role_name}
        '''
        result = self._values.get("database_role_name")
        assert result is not None, "Required property 'database_role_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def all_privileges(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Grant all privileges on the database role.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#all_privileges GrantPrivilegesToDatabaseRole#all_privileges}
        '''
        result = self._values.get("all_privileges")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def always_apply(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the resource will always produce a “plan” and on “apply” it will re-grant defined privileges.

        It is supposed to be used only in “grant privileges on all X’s in database / schema Y” or “grant all privileges to X” scenarios to make sure that every new object in a given database / schema is granted by the account role and every new privilege is granted to the database role. Important note: this flag is not compliant with the Terraform assumptions of the config being eventually convergent (producing an empty plan).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#always_apply GrantPrivilegesToDatabaseRole#always_apply}
        '''
        result = self._values.get("always_apply")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def always_apply_trigger(self) -> typing.Optional[builtins.str]:
        '''This is a helper field and should not be set.

        Its main purpose is to help to achieve the functionality described by the always_apply field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#always_apply_trigger GrantPrivilegesToDatabaseRole#always_apply_trigger}
        '''
        result = self._values.get("always_apply_trigger")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#id GrantPrivilegesToDatabaseRole#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_database(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the database on which privileges will be granted.

        For more information about this resource, see `docs <./database>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#on_database GrantPrivilegesToDatabaseRole#on_database}
        '''
        result = self._values.get("on_database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_schema(self) -> typing.Optional["GrantPrivilegesToDatabaseRoleOnSchema"]:
        '''on_schema block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#on_schema GrantPrivilegesToDatabaseRole#on_schema}
        '''
        result = self._values.get("on_schema")
        return typing.cast(typing.Optional["GrantPrivilegesToDatabaseRoleOnSchema"], result)

    @builtins.property
    def on_schema_object(
        self,
    ) -> typing.Optional["GrantPrivilegesToDatabaseRoleOnSchemaObject"]:
        '''on_schema_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#on_schema_object GrantPrivilegesToDatabaseRole#on_schema_object}
        '''
        result = self._values.get("on_schema_object")
        return typing.cast(typing.Optional["GrantPrivilegesToDatabaseRoleOnSchemaObject"], result)

    @builtins.property
    def privileges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The privileges to grant on the database role.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#privileges GrantPrivilegesToDatabaseRole#privileges}
        '''
        result = self._values.get("privileges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def with_grant_option(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If specified, allows the recipient role to grant the privileges to other roles.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#with_grant_option GrantPrivilegesToDatabaseRole#with_grant_option}
        '''
        result = self._values.get("with_grant_option")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantPrivilegesToDatabaseRoleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToDatabaseRole.GrantPrivilegesToDatabaseRoleOnSchema",
    jsii_struct_bases=[],
    name_mapping={
        "all_schemas_in_database": "allSchemasInDatabase",
        "future_schemas_in_database": "futureSchemasInDatabase",
        "schema_name": "schemaName",
    },
)
class GrantPrivilegesToDatabaseRoleOnSchema:
    def __init__(
        self,
        *,
        all_schemas_in_database: typing.Optional[builtins.str] = None,
        future_schemas_in_database: typing.Optional[builtins.str] = None,
        schema_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param all_schemas_in_database: The fully qualified name of the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#all_schemas_in_database GrantPrivilegesToDatabaseRole#all_schemas_in_database}
        :param future_schemas_in_database: The fully qualified name of the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#future_schemas_in_database GrantPrivilegesToDatabaseRole#future_schemas_in_database}
        :param schema_name: The fully qualified name of the schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#schema_name GrantPrivilegesToDatabaseRole#schema_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7684c1c67a25a2ababc11d44a0c75b4a0b5ca484112a1abd301af3ae179c3c1d)
            check_type(argname="argument all_schemas_in_database", value=all_schemas_in_database, expected_type=type_hints["all_schemas_in_database"])
            check_type(argname="argument future_schemas_in_database", value=future_schemas_in_database, expected_type=type_hints["future_schemas_in_database"])
            check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all_schemas_in_database is not None:
            self._values["all_schemas_in_database"] = all_schemas_in_database
        if future_schemas_in_database is not None:
            self._values["future_schemas_in_database"] = future_schemas_in_database
        if schema_name is not None:
            self._values["schema_name"] = schema_name

    @builtins.property
    def all_schemas_in_database(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#all_schemas_in_database GrantPrivilegesToDatabaseRole#all_schemas_in_database}
        '''
        result = self._values.get("all_schemas_in_database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def future_schemas_in_database(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#future_schemas_in_database GrantPrivilegesToDatabaseRole#future_schemas_in_database}
        '''
        result = self._values.get("future_schemas_in_database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_name(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the schema.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#schema_name GrantPrivilegesToDatabaseRole#schema_name}
        '''
        result = self._values.get("schema_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantPrivilegesToDatabaseRoleOnSchema(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToDatabaseRole.GrantPrivilegesToDatabaseRoleOnSchemaObject",
    jsii_struct_bases=[],
    name_mapping={
        "all": "all",
        "future": "future",
        "object_name": "objectName",
        "object_type": "objectType",
    },
)
class GrantPrivilegesToDatabaseRoleOnSchemaObject:
    def __init__(
        self,
        *,
        all: typing.Optional[typing.Union["GrantPrivilegesToDatabaseRoleOnSchemaObjectAll", typing.Dict[builtins.str, typing.Any]]] = None,
        future: typing.Optional[typing.Union["GrantPrivilegesToDatabaseRoleOnSchemaObjectFuture", typing.Dict[builtins.str, typing.Any]]] = None,
        object_name: typing.Optional[builtins.str] = None,
        object_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param all: all block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#all GrantPrivilegesToDatabaseRole#all}
        :param future: future block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#future GrantPrivilegesToDatabaseRole#future}
        :param object_name: The fully qualified name of the object on which privileges will be granted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#object_name GrantPrivilegesToDatabaseRole#object_name}
        :param object_type: The object type of the schema object on which privileges will be granted. Valid values are: AGGREGATION POLICY | ALERT | AUTHENTICATION POLICY | CORTEX SEARCH SERVICE | DATA METRIC FUNCTION | DYNAMIC TABLE | EVENT TABLE | EXTERNAL TABLE | FILE FORMAT | FUNCTION | GIT REPOSITORY | HYBRID TABLE | IMAGE REPOSITORY | ICEBERG TABLE | MASKING POLICY | MATERIALIZED VIEW | MODEL | NETWORK RULE | NOTEBOOK | PACKAGES POLICY | PASSWORD POLICY | PIPE | PROCEDURE | PROJECTION POLICY | ROW ACCESS POLICY | SECRET | SERVICE | SESSION POLICY | SEQUENCE | SNAPSHOT | STAGE | STREAM | TABLE | TAG | TASK | VIEW | STREAMLIT | DATASET Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#object_type GrantPrivilegesToDatabaseRole#object_type}
        '''
        if isinstance(all, dict):
            all = GrantPrivilegesToDatabaseRoleOnSchemaObjectAll(**all)
        if isinstance(future, dict):
            future = GrantPrivilegesToDatabaseRoleOnSchemaObjectFuture(**future)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f49e690505885d5e22fac1142bf0aaa501721e79e37f46bcb6df0638f15e0202)
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
    def all(self) -> typing.Optional["GrantPrivilegesToDatabaseRoleOnSchemaObjectAll"]:
        '''all block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#all GrantPrivilegesToDatabaseRole#all}
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional["GrantPrivilegesToDatabaseRoleOnSchemaObjectAll"], result)

    @builtins.property
    def future(
        self,
    ) -> typing.Optional["GrantPrivilegesToDatabaseRoleOnSchemaObjectFuture"]:
        '''future block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#future GrantPrivilegesToDatabaseRole#future}
        '''
        result = self._values.get("future")
        return typing.cast(typing.Optional["GrantPrivilegesToDatabaseRoleOnSchemaObjectFuture"], result)

    @builtins.property
    def object_name(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the object on which privileges will be granted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#object_name GrantPrivilegesToDatabaseRole#object_name}
        '''
        result = self._values.get("object_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_type(self) -> typing.Optional[builtins.str]:
        '''The object type of the schema object on which privileges will be granted.

        Valid values are: AGGREGATION POLICY | ALERT | AUTHENTICATION POLICY | CORTEX SEARCH SERVICE | DATA METRIC FUNCTION | DYNAMIC TABLE | EVENT TABLE | EXTERNAL TABLE | FILE FORMAT | FUNCTION | GIT REPOSITORY | HYBRID TABLE | IMAGE REPOSITORY | ICEBERG TABLE | MASKING POLICY | MATERIALIZED VIEW | MODEL | NETWORK RULE | NOTEBOOK | PACKAGES POLICY | PASSWORD POLICY | PIPE | PROCEDURE | PROJECTION POLICY | ROW ACCESS POLICY | SECRET | SERVICE | SESSION POLICY | SEQUENCE | SNAPSHOT | STAGE | STREAM | TABLE | TAG | TASK | VIEW | STREAMLIT | DATASET

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#object_type GrantPrivilegesToDatabaseRole#object_type}
        '''
        result = self._values.get("object_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantPrivilegesToDatabaseRoleOnSchemaObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToDatabaseRole.GrantPrivilegesToDatabaseRoleOnSchemaObjectAll",
    jsii_struct_bases=[],
    name_mapping={
        "object_type_plural": "objectTypePlural",
        "in_database": "inDatabase",
        "in_schema": "inSchema",
    },
)
class GrantPrivilegesToDatabaseRoleOnSchemaObjectAll:
    def __init__(
        self,
        *,
        object_type_plural: builtins.str,
        in_database: typing.Optional[builtins.str] = None,
        in_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_type_plural: The plural object type of the schema object on which privileges will be granted. Valid values are: AGGREGATION POLICIES | ALERTS | AUTHENTICATION POLICIES | CORTEX SEARCH SERVICES | DATA METRIC FUNCTIONS | DYNAMIC TABLES | EVENT TABLES | EXTERNAL TABLES | FILE FORMATS | FUNCTIONS | GIT REPOSITORIES | HYBRID TABLES | IMAGE REPOSITORIES | ICEBERG TABLES | MASKING POLICIES | MATERIALIZED VIEWS | MODELS | NETWORK RULES | NOTEBOOKS | PACKAGES POLICIES | PASSWORD POLICIES | PIPES | PROCEDURES | PROJECTION POLICIES | ROW ACCESS POLICIES | SECRETS | SERVICES | SESSION POLICIES | SEQUENCES | SNAPSHOTS | STAGES | STREAMS | TABLES | TAGS | TASKS | VIEWS | STREAMLITS | DATASETS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#object_type_plural GrantPrivilegesToDatabaseRole#object_type_plural}
        :param in_database: The fully qualified name of the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#in_database GrantPrivilegesToDatabaseRole#in_database}
        :param in_schema: The fully qualified name of the schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#in_schema GrantPrivilegesToDatabaseRole#in_schema}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9018d9cb5904d5f571723d0017b681212421e8b1cbd10a7e8ac713bd354b268)
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
        '''The plural object type of the schema object on which privileges will be granted.

        Valid values are: AGGREGATION POLICIES | ALERTS | AUTHENTICATION POLICIES | CORTEX SEARCH SERVICES | DATA METRIC FUNCTIONS | DYNAMIC TABLES | EVENT TABLES | EXTERNAL TABLES | FILE FORMATS | FUNCTIONS | GIT REPOSITORIES | HYBRID TABLES | IMAGE REPOSITORIES | ICEBERG TABLES | MASKING POLICIES | MATERIALIZED VIEWS | MODELS | NETWORK RULES | NOTEBOOKS | PACKAGES POLICIES | PASSWORD POLICIES | PIPES | PROCEDURES | PROJECTION POLICIES | ROW ACCESS POLICIES | SECRETS | SERVICES | SESSION POLICIES | SEQUENCES | SNAPSHOTS | STAGES | STREAMS | TABLES | TAGS | TASKS | VIEWS | STREAMLITS | DATASETS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#object_type_plural GrantPrivilegesToDatabaseRole#object_type_plural}
        '''
        result = self._values.get("object_type_plural")
        assert result is not None, "Required property 'object_type_plural' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def in_database(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#in_database GrantPrivilegesToDatabaseRole#in_database}
        '''
        result = self._values.get("in_database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def in_schema(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the schema.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#in_schema GrantPrivilegesToDatabaseRole#in_schema}
        '''
        result = self._values.get("in_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantPrivilegesToDatabaseRoleOnSchemaObjectAll(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GrantPrivilegesToDatabaseRoleOnSchemaObjectAllOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToDatabaseRole.GrantPrivilegesToDatabaseRoleOnSchemaObjectAllOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6b8696834c6dbd58ed46b93fa6bba448d3c10bedc0c3a9a6be18bffd12bdd45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03f04c8cf57a226d304134c8fd6deab5343fb4f5b57dae4fceb0c4b2533fe32f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inDatabase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inSchema")
    def in_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inSchema"))

    @in_schema.setter
    def in_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e4fa309f622e56cc3002b3491873fe31d1c39d4763bb4abc7675152ac083d13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectTypePlural")
    def object_type_plural(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectTypePlural"))

    @object_type_plural.setter
    def object_type_plural(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9defba9a79f064e6af120123142a296ed1d8cc1c6ee785fb2f7a9cb7bb586efb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectTypePlural", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GrantPrivilegesToDatabaseRoleOnSchemaObjectAll]:
        return typing.cast(typing.Optional[GrantPrivilegesToDatabaseRoleOnSchemaObjectAll], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GrantPrivilegesToDatabaseRoleOnSchemaObjectAll],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__448e3e2aa52dda164dd4f8fe2ff1eaa07734c71e31aa0f84884348a21466ff70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToDatabaseRole.GrantPrivilegesToDatabaseRoleOnSchemaObjectFuture",
    jsii_struct_bases=[],
    name_mapping={
        "object_type_plural": "objectTypePlural",
        "in_database": "inDatabase",
        "in_schema": "inSchema",
    },
)
class GrantPrivilegesToDatabaseRoleOnSchemaObjectFuture:
    def __init__(
        self,
        *,
        object_type_plural: builtins.str,
        in_database: typing.Optional[builtins.str] = None,
        in_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_type_plural: The plural object type of the schema object on which privileges will be granted. Valid values are: ALERTS | AUTHENTICATION POLICIES | DATA METRIC FUNCTIONS | DYNAMIC TABLES | EVENT TABLES | EXTERNAL TABLES | FILE FORMATS | FUNCTIONS | GIT REPOSITORIES | HYBRID TABLES | ICEBERG TABLES | MATERIALIZED VIEWS | MODELS | NETWORK RULES | NOTEBOOKS | PASSWORD POLICIES | PIPES | PROCEDURES | SECRETS | SERVICES | SEQUENCES | SNAPSHOTS | STAGES | STREAMS | TABLES | TASKS | VIEWS | DATASETS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#object_type_plural GrantPrivilegesToDatabaseRole#object_type_plural}
        :param in_database: The fully qualified name of the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#in_database GrantPrivilegesToDatabaseRole#in_database}
        :param in_schema: The fully qualified name of the schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#in_schema GrantPrivilegesToDatabaseRole#in_schema}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc6012563f334d9938fb9338fb662d2c8220632e4f1c416be70e033362d718f)
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
        '''The plural object type of the schema object on which privileges will be granted.

        Valid values are: ALERTS | AUTHENTICATION POLICIES | DATA METRIC FUNCTIONS | DYNAMIC TABLES | EVENT TABLES | EXTERNAL TABLES | FILE FORMATS | FUNCTIONS | GIT REPOSITORIES | HYBRID TABLES | ICEBERG TABLES | MATERIALIZED VIEWS | MODELS | NETWORK RULES | NOTEBOOKS | PASSWORD POLICIES | PIPES | PROCEDURES | SECRETS | SERVICES | SEQUENCES | SNAPSHOTS | STAGES | STREAMS | TABLES | TASKS | VIEWS | DATASETS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#object_type_plural GrantPrivilegesToDatabaseRole#object_type_plural}
        '''
        result = self._values.get("object_type_plural")
        assert result is not None, "Required property 'object_type_plural' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def in_database(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#in_database GrantPrivilegesToDatabaseRole#in_database}
        '''
        result = self._values.get("in_database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def in_schema(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the schema.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#in_schema GrantPrivilegesToDatabaseRole#in_schema}
        '''
        result = self._values.get("in_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantPrivilegesToDatabaseRoleOnSchemaObjectFuture(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GrantPrivilegesToDatabaseRoleOnSchemaObjectFutureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToDatabaseRole.GrantPrivilegesToDatabaseRoleOnSchemaObjectFutureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1a06c48257602d779defca87779e47e778837c2ad89f7407a41666f6161bb20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab545af73865ff6eb4983cbf199abc6430ac122116d25f16f1d9271d4e81074e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inDatabase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inSchema")
    def in_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inSchema"))

    @in_schema.setter
    def in_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7f8a847df098b78804e095c17d963bb796c98bedcf0282a85bff68b63aa1ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectTypePlural")
    def object_type_plural(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectTypePlural"))

    @object_type_plural.setter
    def object_type_plural(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f1cdaa854cd814d518a4d121fef2adf8f7b0ea03855ac4291d57bba2a947e9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectTypePlural", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GrantPrivilegesToDatabaseRoleOnSchemaObjectFuture]:
        return typing.cast(typing.Optional[GrantPrivilegesToDatabaseRoleOnSchemaObjectFuture], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GrantPrivilegesToDatabaseRoleOnSchemaObjectFuture],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fca9a6ffdb1f2842cf7c6aa2b3ac9d700e2be33a8fb42aea429a1031b28c225)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GrantPrivilegesToDatabaseRoleOnSchemaObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToDatabaseRole.GrantPrivilegesToDatabaseRoleOnSchemaObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__287c4663c936f2af404638ec0ff66a620abf84effd0540408c1b07cc8276f2fd)
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
        :param object_type_plural: The plural object type of the schema object on which privileges will be granted. Valid values are: AGGREGATION POLICIES | ALERTS | AUTHENTICATION POLICIES | CORTEX SEARCH SERVICES | DATA METRIC FUNCTIONS | DYNAMIC TABLES | EVENT TABLES | EXTERNAL TABLES | FILE FORMATS | FUNCTIONS | GIT REPOSITORIES | HYBRID TABLES | IMAGE REPOSITORIES | ICEBERG TABLES | MASKING POLICIES | MATERIALIZED VIEWS | MODELS | NETWORK RULES | NOTEBOOKS | PACKAGES POLICIES | PASSWORD POLICIES | PIPES | PROCEDURES | PROJECTION POLICIES | ROW ACCESS POLICIES | SECRETS | SERVICES | SESSION POLICIES | SEQUENCES | SNAPSHOTS | STAGES | STREAMS | TABLES | TAGS | TASKS | VIEWS | STREAMLITS | DATASETS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#object_type_plural GrantPrivilegesToDatabaseRole#object_type_plural}
        :param in_database: The fully qualified name of the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#in_database GrantPrivilegesToDatabaseRole#in_database}
        :param in_schema: The fully qualified name of the schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#in_schema GrantPrivilegesToDatabaseRole#in_schema}
        '''
        value = GrantPrivilegesToDatabaseRoleOnSchemaObjectAll(
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
        :param object_type_plural: The plural object type of the schema object on which privileges will be granted. Valid values are: ALERTS | AUTHENTICATION POLICIES | DATA METRIC FUNCTIONS | DYNAMIC TABLES | EVENT TABLES | EXTERNAL TABLES | FILE FORMATS | FUNCTIONS | GIT REPOSITORIES | HYBRID TABLES | ICEBERG TABLES | MATERIALIZED VIEWS | MODELS | NETWORK RULES | NOTEBOOKS | PASSWORD POLICIES | PIPES | PROCEDURES | SECRETS | SERVICES | SEQUENCES | SNAPSHOTS | STAGES | STREAMS | TABLES | TASKS | VIEWS | DATASETS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#object_type_plural GrantPrivilegesToDatabaseRole#object_type_plural}
        :param in_database: The fully qualified name of the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#in_database GrantPrivilegesToDatabaseRole#in_database}
        :param in_schema: The fully qualified name of the schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_database_role#in_schema GrantPrivilegesToDatabaseRole#in_schema}
        '''
        value = GrantPrivilegesToDatabaseRoleOnSchemaObjectFuture(
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
    def all(self) -> GrantPrivilegesToDatabaseRoleOnSchemaObjectAllOutputReference:
        return typing.cast(GrantPrivilegesToDatabaseRoleOnSchemaObjectAllOutputReference, jsii.get(self, "all"))

    @builtins.property
    @jsii.member(jsii_name="future")
    def future(
        self,
    ) -> GrantPrivilegesToDatabaseRoleOnSchemaObjectFutureOutputReference:
        return typing.cast(GrantPrivilegesToDatabaseRoleOnSchemaObjectFutureOutputReference, jsii.get(self, "future"))

    @builtins.property
    @jsii.member(jsii_name="allInput")
    def all_input(
        self,
    ) -> typing.Optional[GrantPrivilegesToDatabaseRoleOnSchemaObjectAll]:
        return typing.cast(typing.Optional[GrantPrivilegesToDatabaseRoleOnSchemaObjectAll], jsii.get(self, "allInput"))

    @builtins.property
    @jsii.member(jsii_name="futureInput")
    def future_input(
        self,
    ) -> typing.Optional[GrantPrivilegesToDatabaseRoleOnSchemaObjectFuture]:
        return typing.cast(typing.Optional[GrantPrivilegesToDatabaseRoleOnSchemaObjectFuture], jsii.get(self, "futureInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a836928c737176b53f7c9368cb9a9b2e9ea20c280aea8e30828cd37bbaec97b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectType")
    def object_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectType"))

    @object_type.setter
    def object_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5fb023188a14948453daa2d03347a3828662f76009a7b98941aec0caae273a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GrantPrivilegesToDatabaseRoleOnSchemaObject]:
        return typing.cast(typing.Optional[GrantPrivilegesToDatabaseRoleOnSchemaObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GrantPrivilegesToDatabaseRoleOnSchemaObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b6ffd0eb3fb5372c970670b78b4b3bdeafae382587ac66d7adddb67c7269ed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GrantPrivilegesToDatabaseRoleOnSchemaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToDatabaseRole.GrantPrivilegesToDatabaseRoleOnSchemaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76e8a25dc908f31e92b1778939a3de6a0dae5029c264c2c106373b3c2c8e3e7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllSchemasInDatabase")
    def reset_all_schemas_in_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllSchemasInDatabase", []))

    @jsii.member(jsii_name="resetFutureSchemasInDatabase")
    def reset_future_schemas_in_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFutureSchemasInDatabase", []))

    @jsii.member(jsii_name="resetSchemaName")
    def reset_schema_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaName", []))

    @builtins.property
    @jsii.member(jsii_name="allSchemasInDatabaseInput")
    def all_schemas_in_database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allSchemasInDatabaseInput"))

    @builtins.property
    @jsii.member(jsii_name="futureSchemasInDatabaseInput")
    def future_schemas_in_database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "futureSchemasInDatabaseInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaNameInput")
    def schema_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaNameInput"))

    @builtins.property
    @jsii.member(jsii_name="allSchemasInDatabase")
    def all_schemas_in_database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allSchemasInDatabase"))

    @all_schemas_in_database.setter
    def all_schemas_in_database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a31609af1cb4c41f0c98116c5b3159c027f1184543b690d5a7b2c472f33e50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allSchemasInDatabase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="futureSchemasInDatabase")
    def future_schemas_in_database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "futureSchemasInDatabase"))

    @future_schemas_in_database.setter
    def future_schemas_in_database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b336c81d7ad408485d9094e4a4e6c8e28d9525b5e594cfc490a1b50df5ea1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "futureSchemasInDatabase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schemaName")
    def schema_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaName"))

    @schema_name.setter
    def schema_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d0338988ffaa04616761eebcbcf0f0a0fc0a2ce6a02ac83d4eb36a53a5396a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GrantPrivilegesToDatabaseRoleOnSchema]:
        return typing.cast(typing.Optional[GrantPrivilegesToDatabaseRoleOnSchema], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GrantPrivilegesToDatabaseRoleOnSchema],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a1b5f08b312f627d52fa13ae9ec4786411d28eef70dbba4f23ef6bb65bf10f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GrantPrivilegesToDatabaseRole",
    "GrantPrivilegesToDatabaseRoleConfig",
    "GrantPrivilegesToDatabaseRoleOnSchema",
    "GrantPrivilegesToDatabaseRoleOnSchemaObject",
    "GrantPrivilegesToDatabaseRoleOnSchemaObjectAll",
    "GrantPrivilegesToDatabaseRoleOnSchemaObjectAllOutputReference",
    "GrantPrivilegesToDatabaseRoleOnSchemaObjectFuture",
    "GrantPrivilegesToDatabaseRoleOnSchemaObjectFutureOutputReference",
    "GrantPrivilegesToDatabaseRoleOnSchemaObjectOutputReference",
    "GrantPrivilegesToDatabaseRoleOnSchemaOutputReference",
]

publication.publish()

def _typecheckingstub__02d7ad43ea8f91f0d10978caf4a9250c54b3ca7c7d61ea040d3ac99e454cab0c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database_role_name: builtins.str,
    all_privileges: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    always_apply: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    always_apply_trigger: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    on_database: typing.Optional[builtins.str] = None,
    on_schema: typing.Optional[typing.Union[GrantPrivilegesToDatabaseRoleOnSchema, typing.Dict[builtins.str, typing.Any]]] = None,
    on_schema_object: typing.Optional[typing.Union[GrantPrivilegesToDatabaseRoleOnSchemaObject, typing.Dict[builtins.str, typing.Any]]] = None,
    privileges: typing.Optional[typing.Sequence[builtins.str]] = None,
    with_grant_option: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__22217f71b53ff727e01696aa73e681840cc9da7abb1e86427909fdbac1b15396(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06657da865051e79467d93ff025a73a0dec63b038ffd421303960324e1cd21e7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663e44b835f6ee3a2a5e66203448f0b1fd553048d60c146fd7bca8c962642fe7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9406fc9e16dca18d81093d9dc61c2729de3c9a33badbc0493709a42f9adb4088(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edaada8cd2f15dc8e669cdac70298254d701cedfd9d360d77cf127d00410cbfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cab57df862a8b450e58dbea75b1d61929eb7991db9d55f786c4a19c59d8b06a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7452b3d3071e10972d5a815bd386d7bfc3376b576bb0596cdfbbfb454c1470(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69cec71a3d146dd6c919a83e6b045906aa7bcfd274fa4b3c57a247d46d63b97e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83794808274aa5d5076aedec292e7e84b2816e34bff0f4728359e1d9716bdc98(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45d6b8de65d8dc580a3c825b8df5fae6970b8ac80df6abcac8e16480969f441(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    database_role_name: builtins.str,
    all_privileges: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    always_apply: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    always_apply_trigger: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    on_database: typing.Optional[builtins.str] = None,
    on_schema: typing.Optional[typing.Union[GrantPrivilegesToDatabaseRoleOnSchema, typing.Dict[builtins.str, typing.Any]]] = None,
    on_schema_object: typing.Optional[typing.Union[GrantPrivilegesToDatabaseRoleOnSchemaObject, typing.Dict[builtins.str, typing.Any]]] = None,
    privileges: typing.Optional[typing.Sequence[builtins.str]] = None,
    with_grant_option: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7684c1c67a25a2ababc11d44a0c75b4a0b5ca484112a1abd301af3ae179c3c1d(
    *,
    all_schemas_in_database: typing.Optional[builtins.str] = None,
    future_schemas_in_database: typing.Optional[builtins.str] = None,
    schema_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49e690505885d5e22fac1142bf0aaa501721e79e37f46bcb6df0638f15e0202(
    *,
    all: typing.Optional[typing.Union[GrantPrivilegesToDatabaseRoleOnSchemaObjectAll, typing.Dict[builtins.str, typing.Any]]] = None,
    future: typing.Optional[typing.Union[GrantPrivilegesToDatabaseRoleOnSchemaObjectFuture, typing.Dict[builtins.str, typing.Any]]] = None,
    object_name: typing.Optional[builtins.str] = None,
    object_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9018d9cb5904d5f571723d0017b681212421e8b1cbd10a7e8ac713bd354b268(
    *,
    object_type_plural: builtins.str,
    in_database: typing.Optional[builtins.str] = None,
    in_schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b8696834c6dbd58ed46b93fa6bba448d3c10bedc0c3a9a6be18bffd12bdd45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f04c8cf57a226d304134c8fd6deab5343fb4f5b57dae4fceb0c4b2533fe32f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4fa309f622e56cc3002b3491873fe31d1c39d4763bb4abc7675152ac083d13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9defba9a79f064e6af120123142a296ed1d8cc1c6ee785fb2f7a9cb7bb586efb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448e3e2aa52dda164dd4f8fe2ff1eaa07734c71e31aa0f84884348a21466ff70(
    value: typing.Optional[GrantPrivilegesToDatabaseRoleOnSchemaObjectAll],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc6012563f334d9938fb9338fb662d2c8220632e4f1c416be70e033362d718f(
    *,
    object_type_plural: builtins.str,
    in_database: typing.Optional[builtins.str] = None,
    in_schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a06c48257602d779defca87779e47e778837c2ad89f7407a41666f6161bb20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab545af73865ff6eb4983cbf199abc6430ac122116d25f16f1d9271d4e81074e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7f8a847df098b78804e095c17d963bb796c98bedcf0282a85bff68b63aa1ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f1cdaa854cd814d518a4d121fef2adf8f7b0ea03855ac4291d57bba2a947e9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fca9a6ffdb1f2842cf7c6aa2b3ac9d700e2be33a8fb42aea429a1031b28c225(
    value: typing.Optional[GrantPrivilegesToDatabaseRoleOnSchemaObjectFuture],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__287c4663c936f2af404638ec0ff66a620abf84effd0540408c1b07cc8276f2fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a836928c737176b53f7c9368cb9a9b2e9ea20c280aea8e30828cd37bbaec97b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5fb023188a14948453daa2d03347a3828662f76009a7b98941aec0caae273a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6ffd0eb3fb5372c970670b78b4b3bdeafae382587ac66d7adddb67c7269ed4(
    value: typing.Optional[GrantPrivilegesToDatabaseRoleOnSchemaObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e8a25dc908f31e92b1778939a3de6a0dae5029c264c2c106373b3c2c8e3e7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a31609af1cb4c41f0c98116c5b3159c027f1184543b690d5a7b2c472f33e50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b336c81d7ad408485d9094e4a4e6c8e28d9525b5e594cfc490a1b50df5ea1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d0338988ffaa04616761eebcbcf0f0a0fc0a2ce6a02ac83d4eb36a53a5396a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a1b5f08b312f627d52fa13ae9ec4786411d28eef70dbba4f23ef6bb65bf10f(
    value: typing.Optional[GrantPrivilegesToDatabaseRoleOnSchema],
) -> None:
    """Type checking stubs"""
    pass
