r'''
# `snowflake_grant_privileges_to_account_role`

Refer to the Terraform Registry for docs: [`snowflake_grant_privileges_to_account_role`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role).
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


class GrantPrivilegesToAccountRole(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToAccountRole.GrantPrivilegesToAccountRole",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role snowflake_grant_privileges_to_account_role}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_role_name: builtins.str,
        all_privileges: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        always_apply: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        always_apply_trigger: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        on_account: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        on_account_object: typing.Optional[typing.Union["GrantPrivilegesToAccountRoleOnAccountObject", typing.Dict[builtins.str, typing.Any]]] = None,
        on_schema: typing.Optional[typing.Union["GrantPrivilegesToAccountRoleOnSchema", typing.Dict[builtins.str, typing.Any]]] = None,
        on_schema_object: typing.Optional[typing.Union["GrantPrivilegesToAccountRoleOnSchemaObject", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role snowflake_grant_privileges_to_account_role} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_role_name: The fully qualified name of the account role to which privileges will be granted. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#account_role_name GrantPrivilegesToAccountRole#account_role_name}
        :param all_privileges: Grant all privileges on the account role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#all_privileges GrantPrivilegesToAccountRole#all_privileges}
        :param always_apply: If true, the resource will always produce a “plan” and on “apply” it will re-grant defined privileges. It is supposed to be used only in “grant privileges on all X’s in database / schema Y” or “grant all privileges to X” scenarios to make sure that every new object in a given database / schema is granted by the account role and every new privilege is granted to the database role. Important note: this flag is not compliant with the Terraform assumptions of the config being eventually convergent (producing an empty plan). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#always_apply GrantPrivilegesToAccountRole#always_apply}
        :param always_apply_trigger: This is a helper field and should not be set. Its main purpose is to help to achieve the functionality described by the always_apply field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#always_apply_trigger GrantPrivilegesToAccountRole#always_apply_trigger}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#id GrantPrivilegesToAccountRole#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param on_account: If true, the privileges will be granted on the account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#on_account GrantPrivilegesToAccountRole#on_account}
        :param on_account_object: on_account_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#on_account_object GrantPrivilegesToAccountRole#on_account_object}
        :param on_schema: on_schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#on_schema GrantPrivilegesToAccountRole#on_schema}
        :param on_schema_object: on_schema_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#on_schema_object GrantPrivilegesToAccountRole#on_schema_object}
        :param privileges: The privileges to grant on the account role. This field is case-sensitive; use only upper-case privileges. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#privileges GrantPrivilegesToAccountRole#privileges}
        :param with_grant_option: Specifies whether the grantee can grant the privileges to other users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#with_grant_option GrantPrivilegesToAccountRole#with_grant_option}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a1b5c0efc498aa0a5ec3c37e160f9d9791dbf9fc223c589a2d569fe57976f3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GrantPrivilegesToAccountRoleConfig(
            account_role_name=account_role_name,
            all_privileges=all_privileges,
            always_apply=always_apply,
            always_apply_trigger=always_apply_trigger,
            id=id,
            on_account=on_account,
            on_account_object=on_account_object,
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
        '''Generates CDKTF code for importing a GrantPrivilegesToAccountRole resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GrantPrivilegesToAccountRole to import.
        :param import_from_id: The id of the existing GrantPrivilegesToAccountRole that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GrantPrivilegesToAccountRole to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb0437d7fdb60a1f772a7ca3c3b0cce2dcb3ce90cbc7a2ea7d6a0c9838db5f7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putOnAccountObject")
    def put_on_account_object(
        self,
        *,
        object_name: builtins.str,
        object_type: builtins.str,
    ) -> None:
        '''
        :param object_name: The fully qualified name of the object on which privileges will be granted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_name GrantPrivilegesToAccountRole#object_name}
        :param object_type: The object type of the account object on which privileges will be granted. Valid values are: USER | RESOURCE MONITOR | WAREHOUSE | COMPUTE POOL | DATABASE | INTEGRATION | FAILOVER GROUP | REPLICATION GROUP | EXTERNAL VOLUME Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_type GrantPrivilegesToAccountRole#object_type}
        '''
        value = GrantPrivilegesToAccountRoleOnAccountObject(
            object_name=object_name, object_type=object_type
        )

        return typing.cast(None, jsii.invoke(self, "putOnAccountObject", [value]))

    @jsii.member(jsii_name="putOnSchema")
    def put_on_schema(
        self,
        *,
        all_schemas_in_database: typing.Optional[builtins.str] = None,
        future_schemas_in_database: typing.Optional[builtins.str] = None,
        schema_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param all_schemas_in_database: The fully qualified name of the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#all_schemas_in_database GrantPrivilegesToAccountRole#all_schemas_in_database}
        :param future_schemas_in_database: The fully qualified name of the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#future_schemas_in_database GrantPrivilegesToAccountRole#future_schemas_in_database}
        :param schema_name: The fully qualified name of the schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#schema_name GrantPrivilegesToAccountRole#schema_name}
        '''
        value = GrantPrivilegesToAccountRoleOnSchema(
            all_schemas_in_database=all_schemas_in_database,
            future_schemas_in_database=future_schemas_in_database,
            schema_name=schema_name,
        )

        return typing.cast(None, jsii.invoke(self, "putOnSchema", [value]))

    @jsii.member(jsii_name="putOnSchemaObject")
    def put_on_schema_object(
        self,
        *,
        all: typing.Optional[typing.Union["GrantPrivilegesToAccountRoleOnSchemaObjectAll", typing.Dict[builtins.str, typing.Any]]] = None,
        future: typing.Optional[typing.Union["GrantPrivilegesToAccountRoleOnSchemaObjectFuture", typing.Dict[builtins.str, typing.Any]]] = None,
        object_name: typing.Optional[builtins.str] = None,
        object_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param all: all block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#all GrantPrivilegesToAccountRole#all}
        :param future: future block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#future GrantPrivilegesToAccountRole#future}
        :param object_name: The fully qualified name of the object on which privileges will be granted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_name GrantPrivilegesToAccountRole#object_name}
        :param object_type: The object type of the schema object on which privileges will be granted. Valid values are: AGGREGATION POLICY | ALERT | AUTHENTICATION POLICY | CORTEX SEARCH SERVICE | DATA METRIC FUNCTION | DYNAMIC TABLE | EVENT TABLE | EXTERNAL TABLE | FILE FORMAT | FUNCTION | GIT REPOSITORY | HYBRID TABLE | IMAGE REPOSITORY | ICEBERG TABLE | MASKING POLICY | MATERIALIZED VIEW | MODEL | NETWORK RULE | NOTEBOOK | PACKAGES POLICY | PASSWORD POLICY | PIPE | PROCEDURE | PROJECTION POLICY | ROW ACCESS POLICY | SECRET | SERVICE | SESSION POLICY | SEQUENCE | SNAPSHOT | STAGE | STREAM | TABLE | TAG | TASK | VIEW | STREAMLIT | DATASET Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_type GrantPrivilegesToAccountRole#object_type}
        '''
        value = GrantPrivilegesToAccountRoleOnSchemaObject(
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

    @jsii.member(jsii_name="resetOnAccount")
    def reset_on_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnAccount", []))

    @jsii.member(jsii_name="resetOnAccountObject")
    def reset_on_account_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnAccountObject", []))

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
    @jsii.member(jsii_name="onAccountObject")
    def on_account_object(
        self,
    ) -> "GrantPrivilegesToAccountRoleOnAccountObjectOutputReference":
        return typing.cast("GrantPrivilegesToAccountRoleOnAccountObjectOutputReference", jsii.get(self, "onAccountObject"))

    @builtins.property
    @jsii.member(jsii_name="onSchema")
    def on_schema(self) -> "GrantPrivilegesToAccountRoleOnSchemaOutputReference":
        return typing.cast("GrantPrivilegesToAccountRoleOnSchemaOutputReference", jsii.get(self, "onSchema"))

    @builtins.property
    @jsii.member(jsii_name="onSchemaObject")
    def on_schema_object(
        self,
    ) -> "GrantPrivilegesToAccountRoleOnSchemaObjectOutputReference":
        return typing.cast("GrantPrivilegesToAccountRoleOnSchemaObjectOutputReference", jsii.get(self, "onSchemaObject"))

    @builtins.property
    @jsii.member(jsii_name="accountRoleNameInput")
    def account_role_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountRoleNameInput"))

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
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="onAccountInput")
    def on_account_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "onAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="onAccountObjectInput")
    def on_account_object_input(
        self,
    ) -> typing.Optional["GrantPrivilegesToAccountRoleOnAccountObject"]:
        return typing.cast(typing.Optional["GrantPrivilegesToAccountRoleOnAccountObject"], jsii.get(self, "onAccountObjectInput"))

    @builtins.property
    @jsii.member(jsii_name="onSchemaInput")
    def on_schema_input(
        self,
    ) -> typing.Optional["GrantPrivilegesToAccountRoleOnSchema"]:
        return typing.cast(typing.Optional["GrantPrivilegesToAccountRoleOnSchema"], jsii.get(self, "onSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="onSchemaObjectInput")
    def on_schema_object_input(
        self,
    ) -> typing.Optional["GrantPrivilegesToAccountRoleOnSchemaObject"]:
        return typing.cast(typing.Optional["GrantPrivilegesToAccountRoleOnSchemaObject"], jsii.get(self, "onSchemaObjectInput"))

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
    @jsii.member(jsii_name="accountRoleName")
    def account_role_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountRoleName"))

    @account_role_name.setter
    def account_role_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d46360bc5d72806d31f8dd8d0a46fba9e16b436ea60ab0c76d0de61af35d3d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountRoleName", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__d60934c7532fcc1360ac8df165bf0d8e0422908ccdcb7799d712919dd7361aff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__713073909d94537630fef94627d1e726e0717a09f0a74f926f6565a9251669da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alwaysApply", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alwaysApplyTrigger")
    def always_apply_trigger(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alwaysApplyTrigger"))

    @always_apply_trigger.setter
    def always_apply_trigger(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c66654cdde8c18a24b8edf6d0c88d2f458cf42ff102a6e33725443858afec2a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alwaysApplyTrigger", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95ab2890e2cc5f38c74c8bea4ba52d2059a3516b8c9ccfff026535e599a6b0e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onAccount")
    def on_account(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "onAccount"))

    @on_account.setter
    def on_account(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe9837294f94afd35215a6646033c651643a5180daf61b1172f47d2eb75ad342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privileges")
    def privileges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "privileges"))

    @privileges.setter
    def privileges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f724d3edf454539d697fbee7ba82cb8c8d2ded75e2694c23523bb81bba121713)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a66b59203dd1fa31d05f9702b79ba256fbf6878af98e3fbfaabf491c51f82a8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withGrantOption", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToAccountRole.GrantPrivilegesToAccountRoleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_role_name": "accountRoleName",
        "all_privileges": "allPrivileges",
        "always_apply": "alwaysApply",
        "always_apply_trigger": "alwaysApplyTrigger",
        "id": "id",
        "on_account": "onAccount",
        "on_account_object": "onAccountObject",
        "on_schema": "onSchema",
        "on_schema_object": "onSchemaObject",
        "privileges": "privileges",
        "with_grant_option": "withGrantOption",
    },
)
class GrantPrivilegesToAccountRoleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_role_name: builtins.str,
        all_privileges: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        always_apply: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        always_apply_trigger: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        on_account: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        on_account_object: typing.Optional[typing.Union["GrantPrivilegesToAccountRoleOnAccountObject", typing.Dict[builtins.str, typing.Any]]] = None,
        on_schema: typing.Optional[typing.Union["GrantPrivilegesToAccountRoleOnSchema", typing.Dict[builtins.str, typing.Any]]] = None,
        on_schema_object: typing.Optional[typing.Union["GrantPrivilegesToAccountRoleOnSchemaObject", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param account_role_name: The fully qualified name of the account role to which privileges will be granted. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#account_role_name GrantPrivilegesToAccountRole#account_role_name}
        :param all_privileges: Grant all privileges on the account role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#all_privileges GrantPrivilegesToAccountRole#all_privileges}
        :param always_apply: If true, the resource will always produce a “plan” and on “apply” it will re-grant defined privileges. It is supposed to be used only in “grant privileges on all X’s in database / schema Y” or “grant all privileges to X” scenarios to make sure that every new object in a given database / schema is granted by the account role and every new privilege is granted to the database role. Important note: this flag is not compliant with the Terraform assumptions of the config being eventually convergent (producing an empty plan). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#always_apply GrantPrivilegesToAccountRole#always_apply}
        :param always_apply_trigger: This is a helper field and should not be set. Its main purpose is to help to achieve the functionality described by the always_apply field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#always_apply_trigger GrantPrivilegesToAccountRole#always_apply_trigger}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#id GrantPrivilegesToAccountRole#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param on_account: If true, the privileges will be granted on the account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#on_account GrantPrivilegesToAccountRole#on_account}
        :param on_account_object: on_account_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#on_account_object GrantPrivilegesToAccountRole#on_account_object}
        :param on_schema: on_schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#on_schema GrantPrivilegesToAccountRole#on_schema}
        :param on_schema_object: on_schema_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#on_schema_object GrantPrivilegesToAccountRole#on_schema_object}
        :param privileges: The privileges to grant on the account role. This field is case-sensitive; use only upper-case privileges. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#privileges GrantPrivilegesToAccountRole#privileges}
        :param with_grant_option: Specifies whether the grantee can grant the privileges to other users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#with_grant_option GrantPrivilegesToAccountRole#with_grant_option}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(on_account_object, dict):
            on_account_object = GrantPrivilegesToAccountRoleOnAccountObject(**on_account_object)
        if isinstance(on_schema, dict):
            on_schema = GrantPrivilegesToAccountRoleOnSchema(**on_schema)
        if isinstance(on_schema_object, dict):
            on_schema_object = GrantPrivilegesToAccountRoleOnSchemaObject(**on_schema_object)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c5985946c9d83bd0b5ca0cb3e060c43945ed0c98648765ac15b5023927c85ec)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_role_name", value=account_role_name, expected_type=type_hints["account_role_name"])
            check_type(argname="argument all_privileges", value=all_privileges, expected_type=type_hints["all_privileges"])
            check_type(argname="argument always_apply", value=always_apply, expected_type=type_hints["always_apply"])
            check_type(argname="argument always_apply_trigger", value=always_apply_trigger, expected_type=type_hints["always_apply_trigger"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument on_account", value=on_account, expected_type=type_hints["on_account"])
            check_type(argname="argument on_account_object", value=on_account_object, expected_type=type_hints["on_account_object"])
            check_type(argname="argument on_schema", value=on_schema, expected_type=type_hints["on_schema"])
            check_type(argname="argument on_schema_object", value=on_schema_object, expected_type=type_hints["on_schema_object"])
            check_type(argname="argument privileges", value=privileges, expected_type=type_hints["privileges"])
            check_type(argname="argument with_grant_option", value=with_grant_option, expected_type=type_hints["with_grant_option"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_role_name": account_role_name,
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
        if on_account is not None:
            self._values["on_account"] = on_account
        if on_account_object is not None:
            self._values["on_account_object"] = on_account_object
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
    def account_role_name(self) -> builtins.str:
        '''The fully qualified name of the account role to which privileges will be granted.

        For more information about this resource, see `docs <./account_role>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#account_role_name GrantPrivilegesToAccountRole#account_role_name}
        '''
        result = self._values.get("account_role_name")
        assert result is not None, "Required property 'account_role_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def all_privileges(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Grant all privileges on the account role.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#all_privileges GrantPrivilegesToAccountRole#all_privileges}
        '''
        result = self._values.get("all_privileges")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def always_apply(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the resource will always produce a “plan” and on “apply” it will re-grant defined privileges.

        It is supposed to be used only in “grant privileges on all X’s in database / schema Y” or “grant all privileges to X” scenarios to make sure that every new object in a given database / schema is granted by the account role and every new privilege is granted to the database role. Important note: this flag is not compliant with the Terraform assumptions of the config being eventually convergent (producing an empty plan).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#always_apply GrantPrivilegesToAccountRole#always_apply}
        '''
        result = self._values.get("always_apply")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def always_apply_trigger(self) -> typing.Optional[builtins.str]:
        '''This is a helper field and should not be set.

        Its main purpose is to help to achieve the functionality described by the always_apply field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#always_apply_trigger GrantPrivilegesToAccountRole#always_apply_trigger}
        '''
        result = self._values.get("always_apply_trigger")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#id GrantPrivilegesToAccountRole#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_account(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the privileges will be granted on the account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#on_account GrantPrivilegesToAccountRole#on_account}
        '''
        result = self._values.get("on_account")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def on_account_object(
        self,
    ) -> typing.Optional["GrantPrivilegesToAccountRoleOnAccountObject"]:
        '''on_account_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#on_account_object GrantPrivilegesToAccountRole#on_account_object}
        '''
        result = self._values.get("on_account_object")
        return typing.cast(typing.Optional["GrantPrivilegesToAccountRoleOnAccountObject"], result)

    @builtins.property
    def on_schema(self) -> typing.Optional["GrantPrivilegesToAccountRoleOnSchema"]:
        '''on_schema block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#on_schema GrantPrivilegesToAccountRole#on_schema}
        '''
        result = self._values.get("on_schema")
        return typing.cast(typing.Optional["GrantPrivilegesToAccountRoleOnSchema"], result)

    @builtins.property
    def on_schema_object(
        self,
    ) -> typing.Optional["GrantPrivilegesToAccountRoleOnSchemaObject"]:
        '''on_schema_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#on_schema_object GrantPrivilegesToAccountRole#on_schema_object}
        '''
        result = self._values.get("on_schema_object")
        return typing.cast(typing.Optional["GrantPrivilegesToAccountRoleOnSchemaObject"], result)

    @builtins.property
    def privileges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The privileges to grant on the account role. This field is case-sensitive; use only upper-case privileges.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#privileges GrantPrivilegesToAccountRole#privileges}
        '''
        result = self._values.get("privileges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def with_grant_option(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the grantee can grant the privileges to other users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#with_grant_option GrantPrivilegesToAccountRole#with_grant_option}
        '''
        result = self._values.get("with_grant_option")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantPrivilegesToAccountRoleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToAccountRole.GrantPrivilegesToAccountRoleOnAccountObject",
    jsii_struct_bases=[],
    name_mapping={"object_name": "objectName", "object_type": "objectType"},
)
class GrantPrivilegesToAccountRoleOnAccountObject:
    def __init__(self, *, object_name: builtins.str, object_type: builtins.str) -> None:
        '''
        :param object_name: The fully qualified name of the object on which privileges will be granted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_name GrantPrivilegesToAccountRole#object_name}
        :param object_type: The object type of the account object on which privileges will be granted. Valid values are: USER | RESOURCE MONITOR | WAREHOUSE | COMPUTE POOL | DATABASE | INTEGRATION | FAILOVER GROUP | REPLICATION GROUP | EXTERNAL VOLUME Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_type GrantPrivilegesToAccountRole#object_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861fe2cce2c2602466faa6646a59aba444110adbe74e8cca588a21e7f9d1e3e4)
            check_type(argname="argument object_name", value=object_name, expected_type=type_hints["object_name"])
            check_type(argname="argument object_type", value=object_type, expected_type=type_hints["object_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_name": object_name,
            "object_type": object_type,
        }

    @builtins.property
    def object_name(self) -> builtins.str:
        '''The fully qualified name of the object on which privileges will be granted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_name GrantPrivilegesToAccountRole#object_name}
        '''
        result = self._values.get("object_name")
        assert result is not None, "Required property 'object_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object_type(self) -> builtins.str:
        '''The object type of the account object on which privileges will be granted.

        Valid values are: USER | RESOURCE MONITOR | WAREHOUSE | COMPUTE POOL | DATABASE | INTEGRATION | FAILOVER GROUP | REPLICATION GROUP | EXTERNAL VOLUME

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_type GrantPrivilegesToAccountRole#object_type}
        '''
        result = self._values.get("object_type")
        assert result is not None, "Required property 'object_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantPrivilegesToAccountRoleOnAccountObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GrantPrivilegesToAccountRoleOnAccountObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToAccountRole.GrantPrivilegesToAccountRoleOnAccountObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e40b32d80f4c434211a96dbb7d37115313c4a48df2e6ee339cbcd4fed95a3a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__f29b3f8bdf2671559f52f3f630e42e65bad384430cc04aa1edff75b2436033fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectType")
    def object_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectType"))

    @object_type.setter
    def object_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98fc1eaac18ad53ec3e95282b7b73cfdd7f15a3fab9a39d668689ebc6e680ac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GrantPrivilegesToAccountRoleOnAccountObject]:
        return typing.cast(typing.Optional[GrantPrivilegesToAccountRoleOnAccountObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GrantPrivilegesToAccountRoleOnAccountObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f23f0c067a43026dd2853943d76e72423dfe76928370b9c5bdb5b3a783d38fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToAccountRole.GrantPrivilegesToAccountRoleOnSchema",
    jsii_struct_bases=[],
    name_mapping={
        "all_schemas_in_database": "allSchemasInDatabase",
        "future_schemas_in_database": "futureSchemasInDatabase",
        "schema_name": "schemaName",
    },
)
class GrantPrivilegesToAccountRoleOnSchema:
    def __init__(
        self,
        *,
        all_schemas_in_database: typing.Optional[builtins.str] = None,
        future_schemas_in_database: typing.Optional[builtins.str] = None,
        schema_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param all_schemas_in_database: The fully qualified name of the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#all_schemas_in_database GrantPrivilegesToAccountRole#all_schemas_in_database}
        :param future_schemas_in_database: The fully qualified name of the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#future_schemas_in_database GrantPrivilegesToAccountRole#future_schemas_in_database}
        :param schema_name: The fully qualified name of the schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#schema_name GrantPrivilegesToAccountRole#schema_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da8f6140aa5a41d99056f85bf4ce542b028117f7976db91cdeb4733b2e4d44f0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#all_schemas_in_database GrantPrivilegesToAccountRole#all_schemas_in_database}
        '''
        result = self._values.get("all_schemas_in_database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def future_schemas_in_database(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#future_schemas_in_database GrantPrivilegesToAccountRole#future_schemas_in_database}
        '''
        result = self._values.get("future_schemas_in_database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_name(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the schema.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#schema_name GrantPrivilegesToAccountRole#schema_name}
        '''
        result = self._values.get("schema_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantPrivilegesToAccountRoleOnSchema(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToAccountRole.GrantPrivilegesToAccountRoleOnSchemaObject",
    jsii_struct_bases=[],
    name_mapping={
        "all": "all",
        "future": "future",
        "object_name": "objectName",
        "object_type": "objectType",
    },
)
class GrantPrivilegesToAccountRoleOnSchemaObject:
    def __init__(
        self,
        *,
        all: typing.Optional[typing.Union["GrantPrivilegesToAccountRoleOnSchemaObjectAll", typing.Dict[builtins.str, typing.Any]]] = None,
        future: typing.Optional[typing.Union["GrantPrivilegesToAccountRoleOnSchemaObjectFuture", typing.Dict[builtins.str, typing.Any]]] = None,
        object_name: typing.Optional[builtins.str] = None,
        object_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param all: all block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#all GrantPrivilegesToAccountRole#all}
        :param future: future block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#future GrantPrivilegesToAccountRole#future}
        :param object_name: The fully qualified name of the object on which privileges will be granted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_name GrantPrivilegesToAccountRole#object_name}
        :param object_type: The object type of the schema object on which privileges will be granted. Valid values are: AGGREGATION POLICY | ALERT | AUTHENTICATION POLICY | CORTEX SEARCH SERVICE | DATA METRIC FUNCTION | DYNAMIC TABLE | EVENT TABLE | EXTERNAL TABLE | FILE FORMAT | FUNCTION | GIT REPOSITORY | HYBRID TABLE | IMAGE REPOSITORY | ICEBERG TABLE | MASKING POLICY | MATERIALIZED VIEW | MODEL | NETWORK RULE | NOTEBOOK | PACKAGES POLICY | PASSWORD POLICY | PIPE | PROCEDURE | PROJECTION POLICY | ROW ACCESS POLICY | SECRET | SERVICE | SESSION POLICY | SEQUENCE | SNAPSHOT | STAGE | STREAM | TABLE | TAG | TASK | VIEW | STREAMLIT | DATASET Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_type GrantPrivilegesToAccountRole#object_type}
        '''
        if isinstance(all, dict):
            all = GrantPrivilegesToAccountRoleOnSchemaObjectAll(**all)
        if isinstance(future, dict):
            future = GrantPrivilegesToAccountRoleOnSchemaObjectFuture(**future)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba8a57ce63907e4c92ebfd9f0109d1f22f5e3d6a167865156ac67e754b31919)
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
    def all(self) -> typing.Optional["GrantPrivilegesToAccountRoleOnSchemaObjectAll"]:
        '''all block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#all GrantPrivilegesToAccountRole#all}
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional["GrantPrivilegesToAccountRoleOnSchemaObjectAll"], result)

    @builtins.property
    def future(
        self,
    ) -> typing.Optional["GrantPrivilegesToAccountRoleOnSchemaObjectFuture"]:
        '''future block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#future GrantPrivilegesToAccountRole#future}
        '''
        result = self._values.get("future")
        return typing.cast(typing.Optional["GrantPrivilegesToAccountRoleOnSchemaObjectFuture"], result)

    @builtins.property
    def object_name(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the object on which privileges will be granted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_name GrantPrivilegesToAccountRole#object_name}
        '''
        result = self._values.get("object_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_type(self) -> typing.Optional[builtins.str]:
        '''The object type of the schema object on which privileges will be granted.

        Valid values are: AGGREGATION POLICY | ALERT | AUTHENTICATION POLICY | CORTEX SEARCH SERVICE | DATA METRIC FUNCTION | DYNAMIC TABLE | EVENT TABLE | EXTERNAL TABLE | FILE FORMAT | FUNCTION | GIT REPOSITORY | HYBRID TABLE | IMAGE REPOSITORY | ICEBERG TABLE | MASKING POLICY | MATERIALIZED VIEW | MODEL | NETWORK RULE | NOTEBOOK | PACKAGES POLICY | PASSWORD POLICY | PIPE | PROCEDURE | PROJECTION POLICY | ROW ACCESS POLICY | SECRET | SERVICE | SESSION POLICY | SEQUENCE | SNAPSHOT | STAGE | STREAM | TABLE | TAG | TASK | VIEW | STREAMLIT | DATASET

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_type GrantPrivilegesToAccountRole#object_type}
        '''
        result = self._values.get("object_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantPrivilegesToAccountRoleOnSchemaObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToAccountRole.GrantPrivilegesToAccountRoleOnSchemaObjectAll",
    jsii_struct_bases=[],
    name_mapping={
        "object_type_plural": "objectTypePlural",
        "in_database": "inDatabase",
        "in_schema": "inSchema",
    },
)
class GrantPrivilegesToAccountRoleOnSchemaObjectAll:
    def __init__(
        self,
        *,
        object_type_plural: builtins.str,
        in_database: typing.Optional[builtins.str] = None,
        in_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_type_plural: The plural object type of the schema object on which privileges will be granted. Valid values are: AGGREGATION POLICIES | ALERTS | AUTHENTICATION POLICIES | CORTEX SEARCH SERVICES | DATA METRIC FUNCTIONS | DYNAMIC TABLES | EVENT TABLES | EXTERNAL TABLES | FILE FORMATS | FUNCTIONS | GIT REPOSITORIES | HYBRID TABLES | IMAGE REPOSITORIES | ICEBERG TABLES | MASKING POLICIES | MATERIALIZED VIEWS | MODELS | NETWORK RULES | NOTEBOOKS | PACKAGES POLICIES | PASSWORD POLICIES | PIPES | PROCEDURES | PROJECTION POLICIES | ROW ACCESS POLICIES | SECRETS | SERVICES | SESSION POLICIES | SEQUENCES | SNAPSHOTS | STAGES | STREAMS | TABLES | TAGS | TASKS | VIEWS | STREAMLITS | DATASETS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_type_plural GrantPrivilegesToAccountRole#object_type_plural}
        :param in_database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#in_database GrantPrivilegesToAccountRole#in_database}.
        :param in_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#in_schema GrantPrivilegesToAccountRole#in_schema}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f9b4959bcc1650a186605cea96122be18bf8f58db694d192d84222834932f06)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_type_plural GrantPrivilegesToAccountRole#object_type_plural}
        '''
        result = self._values.get("object_type_plural")
        assert result is not None, "Required property 'object_type_plural' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def in_database(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#in_database GrantPrivilegesToAccountRole#in_database}.'''
        result = self._values.get("in_database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def in_schema(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#in_schema GrantPrivilegesToAccountRole#in_schema}.'''
        result = self._values.get("in_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantPrivilegesToAccountRoleOnSchemaObjectAll(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GrantPrivilegesToAccountRoleOnSchemaObjectAllOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToAccountRole.GrantPrivilegesToAccountRoleOnSchemaObjectAllOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54c1aa6f365147d1b2993b838ea038f12f85d82be9bf4a4260b56050a2d37462)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81a0e8d8d5579b29969abb477b453ae5a467b04bf49dbcbf5dfc9584be21e39f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inDatabase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inSchema")
    def in_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inSchema"))

    @in_schema.setter
    def in_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d37c111989f30f885f98980b3fdc11d9ce855332bb16d9eb023f4b1536480f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectTypePlural")
    def object_type_plural(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectTypePlural"))

    @object_type_plural.setter
    def object_type_plural(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df3dad412c548f1bfd8525566844c155bbbab67090e7b4160d20f4e7538f4a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectTypePlural", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GrantPrivilegesToAccountRoleOnSchemaObjectAll]:
        return typing.cast(typing.Optional[GrantPrivilegesToAccountRoleOnSchemaObjectAll], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GrantPrivilegesToAccountRoleOnSchemaObjectAll],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ed5d8b5099ea080ebec5d3f6b56afb888dd6ce6407133db01093d717c58278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToAccountRole.GrantPrivilegesToAccountRoleOnSchemaObjectFuture",
    jsii_struct_bases=[],
    name_mapping={
        "object_type_plural": "objectTypePlural",
        "in_database": "inDatabase",
        "in_schema": "inSchema",
    },
)
class GrantPrivilegesToAccountRoleOnSchemaObjectFuture:
    def __init__(
        self,
        *,
        object_type_plural: builtins.str,
        in_database: typing.Optional[builtins.str] = None,
        in_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_type_plural: The plural object type of the schema object on which privileges will be granted. Valid values are: ALERTS | AUTHENTICATION POLICIES | DATA METRIC FUNCTIONS | DYNAMIC TABLES | EVENT TABLES | EXTERNAL TABLES | FILE FORMATS | FUNCTIONS | GIT REPOSITORIES | HYBRID TABLES | ICEBERG TABLES | MATERIALIZED VIEWS | MODELS | NETWORK RULES | NOTEBOOKS | PASSWORD POLICIES | PIPES | PROCEDURES | SECRETS | SERVICES | SEQUENCES | SNAPSHOTS | STAGES | STREAMS | TABLES | TASKS | VIEWS | DATASETS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_type_plural GrantPrivilegesToAccountRole#object_type_plural}
        :param in_database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#in_database GrantPrivilegesToAccountRole#in_database}.
        :param in_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#in_schema GrantPrivilegesToAccountRole#in_schema}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00dbb378ae62ccfb2a7ece8b8ae62e07336fd57a841e911220a51335dd22862b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_type_plural GrantPrivilegesToAccountRole#object_type_plural}
        '''
        result = self._values.get("object_type_plural")
        assert result is not None, "Required property 'object_type_plural' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def in_database(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#in_database GrantPrivilegesToAccountRole#in_database}.'''
        result = self._values.get("in_database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def in_schema(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#in_schema GrantPrivilegesToAccountRole#in_schema}.'''
        result = self._values.get("in_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantPrivilegesToAccountRoleOnSchemaObjectFuture(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GrantPrivilegesToAccountRoleOnSchemaObjectFutureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToAccountRole.GrantPrivilegesToAccountRoleOnSchemaObjectFutureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__660b174d944d3e3f582ecb891f288d68195f60a89a0827714a8c30126fd63ad7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05e07c1c3abd1462c44b4910b7109621fc7579afa23ffd28c0b9fbefcb261eba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inDatabase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inSchema")
    def in_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inSchema"))

    @in_schema.setter
    def in_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0497e4dd951f369b85ae8a27daaae03ae7a2985e033f36fa8ee3a98f8c93a255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectTypePlural")
    def object_type_plural(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectTypePlural"))

    @object_type_plural.setter
    def object_type_plural(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12afc1d704770fe71957db5e9d6d47951a6d34cc4733707c4c59d2474257c2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectTypePlural", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GrantPrivilegesToAccountRoleOnSchemaObjectFuture]:
        return typing.cast(typing.Optional[GrantPrivilegesToAccountRoleOnSchemaObjectFuture], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GrantPrivilegesToAccountRoleOnSchemaObjectFuture],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a68acdd150c95c34c4f22f322078fbc306ed4a219342612c7b9387da38e21b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GrantPrivilegesToAccountRoleOnSchemaObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToAccountRole.GrantPrivilegesToAccountRoleOnSchemaObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98d71c2e658516fff02fa3a5fc8ec804bc15b38f5f3b386a3ced42d98089931c)
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
        :param object_type_plural: The plural object type of the schema object on which privileges will be granted. Valid values are: AGGREGATION POLICIES | ALERTS | AUTHENTICATION POLICIES | CORTEX SEARCH SERVICES | DATA METRIC FUNCTIONS | DYNAMIC TABLES | EVENT TABLES | EXTERNAL TABLES | FILE FORMATS | FUNCTIONS | GIT REPOSITORIES | HYBRID TABLES | IMAGE REPOSITORIES | ICEBERG TABLES | MASKING POLICIES | MATERIALIZED VIEWS | MODELS | NETWORK RULES | NOTEBOOKS | PACKAGES POLICIES | PASSWORD POLICIES | PIPES | PROCEDURES | PROJECTION POLICIES | ROW ACCESS POLICIES | SECRETS | SERVICES | SESSION POLICIES | SEQUENCES | SNAPSHOTS | STAGES | STREAMS | TABLES | TAGS | TASKS | VIEWS | STREAMLITS | DATASETS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_type_plural GrantPrivilegesToAccountRole#object_type_plural}
        :param in_database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#in_database GrantPrivilegesToAccountRole#in_database}.
        :param in_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#in_schema GrantPrivilegesToAccountRole#in_schema}.
        '''
        value = GrantPrivilegesToAccountRoleOnSchemaObjectAll(
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
        :param object_type_plural: The plural object type of the schema object on which privileges will be granted. Valid values are: ALERTS | AUTHENTICATION POLICIES | DATA METRIC FUNCTIONS | DYNAMIC TABLES | EVENT TABLES | EXTERNAL TABLES | FILE FORMATS | FUNCTIONS | GIT REPOSITORIES | HYBRID TABLES | ICEBERG TABLES | MATERIALIZED VIEWS | MODELS | NETWORK RULES | NOTEBOOKS | PASSWORD POLICIES | PIPES | PROCEDURES | SECRETS | SERVICES | SEQUENCES | SNAPSHOTS | STAGES | STREAMS | TABLES | TASKS | VIEWS | DATASETS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#object_type_plural GrantPrivilegesToAccountRole#object_type_plural}
        :param in_database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#in_database GrantPrivilegesToAccountRole#in_database}.
        :param in_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/grant_privileges_to_account_role#in_schema GrantPrivilegesToAccountRole#in_schema}.
        '''
        value = GrantPrivilegesToAccountRoleOnSchemaObjectFuture(
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
    def all(self) -> GrantPrivilegesToAccountRoleOnSchemaObjectAllOutputReference:
        return typing.cast(GrantPrivilegesToAccountRoleOnSchemaObjectAllOutputReference, jsii.get(self, "all"))

    @builtins.property
    @jsii.member(jsii_name="future")
    def future(self) -> GrantPrivilegesToAccountRoleOnSchemaObjectFutureOutputReference:
        return typing.cast(GrantPrivilegesToAccountRoleOnSchemaObjectFutureOutputReference, jsii.get(self, "future"))

    @builtins.property
    @jsii.member(jsii_name="allInput")
    def all_input(
        self,
    ) -> typing.Optional[GrantPrivilegesToAccountRoleOnSchemaObjectAll]:
        return typing.cast(typing.Optional[GrantPrivilegesToAccountRoleOnSchemaObjectAll], jsii.get(self, "allInput"))

    @builtins.property
    @jsii.member(jsii_name="futureInput")
    def future_input(
        self,
    ) -> typing.Optional[GrantPrivilegesToAccountRoleOnSchemaObjectFuture]:
        return typing.cast(typing.Optional[GrantPrivilegesToAccountRoleOnSchemaObjectFuture], jsii.get(self, "futureInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__bb9fcfa95199000f29f1a860a79b621f6da5ef0f10ae35c27a46e548b07606e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectType")
    def object_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectType"))

    @object_type.setter
    def object_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__801b403f3da7019c65c5aa07ede797d9b163c0f24679d7d1dbd3c31706d282da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GrantPrivilegesToAccountRoleOnSchemaObject]:
        return typing.cast(typing.Optional[GrantPrivilegesToAccountRoleOnSchemaObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GrantPrivilegesToAccountRoleOnSchemaObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__338c10d672947d68d67ad352ab9d8848809a2c71c6ac4787757a137d8cc1d235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GrantPrivilegesToAccountRoleOnSchemaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.grantPrivilegesToAccountRole.GrantPrivilegesToAccountRoleOnSchemaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a6d8be513687f71776525ae4d82ade2498c950c2e8dfcd6c89dade986a14cea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8024bc45effe8b8013042bc9a63b9001bfb71068619c0148ab920de018d75ccc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allSchemasInDatabase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="futureSchemasInDatabase")
    def future_schemas_in_database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "futureSchemasInDatabase"))

    @future_schemas_in_database.setter
    def future_schemas_in_database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c9ceeea652bc7c99c426a7fa8c3e5775301e4b27967eeb3e61fb8f171c4e675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "futureSchemasInDatabase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schemaName")
    def schema_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaName"))

    @schema_name.setter
    def schema_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c86f0854bfef4dd856a62257b10a707b02b98d19557c443aa355d043bb40e05d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GrantPrivilegesToAccountRoleOnSchema]:
        return typing.cast(typing.Optional[GrantPrivilegesToAccountRoleOnSchema], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GrantPrivilegesToAccountRoleOnSchema],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd21724884042986f7793d1119acbfbcda964fb4d3dc0a5ef2550213ccd14f47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GrantPrivilegesToAccountRole",
    "GrantPrivilegesToAccountRoleConfig",
    "GrantPrivilegesToAccountRoleOnAccountObject",
    "GrantPrivilegesToAccountRoleOnAccountObjectOutputReference",
    "GrantPrivilegesToAccountRoleOnSchema",
    "GrantPrivilegesToAccountRoleOnSchemaObject",
    "GrantPrivilegesToAccountRoleOnSchemaObjectAll",
    "GrantPrivilegesToAccountRoleOnSchemaObjectAllOutputReference",
    "GrantPrivilegesToAccountRoleOnSchemaObjectFuture",
    "GrantPrivilegesToAccountRoleOnSchemaObjectFutureOutputReference",
    "GrantPrivilegesToAccountRoleOnSchemaObjectOutputReference",
    "GrantPrivilegesToAccountRoleOnSchemaOutputReference",
]

publication.publish()

def _typecheckingstub__61a1b5c0efc498aa0a5ec3c37e160f9d9791dbf9fc223c589a2d569fe57976f3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_role_name: builtins.str,
    all_privileges: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    always_apply: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    always_apply_trigger: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    on_account: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    on_account_object: typing.Optional[typing.Union[GrantPrivilegesToAccountRoleOnAccountObject, typing.Dict[builtins.str, typing.Any]]] = None,
    on_schema: typing.Optional[typing.Union[GrantPrivilegesToAccountRoleOnSchema, typing.Dict[builtins.str, typing.Any]]] = None,
    on_schema_object: typing.Optional[typing.Union[GrantPrivilegesToAccountRoleOnSchemaObject, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__fbb0437d7fdb60a1f772a7ca3c3b0cce2dcb3ce90cbc7a2ea7d6a0c9838db5f7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d46360bc5d72806d31f8dd8d0a46fba9e16b436ea60ab0c76d0de61af35d3d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60934c7532fcc1360ac8df165bf0d8e0422908ccdcb7799d712919dd7361aff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__713073909d94537630fef94627d1e726e0717a09f0a74f926f6565a9251669da(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66654cdde8c18a24b8edf6d0c88d2f458cf42ff102a6e33725443858afec2a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ab2890e2cc5f38c74c8bea4ba52d2059a3516b8c9ccfff026535e599a6b0e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe9837294f94afd35215a6646033c651643a5180daf61b1172f47d2eb75ad342(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f724d3edf454539d697fbee7ba82cb8c8d2ded75e2694c23523bb81bba121713(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66b59203dd1fa31d05f9702b79ba256fbf6878af98e3fbfaabf491c51f82a8e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5985946c9d83bd0b5ca0cb3e060c43945ed0c98648765ac15b5023927c85ec(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_role_name: builtins.str,
    all_privileges: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    always_apply: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    always_apply_trigger: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    on_account: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    on_account_object: typing.Optional[typing.Union[GrantPrivilegesToAccountRoleOnAccountObject, typing.Dict[builtins.str, typing.Any]]] = None,
    on_schema: typing.Optional[typing.Union[GrantPrivilegesToAccountRoleOnSchema, typing.Dict[builtins.str, typing.Any]]] = None,
    on_schema_object: typing.Optional[typing.Union[GrantPrivilegesToAccountRoleOnSchemaObject, typing.Dict[builtins.str, typing.Any]]] = None,
    privileges: typing.Optional[typing.Sequence[builtins.str]] = None,
    with_grant_option: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861fe2cce2c2602466faa6646a59aba444110adbe74e8cca588a21e7f9d1e3e4(
    *,
    object_name: builtins.str,
    object_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e40b32d80f4c434211a96dbb7d37115313c4a48df2e6ee339cbcd4fed95a3a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29b3f8bdf2671559f52f3f630e42e65bad384430cc04aa1edff75b2436033fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98fc1eaac18ad53ec3e95282b7b73cfdd7f15a3fab9a39d668689ebc6e680ac6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f23f0c067a43026dd2853943d76e72423dfe76928370b9c5bdb5b3a783d38fa(
    value: typing.Optional[GrantPrivilegesToAccountRoleOnAccountObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8f6140aa5a41d99056f85bf4ce542b028117f7976db91cdeb4733b2e4d44f0(
    *,
    all_schemas_in_database: typing.Optional[builtins.str] = None,
    future_schemas_in_database: typing.Optional[builtins.str] = None,
    schema_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba8a57ce63907e4c92ebfd9f0109d1f22f5e3d6a167865156ac67e754b31919(
    *,
    all: typing.Optional[typing.Union[GrantPrivilegesToAccountRoleOnSchemaObjectAll, typing.Dict[builtins.str, typing.Any]]] = None,
    future: typing.Optional[typing.Union[GrantPrivilegesToAccountRoleOnSchemaObjectFuture, typing.Dict[builtins.str, typing.Any]]] = None,
    object_name: typing.Optional[builtins.str] = None,
    object_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9b4959bcc1650a186605cea96122be18bf8f58db694d192d84222834932f06(
    *,
    object_type_plural: builtins.str,
    in_database: typing.Optional[builtins.str] = None,
    in_schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c1aa6f365147d1b2993b838ea038f12f85d82be9bf4a4260b56050a2d37462(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a0e8d8d5579b29969abb477b453ae5a467b04bf49dbcbf5dfc9584be21e39f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37c111989f30f885f98980b3fdc11d9ce855332bb16d9eb023f4b1536480f40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df3dad412c548f1bfd8525566844c155bbbab67090e7b4160d20f4e7538f4a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ed5d8b5099ea080ebec5d3f6b56afb888dd6ce6407133db01093d717c58278(
    value: typing.Optional[GrantPrivilegesToAccountRoleOnSchemaObjectAll],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00dbb378ae62ccfb2a7ece8b8ae62e07336fd57a841e911220a51335dd22862b(
    *,
    object_type_plural: builtins.str,
    in_database: typing.Optional[builtins.str] = None,
    in_schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660b174d944d3e3f582ecb891f288d68195f60a89a0827714a8c30126fd63ad7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e07c1c3abd1462c44b4910b7109621fc7579afa23ffd28c0b9fbefcb261eba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0497e4dd951f369b85ae8a27daaae03ae7a2985e033f36fa8ee3a98f8c93a255(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12afc1d704770fe71957db5e9d6d47951a6d34cc4733707c4c59d2474257c2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a68acdd150c95c34c4f22f322078fbc306ed4a219342612c7b9387da38e21b9(
    value: typing.Optional[GrantPrivilegesToAccountRoleOnSchemaObjectFuture],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d71c2e658516fff02fa3a5fc8ec804bc15b38f5f3b386a3ced42d98089931c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb9fcfa95199000f29f1a860a79b621f6da5ef0f10ae35c27a46e548b07606e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__801b403f3da7019c65c5aa07ede797d9b163c0f24679d7d1dbd3c31706d282da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338c10d672947d68d67ad352ab9d8848809a2c71c6ac4787757a137d8cc1d235(
    value: typing.Optional[GrantPrivilegesToAccountRoleOnSchemaObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6d8be513687f71776525ae4d82ade2498c950c2e8dfcd6c89dade986a14cea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8024bc45effe8b8013042bc9a63b9001bfb71068619c0148ab920de018d75ccc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9ceeea652bc7c99c426a7fa8c3e5775301e4b27967eeb3e61fb8f171c4e675(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86f0854bfef4dd856a62257b10a707b02b98d19557c443aa355d043bb40e05d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd21724884042986f7793d1119acbfbcda964fb4d3dc0a5ef2550213ccd14f47(
    value: typing.Optional[GrantPrivilegesToAccountRoleOnSchema],
) -> None:
    """Type checking stubs"""
    pass
