r'''
# `postgresql_role`

Refer to the Terraform Registry for docs: [`postgresql_role`](https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role).
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


class Role(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-postgresql.role.Role",
):
    '''Represents a {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role postgresql_role}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        assume_role: typing.Optional[builtins.str] = None,
        bypass_row_level_security: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection_limit: typing.Optional[jsii.Number] = None,
        create_database: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_role: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encrypted: typing.Optional[builtins.str] = None,
        encrypted_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        idle_in_transaction_session_timeout: typing.Optional[jsii.Number] = None,
        inherit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        login: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password: typing.Optional[builtins.str] = None,
        replication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        search_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_drop_role: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_reassign_owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        statement_timeout: typing.Optional[jsii.Number] = None,
        superuser: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        valid_until: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role postgresql_role} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#name Role#name}
        :param assume_role: Role to switch to at login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#assume_role Role#assume_role}
        :param bypass_row_level_security: Determine whether a role bypasses every row-level security (RLS) policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#bypass_row_level_security Role#bypass_row_level_security}
        :param connection_limit: How many concurrent connections can be made with this role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#connection_limit Role#connection_limit}
        :param create_database: Define a role's ability to create databases. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#create_database Role#create_database}
        :param create_role: Determine whether this role will be permitted to create new roles. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#create_role Role#create_role}
        :param encrypted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#encrypted Role#encrypted}.
        :param encrypted_password: Control whether the password is stored encrypted in the system catalogs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#encrypted_password Role#encrypted_password}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#id Role#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param idle_in_transaction_session_timeout: Terminate any session with an open transaction that has been idle for longer than the specified duration in milliseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#idle_in_transaction_session_timeout Role#idle_in_transaction_session_timeout}
        :param inherit: Determine whether a role "inherits" the privileges of roles it is a member of. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#inherit Role#inherit}
        :param login: Determine whether a role is allowed to log in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#login Role#login}
        :param password: Sets the role's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#password Role#password}
        :param replication: Determine whether a role is allowed to initiate streaming replication or put the system in and out of backup mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#replication Role#replication}
        :param roles: Role(s) to grant to this new role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#roles Role#roles}
        :param search_path: Sets the role's search path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#search_path Role#search_path}
        :param skip_drop_role: Skip actually running the DROP ROLE command when removing a ROLE from PostgreSQL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#skip_drop_role Role#skip_drop_role}
        :param skip_reassign_owned: Skip actually running the REASSIGN OWNED command when removing a role from PostgreSQL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#skip_reassign_owned Role#skip_reassign_owned}
        :param statement_timeout: Abort any statement that takes more than the specified number of milliseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#statement_timeout Role#statement_timeout}
        :param superuser: Determine whether the new role is a "superuser". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#superuser Role#superuser}
        :param valid_until: Sets a date and time after which the role's password is no longer valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#valid_until Role#valid_until}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e59e606efc89063192a8fbbf0eef1ef4f13aa567b0011413bb6a2652e7a7b0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RoleConfig(
            name=name,
            assume_role=assume_role,
            bypass_row_level_security=bypass_row_level_security,
            connection_limit=connection_limit,
            create_database=create_database,
            create_role=create_role,
            encrypted=encrypted,
            encrypted_password=encrypted_password,
            id=id,
            idle_in_transaction_session_timeout=idle_in_transaction_session_timeout,
            inherit=inherit,
            login=login,
            password=password,
            replication=replication,
            roles=roles,
            search_path=search_path,
            skip_drop_role=skip_drop_role,
            skip_reassign_owned=skip_reassign_owned,
            statement_timeout=statement_timeout,
            superuser=superuser,
            valid_until=valid_until,
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
        '''Generates CDKTF code for importing a Role resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Role to import.
        :param import_from_id: The id of the existing Role that should be imported. Refer to the {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Role to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ede7005aef4352962b5022970598ebe00c0816f863c21e808f9ef5cffbb9578)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAssumeRole")
    def reset_assume_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssumeRole", []))

    @jsii.member(jsii_name="resetBypassRowLevelSecurity")
    def reset_bypass_row_level_security(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBypassRowLevelSecurity", []))

    @jsii.member(jsii_name="resetConnectionLimit")
    def reset_connection_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionLimit", []))

    @jsii.member(jsii_name="resetCreateDatabase")
    def reset_create_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateDatabase", []))

    @jsii.member(jsii_name="resetCreateRole")
    def reset_create_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateRole", []))

    @jsii.member(jsii_name="resetEncrypted")
    def reset_encrypted(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncrypted", []))

    @jsii.member(jsii_name="resetEncryptedPassword")
    def reset_encrypted_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptedPassword", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdleInTransactionSessionTimeout")
    def reset_idle_in_transaction_session_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleInTransactionSessionTimeout", []))

    @jsii.member(jsii_name="resetInherit")
    def reset_inherit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInherit", []))

    @jsii.member(jsii_name="resetLogin")
    def reset_login(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogin", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetReplication")
    def reset_replication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplication", []))

    @jsii.member(jsii_name="resetRoles")
    def reset_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoles", []))

    @jsii.member(jsii_name="resetSearchPath")
    def reset_search_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearchPath", []))

    @jsii.member(jsii_name="resetSkipDropRole")
    def reset_skip_drop_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipDropRole", []))

    @jsii.member(jsii_name="resetSkipReassignOwned")
    def reset_skip_reassign_owned(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipReassignOwned", []))

    @jsii.member(jsii_name="resetStatementTimeout")
    def reset_statement_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatementTimeout", []))

    @jsii.member(jsii_name="resetSuperuser")
    def reset_superuser(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuperuser", []))

    @jsii.member(jsii_name="resetValidUntil")
    def reset_valid_until(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidUntil", []))

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
    @jsii.member(jsii_name="assumeRoleInput")
    def assume_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assumeRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="bypassRowLevelSecurityInput")
    def bypass_row_level_security_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bypassRowLevelSecurityInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionLimitInput")
    def connection_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "connectionLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="createDatabaseInput")
    def create_database_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "createDatabaseInput"))

    @builtins.property
    @jsii.member(jsii_name="createRoleInput")
    def create_role_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "createRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptedInput")
    def encrypted_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptedInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptedPasswordInput")
    def encrypted_password_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptedPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="idleInTransactionSessionTimeoutInput")
    def idle_in_transaction_session_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "idleInTransactionSessionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="inheritInput")
    def inherit_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "inheritInput"))

    @builtins.property
    @jsii.member(jsii_name="loginInput")
    def login_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "loginInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationInput")
    def replication_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "replicationInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="searchPathInput")
    def search_path_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "searchPathInput"))

    @builtins.property
    @jsii.member(jsii_name="skipDropRoleInput")
    def skip_drop_role_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipDropRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="skipReassignOwnedInput")
    def skip_reassign_owned_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipReassignOwnedInput"))

    @builtins.property
    @jsii.member(jsii_name="statementTimeoutInput")
    def statement_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "statementTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="superuserInput")
    def superuser_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "superuserInput"))

    @builtins.property
    @jsii.member(jsii_name="validUntilInput")
    def valid_until_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "validUntilInput"))

    @builtins.property
    @jsii.member(jsii_name="assumeRole")
    def assume_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assumeRole"))

    @assume_role.setter
    def assume_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e60c036260b4ed8c8d2bdead55834b056e677e63b06fcaafdd29861067f6121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assumeRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bypassRowLevelSecurity")
    def bypass_row_level_security(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bypassRowLevelSecurity"))

    @bypass_row_level_security.setter
    def bypass_row_level_security(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83de1683a55c6cfa8138c3d45d1968912432116737d6935fc158bbc92da9800e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bypassRowLevelSecurity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionLimit")
    def connection_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "connectionLimit"))

    @connection_limit.setter
    def connection_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50818eefe75f6f9b163172bb5bb168f72c767a50eaacb64f67a0482e1156655f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createDatabase")
    def create_database(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "createDatabase"))

    @create_database.setter
    def create_database(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb021cab80e76572ceaa2a05b9fa061d94ae2896b75cce066431bf4eb684398f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createDatabase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createRole")
    def create_role(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "createRole"))

    @create_role.setter
    def create_role(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51c64649c471a227aba309f1ee4e631ad6a2f2c87b0f62ce5dd2dfaa6a3902f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encrypted")
    def encrypted(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encrypted"))

    @encrypted.setter
    def encrypted(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ab1c3b41790613b66ed4166b39ebbcd73359804e58356f8dc989357c1f408d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encrypted", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptedPassword")
    def encrypted_password(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encryptedPassword"))

    @encrypted_password.setter
    def encrypted_password(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3abf905d610e0ed615341af5e5f803ff22c47cd066f45d0d62257b4d6d7f7ddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptedPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b69003949e278ff6cf868eb6e223095eb67f32906078e942c5ebc73ab0e13de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idleInTransactionSessionTimeout")
    def idle_in_transaction_session_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "idleInTransactionSessionTimeout"))

    @idle_in_transaction_session_timeout.setter
    def idle_in_transaction_session_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6275863b051643846ad37f07b1e2c23dcbca3f8e5e51b7afb28665204a5d5584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleInTransactionSessionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inherit")
    def inherit(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "inherit"))

    @inherit.setter
    def inherit(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a1005c181de8108726f53861d8ea27421a8aaa9f546d9663ff2be46721266d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inherit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="login")
    def login(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "login"))

    @login.setter
    def login(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed4322448f665db5a2cac8b00ff8472ce856eb2f0ee74a3207541312321abaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "login", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab1e72eab99bfa466d95d7846a3eda856fc57761800df119d75bb72fd1674c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6275925c734137edec505782509ac8f1b6d2642c5bf99be026ea50c759d21d8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replication")
    def replication(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "replication"))

    @replication.setter
    def replication(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11daced1578a006a1a209214f2d48294648e89a362792bc839c556a3345a28f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a28a7bbdf9bdcd0e5d7c76fd37f89cbc1667a50a01f06d1a1cc899f60ab3f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="searchPath")
    def search_path(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "searchPath"))

    @search_path.setter
    def search_path(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a59f824b5522ebe49b1fe2d4d619e1dd27b894094639582b3c95f2805089b780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipDropRole")
    def skip_drop_role(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipDropRole"))

    @skip_drop_role.setter
    def skip_drop_role(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb0d21498de9c6be832b5826e2d25c228ca0fc187c562d091484d16cd9b2eae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipDropRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipReassignOwned")
    def skip_reassign_owned(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipReassignOwned"))

    @skip_reassign_owned.setter
    def skip_reassign_owned(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a3c26076f2ddac366d5e7ffd9e3c63ac5705a34f87917d0981b09cce3aee0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipReassignOwned", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementTimeout")
    def statement_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statementTimeout"))

    @statement_timeout.setter
    def statement_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b9755b897da851a4529775e09ffdec177e4b237bb4bbc52dc9f99f17df9e52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="superuser")
    def superuser(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "superuser"))

    @superuser.setter
    def superuser(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0227b43350a9160b0e019b5c4a8eabdbc32fdbdc581f8a430325870488758336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "superuser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validUntil")
    def valid_until(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "validUntil"))

    @valid_until.setter
    def valid_until(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73ee0ef2083edaaa577ad969a8503a3eec640141c78fce5f7ce8a67c0f9a449a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validUntil", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-postgresql.role.RoleConfig",
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
        "assume_role": "assumeRole",
        "bypass_row_level_security": "bypassRowLevelSecurity",
        "connection_limit": "connectionLimit",
        "create_database": "createDatabase",
        "create_role": "createRole",
        "encrypted": "encrypted",
        "encrypted_password": "encryptedPassword",
        "id": "id",
        "idle_in_transaction_session_timeout": "idleInTransactionSessionTimeout",
        "inherit": "inherit",
        "login": "login",
        "password": "password",
        "replication": "replication",
        "roles": "roles",
        "search_path": "searchPath",
        "skip_drop_role": "skipDropRole",
        "skip_reassign_owned": "skipReassignOwned",
        "statement_timeout": "statementTimeout",
        "superuser": "superuser",
        "valid_until": "validUntil",
    },
)
class RoleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        assume_role: typing.Optional[builtins.str] = None,
        bypass_row_level_security: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection_limit: typing.Optional[jsii.Number] = None,
        create_database: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_role: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encrypted: typing.Optional[builtins.str] = None,
        encrypted_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        idle_in_transaction_session_timeout: typing.Optional[jsii.Number] = None,
        inherit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        login: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password: typing.Optional[builtins.str] = None,
        replication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        search_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_drop_role: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_reassign_owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        statement_timeout: typing.Optional[jsii.Number] = None,
        superuser: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        valid_until: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#name Role#name}
        :param assume_role: Role to switch to at login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#assume_role Role#assume_role}
        :param bypass_row_level_security: Determine whether a role bypasses every row-level security (RLS) policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#bypass_row_level_security Role#bypass_row_level_security}
        :param connection_limit: How many concurrent connections can be made with this role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#connection_limit Role#connection_limit}
        :param create_database: Define a role's ability to create databases. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#create_database Role#create_database}
        :param create_role: Determine whether this role will be permitted to create new roles. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#create_role Role#create_role}
        :param encrypted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#encrypted Role#encrypted}.
        :param encrypted_password: Control whether the password is stored encrypted in the system catalogs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#encrypted_password Role#encrypted_password}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#id Role#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param idle_in_transaction_session_timeout: Terminate any session with an open transaction that has been idle for longer than the specified duration in milliseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#idle_in_transaction_session_timeout Role#idle_in_transaction_session_timeout}
        :param inherit: Determine whether a role "inherits" the privileges of roles it is a member of. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#inherit Role#inherit}
        :param login: Determine whether a role is allowed to log in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#login Role#login}
        :param password: Sets the role's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#password Role#password}
        :param replication: Determine whether a role is allowed to initiate streaming replication or put the system in and out of backup mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#replication Role#replication}
        :param roles: Role(s) to grant to this new role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#roles Role#roles}
        :param search_path: Sets the role's search path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#search_path Role#search_path}
        :param skip_drop_role: Skip actually running the DROP ROLE command when removing a ROLE from PostgreSQL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#skip_drop_role Role#skip_drop_role}
        :param skip_reassign_owned: Skip actually running the REASSIGN OWNED command when removing a role from PostgreSQL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#skip_reassign_owned Role#skip_reassign_owned}
        :param statement_timeout: Abort any statement that takes more than the specified number of milliseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#statement_timeout Role#statement_timeout}
        :param superuser: Determine whether the new role is a "superuser". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#superuser Role#superuser}
        :param valid_until: Sets a date and time after which the role's password is no longer valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#valid_until Role#valid_until}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acfac6cd9793e31e288a66bfff5e43e65f4432f03ded8a4e3c21227a7a60570f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument assume_role", value=assume_role, expected_type=type_hints["assume_role"])
            check_type(argname="argument bypass_row_level_security", value=bypass_row_level_security, expected_type=type_hints["bypass_row_level_security"])
            check_type(argname="argument connection_limit", value=connection_limit, expected_type=type_hints["connection_limit"])
            check_type(argname="argument create_database", value=create_database, expected_type=type_hints["create_database"])
            check_type(argname="argument create_role", value=create_role, expected_type=type_hints["create_role"])
            check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
            check_type(argname="argument encrypted_password", value=encrypted_password, expected_type=type_hints["encrypted_password"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument idle_in_transaction_session_timeout", value=idle_in_transaction_session_timeout, expected_type=type_hints["idle_in_transaction_session_timeout"])
            check_type(argname="argument inherit", value=inherit, expected_type=type_hints["inherit"])
            check_type(argname="argument login", value=login, expected_type=type_hints["login"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument replication", value=replication, expected_type=type_hints["replication"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument search_path", value=search_path, expected_type=type_hints["search_path"])
            check_type(argname="argument skip_drop_role", value=skip_drop_role, expected_type=type_hints["skip_drop_role"])
            check_type(argname="argument skip_reassign_owned", value=skip_reassign_owned, expected_type=type_hints["skip_reassign_owned"])
            check_type(argname="argument statement_timeout", value=statement_timeout, expected_type=type_hints["statement_timeout"])
            check_type(argname="argument superuser", value=superuser, expected_type=type_hints["superuser"])
            check_type(argname="argument valid_until", value=valid_until, expected_type=type_hints["valid_until"])
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
        if assume_role is not None:
            self._values["assume_role"] = assume_role
        if bypass_row_level_security is not None:
            self._values["bypass_row_level_security"] = bypass_row_level_security
        if connection_limit is not None:
            self._values["connection_limit"] = connection_limit
        if create_database is not None:
            self._values["create_database"] = create_database
        if create_role is not None:
            self._values["create_role"] = create_role
        if encrypted is not None:
            self._values["encrypted"] = encrypted
        if encrypted_password is not None:
            self._values["encrypted_password"] = encrypted_password
        if id is not None:
            self._values["id"] = id
        if idle_in_transaction_session_timeout is not None:
            self._values["idle_in_transaction_session_timeout"] = idle_in_transaction_session_timeout
        if inherit is not None:
            self._values["inherit"] = inherit
        if login is not None:
            self._values["login"] = login
        if password is not None:
            self._values["password"] = password
        if replication is not None:
            self._values["replication"] = replication
        if roles is not None:
            self._values["roles"] = roles
        if search_path is not None:
            self._values["search_path"] = search_path
        if skip_drop_role is not None:
            self._values["skip_drop_role"] = skip_drop_role
        if skip_reassign_owned is not None:
            self._values["skip_reassign_owned"] = skip_reassign_owned
        if statement_timeout is not None:
            self._values["statement_timeout"] = statement_timeout
        if superuser is not None:
            self._values["superuser"] = superuser
        if valid_until is not None:
            self._values["valid_until"] = valid_until

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
        '''The name of the role.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#name Role#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def assume_role(self) -> typing.Optional[builtins.str]:
        '''Role to switch to at login.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#assume_role Role#assume_role}
        '''
        result = self._values.get("assume_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bypass_row_level_security(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine whether a role bypasses every row-level security (RLS) policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#bypass_row_level_security Role#bypass_row_level_security}
        '''
        result = self._values.get("bypass_row_level_security")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def connection_limit(self) -> typing.Optional[jsii.Number]:
        '''How many concurrent connections can be made with this role.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#connection_limit Role#connection_limit}
        '''
        result = self._values.get("connection_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def create_database(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Define a role's ability to create databases.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#create_database Role#create_database}
        '''
        result = self._values.get("create_database")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def create_role(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine whether this role will be permitted to create new roles.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#create_role Role#create_role}
        '''
        result = self._values.get("create_role")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encrypted(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#encrypted Role#encrypted}.'''
        result = self._values.get("encrypted")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encrypted_password(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Control whether the password is stored encrypted in the system catalogs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#encrypted_password Role#encrypted_password}
        '''
        result = self._values.get("encrypted_password")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#id Role#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_in_transaction_session_timeout(self) -> typing.Optional[jsii.Number]:
        '''Terminate any session with an open transaction that has been idle for longer than the specified duration in milliseconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#idle_in_transaction_session_timeout Role#idle_in_transaction_session_timeout}
        '''
        result = self._values.get("idle_in_transaction_session_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def inherit(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine whether a role "inherits" the privileges of roles it is a member of.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#inherit Role#inherit}
        '''
        result = self._values.get("inherit")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def login(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine whether a role is allowed to log in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#login Role#login}
        '''
        result = self._values.get("login")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Sets the role's password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#password Role#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine whether a role is allowed to initiate streaming replication or put the system in and out of backup mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#replication Role#replication}
        '''
        result = self._values.get("replication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Role(s) to grant to this new role.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#roles Role#roles}
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def search_path(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Sets the role's search path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#search_path Role#search_path}
        '''
        result = self._values.get("search_path")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def skip_drop_role(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Skip actually running the DROP ROLE command when removing a ROLE from PostgreSQL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#skip_drop_role Role#skip_drop_role}
        '''
        result = self._values.get("skip_drop_role")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_reassign_owned(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Skip actually running the REASSIGN OWNED command when removing a role from PostgreSQL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#skip_reassign_owned Role#skip_reassign_owned}
        '''
        result = self._values.get("skip_reassign_owned")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def statement_timeout(self) -> typing.Optional[jsii.Number]:
        '''Abort any statement that takes more than the specified number of milliseconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#statement_timeout Role#statement_timeout}
        '''
        result = self._values.get("statement_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def superuser(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine whether the new role is a "superuser".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#superuser Role#superuser}
        '''
        result = self._values.get("superuser")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def valid_until(self) -> typing.Optional[builtins.str]:
        '''Sets a date and time after which the role's password is no longer valid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/resources/role#valid_until Role#valid_until}
        '''
        result = self._values.get("valid_until")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Role",
    "RoleConfig",
]

publication.publish()

def _typecheckingstub__34e59e606efc89063192a8fbbf0eef1ef4f13aa567b0011413bb6a2652e7a7b0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    assume_role: typing.Optional[builtins.str] = None,
    bypass_row_level_security: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    connection_limit: typing.Optional[jsii.Number] = None,
    create_database: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    create_role: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encrypted: typing.Optional[builtins.str] = None,
    encrypted_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    idle_in_transaction_session_timeout: typing.Optional[jsii.Number] = None,
    inherit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    login: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password: typing.Optional[builtins.str] = None,
    replication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    search_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_drop_role: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_reassign_owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    statement_timeout: typing.Optional[jsii.Number] = None,
    superuser: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    valid_until: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__0ede7005aef4352962b5022970598ebe00c0816f863c21e808f9ef5cffbb9578(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e60c036260b4ed8c8d2bdead55834b056e677e63b06fcaafdd29861067f6121(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83de1683a55c6cfa8138c3d45d1968912432116737d6935fc158bbc92da9800e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50818eefe75f6f9b163172bb5bb168f72c767a50eaacb64f67a0482e1156655f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb021cab80e76572ceaa2a05b9fa061d94ae2896b75cce066431bf4eb684398f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c64649c471a227aba309f1ee4e631ad6a2f2c87b0f62ce5dd2dfaa6a3902f7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ab1c3b41790613b66ed4166b39ebbcd73359804e58356f8dc989357c1f408d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3abf905d610e0ed615341af5e5f803ff22c47cd066f45d0d62257b4d6d7f7ddb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b69003949e278ff6cf868eb6e223095eb67f32906078e942c5ebc73ab0e13de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6275863b051643846ad37f07b1e2c23dcbca3f8e5e51b7afb28665204a5d5584(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a1005c181de8108726f53861d8ea27421a8aaa9f546d9663ff2be46721266d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed4322448f665db5a2cac8b00ff8472ce856eb2f0ee74a3207541312321abaa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab1e72eab99bfa466d95d7846a3eda856fc57761800df119d75bb72fd1674c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6275925c734137edec505782509ac8f1b6d2642c5bf99be026ea50c759d21d8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11daced1578a006a1a209214f2d48294648e89a362792bc839c556a3345a28f1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a28a7bbdf9bdcd0e5d7c76fd37f89cbc1667a50a01f06d1a1cc899f60ab3f5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a59f824b5522ebe49b1fe2d4d619e1dd27b894094639582b3c95f2805089b780(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb0d21498de9c6be832b5826e2d25c228ca0fc187c562d091484d16cd9b2eae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a3c26076f2ddac366d5e7ffd9e3c63ac5705a34f87917d0981b09cce3aee0a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b9755b897da851a4529775e09ffdec177e4b237bb4bbc52dc9f99f17df9e52(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0227b43350a9160b0e019b5c4a8eabdbc32fdbdc581f8a430325870488758336(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ee0ef2083edaaa577ad969a8503a3eec640141c78fce5f7ce8a67c0f9a449a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfac6cd9793e31e288a66bfff5e43e65f4432f03ded8a4e3c21227a7a60570f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    assume_role: typing.Optional[builtins.str] = None,
    bypass_row_level_security: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    connection_limit: typing.Optional[jsii.Number] = None,
    create_database: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    create_role: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encrypted: typing.Optional[builtins.str] = None,
    encrypted_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    idle_in_transaction_session_timeout: typing.Optional[jsii.Number] = None,
    inherit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    login: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password: typing.Optional[builtins.str] = None,
    replication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    search_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_drop_role: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_reassign_owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    statement_timeout: typing.Optional[jsii.Number] = None,
    superuser: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    valid_until: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
