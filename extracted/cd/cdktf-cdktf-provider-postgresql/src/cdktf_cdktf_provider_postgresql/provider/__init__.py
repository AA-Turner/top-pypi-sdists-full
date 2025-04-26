r'''
# `provider`

Refer to the Terraform Registry for docs: [`postgresql`](https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs).
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


class PostgresqlProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-postgresql.provider.PostgresqlProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs postgresql}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
        aws_rds_iam_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        aws_rds_iam_profile: typing.Optional[builtins.str] = None,
        aws_rds_iam_provider_role_arn: typing.Optional[builtins.str] = None,
        aws_rds_iam_region: typing.Optional[builtins.str] = None,
        azure_identity_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        azure_tenant_id: typing.Optional[builtins.str] = None,
        clientcert: typing.Optional[typing.Union["PostgresqlProviderClientcert", typing.Dict[builtins.str, typing.Any]]] = None,
        connect_timeout: typing.Optional[jsii.Number] = None,
        database: typing.Optional[builtins.str] = None,
        database_username: typing.Optional[builtins.str] = None,
        expected_version: typing.Optional[builtins.str] = None,
        gcp_iam_impersonate_service_account: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        max_connections: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        scheme: typing.Optional[builtins.str] = None,
        sslmode: typing.Optional[builtins.str] = None,
        ssl_mode: typing.Optional[builtins.str] = None,
        sslrootcert: typing.Optional[builtins.str] = None,
        superuser: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs postgresql} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#alias PostgresqlProvider#alias}
        :param aws_rds_iam_auth: Use rds_iam instead of password authentication (see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#aws_rds_iam_auth PostgresqlProvider#aws_rds_iam_auth}
        :param aws_rds_iam_profile: AWS profile to use for IAM auth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#aws_rds_iam_profile PostgresqlProvider#aws_rds_iam_profile}
        :param aws_rds_iam_provider_role_arn: AWS IAM role to assume for IAM auth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#aws_rds_iam_provider_role_arn PostgresqlProvider#aws_rds_iam_provider_role_arn}
        :param aws_rds_iam_region: AWS region to use for IAM auth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#aws_rds_iam_region PostgresqlProvider#aws_rds_iam_region}
        :param azure_identity_auth: Use MS Azure identity OAuth token (see: https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/how-to-configure-sign-in-azure-ad-authentication). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#azure_identity_auth PostgresqlProvider#azure_identity_auth}
        :param azure_tenant_id: MS Azure tenant ID (see: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/client_config.html). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#azure_tenant_id PostgresqlProvider#azure_tenant_id}
        :param clientcert: clientcert block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#clientcert PostgresqlProvider#clientcert}
        :param connect_timeout: Maximum wait for connection, in seconds. Zero or not specified means wait indefinitely. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#connect_timeout PostgresqlProvider#connect_timeout}
        :param database: The name of the database to connect to in order to conenct to (defaults to ``postgres``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#database PostgresqlProvider#database}
        :param database_username: Database username associated to the connected user (for user name maps). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#database_username PostgresqlProvider#database_username}
        :param expected_version: Specify the expected version of PostgreSQL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#expected_version PostgresqlProvider#expected_version}
        :param gcp_iam_impersonate_service_account: Service account to impersonate when using GCP IAM authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#gcp_iam_impersonate_service_account PostgresqlProvider#gcp_iam_impersonate_service_account}
        :param host: Name of PostgreSQL server address to connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#host PostgresqlProvider#host}
        :param max_connections: Maximum number of connections to establish to the database. Zero means unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#max_connections PostgresqlProvider#max_connections}
        :param password: Password to be used if the PostgreSQL server demands password authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#password PostgresqlProvider#password}
        :param port: The PostgreSQL port number to connect to at the server host, or socket file name extension for Unix-domain connections. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#port PostgresqlProvider#port}
        :param scheme: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#scheme PostgresqlProvider#scheme}.
        :param sslmode: This option determines whether or with what priority a secure SSL TCP/IP connection will be negotiated with the PostgreSQL server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#sslmode PostgresqlProvider#sslmode}
        :param ssl_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#ssl_mode PostgresqlProvider#ssl_mode}.
        :param sslrootcert: The SSL server root certificate file path. The file must contain PEM encoded data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#sslrootcert PostgresqlProvider#sslrootcert}
        :param superuser: Specify if the user to connect as is a Postgres superuser or not.If not, some feature might be disabled (e.g.: Refreshing state password from Postgres). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#superuser PostgresqlProvider#superuser}
        :param username: PostgreSQL user name to connect as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#username PostgresqlProvider#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873dda44896731f3ed4ac28494dd70199e52e0d56618c8331c8cac2815eb1e7b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = PostgresqlProviderConfig(
            alias=alias,
            aws_rds_iam_auth=aws_rds_iam_auth,
            aws_rds_iam_profile=aws_rds_iam_profile,
            aws_rds_iam_provider_role_arn=aws_rds_iam_provider_role_arn,
            aws_rds_iam_region=aws_rds_iam_region,
            azure_identity_auth=azure_identity_auth,
            azure_tenant_id=azure_tenant_id,
            clientcert=clientcert,
            connect_timeout=connect_timeout,
            database=database,
            database_username=database_username,
            expected_version=expected_version,
            gcp_iam_impersonate_service_account=gcp_iam_impersonate_service_account,
            host=host,
            max_connections=max_connections,
            password=password,
            port=port,
            scheme=scheme,
            sslmode=sslmode,
            ssl_mode=ssl_mode,
            sslrootcert=sslrootcert,
            superuser=superuser,
            username=username,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a PostgresqlProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PostgresqlProvider to import.
        :param import_from_id: The id of the existing PostgresqlProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PostgresqlProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__294081ad4cecc88cd29ad89d8e75399fa18b9777f88d4e977b88e635f9e49876)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetAwsRdsIamAuth")
    def reset_aws_rds_iam_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRdsIamAuth", []))

    @jsii.member(jsii_name="resetAwsRdsIamProfile")
    def reset_aws_rds_iam_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRdsIamProfile", []))

    @jsii.member(jsii_name="resetAwsRdsIamProviderRoleArn")
    def reset_aws_rds_iam_provider_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRdsIamProviderRoleArn", []))

    @jsii.member(jsii_name="resetAwsRdsIamRegion")
    def reset_aws_rds_iam_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRdsIamRegion", []))

    @jsii.member(jsii_name="resetAzureIdentityAuth")
    def reset_azure_identity_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureIdentityAuth", []))

    @jsii.member(jsii_name="resetAzureTenantId")
    def reset_azure_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureTenantId", []))

    @jsii.member(jsii_name="resetClientcert")
    def reset_clientcert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientcert", []))

    @jsii.member(jsii_name="resetConnectTimeout")
    def reset_connect_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectTimeout", []))

    @jsii.member(jsii_name="resetDatabase")
    def reset_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabase", []))

    @jsii.member(jsii_name="resetDatabaseUsername")
    def reset_database_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseUsername", []))

    @jsii.member(jsii_name="resetExpectedVersion")
    def reset_expected_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpectedVersion", []))

    @jsii.member(jsii_name="resetGcpIamImpersonateServiceAccount")
    def reset_gcp_iam_impersonate_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpIamImpersonateServiceAccount", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetMaxConnections")
    def reset_max_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConnections", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetScheme")
    def reset_scheme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheme", []))

    @jsii.member(jsii_name="resetSslmode")
    def reset_sslmode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslmode", []))

    @jsii.member(jsii_name="resetSslMode")
    def reset_ssl_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslMode", []))

    @jsii.member(jsii_name="resetSslrootcert")
    def reset_sslrootcert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslrootcert", []))

    @jsii.member(jsii_name="resetSuperuser")
    def reset_superuser(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuperuser", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

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
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRdsIamAuthInput")
    def aws_rds_iam_auth_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "awsRdsIamAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRdsIamProfileInput")
    def aws_rds_iam_profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRdsIamProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRdsIamProviderRoleArnInput")
    def aws_rds_iam_provider_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRdsIamProviderRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRdsIamRegionInput")
    def aws_rds_iam_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRdsIamRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="azureIdentityAuthInput")
    def azure_identity_auth_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "azureIdentityAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="azureTenantIdInput")
    def azure_tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureTenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientcertInput")
    def clientcert_input(self) -> typing.Optional["PostgresqlProviderClientcert"]:
        return typing.cast(typing.Optional["PostgresqlProviderClientcert"], jsii.get(self, "clientcertInput"))

    @builtins.property
    @jsii.member(jsii_name="connectTimeoutInput")
    def connect_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "connectTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseUsernameInput")
    def database_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="expectedVersionInput")
    def expected_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expectedVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpIamImpersonateServiceAccountInput")
    def gcp_iam_impersonate_service_account_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpIamImpersonateServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnectionsInput")
    def max_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="schemeInput")
    def scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemeInput"))

    @builtins.property
    @jsii.member(jsii_name="sslmodeInput")
    def sslmode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslmodeInput"))

    @builtins.property
    @jsii.member(jsii_name="sslModeInput")
    def ssl_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslModeInput"))

    @builtins.property
    @jsii.member(jsii_name="sslrootcertInput")
    def sslrootcert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslrootcertInput"))

    @builtins.property
    @jsii.member(jsii_name="superuserInput")
    def superuser_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "superuserInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc0f2b6c6f6f94b52d4c7648d7c745cbc1a338dcdaec6a66c040984db8eb83a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="awsRdsIamAuth")
    def aws_rds_iam_auth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "awsRdsIamAuth"))

    @aws_rds_iam_auth.setter
    def aws_rds_iam_auth(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc62e854be1beb6aa7978c09901437eb95114712c03376964c9f66d4a60e24cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRdsIamAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="awsRdsIamProfile")
    def aws_rds_iam_profile(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRdsIamProfile"))

    @aws_rds_iam_profile.setter
    def aws_rds_iam_profile(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b173d3edc65c9c3552ccf4498d35f0d9129d15536427a8794bf01d43f01a3a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRdsIamProfile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="awsRdsIamProviderRoleArn")
    def aws_rds_iam_provider_role_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRdsIamProviderRoleArn"))

    @aws_rds_iam_provider_role_arn.setter
    def aws_rds_iam_provider_role_arn(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fa115a053eed9e507d181bc20bd0e955153f99ff9eddb710951b59ea19ac7b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRdsIamProviderRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="awsRdsIamRegion")
    def aws_rds_iam_region(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRdsIamRegion"))

    @aws_rds_iam_region.setter
    def aws_rds_iam_region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a68d986cc9908ca93ffff3232b82c8d10cb6db9f7c861517afe3deb72aa7f226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRdsIamRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="azureIdentityAuth")
    def azure_identity_auth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "azureIdentityAuth"))

    @azure_identity_auth.setter
    def azure_identity_auth(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b83c13c54d92c5ea76c516de42843fbf68da2f6619da5e0626b5258a5935ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureIdentityAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="azureTenantId")
    def azure_tenant_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureTenantId"))

    @azure_tenant_id.setter
    def azure_tenant_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3127998d537c3e8e585b86f0880a30891fe353d506acfbac7b7e87848d3ee04c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureTenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientcert")
    def clientcert(self) -> typing.Optional["PostgresqlProviderClientcert"]:
        return typing.cast(typing.Optional["PostgresqlProviderClientcert"], jsii.get(self, "clientcert"))

    @clientcert.setter
    def clientcert(
        self,
        value: typing.Optional["PostgresqlProviderClientcert"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de48e1759bfb9c4eba5f859b5657087318c26150d30749a751edd55175846b83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientcert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectTimeout")
    def connect_timeout(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "connectTimeout"))

    @connect_timeout.setter
    def connect_timeout(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c904c7d078952dc0b092e5e5e58c15afac166b970d3002612e3c3031fe3a46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "database"))

    @database.setter
    def database(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc54f4a58a539e3f45798ed76298e1104edc9948a353d2e241542b6bc7e2ef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseUsername")
    def database_username(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseUsername"))

    @database_username.setter
    def database_username(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57d9a6232c3ee2451eac4bcf47dee1bb29cc64168d773a486cc028349797c6e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expectedVersion")
    def expected_version(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expectedVersion"))

    @expected_version.setter
    def expected_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcff7c2f8acf9e2548230b4c1d62e39b9371607e4b2d946625ad4d1280512767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expectedVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcpIamImpersonateServiceAccount")
    def gcp_iam_impersonate_service_account(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpIamImpersonateServiceAccount"))

    @gcp_iam_impersonate_service_account.setter
    def gcp_iam_impersonate_service_account(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d6b09d9e36957e1ca6d2410fb95572c136e90b7e7fa0348e386ee4a09dde84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpIamImpersonateServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "host"))

    @host.setter
    def host(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f13c807cf51e1d04e68dde241ad0ee60c86c1f11a4108a22100d084a6a267c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConnections")
    def max_connections(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnections"))

    @max_connections.setter
    def max_connections(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbdad577b7593c5b15cb3aa112227b532f4af2a590a2c157345983d23b1ad9df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "password"))

    @password.setter
    def password(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b3f48ed7fdd396b191b2e0fabd390014cdd5dc5ff9b29854372610c02b993e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "port"))

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0186590d259d14f8769676cadfb819518e6ee3766eab90c95d14f134fa386203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheme"))

    @scheme.setter
    def scheme(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d37316260fd15fa42b191235c36ae0adb72e4e6efa10a6481aba0a18f5aaab85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslmode")
    def sslmode(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslmode"))

    @sslmode.setter
    def sslmode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825b3e3cff1f8852f807c11f8b58388de7c44ec41855bf527387df68e18df9b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslmode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslMode")
    def ssl_mode(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslMode"))

    @ssl_mode.setter
    def ssl_mode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7dc8c36733660e5c4fda40f09057707d7c8e0d20257fc8e9fc3776a2eb5208)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslrootcert")
    def sslrootcert(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslrootcert"))

    @sslrootcert.setter
    def sslrootcert(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d16fe1571b837ab905976d3dd0540fd3c84eaf89fb69bc720d90a755981b131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslrootcert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="superuser")
    def superuser(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "superuser"))

    @superuser.setter
    def superuser(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72033df84f4029db4a39f6b615083b89a815275c8f819ce405e95de0ac023977)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "superuser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "username"))

    @username.setter
    def username(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8850823304003c1baa5b2ec921306724929385ee5617191fb0d24c1516b41d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-postgresql.provider.PostgresqlProviderClientcert",
    jsii_struct_bases=[],
    name_mapping={"cert": "cert", "key": "key", "sslinline": "sslinline"},
)
class PostgresqlProviderClientcert:
    def __init__(
        self,
        *,
        cert: builtins.str,
        key: builtins.str,
        sslinline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cert: The SSL client certificate file path. The file must contain PEM encoded data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#cert PostgresqlProvider#cert}
        :param key: The SSL client certificate private key file path. The file must contain PEM encoded data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#key PostgresqlProvider#key}
        :param sslinline: Must be set to true if you are inlining the cert/key instead of using a file path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#sslinline PostgresqlProvider#sslinline}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17fff281aae5956890689f9551e028540c4b095ea7e40dfc387ca3f724da72f6)
            check_type(argname="argument cert", value=cert, expected_type=type_hints["cert"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument sslinline", value=sslinline, expected_type=type_hints["sslinline"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cert": cert,
            "key": key,
        }
        if sslinline is not None:
            self._values["sslinline"] = sslinline

    @builtins.property
    def cert(self) -> builtins.str:
        '''The SSL client certificate file path. The file must contain PEM encoded data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#cert PostgresqlProvider#cert}
        '''
        result = self._values.get("cert")
        assert result is not None, "Required property 'cert' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''The SSL client certificate private key file path. The file must contain PEM encoded data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#key PostgresqlProvider#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sslinline(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Must be set to true if you are inlining the cert/key instead of using a file path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#sslinline PostgresqlProvider#sslinline}
        '''
        result = self._values.get("sslinline")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PostgresqlProviderClientcert(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-postgresql.provider.PostgresqlProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "aws_rds_iam_auth": "awsRdsIamAuth",
        "aws_rds_iam_profile": "awsRdsIamProfile",
        "aws_rds_iam_provider_role_arn": "awsRdsIamProviderRoleArn",
        "aws_rds_iam_region": "awsRdsIamRegion",
        "azure_identity_auth": "azureIdentityAuth",
        "azure_tenant_id": "azureTenantId",
        "clientcert": "clientcert",
        "connect_timeout": "connectTimeout",
        "database": "database",
        "database_username": "databaseUsername",
        "expected_version": "expectedVersion",
        "gcp_iam_impersonate_service_account": "gcpIamImpersonateServiceAccount",
        "host": "host",
        "max_connections": "maxConnections",
        "password": "password",
        "port": "port",
        "scheme": "scheme",
        "sslmode": "sslmode",
        "ssl_mode": "sslMode",
        "sslrootcert": "sslrootcert",
        "superuser": "superuser",
        "username": "username",
    },
)
class PostgresqlProviderConfig:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        aws_rds_iam_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        aws_rds_iam_profile: typing.Optional[builtins.str] = None,
        aws_rds_iam_provider_role_arn: typing.Optional[builtins.str] = None,
        aws_rds_iam_region: typing.Optional[builtins.str] = None,
        azure_identity_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        azure_tenant_id: typing.Optional[builtins.str] = None,
        clientcert: typing.Optional[typing.Union[PostgresqlProviderClientcert, typing.Dict[builtins.str, typing.Any]]] = None,
        connect_timeout: typing.Optional[jsii.Number] = None,
        database: typing.Optional[builtins.str] = None,
        database_username: typing.Optional[builtins.str] = None,
        expected_version: typing.Optional[builtins.str] = None,
        gcp_iam_impersonate_service_account: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        max_connections: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        scheme: typing.Optional[builtins.str] = None,
        sslmode: typing.Optional[builtins.str] = None,
        ssl_mode: typing.Optional[builtins.str] = None,
        sslrootcert: typing.Optional[builtins.str] = None,
        superuser: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#alias PostgresqlProvider#alias}
        :param aws_rds_iam_auth: Use rds_iam instead of password authentication (see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#aws_rds_iam_auth PostgresqlProvider#aws_rds_iam_auth}
        :param aws_rds_iam_profile: AWS profile to use for IAM auth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#aws_rds_iam_profile PostgresqlProvider#aws_rds_iam_profile}
        :param aws_rds_iam_provider_role_arn: AWS IAM role to assume for IAM auth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#aws_rds_iam_provider_role_arn PostgresqlProvider#aws_rds_iam_provider_role_arn}
        :param aws_rds_iam_region: AWS region to use for IAM auth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#aws_rds_iam_region PostgresqlProvider#aws_rds_iam_region}
        :param azure_identity_auth: Use MS Azure identity OAuth token (see: https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/how-to-configure-sign-in-azure-ad-authentication). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#azure_identity_auth PostgresqlProvider#azure_identity_auth}
        :param azure_tenant_id: MS Azure tenant ID (see: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/client_config.html). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#azure_tenant_id PostgresqlProvider#azure_tenant_id}
        :param clientcert: clientcert block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#clientcert PostgresqlProvider#clientcert}
        :param connect_timeout: Maximum wait for connection, in seconds. Zero or not specified means wait indefinitely. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#connect_timeout PostgresqlProvider#connect_timeout}
        :param database: The name of the database to connect to in order to conenct to (defaults to ``postgres``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#database PostgresqlProvider#database}
        :param database_username: Database username associated to the connected user (for user name maps). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#database_username PostgresqlProvider#database_username}
        :param expected_version: Specify the expected version of PostgreSQL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#expected_version PostgresqlProvider#expected_version}
        :param gcp_iam_impersonate_service_account: Service account to impersonate when using GCP IAM authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#gcp_iam_impersonate_service_account PostgresqlProvider#gcp_iam_impersonate_service_account}
        :param host: Name of PostgreSQL server address to connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#host PostgresqlProvider#host}
        :param max_connections: Maximum number of connections to establish to the database. Zero means unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#max_connections PostgresqlProvider#max_connections}
        :param password: Password to be used if the PostgreSQL server demands password authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#password PostgresqlProvider#password}
        :param port: The PostgreSQL port number to connect to at the server host, or socket file name extension for Unix-domain connections. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#port PostgresqlProvider#port}
        :param scheme: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#scheme PostgresqlProvider#scheme}.
        :param sslmode: This option determines whether or with what priority a secure SSL TCP/IP connection will be negotiated with the PostgreSQL server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#sslmode PostgresqlProvider#sslmode}
        :param ssl_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#ssl_mode PostgresqlProvider#ssl_mode}.
        :param sslrootcert: The SSL server root certificate file path. The file must contain PEM encoded data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#sslrootcert PostgresqlProvider#sslrootcert}
        :param superuser: Specify if the user to connect as is a Postgres superuser or not.If not, some feature might be disabled (e.g.: Refreshing state password from Postgres). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#superuser PostgresqlProvider#superuser}
        :param username: PostgreSQL user name to connect as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#username PostgresqlProvider#username}
        '''
        if isinstance(clientcert, dict):
            clientcert = PostgresqlProviderClientcert(**clientcert)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af0cedc5a2e044ea705446ddbefd2a58e4b5080becd8b24f22f9c36fa4d87d5f)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument aws_rds_iam_auth", value=aws_rds_iam_auth, expected_type=type_hints["aws_rds_iam_auth"])
            check_type(argname="argument aws_rds_iam_profile", value=aws_rds_iam_profile, expected_type=type_hints["aws_rds_iam_profile"])
            check_type(argname="argument aws_rds_iam_provider_role_arn", value=aws_rds_iam_provider_role_arn, expected_type=type_hints["aws_rds_iam_provider_role_arn"])
            check_type(argname="argument aws_rds_iam_region", value=aws_rds_iam_region, expected_type=type_hints["aws_rds_iam_region"])
            check_type(argname="argument azure_identity_auth", value=azure_identity_auth, expected_type=type_hints["azure_identity_auth"])
            check_type(argname="argument azure_tenant_id", value=azure_tenant_id, expected_type=type_hints["azure_tenant_id"])
            check_type(argname="argument clientcert", value=clientcert, expected_type=type_hints["clientcert"])
            check_type(argname="argument connect_timeout", value=connect_timeout, expected_type=type_hints["connect_timeout"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument database_username", value=database_username, expected_type=type_hints["database_username"])
            check_type(argname="argument expected_version", value=expected_version, expected_type=type_hints["expected_version"])
            check_type(argname="argument gcp_iam_impersonate_service_account", value=gcp_iam_impersonate_service_account, expected_type=type_hints["gcp_iam_impersonate_service_account"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument max_connections", value=max_connections, expected_type=type_hints["max_connections"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
            check_type(argname="argument sslmode", value=sslmode, expected_type=type_hints["sslmode"])
            check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
            check_type(argname="argument sslrootcert", value=sslrootcert, expected_type=type_hints["sslrootcert"])
            check_type(argname="argument superuser", value=superuser, expected_type=type_hints["superuser"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if aws_rds_iam_auth is not None:
            self._values["aws_rds_iam_auth"] = aws_rds_iam_auth
        if aws_rds_iam_profile is not None:
            self._values["aws_rds_iam_profile"] = aws_rds_iam_profile
        if aws_rds_iam_provider_role_arn is not None:
            self._values["aws_rds_iam_provider_role_arn"] = aws_rds_iam_provider_role_arn
        if aws_rds_iam_region is not None:
            self._values["aws_rds_iam_region"] = aws_rds_iam_region
        if azure_identity_auth is not None:
            self._values["azure_identity_auth"] = azure_identity_auth
        if azure_tenant_id is not None:
            self._values["azure_tenant_id"] = azure_tenant_id
        if clientcert is not None:
            self._values["clientcert"] = clientcert
        if connect_timeout is not None:
            self._values["connect_timeout"] = connect_timeout
        if database is not None:
            self._values["database"] = database
        if database_username is not None:
            self._values["database_username"] = database_username
        if expected_version is not None:
            self._values["expected_version"] = expected_version
        if gcp_iam_impersonate_service_account is not None:
            self._values["gcp_iam_impersonate_service_account"] = gcp_iam_impersonate_service_account
        if host is not None:
            self._values["host"] = host
        if max_connections is not None:
            self._values["max_connections"] = max_connections
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if scheme is not None:
            self._values["scheme"] = scheme
        if sslmode is not None:
            self._values["sslmode"] = sslmode
        if ssl_mode is not None:
            self._values["ssl_mode"] = ssl_mode
        if sslrootcert is not None:
            self._values["sslrootcert"] = sslrootcert
        if superuser is not None:
            self._values["superuser"] = superuser
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#alias PostgresqlProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_rds_iam_auth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use rds_iam instead of password authentication (see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#aws_rds_iam_auth PostgresqlProvider#aws_rds_iam_auth}
        '''
        result = self._values.get("aws_rds_iam_auth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def aws_rds_iam_profile(self) -> typing.Optional[builtins.str]:
        '''AWS profile to use for IAM auth.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#aws_rds_iam_profile PostgresqlProvider#aws_rds_iam_profile}
        '''
        result = self._values.get("aws_rds_iam_profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_rds_iam_provider_role_arn(self) -> typing.Optional[builtins.str]:
        '''AWS IAM role to assume for IAM auth.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#aws_rds_iam_provider_role_arn PostgresqlProvider#aws_rds_iam_provider_role_arn}
        '''
        result = self._values.get("aws_rds_iam_provider_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_rds_iam_region(self) -> typing.Optional[builtins.str]:
        '''AWS region to use for IAM auth.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#aws_rds_iam_region PostgresqlProvider#aws_rds_iam_region}
        '''
        result = self._values.get("aws_rds_iam_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure_identity_auth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use MS Azure identity OAuth token (see: https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/how-to-configure-sign-in-azure-ad-authentication).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#azure_identity_auth PostgresqlProvider#azure_identity_auth}
        '''
        result = self._values.get("azure_identity_auth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def azure_tenant_id(self) -> typing.Optional[builtins.str]:
        '''MS Azure tenant ID (see: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/client_config.html).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#azure_tenant_id PostgresqlProvider#azure_tenant_id}
        '''
        result = self._values.get("azure_tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def clientcert(self) -> typing.Optional[PostgresqlProviderClientcert]:
        '''clientcert block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#clientcert PostgresqlProvider#clientcert}
        '''
        result = self._values.get("clientcert")
        return typing.cast(typing.Optional[PostgresqlProviderClientcert], result)

    @builtins.property
    def connect_timeout(self) -> typing.Optional[jsii.Number]:
        '''Maximum wait for connection, in seconds. Zero or not specified means wait indefinitely.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#connect_timeout PostgresqlProvider#connect_timeout}
        '''
        result = self._values.get("connect_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def database(self) -> typing.Optional[builtins.str]:
        '''The name of the database to connect to in order to conenct to (defaults to ``postgres``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#database PostgresqlProvider#database}
        '''
        result = self._values.get("database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_username(self) -> typing.Optional[builtins.str]:
        '''Database username associated to the connected user (for user name maps).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#database_username PostgresqlProvider#database_username}
        '''
        result = self._values.get("database_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expected_version(self) -> typing.Optional[builtins.str]:
        '''Specify the expected version of PostgreSQL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#expected_version PostgresqlProvider#expected_version}
        '''
        result = self._values.get("expected_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcp_iam_impersonate_service_account(self) -> typing.Optional[builtins.str]:
        '''Service account to impersonate when using GCP IAM authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#gcp_iam_impersonate_service_account PostgresqlProvider#gcp_iam_impersonate_service_account}
        '''
        result = self._values.get("gcp_iam_impersonate_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Name of PostgreSQL server address to connect to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#host PostgresqlProvider#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of connections to establish to the database. Zero means unlimited.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#max_connections PostgresqlProvider#max_connections}
        '''
        result = self._values.get("max_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password to be used if the PostgreSQL server demands password authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#password PostgresqlProvider#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The PostgreSQL port number to connect to at the server host, or socket file name extension for Unix-domain connections.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#port PostgresqlProvider#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#scheme PostgresqlProvider#scheme}.'''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sslmode(self) -> typing.Optional[builtins.str]:
        '''This option determines whether or with what priority a secure SSL TCP/IP connection will be negotiated with the PostgreSQL server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#sslmode PostgresqlProvider#sslmode}
        '''
        result = self._values.get("sslmode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#ssl_mode PostgresqlProvider#ssl_mode}.'''
        result = self._values.get("ssl_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sslrootcert(self) -> typing.Optional[builtins.str]:
        '''The SSL server root certificate file path. The file must contain PEM encoded data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#sslrootcert PostgresqlProvider#sslrootcert}
        '''
        result = self._values.get("sslrootcert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def superuser(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if the user to connect as is a Postgres superuser or not.If not, some feature might be disabled (e.g.: Refreshing state password from Postgres).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#superuser PostgresqlProvider#superuser}
        '''
        result = self._values.get("superuser")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''PostgreSQL user name to connect as.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs#username PostgresqlProvider#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PostgresqlProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PostgresqlProvider",
    "PostgresqlProviderClientcert",
    "PostgresqlProviderConfig",
]

publication.publish()

def _typecheckingstub__873dda44896731f3ed4ac28494dd70199e52e0d56618c8331c8cac2815eb1e7b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias: typing.Optional[builtins.str] = None,
    aws_rds_iam_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    aws_rds_iam_profile: typing.Optional[builtins.str] = None,
    aws_rds_iam_provider_role_arn: typing.Optional[builtins.str] = None,
    aws_rds_iam_region: typing.Optional[builtins.str] = None,
    azure_identity_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    azure_tenant_id: typing.Optional[builtins.str] = None,
    clientcert: typing.Optional[typing.Union[PostgresqlProviderClientcert, typing.Dict[builtins.str, typing.Any]]] = None,
    connect_timeout: typing.Optional[jsii.Number] = None,
    database: typing.Optional[builtins.str] = None,
    database_username: typing.Optional[builtins.str] = None,
    expected_version: typing.Optional[builtins.str] = None,
    gcp_iam_impersonate_service_account: typing.Optional[builtins.str] = None,
    host: typing.Optional[builtins.str] = None,
    max_connections: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    scheme: typing.Optional[builtins.str] = None,
    sslmode: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
    sslrootcert: typing.Optional[builtins.str] = None,
    superuser: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294081ad4cecc88cd29ad89d8e75399fa18b9777f88d4e977b88e635f9e49876(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc0f2b6c6f6f94b52d4c7648d7c745cbc1a338dcdaec6a66c040984db8eb83a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc62e854be1beb6aa7978c09901437eb95114712c03376964c9f66d4a60e24cf(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b173d3edc65c9c3552ccf4498d35f0d9129d15536427a8794bf01d43f01a3a9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa115a053eed9e507d181bc20bd0e955153f99ff9eddb710951b59ea19ac7b6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a68d986cc9908ca93ffff3232b82c8d10cb6db9f7c861517afe3deb72aa7f226(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b83c13c54d92c5ea76c516de42843fbf68da2f6619da5e0626b5258a5935ca(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3127998d537c3e8e585b86f0880a30891fe353d506acfbac7b7e87848d3ee04c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de48e1759bfb9c4eba5f859b5657087318c26150d30749a751edd55175846b83(
    value: typing.Optional[PostgresqlProviderClientcert],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c904c7d078952dc0b092e5e5e58c15afac166b970d3002612e3c3031fe3a46(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc54f4a58a539e3f45798ed76298e1104edc9948a353d2e241542b6bc7e2ef7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d9a6232c3ee2451eac4bcf47dee1bb29cc64168d773a486cc028349797c6e0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcff7c2f8acf9e2548230b4c1d62e39b9371607e4b2d946625ad4d1280512767(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d6b09d9e36957e1ca6d2410fb95572c136e90b7e7fa0348e386ee4a09dde84(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13c807cf51e1d04e68dde241ad0ee60c86c1f11a4108a22100d084a6a267c83(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbdad577b7593c5b15cb3aa112227b532f4af2a590a2c157345983d23b1ad9df(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3f48ed7fdd396b191b2e0fabd390014cdd5dc5ff9b29854372610c02b993e3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0186590d259d14f8769676cadfb819518e6ee3766eab90c95d14f134fa386203(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37316260fd15fa42b191235c36ae0adb72e4e6efa10a6481aba0a18f5aaab85(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825b3e3cff1f8852f807c11f8b58388de7c44ec41855bf527387df68e18df9b0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7dc8c36733660e5c4fda40f09057707d7c8e0d20257fc8e9fc3776a2eb5208(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d16fe1571b837ab905976d3dd0540fd3c84eaf89fb69bc720d90a755981b131(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72033df84f4029db4a39f6b615083b89a815275c8f819ce405e95de0ac023977(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8850823304003c1baa5b2ec921306724929385ee5617191fb0d24c1516b41d0d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17fff281aae5956890689f9551e028540c4b095ea7e40dfc387ca3f724da72f6(
    *,
    cert: builtins.str,
    key: builtins.str,
    sslinline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0cedc5a2e044ea705446ddbefd2a58e4b5080becd8b24f22f9c36fa4d87d5f(
    *,
    alias: typing.Optional[builtins.str] = None,
    aws_rds_iam_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    aws_rds_iam_profile: typing.Optional[builtins.str] = None,
    aws_rds_iam_provider_role_arn: typing.Optional[builtins.str] = None,
    aws_rds_iam_region: typing.Optional[builtins.str] = None,
    azure_identity_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    azure_tenant_id: typing.Optional[builtins.str] = None,
    clientcert: typing.Optional[typing.Union[PostgresqlProviderClientcert, typing.Dict[builtins.str, typing.Any]]] = None,
    connect_timeout: typing.Optional[jsii.Number] = None,
    database: typing.Optional[builtins.str] = None,
    database_username: typing.Optional[builtins.str] = None,
    expected_version: typing.Optional[builtins.str] = None,
    gcp_iam_impersonate_service_account: typing.Optional[builtins.str] = None,
    host: typing.Optional[builtins.str] = None,
    max_connections: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    scheme: typing.Optional[builtins.str] = None,
    sslmode: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
    sslrootcert: typing.Optional[builtins.str] = None,
    superuser: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
