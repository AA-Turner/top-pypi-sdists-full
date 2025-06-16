r'''
# `google_datastream_connection_profile`

Refer to the Terraform Registry for docs: [`google_datastream_connection_profile`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile).
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


class GoogleDatastreamConnectionProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile google_datastream_connection_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        connection_profile_id: builtins.str,
        display_name: builtins.str,
        location: builtins.str,
        bigquery_profile: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileBigqueryProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        create_without_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forward_ssh_connectivity: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileForwardSshConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_profile: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileGcsProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mysql_profile: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileMysqlProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle_profile: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileOracleProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql_profile: typing.Optional[typing.Union["GoogleDatastreamConnectionProfilePostgresqlProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        private_connectivity: typing.Optional[typing.Union["GoogleDatastreamConnectionProfilePrivateConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        salesforce_profile: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileSalesforceProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        sql_server_profile: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileSqlServerProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile google_datastream_connection_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param connection_profile_id: The connection profile identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#connection_profile_id GoogleDatastreamConnectionProfile#connection_profile_id}
        :param display_name: Display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#display_name GoogleDatastreamConnectionProfile#display_name}
        :param location: The name of the location this connection profile is located in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#location GoogleDatastreamConnectionProfile#location}
        :param bigquery_profile: bigquery_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#bigquery_profile GoogleDatastreamConnectionProfile#bigquery_profile}
        :param create_without_validation: Create the connection profile without validating it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#create_without_validation GoogleDatastreamConnectionProfile#create_without_validation}
        :param forward_ssh_connectivity: forward_ssh_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#forward_ssh_connectivity GoogleDatastreamConnectionProfile#forward_ssh_connectivity}
        :param gcs_profile: gcs_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#gcs_profile GoogleDatastreamConnectionProfile#gcs_profile}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#id GoogleDatastreamConnectionProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#labels GoogleDatastreamConnectionProfile#labels}
        :param mysql_profile: mysql_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#mysql_profile GoogleDatastreamConnectionProfile#mysql_profile}
        :param oracle_profile: oracle_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#oracle_profile GoogleDatastreamConnectionProfile#oracle_profile}
        :param postgresql_profile: postgresql_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#postgresql_profile GoogleDatastreamConnectionProfile#postgresql_profile}
        :param private_connectivity: private_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#private_connectivity GoogleDatastreamConnectionProfile#private_connectivity}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#project GoogleDatastreamConnectionProfile#project}.
        :param salesforce_profile: salesforce_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#salesforce_profile GoogleDatastreamConnectionProfile#salesforce_profile}
        :param sql_server_profile: sql_server_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#sql_server_profile GoogleDatastreamConnectionProfile#sql_server_profile}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#timeouts GoogleDatastreamConnectionProfile#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c025b707bafbe1605b24d076e3fe778ff8ffc1eb64d5f83a61b70121507da1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDatastreamConnectionProfileConfig(
            connection_profile_id=connection_profile_id,
            display_name=display_name,
            location=location,
            bigquery_profile=bigquery_profile,
            create_without_validation=create_without_validation,
            forward_ssh_connectivity=forward_ssh_connectivity,
            gcs_profile=gcs_profile,
            id=id,
            labels=labels,
            mysql_profile=mysql_profile,
            oracle_profile=oracle_profile,
            postgresql_profile=postgresql_profile,
            private_connectivity=private_connectivity,
            project=project,
            salesforce_profile=salesforce_profile,
            sql_server_profile=sql_server_profile,
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
        '''Generates CDKTF code for importing a GoogleDatastreamConnectionProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDatastreamConnectionProfile to import.
        :param import_from_id: The id of the existing GoogleDatastreamConnectionProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDatastreamConnectionProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed71633433e7fb41d54ec37f23ca4b5d70c61430091d11cedc3c47e9d42c23f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBigqueryProfile")
    def put_bigquery_profile(self) -> None:
        value = GoogleDatastreamConnectionProfileBigqueryProfile()

        return typing.cast(None, jsii.invoke(self, "putBigqueryProfile", [value]))

    @jsii.member(jsii_name="putForwardSshConnectivity")
    def put_forward_ssh_connectivity(
        self,
        *,
        hostname: builtins.str,
        username: builtins.str,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        private_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hostname: Hostname for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#hostname GoogleDatastreamConnectionProfile#hostname}
        :param username: Username for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        :param password: SSH password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        :param port: Port for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#port GoogleDatastreamConnectionProfile#port}
        :param private_key: SSH private key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#private_key GoogleDatastreamConnectionProfile#private_key}
        '''
        value = GoogleDatastreamConnectionProfileForwardSshConnectivity(
            hostname=hostname,
            username=username,
            password=password,
            port=port,
            private_key=private_key,
        )

        return typing.cast(None, jsii.invoke(self, "putForwardSshConnectivity", [value]))

    @jsii.member(jsii_name="putGcsProfile")
    def put_gcs_profile(
        self,
        *,
        bucket: builtins.str,
        root_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: The Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#bucket GoogleDatastreamConnectionProfile#bucket}
        :param root_path: The root path inside the Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#root_path GoogleDatastreamConnectionProfile#root_path}
        '''
        value = GoogleDatastreamConnectionProfileGcsProfile(
            bucket=bucket, root_path=root_path
        )

        return typing.cast(None, jsii.invoke(self, "putGcsProfile", [value]))

    @jsii.member(jsii_name="putMysqlProfile")
    def put_mysql_profile(
        self,
        *,
        hostname: builtins.str,
        username: builtins.str,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        secret_manager_stored_password: typing.Optional[builtins.str] = None,
        ssl_config: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileMysqlProfileSslConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hostname: Hostname for the MySQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#hostname GoogleDatastreamConnectionProfile#hostname}
        :param username: Username for the MySQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        :param password: Password for the MySQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        :param port: Port for the MySQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#port GoogleDatastreamConnectionProfile#port}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_password GoogleDatastreamConnectionProfile#secret_manager_stored_password}
        :param ssl_config: ssl_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#ssl_config GoogleDatastreamConnectionProfile#ssl_config}
        '''
        value = GoogleDatastreamConnectionProfileMysqlProfile(
            hostname=hostname,
            username=username,
            password=password,
            port=port,
            secret_manager_stored_password=secret_manager_stored_password,
            ssl_config=ssl_config,
        )

        return typing.cast(None, jsii.invoke(self, "putMysqlProfile", [value]))

    @jsii.member(jsii_name="putOracleProfile")
    def put_oracle_profile(
        self,
        *,
        database_service: builtins.str,
        hostname: builtins.str,
        username: builtins.str,
        connection_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        secret_manager_stored_password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database_service: Database for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#database_service GoogleDatastreamConnectionProfile#database_service}
        :param hostname: Hostname for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#hostname GoogleDatastreamConnectionProfile#hostname}
        :param username: Username for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        :param connection_attributes: Connection string attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#connection_attributes GoogleDatastreamConnectionProfile#connection_attributes}
        :param password: Password for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        :param port: Port for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#port GoogleDatastreamConnectionProfile#port}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_password GoogleDatastreamConnectionProfile#secret_manager_stored_password}
        '''
        value = GoogleDatastreamConnectionProfileOracleProfile(
            database_service=database_service,
            hostname=hostname,
            username=username,
            connection_attributes=connection_attributes,
            password=password,
            port=port,
            secret_manager_stored_password=secret_manager_stored_password,
        )

        return typing.cast(None, jsii.invoke(self, "putOracleProfile", [value]))

    @jsii.member(jsii_name="putPostgresqlProfile")
    def put_postgresql_profile(
        self,
        *,
        database: builtins.str,
        hostname: builtins.str,
        username: builtins.str,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        secret_manager_stored_password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database: Database for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#database GoogleDatastreamConnectionProfile#database}
        :param hostname: Hostname for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#hostname GoogleDatastreamConnectionProfile#hostname}
        :param username: Username for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        :param password: Password for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        :param port: Port for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#port GoogleDatastreamConnectionProfile#port}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_password GoogleDatastreamConnectionProfile#secret_manager_stored_password}
        '''
        value = GoogleDatastreamConnectionProfilePostgresqlProfile(
            database=database,
            hostname=hostname,
            username=username,
            password=password,
            port=port,
            secret_manager_stored_password=secret_manager_stored_password,
        )

        return typing.cast(None, jsii.invoke(self, "putPostgresqlProfile", [value]))

    @jsii.member(jsii_name="putPrivateConnectivity")
    def put_private_connectivity(self, *, private_connection: builtins.str) -> None:
        '''
        :param private_connection: A reference to a private connection resource. Format: 'projects/{project}/locations/{location}/privateConnections/{name}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#private_connection GoogleDatastreamConnectionProfile#private_connection}
        '''
        value = GoogleDatastreamConnectionProfilePrivateConnectivity(
            private_connection=private_connection
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateConnectivity", [value]))

    @jsii.member(jsii_name="putSalesforceProfile")
    def put_salesforce_profile(
        self,
        *,
        domain: builtins.str,
        oauth2_client_credentials: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        user_credentials: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileSalesforceProfileUserCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param domain: Domain for the Salesforce Org. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#domain GoogleDatastreamConnectionProfile#domain}
        :param oauth2_client_credentials: oauth2_client_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#oauth2_client_credentials GoogleDatastreamConnectionProfile#oauth2_client_credentials}
        :param user_credentials: user_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#user_credentials GoogleDatastreamConnectionProfile#user_credentials}
        '''
        value = GoogleDatastreamConnectionProfileSalesforceProfile(
            domain=domain,
            oauth2_client_credentials=oauth2_client_credentials,
            user_credentials=user_credentials,
        )

        return typing.cast(None, jsii.invoke(self, "putSalesforceProfile", [value]))

    @jsii.member(jsii_name="putSqlServerProfile")
    def put_sql_server_profile(
        self,
        *,
        database: builtins.str,
        hostname: builtins.str,
        username: builtins.str,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        secret_manager_stored_password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database: Database for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#database GoogleDatastreamConnectionProfile#database}
        :param hostname: Hostname for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#hostname GoogleDatastreamConnectionProfile#hostname}
        :param username: Username for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        :param password: Password for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        :param port: Port for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#port GoogleDatastreamConnectionProfile#port}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_password GoogleDatastreamConnectionProfile#secret_manager_stored_password}
        '''
        value = GoogleDatastreamConnectionProfileSqlServerProfile(
            database=database,
            hostname=hostname,
            username=username,
            password=password,
            port=port,
            secret_manager_stored_password=secret_manager_stored_password,
        )

        return typing.cast(None, jsii.invoke(self, "putSqlServerProfile", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#create GoogleDatastreamConnectionProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#delete GoogleDatastreamConnectionProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#update GoogleDatastreamConnectionProfile#update}.
        '''
        value = GoogleDatastreamConnectionProfileTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBigqueryProfile")
    def reset_bigquery_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigqueryProfile", []))

    @jsii.member(jsii_name="resetCreateWithoutValidation")
    def reset_create_without_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateWithoutValidation", []))

    @jsii.member(jsii_name="resetForwardSshConnectivity")
    def reset_forward_ssh_connectivity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardSshConnectivity", []))

    @jsii.member(jsii_name="resetGcsProfile")
    def reset_gcs_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsProfile", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMysqlProfile")
    def reset_mysql_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysqlProfile", []))

    @jsii.member(jsii_name="resetOracleProfile")
    def reset_oracle_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOracleProfile", []))

    @jsii.member(jsii_name="resetPostgresqlProfile")
    def reset_postgresql_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostgresqlProfile", []))

    @jsii.member(jsii_name="resetPrivateConnectivity")
    def reset_private_connectivity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateConnectivity", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSalesforceProfile")
    def reset_salesforce_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSalesforceProfile", []))

    @jsii.member(jsii_name="resetSqlServerProfile")
    def reset_sql_server_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlServerProfile", []))

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
    @jsii.member(jsii_name="bigqueryProfile")
    def bigquery_profile(
        self,
    ) -> "GoogleDatastreamConnectionProfileBigqueryProfileOutputReference":
        return typing.cast("GoogleDatastreamConnectionProfileBigqueryProfileOutputReference", jsii.get(self, "bigqueryProfile"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="forwardSshConnectivity")
    def forward_ssh_connectivity(
        self,
    ) -> "GoogleDatastreamConnectionProfileForwardSshConnectivityOutputReference":
        return typing.cast("GoogleDatastreamConnectionProfileForwardSshConnectivityOutputReference", jsii.get(self, "forwardSshConnectivity"))

    @builtins.property
    @jsii.member(jsii_name="gcsProfile")
    def gcs_profile(
        self,
    ) -> "GoogleDatastreamConnectionProfileGcsProfileOutputReference":
        return typing.cast("GoogleDatastreamConnectionProfileGcsProfileOutputReference", jsii.get(self, "gcsProfile"))

    @builtins.property
    @jsii.member(jsii_name="mysqlProfile")
    def mysql_profile(
        self,
    ) -> "GoogleDatastreamConnectionProfileMysqlProfileOutputReference":
        return typing.cast("GoogleDatastreamConnectionProfileMysqlProfileOutputReference", jsii.get(self, "mysqlProfile"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="oracleProfile")
    def oracle_profile(
        self,
    ) -> "GoogleDatastreamConnectionProfileOracleProfileOutputReference":
        return typing.cast("GoogleDatastreamConnectionProfileOracleProfileOutputReference", jsii.get(self, "oracleProfile"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlProfile")
    def postgresql_profile(
        self,
    ) -> "GoogleDatastreamConnectionProfilePostgresqlProfileOutputReference":
        return typing.cast("GoogleDatastreamConnectionProfilePostgresqlProfileOutputReference", jsii.get(self, "postgresqlProfile"))

    @builtins.property
    @jsii.member(jsii_name="privateConnectivity")
    def private_connectivity(
        self,
    ) -> "GoogleDatastreamConnectionProfilePrivateConnectivityOutputReference":
        return typing.cast("GoogleDatastreamConnectionProfilePrivateConnectivityOutputReference", jsii.get(self, "privateConnectivity"))

    @builtins.property
    @jsii.member(jsii_name="salesforceProfile")
    def salesforce_profile(
        self,
    ) -> "GoogleDatastreamConnectionProfileSalesforceProfileOutputReference":
        return typing.cast("GoogleDatastreamConnectionProfileSalesforceProfileOutputReference", jsii.get(self, "salesforceProfile"))

    @builtins.property
    @jsii.member(jsii_name="sqlServerProfile")
    def sql_server_profile(
        self,
    ) -> "GoogleDatastreamConnectionProfileSqlServerProfileOutputReference":
        return typing.cast("GoogleDatastreamConnectionProfileSqlServerProfileOutputReference", jsii.get(self, "sqlServerProfile"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDatastreamConnectionProfileTimeoutsOutputReference":
        return typing.cast("GoogleDatastreamConnectionProfileTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryProfileInput")
    def bigquery_profile_input(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileBigqueryProfile"]:
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileBigqueryProfile"], jsii.get(self, "bigqueryProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionProfileIdInput")
    def connection_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="createWithoutValidationInput")
    def create_without_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "createWithoutValidationInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardSshConnectivityInput")
    def forward_ssh_connectivity_input(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileForwardSshConnectivity"]:
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileForwardSshConnectivity"], jsii.get(self, "forwardSshConnectivityInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsProfileInput")
    def gcs_profile_input(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileGcsProfile"]:
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileGcsProfile"], jsii.get(self, "gcsProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="mysqlProfileInput")
    def mysql_profile_input(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileMysqlProfile"]:
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileMysqlProfile"], jsii.get(self, "mysqlProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="oracleProfileInput")
    def oracle_profile_input(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileOracleProfile"]:
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileOracleProfile"], jsii.get(self, "oracleProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlProfileInput")
    def postgresql_profile_input(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfilePostgresqlProfile"]:
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfilePostgresqlProfile"], jsii.get(self, "postgresqlProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="privateConnectivityInput")
    def private_connectivity_input(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfilePrivateConnectivity"]:
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfilePrivateConnectivity"], jsii.get(self, "privateConnectivityInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="salesforceProfileInput")
    def salesforce_profile_input(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileSalesforceProfile"]:
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileSalesforceProfile"], jsii.get(self, "salesforceProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlServerProfileInput")
    def sql_server_profile_input(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileSqlServerProfile"]:
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileSqlServerProfile"], jsii.get(self, "sqlServerProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDatastreamConnectionProfileTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDatastreamConnectionProfileTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionProfileId")
    def connection_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionProfileId"))

    @connection_profile_id.setter
    def connection_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a954a35a4da09190999a985a8a5397b03bbef43e3feeb5e7f8b89c8aa8e98139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionProfileId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createWithoutValidation")
    def create_without_validation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "createWithoutValidation"))

    @create_without_validation.setter
    def create_without_validation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb967db6c12045e52a39294c43218f35056bb11a37bbc527553dd08af6b3ba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createWithoutValidation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22de0186e58c1f64abfe601f7355907fe81f60d93409ebdcd5e414360d60d6b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20c06dc2765f8b068770b76b53e3f3fa7bce2f551ddf49e5ad7d5e6176d13d42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c76183c236282f7dd139e5e8807c019f97d3e93df01d765ffefecbacf55c9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510def3c54ba7446ef8c8eae2bec58049c2f1d6c0900c03465015bcec144bde1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d7179cafd457d68cdbc09f2c0d6220b32f114af9bcb9b97fc64d7af4b22df1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileBigqueryProfile",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDatastreamConnectionProfileBigqueryProfile:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatastreamConnectionProfileBigqueryProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatastreamConnectionProfileBigqueryProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileBigqueryProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0e3bbd28ef2515dd9cc9072d23ae81fbd6ef455ad4c587cb4e20faeb882a06b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatastreamConnectionProfileBigqueryProfile]:
        return typing.cast(typing.Optional[GoogleDatastreamConnectionProfileBigqueryProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatastreamConnectionProfileBigqueryProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b0f9f5642ff9a298e1931841f9f8a0f8452c625114f6da702366e7302fb180f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "connection_profile_id": "connectionProfileId",
        "display_name": "displayName",
        "location": "location",
        "bigquery_profile": "bigqueryProfile",
        "create_without_validation": "createWithoutValidation",
        "forward_ssh_connectivity": "forwardSshConnectivity",
        "gcs_profile": "gcsProfile",
        "id": "id",
        "labels": "labels",
        "mysql_profile": "mysqlProfile",
        "oracle_profile": "oracleProfile",
        "postgresql_profile": "postgresqlProfile",
        "private_connectivity": "privateConnectivity",
        "project": "project",
        "salesforce_profile": "salesforceProfile",
        "sql_server_profile": "sqlServerProfile",
        "timeouts": "timeouts",
    },
)
class GoogleDatastreamConnectionProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        connection_profile_id: builtins.str,
        display_name: builtins.str,
        location: builtins.str,
        bigquery_profile: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileBigqueryProfile, typing.Dict[builtins.str, typing.Any]]] = None,
        create_without_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forward_ssh_connectivity: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileForwardSshConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_profile: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileGcsProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mysql_profile: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileMysqlProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle_profile: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileOracleProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql_profile: typing.Optional[typing.Union["GoogleDatastreamConnectionProfilePostgresqlProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        private_connectivity: typing.Optional[typing.Union["GoogleDatastreamConnectionProfilePrivateConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        salesforce_profile: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileSalesforceProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        sql_server_profile: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileSqlServerProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param connection_profile_id: The connection profile identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#connection_profile_id GoogleDatastreamConnectionProfile#connection_profile_id}
        :param display_name: Display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#display_name GoogleDatastreamConnectionProfile#display_name}
        :param location: The name of the location this connection profile is located in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#location GoogleDatastreamConnectionProfile#location}
        :param bigquery_profile: bigquery_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#bigquery_profile GoogleDatastreamConnectionProfile#bigquery_profile}
        :param create_without_validation: Create the connection profile without validating it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#create_without_validation GoogleDatastreamConnectionProfile#create_without_validation}
        :param forward_ssh_connectivity: forward_ssh_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#forward_ssh_connectivity GoogleDatastreamConnectionProfile#forward_ssh_connectivity}
        :param gcs_profile: gcs_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#gcs_profile GoogleDatastreamConnectionProfile#gcs_profile}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#id GoogleDatastreamConnectionProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#labels GoogleDatastreamConnectionProfile#labels}
        :param mysql_profile: mysql_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#mysql_profile GoogleDatastreamConnectionProfile#mysql_profile}
        :param oracle_profile: oracle_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#oracle_profile GoogleDatastreamConnectionProfile#oracle_profile}
        :param postgresql_profile: postgresql_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#postgresql_profile GoogleDatastreamConnectionProfile#postgresql_profile}
        :param private_connectivity: private_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#private_connectivity GoogleDatastreamConnectionProfile#private_connectivity}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#project GoogleDatastreamConnectionProfile#project}.
        :param salesforce_profile: salesforce_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#salesforce_profile GoogleDatastreamConnectionProfile#salesforce_profile}
        :param sql_server_profile: sql_server_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#sql_server_profile GoogleDatastreamConnectionProfile#sql_server_profile}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#timeouts GoogleDatastreamConnectionProfile#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bigquery_profile, dict):
            bigquery_profile = GoogleDatastreamConnectionProfileBigqueryProfile(**bigquery_profile)
        if isinstance(forward_ssh_connectivity, dict):
            forward_ssh_connectivity = GoogleDatastreamConnectionProfileForwardSshConnectivity(**forward_ssh_connectivity)
        if isinstance(gcs_profile, dict):
            gcs_profile = GoogleDatastreamConnectionProfileGcsProfile(**gcs_profile)
        if isinstance(mysql_profile, dict):
            mysql_profile = GoogleDatastreamConnectionProfileMysqlProfile(**mysql_profile)
        if isinstance(oracle_profile, dict):
            oracle_profile = GoogleDatastreamConnectionProfileOracleProfile(**oracle_profile)
        if isinstance(postgresql_profile, dict):
            postgresql_profile = GoogleDatastreamConnectionProfilePostgresqlProfile(**postgresql_profile)
        if isinstance(private_connectivity, dict):
            private_connectivity = GoogleDatastreamConnectionProfilePrivateConnectivity(**private_connectivity)
        if isinstance(salesforce_profile, dict):
            salesforce_profile = GoogleDatastreamConnectionProfileSalesforceProfile(**salesforce_profile)
        if isinstance(sql_server_profile, dict):
            sql_server_profile = GoogleDatastreamConnectionProfileSqlServerProfile(**sql_server_profile)
        if isinstance(timeouts, dict):
            timeouts = GoogleDatastreamConnectionProfileTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d76c8a675707d09d73528c9de0908f53419150d9e1bcbcd92da96b8bfe0dce9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument connection_profile_id", value=connection_profile_id, expected_type=type_hints["connection_profile_id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument bigquery_profile", value=bigquery_profile, expected_type=type_hints["bigquery_profile"])
            check_type(argname="argument create_without_validation", value=create_without_validation, expected_type=type_hints["create_without_validation"])
            check_type(argname="argument forward_ssh_connectivity", value=forward_ssh_connectivity, expected_type=type_hints["forward_ssh_connectivity"])
            check_type(argname="argument gcs_profile", value=gcs_profile, expected_type=type_hints["gcs_profile"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument mysql_profile", value=mysql_profile, expected_type=type_hints["mysql_profile"])
            check_type(argname="argument oracle_profile", value=oracle_profile, expected_type=type_hints["oracle_profile"])
            check_type(argname="argument postgresql_profile", value=postgresql_profile, expected_type=type_hints["postgresql_profile"])
            check_type(argname="argument private_connectivity", value=private_connectivity, expected_type=type_hints["private_connectivity"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument salesforce_profile", value=salesforce_profile, expected_type=type_hints["salesforce_profile"])
            check_type(argname="argument sql_server_profile", value=sql_server_profile, expected_type=type_hints["sql_server_profile"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_profile_id": connection_profile_id,
            "display_name": display_name,
            "location": location,
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
        if bigquery_profile is not None:
            self._values["bigquery_profile"] = bigquery_profile
        if create_without_validation is not None:
            self._values["create_without_validation"] = create_without_validation
        if forward_ssh_connectivity is not None:
            self._values["forward_ssh_connectivity"] = forward_ssh_connectivity
        if gcs_profile is not None:
            self._values["gcs_profile"] = gcs_profile
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if mysql_profile is not None:
            self._values["mysql_profile"] = mysql_profile
        if oracle_profile is not None:
            self._values["oracle_profile"] = oracle_profile
        if postgresql_profile is not None:
            self._values["postgresql_profile"] = postgresql_profile
        if private_connectivity is not None:
            self._values["private_connectivity"] = private_connectivity
        if project is not None:
            self._values["project"] = project
        if salesforce_profile is not None:
            self._values["salesforce_profile"] = salesforce_profile
        if sql_server_profile is not None:
            self._values["sql_server_profile"] = sql_server_profile
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
    def connection_profile_id(self) -> builtins.str:
        '''The connection profile identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#connection_profile_id GoogleDatastreamConnectionProfile#connection_profile_id}
        '''
        result = self._values.get("connection_profile_id")
        assert result is not None, "Required property 'connection_profile_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Display name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#display_name GoogleDatastreamConnectionProfile#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The name of the location this connection profile is located in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#location GoogleDatastreamConnectionProfile#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bigquery_profile(
        self,
    ) -> typing.Optional[GoogleDatastreamConnectionProfileBigqueryProfile]:
        '''bigquery_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#bigquery_profile GoogleDatastreamConnectionProfile#bigquery_profile}
        '''
        result = self._values.get("bigquery_profile")
        return typing.cast(typing.Optional[GoogleDatastreamConnectionProfileBigqueryProfile], result)

    @builtins.property
    def create_without_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Create the connection profile without validating it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#create_without_validation GoogleDatastreamConnectionProfile#create_without_validation}
        '''
        result = self._values.get("create_without_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def forward_ssh_connectivity(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileForwardSshConnectivity"]:
        '''forward_ssh_connectivity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#forward_ssh_connectivity GoogleDatastreamConnectionProfile#forward_ssh_connectivity}
        '''
        result = self._values.get("forward_ssh_connectivity")
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileForwardSshConnectivity"], result)

    @builtins.property
    def gcs_profile(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileGcsProfile"]:
        '''gcs_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#gcs_profile GoogleDatastreamConnectionProfile#gcs_profile}
        '''
        result = self._values.get("gcs_profile")
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileGcsProfile"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#id GoogleDatastreamConnectionProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#labels GoogleDatastreamConnectionProfile#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mysql_profile(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileMysqlProfile"]:
        '''mysql_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#mysql_profile GoogleDatastreamConnectionProfile#mysql_profile}
        '''
        result = self._values.get("mysql_profile")
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileMysqlProfile"], result)

    @builtins.property
    def oracle_profile(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileOracleProfile"]:
        '''oracle_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#oracle_profile GoogleDatastreamConnectionProfile#oracle_profile}
        '''
        result = self._values.get("oracle_profile")
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileOracleProfile"], result)

    @builtins.property
    def postgresql_profile(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfilePostgresqlProfile"]:
        '''postgresql_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#postgresql_profile GoogleDatastreamConnectionProfile#postgresql_profile}
        '''
        result = self._values.get("postgresql_profile")
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfilePostgresqlProfile"], result)

    @builtins.property
    def private_connectivity(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfilePrivateConnectivity"]:
        '''private_connectivity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#private_connectivity GoogleDatastreamConnectionProfile#private_connectivity}
        '''
        result = self._values.get("private_connectivity")
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfilePrivateConnectivity"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#project GoogleDatastreamConnectionProfile#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def salesforce_profile(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileSalesforceProfile"]:
        '''salesforce_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#salesforce_profile GoogleDatastreamConnectionProfile#salesforce_profile}
        '''
        result = self._values.get("salesforce_profile")
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileSalesforceProfile"], result)

    @builtins.property
    def sql_server_profile(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileSqlServerProfile"]:
        '''sql_server_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#sql_server_profile GoogleDatastreamConnectionProfile#sql_server_profile}
        '''
        result = self._values.get("sql_server_profile")
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileSqlServerProfile"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDatastreamConnectionProfileTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#timeouts GoogleDatastreamConnectionProfile#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatastreamConnectionProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileForwardSshConnectivity",
    jsii_struct_bases=[],
    name_mapping={
        "hostname": "hostname",
        "username": "username",
        "password": "password",
        "port": "port",
        "private_key": "privateKey",
    },
)
class GoogleDatastreamConnectionProfileForwardSshConnectivity:
    def __init__(
        self,
        *,
        hostname: builtins.str,
        username: builtins.str,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        private_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hostname: Hostname for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#hostname GoogleDatastreamConnectionProfile#hostname}
        :param username: Username for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        :param password: SSH password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        :param port: Port for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#port GoogleDatastreamConnectionProfile#port}
        :param private_key: SSH private key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#private_key GoogleDatastreamConnectionProfile#private_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__898b49febbfd20102d4d918be1907067211b06d866e869ed02325d9b7b071717)
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hostname": hostname,
            "username": username,
        }
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if private_key is not None:
            self._values["private_key"] = private_key

    @builtins.property
    def hostname(self) -> builtins.str:
        '''Hostname for the SSH tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#hostname GoogleDatastreamConnectionProfile#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for the SSH tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''SSH password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port for the SSH tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#port GoogleDatastreamConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''SSH private key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#private_key GoogleDatastreamConnectionProfile#private_key}
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatastreamConnectionProfileForwardSshConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatastreamConnectionProfileForwardSshConnectivityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileForwardSshConnectivityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ab34a3ad9c4fab9ef80bde8f769b5983d36ff181bba13ef367f9b893ffa7bda)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPrivateKey")
    def reset_private_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKey", []))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyInput")
    def private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__725084f46e39078f6024fd0671c96dfbd6dc4d5e49acdaa29c2c6e1328cc4844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6da96edd9b84b64672117f5a284cecdbaa5d7d2b2f8d4e213e0b61995839ec56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c3b6afed0107cb7325ab3ba5c7f77e3ca333e3411de2d8f47bd64e534b55e3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e1eda28eb3c256d292f8254ad001d114d61dbacd492719cd148de54becbd84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5665cf24ed8693ff398ba5062c59fd868f5c3bb3ee62409916f26478afb96a99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatastreamConnectionProfileForwardSshConnectivity]:
        return typing.cast(typing.Optional[GoogleDatastreamConnectionProfileForwardSshConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatastreamConnectionProfileForwardSshConnectivity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c3add45012b8d98389c7a11197322d34ce87b9508063065e10a9456aa93b428)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileGcsProfile",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "root_path": "rootPath"},
)
class GoogleDatastreamConnectionProfileGcsProfile:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        root_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: The Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#bucket GoogleDatastreamConnectionProfile#bucket}
        :param root_path: The root path inside the Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#root_path GoogleDatastreamConnectionProfile#root_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e83ca2cc5573d02b04aa4b260739729db1fb993d0c483e36d23ee943c485b9d1)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument root_path", value=root_path, expected_type=type_hints["root_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if root_path is not None:
            self._values["root_path"] = root_path

    @builtins.property
    def bucket(self) -> builtins.str:
        '''The Cloud Storage bucket name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#bucket GoogleDatastreamConnectionProfile#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def root_path(self) -> typing.Optional[builtins.str]:
        '''The root path inside the Cloud Storage bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#root_path GoogleDatastreamConnectionProfile#root_path}
        '''
        result = self._values.get("root_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatastreamConnectionProfileGcsProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatastreamConnectionProfileGcsProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileGcsProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__982aaa0b9b3c7a34bec17f7b9b5beea7f0569d3346b938a7591984eddbeb13d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRootPath")
    def reset_root_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootPath", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="rootPathInput")
    def root_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootPathInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__555f62bc769a5fe35d1746b68ffb7282a2dd37bf817c331192a108ed26ed4b8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootPath")
    def root_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootPath"))

    @root_path.setter
    def root_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9c16a7ce04103b7905f741c4c792e365622c5b0b96299af0b89a9ee0b5b78ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatastreamConnectionProfileGcsProfile]:
        return typing.cast(typing.Optional[GoogleDatastreamConnectionProfileGcsProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatastreamConnectionProfileGcsProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd02487b575cc3309bcc24daa5b741408cd7747d159a4590a83801cd6bf3da2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileMysqlProfile",
    jsii_struct_bases=[],
    name_mapping={
        "hostname": "hostname",
        "username": "username",
        "password": "password",
        "port": "port",
        "secret_manager_stored_password": "secretManagerStoredPassword",
        "ssl_config": "sslConfig",
    },
)
class GoogleDatastreamConnectionProfileMysqlProfile:
    def __init__(
        self,
        *,
        hostname: builtins.str,
        username: builtins.str,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        secret_manager_stored_password: typing.Optional[builtins.str] = None,
        ssl_config: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileMysqlProfileSslConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hostname: Hostname for the MySQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#hostname GoogleDatastreamConnectionProfile#hostname}
        :param username: Username for the MySQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        :param password: Password for the MySQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        :param port: Port for the MySQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#port GoogleDatastreamConnectionProfile#port}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_password GoogleDatastreamConnectionProfile#secret_manager_stored_password}
        :param ssl_config: ssl_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#ssl_config GoogleDatastreamConnectionProfile#ssl_config}
        '''
        if isinstance(ssl_config, dict):
            ssl_config = GoogleDatastreamConnectionProfileMysqlProfileSslConfig(**ssl_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7401859cd51507652b057cf22bd22d76c2cebbe04b305c6303d69445df564cc)
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument secret_manager_stored_password", value=secret_manager_stored_password, expected_type=type_hints["secret_manager_stored_password"])
            check_type(argname="argument ssl_config", value=ssl_config, expected_type=type_hints["ssl_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hostname": hostname,
            "username": username,
        }
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if secret_manager_stored_password is not None:
            self._values["secret_manager_stored_password"] = secret_manager_stored_password
        if ssl_config is not None:
            self._values["ssl_config"] = ssl_config

    @builtins.property
    def hostname(self) -> builtins.str:
        '''Hostname for the MySQL connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#hostname GoogleDatastreamConnectionProfile#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for the MySQL connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for the MySQL connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port for the MySQL connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#port GoogleDatastreamConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_manager_stored_password(self) -> typing.Optional[builtins.str]:
        '''A reference to a Secret Manager resource name storing the user's password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_password GoogleDatastreamConnectionProfile#secret_manager_stored_password}
        '''
        result = self._values.get("secret_manager_stored_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_config(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileMysqlProfileSslConfig"]:
        '''ssl_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#ssl_config GoogleDatastreamConnectionProfile#ssl_config}
        '''
        result = self._values.get("ssl_config")
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileMysqlProfileSslConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatastreamConnectionProfileMysqlProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatastreamConnectionProfileMysqlProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileMysqlProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__483e608169e9ed202cf8688ea06f6cb1806389166db00ccb8727f8c78f55042b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSslConfig")
    def put_ssl_config(
        self,
        *,
        ca_certificate: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_certificate: PEM-encoded certificate of the CA that signed the source database server's certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#ca_certificate GoogleDatastreamConnectionProfile#ca_certificate}
        :param client_certificate: PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' and the 'caCertificate' fields are mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#client_certificate GoogleDatastreamConnectionProfile#client_certificate}
        :param client_key: PEM-encoded private key associated with the Client Certificate. If this field is used then the 'client_certificate' and the 'ca_certificate' fields are mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#client_key GoogleDatastreamConnectionProfile#client_key}
        '''
        value = GoogleDatastreamConnectionProfileMysqlProfileSslConfig(
            ca_certificate=ca_certificate,
            client_certificate=client_certificate,
            client_key=client_key,
        )

        return typing.cast(None, jsii.invoke(self, "putSslConfig", [value]))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetSecretManagerStoredPassword")
    def reset_secret_manager_stored_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretManagerStoredPassword", []))

    @jsii.member(jsii_name="resetSslConfig")
    def reset_ssl_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslConfig", []))

    @builtins.property
    @jsii.member(jsii_name="sslConfig")
    def ssl_config(
        self,
    ) -> "GoogleDatastreamConnectionProfileMysqlProfileSslConfigOutputReference":
        return typing.cast("GoogleDatastreamConnectionProfileMysqlProfileSslConfigOutputReference", jsii.get(self, "sslConfig"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredPasswordInput")
    def secret_manager_stored_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretManagerStoredPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="sslConfigInput")
    def ssl_config_input(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileMysqlProfileSslConfig"]:
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileMysqlProfileSslConfig"], jsii.get(self, "sslConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9ec72300927cd13cec9a1a7c2c9d8fd2b2d6185706998b39fdb77267e7fc52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c7b1b4f2c9eca1812d57e69a603894de8b0e29b779971621d7b3ac5d108408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc9032809bbb4a6b403ba995b3dd6fe63575e2f720575caa1a1f212460ac439d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredPassword")
    def secret_manager_stored_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretManagerStoredPassword"))

    @secret_manager_stored_password.setter
    def secret_manager_stored_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b727ae49fe4a984616281e5046a996ff2753c7fdc5817abde2d12c7fd27591c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretManagerStoredPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__591745bb73df6675029344ae13c1b369a641b3f38906ddc2e23df885e48875ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatastreamConnectionProfileMysqlProfile]:
        return typing.cast(typing.Optional[GoogleDatastreamConnectionProfileMysqlProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatastreamConnectionProfileMysqlProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1997f4dedbf609d3ebba80e6d3aba4336f6a9c9aa59462baa0b0a1d9c109a93f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileMysqlProfileSslConfig",
    jsii_struct_bases=[],
    name_mapping={
        "ca_certificate": "caCertificate",
        "client_certificate": "clientCertificate",
        "client_key": "clientKey",
    },
)
class GoogleDatastreamConnectionProfileMysqlProfileSslConfig:
    def __init__(
        self,
        *,
        ca_certificate: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_certificate: PEM-encoded certificate of the CA that signed the source database server's certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#ca_certificate GoogleDatastreamConnectionProfile#ca_certificate}
        :param client_certificate: PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' and the 'caCertificate' fields are mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#client_certificate GoogleDatastreamConnectionProfile#client_certificate}
        :param client_key: PEM-encoded private key associated with the Client Certificate. If this field is used then the 'client_certificate' and the 'ca_certificate' fields are mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#client_key GoogleDatastreamConnectionProfile#client_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ccffedae518b06bd344ecf910a151bb2126dc4d9d992330bcd0694aed895da)
            check_type(argname="argument ca_certificate", value=ca_certificate, expected_type=type_hints["ca_certificate"])
            check_type(argname="argument client_certificate", value=client_certificate, expected_type=type_hints["client_certificate"])
            check_type(argname="argument client_key", value=client_key, expected_type=type_hints["client_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ca_certificate is not None:
            self._values["ca_certificate"] = ca_certificate
        if client_certificate is not None:
            self._values["client_certificate"] = client_certificate
        if client_key is not None:
            self._values["client_key"] = client_key

    @builtins.property
    def ca_certificate(self) -> typing.Optional[builtins.str]:
        '''PEM-encoded certificate of the CA that signed the source database server's certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#ca_certificate GoogleDatastreamConnectionProfile#ca_certificate}
        '''
        result = self._values.get("ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate(self) -> typing.Optional[builtins.str]:
        '''PEM-encoded certificate that will be used by the replica to authenticate against the source database server.

        If this field
        is used then the 'clientKey' and the 'caCertificate' fields are
        mandatory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#client_certificate GoogleDatastreamConnectionProfile#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_key(self) -> typing.Optional[builtins.str]:
        '''PEM-encoded private key associated with the Client Certificate.

        If this field is used then the 'client_certificate' and the
        'ca_certificate' fields are mandatory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#client_key GoogleDatastreamConnectionProfile#client_key}
        '''
        result = self._values.get("client_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatastreamConnectionProfileMysqlProfileSslConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatastreamConnectionProfileMysqlProfileSslConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileMysqlProfileSslConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__740e78106914654eee1e46ad982fff7f4f9952c2ea88f36dca3b14c9cd755d3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCaCertificate")
    def reset_ca_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaCertificate", []))

    @jsii.member(jsii_name="resetClientCertificate")
    def reset_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificate", []))

    @jsii.member(jsii_name="resetClientKey")
    def reset_client_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientKey", []))

    @builtins.property
    @jsii.member(jsii_name="caCertificateSet")
    def ca_certificate_set(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "caCertificateSet"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateSet")
    def client_certificate_set(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "clientCertificateSet"))

    @builtins.property
    @jsii.member(jsii_name="clientKeySet")
    def client_key_set(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "clientKeySet"))

    @builtins.property
    @jsii.member(jsii_name="caCertificateInput")
    def ca_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateInput")
    def client_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="clientKeyInput")
    def client_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="caCertificate")
    def ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCertificate"))

    @ca_certificate.setter
    def ca_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e458d7e54ab8f7ab1dda35b662f2d59af8a809541aa1b0ad5d99b18b3540f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificate"))

    @client_certificate.setter
    def client_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da8f1f357ef2c243c40ce562b122699bb6870598af0442f4ab85cfb82a0ea4db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientKey")
    def client_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientKey"))

    @client_key.setter
    def client_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83019c9a78d673a5bd633ff22e5da184d20e95159d0dfc677e125906dbc87533)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatastreamConnectionProfileMysqlProfileSslConfig]:
        return typing.cast(typing.Optional[GoogleDatastreamConnectionProfileMysqlProfileSslConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatastreamConnectionProfileMysqlProfileSslConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b0ad3a36da99c9c6f61861f5c30abab76ac3fd9268b15811b9da8d2d9a1946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileOracleProfile",
    jsii_struct_bases=[],
    name_mapping={
        "database_service": "databaseService",
        "hostname": "hostname",
        "username": "username",
        "connection_attributes": "connectionAttributes",
        "password": "password",
        "port": "port",
        "secret_manager_stored_password": "secretManagerStoredPassword",
    },
)
class GoogleDatastreamConnectionProfileOracleProfile:
    def __init__(
        self,
        *,
        database_service: builtins.str,
        hostname: builtins.str,
        username: builtins.str,
        connection_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        secret_manager_stored_password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database_service: Database for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#database_service GoogleDatastreamConnectionProfile#database_service}
        :param hostname: Hostname for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#hostname GoogleDatastreamConnectionProfile#hostname}
        :param username: Username for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        :param connection_attributes: Connection string attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#connection_attributes GoogleDatastreamConnectionProfile#connection_attributes}
        :param password: Password for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        :param port: Port for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#port GoogleDatastreamConnectionProfile#port}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_password GoogleDatastreamConnectionProfile#secret_manager_stored_password}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9662007413da42d3060218fabb0f6dd2085dba719d0243aaa5045e77955a0d05)
            check_type(argname="argument database_service", value=database_service, expected_type=type_hints["database_service"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument connection_attributes", value=connection_attributes, expected_type=type_hints["connection_attributes"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument secret_manager_stored_password", value=secret_manager_stored_password, expected_type=type_hints["secret_manager_stored_password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_service": database_service,
            "hostname": hostname,
            "username": username,
        }
        if connection_attributes is not None:
            self._values["connection_attributes"] = connection_attributes
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if secret_manager_stored_password is not None:
            self._values["secret_manager_stored_password"] = secret_manager_stored_password

    @builtins.property
    def database_service(self) -> builtins.str:
        '''Database for the Oracle connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#database_service GoogleDatastreamConnectionProfile#database_service}
        '''
        result = self._values.get("database_service")
        assert result is not None, "Required property 'database_service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> builtins.str:
        '''Hostname for the Oracle connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#hostname GoogleDatastreamConnectionProfile#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for the Oracle connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connection_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Connection string attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#connection_attributes GoogleDatastreamConnectionProfile#connection_attributes}
        '''
        result = self._values.get("connection_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for the Oracle connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port for the Oracle connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#port GoogleDatastreamConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_manager_stored_password(self) -> typing.Optional[builtins.str]:
        '''A reference to a Secret Manager resource name storing the user's password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_password GoogleDatastreamConnectionProfile#secret_manager_stored_password}
        '''
        result = self._values.get("secret_manager_stored_password")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatastreamConnectionProfileOracleProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatastreamConnectionProfileOracleProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileOracleProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0f490b6ceab9a7f6d316cd9c146a684eb2f6b661fbe38d8cc9ece28039d6e5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConnectionAttributes")
    def reset_connection_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionAttributes", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetSecretManagerStoredPassword")
    def reset_secret_manager_stored_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretManagerStoredPassword", []))

    @builtins.property
    @jsii.member(jsii_name="connectionAttributesInput")
    def connection_attributes_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "connectionAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseServiceInput")
    def database_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredPasswordInput")
    def secret_manager_stored_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretManagerStoredPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionAttributes")
    def connection_attributes(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "connectionAttributes"))

    @connection_attributes.setter
    def connection_attributes(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c6b08e63c1e4a24048dca18b229acfbc92b5a3faf15cfbfa826b93d2bb11a68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionAttributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseService")
    def database_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseService"))

    @database_service.setter
    def database_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f281bea093568633e8dc2b389e44c922628e70173b744ff6ad26b5dcfce65755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d7c4cc462445bc16e8473390528b79cd7b360e61d1aee93de63501657c70b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38b5f4c76a421740313af11d7a046e34497ee13f2f6cd2b49fefc7d090c1951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ace61c93384c63d393d6c2839df038c561f4c2efa70268ba363f9dadf75a03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredPassword")
    def secret_manager_stored_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretManagerStoredPassword"))

    @secret_manager_stored_password.setter
    def secret_manager_stored_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1a140856fee6da7fba163da77b0983fd47617c514706ae0a230309ec3df8cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretManagerStoredPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac55ebb8a5cb80edec2d0b317edb652164142aed014b36abde39af2e4f142c85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatastreamConnectionProfileOracleProfile]:
        return typing.cast(typing.Optional[GoogleDatastreamConnectionProfileOracleProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatastreamConnectionProfileOracleProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e53fdc3b6c03fb46906fb593d0f43c43c21790fda6d6c866c95e22b97ebda8f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfilePostgresqlProfile",
    jsii_struct_bases=[],
    name_mapping={
        "database": "database",
        "hostname": "hostname",
        "username": "username",
        "password": "password",
        "port": "port",
        "secret_manager_stored_password": "secretManagerStoredPassword",
    },
)
class GoogleDatastreamConnectionProfilePostgresqlProfile:
    def __init__(
        self,
        *,
        database: builtins.str,
        hostname: builtins.str,
        username: builtins.str,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        secret_manager_stored_password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database: Database for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#database GoogleDatastreamConnectionProfile#database}
        :param hostname: Hostname for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#hostname GoogleDatastreamConnectionProfile#hostname}
        :param username: Username for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        :param password: Password for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        :param port: Port for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#port GoogleDatastreamConnectionProfile#port}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_password GoogleDatastreamConnectionProfile#secret_manager_stored_password}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b173cf7280ddb041e7a9f07ed1c2c54ebe33a5a75e9e43dd8734e82a78f3e151)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument secret_manager_stored_password", value=secret_manager_stored_password, expected_type=type_hints["secret_manager_stored_password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "hostname": hostname,
            "username": username,
        }
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if secret_manager_stored_password is not None:
            self._values["secret_manager_stored_password"] = secret_manager_stored_password

    @builtins.property
    def database(self) -> builtins.str:
        '''Database for the PostgreSQL connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#database GoogleDatastreamConnectionProfile#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> builtins.str:
        '''Hostname for the PostgreSQL connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#hostname GoogleDatastreamConnectionProfile#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for the PostgreSQL connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for the PostgreSQL connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port for the PostgreSQL connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#port GoogleDatastreamConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_manager_stored_password(self) -> typing.Optional[builtins.str]:
        '''A reference to a Secret Manager resource name storing the user's password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_password GoogleDatastreamConnectionProfile#secret_manager_stored_password}
        '''
        result = self._values.get("secret_manager_stored_password")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatastreamConnectionProfilePostgresqlProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatastreamConnectionProfilePostgresqlProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfilePostgresqlProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f9bbac4265d2af2f2b761fcf9245d516f0fc475a5ae3b54cba669441fbb1b65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetSecretManagerStoredPassword")
    def reset_secret_manager_stored_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretManagerStoredPassword", []))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredPasswordInput")
    def secret_manager_stored_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretManagerStoredPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f458c216a74c1c385f0e9c0be3c833cf066433374d7f799b3beae63116c1cde6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a14bd26d89ddfef5dd62ebd00af8fd8b0efd65b8b2036a36598dfa71d69f3e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6da7781f1d016f32f6a36cd7dbb649c358ef972fd96d8be968b3780eb16067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3571fdea9e6d562b689b7a90f9d3a2b5b4a505ff2304b76cd5dbcb8cbfb2557d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredPassword")
    def secret_manager_stored_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretManagerStoredPassword"))

    @secret_manager_stored_password.setter
    def secret_manager_stored_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e40ea0c93ffab1b6b4d3d75158932690cc1895c2cb1af92afcc54619c9ee8229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretManagerStoredPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aaf7b2afb17b935b3165cc5c3a6163bfdb569b410b2bdb6c343e7718fa988ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatastreamConnectionProfilePostgresqlProfile]:
        return typing.cast(typing.Optional[GoogleDatastreamConnectionProfilePostgresqlProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatastreamConnectionProfilePostgresqlProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c88577540044f07eb0682a73a82140cf34e0c87182f26feff92a4724fe2e873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfilePrivateConnectivity",
    jsii_struct_bases=[],
    name_mapping={"private_connection": "privateConnection"},
)
class GoogleDatastreamConnectionProfilePrivateConnectivity:
    def __init__(self, *, private_connection: builtins.str) -> None:
        '''
        :param private_connection: A reference to a private connection resource. Format: 'projects/{project}/locations/{location}/privateConnections/{name}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#private_connection GoogleDatastreamConnectionProfile#private_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23828d599e4a7c0d2612f3779e56efe093352db0ee5bed7640cc787cba04778f)
            check_type(argname="argument private_connection", value=private_connection, expected_type=type_hints["private_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "private_connection": private_connection,
        }

    @builtins.property
    def private_connection(self) -> builtins.str:
        '''A reference to a private connection resource. Format: 'projects/{project}/locations/{location}/privateConnections/{name}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#private_connection GoogleDatastreamConnectionProfile#private_connection}
        '''
        result = self._values.get("private_connection")
        assert result is not None, "Required property 'private_connection' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatastreamConnectionProfilePrivateConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatastreamConnectionProfilePrivateConnectivityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfilePrivateConnectivityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__816c0fb0efb85478fec71dd0e7b94f21325f809d647b8d5e5b3d128d30bdb24e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="privateConnectionInput")
    def private_connection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="privateConnection")
    def private_connection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateConnection"))

    @private_connection.setter
    def private_connection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae132036e807e06f42cee981b8bda8f62aef85982f3e4edf1ec5b121425754aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateConnection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatastreamConnectionProfilePrivateConnectivity]:
        return typing.cast(typing.Optional[GoogleDatastreamConnectionProfilePrivateConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatastreamConnectionProfilePrivateConnectivity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84d90d6090eeb736f960a5f15b47f0fd7bfc3d775b81caec38be84ec22e8b978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileSalesforceProfile",
    jsii_struct_bases=[],
    name_mapping={
        "domain": "domain",
        "oauth2_client_credentials": "oauth2ClientCredentials",
        "user_credentials": "userCredentials",
    },
)
class GoogleDatastreamConnectionProfileSalesforceProfile:
    def __init__(
        self,
        *,
        domain: builtins.str,
        oauth2_client_credentials: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        user_credentials: typing.Optional[typing.Union["GoogleDatastreamConnectionProfileSalesforceProfileUserCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param domain: Domain for the Salesforce Org. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#domain GoogleDatastreamConnectionProfile#domain}
        :param oauth2_client_credentials: oauth2_client_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#oauth2_client_credentials GoogleDatastreamConnectionProfile#oauth2_client_credentials}
        :param user_credentials: user_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#user_credentials GoogleDatastreamConnectionProfile#user_credentials}
        '''
        if isinstance(oauth2_client_credentials, dict):
            oauth2_client_credentials = GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentials(**oauth2_client_credentials)
        if isinstance(user_credentials, dict):
            user_credentials = GoogleDatastreamConnectionProfileSalesforceProfileUserCredentials(**user_credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7731eb2b6afc437128b5482fc1a013c2ba6757d13dc9d3d750719bf14b8c10c)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument oauth2_client_credentials", value=oauth2_client_credentials, expected_type=type_hints["oauth2_client_credentials"])
            check_type(argname="argument user_credentials", value=user_credentials, expected_type=type_hints["user_credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain": domain,
        }
        if oauth2_client_credentials is not None:
            self._values["oauth2_client_credentials"] = oauth2_client_credentials
        if user_credentials is not None:
            self._values["user_credentials"] = user_credentials

    @builtins.property
    def domain(self) -> builtins.str:
        '''Domain for the Salesforce Org.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#domain GoogleDatastreamConnectionProfile#domain}
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth2_client_credentials(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentials"]:
        '''oauth2_client_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#oauth2_client_credentials GoogleDatastreamConnectionProfile#oauth2_client_credentials}
        '''
        result = self._values.get("oauth2_client_credentials")
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentials"], result)

    @builtins.property
    def user_credentials(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileSalesforceProfileUserCredentials"]:
        '''user_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#user_credentials GoogleDatastreamConnectionProfile#user_credentials}
        '''
        result = self._values.get("user_credentials")
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileSalesforceProfileUserCredentials"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatastreamConnectionProfileSalesforceProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "secret_manager_stored_client_secret": "secretManagerStoredClientSecret",
    },
)
class GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentials:
    def __init__(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        secret_manager_stored_client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Client ID to use for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#client_id GoogleDatastreamConnectionProfile#client_id}
        :param client_secret: Client secret to use for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#client_secret GoogleDatastreamConnectionProfile#client_secret}
        :param secret_manager_stored_client_secret: A reference to a Secret Manager resource name storing the client secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_client_secret GoogleDatastreamConnectionProfile#secret_manager_stored_client_secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c72e0b4a3528b01a329f14fd76cfe01879dc9a000c4c09e0a1fd082611c9c65)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument secret_manager_stored_client_secret", value=secret_manager_stored_client_secret, expected_type=type_hints["secret_manager_stored_client_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if secret_manager_stored_client_secret is not None:
            self._values["secret_manager_stored_client_secret"] = secret_manager_stored_client_secret

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Client ID to use for authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#client_id GoogleDatastreamConnectionProfile#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Client secret to use for authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#client_secret GoogleDatastreamConnectionProfile#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_manager_stored_client_secret(self) -> typing.Optional[builtins.str]:
        '''A reference to a Secret Manager resource name storing the client secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_client_secret GoogleDatastreamConnectionProfile#secret_manager_stored_client_secret}
        '''
        result = self._values.get("secret_manager_stored_client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__041da4efc4e4ba2545f1b33396b66bbfa8e84eabf3faf0954510c1bf19c93c8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetSecretManagerStoredClientSecret")
    def reset_secret_manager_stored_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretManagerStoredClientSecret", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredClientSecretInput")
    def secret_manager_stored_client_secret_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretManagerStoredClientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e110a33b9a5a88c30c75b3182356b5b837260b3f7b012fe293218bbfb8fcfbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573409c50c4ba7f999bc9b7e0a8897ad8bfebe7dd757c6ccb50242971ff8e9bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredClientSecret")
    def secret_manager_stored_client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretManagerStoredClientSecret"))

    @secret_manager_stored_client_secret.setter
    def secret_manager_stored_client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed7fe388d4c58bc2250054673272d988ae715a80fceeb369bbb6bc73f6e7084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretManagerStoredClientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentials]:
        return typing.cast(typing.Optional[GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c96d8f80306fe90e27ab3e1139ef7e2409bf0103da8344f00353ad45ab0bd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDatastreamConnectionProfileSalesforceProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileSalesforceProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7586b996d9c9c6eb22d0d39d94ee15802622b300ec13324b01609eae7a40711a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauth2ClientCredentials")
    def put_oauth2_client_credentials(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        secret_manager_stored_client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Client ID to use for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#client_id GoogleDatastreamConnectionProfile#client_id}
        :param client_secret: Client secret to use for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#client_secret GoogleDatastreamConnectionProfile#client_secret}
        :param secret_manager_stored_client_secret: A reference to a Secret Manager resource name storing the client secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_client_secret GoogleDatastreamConnectionProfile#secret_manager_stored_client_secret}
        '''
        value = GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentials(
            client_id=client_id,
            client_secret=client_secret,
            secret_manager_stored_client_secret=secret_manager_stored_client_secret,
        )

        return typing.cast(None, jsii.invoke(self, "putOauth2ClientCredentials", [value]))

    @jsii.member(jsii_name="putUserCredentials")
    def put_user_credentials(
        self,
        *,
        password: typing.Optional[builtins.str] = None,
        secret_manager_stored_password: typing.Optional[builtins.str] = None,
        secret_manager_stored_security_token: typing.Optional[builtins.str] = None,
        security_token: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: Password of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_password GoogleDatastreamConnectionProfile#secret_manager_stored_password}
        :param secret_manager_stored_security_token: A reference to a Secret Manager resource name storing the user's security token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_security_token GoogleDatastreamConnectionProfile#secret_manager_stored_security_token}
        :param security_token: Security token of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#security_token GoogleDatastreamConnectionProfile#security_token}
        :param username: Username to use for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        '''
        value = GoogleDatastreamConnectionProfileSalesforceProfileUserCredentials(
            password=password,
            secret_manager_stored_password=secret_manager_stored_password,
            secret_manager_stored_security_token=secret_manager_stored_security_token,
            security_token=security_token,
            username=username,
        )

        return typing.cast(None, jsii.invoke(self, "putUserCredentials", [value]))

    @jsii.member(jsii_name="resetOauth2ClientCredentials")
    def reset_oauth2_client_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2ClientCredentials", []))

    @jsii.member(jsii_name="resetUserCredentials")
    def reset_user_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserCredentials", []))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientCredentials")
    def oauth2_client_credentials(
        self,
    ) -> GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentialsOutputReference:
        return typing.cast(GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentialsOutputReference, jsii.get(self, "oauth2ClientCredentials"))

    @builtins.property
    @jsii.member(jsii_name="userCredentials")
    def user_credentials(
        self,
    ) -> "GoogleDatastreamConnectionProfileSalesforceProfileUserCredentialsOutputReference":
        return typing.cast("GoogleDatastreamConnectionProfileSalesforceProfileUserCredentialsOutputReference", jsii.get(self, "userCredentials"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientCredentialsInput")
    def oauth2_client_credentials_input(
        self,
    ) -> typing.Optional[GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentials]:
        return typing.cast(typing.Optional[GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentials], jsii.get(self, "oauth2ClientCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="userCredentialsInput")
    def user_credentials_input(
        self,
    ) -> typing.Optional["GoogleDatastreamConnectionProfileSalesforceProfileUserCredentials"]:
        return typing.cast(typing.Optional["GoogleDatastreamConnectionProfileSalesforceProfileUserCredentials"], jsii.get(self, "userCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fd0df86f62fdbdc5d102fcef493c3b956d23a1b24966fd7c2041d5c94bc90a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatastreamConnectionProfileSalesforceProfile]:
        return typing.cast(typing.Optional[GoogleDatastreamConnectionProfileSalesforceProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatastreamConnectionProfileSalesforceProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125c7cc2a6f06627473afad900aede3acdd8dd3960afad70a2efd0c8a179df57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileSalesforceProfileUserCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "password": "password",
        "secret_manager_stored_password": "secretManagerStoredPassword",
        "secret_manager_stored_security_token": "secretManagerStoredSecurityToken",
        "security_token": "securityToken",
        "username": "username",
    },
)
class GoogleDatastreamConnectionProfileSalesforceProfileUserCredentials:
    def __init__(
        self,
        *,
        password: typing.Optional[builtins.str] = None,
        secret_manager_stored_password: typing.Optional[builtins.str] = None,
        secret_manager_stored_security_token: typing.Optional[builtins.str] = None,
        security_token: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: Password of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_password GoogleDatastreamConnectionProfile#secret_manager_stored_password}
        :param secret_manager_stored_security_token: A reference to a Secret Manager resource name storing the user's security token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_security_token GoogleDatastreamConnectionProfile#secret_manager_stored_security_token}
        :param security_token: Security token of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#security_token GoogleDatastreamConnectionProfile#security_token}
        :param username: Username to use for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d8eae5d241055fcc2dfa2bc9d26b27632752f4c06bd1b261198d408efc59f1)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument secret_manager_stored_password", value=secret_manager_stored_password, expected_type=type_hints["secret_manager_stored_password"])
            check_type(argname="argument secret_manager_stored_security_token", value=secret_manager_stored_security_token, expected_type=type_hints["secret_manager_stored_security_token"])
            check_type(argname="argument security_token", value=security_token, expected_type=type_hints["security_token"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if password is not None:
            self._values["password"] = password
        if secret_manager_stored_password is not None:
            self._values["secret_manager_stored_password"] = secret_manager_stored_password
        if secret_manager_stored_security_token is not None:
            self._values["secret_manager_stored_security_token"] = secret_manager_stored_security_token
        if security_token is not None:
            self._values["security_token"] = security_token
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password of the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_manager_stored_password(self) -> typing.Optional[builtins.str]:
        '''A reference to a Secret Manager resource name storing the user's password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_password GoogleDatastreamConnectionProfile#secret_manager_stored_password}
        '''
        result = self._values.get("secret_manager_stored_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_manager_stored_security_token(self) -> typing.Optional[builtins.str]:
        '''A reference to a Secret Manager resource name storing the user's security token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_security_token GoogleDatastreamConnectionProfile#secret_manager_stored_security_token}
        '''
        result = self._values.get("secret_manager_stored_security_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_token(self) -> typing.Optional[builtins.str]:
        '''Security token of the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#security_token GoogleDatastreamConnectionProfile#security_token}
        '''
        result = self._values.get("security_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username to use for authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatastreamConnectionProfileSalesforceProfileUserCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatastreamConnectionProfileSalesforceProfileUserCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileSalesforceProfileUserCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b44e218a1f9ec8e2d1b908ba49cc7611b9865743c885690b97713e04d72bc4ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetSecretManagerStoredPassword")
    def reset_secret_manager_stored_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretManagerStoredPassword", []))

    @jsii.member(jsii_name="resetSecretManagerStoredSecurityToken")
    def reset_secret_manager_stored_security_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretManagerStoredSecurityToken", []))

    @jsii.member(jsii_name="resetSecurityToken")
    def reset_security_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityToken", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredPasswordInput")
    def secret_manager_stored_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretManagerStoredPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredSecurityTokenInput")
    def secret_manager_stored_security_token_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretManagerStoredSecurityTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="securityTokenInput")
    def security_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7ef7d54bfcf8d374f078f69a305e8cae0c6a33bc34bfe3f1de548a821c9a609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredPassword")
    def secret_manager_stored_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretManagerStoredPassword"))

    @secret_manager_stored_password.setter
    def secret_manager_stored_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fe0615e68cb8545a044634cd6adc730b504fc2e954e2cd494ba8c9af9b003cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretManagerStoredPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredSecurityToken")
    def secret_manager_stored_security_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretManagerStoredSecurityToken"))

    @secret_manager_stored_security_token.setter
    def secret_manager_stored_security_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f1128e19b6a585960cec1088942c96775fc0e0f894dcd7471042722128095e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretManagerStoredSecurityToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityToken")
    def security_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityToken"))

    @security_token.setter
    def security_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__190e9bd186885980ed92f953d555f38406656bf74d510d3036d0f1f40030d7c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d170ad59cc4de7cbe2400716f153e1bd9689324d535b5c5a4a6bd8f2ef1e845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatastreamConnectionProfileSalesforceProfileUserCredentials]:
        return typing.cast(typing.Optional[GoogleDatastreamConnectionProfileSalesforceProfileUserCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatastreamConnectionProfileSalesforceProfileUserCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf7918afee1748ad5f32260e5c72b34b75edd290a7de7fd1863017e6a0783b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileSqlServerProfile",
    jsii_struct_bases=[],
    name_mapping={
        "database": "database",
        "hostname": "hostname",
        "username": "username",
        "password": "password",
        "port": "port",
        "secret_manager_stored_password": "secretManagerStoredPassword",
    },
)
class GoogleDatastreamConnectionProfileSqlServerProfile:
    def __init__(
        self,
        *,
        database: builtins.str,
        hostname: builtins.str,
        username: builtins.str,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        secret_manager_stored_password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database: Database for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#database GoogleDatastreamConnectionProfile#database}
        :param hostname: Hostname for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#hostname GoogleDatastreamConnectionProfile#hostname}
        :param username: Username for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        :param password: Password for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        :param port: Port for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#port GoogleDatastreamConnectionProfile#port}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_password GoogleDatastreamConnectionProfile#secret_manager_stored_password}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc07de7fd3107be65eb05e9769aeb22efcf6ed959ec1662069df10e68cf21279)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument secret_manager_stored_password", value=secret_manager_stored_password, expected_type=type_hints["secret_manager_stored_password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "hostname": hostname,
            "username": username,
        }
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if secret_manager_stored_password is not None:
            self._values["secret_manager_stored_password"] = secret_manager_stored_password

    @builtins.property
    def database(self) -> builtins.str:
        '''Database for the SQL Server connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#database GoogleDatastreamConnectionProfile#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> builtins.str:
        '''Hostname for the SQL Server connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#hostname GoogleDatastreamConnectionProfile#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for the SQL Server connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#username GoogleDatastreamConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for the SQL Server connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#password GoogleDatastreamConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port for the SQL Server connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#port GoogleDatastreamConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_manager_stored_password(self) -> typing.Optional[builtins.str]:
        '''A reference to a Secret Manager resource name storing the user's password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#secret_manager_stored_password GoogleDatastreamConnectionProfile#secret_manager_stored_password}
        '''
        result = self._values.get("secret_manager_stored_password")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatastreamConnectionProfileSqlServerProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatastreamConnectionProfileSqlServerProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileSqlServerProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfa9f50a3e37f50d13273074f2e7d299c1b356871de49d1be18f37c7ef8f8523)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetSecretManagerStoredPassword")
    def reset_secret_manager_stored_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretManagerStoredPassword", []))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredPasswordInput")
    def secret_manager_stored_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretManagerStoredPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5628a8c1332f2de98350331a1d11baeef02598fbcef204e411067feebaa6a05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c00cc1f773ac4fc32327e475d2123be132a61450f0b69de86645197eb1ae16bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e47721167b85be3bd74764f0c19ff6badd757a5e660ed16f1ee9c8759db75ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c9252b094918950889a4fa6efca6d11d3a63349d4df16ddaf11b64bf9fcff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredPassword")
    def secret_manager_stored_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretManagerStoredPassword"))

    @secret_manager_stored_password.setter
    def secret_manager_stored_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a2e7c8602a3cddb05a89fc2d243b94b7ab9b7f707d0d9674502198045443f9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretManagerStoredPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b356d7d3315f5597afdc4e32604d36ebbf1ba9c5fe82982791e89f7a88c47a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatastreamConnectionProfileSqlServerProfile]:
        return typing.cast(typing.Optional[GoogleDatastreamConnectionProfileSqlServerProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatastreamConnectionProfileSqlServerProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e4bb879ee4e1995bc8108f7c38f9a71682e21b7966ba4f82ceca42ce8a009e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDatastreamConnectionProfileTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#create GoogleDatastreamConnectionProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#delete GoogleDatastreamConnectionProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#update GoogleDatastreamConnectionProfile#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce93c0fd6deead03bd05b05ce217d17cb40ca9e050be254d3fa3099a3e1bb31a)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#create GoogleDatastreamConnectionProfile#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#delete GoogleDatastreamConnectionProfile#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_datastream_connection_profile#update GoogleDatastreamConnectionProfile#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatastreamConnectionProfileTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatastreamConnectionProfileTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatastreamConnectionProfile.GoogleDatastreamConnectionProfileTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a86f6e7cbe19ac8228e891cb7504498990c93f9b818164b30dfe14612d1eac7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6d6ee028a796d7fe3846b6fe1c69c108b320f79376d57fede70396535dea4b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b05a8a6a6dfec9a13b9b56ceefad8c79f5f296356cb36c66c5a2a1a7b6e92eb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65e5c677b938bc2e96c220f5a9aa1d01d9c65f051e19d387106c10b4e2e87583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatastreamConnectionProfileTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatastreamConnectionProfileTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatastreamConnectionProfileTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c5efb63c139de3658e6fab3614a9d8877afaf76f8b1e7742cb8ef586484f26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDatastreamConnectionProfile",
    "GoogleDatastreamConnectionProfileBigqueryProfile",
    "GoogleDatastreamConnectionProfileBigqueryProfileOutputReference",
    "GoogleDatastreamConnectionProfileConfig",
    "GoogleDatastreamConnectionProfileForwardSshConnectivity",
    "GoogleDatastreamConnectionProfileForwardSshConnectivityOutputReference",
    "GoogleDatastreamConnectionProfileGcsProfile",
    "GoogleDatastreamConnectionProfileGcsProfileOutputReference",
    "GoogleDatastreamConnectionProfileMysqlProfile",
    "GoogleDatastreamConnectionProfileMysqlProfileOutputReference",
    "GoogleDatastreamConnectionProfileMysqlProfileSslConfig",
    "GoogleDatastreamConnectionProfileMysqlProfileSslConfigOutputReference",
    "GoogleDatastreamConnectionProfileOracleProfile",
    "GoogleDatastreamConnectionProfileOracleProfileOutputReference",
    "GoogleDatastreamConnectionProfilePostgresqlProfile",
    "GoogleDatastreamConnectionProfilePostgresqlProfileOutputReference",
    "GoogleDatastreamConnectionProfilePrivateConnectivity",
    "GoogleDatastreamConnectionProfilePrivateConnectivityOutputReference",
    "GoogleDatastreamConnectionProfileSalesforceProfile",
    "GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentials",
    "GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentialsOutputReference",
    "GoogleDatastreamConnectionProfileSalesforceProfileOutputReference",
    "GoogleDatastreamConnectionProfileSalesforceProfileUserCredentials",
    "GoogleDatastreamConnectionProfileSalesforceProfileUserCredentialsOutputReference",
    "GoogleDatastreamConnectionProfileSqlServerProfile",
    "GoogleDatastreamConnectionProfileSqlServerProfileOutputReference",
    "GoogleDatastreamConnectionProfileTimeouts",
    "GoogleDatastreamConnectionProfileTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__37c025b707bafbe1605b24d076e3fe778ff8ffc1eb64d5f83a61b70121507da1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    connection_profile_id: builtins.str,
    display_name: builtins.str,
    location: builtins.str,
    bigquery_profile: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileBigqueryProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    create_without_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forward_ssh_connectivity: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileForwardSshConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs_profile: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileGcsProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mysql_profile: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileMysqlProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    oracle_profile: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileOracleProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    postgresql_profile: typing.Optional[typing.Union[GoogleDatastreamConnectionProfilePostgresqlProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    private_connectivity: typing.Optional[typing.Union[GoogleDatastreamConnectionProfilePrivateConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    salesforce_profile: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileSalesforceProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    sql_server_profile: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileSqlServerProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7ed71633433e7fb41d54ec37f23ca4b5d70c61430091d11cedc3c47e9d42c23f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a954a35a4da09190999a985a8a5397b03bbef43e3feeb5e7f8b89c8aa8e98139(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb967db6c12045e52a39294c43218f35056bb11a37bbc527553dd08af6b3ba8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22de0186e58c1f64abfe601f7355907fe81f60d93409ebdcd5e414360d60d6b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c06dc2765f8b068770b76b53e3f3fa7bce2f551ddf49e5ad7d5e6176d13d42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c76183c236282f7dd139e5e8807c019f97d3e93df01d765ffefecbacf55c9e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510def3c54ba7446ef8c8eae2bec58049c2f1d6c0900c03465015bcec144bde1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d7179cafd457d68cdbc09f2c0d6220b32f114af9bcb9b97fc64d7af4b22df1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e3bbd28ef2515dd9cc9072d23ae81fbd6ef455ad4c587cb4e20faeb882a06b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0f9f5642ff9a298e1931841f9f8a0f8452c625114f6da702366e7302fb180f(
    value: typing.Optional[GoogleDatastreamConnectionProfileBigqueryProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d76c8a675707d09d73528c9de0908f53419150d9e1bcbcd92da96b8bfe0dce9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection_profile_id: builtins.str,
    display_name: builtins.str,
    location: builtins.str,
    bigquery_profile: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileBigqueryProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    create_without_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forward_ssh_connectivity: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileForwardSshConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs_profile: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileGcsProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mysql_profile: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileMysqlProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    oracle_profile: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileOracleProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    postgresql_profile: typing.Optional[typing.Union[GoogleDatastreamConnectionProfilePostgresqlProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    private_connectivity: typing.Optional[typing.Union[GoogleDatastreamConnectionProfilePrivateConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    salesforce_profile: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileSalesforceProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    sql_server_profile: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileSqlServerProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__898b49febbfd20102d4d918be1907067211b06d866e869ed02325d9b7b071717(
    *,
    hostname: builtins.str,
    username: builtins.str,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    private_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab34a3ad9c4fab9ef80bde8f769b5983d36ff181bba13ef367f9b893ffa7bda(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725084f46e39078f6024fd0671c96dfbd6dc4d5e49acdaa29c2c6e1328cc4844(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da96edd9b84b64672117f5a284cecdbaa5d7d2b2f8d4e213e0b61995839ec56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3b6afed0107cb7325ab3ba5c7f77e3ca333e3411de2d8f47bd64e534b55e3f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e1eda28eb3c256d292f8254ad001d114d61dbacd492719cd148de54becbd84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5665cf24ed8693ff398ba5062c59fd868f5c3bb3ee62409916f26478afb96a99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c3add45012b8d98389c7a11197322d34ce87b9508063065e10a9456aa93b428(
    value: typing.Optional[GoogleDatastreamConnectionProfileForwardSshConnectivity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83ca2cc5573d02b04aa4b260739729db1fb993d0c483e36d23ee943c485b9d1(
    *,
    bucket: builtins.str,
    root_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982aaa0b9b3c7a34bec17f7b9b5beea7f0569d3346b938a7591984eddbeb13d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555f62bc769a5fe35d1746b68ffb7282a2dd37bf817c331192a108ed26ed4b8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c16a7ce04103b7905f741c4c792e365622c5b0b96299af0b89a9ee0b5b78ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd02487b575cc3309bcc24daa5b741408cd7747d159a4590a83801cd6bf3da2(
    value: typing.Optional[GoogleDatastreamConnectionProfileGcsProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7401859cd51507652b057cf22bd22d76c2cebbe04b305c6303d69445df564cc(
    *,
    hostname: builtins.str,
    username: builtins.str,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    secret_manager_stored_password: typing.Optional[builtins.str] = None,
    ssl_config: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileMysqlProfileSslConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__483e608169e9ed202cf8688ea06f6cb1806389166db00ccb8727f8c78f55042b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9ec72300927cd13cec9a1a7c2c9d8fd2b2d6185706998b39fdb77267e7fc52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c7b1b4f2c9eca1812d57e69a603894de8b0e29b779971621d7b3ac5d108408(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc9032809bbb4a6b403ba995b3dd6fe63575e2f720575caa1a1f212460ac439d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b727ae49fe4a984616281e5046a996ff2753c7fdc5817abde2d12c7fd27591c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591745bb73df6675029344ae13c1b369a641b3f38906ddc2e23df885e48875ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1997f4dedbf609d3ebba80e6d3aba4336f6a9c9aa59462baa0b0a1d9c109a93f(
    value: typing.Optional[GoogleDatastreamConnectionProfileMysqlProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ccffedae518b06bd344ecf910a151bb2126dc4d9d992330bcd0694aed895da(
    *,
    ca_certificate: typing.Optional[builtins.str] = None,
    client_certificate: typing.Optional[builtins.str] = None,
    client_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740e78106914654eee1e46ad982fff7f4f9952c2ea88f36dca3b14c9cd755d3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e458d7e54ab8f7ab1dda35b662f2d59af8a809541aa1b0ad5d99b18b3540f13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8f1f357ef2c243c40ce562b122699bb6870598af0442f4ab85cfb82a0ea4db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83019c9a78d673a5bd633ff22e5da184d20e95159d0dfc677e125906dbc87533(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b0ad3a36da99c9c6f61861f5c30abab76ac3fd9268b15811b9da8d2d9a1946(
    value: typing.Optional[GoogleDatastreamConnectionProfileMysqlProfileSslConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9662007413da42d3060218fabb0f6dd2085dba719d0243aaa5045e77955a0d05(
    *,
    database_service: builtins.str,
    hostname: builtins.str,
    username: builtins.str,
    connection_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    secret_manager_stored_password: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f490b6ceab9a7f6d316cd9c146a684eb2f6b661fbe38d8cc9ece28039d6e5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c6b08e63c1e4a24048dca18b229acfbc92b5a3faf15cfbfa826b93d2bb11a68(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f281bea093568633e8dc2b389e44c922628e70173b744ff6ad26b5dcfce65755(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d7c4cc462445bc16e8473390528b79cd7b360e61d1aee93de63501657c70b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38b5f4c76a421740313af11d7a046e34497ee13f2f6cd2b49fefc7d090c1951(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ace61c93384c63d393d6c2839df038c561f4c2efa70268ba363f9dadf75a03(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1a140856fee6da7fba163da77b0983fd47617c514706ae0a230309ec3df8cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac55ebb8a5cb80edec2d0b317edb652164142aed014b36abde39af2e4f142c85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53fdc3b6c03fb46906fb593d0f43c43c21790fda6d6c866c95e22b97ebda8f7(
    value: typing.Optional[GoogleDatastreamConnectionProfileOracleProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b173cf7280ddb041e7a9f07ed1c2c54ebe33a5a75e9e43dd8734e82a78f3e151(
    *,
    database: builtins.str,
    hostname: builtins.str,
    username: builtins.str,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    secret_manager_stored_password: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9bbac4265d2af2f2b761fcf9245d516f0fc475a5ae3b54cba669441fbb1b65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f458c216a74c1c385f0e9c0be3c833cf066433374d7f799b3beae63116c1cde6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a14bd26d89ddfef5dd62ebd00af8fd8b0efd65b8b2036a36598dfa71d69f3e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6da7781f1d016f32f6a36cd7dbb649c358ef972fd96d8be968b3780eb16067(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3571fdea9e6d562b689b7a90f9d3a2b5b4a505ff2304b76cd5dbcb8cbfb2557d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40ea0c93ffab1b6b4d3d75158932690cc1895c2cb1af92afcc54619c9ee8229(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aaf7b2afb17b935b3165cc5c3a6163bfdb569b410b2bdb6c343e7718fa988ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c88577540044f07eb0682a73a82140cf34e0c87182f26feff92a4724fe2e873(
    value: typing.Optional[GoogleDatastreamConnectionProfilePostgresqlProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23828d599e4a7c0d2612f3779e56efe093352db0ee5bed7640cc787cba04778f(
    *,
    private_connection: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816c0fb0efb85478fec71dd0e7b94f21325f809d647b8d5e5b3d128d30bdb24e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae132036e807e06f42cee981b8bda8f62aef85982f3e4edf1ec5b121425754aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d90d6090eeb736f960a5f15b47f0fd7bfc3d775b81caec38be84ec22e8b978(
    value: typing.Optional[GoogleDatastreamConnectionProfilePrivateConnectivity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7731eb2b6afc437128b5482fc1a013c2ba6757d13dc9d3d750719bf14b8c10c(
    *,
    domain: builtins.str,
    oauth2_client_credentials: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    user_credentials: typing.Optional[typing.Union[GoogleDatastreamConnectionProfileSalesforceProfileUserCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c72e0b4a3528b01a329f14fd76cfe01879dc9a000c4c09e0a1fd082611c9c65(
    *,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    secret_manager_stored_client_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041da4efc4e4ba2545f1b33396b66bbfa8e84eabf3faf0954510c1bf19c93c8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e110a33b9a5a88c30c75b3182356b5b837260b3f7b012fe293218bbfb8fcfbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573409c50c4ba7f999bc9b7e0a8897ad8bfebe7dd757c6ccb50242971ff8e9bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed7fe388d4c58bc2250054673272d988ae715a80fceeb369bbb6bc73f6e7084(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c96d8f80306fe90e27ab3e1139ef7e2409bf0103da8344f00353ad45ab0bd2(
    value: typing.Optional[GoogleDatastreamConnectionProfileSalesforceProfileOauth2ClientCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7586b996d9c9c6eb22d0d39d94ee15802622b300ec13324b01609eae7a40711a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd0df86f62fdbdc5d102fcef493c3b956d23a1b24966fd7c2041d5c94bc90a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125c7cc2a6f06627473afad900aede3acdd8dd3960afad70a2efd0c8a179df57(
    value: typing.Optional[GoogleDatastreamConnectionProfileSalesforceProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d8eae5d241055fcc2dfa2bc9d26b27632752f4c06bd1b261198d408efc59f1(
    *,
    password: typing.Optional[builtins.str] = None,
    secret_manager_stored_password: typing.Optional[builtins.str] = None,
    secret_manager_stored_security_token: typing.Optional[builtins.str] = None,
    security_token: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b44e218a1f9ec8e2d1b908ba49cc7611b9865743c885690b97713e04d72bc4ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ef7d54bfcf8d374f078f69a305e8cae0c6a33bc34bfe3f1de548a821c9a609(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe0615e68cb8545a044634cd6adc730b504fc2e954e2cd494ba8c9af9b003cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1128e19b6a585960cec1088942c96775fc0e0f894dcd7471042722128095e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190e9bd186885980ed92f953d555f38406656bf74d510d3036d0f1f40030d7c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d170ad59cc4de7cbe2400716f153e1bd9689324d535b5c5a4a6bd8f2ef1e845(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf7918afee1748ad5f32260e5c72b34b75edd290a7de7fd1863017e6a0783b8(
    value: typing.Optional[GoogleDatastreamConnectionProfileSalesforceProfileUserCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc07de7fd3107be65eb05e9769aeb22efcf6ed959ec1662069df10e68cf21279(
    *,
    database: builtins.str,
    hostname: builtins.str,
    username: builtins.str,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    secret_manager_stored_password: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa9f50a3e37f50d13273074f2e7d299c1b356871de49d1be18f37c7ef8f8523(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5628a8c1332f2de98350331a1d11baeef02598fbcef204e411067feebaa6a05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00cc1f773ac4fc32327e475d2123be132a61450f0b69de86645197eb1ae16bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e47721167b85be3bd74764f0c19ff6badd757a5e660ed16f1ee9c8759db75ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c9252b094918950889a4fa6efca6d11d3a63349d4df16ddaf11b64bf9fcff1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2e7c8602a3cddb05a89fc2d243b94b7ab9b7f707d0d9674502198045443f9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b356d7d3315f5597afdc4e32604d36ebbf1ba9c5fe82982791e89f7a88c47a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e4bb879ee4e1995bc8108f7c38f9a71682e21b7966ba4f82ceca42ce8a009e(
    value: typing.Optional[GoogleDatastreamConnectionProfileSqlServerProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce93c0fd6deead03bd05b05ce217d17cb40ca9e050be254d3fa3099a3e1bb31a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a86f6e7cbe19ac8228e891cb7504498990c93f9b818164b30dfe14612d1eac7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6ee028a796d7fe3846b6fe1c69c108b320f79376d57fede70396535dea4b74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b05a8a6a6dfec9a13b9b56ceefad8c79f5f296356cb36c66c5a2a1a7b6e92eb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e5c677b938bc2e96c220f5a9aa1d01d9c65f051e19d387106c10b4e2e87583(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c5efb63c139de3658e6fab3614a9d8877afaf76f8b1e7742cb8ef586484f26(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatastreamConnectionProfileTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
