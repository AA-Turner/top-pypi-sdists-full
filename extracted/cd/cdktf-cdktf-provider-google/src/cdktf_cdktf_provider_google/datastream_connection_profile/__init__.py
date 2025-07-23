r'''
# `google_datastream_connection_profile`

Refer to the Terraform Registry for docs: [`google_datastream_connection_profile`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile).
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


class DatastreamConnectionProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile google_datastream_connection_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        connection_profile_id: builtins.str,
        display_name: builtins.str,
        location: builtins.str,
        bigquery_profile: typing.Optional[typing.Union["DatastreamConnectionProfileBigqueryProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        create_without_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forward_ssh_connectivity: typing.Optional[typing.Union["DatastreamConnectionProfileForwardSshConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_profile: typing.Optional[typing.Union["DatastreamConnectionProfileGcsProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mysql_profile: typing.Optional[typing.Union["DatastreamConnectionProfileMysqlProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle_profile: typing.Optional[typing.Union["DatastreamConnectionProfileOracleProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql_profile: typing.Optional[typing.Union["DatastreamConnectionProfilePostgresqlProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        private_connectivity: typing.Optional[typing.Union["DatastreamConnectionProfilePrivateConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        sql_server_profile: typing.Optional[typing.Union["DatastreamConnectionProfileSqlServerProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DatastreamConnectionProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile google_datastream_connection_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param connection_profile_id: The connection profile identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#connection_profile_id DatastreamConnectionProfile#connection_profile_id}
        :param display_name: Display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#display_name DatastreamConnectionProfile#display_name}
        :param location: The name of the location this connection profile is located in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#location DatastreamConnectionProfile#location}
        :param bigquery_profile: bigquery_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#bigquery_profile DatastreamConnectionProfile#bigquery_profile}
        :param create_without_validation: Create the connection profile without validating it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#create_without_validation DatastreamConnectionProfile#create_without_validation}
        :param forward_ssh_connectivity: forward_ssh_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#forward_ssh_connectivity DatastreamConnectionProfile#forward_ssh_connectivity}
        :param gcs_profile: gcs_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#gcs_profile DatastreamConnectionProfile#gcs_profile}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#id DatastreamConnectionProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#labels DatastreamConnectionProfile#labels}
        :param mysql_profile: mysql_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#mysql_profile DatastreamConnectionProfile#mysql_profile}
        :param oracle_profile: oracle_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#oracle_profile DatastreamConnectionProfile#oracle_profile}
        :param postgresql_profile: postgresql_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#postgresql_profile DatastreamConnectionProfile#postgresql_profile}
        :param private_connectivity: private_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#private_connectivity DatastreamConnectionProfile#private_connectivity}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#project DatastreamConnectionProfile#project}.
        :param sql_server_profile: sql_server_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#sql_server_profile DatastreamConnectionProfile#sql_server_profile}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#timeouts DatastreamConnectionProfile#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c561713e5931b76475298816158f7084a2e57a9756562dfade012aca01f69516)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DatastreamConnectionProfileConfig(
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
        '''Generates CDKTF code for importing a DatastreamConnectionProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DatastreamConnectionProfile to import.
        :param import_from_id: The id of the existing DatastreamConnectionProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DatastreamConnectionProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edc09f15ae32ab928a3477d3359deddfaf3c0e76f948c57455bdad119c024ec1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBigqueryProfile")
    def put_bigquery_profile(self) -> None:
        value = DatastreamConnectionProfileBigqueryProfile()

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
        :param hostname: Hostname for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param username: Username for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param password: SSH password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param port: Port for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#port DatastreamConnectionProfile#port}
        :param private_key: SSH private key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#private_key DatastreamConnectionProfile#private_key}
        '''
        value = DatastreamConnectionProfileForwardSshConnectivity(
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
        :param bucket: The Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#bucket DatastreamConnectionProfile#bucket}
        :param root_path: The root path inside the Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#root_path DatastreamConnectionProfile#root_path}
        '''
        value = DatastreamConnectionProfileGcsProfile(
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
        ssl_config: typing.Optional[typing.Union["DatastreamConnectionProfileMysqlProfileSslConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hostname: Hostname for the MySQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param username: Username for the MySQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param password: Password for the MySQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param port: Port for the MySQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#port DatastreamConnectionProfile#port}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#secret_manager_stored_password DatastreamConnectionProfile#secret_manager_stored_password}
        :param ssl_config: ssl_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#ssl_config DatastreamConnectionProfile#ssl_config}
        '''
        value = DatastreamConnectionProfileMysqlProfile(
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
        :param database_service: Database for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#database_service DatastreamConnectionProfile#database_service}
        :param hostname: Hostname for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param username: Username for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param connection_attributes: Connection string attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#connection_attributes DatastreamConnectionProfile#connection_attributes}
        :param password: Password for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param port: Port for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#port DatastreamConnectionProfile#port}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#secret_manager_stored_password DatastreamConnectionProfile#secret_manager_stored_password}
        '''
        value = DatastreamConnectionProfileOracleProfile(
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
        :param database: Database for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#database DatastreamConnectionProfile#database}
        :param hostname: Hostname for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param username: Username for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param password: Password for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param port: Port for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#port DatastreamConnectionProfile#port}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#secret_manager_stored_password DatastreamConnectionProfile#secret_manager_stored_password}
        '''
        value = DatastreamConnectionProfilePostgresqlProfile(
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
        :param private_connection: A reference to a private connection resource. Format: 'projects/{project}/locations/{location}/privateConnections/{name}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#private_connection DatastreamConnectionProfile#private_connection}
        '''
        value = DatastreamConnectionProfilePrivateConnectivity(
            private_connection=private_connection
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateConnectivity", [value]))

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
        :param database: Database for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#database DatastreamConnectionProfile#database}
        :param hostname: Hostname for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param username: Username for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param password: Password for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param port: Port for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#port DatastreamConnectionProfile#port}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#secret_manager_stored_password DatastreamConnectionProfile#secret_manager_stored_password}
        '''
        value = DatastreamConnectionProfileSqlServerProfile(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#create DatastreamConnectionProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#delete DatastreamConnectionProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#update DatastreamConnectionProfile#update}.
        '''
        value = DatastreamConnectionProfileTimeouts(
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
    ) -> "DatastreamConnectionProfileBigqueryProfileOutputReference":
        return typing.cast("DatastreamConnectionProfileBigqueryProfileOutputReference", jsii.get(self, "bigqueryProfile"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="forwardSshConnectivity")
    def forward_ssh_connectivity(
        self,
    ) -> "DatastreamConnectionProfileForwardSshConnectivityOutputReference":
        return typing.cast("DatastreamConnectionProfileForwardSshConnectivityOutputReference", jsii.get(self, "forwardSshConnectivity"))

    @builtins.property
    @jsii.member(jsii_name="gcsProfile")
    def gcs_profile(self) -> "DatastreamConnectionProfileGcsProfileOutputReference":
        return typing.cast("DatastreamConnectionProfileGcsProfileOutputReference", jsii.get(self, "gcsProfile"))

    @builtins.property
    @jsii.member(jsii_name="mysqlProfile")
    def mysql_profile(self) -> "DatastreamConnectionProfileMysqlProfileOutputReference":
        return typing.cast("DatastreamConnectionProfileMysqlProfileOutputReference", jsii.get(self, "mysqlProfile"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="oracleProfile")
    def oracle_profile(
        self,
    ) -> "DatastreamConnectionProfileOracleProfileOutputReference":
        return typing.cast("DatastreamConnectionProfileOracleProfileOutputReference", jsii.get(self, "oracleProfile"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlProfile")
    def postgresql_profile(
        self,
    ) -> "DatastreamConnectionProfilePostgresqlProfileOutputReference":
        return typing.cast("DatastreamConnectionProfilePostgresqlProfileOutputReference", jsii.get(self, "postgresqlProfile"))

    @builtins.property
    @jsii.member(jsii_name="privateConnectivity")
    def private_connectivity(
        self,
    ) -> "DatastreamConnectionProfilePrivateConnectivityOutputReference":
        return typing.cast("DatastreamConnectionProfilePrivateConnectivityOutputReference", jsii.get(self, "privateConnectivity"))

    @builtins.property
    @jsii.member(jsii_name="sqlServerProfile")
    def sql_server_profile(
        self,
    ) -> "DatastreamConnectionProfileSqlServerProfileOutputReference":
        return typing.cast("DatastreamConnectionProfileSqlServerProfileOutputReference", jsii.get(self, "sqlServerProfile"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DatastreamConnectionProfileTimeoutsOutputReference":
        return typing.cast("DatastreamConnectionProfileTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryProfileInput")
    def bigquery_profile_input(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileBigqueryProfile"]:
        return typing.cast(typing.Optional["DatastreamConnectionProfileBigqueryProfile"], jsii.get(self, "bigqueryProfileInput"))

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
    ) -> typing.Optional["DatastreamConnectionProfileForwardSshConnectivity"]:
        return typing.cast(typing.Optional["DatastreamConnectionProfileForwardSshConnectivity"], jsii.get(self, "forwardSshConnectivityInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsProfileInput")
    def gcs_profile_input(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileGcsProfile"]:
        return typing.cast(typing.Optional["DatastreamConnectionProfileGcsProfile"], jsii.get(self, "gcsProfileInput"))

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
    ) -> typing.Optional["DatastreamConnectionProfileMysqlProfile"]:
        return typing.cast(typing.Optional["DatastreamConnectionProfileMysqlProfile"], jsii.get(self, "mysqlProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="oracleProfileInput")
    def oracle_profile_input(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileOracleProfile"]:
        return typing.cast(typing.Optional["DatastreamConnectionProfileOracleProfile"], jsii.get(self, "oracleProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlProfileInput")
    def postgresql_profile_input(
        self,
    ) -> typing.Optional["DatastreamConnectionProfilePostgresqlProfile"]:
        return typing.cast(typing.Optional["DatastreamConnectionProfilePostgresqlProfile"], jsii.get(self, "postgresqlProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="privateConnectivityInput")
    def private_connectivity_input(
        self,
    ) -> typing.Optional["DatastreamConnectionProfilePrivateConnectivity"]:
        return typing.cast(typing.Optional["DatastreamConnectionProfilePrivateConnectivity"], jsii.get(self, "privateConnectivityInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlServerProfileInput")
    def sql_server_profile_input(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileSqlServerProfile"]:
        return typing.cast(typing.Optional["DatastreamConnectionProfileSqlServerProfile"], jsii.get(self, "sqlServerProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DatastreamConnectionProfileTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DatastreamConnectionProfileTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionProfileId")
    def connection_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionProfileId"))

    @connection_profile_id.setter
    def connection_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f969eee8b055cb8d89a25e69dfbcfdafbcc3ebfea43ca1aff3940ac3b8705eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5804f9e6b1b385a3e37f8582add91c1d767d01bf74f8429362941f2a130c2819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createWithoutValidation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91037a938adb174f60b4d1ec11f68db70bb6e6fc6681b39eba46b8e46fbca7b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30d608ec4d9ad02d00bc161ea8d01297f843caf5e639a86c1c4bfabeae5b9a56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e57c2587163205b22761f34928ec6f82b04e3fffde89310ee8084db3694903a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467b8b7a449241c9f3bd772826f9aad28045e93ccbba8f189218bc25276bddcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33617e3732ddae32bac5d20ff759f4243f35be1940bc983600e78a1ffc67b762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileBigqueryProfile",
    jsii_struct_bases=[],
    name_mapping={},
)
class DatastreamConnectionProfileBigqueryProfile:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfileBigqueryProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfileBigqueryProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileBigqueryProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb6333376be75ca6d71910fb3f88230a683f0fcc2516c32b80d32cfa2abb9139)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamConnectionProfileBigqueryProfile]:
        return typing.cast(typing.Optional[DatastreamConnectionProfileBigqueryProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamConnectionProfileBigqueryProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__353ad913862a5f5fcfe5dce601ac6b01663ddfd9dd8b5fc6682019f2d9fc368a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileConfig",
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
        "sql_server_profile": "sqlServerProfile",
        "timeouts": "timeouts",
    },
)
class DatastreamConnectionProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bigquery_profile: typing.Optional[typing.Union[DatastreamConnectionProfileBigqueryProfile, typing.Dict[builtins.str, typing.Any]]] = None,
        create_without_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forward_ssh_connectivity: typing.Optional[typing.Union["DatastreamConnectionProfileForwardSshConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_profile: typing.Optional[typing.Union["DatastreamConnectionProfileGcsProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mysql_profile: typing.Optional[typing.Union["DatastreamConnectionProfileMysqlProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle_profile: typing.Optional[typing.Union["DatastreamConnectionProfileOracleProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql_profile: typing.Optional[typing.Union["DatastreamConnectionProfilePostgresqlProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        private_connectivity: typing.Optional[typing.Union["DatastreamConnectionProfilePrivateConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        sql_server_profile: typing.Optional[typing.Union["DatastreamConnectionProfileSqlServerProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DatastreamConnectionProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param connection_profile_id: The connection profile identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#connection_profile_id DatastreamConnectionProfile#connection_profile_id}
        :param display_name: Display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#display_name DatastreamConnectionProfile#display_name}
        :param location: The name of the location this connection profile is located in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#location DatastreamConnectionProfile#location}
        :param bigquery_profile: bigquery_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#bigquery_profile DatastreamConnectionProfile#bigquery_profile}
        :param create_without_validation: Create the connection profile without validating it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#create_without_validation DatastreamConnectionProfile#create_without_validation}
        :param forward_ssh_connectivity: forward_ssh_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#forward_ssh_connectivity DatastreamConnectionProfile#forward_ssh_connectivity}
        :param gcs_profile: gcs_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#gcs_profile DatastreamConnectionProfile#gcs_profile}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#id DatastreamConnectionProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#labels DatastreamConnectionProfile#labels}
        :param mysql_profile: mysql_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#mysql_profile DatastreamConnectionProfile#mysql_profile}
        :param oracle_profile: oracle_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#oracle_profile DatastreamConnectionProfile#oracle_profile}
        :param postgresql_profile: postgresql_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#postgresql_profile DatastreamConnectionProfile#postgresql_profile}
        :param private_connectivity: private_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#private_connectivity DatastreamConnectionProfile#private_connectivity}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#project DatastreamConnectionProfile#project}.
        :param sql_server_profile: sql_server_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#sql_server_profile DatastreamConnectionProfile#sql_server_profile}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#timeouts DatastreamConnectionProfile#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bigquery_profile, dict):
            bigquery_profile = DatastreamConnectionProfileBigqueryProfile(**bigquery_profile)
        if isinstance(forward_ssh_connectivity, dict):
            forward_ssh_connectivity = DatastreamConnectionProfileForwardSshConnectivity(**forward_ssh_connectivity)
        if isinstance(gcs_profile, dict):
            gcs_profile = DatastreamConnectionProfileGcsProfile(**gcs_profile)
        if isinstance(mysql_profile, dict):
            mysql_profile = DatastreamConnectionProfileMysqlProfile(**mysql_profile)
        if isinstance(oracle_profile, dict):
            oracle_profile = DatastreamConnectionProfileOracleProfile(**oracle_profile)
        if isinstance(postgresql_profile, dict):
            postgresql_profile = DatastreamConnectionProfilePostgresqlProfile(**postgresql_profile)
        if isinstance(private_connectivity, dict):
            private_connectivity = DatastreamConnectionProfilePrivateConnectivity(**private_connectivity)
        if isinstance(sql_server_profile, dict):
            sql_server_profile = DatastreamConnectionProfileSqlServerProfile(**sql_server_profile)
        if isinstance(timeouts, dict):
            timeouts = DatastreamConnectionProfileTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487a1a17aaa8d5883afc4619b7b69fdffe73f27fe194eec54b09f744e4810301)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#connection_profile_id DatastreamConnectionProfile#connection_profile_id}
        '''
        result = self._values.get("connection_profile_id")
        assert result is not None, "Required property 'connection_profile_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Display name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#display_name DatastreamConnectionProfile#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The name of the location this connection profile is located in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#location DatastreamConnectionProfile#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bigquery_profile(
        self,
    ) -> typing.Optional[DatastreamConnectionProfileBigqueryProfile]:
        '''bigquery_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#bigquery_profile DatastreamConnectionProfile#bigquery_profile}
        '''
        result = self._values.get("bigquery_profile")
        return typing.cast(typing.Optional[DatastreamConnectionProfileBigqueryProfile], result)

    @builtins.property
    def create_without_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Create the connection profile without validating it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#create_without_validation DatastreamConnectionProfile#create_without_validation}
        '''
        result = self._values.get("create_without_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def forward_ssh_connectivity(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileForwardSshConnectivity"]:
        '''forward_ssh_connectivity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#forward_ssh_connectivity DatastreamConnectionProfile#forward_ssh_connectivity}
        '''
        result = self._values.get("forward_ssh_connectivity")
        return typing.cast(typing.Optional["DatastreamConnectionProfileForwardSshConnectivity"], result)

    @builtins.property
    def gcs_profile(self) -> typing.Optional["DatastreamConnectionProfileGcsProfile"]:
        '''gcs_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#gcs_profile DatastreamConnectionProfile#gcs_profile}
        '''
        result = self._values.get("gcs_profile")
        return typing.cast(typing.Optional["DatastreamConnectionProfileGcsProfile"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#id DatastreamConnectionProfile#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#labels DatastreamConnectionProfile#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mysql_profile(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileMysqlProfile"]:
        '''mysql_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#mysql_profile DatastreamConnectionProfile#mysql_profile}
        '''
        result = self._values.get("mysql_profile")
        return typing.cast(typing.Optional["DatastreamConnectionProfileMysqlProfile"], result)

    @builtins.property
    def oracle_profile(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileOracleProfile"]:
        '''oracle_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#oracle_profile DatastreamConnectionProfile#oracle_profile}
        '''
        result = self._values.get("oracle_profile")
        return typing.cast(typing.Optional["DatastreamConnectionProfileOracleProfile"], result)

    @builtins.property
    def postgresql_profile(
        self,
    ) -> typing.Optional["DatastreamConnectionProfilePostgresqlProfile"]:
        '''postgresql_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#postgresql_profile DatastreamConnectionProfile#postgresql_profile}
        '''
        result = self._values.get("postgresql_profile")
        return typing.cast(typing.Optional["DatastreamConnectionProfilePostgresqlProfile"], result)

    @builtins.property
    def private_connectivity(
        self,
    ) -> typing.Optional["DatastreamConnectionProfilePrivateConnectivity"]:
        '''private_connectivity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#private_connectivity DatastreamConnectionProfile#private_connectivity}
        '''
        result = self._values.get("private_connectivity")
        return typing.cast(typing.Optional["DatastreamConnectionProfilePrivateConnectivity"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#project DatastreamConnectionProfile#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_server_profile(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileSqlServerProfile"]:
        '''sql_server_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#sql_server_profile DatastreamConnectionProfile#sql_server_profile}
        '''
        result = self._values.get("sql_server_profile")
        return typing.cast(typing.Optional["DatastreamConnectionProfileSqlServerProfile"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DatastreamConnectionProfileTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#timeouts DatastreamConnectionProfile#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DatastreamConnectionProfileTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileForwardSshConnectivity",
    jsii_struct_bases=[],
    name_mapping={
        "hostname": "hostname",
        "username": "username",
        "password": "password",
        "port": "port",
        "private_key": "privateKey",
    },
)
class DatastreamConnectionProfileForwardSshConnectivity:
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
        :param hostname: Hostname for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param username: Username for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param password: SSH password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param port: Port for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#port DatastreamConnectionProfile#port}
        :param private_key: SSH private key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#private_key DatastreamConnectionProfile#private_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a3c92f73b582a3b6d54b7ccb714cfa46ea64f54ad7f1b692929d66ddd8517f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for the SSH tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#username DatastreamConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''SSH password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#password DatastreamConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port for the SSH tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#port DatastreamConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''SSH private key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#private_key DatastreamConnectionProfile#private_key}
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfileForwardSshConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfileForwardSshConnectivityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileForwardSshConnectivityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba194138500b01856acd65d8e4379a8d4089a534fc8e563b432d8005b64f504c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d34a5e35ff8249c556d89b37996ab37080e3a85a17a41eff6af4e13829cb1cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7f550e540fda6c573f21714ae49f5f7e2d026d6abd38cfe6a8173f1bed5cfc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba636d204452922bb6a128cc2043b35415e7cda377d0e0f03516b55e6fe56ccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f1ab931c7a5d7b589c479b995878f405a6908b33568da0d0a275f2ead500a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad702533bb77b88711518b25c2584a58c798df8a70163a638e8821ed045a127a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamConnectionProfileForwardSshConnectivity]:
        return typing.cast(typing.Optional[DatastreamConnectionProfileForwardSshConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamConnectionProfileForwardSshConnectivity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a89aecb02c68cebe6ccf7f25be4564534fa015e82a6b296bb6bd706540230c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileGcsProfile",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "root_path": "rootPath"},
)
class DatastreamConnectionProfileGcsProfile:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        root_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: The Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#bucket DatastreamConnectionProfile#bucket}
        :param root_path: The root path inside the Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#root_path DatastreamConnectionProfile#root_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae297457f0043a945afeb469748927856d7514857eaf7dcf9497611c5e065029)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#bucket DatastreamConnectionProfile#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def root_path(self) -> typing.Optional[builtins.str]:
        '''The root path inside the Cloud Storage bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#root_path DatastreamConnectionProfile#root_path}
        '''
        result = self._values.get("root_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfileGcsProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfileGcsProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileGcsProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c202609fde5b39a149ecc8ba3f4ad477585841be808a9d9bb2af014d72f51b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c45fcb6434e7ef947eee9a3633d0a32771d567533b0839e318ea0ef365d8f2bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootPath")
    def root_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootPath"))

    @root_path.setter
    def root_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__089fd3410df160293519f8d04712c0349050fcc4c15909e4a4f9210e1b57fff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DatastreamConnectionProfileGcsProfile]:
        return typing.cast(typing.Optional[DatastreamConnectionProfileGcsProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamConnectionProfileGcsProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f8849c1b7b773d7001a39df3159e73b64270409ce21f311ec42a3d9d3a4eaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileMysqlProfile",
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
class DatastreamConnectionProfileMysqlProfile:
    def __init__(
        self,
        *,
        hostname: builtins.str,
        username: builtins.str,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        secret_manager_stored_password: typing.Optional[builtins.str] = None,
        ssl_config: typing.Optional[typing.Union["DatastreamConnectionProfileMysqlProfileSslConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hostname: Hostname for the MySQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param username: Username for the MySQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param password: Password for the MySQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param port: Port for the MySQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#port DatastreamConnectionProfile#port}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#secret_manager_stored_password DatastreamConnectionProfile#secret_manager_stored_password}
        :param ssl_config: ssl_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#ssl_config DatastreamConnectionProfile#ssl_config}
        '''
        if isinstance(ssl_config, dict):
            ssl_config = DatastreamConnectionProfileMysqlProfileSslConfig(**ssl_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68218584ca8c118a07a5777153ba51c98386912602b535814da5d932850ad63f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for the MySQL connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#username DatastreamConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for the MySQL connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#password DatastreamConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port for the MySQL connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#port DatastreamConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_manager_stored_password(self) -> typing.Optional[builtins.str]:
        '''A reference to a Secret Manager resource name storing the user's password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#secret_manager_stored_password DatastreamConnectionProfile#secret_manager_stored_password}
        '''
        result = self._values.get("secret_manager_stored_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_config(
        self,
    ) -> typing.Optional["DatastreamConnectionProfileMysqlProfileSslConfig"]:
        '''ssl_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#ssl_config DatastreamConnectionProfile#ssl_config}
        '''
        result = self._values.get("ssl_config")
        return typing.cast(typing.Optional["DatastreamConnectionProfileMysqlProfileSslConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfileMysqlProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfileMysqlProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileMysqlProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de69cd24bdc0081e30ed1ad98a5ae96f2a0eb1ac3f93f761c71fd9ee354df024)
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
        :param ca_certificate: PEM-encoded certificate of the CA that signed the source database server's certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#ca_certificate DatastreamConnectionProfile#ca_certificate}
        :param client_certificate: PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' and the 'caCertificate' fields are mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#client_certificate DatastreamConnectionProfile#client_certificate}
        :param client_key: PEM-encoded private key associated with the Client Certificate. If this field is used then the 'client_certificate' and the 'ca_certificate' fields are mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#client_key DatastreamConnectionProfile#client_key}
        '''
        value = DatastreamConnectionProfileMysqlProfileSslConfig(
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
    ) -> "DatastreamConnectionProfileMysqlProfileSslConfigOutputReference":
        return typing.cast("DatastreamConnectionProfileMysqlProfileSslConfigOutputReference", jsii.get(self, "sslConfig"))

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
    ) -> typing.Optional["DatastreamConnectionProfileMysqlProfileSslConfig"]:
        return typing.cast(typing.Optional["DatastreamConnectionProfileMysqlProfileSslConfig"], jsii.get(self, "sslConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__03e669278c26eb9292f29eea3881b254d5eb94bf9153ce03f4c4a33ea798f234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__033051791259232096a37c32d9fcd1da9f60a88756c56b928470778949446d30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__424616460a42a7aad8c351776aad0a81ed951725665ed70ec415d1023faeb7a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredPassword")
    def secret_manager_stored_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretManagerStoredPassword"))

    @secret_manager_stored_password.setter
    def secret_manager_stored_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a548c23fd138ff63293f29507a18f5ce975af2901381b5be34a00a198497fa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretManagerStoredPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c432abdcbe8a5ebe7a68fa510e13e78db33d67d30027e7a21528f72a8b4f7773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamConnectionProfileMysqlProfile]:
        return typing.cast(typing.Optional[DatastreamConnectionProfileMysqlProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamConnectionProfileMysqlProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__124ce79fbff6cb8d0782acbb00b9d0a1600aaff26b8918a626c92a97dcd4abf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileMysqlProfileSslConfig",
    jsii_struct_bases=[],
    name_mapping={
        "ca_certificate": "caCertificate",
        "client_certificate": "clientCertificate",
        "client_key": "clientKey",
    },
)
class DatastreamConnectionProfileMysqlProfileSslConfig:
    def __init__(
        self,
        *,
        ca_certificate: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_certificate: PEM-encoded certificate of the CA that signed the source database server's certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#ca_certificate DatastreamConnectionProfile#ca_certificate}
        :param client_certificate: PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' and the 'caCertificate' fields are mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#client_certificate DatastreamConnectionProfile#client_certificate}
        :param client_key: PEM-encoded private key associated with the Client Certificate. If this field is used then the 'client_certificate' and the 'ca_certificate' fields are mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#client_key DatastreamConnectionProfile#client_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da7e17b258ff2f17f48bfc7eff716c26fe1c85fc96c592b524e056c808a3e4d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#ca_certificate DatastreamConnectionProfile#ca_certificate}
        '''
        result = self._values.get("ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate(self) -> typing.Optional[builtins.str]:
        '''PEM-encoded certificate that will be used by the replica to authenticate against the source database server.

        If this field
        is used then the 'clientKey' and the 'caCertificate' fields are
        mandatory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#client_certificate DatastreamConnectionProfile#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_key(self) -> typing.Optional[builtins.str]:
        '''PEM-encoded private key associated with the Client Certificate.

        If this field is used then the 'client_certificate' and the
        'ca_certificate' fields are mandatory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#client_key DatastreamConnectionProfile#client_key}
        '''
        result = self._values.get("client_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfileMysqlProfileSslConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfileMysqlProfileSslConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileMysqlProfileSslConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2ce57ab7d22c0fedeb5c2b1be077987c4a3397ecaf06082b9d13ad1b6d5a623)
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
            type_hints = typing.get_type_hints(_typecheckingstub__958a5266011168ed1c23ce72f72c989b14a7df838539912eb6f77e8fe3d686df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificate"))

    @client_certificate.setter
    def client_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11eddf71e4a9fe35b50d13a7db09536ec4055b89b1b43256e850c328df70d49e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientKey")
    def client_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientKey"))

    @client_key.setter
    def client_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9074d1c993a570f03c592f3a62cf91bbf5d7f392315e433823ee39b2381308d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamConnectionProfileMysqlProfileSslConfig]:
        return typing.cast(typing.Optional[DatastreamConnectionProfileMysqlProfileSslConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamConnectionProfileMysqlProfileSslConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ab60bb3f42b00bf517d7f2746bbe8d2778e2e84e31c0f0cf21498ce4b0aec1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileOracleProfile",
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
class DatastreamConnectionProfileOracleProfile:
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
        :param database_service: Database for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#database_service DatastreamConnectionProfile#database_service}
        :param hostname: Hostname for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param username: Username for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param connection_attributes: Connection string attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#connection_attributes DatastreamConnectionProfile#connection_attributes}
        :param password: Password for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param port: Port for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#port DatastreamConnectionProfile#port}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#secret_manager_stored_password DatastreamConnectionProfile#secret_manager_stored_password}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ccfc87d8e0440986c365e8f5c06d2f123c4370f34cabd11f77181293c40ba7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#database_service DatastreamConnectionProfile#database_service}
        '''
        result = self._values.get("database_service")
        assert result is not None, "Required property 'database_service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> builtins.str:
        '''Hostname for the Oracle connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for the Oracle connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#username DatastreamConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connection_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Connection string attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#connection_attributes DatastreamConnectionProfile#connection_attributes}
        '''
        result = self._values.get("connection_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for the Oracle connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#password DatastreamConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port for the Oracle connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#port DatastreamConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_manager_stored_password(self) -> typing.Optional[builtins.str]:
        '''A reference to a Secret Manager resource name storing the user's password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#secret_manager_stored_password DatastreamConnectionProfile#secret_manager_stored_password}
        '''
        result = self._values.get("secret_manager_stored_password")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfileOracleProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfileOracleProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileOracleProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22ed39578300414705b68996391a29943b6a5e1b4e4620892d86b1ed1dee9b3b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71a51accd780dd19412fabea172ea71f534619b87266f5020b29ced8c3a1010d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionAttributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseService")
    def database_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseService"))

    @database_service.setter
    def database_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51bb2bd2fb0f671473ab1cac13ae778199b25d2625a0fe685bb1b5e91bc04753)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b5177b75a58661764023119a171faf45a18bbffc4cce47225f4f3ab4003714c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed0de318d1418234978f899106dc3abe304fa41c476fa9457655fed0ae34f837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f59ccc0009ec1045e3455a473c31c0344c6e7812015447423bb0cdc33089a8f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredPassword")
    def secret_manager_stored_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretManagerStoredPassword"))

    @secret_manager_stored_password.setter
    def secret_manager_stored_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2151019c1339fb6af3c149889e7ce8b3df5cef5088c9cc4345abe80b6df6482a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretManagerStoredPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c69f400dbf8d1d931a56328452a5db5daf05f0d5b9760d706127a27bf823ed55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamConnectionProfileOracleProfile]:
        return typing.cast(typing.Optional[DatastreamConnectionProfileOracleProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamConnectionProfileOracleProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd5673ddf374e916be4c421767ebc7ee36ca1305330e36f2510728237da1fa7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfilePostgresqlProfile",
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
class DatastreamConnectionProfilePostgresqlProfile:
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
        :param database: Database for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#database DatastreamConnectionProfile#database}
        :param hostname: Hostname for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param username: Username for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param password: Password for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param port: Port for the PostgreSQL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#port DatastreamConnectionProfile#port}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#secret_manager_stored_password DatastreamConnectionProfile#secret_manager_stored_password}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ccc0af5cc69240a25cf2434ed0cfe099fb38e6121cd425c37f6742e9f28ecaa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#database DatastreamConnectionProfile#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> builtins.str:
        '''Hostname for the PostgreSQL connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for the PostgreSQL connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#username DatastreamConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for the PostgreSQL connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#password DatastreamConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port for the PostgreSQL connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#port DatastreamConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_manager_stored_password(self) -> typing.Optional[builtins.str]:
        '''A reference to a Secret Manager resource name storing the user's password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#secret_manager_stored_password DatastreamConnectionProfile#secret_manager_stored_password}
        '''
        result = self._values.get("secret_manager_stored_password")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfilePostgresqlProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfilePostgresqlProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfilePostgresqlProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__babaa3ebccd0e890f48fc37d363c58ef73457776d4c8aaba5a56d25627140d58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcf5fe248743e7d3b2c882fb0edb9bd26c434fbec1fb274156b40c8abc022fca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b68cd2db19d9144c5e50290f18530edd84a65df63be8d4702da8bc10b84712e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61ff0d24f107d789c031e91062df3a342c831244588ab20dc2c77a0074ef3632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138e31ab097c2856a697cbe4eb3c8cc30fb4f87d43e9f1b90eb9c01258796fa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredPassword")
    def secret_manager_stored_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretManagerStoredPassword"))

    @secret_manager_stored_password.setter
    def secret_manager_stored_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8f03477dc58ce942a570661af7af60912c99fee08be6d2c6f90de3817987b5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretManagerStoredPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25f7fc430d9a9262958189ed4d2e028459a3b73d652e28b9d6282ef4eb085a24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamConnectionProfilePostgresqlProfile]:
        return typing.cast(typing.Optional[DatastreamConnectionProfilePostgresqlProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamConnectionProfilePostgresqlProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edc7adf5d6e8113542541e808dec926baff63aea496a5c8a9a0d8360e2a8cf18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfilePrivateConnectivity",
    jsii_struct_bases=[],
    name_mapping={"private_connection": "privateConnection"},
)
class DatastreamConnectionProfilePrivateConnectivity:
    def __init__(self, *, private_connection: builtins.str) -> None:
        '''
        :param private_connection: A reference to a private connection resource. Format: 'projects/{project}/locations/{location}/privateConnections/{name}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#private_connection DatastreamConnectionProfile#private_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f511a5575005e053baf717c3cbb34489ea07733772538ddc1494d71bd66b33)
            check_type(argname="argument private_connection", value=private_connection, expected_type=type_hints["private_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "private_connection": private_connection,
        }

    @builtins.property
    def private_connection(self) -> builtins.str:
        '''A reference to a private connection resource. Format: 'projects/{project}/locations/{location}/privateConnections/{name}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#private_connection DatastreamConnectionProfile#private_connection}
        '''
        result = self._values.get("private_connection")
        assert result is not None, "Required property 'private_connection' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfilePrivateConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfilePrivateConnectivityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfilePrivateConnectivityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e223e75556bb5340dde5ed4cc08ef3584424d72eb2818514f492cf479c48cc3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__04e4ddb593fb69f35fccaed3b55c2236f902e489c82411a55ad79b32d5b2f3ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateConnection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamConnectionProfilePrivateConnectivity]:
        return typing.cast(typing.Optional[DatastreamConnectionProfilePrivateConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamConnectionProfilePrivateConnectivity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84f5f76d9b58bd56432b1ba45e60bfc88eccb23e59c65d37f3bdd8d944255ce0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileSqlServerProfile",
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
class DatastreamConnectionProfileSqlServerProfile:
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
        :param database: Database for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#database DatastreamConnectionProfile#database}
        :param hostname: Hostname for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        :param username: Username for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#username DatastreamConnectionProfile#username}
        :param password: Password for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#password DatastreamConnectionProfile#password}
        :param port: Port for the SQL Server connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#port DatastreamConnectionProfile#port}
        :param secret_manager_stored_password: A reference to a Secret Manager resource name storing the user's password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#secret_manager_stored_password DatastreamConnectionProfile#secret_manager_stored_password}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5abbcce100d362dd307ca90f609e9cb140af03c4dc1ee984c7447d43e12ca95)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#database DatastreamConnectionProfile#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> builtins.str:
        '''Hostname for the SQL Server connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#hostname DatastreamConnectionProfile#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for the SQL Server connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#username DatastreamConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for the SQL Server connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#password DatastreamConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port for the SQL Server connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#port DatastreamConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_manager_stored_password(self) -> typing.Optional[builtins.str]:
        '''A reference to a Secret Manager resource name storing the user's password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#secret_manager_stored_password DatastreamConnectionProfile#secret_manager_stored_password}
        '''
        result = self._values.get("secret_manager_stored_password")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfileSqlServerProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfileSqlServerProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileSqlServerProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e795c9a4ac02326254f204357353d4c759c0611aee647b60e7bd5829d42c2fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__877cf6a2b6e93a09274e48ae269f15080efdf4e7e3f0bd06c8e17d71b17401b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ac2e0601b9caa8db0436b98edf2cc097167f155491b57aa95f9e9d4a2f43fca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3946b2b7f997141e4afb6dc159d419e7cef09682542bd25e665ac4917b0afe48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f6c5cb5b25abcaa9cf838740d6bccc2e1d4b6abfad935d6209cf336ac6b4012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretManagerStoredPassword")
    def secret_manager_stored_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretManagerStoredPassword"))

    @secret_manager_stored_password.setter
    def secret_manager_stored_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c78346c42c1c7eab7b028a5802c2506effac68ca9b54b7d9005f03512c96a1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretManagerStoredPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb27bb713503a3618c1a5171b32674e4da9813008ba1a3d0a389e799006f5e79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamConnectionProfileSqlServerProfile]:
        return typing.cast(typing.Optional[DatastreamConnectionProfileSqlServerProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamConnectionProfileSqlServerProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975dfae2e74f2d8d2df9a6d52e922a030538f5a3af4759d851cb280e6cf21f60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DatastreamConnectionProfileTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#create DatastreamConnectionProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#delete DatastreamConnectionProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#update DatastreamConnectionProfile#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f743875a2b79d53201c22d2bb5fab589fd25a4ad34dbcc68fa1abaedc9e4b2d0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#create DatastreamConnectionProfile#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#delete DatastreamConnectionProfile#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_connection_profile#update DatastreamConnectionProfile#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamConnectionProfileTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamConnectionProfileTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamConnectionProfile.DatastreamConnectionProfileTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__403ae6956be740c070551d7ca907f9d23f80938e35a35440b31f17db5c6f0ce9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ae90dbb8ca32c41d658bdaee4329474de1854c1b2e1302a901c05bcaee9a746)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a3c1fe0978e82ec46bb33c8c9c9d68f9a706e1eafd48a6c1c5e7507bded4409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05930684bab419ac49ee0ca44dd66f339e7d0ee3d33079d3dc070e1c0e130890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamConnectionProfileTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamConnectionProfileTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamConnectionProfileTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b30dbbe60fade040baed4d064db06a92271d2ea6dd11ec93b1a29b4f8a62eaba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DatastreamConnectionProfile",
    "DatastreamConnectionProfileBigqueryProfile",
    "DatastreamConnectionProfileBigqueryProfileOutputReference",
    "DatastreamConnectionProfileConfig",
    "DatastreamConnectionProfileForwardSshConnectivity",
    "DatastreamConnectionProfileForwardSshConnectivityOutputReference",
    "DatastreamConnectionProfileGcsProfile",
    "DatastreamConnectionProfileGcsProfileOutputReference",
    "DatastreamConnectionProfileMysqlProfile",
    "DatastreamConnectionProfileMysqlProfileOutputReference",
    "DatastreamConnectionProfileMysqlProfileSslConfig",
    "DatastreamConnectionProfileMysqlProfileSslConfigOutputReference",
    "DatastreamConnectionProfileOracleProfile",
    "DatastreamConnectionProfileOracleProfileOutputReference",
    "DatastreamConnectionProfilePostgresqlProfile",
    "DatastreamConnectionProfilePostgresqlProfileOutputReference",
    "DatastreamConnectionProfilePrivateConnectivity",
    "DatastreamConnectionProfilePrivateConnectivityOutputReference",
    "DatastreamConnectionProfileSqlServerProfile",
    "DatastreamConnectionProfileSqlServerProfileOutputReference",
    "DatastreamConnectionProfileTimeouts",
    "DatastreamConnectionProfileTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c561713e5931b76475298816158f7084a2e57a9756562dfade012aca01f69516(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    connection_profile_id: builtins.str,
    display_name: builtins.str,
    location: builtins.str,
    bigquery_profile: typing.Optional[typing.Union[DatastreamConnectionProfileBigqueryProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    create_without_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forward_ssh_connectivity: typing.Optional[typing.Union[DatastreamConnectionProfileForwardSshConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs_profile: typing.Optional[typing.Union[DatastreamConnectionProfileGcsProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mysql_profile: typing.Optional[typing.Union[DatastreamConnectionProfileMysqlProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    oracle_profile: typing.Optional[typing.Union[DatastreamConnectionProfileOracleProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    postgresql_profile: typing.Optional[typing.Union[DatastreamConnectionProfilePostgresqlProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    private_connectivity: typing.Optional[typing.Union[DatastreamConnectionProfilePrivateConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    sql_server_profile: typing.Optional[typing.Union[DatastreamConnectionProfileSqlServerProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DatastreamConnectionProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__edc09f15ae32ab928a3477d3359deddfaf3c0e76f948c57455bdad119c024ec1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f969eee8b055cb8d89a25e69dfbcfdafbcc3ebfea43ca1aff3940ac3b8705eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5804f9e6b1b385a3e37f8582add91c1d767d01bf74f8429362941f2a130c2819(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91037a938adb174f60b4d1ec11f68db70bb6e6fc6681b39eba46b8e46fbca7b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30d608ec4d9ad02d00bc161ea8d01297f843caf5e639a86c1c4bfabeae5b9a56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e57c2587163205b22761f34928ec6f82b04e3fffde89310ee8084db3694903a0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467b8b7a449241c9f3bd772826f9aad28045e93ccbba8f189218bc25276bddcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33617e3732ddae32bac5d20ff759f4243f35be1940bc983600e78a1ffc67b762(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb6333376be75ca6d71910fb3f88230a683f0fcc2516c32b80d32cfa2abb9139(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353ad913862a5f5fcfe5dce601ac6b01663ddfd9dd8b5fc6682019f2d9fc368a(
    value: typing.Optional[DatastreamConnectionProfileBigqueryProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487a1a17aaa8d5883afc4619b7b69fdffe73f27fe194eec54b09f744e4810301(
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
    bigquery_profile: typing.Optional[typing.Union[DatastreamConnectionProfileBigqueryProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    create_without_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forward_ssh_connectivity: typing.Optional[typing.Union[DatastreamConnectionProfileForwardSshConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs_profile: typing.Optional[typing.Union[DatastreamConnectionProfileGcsProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mysql_profile: typing.Optional[typing.Union[DatastreamConnectionProfileMysqlProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    oracle_profile: typing.Optional[typing.Union[DatastreamConnectionProfileOracleProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    postgresql_profile: typing.Optional[typing.Union[DatastreamConnectionProfilePostgresqlProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    private_connectivity: typing.Optional[typing.Union[DatastreamConnectionProfilePrivateConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    sql_server_profile: typing.Optional[typing.Union[DatastreamConnectionProfileSqlServerProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DatastreamConnectionProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a3c92f73b582a3b6d54b7ccb714cfa46ea64f54ad7f1b692929d66ddd8517f(
    *,
    hostname: builtins.str,
    username: builtins.str,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    private_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba194138500b01856acd65d8e4379a8d4089a534fc8e563b432d8005b64f504c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d34a5e35ff8249c556d89b37996ab37080e3a85a17a41eff6af4e13829cb1cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f550e540fda6c573f21714ae49f5f7e2d026d6abd38cfe6a8173f1bed5cfc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba636d204452922bb6a128cc2043b35415e7cda377d0e0f03516b55e6fe56ccd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f1ab931c7a5d7b589c479b995878f405a6908b33568da0d0a275f2ead500a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad702533bb77b88711518b25c2584a58c798df8a70163a638e8821ed045a127a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a89aecb02c68cebe6ccf7f25be4564534fa015e82a6b296bb6bd706540230c(
    value: typing.Optional[DatastreamConnectionProfileForwardSshConnectivity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae297457f0043a945afeb469748927856d7514857eaf7dcf9497611c5e065029(
    *,
    bucket: builtins.str,
    root_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c202609fde5b39a149ecc8ba3f4ad477585841be808a9d9bb2af014d72f51b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45fcb6434e7ef947eee9a3633d0a32771d567533b0839e318ea0ef365d8f2bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__089fd3410df160293519f8d04712c0349050fcc4c15909e4a4f9210e1b57fff2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f8849c1b7b773d7001a39df3159e73b64270409ce21f311ec42a3d9d3a4eaf(
    value: typing.Optional[DatastreamConnectionProfileGcsProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68218584ca8c118a07a5777153ba51c98386912602b535814da5d932850ad63f(
    *,
    hostname: builtins.str,
    username: builtins.str,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    secret_manager_stored_password: typing.Optional[builtins.str] = None,
    ssl_config: typing.Optional[typing.Union[DatastreamConnectionProfileMysqlProfileSslConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de69cd24bdc0081e30ed1ad98a5ae96f2a0eb1ac3f93f761c71fd9ee354df024(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e669278c26eb9292f29eea3881b254d5eb94bf9153ce03f4c4a33ea798f234(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__033051791259232096a37c32d9fcd1da9f60a88756c56b928470778949446d30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424616460a42a7aad8c351776aad0a81ed951725665ed70ec415d1023faeb7a6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a548c23fd138ff63293f29507a18f5ce975af2901381b5be34a00a198497fa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c432abdcbe8a5ebe7a68fa510e13e78db33d67d30027e7a21528f72a8b4f7773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__124ce79fbff6cb8d0782acbb00b9d0a1600aaff26b8918a626c92a97dcd4abf0(
    value: typing.Optional[DatastreamConnectionProfileMysqlProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da7e17b258ff2f17f48bfc7eff716c26fe1c85fc96c592b524e056c808a3e4d(
    *,
    ca_certificate: typing.Optional[builtins.str] = None,
    client_certificate: typing.Optional[builtins.str] = None,
    client_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ce57ab7d22c0fedeb5c2b1be077987c4a3397ecaf06082b9d13ad1b6d5a623(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958a5266011168ed1c23ce72f72c989b14a7df838539912eb6f77e8fe3d686df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11eddf71e4a9fe35b50d13a7db09536ec4055b89b1b43256e850c328df70d49e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9074d1c993a570f03c592f3a62cf91bbf5d7f392315e433823ee39b2381308d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab60bb3f42b00bf517d7f2746bbe8d2778e2e84e31c0f0cf21498ce4b0aec1f(
    value: typing.Optional[DatastreamConnectionProfileMysqlProfileSslConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ccfc87d8e0440986c365e8f5c06d2f123c4370f34cabd11f77181293c40ba7(
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

def _typecheckingstub__22ed39578300414705b68996391a29943b6a5e1b4e4620892d86b1ed1dee9b3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a51accd780dd19412fabea172ea71f534619b87266f5020b29ced8c3a1010d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51bb2bd2fb0f671473ab1cac13ae778199b25d2625a0fe685bb1b5e91bc04753(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5177b75a58661764023119a171faf45a18bbffc4cce47225f4f3ab4003714c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed0de318d1418234978f899106dc3abe304fa41c476fa9457655fed0ae34f837(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59ccc0009ec1045e3455a473c31c0344c6e7812015447423bb0cdc33089a8f8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2151019c1339fb6af3c149889e7ce8b3df5cef5088c9cc4345abe80b6df6482a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69f400dbf8d1d931a56328452a5db5daf05f0d5b9760d706127a27bf823ed55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5673ddf374e916be4c421767ebc7ee36ca1305330e36f2510728237da1fa7c(
    value: typing.Optional[DatastreamConnectionProfileOracleProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ccc0af5cc69240a25cf2434ed0cfe099fb38e6121cd425c37f6742e9f28ecaa(
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

def _typecheckingstub__babaa3ebccd0e890f48fc37d363c58ef73457776d4c8aaba5a56d25627140d58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf5fe248743e7d3b2c882fb0edb9bd26c434fbec1fb274156b40c8abc022fca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68cd2db19d9144c5e50290f18530edd84a65df63be8d4702da8bc10b84712e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ff0d24f107d789c031e91062df3a342c831244588ab20dc2c77a0074ef3632(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138e31ab097c2856a697cbe4eb3c8cc30fb4f87d43e9f1b90eb9c01258796fa5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8f03477dc58ce942a570661af7af60912c99fee08be6d2c6f90de3817987b5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f7fc430d9a9262958189ed4d2e028459a3b73d652e28b9d6282ef4eb085a24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edc7adf5d6e8113542541e808dec926baff63aea496a5c8a9a0d8360e2a8cf18(
    value: typing.Optional[DatastreamConnectionProfilePostgresqlProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f511a5575005e053baf717c3cbb34489ea07733772538ddc1494d71bd66b33(
    *,
    private_connection: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e223e75556bb5340dde5ed4cc08ef3584424d72eb2818514f492cf479c48cc3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e4ddb593fb69f35fccaed3b55c2236f902e489c82411a55ad79b32d5b2f3ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f5f76d9b58bd56432b1ba45e60bfc88eccb23e59c65d37f3bdd8d944255ce0(
    value: typing.Optional[DatastreamConnectionProfilePrivateConnectivity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5abbcce100d362dd307ca90f609e9cb140af03c4dc1ee984c7447d43e12ca95(
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

def _typecheckingstub__1e795c9a4ac02326254f204357353d4c759c0611aee647b60e7bd5829d42c2fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__877cf6a2b6e93a09274e48ae269f15080efdf4e7e3f0bd06c8e17d71b17401b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ac2e0601b9caa8db0436b98edf2cc097167f155491b57aa95f9e9d4a2f43fca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3946b2b7f997141e4afb6dc159d419e7cef09682542bd25e665ac4917b0afe48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f6c5cb5b25abcaa9cf838740d6bccc2e1d4b6abfad935d6209cf336ac6b4012(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c78346c42c1c7eab7b028a5802c2506effac68ca9b54b7d9005f03512c96a1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb27bb713503a3618c1a5171b32674e4da9813008ba1a3d0a389e799006f5e79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975dfae2e74f2d8d2df9a6d52e922a030538f5a3af4759d851cb280e6cf21f60(
    value: typing.Optional[DatastreamConnectionProfileSqlServerProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f743875a2b79d53201c22d2bb5fab589fd25a4ad34dbcc68fa1abaedc9e4b2d0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__403ae6956be740c070551d7ca907f9d23f80938e35a35440b31f17db5c6f0ce9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae90dbb8ca32c41d658bdaee4329474de1854c1b2e1302a901c05bcaee9a746(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a3c1fe0978e82ec46bb33c8c9c9d68f9a706e1eafd48a6c1c5e7507bded4409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05930684bab419ac49ee0ca44dd66f339e7d0ee3d33079d3dc070e1c0e130890(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30dbbe60fade040baed4d064db06a92271d2ea6dd11ec93b1a29b4f8a62eaba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamConnectionProfileTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
